# Storyboard v2.6.2 — fiche de réalisation

Construit à partir du script v21 et de la structure v6 **verrouillés**. Statut : `storyboard_draft` (non validé).

## SEQ-01 — Jours de voyage, quelques SMS

*Musique : aucune musique : ambiance réelle puis silence ; la musique n'entre qu'après le titre*

### SC-01 · 0.0–6.0 s (6.0 s) · illustration · illustration (carte + dessin au trait LUKOJI, non générée) · mention « ILLUSTRATION »

- **Narration** : Pour envoyer de l'argent à sa famille, au Kenya, on pouvait voyager pendant des jours.
- **Objectif / rythme** : Établir le contexte géographique et la longueur du trajet, par une image clairement illustrative. · ouverture, tension douce
- **Visuel** : Carte du Kenya (aplats #555555 sur noir, frontières Natural Earth). Un tracé orange schématique part de Nairobi vers une région rurale non nommée ; un autocar dessiné au trait (silhouette blanc cassé, sans logo, sans inscription, aucune personne visible) avance lentement le long du tracé.
- **Composition / cadrage** : carte légèrement décentrée à droite ; tracé en diagonale ; autocar petit dans le cadre · plan large
- **Mouvement** : caméra fixe · graphique : l'autocar avance le long du tracé pendant toute la phrase (mouvement unique, lent)
- **Texte à l'écran** : KENYA / SOURCE DU RÉCIT : VODAFONE (2017)
- **Source visuelle** : R20, R22 (a_produire)
- **Source factuelle** : F61
- **Remplacement** : Carte seule avec le tracé (sans autocar).
- **Transitions** : entrée ouverture au noir (0,5 s) · sortie coupe franche
- **Son** : vent et route lointaine, très bas (Freesound, CC0)
- **Difficulté / méthode** : moyenne · Inkscape (dessin) + DaVinci Resolve/Fusion ou Blender (animation 2D), outils gratuits
- **Montage** : Carte maîtresse, état 0/4 (ouverture). Le tracé n'est pas le fil de l'argent : pas de raccord avec SC-14.
- **Risques** : Illustration : mention à l'écran ; aucune personne, aucune marque ; ne suggère aucune date précise.
- **Motion design** : comprendre : envoyer de l'argent supposait un long trajet par la route · éléments : carte du Kenya, tracé orange, autocar au trait · mouvement : déplacement linéaire, sans rebond · durée : 6 s · entrée : ouverture au noir · sortie : l'autocar sort du cadre · style : trait blanc cassé, tracé orange (pas encore le « fil de l'argent ») · contraintes : aucune ville de destination nommée, aucun compteur de jours · assets : Natural Earth (R20), dessin vectoriel Inkscape (R22)

### SC-02 · 6.0–10.4 s (4.4 s) · document · authentique (capture d'un document cité)

- **Narration** : Ou confier son argent à une compagnie de bus, et attendre.
- **Objectif / rythme** : Montrer la source réelle de la pratique : l'enquête nationale FinAccess 2006. · preuve discrète
- **Visuel** : Extrait du tableau 8.5 du rapport FinAccess 2006 : la ligne « Through a bus or matatu company » soulignée en orange, le reste du tableau assombri.
- **Composition / cadrage** : ligne du tableau au centre, titre du rapport en haut à gauche · plan serré sur l'extrait
- **Mouvement** : caméra fixe · graphique : trait orange fixe sous l'extrait
- **Texte à l'écran** : FINACCESS 2006 · ENQUÊTE NATIONALE · TABLEAU 8.5
- **Source visuelle** : R26 (a_capturer)
- **Source factuelle** : F72, F73
- **Remplacement** : Typographie seule : « ENVOI PAR UNE COMPAGNIE DE BUS OU DE MATATU — FINACCESS 2006 ».
- **Transitions** : entrée coupe franche · sortie coupe sèche au noir
- **Son** : la rumeur de rue se coupe sur « attendre »
- **Difficulté / méthode** : faible · capture d'écran haute définition de la page, fond #0B0B0B, extrait court, URL et date de consultation à l'écran
- **Montage** : Couper l'ambiance exactement sur « attendre » : une demi-seconde de silence.
- **Risques** : Le tableau porte sur les 12 mois précédant l'enquête de 2006 : ne pas afficher de pourcentage sans sa base.

### SC-03 · 10.4–13.0 s (2.6 s) · reconstitution · reconstitution (insert filmé sur table) · mention « RECONSTITUTION »

- **Narration** : Aujourd'hui, quelques SMS suffisent.
- **Objectif / rythme** : Rupture : des jours de voyage contre quelques SMS. · rupture, accélération
- **Visuel** : Insert très serré : un téléphone à clavier posé sur une table de bois reçoit un SMS ; l'écran affiche un texte générique (« Vous avez reçu… »), sans marque ni numéro réel.
- **Composition / cadrage** : écran au tiers gauche, profondeur de champ courte · insert très serré
- **Mouvement** : caméra insert_detail · graphique : aucun
- **Texte à l'écran** : —
- **Source visuelle** : R22 (a_produire)
- **Source factuelle** : F43
- **Remplacement** : Illustration au trait : bulle de SMS orange sur fond noir (mention ILLUSTRATION).
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : silence de pièce · effets : vibration du téléphone, bip unique (signature sonore 1/3)
- **Difficulté / méthode** : moyenne · tournage LUKOJI sur table (téléphone basique, mains), lumière douce ; aucun visage, aucune marque, texte de SMS générique
- **Montage** : Le bip tombe sur « SMS ».
- **Risques** : Ne reproduire aucune interface réelle de M-Pesa ou de Safaricom.

### SC-04 · 13.0–19.2 s (6.2 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Le service s'appelle M-Pesa. Et ses concepteurs ne l'avaient pas inventé pour ça.
- **Objectif / rythme** : Nommer le sujet et laisser la question ouverte. · révélation du sujet, puis question suspendue
- **Visuel** : Sur noir, « M-PESA » s'écrit en Archivo Black blanc ; la dernière phrase est dite sur le noir ; le titre de travail apparaît ensuite en IBM Plex Mono.
- **Composition / cadrage** : nom centré, titre en bas · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition lettre à lettre (12 images), sans rebond
- **Texte à l'écran** : M-PESA / QUAND LES CLIENTS ONT CHANGÉ LE PRODUIT
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : —
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie carton « KENYA · 2006 » en coupe franche
- **Son** : silence
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : Une seconde de noir après « pour ça », avant le carton.
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : le nom du service, puis le titre du film · éléments : deux lignes de texte · mouvement : apparition sèche, maintien, disparition · durée : 4 s + 1 s de noir · entrée : sur « s'appelle M-Pesa » · sortie : 1 s après « pour ça » · style : éditorial sobre · contraintes : lisible en 9:16 recadré · assets : polices de brand/fonts

## SEQ-02 — Hors des banques

*Musique : nappe grave, sobre, tempo lent (piano préparé ou cordes basses), très en retrait*

### SC-05 · 19.8–27.4 s (7.6 s) · carte · graphique éditorial (création LUKOJI)

- **Narration** : Au milieu des années deux mille, la distance n'est pas le seul obstacle. Une enquête nationale, FinAccess, le mesure.
- **Objectif / rythme** : Poser le territoire et annoncer la mesure. · installation
- **Visuel** : Retour de la carte du Kenya (aplats #555555 sur noir), sans tracé ; Nairobi seule nommée ; carton « 2006 » en haut à droite.
- **Composition / cadrage** : pays centré, légèrement à droite pour laisser la place aux chiffres · plan large
- **Mouvement** : caméra fixe · graphique : fondu d'entrée de la carte (8 images)
- **Texte à l'écran** : KENYA / NAIROBI / 2006
- **Source visuelle** : R20 (a_produire)
- **Source factuelle** : —
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : nappe grave
- **Difficulté / méthode** : moyenne · After Effects ou équivalent libre (Blender 2D, Natron) ; fond de carte Natural Earth (domaine public), projection simple
- **Montage** : Carte maîtresse, état 1/4 (déjà vue en ouverture, SC-01).
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : où se passe l'histoire · éléments : frontières, Nairobi · mouvement : apparition · durée : 6 s · entrée : sur « Au milieu des années deux mille » · sortie : coupe vers le graphique · style : aplats, sans relief · contraintes : frontières exactes · assets : Natural Earth 1:10m

### SC-06 · 27.4–36.2 s (8.8 s) · graphique · graphique éditorial (création LUKOJI)

- **Narration** : En 2006, seuls 26,7 % des adultes kényans utilisent un service financier formel, comme une banque ou une assurance.
- **Objectif / rythme** : Donner le chiffre antérieur au lancement, avec son périmètre exact. · information clé
- **Visuel** : Barre unique, échelle 0-100 % : 26,7 % en jaune. Sous la barre : « ADULTES · SERVICE FINANCIER FORMEL ».
- **Composition / cadrage** : barre à gauche, valeur en Archivo Black jaune, légende en Plex Mono · plein cadre
- **Mouvement** : caméra fixe · graphique : la barre monte jusqu'à 26,7 %
- **Texte à l'écran** : 26,7 % / ADULTES UTILISANT UN SERVICE FINANCIER FORMEL · 2006 / SOURCE : FINACCESS (CBK · KNBS · FSD KENYA), SÉRIE 2019
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F74
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : nappe grave
- **Difficulté / méthode** : faible · gabarit unique LUKOJI (Archivo Black / IBM Plex Mono)
- **Montage** : Conserver le fichier projet : la même barre reviendra en SEQ-08.
- **Risques** : Ne pas écrire « bancarisés » : la définition inclut assurances, coopératives et microfinance.
- **Motion design** : comprendre : un quart des adultes seulement utilise la finance formelle en 2006 · éléments : une barre, une valeur, une légende · mouvement : montée linéaire 1 s · durée : 8 s · entrée : sur « En 2006 » · sortie : figée, puis coupe · style : gabarit chiffres LUKOJI · contraintes : même objet et même échelle qu'en SEQ-08 · assets : gabarit graphique unique

### SC-07 · 36.2–48.2 s (12.0 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Ce manque intéresse un acteur venu de loin : le ministère britannique du Développement international. Il cherche des entreprises capables d'inventer des services pour les personnes qui n'ont pas de compte.
- **Objectif / rythme** : Introduire le financeur et son objectif. · progression
- **Visuel** : Sur noir, le nom du ministère en IBM Plex Mono, puis son objectif en une ligne : « des services pour les personnes sans compte ».
- **Composition / cadrage** : texte centré, deux lignes · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition ligne à ligne
- **Texte à l'écran** : MINISTÈRE BRITANNIQUE DU DÉVELOPPEMENT INTERNATIONAL (DFID) / OBJECTIF : DES SERVICES POUR LES PERSONNES SANS COMPTE
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F41
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : nappe grave
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : Pas de drapeau ni de carte de Londres.
- **Risques** : Aucun risque particulier identifié.

### SC-08 · 48.2–51.8 s (3.6 s) · document · authentique (capture d'un document cité)

- **Narration** : Selon Vodafone, l'entreprise saisit l'occasion et obtient une subvention.
- **Objectif / rythme** : Montrer le document qui mentionne la subvention. · preuve
- **Visuel** : Page Vodafone (2017) : trait orange sous « a grant from the Department for International Development in the UK… to help the unbanked » ; traduction courte en sous-titre.
- **Composition / cadrage** : paragraphe au centre, page assombrie autour · plan serré sur l'extrait
- **Mouvement** : caméra fixe · graphique : trait orange fixe sous l'extrait
- **Texte à l'écran** : SOURCE : VODAFONE (2017) · RÉCIT DE L'ENTREPRISE
- **Source visuelle** : R12 (a_capturer)
- **Source factuelle** : F41
- **Remplacement** : Typographie : nom du ministère + phrase source.
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : nappe grave
- **Difficulté / méthode** : faible · capture d'écran haute définition de la page, fond #0B0B0B, extrait court, URL et date de consultation à l'écran
- **Montage** : Tenir 2 s sur la phrase soulignée.
- **Risques** : Source intéressée : la légende le dit.

## SEQ-03 — Le prototype de Thika

*Musique : même nappe, une note répétée qui installe l'attente*

### SC-09 · 52.4–56.0 s (3.6 s) · carte · graphique éditorial (création LUKOJI)

- **Narration** : Au Kenya, le projet se monte avec l'opérateur Safaricom.
- **Objectif / rythme** : Situer l'opérateur kényan. · progression
- **Visuel** : Retour sur la carte : Nairobi s'éclaire, étiquette « SAFARICOM · OPÉRATEUR KÉNYAN ».
- **Composition / cadrage** : Nairobi au centre-bas · plan large
- **Mouvement** : caméra fixe · graphique : halo bref sur Nairobi
- **Texte à l'écran** : SAFARICOM · OPÉRATEUR KÉNYAN
- **Source visuelle** : R20 (a_produire)
- **Source factuelle** : F42
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : nappe
- **Difficulté / méthode** : moyenne · After Effects ou équivalent libre (Blender 2D, Natron) ; fond de carte Natural Earth (domaine public), projection simple
- **Montage** : Carte maîtresse, état 2/4.
- **Risques** : Aucun logo de l'opérateur.

### SC-10 · 56.0–65.6 s (9.6 s) · document · authentique (capture d'un document cité)

- **Narration** : Ce qui suit, on le connaît surtout par ceux qui l'ont mené. Un article publié en 2007 par deux responsables du projet.
- **Objectif / rythme** : Dire d'où vient le récit des origines (1/2) : l'article de l'équipe projet. · ralentissement : moment de méthode
- **Visuel** : Page de titre de l'article de Hughes & Lonie (Innovations, MIT Press, 2007) ; trait orange sous le titre.
- **Composition / cadrage** : page à gauche, place libre à droite pour le document suivant · plan serré sur l'extrait
- **Mouvement** : caméra fixe · graphique : trait orange fixe sous l'extrait
- **Texte à l'écran** : HUGHES & LONIE · INNOVATIONS (MIT PRESS) · 2007 · ÉQUIPE DU PROJET
- **Source visuelle** : R29 (a_capturer)
- **Source factuelle** : F76
- **Remplacement** : Typographie : référence complète de l'article.
- **Transitions** : entrée coupe franche · sortie glissement latéral (split-screen)
- **Son** : nappe
- **Difficulté / méthode** : faible · capture d'écran haute définition de la page, fond #0B0B0B, extrait court, URL et date de consultation à l'écran
- **Montage** : Le document suivant entre à droite : les deux sources restent un instant côte à côte.
- **Risques** : Source liée à Vodafone : la légende dit « équipe du projet ».

### SC-11 · 65.6–72.8 s (7.2 s) · document · authentique (capture d'un document cité)

- **Narration** : Puis un texte de Michael Joseph, ancien directeur général de Safaricom, publié par Vodafone en 2017.
- **Objectif / rythme** : Dire d'où vient le récit (2/2) : le texte de Michael Joseph publié par Vodafone. · ralentissement
- **Visuel** : Page Vodafone (2017) recadrée sur la signature « Michael Joseph, Vodafone Group's Director of Mobile Money » ; la page de 2007 reste à gauche.
- **Composition / cadrage** : split-screen : 2007 à gauche, 2017 à droite · plan serré sur l'extrait
- **Mouvement** : caméra fixe · graphique : trait orange fixe sous l'extrait
- **Texte à l'écran** : MICHAEL JOSEPH · VODAFONE · 2017
- **Source visuelle** : R12 (a_capturer)
- **Source factuelle** : F62
- **Remplacement** : Typographie : nom, fonction, date et éditeur.
- **Transitions** : entrée glissement latéral · sortie coupe franche
- **Son** : nappe
- **Difficulté / méthode** : faible · capture d'écran haute définition de la page, fond #0B0B0B, extrait court, URL et date de consultation à l'écran
- **Montage** : Ne montrer aucune photo de Michael Joseph (aucune image libre identifiée).
- **Risques** : Ne pas suggérer qu'il a inventé seul le service.

### SC-12 · 72.8–85.2 s (12.4 s) · animation · illustration (dessin au trait LUKOJI, non générée) · mention « ILLUSTRATION »

- **Narration** : Selon ces récits, il ne s'agit pas, au départ, d'envoyer de l'argent. L'équipe travaille sur le microcrédit : verser de petits prêts par téléphone, et les faire rembourser de la même façon.
- **Objectif / rythme** : Révéler l'intention initiale : le microcrédit. · révélation
- **Visuel** : Animation au trait : une petite somme part d'une institution de microcrédit (bâtiment schématique, sans nom) vers un téléphone, puis revient en petits remboursements.
- **Composition / cadrage** : institution à gauche, téléphone à droite, trajet en arc · plan large
- **Mouvement** : caméra fixe · graphique : aller simple, puis trois petits retours
- **Texte à l'écran** : SELON L'ÉQUIPE PROJET ET VODAFONE
- **Source visuelle** : R22 (a_produire)
- **Source factuelle** : F8
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : nappe
- **Difficulté / méthode** : moyenne · dessin vectoriel au trait (noir, blanc cassé, orange) animé en 2D
- **Montage** : Deux boucles au maximum.
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : le prototype servait à verser et rembourser des microcrédits · éléments : bâtiment, téléphone, pièces stylisées · mouvement : trajet en arc, retours en pointillés · durée : 11 s · entrée : sur « L'équipe travaille sur le microcrédit » · sortie : la boucle se fige · style : trait orange sur noir · contraintes : aucun nom d'institution réelle · assets : illustrations vectorielles R22

### SC-13 · 85.2–93.2 s (8.0 s) · carte · graphique éditorial (création LUKOJI)

- **Narration** : Le prototype est testé à partir d'octobre 2005, à Nairobi et à Thika, au nord de la capitale.
- **Objectif / rythme** : Situer et dater le prototype. · précision
- **Visuel** : La carte se resserre sur la région de Nairobi : Nairobi et Thika apparaissent, date « OCTOBRE 2005 ».
- **Composition / cadrage** : deux points, Thika au nord · plan large
- **Mouvement** : caméra fixe · graphique : recadrage de carte (zoom 2D motivé : passer du pays à la région), 1,5 s
- **Texte à l'écran** : NAIROBI / THIKA / PILOTE · OCTOBRE 2005
- **Source visuelle** : R20 (a_produire)
- **Source factuelle** : F76
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : nappe
- **Difficulté / méthode** : moyenne · After Effects ou équivalent libre (Blender 2D, Natron) ; fond de carte Natural Earth (domaine public), projection simple
- **Montage** : Carte maîtresse, état 2/4 (détail).
- **Risques** : Ne pas ajouter le troisième lieu (Mathare) sans le dire : il n'est pas dans la voix off.
- **Motion design** : comprendre : où et quand le prototype est testé · éléments : deux points, une date · mouvement : recadrage unique · durée : 6 s · entrée : sur « Le prototype » · sortie : coupe · style : carte maîtresse · contraintes : positions exactes · assets : Natural Earth + coordonnées des villes

## SEQ-04 — Le détournement

*Musique : pulsation légère qui démarre avec les fils, coupée net avant la citation*

### SC-14 · 93.8–106.6 s (12.8 s) · carte · graphique éditorial (création LUKOJI)

- **Narration** : Sur le terrain, les clients font autre chose. D'après Michael Joseph, ceux qui reçoivent un prêt envoient l'argent à d'autres personnes, parfois à des centaines de kilomètres. Le portable devient un coursier.
- **Objectif / rythme** : Faire voir le détournement : l'argent part ailleurs. · accélération
- **Visuel** : Depuis la région de Nairobi, des fils orange partent vers plusieurs régions du Kenya (premier fil de l'argent).
- **Composition / cadrage** : origine au centre, fils vers les bords · plan large
- **Mouvement** : caméra suivi_trace · graphique : les fils s'étirent, accélèrent sur « coursier »
- **Texte à l'écran** : D'APRÈS MICHAEL JOSEPH (VODAFONE, 2017)
- **Source visuelle** : R20 (a_produire)
- **Source factuelle** : F8
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe au noir
- **Son** : pulsation légère
- **Difficulté / méthode** : moyenne · After Effects ou équivalent libre (Blender 2D, Natron) ; fond de carte Natural Earth (domaine public), projection simple
- **Montage** : Carte maîtresse, état 3/4 ; fil 1/3.
- **Risques** : Ne pas nommer de villes de destination (non sourcées).
- **Motion design** : comprendre : l'argent prêté circule vers d'autres personnes, loin · éléments : 5 à 7 fils orange · mouvement : tracés progressifs, vitesse croissante · durée : 11 s · entrée : sur « ceux qui reçoivent un prêt » · sortie : les fils se figent · style : fil de l'argent (1/3) · contraintes : destinations schématiques, non nommées · assets : carte maîtresse

### SC-15 · 106.6–113.8 s (7.2 s) · document · authentique (capture d'un document cité)

- **Narration** : Plutôt que de corriger cet usage, l'équipe décide de le suivre. « Alors nous avons pris un risque », raconte-t-il.
- **Objectif / rythme** : Le moment de décision, montré dans le document qui le rapporte. · tension, puis décision
- **Visuel** : Page Vodafone (2017) recadrée sur « So we took a chance, and re-engineered the loans system… » ; sous-titre : « Alors nous avons pris un risque ».
- **Composition / cadrage** : phrase au centre, page floutée · plan serré sur l'extrait
- **Mouvement** : caméra fixe · graphique : trait orange fixe sous l'extrait
- **Texte à l'écran** : « ALORS NOUS AVONS PRIS UN RISQUE » / MICHAEL JOSEPH · VODAFONE · 2017
- **Source visuelle** : R12 (a_capturer)
- **Source factuelle** : F63
- **Remplacement** : Typographie de la citation, original anglais dessous.
- **Transitions** : entrée coupe du noir · sortie coupe franche
- **Son** : silence d'une seconde avant la citation
- **Difficulté / méthode** : faible · capture d'écran haute définition de la page, fond #0B0B0B, extrait court, URL et date de consultation à l'écran
- **Montage** : La musique s'arrête avant « Alors » ; reprise sur le plan suivant.
- **Risques** : Citation traduite : original visible ; texte d'anniversaire de l'entreprise (2017), date affichée.

### SC-16 · 113.8–121.0 s (7.2 s) · infographie · graphique éditorial (création LUKOJI)

- **Narration** : Le système de prêts est reconstruit autour d'une seule fonction : envoyer de l'argent d'un téléphone à un autre.
- **Objectif / rythme** : Résumer la transformation du produit. · résolution
- **Visuel** : Le schéma « PRÊT → REMBOURSEMENT » se réécrit en « TÉLÉPHONE → TÉLÉPHONE ».
- **Composition / cadrage** : schéma centré · plein cadre
- **Mouvement** : caméra fixe · graphique : réécriture du schéma (pas de morphing d'icônes)
- **Texte à l'écran** : PRÊT → REMBOURSEMENT / TÉLÉPHONE → TÉLÉPHONE
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F9
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : pulsation reprise
- **Difficulté / méthode** : moyenne · motion design 2D, gabarit LUKOJI
- **Montage** : —
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : le produit change de fonction · éléments : deux lignes de texte, une flèche · mouvement : la première ligne s'efface, la seconde s'écrit · durée : 7 s · entrée : sur « reconstruit » · sortie : coupe · style : typographie éditoriale · contraintes : — · assets : gabarit

## SEQ-05 — Une banque sans agences

*Musique : motif léger et rythmé (percussions sèches), explicatif*

### SC-17 · 121.6–131.2 s (9.6 s) · photo_lieu · authentique (photo réelle, date inconnue)

- **Narration** : Reste un problème très concret : comment faire entrer des billets dans un téléphone, et les en faire sortir ? La réponse passe par des commerçants.
- **Objectif / rythme** : Montrer un vrai point d'argent mobile. · respiration, terrain
- **Visuel** : Kiosque M-Pesa au Kenya (R04) en plan serré sur le lettrage peint « M-PESA » du mur vert ; la boutique entière n'est montrée qu'en SC-21.
- **Composition / cadrage** : lettrage vertical au centre, mur vert plein cadre · plan serré
- **Mouvement** : caméra fixe · graphique : aucun
- **Texte à l'écran** : KENYA · DATE INCONNUE · PHOTO : REALT0N12 · CC BY-SA 3.0
- **Source visuelle** : R04 (contenu_inspecte)
- **Source factuelle** : F43
- **Remplacement** : Typographie « LA RÉPONSE : DES COMMERÇANTS » sur noir.
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : ambiance de rue (Freesound, CC0)
- **Difficulté / méthode** : faible · photo libre Wikimedia Commons, recadrage 16:9, légende lieu / date / auteur / licence
- **Montage** : Recadrage serré (le logo Safaricom hors cadre) ; image recadrée = adaptation sous CC BY-SA 3.0.
- **Risques** : Date inconnue : le dire ; ne jamais afficher la date des métadonnées.

### SC-18 · 131.2–134.0 s (2.8 s) · reconstitution · reconstitution (insert filmé sur table) · mention « RECONSTITUTION »

- **Narration** : Le client dépose ses espèces au comptoir.
- **Objectif / rythme** : Rendre concret le dépôt d'espèces. · détail
- **Visuel** : Insert : deux mains posent des billets sur un comptoir de bois, à côté d'un téléphone à clavier ; aucun visage.
- **Composition / cadrage** : mains au centre, téléphone en bord de cadre · insert très serré
- **Mouvement** : caméra insert_detail · graphique : aucun
- **Texte à l'écran** : —
- **Source visuelle** : R22 (a_produire)
- **Source factuelle** : F43
- **Remplacement** : Illustration au trait : billets → comptoir (mention ILLUSTRATION).
- **Transitions** : entrée coupe franche · sortie raccord par le fil
- **Son** : ambiance de boutique, discrète · effets : froissement de billets (discret)
- **Difficulté / méthode** : moyenne · tournage LUKOJI sur table (téléphone basique, mains), lumière douce ; aucun visage, aucune marque, texte de SMS générique
- **Montage** : Billets génériques ou flous : ne pas falsifier de monnaie.
- **Risques** : Ne montrer aucune marque ni interface.

### SC-19 · 134.0–141.6 s (7.6 s) · animation · illustration (dessin au trait LUKOJI, non générée) · mention « ILLUSTRATION »

- **Narration** : Quelques SMS plus tard, la somme est devenue de la monnaie électronique, stockée sur sa carte SIM. Il l'envoie.
- **Objectif / rythme** : Expliquer la conversion en monnaie électronique. · explication
- **Visuel** : Animation pas à pas : billets → SMS → montant inscrit dans une carte SIM dessinée ; le fil orange part de la SIM.
- **Composition / cadrage** : trois étapes de gauche à droite · plan large
- **Mouvement** : caméra suivi_trace · graphique : le fil part de la SIM vers la droite
- **Texte à l'écran** : —
- **Source visuelle** : R22 (a_produire)
- **Source factuelle** : F43
- **Remplacement** : —
- **Transitions** : entrée raccord par le fil · sortie raccord par le fil
- **Son** : motif rythmé léger · effets : bip de SMS (signature sonore 2/3)
- **Difficulté / méthode** : moyenne · dessin vectoriel au trait (noir, blanc cassé, orange) animé en 2D
- **Montage** : Fil 2/3.
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : l'argent devient électronique et voyage par SMS · éléments : billets, bulle SMS, carte SIM, fil · mouvement : trois étapes enchaînées · durée : 9 s · entrée : sur « Quelques SMS plus tard » · sortie : le fil sort du cadre · style : trait orange (fil 2/3) · contraintes : aucune interface réelle · assets : R22

### SC-20 · 141.6–146.8 s (5.2 s) · illustration · illustration (dessin au trait LUKOJI, non générée) · mention « ILLUSTRATION »

- **Narration** : Plus loin, le destinataire retire les billets chez un commerçant de son quartier.
- **Objectif / rythme** : Le retrait chez un commerçant du quartier. · arrivée
- **Visuel** : Le fil orange venu de la carte SIM (SC-19) aboutit à un petit kiosque dessiné au trait, sans enseigne ni marque ; une main dessinée reçoit des billets.
- **Composition / cadrage** : kiosque au tiers droit, fil entrant par la gauche · plan moyen
- **Mouvement** : caméra fixe · graphique : le fil se termine sur le comptoir dessiné
- **Texte à l'écran** : —
- **Source visuelle** : R22 (a_produire)
- **Source factuelle** : F43
- **Remplacement** : Carton typographique « RETRAIT CHEZ UN COMMERÇANT ».
- **Transitions** : entrée raccord par le fil · sortie coupe franche
- **Son** : motif rythmé léger
- **Difficulté / méthode** : moyenne · Inkscape + animation 2D (outils gratuits)
- **Montage** : Même style graphique que SC-19 (continuité de l'explication).
- **Risques** : Illustration mentionnée ; aucune marque.

### SC-21 · 146.8–155.6 s (8.8 s) · photo_lieu · authentique (photo réelle, datée)

- **Narration** : Ces agents, raconte Vodafone, sont souvent de petites boutiques familiales, plus habituées à vendre des marchandises qu'à manipuler l'argent de leurs clients.
- **Objectif / rythme** : Les agents sont de petites boutiques. · respiration
- **Visuel** : Kiosque M-Pesa au Kenya (photo réelle, date inconnue) ; en bas, la citation « ‘mom and pop’ stores ».
- **Composition / cadrage** : kiosque plein cadre · plan moyen
- **Mouvement** : caméra fixe · graphique : aucun
- **Texte à l'écran** : KENYA · DATE INCONNUE · PHOTO : REALT0N12 · CC BY-SA 3.0 / « ‘MOM AND POP’ STORES » — VODAFONE (2017)
- **Source visuelle** : R04 (metadonnees_verifiees)
- **Source factuelle** : F44
- **Remplacement** : R02.
- **Transitions** : entrée coupe franche · sortie coupe sèche au noir
- **Son** : ambiance de rue
- **Difficulté / méthode** : faible · photo libre Wikimedia Commons, recadrage 16:9, légende lieu / date / auteur / licence
- **Montage** : Ne jamais afficher la date des métadonnées (2005, impossible).
- **Risques** : Date inconnue : le dire ; contenu à inspecter.

## SEQ-06 — Le régulateur et les banques

*Musique : tension : basse tenue, dissonance discrète sur la question, résolution partielle sur « feu vert »*

### SC-22 · 156.2–163.4 s (7.2 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Un opérateur de téléphonie qui fait circuler de l'argent : est-ce encore du téléphone, ou déjà de la banque ?
- **Objectif / rythme** : Poser la question qui structure la seconde moitié du film. · tension : question
- **Visuel** : Écran partagé sur noir : « TÉLÉPHONE ? » à gauche, « BANQUE ? » à droite ; une ligne verticale orange les sépare.
- **Composition / cadrage** : symétrie gauche / droite · plein cadre
- **Mouvement** : caméra fixe · graphique : les deux mots apparaissent l'un après l'autre
- **Texte à l'écran** : TÉLÉPHONE ? / BANQUE ?
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : —
- **Remplacement** : —
- **Transitions** : entrée coupe du noir · sortie coupe franche
- **Son** : basse tenue, dissonance discrète
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : Conserver le fichier : le motif revient deux fois.
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : le service brouille la frontière entre téléphone et banque · éléments : deux mots, une ligne · mouvement : apparitions successives · durée : 6 s · entrée : sur « téléphone » · sortie : figé · style : Archivo Black · contraintes : motif repris en SEQ-06 et SEQ-09 · assets : gabarit

### SC-23 · 163.4–175.0 s (11.6 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Pour des banques, la réponse est claire. Selon Agence Ecofin, elles y voient une incursion dans leur métier : un opérateur ne peut pas exercer une activité bancaire sans licence.
- **Objectif / rythme** : Donner la voix de l'opposition. · conflit
- **Visuel** : Citation d'Agence Ecofin en IBM Plex Mono : « une incursion dans leur champ de compétence » ; le mot « BANQUE ? » de l'écran précédent reste en filigrane.
- **Composition / cadrage** : citation centrée · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition ligne à ligne
- **Texte à l'écran** : « UNE INCURSION DANS LEUR CHAMP DE COMPÉTENCE » / SOURCE : AGENCE ECOFIN
- **Source visuelle** : R15 (non_obtenue)
- **Source factuelle** : F46
- **Remplacement** : Capture de l'article d'Agence Ecofin si l'éditeur peut la réaliser dans un navigateur.
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : tension
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : —
- **Risques** : Article non relu (site protégé) ; banques non nommées.

### SC-24 · 175.0–178.6 s (3.6 s) · archive_photo · archive (photo datée de mars 2007)

- **Narration** : C'est à la Banque centrale du Kenya de trancher.
- **Objectif / rythme** : Le régulateur entre en scène. · ralentissement, arbitrage
- **Visuel** : Photo de la Banque centrale du Kenya prise le 7 mars 2007 : panoramique vertical lent de la façade vers l'enseigne « CENTRAL BANK OF KENYA » (révélation de l'institution).
- **Composition / cadrage** : façade en contre-plongée, enseigne en bas à droite · plan large
- **Mouvement** : caméra panoramique · graphique : aucun
- **Texte à l'écran** : BANQUE CENTRALE DU KENYA · 7 MARS 2007 · PHOTO : DEMOSH · CC BY 2.0
- **Source visuelle** : R06 (contenu_inspecte)
- **Source factuelle** : —
- **Remplacement** : R07 (qualité faible) ou typographie « BANQUE CENTRALE DU KENYA ».
- **Transitions** : entrée coupe franche · sortie coupe franche (même photo)
- **Son** : ambiance de ville lointaine
- **Difficulté / méthode** : faible · photo libre Wikimedia Commons datée, légende complète
- **Montage** : Le panoramique a une fonction : révéler l'enseigne ; vitesse calée sur la phrase.
- **Risques** : Coïncidence de date : ne pas suggérer que la photo documente une décision sur M-Pesa.

### SC-25 · 178.6–191.8 s (13.2 s) · archive_photo · archive (photo datée de mars 2007)

- **Narration** : Toujours selon cette agence, elle donne son feu vert, mais sous conditions. Un plafond de dépôt contre le blanchiment, la protection des clients, la sécurité des agents. Et chaque client doit être enregistré.
- **Objectif / rythme** : Le feu vert sous conditions. · explication
- **Visuel** : Même photo, cadre fixe sur l'enseigne, assombri à gauche ; trois conditions puis l'enregistrement des clients s'inscrivent en liste.
- **Composition / cadrage** : liste à gauche, enseigne à droite · plan large
- **Mouvement** : caméra fixe · graphique : quatre lignes successives
- **Texte à l'écran** : PLAFOND DE DÉPÔT (BLANCHIMENT) / PROTECTION DES CLIENTS / SÉCURITÉ DES AGENTS / ENREGISTREMENT DE CHAQUE CLIENT / SOURCES : AGENCE ECOFIN · VODAFONE
- **Source visuelle** : R06 (contenu_inspecte)
- **Source factuelle** : F45
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : résolution partielle de la tension
- **Difficulté / méthode** : faible · photo libre Wikimedia Commons datée, légende complète
- **Montage** : —
- **Risques** : Aucun risque particulier identifié.

### SC-26 · 191.8–195.0 s (3.2 s) · infographie · graphique éditorial (création LUKOJI)

- **Narration** : M-Pesa est lancé en mars 2007.
- **Objectif / rythme** : Dater le lancement et rappeler le pilote. · repère
- **Visuel** : Frise sobre : « OCT. 2005 · PILOTE » → « MARS 2007 · LANCEMENT ».
- **Composition / cadrage** : frise horizontale centrée · plein cadre
- **Mouvement** : caméra fixe · graphique : la frise se trace de gauche à droite
- **Texte à l'écran** : OCT. 2005 · PILOTE / MARS 2007 · LANCEMENT
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F7
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : nappe
- **Difficulté / méthode** : moyenne · motion design 2D, gabarit LUKOJI
- **Montage** : —
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : un an et demi entre le pilote et le lancement · éléments : ligne, deux jalons · mouvement : tracé 1,5 s · durée : 4 s · entrée : sur « lancé » · sortie : coupe · style : frise LUKOJI · contraintes : pas de jour précis · assets : gabarit

### SC-27 · 195.0–199.6 s (4.6 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Mais la question de départ, elle, ne disparaîtra pas.
- **Objectif / rythme** : Laisser la question ouverte jusqu'à SEQ-09. · suspension
- **Visuel** : Retour de l'écran partagé « TÉLÉPHONE ? / BANQUE ? », qui s'assombrit lentement.
- **Composition / cadrage** : symétrie · plein cadre
- **Mouvement** : caméra fixe · graphique : assombrissement lent
- **Texte à l'écran** : TÉLÉPHONE ? / BANQUE ?
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : —
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie fondu au noir court (0,5 s)
- **Son** : basse tenue qui s'éteint
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : Une seconde de silence avant SEQ-07.
- **Risques** : Aucun risque particulier identifié.

## SEQ-07 — La croissance, selon l'entreprise

*Musique : motif d'ampleur retenu, sans triomphalisme*

### SC-28 · 200.2–205.4 s (5.2 s) · graphique · graphique éditorial (création LUKOJI)

- **Narration** : Vodafone annonce 1,2 million d'utilisateurs à la fin de la première année.
- **Objectif / rythme** : Donner l'échelle de départ, en citant l'entreprise. · relance
- **Visuel** : Chiffre unique « 1,2 MILLION », sous-titre « UTILISATEURS À LA FIN DE LA PREMIÈRE ANNÉE ».
- **Composition / cadrage** : chiffre centré · plein cadre
- **Mouvement** : caméra fixe · graphique : compteur bref (1 s)
- **Texte à l'écran** : 1,2 MILLION / SOURCE : VODAFONE · CHIFFRE DE L'ENTREPRISE
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F10
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : motif d'ampleur retenu
- **Difficulté / méthode** : faible · gabarit unique LUKOJI (Archivo Black / IBM Plex Mono)
- **Montage** : —
- **Risques** : Chiffre non audité.

### SC-29 · 205.4–217.0 s (11.6 s) · carte · graphique éditorial (création LUKOJI)

- **Narration** : En 2022, l'entreprise en revendique plus de 51 millions, servis par 600 000 agents, dans sept pays. Parmi eux, la République démocratique du Congo.
- **Objectif / rythme** : Rendre visible le périmètre des 51 millions : sept pays. · ampleur
- **Visuel** : Carte de l'Afrique : les sept pays cités par Vodafone s'allument (Kenya, Tanzanie, Mozambique, RDC, Lesotho, Ghana, Égypte) ; la RDC reste éclairée plus longtemps.
- **Composition / cadrage** : Afrique centrée · plan large
- **Mouvement** : caméra fixe · graphique : les pays s'allument un à un, la RDC en dernier
- **Texte à l'écran** : 51 MILLIONS DE CLIENTS DANS 7 PAYS · 600 000 AGENTS · 2022 / SOURCE : VODAFONE · CHIFFRES DE L'ENTREPRISE / RÉPUBLIQUE DÉMOCRATIQUE DU CONGO
- **Source visuelle** : R20 (a_produire)
- **Source factuelle** : F49
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : motif d'ampleur
- **Difficulté / méthode** : moyenne · After Effects ou équivalent libre (Blender 2D, Natron) ; fond de carte Natural Earth (domaine public), projection simple
- **Montage** : Lève l'ambiguïté orale des « 51 millions ».
- **Risques** : Pas de globe 3D.
- **Motion design** : comprendre : les 51 millions concernent sept pays, pas le seul Kenya · éléments : carte d'Afrique, 7 pays · mouvement : allumage successif · durée : 10 s · entrée : sur « En 2022 » · sortie : la RDC reste allumée · style : aplats · contraintes : liste des pays : page Vodafone de 2022 · assets : Natural Earth

### SC-30 · 217.0–225.8 s (8.8 s) · document · authentique (capture d'un document cité)

- **Narration** : Ce sont les chiffres de Vodafone. Ils disent combien de clients le service a gagnés. Pas ce qui a changé pour eux.
- **Objectif / rythme** : Montrer que ces chiffres viennent d'un communiqué. · pivot critique
- **Visuel** : Page Vodafone de 2022 ; en surimpression, une ligne : « CHIFFRES DE L'ENTREPRISE ».
- **Composition / cadrage** : page plein cadre, ligne en bas · plan serré sur l'extrait
- **Mouvement** : caméra fixe · graphique : trait orange fixe sous l'extrait
- **Texte à l'écran** : CHIFFRES DE L'ENTREPRISE · VODAFONE · 2022
- **Source visuelle** : R24 (a_capturer)
- **Source factuelle** : F49
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe sèche
- **Son** : la musique s'interrompt sur « Pas ce qui a changé »
- **Difficulté / méthode** : faible · capture d'écran haute définition de la page, fond #0B0B0B, extrait court, URL et date de consultation à l'écran
- **Montage** : —
- **Risques** : Aucun risque particulier identifié.

## SEQ-08 — Ce que mesurent les chercheurs

*Musique : musique très basse ou absente : la voix et les chiffres portent ; silence sur « Pas un décompte »*

### SC-31 · 226.4–233.6 s (7.2 s) · graphique · graphique éditorial (création LUKOJI)

- **Narration** : Revenons à l'enquête FinAccess. En 2019, 82,9 % des adultes utilisent un service financier formel.
- **Objectif / rythme** : Reprendre la barre de SEQ-02 : le bond. · rappel
- **Visuel** : La barre de SEQ-02 revient à 26,7 % (2006) et monte jusqu'à 82,9 % (2019).
- **Composition / cadrage** : même gabarit et même échelle qu'en SEQ-02 · plein cadre
- **Mouvement** : caméra fixe · graphique : montée de la barre (1,5 s)
- **Texte à l'écran** : 2006 : 26,7 % / 2019 : 82,9 % / ADULTES · SERVICE FINANCIER FORMEL / SOURCE : FINACCESS 2019 (CBK · KNBS · FSD KENYA)
- **Source visuelle** : R21, R27 (a_capturer, a_produire)
- **Source factuelle** : F75
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : musique très basse
- **Difficulté / méthode** : faible · gabarit unique LUKOJI (Archivo Black / IBM Plex Mono)
- **Montage** : —
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : la finance formelle a fortement progressé · éléments : barre de SEQ-02 · mouvement : montée · durée : 7 s · entrée : sur « En 2019 » · sortie : figée · style : gabarit chiffres · contraintes : même échelle qu'en SEQ-02 · assets : projet de SEQ-02

### SC-32 · 233.6–244.8 s (11.2 s) · graphique · graphique éditorial (création LUKOJI)

- **Narration** : Mais l'argent mobile y est lui-même compté comme de la finance formelle. Cette courbe ne dit donc pas ce que M-Pesa a changé dans la vie des gens.
- **Objectif / rythme** : Expliquer le biais de définition. · nuance
- **Visuel** : Sur la barre figée, une zone hachurée et l'étiquette « INCLUT L'ARGENT MOBILE (CLASSÉ FORMEL) », sans pourcentage ; puis « ≠ CE QUE M-PESA A CHANGÉ ».
- **Composition / cadrage** : barre à gauche, étiquettes à droite · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition des hachures puis des étiquettes
- **Texte à l'écran** : INCLUT L'ARGENT MOBILE (CLASSÉ FORMEL) / ≠ CE QUE M-PESA A CHANGÉ
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F75
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : musique très basse
- **Difficulté / méthode** : faible · gabarit unique LUKOJI (Archivo Black / IBM Plex Mono)
- **Montage** : —
- **Risques** : Ne pas quantifier la part de l'argent mobile (non sourcée).
- **Motion design** : comprendre : la hausse inclut mécaniquement l'argent mobile · éléments : hachures, deux étiquettes · mouvement : apparitions · durée : 10 s · entrée : sur « Mais » · sortie : coupe · style : hachures grises · contraintes : aucun chiffre inventé pour la part du mobile · assets : gabarit

### SC-33 · 244.8–257.2 s (12.4 s) · infographie · graphique éditorial (création LUKOJI)

- **Narration** : Pour le mesurer, les économistes Tavneet Suri et William Jack suivent des familles kényanes depuis 2008. Ils les comparent en fonction du nombre d'agents installés près de chez elles.
- **Objectif / rythme** : Expliquer la méthode avant le résultat. · méthode
- **Visuel** : Schéma : un panel de familles suivies de 2008 à 2014 ; autour d'un foyer, un cercle de 1 km où apparaissent des points d'agents.
- **Composition / cadrage** : frise 2008-2014 en haut, cercle en bas · plein cadre
- **Mouvement** : caméra fixe · graphique : la frise se trace, puis les points apparaissent dans le cercle
- **Texte à l'écran** : TAVNEET SURI · WILLIAM JACK / PANEL DE MÉNAGES · 2008 → 2014 / AGENTS DANS UN RAYON DE 1 KM
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F79
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : silence musical, voix seule
- **Difficulté / méthode** : moyenne · motion design 2D, gabarit LUKOJI
- **Montage** : —
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : on compare des familles selon le nombre d'agents installés près de chez elles · éléments : frise, foyer, cercle, points · mouvement : tracé puis apparitions · durée : 12 s · entrée : sur « Pour le mesurer » · sortie : coupe · style : schéma épuré · contraintes : ne pas montrer de « groupe témoin » : la mesure est continue · assets : gabarit

### SC-34 · 257.2–261.6 s (4.4 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Leur conclusion paraît dans la revue Science en 2016.
- **Objectif / rythme** : Montrer la publication scientifique. · caution
- **Visuel** : Carte de référence typographique originale, sur noir : « The long-run poverty and gender impacts of mobile money » · Tavneet Suri & William Jack · Science · 2016. La carte se réduit ensuite en haut d'écran et reste visible pendant les visualisations originales des résultats (SC-35, SC-36).
- **Composition / cadrage** : titre en IBM Plex Mono au centre, auteurs et revue dessous · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition ligne à ligne, puis réduction en bandeau
- **Texte à l'écran** : « THE LONG-RUN POVERTY AND GENDER IMPACTS OF MOBILE MONEY » / TAVNEET SURI & WILLIAM JACK · SCIENCE · 2016
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F78
- **Remplacement** : Référence seule sur noir, sans bandeau.
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : voix seule
- **Difficulté / méthode** : faible · typographie animée (gabarit LUKOJI)
- **Montage** : Aucune page, figure ou illustration de l'article.
- **Risques** : Aucun élément protégé de l'article n'est reproduit.

### SC-35 · 261.6–271.2 s (9.6 s) · graphique · graphique éditorial (création LUKOJI)

- **Narration** : Selon eux, l'accès à M-Pesa aurait fait sortir au moins 194 000 foyers de l'extrême pauvreté, soit 2 % des ménages du pays.
- **Objectif / rythme** : Rendre l'ordre de grandeur lisible. · révélation du résultat
- **Visuel** : Grille de 100 carrés gris ; 2 deviennent orange. Légende : « AU MOINS 194 000 FOYERS · 2 % DES MÉNAGES · ESTIMATION ».
- **Composition / cadrage** : grille centrée, légende dessous · plein cadre
- **Mouvement** : caméra fixe · graphique : deux carrés s'allument
- **Texte à l'écran** : AU MOINS 194 000 FOYERS (ESTIMATION) / 2 % DES MÉNAGES / SOURCE : SURI & JACK, SCIENCE (2016)
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F78
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : voix seule
- **Difficulté / méthode** : faible · gabarit unique LUKOJI (Archivo Black / IBM Plex Mono)
- **Montage** : —
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : un effet réel mais limité à 2 % des ménages · éléments : grille 10×10 · mouvement : allumage · durée : 10 s · entrée : sur « au moins » · sortie : figée · style : gabarit · contraintes : mot « estimation » toujours visible · assets : gabarit

### SC-36 · 271.2–280.4 s (9.2 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Le seuil retenu : 1,25 dollar par jour et par personne. L'effet serait plus fort pour les foyers dirigés par des femmes.
- **Objectif / rythme** : Définir le seuil et donner l'effet par genre. · précision
- **Visuel** : Sous la grille : « SEUIL : 1,25 $ PAR JOUR ET PAR PERSONNE », puis « EFFET PLUS FORT : FOYERS DIRIGÉS PAR DES FEMMES ».
- **Composition / cadrage** : deux lignes sous la grille · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition ligne à ligne
- **Texte à l'écran** : SEUIL : 1,25 $ PAR JOUR ET PAR PERSONNE / EFFET PLUS FORT : FOYERS DIRIGÉS PAR DES FEMMES
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F78, F12
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : voix seule
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : Aucune photo de personne associée à ces chiffres.
- **Risques** : Aucun risque particulier identifié.

### SC-37 · 280.4–285.3 s (4.9 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : C'est une estimation, extrapolée à l'échelle du pays. Pas un décompte.
- **Objectif / rythme** : Clore sur la limite. · ralentissement, limite
- **Visuel** : Le mot « ESTIMATION » en grand, puis « ≠ DÉCOMPTE ».
- **Composition / cadrage** : mot centré · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition sèche
- **Texte à l'écran** : ESTIMATION / ≠ DÉCOMPTE
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F78
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe au noir
- **Son** : silence
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : Silence complet sur « Pas un décompte ».
- **Risques** : Aucun risque particulier identifié.

## SEQ-09 — Le prix du succès

*Musique : reprise en mineur après une seconde de silence ; montée lente jusqu'aux sénateurs, retombée*

### SC-38 · 285.9–287.9 s (2.0 s) · plan_ambiance · noir (respiration)

- **Narration** : — (sans voix off)
- **Objectif / rythme** : Marquer le changement de régime du film. · respiration, rupture
- **Visuel** : Noir complet, sans texte.
- **Composition / cadrage** : — · plein cadre
- **Mouvement** : caméra fixe · graphique : aucun
- **Texte à l'écran** : —
- **Source visuelle** : — (—)
- **Source factuelle** : —
- **Remplacement** : —
- **Transitions** : entrée coupe au noir · sortie coupe franche
- **Son** : silence total
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : 2 s de silence.
- **Risques** : Aucun risque particulier identifié.

### SC-39 · 287.9–296.7 s (8.8 s) · graphique · graphique éditorial (création LUKOJI)

- **Narration** : Ce succès a un prix, et d'abord pour les usagers. Selon Agence Ecofin, certains transferts coûtent près de 7 % du montant envoyé.
- **Objectif / rythme** : Le coût, du côté des usagers. · relance : le coût
- **Visuel** : Sur noir, une jauge horizontale se remplit jusqu'à 7 % ; légende « CERTAINS TRANSFERTS ».
- **Composition / cadrage** : jauge au centre, valeur en Archivo Black jaune · plein cadre
- **Mouvement** : caméra fixe · graphique : remplissage de la jauge (1 s)
- **Texte à l'écran** : JUSQU'À 7 % DU MONTANT · CERTAINS TRANSFERTS / SOURCE : AGENCE ECOFIN (2025)
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F55
- **Remplacement** : Chiffre seul en typographie.
- **Transitions** : entrée coupe du noir · sortie coupe franche
- **Son** : reprise musicale en mineur
- **Difficulté / méthode** : faible · gabarit chiffres LUKOJI
- **Montage** : « Certains transferts » toujours visible.
- **Risques** : Ne pas généraliser le chiffre à tous les transferts.

### SC-40 · 296.7–309.1 s (12.4 s) · photo_lieu · authentique (photo de 2007, réutilisée)

- **Narration** : Des médias kényans rapportent que la Banque centrale prépare une réponse. Elle voudrait ramener le coût moyen d'environ 23 shillings à 10 shillings par transaction, d'ici 2028.
- **Objectif / rythme** : Le régulateur prépare une réponse. · réponse annoncée
- **Visuel** : Banque centrale du Kenya (R06), cadre serré sur l'enseigne ; flèche « 23 → 10 KES » et le mot « PROJET ».
- **Composition / cadrage** : enseigne à droite, flèche à gauche · plan large
- **Mouvement** : caméra fixe · graphique : la flèche descend
- **Texte à l'écran** : 23 → 10 SHILLINGS PAR TRANSACTION (COÛT MOYEN) / PROJET · D'ICI 2028 · RAPPORTÉ PAR DES MÉDIAS KÉNYANS (VIA AGENCE ECOFIN)
- **Source visuelle** : R06 (contenu_inspecte)
- **Source factuelle** : F55
- **Remplacement** : R07 (qualité faible) ou flèche graphique seule.
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : musique en mineur
- **Difficulté / méthode** : faible · photo libre Wikimedia Commons datée, légende complète
- **Montage** : Le mot « PROJET » reste visible tout le plan.
- **Risques** : Ne pas présenter le plafonnement comme adopté ; photo de 2007 réutilisée : légende.

### SC-41 · 309.1–320.3 s (11.2 s) · graphique · graphique éditorial (création LUKOJI)

- **Narration** : Pour Safaricom, en revanche, M-Pesa est devenu un pilier. Sur l'exercice 2025, d'après l'entreprise, il représente 44,2 % de ses revenus de services au Kenya.
- **Objectif / rythme** : Le poids du service pour l'opérateur. · contrepoint
- **Visuel** : Barre horizontale des revenus de services de Safaricom au Kenya : 44,2 % pour M-PESA.
- **Composition / cadrage** : barre horizontale, valeur jaune · plein cadre
- **Mouvement** : caméra fixe · graphique : remplissage 1 s
- **Texte à l'écran** : 44,2 % DES REVENUS DE SERVICES AU KENYA / EXERCICE 2025 · SOURCE : SAFARICOM
- **Source visuelle** : R21, R31 (a_capturer, a_produire)
- **Source factuelle** : F80
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : musique qui monte légèrement
- **Difficulté / méthode** : faible · gabarit unique LUKOJI (Archivo Black / IBM Plex Mono)
- **Montage** : Pas de camembert.
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : M-Pesa pèse près de la moitié des revenus de services de Safaricom au Kenya · éléments : une barre · mouvement : remplissage · durée : 8 s · entrée : sur « Pour Safaricom » · sortie : coupe · style : gabarit · contraintes : périmètre exact : services, Kenya · assets : gabarit

### SC-42 · 320.3–333.5 s (13.2 s) · document · authentique (capture d'un document cité)

- **Narration** : Et la question posée dès les débuts revient. En novembre 2020, des sénateurs kényans réclament à nouveau que Safaricom soit déclarée dominante, et que ses activités télécoms soient séparées de M-Pesa.
- **Objectif / rythme** : La question de SEQ-06 revient, portée par des élus. · tension politique
- **Visuel** : Titre de l'article de The Star (17/11/2020) ; puis retour bref du motif « TÉLÉPHONE ? / BANQUE ? » en filigrane.
- **Composition / cadrage** : titre au centre, motif en filigrane · plan serré sur l'extrait
- **Mouvement** : caméra fixe · graphique : apparition du motif en surimpression (20 % d'opacité)
- **Texte à l'écran** : THE STAR · 17 NOVEMBRE 2020 / SÉNAT KÉNYAN · COMITÉ DES TIC
- **Source visuelle** : R30 (a_capturer)
- **Source factuelle** : F81
- **Remplacement** : Typographie : titre et date de l'article.
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : point culminant de la tension
- **Difficulté / méthode** : faible · capture d'écran haute définition de la page, fond #0B0B0B, extrait court, URL et date de consultation à l'écran
- **Montage** : Rappel explicite du motif de SEQ-06.
- **Risques** : Article de la rubrique Opinion/Columnists : la légende dit seulement « The Star ».

### SC-43 · 333.5–345.9 s (12.4 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Le service a aussi ouvert la porte à d'autres usages. Le crédit sur mobile a démocratisé l'emprunt, mais il soulève, selon Agence Ecofin, la question de la protection des plus pauvres.
- **Objectif / rythme** : Les nouveaux usages et leur risque. · élargissement
- **Visuel** : Citation d'Agence Ecofin en IBM Plex Mono : « des questions se posent quant à la protection des pauvres ».
- **Composition / cadrage** : citation centrée · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition ligne à ligne
- **Texte à l'écran** : « DES QUESTIONS SE POSENT QUANT À LA PROTECTION DES PAUVRES » / SOURCE : AGENCE ECOFIN (2019)
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F58
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : musique qui retombe
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : —
- **Risques** : Article non relu (site protégé).

### SC-44 · 345.9–352.7 s (6.8 s) · infographie · graphique éditorial (création LUKOJI)

- **Narration** : En septembre 2018, FSD Kenya recensait déjà environ 110 applications de prêt sur téléphone.
- **Objectif / rythme** : Donner l'ampleur du crédit numérique. · chiffre final
- **Visuel** : 110 petits carrés neutres (applications) apparaissent en grille ; à côté, la couverture du rapport de FSD Kenya.
- **Composition / cadrage** : grille à gauche, document à droite · plein cadre
- **Mouvement** : caméra fixe · graphique : les carrés apparaissent par rangées
- **Texte à l'écran** : ≈ 110 APPLICATIONS DE PRÊT · SEPTEMBRE 2018 / SOURCE : FSD KENYA, DIGITAL CREDIT AUDIT REPORT (2019)
- **Source visuelle** : R21, R32 (a_capturer, a_produire)
- **Source factuelle** : F82
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe au noir
- **Son** : musique éteinte
- **Difficulté / méthode** : moyenne · motion design 2D, gabarit LUKOJI
- **Montage** : —
- **Risques** : Aucun risque particulier identifié.
- **Motion design** : comprendre : le crédit sur téléphone s'est multiplié très vite · éléments : 110 carrés neutres · mouvement : apparition par rangées · durée : 7 s · entrée : sur « En septembre 2018 » · sortie : figée puis coupe · style : carrés gris, aucune icône réelle · contraintes : aucun logo d'application · assets : gabarit

## SEQ-10 — À quelles conditions

*Musique : thème final dépouillé ; la dernière question tombe sur un silence avant le fondu*

### SC-45 · 353.3–362.9 s (9.6 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Une dernière critique vient de la recherche. Une thèse d'économie, présentée dans la Revue de la régulation, compare les monnaies locales et l'argent mobile.
- **Objectif / rythme** : Une critique académique, avec son cadre. · critique de fond
- **Visuel** : Carte de référence sur noir : « Présentation de thèse · Revue de la régulation (OpenEdition) » ; la phrase source suit en SC-46.
- **Composition / cadrage** : référence centrée · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition ligne à ligne
- **Texte à l'écran** : PRÉSENTATION DE THÈSE · REVUE DE LA RÉGULATION (OPENEDITION)
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F59
- **Remplacement** : Capture manuelle de la page par l'éditeur (facultative, R14).
- **Transitions** : entrée coupe du noir · sortie coupe franche
- **Son** : thème final, très bas
- **Difficulté / méthode** : faible · typographie animée (gabarit LUKOJI)
- **Montage** : —
- **Risques** : Auteur non nommé (non relevé) ; la référence ne l'invente pas.

### SC-46 · 362.9–368.1 s (5.2 s) · typographie_animee · typographie éditoriale (création LUKOJI)

- **Narration** : Selon son auteur, seules les premières visent les causes systémiques de la pauvreté.
- **Objectif / rythme** : Donner le jugement de l'auteur, dans ses propres termes. · critique de fond
- **Visuel** : La phrase source en IBM Plex Mono : « Les monnaies locales visent les causes systémiques de la pauvreté, ce que les systèmes de monnaie mobile ne font pas. »
- **Composition / cadrage** : citation centrée · plein cadre
- **Mouvement** : caméra fixe · graphique : apparition ligne à ligne
- **Texte à l'écran** : « LES MONNAIES LOCALES VISENT LES CAUSES SYSTÉMIQUES DE LA PAUVRETÉ, CE QUE LES SYSTÈMES DE MONNAIE MOBILE NE FONT PAS. » / PRÉSENTATION DE THÈSE · REVUE DE LA RÉGULATION
- **Source visuelle** : R21 (a_produire)
- **Source factuelle** : F59
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : thème final, très bas
- **Difficulté / méthode** : faible · typographie animée (Archivo Black, IBM Plex Mono)
- **Montage** : —
- **Risques** : Citation exacte de la source capturée en phase 1.

### SC-47 · 368.1–374.1 s (6.0 s) · reconstitution · montage-rappel : insert de reconstitution, illustration, photo réelle · mention « RECONSTITUTION (téléphone) · ILLUSTRATION (SMS) · PHOTO : KENYA, DATE INCONNUE (boutique) »

- **Narration** : Reste la leçon de départ. Le téléphone, le SMS, les petites boutiques : tout existait déjà.
- **Objectif / rythme** : Tout existait déjà : le rappeler par l'image. · rappel, respiration
- **Visuel** : Rappel de trois plans du film, en coupes sèches calées sur la voix : l'insert du téléphone (SC-03), la bulle de SMS dessinée (SC-19), la boutique peinte (R04, cadre de SC-21). Chaque plan garde sa propre mention.
- **Composition / cadrage** : trois plans fixes déjà vus · plans de rappel
- **Mouvement** : caméra fixe · graphique : aucun
- **Texte à l'écran** : RECONSTITUTION / ILLUSTRATION / KENYA · DATE INCONNUE · PHOTO : REALT0N12 · CC BY-SA 3.0
- **Source visuelle** : R22, R04 (a_produire, contenu_inspecte)
- **Source factuelle** : —
- **Remplacement** : Les trois mots « TÉLÉPHONE · SMS · BOUTIQUES » en typographie.
- **Transitions** : entrée coupe franche · sortie coupe franche
- **Son** : ambiance de rue légère
- **Difficulté / méthode** : faible · réutilisation des plans SC-03, SC-19, SC-21
- **Montage** : Coupes calées sur « téléphone », « SMS », « boutiques » ; mention propre à chaque plan.
- **Risques** : Ne pas présenter l'insert ni le dessin comme des archives.

### SC-48 · 374.1–382.9 s (8.8 s) · carte · graphique éditorial (création LUKOJI)

- **Narration** : Si l'on suit le récit de ses concepteurs, ce qui était nouveau, c'est d'avoir regardé ce que les clients en faisaient vraiment.
- **Objectif / rythme** : Boucler la carte du récit sur la leçon du titre. · synthèse
- **Visuel** : Dernier retour à la carte du Kenya : les fils orange sont devenus denses (dernier fil de l'argent).
- **Composition / cadrage** : pays centré · plan large
- **Mouvement** : caméra fixe · graphique : les fils se densifient lentement
- **Texte à l'écran** : SELON LE RÉCIT DE SES CONCEPTEURS
- **Source visuelle** : R20 (a_produire)
- **Source factuelle** : —
- **Remplacement** : —
- **Transitions** : entrée coupe franche · sortie glissement de carte vers l'Afrique centrale
- **Son** : thème final · effets : bip de SMS (signature sonore 3/3)
- **Difficulté / méthode** : moyenne · After Effects ou équivalent libre (Blender 2D, Natron) ; fond de carte Natural Earth (domaine public), projection simple
- **Montage** : Carte maîtresse, état 4/4 ; fil 3/3.
- **Risques** : Interprétation éditoriale : le sous-titre l'attribue au récit des concepteurs.
- **Motion design** : comprendre : l'usage des clients a dessiné le réseau · éléments : carte, fils · mouvement : densification · durée : 9 s · entrée : sur « Si l'on suit » · sortie : glissement vers l'Afrique · style : fil 3/3 · contraintes : — · assets : carte maîtresse

### SC-49 · 382.9–394.5 s (11.6 s) · carte · graphique éditorial (création LUKOJI)

- **Narration** : M-Pesa est aussi présent en République démocratique du Congo, selon Vodafone. Ce film ne dit pas ce qu'il y a changé : l'histoire kényane ne se transpose pas telle quelle.
- **Objectif / rythme** : Ouvrir vers la RDC sans comparaison. · ouverture prudente
- **Visuel** : La carte glisse du Kenya vers la RDC, qui s'éclaire seule ; aucune donnée comparative.
- **Composition / cadrage** : RDC centrée · plan large
- **Mouvement** : caméra fixe · graphique : glissement de carte (motivé : changement de pays)
- **Texte à l'écran** : RÉPUBLIQUE DÉMOCRATIQUE DU CONGO / PRÉSENCE DE M-PESA SELON VODAFONE (2022)
- **Source visuelle** : R20 (a_produire)
- **Source factuelle** : F49
- **Remplacement** : —
- **Transitions** : entrée glissement de carte · sortie fondu enchaîné (1 s)
- **Son** : thème final
- **Difficulté / méthode** : moyenne · After Effects ou équivalent libre (Blender 2D, Natron) ; fond de carte Natural Earth (domaine public), projection simple
- **Montage** : —
- **Risques** : Ne montrer aucun chiffre pour la RDC.

### SC-50 · 394.5–406.5 s (12.0 s) · plan_ambiance · authentique (photo réelle de 2013) utilisée comme image d'illustration · mention « IMAGE D'ILLUSTRATION — KINSHASA, 2013 »

- **Narration** : Mais elle laisse une question à poser, ici aussi. Quand un service privé devient aussi central, à quelles conditions fonctionne-t-il, et au profit de qui ?
- **Objectif / rythme** : Poser la question au public congolais. · question finale, ralentissement
- **Visuel** : Boulevard du 30 Juin, Kinshasa (photo réelle, 2013) ; la dernière question s'inscrit en Archivo Black ; silence, puis fondu au noir.
- **Composition / cadrage** : boulevard en perspective, question au tiers inférieur · plan moyen
- **Mouvement** : caméra fixe · graphique : apparition de la question
- **Texte à l'écran** : À QUELLES CONDITIONS, ET AU PROFIT DE QUI ? / PHOTO : ANTOINE MOENS DE HASE · CC BY 2.0
- **Source visuelle** : R11 (metadonnees_verifiees)
- **Source factuelle** : —
- **Remplacement** : Plan tourné par LUKOJI à Kinshasa (préférable) ; à défaut, la question sur noir.
- **Transitions** : entrée fondu enchaîné · sortie fondu au noir (fin ; la signature LUKOJI est ajoutée par le moteur vidéo)
- **Son** : ambiance de ville lointaine, puis silence
- **Difficulté / méthode** : faible · photo libre Wikimedia Commons, recadrage 16:9, légende lieu / date / auteur / licence
- **Montage** : Deux secondes de silence avant le fondu.
- **Risques** : Aucun argent mobile visible : image d'illustration ; contenu à inspecter.
