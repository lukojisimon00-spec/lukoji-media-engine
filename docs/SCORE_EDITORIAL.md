# Score éditorial — formule v1.0

Le score est une **aide au tri**, pas une vérité. Il est publié en **quatre axes séparés**, puis combiné en un
indice de priorité. Paramètres : `config/research.toml › [score]`. Code : `src/lukoji_engine/scoring.py`.

## 1. Attrait (0–100) — jugement éditorial, justifié

Six critères notés de 1 à 5. Chaque note exige une **justification écrite** ; une justification manquante est signalée.

| Critère | Poids |
|---|---|
| Potentiel narratif | 0,22 |
| Intérêt du public | 0,20 |
| Originalité de l'angle | 0,16 |
| Potentiel visuel | 0,14 |
| Potentiel de hook | 0,14 |
| Pertinence pour LUKOJI MEDIA | 0,14 |

`attrait = 100 × Σ poids × (note − 1) / 4`. Une note de 1 partout donne 0, une note de 5 partout donne 100.

## 2. Solidité (0–100) — CALCULÉE, jamais déclarée

Elle se fonde uniquement sur les sources réellement consultées et sur le statut calculé des faits :

`solidité = 60 × (faits clés confirmés / faits clés) + 25 × min(1, organisations A/B probantes / 3) + 15 × [au moins une source A probante] − 15 × (faits clés contradictoires)`

Les opinions et les hypothèses ne comptent pas comme faits clés.

### Statut d'un fait (calculé)

Une preuve est **probante** si :
- la page a été consultée : par le moteur (`page_verifiee`, extrait **retrouvé** dans le texte) ou par l'agent de lecture (`page_lue_agent`, extrait rapporté mot pour mot) ;
- la source n'est pas indisponible ;
- l'extrait n'est pas introuvable dans la page récupérée.

Un simple **résultat de recherche** (titre et extrait d'un moteur) n'est **jamais** probant.

| Statut | Règle |
|---|---|
| confirmé | 1 source **A** probante, ou ≥ 2 sources A/B probantes d'**organisations distinctes** |
| confirmé (sujet sensible) | ≥ 2 organisations A/B distinctes, sans exception, même avec une source A |
| source unique | une seule organisation A/B (ou une seule A sur un sujet sensible) : à recouper |
| contradictoire | au moins une source A/B probante contredit |
| à vérifier | rien de probant, ou seulement des sources C |
| opinion attribuée | opinion documentée et attribuée (ce n'est pas un fait) |
| hypothèse | jamais confirmée par construction |

Deux pages d'un même éditeur (par exemple deux titres d'un même groupe de presse) comptent pour **une** organisation.

## 3. Risques (1–5)

- **Risque factuel** (calculé) : `1 + arrondi(4 × part des faits clés non confirmés)`, + 1 en cas de contradiction (maximum 5).
- **Risque juridique** (déclaré et justifié) : minimum 3 pour les familles « scandale » et « enquête », puisque des personnes ou des organisations y sont mises en cause.

## 4. Effort

**Difficulté de production** de 1 à 5, déclarée et justifiée.

## Indice de priorité

`priorité = attrait × solidité/100 × (1 − 0,10 × (risque max − 1)) × (1 − 0,05 × (difficulté − 1))`

## Signalements et classement

Un sujet est **signalé** (non prioritaire) dans l'un de ces cas :
- `insuffisamment_documente` : solidité < 50 ;
- `risque_juridique_eleve` : risque juridique ≥ 4 ;
- `risque_factuel_eleve` : risque factuel ≥ 4 ;
- `contradictions_sur_faits_cles`.

Les sujets signalés sont **toujours classés après** les sujets sains, quel que soit leur attrait. Un sujet risqué ou mal documenté n'est jamais favorisé.

Autres signalements, informatifs :
- `format_non_soutenu:<format>` : les faits confirmés ne suffisent pas pour ce format ;
- `angle_similaire_a_un_contenu_existant` ;
- `categorie_source_declaree_a_revoir` : domaine absent du registre, catégorie proposée par le chercheur ;
- `famille_sensible:recoupement_renforce`.

## Formats réellement soutenus

| Format | Condition minimale |
|---|---|
| Short / Reel | ≥ 1 fait clé confirmé et une accroche |
| Affiche | ≥ 1 fait ou chiffre clé confirmé |
| Documentaire 8–10 min | ≥ 4 faits confirmés et ≥ 3 organisations A/B |
| Série | ≥ 6 faits confirmés, ≥ 3 organisations A/B, ≥ 2 épisodes |

## Limites connues

- Les six notes d'attrait restent un **jugement**. La formule rend ce jugement lisible et comparable, mais ne le rend pas objectif.
- Les poids sont des choix éditoriaux de départ. Ils devront être recalibrés en phase 8 avec les statistiques réelles.
- La solidité mesure la **documentation disponible**, pas la vérité absolue : deux médias peuvent reprendre la même erreur. C'est pourquoi les sources primaires (A) et la diversité des organisations sont valorisées.
