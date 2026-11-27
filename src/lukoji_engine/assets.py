"""Kit de marque : intégrité des originaux, manifeste versionné, rendus dérivés des logos.

Règles :
- les originaux (brand/originals, brand/fonts) ne sont jamais modifiés ; leur SHA-256 est vérifié ;
- un dérivé est soit une DÉCOUPE sans retouche, soit un RENDU du SVG officiel (géométrie intacte,
  seule la couleur du trait peut être substituée par une couleur de la palette),
  soit un REDIMENSIONNEMENT proportionnel (alpha prémultiplié, Lanczos) ;
- chaque dérivé enregistre sa source (sha256) et ses paramètres ; une nouvelle version est créée
  dès que le contenu change.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageFilter

from .config import load_config
from .db import Database, now
from .log import get_logger
from .paths import ensure_dir, rel, resolve

log = get_logger("assets")

GENERATOR_VERSION = "1"


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def image_size(path: Path) -> tuple[int | None, int | None]:
    if path.suffix.lower() in (".png", ".jpg", ".jpeg"):
        with Image.open(path) as im:
            return im.size
    return None, None


def alpha_bbox(im: Image.Image, threshold: int = 8) -> tuple[int, int, int, int]:
    """Boîte (x0, y0, x1, y1) exclusive des pixels dont l'alpha dépasse le seuil."""
    a = im.getchannel("A").point(lambda v: 255 if v > threshold else 0)
    box = a.getbbox()
    if not box:
        raise ValueError("image entièrement transparente")
    return box


# ---------------------------------------------------------------------------
# Manifeste des originaux
# ---------------------------------------------------------------------------
def build_manifest(db: Database | None = None) -> dict:
    cfg = load_config()
    entries = []
    for item in cfg.brand["originals"]:
        path = resolve(item["file"])
        if not path.exists():
            raise FileNotFoundError(f"ressource de marque manquante : {item['file']}")
        w, h = image_size(path)
        entry = {
            "key": item["key"], "file": item["file"], "sha256": sha256_file(path),
            "bytes": path.stat().st_size, "width": w, "height": h,
            "role": item["role"], "uploads": item.get("uploads", []),
        }
        entries.append(entry)
        if db:
            db.register_asset(key=item["key"], kind="original", path=item["file"], sha256=entry["sha256"],
                              bytes_=entry["bytes"], width=w, height=h, role=item["role"])
    manifest = {"generated_at": now(), "generator": GENERATOR_VERSION, "originals": entries}
    out = cfg.path("manifest")
    previous = json.loads(out.read_text()) if out.exists() else None
    if previous:
        old = {e["key"]: e["sha256"] for e in previous["originals"]}
        changed = [e["key"] for e in entries if e["key"] in old and old[e["key"]] != e["sha256"]]
        if changed:
            raise RuntimeError(
                f"Des originaux ont changé depuis le manifeste ({', '.join(changed)}). "
                "Refus de réécrire : vérifier l'origine du changement, puis supprimer manuellement le manifeste.")
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    log.info("manifeste écrit", extra={"originals": len(entries), "path": rel(out)})
    return manifest


def verify_manifest() -> list[dict]:
    """Compare chaque original au manifeste. Retourne la liste des écarts (vide = intègre)."""
    cfg = load_config()
    mpath = cfg.path("manifest")
    if not mpath.exists():
        return [{"key": "*", "problem": "manifeste absent (lancer `brand build`)"}]
    manifest = json.loads(mpath.read_text())
    problems = []
    declared = {i["key"] for i in cfg.brand["originals"]}
    for e in manifest["originals"]:
        path = resolve(e["file"])
        if not path.exists():
            problems.append({"key": e["key"], "problem": "fichier manquant"})
        elif sha256_file(path) != e["sha256"]:
            problems.append({"key": e["key"], "problem": "empreinte SHA-256 différente (fichier modifié)"})
    missing = declared - {e["key"] for e in manifest["originals"]}
    problems += [{"key": k, "problem": "déclaré dans brand.toml mais absent du manifeste"} for k in missing]
    return problems


def original_path(key: str) -> Path:
    for item in load_config().brand["originals"]:
        if item["key"] == key:
            return resolve(item["file"])
    raise KeyError(key)


# ---------------------------------------------------------------------------
# Rendus dérivés
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class LogoImage:
    """Image de logo prête à incruster. `box_w`/`box_h` = taille du logo ; `pad` = marge d'ombre."""
    path: Path
    box_w: int
    box_h: int
    pad: int
    sha256: str
    source_key: str
    source_aspect: float

    @property
    def aspect(self) -> float:
        return self.box_w / self.box_h


def fit_size(aspect: float, *, width: int | None = None, height: int | None = None, slack: int = 3) -> tuple[int, int]:
    """Couple (largeur, hauteur) entier le plus fidèle au ratio source, à ±`slack` px de la cible.

    Aux petites tailles, l'arrondi seul peut écarter le ratio de ~1 % ; on choisit la taille voisine
    qui minimise l'écart (le logo n'est jamais étiré : seule sa taille varie de quelques pixels).
    """
    if not width and not height:
        raise ValueError("largeur ou hauteur requise")
    best = None
    for d in range(-slack, slack + 1):
        if width:
            w = width + d; h = max(1, round(w / aspect))
        else:
            h = height + d; w = max(1, round(h * aspect))
        err = abs((w / h) / aspect - 1)
        key = (round(err, 5), abs(d))
        if best is None or key < best[0]:
            best = (key, (w, h))
    return best[1]


