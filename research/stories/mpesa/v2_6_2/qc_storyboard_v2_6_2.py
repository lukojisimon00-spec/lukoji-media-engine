"""QC du storyboard v2.6.2 (moteur v10) et plans de production (pilote M-Pesa) — lecture seule, aucun changement de statut.

Niveaux : BLOQUANT · RISQUE MAJEUR · ALERTE · RECOMMANDATION · CONFORME. Pas de score global : remplir les champs ne
vaut pas qualité. N'appelle PAS `story qc` (qui ferait passer le projet en storyboard_review).

Produit dans docs/stories/STO-20261127-001/v2_6_2/ : qc_storyboard.md/.json, storyboard_production.md, plan_sourcing.md,
archives_a_rechercher.md, illustrations_a_produire.md, plan_motion_design.md, plan_sound_design.md, scenes_a_risque.md.

Usage : python3 research/stories/mpesa/v2_6_2/qc_storyboard_v2_6_2.py   (code retour 1 si un BLOQUANT)
"""
from __future__ import annotations

import collections
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))
from lukoji_engine.story import storyboard as sbe  # noqa: E402
from lukoji_engine.story.text import speech_seconds  # noqa: E402

SID = "STO-20261127-001"
OUT = ROOT / f"docs/stories/{SID}/v2_6_2"
MOTION = {"graphique", "infographie", "typographie_animee", "carte", "animation", "comparaison", "zoom_detail"}
EXCLUDED = {"F38", "F39", "F47", "F48", "F51", "F53", "F54", "F56", "F57", "F64", "F65", "F66", "F67", "F11", "F13", "F70", "F71"}


