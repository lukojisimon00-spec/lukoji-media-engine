# Revue éditoriale finale — pilote M-Pesa

`STO-20261127-001` · revue du 27/11/2026 · document **consultatif** : il prépare une décision humaine et ne vaut pas validation.

## 0. Ce qui a été examiné (vérifié dans le dépôt et dans la base)

| Élément | Version réellement présente | Fichier ou emplacement |
|---|---|---|
| Script | **v2.1** = moteur **v16** (texte identique, vérifié mot pour mot) | `research/stories/mpesa/v2_1/script_v2_1.json`, `docs/stories/STO-20261127-001/v2_1/script.md` |
| Dossier factuel | moteur **v4** (53 faits) | base `var/lukoji.sqlite3` ; export `v2_1/verification_factuelle.md`, `v2_1/bundle.json` |
| Structure | moteur **v4** (contenu identique à v3) | `research/stories/mpesa/v2/structure_v2.json` |
| Hooks | moteur **v4** (contenu identique à v3 ; H9 choisi) | `research/stories/mpesa/v2/hooks_v2.json` |
| Direction artistique | moteur **v3** (contenu identique à v2) | `research/stories/mpesa/v2/direction_v2.json` |
| Storyboard | moteur **v7**, **obsolète** (construit sur le script v13) | `research/stories/mpesa/v2/storyboard_v2.json`, `docs/stories/STO-20261127-001/v2/` |
| Audits précédents | audit humain v1, révision v2, fact-check final | `AUDIT_EDITORIAL_HUMAIN.md`, `v2/REVISION_V2.md`, `FACTCHECK_FINAL_V2.md` |
| Versions antérieures | script v1 à v15, storyboard v1 à v7 : toutes présentes en base ; exports v1 et v2 présents | `docs/stories/STO-20261127-001/` et `…/v2/` |

**État du projet** : statut `structure_draft`, **aucune validation enregistrée**. Le dernier QC du moteur (n° 10) relève 6 bloquants, tous dus au storyboard obsolète.

**Écarts relevés pendant la vérification** (constatés, non corrigés) :
1. **La structure v4 n'est pas alignée sur le script v2.1.** Ses étapes citent encore des faits retirés ou remplacés : F66 en E6 ; F51 et F11 en E8 ; F53, F64, F65 et F67 en E9. Valider cette structure, ce serait valider une liste de faits périmée.
2. **La transition de SEQ-06** (« Le service survit au débat. Et il grandit. ») renvoie au débat public et au communiqué de 2009, **retirés** au fact-check. Elle n'a plus d'objet.
3. **L'en-tête de `v2_1/script.md`** affiche « durée estimée 6.7 min ». Le décompte du moteur pour le script v2.1 donne 936 mots, soit environ **6,3 min** (379,8 s).
4. **Le titre du projet en base** reste « M-Pesa : le prêt par SMS qui est devenu une révolution de l'argent mobile ». Le script porte « M-Pesa : le détournement qui a changé l'argent au Kenya ».

---

## 1. Audit narratif

### Vue d'ensemble

| Séq. | Mots | ≈ durée | Fonction | Appréciation |
|---|---|---|---|---|
| SEQ-01 Jours de voyage | 43 | 17 s | accroche | **Forte** |
| SEQ-02 Hors des banques | 78 | 31 s | contexte | Correcte, un peu didactique |
| SEQ-03 Le prototype de Thika | 77 | 31 s | révélation | **Bonne** |
| SEQ-04 Le détournement | 70 | 28 s | tournant | **Bonne** (meilleure séquence) |
| SEQ-05 Une banque sans agences | 87 | 35 s | mécanisme | Claire |
| SEQ-06 Le régulateur et les banques | 70 | 28 s | obstacle | **Faible** depuis le fact-check |
| SEQ-07 Croissance selon l'entreprise | 58 | 23 s | échelle | Correcte, courte |
| SEQ-08 Ce que mesurent les chercheurs | 193 | 77 s | preuve | **Trop dense** |
| SEQ-09 Le prix du succès | 137 | 55 s | limites | **Liste** |
| SEQ-10 À quelles conditions | 101 | 40 s | conclusion | Moyenne |

### Hook (SEQ-01)

L'ouverture est concrète, sans formule toute faite, et pose une vraie question (« pas inventé pour ça ») sans y répondre. La révélation du microcrédit attend SEQ-03 : le défaut principal de la v1 est corrigé. Le hook est évalué en détail au §4.

### Promesse narrative

