# Story Engine (phase 2)

Transforme un sujet **validé** en projet narratif prêt pour le moteur vidéo (phase 3).
Rôles :
- l'**auteur** (agent de rédaction ou éditeur) écrit le dossier d'angle, les hooks, la structure, le script, la direction artistique et le storyboard, en documents JSON ;
- le **moteur** relie chaque phrase aux faits et aux preuves, calcule durées et scores, contrôle la qualité, versionne tout, applique les statuts et les validations, puis exporte.

Le code ne produit aucun texte : rien n'est inventé par gabarit.

## Modules (`src/lukoji_engine/story/`)

| Module | Rôle |
|---|---|
| `project.py` | projets, 11 statuts, versions de chaque élément et de leurs dépendances, éléments obsolètes, ré-attachement, comparaison de versions, validations, journal |
| `research.py` | dossier factuel construit depuis la base ; **règle d'usage** de chaque fait : libre, attribution obligatoire, prudence obligatoire ou interdit ; vérification de la recherche |
| `factcheck.py` | contrôle d'un passage de voix off : faits cités, attribution, prudence, **chaque chiffre prononcé doit figurer dans un fait cité ou ses preuves** |
| `hooks.py` | Hook Engine : 8 approches obligatoires, durée, 8 critères notés 1 à 5 et justifiés, plafonds automatiques (surenchère → honnêteté ≤ 2 ; problème factuel → hook éliminé), recommandation |
| `narrative.py` | Narrative Engine : catalogue de 9 structures, choix justifié, alternatives écartées, ouverture, conclusion et étape « limites » |
| `script.py` | Script Engine : mots et durée par séquence, sources rattachées, hook repris en ouverture, phrases longues, répétitions, formules creuses, transitions génériques, durée du format |
| `storyboard.py` | Storyboard Engine : découpage **exact** de la voix off, durées, variété, authenticité et mentions à l'écran, raison narrative |
| `visual.py` | Visual Director : direction propre au projet, palette de la charte (ou écart justifié), 6 catégories de visuels, comparaison avec les autres projets |
| `qc.py` | contrôle qualité : 5 catégories, scores, bloquants, alertes, suggestions, statut |
| `engine.py` | orchestration : enregistrer, contrôler, valider, modifier un hook ou une séquence, finaliser |
| `export.py` | exports Markdown et JSON (`lukoji.storyboard/1.0`), validateur du schéma |
| `text.py` | outils de texte français (durée, nombres, répétitions, clichés) |

Règles : `config/story.toml` (débit de 150 mots/min, formats, hooks, lexiques, types visuels, poids du QC).

## Statuts et validations

```
research_pending → research_verified → structure_draft → structure_approved → script_draft → script_review
→ script_approved → storyboard_draft → storyboard_review → storyboard_approved → ready_for_phase3
```

- Un projet n'est créé que depuis un sujet **« valide »**. Le sujet passe alors « en_production » (cycle de la phase 1).
- `research_verified` exige au moins 3 faits clés confirmés et une analyse de l'angle.
- `*_draft` : un élément de l'étape a été enregistré.
- `*_review` : le QC ne relève aucun bloquant pour l'étape.
- `*_approved` : **validation humaine** (`story approve`), liée aux versions exactes et à un QC exécuté sur ces versions.
- **Brouillons anticipés** : on peut rédiger le script ou le storyboard avant la validation de l'étape précédente. Ils sont versionnés et contrôlés, mais ne font pas avancer le statut. Aucune validation n'est jamais automatique.
- Modifier un élément déjà validé ramène le projet au brouillon de l'étape. Les éléments dépendants deviennent « obsolètes » (bloquant au QC) et sont conservés, jamais effacés.

## Commandes

```bash
./bin/lukoji sujets valider SUJ-… --note "…"                 # décision éditoriale (phase 1)
./bin/lukoji recherche completer SUJ-… dossier.json --captures research/captures/…   # recherche complémentaire
./bin/lukoji story create SUJ-… [--format documentaire_long|short]
./bin/lukoji story list | show STO-…
./bin/lukoji story research STO-… --file analyse_angle.json   # dossier factuel + vérification
./bin/lukoji story hooks STO-… --file hooks.json               # ou --choisir H3 --note "…" | --modifier H2 --json '{…}'
./bin/lukoji story structure STO-… --file structure.json
./bin/lukoji story script STO-… --file script.json             # ou --sequence SEQ-04 --json '{"voix_off": "…"}'
./bin/lukoji story direction STO-… --file direction.json
./bin/lukoji story storyboard STO-… --file storyboard.json     # régénérable sans toucher au script
./bin/lukoji story qc STO-… [--json-out rapport.json]
./bin/lukoji story approve STO-… --etape structure|script|storyboard --note "…"
./bin/lukoji story finalize STO-…                              # → ready_for_phase3 (QC sans bloquant exigé)
./bin/lukoji story versions STO-… [--element script] · story diff STO-… --element script 3 4
./bin/lukoji story export STO-… --out dossier/                 # script.md, storyboard.json/.md, direction, vérification, QC, hooks, bundle
./bin/lukoji story html STO-… --out page.html                  # Media Center : page projet (lecture seule)
```

## Capture des sources sans texte intégral

`scripts/capture_sources.py urls.txt dossier --extraits-seulement --motifs "…"` : le moteur lit la page complète, garde son empreinte SHA-256 et au plus 60 phrases exactes de 400 caractères maximum, puis supprime le texte intégral. Les citations sont vérifiées contre ces phrases ; un séparateur empêche une citation d'enjamber deux phrases non contiguës.
