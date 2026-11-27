"""Projet narratif SIMULÉ pour les tests du Story Engine (données fictives, jamais présentées comme réelles)."""
import copy

TYPES = ["paradoxal", "historique", "narratif", "tension", "consequence", "question", "revelation", "cinematographique"]
CRIT = ["curiosite", "clarte", "originalite", "tension", "pertinence", "coherence_preuves", "potentiel_visuel", "honnetete_promesse"]


def notes(n=4):
    return {c: {"note": n, "justification": "test"} for c in CRIT}


def hooks(refs):
    """refs : faits confirmés du dossier simulé (ex. F1, F2)."""
    a = refs[0]
    hs = []
    for i, t in enumerate(TYPES, start=1):
        hs.append({"id": f"H{i}", "type": t,
                   "voix_off": "Une coopérative de Goma réunit aujourd'hui des producteurs autour d'un projet commun. Son histoire commence pourtant par une idée modeste.",
                   "concept_visuel": "carte", "mouvement": "zoom", "son": "nappe", "tension": "contraste", "lien_suite": "contexte",
                   "risques": "aucun", "faits": [a], "notes": notes(4 if i > 1 else 5)})
    return {"hooks": hs, "choisi": "H1", "justification_choix": "meilleur score"}


def structure(refs):
    roles = ["hook", "contexte", "origine", "tournant", "developpement", "limites", "conclusion"]
    return {"type": "transformation", "justification": "test", "alternatives_ecartees": [{"type": "chronologie", "raison": "test"}],
            "angle": "angle de test", "etapes": [{"id": f"E{i}", "role": r, "titre": r, "objectif": "objectif", "faits": [refs[0]],
                                                  "duree_cible_s": 60} for i, r in enumerate(roles, start=1)]}


PHRASE = ("Les membres de la coopérative se retrouvent chaque semaine pour décider ensemble des prochaines étapes du projet commun. "
          "Ils discutent des prix, des routes et des besoins des familles qui vivent autour de la ville. ")


def script(refs, n_seq=7, filler=4):
    seqs = []
    for i in range(1, n_seq + 1):
        vo = PHRASE * filler
        if i == 1:
            vo = hooks(refs)["hooks"][0]["voix_off"] + " " + vo
        seqs.append({"id": f"SEQ-{i:02d}", "etape": f"E{i}", "titre": f"Séquence {i}", "voix_off": vo.strip(),
                     "objectif": "objectif", "faits": [refs[0]], "emotion": "intérêt",
                     "transition": "suite" if i < n_seq else ""})
    return {"titre": "Projet simulé", "sequences": seqs}


VTYPES = ["carte", "graphique", "archive_photo", "typographie_animee", "plan_ambiance", "infographie", "document", "animation"]


def storyboard(script_doc):
    from lukoji_engine.story.text import sentences
    scenes, k = [], 0
    for s in script_doc["sequences"]:
        ss = sentences(s["voix_off"])
        for j in range(0, len(ss), 2):
            t = VTYPES[k % len(VTYPES)]
            auth = {"archive_photo": "authentique", "document": "authentique", "plan_ambiance": "symbolique",
                    "animation": "illustration"}.get(t, "graphique_explicatif")
            sc = {"id": f"SC-{k + 1:03d}", "sequence": s["id"], "voix_off": " ".join(ss[j:j + 2]), "type_visuel": t,
                  "authenticite": auth, "description": "d", "sujet": "s", "composition": "c", "cadrage": "plan large",
                  "mouvement_camera": "fixe", "mouvement_graphique": "aucun", "transition": "coupe", "ambiance": "nappe",
                  "instructions_montage": "caler sur la voix", "raison_narrative": "raison", "risques_representation": "aucun",
                  "sources_visuelles": ["source simulée"] if auth == "authentique" else []}
            if auth in ("symbolique", "illustration"):
                sc["mention_ecran"] = "IMAGE D'ILLUSTRATION"
            scenes.append(sc)
            k += 1
    return {"scenes": scenes}


def visual():
    cats = {c: "règle" for c in ("authentique", "illustration", "reconstitution", "graphique_explicatif", "image_generee", "symbolique")}
    return {"style_general": "sobre et graphique", "atmosphere": "calme", "palette": {"dominantes": ["#0B0B0B", "#F6F6F3"], "accents": ["#FF8A00"]},
            "typographie": {"titres": "Archivo Black", "labels": "IBM Plex Mono"}, "realisme": "documentaire", "archives": "sourcées",
            "cartes": "aplats", "graphiques": "plats", "motion": "doux", "transitions": "coupes", "sound_design": "sobre",
            "categories_visuelles": cats}


def analyse():
    return {"angle_retenu": "angle", "verdict_angle": "confirme", "justification": "preuves suffisantes (simulées)"}


def deep(x):
    return copy.deepcopy(x)
