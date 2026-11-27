# Rapport — Phase 2.6 : reconstruction du storyboard

`STO-20261127-001` · « Quand les clients ont changé le produit » · 27/11/2026

**Statut : `storyboard_draft`. Storyboard NON VALIDÉ.** Aucune validation n'a été enregistrée. Il n'y a ni rendu ni Phase 3, aucune image n'a été générée, et le moteur n'a pas été modifié.

## 1. Versions de référence vérifiées

- **Verrou** (`VERROU_VALIDATION.json`, script `verifier`) : les 12 versions couvertes par les deux validations de Simon Lukoji sont présentes et inchangées (empreintes SHA-256 recalculées). La reconstruction est **autorisée**.
- **Sources utilisées** :
  - script **v21** (v2.2) et structure **v6** ;
  - dossier factuel **v4** ;
  - direction artistique **v5** (contenu de la direction v2) ;
  - registre des décisions ;
  - storyboard v7, lu seulement pour repérer ce qui devait être remplacé.
- **Contrôle avant toute écriture** : le générateur (`build_storyboard_v2_6.py`) **refuse de s'exécuter** si l'empreinte du script ou de la structure diffère de celle du verrou.
- **Aucune modification** du script, de la structure, du dossier factuel, du verrou ni des empreintes.

## 2. Nouvelle version

- **Storyboard v9** dans le moteur (version éditoriale v2.6), construit sur le script v21 et la direction v5.
- **Storyboard v8** : enregistré par erreur avec un champ « animation » dans un format refusé par l'export du moteur (dictionnaire au lieu d'un texte). Il est conservé et remplacé par la v9, où la fiche de motion design est déplacée dans un champ distinct.
- Les versions v1 à v7 sont conservées.

## 3. Scènes et durée

**50 scènes.** Le découpage suit la narration, sans règle d'une phrase par plan : une scène porte de 0 à 4 phrases, ou une partie de phrase.

| Séquence | Scènes | Durée | Plan le plus court / le plus long |
|---|---|---|---|
| SEQ-01 | 4 | 19,2 s | 2,6 / 6,2 s |
| SEQ-02 | 4 | 32,0 s | 3,6 / 12,0 s |
| SEQ-03 | 5 | 40,8 s | 3,6 / 12,4 s |
| SEQ-04 | 3 | 27,2 s | 7,2 / 12,8 s |
| SEQ-05 | 5 | 34,0 s | 2,8 / 9,6 s |
| SEQ-06 | 6 | 43,4 s | 3,2 / 13,2 s |
| SEQ-07 | 3 | 25,6 s | 5,2 / 11,6 s |
| SEQ-08 | 7 | 58,9 s | 4,4 / 12,4 s |
| SEQ-09 | 7 | 66,8 s | 2,0 / 13,2 s |
| SEQ-10 | 6 | 53,2 s | 5,2 / 12,0 s |

**Durée estimée : 406,5 s ≈ 6 min 47 s.** Elle se décompose ainsi :
- voix off et pauses du script : 399,0 s ;
- silences et tenues voulus : 7,5 s (noir après le titre, suspension en fin de SEQ-06, noir avant SEQ-09, silence final).

L'export du moteur affiche « 6.8 min ». La signature LUKOJI de fin sera ajoutée par le moteur vidéo et n'est pas comptée.

## 4. Répartition des types visuels

