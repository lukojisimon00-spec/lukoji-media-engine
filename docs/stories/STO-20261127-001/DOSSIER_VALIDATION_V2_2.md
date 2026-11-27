# Dossier de validation — « Quand les clients ont changé le produit »

`STO-20261127-001` · préparé le 27/11/2026 (phase 2.5) · **AUCUNE VALIDATION N'EST ENREGISTRÉE.** Le projet est en `structure_draft` (0 validation en base). Ce document sert à décider ; il n'est pas une décision.

## 1. Contrôle final

| Point | Résultat | Détail |
|---|---|---|
| « 51 millions » (SEQ-07) | **Conforme, ambiguïté orale mineure** | Texte : « En 2022, l'entreprise en revendique plus de 51 millions, servis par 600 000 agents, dans sept pays. Parmi eux, la République démocratique du Congo. » Source lue (Vodafone, 07/03/2022) : « 51 million customers across seven countries ». Le périmètre (sept pays) figure bien dans la phrase, mais en fin de phrase : à l'oral, « 51 millions » peut être entendu un instant comme kényan. Le storyboard affichait déjà « 7 PAYS » à l'écran. Reformulation possible, **non appliquée** : « En 2022, dans sept pays, l'entreprise en revendique plus de 51 millions… » Elle créerait une nouvelle version avant validation |
| Titre | Conforme | « Quand les clients ont changé le produit » : base (`story_projects.title`), script v2.2, exports v2.2 |
| Hook H9 prudent | Conforme | Choisi dans les hooks v5 et identique mot pour mot à l'ouverture de SEQ-01 (« confier son argent à une compagnie de bus ») |
| Cohérence script / structure | Conforme | 10 séquences et 10 étapes, mêmes faits et mêmes transitions (contrôle `v2_2/qc_consolidation.md`, 23/23) |
| Cohérence script / dossier factuel v4 | Conforme | Contrôle factuel du moteur : 0 bloquant (faits connus, attributions présentes, chaque nombre présent dans un fait ou une preuve) ; aucun fait retiré cité ; ni paris en ligne, ni communiqué de 2009 |
| Durée | Conforme | **984 mots (décompte du moteur) · 399,0 s ≈ 6,7 min**, calculée sur le script à 150 mots/min, pauses comprises, et **non** sur le storyboard obsolète (export propre au pilote) |
| Fichiers et base | Identiques | Empreintes SHA-256 des fichiers versionnés = empreintes en base (`v2_2/fiche_validation.json`) |

## 2. Synthèse pour la décision

### Script v2.2 (moteur : script v21)

