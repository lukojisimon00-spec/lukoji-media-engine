"""Storyboard v2.6.2 (moteur v10) : corrections ciblées du storyboard v9, décidées par l'éditeur en phase 2.6.2.

Part du storyboard v9 (research/stories/mpesa/v2_6/storyboard_v2_6.json, identique à la version du moteur), vérifie le
verrou (script v21, structure v6) et ne modifie QUE les scènes concernées. La voix off, les faits, les durées et les
transitions des autres scènes sont repris à l'identique.

Décisions appliquées :
1. SC-01 : R01 remplacée par la carte du Kenya et un autocar dessiné au trait (illustration).
2. SC-34 : page de Science remplacée par une référence typographique originale ; les résultats restent montrés par les
   visualisations originales (SC-35, SC-36).
3. R02 et R03 abandonnées (non inspectées) : SC-17 → R04 recadrée ; SC-20 → kiosque dessiné ; SC-39 → jauge graphique ;
   SC-47 → rappel de plans du film (insert téléphone, SMS dessiné, boutique R04).
Mises en cohérence nécessaires : SC-05 (la carte n'apparaît plus pour la première fois) ; SC-45 (capture OpenEdition
rendue facultative : référence typographique, risque de capture manuelle supprimé).

Usage : python3 research/stories/mpesa/v2_6_2/build_storyboard_v2_6_2.py
"""
from __future__ import annotations

import copy
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "research/stories/mpesa/v2_6"))
from build_storyboard_v2_6 import load_locked  # noqa: E402  (contrôle d'empreinte du script et de la structure)

V9_FILE = ROOT / "research/stories/mpesa/v2_6/storyboard_v2_6.json"
RES = {r["id"]: r for r in json.loads((HERE / "ressources_visuelles_v2_6_2.json").read_text(encoding="utf-8"))["ressources"]}

