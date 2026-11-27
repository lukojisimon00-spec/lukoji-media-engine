"""Phase 1 — moteur de recherche et de propositions. Données SIMULÉES (voir research_fakes.py) :
aucun de ces tests n'est une recherche réelle."""
import json
import os
import subprocess
import urllib.error
from pathlib import Path

import pytest

from lukoji_engine import config, mediacenter, providers, sources as src
from lukoji_engine.db import Database
from lukoji_engine.scoring import Evidence, claim_status, compute_score, eligible_formats
from lukoji_engine.subjects import (DossierError, find_duplicates, import_dossier, ranked, search_subjects,
                                    subject_details, transition, add_note, validate_dossier)
from research_fakes import PAGES, URL_404, URL_A, URL_B1, FakeOpener, make_dossier, page

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def db():
    d = Database(config.load_config().path("db"))
    d.migrate()
    yield d
    d.close()


@pytest.fixture
def online():
    return FakeOpener(dict(PAGES))


@pytest.fixture
def offline():
    return FakeOpener({})  # tout hôte refusé, comme le proxy de cet environnement


# ---------------------------------------------------------------- URL
@pytest.mark.parametrize("url", [
    "https://www.rfi.fr/fr/afrique/20261101-article", "http://www.radiookapi.net/2026/11/01/x",
    "https://fr.wikipedia.org/wiki/Air_Afrique", "https://www.worldbank.org/en/news/press-release/2025/01/01/x",
])
def test_valid_urls(url):
    assert src.validate_url(url) == []


@pytest.mark.parametrize("url, why", [
    ("", "vide"), ("ftp://www.rfi.fr/x", "schéma"), ("https://localhost/x", "hôte"),
    ("https://www.example.com/article", "exemple"), ("https://192.168.1.10/x", "privée"),
    ("https://www.rfi .fr/x", "espaces"), ("https://www.rfi.f/x", "extension"), ("javascript:alert(1)", "schéma"),
    ("https://user:pass@www.rfi.fr/x", "identifiants"), ("https://-bad.com/x", "mal formé"),
])
def test_invalid_urls_are_rejected(url, why):
    assert any(why in p for p in src.validate_url(url)), src.validate_url(url)


def test_normalize_removes_tracking_and_fragment():
    assert src.normalize_url("https://WWW.RFI.fr/a?utm_source=x&id=3#top") == "https://www.rfi.fr/a?id=3"


# ---------------------------------------------------------------- sources
def test_classification_registry_and_defaults():
    assert src.classify("https://www.rfi.fr/x")["category"] == "B"
    assert src.classify("https://data.gouv.fr/x") == {"organisation": "Gouvernement français", "category": "A",
                                                      "nature": "gouvernement", "category_origin": "registre"}
    assert src.classify("https://fr.wikipedia.org/wiki/X")["category"] == "C"
    unknown = src.classify("https://blog-inconnu.net/x")
    assert unknown["category"] == "C" and unknown["category_origin"] == "defaut_C"
    declared = src.classify("https://institut-inconnu.org/x", {"categorie": "B", "justification_categorie": "revue à comité",
                                                               "organisation": "Institut"})
    assert declared["category"] == "B" and declared["category_origin"] == "declaree"
    # catégorie déclarée SANS justification : ignorée
    assert src.classify("https://institut-inconnu.org/x", {"categorie": "A"})["category"] == "C"


def test_fetch_parses_metadata_and_text(online):
    fr = src.fetch(URL_A, online)
    assert fr.ok and fr.availability == "disponible"
    assert fr.title == "Rapport simulé" and fr.published_at.startswith("2026-10-01")
    assert "ne pas lire" not in fr.text and "1,2 million de tonnes" in fr.text
    assert src.excerpt_in_text("le corridor fictif a transporté 1,2 million", fr.text)
    assert not src.excerpt_in_text("le corridor a transporté 5 millions", fr.text)


def test_excerpt_tolerates_typography_only():
    text = "L’entreprise a levé « 30 millions » de dollars"
    assert src.excerpt_in_text("L'entreprise a levé \"30 millions\" de dollars", text)
    assert not src.excerpt_in_text("L'entreprise a levé 40 millions de dollars", text)
    assert not src.excerpt_in_text("trop court", text)


