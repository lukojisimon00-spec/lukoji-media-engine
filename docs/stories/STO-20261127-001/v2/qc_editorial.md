# QC éditorial — version 2

**Verdict automatique : PRÊT POUR LA VALIDATION HUMAINE (non validé)**

> Aucun score global : une erreur bloquante n'est jamais compensée par d'autres résultats. Ce verdict ne vaut pas validation : seules les décisions de l'éditeur (dernier volet) peuvent valider le pilote.

## QC technique

28 contrôle(s) ok · 0 bloquant(s) · 0 alerte(s)

| Contrôle | Résultat | Détail |
|---|---|---|
| export présent : script.md | ok |  |
| export présent : storyboard.md | ok |  |
| export présent : storyboard.json | ok |  |
| export présent : direction_artistique.md | ok |  |
| export présent : verification_factuelle.md | ok |  |
| export présent : qc.md | ok |  |
| export présent : qc.json | ok |  |
| export présent : bundle.json | ok |  |
| export présent : hooks.md | ok |  |
| export présent : registre_factuel.md | ok |  |
| export présent : registre_factuel.json | ok |  |
| JSON lisible : storyboard.json | ok |  |
| JSON lisible : bundle.json | ok |  |
| JSON lisible : qc.json | ok |  |
| JSON lisible : registre_factuel.json | ok |  |
| storyboard.json conforme au schéma lukoji.storyboard/1.0 | ok | 0 erreur(s) |
| intégrité de la base (PRAGMA integrity_check) | ok | ok |
| version 1 conservée : research v2 | ok |  |
| version 1 conservée : hooks v2 | ok |  |
| version 1 conservée : structure v2 | ok |  |
| version 1 conservée : script v9 | ok |  |
| version 1 conservée : storyboard v2 | ok |  |
| version 1 conservée : visual v1 | ok |  |
| version 2 créée (script postérieur à v9) | ok | script v13 |
| aucune validation humaine enregistrée par l'agent | ok | 0 validation(s) |
| statut inchangé (structure_draft) | ok | structure_draft |
| durée estimée dans la cible 6–8 min | ok | 968 mots · ≈ 392.6 s |
| storyboard synchronisé mot pour mot avec le script | ok |  |

## QC factuel

17 contrôle(s) ok · 0 bloquant(s) · 1 alerte(s)

