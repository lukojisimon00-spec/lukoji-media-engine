"""STORY QUALITY CONTROL : contrôle factuel, narratif, script, visuel et durée.

Score par catégorie = 100 − 30 × bloquants − 6 × alertes (min. 0) ; score global = moyenne pondérée
(config/story.toml › [qc].poids). Statut : « bloque » dès qu'UNE erreur bloquante existe, quel que soit le
score ; « a_revoir » si des alertes subsistent ; « valide » sinon. Un score élevé ne masque jamais un bloquant.
"""
from __future__ import annotations

from .text import story_config

CATEGORY_OF = {
    # factuel
    "fait_inconnu": "factuel", "fait_interdit": "factuel", "attribution_manquante": "factuel", "prudence_manquante": "factuel",
    "chiffre_non_source": "factuel", "recherche_bloquante": "factuel", "recherche_alerte": "factuel",
    # durée
    "duree_hors_format": "duree", "duree_structure": "duree", "duree_hook": "duree", "duree_scene": "duree",
    "duree_trop_courte": "duree", "duree_absente": "duree", "desynchro_duree": "duree",
    # script
    "phrase_longue": "script", "cliche": "script", "transition_generique": "script", "repetition": "script",
    "transition_manquante": "script",
    # visuel
    "type_inconnu": "visuel", "authenticite_inconnue": "visuel", "authenticite_incoherente": "visuel",
    "mention_manquante": "visuel", "archive_non_identifiee": "visuel", "mouvement_inconnu": "visuel", "monotonie": "visuel",
    "zooms_lents": "visuel", "variete_faible": "visuel", "voix_off_desynchronisee": "visuel", "sequence_sans_scene": "visuel",
    "sequence_inconnue": "visuel", "couleur_invalide": "visuel", "couleur_hors_charte": "visuel", "typo_charte": "visuel",
    "categorie_non_definie": "visuel", "direction_repetitive": "visuel",
}
SUGGESTIONS = {
    "attribution_manquante": "Attribuer le fait dans la phrase (« selon … », « d'après … », « estime … »).",
    "chiffre_non_source": "Retirer le nombre, l'écrire en toutes lettres s'il n'est pas un fait, ou citer le fait qui le contient.",
    "fait_interdit": "Retirer l'affirmation ou compléter la recherche pour confirmer le fait.",
    "prudence_manquante": "Formuler l'hypothèse avec prudence (« pourrait », « semble », « reste à établir »).",
    "phrase_longue": "Couper la phrase en deux : une idée par phrase en voix off.",
    "cliche": "Remplacer la formule creuse par un fait ou une image concrète.",
    "repetition": "Varier le vocabulaire ou supprimer la redite.",
    "transition_generique": "Faire naître la transition de l'histoire (une question, une conséquence, un contraste).",
    "duree_hors_format": "Couper ou développer des séquences pour revenir dans la fourchette du format.",
    "mention_manquante": "Ajouter une mention à l'écran (« Reconstitution », « Illustration », « Image symbolique »).",
    "archive_non_identifiee": "Identifier l'archive (fonds, licence) ou requalifier le visuel en image symbolique avec mention.",
    "monotonie": "Alterner les types de visuels (carte, archive, typographie, graphique, plan d'ambiance).",
    "zooms_lents": "Remplacer des zooms lents par des mouvements motivés (insert, parallaxe, suivi de tracé).",
    "voix_off_desynchronisee": "Redécouper les segments de voix off des scènes pour reconstituer exactement la séquence.",
    "aucun_choix": "Choisir un hook (le recommandé ou un autre, avec justification).",
    "nuance_absente": "Ajouter une étape « limites » : critiques, coûts, controverses documentées.",
}


def categorize(problem: dict) -> str:
    c = CATEGORY_OF.get(problem["code"])
    if c:
        return c
    o = problem.get("ou", "")
    if o.startswith(("scène", "storyboard", "direction")):
        return "visuel"
    if o.startswith(("hook", "structure", "étape")) or problem["code"] in ("etapes_non_couvertes", "nuance_absente", "hook_absent"):
        return "narratif"
    if o.startswith(("séquence", "script")):
        return "script"
    return "narratif"


def build_report(sections: dict, versions: dict, info: dict) -> dict:
    """sections : {nom: [problèmes]} ; info : indicateurs (durées, hook, mots…)."""
    cfg = story_config()["qc"]
    cats = {c: {"bloquants": [], "alertes": [], "score": 100.0} for c in cfg["poids"]}
    for section, problems in sections.items():
        for pb in problems:
            pb = dict(pb, section=section)
            cat = categorize(pb)
            cats[cat]["bloquants" if pb["severite"] == "bloquant" else "alertes"].append(pb)
    for c, d in cats.items():
        d["score"] = max(0.0, 100.0 - 30 * len(d["bloquants"]) - 6 * len(d["alertes"]))
    glob = round(sum(cfg["poids"][c] * cats[c]["score"] for c in cats), 1)
    nb_b = sum(len(d["bloquants"]) for d in cats.values())
    nb_a = sum(len(d["alertes"]) for d in cats.values())
    status = "bloque" if nb_b else ("a_revoir" if nb_a else "valide")
    seen, sugg = set(), []
    for d in cats.values():
        for pb in d["bloquants"] + d["alertes"]:
            s = SUGGESTIONS.get(pb["code"])
            if s and pb["code"] not in seen:
                seen.add(pb["code"])
                sugg.append({"code": pb["code"], "suggestion": s})
    return {"statut": status, "score_global": glob, "bloquants": nb_b, "alertes": nb_a,
            "categories": cats, "suggestions": sugg, "versions": versions, "indicateurs": info}


def stage_blocking(report: dict, stage: str) -> list[dict]:
    """Bloquants pertinents pour valider une étape."""
    sections = {"structure": {"recherche", "hooks", "structure"},
                "script": {"recherche", "hooks", "structure", "script"},
                "storyboard": {"recherche", "hooks", "structure", "script", "storyboard", "direction"}}[stage]
    return [pb for d in report["categories"].values() for pb in d["bloquants"] if pb["section"] in sections]
