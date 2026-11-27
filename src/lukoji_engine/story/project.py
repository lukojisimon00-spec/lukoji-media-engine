"""Projet narratif : statuts, versions des éléments, dépendances, validations, journal.

Cycle de vie (cohérent avec le cycle du sujet : un projet ne naît que d'un sujet « valide », qui passe alors
« en_production ») :

  research_pending → research_verified → structure_draft → structure_approved → script_draft → script_review
  → script_approved → storyboard_draft → storyboard_review → storyboard_approved → ready_for_phase3

- *_draft  : un élément de l'étape a été enregistré (nouvelle version) ;
- *_review : le contrôle qualité de l'étape ne relève aucune erreur bloquante ; en attente de validation humaine ;
- *_approved : validé par l'éditeur (validation liée aux versions exactes validées).
Modifier un élément d'une étape déjà validée ramène le projet au brouillon de cette étape ; les éléments
dépendants (ex. storyboard basé sur une ancienne version du script) sont signalés « obsolètes », jamais effacés.
"""
from __future__ import annotations

import difflib
import hashlib
import json

from ..db import Database, now
from ..log import get_logger
from ..subjects import get_subject, transition as subject_transition

log = get_logger("story")

STATUSES = ("research_pending", "research_verified", "structure_draft", "structure_approved", "script_draft",
            "script_review", "script_approved", "storyboard_draft", "storyboard_review", "storyboard_approved",
            "ready_for_phase3")
ORDER = {s: i for i, s in enumerate(STATUSES)}
KINDS = ("research", "hooks", "structure", "script", "storyboard", "visual")
STAGE_OF = {"research": "research", "hooks": "structure", "structure": "structure", "script": "script",
            "storyboard": "storyboard", "visual": "storyboard"}
# Dépendances : un élément est construit sur les versions courantes de ces éléments.
DEPENDS = {"hooks": ["research"], "structure": ["research", "hooks"], "script": ["research", "hooks", "structure"],
           "storyboard": ["script", "visual"], "visual": ["structure"]}
STAGES = ("research", "structure", "script", "storyboard")
# Une étape ne s'OUVRE (statut *_draft/*_review/*_approved) que si la précédente est validée par un humain.

# Migration n° 3 : voir db.MIGRATIONS (tables story_projects, story_artifacts, story_events, story_approvals, story_qc).



class StoryError(ValueError):
    pass


def _sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def _event(db: Database, pid: int, frm: str | None, to: str, note: str, actor: str) -> None:
    db.conn.execute("INSERT INTO story_events (project_id, from_status, to_status, note, actor, at) VALUES (?,?,?,?,?,?)",
                    (pid, frm, to, note, actor, now()))


def get_project(db: Database, sid: str) -> dict:
    r = db.conn.execute("SELECT * FROM story_projects WHERE sid = ?", (sid,)).fetchone()
    if not r:
        raise StoryError(f"projet narratif inconnu : {sid}")
    return dict(r)


def list_projects(db: Database) -> list[dict]:
    return [dict(r) for r in db.conn.execute(
        "SELECT p.*, s.uid AS subject_uid FROM story_projects p JOIN subjects s ON s.id = p.subject_id ORDER BY p.id")]


