import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _isolated_var(tmp_path, monkeypatch):
    """Chaque test écrit sa base / ses caches dans un dossier temporaire (jamais dans var/)."""
    from lukoji_engine import config
    monkeypatch.setenv("LUKOJI_PATHS__DB", str(tmp_path / "test.sqlite3"))
    monkeypatch.setenv("LUKOJI_PATHS__CACHE", str(tmp_path / "cache"))
    monkeypatch.setenv("LUKOJI_PATHS__OUT", str(tmp_path / "out"))
    config.load_config.cache_clear()
    yield
    config.load_config.cache_clear()


@pytest.fixture
def synthetic_vertical(tmp_path) -> Path:
    """Vidéo 1080x1920, 13 s : fond noir (0–6 s) puis fond clair (6–13 s), un bloc de « texte »
    en haut à gauche de la zone sûre entre 2 s et 8 s, son sinusoïdal."""
    out = tmp_path / "synthetic_vertical.mp4"
    vf = ("drawbox=x=0:y=0:w=1080:h=1920:color=0xF6F6F3:t=fill:enable='gte(t,6)',"
          "drawbox=x=70:y=290:w=300:h=90:color=0xFF8A00:t=fill:enable='between(t,2,8)',"
          "drawbox=x=90:y=310:w=200:h=12:color=0x0B0B0B:t=fill:enable='between(t,2,8)',"
          "drawbox=x=90:y=340:w=160:h=12:color=0x0B0B0B:t=fill:enable='between(t,2,8)'")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x0B0B0B:s=1080x1920:r=30:d=13",
                    "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=13",
                    "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", str(out)], check=True)
    return out
