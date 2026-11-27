"""Contrôle factuel d'un passage de voix off : faits cités, règles d'usage, chiffres sourcés."""
from __future__ import annotations

from .text import has_marker, numbers, story_config


def facts_index(research: dict) -> dict:
    return {f["ref"]: f for f in research.get("faits", [])}


def check_passage(text: str, refs: list[str], facts: dict, where: str) -> list[dict]:
    """Problèmes d'un passage : [{severite, code, message, ou}]."""
    cfg = story_config()["ecriture"]
    out = []

    def add(sev, code, msg):
        out.append({"severite": sev, "code": code, "message": msg, "ou": where})

    known = []
    for r in refs:
        f = facts.get(r)
        if not f:
            add("bloquant", "fait_inconnu", f"fait {r} absent du dossier factuel")
            continue
        known.append(f)
        if f["usage"] == "interdit":
            add("bloquant", "fait_interdit", f"{r} est « {f['statut']} » : ne peut pas être affirmé ({f['texte'][:70]}…)")
        elif f["usage"] == "attribution_obligatoire" and not has_marker(text, cfg["attribution"]):
            add("bloquant", "attribution_manquante",
                f"{r} ({f['statut']}, {f['type']}) doit être attribué à sa source dans la voix off")
        elif f["usage"] == "prudence_obligatoire" and not has_marker(text, cfg["prudence"]):
            add("bloquant", "prudence_manquante", f"{r} est une hypothèse : formulation prudente exigée")
    sourced = set()
    for f in known:
        sourced |= numbers(f["texte"])
        for p in f.get("preuves", []):
            sourced |= numbers(p["extrait"])
    for n in sorted(numbers(text)):
        if n not in sourced:
            add("bloquant", "chiffre_non_source", f"le nombre « {n} » n'apparaît dans aucun fait cité ni aucune preuve")
    return out
