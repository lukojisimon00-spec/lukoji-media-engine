"""Phase 2 — Story Engine. Projet SIMULÉ (story_fakes) pour les règles ; pilote M-Pesa réel en fin de fichier."""
import json
import os
import subprocess
from pathlib import Path

import pytest

import story_fakes as F
from lukoji_engine import config
from lukoji_engine.db import Database
from lukoji_engine.story import engine as eng, export as ex, hooks as hk, narrative, project as pj, qc as sqc, research as rs
from lukoji_engine.story import script as sc, storyboard as sb, text as tx, visual as vd
from lukoji_engine.subjects import import_dossier, subject_details, transition
from research_fakes import PAGES, URL_A, FakeOpener, make_dossier

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def db():
    d = Database(config.load_config().path("db"))
    d.migrate()
    yield d
    d.close()


def _subject(db, validate=True):
    d = make_dossier()
    d["propositions"][0]["faits"].append({"texte": "Le corridor fictif fait l'objet d'un rapport.", "type": "fait", "importance": "cle",
                                          "preuves": [{"source": "a", "extrait": "Selon ce rapport simulé"}]})
    uid = import_dossier(db, d, opener=FakeOpener(dict(PAGES)))["propositions"][0]["uid"]
    if validate:
        transition(db, uid, "valide", "test")
    claims = subject_details(db, uid)["claims"]
    conf = [f"F{c['id']}" for c in claims if c["status"] == "confirme"]
    other = [f"F{c['id']}" for c in claims if c["status"] != "confirme"]
    return uid, conf, other


@pytest.fixture
def proj(db):
    uid, conf, other = _subject(db)
    p = pj.create_project(db, uid, "documentaire_long", "test")
    rs.verify(db, p["sid"], F.analyse(), "test")
    return {"sid": p["sid"], "uid": uid, "conf": conf, "other": other}


def _facts(db, sid):
    return eng._ctx(db, pj.get_project(db, sid))["facts"]


# ------------------------------------------------------------------ projet et recherche
def test_project_requires_validated_subject_and_is_unique(db):
    uid, _, _ = _subject(db, validate=False)
    with pytest.raises(pj.StoryError, match="valide"):
        pj.create_project(db, uid)
    transition(db, uid, "valide", "test")
    p = pj.create_project(db, uid)
    assert p["status"] == "research_pending" and subject_details(db, uid)["status"] == "en_production"
    with pytest.raises(pj.StoryError, match="existe déjà"):
        pj.create_project(db, uid)


def test_research_gate_and_usage_rules(db):
    uid, conf, other = _subject(db)
    p = pj.create_project(db, uid)
    r = rs.verify(db, p["sid"], None, "test")
    assert r["statut"] == "research_pending" and any("analyse" in b for b in r["bloquant"])
    r = rs.verify(db, p["sid"], F.analyse(), "test")
    assert r["statut"] == "research_verified"
    assert rs.usage_rule("confirme", "fait") == "libre"
    assert rs.usage_rule("confirme", "declaration") == "attribution_obligatoire"
    assert rs.usage_rule("source_unique", "chiffre") == "attribution_obligatoire"
    assert rs.usage_rule("hypothese", "hypothese") == "prudence_obligatoire"
    assert rs.usage_rule("a_verifier", "fait") == rs.usage_rule("contradictoire", "fait") == "interdit"


# ------------------------------------------------------------------ hooks
def test_hooks_require_eight_types_and_score(db, proj):
    facts = _facts(db, proj["sid"])
    doc = F.hooks(proj["conf"][:2])
    ev = hk.evaluate(doc, facts)
    assert ev["choix"]["recommande"] == "H1" and not any(p["severite"] == "bloquant" for p in ev["problemes"])
    short = F.deep(doc)
    short["hooks"] = short["hooks"][:7]
    assert any(p["code"] == "types_manquants" for p in hk.evaluate(short, facts)["problemes"])


