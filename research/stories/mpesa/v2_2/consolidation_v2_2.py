"""Phase 2.4 — exports consolidés et contrôle de cohérence du pilote M-Pesa (STO-20261127-001).

Lecture seule sur la base. Produit dans docs/stories/STO-20261127-001/v2_2/ :
- script.md                 : script consolidé, durée calculée sur les mots (débit de config/story.toml)
- structure.md              : structure narrative consolidée
- qc_consolidation.md/.json : contrôles de cohérence (aucun ne vaut validation éditoriale)

Pourquoi un export propre : l'export du moteur calcule la durée et le minutage des séquences à partir des
scènes du storyboard ; le storyboard v7 étant obsolète (non reconstruit, à la demande de l'éditeur), son en-tête
serait faux. Le moteur n'est pas modifié.

Usage : python3 research/stories/mpesa/v2_2/consolidation_v2_2.py   (code retour 1 si un contrôle bloquant échoue)
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))
from lukoji_engine.story.factcheck import check_passage, facts_index  # noqa: E402  (lecture seule)
from lukoji_engine.story.text import speech_seconds, story_config, word_count  # noqa: E402

SID = "STO-20261127-001"
TITLE = "Quand les clients ont changé le produit"
OUT = ROOT / f"docs/stories/{SID}/v2_2"
REMOVED = ["F38", "F39", "F47", "F48", "F51", "F53", "F54", "F56", "F57", "F64", "F65", "F66", "F67", "F11", "F13", "F70", "F71"]
KEEP_VERSIONS = {"script": [9, 13, 16], "structure": [2, 3, 4], "research": [2, 3, 4], "hooks": [2, 3, 4], "storyboard": [2, 7]}
H9 = ("Pour envoyer de l'argent à sa famille, au Kenya, on pouvait voyager pendant des jours. Ou confier son argent à une "
      "compagnie de bus, et attendre. Aujourd'hui, quelques SMS suffisent. Le service s'appelle M-Pesa. Et ses concepteurs "
      "ne l'avaient pas inventé pour ça.")


def load():
    c = sqlite3.connect(ROOT / "var/lukoji.sqlite3")
    c.row_factory = sqlite3.Row
    p = dict(c.execute("SELECT * FROM story_projects WHERE sid = ?", (SID,)).fetchone())
    arts, vers = {}, {}
    for r in c.execute("SELECT kind, version, content_json, based_on_json FROM story_artifacts WHERE project_id = ? ORDER BY version",
                       (p["id"],)):
        vers.setdefault(r["kind"], []).append(r["version"])
        arts[r["kind"]] = (r["version"], json.loads(r["content_json"]), json.loads(r["based_on_json"]))
    return {"p": p, "arts": arts, "vers": vers,
            "approvals": c.execute("SELECT COUNT(*) FROM story_approvals WHERE project_id = ?", (p["id"],)).fetchone()[0],
            "integrity": c.execute("PRAGMA integrity_check").fetchone()[0]}


def durations(script: dict) -> tuple[list, float]:
    cfg = story_config()["rythme"]
    wpm, pause = cfg["mots_par_minute"], cfg["pause_entre_sequences_s"]
    t, out = 0.0, []
    for i, s in enumerate(script["sequences"]):
        d = speech_seconds(s["voix_off"])
        out.append((s["id"], round(t, 1), round(t + d, 1), d))
        t += d + (pause if i < len(script["sequences"]) - 1 else 0)
    return out, round(t, 1)


def main() -> int:
    d = load()
    (sv, script, s_based), (stv, struct, st_based) = d["arts"]["script"], d["arts"]["structure"]
    (hv, hooks, h_based), (rv, research, _) = d["arts"]["hooks"], d["arts"]["research"]
    vv = d["arts"]["visual"][0]
    facts = facts_index(research)
    timing, total = durations(script)
    wpm = story_config()["rythme"]["mots_par_minute"]
    words = sum(word_count(s["voix_off"]) for s in script["sequences"])
    vo = " ".join(s["voix_off"] for s in script["sequences"])
    checks = []

    def chk(cat, name, ok, detail="", blocking=True):
        checks.append({"categorie": cat, "controle": name, "resultat": "ok" if ok else ("BLOQUANT" if blocking else "alerte"), "detail": detail})

    # Alignement script / structure
    st_by = {e["sequence"]: e for e in struct["etapes"]}
    mis = [s["id"] for s in script["sequences"] if s["id"] not in st_by or st_by[s["id"]]["faits"] != s["faits"]
           or st_by[s["id"]]["id"] != s["etape"]]
    chk("alignement", "chaque séquence a son étape, avec les mêmes faits", not mis and len(struct["etapes"]) == len(script["sequences"]), ", ".join(mis))
    tr = [s["id"] for s in script["sequences"] if (s.get("transition") or "") != st_by.get(s["id"], {}).get("transition_sortie", None)]
    chk("alignement", "transitions identiques dans le script et la structure", not tr, ", ".join(tr))
    # Rattachements
    chk("versions", "hooks, structure et script rattachés au dossier factuel courant",
        h_based.get("research") == rv and st_based.get("research") == rv and s_based.get("research") == rv,
        f"dossier v{rv} · hooks {h_based} · structure {st_based} · script {s_based}")
    chk("versions", "script rattaché aux hooks et à la structure courants",
        s_based.get("hooks") == hv and s_based.get("structure") == stv, f"script basé sur {s_based}")
    for k, vs in KEEP_VERSIONS.items():
        miss = [v for v in vs if v not in d["vers"].get(k, [])]
        chk("versions", f"versions antérieures conservées : {k} {vs}", not miss, f"manquantes : {miss}" if miss else "")
    # Script / dossier factuel
    problems = []
    for s in script["sequences"]:
        problems += [p for p in check_passage(s["voix_off"], s["faits"], facts, s["id"]) if p["severite"] == "bloquant"]
    chk("factuel", "faits connus, utilisables, attribués ; chaque nombre présent dans un fait ou une preuve (contrôle du moteur)",
        not problems, " ; ".join(f"{p['ou']} : {p['message']}" for p in problems))
    cited = {f for s in script["sequences"] for f in s["faits"]} | {f for e in struct["etapes"] for f in e["faits"]}
    bad = sorted(cited & set(REMOVED))
    chk("factuel", "aucun fait retiré cité (script et structure)", not bad, ", ".join(bad))
    for pat, why in {r"2009|communiqu|traîne": "communiqué de la Banque centrale de 2009",
                     r"\bparis\b|\bpari\b|betting|jeux d": "paris en ligne",
                     r"chauffeur": "« chauffeur de bus » (version non prudente du hook)",
                     r"\b49\b|41 ?%|90,8|\b400\b|\b22 ?%|\b77 ?%": "chiffres retirés"}.items():
        m = re.search(pat, vo, flags=re.I)
        chk("factuel", f"absent de la voix off : {why}", not m, m.group(0) if m else "")
    # Titre, hook, durée
    chk("titre", "titre du projet en base", d["p"]["title"] == TITLE, d["p"]["title"])
    chk("titre", "titre du script", script.get("titre") == TITLE, script.get("titre", ""))
    h9 = next(h for h in hooks["hooks"] if h["id"] == "H9")
    chk("hook", "H9 prudent choisi et identique à l'ouverture du script",
        hooks["choisi"] == "H9" and h9["voix_off"] == H9 and script["sequences"][0]["voix_off"] == H9)
    chk("duree", f"durée calculée sur les mots ({wpm} mots/min + pauses) dans la cible 6-8 min", 360 <= total <= 480,
        f"{words} mots (décompte du moteur) · {total} s · {total / 60:.1f} min")
    # Base et statut
    chk("base", "intégrité de la base", d["integrity"] == "ok", d["integrity"])
    chk("base", "aucune validation enregistrée", d["approvals"] == 0, str(d["approvals"]))
    chk("base", "statut inchangé : structure_draft", d["p"]["status"] == "structure_draft", d["p"]["status"])
    chk("storyboard", "storyboard non reconstruit (v7, obsolète par décision)", max(d["vers"]["storyboard"]) == 7,
        "à reprendre après validation du script et de la structure", blocking=False)

    OUT.mkdir(parents=True, exist_ok=True)
    # Script consolidé
    L = [f"# Script — {d['p']['title']}", "",
         f"`{SID}` · version éditoriale **v2.2** (moteur : script v{sv}, structure v{stv}, hooks v{hv}, dossier factuel v{rv}, direction v{vv}) · "
         f"**{words} mots · durée estimée {total} s ≈ {total / 60:.1f} min** ({wpm} mots/min, pauses comprises) · statut `{d['p']['status']}` · **NON VALIDÉ**", ""]
    tm = {x[0]: x for x in timing}
    for s in script["sequences"]:
        _, a, b, du = tm[s["id"]]
        srcs = []
        for f in s["faits"]:
            for pv in facts[f]["preuves"]:
                if pv["source"] not in srcs:
                    srcs.append(pv["source"])
        L += [f"## {s['id']} — {s['titre']}", "",
              f"*{a:.0f}–{b:.0f} s · voix {du} s · étape {s['etape']} · objectif : {s['objectif']} · émotion : {s['emotion']}*", "",
              s["voix_off"], "", f"Faits : {', '.join(s['faits'])} · Sources : {', '.join(srcs)}  ",
              f"Transition : {s.get('transition') or '—'}", ""]
    (OUT / "script.md").write_text("\n".join(L), encoding="utf-8")
    # Structure consolidée
    L = [f"# Structure narrative — {d['p']['title']}", "",
         f"Structure v{stv} (moteur) · type « {struct['type']} » · alignée sur le script v{sv} · **NON VALIDÉE**", "",
         f"**Promesse** : {struct['promesse']}", "", f"**Angle** : {struct['angle']}", "",
         "| Étape | Séq. | Rôle | Fonction narrative | Conflit / question / progression | Indispensable | Secondaire | Risque de décrochage | Faits | Durée | Transition de sortie |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for e in struct["etapes"]:
        L.append(f"| {e['id']} | {e['sequence']} | {e['role']} | {e['fonction_narrative']} | {e['conflit_question_progression']} | "
                 f"{' ; '.join(e['informations_indispensables'])} | {' ; '.join(e['informations_secondaires'])} | {e['risque_decrochage']} | "
                 f"{', '.join(e['faits'])} | {e['duree_cible_s']} s | {e['transition_sortie'] or '—'} |")
    L += ["", "**Fil de tension** : question ouverte en SEQ-01 (pour quoi ?), résolue en SEQ-03 et SEQ-04 ; question ouverte en SEQ-06 "
          "(téléphone ou banque ?), reprise en SEQ-09 (sénateurs, 2020) ; question finale en SEQ-10 (à quelles conditions, au profit de qui ?).", ""]
    (OUT / "structure.md").write_text("\n".join(L), encoding="utf-8")
    # QC
    blk = [c for c in checks if c["resultat"] == "BLOQUANT"]
    (OUT / "qc_consolidation.json").write_text(json.dumps({"bloquants": len(blk), "valide": False, "controles": checks},
                                                           ensure_ascii=False, indent=1), encoding="utf-8")
    L = ["# Contrôle de cohérence — consolidation v2.2", "",
         f"**{len(checks) - len(blk)} contrôles ok ou alertes · {len(blk)} bloquant(s).** Ces contrôles sont techniques et documentaires : "
         "ils ne valent **pas** validation éditoriale.", "", "| Catégorie | Contrôle | Résultat | Détail |", "|---|---|---|---|"]
    L += [f"| {c['categorie']} | {c['controle']} | {c['resultat']} | {c['detail']} |" for c in checks]
    (OUT / "qc_consolidation.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    for c in blk:
        print("BLOQUANT", c["controle"], "—", c["detail"])
    print(f"consolidation : {len(checks)} contrôles, {len(blk)} bloquant(s) · {words} mots · {total} s → {OUT}")
    return 1 if blk else 0


if __name__ == "__main__":
    sys.exit(main())
