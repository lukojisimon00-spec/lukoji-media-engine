"""Pilote M-Pesa, révision v2 : contrôles sur les fichiers versionnés (sans base de données).

Vérifie que les exports v2 commités sont cohérents entre eux et n'ont pas régressé sur les corrections de l'audit
éditorial humain (commit 70d0f17), et que la version 1 reste consultable.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "docs/stories/STO-20261127-001"
V2 = V1 / "v2"
SRC = ROOT / "research/stories/mpesa/v2"

pytestmark = pytest.mark.skipif(not (V2 / "storyboard.json").exists(), reason="exports v2 absents")


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_v1_toujours_consultable():
    for f in ("script.md", "storyboard.json", "storyboard.md", "hooks.md", "qc.md", "AUDIT_EDITORIAL_HUMAIN.md"):
        assert (V1 / f).exists(), f
    assert "Au Kenya, envoyer de l'argent par téléphone est devenu un geste du quotidien." in (V1 / "script.md").read_text(encoding="utf-8")


def test_storyboard_v2_conforme_au_schema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load(ROOT / "schemas/storyboard.schema.json")
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(_load(V2 / "storyboard.json")))
    assert not errors, errors[0].message


def test_storyboard_reconstitue_le_script_mot_pour_mot():
    script = _load(SRC / "script_v2.json")
    sb = _load(V2 / "storyboard.json")
    by_seq: dict[str, list[str]] = {}
    for sc in sb["scenes"]:
        by_seq.setdefault(sc["sequence"], []).append(sc["voix_off"])
    for seq in script["sequences"]:
        assert " ".join(by_seq[seq["id"]]).split() == seq["voix_off"].split(), seq["id"]


def test_registre_aucun_fait_exclu_ou_incertain_dans_la_voix_off():
    reg = _load(V2 / "registre_factuel.json")
    script = _load(SRC / "script_v2.json")
    status = {e["ref"]: e["statut"] for e in reg["faits"]}
    vo = " ".join(s["voix_off"] for s in script["sequences"])
    for seq in script["sequences"]:
        for ref in seq["faits"]:
            assert status.get(ref) in ("confirmed", "corroborated", "single_source"), (seq["id"], ref, status.get(ref))
    for e in reg["faits"]:
        assert e["statut"] in ("confirmed", "corroborated", "single_source", "uncertain", "excluded")
        if e["utilise_v2"]:
            assert e["formulation_voix_off"] in vo, e["ref"]
        if e["statut"] == "corroborated":
            assert len(e["organisations_consultees"]) >= 2, e["ref"]


@pytest.mark.parametrize("motif", [r"\b22 ?%", r"\b77 ?%", r"\b400\b", r"90,8", r"\b2018\b", r"trop dominant",
                                   r"thèse publiée", r"maison familiale", r"Cette histoire raconte"])
def test_corrections_de_l_audit_sans_regression(motif):
    vo = " ".join(s["voix_off"] for s in _load(SRC / "script_v2.json")["sequences"])
    assert not re.search(motif, vo, flags=re.I)


def test_microcredit_revele_une_seule_fois_et_pas_dans_l_ouverture():
    seqs = _load(SRC / "script_v2.json")["sequences"]
    hits = [s["id"] for s in seqs if "microcrédit" in s["voix_off"].lower()]
    assert hits == ["SEQ-03"]


def test_scenes_authentiques_adossees_a_une_ressource_identifiee():
    res = {r["id"]: r for r in _load(SRC / "ressources_visuelles_v2.json")["ressources"]}
    for sc in _load(SRC / "storyboard_v2.json")["scenes"]:
        assert sc["authenticite"] not in ("reconstitution", "image_generee"), sc["id"]
        assert sc.get("mouvement_camera") != "camera_3d_simulee", sc["id"]
        if sc["authenticite"] == "authentique":
            assert {res[r]["statut"] for r in sc["ressources"]} <= {"metadonnees_verifiees", "a_capturer"}, sc["id"]
        if sc["authenticite"] in ("symbolique", "illustration"):
            assert sc.get("mention_ecran"), sc["id"]


def test_qc_editorial_ne_declare_jamais_le_pilote_valide():
    qc = _load(V2 / "qc_editorial.json")
    assert qc["valide"] is False
    assert qc["verdict"] in ("bloque", "pret_pour_validation_humaine")
