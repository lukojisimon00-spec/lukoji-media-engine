# Révision éditoriale corrective — pilote M-Pesa, version 2

`STO-20261127-001` · révision du 27/11/2026 à partir de l'audit éditorial humain (commit `70d0f17`).

**Statut : NON VALIDÉ.** La version 2 est présentée pour validation humaine. Le projet reste en `structure_draft` et aucune validation n'a été enregistrée.

---

## 1. Versions

La version 1 reste consultable :
- dans la base : research v2, hooks v2, structure v2, script v9, storyboard v2, visual v1 ;
- dans les fichiers : `docs/stories/STO-20261127-001/*.md|json`, que la révision n'a pas modifiés.

| Élément | Version 1 (audit) | Version 2 (courante) | Fichier source v2 |
|---|---|---|---|
| Dossier factuel | research v2 | **research v3** | `research/stories/mpesa/v2/recherche_complementaire_v2.json` + `analyse_angle_v2.json` |
| Hooks | hooks v2 | **hooks v3** (8 hooks annotés + H9, H10, H11 ; H9 choisi) | `hooks_v2.json` |
| Structure | structure v2 | **structure v3** | `structure_v2.json` |
| Script | script v9 | **script v13** (v10 à v13 : réécriture puis trois retouches de forme) | `script_v2.json` |
| Direction artistique | visual v1 | **visual v2** | `direction_v2.json` |
| Storyboard | storyboard v2 (58 scènes) | **storyboard v7** (44 scènes ; v3 à v6 : étapes de rééquilibrage) | `storyboard_v2.json` (généré par `build_storyboard_v2.py`) |

La base `var/lukoji.sqlite3` n'est pas versionnée. Les fichiers sources v2 ci-dessus permettent de reconstituer les versions par import.

## 2. Les cinq bloquants

| # | Bloquant | Vérification réellement faite | Décision v2 |
|---|---|---|---|
| B1 | 22 % / 77 % présentés comme antérieurs à M-Pesa | **Page MIT News (2010) relue le 27/11** (session en lecture seule) : enquête de **2008**, menée auprès de **3 000 ménages**, dans des zones représentant **92 %** de la population. Le chiffre de 77 % (« under the mattress… so to speak ») vient d'un working paper ; sa base (ménages ? personnes ?) n'est pas précisée. L'origine du 22 % (« 22 percent of adults ») n'est pas indiquée. Le working paper NBER w16721 n'a **pas** pu être consulté (hôte non autorisé). | **Retirés du script.** Un fait correctement daté (F69) est ajouté au dossier, sans être utilisé. Le contexte « avant M-Pesa » repose désormais sur un chiffre de **2006** (27 %, FinAccess via Agence Ecofin, F51). |
| B2 | Sénateurs « dès 2018 », « trop dominant » | Page Ecofin **non relue** : Cloudflare la bloque (HTTP 403). La date repose sur trois indices concordants :<br>– les liens connexes de l'article sont datés du 09/03/2017 et du 20/02/2018, donc l'article est postérieur ;<br>– sa place dans la numérotation des articles Ecofin le situe entre novembre 2019 et mai 2022 ;<br>– les URL de The Star (`2020-11-18-senators-reignite-push-to-split-safaricom`) et de Techweez (`2020/11/18`) sont datées, mais ces pages n'ont été vues qu'en **résultat de recherche** et non lues.<br>L'acteur est le **comité sénatorial des TIC**. Les sénateurs jugent Safaricom « **de plus en plus dominante** ». Le mot « trop dominant » vient d'un rapport cité dans le même article. | **Fait redaté** (F64, « En novembre 2020 ») avec la formulation exacte. La date de la source S26 est corrigée de 2018-11 à 2020-11. Le point reste à confirmer par l'éditeur (décision humaine). |
| B3 | 90,8 % de parts de marché | La presse kényane (Capital FM, TechCabal, vus en **résultat de recherche** seulement) confirme 90,8 % pour le **trimestre clos fin mars 2025**, contre 94,9 % un an plus tôt, d'après l'Autorité des communications. Ni l'**indicateur** (abonnements, transactions ou valeur ?) ni le rapport original n'ont pu être consultés. | **Retiré du script et du storyboard** (le camembert est supprimé). Il est documenté au dossier comme incertain (F71). |
| B4 | « 400 agences bancaires » (début 2012) | Le communiqué de la Banque centrale du Kenya sur le rapport de supervision 2012 (**résultat de recherche seulement**) indique **1 161 agences en décembre 2011** et 1 272 en décembre 2012. Le chiffre d'Ecofin est donc contredit. Pour comparaison, Safaricom déclarait environ 39 400 agents à fin mars 2012, selon un autre résultat de recherche ; ce chiffre est d'un autre périmètre et n'est pas utilisé. | **Comparaison supprimée**, ainsi que les 30 000 points. L'article Ecofin S24 est signalé comme moins fiable dans son champ « limites ». |
| B5 | 12 scènes « authentiques » sans ressource identifiée | Les métadonnées de 16 fichiers Wikimedia Commons ont été lues via l'API de en.wikipedia.org (URL directe, auteur, date, licence). **Le contenu visuel des images n'a pas été regardé.** | **7 fichiers retenus pour le montage** (R01, R02, R03, R04, R06, R07, R11 — voir §6) ; 4 autres identifiés mais non utilisés. Les pages Vodafone, MIT et OpenEdition sont à capturer. Les archives introuvables sont déclarées **non obtenues** et remplacées par une carte, une typographie ou une illustration mentionnée. Aucune scène ne prétend plus disposer d'une archive qu'elle n'a pas. |

