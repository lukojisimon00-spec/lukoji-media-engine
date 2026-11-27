"""Orchestration du Story Engine : enregistrer, contrôler, valider, modifier, finaliser."""
from __future__ import annotations

import json

from ..db import Database, now
from . import hooks as hk, narrative, qc as sqc, script as sc, storyboard as sb, visual as vd
from .factcheck import facts_index
from .project import (ORDER, StoryError, current, current_versions, get_project, record_approval, save_artifact,
                      set_status, stale)
from .text import story_config


def _ctx(db: Database, project: dict) -> dict:
    out = {}
    for k in ("research", "hooks", "structure", "script", "storyboard", "visual"):
        c = current(db, project, k)
        out[k] = c["content"] if c else None
    out["facts"] = facts_index(out["research"] or {})
    return out


def evaluate_all(db: Database, project: dict) -> dict:
    ctx = _ctx(db, project)
    fmt = project["format"]
    res: dict = {}
    sections: dict = {}
    r = ctx["research"] or {}
    sections["recherche"] = [{"severite": "bloquant", "code": "recherche_bloquante", "message": m, "ou": "recherche"} for m in r.get("bloquant", [])] \
        + [{"severite": "alerte", "code": "recherche_alerte", "message": m, "ou": "recherche"} for m in r.get("alertes", [])]
    if ctx["hooks"]:
        res["hooks"] = hk.evaluate(ctx["hooks"], ctx["facts"])
        sections["hooks"] = res["hooks"]["problemes"]
    if ctx["structure"]:
        res["structure"] = narrative.evaluate(ctx["structure"], ctx["facts"], fmt)
        sections["structure"] = res["structure"]["problemes"]
    if ctx["script"] and ctx["structure"] and ctx["hooks"]:
        res["script"] = sc.evaluate(ctx["script"], ctx["facts"], ctx["structure"], ctx["hooks"], fmt)
        sections["script"] = res["script"]["problemes"]
    if ctx["visual"]:
        others = []
        for row in db.conn.execute("SELECT a.content_json FROM story_artifacts a WHERE a.kind = 'visual' AND a.project_id != ?"
                                   " AND a.version = (SELECT MAX(version) FROM story_artifacts b WHERE b.project_id = a.project_id"
                                   " AND b.kind = 'visual')", (project["id"],)):
            others.append(json.loads(row[0]))
        res["direction"] = vd.evaluate(ctx["visual"], others)
        sections["direction"] = res["direction"]["problemes"]
    if ctx["storyboard"] and ctx["script"]:
        res["storyboard"] = sb.evaluate(ctx["storyboard"], ctx["script"])
        sections["storyboard"] = res["storyboard"]["problemes"]
        if res.get("script"):
            d_sc, d_sb = res["script"]["duree_s"], res["storyboard"]["duree_s"]
            tol = story_config()["storyboard"]["tolerance_synchro"]
            if d_sb and abs(d_sb - d_sc) / d_sc > tol:
                sections["storyboard"].append({"severite": "alerte", "code": "desynchro_duree",
                                               "message": f"storyboard {d_sb} s vs script {d_sc} s", "ou": "storyboard"})
    st = stale(db, project)
    for k, why in st.items():
        sections.setdefault(k if k != "visual" else "direction", []).append(
            {"severite": "bloquant", "code": "element_obsolete", "message": f"{k} construit sur une version périmée : {why}", "ou": k})
    info = {}
    if res.get("hooks"):
        best = next((x for x in res["hooks"]["resultats"] if x["id"] == res["hooks"]["choix"]["choisi"]), None)
        info["hook_choisi"] = res["hooks"]["choix"]["choisi"]
        info["hook_recommande"] = res["hooks"]["choix"]["recommande"]
        info["hook_score"] = best["score"] if best else None
    if res.get("script"):
        info.update(script_mots=res["script"]["mots"], script_duree_s=res["script"]["duree_s"],
                    sequences=len(res["script"]["sequences"]))
    if res.get("storyboard"):
        info.update(scenes=res["storyboard"]["nb_scenes"], storyboard_duree_s=res["storyboard"]["duree_s"],
                    types_visuels=res["storyboard"]["types_distincts"])
    report = sqc.build_report(sections, current_versions(db, project), info)
    report["details"] = res
    return report


def run_qc(db: Database, sid: str, actor: str = "moteur") -> dict:
    project = get_project(db, sid)
    report = evaluate_all(db, project)
    with db.tx():
        qid = db.conn.execute("INSERT INTO story_qc (project_id, versions_json, report_json, status, score, run_at) VALUES (?,?,?,?,?,?)",
                              (project["id"], json.dumps(report["versions"]), json.dumps(report, ensure_ascii=False),
                               report["statut"], report["score_global"], now())).lastrowid
    report["qc_id"] = qid
    # Passage en revue : l'étape en brouillon sans bloquant pertinent passe « *_review ».
    st = project["status"]
    for stage in ("script", "storyboard"):
        if st == f"{stage}_draft" and not sqc.stage_blocking(report, stage):
            set_status(db, project, f"{stage}_review", f"contrôle qualité n° {qid} sans erreur bloquante", actor)
    return report


