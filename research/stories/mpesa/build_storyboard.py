"""Construit research/stories/mpesa/storyboard.json : chaque scène reprend EXACTEMENT des phrases du script courant.
Usage : PYTHONPATH=src python3 research/stories/mpesa/build_storyboard.py"""
import json
from lukoji_engine.story.text import sentences

script = json.load(open("research/stories/mpesa/script.json"))
S = {s["id"]: sentences(s["voix_off"]) for s in script["sequences"]}
SRC_TEXTE = "IBM Plex Mono, bas gauche"
COMMONS = "Wikimedia Commons — catégorie « M-Pesa » (licence à vérifier photo par photo)"
PRESSE = "Médiathèques presse Safaricom / Vodafone (droits à demander ; source intéressée, légender)"
scenes = []


def sc(seq, idx, type_, auth, desc, sujet, compo, cadrage, cam, graph, why, risk, montage, transition="coupe franche",
       ambiance="nappe grave discrète", effets=(), texte=(), anim=(), sources=(), recherche=(), mention=None, duree=None):
    vo = " ".join(S[seq][i] for i in idx) if idx else ""
    d = {"id": f"SC-{len(scenes) + 1:03d}", "sequence": seq, "voix_off": vo, "type_visuel": type_, "authenticite": auth,
         "description": desc, "sujet": sujet, "composition": compo, "cadrage": cadrage, "mouvement_camera": cam,
         "mouvement_graphique": graph, "animation": list(anim), "texte_ecran": list(texte), "sources_visuelles": list(sources),
         "recherche": list(recherche), "transition": transition, "ambiance": ambiance, "effets_sonores": list(effets),
         "risques_representation": risk, "instructions_montage": montage, "raison_narrative": why}
    if mention:
        d["mention_ecran"] = mention
    if duree:
        d["duree_s"] = duree
    scenes.append(d)


# SEQ-01 — Le paradoxe d'origine
sc("SEQ-01", [0], "reconstitution", "reconstitution", "Gros plan sur un téléphone à clavier posé sur un comptoir ; un SMS de confirmation de transfert s'affiche.",
   "téléphone à clavier", "téléphone au tiers gauche, comptoir flou derrière", "insert très serré", "insert_detail", "aucun",
   "Ouvrir sur le geste quotidien que tout le monde connaît.", "Ne pas reproduire un vrai écran de marque ni un vrai numéro ; texte de SMS générique.",
   "Caler le bip du SMS sur « geste du quotidien ».", ambiance="rumeur de rue lointaine", effets=["bip de réception de SMS"],
   mention="RECONSTITUTION", recherche=["téléphone à clavier Nokia années 2000 accessoire de tournage"])
sc("SEQ-01", [1, 2], "typographie_animee", "graphique_explicatif", "Sur l'écran du téléphone, la ligne « REMBOURSEMENT DE PRÊT » apparaît puis se barre.",
   "texte du SMS", "texte centré, fond noir", "plein écran", "fixe", "barre orange qui raye le texte en suivant la voix",
   "Matérialiser le paradoxe : l'usage prévu n'était pas l'envoi d'argent.", "Aucun : typographie explicative.",
   "Le trait de rature démarre sur « Pourtant ».", texte=["REMBOURSEMENT DE PRÊT"], anim=["rature orange #FF8A00 de gauche à droite"], effets=["note grave à la rature"])
sc("SEQ-01", [3], "typographie_animee", "graphique_explicatif", "Sous la ligne barrée, « ENVOI À LA FAMILLE » s'écrit lettre par lettre.",
   "texte du SMS", "deux lignes empilées", "plein écran", "fixe", "écriture machine en IBM Plex Mono",
   "Montrer que ce sont les usagers qui ont réécrit la fonction du service.", "Formulation générique, pas une citation.",
   "Fin d'écriture synchronisée avec « autrement ».", texte=["ENVOI À LA FAMILLE"], anim=["apparition lettre par lettre"])
sc("SEQ-01", [4], "carte", "graphique_explicatif", "Le texte se rétracte en un point orange qui devient un fil traversant une carte sombre du Kenya.",
   "carte du Kenya", "carte centrée, fil orange qui la traverse", "plan large", "camera_3d_simulee", "le fil se ramifie en plusieurs tracés",
   "Introduire le motif visuel du film : le fil de l'argent.", "Carte schématique : ne pas laisser croire à des flux réels mesurés.",
   "Transition par le tracé : le fil sort du téléphone et entre dans la carte.", transition="raccord par le fil orange", anim=["fil orange animé", "ramifications"],
   texte=["Kenya"])
