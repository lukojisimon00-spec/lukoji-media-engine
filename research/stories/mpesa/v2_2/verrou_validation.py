"""Préparation, enregistrement durable et contrôle des validations HUMAINES du pilote M-Pesa (STO-20261127-001).

Ce script ne valide RIEN. La validation se fait uniquement par la commande du moteur, lancée par le responsable
éditorial ou sur son instruction explicite :

    ./bin/lukoji story approve STO-20261127-001 --etape structure --acteur "<nom du responsable>" --note "…"
    ./bin/lukoji story qc STO-20261127-001                 # ouvre la revue du script (script_review) si rien ne bloque
    ./bin/lukoji story approve STO-20261127-001 --etape script --acteur "<nom du responsable>" --note "…"

Modes (tous en lecture seule sur la base) :
- fiche    : avant validation. Écrit la fiche des versions EXACTES soumises (version, empreinte SHA-256, fichier source),
             et vérifie que les fichiers versionnés dans Git sont identiques aux versions de la base.
- verrou   : après validation. Lit les validations enregistrées (table story_approvals) et écrit un fichier de verrou
             VERSIONNÉ dans Git (la base est locale et non versionnée : sans ce fichier, la validation serait perdue avec
             le conteneur). Le verrou contient, pour chaque étape validée, les versions et leurs empreintes.
- verifier : contrôle que les versions verrouillées sont toujours présentes et inchangées (empreinte recalculée), et dit
             si la reconstruction du storyboard est autorisée (structure ET script validés, et versions courantes =
             versions validées).

Usage : python3 research/stories/mpesa/v2_2/verrou_validation.py fiche|verrou|verifier
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SID = "STO-20261127-001"
DOCS = ROOT / f"docs/stories/{SID}"
FICHE = DOCS / "v2_2/fiche_validation.json"
VERROU = DOCS / "VERROU_VALIDATION.json"
SOURCES = {"script": HERE / "script_v2_2.json", "structure": HERE / "structure_v2_2.json", "hooks": HERE / "hooks_v2_2.json"}


def sha(obj) -> str:
    """Même empreinte que le moteur (project._sha)."""
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def db():
    c = sqlite3.connect(ROOT / "var/lukoji.sqlite3")
    c.row_factory = sqlite3.Row
    return c


def project(c):
    return dict(c.execute("SELECT * FROM story_projects WHERE sid = ?", (SID,)).fetchone())


def artifact(c, pid, kind, version=None):
    q = "SELECT version, sha256, content_json, based_on_json, author, created_at FROM story_artifacts WHERE project_id = ? AND kind = ?"
    args = [pid, kind]
    if version is None:
        q += " ORDER BY version DESC LIMIT 1"
    else:
        q += " AND version = ?"
        args.append(version)
    r = c.execute(q, args).fetchone()
    return dict(r) if r else None


def fiche() -> int:
    c = db()
    p = project(c)
    out = {"projet": SID, "titre": p["title"], "statut": p["status"], "avertissement":
           "Fiche préparatoire : AUCUNE validation n'est enregistrée par ce document.", "etapes": {}}
    ok = True
    for stage, kinds in (("structure", ["research", "hooks", "structure"]), ("script", ["research", "hooks", "structure", "script"])):
        out["etapes"][stage] = {}
        for k in kinds:
            a = artifact(c, p["id"], k)
            recomputed = sha(json.loads(a["content_json"]))
            same_file = None
            if k in SOURCES:
                same_file = sha(json.loads(SOURCES[k].read_text(encoding="utf-8"))) == a["sha256"]
                ok &= same_file
            ok &= recomputed == a["sha256"]
            out["etapes"][stage][k] = {"version": a["version"], "sha256": a["sha256"], "base_sur": json.loads(a["based_on_json"]),
                                       "empreinte_recalculee_ok": recomputed == a["sha256"],
                                       "fichier_versionne": str(SOURCES[k].relative_to(ROOT)) if k in SOURCES else None,
                                       "fichier_identique_a_la_base": same_file}
    qc = c.execute("SELECT id, versions_json, status FROM story_qc WHERE project_id = ? ORDER BY id DESC LIMIT 1", (p["id"],)).fetchone()
    cur = {k: artifact(c, p["id"], k)["version"] for k in ("research", "hooks", "structure", "script", "storyboard", "visual")}
    out["dernier_qc"] = {"id": qc["id"], "statut": qc["status"], "sur_versions_courantes": json.loads(qc["versions_json"]) == cur}
    out["validations_existantes"] = c.execute("SELECT COUNT(*) FROM story_approvals WHERE project_id = ?", (p["id"],)).fetchone()[0]
    FICHE.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"fiche : {FICHE.relative_to(ROOT)} · cohérence fichiers/base : {'ok' if ok else 'ÉCART'}")
    return 0 if ok else 1


def verrou() -> int:
    c = db()
    p = project(c)
    rows = [dict(r) for r in c.execute("SELECT * FROM story_approvals WHERE project_id = ? ORDER BY id", (p["id"],))]
    if not rows:
        print("aucune validation enregistrée : rien à verrouiller")
        return 1
    lock = {"projet": SID, "titre": p["title"], "statut_au_verrouillage": p["status"], "validations": []}
    for r in rows:
        versions = json.loads(r["versions_json"])
        lock["validations"].append({
            "etape": r["stage"], "acteur": r["actor"], "date": r["at"], "note": r["note"], "qc_id": r["qc_id"],
            "versions": {k: {"version": v, "sha256": artifact(c, p["id"], k, v)["sha256"]} for k, v in versions.items()}})
    VERROU.write_text(json.dumps(lock, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"verrou écrit : {VERROU.relative_to(ROOT)} ({len(rows)} validation(s)) — à commiter")
    return 0


def verifier() -> int:
    if not VERROU.exists():
        print("aucun verrou : aucune validation humaine n'a été verrouillée ; reconstruction du storyboard NON autorisée")
        return 1
    lock = json.loads(VERROU.read_text(encoding="utf-8"))
    c = db()
    p = project(c)
    ok = True
    for v in lock["validations"]:
        for k, x in v["versions"].items():
            a = artifact(c, p["id"], k, x["version"])
            good = bool(a) and a["sha256"] == x["sha256"] and sha(json.loads(a["content_json"])) == x["sha256"]
            ok &= good
            print(f"{v['etape']:10} {k:10} v{x['version']:<3} {'inchangée' if good else 'ABSENTE OU MODIFIÉE'}")
    stages = {v["etape"]: v for v in lock["validations"]}
    allowed = ok and "structure" in stages and "script" in stages
    if allowed:
        cur = {k: artifact(c, p["id"], k)["version"] for k in ("research", "hooks", "structure", "script")}
        validated = {k: x["version"] for k, x in stages["script"]["versions"].items() if k in cur}
        allowed = cur == validated
        if not allowed:
            print(f"versions courantes {cur} ≠ versions validées {validated} : nouvelle validation requise")
    print("reconstruction du storyboard :", "AUTORISÉE à partir des versions validées" if allowed else "NON autorisée")
    return 0 if ok else 1


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"fiche": fiche, "verrou": verrou, "verifier": verifier}.get(mode, lambda: (print(__doc__), 2)[1])())
