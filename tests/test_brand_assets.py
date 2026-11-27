import shutil
from pathlib import Path

import numpy as np
from PIL import Image

from lukoji_engine import assets, config
from lukoji_engine.assets import fit_size, logo_image, original_path, verify_manifest
from lukoji_engine.paths import repo_root


def test_manifest_matches_originals():
    assert verify_manifest() == []


def test_originals_are_read_only_and_svg_is_official():
    for item in config.load_config().brand["originals"]:
        p = repo_root() / item["file"]
        assert p.exists(), item["file"]
    svg = original_path("symbole_svg").read_text()
    assert 'viewBox="0 0 320 670"' in svg and 'stroke="#0B0B0B"' in svg


def test_tampered_original_is_detected(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    for d in ("config", "brand", "scripts"):
        shutil.copytree(repo_root() / d, root / d)
    target = root / "brand/originals/symbole_officiel.svg"
    target.chmod(0o644)
    target.write_text(target.read_text().replace('stroke-width="16"', 'stroke-width="18"'))
    monkeypatch.setenv("LUKOJI_ROOT", str(root))
    problems = verify_manifest()
    assert any(p["key"] == "symbole_svg" for p in problems)


def test_fit_size_minimises_ratio_error():
    aspect = 1803 / 487
    w, h = fit_size(aspect, width=220)
    assert abs((w / h) / aspect - 1) < 0.005 and abs(w - 220) <= 3


def test_lockup_keeps_official_ratio():
    lg = logo_image("lockup", "white", width=220)
    assert abs(lg.aspect / lg.source_aspect - 1) < 0.005
    with Image.open(lg.path) as im:
        assert im.size == (lg.box_w, lg.box_h)


def test_symbol_from_svg_matches_official_png():
    """Le rendu du SVG officiel doit coïncider avec le PNG officiel du symbole (IoU ≥ 0.97)."""
    lg = logo_image("symbole", "black", height=600)
    with Image.open(lg.path) as im:
        a = np.asarray(im.convert("RGBA"))[..., 3] > 128
    with Image.open(original_path("symbole_noir")) as ref:
        ref = ref.convert("RGBA")
        ref = ref.crop(assets.alpha_bbox(ref)).resize(a.shape[::-1], Image.LANCZOS)
        b = np.asarray(ref)[..., 3] > 128
    iou = (a & b).sum() / (a | b).sum()
    assert iou >= 0.97, iou


def test_signature_crops_are_pixel_exact():
    parts = assets.vertical_lockup_parts("negatif")
    x0, y0, x1, y1 = parts["layout"]["logotype"]
    with Image.open(parts["logotype"]) as crop, Image.open(original_path("vertical_slogan_blanc")) as src:
        ref = src.convert("RGBA").crop((x0, y0, x1 + 1, y1 + 1))
        assert np.array_equal(np.asarray(crop.convert("RGBA")), np.asarray(ref))
