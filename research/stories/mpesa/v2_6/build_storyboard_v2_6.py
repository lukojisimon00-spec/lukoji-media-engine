"""Storyboard v2.6 du pilote M-Pesa (« Quand les clients ont changé le produit »), reconstruit à partir des versions
VERROUILLÉES : script v21 (v2.2) et structure v6, contrôlées par empreinte avant toute écriture.

Découpage : chaque scène porte un segment EXACT de la voix off, défini par la fin du segment (sous-chaîne incluse).
Une scène peut porter plusieurs phrases ou une partie de phrase ; une scène sans voix off (respiration) déclare sa durée.
La voix off n'est jamais réécrite : le script reconstitue la séquence mot pour mot (contrôle du moteur).

Usage : python3 research/stories/mpesa/v2_6/build_storyboard_v2_6.py   → storyboard_v2_6.json à côté
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
LOCK = json.loads((ROOT / "docs/stories/STO-20261127-001/VERROU_VALIDATION.json").read_text(encoding="utf-8"))
SCRIPT_FILE = ROOT / "research/stories/mpesa/v2_2/script_v2_2.json"
STRUCT_FILE = ROOT / "research/stories/mpesa/v2_2/structure_v2_2.json"
RES = {r["id"]: r for r in json.loads((HERE / "ressources_visuelles_v2_6.json").read_text(encoding="utf-8"))["ressources"]}


def _sha(o) -> str:
    return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def load_locked() -> tuple[dict, dict]:
    """Charge script et structure, et refuse toute divergence avec les empreintes verrouillées."""
    script = json.loads(SCRIPT_FILE.read_text(encoding="utf-8"))
    struct = json.loads(STRUCT_FILE.read_text(encoding="utf-8"))
    v = {x["etape"]: x for x in LOCK["validations"]}
    if _sha(script) != v["script"]["versions"]["script"]["sha256"]:
        raise SystemExit("ARRÊT : le script ne correspond pas à la version validée (empreinte)")
    if _sha(struct) != v["structure"]["versions"]["structure"]["sha256"]:
        raise SystemExit("ARRÊT : la structure ne correspond pas à la version validée (empreinte)")
    return script, struct


# Préréglages par famille de plan (complétés scène par scène).
P = {
 "photo": dict(type_visuel="photo_lieu", authenticite="authentique", statut_image="authentique (photo réelle, datée)",
               cadrage="plan moyen", mouvement_camera="fixe", mouvement_graphique="aucun", difficulte="faible",
               methode="photo libre Wikimedia Commons, recadrage 16:9, légende lieu / date / auteur / licence"),
 "archive": dict(type_visuel="archive_photo", authenticite="authentique", statut_image="archive (photo datée de mars 2007)",
                 cadrage="plan large", mouvement_camera="panoramique", mouvement_graphique="aucun", difficulte="faible",
                 methode="photo libre Wikimedia Commons datée, légende complète"),
 "doc": dict(type_visuel="document", authenticite="authentique", statut_image="authentique (capture d'un document cité)",
             cadrage="plan serré sur l'extrait", mouvement_camera="fixe", mouvement_graphique="trait orange fixe sous l'extrait",
             difficulte="faible", methode="capture d'écran haute définition de la page, fond #0B0B0B, extrait court, URL et date de consultation à l'écran"),
 "carte": dict(type_visuel="carte", authenticite="graphique_explicatif", statut_image="graphique éditorial (création LUKOJI)",
               cadrage="plan large", mouvement_camera="fixe", difficulte="moyenne",
               methode="After Effects ou équivalent libre (Blender 2D, Natron) ; fond de carte Natural Earth (domaine public), projection simple"),
 "graph": dict(type_visuel="graphique", authenticite="graphique_explicatif", statut_image="graphique éditorial (création LUKOJI)",
               cadrage="plein cadre", mouvement_camera="fixe", difficulte="faible", methode="gabarit unique LUKOJI (Archivo Black / IBM Plex Mono)"),
 "info": dict(type_visuel="infographie", authenticite="graphique_explicatif", statut_image="graphique éditorial (création LUKOJI)",
              cadrage="plein cadre", mouvement_camera="fixe", difficulte="moyenne", methode="motion design 2D, gabarit LUKOJI"),
 "typo": dict(type_visuel="typographie_animee", authenticite="graphique_explicatif", statut_image="typographie éditoriale (création LUKOJI)",
              cadrage="plein cadre", mouvement_camera="fixe", difficulte="faible", methode="typographie animée (Archivo Black, IBM Plex Mono)"),
 "illus": dict(type_visuel="animation", authenticite="illustration", statut_image="illustration (dessin au trait LUKOJI, non générée)",
               mention_ecran="ILLUSTRATION", cadrage="plan large", mouvement_camera="fixe", difficulte="moyenne",
               methode="dessin vectoriel au trait (noir, blanc cassé, orange) animé en 2D"),
 "recon": dict(type_visuel="reconstitution", authenticite="reconstitution", statut_image="reconstitution (insert filmé sur table)",
               mention_ecran="RECONSTITUTION", cadrage="insert très serré", mouvement_camera="insert_detail", difficulte="moyenne",
               methode="tournage LUKOJI sur table (téléphone basique, mains), lumière douce ; aucun visage, aucune marque, texte de SMS générique"),
}

M = {  # intentions musicales par séquence
 "SEQ-01": "aucune musique : ambiance réelle puis silence ; la musique n'entre qu'après le titre",
 "SEQ-02": "nappe grave, sobre, tempo lent (piano préparé ou cordes basses), très en retrait",
 "SEQ-03": "même nappe, une note répétée qui installe l'attente",
 "SEQ-04": "pulsation légère qui démarre avec les fils, coupée net avant la citation",
 "SEQ-05": "motif léger et rythmé (percussions sèches), explicatif",
 "SEQ-06": "tension : basse tenue, dissonance discrète sur la question, résolution partielle sur « feu vert »",
 "SEQ-07": "motif d'ampleur retenu, sans triomphalisme",
 "SEQ-08": "musique très basse ou absente : la voix et les chiffres portent ; silence sur « Pas un décompte »",
 "SEQ-09": "reprise en mineur après une seconde de silence ; montée lente jusqu'aux sénateurs, retombée",
 "SEQ-10": "thème final dépouillé ; la dernière question tombe sur un silence avant le fondu",
}

SPEC = [
 # ---------------------------------------------------------------- SEQ-01
 dict(seq="SEQ-01", fin="voyager pendant des jours.", kind="photo", type_visuel="plan_ambiance", authenticite="symbolique",
      statut_image="authentique (photo réelle de 2025) utilisée comme image d'illustration", mention_ecran="IMAGE D'ILLUSTRATION — NAIROBI, 2025",
      rythme="ouverture, tension douce", intention="Ancrer le récit dans le transport routier kényan, sans prétendre montrer l'époque.",
      description="Matatu violet arrêté dans une avenue de Nairobi (photo réelle, 2025). Recadrage 16:9 sur la bande centrale : le véhicule en entier, l'arrière-plan d'immeubles en haut du cadre.",
      sujet="matatu, avenue de Nairobi", composition="véhicule au tiers inférieur, ligne de toit au centre, ciel coupé",
      texte_ecran=["NAIROBI · PHOTO 2025 · AEIRA-WMF · CC BY 4.0"], res=["R01"], faits=["F61"],
      remplacement="Carte du Kenya au trait, sans photo ; ou photo d'autocar interurbain kényan identifiée plus tard.",
      ambiance="rumeur de circulation (Freesound, CC0)", effets=[], transition_entree="ouverture au noir (0,5 s)", transition="coupe franche",
      montage="Le passager visible à la porte reste petit dans le cadre ; masquer l'enseigne publicitaire « TECNO » par le recadrage.",
      risques="Photo de 2025 : ne prouve pas la pratique ancienne ; mention de date obligatoire ; personne identifiable à la porte (photo de rue, licence libre)."),
 dict(seq="SEQ-01", fin="et attendre.", kind="doc", rythme="preuve discrète",
      intention="Montrer la source réelle de la pratique : l'enquête nationale FinAccess 2006.",
      description="Extrait du tableau 8.5 du rapport FinAccess 2006 : la ligne « Through a bus or matatu company » soulignée en orange, le reste du tableau assombri.",
      sujet="tableau FinAccess 2006", composition="ligne du tableau au centre, titre du rapport en haut à gauche",
      texte_ecran=["FINACCESS 2006 · ENQUÊTE NATIONALE · TABLEAU 8.5"], res=["R26"], faits=["F72", "F73"],
      remplacement="Typographie seule : « ENVOI PAR UNE COMPAGNIE DE BUS OU DE MATATU — FINACCESS 2006 ».",
      ambiance="la rumeur de rue se coupe sur « attendre »", effets=[], transition_entree="coupe franche", transition="coupe sèche au noir",
      montage="Couper l'ambiance exactement sur « attendre » : une demi-seconde de silence.",
      risques="Le tableau porte sur les 12 mois précédant l'enquête de 2006 : ne pas afficher de pourcentage sans sa base."),
 dict(seq="SEQ-01", fin="quelques SMS suffisent.", kind="recon", rythme="rupture, accélération",
      intention="Rupture : des jours de voyage contre quelques SMS.",
      description="Insert très serré : un téléphone à clavier posé sur une table de bois reçoit un SMS ; l'écran affiche un texte générique (« Vous avez reçu… »), sans marque ni numéro réel.",
      sujet="téléphone à clavier, SMS", composition="écran au tiers gauche, profondeur de champ courte", texte_ecran=[], res=["R22"], faits=["F43"],
      remplacement="Illustration au trait : bulle de SMS orange sur fond noir (mention ILLUSTRATION).",
      ambiance="silence de pièce", effets=["vibration du téléphone, bip unique (signature sonore 1/3)"], transition_entree="coupe franche", transition="coupe franche", duree_extra=1.0,
      montage="Le bip tombe sur « SMS ».", risques="Ne reproduire aucune interface réelle de M-Pesa ou de Safaricom."),
 dict(seq="SEQ-01", fin="inventé pour ça.", kind="typo", rythme="révélation du sujet, puis question suspendue",
      intention="Nommer le sujet et laisser la question ouverte.",
      description="Sur noir, « M-PESA » s'écrit en Archivo Black blanc ; la dernière phrase est dite sur le noir ; le titre de travail apparaît ensuite en IBM Plex Mono.",
      sujet="titre", composition="nom centré, titre en bas", texte_ecran=["M-PESA", "QUAND LES CLIENTS ONT CHANGÉ LE PRODUIT"], res=["R21"], faits=[],
      mouvement_graphique="apparition lettre à lettre (12 images), sans rebond",
      animation=dict(comprendre="le nom du service, puis le titre du film", elements="deux lignes de texte", mouvement="apparition sèche, maintien, disparition",
                     duree="4 s + 1 s de noir", entree="sur « s'appelle M-Pesa »", sortie="1 s après « pour ça »", style="éditorial sobre",
                     contraintes="lisible en 9:16 recadré", assets="polices de brand/fonts"),
      ambiance="silence", effets=[], transition_entree="coupe franche", transition="carton « KENYA · 2006 » en coupe franche", duree_extra=1.0,
      montage="Une seconde de noir après « pour ça », avant le carton.", risques=""),
 # ---------------------------------------------------------------- SEQ-02
 dict(seq="SEQ-02", fin="le mesure.", kind="carte", rythme="installation",
      intention="Poser le territoire et annoncer la mesure.", description="Première apparition de la carte du Kenya (aplats #555555 sur noir), Nairobi seule nommée ; carton « 2006 » en haut à droite.",
      sujet="carte du Kenya", composition="pays centré, légèrement à droite pour laisser la place aux chiffres", mouvement_graphique="fondu d'entrée de la carte (8 images)",
      texte_ecran=["KENYA", "NAIROBI", "2006"], res=["R20"], faits=[],
      animation=dict(comprendre="où se passe l'histoire", elements="frontières, Nairobi", mouvement="apparition", duree="6 s", entree="sur « Au milieu des années deux mille »",
                     sortie="coupe vers le graphique", style="aplats, sans relief", contraintes="frontières exactes", assets="Natural Earth 1:10m"),
      ambiance="nappe grave", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Carte maîtresse, état 1/4.", risques=""),
 dict(seq="SEQ-02", fin="comme une banque ou une assurance.", kind="graph", rythme="information clé",
      intention="Donner le chiffre antérieur au lancement, avec son périmètre exact.",
      description="Barre unique, échelle 0-100 % : 26,7 % en jaune. Sous la barre : « ADULTES · SERVICE FINANCIER FORMEL ».",
      sujet="26,7 % en 2006", composition="barre à gauche, valeur en Archivo Black jaune, légende en Plex Mono", mouvement_graphique="la barre monte jusqu'à 26,7 %",
      texte_ecran=["26,7 %", "ADULTES UTILISANT UN SERVICE FINANCIER FORMEL · 2006", "SOURCE : FINACCESS (CBK · KNBS · FSD KENYA), SÉRIE 2019"], res=["R21"], faits=["F74"],
      animation=dict(comprendre="un quart des adultes seulement utilise la finance formelle en 2006", elements="une barre, une valeur, une légende",
                     mouvement="montée linéaire 1 s", duree="8 s", entree="sur « En 2006 »", sortie="figée, puis coupe", style="gabarit chiffres LUKOJI",
                     contraintes="même objet et même échelle qu'en SEQ-08", assets="gabarit graphique unique"),
      ambiance="nappe grave", effets=[], transition_entree="coupe franche", transition="coupe franche",
      montage="Conserver le fichier projet : la même barre reviendra en SEQ-08.", risques="Ne pas écrire « bancarisés » : la définition inclut assurances, coopératives et microfinance."),
 dict(seq="SEQ-02", fin="qui n'ont pas de compte.", kind="typo", rythme="progression",
      intention="Introduire le financeur et son objectif.",
      description="Sur noir, le nom du ministère en IBM Plex Mono, puis son objectif en une ligne : « des services pour les personnes sans compte ».",
      sujet="ministère britannique du Développement international", composition="texte centré, deux lignes", mouvement_graphique="apparition ligne à ligne",
      texte_ecran=["MINISTÈRE BRITANNIQUE DU DÉVELOPPEMENT INTERNATIONAL (DFID)", "OBJECTIF : DES SERVICES POUR LES PERSONNES SANS COMPTE"], res=["R21"], faits=["F41"],
      ambiance="nappe grave", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Pas de drapeau ni de carte de Londres.", risques=""),
 dict(seq="SEQ-02", fin="obtient une subvention.", kind="doc", rythme="preuve",
      intention="Montrer le document qui mentionne la subvention.",
      description="Page Vodafone (2017) : trait orange sous « a grant from the Department for International Development in the UK… to help the unbanked » ; traduction courte en sous-titre.",
      sujet="page Vodafone 2017", composition="paragraphe au centre, page assombrie autour", texte_ecran=["SOURCE : VODAFONE (2017) · RÉCIT DE L'ENTREPRISE"], res=["R12"], faits=["F41"],
      remplacement="Typographie : nom du ministère + phrase source.", ambiance="nappe grave", effets=[], transition_entree="coupe franche", transition="coupe franche",
      montage="Tenir 2 s sur la phrase soulignée.", risques="Source intéressée : la légende le dit."),
 # ---------------------------------------------------------------- SEQ-03
 dict(seq="SEQ-03", fin="l'opérateur Safaricom.", kind="carte", rythme="progression",
      intention="Situer l'opérateur kényan.", description="Retour sur la carte : Nairobi s'éclaire, étiquette « SAFARICOM · OPÉRATEUR KÉNYAN ».",
      sujet="carte, Nairobi", composition="Nairobi au centre-bas", mouvement_graphique="halo bref sur Nairobi", texte_ecran=["SAFARICOM · OPÉRATEUR KÉNYAN"], res=["R20"], faits=["F42"],
      ambiance="nappe", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Carte maîtresse, état 2/4.", risques="Aucun logo de l'opérateur."),
 dict(seq="SEQ-03", fin="deux responsables du projet.", kind="doc", rythme="ralentissement : moment de méthode",
      intention="Dire d'où vient le récit des origines (1/2) : l'article de l'équipe projet.",
      description="Page de titre de l'article de Hughes & Lonie (Innovations, MIT Press, 2007) ; trait orange sous le titre.",
      sujet="article de 2007", composition="page à gauche, place libre à droite pour le document suivant", texte_ecran=["HUGHES & LONIE · INNOVATIONS (MIT PRESS) · 2007 · ÉQUIPE DU PROJET"], res=["R29"], faits=["F76"],
      remplacement="Typographie : référence complète de l'article.", ambiance="nappe", effets=[], transition_entree="coupe franche", transition="glissement latéral (split-screen)",
      montage="Le document suivant entre à droite : les deux sources restent un instant côte à côte.", risques="Source liée à Vodafone : la légende dit « équipe du projet »."),
 dict(seq="SEQ-03", fin="publié par Vodafone en 2017.", kind="doc", rythme="ralentissement",
      intention="Dire d'où vient le récit (2/2) : le texte de Michael Joseph publié par Vodafone.",
      description="Page Vodafone (2017) recadrée sur la signature « Michael Joseph, Vodafone Group's Director of Mobile Money » ; la page de 2007 reste à gauche.",
      sujet="signature Michael Joseph", composition="split-screen : 2007 à gauche, 2017 à droite", texte_ecran=["MICHAEL JOSEPH · VODAFONE · 2017"], res=["R12"], faits=["F62"],
      remplacement="Typographie : nom, fonction, date et éditeur.", ambiance="nappe", effets=[], transition_entree="glissement latéral", transition="coupe franche",
      montage="Ne montrer aucune photo de Michael Joseph (aucune image libre identifiée).", risques="Ne pas suggérer qu'il a inventé seul le service."),
 dict(seq="SEQ-03", fin="de la même façon.", kind="illus", rythme="révélation",
      intention="Révéler l'intention initiale : le microcrédit.",
      description="Animation au trait : une petite somme part d'une institution de microcrédit (bâtiment schématique, sans nom) vers un téléphone, puis revient en petits remboursements.",
      sujet="boucle prêt / remboursement", composition="institution à gauche, téléphone à droite, trajet en arc", mouvement_graphique="aller simple, puis trois petits retours",
      texte_ecran=["SELON L'ÉQUIPE PROJET ET VODAFONE"], res=["R22"], faits=["F8"],
      animation=dict(comprendre="le prototype servait à verser et rembourser des microcrédits", elements="bâtiment, téléphone, pièces stylisées", mouvement="trajet en arc, retours en pointillés",
                     duree="11 s", entree="sur « L'équipe travaille sur le microcrédit »", sortie="la boucle se fige", style="trait orange sur noir",
                     contraintes="aucun nom d'institution réelle", assets="illustrations vectorielles R22"),
      ambiance="nappe", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Deux boucles au maximum.", risques=""),
 dict(seq="SEQ-03", fin="au nord de la capitale.", kind="carte", rythme="précision",
      intention="Situer et dater le prototype.", description="La carte se resserre sur la région de Nairobi : Nairobi et Thika apparaissent, date « OCTOBRE 2005 ».",
      sujet="Nairobi, Thika", composition="deux points, Thika au nord", mouvement_graphique="recadrage de carte (zoom 2D motivé : passer du pays à la région), 1,5 s",
      texte_ecran=["NAIROBI", "THIKA", "PILOTE · OCTOBRE 2005"], res=["R20"], faits=["F76"],
      animation=dict(comprendre="où et quand le prototype est testé", elements="deux points, une date", mouvement="recadrage unique", duree="6 s",
                     entree="sur « Le prototype »", sortie="coupe", style="carte maîtresse", contraintes="positions exactes", assets="Natural Earth + coordonnées des villes"),
      ambiance="nappe", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Carte maîtresse, état 2/4 (détail).", risques="Ne pas ajouter le troisième lieu (Mathare) sans le dire : il n'est pas dans la voix off."),
 # ---------------------------------------------------------------- SEQ-04
 dict(seq="SEQ-04", fin="devient un coursier.", kind="carte", rythme="accélération",
      intention="Faire voir le détournement : l'argent part ailleurs.", description="Depuis la région de Nairobi, des fils orange partent vers plusieurs régions du Kenya (premier fil de l'argent).",
      sujet="fils orange", composition="origine au centre, fils vers les bords", mouvement_camera="suivi_trace", mouvement_graphique="les fils s'étirent, accélèrent sur « coursier »",
      texte_ecran=["D'APRÈS MICHAEL JOSEPH (VODAFONE, 2017)"], res=["R20"], faits=["F8"],
      animation=dict(comprendre="l'argent prêté circule vers d'autres personnes, loin", elements="5 à 7 fils orange", mouvement="tracés progressifs, vitesse croissante",
                     duree="11 s", entree="sur « ceux qui reçoivent un prêt »", sortie="les fils se figent", style="fil de l'argent (1/3)", contraintes="destinations schématiques, non nommées", assets="carte maîtresse"),
      ambiance="pulsation légère", effets=[], transition_entree="coupe franche", transition="coupe au noir", montage="Carte maîtresse, état 3/4 ; fil 1/3.", risques="Ne pas nommer de villes de destination (non sourcées)."),
 dict(seq="SEQ-04", fin="raconte-t-il.", kind="doc", rythme="tension, puis décision",
      intention="Le moment de décision, montré dans le document qui le rapporte.",
      description="Page Vodafone (2017) recadrée sur « So we took a chance, and re-engineered the loans system… » ; sous-titre : « Alors nous avons pris un risque ».",
      sujet="citation de Michael Joseph", composition="phrase au centre, page floutée", texte_ecran=["« ALORS NOUS AVONS PRIS UN RISQUE »", "MICHAEL JOSEPH · VODAFONE · 2017"], res=["R12"], faits=["F63"],
      remplacement="Typographie de la citation, original anglais dessous.", ambiance="silence d'une seconde avant la citation", effets=[], transition_entree="coupe du noir", transition="coupe franche",
      montage="La musique s'arrête avant « Alors » ; reprise sur le plan suivant.", risques="Citation traduite : original visible ; texte d'anniversaire de l'entreprise (2017), date affichée."),
 dict(seq="SEQ-04", fin="d'un téléphone à un autre.", kind="info", rythme="résolution",
      intention="Résumer la transformation du produit.", description="Le schéma « PRÊT → REMBOURSEMENT » se réécrit en « TÉLÉPHONE → TÉLÉPHONE ».",
      sujet="schéma de fonction", composition="schéma centré", mouvement_graphique="réécriture du schéma (pas de morphing d'icônes)",
      texte_ecran=["PRÊT → REMBOURSEMENT", "TÉLÉPHONE → TÉLÉPHONE"], res=["R21"], faits=["F9"],
      animation=dict(comprendre="le produit change de fonction", elements="deux lignes de texte, une flèche", mouvement="la première ligne s'efface, la seconde s'écrit",
                     duree="7 s", entree="sur « reconstruit »", sortie="coupe", style="typographie éditoriale", contraintes="", assets="gabarit"),
      ambiance="pulsation reprise", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques=""),
 # ---------------------------------------------------------------- SEQ-05
 dict(seq="SEQ-05", fin="La réponse passe par des commerçants.", kind="photo", rythme="respiration, terrain",
      intention="Montrer un vrai point d'argent mobile.", description="Agent M-PESA et Equity à Nairobi (photo réelle, 2016).",
      sujet="agent d'argent mobile", composition="comptoir et enseigne", texte_ecran=["NAIROBI · 2016 · PHOTO : FIONA GRAHAM · CC BY-SA 2.0"], res=["R02"], faits=["F43"],
      remplacement="R03 (kiosque de Nairobi, 2026).", ambiance="ambiance de rue (Freesound, CC0)", effets=[], transition_entree="coupe franche", transition="coupe franche",
      montage="Contenu visuel à inspecter avant montage.", risques="Photo de 2016 datée ; enseignes de marques visibles, non mises en valeur."),
 dict(seq="SEQ-05", fin="au comptoir.", kind="recon", rythme="détail",
      intention="Rendre concret le dépôt d'espèces.", description="Insert : deux mains posent des billets sur un comptoir de bois, à côté d'un téléphone à clavier ; aucun visage.",
      sujet="dépôt d'espèces", composition="mains au centre, téléphone en bord de cadre", texte_ecran=[], res=["R22"], faits=["F43"],
      remplacement="Illustration au trait : billets → comptoir (mention ILLUSTRATION).", ambiance="ambiance de boutique, discrète", effets=["froissement de billets (discret)"],
      transition_entree="coupe franche", transition="raccord par le fil", montage="Billets génériques ou flous : ne pas falsifier de monnaie.", risques="Ne montrer aucune marque ni interface."),
 dict(seq="SEQ-05", fin="Il l'envoie.", kind="illus", rythme="explication",
      intention="Expliquer la conversion en monnaie électronique.", description="Animation pas à pas : billets → SMS → montant inscrit dans une carte SIM dessinée ; le fil orange part de la SIM.",
      sujet="SMS et carte SIM", composition="trois étapes de gauche à droite", mouvement_camera="suivi_trace", mouvement_graphique="le fil part de la SIM vers la droite",
      texte_ecran=[], res=["R22"], faits=["F43"],
      animation=dict(comprendre="l'argent devient électronique et voyage par SMS", elements="billets, bulle SMS, carte SIM, fil", mouvement="trois étapes enchaînées",
                     duree="9 s", entree="sur « Quelques SMS plus tard »", sortie="le fil sort du cadre", style="trait orange (fil 2/3)", contraintes="aucune interface réelle", assets="R22"),
      ambiance="motif rythmé léger", effets=["bip de SMS (signature sonore 2/3)"], transition_entree="raccord par le fil", transition="raccord par le fil", montage="Fil 2/3.", risques=""),
 dict(seq="SEQ-05", fin="de son quartier.", kind="photo", rythme="arrivée",
      intention="Le retrait chez un commerçant du quartier.", description="Le fil s'arrête au bord du cadre ; photo réelle d'un kiosque de Nairobi qui propose de l'argent mobile (2026).",
      sujet="kiosque de quartier", composition="kiosque au centre", texte_ecran=["NAIROBI · 2026 · PHOTO : PUNKKATZ · CC BY 4.0"], res=["R03"], faits=["F43"],
      remplacement="R02 recadrée différemment.", ambiance="ambiance de rue", effets=[], transition_entree="raccord par le fil", transition="coupe franche",
      montage="Le fil ne se superpose pas à la photo.", risques="Photo de 2026 datée ; contenu à inspecter."),
 dict(seq="SEQ-05", fin="l'argent de leurs clients.", kind="photo", rythme="respiration",
      intention="Les agents sont de petites boutiques.", description="Kiosque M-Pesa au Kenya (photo réelle, date inconnue) ; en bas, la citation « ‘mom and pop’ stores ».",
      sujet="kiosque M-Pesa", composition="kiosque plein cadre", texte_ecran=["KENYA · DATE INCONNUE · PHOTO : REALT0N12 · CC BY-SA 3.0", "« ‘MOM AND POP’ STORES » — VODAFONE (2017)"], res=["R04"], faits=["F44"],
      remplacement="R02.", ambiance="ambiance de rue", effets=[], transition_entree="coupe franche", transition="coupe sèche au noir",
      montage="Ne jamais afficher la date des métadonnées (2005, impossible).", risques="Date inconnue : le dire ; contenu à inspecter."),
 # ---------------------------------------------------------------- SEQ-06
 dict(seq="SEQ-06", fin="ou déjà de la banque ?", kind="typo", rythme="tension : question",
      intention="Poser la question qui structure la seconde moitié du film.", description="Écran partagé sur noir : « TÉLÉPHONE ? » à gauche, « BANQUE ? » à droite ; une ligne verticale orange les sépare.",
      sujet="question du statut", composition="symétrie gauche / droite", mouvement_graphique="les deux mots apparaissent l'un après l'autre",
      texte_ecran=["TÉLÉPHONE ?", "BANQUE ?"], res=["R21"], faits=[],
      animation=dict(comprendre="le service brouille la frontière entre téléphone et banque", elements="deux mots, une ligne", mouvement="apparitions successives",
                     duree="6 s", entree="sur « téléphone »", sortie="figé", style="Archivo Black", contraintes="motif repris en SEQ-06 et SEQ-09", assets="gabarit"),
      ambiance="basse tenue, dissonance discrète", effets=[], transition_entree="coupe du noir", transition="coupe franche", montage="Conserver le fichier : le motif revient deux fois.", risques=""),
 dict(seq="SEQ-06", fin="sans licence.", kind="typo", rythme="conflit",
      intention="Donner la voix de l'opposition.", description="Citation d'Agence Ecofin en IBM Plex Mono : « une incursion dans leur champ de compétence » ; le mot « BANQUE ? » de l'écran précédent reste en filigrane.",
      sujet="objection des banques", composition="citation centrée", mouvement_graphique="apparition ligne à ligne", texte_ecran=["« UNE INCURSION DANS LEUR CHAMP DE COMPÉTENCE »", "SOURCE : AGENCE ECOFIN"], res=["R15"], faits=["F46"],
      remplacement="Capture de l'article d'Agence Ecofin si l'éditeur peut la réaliser dans un navigateur.", ambiance="tension", effets=[], transition_entree="coupe franche", transition="coupe franche",
      montage="", risques="Article non relu (site protégé) ; banques non nommées."),
 dict(seq="SEQ-06", fin="de trancher.", kind="archive", rythme="ralentissement, arbitrage",
      intention="Le régulateur entre en scène.", description="Photo de la Banque centrale du Kenya prise le 7 mars 2007 : panoramique vertical lent de la façade vers l'enseigne « CENTRAL BANK OF KENYA » (révélation de l'institution).",
      sujet="Banque centrale du Kenya", composition="façade en contre-plongée, enseigne en bas à droite", texte_ecran=["BANQUE CENTRALE DU KENYA · 7 MARS 2007 · PHOTO : DEMOSH · CC BY 2.0"], res=["R06"], faits=[],
      remplacement="R07 (qualité faible) ou typographie « BANQUE CENTRALE DU KENYA ».", ambiance="ambiance de ville lointaine", effets=[], transition_entree="coupe franche", transition="coupe franche (même photo)",
      montage="Le panoramique a une fonction : révéler l'enseigne ; vitesse calée sur la phrase.", risques="Coïncidence de date : ne pas suggérer que la photo documente une décision sur M-Pesa."),
 dict(seq="SEQ-06", fin="doit être enregistré.", kind="archive", mouvement_camera="fixe", rythme="explication",
      intention="Le feu vert sous conditions.", description="Même photo, cadre fixe sur l'enseigne, assombri à gauche ; trois conditions puis l'enregistrement des clients s'inscrivent en liste.",
      sujet="conditions du régulateur", composition="liste à gauche, enseigne à droite", mouvement_graphique="quatre lignes successives",
      texte_ecran=["PLAFOND DE DÉPÔT (BLANCHIMENT)", "PROTECTION DES CLIENTS", "SÉCURITÉ DES AGENTS", "ENREGISTREMENT DE CHAQUE CLIENT", "SOURCES : AGENCE ECOFIN · VODAFONE"], res=["R06"], faits=["F45"],
      ambiance="résolution partielle de la tension", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques=""),
 dict(seq="SEQ-06", fin="lancé en mars 2007.", kind="info", rythme="repère",
      intention="Dater le lancement et rappeler le pilote.", description="Frise sobre : « OCT. 2005 · PILOTE » → « MARS 2007 · LANCEMENT ».",
      sujet="frise", composition="frise horizontale centrée", mouvement_graphique="la frise se trace de gauche à droite", texte_ecran=["OCT. 2005 · PILOTE", "MARS 2007 · LANCEMENT"], res=["R21"], faits=["F7"],
      animation=dict(comprendre="un an et demi entre le pilote et le lancement", elements="ligne, deux jalons", mouvement="tracé 1,5 s", duree="4 s",
                     entree="sur « lancé »", sortie="coupe", style="frise LUKOJI", contraintes="pas de jour précis", assets="gabarit"),
      ambiance="nappe", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques=""),
 dict(seq="SEQ-06", fin="ne disparaîtra pas.", kind="typo", rythme="suspension",
      intention="Laisser la question ouverte jusqu'à SEQ-09.", description="Retour de l'écran partagé « TÉLÉPHONE ? / BANQUE ? », qui s'assombrit lentement.",
      sujet="question ouverte", composition="symétrie", mouvement_graphique="assombrissement lent", texte_ecran=["TÉLÉPHONE ?", "BANQUE ?"], res=["R21"], faits=[],
      ambiance="basse tenue qui s'éteint", effets=[], transition_entree="coupe franche", transition="fondu au noir court (0,5 s)", duree_extra=1.0,
      montage="Une seconde de silence avant SEQ-07.", risques=""),
 # ---------------------------------------------------------------- SEQ-07
 dict(seq="SEQ-07", fin="la fin de la première année.", kind="graph", rythme="relance",
      intention="Donner l'échelle de départ, en citant l'entreprise.", description="Chiffre unique « 1,2 MILLION », sous-titre « UTILISATEURS À LA FIN DE LA PREMIÈRE ANNÉE ».",
      sujet="1,2 million", composition="chiffre centré", mouvement_graphique="compteur bref (1 s)", texte_ecran=["1,2 MILLION", "SOURCE : VODAFONE · CHIFFRE DE L'ENTREPRISE"], res=["R21"], faits=["F10"],
      ambiance="motif d'ampleur retenu", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques="Chiffre non audité."),
 dict(seq="SEQ-07", fin="la République démocratique du Congo.", kind="carte", rythme="ampleur",
      intention="Rendre visible le périmètre des 51 millions : sept pays.", description="Carte de l'Afrique : les sept pays cités par Vodafone s'allument (Kenya, Tanzanie, Mozambique, RDC, Lesotho, Ghana, Égypte) ; la RDC reste éclairée plus longtemps.",
      sujet="sept pays", composition="Afrique centrée", mouvement_graphique="les pays s'allument un à un, la RDC en dernier",
      texte_ecran=["51 MILLIONS DE CLIENTS DANS 7 PAYS · 600 000 AGENTS · 2022", "SOURCE : VODAFONE · CHIFFRES DE L'ENTREPRISE", "RÉPUBLIQUE DÉMOCRATIQUE DU CONGO"], res=["R20"], faits=["F49"],
      animation=dict(comprendre="les 51 millions concernent sept pays, pas le seul Kenya", elements="carte d'Afrique, 7 pays", mouvement="allumage successif",
                     duree="10 s", entree="sur « En 2022 »", sortie="la RDC reste allumée", style="aplats", contraintes="liste des pays : page Vodafone de 2022", assets="Natural Earth"),
      ambiance="motif d'ampleur", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Lève l'ambiguïté orale des « 51 millions ».", risques="Pas de globe 3D."),
 dict(seq="SEQ-07", fin="Pas ce qui a changé pour eux.", kind="doc", rythme="pivot critique",
      intention="Montrer que ces chiffres viennent d'un communiqué.", description="Page Vodafone de 2022 ; en surimpression, une ligne : « CHIFFRES DE L'ENTREPRISE ».",
      sujet="page Vodafone 2022", composition="page plein cadre, ligne en bas", texte_ecran=["CHIFFRES DE L'ENTREPRISE · VODAFONE · 2022"], res=["R24"], faits=["F49"],
      ambiance="la musique s'interrompt sur « Pas ce qui a changé »", effets=[], transition_entree="coupe franche", transition="coupe sèche", montage="", risques=""),
 # ---------------------------------------------------------------- SEQ-08
 dict(seq="SEQ-08", fin="un service financier formel.", kind="graph", rythme="rappel",
      intention="Reprendre la barre de SEQ-02 : le bond.", description="La barre de SEQ-02 revient à 26,7 % (2006) et monte jusqu'à 82,9 % (2019).",
      sujet="26,7 % → 82,9 %", composition="même gabarit et même échelle qu'en SEQ-02", mouvement_graphique="montée de la barre (1,5 s)",
      texte_ecran=["2006 : 26,7 %", "2019 : 82,9 %", "ADULTES · SERVICE FINANCIER FORMEL", "SOURCE : FINACCESS 2019 (CBK · KNBS · FSD KENYA)"], res=["R21", "R27"], faits=["F75"],
      animation=dict(comprendre="la finance formelle a fortement progressé", elements="barre de SEQ-02", mouvement="montée", duree="7 s",
                     entree="sur « En 2019 »", sortie="figée", style="gabarit chiffres", contraintes="même échelle qu'en SEQ-02", assets="projet de SEQ-02"),
      ambiance="musique très basse", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques=""),
 dict(seq="SEQ-08", fin="dans la vie des gens.", kind="graph", rythme="nuance",
      intention="Expliquer le biais de définition.", description="Sur la barre figée, une zone hachurée et l'étiquette « INCLUT L'ARGENT MOBILE (CLASSÉ FORMEL) », sans pourcentage ; puis « ≠ CE QUE M-PESA A CHANGÉ ».",
      sujet="biais de définition", composition="barre à gauche, étiquettes à droite", mouvement_graphique="apparition des hachures puis des étiquettes",
      texte_ecran=["INCLUT L'ARGENT MOBILE (CLASSÉ FORMEL)", "≠ CE QUE M-PESA A CHANGÉ"], res=["R21"], faits=["F75"],
      animation=dict(comprendre="la hausse inclut mécaniquement l'argent mobile", elements="hachures, deux étiquettes", mouvement="apparitions", duree="10 s",
                     entree="sur « Mais »", sortie="coupe", style="hachures grises", contraintes="aucun chiffre inventé pour la part du mobile", assets="gabarit"),
      ambiance="musique très basse", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques="Ne pas quantifier la part de l'argent mobile (non sourcée)."),
 dict(seq="SEQ-08", fin="près de chez elles.", kind="info", rythme="méthode",
      intention="Expliquer la méthode avant le résultat.", description="Schéma : un panel de familles suivies de 2008 à 2014 ; autour d'un foyer, un cercle de 1 km où apparaissent des points d'agents.",
      sujet="méthode de Suri et Jack", composition="frise 2008-2014 en haut, cercle en bas", mouvement_graphique="la frise se trace, puis les points apparaissent dans le cercle",
      texte_ecran=["TAVNEET SURI · WILLIAM JACK", "PANEL DE MÉNAGES · 2008 → 2014", "AGENTS DANS UN RAYON DE 1 KM"], res=["R21"], faits=["F79"],
      animation=dict(comprendre="on compare des familles selon le nombre d'agents installés près de chez elles", elements="frise, foyer, cercle, points",
                     mouvement="tracé puis apparitions", duree="12 s", entree="sur « Pour le mesurer »", sortie="coupe", style="schéma épuré", contraintes="ne pas montrer de « groupe témoin » : la mesure est continue", assets="gabarit"),
      ambiance="silence musical, voix seule", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques=""),
 dict(seq="SEQ-08", fin="dans la revue Science en 2016.", kind="doc", rythme="caution",
      intention="Montrer la publication scientifique.", description="Première page de l'article de Science (2016) : titre et noms des auteurs, trait orange sous le titre.",
      sujet="article de Science", composition="titre au centre", texte_ecran=["SCIENCE · VOL. 354 · 9 DÉCEMBRE 2016"], res=["R28"], faits=["F78"],
      remplacement="Page MIT News (R13) qui rend compte de l'étude, ou référence en typographie.", ambiance="voix seule", effets=[], transition_entree="coupe franche", transition="coupe franche",
      montage="Extrait court (titre) ; tenir au moins 3 s.", risques="Droits de reproduction de l'article à confirmer (AAAS) ; à défaut, typographie."),
 dict(seq="SEQ-08", fin="2 % des ménages du pays.", kind="graph", rythme="révélation du résultat",
      intention="Rendre l'ordre de grandeur lisible.", description="Grille de 100 carrés gris ; 2 deviennent orange. Légende : « AU MOINS 194 000 FOYERS · 2 % DES MÉNAGES · ESTIMATION ».",
      sujet="2 %", composition="grille centrée, légende dessous", mouvement_graphique="deux carrés s'allument",
      texte_ecran=["AU MOINS 194 000 FOYERS (ESTIMATION)", "2 % DES MÉNAGES", "SOURCE : SURI & JACK, SCIENCE (2016)"], res=["R21"], faits=["F78"],
      animation=dict(comprendre="un effet réel mais limité à 2 % des ménages", elements="grille 10×10", mouvement="allumage", duree="10 s",
                     entree="sur « au moins »", sortie="figée", style="gabarit", contraintes="mot « estimation » toujours visible", assets="gabarit"),
      ambiance="voix seule", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques=""),
 dict(seq="SEQ-08", fin="dirigés par des femmes.", kind="typo", rythme="précision",
      intention="Définir le seuil et donner l'effet par genre.", description="Sous la grille : « SEUIL : 1,25 $ PAR JOUR ET PAR PERSONNE », puis « EFFET PLUS FORT : FOYERS DIRIGÉS PAR DES FEMMES ».",
      sujet="seuil et effet par genre", composition="deux lignes sous la grille", mouvement_graphique="apparition ligne à ligne",
      texte_ecran=["SEUIL : 1,25 $ PAR JOUR ET PAR PERSONNE", "EFFET PLUS FORT : FOYERS DIRIGÉS PAR DES FEMMES"], res=["R21"], faits=["F78", "F12"],
      ambiance="voix seule", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Aucune photo de personne associée à ces chiffres.", risques=""),
 dict(seq="SEQ-08", fin="Pas un décompte.", kind="typo", rythme="ralentissement, limite",
      intention="Clore sur la limite.", description="Le mot « ESTIMATION » en grand, puis « ≠ DÉCOMPTE ».",
      sujet="limite méthodologique", composition="mot centré", mouvement_graphique="apparition sèche", texte_ecran=["ESTIMATION", "≠ DÉCOMPTE"], res=["R21"], faits=["F78"],
      ambiance="silence", effets=[], transition_entree="coupe franche", transition="coupe au noir", duree_extra=0.5, montage="Silence complet sur « Pas un décompte ».", risques=""),
 # ---------------------------------------------------------------- SEQ-09
 dict(seq="SEQ-09", fin=None, duree=2.0, kind="typo", type_visuel="plan_ambiance", authenticite="graphique_explicatif", statut_image="noir (respiration)",
      rythme="respiration, rupture", intention="Marquer le changement de régime du film.", description="Noir complet, sans texte.",
      sujet="noir", composition="—", mouvement_graphique="aucun", texte_ecran=[], res=[], faits=[], ambiance="silence total", effets=[],
      transition_entree="coupe au noir", transition="coupe franche", montage="2 s de silence.", risques=""),
 dict(seq="SEQ-09", fin="montant envoyé.", kind="photo", rythme="relance : le coût",
      intention="Le coût, du côté des usagers.", description="Agent M-PESA de Nairobi (R02), autre recadrage que SEQ-05 (enseigne seule) ; en bas, « JUSQU'À 7 % (CERTAINS TRANSFERTS) ».",
      sujet="agent, coût", composition="enseigne plein cadre, chiffre en bas à gauche", texte_ecran=["JUSQU'À 7 % DU MONTANT · CERTAINS TRANSFERTS", "SOURCE : AGENCE ECOFIN (2025)", "PHOTO : FIONA GRAHAM · CC BY-SA 2.0"], res=["R02"], faits=["F55"],
      remplacement="Jauge graphique seule.", ambiance="reprise musicale en mineur", effets=[], transition_entree="coupe du noir", transition="coupe franche",
      montage="Deuxième usage de R02 : recadrage nettement différent.", risques="« Certains transferts » : ne pas généraliser ; contenu de la photo à inspecter."),
 dict(seq="SEQ-09", fin="d'ici 2028.", kind="archive", type_visuel="photo_lieu", mouvement_camera="fixe", statut_image="authentique (photo de 2007, réutilisée)",
      rythme="réponse annoncée", intention="Le régulateur prépare une réponse.", description="Banque centrale du Kenya (R06), cadre serré sur l'enseigne ; flèche « 23 → 10 KES » et le mot « PROJET ».",
      sujet="projet de baisse des frais", composition="enseigne à droite, flèche à gauche", mouvement_graphique="la flèche descend",
      texte_ecran=["23 → 10 SHILLINGS PAR TRANSACTION (COÛT MOYEN)", "PROJET · D'ICI 2028 · RAPPORTÉ PAR DES MÉDIAS KÉNYANS (VIA AGENCE ECOFIN)"], res=["R06"], faits=["F55"],
      remplacement="R07 (qualité faible) ou flèche graphique seule.", ambiance="musique en mineur", effets=[], transition_entree="coupe franche", transition="coupe franche",
      montage="Le mot « PROJET » reste visible tout le plan.", risques="Ne pas présenter le plafonnement comme adopté ; photo de 2007 réutilisée : légende."),
 dict(seq="SEQ-09", fin="revenus de services au Kenya.", kind="graph", rythme="contrepoint",
      intention="Le poids du service pour l'opérateur.", description="Barre horizontale des revenus de services de Safaricom au Kenya : 44,2 % pour M-PESA.",
      sujet="44,2 %", composition="barre horizontale, valeur jaune", mouvement_graphique="remplissage 1 s",
      texte_ecran=["44,2 % DES REVENUS DE SERVICES AU KENYA", "EXERCICE 2025 · SOURCE : SAFARICOM"], res=["R21", "R31"], faits=["F80"],
      animation=dict(comprendre="M-Pesa pèse près de la moitié des revenus de services de Safaricom au Kenya", elements="une barre", mouvement="remplissage", duree="8 s",
                     entree="sur « Pour Safaricom »", sortie="coupe", style="gabarit", contraintes="périmètre exact : services, Kenya", assets="gabarit"),
      ambiance="musique qui monte légèrement", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Pas de camembert.", risques=""),
 dict(seq="SEQ-09", fin="séparées de M-Pesa.", kind="doc", rythme="tension politique",
      intention="La question de SEQ-06 revient, portée par des élus.", description="Titre de l'article de The Star (17/11/2020) ; puis retour bref du motif « TÉLÉPHONE ? / BANQUE ? » en filigrane.",
      sujet="sénateurs, 2020", composition="titre au centre, motif en filigrane", mouvement_graphique="apparition du motif en surimpression (20 % d'opacité)",
      texte_ecran=["THE STAR · 17 NOVEMBRE 2020", "SÉNAT KÉNYAN · COMITÉ DES TIC"], res=["R30"], faits=["F81"],
      remplacement="Typographie : titre et date de l'article.", ambiance="point culminant de la tension", effets=[], transition_entree="coupe franche", transition="coupe franche",
      montage="Rappel explicite du motif de SEQ-06.", risques="Article de la rubrique Opinion/Columnists : la légende dit seulement « The Star »."),
 dict(seq="SEQ-09", fin="la protection des plus pauvres.", kind="typo", rythme="élargissement",
      intention="Les nouveaux usages et leur risque.", description="Citation d'Agence Ecofin en IBM Plex Mono : « des questions se posent quant à la protection des pauvres ».",
      sujet="crédit mobile", composition="citation centrée", mouvement_graphique="apparition ligne à ligne", texte_ecran=["« DES QUESTIONS SE POSENT QUANT À LA PROTECTION DES PAUVRES »", "SOURCE : AGENCE ECOFIN (2019)"], res=["R21"], faits=["F58"],
      ambiance="musique qui retombe", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques="Article non relu (site protégé)."),
 dict(seq="SEQ-09", fin="applications de prêt sur téléphone.", kind="info", rythme="chiffre final",
      intention="Donner l'ampleur du crédit numérique.", description="110 petits carrés neutres (applications) apparaissent en grille ; à côté, la couverture du rapport de FSD Kenya.",
      sujet="110 applications", composition="grille à gauche, document à droite", mouvement_graphique="les carrés apparaissent par rangées",
      texte_ecran=["≈ 110 APPLICATIONS DE PRÊT · SEPTEMBRE 2018", "SOURCE : FSD KENYA, DIGITAL CREDIT AUDIT REPORT (2019)"], res=["R21", "R32"], faits=["F82"],
      animation=dict(comprendre="le crédit sur téléphone s'est multiplié très vite", elements="110 carrés neutres", mouvement="apparition par rangées", duree="7 s",
                     entree="sur « En septembre 2018 »", sortie="figée puis coupe", style="carrés gris, aucune icône réelle", contraintes="aucun logo d'application", assets="gabarit"),
      ambiance="musique éteinte", effets=[], transition_entree="coupe franche", transition="coupe au noir", montage="", risques=""),
 # ---------------------------------------------------------------- SEQ-10
 dict(seq="SEQ-10", fin="les monnaies locales et l'argent mobile.", kind="doc", rythme="critique de fond",
      intention="Une critique académique, avec son cadre.", description="Page OpenEdition (Revue de la régulation, présentation de thèse) ; trait orange sous la phrase comparant monnaies locales et monnaie mobile.",
      sujet="présentation de thèse", composition="paragraphe au centre", texte_ecran=["PRÉSENTATION DE THÈSE · REVUE DE LA RÉGULATION (OPENEDITION)"], res=["R14"], faits=["F59"],
      remplacement="Typographie de la phrase source et de la référence (capture bloquée pour l'agent : à réaliser dans un navigateur).", ambiance="thème final, très bas", effets=[],
      transition_entree="coupe du noir", transition="coupe franche", montage="", risques="Auteur non nommé ; page non relue depuis la protection anti-robots."),
 dict(seq="SEQ-10", fin="causes systémiques de la pauvreté.", kind="typo", rythme="critique de fond",
      intention="Donner le jugement de l'auteur, dans ses propres termes.", description="La phrase source en IBM Plex Mono : « Les monnaies locales visent les causes systémiques de la pauvreté, ce que les systèmes de monnaie mobile ne font pas. »",
      sujet="citation de la thèse", composition="citation centrée", mouvement_graphique="apparition ligne à ligne",
      texte_ecran=["« LES MONNAIES LOCALES VISENT LES CAUSES SYSTÉMIQUES DE LA PAUVRETÉ, CE QUE LES SYSTÈMES DE MONNAIE MOBILE NE FONT PAS. »", "PRÉSENTATION DE THÈSE · REVUE DE LA RÉGULATION"], res=["R21"], faits=["F59"],
      ambiance="thème final, très bas", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="", risques="Citation exacte de la source capturée en phase 1."),
 dict(seq="SEQ-10", fin="tout existait déjà.", kind="photo", rythme="rappel, respiration",
      intention="Tout existait déjà : le rappeler par l'image.", description="Trois photos déjà vues, en coupes sèches de 2 s : agent de Nairobi (2016), kiosque (date inconnue), kiosque de Nairobi (2026).",
      sujet="rappel", composition="trois plans fixes", texte_ecran=["PHOTOS : F. GRAHAM (CC BY-SA 2.0) · REALT0N12 (CC BY-SA 3.0) · PUNKKATZ (CC BY 4.0)"], res=["R02", "R04", "R03"], faits=[],
      ambiance="ambiance de rue légère", effets=[], transition_entree="coupe franche", transition="coupe franche", montage="Coupes calées sur « téléphone », « SMS », « boutiques ».", risques=""),
 dict(seq="SEQ-10", fin="en faisaient vraiment.", kind="carte", rythme="synthèse",
      intention="Boucler la carte du récit sur la leçon du titre.", description="Dernier retour à la carte du Kenya : les fils orange sont devenus denses (dernier fil de l'argent).",
      sujet="carte, fils denses", composition="pays centré", mouvement_graphique="les fils se densifient lentement", texte_ecran=["SELON LE RÉCIT DE SES CONCEPTEURS"], res=["R20"], faits=[],
      animation=dict(comprendre="l'usage des clients a dessiné le réseau", elements="carte, fils", mouvement="densification", duree="9 s", entree="sur « Si l'on suit »",
                     sortie="glissement vers l'Afrique", style="fil 3/3", contraintes="", assets="carte maîtresse"),
      ambiance="thème final", effets=["bip de SMS (signature sonore 3/3)"], transition_entree="coupe franche", transition="glissement de carte vers l'Afrique centrale",
      montage="Carte maîtresse, état 4/4 ; fil 3/3.", risques="Interprétation éditoriale : le sous-titre l'attribue au récit des concepteurs."),
 dict(seq="SEQ-10", fin="ne se transpose pas telle quelle.", kind="carte", rythme="ouverture prudente",
      intention="Ouvrir vers la RDC sans comparaison.", description="La carte glisse du Kenya vers la RDC, qui s'éclaire seule ; aucune donnée comparative.",
      sujet="RDC", composition="RDC centrée", mouvement_graphique="glissement de carte (motivé : changement de pays)", texte_ecran=["RÉPUBLIQUE DÉMOCRATIQUE DU CONGO", "PRÉSENCE DE M-PESA SELON VODAFONE (2022)"], res=["R20"], faits=["F49"],
      ambiance="thème final", effets=[], transition_entree="glissement de carte", transition="fondu enchaîné (1 s)", montage="", risques="Ne montrer aucun chiffre pour la RDC."),
 dict(seq="SEQ-10", fin="au profit de qui ?", kind="photo", type_visuel="plan_ambiance", authenticite="symbolique",
      statut_image="authentique (photo réelle de 2013) utilisée comme image d'illustration", mention_ecran="IMAGE D'ILLUSTRATION — KINSHASA, 2013",
      rythme="question finale, ralentissement", intention="Poser la question au public congolais.", description="Boulevard du 30 Juin, Kinshasa (photo réelle, 2013) ; la dernière question s'inscrit en Archivo Black ; silence, puis fondu au noir.",
      sujet="Kinshasa", composition="boulevard en perspective, question au tiers inférieur", mouvement_graphique="apparition de la question", texte_ecran=["À QUELLES CONDITIONS, ET AU PROFIT DE QUI ?", "PHOTO : ANTOINE MOENS DE HASE · CC BY 2.0"], res=["R11"], faits=[],
      remplacement="Plan tourné par LUKOJI à Kinshasa (préférable) ; à défaut, la question sur noir.", ambiance="ambiance de ville lointaine, puis silence", effets=[],
      transition_entree="fondu enchaîné", transition="fondu au noir (fin ; la signature LUKOJI est ajoutée par le moteur vidéo)", duree_extra=2.0,
      montage="Deux secondes de silence avant le fondu.", risques="Aucun argent mobile visible : image d'illustration ; contenu à inspecter."),
]


def build() -> dict:
    script, struct = load_locked()
    seqs = {s["id"]: s for s in script["sequences"]}
    pos = {k: 0 for k in seqs}
    scenes = []
    for i, sp in enumerate(SPEC, 1):
        base = dict(P[sp["kind"]])
        base.update({k: v for k, v in sp.items() if k in base or k in ("type_visuel", "authenticite", "statut_image", "mention_ecran", "mouvement_camera")})
        seq = sp["seq"]
        vo = ""
        if sp.get("fin"):
            text = seqs[seq]["voix_off"]
            j = text.find(sp["fin"], pos[seq])
            if j < 0:
                raise SystemExit(f"scène {i} : fin introuvable dans {seq} : {sp['fin']!r}")
            end = j + len(sp["fin"])
            vo = text[pos[seq]:end].strip()
            pos[seq] = end
        res = sp["res"]
        sc = {
            "id": f"SC-{i:02d}", "sequence": seq, "voix_off": vo, "intention": sp["intention"], "rythme": sp["rythme"],
            "type_visuel": base["type_visuel"], "authenticite": base["authenticite"], "statut_image": base["statut_image"],
            "description": sp["description"], "sujet": sp["sujet"], "composition": sp["composition"], "cadrage": base["cadrage"],
            "mouvement_camera": base["mouvement_camera"], "mouvement_graphique": sp.get("mouvement_graphique", base.get("mouvement_graphique", "aucun")),
            "animation": ([f"{sp['animation']['mouvement']} ({sp['animation']['duree']}) — {sp['animation']['comprendre']}"] if sp.get("animation") else []),
            "motion_design": sp.get("animation"), "texte_ecran": sp["texte_ecran"],
            "ressources": res, "statut_ressource": sorted({RES[r]["statut"] for r in res}),
            "sources_visuelles": [RES[r].get("page") or RES[r].get("url_directe") or RES[r]["description"] for r in res],
            "source_factuelle": sp["faits"], "plan_remplacement": sp.get("remplacement", "—"),
            "transition_entree": sp["transition_entree"], "transition": sp["transition"],
            "ambiance": sp["ambiance"], "effets_sonores": sp["effets"], "musique": M[seq],
            "difficulte": base["difficulte"], "methode_production": base["methode"],
            "instructions_montage": sp.get("montage") or "—", "raison_narrative": sp["intention"],
            "risques_representation": sp.get("risques") or "Aucun risque particulier identifié.",
        }
        if base.get("mention_ecran"):
            sc["mention_ecran"] = base["mention_ecran"]
        if sp.get("duree"):
            sc["duree_s"] = sp["duree"]
        elif sp.get("duree_extra"):
            from lukoji_engine.story.text import speech_seconds  # noqa: PLC0415
            sc["duree_s"] = round(speech_seconds(vo) + sp["duree_extra"], 1)
        scenes.append(sc)
    for k, s in seqs.items():
        rest = s["voix_off"][pos[k]:].strip()
        if rest:
            raise SystemExit(f"{k} : voix off non couverte : {rest[:60]!r}")
    return {"version_editoriale": "v2.6 — storyboard reconstruit à partir du script v21 et de la structure v6 verrouillés",
            "base_validee": {"script": 21, "structure": 6}, "scenes": scenes}


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))
    doc = build()
    (HERE / "storyboard_v2_6.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"storyboard v2.6 : {len(doc['scenes'])} scènes")