def create_project(db: Database, subject_uid: str, fmt: str = "documentaire_long", actor: str = "editeur") -> dict:
    from .text import story_config
    if fmt not in story_config()["formats"]:
        raise StoryError(f"format inconnu : {fmt}")
    subj = get_subject(db, subject_uid)
    if not subj:
        raise StoryError(f"sujet inconnu : {subject_uid}")
    existing = db.conn.execute("SELECT sid FROM story_projects WHERE subject_id = ?", (subj["id"],)).fetchone()
    if existing:
        raise StoryError(f"un projet existe déjà pour ce sujet : {existing[0]} (reprendre ce projet)")
    if subj["status"] != "valide":
        raise StoryError(f"le sujet {subject_uid} doit être « valide » (statut actuel : {subj['status']}) : "
                         "aucun projet narratif sans validation éditoriale")
    day = now()[:10].replace("-", "")
    n = db.conn.execute("SELECT COUNT(*) FROM story_projects WHERE sid LIKE ?", (f"STO-{day}-%",)).fetchone()[0]
    sid = f"STO-{day}-{n + 1:03d}"
    with db.tx():
        pid = db.conn.execute("INSERT INTO story_projects (sid, subject_id, title, format, status, created_at, updated_at)"
                              " VALUES (?,?,?,?,?,?,?)", (sid, subj["id"], subj["title"], fmt, "research_pending", now(), now())).lastrowid
        _event(db, pid, None, "research_pending", f"projet créé depuis {subject_uid}", actor)
    subject_transition(db, subject_uid, "en_production", f"projet narratif {sid} ouvert", actor)
    log.info("projet narratif créé", extra={"sid": sid, "sujet": subject_uid})
    return get_project(db, sid)


def set_status(db: Database, project: dict, to: str, note: str, actor: str) -> dict:
    if to not in STATUSES:
        raise StoryError(f"statut inconnu : {to}")
    with db.tx():
        db.conn.execute("UPDATE story_projects SET status = ?, updated_at = ? WHERE id = ?", (to, now(), project["id"]))
        _event(db, project["id"], project["status"], to, note, actor)
    log.info("statut narratif", extra={"sid": project["sid"], "de": project["status"], "vers": to, "note": note})
    return get_project(db, project["sid"])


# ---------------------------------------------------------------------------
# Éléments versionnés
# ---------------------------------------------------------------------------
def current(db: Database, project: dict, kind: str) -> dict | None:
    r = db.conn.execute("SELECT * FROM story_artifacts WHERE project_id = ? AND kind = ? ORDER BY version DESC LIMIT 1",
                        (project["id"], kind)).fetchone()
    if not r:
        return None
    d = dict(r)
    d["content"] = json.loads(d.pop("content_json"))
    d["based_on"] = json.loads(d.pop("based_on_json"))
    return d


def version(db: Database, project: dict, kind: str, v: int) -> dict:
    r = db.conn.execute("SELECT * FROM story_artifacts WHERE project_id = ? AND kind = ? AND version = ?",
                        (project["id"], kind, v)).fetchone()
    if not r:
        raise StoryError(f"version introuvable : {kind} v{v}")
    d = dict(r)
    d["content"] = json.loads(d.pop("content_json"))
    d["based_on"] = json.loads(d.pop("based_on_json"))
    return d


def versions(db: Database, project: dict, kind: str | None = None) -> list[dict]:
    q = "SELECT kind, version, sha256, based_on_json, author, note, created_at FROM story_artifacts WHERE project_id = ?"
    args: tuple = (project["id"],)
    if kind:
        q, args = q + " AND kind = ?", args + (kind,)
    return [dict(r, based_on=json.loads(r["based_on_json"])) for r in db.conn.execute(q + " ORDER BY kind, version", args)]


def current_versions(db: Database, project: dict) -> dict:
    out = {}
    for k in KINDS:
        c = current(db, project, k)
        if c:
            out[k] = c["version"]
    return out


def stale(db: Database, project: dict) -> dict:
    """Éléments construits sur une version qui n'est plus la version courante d'une dépendance."""
    cur = current_versions(db, project)
    out = {}
    for k in KINDS:
        c = current(db, project, k)
        if not c:
            continue
        bad = {dep: v for dep, v in c["based_on"].items() if cur.get(dep) != v}
        if bad:
            out[k] = {dep: f"construit sur v{v}, courante v{cur.get(dep)}" for dep, v in bad.items()}
    return out