def test_hook_honesty_and_evidence_caps(db, proj):
    facts = _facts(db, proj["sid"])
    doc = F.hooks(proj["conf"][:2])
    doc["hooks"][0]["voix_off"] += " Une histoire incroyable que personne ne connaît."
    doc["hooks"][1]["voix_off"] += " Elle compte 7000 membres."              # nombre non sourcé
    doc["hooks"][2]["faits"] = [proj["other"][0]]                            # fait non confirmé
    ev = hk.evaluate(doc, facts)
    r = {x["id"]: x for x in ev["resultats"]}
    assert r["H1"]["criteres"]["honnetete_promesse"]["retenue"] == 2 and not r["H1"]["elimine"]
    assert r["H2"]["elimine"] and r["H2"]["criteres"]["coherence_preuves"]["retenue"] == 1
    assert r["H3"]["elimine"]                                                # interdit, ou attribution manquante
    assert ev["choix"]["recommande"] not in ("H2", "H3")
    doc["choisi"] = "H2"
    assert any(p["code"] == "choix_elimine" for p in hk.evaluate(doc, facts)["problemes"])


# ------------------------------------------------------------------ structure
def test_structure_rules(db, proj):
    facts = _facts(db, proj["sid"])
    ok = narrative.evaluate(F.structure(proj["conf"]), facts, "documentaire_long")
    assert not [p for p in ok["problemes"] if p["severite"] == "bloquant"]
    bad = F.structure(proj["conf"])
    bad["type"] = "inconnue"
    bad["etapes"] = [s for s in bad["etapes"] if s["role"] != "limites"][1:]
    bad["etapes"][0]["faits"] = [proj["other"][0]]
    codes = {p["code"] for p in narrative.evaluate(bad, facts, "documentaire_long")["problemes"]}
    assert {"structure_inconnue", "ouverture", "nuance_absente"} <= codes
    assert set(narrative.CATALOGUE) == set(tx.story_config()["structures"]["catalogue"])


# ------------------------------------------------------------------ texte et durée
def test_duration_and_text_tools():
    assert tx.speech_seconds("mot " * 150) == 60.0
    assert tx.numbers("29,5 millions, 287 400 et 287,400 agents ; 7 % en 2007") == {"29.5", "287400", "7", "2007"}
    assert tx.find_cliches("Dans un monde où tout change, plongeons.", tx.story_config()["ecriture"]["cliches"]) == ["dans un monde où", "plongeons"]
    assert tx.repetitions("l'argent l'argent l'argent", 60, 3) == [("argent", 3)]


# ------------------------------------------------------------------ script
def test_script_checks(db, proj):
    facts, st, hooks = _facts(db, proj["sid"]), F.structure(proj["conf"]), F.hooks(proj["conf"][:2])
    good = sc.evaluate(F.script(proj["conf"]), facts, st, hooks, "documentaire_long")
    assert not [p for p in good["problemes"] if p["severite"] == "bloquant"], good["problemes"]
    assert 360 <= good["duree_s"] <= 480 and good["sequences"][0]["sources"]
    bad = F.script(proj["conf"], filler=1)
    bad["sequences"][0]["voix_off"] = "Une autre ouverture. Dans un monde où tout change, la coopérative compte 4512 membres."
    bad["sequences"][1]["faits"] = [proj["other"][0]]
    codes = {p["code"] for p in sc.evaluate(bad, facts, st, hooks, "documentaire_long")["problemes"]}
    assert {"duree_hors_format", "hook_absent", "chiffre_non_source", "cliche"} <= codes
    assert codes & {"fait_interdit", "attribution_manquante"}