sc("SEQ-01", [5], "photo_lieu", "authentique", "Vue d'une rue commerçante de Nairobi aujourd'hui, avec des enseignes d'agents d'argent mobile.",
   "rue commerçante", "enseignes au premier plan, passants flous", "plan moyen", "parallaxe", "titre du film qui apparaît en bas",
   "Ancrer le présent avant de remonter le temps, et annoncer le débat.", "Photo récente : la légender comme telle, pas comme 2007.",
   "Apparition du titre sur « fait aussi débat ».", sources=[COMMONS, "agences photo (AFP, Reuters) — licence payante, alternative gratuite à privilégier"],
   recherche=["Nairobi street M-Pesa agent shop photo", "M-Pesa kiosk Kenya"], texte=["M-PESA : LE DÉTOURNEMENT", "Photo : Nairobi, date à préciser"],
   ambiance="ambiance de rue réelle")
# SEQ-02 — L'argent sous le matelas
sc("SEQ-02", [0, 1], "archive_photo", "authentique", "Photographie d'époque d'un quartier populaire kényan au milieu des années 2000.",
   "quartier résidentiel", "photo plein cadre avec marge noire", "plan large", "panoramique", "date d'archive en surimpression",
   "Situer l'époque et le pays.", "Vérifier date et lieu de la photo ; ne pas utiliser une photo d'un autre pays.",
   "Panoramique lent de gauche à droite, 4 s maximum.", transition="fondu court (6 images)", sources=[COMMONS, "archives de presse kényanes (Nation Media Group) — droits à demander"],
   recherche=["Kenya 2005 neighbourhood photo archive", "Nairobi 2006 street archive"], texte=["KENYA — MILIEU DES ANNÉES 2000"], ambiance="ambiance de quartier")
sc("SEQ-02", [2, 3], "carte", "graphique_explicatif", "Carte : une ville (Nairobi) reliée par un fil orange pointillé à plusieurs villages.",
   "migrations ville / village", "Nairobi au centre, villages en périphérie", "plan large", "fixe", "fils pointillés qui clignotent",
   "Visualiser la distance entre ceux qui gagnent et ceux qui attendent l'argent.", "Tracés illustratifs, non statistiques.",
   "Les pointillés avancent au rythme de la phrase.", anim=["fils pointillés"], texte=["Nairobi"])
sc("SEQ-02", [4, 5], "image_symbolique", "symbolique", "Gare routière animée ; une main tend une enveloppe à un chauffeur de bus par la fenêtre.",
   "enveloppe et chauffeur", "bus en arrière-plan, mains au premier plan", "plan rapproché", "travelling", "aucun",
   "Rendre concret le moyen de transfert d'avant, documenté par Vodafone.", "Image symbolique : mention obligatoire, ne pas suggérer une scène réelle datée.",
   "Coupe sur « Le problème, c'est le chemin » ; travelling latéral le long du bus.", mention="IMAGE D'ILLUSTRATION",
   recherche=["Kenya matatu bus station stock video", "hand giving envelope bus driver"], ambiance="moteurs de bus, brouhaha", effets=["klaxon lointain"],
   texte=["SOURCE : VODAFONE"])
sc("SEQ-02", [6], "photo_lieu", "authentique", "Façade d'une agence bancaire fermée, rideau baissé, dans une petite ville.",
   "agence bancaire", "façade de face, rideau métallique", "plan moyen", "fixe", "assombrissement progressif",
   "Montrer la distance symbolique et physique avec la banque.", "Photo réelle d'une agence : ne pas désigner une banque précise comme fautive.",
   "Plan fixe 3 s, assombrissement en fin.", sources=[COMMONS], recherche=["Kenya bank branch small town photo"], ambiance="silence relatif")
sc("SEQ-02", [7], "graphique", "graphique_explicatif", "Barre unique : 22 % des adultes ont un compte bancaire.",
   "chiffre 22 %", "barre jaune à gauche, chiffre en Archivo Black", "plein écran", "fixe", "la barre monte jusqu'à 22 %",
   "Donner l'ampleur du problème, chiffre attribué.", "Unité « adultes » à afficher clairement.",
   "Chiffre affiché exactement sur « 22 % ».", texte=["22 % DES ADULTES ONT UN COMPTE BANCAIRE", "SOURCE : SURI & JACK, VIA MIT NEWS (2010)"], anim=["montée de barre"])
sc("SEQ-02", [8], "image_symbolique", "symbolique", "Gros plan : des billets glissés sous un matelas, lumière de lampe.",
   "billets sous un matelas", "billets au centre, tissu en flou", "insert", "insert_detail", "le chiffre 77 % apparaît en surimpression",
   "Traduire en image l'épargne informelle.", "Image symbolique : mention ; billets kényans génériques, pas de mise en scène misérabiliste.",
   "Surimpression du chiffre sur « 77 % ».", mention="IMAGE D'ILLUSTRATION", texte=["77 %", "SOURCE : SURI & JACK, VIA MIT NEWS (2010)"], recherche=["money under mattress close up stock"],
   effets=["froissement de billets"])
