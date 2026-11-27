"""Statut des faits et score éditorial (formule documentée dans docs/SCORE_EDITORIAL.md).

Le score n'est PAS une vérité : c'est une aide au tri, décomposée en quatre axes publiés séparément
(attrait, solidité, risque, effort) puis combinés en un indice de priorité. Les sujets insuffisamment
documentés ou à risque élevé sont signalés et classés APRÈS les sujets sains, quel que soit leur attrait.
"""
from __future__ import annotations

from dataclasses import dataclass

from .config import load_config

EDITORIAL_CRITERIA = ("potentiel_narratif", "interet_public", "originalite", "potentiel_visuel",
                      "potentiel_hook", "pertinence_lukoji")
CLAIM_KINDS = ("fait", "chiffre", "declaration", "opinion", "hypothese")
CLAIM_STATUS_LABELS = {
    "confirme": "confirmé",
    "source_unique": "rapporté par une seule source fiable — à recouper",
    "a_verifier": "à vérifier",
    "contradictoire": "contradictoire — sources en désaccord",
    "opinion_attribuee": "opinion attribuée (pas un fait)",
    "hypothese": "hypothèse (jamais présentée comme un fait)",
}


@dataclass(frozen=True)
class Evidence:
    category: str        # A | B | C
    organisation: str
    probative: bool      # page consultée et extrait non démenti
    stance: str          # soutient | contredit | nuance


def claim_status(kind: str, evidence: list[Evidence], sensitive: bool) -> tuple[str, str]:
    """Statut CALCULÉ d'une affirmation + explication lisible."""
    vcfg = load_config().research["verification"]
    need = vcfg["min_sources_independantes"]
    if kind == "hypothese":
        return "hypothese", "type « hypothèse » : jamais confirmée par construction"
    strong = [e for e in evidence if e.probative and e.category in ("A", "B")]
    sup = [e for e in strong if e.stance == "soutient"]
    con = [e for e in strong if e.stance == "contredit"]
    orgs = sorted({e.organisation for e in sup})
    c_only = [e for e in evidence if e.probative and e.category == "C" and e.stance == "soutient"]
    if con:
        return "contradictoire", f"{len(con)} source(s) A/B contredisent ({', '.join(sorted({e.organisation for e in con}))})"
    if kind == "opinion":
        if sup or c_only:
            return "opinion_attribuee", "opinion documentée et attribuée à son auteur"
        return "a_verifier", "aucune source probante ne documente cette opinion"
    has_a = any(e.category == "A" for e in sup)
    if sensitive:
        if len(orgs) >= need:
            return "confirme", f"sujet sensible : {len(orgs)} organisations indépendantes ({', '.join(orgs)})"
        if len(orgs) == 1:
            return "source_unique", f"sujet sensible : une seule organisation ({orgs[0]}), {need} requises"
    else:
        if has_a:
            return "confirme", "source primaire (A) consultée : " + ", ".join(sorted({e.organisation for e in sup if e.category == 'A'}))
        if len(orgs) >= need:
            return "confirme", f"{len(orgs)} sources secondaires fiables indépendantes ({', '.join(orgs)})"
        if len(orgs) == 1:
            return "source_unique", f"une seule source fiable ({orgs[0]}) — à recouper"
    if c_only:
        return "a_verifier", "uniquement des sources complémentaires (C) : insuffisant pour confirmer"
    if any(not e.probative for e in evidence):
        return "a_verifier", "sources non probantes (non consultées, indisponibles ou extrait introuvable)"
    return "a_verifier", "aucune preuve"


def _note(entry) -> tuple[int | None, str]:
    if isinstance(entry, dict):
        return entry.get("note"), (entry.get("justification") or "").strip()
    return None, ""