# ------------------------------------------------------------------ storyboard et direction
def test_storyboard_checks():
    script_doc = F.script(["F1"])
    good = sb.evaluate(F.storyboard(script_doc), script_doc)
    assert not [p for p in good["problemes"] if p["severite"] == "bloquant"], good["problemes"][:3]
    assert good["types_distincts"] >= 6
    bad = F.storyboard(script_doc)
    bad["scenes"][0]["voix_off"] = "Texte qui ne correspond pas."
    bad["scenes"][4].pop("mention_ecran", None)
    bad["scenes"][1]["type_visuel"] = "image_generee"
    for s in bad["scenes"][5:9]:
        s["type_visuel"], s["authenticite"] = "carte", "graphique_explicatif"
    codes = {p["code"] for p in sb.evaluate(bad, script_doc)["problemes"]}
    assert {"voix_off_desynchronisee", "mention_manquante", "authenticite_incoherente", "monotonie"} <= codes


def test_visual_director():
    assert not vd.evaluate(F.visual())["problemes"]
    bad = F.visual()
    bad["palette"]["accents"].append("#00FF00")
    bad["categories_visuelles"].pop("reconstitution")
    codes = {p["code"] for p in vd.evaluate(bad, [F.visual()])["problemes"]}
    assert {"couleur_hors_charte", "categorie_non_definie", "direction_repetitive"} <= codes
    ok = F.visual()
    ok["palette"]["accents"].append("#00FF00")
    ok["palette"]["hors_charte"] = {"#00FF00": "justification test"}
    assert "couleur_hors_charte" not in {p["code"] for p in vd.evaluate(ok)["problemes"]}


def test_qc_blocking_never_hidden_by_score():
    rep = sqc.build_report({"script": [{"severite": "bloquant", "code": "chiffre_non_source", "message": "x", "ou": "séquence S"}]}, {}, {})
    assert rep["statut"] == "bloque" and rep["score_global"] > 80 and rep["categories"]["factuel"]["score"] == 70
    assert any(s["code"] == "chiffre_non_source" for s in rep["suggestions"])


# ------------------------------------------------------------------ cycle complet, validations humaines
def _fill(db, sid, conf):
    eng.set_element(db, sid, "hooks", F.hooks(conf[:2]), "auteur")
    eng.set_element(db, sid, "structure", F.structure(conf), "auteur")
    eng.set_element(db, sid, "script", F.script(conf), "auteur")
    eng.set_element(db, sid, "visual", F.visual(), "auteur")
    eng.set_element(db, sid, "storyboard", F.storyboard(F.script(conf)), "auteur")


def test_full_workflow_requires_human_approvals_in_order(db, proj):
    sid = proj["sid"]
    _fill(db, sid, proj["conf"])
    assert pj.get_project(db, sid)["status"] == "structure_draft"          # brouillons anticipés : statut inchangé
    with pytest.raises(pj.StoryError, match="contrôle qualité"):
        eng.approve(db, sid, "structure", "editeur")                        # QC obligatoire sur les versions courantes
    with pytest.raises(pj.StoryError, match="impossible"):
        eng.approve(db, sid, "script", "editeur")                          # ordre imposé
    rep = eng.run_qc(db, sid)
    assert rep["bloquants"] == 0, [p for d in rep["categories"].values() for p in d["bloquants"]][:3]
    assert eng.approve(db, sid, "structure", "editeur")["status"] == "script_draft"
    eng.run_qc(db, sid)
    assert pj.get_project(db, sid)["status"] == "script_review"
    assert eng.approve(db, sid, "script", "editeur")["status"] == "storyboard_draft"
    eng.run_qc(db, sid)
    assert eng.approve(db, sid, "storyboard", "editeur")["status"] == "storyboard_approved"
    assert eng.finalize(db, sid, "editeur")["status"] == "ready_for_phase3"
    assert [a["stage"] for a in pj.approvals(db, pj.get_project(db, sid))] == ["structure", "script", "storyboard", "phase3"]