PATCH = {
 "SC-01": dict(
    type_visuel="illustration", authenticite="illustration", statut_image="illustration (carte + dessin au trait LUKOJI, non générée)",
    mention_ecran="ILLUSTRATION",
    intention="Établir le contexte géographique et la longueur du trajet, par une image clairement illustrative.",
    description="Carte du Kenya (aplats #555555 sur noir, frontières Natural Earth). Un tracé orange schématique part de Nairobi vers une région rurale non nommée ; un autocar dessiné au trait (silhouette blanc cassé, sans logo, sans inscription, aucune personne visible) avance lentement le long du tracé.",
    sujet="carte du Kenya, autocar dessiné", composition="carte légèrement décentrée à droite ; tracé en diagonale ; autocar petit dans le cadre",
    cadrage="plan large", mouvement_camera="fixe", mouvement_graphique="l'autocar avance le long du tracé pendant toute la phrase (mouvement unique, lent)",
    animation=["déplacement linéaire de l'autocar (6 s) — la distance et la durée du trajet"],
    motion_design=dict(comprendre="envoyer de l'argent supposait un long trajet par la route", elements="carte du Kenya, tracé orange, autocar au trait",
                       mouvement="déplacement linéaire, sans rebond", duree="6 s", entree="ouverture au noir", sortie="l'autocar sort du cadre",
                       style="trait blanc cassé, tracé orange (pas encore le « fil de l'argent »)", contraintes="aucune ville de destination nommée, aucun compteur de jours",
                       assets="Natural Earth (R20), dessin vectoriel Inkscape (R22)"),
    texte_ecran=["KENYA", "SOURCE DU RÉCIT : VODAFONE (2017)"], ressources=["R20", "R22"],
    plan_remplacement="Carte seule avec le tracé (sans autocar).", ambiance="vent et route lointaine, très bas (Freesound, CC0)",
    instructions_montage="Carte maîtresse, état 0/4 (ouverture). Le tracé n'est pas le fil de l'argent : pas de raccord avec SC-14.",
    methode_production="Inkscape (dessin) + DaVinci Resolve/Fusion ou Blender (animation 2D), outils gratuits",
    difficulte="moyenne",
    risques_representation="Illustration : mention à l'écran ; aucune personne, aucune marque ; ne suggère aucune date précise."),
 "SC-05": dict(
    description="Retour de la carte du Kenya (aplats #555555 sur noir), sans tracé ; Nairobi seule nommée ; carton « 2006 » en haut à droite.",
    instructions_montage="Carte maîtresse, état 1/4 (déjà vue en ouverture, SC-01)."),
 "SC-17": dict(
    ressources=["R04"], description="Kiosque M-Pesa au Kenya (R04) en plan serré sur le lettrage peint « M-PESA » du mur vert ; la boutique entière n'est montrée qu'en SC-21.",
    sujet="lettrage peint « M-PESA »", composition="lettrage vertical au centre, mur vert plein cadre", cadrage="plan serré",
    texte_ecran=["KENYA · DATE INCONNUE · PHOTO : REALT0N12 · CC BY-SA 3.0"], statut_image="authentique (photo réelle, date inconnue)",
    plan_remplacement="Typographie « LA RÉPONSE : DES COMMERÇANTS » sur noir.",
    instructions_montage="Recadrage serré (le logo Safaricom hors cadre) ; image recadrée = adaptation sous CC BY-SA 3.0.",
    risques_representation="Date inconnue : le dire ; ne jamais afficher la date des métadonnées."),
 "SC-20": dict(
    type_visuel="illustration", authenticite="illustration", statut_image="illustration (dessin au trait LUKOJI, non générée)", mention_ecran="ILLUSTRATION",
    ressources=["R22"], description="Le fil orange venu de la carte SIM (SC-19) aboutit à un petit kiosque dessiné au trait, sans enseigne ni marque ; une main dessinée reçoit des billets.",
    sujet="kiosque dessiné, retrait", composition="kiosque au tiers droit, fil entrant par la gauche", cadrage="plan moyen",
    mouvement_graphique="le fil se termine sur le comptoir dessiné", animation=["fin du tracé du fil (2 s) — l'argent est retiré plus loin"],
    texte_ecran=[], plan_remplacement="Carton typographique « RETRAIT CHEZ UN COMMERÇANT ».", ambiance="motif rythmé léger",
    instructions_montage="Même style graphique que SC-19 (continuité de l'explication).", methode_production="Inkscape + animation 2D (outils gratuits)",
    difficulte="moyenne", risques_representation="Illustration mentionnée ; aucune marque."),
 "SC-34": dict(
    type_visuel="typographie_animee", authenticite="graphique_explicatif", statut_image="typographie éditoriale (création LUKOJI)",
    ressources=["R21"], description="Carte de référence typographique originale, sur noir : « The long-run poverty and gender impacts of mobile money » · Tavneet Suri & William Jack · Science · 2016. La carte se réduit ensuite en haut d'écran et reste visible pendant les visualisations originales des résultats (SC-35, SC-36).",
    sujet="référence de l'étude", composition="titre en IBM Plex Mono au centre, auteurs et revue dessous", cadrage="plein cadre",
    mouvement_camera="fixe", mouvement_graphique="apparition ligne à ligne, puis réduction en bandeau",
    animation=["apparition puis réduction en bandeau (4 s) — la référence exacte de l'étude"],
    texte_ecran=["« THE LONG-RUN POVERTY AND GENDER IMPACTS OF MOBILE MONEY »", "TAVNEET SURI & WILLIAM JACK · SCIENCE · 2016"],
    plan_remplacement="Référence seule sur noir, sans bandeau.", instructions_montage="Aucune page, figure ou illustration de l'article.",
    methode_production="typographie animée (gabarit LUKOJI)", difficulte="faible",
    risques_representation="Aucun élément protégé de l'article n'est reproduit."),
 "SC-39": dict(
    type_visuel="graphique", authenticite="graphique_explicatif", statut_image="graphique éditorial (création LUKOJI)",
    ressources=["R21"], description="Sur noir, une jauge horizontale se remplit jusqu'à 7 % ; légende « CERTAINS TRANSFERTS ».",
    sujet="coût des transferts", composition="jauge au centre, valeur en Archivo Black jaune", cadrage="plein cadre",
    mouvement_camera="fixe", mouvement_graphique="remplissage de la jauge (1 s)", animation=["remplissage (1 s) — le coût peut atteindre 7 % du montant"],
    texte_ecran=["JUSQU'À 7 % DU MONTANT · CERTAINS TRANSFERTS", "SOURCE : AGENCE ECOFIN (2025)"],
    plan_remplacement="Chiffre seul en typographie.", instructions_montage="« Certains transferts » toujours visible.",
    methode_production="gabarit chiffres LUKOJI", difficulte="faible", risques_representation="Ne pas généraliser le chiffre à tous les transferts."),
 "SC-45": dict(
    type_visuel="typographie_animee", authenticite="graphique_explicatif", statut_image="typographie éditoriale (création LUKOJI)",
    ressources=["R21"], description="Carte de référence sur noir : « Présentation de thèse · Revue de la régulation (OpenEdition) » ; la phrase source suit en SC-46.",
    sujet="référence de la thèse", composition="référence centrée", cadrage="plein cadre", mouvement_camera="fixe",
    mouvement_graphique="apparition ligne à ligne", texte_ecran=["PRÉSENTATION DE THÈSE · REVUE DE LA RÉGULATION (OPENEDITION)"],
    plan_remplacement="Capture manuelle de la page par l'éditeur (facultative, R14).", instructions_montage="—",
    methode_production="typographie animée (gabarit LUKOJI)", difficulte="faible",
    risques_representation="Auteur non nommé (non relevé) ; la référence ne l'invente pas."),
 "SC-47": dict(
    type_visuel="reconstitution", authenticite="reconstitution", statut_image="montage-rappel : insert de reconstitution, illustration, photo réelle",
    mention_ecran="RECONSTITUTION (téléphone) · ILLUSTRATION (SMS) · PHOTO : KENYA, DATE INCONNUE (boutique)",
    ressources=["R22", "R04"], description="Rappel de trois plans du film, en coupes sèches calées sur la voix : l'insert du téléphone (SC-03), la bulle de SMS dessinée (SC-19), la boutique peinte (R04, cadre de SC-21). Chaque plan garde sa propre mention.",
    sujet="rappel", composition="trois plans fixes déjà vus", cadrage="plans de rappel", mouvement_camera="fixe", mouvement_graphique="aucun",
    animation=[], texte_ecran=["RECONSTITUTION", "ILLUSTRATION", "KENYA · DATE INCONNUE · PHOTO : REALT0N12 · CC BY-SA 3.0"],
    plan_remplacement="Les trois mots « TÉLÉPHONE · SMS · BOUTIQUES » en typographie.",
    instructions_montage="Coupes calées sur « téléphone », « SMS », « boutiques » ; mention propre à chaque plan.",
    methode_production="réutilisation des plans SC-03, SC-19, SC-21", difficulte="faible",
    risques_representation="Ne pas présenter l'insert ni le dessin comme des archives."),
}


