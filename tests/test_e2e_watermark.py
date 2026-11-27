"""Bout en bout : rendu réel FFmpeg + Chromium sur vidéo synthétique, puis contrôle qualité.
Inclut des tests NÉGATIFS : le QC doit refuser un rendu sans filigrane et un logo déformé."""
import json
import shutil
import subprocess

import pytest

from lukoji_engine import config, qc
from lukoji_engine.db import Database
from lukoji_engine.paths import resolve
from lukoji_engine.watermark import apply

pytestmark = pytest.mark.e2e


@pytest.fixture
def rendered(synthetic_vertical, tmp_path):
    db = Database(config.load_config().path("db")); db.migrate()
    out = tmp_path / "out" / "wm.mp4"
    sc = apply(synthetic_vertical, out, profile_name="vertical_universal", kind="short",
               content_slug="e2e", db=db)
    return out, sc, db


def _status(report, name):
    return next(c for c in report["checks"] if c["name"] == name)


def test_render_is_conform(rendered):
    out, sc, db = rendered
    report = qc.run_qc(out)
    failed = [c for c in report["checks"] if not c["passed"]]
    assert report["status"] == "conforme", failed
    assert sc["total_duration"] == pytest.approx(13 + 1.6 - 0.25, abs=0.01)


def test_placement_avoids_text_and_colour_adapts(rendered):
    _, sc, _ = rendered
    wm = sc["watermark"]
    assert wm["anchor"] != "top_left"                      # bloc de texte 2–8 s en haut à gauche
    top_left = next(c for c in wm["candidates"] if c["anchor"] == "top_left")
    assert top_left["rejected"] and "masquerait" in top_left["rejected"]
    colours = [s["color"] for s in wm["segments"]]
    assert colours == ["white", "black"]                   # fond noir puis fond clair
    assert abs(wm["segments"][1]["start"] - 6.0) <= 0.5


def test_render_registered_in_db(rendered):
    _, sc, db = rendered
    assert db.get_content("e2e")["kind"] == "short"
    assert db.conn.execute("SELECT COUNT(*) FROM renders").fetchone()[0] == 1


def test_qc_rejects_video_without_watermark(rendered, synthetic_vertical, tmp_path):
    out, sc, _ = rendered
    fake = tmp_path / "sans_filigrane.mp4"
    # Même durée/format que le rendu, mais sans logo.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(synthetic_vertical), "-i", str(out),
                    "-filter_complex", f"[0:v]fps=30,format=yuv420p,tpad=stop_mode=clone:stop_duration=2[v]",
                    "-map", "[v]", "-map", "1:a", "-t", str(sc["total_duration"]),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(fake)],
                   check=True)
    shutil.copy(str(out) + ".json", str(fake) + ".json")
    report = qc.run_qc(fake)
    assert not _status(report, "filigrane_present_et_conforme")["passed"]
    assert report["status"] == "echec"


def test_qc_rejects_stretched_logo(rendered, synthetic_vertical, tmp_path):
    out, sc, _ = rendered
    wm = sc["watermark"]
    x, y, w, h = wm["box"]
    logo = resolve(wm["logos"]["white"]["path"])
    pad = wm["logos"]["white"]["pad"]
    bad = tmp_path / "logo_etire.mp4"
    # Logo étiré de 12 % en largeur, même position : doit être détecté.
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(synthetic_vertical), "-loop", "1", "-i", str(logo),
                    "-i", str(out), "-filter_complex",
                    f"[1:v]scale=iw*1.12:ih,format=rgba,colorchannelmixer=aa={wm['opacity']}[l];"
                    f"[0:v][l]overlay={x - pad}:{y - pad}:shortest=1,fps=30,format=yuv420p,"
                    f"tpad=stop_mode=clone:stop_duration=2[v]",
                    "-map", "[v]", "-map", "2:a", "-t", str(sc["total_duration"]),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", str(bad)], check=True)
    shutil.copy(str(out) + ".json", str(bad) + ".json")
    report = qc.run_qc(bad)
    assert not _status(report, "filigrane_present_et_conforme")["passed"]


def test_short_content_gets_no_signature(synthetic_vertical, tmp_path):
    out = tmp_path / "court.mp4"
    sc = apply(synthetic_vertical, out, profile_name="tiktok", kind="short", source_out=8.0)
    assert "skipped" in sc["signature"] and sc["total_duration"] == pytest.approx(8.0, abs=0.01)
    assert qc.run_qc(out)["status"] == "conforme"