def test_unavailable_vs_blocked_sources():
    o = FakeOpener({URL_404: 404, URL_A: urllib.error.URLError("timeout")})
    assert src.fetch(URL_404, o).availability == "indisponible"
    assert src.fetch(URL_A, o).availability == "inaccessible_environnement"


# ---------------------------------------------------------------- statut des faits
E = Evidence


def test_claim_status_rules():
    a, b1, b2 = E("A", "Banque mondiale", True, "soutient"), E("B", "RFI", True, "soutient"), E("B", "Le Monde", True, "soutient")
    assert claim_status("fait", [a], False)[0] == "confirme"
    assert claim_status("fait", [b1], False)[0] == "source_unique"
    assert claim_status("fait", [b1, b2], False)[0] == "confirme"
    assert claim_status("fait", [b1, E("B", "RFI", True, "soutient")], False)[0] == "source_unique"  # même organisation
    assert claim_status("fait", [E("C", "Blog", True, "soutient")] * 3, False)[0] == "a_verifier"
    assert claim_status("fait", [E("B", "RFI", False, "soutient")], False)[0] == "a_verifier"      # non probante
    assert claim_status("fait", [a, E("B", "Le Monde", True, "contredit")], False)[0] == "contradictoire"
    assert claim_status("fait", [a], True)[0] == "source_unique"            # sensible : 2 organisations exigées
    assert claim_status("fait", [a, b1], True)[0] == "confirme"
    assert claim_status("hypothese", [a, b1, b2], False)[0] == "hypothese"
    assert claim_status("opinion", [b1], False)[0] == "opinion_attribuee"


# ---------------------------------------------------------------- score
RATINGS = {k: {"note": 4, "justification": "j"} for k in
           ("potentiel_narratif", "interet_public", "originalite", "potentiel_visuel", "potentiel_hook", "pertinence_lukoji")}
LOW = {"note": 1, "justification": "j"}


def _score(claims, srcs, family="business", ratings=RATINGS, legal=LOW):
    return compute_score(ratings=ratings, claims=claims, sources=srcs, family=family, difficulty={"note": 2, "justification": "j"},
                         legal_risk=legal)


def test_score_is_transparent_and_penalises_weak_documentation():
    good = _score([{"importance": "cle", "kind": "fait", "status": "confirme"}] * 3,
                  [{"category": "A", "organisation": "BM", "probative": True},
                   {"category": "B", "organisation": "RFI", "probative": True},
                   {"category": "B", "organisation": "Le Monde", "probative": True}])
    weak = _score([{"importance": "cle", "kind": "fait", "status": "a_verifier"}] * 3,
                  [{"category": "C", "organisation": "Blog", "probative": True}])
    assert good["attrait"] == weak["attrait"] == 75.0            # même attrait…
    assert good["solidite"] == 100.0 and weak["solidite"] == 0.0  # …mais solidité calculée
    assert good["prioritaire"] and not weak["prioritaire"]
    assert "insuffisamment_documente" in weak["drapeaux"] and weak["risque_factuel"] == 5
    assert good["priorite"] > weak["priorite"] == 0.0


def test_score_requires_valid_ratings_and_flags_missing_justification():
    bad = dict(RATINGS, originalite={"note": 9, "justification": "x"})
    with pytest.raises(ValueError):
        _score([], [], ratings=bad)
    nojust = dict(RATINGS, originalite={"note": 3, "justification": ""})
    assert "justification_manquante:originalite" in _score([], [], ratings=nojust)["drapeaux"]


def test_scandal_family_has_minimum_legal_risk():
    s = _score([{"importance": "cle", "kind": "fait", "status": "confirme"}], [], family="scandale")
    assert s["risque_juridique"] >= 3 and "famille_sensible:recoupement_renforce" in s["drapeaux"]


def test_format_eligibility():
    one = [{"importance": "cle", "kind": "chiffre", "status": "confirme"}]
    srcs = [{"category": "B", "organisation": o, "probative": True} for o in ("RFI", "Le Monde", "BBC")]
    el = eligible_formats(one, srcs, "accroche", 1)
    assert el["short"]["eligible"] and el["affiche"]["eligible"] and not el["documentaire"]["eligible"]
    many = one * 6
    assert eligible_formats(many, srcs, "x", 3)["serie"]["eligible"]
    assert not eligible_formats(many, srcs, "x", 1)["serie"]["eligible"]