# SEQ-03 — Une subvention et un prototype
sc("SEQ-03", [0, 1], "document", "authentique", "Capture de la page Vodafone qui mentionne la subvention du ministère britannique du Développement international ; surlignage orange de la phrase.",
   "page source Vodafone", "page en biais, phrase surlignée", "plan rapproché", "insert_detail", "surlignage progressif",
   "Montrer la source de l'information sur l'origine du financement.", "Capture d'une source intéressée : la légender comme communication de Vodafone.",
   "Surlignage synchronisé avec « ministère britannique ».", sources=["https://www.vodafone.com/news/newsroom/digital-society/m-pesa-created (capture, citation courte)"],
   texte=["SOURCE : VODAFONE"], anim=["surlignage orange"], effets=["clic de souris discret"])
sc("SEQ-03", [2, 3], "infographie", "graphique_explicatif", "Schéma : trois blocs reliés — ministère britannique → Vodafone → Safaricom (Kenya).",
   "acteurs du projet", "trois blocs horizontaux", "plein écran", "fixe", "les flèches s'allument une à une",
   "Clarifier qui finance et qui opère.", "Ne pas représenter de montants (non documentés).",
   "Une flèche par proposition de la voix off.", texte=["MINISTÈRE BRITANNIQUE DU DÉVELOPPEMENT INTERNATIONAL", "VODAFONE", "SAFARICOM — KENYA"],
   anim=["flèches orange successives"])
sc("SEQ-03", [4, 5], "animation", "illustration", "Animation : une petite somme part d'une institution de microcrédit vers un téléphone, puis revient par remboursements.",
   "cycle du microcrédit", "téléphone stylisé au centre, institution à gauche", "plein écran", "fixe", "aller-retour de pièces stylisées",
   "Montrer l'intention initiale : le cycle prêt / remboursement.", "Illustration : mention ; pas de logo d'institution réelle.",
   "La boucle aller-retour dure toute la phrase sur le microcrédit.", mention="ILLUSTRATION", anim=["pièces stylisées en aller-retour"], effets=["tintement léger"])
sc("SEQ-03", [6], "carte", "graphique_explicatif", "Zoom de carte : de l'Afrique de l'Est jusqu'à Thika, au nord de Nairobi.",
   "localisation de Thika", "Thika marquée d'un point orange", "plan large puis serré", "camera_3d_simulee", "point pulsant sur Thika",
   "Situer précisément le test.", "Position exacte de Thika à vérifier sur fond cartographique libre (OpenStreetMap).",
   "Atterrissage du zoom sur « Thika ».", transition="raccord par le zoom", texte=["THIKA", "NAIROBI"], sources=["OpenStreetMap (ODbL, attribution requise)"],
   anim=["point pulsant"])
# SEQ-04 — Le détournement
sc("SEQ-04", [0, 1], "reconstitution", "reconstitution", "Silhouettes à contre-jour devant une boutique : un homme compte des billets reçus via son téléphone.",
   "usager anonyme", "silhouette à contre-jour, téléphone lumineux", "plan moyen", "fixe", "aucun",
   "Faire sentir l'écart entre le plan et la réalité observée.", "Reconstitution : mention ; silhouettes anonymes, aucun visage identifiable.",
   "Plan fixe, laisser respirer 0,5 s après « avec le plan ».", mention="RECONSTITUTION", ambiance="ambiance de fin de journée", recherche=["silhouette counting money phone backlight"])
sc("SEQ-04", [2], "carte", "graphique_explicatif", "Depuis Thika, de nombreux fils orange partent vers d'autres régions du Kenya.",
   "flux sortants", "Thika au centre, fils rayonnants", "plan large", "suivi_trace", "fils qui s'étirent sur des centaines de kilomètres",
   "Visualiser le détournement : l'argent prêté part ailleurs.", "Tracés illustratifs : pas de données de flux réelles.",
   "La caméra suit le fil le plus long.", anim=["fils rayonnants"], effets=["notifications qui se multiplient"])
sc("SEQ-04", [3, 4], "illustration", "illustration", "Illustration : un téléphone dessiné porte une petite sacoche de coursier.",
   "téléphone-coursier", "téléphone centré, sacoche orange", "plein écran", "fixe", "petite animation de marche",
   "Image mémorable de la métaphore du coursier, puis de la décision de suivre l'usage.", "Illustration : mention.",
   "L'illustration se fige sur « décide de le suivre ».", mention="ILLUSTRATION", anim=["marche en boucle"], effets=["pas légers"])
sc("SEQ-04", [5], "typographie_animee", "graphique_explicatif", "Le schéma « prêt → remboursement » se transforme en « téléphone → téléphone ».",
   "nouvelle fonction", "deux icônes de téléphone reliées par le fil", "plein écran", "fixe", "morphing des icônes",
   "Montrer le pivot du produit.", "Aucun.", "Morphing calé sur « d'un téléphone à un autre ».", texte=["PRÊT → REMBOURSEMENT", "TÉLÉPHONE → TÉLÉPHONE"], anim=["morphing"])
