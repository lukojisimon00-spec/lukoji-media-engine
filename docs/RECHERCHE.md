# Moteur de recherche et de propositions éditoriales (phase 1)

## Principe : aucune invention

Le moteur **ne génère jamais de faits**. Il organise et **contrôle** une recherche réelle :

```
Découverte                Lecture                    Contrôle (moteur)               Décision (vous)
───────────               ───────                    ─────────────────               ───────────────
collecteurs auto     →    pages récupérées par  →    URL valides, catégorie A/B/C, →  Media Center V0
(Wikipédia, GDELT,        le moteur (ou lues par     extraits retrouvés dans la page,  valider / rejeter /
 RSS) ou recherche        l'agent de lecture)        statut CALCULÉ de chaque fait,    reporter / remarque
 web de l'agent                                      score, formats, doublons          (journalisé)
```

| Étape | Qui | Ce qui est garanti |
|---|---|---|
| Découverte | collecteurs (`recherche collecter`) ou recherche web de l'agent | Une piste n'est **jamais** une preuve (niveau `resultat_recherche`) |
| Lecture | moteur (`page_verifiee`) ou agent de lecture (`page_lue_agent`) | Chaque source déclare son niveau de consultation ; « lu » n'est jamais revendiqué pour un simple extrait de recherche |
| Synthèse (angle, accroche, récit) | agent de recherche → dossier JSON | Le dossier est **validé** : champs obligatoires, notes justifiées, extraits cités mot pour mot |
| Contrôle | moteur (`recherche importer`) | URL valides et publiques ; extraits **retrouvés** dans le texte récupéré ; statut des faits et score **calculés** ; doublons détectés |
| Décision | éditeur (`sujets valider|rejeter|reporter|reactiver|note`) | Transitions contrôlées, historique horodaté |

## Modules

| Fichier | Rôle |
|---|---|
| `config/research.toml` | familles (17), territoires, collecteurs, **registre des sources** (≈ 60 domaines → organisation, A/B/C), règles de vérification, poids du score, seuils de doublons |
| `src/lukoji_engine/providers.py` | collecteurs Wikipédia (FR/EN), GDELT (actualité mondiale), flux RSS (8 médias) ; échecs signalés, jamais simulés |
| `src/lukoji_engine/sources.py` | validation et normalisation des URL, classement A/B/C, récupération HTML (bibliothèque standard), métadonnées (titre, éditeur, date), vérification d'extraits |
| `src/lukoji_engine/scoring.py` | statut calculé des faits, score en 4 axes, formats réellement soutenus ([formule](SCORE_EDITORIAL.md)) |
| `src/lukoji_engine/textsim.py` | similarité TF-IDF (unigrammes et bigrammes, racinisation légère FR/EN) et Jaccard sur les entités |
| `src/lukoji_engine/subjects.py` | import des dossiers, doublons, cycle de vie, décisions, recherche de sujets abandonnés |
| `src/lukoji_engine/mediacenter.py` | Media Center V0 : liste, fiche, comparaison, page HTML statique |
| `scripts/capture_sources.py` | capture des pages **par le moteur** dans un environnement dont le réseau autorise les hôtes |

## Base de données (migration 2)

| Table | Contenu |
|---|---|
| `research_runs` | chaque session de recherche : mode, paramètres, statut (`termine`, `termine_avec_limites`, `echec`), erreurs |
| `search_hits` | pistes brutes des collecteurs (jamais des preuves) |
| `sources` | URL normalisée unique, organisation, catégorie et origine de la catégorie, dates de publication et de consultation, niveau de consultation, disponibilité, empreinte du texte, limites |
| `subjects` | identifiant `SUJ-AAAAMMJJ-NNN`, sujet, angle, accroche, résumé, formats, notes, score, drapeaux, doublons, statut |
| `claims` / `claim_evidence` | faits (type, importance, statut calculé et motif) et preuves (source, position, extrait, vérification de l'extrait) |
| `subject_events` / `subject_notes` | journal des décisions et remarques |

### Cycle de vie d'un sujet

```
recherche → propose → valide → en_production → produit → publie
              │  ↑       │  ↑          │
              │  └─ reporte ┘          └→ valide (retour)
              └→ rejete → propose (réactivation d'un sujet abandonné)
```

Toute autre transition est refusée. En particulier, il est impossible de publier ou de produire sans validation.

## Doublons

Le nouveau sujet est comparé à tous les sujets en base, aux contenus du registre et aux **articles déjà publiés sur le blog LUKOJI**, lus sans aucune modification. Deux similarités sont calculées :
- **thème** : 0,6 × cosinus TF-IDF (titre, sujet, entités) + 0,4 × Jaccard des entités ;
- **angle** : cosinus TF-IDF des angles narratifs.

| Verdict | Règle | Effet |
|---|---|---|
| `meme_sujet` | thème ≥ 0,55 | proposition **refusée**, avec conseil (réactiver un sujet abandonné, ou trouver un autre angle si le sujet est déjà publié) |
| `angle_similaire` | thème ≥ 0,35 et angle ≥ 0,45 | enregistrée et signalée |
| `sujet_proche` | thème ≥ 0,35 | indiquée dans la fiche |

`sujets search "texte" --status rejete,reporte` retrouve un sujet abandonné.

## Limites réelles des outils (novembre 2026)

1. **Réseau de l'environnement « Default »** : il bloque Wikipédia, GDELT, les flux RSS et les sites de presse. Les collecteurs échouent proprement ; l'échec est enregistré et rien n'est simulé. L'environnement « LUKOJI Recherche » autorise 20 hôtes de recherche ; une session doit **démarrer** sur cet environnement pour en profiter.
2. **Moteur de recherche de l'agent** : il refuse certains domaines (lemonde.fr, rfi.fr, bbc.com, lesechos.fr, liberation.fr, lefigaro.fr, nytimes.com, theguardian.com, apnews.com, ft.com, economist.com, dw.com).
3. **Agent de lecture** : il est soumis au même réseau que la session.
4. **Registre des sources** : un domaine absent est classé C par défaut. Une catégorie déclarée par le chercheur est conservée mais signalée « à revoir ».
5. **Vérification d'extrait** : elle prouve que la citation figure dans la page, pas que la page dit vrai. D'où les règles de recoupement par organisations indépendantes.
6. **Paywalls** : une page partiellement lisible est signalée dans les limites de la source.

## Reproduire

```bash
python3 -m pytest -q tests/test_research.py             # 41 tests, données SIMULÉES, sans réseau
./bin/lukoji recherche collecter "Air Afrique"          # collecteurs réels (échec propre si réseau bloqué)
python3 scripts/capture_sources.py research/urls_2026-11-27.txt research/captures/2026-11-27
./bin/lukoji recherche importer research/dossiers/2026-11-27.json --captures research/captures/2026-11-27
./bin/lukoji sujets list
./bin/lukoji sujets show SUJ-…                          # fiche complète : sources, faits, preuves, score
./bin/lukoji sujets compare SUJ-… SUJ-…
./bin/lukoji sujets valider SUJ-… --note "…"            # ou rejeter / reporter / reactiver / note
./bin/lukoji sujets html --out var/out/media_center.html
```
