"""HOOK ENGINE : ouvertures audiovisuelles, contrôle, notation, sélection.

Un hook est une OUVERTURE (voix off + image + mouvement + son), pas un titre prononcé. Les propositions sont
rédigées par l'auteur ; le moteur :
- exige au moins 8 propositions couvrant les 8 approches ;
- calcule la durée de la voix off ;
- vérifie les faits (règles d'usage, chiffres sourcés) et la surenchère (lexique sensationnaliste) ;
- note chaque hook (8 critères 1–5 justifiés, pondérés) puis applique des plafonds AUTOMATIQUES :
  un problème factuel élimine le hook ; un mot de surenchère plafonne « honnêteté de la promesse » à 2 ;
- recommande le meilleur hook NON éliminé (jamais le plus spectaculaire par défaut).
"""
from __future__ import annotations

from .factcheck import check_passage
from .text import find_cliches, norm, speech_seconds, story_config, word_count

FIELDS = ("id", "type", "voix_off", "concept_visuel", "mouvement", "son", "tension", "lien_suite", "risques", "faits", "notes")


def evaluate(doc: dict, facts: dict) -> dict:
    cfg = story_config()
    hc = cfg["hooks"]
    problems: list[dict] = []
    hooks = doc.get("hooks") or []
    if len(hooks) < hc["minimum"]:
        problems.append({"severite": "bloquant", "code": "hooks_insuffisants", "message": f"{len(hooks)} hook(s) : {hc['minimum']} minimum", "ou": "hooks"})
    missing_types = [t for t in hc["types"] if t not in {h.get("type") for h in hooks}]
    if missing_types:
        problems.append({"severite": "bloquant", "code": "types_manquants", "message": f"approches absentes : {', '.join(missing_types)}", "ou": "hooks"})
    ids = [h.get("id") for h in hooks]
    if len(set(ids)) != len(ids):
        problems.append({"severite": "bloquant", "code": "id_double", "message": "identifiants de hooks en double", "ou": "hooks"})
    results = []
    for h in hooks:
        where = f"hook {h.get('id')}"
        hp: list[dict] = []
        for f in FIELDS:
            if not h.get(f) and f != "faits":
                hp.append({"severite": "bloquant", "code": "champ_manquant", "message": f"champ « {f} » manquant", "ou": where})
        if h.get("type") not in hc["types"]:
            hp.append({"severite": "bloquant", "code": "type_inconnu", "message": f"type inconnu {h.get('type')!r}", "ou": where})
        vo = h.get("voix_off", "")
        dur = speech_seconds(vo)
        if not hc["duree_min_s"] <= dur <= hc["duree_max_s"]:
            hp.append({"severite": "alerte", "code": "duree_hook", "message": f"{dur} s (attendu {hc['duree_min_s']}–{hc['duree_max_s']} s)", "ou": where})
        hp += check_passage(vo, h.get("faits") or [], facts, where)
        sens = [w for w in hc["lexique_sensationnel"] if norm(w) in norm(vo)]
        if sens:
            hp.append({"severite": "alerte", "code": "surenchere", "message": f"vocabulaire de surenchère : {', '.join(sens)}", "ou": where})
        cl = find_cliches(vo, cfg["ecriture"]["cliches"])
        if cl:
            hp.append({"severite": "alerte", "code": "cliche", "message": f"formules creuses : {', '.join(cl)}", "ou": where})
        # Notation
        notes = h.get("notes") or {}
        detail, total = {}, 0.0
        for crit, w in hc["criteres"].items():
            e = notes.get(crit) or {}
            n = e.get("note") if isinstance(e.get("note"), int) and 1 <= e.get("note") <= 5 else None
            if n is None or not str(e.get("justification") or "").strip():
                hp.append({"severite": "bloquant", "code": "note_manquante", "message": f"note justifiée manquante : {crit}", "ou": where})
                n = 1
            plafond = None
            if crit == "honnetete_promesse" and sens:
                plafond = 2
            if crit == "coherence_preuves" and any(p["severite"] == "bloquant" and p["code"] in
                                                   ("fait_interdit", "chiffre_non_source", "attribution_manquante",
                                                    "prudence_manquante", "fait_inconnu") for p in hp):
                plafond = 1
            applied = min(n, plafond) if plafond else n
            detail[crit] = {"note": n, "retenue": applied, "plafond_auto": plafond, "poids": w,
                            "justification": e.get("justification", "")}
            total += w * (applied - 1) / 4
        elimine = any(p["severite"] == "bloquant" for p in hp)
        results.append({"id": h.get("id"), "type": h.get("type"), "mots": word_count(vo), "duree_s": dur,
                        "score": round(total * 100, 1), "elimine": elimine, "criteres": detail, "problemes": hp})
        problems += hp
    ok = [r for r in results if not r["elimine"]]
    best = max(ok, key=lambda r: (r["score"], r["criteres"].get("coherence_preuves", {}).get("retenue", 0)), default=None)
    chosen = doc.get("choisi")
    choice = {"recommande": best["id"] if best else None, "choisi": chosen,
              "justification": doc.get("justification_choix", "")}
    if chosen:
        r = next((x for x in results if x["id"] == chosen), None)
        if not r:
            problems.append({"severite": "bloquant", "code": "choix_inconnu", "message": f"hook choisi inconnu : {chosen}", "ou": "hooks"})
        elif r["elimine"]:
            problems.append({"severite": "bloquant", "code": "choix_elimine", "message": f"le hook choisi {chosen} est éliminé (problème factuel ou champ manquant)", "ou": "hooks"})
        elif best and chosen != best["id"] and not choice["justification"]:
            problems.append({"severite": "alerte", "code": "choix_non_justifie", "message": f"choix {chosen} ≠ recommandation {best['id']} sans justification", "ou": "hooks"})
    else:
        problems.append({"severite": "bloquant", "code": "aucun_choix", "message": "aucun hook choisi", "ou": "hooks"})
    return {"resultats": sorted(results, key=lambda r: (r["elimine"], -r["score"])), "choix": choice, "problemes": problems}


def chosen_hook(doc: dict) -> dict | None:
    return next((h for h in doc.get("hooks", []) if h.get("id") == doc.get("choisi")), None)