| Type | Nb | | Statut de l'image | Nb |
|---|---|---|---|---|
| document (capture d'un document cité) | 9 | | authentique (photo ou document réel) | 17 |
| typographie animée | 9 | | archive datée (Banque centrale, mars 2007) | 2 |
| carte | 7 | | graphique éditorial | 17 |
| graphique | 6 | | typographie éditoriale | 9 |
| photo de lieu | 6 | | illustration (trait LUKOJI) | 2 |
| infographie | 4 | | reconstitution (inserts sur table) | 2 |
| image d'ambiance (photo-illustration ou noir) | 3 | | noir (respiration) | 1 |
| archive photo | 2 | | **générée par IA** | **0** |
| animation au trait | 2 | | | |
| reconstitution | 2 | | | |

**Rythme** :
- **Accélérations** : les fils de SEQ-04, le mécanisme de SEQ-05.
- **Ralentissements** : la méthode des sources en SEQ-03, l'arbitrage de la Banque centrale en SEQ-06, la limite « Pas un décompte » en SEQ-08, la question finale.
- **Tension** : « TÉLÉPHONE ? / BANQUE ? » en SEQ-06, repris en SEQ-09 (sénateurs).
- **Révélations** : le microcrédit (SEQ-03), les 2 % (SEQ-08).
- **Respirations** : les photos de terrain de SEQ-05 et le noir avant SEQ-09.

## 5. Motion design

- **Part** : 28 plans sur 50 (56 %), sous le seuil de 60 %. La plus longue suite de plans graphiques en compte 4.
- **Fiches complètes** : 18 plans ont une fiche détaillée (ce que le spectateur comprend, éléments, mouvement, durée, entrée et sortie, style, contraintes, assets) : `v2_6/plan_motion_design.md`.
- **Fil orange** : 3 apparitions seulement (SEQ-04, SEQ-05, SEQ-10).
- **Carte maîtresse** : 4 états du Kenya, plus une carte de l'Afrique. La carte des **sept pays** cités par Vodafone lève visuellement l'ambiguïté des « 51 millions ».
- **Écarté** : pas de 3D, pas de zoom décoratif, pas de morphing d'icônes. Les deux seuls mouvements de caméra sur photo ont une fonction : le panoramique qui révèle l'enseigne de la Banque centrale, et le recadrage de carte de la région de Nairobi.

## 6. Archives et documents

- **Photos réelles utilisées** : R01, R02, R03, R04, R06 et R11, plus R07 en remplacement seulement.
  - **R01** (matatu de 2025) et **R06** (Banque centrale, mars 2007) : **inspectées visuellement**.
  - **R07** : inspectée ; **qualité insuffisante** pour la HD.
  - **R02, R03, R04 et R11** : **non inspectées**. Wikimedia a limité le débit (HTTP 429) et je n'ai pas insisté.
- **Documents à capturer** (pages lues pendant le fact-check, captures non réalisées) : FinAccess 2006 et 2019, *Science* 2016, Hughes & Lonie 2007, Vodafone 2017 et 2022, The Star 2020, Safaricom FY25 (URL exacte à relever), FSD Kenya 2019, OpenEdition (capture manuelle, protégée contre les robots).
- **Non obtenus** :
  - articles d'Agence Ecofin (substitut : citations en typographie) ;
  - archives du Kenya d'avant 2007 ;
  - prototype de Thika ;
  - rue de Kinshasa avec argent mobile.
- **Détails** : `v2_6/plan_sourcing.md` et `v2_6/archives_a_rechercher.md`.

## 7. Images générées

**Aucune.** À produire par LUKOJI :
- 2 illustrations au trait (boucle du microcrédit, conversion SMS → carte SIM) ;
- 2 inserts de reconstitution sur table (SMS reçu, dépôt d'espèces), mentionnés à l'écran, avec une illustration en remplacement ;
- les gabarits graphiques.

Détails : `v2_6/illustrations_a_produire.md`.

## 8. Risques de production

1. **Photos non inspectées** (R02, R03, R04, R11) : elles portent 6 scènes. Il faut les contrôler avant le montage ; un remplacement est prévu pour chacune.
2. **Droits** :
   - les citations de documents sont à confirmer ;
   - la page de l'article de *Science* (AAAS) relève d'un risque majeur, avec un remplacement prévu (page MIT News ou typographie).
3. **Matatu de 2025 (SEQ-01)** : il s'agit d'une image d'illustration au format portrait, avec une personne visible et une enseigne publicitaire. Il faudra un recadrage 16:9 et la mention de date. Une photo datée d'avant 2007 serait préférable (piste).
4. **Répétitions** : la page Vodafone 2017, l'agent de Nairobi et la Banque centrale apparaissent chacun dans 3 scènes, avec des recadrages différents.
5. **Production** :
   - 2 inserts à tourner ;
   - sons et musique à sélectionner et créditer (Freesound, musique libre ou originale) ;
   - un plan tourné à Kinshasa serait préférable à la photo de 2013.
6. **Sources fragiles** (rappel) : faits d'Agence Ecofin non relus et présentation de thèse non relue. Les affichages restent attribués.

## 9. Résultats des contrôles

- **QC du storyboard** (`v2_6/qc_storyboard.md`) : **BLOQUANT 0 · RISQUE MAJEUR 9 · ALERTE 20 · RECOMMANDATION 4 · CONFORME 17**. Les 9 risques majeurs se répartissent ainsi : 8 portent sur les photos non inspectées, 1 sur les droits de *Science*.
- **Contrôle du moteur** (évaluation à l'export, `v2_6/qc.md`) :
  - **0 bloquant**, 3 alertes déjà connues (faits F13, F70 et F71 inutilisables, sources lues par l'agent, H2 écarté) ;
  - voix off reconstituée mot pour mot ;
  - JSON conforme au schéma `lukoji.storyboard/1.0`.
- **Statut** : la commande `story qc` n'a **pas** été lancée, car elle ferait passer le projet en `storyboard_review`. Le projet reste en `storyboard_draft`, comme demandé.

## 10. Tests

`python3 -m pytest -q` : **133 passed**, dont un nouveau test. Il vérifie :
- l'empreinte du script verrouillé ;
- la voix off reconstituée mot pour mot ;
- l'absence d'image générée ;
- les mentions à l'écran ;
- que les faits affichés appartiennent aux faits de la séquence validée.

## 11. Recommandation

**Prêt pour une revue humaine du storyboard, sous réserve.** Avant de valider le storyboard (`story qc`, puis `story approve --etape storyboard`), il faut :
1. inspecter R02, R03, R04 et R11 ;
2. décider de l'image d'ouverture (matatu de 2025 ou photo d'avant 2007 à trouver) ;
3. confirmer les droits de citation, en particulier pour *Science* ;
4. accepter les deux inserts de reconstitution ou leur remplacement par des illustrations.

## Fichiers

- **Rapport** : `docs/stories/STO-20261127-001/RAPPORT_PHASE_2_6.md`
- **Storyboard et exports** : `docs/stories/STO-20261127-001/v2_6/` (`storyboard.json`, `storyboard.md`, `storyboard_production.md`, `script.md`, `bundle.json`, `media_center.html`)
- **Plans** : `plan_sourcing.md`, `archives_a_rechercher.md`, `illustrations_a_produire.md`, `plan_motion_design.md`, `plan_sound_design.md`, `scenes_a_risque.md`
- **Contrôles** : `qc_storyboard.md` et `.json`, `qc.md` et `.json`
- **Sources** : `research/stories/mpesa/v2_6/` (`build_storyboard_v2_6.py`, `storyboard_v2_6.json`, `ressources_visuelles_v2_6.json`, `qc_storyboard_v2_6.py`)
