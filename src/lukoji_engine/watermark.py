"""Filigrane LUKOJI : placement sûr, couleur adaptée au fond, incrustation sans déformation.

Étapes :
  1. le logo est rendu à sa taille finale EXACTE (ratio de la source officielle) : FFmpeg ne le
     redimensionne jamais, il est seulement superposé -> aucune déformation possible ;
  2. les positions candidates sont les coins de la zone sûre du profil (intersection des
     plateformes ciblées et des aperçus recadrés) ; celles qui touchent une zone réservée
     (sous-titres, texte clé, visage déclaré, filigrane YouTube…) sont exclues ;
  3. parmi les candidates restantes, on retient la zone la plus « calme » (densité de contours
     la plus faible sur toute la durée), pondérée par l'ordre de préférence ;
  4. la luminance sous le logo est suivie dans le temps : logo blanc sur fond sombre, noir sur
     fond clair, avec hystérésis et durée minimale de segment (pas de clignotement) ;
  5. la signature de fin (optionnelle) est enchaînée par un fondu ; le filigrane n'y figure pas.
Un fichier JSON « sidecar » décrit tout le rendu ; il sert au contrôle qualité.
"""
from __future__ import annotations

import json
import shlex
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image

from . import signature as sigmod
from .assets import LogoImage, logo_image, sha256_file, verify_manifest
from .config import load_config
from .db import Database
from .geometry import Profile, Rect, anchor_box, get_profile
from .log import get_logger
from .media import luminance, normalize_filter, probe, read_region_series, run_ffmpeg
from .paths import ensure_dir, rel

log = get_logger("watermark")


@dataclass
class Segment:
    start: float
    end: float
    color: str              # "white" | "black"
    bg_luma: float          # luminance moyenne du fond sous le logo
    contrast: float         # |luminance logo - luminance fond|


@dataclass
class Candidate:
    anchor: str
    box: list[int]
    rejected: str | None = None
    busyness: float | None = None
    score: float | None = None
    occlusion: dict | None = None


@dataclass
class WatermarkPlan:
    profile: str
    canvas: list[int]
    variant: str
    box: list[int]
    anchor: str
    opacity: float
    fade_in: float
    segments: list[Segment]
    candidates: list[Candidate]
    avoid: list[list[int]]
    clear: bool = True                          # False = aucune position dégagée -> validation humaine
    logos: dict = field(default_factory=dict)   # couleur -> {path, sha256, box_w, box_h, pad, source_aspect}


def _wcfg() -> dict:
    return load_config().brand["watermark"]


def _logo_size(profile: Profile, variant: str) -> dict:
    layout = _wcfg()["layouts"][profile.orientation]
    return {"width": layout["lockup_width"]} if variant == "lockup" else {"height": layout["symbole_height"]}


def _make_logo(variant: str, color: str, profile: Profile, db: Database | None) -> LogoImage:
    w = _wcfg()
    shadow = w["shadow"] == "on" or (w["shadow"] == "auto" and color == "white")
    return logo_image(variant, color, shadow=shadow, shadow_opacity=w["shadow_opacity"], db=db,
                      **_logo_size(profile, variant))


def edge_density(series: np.ndarray) -> np.ndarray:
    """Densité de contours par image (0–1) : proxy des textes, visages et détails à ne pas couvrir."""
    if len(series) == 0:
        return np.zeros(0)
    lum = luminance(series)
    gx = np.abs(np.diff(lum, axis=2)).mean(axis=(1, 2))
    gy = np.abs(np.diff(lum, axis=1)).mean(axis=(1, 2))
    return gx + gy


def occlusion_profile(src: Path, vf: str, box: Rect, canvas: Rect, duration: float, start: float = 0.0) -> dict:
    """Mesure, sur toute la durée, si la zone `box` (+12 px) contient du détail."""
    w = _wcfg()
    step, thr = w["occlusion_step"], w["occlusion_threshold"]
    region = box.expand(12).intersect(canvas)
    g = edge_density(read_region_series(src, (region.x, region.y, region.w, region.h), step, duration,
                                        vf=vf, start=start))
    busy = g > thr
    spans, i = [], 0
    while i < len(busy):
        if busy[i]:
            j = i
            while j + 1 < len(busy) and busy[j + 1]:
                j += 1
            spans.append([round(i * step, 2), round((j + 1) * step, 2)])
            i = j + 1
        else:
            i += 1
    return {"max": round(float(g.max()) if len(g) else 0.0, 5),
            "p95": round(float(np.percentile(g, 95)) if len(g) else 0.0, 5),
            "occluded_fraction": round(float(busy.mean()) if len(busy) else 0.0, 4),
            "occluded_spans": spans, "threshold": thr}