def compute_score(*, ratings: dict, claims: list[dict], sources: list[dict], family: str,
                  difficulty: dict, legal_risk: dict) -> dict:
    """claims : [{importance, kind, status}] ; sources : [{category, organisation, probative}]."""
    cfg = load_config().research
    scfg = cfg["score"]
    weights = scfg["poids_attrait"]
    flags: list[str] = []

    # 1) ATTRAIT (0–100) : critères éditoriaux 1–5 justifiés.
    attrait = 0.0
    detail = {}
    for crit in EDITORIAL_CRITERIA:
        note, just = _note(ratings.get(crit))
        if note is None or not (1 <= int(note) <= 5):
            raise ValueError(f"note éditoriale manquante ou hors 1–5 : {crit}")
        if not just:
            flags.append(f"justification_manquante:{crit}")
        attrait += weights[crit] * (int(note) - 1) / 4
        detail[crit] = {"note": int(note), "poids": weights[crit], "justification": just}
    attrait = round(attrait * 100, 1)

    # 2) SOLIDITÉ (0–100) : CALCULÉE à partir des faits et des sources réellement consultées.
    key = [c for c in claims if c["importance"] == "cle" and c["kind"] not in ("opinion", "hypothese")]
    confirmed_key = [c for c in key if c["status"] == "confirme"]
    contradicted = [c for c in key if c["status"] == "contradictoire"]
    share = len(confirmed_key) / len(key) if key else 0.0
    ab_orgs = {s["organisation"] for s in sources if s["probative"] and s["category"] in ("A", "B")}
    has_a = any(s["probative"] and s["category"] == "A" for s in sources)
    solidite = 60 * share + 25 * min(1.0, len(ab_orgs) / 3) + 15 * (1 if has_a else 0)
    solidite = max(0.0, solidite - 15 * len(contradicted))
    solidite = round(solidite, 1)
    if not key:
        flags.append("aucun_fait_cle")

    # 3) RISQUES (1–5)
    unconfirmed = 1 - share if key else 1.0
    risque_factuel = min(5, 1 + round(4 * unconfirmed) + (1 if contradicted else 0))
    rj, rj_just = _note(legal_risk)
    if rj is None or not (1 <= int(rj) <= 5):
        raise ValueError("risque juridique : note 1–5 requise")
    if not rj_just:
        flags.append("justification_manquante:risque_juridique")
    family_cfg = cfg["familles"].get(family, {})
    risque_juridique = int(rj)
    if family in ("scandale", "enquete"):
        risque_juridique = max(risque_juridique, 3)  # personnes ou organisations mises en cause

    # 4) EFFORT (1–5)
    diff, diff_just = _note(difficulty)
    if diff is None or not (1 <= int(diff) <= 5):
        raise ValueError("difficulté : note 1–5 requise")
    diff = int(diff)

    # Indice de priorité (aide au tri, pas une vérité)
    risk = max(risque_factuel, risque_juridique)
    priorite = attrait * (solidite / 100) * (1 - 0.10 * (risk - 1)) * (1 - 0.05 * (diff - 1))
    priorite = round(priorite, 1)

    if solidite < scfg["solidite_min_prioritaire"]:
        flags.append("insuffisamment_documente")
    if risque_juridique >= scfg["risque_juridique_alerte"]:
        flags.append("risque_juridique_eleve")
    if risque_factuel >= 4:
        flags.append("risque_factuel_eleve")
    if contradicted:
        flags.append("contradictions_sur_faits_cles")
    if family_cfg.get("sensible"):
        flags.append("famille_sensible:recoupement_renforce")

    return {
        "version_formule": scfg["version"],
        "attrait": attrait, "solidite": solidite,
        "risque_factuel": risque_factuel, "risque_juridique": risque_juridique,
        "risque_juridique_justification": rj_just,
        "difficulte": diff, "difficulte_justification": diff_just,
        "priorite": priorite,
        "faits_cles": {"total": len(key), "confirmes": len(confirmed_key), "contradictoires": len(contradicted)},
        "organisations_AB_probantes": sorted(ab_orgs), "source_primaire": has_a,
        "criteres": detail, "drapeaux": flags,
        "prioritaire": not any(f in flags for f in ("insuffisamment_documente", "risque_juridique_eleve",
                                                    "risque_factuel_eleve", "contradictions_sur_faits_cles")),
    }


def eligible_formats(claims: list[dict], sources: list[dict], hook: str, episodes: int) -> dict:
    """Formats que les faits disponibles permettent RÉELLEMENT de soutenir."""
    confirmed = [c for c in claims if c["status"] == "confirme"]
    confirmed_key = [c for c in confirmed if c["importance"] == "cle"]
    ab_orgs = {s["organisation"] for s in sources if s["probative"] and s["category"] in ("A", "B")}
    out = {
        "short": (len(confirmed_key) >= 1 and bool(hook.strip()), "≥ 1 fait clé confirmé + une accroche"),
        "affiche": (any(c["kind"] in ("chiffre", "fait") for c in confirmed_key), "≥ 1 fait ou chiffre clé confirmé"),
        "documentaire": (len(confirmed) >= 4 and len(ab_orgs) >= 3, "≥ 4 faits confirmés et ≥ 3 organisations A/B"),
        "serie": (len(confirmed) >= 6 and len(ab_orgs) >= 3 and episodes >= 2, "≥ 6 faits confirmés, ≥ 3 organisations A/B, ≥ 2 épisodes"),
    }
    return {k: {"eligible": v[0], "condition": v[1]} for k, v in out.items()}
