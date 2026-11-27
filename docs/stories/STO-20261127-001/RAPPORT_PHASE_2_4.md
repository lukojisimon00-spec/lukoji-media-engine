# Rapport — Phase 2.4 : consolidation éditoriale du pilote M-Pesa

`STO-20261127-001` · titre de travail : **Quand les clients ont changé le produit** · 27/11/2026

**Statut du projet : `structure_draft` — NON VALIDÉ.** Aucune validation humaine n'a été enregistrée, et ce rapport n'en est pas une. Il n'y a pas de Phase 3, pas de storyboard reconstruit, pas d'image ni de vidéo.

## 1. Versions créées (toutes les versions antérieures sont conservées)

| Élément | Avant | Après | Fichier source |
|---|---|---|---|
| Script | v16 (v2.1) | **v17 → v21** (v2.2). v17 : première consolidation ; v18-v20 : phrases scindées et répétitions réduites ; v21 : rattachement à la structure v6, contenu identique à v20 | `research/stories/mpesa/v2_2/script_v2_2.json` |
| Structure | v4 | **v5 → v6**. v6 : durées alignées sur le script final | `research/stories/mpesa/v2_2/structure_v2_2.json` |
| Hooks | v4 | **v5** (H9 prudent) | `research/stories/mpesa/v2_2/hooks_v2_2.json` |
| Direction artistique | v3 | **v4 → v5** (rattachements, contenu inchangé) | `research/stories/mpesa/v2/direction_v2.json` |
| Dossier factuel | v4 | v4 (inchangé) | — |
| Storyboard | v7 | v7 (inchangé, **obsolète**) | — |
| Titre du projet (base) | « M-Pesa : le prêt par SMS qui est devenu une révolution de l'argent mobile » | « Quand les clients ont changé le produit » (journalisé dans `story_events`, statut inchangé) | — |

Les documents conservés sans modification sont le script v2.1, la structure v4, `FACTCHECK_FINAL_V2.md`, `REVUE_EDITORIALE_FINALE.md`, l'audit humain et les exports v1, v2 et v2.1.

## 2. Modifications exactes du script (v2.1 → v2.2)

Mots selon le décompte du moteur : 936 → **984** ; durée **399,0 s ≈ 6,7 min**, pauses comprises.