def test_edit_sequence_versions_stale_and_resume(db, proj):
    sid = proj["sid"]
    _fill(db, sid, proj["conf"])
    p = pj.get_project(db, sid)
    v_before = pj.current(db, p, "script")["version"]
    eng.edit_sequence(db, sid, "SEQ-03", {"voix_off": F.PHRASE.strip() * 1}, "auteur")
    p = pj.get_project(db, sid)
    assert pj.current(db, p, "script")["version"] == v_before + 1
    assert "storyboard" in pj.stale(db, p)                                   # storyboard conservé mais signalé obsolète
    assert pj.version(db, p, "script", v_before)["content"]["sequences"][2]["voix_off"] != pj.current(db, p, "script")["content"]["sequences"][2]["voix_off"]
    assert "SEQ-03" in json.dumps(pj.diff(db, p, "script", v_before, v_before + 1), ensure_ascii=False) or pj.diff(db, p, "script", v_before, v_before + 1)
    rep = eng.evaluate_all(db, p)
    assert any(x["code"] == "element_obsolete" for d in rep["categories"].values() for x in d["bloquants"])
    # Reprise : nouveau storyboard construit sur le script courant, sans perdre le script.
    eng.set_element(db, sid, "storyboard", F.storyboard(pj.current(db, p, "script")["content"]), "auteur", "régénéré")
    p = pj.get_project(db, sid)
    assert "storyboard" not in pj.stale(db, p) and pj.current(db, p, "script")["version"] == v_before + 1
    # Ré-attachement d'un élément inchangé à une nouvelle version de recherche.
    rs.verify(db, sid, dict(F.analyse(), justification="v2"), "test")
    assert "hooks" in pj.stale(db, pj.get_project(db, sid))
    eng.set_element(db, sid, "hooks", pj.current(db, p, "hooks")["content"], "auteur")
    assert "hooks" not in pj.stale(db, pj.get_project(db, sid))


def test_choose_and_edit_hook(db, proj):
    sid = proj["sid"]
    eng.set_element(db, sid, "hooks", F.hooks(proj["conf"][:2]), "auteur")
    eng.choose_hook(db, sid, "H3", "test de choix", "editeur")
    p = pj.get_project(db, sid)
    assert pj.current(db, p, "hooks")["content"]["choisi"] == "H3"
    eng.edit_hook(db, sid, "H3", {"son": "silence"}, "editeur")
    assert pj.current(db, pj.get_project(db, sid), "hooks")["content"]["hooks"][2]["son"] == "silence"
    with pytest.raises(pj.StoryError):
        eng.choose_hook(db, sid, "H99", "", "editeur")


# ------------------------------------------------------------------ exports, CLI, Media Center
def test_exports_json_schema_and_markdown(db, proj, tmp_path):
    sid = proj["sid"]
    _fill(db, sid, proj["conf"])
    out = ex.export_bundle(db, sid, tmp_path / "exp")
    files = set(out["fichiers"])
    assert {"storyboard.json", "script.md", "storyboard.md", "direction_artistique.md", "verification_factuelle.md", "qc.md", "bundle.json"} <= files
    doc = json.loads((tmp_path / "exp" / "storyboard.json").read_text())
    assert ex.validate_storyboard_json(doc) == [] and doc["schema"] == "lukoji.storyboard/1.0"
    assert doc["scenes"][0]["debut_s"] == 0 and doc["rythme"]["duree_totale_s"] > 0
    broken = F.deep(doc)
    broken["scenes"][1]["debut_s"] = -5
    del broken["scenes"][2]["visuel"]["type"]
    assert len(ex.validate_storyboard_json(broken)) >= 2
    schema = json.loads((ROOT / "schemas" / "storyboard.schema.json").read_text())
    assert set(schema["required"]) <= set(doc)
    assert "SEQ-01" in (tmp_path / "exp" / "script.md").read_text()