def save_artifact(db: Database, project: dict, kind: str, content: dict, *, author: str, note: str = "") -> dict:
    """Enregistre une nouvelle version (le contenu identique à la version courante n'est pas dupliqué)."""
    if kind not in KINDS:
        raise StoryError(f"élément inconnu : {kind}")
    project = get_project(db, project["sid"])
    stage = STAGE_OF[kind]
    if stage != "research" and ORDER[project["status"]] < ORDER["research_verified"]:
        raise StoryError(f"« {kind} » exige une recherche vérifiée (statut actuel : {project['status']})")
    cur = current(db, project, kind)
    sha = _sha(content)
    cv = current_versions(db, project)
    missing = [d for d in DEPENDS.get(kind, []) if d not in cv]
    if missing:
        raise StoryError(f"« {kind} » dépend de : {', '.join(missing)} (à enregistrer d'abord)")
    based = {d: cv[d] for d in DEPENDS.get(kind, [])}
    if cur and cur["sha256"] == sha and cur["based_on"] == based:
        return cur                      # rien de nouveau
    if cur and cur["sha256"] == sha:
        note = note or f"contenu inchangé, ré-attaché à {based}"
    v = (cur["version"] + 1) if cur else 1
    with db.tx():
        db.conn.execute("INSERT INTO story_artifacts (project_id, kind, version, content_json, sha256, based_on_json, author,"
                        " note, created_at) VALUES (?,?,?,?,?,?,?,?,?)",
                        (project["id"], kind, v, json.dumps(content, ensure_ascii=False), sha, json.dumps(based), author,
                         note, now()))
    log.info("version enregistrée", extra={"sid": project["sid"], "element": kind, "version": v, "note": note})
    # Statut : l'étape OUVERTE (celle que les validations humaines permettent d'atteindre) passe en brouillon ;
    # une étape déjà validée qu'on modifie revient en brouillon ; une étape future est un « brouillon anticipé »
    # (versionné et contrôlé, mais sans effet sur le statut tant que l'étape précédente n'est pas validée).
    if stage != "research":
        opened = open_stage(project["status"])
        draft = f"{stage}_draft"
        if STAGES.index(stage) <= STAGES.index(opened):
            if project["status"] != draft:
                set_status(db, project, draft, f"{kind} v{v} enregistré", author)
        else:
            log.info("brouillon anticipé", extra={"sid": project["sid"], "element": kind, "etape_ouverte": opened})
    return current(db, project, kind)


def open_stage(status: str) -> str:
    """Étape la plus avancée que les validations humaines permettent de travailler."""
    if ORDER[status] < ORDER["structure_approved"]:
        return "structure"
    if ORDER[status] < ORDER["script_approved"]:
        return "script"
    return "storyboard"


def diff(db: Database, project: dict, kind: str, v1: int, v2: int) -> str:
    a = json.dumps(version(db, project, kind, v1)["content"], ensure_ascii=False, indent=1, sort_keys=True).splitlines()
    b = json.dumps(version(db, project, kind, v2)["content"], ensure_ascii=False, indent=1, sort_keys=True).splitlines()
    return "\n".join(difflib.unified_diff(a, b, f"{kind} v{v1}", f"{kind} v{v2}", lineterm="", n=1))


def approvals(db: Database, project: dict) -> list[dict]:
    return [dict(r, versions=json.loads(r["versions_json"])) for r in db.conn.execute(
        "SELECT * FROM story_approvals WHERE project_id = ? ORDER BY id", (project["id"],))]


def events(db: Database, project: dict) -> list[dict]:
    return [dict(r) for r in db.conn.execute("SELECT * FROM story_events WHERE project_id = ? ORDER BY id", (project["id"],))]


def record_approval(db: Database, project: dict, stage: str, qc_id: int | None, actor: str, note: str) -> None:
    with db.tx():
        db.conn.execute("INSERT INTO story_approvals (project_id, stage, versions_json, qc_id, actor, note, at) VALUES (?,?,?,?,?,?,?)",
                        (project["id"], stage, json.dumps(current_versions(db, project)), qc_id, actor, note, now()))
