"""Géométrie des canevas : rectangles, zones de sécurité par plateforme, ancrages du filigrane."""
from __future__ import annotations

from dataclasses import dataclass, field

from .config import load_config


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    @property
    def right(self) -> int:
        return self.x + self.w

    @property
    def bottom(self) -> int:
        return self.y + self.h

    def intersect(self, other: "Rect") -> "Rect":
        x0, y0 = max(self.x, other.x), max(self.y, other.y)
        x1, y1 = min(self.right, other.right), min(self.bottom, other.bottom)
        return Rect(x0, y0, max(0, x1 - x0), max(0, y1 - y0))

    def intersects(self, other: "Rect") -> bool:
        i = self.intersect(other)
        return i.w > 0 and i.h > 0

    def contains(self, other: "Rect") -> bool:
        return (other.x >= self.x and other.y >= self.y
                and other.right <= self.right and other.bottom <= self.bottom)

    def expand(self, pad: int) -> "Rect":
        return Rect(self.x - pad, self.y - pad, self.w + 2 * pad, self.h + 2 * pad)

    def as_list(self) -> list[int]:
        return [self.x, self.y, self.w, self.h]

    @staticmethod
    def parse(text: str) -> "Rect":
        parts = [int(float(p)) for p in text.replace(" ", "").split(",")]
        if len(parts) != 4:
            raise ValueError("format attendu : x,y,largeur,hauteur")
        return Rect(*parts)


@dataclass(frozen=True)
class Profile:
    name: str
    label: str
    width: int
    height: int
    fps: int
    orientation: str
    safe: Rect
    reserved: tuple[Rect, ...] = field(default_factory=tuple)
    members: tuple[str, ...] = field(default_factory=tuple)
    verified: bool = False
    notes: str = ""

    @property
    def canvas(self) -> Rect:
        return Rect(0, 0, self.width, self.height)

    @property
    def ratio(self) -> float:
        return self.width / self.height


def central_crop(width: int, height: int, ratio: tuple[int, int]) -> Rect:
    """Recadrage central au ratio donné (largeur:hauteur) inscrit dans le canevas."""
    rw, rh = ratio
    if width / height > rw / rh:
        w = round(height * rw / rh)
        return Rect((width - w) // 2, 0, w, height)
    h = round(width * rh / rw)
    return Rect(0, (height - h) // 2, width, h)


def _single_profile(name: str, spec: dict) -> Profile:
    w, h = spec["canvas"]
    m = spec["marges"]
    safe = Rect(m["left"], m["top"], w - m["left"] - m["right"], h - m["top"] - m["bottom"])
    for apercu in spec.get("apercus", []):
        safe = safe.intersect(central_crop(w, h, tuple(apercu["ratio"])))
    reserved = tuple(Rect(*r) for r in spec.get("reserve", []))
    return Profile(name, spec["label"], w, h, spec["fps"], spec["orientation"], safe, reserved,
                   (name,), bool(spec.get("verifie_sur_appareil", False)), spec.get("notes", ""))


def get_profile(name: str) -> Profile:
    specs = load_config().platforms["profiles"]
    if name not in specs:
        raise KeyError(f"profil inconnu : {name} (disponibles : {', '.join(specs)})")
    spec = specs[name]
    if "union_of" not in spec:
        return _single_profile(name, spec)
    members = [get_profile(m) for m in spec["union_of"]]
    w, h = spec["canvas"]
    safe = Rect(0, 0, w, h)
    reserved: list[Rect] = []
    for p in members:
        if (p.width, p.height) != (w, h):
            raise ValueError(f"{name} : canevas incompatible avec {p.name}")
        safe = safe.intersect(p.safe)
        reserved.extend(p.reserved)
    return Profile(name, spec["label"], w, h, spec["fps"], spec["orientation"], safe, tuple(reserved),
                   tuple(p.name for p in members), all(p.verified for p in members), spec.get("notes", ""))


def list_profiles() -> list[str]:
    return list(load_config().platforms["profiles"])


def anchor_box(anchor: str, safe: Rect, w: int, h: int) -> Rect:
    """Place une boîte w×h contre le coin `anchor` de la zone sûre."""
    xs = {"left": safe.x, "right": safe.right - w, "center": safe.x + (safe.w - w) // 2}
    ys = {"top": safe.y, "bottom": safe.bottom - h}
    vert, horiz = anchor.split("_")
    return Rect(xs[horiz], ys[vert], w, h)
