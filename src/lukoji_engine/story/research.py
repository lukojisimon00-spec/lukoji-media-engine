"""Vérification de la recherche : dossier factuel du projet et règle d'usage de chaque fait dans le script.

Règles d'usage (calculées depuis le statut du fait, jamais déclarées) :
- libre                      : fait ou chiffre CONFIRMÉ ;
- attribution_obligatoire    : source unique, déclaration ou opinion — la voix off doit dire QUI l'affirme ;
- prudence_obligatoire       : hypothèse — la voix off doit marquer l'incertitude ;
- interdit                   : à vérifier ou contradictoire — ne peut pas être affirmé.
"""
from __future__ import annotations

import json

from ..db import Database
from .project import StoryError, get_project, save_artifact, set_status
from .text import story_config


def usage_rule(status: str, kind: str) -> str:
    if status == "confirme":
        return "attribution_obligatoire" if kind in ("declaration", "opinion") else "libre"
    if status in ("source_unique", "opinion_attribuee"):
        return "attribution_obligatoire"
    if status == "hypothese":
        return "prudence_obligatoire"
    return "interdit"


def fact_sheet(db: Database, subject_id: int) -> dict:
    facts = []
    for c in db.conn.execute("SELECT * FROM claims WHERE subject_id = ? ORDER BY id", (subject_id,)):
        ev = [dict(e) for e in db.conn.execute(
            "SELECT ce.stance, ce.excerpt, ce.excerpt_check, so.id AS sid, so.organisation, so.category, so.url,"
            " so.published_at, so.consultation FROM claim_evidence ce JOIN sources so ON so.id = ce.source_id"
            " WHERE ce.claim_id = ?", (c["id"],))]
        facts.append({
            "ref": f"F{c['id']}", "texte": c["text"], "type": c["kind"], "importance": c["importance"],
            "statut": c["status"], "motif": c["status_detail"], "usage": usage_rule(c["status"], c["kind"]),
            "preuves": [{"source": f"S{e['sid']}", "organisation": e["organisation"], "categorie": e["category"],
                         "position": e["stance"], "extrait": e["excerpt"], "verification": e["excerpt_check"]} for e in ev],
        })
    sources = [dict(r) for r in db.conn.execute(
        "SELECT so.id, so.url, so.title, so.organisation, so.category, so.category_origin, so.nature, so.published_at,"
        " so.accessed_at, so.consultation, so.availability, so.limitations FROM subject_sources ss"
        " JOIN sources so ON so.id = ss.source_id WHERE ss.subject_id = ? ORDER BY so.category, so.organisation", (subject_id,))]
    for s in sources:
        s["ref"] = f"S{s.pop('id')}"
    return {"faits": facts, "sources": sources}


def verify(db: Database, sid: str, analysis: dict | None, actor: str = "moteur") -> dict:
    """Construit le dossier factuel, y joint l'analyse de l'angle par l'auteur, et décide du passage
    à « research_verified » (règles publiées dans config/story.toml)."""
    project = get_project(db, sid)
    sheet = fact_sheet(db, project["subject_id"])
    subj = dict(db.conn.execute("SELECT uid, angle FROM subjects WHERE id = ?", (project["subject_id"],)).fetchone())
    key_conf = [f for f in sheet["faits"] if f["importance"] == "cle" and f["statut"] == "confirme"]
    contradictions = [f["ref"] for f in sheet["faits"] if f["statut"] == "contradictoire"]
    unverified = [f["ref"] for f in sheet["faits"] if f["usage"] == "interdit"]
    not_probative = [s["ref"] for s in sheet["sources"] if s["consultation"] != "page_verifiee"]
    need = story_config()["qc"]["recherche_min_faits_cles_confirmes"]
    blocking, warnings = [], []
    if len(key_conf) < need:
        blocking.append(f"{len(key_conf)} fait(s) clé(s) confirmé(s) : {need} requis")
    if not analysis or not all(analysis.get(k) for k in ("angle_retenu", "verdict_angle", "justification")):
        blocking.append("analyse de l'angle manquante (angle_retenu, verdict_angle, justification)")
    if unverified:
        warnings.append(f"faits non utilisables comme faits dans le script (à vérifier ou contradictoires) : {', '.join(unverified)}")
    if not_probative:
        warnings.append(f"sources non vérifiées : {', '.join(not_probative)}")
    content = {
        "sujet": subj["uid"], "angle_initial": subj["angle"], "analyse": analysis or {},
        "bilan": {"faits": len(sheet["faits"]), "faits_cles_confirmes": len(key_conf),
                  "par_usage": {u: sum(1 for f in sheet["faits"] if f["usage"] == u)
                                for u in ("libre", "attribution_obligatoire", "prudence_obligatoire", "interdit")},
                  "sources": len(sheet["sources"]), "sources_verifiees": len(sheet["sources"]) - len(not_probative),
                  "contradictions": contradictions},
        "bloquant": blocking, "alertes": warnings, **sheet,
    }
    art = save_artifact(db, project, "research", content, author=actor, note="dossier factuel")
    project = get_project(db, sid)
    if not blocking and project["status"] == "research_pending":
        set_status(db, project, "research_verified", f"recherche vérifiée (research v{art['version']})", actor)
    elif blocking and project["status"] == "research_verified":
        set_status(db, project, "research_pending", "recherche à reprendre : " + " ; ".join(blocking), actor)
    return {"version": art["version"], "bloquant": blocking, "alertes": warnings, "bilan": content["bilan"],
            "statut": get_project(db, sid)["status"]}
