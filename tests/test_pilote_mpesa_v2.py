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


V21 = ROOT / "research/stories/mpesa/v2_1/script_v2_1.json"


@pytest.mark.skipif(not V21.exists(), reason="script v2.1 absent")
@pytest.mark.parametrize("motif", [r"27 janvier 2009", r"traîne généralement", r"deuxième source de revenus",
                                   r"49 plateformes", r"\b41 ?%", r"\b8 ?% vers", r"testé à Thika, au nord",
                                   r"44,2 % des revenus de Safaricom", r"menacent"])
def test_fact_check_final_corrections_appliquees(motif):
    vo = " ".join(s["voix_off"] for s in _load(V21)["sequences"])
    assert not re.search(motif, vo, flags=re.I)


V22 = ROOT / "research/stories/mpesa/v2_2"


@pytest.mark.skipif(not (V22 / "script_v2_2.json").exists(), reason="consolidation v2.2 absente")
def test_consolidation_v2_2_coherente():
    script = _load(V22 / "script_v2_2.json")
    struct = _load(V22 / "structure_v2_2.json")
    hooks = _load(V22 / "hooks_v2_2.json")
    assert script["titre"] == "Quand les clients ont changé le produit"
    h9 = next(h for h in hooks["hooks"] if h["id"] == "H9")
    assert hooks["choisi"] == "H9" and "compagnie de bus" in h9["voix_off"]
    assert script["sequences"][0]["voix_off"] == h9["voix_off"]
    by = {e["sequence"]: e for e in struct["etapes"]}
    removed = {"F38", "F39", "F47", "F48", "F51", "F53", "F54", "F56", "F57", "F64", "F65", "F66", "F67", "F11", "F13"}
    for s in script["sequences"]:
        assert by[s["id"]]["faits"] == s["faits"], s["id"]
        assert by[s["id"]]["transition_sortie"] == (s.get("transition") or ""), s["id"]
        assert not set(s["faits"]) & removed, s["id"]
    vo = " ".join(s["voix_off"] for s in script["sequences"])
    for motif in (r"2009", r"communiqu", r"\bparis\b", r"chauffeur", r"\b49\b", r"41 ?%", r"survit au débat"):
        assert not re.search(motif, vo, flags=re.I), motif


FICHE = ROOT / "docs/stories/STO-20261127-001/v2_2/fiche_validation.json"


@pytest.mark.skipif(not FICHE.exists(), reason="fiche de validation absente")
def test_fiche_de_validation_correspond_aux_fichiers_versionnes():
    import hashlib

    def sha(o):
        return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

    fiche = _load(FICHE)
    for stage in ("structure", "script"):
        for kind, entry in fiche["etapes"][stage].items():
            if entry["fichier_versionne"]:
                assert sha(_load(ROOT / entry["fichier_versionne"])) == entry["sha256"], (stage, kind)
    verrou = ROOT / "docs/stories/STO-20261127-001/VERROU_VALIDATION.json"
    if not verrou.exists():
        assert fiche["validations_existantes"] == 0


SB26 = ROOT / "research/stories/mpesa/v2_6/storyboard_v2_6.json"


@pytest.mark.skipif(not SB26.exists(), reason="storyboard v2.6 absent")
def test_storyboard_v2_6_fidele_aux_versions_verrouillees():
    import hashlib

    def sha(o):
        return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

    lock = {v["etape"]: v for v in _load(ROOT / "docs/stories/STO-20261127-001/VERROU_VALIDATION.json")["validations"]}
    script = _load(V22 / "script_v2_2.json")
    assert sha(script) == lock["script"]["versions"]["script"]["sha256"]
    sb = _load(SB26)
    by: dict[str, list[str]] = {}
    for sc in sb["scenes"]:
        by.setdefault(sc["sequence"], []).append(sc["voix_off"])
        assert sc["authenticite"] != "image_generee", sc["id"]
        if sc["authenticite"] in ("symbolique", "illustration", "reconstitution"):
            assert sc.get("mention_ecran"), sc["id"]
        assert set(sc["source_factuelle"]) <= set(next(s for s in script["sequences"] if s["id"] == sc["sequence"])["faits"]), sc["id"]
    for seq in script["sequences"]:
        assert " ".join(v for v in by[seq["id"]] if v).split() == seq["voix_off"].split(), seq["id"]


REG261 = ROOT / "research/stories/mpesa/v2_6_1/ressources_visuelles_v2_6_1.json"


@pytest.mark.skipif(not REG261.exists(), reason="registre v2.6.1 absent")
def test_revue_2_6_1_tracabilite_et_storyboard_intact():
    reg = {r["id"]: r for r in _load(REG261)["ressources"]}
    for rid in ("R02", "R03"):
        assert reg[rid]["statut"] != "contenu_inspecte" and "NON inspecté" in reg[rid]["inspection"]
    for rid in ("R01", "R04", "R06", "R11"):
        assert reg[rid]["statut"] == "contenu_inspecte"
    v26 = {r["id"]: r for r in _load(ROOT / "research/stories/mpesa/v2_6/ressources_visuelles_v2_6.json")["ressources"]}
    assert v26["R04"]["statut"] == "metadonnees_verifiees"  # registre v2.6 conservé tel quel
    sb = _load(SB26)
    assert len(sb["scenes"]) == 50 and sb["base_validee"] == {"script": 21, "structure": 6}


SB262 = ROOT / "research/stories/mpesa/v2_6_2/storyboard_v2_6_2.json"


@pytest.mark.skipif(not SB262.exists(), reason="storyboard v2.6.2 absent")
def test_storyboard_v10_corrections_ciblees():
    v9, v10 = _load(SB26), _load(SB262)
    assert [s["id"] for s in v9["scenes"]] == [s["id"] for s in v10["scenes"]]
    for a, b in zip(v9["scenes"], v10["scenes"]):
        assert a["voix_off"] == b["voix_off"] and a.get("duree_s") == b.get("duree_s") and a["source_factuelle"] == b["source_factuelle"], a["id"]
        assert not set(b["ressources"]) & {"R01", "R02", "R03", "R28"}, b["id"]
        if b["authenticite"] in ("symbolique", "illustration", "reconstitution"):
            assert b.get("mention_ecran"), b["id"]
    changed = [b["id"] for a, b in zip(v9["scenes"], v10["scenes"]) if a != b]
    assert changed == ["SC-01", "SC-05", "SC-17", "SC-20", "SC-34", "SC-39", "SC-45", "SC-47"]
    reg = {r["id"]: r for r in _load(ROOT / "research/stories/mpesa/v2_6_2/ressources_visuelles_v2_6_2.json")["ressources"]}
    assert reg["R02"]["statut"] != "contenu_inspecte" and reg["R03"]["statut"] != "contenu_inspecte"