| Séq. | Mots | Modification |
|---|---|---|
| SEQ-01 | 43 → 43 | « confier ses billets à un chauffeur de bus » devient « confier son argent à une compagnie de bus ». Faits : + F72, F73 (FinAccess 2006, Hughes & Lonie, CGAP) |
| SEQ-02 | = | — |
| SEQ-03 | 78 → 102 | Attribution explicite du récit : « Ce qui suit, on le connaît surtout par ceux qui l'ont mené. Un article publié en 2007 par deux responsables du projet. Puis un texte de Michael Joseph… publié par Vodafone en 2017. Selon ces récits… ». Faits : + F76 |
| SEQ-04 | 67 → 68 | « D'après Michael Joseph, ceux qui reçoivent un prêt… » ; « raconte-t-il » |
| SEQ-05 | = | Nouvelle transition : « Le mécanisme fonctionne. Reste à savoir qui a le droit de le faire fonctionner. » |
| SEQ-06 | 71 → 106 | Réécrite autour d'une question : téléphone ou banque ? Objection des banques (Ecofin), arbitrage de la Banque centrale sous conditions (Ecofin), enregistrement des clients, lancement en mars 2007, puis « Mais la question de départ, elle, ne disparaîtra pas. » Nouvelle transition. Aucun fait nouveau (F46, F45, F7) |
| SEQ-07 | = | — |
| SEQ-08 | 202 → 146 | Retirés : la répartition parents / enfants (F40, F68), les 185 000 femmes et une phrase de transition. « Au moins 194 000 foyers », « Selon eux », « C'est une estimation, extrapolée à l'échelle du pays. Pas un décompte. » Faits : F75, F79, F78, F12 |
| SEQ-09 | 148 → 162 | Réordonnée en progression (usagers → régulateur → opérateur → question politique → nouveaux usages) ; liens explicites (« et d'abord pour les usagers », « en revanche », « Et la question posée dès les débuts revient », « Le service a aussi ouvert la porte à d'autres usages »). Mêmes faits |
| SEQ-10 | 98 → 128 | Thèse citée avec son cadre (monnaies locales) ; leçon attribuée (« Si l'on suit le récit de ses concepteurs… ce que les clients en faisaient ») ; RDC : présence selon Vodafone, refus explicite de transposer, question ouverte |

Le tableau complet des décisions est dans `REGISTRE_DECISIONS_EDITORIALES.md`.

## 3. Décisions appliquées

D01 (titre), D04 (H9 prudent), D05 (attribution des origines), D06 (pas de paris en ligne), D07 (faits Ecofin limités et attribués), D08 à D12 (SEQ-06, 08, 09, 10 et thèse), D13 (structure sans faits retirés), D14 (transition de SEQ-06), D15 (durée), D16 (rattachements).

**Non appliquées, volontairement** : D02 (exports historiques), D03 (titre du sujet de la phase 1), D22 (storyboard).

**En attente** : D17 (« dans sept pays »), D18 (témoignages), D19 (source indépendante sur les origines), D20 (projet de baisse des frais), D21 (relecture d'Ecofin et de la thèse), D23 (validation).

## 4. Contrôles et tests

- **Contrôle de cohérence de la consolidation** (`v2_2/qc_consolidation.md`) : **23 contrôles, 0 bloquant**. Il vérifie :
  - alignement script / structure (faits et transitions) ;
  - rattachement des versions ;
  - conservation des versions antérieures ;
  - contrôle factuel du moteur (faits connus, attributions, chaque nombre présent dans un fait ou une preuve) ;
  - absence des faits retirés, du communiqué de 2009, des paris en ligne et de « chauffeur » ;
  - titre en base et dans le script ;
  - H9 prudent ;
  - durée dans la cible ;
  - intégrité de la base, absence de validation, statut.
- **QC du moteur** (n° 11) : 0 bloquant en factuel, narratif, script et durée. **9 bloquants en visuel**, tous dus au storyboard v7 obsolète, qui n'a pas été reconstruit. Je n'ai désactivé aucun contrôle.
- **Tests** : `python3 -m pytest -q` donne **131 passed** (130 existants et 1 nouveau test de cohérence v2.2).
- **Base** : `PRAGMA integrity_check` = ok ; aucune validation ; statut `structure_draft`.

Ces résultats sont techniques. **Ils ne valent pas validation éditoriale.**

## 5. Incohérences restantes

1. **Storyboard v7 obsolète.** Il est construit sur le script v13 et la direction v2. Scènes à reprendre après validation, en plus de la liste du fact-check :
   - SC-01 : hook « compagnie de bus » ;
   - SC-08 : deux sources d'origine à l'écran (article de 2007, texte de 2017) ;
   - SC-18 à SC-22 : SEQ-06 réécrite ;
   - SC-28 et SC-33 : parents / enfants et 185 000 femmes retirés de la voix off ;
   - SC-34 à SC-40 : nouvel ordre de SEQ-09 ;
   - SC-41 à SC-44 : SEQ-10 réécrite.
2. **Export du moteur** : son en-tête de durée dépend du storyboard. L'export v2.2 est donc produit par un script propre au pilote. **Comportement du moteur signalé, non modifié.**
3. **Titre du sujet de la phase 1** inchangé (D03).
4. **Ambiguïté des « 51 millions »** en SEQ-07 (D17).
5. **Le récit des origines n'a toujours pas de source indépendante** de Vodafone (D19). Il est désormais attribué comme tel.
6. **SEQ-09 et SEQ-10 sont un peu plus longues qu'en v2.1** (+14 et +30 mots) : la progression et l'honnêteté du lien avec la RDC ont été préférées à la brièveté. SEQ-08 est passée de 202 à 146 mots.

## 6. Fichiers

**Nouveaux** :
- `docs/stories/STO-20261127-001/v2_2/script.md` : script consolidé
- `docs/stories/STO-20261127-001/v2_2/structure.md` : structure narrative consolidée
- `docs/stories/STO-20261127-001/v2_2/qc_consolidation.md` et `qc_consolidation.json`
- `docs/stories/STO-20261127-001/REGISTRE_DECISIONS_EDITORIALES.md`
- `docs/stories/STO-20261127-001/RAPPORT_PHASE_2_4.md`
- `research/stories/mpesa/v2_2/script_v2_2.json`, `structure_v2_2.json`, `hooks_v2_2.json`, `consolidation_v2_2.py`

**Modifié** :
- `tests/test_pilote_mpesa_v2.py` : un test ajouté.