def main() -> int:
    sb = json.loads((HERE / "storyboard_v2_6_2.json").read_text(encoding="utf-8"))
    script = json.loads((ROOT / "research/stories/mpesa/v2_2/script_v2_2.json").read_text(encoding="utf-8"))
    struct = json.loads((ROOT / "research/stories/mpesa/v2_2/structure_v2_2.json").read_text(encoding="utf-8"))
    res = {r["id"]: r for r in json.loads((HERE / "ressources_visuelles_v2_6_2.json").read_text(encoding="utf-8"))["ressources"]}
    c = sqlite3.connect(ROOT / "var/lukoji.sqlite3")
    pid, status = c.execute("SELECT id, status FROM story_projects WHERE sid = ?", (SID,)).fetchone()
    research = json.loads(c.execute("SELECT content_json FROM story_artifacts WHERE project_id = ? AND kind = 'research' "
                                    "ORDER BY version DESC LIMIT 1", (pid,)).fetchone()[0])
    cur_sb = c.execute("SELECT version, content_json, based_on_json FROM story_artifacts WHERE project_id = ? AND kind = 'storyboard' "
                       "ORDER BY version DESC LIMIT 1", (pid,)).fetchone()
    facts = {f["ref"] for f in research["faits"]}
    scenes = sb["scenes"]
    seqs = {s["id"]: s for s in script["sequences"]}
    out = []

    def add(level, cat, ctrl, detail="", scene=""):
        out.append({"niveau": level, "categorie": cat, "controle": ctrl, "detail": detail, "scene": scene})

    # --- Sources de vérité
    v = subprocess.run([sys.executable, str(ROOT / "research/stories/mpesa/v2_2/verrou_validation.py"), "verifier"],
                       capture_output=True, text=True)
    add("CONFORME" if v.returncode == 0 and "AUTORISÉE" in v.stdout else "BLOQUANT", "verrou",
        "versions validées intactes et reconstruction autorisée", v.stdout.strip().splitlines()[-1])
    based = json.loads(cur_sb[2])
    add("CONFORME" if based == {"script": 21, "visual": 5} else "BLOQUANT", "verrou",
        "storyboard du moteur construit sur le script v21 (et la direction v5)", f"storyboard v{cur_sb[0]} basé sur {based}")
    add("CONFORME" if json.loads(cur_sb[1]) == sb else "BLOQUANT", "verrou", "fichier storyboard_v2_6_2.json = version du moteur (v10)", f"v{cur_sb[0]}")
    add("CONFORME" if status == "storyboard_draft" else "BLOQUANT", "statut", "projet en storyboard_draft", status)
    # --- Couverture et structure
    r = sbe.evaluate(sb, script)
    blk = [p for p in r["problemes"] if p["severite"] == "bloquant"]
    add("CONFORME" if not blk else "BLOQUANT", "couverture", "voix off reconstituée mot pour mot, champs requis (contrôle du moteur)",
        "; ".join(p["message"] for p in blk))
    present = {s["sequence"] for s in scenes}
    add("CONFORME" if present == set(seqs) and len(seqs) == 10 else "BLOQUANT", "structure", "les dix séquences du script validé sont couvertes", ", ".join(sorted(present)))
    st_seq = {e["sequence"] for e in struct["etapes"]}
    add("CONFORME" if st_seq == present else "BLOQUANT", "structure", "correspondance avec les étapes de la structure v6", "")
    for s in scenes:
        if not s.get("intention", "").strip():
            add("BLOQUANT", "fonction", "scène sans fonction narrative", "", s["id"])
        bad = [f for f in s["source_factuelle"] if f not in seqs[s["sequence"]]["faits"] or f in EXCLUDED or f not in facts]
        if bad:
            add("BLOQUANT", "sources", "fait affiché hors des faits de la séquence, exclu ou inconnu", ", ".join(bad), s["id"])
    add("CONFORME", "sources", "faits affichés ⊂ faits de la séquence validée, aucun fait exclu", "") if not any(o["categorie"] == "sources" for o in out) else None
    # --- Durées
    total = round(sum(sbe.scene_duration(s) for s in scenes) + 0.6 * 9, 1)
    vo_total = round(sum(speech_seconds(s["voix_off"]) for s in script["sequences"]) + 0.6 * 9, 1)
    add("CONFORME" if 360 <= total <= 480 else "BLOQUANT", "duree", "durée du storyboard dans la cible 6–8 min",
        f"{total} s ≈ {total / 60:.1f} min (voix off seule : {vo_total} s ; +{round(total - vo_total, 1)} s de silences et de tenues)")
    for s in scenes:
        d = sbe.scene_duration(s)
        if d < 2.0 or d > 14.0:
            add("ALERTE", "duree", "durée de scène hors 2–14 s", f"{d} s", s["id"])
        if s["mouvement_camera"] == "fixe" and s["mouvement_graphique"] in ("aucun", "") and d > 9 and s["type_visuel"] in ("photo_lieu", "plan_ambiance", "archive_photo", "document"):
            add("ALERTE", "statisme", "plan fixe sans mouvement graphique de plus de 9 s", f"{d} s", s["id"])
    # --- Transitions
    for a, b in zip(scenes, scenes[1:]):
        if "fil" in a["transition"] and "fil" not in b["transition_entree"]:
            add("ALERTE", "transitions", "raccord par le fil sans entrée correspondante", f"{a['id']} → {b['id']}", b["id"])
    add("CONFORME", "transitions", "chaque scène a une transition d'entrée et de sortie",
        "") if all(s["transition"] and s["transition_entree"] for s in scenes) else add("BLOQUANT", "transitions", "transition manquante")
    # --- Diversité, répétition, motion
    types = collections.Counter(s["type_visuel"] for s in scenes)
    motion = sum(n for t, n in types.items() if t in MOTION)
    share = motion / len(scenes)
    add("CONFORME" if share <= 0.6 else "RISQUE MAJEUR", "diversite", "part du motion design ≤ 60 %", f"{motion}/{len(scenes)} ({share:.0%}) · types : {dict(types)}")
    run = mx = 0
    prev = None
    worst = ""
    for s in scenes:
        fam = "motion" if s["type_visuel"] in MOTION else "réel"
        run = run + 1 if fam == prev else 1
        prev = fam
        if run > mx:
            mx, worst = run, s["id"]
    add("ALERTE" if mx > 4 else "CONFORME", "diversite", "pas plus de 4 plans de motion design consécutifs", f"suite maximale : {mx} (jusqu'à {worst})")
    uses = collections.Counter(r_ for s in scenes for r_ in s["ressources"] if r_ not in ("R20", "R21", "R22"))
    for r_, n in uses.items():
        if n >= 3:
            add("ALERTE", "repetition", "même ressource utilisée 3 fois ou plus", f"{r_} ({res[r_]['description'][:60]}) : {n} scènes")
    for s in scenes:
        if s["type_visuel"] in ("animation", "infographie", "carte") and not s.get("motion_design"):
            add("RECOMMANDATION", "motion", "fiche de motion design à détailler", s["type_visuel"], s["id"])
    # --- Faisabilité, droits, sourcing
    for s in scenes:
        for r_ in s["ressources"]:
            st = res[r_]["statut"]
            if st == "non_obtenue":
                lvl = "ALERTE" if s.get("plan_remplacement", "—") != "—" or s["type_visuel"] == "typographie_animee" else "BLOQUANT"
                add(lvl, "sourcing", "ressource non obtenue (substitut prévu)" if lvl == "ALERTE" else "ressource non obtenue sans substitut", r_, s["id"])
            elif st == "metadonnees_verifiees":
                add("RISQUE MAJEUR", "sourcing", "photo dont le contenu n'a pas été inspecté", f"{r_} : {res[r_].get('inspection', '')}", s["id"])
            elif st == "a_capturer":
                add("ALERTE", "droits", "document à capturer ; droits de citation à confirmer", r_, s["id"])
    if any("R28" in s["ressources"] for s in scenes):
        add("RISQUE MAJEUR", "droits", "article de Science (AAAS) : reproduction d'une page à confirmer", "remplacement prévu : page MIT News ou typographie")
    if any("R14" in s["ressources"] for s in scenes):
        add("ALERTE", "sourcing", "page OpenEdition protégée contre les robots : capture manuelle par l'éditeur", "")
    if any("R31" in s["ressources"] for s in scenes):
        add("ALERTE", "sourcing", "URL exacte du communiqué Safaricom non relevée", "R31")
    gen = [s["id"] for s in scenes if s["authenticite"] == "image_generee"]
    add("CONFORME", "images_generees", "aucune image générée par IA", "") if not gen else add("ALERTE", "images_generees", "images générées", ", ".join(gen))
    rec = [s for s in scenes if s["authenticite"] == "reconstitution"]
    add("CONFORME" if all(s.get("mention_ecran") for s in rec) else "BLOQUANT", "reconstitution", "reconstitutions mentionnées à l'écran", ", ".join(s["id"] for s in rec))
    if rec:
        add("ALERTE", "reconstitution", "inserts à tourner (table, mains, téléphone) ; illustration prévue en remplacement", ", ".join(s["id"] for s in rec))
    sym = [s for s in scenes if s["authenticite"] in ("symbolique", "illustration")]
    add("CONFORME" if all(s.get("mention_ecran") for s in sym) else "BLOQUANT", "authenticite", "images d'illustration et illustrations mentionnées", "")
    hard = [s["id"] for s in scenes if s["difficulte"] == "élevée"]
    add("CONFORME" if not hard else "ALERTE", "complexite", "aucune scène de difficulté élevée", ", ".join(hard))
    add("RECOMMANDATION", "audio", "choisir et créditer les sons Freesound et la musique avant montage (aucun son sélectionné)", "")
    add("CONFORME" if all(s["ambiance"] and s["musique"] for s in scenes) else "ALERTE", "audio", "chaque scène a une ambiance et une intention musicale", "")
    add("RECOMMANDATION", "rythme", "SEQ-08 enchaîne graphiques et schémas : prévoir une respiration visuelle si le test d'écoute montre un décrochage", "")

    # --- Contrôles propres à la v10 (corrections ciblées de la v9)
    v9 = json.loads((ROOT / "research/stories/mpesa/v2_6/storyboard_v2_6.json").read_text(encoding="utf-8"))
    add("CONFORME" if cur_sb[0] == 10 else "BLOQUANT", "version", "storyboard courant = v10", f"v{cur_sb[0]}")
    add("CONFORME" if len(scenes) == len(v9["scenes"]) == 50 and [s["id"] for s in scenes] == [s["id"] for s in v9["scenes"]] else "BLOQUANT",
        "fidelite", "mêmes 50 scènes que la v9, sans nouveau découpage", "")
    same_vo = all(a["voix_off"] == b["voix_off"] and a.get("duree_s") == b.get("duree_s") for a, b in zip(v9["scenes"], scenes))
    add("CONFORME" if same_vo else "BLOQUANT", "fidelite", "voix off et durées déclarées identiques à la v9 (silences conservés)", "")
    same_f = all(a["source_factuelle"] == b["source_factuelle"] for a, b in zip(v9["scenes"], scenes))
    add("CONFORME" if same_f else "BLOQUANT", "fidelite", "faits affichés identiques à la v9 (aucun fait ni chiffre nouveau)", "")
    changed = [b["id"] for a, b in zip(v9["scenes"], scenes) if a != b]
    expected = sb.get("derive_de", {}).get("scenes_modifiees", [])
    add("CONFORME" if changed == expected else "BLOQUANT", "fidelite", "seules les scènes décidées sont modifiées", ", ".join(changed))
    dep = [s["id"] for s in scenes if set(s["ressources"]) & {"R02", "R03"}]
    add("CONFORME" if not dep else "BLOQUANT", "decisions", "aucune dépendance à R02 ou R03", ", ".join(dep))
    add("CONFORME" if res["R02"]["statut"] != "contenu_inspecte" and res["R03"]["statut"] != "contenu_inspecte" else "BLOQUANT",
        "decisions", "R02 et R03 toujours déclarées non inspectées", "")
    s01 = next(s for s in scenes if s["id"] == "SC-01")
    add("CONFORME" if "R01" not in s01["ressources"] and s01["authenticite"] == "illustration" and s01.get("mention_ecran") else "BLOQUANT",
        "decisions", "SC-01 : R01 remplacée par carte + autocar dessiné, mentionné ILLUSTRATION", ", ".join(s01["ressources"]))
    s34 = next(s for s in scenes if s["id"] == "SC-34")
    add("CONFORME" if "R28" not in s34["ressources"] and s34["type_visuel"] == "typographie_animee" else "BLOQUANT",
        "decisions", "SC-34 : référence typographique originale, aucune page de Science", ", ".join(s34["ressources"]))
    add("CONFORME" if not any("R28" in s["ressources"] or "R01" in s["ressources"] for s in scenes) else "BLOQUANT",
        "decisions", "R01 et R28 absentes de toutes les scènes", "")
    counts = collections.Counter(o["niveau"] for o in out)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "qc_storyboard.json").write_text(json.dumps({"niveaux": counts, "valide": False, "controles": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    order = ["BLOQUANT", "RISQUE MAJEUR", "ALERTE", "RECOMMANDATION", "CONFORME"]
    L = ["# QC du storyboard v2.6.2 (moteur v10)", "", " · ".join(f"**{k}** : {counts.get(k, 0)}" for k in order), "",
         "> Pas de score : un storyboard complet n'est pas forcément réalisable. Ce contrôle ne vaut pas validation.", ""]
    for lvl in order:
        rows = [o for o in out if o["niveau"] == lvl]
        if rows:
            L += [f"## {lvl}", "", "| Catégorie | Contrôle | Scène | Détail |", "|---|---|---|---|"]
            L += [f"| {o['categorie']} | {o['controle']} | {o['scene'] or '—'} | {o['detail']} |" for o in rows]
            L.append("")
    (OUT / "qc_storyboard.md").write_text("\n".join(L), encoding="utf-8")
    write_plans(sb, res, script)
    by = collections.defaultdict(list)
    for o in out:
        if o["scene"] and o["niveau"] in ("BLOQUANT", "RISQUE MAJEUR", "ALERTE"):
            by[o["scene"]].append(f"{o['niveau']} — {o['controle']} ({o['detail']})")
    R = ["# Scènes à risque — v2.6", "", "Scènes ayant au moins un BLOQUANT, un RISQUE MAJEUR ou une ALERTE, avec le plan de remplacement prévu.", "",
         "| Scène | Séq. | Risques | Remplacement |", "|---|---|---|---|"]
    sc_by = {s["id"]: s for s in sb["scenes"]}
    for sid in sorted(by, key=lambda x: int(x[3:])):
        R.append(f"| {sid} | {sc_by[sid]['sequence']} | {'<br>'.join(by[sid])} | {sc_by[sid]['plan_remplacement']} |")
    R += ["", "Risques transverses : droits de reproduction des documents (citations courtes à confirmer), article de Science (AAAS), "
          "sons et musique non sélectionnés, inserts de reconstitution à tourner."]
    (OUT / "scenes_a_risque.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    print(" · ".join(f"{k} {counts.get(k, 0)}" for k in order), f"· durée {total} s")
    return 1 if counts.get("BLOQUANT") else 0


def write_plans(sb, res, script):
    scenes = sb["scenes"]
    t = 0.0
    prod = ["# Storyboard v2.6.2 — fiche de réalisation", "",
            "Construit à partir du script v21 et de la structure v6 **verrouillés**. Statut : `storyboard_draft` (non validé).", ""]
    seq = None
    for s in scenes:
        if s["sequence"] != seq:
            seq = s["sequence"]
            sq = next(x for x in script["sequences"] if x["id"] == seq)
            prod += [f"## {seq} — {sq['titre']}", "", f"*Musique : {s['musique']}*", ""]
        d = sbe.scene_duration(s)
        md = s.get("motion_design")
        prod += [f"### {s['id']} · {t:.1f}–{t + d:.1f} s ({d} s) · {s['type_visuel']} · {s['statut_image']}" + (f" · mention « {s['mention_ecran']} »" if s.get("mention_ecran") else ""), "",
                 f"- **Narration** : {s['voix_off'] or '— (sans voix off)'}",
                 f"- **Objectif / rythme** : {s['intention']} · {s['rythme']}",
                 f"- **Visuel** : {s['description']}",
                 f"- **Composition / cadrage** : {s['composition']} · {s['cadrage']}",
                 f"- **Mouvement** : caméra {s['mouvement_camera']} · graphique : {s['mouvement_graphique']}",
                 f"- **Texte à l'écran** : {' / '.join(s['texte_ecran']) or '—'}",
                 f"- **Source visuelle** : {', '.join(s['ressources']) or '—'} ({', '.join(s['statut_ressource']) or '—'})",
                 f"- **Source factuelle** : {', '.join(s['source_factuelle']) or '—'}",
                 f"- **Remplacement** : {s['plan_remplacement']}",
                 f"- **Transitions** : entrée {s['transition_entree']} · sortie {s['transition']}",
                 f"- **Son** : {s['ambiance']}" + (f" · effets : {', '.join(s['effets_sonores'])}" if s["effets_sonores"] else ""),
                 f"- **Difficulté / méthode** : {s['difficulte']} · {s['methode_production']}",
                 f"- **Montage** : {s['instructions_montage']}",
                 f"- **Risques** : {s['risques_representation']}"]
        if md:
            prod.append(f"- **Motion design** : comprendre : {md['comprendre']} · éléments : {md['elements']} · mouvement : {md['mouvement']} · "
                        f"durée : {md['duree']} · entrée : {md['entree']} · sortie : {md['sortie']} · style : {md['style']} · "
                        f"contraintes : {md['contraintes'] or '—'} · assets : {md['assets']}")
        prod.append("")
        t += d
        nxt = scenes[scenes.index(s) + 1] if scenes.index(s) + 1 < len(scenes) else None
        if nxt and nxt["sequence"] != s["sequence"]:
            t += 0.6
    (OUT / "storyboard_production.md").write_text("\n".join(prod), encoding="utf-8")

    used = collections.defaultdict(list)
    for s in scenes:
        for r_ in s["ressources"]:
            used[r_].append(s["id"])
    L = ["# Plan de sourcing visuel — v2.6", "", "| ID | Statut | Inspection | Description | Auteur | Date | Licence / conditions | URL | Scènes |", "|---|---|---|---|---|---|---|---|---|"]
    for rid in sorted(used, key=lambda x: int(x[1:])):
        r = res[rid]
        L.append(f"| {rid} | **{r['statut']}** | {r.get('inspection', '—')} | {r['description']} | {r.get('auteur', '—')} | {r.get('date', '—')} | "
                 f"{r.get('licence', '—')} | {r.get('url_directe') or r.get('page', '—')} | {', '.join(used[rid])} |")
    L += ["", "Rappels : une date de prise de vue n'est pas une date de publication ; les licences CC BY / CC BY-SA imposent le crédit "
          "(et le partage à l'identique pour CC BY-SA en cas de modification) ; aucune image n'est déclarée vérifiée sans inspection."]
    (OUT / "plan_sourcing.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    A = ["# Archives et documents à rechercher ou capturer", "", "## À capturer (pages lues, captures non réalisées)", ""]
    A += [f"- **{rid}** — {res[rid]['description']} — {res[rid].get('url_directe', '—')} — scènes {', '.join(used[rid])}" for rid in sorted(used, key=lambda x: int(x[1:])) if res[rid]["statut"] == "a_capturer"]
    A += ["", "## Photos à inspecter avant montage (métadonnées seulement)", ""]
    A += [f"- **{rid}** — {res[rid]['description']} — scènes {', '.join(used[rid])}" for rid in sorted(used, key=lambda x: int(x[1:])) if res[rid]["statut"] == "metadonnees_verifiees"]
    A += ["", "## Non obtenues (substituts prévus dans le storyboard)", ""]
    A += [f"- **{r['id']}** — {r['description']} — {r.get('limites', '')}" for r in res.values() if r["statut"] == "non_obtenue"]
    A += ["", "## Pistes utiles, non indispensables", "",
          "- Photo d'autocar ou de matatu interurbain au Kenya datée d'avant 2007 (remplacerait l'image d'illustration de 2025 en SEQ-01).",
          "- Plan tourné par LUKOJI à Kinshasa (SEQ-10), à la place de la photo de 2013.",
          "- Photo libre et datée du siège de la Banque centrale en meilleure définition que R07."]
    (OUT / "archives_a_rechercher.md").write_text("\n".join(A) + "\n", encoding="utf-8")

    I = ["# Illustrations, reconstitutions et images générées", "", "**Images générées par IA : aucune.** Aucune scène n'en a besoin ; aucune ne représente une personne, un document, une interface ou un logo.", "",
         "## Illustrations au trait (création LUKOJI)", ""]
    I += [f"- **{s['id']}** ({s['sequence']}) — {s['description']}" for s in scenes if s["authenticite"] == "illustration"]
    I += ["", "## Reconstitutions (inserts à tourner, mention à l'écran)", ""]
    I += [f"- **{s['id']}** ({s['sequence']}) — {s['description']} Remplacement : {s['plan_remplacement']}" for s in scenes if s["authenticite"] == "reconstitution"]
    I += ["", "## Gabarits graphiques (création LUKOJI)", "", "- Carte maîtresse du Kenya (4 états) et carte de l'Afrique (Natural Earth).",
          "- Gabarit chiffres (barre, grille 10×10, jauge), frise, écran partagé « TÉLÉPHONE ? / BANQUE ? », citations en IBM Plex Mono."]
    (OUT / "illustrations_a_produire.md").write_text("\n".join(I) + "\n", encoding="utf-8")

    Mo = ["# Plan de motion design — v2.6", "", "| Scène | Séq. | Type | Ce que le spectateur comprend | Éléments | Mouvement | Durée | Entrée → sortie | Style | Contraintes | Assets |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in scenes:
        md = s.get("motion_design")
        if md:
            Mo.append(f"| {s['id']} | {s['sequence']} | {s['type_visuel']} | {md['comprendre']} | {md['elements']} | {md['mouvement']} | {md['duree']} | "
                      f"{md['entree']} → {md['sortie']} | {md['style']} | {md['contraintes'] or '—'} | {md['assets']} |")
    other = [s for s in scenes if s["type_visuel"] in MOTION and not s.get("motion_design")]
    Mo += ["", "## Autres plans graphiques (mouvement simple)", ""] + [f"- **{s['id']}** — {s['type_visuel']} — {s['mouvement_graphique']}" for s in other]
    Mo += ["", "Règles : pas de 3D, pas de zoom décoratif, pas de morphing d'icônes ; le fil orange n'apparaît que trois fois (SC des SEQ-04, SEQ-05, SEQ-10)."]
    (OUT / "plan_motion_design.md").write_text("\n".join(Mo) + "\n", encoding="utf-8")

    So = ["# Plan de sound design — v2.6", "", "| Séquence | Musique | Ambiances | Effets | Silences et transitions |", "|---|---|---|---|---|"]
    for sq in script["sequences"]:
        ss = [s for s in scenes if s["sequence"] == sq["id"]]
        amb = "; ".join(dict.fromkeys(s["ambiance"] for s in ss))
        fx = "; ".join(dict.fromkeys(e for s in ss for e in s["effets_sonores"])) or "—"
        sil = "; ".join(f"{s['id']} : {s['instructions_montage']}" for s in ss if "silence" in s["instructions_montage"].lower() or "silence" in s["ambiance"].lower()) or "—"
        So.append(f"| {sq['id']} | {ss[0]['musique']} | {amb} | {fx} | {sil} |")
    So += ["", "Règles : la voix reste devant ; bip de SMS trois fois seulement ; aucune ambiance qui prétendrait être un enregistrement historique ; "
           "sons Freesound (CC0 ou CC BY, à créditer) et musique libre ou originale, à sélectionner."]
    (OUT / "plan_sound_design.md").write_text("\n".join(So) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
