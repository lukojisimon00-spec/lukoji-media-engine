"""Contrôle qualité automatisé des rendus vidéo.

Chaque contrôle renvoie {name, passed, severity, value, expected, detail}.
Sévérités : « bloquant » (le rendu ne doit pas sortir), « avertissement », « info ».

Le contrôle du filigrane est le plus strict : à partir du sidecar, on reconstruit l'image ATTENDUE
(source normalisée + logo composité à l'opacité prévue) et on la compare au rendu réel. Une
corrélation élevée sur la zone du logo prouve à la fois sa présence, sa position exacte (le pic de
corrélation doit être au décalage 0) et l'absence de déformation (la forme doit coïncider).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .assets import original_path, sha256_file, verify_manifest
from .config import load_config
from .geometry import Rect, get_profile
from .media import luminance, moov_before_mdat, probe, read_frame, run_ffmpeg
from .paths import resolve

BLOQUANT, AVERT, INFO = "bloquant", "avertissement", "info"


def _r(name, passed, severity=BLOQUANT, value=None, expected=None, detail=None) -> dict:
    return {"name": name, "passed": bool(passed), "severity": severity,
            "value": value, "expected": expected, "detail": detail}


def load_sidecar(video: str | Path) -> dict | None:
    p = Path(str(video) + ".json")
    return json.loads(p.read_text()) if p.exists() else None


# ---------------------------------------------------------------------------
# Contrôles techniques
# ---------------------------------------------------------------------------
def technical_checks(video: Path, profile_name: str, expected_duration: float | None) -> list[dict]:
    res: list[dict] = []
    res.append(_r("fichier_present", video.exists() and video.stat().st_size > 0, value=str(video)))
    if not res[-1]["passed"]:
        return res
    p = probe(video)
    prof = get_profile(profile_name)
    enc = load_config().engine["encode"]
    res += [
        _r("conteneur_mp4", "mp4" in p.format_name, value=p.format_name, expected="mp4"),
        _r("dimensions", (p.width, p.height) == (prof.width, prof.height),
           value=f"{p.width}x{p.height}", expected=f"{prof.width}x{prof.height}"),
        _r("ratio", abs(p.ratio - prof.ratio) < 1e-3, value=round(p.ratio, 4), expected=round(prof.ratio, 4)),
        _r("pixels_carres", p.sar in ("1:1", "0:1", "N/A"), value=p.sar, expected="1:1"),
        _r("codec_video", p.vcodec == "h264", value=p.vcodec, expected="h264"),
        _r("profil_h264", p.vprofile.lower() == enc["profile"], AVERT, p.vprofile, enc["profile"]),
        _r("format_pixel", p.pix_fmt == enc["pix_fmt"], value=p.pix_fmt, expected=enc["pix_fmt"]),
        _r("framerate", abs(p.fps - prof.fps) < 0.01 and abs(p.avg_fps - prof.fps) < 0.05,
           value=f"r={p.fps:.3f} avg={p.avg_fps:.3f}", expected=prof.fps),
        _r("audio_present", p.has_audio, value=p.acodec, expected="aac"),
        _r("codec_audio", p.acodec == "aac", value=p.acodec, expected="aac"),
        _r("audio_48k_stereo", p.sample_rate == enc["audio_rate"] and p.channels == 2, AVERT,
           f"{p.sample_rate} Hz / {p.channels} canaux", f"{enc['audio_rate']} Hz / 2 canaux"),
        _r("faststart", moov_before_mdat(video) is True, AVERT, moov_before_mdat(video), True,
           "moov avant mdat : lecture progressive sur le web"),
    ]
    if expected_duration is not None:
        res.append(_r("duree", abs(p.duration - expected_duration) <= 0.1,
                      value=round(p.duration, 3), expected=f"{expected_duration} ± 0.1 s"))
    if p.nb_frames and p.duration:
        expected_frames = round(p.duration * prof.fps)
        res.append(_r("nombre_images", abs(p.nb_frames - expected_frames) <= 2, AVERT, p.nb_frames, expected_frames))
    kbps = p.bit_rate / 1000 if p.bit_rate else 0
    # Encodage à qualité constante (CRF) : le débit dépend du contenu, il est consigné pour information.
    res.append(_r("debit", kbps > 0, INFO, f"{kbps:.0f} kb/s", "variable (CRF)"))
    return res


def audio_checks(video: Path, main_end: float) -> list[dict]:
    """Mesure EBU R128 (info) + crête et silence (avertissements). Le mixage est traité en phase 3."""
    log = run_ffmpeg(["-i", str(video), "-t", f"{main_end:.3f}", "-map", "0:a:0",
                      "-af", "ebur128=peak=true", "-f", "null", "-"], desc="mesure audio")
    tail = log[log.rfind("Summary:"):]
    def grab(label):
        for line in tail.splitlines():
            if line.strip().startswith(label):
                try:
                    return float(line.split(":")[1].split()[0])
                except (ValueError, IndexError):
                    return None
        return None
    lufs, peak = grab("I:"), grab("Peak:")
    return [
        _r("audio_non_silencieux", lufs is not None and lufs > -50, AVERT, lufs, "> -50 LUFS"),
        _r("audio_loudness_lufs", True, INFO, lufs, "cible réseaux sociaux ≈ -14 LUFS (phase 3)"),
        _r("audio_crete_dbtp", peak is not None and peak <= -0.5, AVERT, peak, "≤ -0.5 dBTP"),
    ]


# ---------------------------------------------------------------------------
# Contrôles de marque (filigrane, zones, signature, intégrité)
# ---------------------------------------------------------------------------
def _ncc(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float64).ravel(); b = b.astype(np.float64).ravel()
    a -= a.mean(); b -= b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else 0.0


def _seg_at(segments: list[dict], t: float) -> dict | None:
    return next((s for s in segments if s["start"] <= t < s["end"]), None)


def sample_times(sc: dict, n: int = 6) -> list[float]:
    """Instants d'échantillonnage dans le contenu principal : hors fondu d'entrée, hors transitions."""
    wm = sc["watermark"]
    main = sc["main_duration"]
    lo, hi = wm["fade_in"] + 0.2, main - (sc["signature"].get("transition", 0) or 0) - 0.3
    times = []
    for s in wm["segments"]:
        a, b = max(s["start"] + 0.15, lo), min(s["end"] - 0.15, hi)
        if b > a:
            times.append(round((a + b) / 2, 3))
    extra = list(np.linspace(lo, hi, n))
    for t in extra:
        if all(abs(t - u) > 0.4 for u in times):
            times.append(round(float(t), 3))
    return sorted(times)


def watermark_checks(video: Path, sc: dict) -> list[dict]:
    res: list[dict] = []
    wm = sc["watermark"]
    box = Rect(*wm["box"])
    prof = get_profile(sc["profile"])
    # Zones de sécurité : le logo doit être dans la zone sûre de CHAQUE plateforme ciblée.
    for member in prof.members:
        mp = get_profile(member)
        res.append(_r(f"zone_securite_{member}", mp.safe.contains(box), value=box.as_list(),
                      expected=f"dans {mp.safe.as_list()}"))
    for r in prof.reserved:
        res.append(_r("hors_zone_reservee_plateforme", not box.intersects(r), value=box.as_list(), expected=f"hors {r.as_list()}"))
    for a in wm["avoid"]:
        res.append(_r("hors_zone_reservee_contenu", not box.intersects(Rect(*a)), value=box.as_list(), expected=f"hors {a}"))
    # Intégrité des logos utilisés : empreinte + ratio identique à la source officielle.
    for color, lg in wm["logos"].items():
        path = resolve(lg["path"])
        res.append(_r(f"logo_{color}_empreinte", path.exists() and sha256_file(path) == lg["sha256"],
                      value=lg["sha256"][:12]))
        err = abs((lg["box_w"] / lg["box_h"]) / lg["source_aspect"] - 1)
        res.append(_r(f"logo_{color}_ratio", err < 0.01, value=f"{lg['box_w']}x{lg['box_h']} écart {err * 100:.2f} %",
                      expected="écart < 1 % vs source officielle"))
        with Image.open(path) as im:
            res.append(_r(f"logo_{color}_dimensions", im.size == (lg["box_w"] + 2 * lg["pad"], lg["box_h"] + 2 * lg["pad"]),
                          value=list(im.size)))
    # Présence + position + non-déformation : comparaison au rendu attendu.
    src = Path(sc["input"])
    if not src.exists() or sha256_file(src) != sc["input_sha256"]:
        res.append(_r("filigrane_reconstruction", False, AVERT, detail="source absente ou modifiée : contrôle par comparaison impossible"))
        return res
    # Non-masquage : mesure indépendante sur la source, toute la durée, pas de 0.25 s.
    from .watermark import occlusion_profile
    occ = occlusion_profile(src, sc["normalize_filter"], box, prof.canvas, sc["main_duration"], sc["source_in"])
    res.append(_r("filigrane_ne_masque_pas_le_contenu", occ["occluded_fraction"] == 0,
                  value={"max": occ["max"], "zones_masquees": occ["occluded_spans"]},
                  expected=f"densité de contours ≤ {occ['threshold']} à chaque instant",
                  detail="texte, visage ou graphique sous le filigrane = rendu refusé (règle de marque)"))
    logos = {}
    for color, lg in wm["logos"].items():
        with Image.open(resolve(lg["path"])) as im:
            arr = np.asarray(im.convert("RGBA"), np.float32) / 255.0
        logos[color] = (arr, lg["pad"])
    op = wm["opacity"]
    W, H = sc["watermark"]["canvas"]
    nccs, shifts, contrasts = [], [], []
    for t in sample_times(sc):
        seg = _seg_at(wm["segments"], t)
        if not seg:
            continue
        rgba, pad = logos[seg["color"]]
        x0, y0 = box.x - pad, box.y - pad
        h, w = rgba.shape[:2]
        # Région élargie de 6 px pour tester les décalages.
        m = 6
        rx0, ry0 = max(0, x0 - m), max(0, y0 - m)
        rx1, ry1 = min(W, x0 + w + m), min(H, y0 + h + m)
        srcf = read_frame(src, sc["source_in"] + t, vf=sc["normalize_filter"], size=(W, H)).astype(np.float32) / 255.0
        outf = read_frame(video, t, size=(W, H)).astype(np.float32) / 255.0
        a = rgba[..., 3:4] * op
        pred = srcf.copy()
        pred[y0:y0 + h, x0:x0 + w] = srcf[y0:y0 + h, x0:x0 + w] * (1 - a) + rgba[..., :3] * a
        exp_d = luminance((pred[ry0:ry1, rx0:rx1] * 255).astype(np.uint8)) - luminance((srcf[ry0:ry1, rx0:rx1] * 255).astype(np.uint8))
        out_full = luminance((outf * 255).astype(np.uint8)) - luminance((srcf * 255).astype(np.uint8))
        best, c0 = (-2.0, (0, 0)), -2.0
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                sub = out_full[ry0 + dy: ry1 + dy, rx0 + dx: rx1 + dx]
                if sub.shape != exp_d.shape:
                    continue
                c = _ncc(sub, exp_d)
                if dx == 0 and dy == 0:
                    c0 = c
                if c > best[0]:
                    best = (c, (dx, dy))
        nccs.append(round(c0, 4)); shifts.append(best[1])
        # Visibilité : écart de luminance entre tracés du logo et fond immédiat, dans le rendu.
        core = rgba[pad:pad + box.h, pad:pad + box.w, 3] > 0.6
        lum_out = luminance((outf[box.y:box.bottom, box.x:box.right] * 255).astype(np.uint8))
        lum_src = luminance((srcf[box.y:box.bottom, box.x:box.right] * 255).astype(np.uint8))
        contrasts.append(round(float(abs(lum_out[core].mean() - lum_src[core].mean())), 3))
    res.append(_r("filigrane_present_et_conforme", nccs and min(nccs) >= 0.9, value=nccs, expected="corrélation ≥ 0.90 à chaque instant",
                  detail="rendu réel comparé à la composition attendue (forme, opacité, position)"))
    res.append(_r("filigrane_position_exacte", shifts and all(s == (0, 0) for s in shifts), value=shifts, expected="décalage (0, 0)"))
    res.append(_r("filigrane_visible", contrasts and min(contrasts) >= 0.25, AVERT, contrasts, "écart de luminance ≥ 0.25"))
    # Le contenu hors filigrane ne doit pas être altéré (dérive de couleurs / plage).
    t = sample_times(sc)[len(sample_times(sc)) // 2]
    srcf = read_frame(src, sc["source_in"] + t, vf=sc["normalize_filter"], size=(W, H)).astype(np.float32)
    outf = read_frame(video, t, size=(W, H)).astype(np.float32)
    maskout = np.ones((H, W), bool); maskout[max(0, box.y - 40):box.bottom + 40, max(0, box.x - 40):box.right + 40] = False
    drift = float(abs(luminance(outf.astype(np.uint8))[maskout].mean() - luminance(srcf.astype(np.uint8))[maskout].mean()))
    res.append(_r("contenu_non_altere", drift < 0.01, value=round(drift, 4), expected="dérive de luminance < 0.01"))
    return res


def signature_checks(video: Path, sc: dict) -> list[dict]:
    sig = sc["signature"]
    if "path" not in sig:
        return [_r("signature", True, INFO, "absente", detail=sig.get("skipped"))]
    W, H = sc["watermark"]["canvas"]
    t = sc["total_duration"] - 0.1
    out = read_frame(video, t, size=(W, H)).astype(np.float32)
    with Image.open(resolve(sig["last_frame"])) as im:
        ref = np.asarray(im.convert("RGB"), np.float32)
    mad = float(np.abs(out - ref).mean())
    box = Rect(*sc["watermark"]["box"])
    region = np.abs(out - ref)[box.y:box.bottom, box.x:box.right].mean()
    prof = get_profile(sc["profile"])
    cb = Rect(*sig["content_box"])
    return [
        _r("signature_dans_zone_sure", prof.safe.contains(cb), value=cb.as_list(), expected=f"dans {prof.safe.as_list()}"),
        _r("signature_presente", mad < 3.0, value=round(mad, 3), expected="écart moyen < 3/255 avec l'image finale de référence"),
        _r("signature_sans_filigrane", region < 3.0, value=round(float(region), 3), expected="zone du filigrane inchangée"),
    ]


def brand_checks() -> list[dict]:
    problems = verify_manifest()
    res = [_r("kit_de_marque_integre", not problems, value=problems or "ok")]
    svg = original_path("symbole_svg").read_text()
    res.append(_r("symbole_svg_officiel", 'viewBox="0 0 320 670"' in svg and "stroke-linecap=\"round\"" in svg,
                  value=sha256_file(original_path("symbole_svg"))[:12]))
    for k in ("titres", "labels"):
        p = resolve(load_config().brand["fonts"][k])
        res.append(_r(f"police_{k}", p.exists(), value=str(p.name)))
    return res


def run_qc(video: str | Path, profile_name: str | None = None) -> dict:
    video = Path(video).resolve()
    sc = load_sidecar(video)
    profile_name = profile_name or (sc["profile"] if sc else None)
    if not profile_name:
        raise ValueError("profil requis (aucun sidecar trouvé)")
    results = brand_checks()
    results += technical_checks(video, profile_name, sc["total_duration"] if sc else None)
    if sc and results and video.exists():
        results += audio_checks(video, sc["main_duration"])
        results += watermark_checks(video, sc)
        results += signature_checks(video, sc)
    elif not sc:
        results.append(_r("sidecar", False, AVERT, detail="pas de sidecar : contrôles de filigrane impossibles"))
    blocking = [r for r in results if not r["passed"] and r["severity"] == BLOQUANT]
    warnings = [r for r in results if not r["passed"] and r["severity"] == AVERT]
    status = "echec" if blocking else ("avertissement" if warnings else "conforme")
    return {"video": str(video), "profile": profile_name, "status": status,
            "blocking": len(blocking), "warnings": len(warnings), "checks": results}


# ---------------------------------------------------------------------------
# Planche de contrôle visuel
# ---------------------------------------------------------------------------
ZONE_COLORS = {"tiktok": (255, 0, 80), "instagram_reels": (190, 70, 255), "facebook_reels": (24, 119, 242),
               "youtube_shorts": (255, 210, 63), "youtube_16x9": (255, 210, 63)}


def contact_sheet(video: str | Path, out_png: str | Path, times: list[float] | None = None, thumb_w: int = 360) -> Path:
    """Planche d'images avec zones sûres des plateformes (contours) et boîte du filigrane (orange)."""
    video = Path(video)
    sc = load_sidecar(video)
    p = probe(video)
    times = times or [round(x, 2) for x in np.linspace(0.6, p.duration - 0.1, 6)]
    prof = get_profile(sc["profile"]) if sc else None
    thumbs = []
    for t in times:
        im = Image.fromarray(read_frame(video, t, size=(p.width, p.height))).convert("RGB")
        d = ImageDraw.Draw(im)
        if prof:
            for m in prof.members:
                z = get_profile(m).safe
                d.rectangle([z.x, z.y, z.right, z.bottom], outline=ZONE_COLORS.get(m, (200, 200, 200)), width=4)
            b = sc["watermark"]["box"]
            if t < sc["main_duration"]:
                d.rectangle([b[0] - 3, b[1] - 3, b[0] + b[2] + 3, b[1] + b[3] + 3], outline=(255, 90, 0), width=3)
        th = im.resize((thumb_w, round(thumb_w * p.height / p.width)), Image.LANCZOS)
        ImageDraw.Draw(th).text((8, 8), f"t={t:.2f}s", fill=(255, 90, 0))
        thumbs.append(th)
    gap = 12
    sheet = Image.new("RGB", (len(thumbs) * (thumb_w + gap) + gap, thumbs[0].height + 2 * gap), (246, 246, 243))
    for i, th in enumerate(thumbs):
        sheet.paste(th, (gap + i * (thumb_w + gap), gap))
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_png, optimize=True)
    return out_png