## 3. Corrections factuelles et éditoriales

- **Récit des origines attribué** : la voix off dit « raconte… dans un texte publié par Vodafone », « explique-t-il », « raconte Vodafone ». Le narrateur, Michael Joseph, est identifié : ancien directeur général de Safaricom selon Agence Ecofin, auteur du texte Vodafone de 2017 (F62).
- **Citation réelle au moment pivot** : « Alors nous avons pris un risque » (« So we took a chance », F63).
- **Tension réglementaire documentée** : débat public, puis communiqué de la Banque centrale du **27 janvier 2009** (« la réglementation traîne généralement derrière l'innovation », F66, via Agence Ecofin).
- **Date de lancement** : « mars 2007 », corroborée (F7) ; le jour exact, attesté par Vodafone seule, n'est plus cité.
- **Dates** : paris en ligne datés de l'exercice clos en mars 2022 (F65) ; crédit mobile daté de 2019 (F67) ; projet de baisse des frais présenté comme un **projet** rapporté par des médias kényans (F55).
- **F11** : « depuis 2008 » et seuil de **1,25 $ par jour et par personne**.
- **F12** : « des activités commerciales » au lieu de « le commerce ».
- **Gloses retirées** : « l'argent remonte vers la maison familiale », remplacée par l'interprétation attribuée aux chercheurs (« cela suggère », F68) ; « une infrastructure dont dépend une grande partie d'un pays ».
- **F59** : « thèse publiée » devient « une thèse d'économie, **présentée** dans la Revue de la régulation… selon son auteur ».
- **SEQ-07** : un seul jeu de chiffres d'entreprise (2022). Le passage de « 10 pays » à « sept pays » est supprimé.
- **Titre du script** : « M-Pesa : le détournement qui a changé l'argent au Kenya ». Le titre du **projet en base** (« le prêt par SMS… révolution »), repris dans les en-têtes d'export, n'est pas modifiable par le moteur sans toucher la base : **décision laissée à l'éditeur**.

## 4. Faits retirés, corrigés, incertains

Le détail est dans `registre_factuel.md`.

| Catégorie | Faits |
|---|---|
| Retirés du script | F38 (22 %), F39 (77 %), F47 (30 000 contre 400), F54 (90,8 %), F56 (sénateurs 2018), F57 (paris au présent), F48 (chiffres 2016) ; F13 (Wikipédia seule) toujours exclu |
| Corrigés et remplacés | F56 → F64 ; F57 → F65 ; F38/F39 → F69 (correct, non utilisé) |
| Ajoutés | F62 (Michael Joseph), F63 (citation), F64, F65, F66 (communiqué 2009), F67 (49 plateformes), F68 (interprétation des chercheurs), F69 |
| Incertains (non utilisés) | F70 (agences bancaires, source non lue), F71 (90,8 % selon Capital FM, indicateur inconnu) |
| Toujours à source unique et utilisés | **24 faits sur 28** : la majorité du récit repose sur une seule organisation par fait. Le récit des origines repose sur **Vodafone seule**. Ces faits sont attribués dans la voix off ou à l'écran. |

Le moteur ne permet pas de retirer un fait de son dossier : F38, F39, F47, F54, F56 et F57 y restent avec leur statut calculé. Leur exclusion est portée par le registre v2 et contrôlée par le QC éditorial v2 et par `tests/test_pilote_mpesa_v2.py`.

## 5. Sources

**Réellement vérifiées** :
- **Captures du moteur du 27/11** (extraits seulement), sur lesquelles toutes les citations de la v2 ont été vérifiées : Vodafone S6, S31, S32 ; Agence Ecofin S24 à S30 ; MIT News S7, S33 ; OpenEdition S34 ; Wikipédia S8.
- **Relu le 27/11 pendant la révision** : la page MIT News 2010 (S33).
- **Lues via l'API de en.wikipedia.org** : les métadonnées des fichiers Wikimedia Commons.

**Non accessibles** (déclarées comme telles, jamais présentées comme consultées) :
- **agenceecofin.com** : bloqué par Cloudflare (HTTP 403) depuis l'environnement de recherche ;
- **hors du réseau autorisé** : nber.org (working paper Jack & Suri), centralbank.go.ke (communiqués, rapports de supervision), ca.go.ke (rapports statistiques), the-star.co.ke, capitalfm.africa, commons.wikimedia.org en direct, upload.wikimedia.org ;
- **jamais consultés** : l'article de **Science** (2016), le rapport **FinAccess 2019** et les rapports annuels de **Safaricom**.

Sources ajoutées au dossier au niveau `resultat_recherche` (**non probantes**) : S35 (Banque centrale du Kenya), S36 (The Star), S37 (Capital FM).

## 6. Ressources visuelles

Le détail est dans `ressources_visuelles.md` et `storyboard_production.md`.

- **Obtenues, métadonnées vérifiées** (contenu visuel à contrôler par l'éditeur) :
  - R01 : matatu, Nairobi, 2025, CC BY 4.0 ;
  - R02 : agent M-PESA et Equity, Nairobi, 2016, CC BY-SA 2.0 ;
  - R03 : kiosque, Nairobi, 2026, CC BY 4.0 ;
  - R04 : kiosque M-Pesa, Kenya, date des métadonnées **non fiable**, CC BY-SA 3.0 ;
  - R06 : Banque centrale du Kenya, **7 mars 2007**, CC BY 2.0 ;
  - R07 : Banque centrale du Kenya, 2016, CC BY-SA 4.0 ;
  - R11 : Kinshasa, boulevard du 30 Juin, 2013, CC BY 2.0.
- **Identifiées mais non utilisées** : R05 (point de paiement, pays non précisé), R08 et R09 (Thika aujourd'hui), R10 (Tanzanie).
- **À capturer** (pages publiques accessibles) : R12 (Vodafone 2017), R13 (MIT News 2016), R14 (OpenEdition), R24 (Vodafone 2022), R25 (MIT News 2010).
- **À produire** : carte (Natural Earth), graphiques, illustrations au trait, sons (Freesound).
- **Non obtenues** :
  - R15 : captures des articles d'Agence Ecofin ;
  - R16 : archive du Kenya au milieu des années 2000 ;
  - R17 : prototype de Thika ;
  - R18 : communiqué original de 2009 ;
  - R19 : rue de Kinshasa avec enseignes d'argent mobile.

## 7. Contrôle qualité

- **QC du moteur** (n° 6) : 95,2/100, 0 bloquant, 3 alertes : F13, F70 et F71 inutilisables (attendu), sources S35 à S37 non vérifiées (attendu), surenchère de H2 (hook écarté). Ce score n'est **pas** un indicateur éditorial.
- **QC éditorial v2** (`qc_editorial.md`) : 5 volets séparés, sans score global. Verdict automatique : **prêt pour la validation humaine (non validé)**. 0 bloquant.
- **Alertes restantes** :
  - 24 faits sur 28 reposent sur une seule source ;
  - une suite de 5 scènes de motion design (fin de SEQ-08, début de SEQ-09) ;
  - le contenu visuel des photos n'a pas encore été contrôlé.
- **Volet humain** : 7 décisions en attente, jamais remplies par l'agent.

## 8. Tests

`python3 -m pytest -q` : **121 passed**, soit les 105 tests existants et 16 nouveaux dans `tests/test_pilote_mpesa_v2.py`. Ces nouveaux tests vérifient :
- que la version 1 reste consultable ;
- la conformité du storyboard v2 au schéma ;
- la synchronisation mot pour mot avec le script ;
- l'absence de fait exclu ou incertain ;
- l'absence de régression sur les corrections de l'audit ;
- que le microcrédit n'est révélé qu'une fois ;
- que les scènes authentiques reposent sur une ressource identifiée ;
- que le QC éditorial ne déclare jamais le pilote validé.

## 9. Ce qui n'a pas été fait

- Aucune validation, aucun changement de statut, aucune modification du moteur.
- Aucune image générée ni téléchargée, aucun rendu.
- Pas de Phase 3, aucune publication, aucune dépense.