def test_cli_story(db, proj, tmp_path):
    sid = proj["sid"]
    files = {}
    for k, d in (("hooks", F.hooks(proj["conf"][:2])), ("structure", F.structure(proj["conf"])), ("script", F.script(proj["conf"])),
                 ("direction", F.visual()), ("storyboard", F.storyboard(F.script(proj["conf"])))):
        files[k] = tmp_path / f"{k}.json"
        files[k].write_text(json.dumps(d, ensure_ascii=False))
    run = lambda *a: subprocess.run([str(ROOT / "bin/lukoji"), "story", *a], capture_output=True, text=True, env=dict(os.environ))
    for k in ("hooks", "structure", "script", "direction", "storyboard"):
        r = run(k, sid, "--file", str(files[k]))
        assert r.returncode == 0, r.stderr
    for args in (("list",), ("show", sid), ("qc", sid), ("versions", sid), ("export", sid, "--out", str(tmp_path / "e")),
                 ("html", sid, "--out", str(tmp_path / "m.html"))):
        assert run(*args).returncode == 0, args
    assert run("approve", sid, "--etape", "structure").returncode == 0
    bad = run("approve", sid, "--etape", "storyboard")
    assert bad.returncode == 2 and "impossible" in bad.stderr
    assert run("diff", sid, "--element", "script", "1", "1").returncode == 0


def test_media_center_story_page(db, proj):
    from lukoji_engine.mediacenter import render_story_html
    _fill(db, proj["sid"], proj["conf"])
    page = render_story_html(db, proj["sid"])
    for anchor in ("angle", "preuves", "hooks", "structure", "script", "storyboard", "direction", "qc", "versions"):
        assert f'id="{anchor}"' in page
    assert "viewport" in page and "<script" not in page


def test_existing_data_protected(db, proj):
    before = {t: db.conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in
              ("subjects", "claims", "claim_evidence", "sources", "assets", "contents", "renders")}
    _fill(db, proj["sid"], proj["conf"])
    eng.run_qc(db, proj["sid"])
    after = {t: db.conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in before}
    assert before == after


# ------------------------------------------------------------------ pilote réel M-Pesa
STORY = ROOT / "research" / "stories" / "mpesa"
CAPS1 = ROOT / "research" / "captures" / "2026-11-27"


@pytest.mark.skipif(not any(CAPS1.glob("*.txt")), reason="textes intégraux de la phase 1 absents (conservés hors Git)")
def test_pilot_mpesa_rebuilt_from_repository(db):
    """Reconstruit le pilote M-Pesa depuis les dossiers et captures du dépôt, puis exige un QC sans bloquant."""
    from lukoji_engine.subjects import complete_subject
    rep = import_dossier(db, json.loads((ROOT / "research/dossiers/2026-11-27.json").read_text()), fetch=False, captures=CAPS1)
    uid = next(p["uid"] for p in rep["propositions"] if p["titre"].startswith("M-Pesa"))
    complete_subject(db, uid, STORY / "recherche_complementaire.json", fetch=False, captures=ROOT / "research/captures/2026-11-27-mpesa")
    complete_subject(db, uid, STORY / "recherche_complementaire_2.json", fetch=False, captures=CAPS1)
    transition(db, uid, "valide", "pilote")
    p = pj.create_project(db, uid)
    assert rs.verify(db, p["sid"], json.loads((STORY / "analyse_angle.json").read_text()))["statut"] == "research_verified"
    for kind, f in (("hooks", "hooks"), ("structure", "structure"), ("script", "script"), ("visual", "direction"), ("storyboard", "storyboard")):
        eng.set_element(db, p["sid"], kind, json.loads((STORY / f"{f}.json").read_text()), "pilote")
    rep = eng.run_qc(db, p["sid"])
    assert rep["bloquants"] == 0, [x for d in rep["categories"].values() for x in d["bloquants"]][:5]
    assert 360 <= rep["indicateurs"]["script_duree_s"] <= 480
    assert rep["indicateurs"]["hook_choisi"] == "H1" and rep["details"]["storyboard"]["types_distincts"] >= 6
