"""VISUAL DIRECTOR : direction artistique propre à chaque documentaire, dans le cadre de la charte LUKOJI."""
from __future__ import annotations

import re

from ..config import load_config
from .text import strip_accents

REQUIRED = ("style_general", "atmosphere", "palette", "typographie", "realisme", "archives", "cartes", "graphiques",
            "motion", "transitions", "sound_design", "categories_visuelles")
CATEGORIES = ("authentique", "illustration", "reconstitution", "graphique_explicatif", "image_generee", "symbolique")


def _fingerprint(doc: dict) -> set[str]:
    txt = " ".join(str(doc.get(k, "")) for k in ("style_general", "atmosphere", "motion", "transitions", "cartes", "graphiques"))
    return {w for w in re.findall(r"[a-z]{5,}", strip_accents(txt.lower()))}


def evaluate(doc: dict, others: list[dict] | None = None) -> dict:
    p: list[dict] = []

    def add(sev, code, msg):
        p.append({"severite": sev, "code": code, "message": msg, "ou": "direction artistique"})

    for k in REQUIRED:
        if not doc.get(k):
            add("bloquant", "champ_manquant", f"champ « {k} » manquant")
    brand = {v.upper() for v in load_config().brand["palette"].values()}
    pal = doc.get("palette") or {}
    colors = [c.upper() for c in (pal.get("dominantes") or []) + (pal.get("accents") or [])]
    hors = {c.upper() for c in pal.get("hors_charte", {})} if isinstance(pal.get("hors_charte"), dict) else set()
    for c in colors:
        if not re.fullmatch(r"#[0-9A-F]{6}", c):
            add("bloquant", "couleur_invalide", f"couleur invalide {c}")
        elif c not in brand and c not in hors:
            add("bloquant", "couleur_hors_charte", f"{c} hors charte sans justification (palette.hors_charte)")
    fonts = " ".join(str(v) for v in (doc.get("typographie") or {}).values()) if isinstance(doc.get("typographie"), dict) else str(doc.get("typographie"))
    for needed in ("Archivo Black", "IBM Plex Mono"):
        if needed.lower() not in fonts.lower():
            add("alerte", "typo_charte", f"typographie de la charte absente : {needed}")
    cats = doc.get("categories_visuelles") or {}
    for c in CATEGORIES:
        if not str(cats.get(c) or "").strip():
            add("bloquant", "categorie_non_definie", f"règle manquante pour la catégorie « {c} »")
    sim = 0.0
    for o in others or []:
        a, b = _fingerprint(doc), _fingerprint(o)
        if a and b:
            sim = max(sim, len(a & b) / len(a | b))
    if sim > 0.6:
        add("alerte", "direction_repetitive", f"direction artistique trop proche d'un autre projet (similarité {sim:.2f})")
    return {"couleurs": colors, "similarite_max_autres_projets": round(sim, 2), "problemes": p}
