# Rapport technique — Phase 1 : recherche, veille et propositions éditoriales

Date : 27 novembre 2026. Base : phase 0 validée (commit `8cb312a`), conservée sans régression.

## 1. Livrables

| # | Livrable | Emplacement | État |
|---|---|---|---|
| 1 | Moteur de recherche (collecteurs et import de recherche assistée) | `providers.py`, `subjects.py`, `scripts/capture_sources.py` | ✅ fonctionnel ; collecteurs limités par le réseau (§4) |
| 2 | Gestion des sources (URL, A/B/C, consultation, disponibilité, extraits) | `sources.py`, `config/research.toml` | ✅ |
| 3 | Système de notation transparent | `scoring.py`, [SCORE_EDITORIAL.md](SCORE_EDITORIAL.md) | ✅ |
| 4 | Détection des doublons (thème, angle, entités, blog LUKOJI) | `textsim.py`, `subjects.find_duplicates` | ✅ |
| 5 | Propositions (3 à 5 par session, fiche complète) | `subjects.import_dossier` | ✅ |
| 6 | Media Center V0 (CLI et page HTML statique en lecture seule) | `mediacenter.py`, `./bin/lukoji sujets …` | ✅ |
| 7 | Base de données mise à jour (migration 2, 10 tables) | `db.py` | ✅ |
| 8 | Tests automatisés | `tests/test_research.py` (43), suite complète 86/86 | ✅ |
| 9 | Recherche réelle, 5 propositions | `research/dossiers/2026-11-27.json`, base `SUJ-20261127-001…005` | ✅ |
| 10 | Rapport technique | ce document, [RECHERCHE.md](RECHERCHE.md) | ✅ |
| 11 | Rapport éditorial | [propositions/RAPPORT_EDITORIAL_2026-11-27.md](propositions/RAPPORT_EDITORIAL_2026-11-27.md) | ✅ |
| 12 | Reproduction des tests | §6 | ✅ |

## 2. Inspection initiale (avant développement)

- Git : branche `ccr-3b5e8ca0-t16yir` propre et synchronisée avec GitHub (`8cb312a`).
- Modules de la phase 0 réutilisés sans réécriture : configuration (ajout du fichier `research`), journal JSON, base (migration ajoutée), CLI (commandes ajoutées).
- Base : schéma v1 (6 tables), désormais en v2. Journal : `var/logs/engine.jsonl`, qui trace aussi les collectes, les imports et les décisions.
- **Réseau** : l'environnement « Default » bloque toutes les sources de recherche (Wikipédia, GDELT, RSS, presse : 403 du proxy).

## 3. Architecture retenue : aucune invention possible

Le moteur Python ne rédige rien et ne « sait » rien : il **découvre, contrôle et classe**.
- **Découverte** : collecteurs automatiques, ou recherche web réelle de l'agent.
- **Lecture** : pages récupérées par le moteur, ou lues par l'agent.
- **Synthèse** (angle, accroche, récit) : dossier JSON rédigé par l'agent de recherche.
- **Contrôle** : le moteur, sur des règles calculées.
- **Décision** : vous.

| Garde-fou | Mise en œuvre | Test |
|---|---|---|
| URL valides et publiques | schéma, hôte, extension, IP privées, domaines d'exemple, identifiants, espaces | `test_invalid_urls_are_rejected` (10 cas) |
| Source réellement consultée | niveau obligatoire ; `resultat_recherche` jamais probant | `test_search_results_alone_are_insufficient` |
| Citation exacte | l'extrait doit figurer dans le texte récupéré (typographie seule tolérée) | `test_excerpt_not_found_in_page_is_not_evidence` |
| Source indisponible | jamais probante | `test_unavailable_source_is_never_probative` |
| Réseau bloqué | la lecture de l'agent est conservée avec une limite explicite ; la session est marquée `termine_avec_limites` | `test_blocked_environment_keeps_agent_reading…` |
| Captures intègres | empreinte SHA-256 contrôlée ; capture modifiée = refus | `test_engine_captures_are_used_and_integrity_checked` |
| Indépendance des sources | comptage par organisation ; plateforme (arXiv) = auteur réel | `test_claim_status_rules`, `test_platform_sources…` |
| Échec de collecte | erreur enregistrée, aucun résultat fabriqué | `test_provider_failure_is_reported_never_fabricated` |
| Atomicité | import en échec = transaction annulée, session marquée `echec` | `test_failed_import_marks_run_as_failed` |

