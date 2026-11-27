"""Outils d'analyse de texte pour la voix off (français)."""
from __future__ import annotations

import re
import unicodedata
from collections import Counter

from ..config import load_config
from ..paths import resolve

STOP = set("""le la les un une des de du d l à au aux et ou en dans sur pour par avec sans ce cet cette ces il elle ils elles
on nous vous je tu se sa son ses leur leurs lui qui que qu quoi dont où ne pas plus est sont était été être a ont avait
fait faire tout tous toute toutes comme mais si y n s c j m t aussi très bien alors puis encore déjà même cela ça
vers chez entre contre après avant sous depuis pendant quand dont lors elle elles leurs nos notre votre""".split())


def _load() -> dict:
    import tomllib
    with open(resolve("config/story.toml"), "rb") as fh:
        return tomllib.load(fh)


def story_config() -> dict:
    return _load()


def words(text: str) -> list[str]:
    """Mots prononcés (les nombres comptent pour leur forme orale approximative)."""
    toks = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9’'-]+", text)
    out = []
    for t in toks:
        if re.fullmatch(r"\d[\d\s,.]*", t):
            digits = re.sub(r"\D", "", t)
            out.extend(["n"] * max(1, min(4, len(digits) // 2 + 1)))   # « deux cent quatre-vingt-sept mille » ≈ 4 mots
        else:
            out.append(t)
    return out


def word_count(text: str) -> int:
    return len(words(text))


def speech_seconds(text: str, wpm: float | None = None) -> float:
    wpm = wpm or story_config()["rythme"]["mots_par_minute"]
    return round(word_count(text) / wpm * 60, 1)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?…])\s+", text.strip()) if s.strip()]


def long_sentences(text: str, limit: int) -> list[tuple[int, str]]:
    return [(word_count(s), s) for s in sentences(text) if word_count(s) > limit]


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).replace("’", "'").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def find_cliches(text: str, cliches: list[str]) -> list[str]:
    t = norm(text)
    return [c for c in cliches if norm(c) in t]


def repetitions(text: str, window: int, threshold: int) -> list[tuple[str, int]]:
    """Mots pleins répétés ≥ seuil fois dans une fenêtre glissante de `window` mots."""
    # Les apostrophes séparent les mots (« l'argent » → « argent »).
    toks = [strip_accents(w.lower()) for w in re.findall(r"[A-Za-zÀ-ÿ-]+", text.replace("’", " ").replace("'", " "))]
    toks = [t for t in toks if len(t) > 3 and t not in STOP]
    found: dict[str, int] = {}
    for i in range(0, max(1, len(toks) - window + 1), max(1, window // 3)):
        for w, n in Counter(toks[i:i + window]).items():
            if n >= threshold:
                found[w] = max(found.get(w, 0), n)
    return sorted(found.items(), key=lambda x: -x[1])


_NUM = re.compile(r"\d+(?:[  .,]\d+)*")


def numbers(text: str) -> set[str]:
    """Nombres d'un texte, normalisés (« 29,5 » = « 29.5 », « 287 400 » = « 287,400 » = « 287400 »)."""
    out = set()
    for m in _NUM.finditer(text.replace(" ", " ").replace(" ", " ")):
        raw = m.group(0)
        # séparateur de milliers (groupe de 3 chiffres) ou décimal
        parts = re.split(r"[  .,]", raw)
        if len(parts) > 1 and all(len(p) == 3 for p in parts[1:]):
            out.add("".join(parts))
        elif len(parts) == 2:
            out.add(parts[0] + "." + parts[1])
        else:
            out.add(re.sub(r"\D", "", raw))
    return out


def has_marker(text: str, markers: list[str]) -> bool:
    t = norm(text)
    return any(norm(m) in t for m in markers)