# ---------------------------------------------------------------- dossier
def test_dossier_validation_catches_errors():
    d = make_dossier()
    d["sources"][0]["url"] = "https://www.example.com/faux"
    d["propositions"][0]["famille"] = "inconnue"
    d["propositions"][0]["faits"][0]["preuves"][0]["source"] = "zz"
    d["propositions"][0]["faits"][1]["preuves"][0]["extrait"] = "court"
    del d["propositions"][0]["notes_editoriales"]["originalite"]
    probs = " | ".join(validate_dossier(d))
    for needle in ("domaine d'exemple", "famille inconnue", "source inconnue", "extrait manquant", "originalite"):
        assert needle in probs, needle


def test_import_with_pages_retrieved_verifies_excerpts(db, online):
    rep = import_dossier(db, make_dossier(), opener=online)
    uid = rep["propositions"][0]["uid"]
    s = subject_details(db, uid)
    assert s["status"] == "propose"
    st = lambda start: next(c["status"] for c in s["claims"] if c["text"].startswith(start))
    assert st("Le projet Alpha") == "confirme"          # 2 sources B distinctes, extraits retrouvés
    assert st("Le corridor") == "confirme"              # 1 source A
    assert st("Alpha est le plus") == "a_verifier"      # source C seule
    checks = {e["excerpt_check"] for c in s["claims"] for e in c["evidence"]}
    assert checks == {"verifie"}
    assert all(so["consultation"] == "page_verifiee" for so in s["sources"])
    assert "https://www.rfi.fr/fr/afrique/simule-article" in {so["url"] for so in s["sources"]}  # URL normalisée


def test_excerpt_not_found_in_page_is_not_evidence(db):
    o = FakeOpener(dict(PAGES, **{URL_A: page("Rapport simulé", "Texte sans le chiffre annoncé.")}))
    rep = import_dossier(db, make_dossier(), opener=o)
    s = subject_details(db, rep["propositions"][0]["uid"])
    corridor = next(c for c in s["claims"] if "corridor" in c["text"])
    assert corridor["status"] == "a_verifier" and corridor["evidence"][0]["excerpt_check"] == "absent_de_la_page"


def test_unavailable_source_is_never_probative(db):
    d = make_dossier()
    d["sources"][0]["url"] = URL_404
    o = FakeOpener(dict(PAGES, **{URL_404.rstrip("/") + "/": 404}))
    rep = import_dossier(db, d, opener=o)
    s = subject_details(db, rep["propositions"][0]["uid"])
    so = next(x for x in s["sources"] if x["url"] == URL_404)
    assert so["availability"] == "indisponible" and "indisponible" in so["limitations"]
    assert next(c for c in s["claims"] if "corridor" in c["text"])["status"] == "a_verifier"


def test_blocked_environment_keeps_agent_reading_with_explicit_limitation(db, offline):
    rep = import_dossier(db, make_dossier(), opener=offline)
    s = subject_details(db, rep["propositions"][0]["uid"])
    assert {so["availability"] for so in s["sources"]} == {"inaccessible_environnement"}
    assert all("non récupérable" in so["limitations"] for so in s["sources"])
    assert {e["excerpt_check"] for c in s["claims"] for e in c["evidence"]} == {"rapporte_agent"}
    run = db.conn.execute("SELECT status FROM research_runs WHERE id = ?", (rep["run_id"],)).fetchone()[0]
    assert run == "termine_avec_limites"


def test_search_results_alone_are_insufficient(db, offline):
    d = make_dossier()
    for s in d["sources"]:
        s["consultation"] = "resultat_recherche"
    rep = import_dossier(db, d, opener=offline)
    p = rep["propositions"][0]
    assert p["solidite"] == 0.0 and "insuffisamment_documente" in p["drapeaux"]
    assert "format_non_soutenu:short" in p["drapeaux"]


def test_invalid_dossier_creates_nothing(db):
    d = make_dossier()
    d["sources"][1]["url"] = "pas une url"
    with pytest.raises(DossierError):
        import_dossier(db, d, fetch=False)
    assert db.conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0] == 0


def test_failed_import_marks_run_as_failed(db, monkeypatch):
    import lukoji_engine.subjects as sj
    monkeypatch.setattr(sj, "compute_score", lambda **k: (_ for _ in ()).throw(RuntimeError("panne simulée")))
    with pytest.raises(RuntimeError):
        import_dossier(db, make_dossier(), fetch=False)
    assert db.conn.execute("SELECT status FROM research_runs ORDER BY id DESC").fetchone()[0] == "echec"
    assert db.conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0] == 0   # transaction annulée