sc("SEQ-04", [6, 7], "graphique", "graphique_explicatif", "Deux barres : 41 % des transferts vers des parents, 8 % vers des enfants ; une flèche remonte vers une maison.",
   "destinataires des transferts", "deux barres côte à côte, icône de maison", "plein écran", "fixe", "barres puis flèche",
   "Donner une preuve chiffrée du besoin, attribuée.", "Données d'enquête 2008 : légender la période.",
   "Flèche vers la maison sur « maison familiale ».", texte=["41 % VERS DES PARENTS", "8 % VERS DES ENFANTS", "SOURCE : SURI & JACK, VIA MIT NEWS (2010)"], anim=["barres", "flèche"])
# SEQ-05 — Une banque sans agences
sc("SEQ-05", [0, 1], "photo_lieu", "authentique", "Photo réelle d'un kiosque d'agent d'argent mobile au Kenya, enseigne visible.",
   "kiosque d'agent", "kiosque au centre, rue autour", "plan moyen", "parallaxe", "aucun",
   "Présenter la figure centrale du mécanisme : l'agent.", "Photo réelle sourcée ; ne pas dater de 2007 une photo récente.",
   "Parallaxe légère (avant-plan / arrière-plan détourés).", sources=[COMMONS, PRESSE], recherche=["M-Pesa agent kiosk Kenya photo"], texte=["Photo : source et date à préciser"],
   ambiance="ambiance de rue réelle")
sc("SEQ-05", [2, 3], "animation", "illustration", "Animation pas à pas : billets déposés au comptoir → SMS → montant qui s'inscrit dans une carte SIM stylisée.",
   "conversion espèces → monnaie électronique", "trois étapes de gauche à droite", "plein écran", "fixe", "la carte SIM se remplit d'orange",
   "Expliquer le mécanisme simplement.", "Illustration : mention ; ne pas inventer de montant.",
   "Une étape par membre de phrase.", mention="ILLUSTRATION", anim=["billets", "bulles SMS", "remplissage de la SIM"], effets=["bip de SMS"])
sc("SEQ-05", [4, 5], "carte", "graphique_explicatif", "Le fil orange part de la SIM, traverse la carte et arrive dans une boutique d'un autre quartier.",
   "transfert et retrait", "deux points reliés par le fil", "plan large", "suivi_trace", "le fil arrive et éclate en billets",
   "Compléter le parcours de l'argent jusqu'au retrait.", "Tracé illustratif.", "Raccord par le fil depuis la scène précédente.",
   transition="raccord par le fil orange", anim=["fil orange", "billets à l'arrivée"])
sc("SEQ-05", [6], "reconstitution", "reconstitution", "Une petite boutique de quartier : étagères de marchandises, le commerçant manipule un téléphone et un carnet.",
   "commerçant-agent", "commerçant au tiers droit, étagères au fond", "plan moyen", "travelling", "aucun",
   "Montrer que les agents étaient d'abord des commerçants.", "Reconstitution : mention ; ne pas reproduire une enseigne réelle.",
   "Travelling latéral le long des étagères.", mention="RECONSTITUTION", ambiance="ambiance de boutique", recherche=["small shop Kenya shelves stock video"])
sc("SEQ-05", [7], "comparaison", "graphique_explicatif", "Comparaison visuelle : 30 000 points (nuage de points orange) contre 400 agences (quelques carrés gris).",
   "agents vs agences", "deux nuages côte à côte", "plein écran", "fixe", "les points apparaissent par vagues",
   "Rendre sensible l'écart de réseau.", "Chiffres de source unique (Agence Ecofin) : source affichée.",
   "Dernière vague de points sur « 400 agences bancaires ».", texte=["≈ 30 000 POINTS M-PESA", "400 AGENCES BANCAIRES", "DÉBUT 2012 — SOURCE : AGENCE ECOFIN"], anim=["nuage de points"])
# SEQ-06 — Banques inquiètes, régulateur exigeant
sc("SEQ-06", [0], "plan_ambiance", "symbolique", "Tours de bureaux d'un quartier d'affaires, de nuit.",
   "quartier d'affaires", "verticales des tours", "plan large", "plongee", "aucun",
   "Installer le monde des institutions financières.", "Image symbolique : mention ; aucune banque identifiable.",
   "Coupe franche, changement d'ambiance.", mention="IMAGE D'ILLUSTRATION", ambiance="nappe tendue", recherche=["Nairobi business district night stock"])
