"""Exports du projet narratif pour la phase 3 (Video Engine) et pour la relecture humaine.

Le storyboard JSON suit le schéma stable « lukoji.storyboard/1.0 » (docs/SCHEMA_STORYBOARD.md,
schemas/storyboard.schema.json). Les temps sont absolus en secondes depuis le début de la vidéo.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..db import Database, now
from .engine import _ctx, evaluate_all
from .project import current_versions, get_project
from .storyboard import scene_duration
from .text import speech_seconds, story_config

SCHEMA_ID = "lukoji.storyboard/1.0"
SCENE_KEYS = ("id", "sequence", "ordre", "debut_s", "fin_s", "duree_s", "voix_off", "visuel", "mouvement", "animation",
              "texte_ecran", "sources_visuelles", "recherche", "transition", "son", "risques_representation",
              "instructions_montage", "raison_narrative")


def build_storyboard_json(db: Database, sid: str) -> dict:
    project = get_project(db, sid)
    ctx = _ctx(db, project)
    if not (ctx["script"] and ctx["storyboard"]):
        raise ValueError("script et storyboard requis pour l'export")
    cfg = story_config()
    pause = cfg["rythme"]["pause_entre_sequences_s"]
    subj = db.conn.execute("SELECT uid FROM subjects WHERE id = ?", (project["subject_id"],)).fetchone()[0]
    facts = ctx["facts"]
    by_seq: dict = {}
    for s in ctx["storyboard"]["scenes"]:
        by_seq.setdefault(s["sequence"], []).append(s)
    t, sequences, scenes, order = 0.0, [], [], 0
    for i, seq in enumerate(ctx["script"]["sequences"]):
        start = t
        for s in by_seq.get(seq["id"], []):
            d = scene_duration(s)
            order += 1
            scenes.append({
                "id": s["id"], "sequence": seq["id"], "ordre": order, "debut_s": round(t, 2), "fin_s": round(t + d, 2),
                "duree_s": d, "voix_off": s.get("voix_off", ""),
                "visuel": {"type": s["type_visuel"], "authenticite": s["authenticite"], "mention_ecran": s.get("mention_ecran"),
                           "description": s["description"], "sujet": s["sujet"], "composition": s["composition"],
                           "cadrage": s["cadrage"]},
                "mouvement": {"camera": s["mouvement_camera"], "graphique": s["mouvement_graphique"]},
                "animation": s.get("animation") or [], "texte_ecran": s.get("texte_ecran") or [],
                "sources_visuelles": s.get("sources_visuelles") or [], "recherche": s.get("recherche") or [],
                "transition": s["transition"], "son": {"ambiance": s["ambiance"], "effets": s.get("effets_sonores") or []},
                "risques_representation": s["risques_representation"], "instructions_montage": s["instructions_montage"],
                "raison_narrative": s["raison_narrative"],
            })
            t += d
        sources = []
        for r in seq.get("faits") or []:
            for p in (facts.get(r) or {}).get("preuves", []):
                if p["source"] not in sources:
                    sources.append(p["source"])
        sequences.append({"id": seq["id"], "titre": seq["titre"], "etape": seq["etape"], "voix_off": seq["voix_off"],
                          "debut_s": round(start, 2), "fin_s": round(t, 2), "duree_voix_s": speech_seconds(seq["voix_off"]),
                          "objectif": seq["objectif"], "emotion": seq["emotion"], "transition": seq.get("transition"),
                          "faits": seq.get("faits") or [], "sources": sources})
        if i < len(ctx["script"]["sequences"]) - 1:
            t += pause
    used = {r for s in sequences for r in s["faits"]}
    used_src = {x for s in sequences for x in s["sources"]}
    research = ctx["research"]
    return {
        "schema": SCHEMA_ID, "genere_le": now(),
        "projet": {"id": project["sid"], "titre": project["title"], "sujet": subj, "format": project["format"],
                   "profil_rendu": cfg["formats"][project["format"]]["profil_rendu"], "statut": project["status"],
                   "versions": current_versions(db, project)},
        "rythme": {"mots_par_minute": cfg["rythme"]["mots_par_minute"], "pause_entre_sequences_s": pause,
                   "duree_totale_s": round(t, 2)},
        "direction_artistique": ctx["visual"] or {},
        "sequences": sequences, "scenes": scenes,
        "faits": [{"ref": f["ref"], "texte": f["texte"], "statut": f["statut"], "usage": f["usage"]}
                  for f in research["faits"] if f["ref"] in used],
        "sources": [{"ref": s["ref"], "organisation": s["organisation"], "categorie": s["category"], "titre": s["title"],
                     "url": s["url"], "date_publication": s["published_at"]} for s in research["sources"] if s["ref"] in used_src],
    }


def validate_storyboard_json(doc: dict) -> list[str]:
    """Validation structurelle du schéma lukoji.storyboard/1.0 (sans dépendance externe)."""
    p = []
    if doc.get("schema") != SCHEMA_ID:
        p.append(f"schema ≠ {SCHEMA_ID}")
    for k in ("projet", "rythme", "direction_artistique", "sequences", "scenes", "faits", "sources"):
        if k not in doc:
            p.append(f"clé manquante : {k}")
    last = 0.0
    seq_ids = {s.get("id") for s in doc.get("sequences", [])}
    for sc in doc.get("scenes", []):
        for k in SCENE_KEYS:
            if k not in sc:
                p.append(f"scène {sc.get('id')} : clé manquante {k}")
        if sc.get("sequence") not in seq_ids:
            p.append(f"scène {sc.get('id')} : séquence inconnue")
        if not isinstance(sc.get("debut_s"), (int, float)) or sc["debut_s"] < last - 1e-6:
            p.append(f"scène {sc.get('id')} : début non croissant")
        else:
            last = sc["fin_s"]
        if abs(sc.get("fin_s", 0) - sc.get("debut_s", 0) - sc.get("duree_s", -1)) > 0.05:
            p.append(f"scène {sc.get('id')} : fin − début ≠ durée")
        for k in ("type", "authenticite", "description"):
            if not (sc.get("visuel") or {}).get(k):
                p.append(f"scène {sc.get('id')} : visuel.{k} manquant")
    return p


# ---------------------------------------------------------------------------
# Rendus Markdown
# ---------------------------------------------------------------------------
def script_md(sb: dict) -> str:
    o = [f"# Script — {sb['projet']['titre']}", "",
         f"`{sb['projet']['id']}` · sujet `{sb['projet']['sujet']}` · format {sb['projet']['format']} · "
         f"durée estimée {sb['rythme']['duree_totale_s']/60:.1f} min ({sb['rythme']['mots_par_minute']} mots/min) · "
         f"versions {sb['projet']['versions']}", ""]
    for s in sb["sequences"]:
        o += [f"## {s['id']} — {s['titre']}", "",
              f"*{s['debut_s']:.0f}–{s['fin_s']:.0f} s · voix {s['duree_voix_s']} s · étape {s['etape']} · "
              f"objectif : {s['objectif']} · émotion : {s['emotion']}*", "", s["voix_off"], "",
              f"Faits : {', '.join(s['faits']) or '—'} · Sources : {', '.join(s['sources']) or '—'}"
              + (f"  \nTransition : {s['transition']}" if s.get("transition") else ""), ""]
    o += ["## Sources", ""] + [f"- **{x['ref']}** [{x['categorie']}] {x['organisation']} — [{x['titre']}]({x['url']})"
                               f" ({x['date_publication'] or 'n.d.'})" for x in sb["sources"]]
    return "\n".join(o) + "\n"


def storyboard_md(sb: dict) -> str:
    o = [f"# Storyboard — {sb['projet']['titre']}", "",
         f"{len(sb['scenes'])} scènes · {sb['rythme']['duree_totale_s']/60:.1f} min · schéma `{sb['schema']}`", ""]
    for sc in sb["scenes"]:
        v = sc["visuel"]
        o += [f"### {sc['id']} · {sc['sequence']} · {sc['debut_s']:.1f}–{sc['fin_s']:.1f} s ({sc['duree_s']} s)", "",
              f"> {sc['voix_off'] or '(sans voix off)'}", "",
              f"- **Visuel** : {v['type']} · *{v['authenticite']}*" + (f" · mention à l'écran : « {v['mention_ecran']} »" if v.get("mention_ecran") else ""),
              f"- **Description** : {v['description']}",
              f"- **Sujet / composition / cadrage** : {v['sujet']} · {v['composition']} · {v['cadrage']}",
              f"- **Mouvement** : caméra {sc['mouvement']['camera']} · graphique : {sc['mouvement']['graphique']}"]
        if sc["animation"]:
            o.append(f"- **Animation** : {'; '.join(sc['animation'])}")
        if sc["texte_ecran"]:
            o.append(f"- **Texte à l'écran** : {' | '.join(sc['texte_ecran'])}")
        if sc["sources_visuelles"]:
            o.append(f"- **Sources visuelles envisagées** : {'; '.join(sc['sources_visuelles'])}")
        if sc["recherche"]:
            o.append(f"- **Recherche d'images** : {'; '.join(sc['recherche'])}")
        o += [f"- **Transition** : {sc['transition']}",
              f"- **Son** : {sc['son']['ambiance']}" + (f" · effets : {'; '.join(sc['son']['effets'])}" if sc['son']['effets'] else ""),
              f"- **Raison narrative** : {sc['raison_narrative']}",
              f"- **Risques de représentation** : {sc['risques_representation']}",
              f"- **Montage** : {sc['instructions_montage']}", ""]
    return "\n".join(o)


def visual_md(sb: dict) -> str:
    d = sb["direction_artistique"]
    o = [f"# Direction artistique — {sb['projet']['titre']}", ""]
    for k, v in d.items():
        o.append(f"## {k.replace('_', ' ').capitalize()}")
        o.append("")
        if isinstance(v, dict):
            o += [f"- **{kk}** : {vv}" for kk, vv in v.items()]
        elif isinstance(v, list):
            o += [f"- {x}" for x in v]
        else:
            o.append(str(v))
        o.append("")
    return "\n".join(o)


def verification_md(research: dict, sb: dict) -> str:
    used = {f["ref"] for f in sb["faits"]}
    o = ["# Rapport de vérification factuelle", "",
         f"Sujet `{research['sujet']}` · faits : {research['bilan']['faits']} · faits clés confirmés : "
         f"{research['bilan']['faits_cles_confirmes']} · sources : {research['bilan']['sources']} "
         f"(vérifiées : {research['bilan']['sources_verifiees']})", "",
         "## Analyse de l'angle", "", f"- Angle initial : {research['angle_initial']}"]
    for k, v in (research.get("analyse") or {}).items():
        o.append(f"- {k.replace('_', ' ')} : {v}")
    o += ["", "## Faits (✔ = utilisé dans le script)", "", "| Réf. | Utilisé | Statut | Usage | Fait | Preuves |", "|---|---|---|---|---|---|"]
    for f in research["faits"]:
        prv = "<br>".join(f"{p['source']} {p['organisation']} ({p['categorie']}, {p['position']}, {p['verification']})" for p in f["preuves"]) or "—"
        o.append(f"| {f['ref']} | {'✔' if f['ref'] in used else ''} | {f['statut']} | {f['usage']} | {f['texte']} | {prv} |")
    o += ["", "## Sources", "", "| Réf. | Cat. | Organisation | Titre | Publiée | Consultation | Limites |", "|---|---|---|---|---|---|---|"]
    for s in research["sources"]:
        o.append(f"| {s['ref']} | {s['category']} | {s['organisation']} | [{s['title']}]({s['url']}) | {s['published_at'] or 'n.d.'} | "
                 f"{s['consultation']} / {s['availability']} | {s['limitations'] or ''} |")
    return "\n".join(o) + "\n"


def qc_md(rep: dict) -> str:
    o = ["# Rapport de contrôle qualité", "", f"**Statut : {rep['statut']}** · score global {rep['score_global']}/100 · "
         f"bloquants {rep['bloquants']} · alertes {rep['alertes']} · versions {rep['versions']}", "",
         "| Catégorie | Score | Bloquants | Alertes |", "|---|---|---|---|"]
    for c, d in rep["categories"].items():
        o.append(f"| {c} | {d['score']:.0f} | {len(d['bloquants'])} | {len(d['alertes'])} |")
    o += ["", "## Indicateurs", ""] + [f"- {k} : {v}" for k, v in rep["indicateurs"].items()]
    for c, d in rep["categories"].items():
        if d["bloquants"] or d["alertes"]:
            o += ["", f"## {c}", ""]
            o += [f"- **BLOQUANT** [{p['ou']}] {p['message']}" for p in d["bloquants"]]
            o += [f"- alerte [{p['ou']}] {p['message']}" for p in d["alertes"]]
    if rep["suggestions"]:
        o += ["", "## Suggestions", ""] + [f"- `{s['code']}` : {s['suggestion']}" for s in rep["suggestions"]]
    return "\n".join(o) + "\n"


def hooks_md(hooks: dict, ev: dict) -> str:
    res = {r["id"]: r for r in ev["resultats"]}
    o = ["# Hooks", "", f"Choisi : **{ev['choix']['choisi']}** · recommandé par le moteur : **{ev['choix']['recommande']}**",
         f"Justification : {ev['choix']['justification'] or '—'}", ""]
    for h in hooks["hooks"]:
        r = res[h["id"]]
        o += [f"## {h['id']} — {h['type']} · score {r['score']} · {r['duree_s']} s" + (" · ÉLIMINÉ" if r["elimine"] else ""), "",
              f"> {h['voix_off']}", "", f"- Concept visuel : {h['concept_visuel']}", f"- Mouvement : {h['mouvement']}",
              f"- Son : {h['son']}", f"- Tension : {h['tension']}", f"- Lien avec la suite : {h['lien_suite']}",
              f"- Risques : {h['risques']}", f"- Faits : {', '.join(h.get('faits') or []) or '—'}",
              "- Notes : " + " · ".join(f"{k} {v['retenue']}/5" + (f" (plafond auto {v['plafond_auto']})" if v["plafond_auto"] else "")
                                       for k, v in r["criteres"].items()), ""]
        o += [f"  - {p['severite']} : {p['message']}" for p in r["problemes"]]
    return "\n".join(o) + "\n"


def export_bundle(db: Database, sid: str, out_dir: str | Path) -> dict:
    project = get_project(db, sid)
    ctx = _ctx(db, project)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sb = build_storyboard_json(db, sid)
    problems = validate_storyboard_json(sb)
    if problems:
        raise ValueError("export non conforme au schéma : " + " ; ".join(problems[:5]))
    rep = evaluate_all(db, project)
    from .hooks import evaluate as hk_eval
    files = {
        "storyboard.json": json.dumps(sb, ensure_ascii=False, indent=1),
        "script.md": script_md(sb),
        "storyboard.md": storyboard_md(sb),
        "direction_artistique.md": visual_md(sb),
        "verification_factuelle.md": verification_md(ctx["research"], sb),
        "qc.md": qc_md(rep),
        "qc.json": json.dumps(rep, ensure_ascii=False, indent=1),
        "hooks.md": hooks_md(ctx["hooks"], hk_eval(ctx["hooks"], ctx["facts"])),
        "bundle.json": json.dumps({"schema": "lukoji.bundle/1.0", "projet": sb["projet"], "recherche": ctx["research"],
                                   "hooks": ctx["hooks"], "structure": ctx["structure"], "script": ctx["script"],
                                   "storyboard": sb, "direction_artistique": ctx["visual"], "qc": rep},
                                  ensure_ascii=False, indent=1),
    }
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
    return {"dossier": str(out), "fichiers": sorted(files), "qc": rep["statut"], "score": rep["score_global"]}
