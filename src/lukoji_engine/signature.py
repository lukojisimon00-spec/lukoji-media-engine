"""Signature de fin LUKOJI : animation courte qui reconstitue le logo vertical officiel.

Composition = mise en page EXACTE du fichier officiel `vertical_slogan_*` (positions relatives
du symbole, du logotype et du slogan), mise à l'échelle uniforme :
  1. le symbole est tracé depuis le SVG officiel (animation du trait) ;
  2. le logotype LUKOJI (découpe sans retouche du PNG officiel) apparaît ;
  3. le slogan apparaît (selon le préréglage).
La dernière image est donc le logo vertical officiel. Préréglages : aucune, flash, court, documentaire.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from .assets import _resize_premultiplied, alpha_bbox, original_path, render_svg, vertical_lockup_parts
from .config import load_config
from .db import Database
from .geometry import Profile
from .log import get_logger
from .media import run_ffmpeg
from .paths import ensure_dir, resolve

log = get_logger("signature")
RENDERER_VERSION = "1"


@dataclass(frozen=True)
class Signature:
    path: Path
    duration: float
    preset: str
    last_frame: Path
    spec: dict


def preset_for(kind: str, override: str | None = None) -> str:
    cfg = load_config().brand["signature"]
    name = override or cfg["default_by_kind"].get(kind, "aucune")
    if name not in cfg["presets"]:
        raise ValueError(f"préréglage de signature inconnu : {name} ({', '.join(cfg['presets'])})")
    return name


def should_sign(preset: str, main_duration: float) -> tuple[bool, str]:
    cfg = load_config().brand["signature"]
    if preset == "aucune":
        return False, "préréglage « aucune »"
    if main_duration < cfg["min_main_duration"]:
        return False, f"contenu trop court ({main_duration:.1f}s < {cfg['min_main_duration']}s)"
    return True, "ok"


def _svg_geometry() -> dict:
    svg = original_path("symbole_svg").read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    d = re.search(r'\sd="([^"]+)"', svg).group(1)
    sw = float(re.search(r'stroke-width="([\d.]+)"', svg).group(1))
    cache = ensure_dir(Path(load_config().engine["paths"]["cache"]) / "brand")
    probe_png = cache / "_svg_bbox_probe.png"
    ref_w = 2000
    render_svg(original_path("symbole_svg"), probe_png, ref_w)
    with Image.open(probe_png) as im:
        x0, y0, x1, y1 = alpha_bbox(im.convert("RGBA"))
        W, H = im.size
    probe_png.unlink(missing_ok=True)
    # Boîte de l'encre en unités du viewBox.
    sx, sy = vb[2] / W, vb[3] / H
    return {"viewBox": vb, "d": d, "strokeWidth": sw,
            "ink": [vb[0] + x0 * sx, vb[1] + y0 * sy, vb[0] + x1 * sx, vb[1] + y1 * sy]}


def build_spec(profile: Profile, preset: str, theme: str | None = None, db: Database | None = None) -> dict:
    cfg = load_config().brand
    scfg = cfg["signature"]
    pr = scfg["presets"][preset]
    theme = theme or scfg["theme"]
    palette = cfg["palette"]
    bg = scfg["background"] if theme == "negatif" else palette["blanc"]
    ink = palette["blanc"] if theme == "negatif" else palette["noir"]
    parts = vertical_lockup_parts(theme, db=db)
    lay = parts["layout"]
    blocks = {"symbole": lay["symbole"], "logotype": lay["logotype"]}
    if pr.get("slogan"):
        blocks["slogan"] = lay["slogan"]
    gx0 = min(b[0] for b in blocks.values()); gy0 = min(b[1] for b in blocks.values())
    gx1 = max(b[2] for b in blocks.values()) + 1; gy1 = max(b[3] for b in blocks.values()) + 1
    frac = scfg["layout"]["vertical_canvas_fraction" if profile.orientation == "vertical" else "horizontal_canvas_fraction"]
    scale = frac * profile.height / (gy1 - gy0)
    scale = min(scale, 0.8 * profile.width / (gx1 - gx0))
    off_x = (profile.width - (gx1 - gx0) * scale) / 2 - gx0 * scale
    off_y = (profile.height - (gy1 - gy0) * scale) / 2 - gy0 * scale

    def place(b):
        x0, y0 = round(b[0] * scale + off_x), round(b[1] * scale + off_y)
        return x0, y0, round((b[2] + 1 - b[0]) * scale), round((b[3] + 1 - b[1]) * scale)

    cache = ensure_dir(Path(load_config().engine["paths"]["cache"]) / "signature")
    spec: dict = {"width": profile.width, "height": profile.height, "fps": profile.fps,
                  "duration": pr["duration"], "background": bg, "preset": preset, "theme": theme,
                  "renderer": RENDERER_VERSION, "source_key": parts["source_key"]}
    # Symbole : on fait coïncider la boîte d'encre du SVG avec la boîte du symbole officiel.
    geo = _svg_geometry()
    sx, sy, sw, sh = place(lay["symbole"])
    ix0, iy0, ix1, iy1 = geo["ink"]
    k = sh / (iy1 - iy0)
    vb = geo["viewBox"]
    spec["symbol"] = {
        "viewBox": vb, "d": geo["d"], "strokeWidth": geo["strokeWidth"], "color": ink,
        "x": round(sx - (ix0 - vb[0]) * k, 2), "y": round(sy - (iy0 - vb[1]) * k, 2),
        "w": round(vb[2] * k, 2), "h": round(vb[3] * k, 2), "draw": pr["draw"],
        "target_box": [sx, sy, sw, sh], "ink_aspect_svg": (ix1 - ix0) / (iy1 - iy0),
        "ink_aspect_official": (lay["symbole"][2] + 1 - lay["symbole"][0]) / (lay["symbole"][3] + 1 - lay["symbole"][1]),
    }
    for name in ("logotype", "slogan"):
        if name not in blocks:
            spec[name] = None
            continue
        x, y, w, h = place(lay[name])
        with Image.open(parts[name]) as im:
            resized = _resize_premultiplied(im.convert("RGBA"), (w, h))
        out = cache / f"{name}_{theme}_{w}x{h}.png"
        resized.save(out)
        spec[name] = {"src": str(out), "x": x, "y": y, "w": w, "h": h,
                      "t": pr["logotype"] if name == "logotype" else pr["slogan"],
                      "rise": max(6, round(h * (0.12 if name == "logotype" else 0.25)))}
    # Boîte englobante du contenu de la signature (pour le contrôle des zones sûres).
    boxes = [spec["symbol"]["target_box"]] + [[o["x"], o["y"], o["w"], o["h"]] for o in (spec["logotype"], spec["slogan"]) if o]
    x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes)
    x1 = max(b[0] + b[2] for b in boxes); y1 = max(b[1] + b[3] for b in boxes)
    spec["content_box"] = [x0, y0, x1 - x0, y1 - y0]
    return spec


def render(profile: Profile, preset: str, *, theme: str | None = None, db: Database | None = None,
           force: bool = False) -> Signature:
    if preset == "aucune":
        raise ValueError("rien à rendre pour le préréglage « aucune »")
    spec = build_spec(profile, preset, theme, db=db)
    key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:12]
    base = ensure_dir(Path(load_config().engine["paths"]["cache"]) / "signature")
    out = base / f"signature_{preset}_{profile.width}x{profile.height}_{key}.mp4"
    frames = base / f"frames_{key}"
    last = base / f"signature_{preset}_{profile.width}x{profile.height}_{key}_last.png"
    if out.exists() and last.exists() and not force:
        return Signature(out, spec["duration"], preset, last, spec)
    spec_file = base / f"spec_{key}.json"
    spec["outDir"] = str(frames)
    spec_file.write_text(json.dumps(spec, indent=2))
    node = load_config().get("tools.node", "node")
    log.info("rendu des images de signature", extra={"preset": preset, "canvas": f"{profile.width}x{profile.height}"})
    subprocess.run([node, str(resolve("scripts/render_signature.mjs")), str(spec_file)], check=True,
                   capture_output=True, text=True)
    enc = load_config().engine["encode"]
    run_ffmpeg(["-framerate", str(profile.fps), "-i", str(frames / "%05d.png"),
                "-c:v", enc["video_codec"], "-preset", enc["preset"], "-crf", "14",
                "-pix_fmt", enc["pix_fmt"], "-color_range", "tv", "-colorspace", "bt709",
                "-color_primaries", "bt709", "-color_trc", "bt709", str(out)], desc="encodage signature")
    pngs = sorted(frames.glob("*.png"))
    shutil.copyfile(pngs[-1], last)
    shutil.rmtree(frames)
    spec_file.unlink(missing_ok=True)
    return Signature(out, spec["duration"], preset, last, spec)