sc("SEQ-06", [1], "document", "authentique", "Capture de l'article d'Agence Ecofin, phrase sur l'« incursion » des opérateurs surlignée.",
   "article Agence Ecofin", "page en biais", "plan rapproché", "insert_detail", "surlignage",
   "Attribuer clairement la position des banques à la source.", "Citation courte ; titre et date de l'article visibles.",
   "Surlignage sur « incursion ».", sources=["https://www.agenceecofin.com/banque/0604-10050-paiement-mobile-la-lecon-kenyane-au-monde (capture)"],
   texte=["SOURCE : AGENCE ECOFIN"], anim=["surlignage orange"])
sc("SEQ-06", [2], "photo_lieu", "authentique", "Façade de la Banque centrale du Kenya à Nairobi.",
   "Banque centrale du Kenya", "façade centrée, ciel dégagé", "plan large", "panoramique", "aucun",
   "Introduire l'arbitre réglementaire.", "Photo réelle sourcée ; vérifier qu'il s'agit bien du siège.",
   "Panoramique vertical court.", sources=[COMMONS], recherche=["Central Bank of Kenya building Nairobi photo"], texte=["BANQUE CENTRALE DU KENYA"])
sc("SEQ-06", [3], "infographie", "graphique_explicatif", "Trois conditions apparaissent en liste : plafond de dépôt, protection des consommateurs, sécurité des points de retrait.",
   "conditions du régulateur", "liste verticale, icônes simples", "plein écran", "fixe", "apparition successive",
   "Rendre lisibles les garde-fous.", "Formulation fidèle à la source.", "Une ligne par condition dite.",
   texte=["PLAFOND DE DÉPÔT", "PROTECTION DES CONSOMMATEURS", "SÉCURITÉ DES POINTS DE RETRAIT", "SOURCE : AGENCE ECOFIN"], anim=["apparition ligne par ligne"])
sc("SEQ-06", [4], "zoom_detail", "illustration", "Gros plan d'un formulaire d'enregistrement générique, une case cochée.",
   "enregistrement des clients", "formulaire en diagonale", "insert", "insert_detail", "case qui se coche",
   "Conclure sur l'obligation d'enregistrement.", "Illustration : mention ; formulaire générique, pas un vrai document.",
   "Le coche tombe sur « enregistré ».", mention="ILLUSTRATION", effets=["tampon"], texte=["SOURCE : VODAFONE"])
# SEQ-07 — La croissance, selon l'entreprise
sc("SEQ-07", [0], "typographie_animee", "graphique_explicatif", "La date « 6 MARS 2007 » se pose en grand, Archivo Black.",
   "date de lancement", "date centrée", "plein écran", "fixe", "les chiffres tombent un à un",
   "Marquer le lancement.", "Aucun.", "Impact sonore sur la date.", texte=["6 MARS 2007"], anim=["chiffres qui tombent"], effets=["impact sourd"])
sc("SEQ-07", [1], "graphique", "graphique_explicatif", "Compteur qui monte jusqu'à 1,2 million d'utilisateurs.",
   "première année", "compteur centré", "plein écran", "fixe", "compteur",
   "Première mesure de l'adoption, attribuée.", "Chiffre de l'entreprise : mention « chiffres de l'entreprise ».",
   "Fin du compteur sur « première année ».", texte=["1,2 MILLION", "SOURCE : VODAFONE — CHIFFRES DE L'ENTREPRISE"], anim=["compteur"])
sc("SEQ-07", [2], "carte", "graphique_explicatif", "Carte de l'Afrique et au-delà : les pays M-Pesa de 2016 s'allument un à un.",
   "expansion 2016", "carte du monde recentrée sur l'Afrique", "plan large", "camera_3d_simulee", "pays qui s'allument",
   "Montrer l'échelle internationale annoncée par l'entreprise.", "Liste des pays telle que publiée par Vodafone (2016) ; chiffres de l'entreprise.",
   "Allumage synchronisé avec l'énoncé des chiffres.", texte=["29,5 MILLIONS DE CLIENTS ACTIFS", "287 400 AGENTS", "10 PAYS", "SOURCE : VODAFONE (2016)"], anim=["pays qui s'allument"])
sc("SEQ-07", [3], "zoom_detail", "graphique_explicatif", "Zoom sur la RDC qui pulse en orange sur la carte.",
   "RDC", "RDC au centre", "plan serré", "insert_detail", "pulsation",
   "Créer le lien avec l'audience de LUKOJI.", "Ne pas suggérer une part de marché en RDC (non documentée).",
   "Pulsation sur « République démocratique du Congo ».", texte=["RÉPUBLIQUE DÉMOCRATIQUE DU CONGO"], anim=["pulsation orange"])