def _resize_premultiplied(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    return im.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def _cache_dir() -> Path:
    return ensure_dir(Path(load_config().engine["paths"]["cache"]) / "brand")


def _register(db: Database | None, key: str, path: Path, source_key: str, params: dict, role: str) -> str:
    digest = sha256_file(path)
    if db:
        w, h = image_size(path)
        src = db.latest_asset(source_key)
        db.register_asset(key=key, kind="derived", path=rel(path), sha256=digest, bytes_=path.stat().st_size,
                          width=w, height=h, role=role,
                          derived_from=f"{source_key}@{src['sha256'][:12]}" if src else source_key, params=params)
    return digest


def render_svg(svg: Path, out: Path, width: int, color: str | None = None) -> None:
    node = load_config().get("tools.node", "node")
    cmd = [node, str(resolve("scripts/render_svg.mjs")), str(svg), str(out), str(width)]
    if color:
        cmd.append(color)
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def add_shadow(im: Image.Image, opacity: float, blur_ratio: float = 0.06, offset_ratio: float = 0.035) -> tuple[Image.Image, int]:
    """Ombre portée douce (précédent officiel : horizontal_blanc_ombre). Retourne (image, marge)."""
    h = im.height
    blur = max(1.0, h * blur_ratio)
    dy = max(1, round(h * offset_ratio))
    pad = math.ceil(blur * 3) + dy
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    alpha = Image.new("L", canvas.size, 0)
    alpha.paste(im.getchannel("A"), (pad, pad + dy))
    alpha = alpha.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: round(v * opacity))
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow.putalpha(alpha)
    canvas = Image.alpha_composite(canvas, shadow)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(im, (pad, pad))
    return Image.alpha_composite(canvas, layer), pad


def logo_image(variant: str, color: str, *, width: int | None = None, height: int | None = None,
               shadow: bool = False, shadow_opacity: float = 0.35, db: Database | None = None) -> LogoImage:
    """Rend le logo `variant` ('lockup' | 'symbole') en `color` ('white' | 'black') à la taille exacte.

    Le ratio est celui de la source officielle ; l'autre dimension est déduite (jamais imposée).
    """
    if color not in ("white", "black"):
        raise ValueError("couleur : white | black")
    palette = load_config().brand["palette"]
    hexcol = palette["blanc"] if color == "white" else palette["noir"]
    if variant == "lockup":
        source_key = "horizontal_blanc" if color == "white" else "horizontal_noir"
        with Image.open(original_path(source_key)) as src:
            src = src.convert("RGBA")
            crop = src.crop(alpha_bbox(src))
    elif variant == "symbole":
        source_key = "symbole_svg"
        if not height:
            raise ValueError("le symbole se dimensionne par sa hauteur")
        tmp = _cache_dir() / f"_svg_{color}_{height}.png"
        # Rendu très haute définition puis réduction : bords plus fins qu'un rendu direct.
        render_svg(original_path("symbole_svg"), tmp, width=max(1200, height * 4), color=hexcol)
        with Image.open(tmp) as src:
            src = src.convert("RGBA")
            crop = src.crop(alpha_bbox(src))
        tmp.unlink(missing_ok=True)
    else:
        raise ValueError("variante : lockup | symbole")
    src_aspect = crop.width / crop.height
    size = fit_size(src_aspect, width=width, height=height)
    logo = _resize_premultiplied(crop, size)
    pad = 0
    if shadow:
        logo, pad = add_shadow(logo, shadow_opacity)
    params = {"variant": variant, "color": color, "size": list(size), "shadow": shadow,
              "shadow_opacity": shadow_opacity if shadow else None, "generator": GENERATOR_VERSION}
    key = f"filigrane_{variant}_{color}_{size[0]}x{size[1]}{'_ombre' if shadow else ''}"
    out = _cache_dir() / f"{key}.png"
    logo.save(out, optimize=True)
    digest = _register(db, key, out, source_key, params, "filigrane")
    return LogoImage(out, size[0], size[1], pad, digest, source_key, src_aspect)


def vertical_lockup_parts(theme: str = "negatif", db: Database | None = None) -> dict:
    """Découpes (sans retouche) du logotype et du slogan depuis le logo vertical officiel.

    Retourne les chemins et les boîtes d'origine, pour recomposer exactement la mise en page officielle.
    """
    cfg = load_config()
    layout = cfg.brand["derived"]["vertical_layout"]
    source_key = "vertical_slogan_blanc" if theme == "negatif" else "vertical_slogan_noir"
    parts = {"source_key": source_key, "layout": layout}
    with Image.open(original_path(source_key)) as src:
        src = src.convert("RGBA")
        parts["source_size"] = list(src.size)
        for name in ("logotype", "slogan"):
            x0, y0, x1, y1 = layout[name]
            crop = src.crop((x0, y0, x1 + 1, y1 + 1))
            out = _cache_dir() / f"signature_{name}_{theme}.png"
            crop.save(out, optimize=True)
            _register(db, f"signature_{name}_{theme}", out, source_key,
                      {"crop": [x0, y0, x1, y1], "generator": GENERATOR_VERSION}, "signature")
            parts[name] = str(out)
    return parts