# ---------------------------------------------------------------- doublons
def test_same_subject_is_refused_and_abandoned_subject_can_be_found_and_reactivated(db, offline):
    uid = import_dossier(db, make_dossier(), opener=offline)["propositions"][0]["uid"]
    transition(db, uid, "rejete", "test")
    again = make_dossier()
    again["propositions"][0]["titre"] = "[SIMULÉ] Goma : la coopérative du projet Alpha"   # autre titre, même thème
    rep = import_dossier(db, again, opener=offline)
    assert not rep["propositions"] and rep["refusees"][0]["doublon_de"]["ref"] == uid
    assert "réactiver" in rep["refusees"][0]["conseil"]
    found = search_subjects(db, "coopérative Goma Alpha", ["rejete"])
    assert found and found[0]["uid"] == uid
    assert transition(db, uid, "propose", "réactivé")["status"] == "propose"


def test_dedup_compares_angle_not_only_title():
    items = [{"ref": "X", "title": "Le café du Mayombe", "subject": "Une productrice de café du Mayombe primée",
              "angle": "Comment une productrice a remporté un prix international",
              "entities": ["Mayombe", "café"], "status": "publie", "origin": "test"}]
    same_theme_new_angle = {"titre": "Café congolais", "sujet": "La filière café du Mayombe",
                            "angle": "Pourquoi les prix mondiaux du café rendent la filière fragile",
                            "entites": ["Mayombe", "café"]}
    same_angle = dict(same_theme_new_angle, angle="Comment une productrice de café a remporté un prix international")
    unrelated = {"titre": "Air Afrique", "sujet": "Faillite d'une compagnie aérienne", "angle": "Chronique d'une faillite",
                 "entites": ["Air Afrique"]}
    v1 = find_duplicates(same_theme_new_angle, items)
    v2 = find_duplicates(same_angle, items)
    assert v1 and v1[0]["verdict"] in ("sujet_proche", "meme_sujet")
    assert v2 and v2[0]["similarite_angle"] > v1[0]["similarite_angle"]
    assert find_duplicates(unrelated, items) == []


def test_external_blog_corpus_is_read_only_and_detects_published_topics():
    from lukoji_engine.subjects import external_corpus
    folder = ROOT.parent / "lukoji-blog" / "articles"
    if not folder.is_dir():
        pytest.skip("corpus du blog absent")
    before = {f: f.stat().st_mtime for f in folder.glob("*.html")}
    items = external_corpus()
    assert items and all(i["status"] == "publie" for i in items)
    wave = {"titre": "Wave et la licence d'argent mobile en RDC", "sujet": "Wave obtient une licence de monnaie électronique en RDC",
            "angle": "ce que change la licence d'argent mobile de Wave", "entites": ["Wave", "RDC"]}
    dups = find_duplicates(wave, items)
    assert dups and dups[0]["origin"] == "blog LUKOJI"
    assert {f: f.stat().st_mtime for f in folder.glob("*.html")} == before


# ---------------------------------------------------------------- cycle de vie
def test_lifecycle_transitions_and_journal(db, offline):
    uid = import_dossier(db, make_dossier(), opener=offline)["propositions"][0]["uid"]
    with pytest.raises(ValueError):
        transition(db, uid, "publie")                    # pas de publication sans validation
    with pytest.raises(ValueError):
        transition(db, uid, "en_production")             # pas de production sans validation
    for st in ("reporte", "propose", "valide", "en_production", "produit", "publie"):
        transition(db, uid, st, f"vers {st}")
    with pytest.raises(ValueError):
        transition(db, uid, "propose")                   # publié = état final
    add_note(db, uid, "Remarque de test")
    s = subject_details(db, uid)
    assert [e["to_status"] for e in s["events"]] == ["recherche", "propose", "reporte", "propose", "valide",
                                                     "en_production", "produit", "publie"]
    assert s["notes"][0]["note"] == "Remarque de test"
    with pytest.raises(KeyError):
        transition(db, "SUJ-INCONNU", "valide")