## 4. Limites réelles constatées

| Outil | Constat | Conséquence |
|---|---|---|
| Réseau « Default » (cette session) | Wikipédia, GDELT, RSS et presse bloqués | collecteurs et récupération en échec propre |
| Environnement **« LUKOJI Recherche »** (créé pendant la phase avec votre accord, 20 hôtes) | cette session n'a pas pu y basculer (règle de la plateforme) | pages capturées par une **session dédiée** sur cet environnement (21/25) |
| Wikipédia API | HTTP 429 même avec réseau ouvert (l'agent utilisateur ne contient pas d'adresse de contact) | collecteur Wikipédia à fiabiliser (adresse de contact générique à décider) |
| GDELT | connexion interrompue (`Connection reset by peer`) | à réessayer, ou à remplacer par les flux RSS |
| Sites refusant les lecteurs automatiques | Safaricom Newsroom, History Today, Reviews in History (HTTP 403) | sources non probantes |
| Recherche web de l'agent | refuse 12 grands médias (Le Monde, RFI, BBC, AP, NYT…) | diversité francophone réduite |
| Agent de lecture | soumis au réseau de la session | 1 page lue sur 25 depuis « Default » |
| Paywalls | African Business : seul le chapeau est lisible | signalé dans les limites de la source |

**Droit d'auteur** : les textes intégraux capturés sont conservés hors Git (`.gitignore`). Seul le manifeste (URL, date, SHA-256) est
versionné. ⚠ La branche `captures-recherche-2026-11-27`, poussée par la session de capture, contient ces textes : à supprimer
sur GitHub si vous le souhaitez (je ne l'ai pas fait sans votre accord).

## 5. Résultats de la recherche réelle

- Sessions de recherche : n° 1 (collecteurs, `echec`, 0 piste, aucune inventée) ; n° 2 (assistée, `termine`, 5 propositions, 0 refusée).
- 22 sources :
  - 20 `page_verifiee` ;
  - 2 non probantes (HTTP 403).
  - Par catégorie : 7 A, 10 B, 5 C (dont 1 classée C par défaut : History Today, domaine absent du registre).
  - Origine de la catégorie : 11 registre, 10 déclarées (signalées « à revoir »), 1 par défaut.
- 37 faits :
  - 20 confirmés et 11 en source unique (à recouper) ;
  - 4 à vérifier ;
  - 1 contradictoire (le récit populaire de la tulipomanie, démenti) ;
  - 1 hypothèse attribuée.
- **57 extraits sur 57 retrouvés mot pour mot** dans les pages.
- Doublons : aucun avec la base ni avec les 10 articles du blog (similarité maximale 0,045 : M-Pesa face à l'article Wave).

## 6. Reproduire

```bash
python3 -m pytest -q                                   # 86 tests (≈ 3 min), dont 43 pour la phase 1
python3 -m pytest -q tests/test_research.py            # phase 1 seule (≈ 2 s, données SIMULÉES, sans réseau)
./bin/lukoji recherche collecter "Air Afrique"         # collecteurs réels
# Dans une session sur l'environnement « LUKOJI Recherche » :
python3 scripts/capture_sources.py research/urls_2026-11-27.txt research/captures/2026-11-27
# Puis, avec les captures :
./bin/lukoji recherche importer research/dossiers/2026-11-27.json --captures research/captures/2026-11-27
./bin/lukoji sujets list | show | compare | html | markdown
```

Vérifié le 27/11 : sur une base vierge, l'import redonne exactement les mêmes scores ; un second import refuse les 5 propositions (doublons).
Note : sur une base qui contient déjà ces sujets, un nouvel import est **refusé comme doublon**, ce qui est le comportement attendu.
Utiliser une base vierge (`LUKOJI_PATHS__DB=/tmp/test.sqlite3`) pour rejouer l'import.

## 7. Ce qui n'a pas été fait (hors périmètre)

Aucun script ni storyboard (phase 2), aucune publication, aucun abonnement, aucune modification des projets externes.
