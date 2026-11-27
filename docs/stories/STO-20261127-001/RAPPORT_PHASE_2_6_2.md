# Rapport — Phase 2.6.2 : corrections ciblées et storyboard v10

`STO-20261127-001` · « Quand les clients ont changé le produit » · 27/11/2026

**Statut : `storyboard_draft`. Storyboard v10 NON VALIDÉ.** Ni `story qc`, ni validation, ni rendu, ni image générée, ni audio. Le moteur n'est pas modifié.

## Protection

- **Verrou** : script v21 et structure v6 intacts (empreintes recalculées).
- **Storyboard v9** : confirmé comme version courante avant modification, puis conservé. La v10 en dérive, et le générateur s'arrête si le fichier v9 diffère de la v9 du moteur.
- **Inchangés** : sources factuelles, autres projets, versions verrouillées.

## Modifications appliquées (8 scènes sur 50)

| Scène | Avant (v9) | Après (v10) | Motif |
|---|---|---|---|
| **SC-01** | Photo R01 (matatu de 2025) | **Carte du Kenya et autocar dessiné au trait** : tracé orange vers une région non nommée, sans personne ni marque, mention ILLUSTRATION ; outils gratuits (Inkscape, DaVinci Resolve/Fusion ou Blender) | Décision 1 |
| **SC-05** | « Première apparition de la carte » | « Retour de la carte » (simple mise en cohérence du texte du plan) | Conséquence de SC-01 |
| **SC-17** | Photo R02 (non inspectée) | **R04 en plan serré sur le lettrage peint « M-PESA »** (logo hors cadre) | Décision 3, plan de sécurisation |
| **SC-20** | Photo R03 (non inspectée) | **Kiosque dessiné au trait** où aboutit le fil de SC-19 (ILLUSTRATION) | Décision 3 |
| **SC-34** | Première page de l'article de *Science* | **Référence typographique originale** : titre de l'étude, Tavneet Suri & William Jack, *Science*, 2016. Elle reste en bandeau pendant les visualisations originales (SC-35 et SC-36). **Aucune page ni figure reproduite** | Décision 2 |
| **SC-39** | Photo R02 | **Jauge graphique « 7 % · certains transferts »** | Décision 3 |
| **SC-45** | Capture OpenEdition (manuelle, auteur non relevé) | **Référence typographique** ; capture rendue facultative | Supprime le risque de capture documenté |
| **SC-47** | R02, R03 et R04 | **Rappel de trois plans du film** : insert du téléphone (SC-03, RECONSTITUTION), SMS dessiné (SC-19, ILLUSTRATION), boutique R04 ; chaque plan garde sa mention | Décision 3 |

**Fidélité** (contrôlée automatiquement) :
- mêmes 50 scènes, aucun nouveau découpage ;
- voix off, durées déclarées et faits affichés **identiques à la v9** ;
- aucun chiffre nouveau ;
- silences voulus conservés ;
- durée : **401,1 s de scènes + 5,4 s de pauses = 406,5 s** (inchangée).

## Ressources

Nouveau registre : `research/stories/mpesa/v2_6_2/ressources_visuelles_v2_6_2.json`. Les registres v2.6 et v2.6.1 sont conservés.

| Statut | Ressources | Détail |
|---|---|---|
| Supprimées des scènes | **R01** (ouverture), **R02**, **R03** (abandonnées), **R28** (*Science*) | R02 et R03 restent **non inspectées** : aucune nouvelle tentative |
| Rendue facultative | **R14** (OpenEdition) | — |
| Ajoutées ou plus utilisées | R22 (illustrations : autocar, kiosque) et R04 (3 scènes) | — |
| Inchangées | Statuts d'inspection et de droits | Aucune licence inventée ; aucun droit de citation déclaré confirmé |

## Résultats des contrôles

**QC v10** (`v2_6_2/qc_storyboard.md`) : **BLOQUANT 0 · RISQUE MAJEUR 1 · ALERTE 18 · RECOMMANDATION 4 · CONFORME 25**.

- **Conformes** :
  - verrou, version v10, statut ;
  - 50 scènes identiques à la v9 en voix off, durées et faits ;
  - seules les 8 scènes prévues sont modifiées ;
  - aucune dépendance à R02 ou R03, et les deux restent non inspectées ;
  - R01 et R28 absentes ;
  - SC-01 mentionnée comme illustration ; SC-34 en typographie ;
  - couverture mot pour mot ; durées ; transitions.
- **Risque majeur nouveau** : la **part du motion design passe à 62 %** (31 scènes sur 50, contre 56 % en v9), et **SEQ-08 enchaîne 7 plans graphiques** (SC-31 à SC-37). C'est une **conséquence directe** du remplacement de la page de *Science* et des photos. Je ne l'ai pas corrigé, faute de décision : voir ci-dessous.
- **Alertes** :
  - documents à capturer, aux droits de citation non confirmés ;
  - trois ressources utilisées 3 fois (R12, R04, R06) ;
  - inserts à tourner ;
  - SC-17 en plan fixe de 9,6 s ;
  - URL du communiqué Safaricom à relever.
- **Moteur** (évaluation à l'export) : 0 bloquant ; JSON exporté sans erreur.
- **Statut** : `story qc` non lancé ; le projet reste en `storyboard_draft`.

**Tests** : 135 passed. Un test ajouté vérifie :
- les mêmes scènes, voix off, durées et faits que la v9 ;
- les seules 8 scènes modifiées ;
- l'absence de R01, R02, R03 et R28 ;
- les mentions à l'écran ;
- R02 et R03 non inspectées.

## Risques restants

1. **Densité graphique de SEQ-08** (7 plans de suite) et part du motion design à 62 %. Pistes, **à décider** (non appliquées) :
   - remplacer l'un des plans typographiques de SEQ-08 par un plan réel déjà sécurisé : R06, ou une capture documentaire comme la page FinAccess 2019 (R27) ;
   - ou accepter cette densité pour la séquence la plus analytique, en la vérifiant au test d'écoute.
2. **Droits de citation** des documents à capturer : non confirmés.
3. **Production** : inserts de reconstitution à tourner ; sons et musique à choisir.

## Recommandation

**Le storyboard v10 est prêt pour votre revue.** Les quatre risques majeurs de la phase 2.6.1 sont levés. Il reste **une décision** : la densité graphique de SEQ-08. Elle n'est pas bloquante, mais elle concerne la séquence où le décrochage est le plus probable.

Si vous validez le storyboard en l'état, la procédure est la suivante : `story qc`, puis `story approve --etape storyboard --acteur "…"`, puis le verrou. C'est à vous de la lancer.

## Fichiers

- **Rapport** : `docs/stories/STO-20261127-001/RAPPORT_PHASE_2_6_2.md`
- **Exports** : `docs/stories/STO-20261127-001/v2_6_2/` (`storyboard.json`, `storyboard.md`, `storyboard_production.md`, `qc_storyboard.md`, plans)
- **Sources** : `research/stories/mpesa/v2_6_2/` (`build_storyboard_v2_6_2.py`, `storyboard_v2_6_2.json`, `ressources_visuelles_v2_6_2.json`, `qc_storyboard_v2_6_2.py`)
