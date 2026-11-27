"""Sujets éditoriaux : import d'un dossier de recherche, contrôle, doublons, cycle de vie.

Flux :
  dossier JSON (sources consultées + propositions + faits avec extraits)
    -> validation stricte (schéma, URL, niveaux de consultation, notes justifiées)
    -> récupération des pages par le moteur quand le réseau le permet (vérification des extraits)
    -> statut CALCULÉ de chaque fait, score, formats réellement soutenus
    -> détection des doublons (sujets déjà proposés / produits / publiés / abandonnés)
    -> enregistrement (statut « propose ») + journal des décisions.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import sources as src
from .config import load_config
from .db import Database, now
from .log import get_logger
from .paths import resolve
from .scoring import CLAIM_KINDS, EDITORIAL_CRITERIA, Evidence, claim_status, compute_score, eligible_formats
from .textsim import Corpus, cosine, jaccard

log = get_logger("subjects")

SUBJECT_STATUSES = ("recherche", "propose", "valide", "rejete", "reporte", "en_production", "produit", "publie")
SUBJECT_TRANSITIONS: dict[str, set[str]] = {
    "recherche": {"propose", "rejete"},
    "propose": {"valide", "rejete", "reporte"},
    "reporte": {"propose", "valide", "rejete"},
    "rejete": {"propose"},                       # réactivation d'un sujet abandonné
    "valide": {"en_production", "reporte", "rejete"},
    "en_production": {"produit", "valide"},
    "produit": {"publie"},
    "publie": set(),
}
FORMATS = ("short", "affiche", "documentaire", "serie")


class DossierError(ValueError):
    def __init__(self, problems: list[str]):
        super().__init__("dossier invalide :\n- " + "\n- ".join(problems))
        self.problems = problems


# ---------------------------------------------------------------------------
# Validation du dossier
# ---------------------------------------------------------------------------
def validate_dossier(d: dict) -> list[str]:
    cfg = load_config().research
    p: list[str] = []
    if not isinstance(d.get("session"), dict):
        p.append("bloc « session » manquant (mode, chercheur, requêtes)")
    else:
        for k in ("mode", "chercheur", "requetes"):
            if not d["session"].get(k):
                p.append(f"session.{k} manquant")
    srcs = d.get("sources") or []
    if not srcs:
        p.append("aucune source")
    ids = set()
    for i, s in enumerate(srcs):
        tag = f"sources[{i}] ({s.get('id', '?')})"
        for k in ("id", "url", "titre", "date_consultation", "consultation"):
            if not s.get(k):
                p.append(f"{tag} : champ « {k} » manquant")
        if s.get("id") in ids:
            p.append(f"{tag} : identifiant en double")
        ids.add(s.get("id"))
        for prob in src.validate_url(s.get("url", "")):
            p.append(f"{tag} : URL refusée — {prob}")
        if s.get("consultation") and s["consultation"] not in src.CONSULTATION_LEVELS:
            p.append(f"{tag} : niveau de consultation inconnu {s['consultation']!r}")
        if s.get("date_publication") and not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", str(s["date_publication"])):
            p.append(f"{tag} : date de publication non ISO ({s['date_publication']!r})")
        if s.get("date_consultation") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(s["date_consultation"])):
            p.append(f"{tag} : date de consultation non ISO")
    props = d.get("propositions") or []
    if not props:
        p.append("aucune proposition")
    for j, pr in enumerate(props):
        tag = f"propositions[{j}] ({(pr.get('titre') or '?')[:40]})"
        for k in ("titre", "sujet", "angle", "famille", "territoire", "temporalite", "interet", "accroche",
                  "resume", "potentiel_visuel"):
            if not str(pr.get(k) or "").strip():
                p.append(f"{tag} : champ « {k} » manquant")
        if pr.get("famille") and pr["famille"] not in cfg["familles"]:
            p.append(f"{tag} : famille inconnue {pr['famille']!r}")
        if pr.get("territoire") and pr["territoire"] not in cfg["territoires"]["valeurs"]:
            p.append(f"{tag} : territoire inconnu {pr['territoire']!r}")
        if pr.get("temporalite") and pr["temporalite"] not in cfg["temporalite"]["valeurs"]:
            p.append(f"{tag} : temporalité inconnue {pr['temporalite']!r}")
        for f in pr.get("formats") or []:
            if f not in FORMATS:
                p.append(f"{tag} : format inconnu {f!r}")
        if not pr.get("formats"):
            p.append(f"{tag} : aucun format recommandé")
        notes = pr.get("notes_editoriales") or {}
        for c in EDITORIAL_CRITERIA:
            e = notes.get(c)
            if not isinstance(e, dict) or not isinstance(e.get("note"), int) or not 1 <= e["note"] <= 5:
                p.append(f"{tag} : note éditoriale « {c} » manquante (entier 1–5)")
            elif not str(e.get("justification") or "").strip():
                p.append(f"{tag} : justification manquante pour « {c} »")
        for k in ("difficulte", "risque_juridique"):
            e = pr.get(k)
            if not isinstance(e, dict) or not isinstance(e.get("note"), int) or not 1 <= e["note"] <= 5:
                p.append(f"{tag} : « {k} » doit être {{note 1–5, justification}}")
        faits = pr.get("faits") or []
        if not faits:
            p.append(f"{tag} : aucun fait")
        for k, f in enumerate(faits):
            ft = f"{tag} faits[{k}]"
            if not str(f.get("texte") or "").strip():
                p.append(f"{ft} : texte manquant")
            if f.get("type") not in CLAIM_KINDS:
                p.append(f"{ft} : type invalide {f.get('type')!r} ({', '.join(CLAIM_KINDS)})")
            if f.get("importance") not in ("cle", "secondaire"):
                p.append(f"{ft} : importance « cle » ou « secondaire » requise")
            for m, ev in enumerate(f.get("preuves") or []):
                if ev.get("source") not in ids:
                    p.append(f"{ft} preuves[{m}] : source inconnue {ev.get('source')!r}")
                if len(str(ev.get("extrait") or "").strip()) < 12:
                    p.append(f"{ft} preuves[{m}] : extrait manquant ou trop court (citation exacte requise)")
                if ev.get("position", "soutient") not in ("soutient", "contredit", "nuance"):
                    p.append(f"{ft} preuves[{m}] : position invalide")
    return p


# ---------------------------------------------------------------------------
# Sources : consultation et enregistrement
# ---------------------------------------------------------------------------
@dataclass
class SourceRecord:
    id: int
    key: str
    url: str
    category: str
    organisation: str
    consultation: str
    availability: str
    text: str | None
    row: dict = field(default_factory=dict)


def load_captures(folder: str | Path | None) -> dict:
    """Captures faites par le moteur ailleurs (scripts/capture_sources.py). Empreinte contrôlée."""
    if not folder:
        return {}
    folder = Path(folder)
    manifest = json.loads((folder / "captures.json").read_text(encoding="utf-8"))
    out = {}
    for url, e in manifest.items():
        if e.get("text_file"):
            text = (folder / e["text_file"]).read_text(encoding="utf-8")
            import hashlib
            if hashlib.sha256(text.encode()).hexdigest() != e["text_sha256"]:
                raise ValueError(f"capture altérée (empreinte différente) : {url}")
            e = dict(e, text=text)
        out[url] = e
    return out


def register_source(db: Database, s: dict, *, fetch: bool, opener=None, captures: dict | None = None) -> SourceRecord:
    url = src.normalize_url(s["url"])
    cls = src.classify(url, s)
    consultation = s["consultation"]
    availability, http_status, final_url, sha, tpath, text = "non_verifiee", None, None, None, None, None
    title, published = s["titre"], s.get("date_publication")
    cap = (captures or {}).get(url)
    if fetch:
        fr = src.fetch(url, opener)
        http_status = fr.http_status
        if fr.ok:
            availability, consultation = "disponible", "page_verifiee"
            final_url, sha, tpath, text = fr.final_url, fr.content_sha256, fr.text_path, fr.text
            published = published or (fr.published_at or "")[:10] or None
            cap = None
        else:
            availability = fr.availability
    if cap is not None:
        # Page récupérée PAR LE MOTEUR dans un environnement autorisé : preuve équivalente à une récupération locale.
        if cap.get("text"):
            store = Path(load_config().engine["paths"]["cache"]) / "sources"
            store = resolve(store); store.mkdir(parents=True, exist_ok=True)
            tfile = store / f"{cap['text_sha256'][:16]}.txt"
            tfile.write_text(cap["text"], encoding="utf-8")
            from .paths import rel as _rel
            availability, consultation, http_status = "disponible", "page_verifiee", cap.get("http_status")
            final_url, sha, tpath, text = cap.get("final_url"), cap["text_sha256"], _rel(tfile), cap["text"]
            published = published or (cap.get("published_at") or "")[:10] or None
            s = dict(s, notes=((s.get("notes") or "") + f" | capturée par le moteur le {cap['captured_at']}").strip(" |"))
        else:
            availability, http_status = cap.get("availability", availability), cap.get("http_status", http_status)
    limitations = (s.get("limites") or "").strip()
    if availability == "inaccessible_environnement":
        limitations = (limitations + " | " if limitations else "") + \
            "page non récupérable depuis l'environnement du moteur : extraits non revérifiés localement"
    if availability == "indisponible":
        limitations = (limitations + " | " if limitations else "") + f"source indisponible (HTTP {http_status})"
    if cls["category_origin"] == "declaree":
        limitations = (limitations + " | " if limitations else "") + \
            f"catégorie déclarée ({cls['category']}) : {s.get('justification_categorie')} — domaine hors registre, à revoir"
    row = {"url": url, "final_url": final_url, "domain": src.domain_of(url), "title": title,
           "organisation": cls["organisation"], "category": cls["category"], "category_origin": cls["category_origin"],
           "nature": cls["nature"], "published_at": published, "accessed_at": s["date_consultation"],
           "consultation": consultation, "availability": availability, "http_status": http_status,
           "content_sha256": sha, "text_path": tpath, "limitations": limitations or None, "notes": s.get("notes")}
    existing = db.conn.execute("SELECT id FROM sources WHERE url = ?", (url,)).fetchone()
    cols = list(row)
    if existing:
        db.conn.execute(f"UPDATE sources SET {', '.join(c + ' = ?' for c in cols)} WHERE id = ?",
                        [row[c] for c in cols] + [existing[0]])
        sid = existing[0]
    else:
        sid = db.conn.execute(f"INSERT INTO sources ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                              [row[c] for c in cols]).lastrowid
    if text is None and row["text_path"]:
        text = src.load_cached_text(row["text_path"])
    # Une source indisponible ne prouve rien, quel que soit le niveau déclaré.
    if availability == "indisponible":
        consultation = "resultat_recherche"
    return SourceRecord(sid, s["id"], url, cls["category"], cls["organisation"], consultation, availability, text, row)


# ---------------------------------------------------------------------------
# Doublons
# ---------------------------------------------------------------------------
def _subject_text(p: dict) -> str:
    return " ".join([p.get("titre", ""), p.get("sujet", ""), " ".join(p.get("entites") or [])])


def external_corpus() -> list[dict]:
    """Contenus déjà publiés ailleurs (LECTURE SEULE), ex. articles du blog LUKOJI."""
    items = []
    for c in load_config().research["doublons"].get("corpus_externes", []):
        folder = resolve(c["dossier"])
        if not folder.is_dir():
            continue
        for f in sorted(folder.glob("*.html")):
            raw = f.read_text(encoding="utf-8", errors="replace")
            parsed = src.parse_html(raw)
            m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', raw)
            import html as _html
            desc = _html.unescape(m.group(1)) if m else ""
            title = re.sub(r"\s*[|·–-]\s*LUKOJI.*$", "", parsed["title"] or f.stem)
            items.append({"ref": f"{c['nom']}:{f.name}", "title": title, "subject": desc, "angle": desc,
                          "entities": [], "status": c.get("statut", "publie"), "origin": c["nom"]})
    return items


def existing_items(db: Database) -> list[dict]:
    items = []
    for r in db.conn.execute("SELECT uid, title, subject, angle, entities_json, status FROM subjects"):
        items.append({"ref": r["uid"], "title": r["title"], "subject": r["subject"], "angle": r["angle"],
                      "entities": json.loads(r["entities_json"]), "status": r["status"], "origin": "sujets"})
    for r in db.conn.execute("SELECT slug, title, status, kind FROM contents WHERE kind != 'test'"):
        items.append({"ref": f"contenu:{r['slug']}", "title": r["title"], "subject": r["title"], "angle": "",
                      "entities": [], "status": r["status"], "origin": "contenus"})
    return items + external_corpus()


def find_duplicates(p: dict, items: list[dict]) -> list[dict]:
    """Compare THÈME (titre + sujet + entités) et ANGLE narratif à tous les contenus connus."""
    th = load_config().research["doublons"]
    if not items:
        return []
    subj_docs = [_subject_text(p)] + [" ".join([i["title"], i["subject"], " ".join(i["entities"])]) for i in items]
    angle_docs = [p.get("angle", "")] + [i["angle"] or i["subject"] for i in items]
    cs, ca = Corpus(subj_docs), Corpus(angle_docs)
    vs, va = cs.vector(subj_docs[0]), ca.vector(angle_docs[0])
    out = []
    for i, it in enumerate(items, start=1):
        s_cos = cosine(vs, cs.vector(subj_docs[i]))
        ent = jaccard(p.get("entites") or [], it["entities"])
        subj_sim = round(0.6 * s_cos + 0.4 * ent, 3) if it["entities"] and p.get("entites") else round(s_cos, 3)
        ang_sim = round(cosine(va, ca.vector(angle_docs[i])), 3)
        verdict = None
        if subj_sim >= th["seuil_meme_sujet"]:
            verdict = "meme_sujet"
        elif subj_sim >= th["seuil_sujet_proche"] and ang_sim >= th["seuil_angle_similaire"]:
            verdict = "angle_similaire"
        elif subj_sim >= th["seuil_sujet_proche"]:
            verdict = "sujet_proche"
        if verdict:
            out.append({"ref": it["ref"], "title": it["title"], "status": it["status"], "origin": it["origin"],
                        "similarite_sujet": subj_sim, "similarite_angle": ang_sim, "verdict": verdict})
    return sorted(out, key=lambda x: -x["similarite_sujet"])


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------
def _new_uid(db: Database) -> str:
    day = now()[:10].replace("-", "")
    n = db.conn.execute("SELECT COUNT(*) FROM subjects WHERE uid LIKE ?", (f"SUJ-{day}-%",)).fetchone()[0]
    return f"SUJ-{day}-{n + 1:03d}"


def start_run(db: Database, mode: str, params: dict) -> int:
    return db.conn.execute("INSERT INTO research_runs (mode, started_at, status, params_json) VALUES (?,?,?,?)",
                           (mode, now(), "en_cours", json.dumps(params, ensure_ascii=False))).lastrowid


def finish_run(db: Database, run_id: int, status: str, errors: list | None = None, notes: str | None = None):
    db.conn.execute("UPDATE research_runs SET finished_at = ?, status = ?, errors_json = ?, notes = ? WHERE id = ?",
                    (now(), status, json.dumps(errors or [], ensure_ascii=False), notes, run_id))


def import_dossier(db: Database, dossier: dict | str | Path, *, fetch: bool = True, opener=None,
                   allow_same_subject: bool = False, captures: str | Path | None = None) -> dict:
    if not isinstance(dossier, dict):
        dossier = json.loads(Path(dossier).read_text(encoding="utf-8"))
    problems = validate_dossier(dossier)
    if problems:
        raise DossierError(problems)
    cfg = load_config().research
    sess = dossier["session"]
    run_id = start_run(db, sess["mode"], {"chercheur": sess["chercheur"], "requetes": sess["requetes"],
                                          "notes": sess.get("notes")})
    report = {"run_id": run_id, "sources": [], "propositions": [], "refusees": []}
    errors = []
    try:
        _import_body(db, dossier, cfg, run_id, report, errors, fetch, opener, allow_same_subject,
                     load_captures(captures))
    except Exception as exc:
        finish_run(db, run_id, "echec", [{"type": "exception", "detail": str(exc)}])
        log.error("import en échec", extra={"run_id": run_id, "erreur": str(exc)})
        raise
    return report


def _import_body(db, dossier, cfg, run_id, report, errors, fetch, opener, allow_same_subject, captures):
    with db.tx():
        recs: dict[str, SourceRecord] = {}
        for s in dossier["sources"]:
            r = register_source(db, s, fetch=fetch, opener=opener, captures=captures)
            recs[s["id"]] = r
            report["sources"].append({"id": s["id"], "url": r.url, "categorie": r.category,
                                      "organisation": r.organisation, "consultation": r.consultation,
                                      "disponibilite": r.availability})
            if r.availability == "inaccessible_environnement":
                errors.append({"source": r.url, "type": "inaccessible_environnement"})
        items = existing_items(db)
        for pr in dossier["propositions"]:
            dups = find_duplicates(pr, items)
            same = [d for d in dups if d["verdict"] == "meme_sujet"]
            if same and not allow_same_subject:
                best = same[0]
                advice = {"rejete": "sujet abandonné : le réactiver (`sujets reactiver`) plutôt que le recréer",
                          "reporte": "sujet reporté : le reprendre (`sujets reactiver`)",
                          "publie": "déjà publié : proposer un angle nettement différent",
                          "produit": "déjà produit"}.get(best["status"], "déjà proposé")
                report["refusees"].append({"titre": pr["titre"], "doublon_de": best, "conseil": advice})
                log.warning("proposition refusée : doublon", extra={"titre": pr["titre"], "doublon": best["ref"]})
                continue
            sensitive = cfg["familles"][pr["famille"]].get("sensible", False)
            claims_out, used_sources = [], {}
            for f in pr["faits"]:
                ev_objs, ev_rows = [], []
                for ev in f.get("preuves") or []:
                    r = recs[ev["source"]]
                    check = src.excerpt_status(ev["extrait"], r.consultation, r.text)
                    probative = src.is_probative(r.consultation, check)
                    ev_objs.append(Evidence(r.category, r.organisation, probative, ev.get("position", "soutient")))
                    ev_rows.append((r.id, ev.get("position", "soutient"), ev["extrait"].strip(), check))
                    used_sources[r.id] = {"category": r.category, "organisation": r.organisation,
                                          "probative": used_sources.get(r.id, {}).get("probative", False) or probative}
                status, detail = claim_status(f["type"], ev_objs, sensitive)
                claims_out.append({"text": f["texte"].strip(), "kind": f["type"], "importance": f["importance"],
                                   "status": status, "detail": detail, "notes": f.get("notes"), "evidence": ev_rows})
            src_list = list(used_sources.values())
            score = compute_score(ratings=pr["notes_editoriales"], claims=claims_out, sources=src_list,
                                  family=pr["famille"], difficulty=pr["difficulte"], legal_risk=pr["risque_juridique"])
            elig = eligible_formats(claims_out, src_list, pr["accroche"], int(pr.get("episodes", 1)))
            flags = list(score["drapeaux"])
            for f in pr["formats"]:
                if not elig[f]["eligible"]:
                    flags.append(f"format_non_soutenu:{f}")
            if any(d["verdict"] == "angle_similaire" for d in dups):
                flags.append("angle_similaire_a_un_contenu_existant")
            if any(r.row["category_origin"] == "declaree" for r in recs.values() if r.id in used_sources):
                flags.append("categorie_source_declaree_a_revoir")
            uid = _new_uid(db)
            ts = now()
            sid = db.conn.execute(
                "INSERT INTO subjects (uid, title, subject, angle, family, territory, temporality, interest, hook, summary,"
                " entities_json, formats_json, episodes, visual_potential, difficulty, risks_json, ratings_json,"
                " score_json, priority, flags_json, dedup_json, status, run_id, created_at, updated_at)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (uid, pr["titre"], pr["sujet"], pr["angle"], pr["famille"], pr["territoire"], pr["temporalite"],
                 pr["interet"], pr["accroche"], pr["resume"], json.dumps(pr.get("entites") or [], ensure_ascii=False),
                 json.dumps({"recommandes": pr["formats"], "eligibilite": elig}, ensure_ascii=False),
                 int(pr.get("episodes", 1)), pr["potentiel_visuel"], score["difficulte"],
                 json.dumps(pr.get("risques") or [], ensure_ascii=False),
                 json.dumps({"notes_editoriales": pr["notes_editoriales"], "difficulte": pr["difficulte"],
                             "risque_juridique": pr["risque_juridique"]}, ensure_ascii=False),
                 json.dumps(score, ensure_ascii=False), score["priorite"], json.dumps(flags, ensure_ascii=False),
                 json.dumps(dups, ensure_ascii=False), "recherche", run_id, ts, ts)).lastrowid
            for c in claims_out:
                cid = db.conn.execute("INSERT INTO claims (subject_id, text, kind, importance, status, status_detail, notes)"
                                      " VALUES (?,?,?,?,?,?,?)",
                                      (sid, c["text"], c["kind"], c["importance"], c["status"], c["detail"], c["notes"])).lastrowid
                for (source_id, stance, excerpt, check) in c["evidence"]:
                    db.conn.execute("INSERT INTO claim_evidence (claim_id, source_id, stance, excerpt, excerpt_check)"
                                    " VALUES (?,?,?,?,?)", (cid, source_id, stance, excerpt, check))
            roles = pr.get("sources_roles") or {}
            for key, r in recs.items():
                if r.id in used_sources or key in roles:
                    db.conn.execute("INSERT OR IGNORE INTO subject_sources (subject_id, source_id, role) VALUES (?,?,?)",
                                    (sid, r.id, roles.get(key)))
            _event(db, sid, None, "recherche", "dossier importé", "moteur")
            _event(db, sid, "recherche", "propose", "contrôles terminés : proposition soumise à validation", "moteur")
            db.conn.execute("UPDATE subjects SET status = 'propose' WHERE id = ?", (sid,))
            items.append({"ref": uid, "title": pr["titre"], "subject": pr["sujet"], "angle": pr["angle"],
                          "entities": pr.get("entites") or [], "status": "propose", "origin": "sujets"})
            report["propositions"].append({"uid": uid, "titre": pr["titre"], "priorite": score["priorite"],
                                           "attrait": score["attrait"], "solidite": score["solidite"],
                                           "drapeaux": flags, "doublons": dups})
            log.info("proposition enregistrée", extra={"uid": uid, "titre": pr["titre"], "priorite": score["priorite"],
                                                       "solidite": score["solidite"], "drapeaux": flags})
        finish_run(db, run_id, "termine" if not errors else "termine_avec_limites", errors,
                   f"{len(report['propositions'])} proposition(s), {len(report['refusees'])} refusée(s)")


# ---------------------------------------------------------------------------
# Cycle de vie et décisions
# ---------------------------------------------------------------------------
def _event(db: Database, subject_id: int, frm: str | None, to: str, note: str, actor: str):
    db.conn.execute("INSERT INTO subject_events (subject_id, from_status, to_status, note, actor, at) VALUES (?,?,?,?,?,?)",
                    (subject_id, frm, to, note, actor, now()))


def get_subject(db: Database, uid: str) -> dict | None:
    r = db.conn.execute("SELECT * FROM subjects WHERE uid = ?", (uid,)).fetchone()
    return dict(r) if r else None


def transition(db: Database, uid: str, to: str, note: str = "", actor: str = "editeur") -> dict:
    s = get_subject(db, uid)
    if not s:
        raise KeyError(f"sujet inconnu : {uid}")
    if to not in SUBJECT_STATUSES:
        raise ValueError(f"statut inconnu : {to}")
    if to not in SUBJECT_TRANSITIONS[s["status"]]:
        raise ValueError(f"transition interdite : {s['status']} -> {to}")
    with db.tx():
        db.conn.execute("UPDATE subjects SET status = ?, updated_at = ? WHERE id = ?", (to, now(), s["id"]))
        _event(db, s["id"], s["status"], to, note, actor)
    log.info("décision éditoriale", extra={"uid": uid, "de": s["status"], "vers": to, "note": note, "acteur": actor})
    return get_subject(db, uid)


def add_note(db: Database, uid: str, note: str, actor: str = "editeur") -> None:
    s = get_subject(db, uid)
    if not s:
        raise KeyError(f"sujet inconnu : {uid}")
    if not note.strip():
        raise ValueError("remarque vide")
    with db.tx():
        db.conn.execute("INSERT INTO subject_notes (subject_id, note, actor, at) VALUES (?,?,?,?)",
                        (s["id"], note.strip(), actor, now()))
    log.info("remarque éditoriale", extra={"uid": uid, "note": note.strip(), "acteur": actor})


def search_subjects(db: Database, query: str, statuses: list[str] | None = None) -> list[dict]:
    """Retrouve des sujets (y compris abandonnés) par similarité de thème."""
    rows = [dict(r) for r in db.conn.execute("SELECT * FROM subjects")]
    if statuses:
        rows = [r for r in rows if r["status"] in statuses]
    if not rows:
        return []
    docs = [query] + [" ".join([r["title"], r["subject"], r["angle"], " ".join(json.loads(r["entities_json"]))]) for r in rows]
    c = Corpus(docs)
    q = c.vector(docs[0])
    scored = [(round(cosine(q, c.vector(docs[i + 1])), 3), r) for i, r in enumerate(rows)]
    return [dict(r, pertinence=s) for s, r in sorted(scored, key=lambda x: -x[0]) if s > 0.05]


def subject_details(db: Database, uid: str) -> dict:
    s = get_subject(db, uid)
    if not s:
        raise KeyError(f"sujet inconnu : {uid}")
    for k in ("entities_json", "formats_json", "risks_json", "ratings_json", "score_json", "flags_json", "dedup_json"):
        s[k[:-5]] = json.loads(s.pop(k))
    s["claims"] = []
    for c in db.conn.execute("SELECT * FROM claims WHERE subject_id = ? ORDER BY id", (s["id"],)):
        c = dict(c)
        c["evidence"] = [dict(e) for e in db.conn.execute(
            "SELECT ce.stance, ce.excerpt, ce.excerpt_check, so.url, so.title, so.organisation, so.category,"
            " so.consultation, so.availability FROM claim_evidence ce JOIN sources so ON so.id = ce.source_id"
            " WHERE ce.claim_id = ?", (c["id"],))]
        s["claims"].append(c)
    s["sources"] = [dict(r) for r in db.conn.execute(
        "SELECT so.*, ss.role FROM subject_sources ss JOIN sources so ON so.id = ss.source_id WHERE ss.subject_id = ?"
        " ORDER BY so.category, so.organisation", (s["id"],))]
    s["events"] = [dict(r) for r in db.conn.execute("SELECT * FROM subject_events WHERE subject_id = ? ORDER BY id", (s["id"],))]
    s["notes"] = [dict(r) for r in db.conn.execute("SELECT * FROM subject_notes WHERE subject_id = ? ORDER BY id", (s["id"],))]
    return s


def ranked(db: Database, statuses: list[str] | None = None) -> list[dict]:
    """Classement : sujets « prioritaires » d'abord (sains), puis signalés ; puis indice de priorité."""
    rows = [dict(r) for r in db.conn.execute("SELECT * FROM subjects ORDER BY id")]
    if statuses:
        rows = [r for r in rows if r["status"] in statuses]
    for r in rows:
        r["score"] = json.loads(r["score_json"])
        r["flags"] = json.loads(r["flags_json"])
    return sorted(rows, key=lambda r: (not r["score"].get("prioritaire", False), -(r["priority"] or 0)))
