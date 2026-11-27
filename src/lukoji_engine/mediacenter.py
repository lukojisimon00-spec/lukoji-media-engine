"""LUKOJI MEDIA CENTER V0 — consultation des propositions (terminal + page HTML statique).

Volontairement minimal : pas de serveur, pas d'application. Les décisions passent par la CLI
(`lukoji sujets valider|rejeter|reporter|reactiver|note`), toutes journalisées.
La page HTML est un instantané en lecture seule, autonome (aucune ressource externe sauf polices).
"""
from __future__ import annotations

import html
import json
import textwrap
from pathlib import Path

from .config import load_config
from .db import Database, now
from .scoring import CLAIM_STATUS_LABELS
from .subjects import ranked, subject_details

STATUS_FR = {"recherche": "en recherche", "propose": "proposé", "valide": "validé", "rejete": "rejeté",
             "reporte": "reporté", "en_production": "en production", "produit": "produit", "publie": "publié"}
CHECK_FR = {"verifie": "extrait retrouvé dans la page récupérée par le moteur",
            "rapporte_agent": "extrait rapporté mot pour mot par l'agent de lecture (page complète lue ; non revérifié localement)",
            "absent_de_la_page": "EXTRAIT INTROUVABLE dans la page récupérée",
            "non_probant": "source non consultée (résultat de recherche seulement)"}


def _w(text: str, indent: str = "    ", width: int = 100) -> str:
    return textwrap.fill(str(text), width=width, initial_indent=indent, subsequent_indent=indent)


def render_list(db: Database, statuses: list[str] | None = None) -> str:
    rows = ranked(db, statuses)
    if not rows:
        return "Aucun sujet."
    fam = load_config().research["familles"]
    out = [f"{'UID':18s} {'statut':11s} {'prio':>5s} {'attr':>5s} {'solid':>5s} {'R.fact':>6s} {'R.jur':>5s} {'diff':>4s}  titre"]
    for r in rows:
        s = r["score"]
        mark = "" if s.get("prioritaire") else "  ⚠ " + ",".join(f for f in r["flags"] if not f.startswith("famille_sensible"))
        out.append(f"{r['uid']:18s} {STATUS_FR[r['status']]:11s} {r['priority']:5.1f} {s['attrait']:5.1f} {s['solidite']:5.1f}"
                   f" {s['risque_factuel']:6d} {s['risque_juridique']:5d} {s['difficulte']:4d}  {r['title']}")
        out.append(f"{'':18s} {fam[r['family']]['label']} · {r['territory']} · {r['temporality']}{mark}")
    return "\n".join(out)


def render_show(db: Database, uid: str) -> str:
    s = subject_details(db, uid)
    sc = s["score"]
    o = [f"═══ {s['uid']} · {STATUS_FR[s['status']].upper()} ═══", s["title"], ""]
    for label, key in (("Sujet", "subject"), ("Angle narratif", "angle"), ("Pourquoi c'est intéressant", "interest"),
                       ("Accroche potentielle", "hook"), ("Résumé du récit", "summary"),
                       ("Potentiel visuel", "visual_potential")):
        o += [f"{label} :", _w(s[key]), ""]
    o.append(f"Famille : {s['family']} · Territoire : {s['territory']} · Temporalité : {s['temporality']} · "
             f"Entités : {', '.join(s['entities'])}")
    elig = s["formats"]["eligibilite"]
    o.append("Formats recommandés : " + ", ".join(
        f"{f} ({'soutenu' if elig[f]['eligible'] else 'NON soutenu : ' + elig[f]['condition']})" for f in s["formats"]["recommandes"])
             + (f" · épisodes : {s['episodes']}" if s["episodes"] > 1 else ""))
    o += ["", "── Score (aide au tri, pas une vérité) — formule v" + sc["version_formule"],
          f"  Priorité {sc['priorite']} = attrait {sc['attrait']} × solidité {sc['solidite']}/100 × "
          f"(1 − 0,10×(risque max − 1)) × (1 − 0,05×(difficulté − 1))",
          f"  Risque factuel {sc['risque_factuel']}/5 (calculé) · risque juridique {sc['risque_juridique']}/5 · "
          f"difficulté {sc['difficulte']}/5",
          f"  Faits clés confirmés : {sc['faits_cles']['confirmes']}/{sc['faits_cles']['total']} · "
          f"organisations A/B probantes : {', '.join(sc['organisations_AB_probantes']) or '—'}"]
    for k, v in sc["criteres"].items():
        o.append(f"  {k:20s} {v['note']}/5  — {v['justification']}")
    o.append(f"  difficulté : {sc['difficulte_justification']}")
    o.append(f"  risque juridique : {sc['risque_juridique_justification']}")
    if s["flags"]:
        o.append("  Signalements : " + ", ".join(s["flags"]))
    o += ["", "── Faits"]
    for c in s["claims"]:
        o.append(f"  [{CLAIM_STATUS_LABELS.get(c['status'], c['status'])}] ({c['kind']}, {c['importance']}) {c['text']}")
        o.append(f"      motif : {c['status_detail']}")
        for e in c["evidence"]:
            o.append(f"      · {e['stance']} — {e['organisation']} ({e['category']}) : « {e['excerpt'][:180]} »")
            o.append(f"        {CHECK_FR.get(e['excerpt_check'], e['excerpt_check'])}")
    o += ["", "── Sources"]
    for so in s["sources"]:
        o.append(f"  [{so['category']}] {so['organisation']} — {so['title']}")
        o.append(f"      {so['url']}")
        o.append(f"      publiée : {so['published_at'] or 'date non indiquée'} · consultée : {so['accessed_at']} · "
                 f"consultation : {so['consultation']} · disponibilité : {so['availability']}"
                 + (f" · rôle : {so['role']}" if so.get("role") else ""))
        if so["limitations"]:
            o.append(_w("limites : " + so["limitations"], "      "))
    if s["risks"]:
        o += ["", "── Risques"] + [_w("- " + r, "  ") for r in s["risks"]]
    if s["dedup"]:
        o += ["", "── Proximité avec des contenus existants"]
        for d in s["dedup"]:
            o.append(f"  {d['verdict']} : {d['ref']} « {d['title']} » ({d['status']}) — sujet {d['similarite_sujet']}, angle {d['similarite_angle']}")
    o += ["", "── Historique des décisions"]
    for e in s["events"]:
        o.append(f"  {e['at']} {e['from_status'] or '—'} → {e['to_status']} ({e['actor']}) {e['note'] or ''}")
    for n in s["notes"]:
        o.append(f"  {n['at']} remarque ({n['actor']}) : {n['note']}")
    return "\n".join(o)