def latest_qc(db: Database, project: dict) -> dict | None:
    r = db.conn.execute("SELECT id, report_json FROM story_qc WHERE project_id = ? ORDER BY id DESC LIMIT 1", (project["id"],)).fetchone()
    if not r:
        return None
    rep = json.loads(r["report_json"])
    rep["qc_id"] = r["id"]
    return rep


def approve(db: Database, sid: str, stage: str, actor: str, note: str = "") -> dict:
    project = get_project(db, sid)
    expected = {"structure": "structure_draft", "script": "script_review", "storyboard": "storyboard_review"}
    if stage not in expected:
        raise StoryError("étape à valider : structure | script | storyboard")
    if project["status"] != expected[stage]:
        raise StoryError(f"validation de « {stage} » impossible depuis le statut « {project['status']} » (attendu : {expected[stage]})")
    rep = latest_qc(db, project)
    if not rep or rep["versions"] != current_versions(db, project):
        raise StoryError("lancer d'abord le contrôle qualité sur les versions courantes (`story qc`)")
    blocking = sqc.stage_blocking(rep, stage)
    if blocking:
        raise StoryError(f"{len(blocking)} erreur(s) bloquante(s) : " + " ; ".join(f"[{b['ou']}] {b['message']}" for b in blocking[:5]))
    record_approval(db, project, stage, rep["qc_id"], actor, note)
    project = set_status(db, project, f"{stage}_approved", f"validé par {actor}" + (f" : {note}" if note else ""), actor)
    # L'étape suivante s'ouvre ; si des brouillons anticipés existent, le projet passe à leur brouillon.
    nxt = {"structure": ("script", ["script"]), "script": ("storyboard", ["storyboard", "visual"])}.get(stage)
    if nxt and any(current(db, project, k) for k in nxt[1]):
        project = set_status(db, project, f"{nxt[0]}_draft", "brouillon anticipé repris après validation", actor)
    return project


def finalize(db: Database, sid: str, actor: str, note: str = "") -> dict:
    project = get_project(db, sid)
    if project["status"] != "storyboard_approved":
        raise StoryError(f"finalisation impossible depuis « {project['status']} » (storyboard_approved requis)")
    rep = run_qc(db, sid, actor)
    if rep["bloquants"]:
        raise StoryError(f"{rep['bloquants']} erreur(s) bloquante(s) : finalisation refusée")
    record_approval(db, project, "phase3", rep["qc_id"], actor, note)
    return set_status(db, get_project(db, sid), "ready_for_phase3", "projet prêt pour le moteur vidéo", actor)


def choose_hook(db: Database, sid: str, hook_id: str, justification: str, actor: str) -> dict:
    project = get_project(db, sid)
    cur = current(db, project, "hooks")
    if not cur:
        raise StoryError("aucun hook enregistré")
    doc = json.loads(json.dumps(cur["content"]))
    if hook_id not in {h["id"] for h in doc["hooks"]}:
        raise StoryError(f"hook inconnu : {hook_id}")
    doc["choisi"], doc["justification_choix"] = hook_id, justification
    return save_artifact(db, project, "hooks", doc, author=actor, note=f"choix du hook {hook_id}")


def edit_hook(db: Database, sid: str, hook_id: str, changes: dict, actor: str) -> dict:
    project = get_project(db, sid)
    doc = json.loads(json.dumps(current(db, project, "hooks")["content"]))
    h = next((x for x in doc["hooks"] if x["id"] == hook_id), None)
    if not h:
        raise StoryError(f"hook inconnu : {hook_id}")
    h.update(changes)
    return save_artifact(db, project, "hooks", doc, author=actor, note=f"hook {hook_id} modifié ({', '.join(changes)})")


def edit_sequence(db: Database, sid: str, seq_id: str, changes: dict, actor: str) -> dict:
    """Modifie UNE séquence : nouvelle version du script ; le storyboard existant devient obsolète (conservé)."""
    project = get_project(db, sid)
    cur = current(db, project, "script")
    if not cur:
        raise StoryError("aucun script enregistré")
    doc = json.loads(json.dumps(cur["content"]))
    s = next((x for x in doc["sequences"] if x["id"] == seq_id), None)
    if not s:
        raise StoryError(f"séquence inconnue : {seq_id}")
    s.update(changes)
    return save_artifact(db, project, "script", doc, author=actor, note=f"séquence {seq_id} modifiée ({', '.join(changes)})")


def set_element(db: Database, sid: str, kind: str, doc: dict, actor: str, note: str = "") -> tuple[dict, dict]:
    """Enregistre un élément après contrôle de forme minimal, puis renvoie l'évaluation complète."""
    if not isinstance(doc, dict):
        raise StoryError("document JSON attendu")
    art = save_artifact(db, get_project(db, sid), kind, doc, author=actor, note=note)
    return art, evaluate_all(db, get_project(db, sid))