def choose_placement(src: Path, vf: str, profile: Profile, logo_w: int, logo_h: int, duration: float,
                     avoid: list[Rect], anchors: list[str] | None = None,
                     start: float = 0.0) -> tuple[Rect, str, list[Candidate], bool]:
    """Choisit le coin dégagé préféré. Retourne (boîte, ancre, candidats, dégagée?)."""
    w = _wcfg()
    anchors = anchors or w["layouts"][profile.orientation]["anchors"]
    pad = w["avoid_padding"]
    forbidden = [r.expand(pad) for r in avoid] + list(profile.reserved)
    cands: list[Candidate] = []
    for rank, anchor in enumerate(anchors):
        box = anchor_box(anchor, profile.safe, logo_w, logo_h)
        c = Candidate(anchor, box.as_list())
        cands.append(c)
        if not profile.safe.contains(box):
            c.rejected = "hors zone sûre"
            continue
        hit = next((f for f in forbidden if box.intersects(f)), None)
        if hit:
            c.rejected = f"chevauche une zone réservée {hit.as_list()}"
            continue
        occ = occlusion_profile(src, vf, box, profile.canvas, duration, start)
        c.busyness = occ["p95"]
        c.occlusion = occ
        # Préférence : dégagée d'abord, puis ordre déclaré, puis calme.
        c.score = round(occ["occluded_fraction"] * 100 + rank * 0.01 + occ["p95"], 6)
        if occ["occluded_fraction"] > 0:
            c.rejected = f"masquerait du contenu pendant {occ['occluded_spans']}"
    ok = [c for c in cands if c.rejected is None]
    if ok:
        best = min(ok, key=lambda c: c.score)
        return Rect(*best.box), best.anchor, cands, True
    measured = [c for c in cands if c.score is not None]
    if not measured:
        raise RuntimeError("aucune position de filigrane valide : zones réservées trop étendues "
                           f"({[c.rejected for c in cands]})")
    best = min(measured, key=lambda c: c.score)
    log.warning("aucune position entièrement dégagée : validation humaine requise",
                extra={"anchor": best.anchor, "spans": best.occlusion["occluded_spans"]})
    return Rect(*best.box), best.anchor, cands, False


def color_segments(src: Path, vf: str, box: Rect, mask: np.ndarray, duration: float, mode: str,
                   start: float = 0.0) -> list[Segment]:
    """Segmente la durée selon la luminance du fond SOUS les tracés du logo."""
    w = _wcfg()
    step = w["analysis_step"]
    series = read_region_series(src, (box.x, box.y, box.w, box.h), step, duration, vf=vf, start=start)
    weights = mask / max(mask.sum(), 1e-6)
    lum = np.array([(luminance(f) * weights).sum() for f in series]) if len(series) else np.array([0.0])
    if mode in ("white", "black"):
        states = [mode] * len(lum)
    else:
        states, cur = [], None
        for v in lum:
            if cur is None:
                cur = "black" if v >= (w["light_threshold"] + w["dark_threshold"]) / 2 else "white"
            elif cur == "white" and v > w["light_threshold"]:
                cur = "black"
            elif cur == "black" and v < w["dark_threshold"]:
                cur = "white"
            states.append(cur)
    # Regroupement en segments.
    segs: list[list] = []
    for i, s in enumerate(states):
        t0 = i * step
        if segs and segs[-1][2] == s:
            segs[-1][1] = t0 + step
        else:
            segs.append([t0, t0 + step, s, i])
    # Fusion des segments trop courts dans le voisin précédent (ou suivant pour le premier).
    min_seg = w["min_segment"]
    changed = True
    while changed and len(segs) > 1:
        changed = False
        for i, sg in enumerate(segs):
            if sg[1] - sg[0] < min_seg:
                j = i - 1 if i > 0 else i + 1
                lo, hi = min(segs[i][0], segs[j][0]), max(segs[i][1], segs[j][1])
                segs[j][0], segs[j][1] = lo, hi
                segs.pop(i)
                changed = True
                break
        # recoller les voisins de même couleur
        k = 0
        while k < len(segs) - 1:
            if segs[k][2] == segs[k + 1][2]:
                segs[k][1] = segs[k + 1][1]
                segs.pop(k + 1)
            else:
                k += 1
    segs[0][0] = 0.0
    segs[-1][1] = duration
    out = []
    for s0, s1, color, _ in segs:
        i0, i1 = int(s0 / step), max(int(s0 / step) + 1, int(round(s1 / step)))
        bg = float(lum[i0:i1].mean()) if len(lum[i0:i1]) else float(lum.mean())
        logo_l = 1.0 if color == "white" else 0.0434  # #0B0B0B
        out.append(Segment(round(s0, 3), round(s1, 3), color, round(bg, 3), round(abs(logo_l - bg), 3)))
    return out