sc("SEQ-07", [4], "graphique", "graphique_explicatif", "Deux colonnes : 2016 et 2022 ; clients et agents augmentent.",
   "croissance 2016-2022", "deux colonnes côte à côte", "plein écran", "fixe", "colonnes qui montent",
   "Comparer deux points d'étape fournis par l'entreprise.", "Le nombre de pays baisse (10 → 7) : ne pas le masquer.",
   "Afficher « 7 PAYS » en même temps que la voix.", texte=["2022 : 51 MILLIONS DE CLIENTS", "600 000 AGENTS", "7 PAYS", "SOURCE : VODAFONE (2022)"], anim=["colonnes"])
sc("SEQ-07", [5, 6, 7], "typographie_animee", "graphique_explicatif", "Le mot « SOURCE : VODAFONE » grossit puis se transforme en point d'interrogation.",
   "recul critique", "texte centré", "plein écran", "fixe", "transformation du texte",
   "Signaler explicitement les limites d'une source intéressée.", "Aucun.", "Silence d'une demi-seconde avant la séquence suivante.",
   texte=["CHIFFRES DE L'ENTREPRISE", "ET DANS LA VIE DES GENS ?"], anim=["morphing en point d'interrogation"], transition="coupe franche + demi-seconde de silence")
# SEQ-08 — Ce que mesurent les chercheurs
sc("SEQ-08", [0, 1], "document", "authentique", "Couverture du rapport d'enquête FinAccess / page de l'article qui le cite, surlignage du titre.",
   "enquête FSD Kenya / Banque centrale", "document en biais", "plan rapproché", "insert_detail", "surlignage",
   "Introduire la première mesure, avec sa source.", "Le rapport original n'a pas été consulté : montrer l'article d'Agence Ecofin qui le cite, et le dire.",
   "Surlignage sur « une première réponse ».", sources=["https://www.agenceecofin.com/hebdop3/0611-70837-les-kenyans-dans-la-spirale-du-credit-sur-mobile (capture)"],
   texte=["SOURCE : FSD KENYA / BANQUE CENTRALE, CITÉS PAR AGENCE ECOFIN"])
sc("SEQ-08", [2], "graphique", "graphique_explicatif", "Courbe de 27 % (2006) à 83 % (2019).",
   "inclusion financière", "courbe montante, deux points annotés", "plein écran", "fixe", "la courbe se trace",
   "Montrer l'évolution sur la période.", "Deux points seulement : ne pas inventer de points intermédiaires (relier par une ligne droite).",
   "Tracé synchronisé avec les deux dates.", texte=["2006 : 27 %", "2019 : 83 %"], anim=["tracé de courbe"])
sc("SEQ-08", [3], "typographie_animee", "graphique_explicatif", "Sur la courbe, l'étiquette « PART DE M-PESA ? » apparaît.",
   "limite de la corrélation", "étiquette sur la courbe", "plein écran", "fixe", "apparition de l'étiquette",
   "Marquer la différence entre corrélation et causalité.", "Aucun.", "Coupe franche.", texte=["PART DE M-PESA ?"], anim=["apparition"])
sc("SEQ-08", [4], "carte", "graphique_explicatif", "Carte locale : autour d'un ménage, des points d'agents apparaissent dans un rayon d'un kilomètre.",
   "méthode de l'étude", "ménage au centre, cercle d'un kilomètre", "plan serré", "fixe", "points qui apparaissent dans le cercle",
   "Expliquer la méthode (densité d'agents).", "Schéma illustratif de la méthode, pas des données réelles.",
   "Points qui apparaissent un à un.", texte=["RAYON : 1 KM"], anim=["cercle", "points"])
sc("SEQ-08", [5], "document", "authentique", "Capture de l'article de MIT News qui présente l'étude publiée dans Science.",
   "compte rendu MIT News", "page en biais", "plan rapproché", "insert_detail", "surlignage du titre",
   "Montrer la source réellement consultée (et non l'article original).", "Dire à l'écran qu'il s'agit du compte rendu du MIT.",
   "Surlignage sur « Science ».", sources=["https://news.mit.edu/2016/mobile-money-kenyans-out-poverty-1208 (capture)"], texte=["COMPTE RENDU : MIT NEWS (2016)"])
sc("SEQ-08", [6, 7], "typographie_animee", "graphique_explicatif", "Le nombre « 194 000 MÉNAGES » s'affiche puis se transforme en « ≈ 2 % ».",
   "estimation principale", "chiffre centré", "plein écran", "fixe", "transformation du chiffre",
   "Donner le résultat principal sans exagérer.", "Estimation : le mot « ESTIMATION » reste visible.",
   "Transformation sur « à peu près 2 % ».", texte=["194 000 MÉNAGES (ESTIMATION)", "≈ 2 % DES MÉNAGES KÉNYANS", "SOURCE : SURI & JACK, SCIENCE (2016), VIA MIT NEWS"], anim=["morphing du chiffre"])