La promesse implicite est : « vous allez découvrir pour quoi ce service a vraiment été conçu ». Elle est tenue en SEQ-03 et SEQ-04, puis le film change de nature : il devient une évaluation (chiffres de l'entreprise, chercheurs, limites). Ce virage est légitime, mais **aucune phrase ne l'annonce**. Le spectateur venu pour une histoire reçoit, dans la seconde moitié, une enquête chiffrée.

### Progression des 10 séquences

- **SEQ-01 à SEQ-05** : la progression est nette. Problème, intention, détournement, mécanisme : chaque séquence apporte une information nouvelle.
- **SEQ-06** : depuis le retrait du communiqué de 2009, la séquence pose deux obstacles (conditions du régulateur, hostilité des banques) **sans les résoudre ni les faire monter**. Elle s'arrête sur l'objection des banques, puis la transition orpheline enchaîne sur la croissance. Le conflit, qui était le principal levier de tension du milieu du film, est désormais plat.
- **SEQ-07** : bon pivot critique (« chiffres de l'entreprise », « pas ce qui a changé pour eux »).
- **SEQ-08** : nécessaire, rigoureuse, mais elle concentre 21 % du texte, 8 nombres et deux études. C'est le passage où un spectateur YouTube décroche le plus probablement.
- **SEQ-09** : quatre limites en 55 secondes (frais, poids financier, sénateurs, crédit mobile), 9 nombres. Le format « liste » de la v1 est réduit mais pas supprimé.
- **SEQ-10** : la thèse est attribuée, la « leçon » est formulée, puis la RDC arrive en fin de film.

### Tension

La courbe de tension monte jusqu'à SEQ-04, retombe en SEQ-05 (pédagogie, ce qui est normal), devrait remonter en SEQ-06 mais ne le fait plus, puis devient analytique. La tension du dernier tiers repose sur des chiffres, pas sur une situation ou un personnage.

### Rythme

- Les phrases sont courtes et orales, avec plusieurs ruptures efficaces (« Le portable devient un coursier. », « Pas un décompte. », « Ce succès a un prix. »).
- **Déséquilibre** : les séquences 1 à 7 sont légères (23 à 35 s), les séquences 8 et 9 lourdes (77 s et 55 s). Le film accélère en récit puis ralentit en données.

### Clarté des explications financières

- **Bonne** : le mécanisme agent → SMS → carte SIM → retrait (SEQ-05) ; la distinction « chiffres de l'entreprise / mesure des chercheurs » (SEQ-07 et SEQ-08).
- **Fragile** :
  - « service financier formel » n'est expliqué qu'à moitié (« comme une banque ou une assurance ») ;
  - la nuance « l'argent mobile y est lui-même compté comme de la finance formelle » est juste mais abstraite : elle demandera un appui visuel ;
  - « revenus de services » n'est pas expliqué ;
  - les shillings sont donnés sans repère de valeur.

### Équilibre narration, données, témoignages

- **Narration** : présente jusqu'à SEQ-05.
- **Données** : 25 nombres dans la voix off (années comprises), dont 17 en SEQ-08 et SEQ-09.
- **Témoignages** : **un seul**, celui de Michael Joseph, cadre de Vodafone. **Aucune voix d'usager, d'agent, de régulateur ou de chercheur** n'est entendue directement. C'est la principale faiblesse documentaire : le film parle *des* Kényans sans jamais les laisser parler.

### Répétitions

Les répétitions de mots sont maîtrisées : le moteur ne relève aucune alerte. La répétition notable est d'ordre éditorial : **« Vodafone » apparaît 6 fois** et il y a 9 marqueurs « selon ». Le premier point est traité au §2.

### Transitions

Elles sont globalement fonctionnelles et non scolaires. Exceptions :
- **SEQ-06 → SEQ-07** : orpheline (voir §0, écart 2) ;
- **SEQ-09 → SEQ-10** : la thèse ouvre la conclusion par « une limite plus profonde », ce qui rajoute une cinquième limite après la liste.

### Conclusion

- **Forces** : la phrase « Le téléphone, le SMS, les petites boutiques : tout existait déjà. Ce qui était nouveau, c'est d'avoir regardé ce que les gens en faisaient vraiment. » est la meilleure idée du film. Elle relie le début à la fin.
- **Faiblesses** :
  - cette « leçon » repose entièrement sur le récit de Vodafone (voir §2) ;
  - « appelle des règles, des contre-pouvoirs et des prix surveillés » est une prise de position éditoriale, légitime mais à assumer comme telle ;
  - le lien avec la RDC (« Vodafone revendique la présence de M-Pesa… Là aussi, la question se pose ») reste **générique** : aucun fait sur la RDC n'est donné, alors que c'est le public de LUKOJI.

### Potentiel de rétention (YouTube, 6-8 min)

| Moment | Risque de décrochage |
|---|---|
| 0-30 s | Faible : le hook est solide. |
| 30 s-2 min 20 | Faible : récit avec un mystère révélé à 1 min. |
| 2 min 20-3 min 15 (SEQ-06, SEQ-07) | **Moyen** : SEQ-06 sans issue. |
| 3 min 15-4 min 30 (SEQ-08) | **Élevé** : densité chiffrée. |
| 4 min 30-5 min 30 (SEQ-09) | **Moyen à élevé** : liste. |
| 5 min 30-6 min 20 (SEQ-10) | Moyen : conclusion réflexive, sans images fortes. |

**Séquences faibles** : **SEQ-06** (tension retirée, transition orpheline), **SEQ-08** (densité), **SEQ-09** (liste), et dans une moindre mesure **SEQ-10** (lien RDC générique).

---

## 2. Audit de crédibilité

Référence : dossier factuel v4 et `FACTCHECK_FINAL_V2.md`. Aucune recherche nouvelle n'a été faite.

| Risque | Passage | Constat | Gravité |
|---|---|---|---|
| **Vodafone raconte seule sa propre histoire** | SEQ-02 à SEQ-05, SEQ-07, SEQ-10 | Subvention, intention de microcrédit, détournement, « nous avons pris un risque », mécanisme, chiffres de croissance, présence en RDC : **tout vient de Vodafone** ou de l'équipe projet. L'attribution est honnête (« Selon Vodafone », « raconte », « revendique »), mais l'accumulation donne au film le point de vue de l'entreprise. Une source plus ancienne existe : Hughes & Lonie (2007), le récit de l'équipe projet publié dans une revue de MIT Press. Elle n'est pas indépendante, mais elle est contemporaine des faits et n'est **pas citée** dans la voix off. La seule source indépendante sur la période d'avant M-Pesa (FinAccess 2006, CGAP 2009) ne soutient que le hook. | **Élevée** (perception) |
| Estimation présentée comme certitude | SEQ-08 | Bien traité : conditionnel, « leur estimation, qu'ils présentent comme un minimum », « Pas un décompte ». | Faible |
| Causalité excessive | SEQ-08 | Le texte reste en deçà de l'étude : les auteurs revendiquent un **effet causal**, le script parle d'« estimations ». Ce n'est pas un excès de causalité, plutôt une prudence. La phrase « Pour le savoir, il faut suivre des familles » laisse entendre une observation directe, alors que le résultat national est une **extrapolation**. | Faible |
| Chiffre sans périmètre | SEQ-02 et SEQ-08 | 26,7 % et 82,9 % : il manque « adultes de 18 ans et plus » dans un cas et « enquête menée fin 2018 » dans l'autre. Acceptable à l'oral, **à préciser à l'écran**. | Moyenne |
| Chiffre sans périmètre | SEQ-09 | « 7 % » : sur quels transferts, quel montant ? Ce n'est pas précisé (source : Ecofin seule). « 23 → 10 shillings » : c'est un coût moyen et un projet, mais la base n'est pas vérifiée. | Moyenne |
| Chiffre sans périmètre | SEQ-07 | « 51 millions de clients » sur sept pays, sans dire combien au Kenya ; un spectateur peut comprendre « 51 millions de Kényans ». | **Moyenne à élevée** |
| Certitude malgré une source inaccessible | SEQ-06, SEQ-09 | Les conditions de la Banque centrale, l'« incursion » des banques, les 7 %, le projet de plafonnement et le crédit mobile reposent sur Agence Ecofin, **non relue** (site bloqué). Ils sont attribués, mais l'attribution ne signale pas cette fragilité. | Moyenne |
| Certitude malgré une source inaccessible | SEQ-10 | Présentation de thèse : relecture bloquée, auteur non nommé. | Moyenne |
| Interprétation présentée comme un fait | SEQ-04 | « Plutôt que de corriger cet usage, l'équipe décide de le suivre » : c'est la lecture de Michael Joseph (« we took a chance »), dite par le narrateur. | Moyenne |
| Interprétation présentée comme un fait | SEQ-10 | « Ce qui était nouveau, c'est d'avoir regardé ce que les gens en faisaient vraiment » : interprétation de LUKOJI fondée sur le récit de Vodafone. | Moyenne |
| Interprétation présentée comme un fait | SEQ-10 | « un service devenu aussi central » : jugement éditorial. | Faible |
| Interprétation présentée comme un fait | SEQ-04 | « Le portable devient un coursier » : métaphore, sans risque. | Faible |
| Citation sans contexte | SEQ-04 | « Alors nous avons pris un risque » : citée dix ans après les faits, dans un texte d'anniversaire de l'entreprise. Ce contexte (2017, communication de Vodafone) n'est dit qu'en SEQ-03 (« des années plus tard… un texte publié par Vodafone ») : c'est suffisant à l'oral, mais l'écran doit montrer la date. | Faible |
| Citation sans contexte | SEQ-10 | La thèse est citée sans dire qu'elle compare l'argent mobile aux **monnaies locales**, ce qui est le cadre de son jugement. | Moyenne |
| Hook | SEQ-01 | « confier ses billets à un chauffeur de bus » : le mot « chauffeur » vient de Vodafone seule ; la pratique documentée par FinAccess 2006 passe par une **compagnie** de bus ou de matatu. | Faible (une variante existe, voir §4) |

---

## 3. Titre

**Titre en base** : « M-Pesa : le prêt par SMS qui est devenu une révolution de l'argent mobile ». **Ne convient pas** : « révolution » relève de la surenchère, et « prêt par SMS » est inexact (le pilote de 2005 faisait passer par le téléphone le versement et le remboursement de microcrédits ; le service lancé n'était pas un service de prêt).

**Titre du script** : « M-Pesa : le détournement qui a changé l'argent au Kenya ». Il est intrigant et fidèle à l'angle. « A changé l'argent au Kenya » est une affirmation forte, défendable avec FinAccess et Suri & Jack, mais elle mérite d'être pesée.

**Propositions** (aucune n'est imposée) :

| # | Titre | Points forts | Réserve |
|---|---|---|---|
| 1 | **M-Pesa : le service qui n'était pas fait pour envoyer de l'argent** | Reprend exactement la promesse du hook ; très compréhensible | Un peu long |
| 2 | **M-Pesa, histoire d'un détournement** | Court, documentaire, intrigant | « Détournement » peut évoquer une fraude : la vignette doit lever l'ambiguïté |
| 3 | **M-Pesa : le détournement qui a changé l'argent au Kenya** (actuel) | Clair, fort | Affirmation d'impact assez forte |
| 4 | **M-Pesa : quand les clients ont changé le produit** | Centré sur la leçon du film | Moins de mystère ; repose sur le récit de Vodafone |
| 5 | **M-Pesa : du microcrédit à l'argent mobile** | Le plus sobre et le plus exact | Peu intrigant ; dévoile la révélation de SEQ-03 |

---

## 4. Hook H9 : version prudente

> « Pour envoyer de l'argent à sa famille, au Kenya, on pouvait voyager pendant des jours. Ou confier son argent à une compagnie de bus, et attendre. Aujourd'hui, quelques SMS suffisent. Le service s'appelle M-Pesa. Et ses concepteurs ne l'avaient pas inventé pour ça. »

| Critère | Version actuelle (« chauffeur de bus ») | Version prudente (« compagnie de bus ») |
|---|---|---|
| Exactitude | « Chauffeur » : Vodafone seule | **Conforme à FinAccess 2006** (« through a bus or matatu company ») et compatible avec Hughes & Lonie |
| Image mentale | Plus humaine et concrète (une main, une personne) | Plus abstraite (une entreprise) |
| Risque de contestation | Faible, mais attaquable | Très faible |
| Rythme oral | Identique | Identique (même nombre de mots) |
| « son argent » / « ses billets » | « billets » est concret | « son argent » est plus vague, mais exact |

**Évaluation** : la version prudente est **plus solide** et ne perd presque rien en force, à condition que l'image fasse le travail concret. Le matatu réel reste une **image d'illustration datée de 2025** et ne prouve rien ; la source, elle, doit apparaître à l'écran.

Deux points à noter :
- FinAccess 2006 montre que le moyen le plus courant était **un ami ou un proche** (environ 50 à 56 %), avant les compagnies de bus. Une formulation encore plus fidèle serait « le confier à un proche, ou à une compagnie de bus » ; elle est plus longue.
- Le script n'a pas été modifié. Le choix revient à l'éditeur.

---

## 5. Synthèse et décision

### Forces

- L'angle est juste, sourcé et peu connu : un service conçu pour le microcrédit et détourné par ses usagers.
- Le hook est concret et la révélation est retenue jusqu'à SEQ-03.
- L'écriture est orale, simple et sans formules artificielles.
- La distinction entre chiffres d'entreprise et mesures de chercheurs est explicite.
- Les estimations sont traitées avec prudence (« un minimum », « pas un décompte »).
- Le film comporte une vraie partie critique, datée et attribuée.
- **Aucune affirmation contredite par une source primaire ne subsiste** dans la voix off v2.1.

### Faiblesses

- **SEQ-06 a perdu sa tension** et garde une transition orpheline.
- **SEQ-08 et SEQ-09** concentrent les chiffres (environ 17 nombres en 2 min 15).
- **Aucun témoignage d'usager** : une seule voix entendue, celle d'un cadre de Vodafone.
- **Le lien avec la RDC est générique.**
- La seconde moitié change de régime (de l'histoire à l'évaluation) sans l'annoncer.

### Risques factuels restants

1. Le récit des origines n'a **aucune source indépendante de Vodafone**.
2. Les faits issus d'**Agence Ecofin** (conditions de la Banque centrale, opposition des banques, 7 %, projet de plafonnement, crédit mobile) n'ont pas été relus : le site est bloqué.
3. La **présentation de thèse** n'a pas été relue, et son auteur n'est pas nommé.
4. Le **chiffre de 51 millions** peut être compris comme kényan.
5. Le **projet de plafonnement** des frais doit être confirmé par un document de la Banque centrale avant diffusion.
6. Les **paris en ligne** sont en attente (retirés de la voix off).

### Risques narratifs

- Décrochage probable entre 3 min 15 et 5 min 30.
- Fin réflexive sans image forte ni fait congolais.
- Perception d'un film « vu par Vodafone ».

### Décisions qui nécessitent l'accord humain

1. **Titre** : choisir parmi le §3, puis corriger le titre du projet en base, ce que le moteur ne permet pas sans intervention.
2. **Hook** : version « chauffeur de bus », « compagnie de bus » ou « proche ou compagnie de bus ».
3. **Accepter un récit des origines attribué à Vodafone**, ou demander une source indépendante avant production.
4. **SEQ-06** : accepter une séquence courte sans résolution, ou demander une réécriture limitée, avec au minimum une nouvelle transition et, si possible, un fait vérifié sur le débat de 2008-2009.
5. **SEQ-08 et SEQ-09** : accepter la densité, ou demander un allègement (par exemple déplacer le seuil de 1,25 $ à l'écran seulement, ou retirer une limite).
6. **Témoignages** : produire sans voix d'usager, ou prévoir des témoignages (tournage ou archives sonores identifiées).
7. **RDC** : garder une ouverture générique, ou demander un fait vérifié sur M-Pesa en RDC.
8. **Faits Agence Ecofin non relus** : les accepter avec attribution, ou exiger une seconde source avant diffusion.
9. **Structure** : la structure v4 doit être **réalignée** sur le script v2.1 (listes de faits des étapes E6, E8, E9) avant d'être validée.

### Recommandation (consultative)

| Objet | Recommandation |
|---|---|
| **Script v2.1** | **VALIDABLE SOUS RÉSERVE** : exact au regard du dossier factuel v4, attribué et sans affirmation contredite. Réserves : la transition de SEQ-06 à remplacer, le choix de la version du hook, la précision « dont X au Kenya » ou « dans sept pays » pour les 51 millions, et la mention des périmètres à l'écran (adultes, fin 2018). |
| **Structure v4** | **RÉVISION NÉCESSAIRE (technique)** : ses étapes citent des faits retirés (F66, F51, F11, F53, F64, F65, F67). Il faut la réaligner sur le script v2.1 avant de la soumettre à validation. Le découpage en 10 étapes lui-même est validable. |
| **Ensemble du pilote** | **VALIDABLE SOUS RÉSERVE**, une fois ces deux points traités et les décisions 1, 2 et 3 prises. Les points 4 à 8 améliorent le film sans conditionner son exactitude. |

**Le storyboard v7 n'entre pas dans cette décision** : il est obsolète et devra être repris après la validation du script, selon la liste de scènes du fact-check.

Cette recommandation n'est pas une validation. Seule une validation explicite de l'éditeur, enregistrée par lui, fait avancer le projet.