def _enable_expr(segments: list[Segment], color: str) -> str | None:
    parts = [f"gte(t,{s.start:.3f})*lt(t,{s.end:.3f})" for s in segments if s.color == color]
    return "+".join(parts) if parts else None


def apply(input_path: str | Path, output_path: str | Path, *, profile_name: str, kind: str = "short",
          variant: str | None = None, color_mode: str | None = None, opacity: float | None = None,
          signature_preset: str | None = None, source_in: float = 0.0, source_out: float | None = None,
          avoid: list[Rect] | None = None, anchors: list[str] | None = None,
          content_slug: str | None = None, title: str | None = None, db: Database | None = None) -> dict:
    problems = verify_manifest()
    if problems:
        raise RuntimeError(f"kit de marque non intègre : {problems}")
    cfg = load_config()
    wcfg = _wcfg()
    src = Path(input_path).resolve()
    out = Path(output_path).resolve()
    ensure_dir(out.parent)
    profile = get_profile(profile_name)
    variant = variant or wcfg["variant"]
    color_mode = color_mode or wcfg["color_mode"]
    opacity = float(opacity if opacity is not None else wcfg["opacity"])
    if not 0.2 <= opacity <= 1.0:
        raise ValueError("opacité attendue entre 0.2 et 1.0")
    avoid = avoid or []

    pin = probe(src)
    end = min(source_out, pin.duration) if source_out else pin.duration
    main_dur = round(end - source_in, 3)
    if main_dur <= 0:
        raise ValueError("durée utile nulle (vérifier --source-in / --source-out)")
    vf = normalize_filter(pin.width, pin.height, profile.width, profile.height, profile.fps)

    # 1) taille du logo (blanc de référence pour la géométrie)
    ref = _make_logo(variant, "white", profile, db)
    # 2) placement
    box, anchor, cands, clear = choose_placement(src, vf, profile, ref.box_w, ref.box_h, main_dur, avoid,
                                                 anchors, start=source_in)
    # 3) couleur par segment, mesurée sous les tracés du logo
    with Image.open(ref.path) as im:
        a = np.asarray(im.getchannel("A"), np.float32) / 255.0
    mask = a[ref.pad: ref.pad + ref.box_h, ref.pad: ref.pad + ref.box_w]
    mask = np.where(mask > 0.5, 1.0, 0.0)
    segments = color_segments(src, vf, box, mask, main_dur, color_mode, start=source_in)
    logos = {"white": ref} if any(s.color == "white" for s in segments) else {}
    if any(s.color == "black" for s in segments):
        logos["black"] = _make_logo(variant, "black", profile, db)

    # 4) signature
    preset = sigmod.preset_for(kind, signature_preset)
    sign, why = sigmod.should_sign(preset, main_dur)
    sig = sigmod.render(profile, preset, db=db) if sign else None
    scfg = cfg.brand["signature"]
    xf = scfg["transition"] if sig else 0.0
    total = round(main_dur + (sig.duration - xf if sig else 0.0), 3)

    # 5) graphe FFmpeg
    enc = cfg.engine["encode"]
    fade = wcfg["fade_in"]
    args: list[str] = ["-ss", f"{source_in:.3f}", "-t", f"{main_dur:.3f}", "-i", str(src)]
    filters = [f"[0:v]{vf},format=yuv444p[base]"]
    last = "base"
    for idx, (color, logo) in enumerate(logos.items(), start=1):
        args += ["-loop", "1", "-framerate", str(profile.fps), "-t", f"{main_dur:.3f}", "-i", str(logo.path)]
        chain = f"[{idx}:v]format=rgba,colorchannelmixer=aa={opacity:.3f}"
        if segments[0].color == color and fade > 0:
            chain += f",fade=t=in:st=0:d={fade}:alpha=1"
        filters.append(chain + f"[lg{idx}]")
        expr = _enable_expr(segments, color)
        filters.append(f"[{last}][lg{idx}]overlay=x={box.x - logo.pad}:y={box.y - logo.pad}:format=yuv444"
                       f":eof_action=pass:enable='{expr}'[ov{idx}]")
        last = f"ov{idx}"
    filters.append(f"[{last}]format=yuv420p,settb=AVTB,fps={profile.fps}[main]")
    vout = "main"
    if sig:
        sidx = len(logos) + 1
        args += ["-i", str(sig.path)]
        filters.append(f"[{sidx}:v]format=yuv420p,setsar=1,settb=AVTB,fps={profile.fps}[sig]")
        filters.append(f"[main][sig]xfade=transition=fade:duration={xf}:offset={main_dur - xf:.3f}[vx]")
        vout = "vx"
    if pin.has_audio:
        afo = scfg["audio_fade_out"] if sig else 0.0
        achain = f"[0:a]aresample={enc['audio_rate']},aformat=channel_layouts=stereo"
        if afo:
            achain += f",afade=t=out:st={max(0.0, main_dur - afo):.3f}:d={afo}"
        filters.append(achain + f",apad=whole_dur={total}[aout]")
    else:
        filters.append(f"anullsrc=r={enc['audio_rate']}:cl=stereo,atrim=0:{total}[aout]")
    gop = int(enc["gop_seconds"] * profile.fps)
    args += [
        "-filter_complex", ";".join(filters), "-map", f"[{vout}]", "-map", "[aout]",
        "-c:v", enc["video_codec"], "-preset", enc["preset"], "-crf", str(enc["crf"]),
        "-profile:v", enc["profile"], "-level:v", str(enc["level"]), "-pix_fmt", enc["pix_fmt"],
        "-g", str(gop), "-r", str(profile.fps),
        "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-c:a", enc["audio_codec"], "-b:a", enc["audio_bitrate"], "-ar", str(enc["audio_rate"]),
        "-ac", str(enc["audio_channels"]), "-t", f"{total:.3f}",
    ]
    if enc.get("faststart", True):
        args += ["-movflags", "+faststart"]
    args.append(str(out))
    log.info("encodage", extra={"output": rel(out), "profile": profile.name, "segments": len(segments)})
    run_ffmpeg(args, desc="incrustation du filigrane")

    plan = WatermarkPlan(
        profile=profile.name, canvas=[profile.width, profile.height], variant=variant, box=box.as_list(),
        anchor=anchor, opacity=opacity, fade_in=fade, segments=segments, candidates=cands,
        avoid=[r.as_list() for r in avoid], clear=clear,
        logos={c: {"path": rel(l.path), "sha256": l.sha256, "box_w": l.box_w, "box_h": l.box_h, "pad": l.pad,
                   "source_key": l.source_key, "source_aspect": l.source_aspect} for c, l in logos.items()},
    )
    sidecar = {
        "engine": "lukoji-media-engine", "kind": kind, "input": str(src), "input_sha256": sha256_file(src),
        "output": str(out), "source_in": source_in, "source_out": end, "main_duration": main_dur,
        "total_duration": total, "normalize_filter": vf, "profile": profile.name,
        "profile_members": list(profile.members), "safe_rect": profile.safe.as_list(),
        "watermark": asdict(plan),
        "signature": ({"preset": sig.preset, "path": rel(sig.path), "duration": sig.duration,
                       "start": round(main_dur - xf, 3), "transition": xf, "last_frame": rel(sig.last_frame),
                       "content_box": sig.spec["content_box"]}
                      if sig else {"preset": preset, "skipped": why}),
        "encode": enc, "ffmpeg": shlex.join(["ffmpeg", *args]),
    }
    Path(str(out) + ".json").write_text(json.dumps(sidecar, ensure_ascii=False, indent=2, default=str))

    if db:
        slug = content_slug or out.stem
        content = db.get_or_create_content(slug, kind, title or slug)
        pout = probe(out)
        render_id = db.add_render(content_id=content["id"], path=rel(out), sha256=sha256_file(out),
                                  profile=profile.name, width=pout.width, height=pout.height, fps=pout.fps,
                                  duration=pout.duration, params=sidecar)
        sidecar["render_id"] = render_id
        Path(str(out) + ".json").write_text(json.dumps(sidecar, ensure_ascii=False, indent=2, default=str))
    return sidecar