sc("SEQ-08", [8, 9], "archive_photo", "authentique", "Photographie d'une commerçante kényane tenant son téléphone dans sa boutique.",
   "commerçante", "personne au tiers gauche, boutique autour", "plan moyen", "zoom_avant_lent", "chiffre en surimpression",
   "Incarner le résultat sur les femmes cheffes de famille.", "Photo réelle avec consentement/licence ; ne pas présenter la personne comme bénéficiaire de l'étude.",
   "Zoom avant lent, 5 s maximum.", sources=[COMMONS, PRESSE], recherche=["Kenyan woman shopkeeper mobile phone photo"],
   texte=["≈ 185 000 FEMMES", "SOURCE : SURI & JACK, VIA MIT NEWS"], ambiance="ambiance de boutique")
sc("SEQ-08", [10, 11], "typographie_animee", "graphique_explicatif", "Le mot « ESTIMATION » en grand, puis « ≠ DÉCOMPTE ».",
   "nature des chiffres", "texte centré", "plein écran", "fixe", "barre de différence",
   "Insister sur la prudence méthodologique.", "Aucun.", "Coupe nette en fin de phrase.", texte=["ESTIMATION", "≠ DÉCOMPTE"], anim=["apparition"])
# SEQ-09 — Le revers du succès
sc("SEQ-09", [0], "plan_ambiance", "symbolique", "Écran noir, puis le fil orange se tend et se met à vibrer.",
   "rupture de ton", "fil horizontal au centre", "plein écran", "fixe", "le fil se tend",
   "Rupture : passer du succès aux limites.", "Image abstraite : pas de risque de confusion.", "Silence d'une seconde avant la voix.",
   mention="IMAGE D'ILLUSTRATION", anim=["fil tendu qui vibre"], effets=["corde tendue"], transition="coupe franche après une seconde de noir", duree=3.0)
sc("SEQ-09", [1], "graphique", "graphique_explicatif", "Jauge des frais qui monte jusqu'à 7 % du montant envoyé.",
   "coût des transferts", "jauge centrée", "plein écran", "fixe", "la jauge se remplit",
   "Montrer le coût pour les usagers.", "« Certains transferts » : ne pas présenter 7 % comme un coût moyen.",
   "Remplissage sur « 7 % ».", texte=["JUSQU'À 7 % DU MONTANT (CERTAINS TRANSFERTS)", "SOURCE : AGENCE ECOFIN"], anim=["jauge"])
sc("SEQ-09", [2], "infographie", "graphique_explicatif", "Flèche descendante : de 23 à 10 shillings par transaction, objectif 2028.",
   "objectif du régulateur", "flèche diagonale descendante", "plein écran", "fixe", "la flèche descend",
   "Montrer la réponse annoncée du régulateur.", "Projet de plafonnement : afficher « PROJET », pas « EN VIGUEUR ».",
   "Flèche qui atterrit sur « 2028 ».", texte=["23 → 10 SHILLINGS PAR TRANSACTION", "OBJECTIF 2028 (PROJET) — SOURCE : AGENCE ECOFIN"], anim=["flèche descendante"])
sc("SEQ-09", [3, 4], "graphique", "graphique_explicatif", "Camembert : 90,8 % de parts de marché.",
   "part de marché", "camembert centré", "plein écran", "fixe", "le secteur orange occupe le cercle",
   "Rendre visible la domination.", "Date de la donnée (31 mars 2025) affichée.", "Remplissage synchronisé avec « 90,8 % ».",
   texte=["90,8 % DE PARTS DE MARCHÉ", "31 MARS 2025 — SOURCE : AUTORITÉ DES COMMUNICATIONS, VIA AGENCE ECOFIN"], anim=["camembert"])
sc("SEQ-09", [5], "infographie", "graphique_explicatif", "Barre empilée des revenus de Safaricom : 44,2 % pour M-Pesa.",
   "poids dans les revenus", "barre horizontale", "plein écran", "fixe", "remplissage",
   "Montrer la dépendance de l'opérateur à M-Pesa.", "Exercice 2025 précisé.", "Remplissage sur « 44,2 % ».",
   texte=["44,2 % DES REVENUS DE SAFARICOM", "EXERCICE 2025 — SOURCE : AGENCE ECOFIN"], anim=["barre empilée"])
sc("SEQ-09", [6], "document", "authentique", "Capture de l'article d'Agence Ecofin sur la menace des sénateurs (2018).",
   "article sénateurs", "page en biais", "plan rapproché", "insert_detail", "surlignage",
   "Documenter la critique politique.", "Article de 2018 : date visible ; la menace n'a pas été suivie d'effet à notre connaissance (non vérifié).",
   "Surlignage sur « séparer ».", sources=["https://www.agenceecofin.com/regulation/1811-82596-kenya-les-senateurs-menacent-a-nouveau-de-separer-les-activites-telecoms-et-m-pesa-chez-safaricom (capture)"],
   texte=["2018 — SOURCE : AGENCE ECOFIN"])