def render_compare(db: Database, uids: list[str]) -> str:
    subs = [subject_details(db, u) for u in uids]
    rows = [("UID", lambda s: s["uid"]), ("Statut", lambda s: STATUS_FR[s["status"]]),
            ("Titre", lambda s: s["title"]), ("Angle", lambda s: s["angle"]), ("Accroche", lambda s: s["hook"]),
            ("Formats", lambda s: ", ".join(s["formats"]["recommandes"])),
            ("Priorité", lambda s: s["score"]["priorite"]), ("Attrait", lambda s: s["score"]["attrait"]),
            ("Solidité", lambda s: s["score"]["solidite"]),
            ("Faits clés confirmés", lambda s: f"{s['score']['faits_cles']['confirmes']}/{s['score']['faits_cles']['total']}"),
            ("Risque fact./jur.", lambda s: f"{s['score']['risque_factuel']}/{s['score']['risque_juridique']}"),
            ("Difficulté", lambda s: s["score"]["difficulte"]),
            ("Signalements", lambda s: ", ".join(s["flags"]) or "—")]
    out = []
    for label, fn in rows:
        out.append(f"■ {label}")
        for s in subs:
            out.append(_w(f"{s['uid']} : {fn(s)}", "   ", 110))
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Page HTML statique (lecture seule)
# ---------------------------------------------------------------------------
_CSS = """
:root{--noir:#0B0B0B;--blanc:#FFFFFF;--clair:#F6F6F3;--g1:#BDBDBD;--g2:#9A9A9A;--g3:#555555;--or:#FF8A00;--rouge:#FF5A00;--jaune:#FFD23F}
*{box-sizing:border-box}body{margin:0;background:var(--clair);color:var(--noir);font:15px/1.55 "IBM Plex Mono",ui-monospace,monospace}
header{background:var(--noir);color:var(--blanc);padding:28px 16px}header h1{font:400 30px/1.1 "Archivo Black",system-ui,sans-serif;margin:0}
header p{margin:6px 0 0;color:var(--g1);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
main{max-width:980px;margin:0 auto;padding:16px}
.card{background:var(--blanc);border:1px solid #DCDCD6;border-radius:10px;padding:18px;margin:18px 0}
.card h2{font:400 21px/1.2 "Archivo Black",system-ui,sans-serif;margin:6px 0 10px}
.meta{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--g3)}
.pill{display:inline-block;border:1px solid var(--noir);border-radius:99px;padding:1px 9px;margin:2px 4px 2px 0;font-size:11px}
.warn{border-color:var(--rouge);color:var(--rouge)}.ok{background:var(--noir);color:var(--blanc)}
.scores{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin:12px 0}
.scores div{background:var(--clair);border-radius:8px;padding:8px}.scores b{display:block;font:400 20px "Archivo Black",sans-serif}
details{margin:8px 0}summary{cursor:pointer;font-weight:600}
.claim{border-left:3px solid var(--g1);padding:4px 10px;margin:8px 0}.claim.confirme{border-color:var(--noir)}
.claim.source_unique,.claim.a_verifier{border-color:var(--or)}.claim.contradictoire{border-color:var(--rouge)}
blockquote{margin:4px 0 4px 8px;color:var(--g3);font-size:13px}a{color:var(--noir)}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid #E6E6E0;padding:6px;text-align:left;vertical-align:top}
@media (max-width:600px){header h1{font-size:24px}.card{padding:14px}}
"""


