"""Interface en ligne de commande : python -m lukoji_engine <commande> (ou ./bin/lukoji)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .config import load_config
from .db import Database, STATUSES, KINDS
from .log import get_logger, setup_logging

log = get_logger("cli")


def _db() -> Database:
    db = Database(load_config().path("db"))
    db.migrate()
    return db


def cmd_db_init(a):
    db = _db()
    print(f"Base prête : {db.path} (migrations : {db.migrate()})")


def cmd_brand_build(a):
    from .assets import build_manifest, vertical_lockup_parts
    db = _db()
    m = build_manifest(db)
    for theme in ("negatif", "positif"):
        vertical_lockup_parts(theme, db=db)
    print(f"Manifeste : {len(m['originals'])} originaux enregistrés ; découpes de signature générées.")


def cmd_brand_verify(a):
    from .assets import verify_manifest
    problems = verify_manifest()
    if problems:
        log.error("kit de marque altéré", extra={"problemes": problems})
        print(json.dumps(problems, ensure_ascii=False, indent=2))
        return 1
    log.info("kit de marque intègre")
    print("Kit de marque intègre : toutes les empreintes SHA-256 correspondent.")
    return 0


def cmd_profiles(a):
    from .geometry import get_profile, list_profiles
    for name in list_profiles():
        p = get_profile(name)
        print(f"{name:20s} {p.width}x{p.height} zone sûre {p.safe.as_list()} "
              f"membres={','.join(p.members)} vérifié_sur_appareil={p.verified}")


def _parse_avoid(values):
    from .geometry import Rect
    return [Rect.parse(v) for v in values or []]


def cmd_watermark(a):
    from .watermark import apply
    sc = apply(a.input, a.output, profile_name=a.profile, kind=a.kind, variant=a.variant,
               color_mode=a.color, opacity=a.opacity, signature_preset=a.signature,
               source_in=a.source_in, source_out=a.source_out, avoid=_parse_avoid(a.avoid),
               anchors=a.anchor or None, content_slug=a.slug, title=a.title, db=_db())
    wm = sc["watermark"]
    print(f"Rendu : {sc['output']}")
    print(f"  position {wm['anchor']} {wm['box']} · variante {wm['variant']} · opacité {wm['opacity']}")
    for s in wm["segments"]:
        print(f"  {s['start']:6.2f}–{s['end']:6.2f}s logo {s['color']:5s} fond {s['bg_luma']:.2f} contraste {s['contrast']:.2f}")
    print(f"  signature : {sc['signature']}")
    return 0


def cmd_signature(a):
    from .geometry import get_profile
    from .signature import render
    s = render(get_profile(a.profile), a.preset, theme=a.theme, db=_db(), force=a.force)
    print(f"Signature : {s.path} ({s.duration}s) · image finale {s.last_frame}")


def cmd_qc(a):
    from .qc import run_qc
    from .assets import sha256_file
    report = run_qc(a.video, a.profile)
    for r in report["checks"]:
        mark = "OK " if r["passed"] else ("ÉCHEC" if r["severity"] == "bloquant" else "AVERT" if r["severity"] == "avertissement" else "INFO")
        print(f"[{mark:5s}] {r['name']:36s} {r['value']!s:.110}")
    print(f"=> {report['status'].upper()} · bloquants {report['blocking']} · avertissements {report['warnings']}")
    failed = [c["name"] for c in report["checks"] if not c["passed"] and c["severity"] != "info"]
    (log.info if report["status"] == "conforme" else log.warning)(
        "contrôle qualité", extra={"video": a.video, "statut": report["status"], "controles": len(report["checks"]),
                                   "bloquants": report["blocking"], "avertissements": report["warnings"], "echecs": failed})
    if a.json:
        Path(a.json).write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    db = _db()
    render = db.find_render(sha256_file(a.video))
    if render:
        db.record_qc(render["id"], report["checks"])
    return 1 if report["status"] == "echec" else 0


def cmd_sheet(a):
    from .qc import contact_sheet
    times = [float(t) for t in a.times.split(",")] if a.times else None
    print(contact_sheet(a.video, a.output, times))


def cmd_social(a):
    from .social import load_accounts, validate
    from .config import load_config
    problems = validate(load_config().social)
    accounts = load_accounts(strict=False)
    for acc in accounts.values():
        extra = " (lien de partage)" if acc.is_share_link else ""
        print(f"{acc.platform:10s} {acc.url}{extra}")
        print(f"{'':10s} identifiant={acc.handle or '—'} · formats={','.join(acc.formats)} · publication={acc.publication}")
    for fmt, targets in load_config().social["routage"].items():
        print(f"routage {fmt:12s} -> {', '.join(targets)}")
    if problems:
        print("PROBLÈMES :\n- " + "\n- ".join(problems))
        return 1
    print("Comptes officiels valides · aucun secret · aucune API connectée (phase 0).")
    return 0


# ---------------------------------------------------------------------------
# Phase 1 : recherche, sources, sujets
# ---------------------------------------------------------------------------
def cmd_research_discover(a):
    from .providers import discover
    from .subjects import finish_run, start_run
    from .db import now
    db = _db()
    run_id = start_run(db, "collecteurs", {"requete": a.query, "collecteurs": a.providers})
    results = discover(a.query, a.providers.split(",") if a.providers else None)
    errors, total = [], 0
    for r in results:
        if r.error:
            errors.append({"collecteur": r.provider, **r.error})
            print(f"[{r.provider}] ÉCHEC ({r.error['type']}) : {r.error['detail'][:200]}")
            continue
        print(f"[{r.provider}] {len(r.hits)} résultat(s)")
        for h in r.hits:
            total += 1
            db.conn.execute("INSERT INTO search_hits (run_id, provider, query, rank, title, url, source_name, published_at,"
                            " snippet, retrieved_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                            (run_id, h.provider, h.query, h.rank, h.title, h.url, h.source_name, h.published_at,
                             h.snippet, now()))
            print(f"   {h.rank:2d}. {h.title[:90]} — {h.source_name or ''} {h.published_at or ''}\n       {h.url}")
    status = "termine" if not errors else ("echec" if total == 0 else "termine_avec_limites")
    finish_run(db, run_id, status, errors, f"{total} piste(s) — résultats de recherche, NON des preuves")
    print(f"Session {run_id} : {status} · {total} piste(s) enregistrée(s) (niveau « resultat_recherche »)")
    return 0 if total or not errors else 3


def cmd_research_import(a):
    from .subjects import DossierError, import_dossier
    db = _db()
    try:
        rep = import_dossier(db, a.dossier, fetch=not a.no_fetch, allow_same_subject=a.allow_same_subject,
                             captures=a.captures)
    except DossierError as e:
        print(str(e))
        return 1
    print(f"Session de recherche {rep['run_id']}")
    for s in rep["sources"]:
        print(f"  source {s['id']:4s} [{s['categorie']}] {s['organisation'][:28]:28s} {s['consultation']:18s} {s['disponibilite']}")
    for p in rep["propositions"]:
        print(f"  + {p['uid']} prio {p['priorite']:5.1f} (attrait {p['attrait']}, solidité {p['solidite']}) {p['titre']}")
        if p["drapeaux"]:
            print(f"      signalements : {', '.join(p['drapeaux'])}")
    for r in rep["refusees"]:
        d = r["doublon_de"]
        print(f"  ✗ REFUSÉE (doublon de {d['ref']} « {d['title']} », {d['status']}) : {r['titre']} — {r['conseil']}")
    if a.json:
        Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0


def cmd_sources(a):
    db = _db()
    if a.action == "list":
        for r in db.conn.execute("SELECT * FROM sources ORDER BY category, organisation"):
            print(f"[{r['category']}] {r['organisation'][:30]:30s} {r['consultation']:18s} {r['availability']:26s} {r['url']}")
        return 0
    if a.action == "check":
        from . import sources as src
        bad = 0
        for r in db.conn.execute("SELECT id, url FROM sources ORDER BY id").fetchall():
            fr = src.fetch(r["url"])
            print(f"{fr.availability:26s} {fr.http_status or '-':>4} {r['url']}" + (f"  ({fr.error})" if fr.error else ""))
            bad += fr.availability != "disponible"
            if fr.ok:
                db.conn.execute("UPDATE sources SET availability='disponible', http_status=?, content_sha256=?, text_path=?"
                                " WHERE id=?", (fr.http_status, fr.content_sha256, fr.text_path, r["id"]))
            else:
                db.conn.execute("UPDATE sources SET availability=?, http_status=? WHERE id=? AND availability != 'disponible'",
                                (fr.availability, fr.http_status, r["id"]))
        print(f"{bad} source(s) non récupérée(s) par le moteur")
        return 0


def cmd_sujets(a):
    from . import mediacenter as mc
    from . import subjects as sj
    db = _db()
    act = a.action
    if act == "list":
        print(mc.render_list(db, a.status.split(",") if a.status else None))
    elif act == "show":
        print(mc.render_show(db, a.uid[0]))
    elif act == "compare":
        if len(a.uid) < 2:
            print("indiquer au moins deux UID"); return 1
        print(mc.render_compare(db, a.uid))
    elif act in ("valider", "rejeter", "reporter", "reactiver", "statut"):
        target = {"valider": "valide", "rejeter": "rejete", "reporter": "reporte", "reactiver": "propose"}.get(act, a.to)
        if not target:
            print("--to requis pour « statut »"); return 1
        for uid in a.uid:
            s = sj.transition(db, uid, target, a.note or "", a.acteur)
            print(f"{uid} → {s['status']}" + (f" (« {a.note} »)" if a.note else ""))
    elif act == "note":
        sj.add_note(db, a.uid[0], a.note or "", a.acteur)
        print(f"Remarque enregistrée sur {a.uid[0]}")
    elif act == "history":
        print(mc.render_show(db, a.uid[0]).split("── Historique des décisions")[1])
    elif act == "search":
        q = " ".join(a.uid)
        for r in sj.search_subjects(db, q, a.status.split(",") if a.status else None):
            print(f"{r['pertinence']:.3f} {r['uid']} [{r['status']}] {r['title']}")
    elif act == "html":
        out = a.out or "var/out/media_center.html"
        print(mc.write_html(db, out, a.status.split(",") if a.status else None))
    return 0


def cmd_content(a):
    db = _db()
    if a.action == "add":
        c = db.create_content(a.slug, a.kind, a.title or a.slug)
    elif a.action == "move":
        c = db.transition(a.slug, a.to, a.note or "")
    elif a.action == "history":
        for e in db.history(a.slug):
            print(f"{e['at']} {e['from_status'] or '-':>10s} -> {e['to_status']:10s} {e['note'] or ''}")
        return 0
    else:
        for c in db.list_contents(a.status):
            print(f"{c['id']:4d} {c['kind']:12s} {c['status']:10s} {c['slug']}")
        return 0
    print(json.dumps(c, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="lukoji", description="LUKOJI MEDIA ENGINE — contenus propres LUKOJI")
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("db-init", help="crée / migre la base SQLite").set_defaults(fn=cmd_db_init)
    sub.add_parser("brand-build", help="manifeste des originaux + découpes de signature").set_defaults(fn=cmd_brand_build)
    sub.add_parser("brand-verify", help="vérifie l'intégrité du kit de marque").set_defaults(fn=cmd_brand_verify)
    sub.add_parser("profiles", help="liste les profils et zones sûres").set_defaults(fn=cmd_profiles)
    sub.add_parser("social", help="affiche et valide les comptes sociaux officiels").set_defaults(fn=cmd_social)

    w = sub.add_parser("watermark", help="applique le filigrane (+ signature) à une vidéo")
    w.add_argument("input"); w.add_argument("output")
    w.add_argument("--profile", default="vertical_universal")
    w.add_argument("--kind", default="short", choices=KINDS)
    w.add_argument("--variant", choices=["lockup", "symbole"])
    w.add_argument("--color", choices=["adaptive", "white", "black"])
    w.add_argument("--opacity", type=float)
    w.add_argument("--signature", help="aucune | flash | court | documentaire (défaut selon --kind)")
    w.add_argument("--source-in", type=float, default=0.0)
    w.add_argument("--source-out", type=float)
    w.add_argument("--avoid", action="append", help="zone réservée x,y,l,h (répétable) : sous-titres, texte, visage")
    w.add_argument("--anchor", action="append", help="impose l'ordre des coins (répétable) : top_left, top_right…")
    w.add_argument("--slug"); w.add_argument("--title")
    w.set_defaults(fn=cmd_watermark)

    s = sub.add_parser("signature", help="rend la signature de fin seule")
    s.add_argument("--profile", default="vertical_universal")
    s.add_argument("--preset", default="court")
    s.add_argument("--theme", choices=["negatif", "positif"])
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_signature)

    q = sub.add_parser("qc", help="contrôle qualité d'un rendu")
    q.add_argument("video"); q.add_argument("--profile"); q.add_argument("--json")
    q.set_defaults(fn=cmd_qc)

    sh = sub.add_parser("sheet", help="planche de contrôle visuel (zones + filigrane)")
    sh.add_argument("video"); sh.add_argument("output"); sh.add_argument("--times")
    sh.set_defaults(fn=cmd_sheet)

    r = sub.add_parser("recherche", help="collecte de pistes (Wikipédia, GDELT, RSS) — pistes, pas preuves")
    rs = r.add_subparsers(dest="raction", required=True)
    rd = rs.add_parser("collecter"); rd.add_argument("query"); rd.add_argument("--providers")
    rd.set_defaults(fn=cmd_research_discover)
    ri = rs.add_parser("importer", help="importe un dossier de recherche (sources consultées + propositions)")
    ri.add_argument("dossier"); ri.add_argument("--no-fetch", action="store_true", help="ne pas tenter de récupérer les pages")
    ri.add_argument("--allow-same-subject", action="store_true"); ri.add_argument("--json")
    ri.add_argument("--captures", help="dossier de captures du moteur (scripts/capture_sources.py)")
    ri.set_defaults(fn=cmd_research_import)

    so = sub.add_parser("sources", help="sources enregistrées : list | check (disponibilité)")
    so.add_argument("action", choices=["list", "check"]); so.set_defaults(fn=cmd_sources)

    sj = sub.add_parser("sujets", help="Media Center V0 : consulter et décider")
    sj.add_argument("action", choices=["list", "show", "compare", "valider", "rejeter", "reporter", "reactiver",
                                       "statut", "note", "history", "search", "html"])
    sj.add_argument("uid", nargs="*", help="UID (ou texte pour « search »)")
    sj.add_argument("--note"); sj.add_argument("--status", help="filtre, ex. propose,reporte")
    sj.add_argument("--to", help="statut cible pour « statut »"); sj.add_argument("--out")
    sj.add_argument("--acteur", default="editeur")
    sj.set_defaults(fn=cmd_sujets)

    c = sub.add_parser("content", help="registre des contenus")
    c.add_argument("action", choices=["list", "add", "move", "history"])
    c.add_argument("slug", nargs="?"); c.add_argument("--kind", default="test", choices=KINDS)
    c.add_argument("--title"); c.add_argument("--to", choices=STATUSES); c.add_argument("--note")
    c.add_argument("--status", choices=STATUSES)
    c.set_defaults(fn=cmd_content)
    return ap


def main(argv: list[str] | None = None) -> int:
    cfg = load_config()
    setup_logging(cfg.get("logging.level", "INFO"), cfg.path("var") / "logs" / "engine.jsonl")
    args = build_parser().parse_args(argv)
    import time
    t0 = time.monotonic()
    params = {k: v for k, v in vars(args).items() if k not in ("fn", "cmd") and v not in (None, False, [])}
    log.info("commande démarrée", extra={"cmd": args.cmd, "params": params})
    try:
        code = int(args.fn(args) or 0)
    except Exception as exc:  # erreur lisible + trace dans le journal JSON
        log.exception("échec de la commande", extra={"cmd": args.cmd, "duree_s": round(time.monotonic() - t0, 2)})
        print(f"ERREUR : {exc}", file=sys.stderr)
        return 2
    level = log.info if code == 0 else log.warning
    level("commande terminée", extra={"cmd": args.cmd, "code": code, "duree_s": round(time.monotonic() - t0, 2)})
    return code
