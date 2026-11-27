# QC du storyboard v2.6

**BLOQUANT** : 0 · **RISQUE MAJEUR** : 9 · **ALERTE** : 20 · **RECOMMANDATION** : 4 · **CONFORME** : 17

> Pas de score : un storyboard complet n'est pas forcément réalisable. Ce contrôle ne vaut pas validation.

## RISQUE MAJEUR

| Catégorie | Contrôle | Scène | Détail |
|---|---|---|---|
| sourcing | photo dont le contenu n'a pas été inspecté | SC-17 | R02 : Contenu NON inspecté (limitation de débit Wikimedia, HTTP 429). |
| sourcing | photo dont le contenu n'a pas été inspecté | SC-20 | R03 : Contenu NON inspecté (HTTP 429). |
| sourcing | photo dont le contenu n'a pas été inspecté | SC-21 | R04 : Contenu NON inspecté (HTTP 429). |
| sourcing | photo dont le contenu n'a pas été inspecté | SC-39 | R02 : Contenu NON inspecté (limitation de débit Wikimedia, HTTP 429). |
| sourcing | photo dont le contenu n'a pas été inspecté | SC-47 | R02 : Contenu NON inspecté (limitation de débit Wikimedia, HTTP 429). |
| sourcing | photo dont le contenu n'a pas été inspecté | SC-47 | R04 : Contenu NON inspecté (HTTP 429). |
| sourcing | photo dont le contenu n'a pas été inspecté | SC-47 | R03 : Contenu NON inspecté (HTTP 429). |
| sourcing | photo dont le contenu n'a pas été inspecté | SC-50 | R11 : Contenu NON inspecté (HTTP 429). |
| droits | article de Science (AAAS) : reproduction d'une page à confirmer | — | remplacement prévu : page MIT News ou typographie |

## ALERTE

| Catégorie | Contrôle | Scène | Détail |
|---|---|---|---|
| statisme | plan fixe sans mouvement graphique de plus de 9 s | SC-17 | 9.6 s |
| repetition | même ressource utilisée 3 fois ou plus | — | R12 (Page Vodafone « M-Pesa: creating the leading mobile money se) : 3 scènes |
| repetition | même ressource utilisée 3 fois ou plus | — | R02 (Agent M-PESA et Equity à Nairobi) : 3 scènes |
| repetition | même ressource utilisée 3 fois ou plus | — | R06 (Bâtiment de la Banque centrale du Kenya en 2007) : 3 scènes |
| droits | document à capturer ; droits de citation à confirmer | SC-02 | R26 |
| droits | document à capturer ; droits de citation à confirmer | SC-08 | R12 |
| droits | document à capturer ; droits de citation à confirmer | SC-10 | R29 |
| droits | document à capturer ; droits de citation à confirmer | SC-11 | R12 |
| droits | document à capturer ; droits de citation à confirmer | SC-15 | R12 |
| sourcing | ressource non obtenue (substitut prévu) | SC-23 | R15 |
| droits | document à capturer ; droits de citation à confirmer | SC-30 | R24 |
| droits | document à capturer ; droits de citation à confirmer | SC-31 | R27 |
| droits | document à capturer ; droits de citation à confirmer | SC-34 | R28 |
| droits | document à capturer ; droits de citation à confirmer | SC-41 | R31 |
| droits | document à capturer ; droits de citation à confirmer | SC-42 | R30 |
| droits | document à capturer ; droits de citation à confirmer | SC-44 | R32 |
| droits | document à capturer ; droits de citation à confirmer | SC-45 | R14 |
| sourcing | page OpenEdition protégée contre les robots : capture manuelle par l'éditeur | — |  |
| sourcing | URL exacte du communiqué Safaricom non relevée | — | R31 |
| reconstitution | inserts à tourner (table, mains, téléphone) ; illustration prévue en remplacement | — | SC-03, SC-18 |

## RECOMMANDATION

| Catégorie | Contrôle | Scène | Détail |
|---|---|---|---|
| motion | fiche de motion design à détailler | SC-09 | carte |
| motion | fiche de motion design à détailler | SC-49 | carte |
| audio | choisir et créditer les sons Freesound et la musique avant montage (aucun son sélectionné) | — |  |
| rythme | SEQ-08 enchaîne graphiques et schémas : prévoir une respiration visuelle si le test d'écoute montre un décrochage | — |  |

## CONFORME

| Catégorie | Contrôle | Scène | Détail |
|---|---|---|---|
| verrou | versions validées intactes et reconstruction autorisée | — | reconstruction du storyboard : AUTORISÉE à partir des versions validées |
| verrou | storyboard du moteur construit sur le script v21 (et la direction v5) | — | storyboard v9 basé sur {'script': 21, 'visual': 5} |
| verrou | fichier storyboard_v2_6.json = version du moteur | — | v9 |
| statut | projet en storyboard_draft | — | storyboard_draft |
| couverture | voix off reconstituée mot pour mot, champs requis (contrôle du moteur) | — |  |
| structure | les dix séquences du script validé sont couvertes | — | SEQ-01, SEQ-02, SEQ-03, SEQ-04, SEQ-05, SEQ-06, SEQ-07, SEQ-08, SEQ-09, SEQ-10 |
| structure | correspondance avec les étapes de la structure v6 | — |  |
| sources | faits affichés ⊂ faits de la séquence validée, aucun fait exclu | — |  |
| duree | durée du storyboard dans la cible 6–8 min | — | 406.5 s ≈ 6.8 min (voix off seule : 399.0 s ; +7.5 s de silences et de tenues) |
| transitions | chaque scène a une transition d'entrée et de sortie | — |  |
| diversite | part du motion design ≤ 60 % | — | 28/50 (56%) · types : {'plan_ambiance': 3, 'document': 9, 'reconstitution': 2, 'typographie_animee': 9, 'carte': 7, 'graphique': 6, 'animation': 2, 'infographie': 4, 'photo_lieu': 6, 'archive_photo': 2} |
| diversite | pas plus de 4 plans de motion design consécutifs | — | suite maximale : 4 (jusqu'à SC-07) |
| images_generees | aucune image générée par IA | — |  |
| reconstitution | reconstitutions mentionnées à l'écran | — | SC-03, SC-18 |
| authenticite | images d'illustration et illustrations mentionnées | — |  |
| complexite | aucune scène de difficulté élevée | — |  |
| audio | chaque scène a une ambiance et une intention musicale | — |  |