def build() -> dict:
    load_locked()  # arrête tout si le script ou la structure ne correspondent pas au verrou
    v9 = json.loads(V9_FILE.read_text(encoding="utf-8"))
    c = sqlite3.connect(ROOT / "var/lukoji.sqlite3")
    pid = c.execute("SELECT id FROM story_projects WHERE sid = 'STO-20261127-001'").fetchone()[0]
    db9 = json.loads(c.execute("SELECT content_json FROM story_artifacts WHERE project_id = ? AND kind = 'storyboard' AND version = 9",
                               (pid,)).fetchone()[0])
    if db9 != v9:
        raise SystemExit("ARRÊT : le fichier du storyboard v9 ne correspond pas à la v9 du moteur")
    doc = copy.deepcopy(v9)
    for sc in doc["scenes"]:
        p = PATCH.get(sc["id"])
        if not p:
            continue
        sc.update(copy.deepcopy(p))
        if sc["authenticite"] not in ("symbolique", "illustration", "reconstitution"):
            sc.pop("mention_ecran", None)
        if "motion_design" not in p and sc["type_visuel"] not in ("carte", "graphique", "infographie", "typographie_animee", "animation", "illustration"):
            sc["motion_design"] = None
        sc["raison_narrative"] = sc["intention"]
        sc["statut_ressource"] = sorted({RES[r]["statut"] for r in sc["ressources"]})
        sc["sources_visuelles"] = [RES[r].get("page") or RES[r].get("url_directe") or RES[r]["description"] for r in sc["ressources"]]
    doc["version_editoriale"] = "v2.6.2 — corrections ciblées du storyboard v9 (décisions de l'éditeur, phase 2.6.2)"
    doc["base_validee"] = {"script": 21, "structure": 6}
    doc["derive_de"] = {"storyboard": 9, "scenes_modifiees": sorted(PATCH)}
    return doc


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))
    d = build()
    (HERE / "storyboard_v2_6_2.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"storyboard v2.6.2 : {len(d['scenes'])} scènes · modifiées : {', '.join(d['derive_de']['scenes_modifiees'])}")