sc("SEQ-09", [7, 8], "image_symbolique", "symbolique", "Écran de téléphone flou montrant une interface de paris sportifs générique.",
   "paris en ligne", "téléphone en main, écran flou", "insert", "insert_detail", "aucun",
   "Illustrer un usage préoccupant.", "Image symbolique : mention ; aucune marque de pari identifiable.",
   "Flou permanent sur l'interface.", mention="IMAGE D'ILLUSTRATION", texte=["SOURCE : AGENCE ECOFIN"], recherche=["phone sports betting app blurred stock"])
sc("SEQ-09", [9], "plan_ambiance", "symbolique", "Main qui fait défiler des notifications de crédit sur un téléphone, de nuit.",
   "crédit mobile", "téléphone éclairant la main", "plan rapproché", "fixe", "aucun",
   "Évoquer la question du crédit et de la protection des plus pauvres.", "Image symbolique : mention ; pas de vraie marque de crédit.",
   "Plan fixe, 5 s.", mention="IMAGE D'ILLUSTRATION", ambiance="nappe sombre")
sc("SEQ-09", [10], "document", "authentique", "Capture de l'article de la Revue de la régulation (OpenEdition), titre et phrase clé surlignés.",
   "thèse critique", "page en biais", "plan rapproché", "insert_detail", "surlignage",
   "Donner la parole à la critique académique.", "Opinion attribuée : afficher « ANALYSE CRITIQUE — THÈSE ».",
   "Surlignage sur « causes profondes ».", sources=["https://journals.openedition.org/regulation/15139 (capture)"], texte=["ANALYSE CRITIQUE — REVUE DE LA RÉGULATION"])
# SEQ-10 — Conclusion
sc("SEQ-10", [0, 1], "comparaison", "graphique_explicatif", "Trois objets simples côte à côte : téléphone à clavier, bulle SMS, petite boutique — tous en gris.",
   "briques existantes", "trois icônes alignées", "plein écran", "fixe", "les trois icônes se rapprochent",
   "Montrer que l'innovation tenait à l'assemblage, pas à une technologie nouvelle.", "Aucun.", "Rapprochement des icônes sur « existaient déjà ».",
   anim=["rapprochement des icônes"])
sc("SEQ-10", [2], "carte", "graphique_explicatif", "Le fil orange relie de nouveau les points de la carte, plus dense qu'au début.",
   "usage suivi", "carte du Kenya, fils denses", "plan large", "camera_3d_simulee", "le fil se densifie",
   "Faire écho à l'ouverture : l'usage a dessiné le réseau.", "Tracé illustratif.", "Raccord avec la scène d'ouverture (même cadrage).",
   transition="raccord par le fil orange", anim=["densification des fils"])
sc("SEQ-10", [3, 4], "infographie", "graphique_explicatif", "Le réseau de fils se transforme en colonnes d'un bâtiment ; trois mots apparaissent : RÈGLES, CONTRE-POUVOIRS, PRIX.",
   "infrastructure", "colonnes au centre, mots à droite", "plein écran", "fixe", "morphing fils → colonnes",
   "Rendre visible l'idée d'infrastructure à encadrer.", "Aucun.", "Un mot par énumération.", texte=["RÈGLES", "CONTRE-POUVOIRS", "PRIX SURVEILLÉS"], anim=["morphing"])
sc("SEQ-10", [5], "carte", "graphique_explicatif", "La carte glisse du Kenya vers la RDC, qui s'éclaire.",
   "RDC", "RDC au centre", "plan large", "panoramique", "la RDC s'éclaire",
   "Ramener le propos vers l'audience de LUKOJI.", "Présence de M-Pesa en RDC selon Vodafone : source affichée.",
   "Panoramique sur « Congo ».", texte=["RÉPUBLIQUE DÉMOCRATIQUE DU CONGO", "SOURCE : VODAFONE"], anim=["éclairage progressif"])
sc("SEQ-10", [6, 7], "plan_ambiance", "symbolique", "Rue de Kinshasa au crépuscule, enseignes d'argent mobile ; fondu au noir.",
   "question ouverte", "rue en perspective", "plan large", "travelling", "fondu au noir puis signature LUKOJI",
   "Terminer sur une question ouverte, ancrée chez l'audience.", "Image d'illustration de Kinshasa : mention ; ne pas suggérer que M-Pesa y est dominant.",
   "Fondu au noir sur « au profit de qui », puis signature LUKOJI (préréglage documentaire).", mention="IMAGE D'ILLUSTRATION",
   recherche=["Kinshasa street dusk mobile money signs"], ambiance="ambiance de rue réelle, nappe qui s'éteint", transition="fondu au noir + signature LUKOJI")
json.dump({"scenes": scenes}, open("research/stories/mpesa/storyboard.json", "w"), ensure_ascii=False, indent=1)
print(len(scenes), "scènes")