Le script raconte, en 10 séquences, comment un prototype de microcrédit (selon l'équipe projet et Vodafone) a été détourné par ses usagers, ce que les chercheurs estiment qu'il a changé, et pourquoi sa puissance reste discutée.

**Points solides** :
- un hook documenté par trois sources ;
- la révélation retenue jusqu'à SEQ-03 ;
- une question posée en SEQ-06 et reprise en SEQ-09 ;
- des estimations scientifiques traitées avec prudence ;
- une conclusion qui ne transpose pas le cas kényen à la RDC.

### Structure v6 (moteur : structure v6)

Structure « transformation » : chaque étape a sa fonction, son conflit ou sa question, ses informations indispensables et secondaires, son risque de décrochage et sa transition. Elle est **alignée** sur le script v2.2 et ne cite **aucun** fait retiré. Elle peut servir de base au futur storyboard.

### Risques factuels restants

1. **Origines** : le récit (microcrédit, détournement, « nous avons pris un risque ») ne vient que de l'équipe projet et de Vodafone. Il est **attribué comme tel**, mais aucune source indépendante ne le confirme.
2. **Projet de baisse des frais** (23 → 10 KES d'ici 2028) : rapporté par des médias kényans via Agence Ecofin. Le document de la Banque centrale n'a pas été lu ; c'est à confirmer avant diffusion.
3. **« 51 millions »** : correct, mais l'oral peut induire le spectateur en erreur (voir §1).

### Limites de sources

- **Non relus**, faute d'accès aux sites (protections) : Agence Ecofin (conditions de la Banque centrale, opposition des banques, 7 %, projet de plafonnement, crédit mobile) et la présentation de thèse (auteur non nommé).
- **Science** : lu via une copie hébergée par FinDev Gateway (science.org bloqué).
- **Chiffres d'entreprise** (Vodafone, Safaricom) : déclaratifs, non audités.

### Risques narratifs

- **Densité** : SEQ-08 (146 mots) et SEQ-09 (162 mots) restent les passages où le spectateur risque le plus de décrocher.
- **Témoignages** : aucun témoignage d'usager.
- **Durée des dernières séquences** : SEQ-09 et SEQ-10 se sont allongées pendant la consolidation.

### Recommandation du moteur

| Volet | Recommandation |
|---|---|
| QC du moteur (n° 11) | 0 bloquant en recherche, hooks, structure, script et durée ; 9 bloquants **en visuel uniquement** (storyboard obsolète). **Ces 9 bloquants n'empêchent pas la validation de la structure ni celle du script** : le moteur ne les compte que pour l'étape storyboard |
| Contrôle de consolidation | 23 contrôles, 0 bloquant |
| Recommandation éditoriale (agent, consultative) | **Structure v6 : VALIDABLE.** **Script v2.2 : VALIDABLE SOUS RÉSERVE** de l'acceptation explicite du risque factuel n° 1 (origines attribuées à Vodafone et à l'équipe projet) et du choix de garder ou non la formulation actuelle des « 51 millions » |

Le moteur ne certifie ni la vérité du documentaire ni sa qualité : il vérifie la cohérence et la traçabilité.

## 3. Mécanisme de validation humaine (prêt, non utilisé)

Les validations du script et de la structure sont **distinctes**, **ordonnées** et **liées à des versions exactes**. Ce mécanisme existe déjà dans le moteur (`story approve`) ; il n'a pas été modifié.

### Versions soumises (empreintes : `v2_2/fiche_validation.json`)

| Élément | Version | SHA-256 (début) | Fichier versionné |
|---|---|---|---|
| Dossier factuel | v4 | e05227f4006c | — (base) |
| Hooks | v5 | a89eecdfbad1 | `research/stories/mpesa/v2_2/hooks_v2_2.json` |
| Structure | **v6** | d243c5878317 | `research/stories/mpesa/v2_2/structure_v2_2.json` |
| Script | **v21** (v2.2) | 62bd3ad4d0c8 | `research/stories/mpesa/v2_2/script_v2_2.json` |

### Étapes, sur décision explicite du responsable éditorial

1. **Valider la structure** (statut requis : `structure_draft` ; QC à jour sur les versions courantes ; aucun bloquant en recherche, hooks ou structure) :
   `./bin/lukoji story approve STO-20261127-001 --etape structure --acteur "<nom du responsable>" --note "Structure v6 validée"`
   → statut `structure_approved`, puis `script_draft`, puisque le script existe déjà.
2. **Ouvrir la revue du script** : `./bin/lukoji story qc STO-20261127-001` → `script_review` si aucun bloquant en recherche, hooks, structure ou script.
3. **Valider le script** : `./bin/lukoji story approve STO-20261127-001 --etape script --acteur "<nom du responsable>" --note "Script v2.2 validé"`
   → `script_approved`, puis `storyboard_draft` (le storyboard v7 existe, obsolète).
4. **Verrouiller durablement** : `python3 research/stories/mpesa/v2_2/verrou_validation.py verrou`, puis commit de `docs/stories/STO-20261127-001/VERROU_VALIDATION.json`.
   Cette étape est indispensable : la base `var/lukoji.sqlite3` n'est pas versionnée, et sans ce fichier une validation disparaîtrait avec le conteneur.
5. **Contrôler** : `python3 research/stories/mpesa/v2_2/verrou_validation.py verifier`. Il vérifie que les versions validées sont présentes et inchangées (empreinte recalculée) et n'autorise la reconstruction du storyboard que si la structure **et** le script sont validés **et** que les versions courantes sont exactement les versions validées.

### Garanties et limites du mécanisme

- **Identifiables** : chaque validation enregistre l'étape, l'acteur, la date, la note, le n° de QC et les versions exactes de tous les éléments (`story_approvals`). Le verrou y ajoute les empreintes.
- **Non écrasées** : les éléments ne sont jamais modifiés en place. Toute modification crée une nouvelle version. Modifier une étape validée ramène le projet au brouillon de cette étape et rend les éléments dépendants « obsolètes », sans rien effacer. Les versions validées restent consultables.
- **Immuabilité** : elle est **contrôlée** (empreintes, `verifier`, test automatique) mais **pas imposée au niveau de la base** : une commande SQL directe pourrait encore modifier une ligne. L'imposer exigerait une modification du moteur (déclencheurs SQLite), non faite en phase 2.5 et soumise à votre autorisation.
- **Acteur** : par défaut, le moteur inscrit « editeur ». Toutes les versions de travail produites par l'agent portent aussi cette étiquette. Pour que la validation soit attribuable, **passer le nom réel avec `--acteur`**.
- **Qui lance la commande** : la validation doit venir d'une décision explicite de votre part. Lors d'une phase précédente, une tentative de validation par l'agent a été bloquée par le système de permissions ; le plus sûr est que le responsable éditorial lance lui-même les commandes 1 à 3.

## 4. Ce qui n'a pas été fait

Aucune validation, aucun verrouillage, aucun changement de statut. Le storyboard n'a pas été modifié. Pas de Phase 3, pas de nouvelle recherche, aucune modification du moteur.
