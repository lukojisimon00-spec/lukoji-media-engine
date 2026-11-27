"""Accès bas niveau aux médias via FFmpeg/FFprobe (sondage, extraction d'images, exécution)."""
from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np

from .config import load_config
from .log import get_logger

log = get_logger("media")


class FFmpegError(RuntimeError):
    pass


def _tool(name: str) -> str:
    return load_config().get(f"tools.{name}", name)


def run_ffmpeg(args: list[str], *, desc: str = "ffmpeg") -> str:
    cmd = [_tool("ffmpeg"), "-hide_banner", "-nostdin", "-y", *args]
    log.debug("exécution", extra={"cmd": shlex.join(cmd)})
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise FFmpegError(f"{desc} a échoué ({proc.returncode}) :\n{proc.stderr[-3000:]}")
    return proc.stderr


@dataclass(frozen=True)
class Probe:
    path: str
    format_name: str
    duration: float
    size_bytes: int
    bit_rate: int
    width: int
    height: int
    fps: float
    avg_fps: float
    vcodec: str
    vprofile: str
    pix_fmt: str
    sar: str
    nb_frames: int | None
    has_audio: bool
    acodec: str | None
    sample_rate: int | None
    channels: int | None
    raw: dict

    @property
    def ratio(self) -> float:
        return self.width / self.height


def probe(path: str | Path) -> Probe:
    cmd = [_tool("ffprobe"), "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise FFmpegError(f"ffprobe : {proc.stderr.strip()}")
    data = json.loads(proc.stdout)
    v = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    if v is None:
        raise FFmpegError(f"aucun flux vidéo dans {path}")
    fmt = data["format"]
    return Probe(
        path=str(path), format_name=fmt.get("format_name", ""),
        duration=float(fmt.get("duration") or v.get("duration") or 0),
        size_bytes=int(fmt.get("size", 0)), bit_rate=int(fmt.get("bit_rate", 0) or 0),
        width=int(v["width"]), height=int(v["height"]),
        fps=float(Fraction(v.get("r_frame_rate", "0/1"))), avg_fps=float(Fraction(v.get("avg_frame_rate", "0/1") or "0/1")),
        vcodec=v.get("codec_name", ""), vprofile=v.get("profile", ""), pix_fmt=v.get("pix_fmt", ""),
        sar=v.get("sample_aspect_ratio", "1:1"),
        nb_frames=int(v["nb_frames"]) if v.get("nb_frames") else None,
        has_audio=a is not None, acodec=a.get("codec_name") if a else None,
        sample_rate=int(a["sample_rate"]) if a and a.get("sample_rate") else None,
        channels=int(a["channels"]) if a and a.get("channels") else None, raw=data,
    )


def read_frame(path: str | Path, t: float, *, vf: str | None = None, size: tuple[int, int] | None = None) -> np.ndarray:
    """Image RGB (H, W, 3, uint8) au temps t. `vf` = filtre de normalisation optionnel."""
    if size is None:
        p = probe(path)
        size = (p.width, p.height)
    filters = [vf] if vf else []
    filters.append("format=rgb24")
    cmd = [_tool("ffmpeg"), "-v", "error", "-nostdin", "-ss", f"{t:.3f}", "-i", str(path),
           "-frames:v", "1", "-vf", ",".join(filters), "-f", "rawvideo", "-"]
    out = subprocess.run(cmd, capture_output=True).stdout
    w, h = size
    if len(out) != w * h * 3:
        raise FFmpegError(f"extraction impossible à t={t:.2f}s ({len(out)} octets reçus, {w * h * 3} attendus)")
    return np.frombuffer(out, np.uint8).reshape(h, w, 3)


def read_region_series(path: str | Path, box: tuple[int, int, int, int], step: float, duration: float,
                       *, vf: str | None = None, start: float = 0.0) -> np.ndarray:
    """Série temporelle d'une région (x, y, w, h) échantillonnée tous les `step` secondes.

    Un seul passage FFmpeg : fps -> crop -> rgb24. Retourne (N, h, w, 3) uint8.
    """
    x, y, w, h = box
    filters = [vf] if vf else []
    filters += [f"fps=1/{step}", f"crop={w}:{h}:{x}:{y}", "format=rgb24"]
    cmd = [_tool("ffmpeg"), "-v", "error", "-nostdin", "-ss", f"{start:.3f}", "-i", str(path), "-t", f"{duration:.3f}",
           "-vf", ",".join(filters), "-f", "rawvideo", "-"]
    out = subprocess.run(cmd, capture_output=True).stdout
    n = len(out) // (w * h * 3)
    return np.frombuffer(out[: n * w * h * 3], np.uint8).reshape(n, h, w, 3)


def luminance(rgb: np.ndarray) -> np.ndarray:
    """Luminance relative approximative (0–1), Rec.709, sur valeurs gamma."""
    f = rgb.astype(np.float32) / 255.0
    return 0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]


def moov_before_mdat(path: str | Path) -> bool | None:
    """True si l'atome moov précède mdat (lecture progressive / faststart)."""
    with open(path, "rb") as fh:
        offset = 0
        size_total = Path(path).stat().st_size
        while offset < size_total:
            fh.seek(offset)
            header = fh.read(16)
            if len(header) < 8:
                return None
            size = int.from_bytes(header[:4], "big")
            kind = header[4:8].decode("latin-1")
            if size == 1:
                size = int.from_bytes(header[8:16], "big")
            elif size == 0:
                size = size_total - offset
            if kind == "moov":
                return True
            if kind == "mdat":
                return False
            offset += size
    return None


def normalize_filter(src_w: int, src_h: int, dst_w: int, dst_h: int, fps: int, pad_color: str = "#0B0B0B") -> str:
    """Filtre de mise au canevas : mise à l'échelle sans déformation + bandes si besoin + fps + SAR 1."""
    parts = []
    if (src_w, src_h) != (dst_w, dst_h):
        parts.append(f"scale={dst_w}:{dst_h}:force_original_aspect_ratio=decrease:flags=lanczos")
        parts.append(f"pad={dst_w}:{dst_h}:(ow-iw)/2:(oh-ih)/2:color={pad_color.replace('#', '0x')}")
    parts.append("setsar=1")
    parts.append(f"fps={fps}")
    return ",".join(parts)
