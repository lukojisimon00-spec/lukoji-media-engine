"""STORYBOARD ENGINE : scènes synchronisées avec la voix off, intentions visuelles contrôlées.

Contrôles : découpage EXACT de la voix off (les segments des scènes d'une séquence reconstituent mot pour mot
sa voix off), durées, champs requis, variété des visuels (pas de suite de zooms lents sur images génériques),
authenticité (une reconstitution, illustration, image symbolique ou générée porte une mention à l'écran et
n'est jamais présentée comme l'événement réel), raison narrative de chaque visuel.
"""
from __future__ import annotations

from .text import norm, speech_seconds, story_config

FIELDS = ("id", "sequence", "type_visuel", "authenticite", "description", "sujet", "composition", "cadrage",
          "mouvement_camera", "mouvement_graphique", "transition", "ambiance", "instructions_montage",
          "raison_narrative", "risques_representation")


def scene_duration(sc: dict) -> float:
    spoken = speech_seconds(sc.get("voix_off", "")) if sc.get("voix_off") else 0.0
    declared = sc.get("duree_s")
    return round(max(spoken, float(declared)) if declared else spoken, 1)


def evaluate(doc: dict, script: dict) -> dict:
    cfg = story_config()["storyboard"]
    p: list[dict] = []
    scenes = doc.get("scenes") or []

    def add(sev, code, msg, where):
        p.append({"severite": sev, "code": code, "message": msg, "ou": where})

    seq_vo = {s["id"]: s.get("voix_off", "") for s in script.get("sequences", [])}
    by_seq: dict[str, list] = {}
    computed = []
    for sc in scenes:
        where = f"scène {sc.get('id')}"
        for f in FIELDS:
            if not str(sc.get(f) or "").strip():
                add("bloquant", "champ_manquant", f"champ « {f} » manquant", where)
        if sc.get("sequence") not in seq_vo:
            add("bloquant", "sequence_inconnue", f"séquence {sc.get('sequence')!r} absente du script", where)
        if sc.get("type_visuel") not in cfg["types_visuels"]:
            add("bloquant", "type_inconnu", f"type visuel inconnu {sc.get('type_visuel')!r}", where)
        auth = sc.get("authenticite")
        if auth not in cfg["authenticite"]:
            add("bloquant", "authenticite_inconnue", f"authenticité inconnue {auth!r}", where)
        if sc.get("type_visuel") == "image_generee" and auth != "image_generee":
            add("bloquant", "authenticite_incoherente", "image générée non déclarée comme telle", where)
        if sc.get("type_visuel") == "reconstitution" and auth != "reconstitution":
            add("bloquant", "authenticite_incoherente", "reconstitution non déclarée comme telle", where)
        if auth in cfg["mention_obligatoire"] and not str(sc.get("mention_ecran") or "").strip():
            add("bloquant", "mention_manquante", f"« {auth} » sans mention à l'écran : risque de passer pour un document réel", where)
        if auth == "authentique" and not sc.get("sources_visuelles"):
            add("alerte", "archive_non_identifiee", "visuel « authentique » sans source identifiée : à trouver, sinon passer en symbolique", where)
        if sc.get("mouvement_camera") and sc["mouvement_camera"] not in cfg["mouvements_camera"]:
            add("alerte", "mouvement_inconnu", f"mouvement caméra non standard {sc['mouvement_camera']!r}", where)
        d = scene_duration(sc)
        if not sc.get("voix_off") and not sc.get("duree_s"):
            add("bloquant", "duree_absente", "scène sans voix off : durée à déclarer", where)
        if d and not cfg["duree_scene_min_s"] <= d <= cfg["duree_scene_max_s"]:
            add("alerte", "duree_scene", f"{d} s (attendu {cfg['duree_scene_min_s']}–{cfg['duree_scene_max_s']} s)", where)
        if sc.get("duree_s") and sc.get("voix_off") and float(sc["duree_s"]) < speech_seconds(sc["voix_off"]) * 0.9:
            add("bloquant", "duree_trop_courte", "durée déclarée plus courte que la voix off", where)
        by_seq.setdefault(sc.get("sequence"), []).append(sc)
        computed.append({"id": sc.get("id"), "sequence": sc.get("sequence"), "duree_s": d, "type": sc.get("type_visuel"),
                         "authenticite": auth})
    # Découpage exact de la voix off.
    for sid, vo in seq_vo.items():
        parts = [sc.get("voix_off", "") for sc in by_seq.get(sid, []) if sc.get("voix_off")]
        if not by_seq.get(sid):
            add("bloquant", "sequence_sans_scene", "aucune scène pour cette séquence", f"séquence {sid}")
        elif norm(" ".join(parts)) != norm(vo):
            add("bloquant", "voix_off_desynchronisee", "les segments des scènes ne reconstituent pas exactement la voix off", f"séquence {sid}")
    # Variété.
    types = [sc.get("type_visuel") for sc in scenes]
    run, mx = 1, 1
    for a, b in zip(types, types[1:]):
        run = run + 1 if a == b else 1
        mx = max(mx, run)
        if run > cfg["max_meme_type_consecutif"]:
            add("alerte", "monotonie", f"{run} scènes « {b} » consécutives", "storyboard")
    slow = sum(1 for sc in scenes if sc.get("mouvement_camera") in ("zoom_avant_lent", "zoom_arriere_lent"))
    if scenes and slow / len(scenes) > cfg["part_max_zoom_lent"]:
        add("alerte", "zooms_lents", f"{slow}/{len(scenes)} scènes en zoom lent (max {cfg['part_max_zoom_lent']:.0%})", "storyboard")
    distinct = len(set(types))
    if distinct < 6:
        add("alerte", "variete_faible", f"seulement {distinct} types de visuels", "storyboard")
    ids = [sc.get("id") for sc in scenes]
    if len(set(ids)) != len(ids):
        add("bloquant", "id_double", "identifiants de scènes en double", "storyboard")
    total = round(sum(c["duree_s"] for c in computed), 1)
    return {"scenes": computed, "nb_scenes": len(scenes), "duree_s": total, "types_distincts": distinct,
            "repartition_types": {t: types.count(t) for t in sorted(set(types), key=str)},
            "repartition_authenticite": {a: [c["authenticite"] for c in computed].count(a) for a in sorted({c["authenticite"] for c in computed}, key=str)},
            "part_zoom_lent": round(slow / len(scenes), 2) if scenes else 0, "problemes": p}