def test_ranking_puts_flagged_subjects_last(db, offline, online):
    weak = make_dossier()
    weak["propositions"][0].update(titre="[SIMULÉ] Sujet attrayant mais non sourcé", sujet="Un sujet totalement différent sur le Japon",
                                   angle="Une histoire de samouraïs", entites=["Japon"])
    for k in weak["propositions"][0]["notes_editoriales"]:
        weak["propositions"][0]["notes_editoriales"][k]["note"] = 5
    for s in weak["sources"]:
        s["consultation"] = "resultat_recherche"
    import_dossier(db, weak, opener=offline)
    import_dossier(db, make_dossier(), opener=online)
    order = [r["title"] for r in ranked(db)]
    assert order[0].startswith("[SIMULÉ] Le projet Alpha") and order[-1].startswith("[SIMULÉ] Sujet attrayant")


# ---------------------------------------------------------------- collecteurs
def test_providers_parse_real_formats_with_simulated_responses():
    wiki = json.dumps({"query": {"search": [{"title": "Air Afrique", "snippet": "<span>compagnie</span>",
                                             "timestamp": "2026-01-01T00:00:00Z"}]}}).encode()
    gd = json.dumps({"articles": [{"title": "Titre", "url": "https://www.rfi.fr/x", "domain": "rfi.fr",
                                   "seendate": "20261101T120000Z"}, {"title": "Mauvais", "url": "https://localhost/x"}]}).encode()
    rss = b"<rss><channel><item><title>Startup kenyane</title><link>https://techcabal.com/a</link>" \
          b"<pubDate>Tue, 03 Nov 2026 10:00:00 GMT</pubDate><description>startup</description></item></channel></rss>"

    class O(FakeOpener):
        def open(self, req, timeout=None):
            u = req.full_url
            body = wiki if "wikipedia" in u else gd if "gdeltproject" in u else rss
            from research_fakes import FakeResponse
            return FakeResponse(body, 200, u)

    res = {r.provider: r for r in providers.discover("startup", ["wikipedia", "gdelt", "rss"], opener=O({}))}
    assert res["wikipedia"].hits[0].url == "https://fr.wikipedia.org/wiki/Air_Afrique"
    assert res["wikipedia"].hits[0].snippet == "compagnie"
    assert [h.url for h in res["gdelt"].hits] == ["https://www.rfi.fr/x"]        # URL invalide écartée
    assert res["gdelt"].hits[0].published_at == "2026-11-01"
    assert res["rss"].hits and res["rss"].hits[0].published_at == "2026-11-03"


def test_provider_failure_is_reported_never_fabricated(offline):
    res = providers.discover("entrepreneur", ["wikipedia", "gdelt", "rss", "inconnu"], opener=offline)
    assert all(r.error and not r.hits for r in res)
    assert {r.error["type"] for r in res} == {"inaccessible_environnement", "inconnu"}


# ---------------------------------------------------------------- Media Center & CLI
def test_media_center_views(db, online):
    uid = import_dossier(db, make_dossier(), opener=online)["propositions"][0]["uid"]
    assert uid in mediacenter.render_list(db)
    show = mediacenter.render_show(db, uid)
    assert "https://www.worldbank.org/fr/news/simule-rapport-2026" in show and "Historique des décisions" in show
    html = mediacenter.render_html(db)
    assert uid in html and "<script" not in html.split("</style>")[1]


def test_cli_is_reproducible(tmp_path):
    dossier = tmp_path / "dossier.json"
    dossier.write_text(json.dumps(make_dossier(), ensure_ascii=False), encoding="utf-8")
    env = dict(os.environ)
    run = lambda *a: subprocess.run([str(ROOT / "bin/lukoji"), *a], capture_output=True, text=True, env=env)
    r = run("recherche", "importer", str(dossier), "--no-fetch")
    assert r.returncode == 0, r.stderr
    uid = next(w for w in r.stdout.split() if w.startswith("SUJ-"))
    for args in (("sujets", "list"), ("sujets", "show", uid), ("sujets", "note", uid, "--note", "à creuser"),
                 ("sujets", "reporter", uid, "--note", "plus tard"), ("sujets", "history", uid),
                 ("sujets", "html", "--out", str(tmp_path / "mc.html")), ("sources", "list")):
        assert run(*args).returncode == 0, args
    bad = run("sujets", "statut", uid, "--to", "publie")
    assert bad.returncode == 2 and "transition interdite" in bad.stderr
    again = run("recherche", "importer", str(dossier), "--no-fetch")
    assert "REFUSÉE" in again.stdout                     # doublon détecté à la ré-exécution