| Contrôle | Résultat | Détail |
|---|---|---|
| chaque fait cité figure au registre v2 | ok |  |
| aucun fait incertain ou exclu dans la voix off | ok |  |
| chaque formulation du registre se retrouve mot pour mot dans la voix off | ok |  |
| « corroborated » = au moins deux organisations consultées | ok |  |
| un communiqué d'entreprise n'est jamais compté comme corroboration indépendante | ok |  |
| pas de régression : chiffre de 22 % (origine non établie, enquête postérieure au lancement) | ok |  |
| pas de régression : chiffre de 77 % (base non établie) | ok |  |
| pas de régression : « sous le matelas » (figure de style prise au pied de la lettre en v1) | ok |  |
| pas de régression : « 400 agences bancaires » (contredit par la Banque centrale) | ok |  |
| pas de régression : part de 90,8 % (indicateur non établi) | ok |  |
| pas de régression : date « 2018 » des sénateurs (événement de novembre 2020) | ok |  |
| pas de régression : « trop dominant » (non attribuable aux sénateurs) | ok |  |
| pas de régression : « thèse publiée » (c'est une présentation de thèse) | ok |  |
| pas de régression : glose « maison familiale » | ok |  |
| pas de régression : glose non sourcée sur la dépendance du pays | ok |  |
| pas de régression : jour exact du lancement (Vodafone seule) | ok |  |
| chaque fait à source unique a une attribution déclarée | ok |  |
| répartition des faits utilisés | info | confirmed 2 · corroborated 2 · single_source 24 |
| part des faits utilisés reposant sur une seule organisation | alerte | 24 / 28 faits : la majorité du récit repose sur une seule source par fait |

## QC narratif

11 contrôle(s) ok · 0 bloquant(s) · 0 alerte(s)

| Contrôle | Résultat | Détail |
|---|---|---|
| le microcrédit n'est pas révélé dans l'ouverture (SEQ-01, SEQ-02) | ok | première mention : SEQ-03 |
| le rebondissement (microcrédit) n'est raconté qu'une fois | ok | 1 séquence(s) |
| le hook choisi ouvre bien le script | ok | H9 |
| le hook choisi ne révèle pas la réponse | ok |  |
| aucune formule artificielle relevée par l'audit | ok |  |
| aucune transition ne répète la première phrase de la séquence suivante | ok |  |
| « Selon » en tête de phrase limité (≤ 5) | ok | 5 phrase(s) |
| aucune phrase de plus de 28 mots | ok | max 28 mots |
| phrases courtes de rupture présentes (≥ 4) | ok | 14 phrase(s) de 6 mots ou moins |
| aucune séquence ne dépasse 20 % de la durée | ok | SEQ-08 : 186 mots / 968 |
| la RDC est préparée avant la conclusion | ok |  |

## QC visuel

8 contrôle(s) ok · 0 bloquant(s) · 2 alerte(s)

| Contrôle | Résultat | Détail |
|---|---|---|
| motion design ≤ 60 % des scènes | ok | 26/44 (59%) |
| aucune caméra 3D simulée | ok |  |
| aucun zoom lent | ok |  |
| aucune reconstitution impossible à produire gratuitement | ok |  |
| aucune image générée | ok |  |
| chaque scène « authentique » repose sur une ressource identifiée (métadonnées vérifiées ou page à capturer) | ok |  |
| chaque image symbolique ou illustration porte une mention à l'écran | ok |  |
| fil orange utilisé avec parcimonie (≤ 3 apparitions) | ok | 3 apparition(s) déclarée(s) |
| pas plus de 4 scènes de motion design consécutives | alerte | suite maximale : 5 |
| ressources à capturer ou à produire en Phase 3 | info | R12, R13, R14, R20, R21, R22, R24, R25 |
| ressources non obtenues (substituts prévus) | info | R15 Captures des articles Agence Ecofin (leçon kenyane, sénateurs) ; R16 Archive photo du Kenya au milieu des années 2000 (gare routière, transport d'argent) ; R17 Image du prototype de Thika (2005-2007) ; R18 Communiqué original de la Banque centrale du Kenya (27 janvier 2009) ; R19 Rue de Kinshasa avec enseignes d'argent mobile |
| contenu visuel des photos contrôlé par un humain | alerte | métadonnées seules lues par l'agent : contrôle visuel à faire par l'éditeur |

## QC éditorial humain (décisions en attente)

0 contrôle(s) ok · 0 bloquant(s) · 7 alerte(s)

| Contrôle | Résultat | Détail |
|---|---|---|
| Valider (ou non) la structure v2 — étape « structure » (commande story approve, par l'éditeur seulement). | alerte | décision humaine en attente — jamais remplie par l'agent |
| Choix du hook : H9 (choix éditorial) contre H1 (recommandation du score automatique). | alerte | décision humaine en attente — jamais remplie par l'agent |
| Accepter que la majorité des faits reposent sur une seule organisation, ou demander des corroborations. | alerte | décision humaine en attente — jamais remplie par l'agent |
| Décider si la menace des sénateurs, datée par indices concordants, peut rester avec « novembre 2020 ». | alerte | décision humaine en attente — jamais remplie par l'agent |
| Contrôler visuellement les photos Wikimedia retenues (R01–R04, R06, R11). | alerte | décision humaine en attente — jamais remplie par l'agent |
| Titre du projet en base (« le prêt par SMS … révolution ») : à corriger par l'éditeur ; le script v2 porte « le détournement qui a changé l'argent au Kenya ». | alerte | décision humaine en attente — jamais remplie par l'agent |
| Valider le script puis le storyboard dans l'ordre, après la structure. | alerte | décision humaine en attente — jamais remplie par l'agent |
| QC automatique du moteur (pour mémoire, non décisionnel) | info | QC n° 6 : a_revoir · 95.2 |
