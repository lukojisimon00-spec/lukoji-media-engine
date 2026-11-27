"""QC éditorial v2 du pilote M-Pesa (STO-20261127-001) — contrôle propre au pilote, SANS modifier le moteur.

Cinq volets séparés : technique, factuel, narratif, visuel, éditorial humain.
Règles :
- aucun score global : un score ne compense jamais une erreur bloquante ;
- le verdict automatique ne peut être que « bloqué » ou « prêt pour la validation humaine », JAMAIS « validé » ;
- le volet humain liste les décisions qui restent à prendre par l'éditeur ; il n'est jamais rempli par l'agent.

Lecture seule : ne modifie ni la base, ni les statuts, ni les validations.

Usage : python3 research/stories/mpesa/v2/qc_editorial_v2.py [--db var/lukoji.sqlite3] [--out docs/stories/STO-20261127-001/v2]
Code retour : 1 si au moins un contrôle bloquant échoue.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SID = "STO-20261127-001"
V1_VERSIONS = {"research": 2, "hooks": 2, "structure": 2, "script": 9, "storyboard": 2, "visual": 1}
MOTION_TYPES = {"graphique", "infographie", "typographie_animee", "carte", "animation", "comparaison", "zoom_detail"}

# Formules relevées par l'audit humain (artificielles, scolaires) : interdites dans la voix off v2.
FORMULES_ARTIFICIELLES = ["cette histoire raconte", "pour comprendre, il faut", "c'est là qu'intervient", "un acteur inattendu",
                          "au fond", "n'est pas celle d'une", "que retenir", "alors, qu'a vraiment", "d'autres usages inquiètent",
                          "attire aussi les critiques"]
# Énoncés corrigés par la v2 : leur retour serait une régression factuelle.
REGRESSIONS = {
    r"\b22 ?%": "chiffre de 22 % (origine non établie, enquête postérieure au lancement)",
    r"\b77 ?%": "chiffre de 77 % (base non établie)",
    r"sous le matelas": "« sous le matelas » (figure de style prise au pied de la lettre en v1)",
    r"\b400\b": "« 400 agences bancaires » (contredit par la Banque centrale)",
    r"90,8": "part de 90,8 % (indicateur non établi)",
    r"\b2018\b": "date « 2018 » des sénateurs (événement de novembre 2020)",
    r"trop dominant": "« trop dominant » (non attribuable aux sénateurs)",
    r"thèse publiée": "« thèse publiée » (c'est une présentation de thèse)",
    r"maison familiale": "glose « maison familiale »",
    r"dont dépend une grande partie": "glose non sourcée sur la dépendance du pays",
    r"6 mars": "jour exact du lancement (Vodafone seule)",
}


def load(db: Path) -> dict:
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    pid, status = c.execute("SELECT id, status FROM story_projects WHERE sid = ?", (SID,)).fetchone()
    arts = {}
    versions = {}
    for r in c.execute("SELECT kind, version, content_json FROM story_artifacts WHERE project_id = ? ORDER BY kind, version", (pid,)):
        versions.setdefault(r["kind"], []).append(r["version"])
        arts[(r["kind"], r["version"])] = json.loads(r["content_json"])
    cur = {k: max(v) for k, v in versions.items()}
    approvals = c.execute("SELECT COUNT(*) FROM story_approvals WHERE project_id = ?", (pid,)).fetchone()[0]
    integrity = c.execute("PRAGMA integrity_check").fetchone()[0]
    qc = c.execute("SELECT id, status, score FROM story_qc WHERE project_id = ? ORDER BY id DESC LIMIT 1", (pid,)).fetchone()
    return {"status": status, "versions": versions, "current": cur, "arts": arts, "approvals": approvals,
            "integrity": integrity, "qc_moteur": dict(qc) if qc else None}


class Report:
    def __init__(self):
        self.sections: dict[str, list] = {}

    def check(self, section: str, name: str, ok: bool, detail: str = "", blocking: bool = True):
        self.sections.setdefault(section, []).append(
            {"controle": name, "resultat": "ok" if ok else ("BLOQUANT" if blocking else "alerte"), "detail": detail})

    def info(self, section: str, name: str, detail: str):
        self.sections.setdefault(section, []).append({"controle": name, "resultat": "info", "detail": detail})

    def blocking(self) -> list:
        return [(s, c) for s, cs in self.sections.items() for c in cs if c["resultat"] == "BLOQUANT"]


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?…»])\s+(?=[A-ZÀ-Ý«])", text.strip()) if s.strip()]


def run(db: Path, out: Path) -> Report:
    d = load(db)
    rep = Report()
    script = d["arts"][("script", d["current"]["script"])]
    sb = d["arts"][("storyboard", d["current"]["storyboard"])]
    hooks = d["arts"][("hooks", d["current"]["hooks"])]
    reg = json.loads((out / "registre_factuel.json").read_text(encoding="utf-8"))
    res = {r["id"]: r for r in json.loads((HERE / "ressources_visuelles_v2.json").read_text(encoding="utf-8"))["ressources"]}
    seqs = script["sequences"]
    vo_all = " ".join(s["voix_off"] for s in seqs)
    vo_low = vo_all.lower()
    words = len(vo_all.split())

    # ------------------------------------------------------------------ TECHNIQUE
    T = "technique"
    for f in ("script.md", "storyboard.md", "storyboard.json", "direction_artistique.md", "verification_factuelle.md",
              "qc.md", "qc.json", "bundle.json", "hooks.md", "registre_factuel.md", "registre_factuel.json"):
        rep.check(T, f"export présent : {f}", (out / f).exists())
    for f in ("storyboard.json", "bundle.json", "qc.json", "registre_factuel.json"):
        try:
            json.loads((out / f).read_text(encoding="utf-8"))
            ok = True
        except Exception as e:  # noqa: BLE001
            ok = False
        rep.check(T, f"JSON lisible : {f}", ok)
    try:
        import jsonschema  # type: ignore
        schema = json.loads((ROOT / "schemas/storyboard.schema.json").read_text(encoding="utf-8"))
        errs = sorted(jsonschema.Draft202012Validator(schema).iter_errors(json.loads((out / "storyboard.json").read_text())), key=str)
        rep.check(T, "storyboard.json conforme au schéma lukoji.storyboard/1.0", not errs, f"{len(errs)} erreur(s)" + (f" : {errs[0].message}" if errs else ""))
    except ImportError:
        rep.info(T, "schéma JSON", "module jsonschema absent : conformité non vérifiée par ce script (voir tests du moteur)")
    rep.check(T, "intégrité de la base (PRAGMA integrity_check)", d["integrity"] == "ok", d["integrity"])
    for k, v in V1_VERSIONS.items():
        rep.check(T, f"version 1 conservée : {k} v{v}", v in d["versions"].get(k, []))
    rep.check(T, "version 2 créée (script postérieur à v9)", d["current"]["script"] > V1_VERSIONS["script"], f"script v{d['current']['script']}")
    rep.check(T, "aucune validation humaine enregistrée par l'agent", d["approvals"] == 0, f"{d['approvals']} validation(s)")
    rep.check(T, "statut inchangé (structure_draft)", d["status"] == "structure_draft", d["status"])
    dur = round(words / 150 * 60 + 0.6 * (len(seqs) - 1), 1)
    rep.check(T, "durée estimée dans la cible 6–8 min", 360 <= dur <= 480, f"{words} mots · ≈ {dur} s")
    sb_seq = {}
    for sc in sb["scenes"]:
        sb_seq.setdefault(sc["sequence"], []).append(sc["voix_off"])
    sync = all(" ".join(sb_seq.get(s["id"], [])).split() == s["voix_off"].split() for s in seqs)
    rep.check(T, "storyboard synchronisé mot pour mot avec le script", sync)

    # ------------------------------------------------------------------ FACTUEL
    F = "factuel"
    regf = {e["ref"]: e for e in reg["faits"]}
    used = [f for s in seqs for f in s["faits"]]
    missing = sorted({f for f in used if f not in regf})
    rep.check(F, "chaque fait cité figure au registre v2", not missing, ", ".join(missing))
    bad = sorted({f for f in used if regf.get(f, {}).get("statut") in ("uncertain", "excluded")})
    rep.check(F, "aucun fait incertain ou exclu dans la voix off", not bad, ", ".join(bad))
    absent = [e["ref"] for e in reg["faits"] if e["utilise_v2"] and e["formulation_voix_off"] not in vo_all]
    rep.check(F, "chaque formulation du registre se retrouve mot pour mot dans la voix off", not absent, ", ".join(absent))
    weak = [e["ref"] for e in reg["faits"] if e["statut"] == "corroborated" and len(e["organisations_consultees"]) < 2]
    rep.check(F, "« corroborated » = au moins deux organisations consultées", not weak, ", ".join(weak))
    vend = [e["ref"] for e in reg["faits"] if e["statut"] == "corroborated"
            and set(e["organisations_consultees"]) <= {"Vodafone", "Safaricom"}]
    rep.check(F, "un communiqué d'entreprise n'est jamais compté comme corroboration indépendante", not vend, ", ".join(vend))
    for pat, why in REGRESSIONS.items():
        m = re.search(pat, vo_all, flags=re.I)
        rep.check(F, f"pas de régression : {why}", not m, m.group(0) if m else "")
    att = [e["ref"] for e in reg["faits"] if e["utilise_v2"] and e["statut"] == "single_source" and not e["attribution"].strip()]
    rep.check(F, "chaque fait à source unique a une attribution déclarée", not att, ", ".join(att))
    counts = {s: sum(1 for e in reg["faits"] if e["utilise_v2"] and e["statut"] == s) for s in ("confirmed", "corroborated", "single_source")}
    rep.info(F, "répartition des faits utilisés", " · ".join(f"{k} {v}" for k, v in counts.items()))
    rep.check(F, "part des faits utilisés reposant sur une seule organisation", counts["single_source"] <= len(used) * 0.5,
              f"{counts['single_source']} / {len(set(used))} faits : la majorité du récit repose sur une seule source par fait",
              blocking=False)

    # ------------------------------------------------------------------ NARRATIF
    N = "narratif"
    first = {}
    for i, s in enumerate(seqs):
        for w in ("microcrédit", "prêt"):
            if w in s["voix_off"].lower() and w not in first:
                first[w] = i
    rep.check(N, "le microcrédit n'est pas révélé dans l'ouverture (SEQ-01, SEQ-02)", first.get("microcrédit", 99) >= 2,
              f"première mention : {seqs[first['microcrédit']]['id'] if 'microcrédit' in first else 'aucune'}")
    reveal = sum(1 for s in seqs if "microcrédit" in s["voix_off"].lower())
    rep.check(N, "le rebondissement (microcrédit) n'est raconté qu'une fois", reveal == 1, f"{reveal} séquence(s)")
    chosen = next((h for h in hooks["hooks"] if h["id"] == hooks["choisi"]), None)
    rep.check(N, "le hook choisi ouvre bien le script", chosen is not None and seqs[0]["voix_off"].startswith(chosen["voix_off"][:60]),
              hooks["choisi"])
    rep.check(N, "le hook choisi ne révèle pas la réponse", chosen is not None and "microcrédit" not in chosen["voix_off"].lower()
              and "prêt" not in chosen["voix_off"].lower())
    found = [f for f in FORMULES_ARTIFICIELLES if f in vo_low]
    rep.check(N, "aucune formule artificielle relevée par l'audit", not found, ", ".join(found))
    dup = []
    for a, b in zip(seqs, seqs[1:]):
        if a.get("transition") and sentences(b["voix_off"])[0].rstrip(".").lower() in a["transition"].lower():
            dup.append(a["id"])
    rep.check(N, "aucune transition ne répète la première phrase de la séquence suivante", not dup, ", ".join(dup))
    selon = sum(1 for s in seqs for p in sentences(s["voix_off"]) if p.lower().startswith(("selon", "d'après")))
    rep.check(N, "« Selon » en tête de phrase limité (≤ 5)", selon <= 5, f"{selon} phrase(s)", blocking=False)
    lens = [len(p.split()) for s in seqs for p in sentences(s["voix_off"])]
    rep.check(N, "aucune phrase de plus de 28 mots", max(lens) <= 28, f"max {max(lens)} mots")
    short = sum(1 for n in lens if n <= 6)
    rep.check(N, "phrases courtes de rupture présentes (≥ 4)", short >= 4, f"{short} phrase(s) de 6 mots ou moins", blocking=False)
    longest = max(seqs, key=lambda s: len(s["voix_off"].split()))
    rep.check(N, "aucune séquence ne dépasse 20 % de la durée", len(longest["voix_off"].split()) <= words * 0.2,
              f"{longest['id']} : {len(longest['voix_off'].split())} mots / {words}", blocking=False)
    rep.check(N, "la RDC est préparée avant la conclusion", any("Congo" in s["voix_off"] for s in seqs[:-1]))

    # ------------------------------------------------------------------ VISUEL
    V = "visuel"
    scenes = sb["scenes"]
    n = len(scenes)
    motion = sum(1 for sc in scenes if sc["type_visuel"] in MOTION_TYPES)
    rep.check(V, "motion design ≤ 60 % des scènes", motion / n <= 0.60, f"{motion}/{n} ({motion / n:.0%})", blocking=False)
    rep.check(V, "aucune caméra 3D simulée", not any(sc.get("mouvement_camera") == "camera_3d_simulee" for sc in scenes))
    rep.check(V, "aucun zoom lent", not any("zoom" in (sc.get("mouvement_camera") or "") and "lent" in sc["mouvement_camera"] for sc in scenes),
              blocking=False)
    rep.check(V, "aucune reconstitution impossible à produire gratuitement", not any(sc["authenticite"] == "reconstitution" for sc in scenes))
    rep.check(V, "aucune image générée", not any(sc["authenticite"] == "image_generee" for sc in scenes))
    bad_auth = []
    for sc in scenes:
        if sc["authenticite"] == "authentique":
            st = {res[r]["statut"] for r in sc.get("ressources", [])}
            if not st or not st <= {"metadonnees_verifiees", "a_capturer"}:
                bad_auth.append(sc["id"])
    rep.check(V, "chaque scène « authentique » repose sur une ressource identifiée (métadonnées vérifiées ou page à capturer)",
              not bad_auth, ", ".join(bad_auth))
    no_mention = [sc["id"] for sc in scenes if sc["authenticite"] in ("symbolique", "illustration", "reconstitution") and not sc.get("mention_ecran")]
    rep.check(V, "chaque image symbolique ou illustration porte une mention à l'écran", not no_mention, ", ".join(no_mention))
    fil = sum(1 for sc in scenes if "fil" in (sc.get("instructions_montage") or "").lower() and "apparition du fil" in (sc.get("instructions_montage") or "").lower())
    rep.check(V, "fil orange utilisé avec parcimonie (≤ 3 apparitions)", fil <= 3, f"{fil} apparition(s) déclarée(s)")
    run_, mx, prev = 0, 0, None
    for sc in scenes:
        fam = "motion" if sc["type_visuel"] in MOTION_TYPES else sc["type_visuel"]
        run_ = run_ + 1 if fam == prev else 1
        prev, mx = fam, max(mx, run_)
    rep.check(V, "pas plus de 4 scènes de motion design consécutives", mx <= 4, f"suite maximale : {mx}", blocking=False)
    pending = sorted({r for sc in scenes for r in sc.get("ressources", []) if res[r]["statut"] in ("a_capturer", "a_produire")})
    rep.info(V, "ressources à capturer ou à produire en Phase 3", ", ".join(pending))
    non = [r["id"] + " " + r["description"] for r in res.values() if r["statut"] == "non_obtenue"]
    rep.info(V, "ressources non obtenues (substituts prévus)", " ; ".join(non))
    rep.check(V, "contenu visuel des photos contrôlé par un humain", False,
              "métadonnées seules lues par l'agent : contrôle visuel à faire par l'éditeur", blocking=False)

    # ------------------------------------------------------------------ HUMAIN
    H = "editorial_humain"
    for q in ("Valider (ou non) la structure v2 — étape « structure » (commande story approve, par l'éditeur seulement).",
              "Choix du hook : H9 (choix éditorial) contre H1 (recommandation du score automatique).",
              "Accepter que la majorité des faits reposent sur une seule organisation, ou demander des corroborations.",
              "Décider si la menace des sénateurs, datée par indices concordants, peut rester avec « novembre 2020 ».",
              "Contrôler visuellement les photos Wikimedia retenues (R01–R04, R06, R11).",
              "Titre du projet en base (« le prêt par SMS … révolution ») : à corriger par l'éditeur ; le script v2 porte « le détournement qui a changé l'argent au Kenya ».",
              "Valider le script puis le storyboard dans l'ordre, après la structure."):
        rep.check(H, q, False, "décision humaine en attente — jamais remplie par l'agent", blocking=False)
    rep.info(H, "QC automatique du moteur (pour mémoire, non décisionnel)",
             f"QC n° {d['qc_moteur']['id']} : {d['qc_moteur']['status']} · {d['qc_moteur']['score']}" if d["qc_moteur"] else "aucun")
    return rep


def to_markdown(rep: Report) -> str:
    blk = rep.blocking()
    verdict = "BLOQUÉ" if blk else "PRÊT POUR LA VALIDATION HUMAINE (non validé)"
    titles = {"technique": "QC technique", "factuel": "QC factuel", "narratif": "QC narratif", "visuel": "QC visuel",
              "editorial_humain": "QC éditorial humain (décisions en attente)"}
    L = ["# QC éditorial — version 2", "", f"**Verdict automatique : {verdict}**", "",
         "> Aucun score global : une erreur bloquante n'est jamais compensée par d'autres résultats. "
         "Ce verdict ne vaut pas validation : seules les décisions de l'éditeur (dernier volet) peuvent valider le pilote.", ""]
    for key, label in titles.items():
        cs = rep.sections.get(key, [])
        n_ok = sum(1 for c in cs if c["resultat"] == "ok")
        L += [f"## {label}", "", f"{n_ok} contrôle(s) ok · {sum(1 for c in cs if c['resultat'] == 'BLOQUANT')} bloquant(s) · "
              f"{sum(1 for c in cs if c['resultat'] == 'alerte')} alerte(s)", "", "| Contrôle | Résultat | Détail |", "|---|---|---|"]
        for c in cs:
            L.append(f"| {c['controle']} | {c['resultat']} | {c['detail']} |")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "var/lukoji.sqlite3"))
    ap.add_argument("--out", default=str(ROOT / f"docs/stories/{SID}/v2"))
    a = ap.parse_args()
    out = Path(a.out)
    r = run(Path(a.db), out)
    (out / "qc_editorial.json").write_text(json.dumps({"verdict": "bloque" if r.blocking() else "pret_pour_validation_humaine",
                                                      "valide": False, "sections": r.sections}, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "qc_editorial.md").write_text(to_markdown(r), encoding="utf-8")
    for s, c in r.blocking():
        print(f"BLOQUANT [{s}] {c['controle']} — {c['detail']}")
    print(f"QC éditorial v2 : {'BLOQUÉ' if r.blocking() else 'prêt pour la validation humaine (non validé)'} → {out}/qc_editorial.md")
    sys.exit(1 if r.blocking() else 0)