def render_html(db: Database, statuses: list[str] | None = None, title: str = "Propositions éditoriales") -> str:
    e = html.escape
    subs = [subject_details(db, r["uid"]) for r in ranked(db, statuses)]
    cards = []
    for s in subs:
        sc = s["score"]
        flags = "".join(f'<span class="pill warn">{e(f)}</span>' for f in s["flags"])
        elig = s["formats"]["eligibilite"]
        fmts = "".join(f'<span class="pill {"ok" if elig[f]["eligible"] else "warn"}">{e(f)}'
                       f'{"" if elig[f]["eligible"] else " — non soutenu"}</span>' for f in s["formats"]["recommandes"])
        claims = "".join(
            f'<div class="claim {e(c["status"])}"><b>{e(CLAIM_STATUS_LABELS.get(c["status"], c["status"]))}</b> · '
            f'{e(c["kind"])}, {e(c["importance"])}<br>{e(c["text"])}<br><span class="meta">{e(c["status_detail"])}</span>'
            + "".join(f'<blockquote>« {e(x["excerpt"])} » — <a href="{e(x["url"])}">{e(x["organisation"])}</a> '
                      f'({e(x["category"])}, {e(x["stance"])}) · {e(CHECK_FR.get(x["excerpt_check"], x["excerpt_check"]))}</blockquote>'
                      for x in c["evidence"]) + "</div>" for c in s["claims"])
        srcs = "".join(f'<tr><td>{e(so["category"])}</td><td><a href="{e(so["url"])}">{e(so["title"])}</a><br>'
                       f'<span class="meta">{e(so["organisation"])} · publiée {e(so["published_at"] or "n.d.")} · '
                       f'consultée {e(so["accessed_at"])} · {e(so["consultation"])} · {e(so["availability"])}</span>'
                       + (f'<br><small>{e(so["limitations"])}</small>' if so["limitations"] else "") + "</td></tr>"
                       for so in s["sources"])
        crit = "".join(f'<tr><td>{e(k)}</td><td>{v["note"]}/5</td><td>{e(v["justification"])}</td></tr>'
                       for k, v in sc["criteres"].items())
        cards.append(f"""<section class="card" id="{e(s['uid'])}">
<div class="meta">{e(s['uid'])} · {e(STATUS_FR[s['status']])} · {e(s['family'])} · {e(s['territory'])} · {e(s['temporality'])}</div>
<h2>{e(s['title'])}</h2>{fmts}{flags}
<div class="scores"><div>priorité<b>{sc['priorite']}</b></div><div>attrait<b>{sc['attrait']}</b></div>
<div>solidité<b>{sc['solidite']}</b></div><div>faits clés<b>{sc['faits_cles']['confirmes']}/{sc['faits_cles']['total']}</b></div>
<div>risque fact.<b>{sc['risque_factuel']}/5</b></div><div>risque jur.<b>{sc['risque_juridique']}/5</b></div><div>difficulté<b>{sc['difficulte']}/5</b></div></div>
<p><b>Sujet.</b> {e(s['subject'])}</p><p><b>Angle.</b> {e(s['angle'])}</p><p><b>Accroche.</b> {e(s['hook'])}</p>
<p><b>Intérêt.</b> {e(s['interest'])}</p><p><b>Récit.</b> {e(s['summary'])}</p><p><b>Potentiel visuel.</b> {e(s['visual_potential'])}</p>
<details><summary>Faits et preuves ({len(s['claims'])})</summary>{claims}</details>
<details><summary>Sources ({len(s['sources'])})</summary><table>{srcs}</table></details>
<details><summary>Détail du score</summary><table>{crit}</table><p class="meta">Difficulté : {e(sc['difficulte_justification'])}<br>
Risque juridique : {e(sc['risque_juridique_justification'])}</p></details>
<details><summary>Risques</summary><ul>{''.join(f'<li>{e(r)}</li>' for r in s['risks'])}</ul></details>
</section>""")
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Media Center LUKOJI</title><link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{_CSS}</style></head><body><header><h1>LUKOJI MEDIA CENTER</h1><p>{e(title)} · généré le {e(now())} · lecture seule</p></header>
<main><p class="meta">Score = aide au tri (formule v{e(load_config().research['score']['version'])}, docs/SCORE_EDITORIAL.md). Les sujets signalés sont classés après les sujets sains.
Décisions : <code>./bin/lukoji sujets valider|rejeter|reporter UID --note "…"</code></p>{''.join(cards) or '<p>Aucun sujet.</p>'}</main></body></html>"""


def write_html(db: Database, out: str | Path, statuses: list[str] | None = None) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_html(db, statuses), encoding="utf-8")
    return out
