"""NARRATIVE ENGINE : catalogue de structures, choix justifié, contrôle de la structure d'un projet.

La structure n'est jamais imposée. L'auteur choisit dans le catalogue, justifie, écarte explicitement les
alternatives ; le moteur vérifie la cohérence (ouverture, conclusion, nuance, faits utilisables, durées).
"""
from __future__ import annotations

from .text import story_config

CATALOGUE = {
    "chronologie": {"label": "Chronologie historique",
                    "quand": "Événements dont l'ordre explique le sens ; risque : liste de dates sans tension."},
    "probleme_solution_consequences": {"label": "Problème, solution, conséquences",
                                       "quand": "Innovation répondant à un besoin clair ; risque : ton promotionnel."},
    "enquete": {"label": "Enquête", "quand": "Question ouverte, sources contradictoires, révélation documentée."},
    "portrait": {"label": "Portrait d'une entreprise ou d'une personne", "quand": "Trajectoire portée par un acteur central."},
    "decouverte_progressive": {"label": "Découverte progressive",
                               "quand": "Mécanisme mal connu dévoilé couche après couche."},
    "conflit_resolution": {"label": "Conflit et résolution", "quand": "Opposition d'acteurs identifiés et documentée."},
    "transformation": {"label": "Transformation",
                       "quand": "Un objet ou une société change de nature ; le tournant est au cœur du récit."},
    "comparaison": {"label": "Comparaison", "quand": "Deux modèles ou deux époques éclairés l'un par l'autre."},
    "rebondissements": {"label": "Histoire à rebondissements documentés",
                        "quand": "Plusieurs retournements attestés ; risque : dramatisation."},
}
ROLES = ("hook", "contexte", "probleme", "origine", "developpement", "obstacles", "tournant", "consequences",
         "limites", "conclusion", "autre")


def evaluate(doc: dict, facts: dict, fmt: str) -> dict:
    cfg = story_config()
    p: list[dict] = []

    def add(sev, code, msg, where="structure"):
        p.append({"severite": sev, "code": code, "message": msg, "ou": where})

    t = doc.get("type")
    if t not in CATALOGUE:
        add("bloquant", "structure_inconnue", f"type {t!r} hors catalogue ({', '.join(CATALOGUE)})")
    if not str(doc.get("justification") or "").strip():
        add("bloquant", "justification_manquante", "le choix de structure doit être justifié")
    if not doc.get("alternatives_ecartees"):
        add("alerte", "alternatives", "aucune alternative écartée explicitement")
    if not str(doc.get("angle") or "").strip():
        add("bloquant", "angle_manquant", "angle narratif manquant")
    steps = doc.get("etapes") or []
    if len(steps) < 5:
        add("bloquant", "etapes", f"{len(steps)} étape(s) : structure trop pauvre (5 minimum)")
    roles = [s.get("role") for s in steps]
    for s in steps:
        where = f"étape {s.get('id')}"
        if s.get("role") not in ROLES:
            add("bloquant", "role_inconnu", f"rôle inconnu {s.get('role')!r}", where)
        for k in ("id", "titre", "objectif"):
            if not str(s.get(k) or "").strip():
                add("bloquant", "champ_manquant", f"champ « {k} » manquant", where)
        for r in s.get("faits") or []:
            f = facts.get(r)
            if not f:
                add("bloquant", "fait_inconnu", f"fait {r} absent du dossier factuel", where)
            elif f["usage"] == "interdit":
                add("bloquant", "fait_interdit", f"{r} est « {f['statut']} » : inutilisable comme fait", where)
    if roles and roles[0] != "hook":
        add("bloquant", "ouverture", "la première étape doit être l'ouverture (hook)")
    if roles and roles[-1] != "conclusion":
        add("bloquant", "conclusion", "la dernière étape doit être la conclusion")
    if "limites" not in roles:
        add("alerte", "nuance_absente", "aucune étape « limites » : risque de récit promotionnel")
    total = sum(float(s.get("duree_cible_s") or 0) for s in steps)
    f = cfg["formats"][fmt]
    if not f["duree_min_s"] <= total <= f["duree_max_s"]:
        add("alerte", "duree_structure", f"durée cible totale {total:.0f} s hors format ({f['duree_min_s']}–{f['duree_max_s']} s)")
    return {"type": t, "label": CATALOGUE.get(t, {}).get("label"), "etapes": len(steps), "duree_cible_s": total,
            "roles": roles, "problemes": p}
