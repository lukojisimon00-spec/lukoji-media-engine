# Audit éditorial humain — pilote M-Pesa (`STO-20261127-001`)

*Audit réalisé le 27/11/2026 sur l'état réel du projet : script v9, hooks v2, structure v2, storyboard v2 (58 scènes), direction artistique v1, dossier factuel v2. Statut du projet : `structure_draft`, aucune validation humaine enregistrée. Rien n'a été modifié pendant l'audit : pas de script, de storyboard, de base, de statut ni de validation.*

**Rôles tenus :** directeur éditorial documentaire, scénariste, vérificateur, directeur artistique.
**Principe :** cet audit ne cherche pas à confirmer le 97/100. Il cherche ce qu'un spectateur exigeant, un journaliste vérificateur ou un monteur trouveraient à redire.

**Classement des corrections :**
- **BLOQUANT** : à corriger avant toute validation humaine ;
- **IMPORTANT** : à corriger avant production ;
- **FACULTATIF** : amélioration de qualité.

---

## 1. Résumé exécutif

Le pilote a de vraies qualités :
- un angle juste et sourcé (le détournement d'usage) ;
- une attribution systématique des chiffres ;
- une séquence critique qui existe vraiment ;
- une discipline rare sur les estimations (« Pas un décompte »).

**Le pilote n'est pourtant pas prêt à être validé.** Le 97/100 mesure surtout la conformité aux règles automatiques : attribution présente, nombres présents dans les preuves, durées, types de plans. Il ne mesure pas trois choses : la justesse des dates et contextes, la tension dramatique, la faisabilité visuelle.

**Problèmes de fond :**

1. **Erreur de chronologie dans SEQ-02 (bloquant).** Les chiffres « 22 % des adultes ont un compte bancaire » et « 77 % … sous le matelas » viennent d'une enquête de **2008**, menée **après** le lancement de M-Pesa. L'article MIT de 2010 le dit explicitement (« In a 2008 survey… », « Since its introduction in 2007… »). Le script les place dans « le Kenya du milieu des années deux mille », avant M-Pesa, avec un « alors » qui verrouille ce contresens. Le fait F38 du dossier est déjà mal rédigé (« Avant M-Pesa… »), et l'automate ne pouvait pas le voir.
2. **Trois faits mal datés ou mal qualifiés dans SEQ-09 (bloquant / important) :**
   - la menace des sénateurs est datée « 2018 », alors que l'article capturé indique très probablement **novembre 2020** ;
   - la part de marché de 90,8 % n'a pas d'objet (part de quoi ?) ;
   - la « thèse publiée dans la Revue de la régulation » est en réalité une **présentation de thèse** (un résumé par son auteur).
3. **Le récit dévoile son rebondissement trois fois** : dans le hook (SEQ-01), dans SEQ-03 et dans SEQ-04. Le spectateur connaît la fin du premier acte au bout de 12 secondes. La structure est claire mais **sans suspense**.
4. **Il n'y a aucun personnage.** « L'équipe », « les bénéficiaires », « des banques », « des sénateurs » : le film reste un exposé. Les sources capturées contiennent pourtant au moins une piste humaine (Michael Joseph, ancien directeur général de Safaricom, cité par Agence Ecofin), à enregistrer comme fait avant usage.
5. **Le dernier tiers est une liste.** SEQ-08 et SEQ-09 totalisent 117 s et 11 faits chiffrés. La densité monte au moment où l'attention baisse.
6. **Le storyboard repose sur des images qui n'existent peut-être pas.** 12 scènes « authentiques » comptent sur une « catégorie Wikimedia Commons M-Pesa » non vérifiée, ou sur des médiathèques presse. Trois reconstitutions supposent un tournage au Kenya. Le reste est très majoritairement du motion design (32 scènes sur 58 sont des graphiques explicatifs).

**Décision recommandée : RÉVISER** (détail en section 10). Ni la structure, ni le script, ni le storyboard ne doivent être validés en l'état.

---

## 2. Hooks

### 2.1 Évaluation des 8 hooks

Notes de 1 à 5. Le score du moteur est rappelé entre crochets.

**H1 — paradoxal [91,5] (choisi)**
- Notes : compréhension 5 · curiosité 4 · force narrative 3 · potentiel visuel 3 · crédibilité 5 · risque de sensationnalisme 1 (faible) · cohérence avec le script 4 · rétention 3.
- **Avis :** solide et honnête, mais rédigé comme un résumé, pas comme une scène. Voir 2.2.

**H3 — narratif [85,5]**
- Notes : compréhension 4 · curiosité 4 · force narrative 4 · potentiel visuel 4 · crédibilité 5 · risque 1 · cohérence 4 · rétention 4.
- **Avis :** le plus cinématographique des hooks fiables. Il mérite d'être fusionné avec H1 (voir 2.3).

**H7 — révélation [79]**
- Notes : compréhension 4 · curiosité 4 · force narrative 3 · potentiel visuel 2 · crédibilité 5 · risque 2 · cohérence 4 · rétention 3.
- **Avis :** la révélation est donnée d'emblée et ne laisse rien à révéler ensuite.

**H6 — question [77,5]**
- Notes : compréhension 5 · curiosité 3 · force narrative 2 · potentiel visuel 2 · crédibilité 5 · risque 1 · cohérence 4 · rétention 3.
- **Avis :** une question rhétorique d'ouverture, formule usée sur YouTube.

**H8 — cinématographique [68]**
- Notes : compréhension 3 · curiosité 3 · force narrative 4 · potentiel visuel 5 · crédibilité 4 · risque 2 · cohérence 3 · rétention 3.
- **Avis :** fort visuellement, mais il dépend d'images qu'on n'a pas (tournage).

**H5 — conséquence [65]**
- Notes : compréhension 4 · curiosité 3 · force narrative 3 · potentiel visuel 3 · crédibilité 4 · risque 3 · cohérence 3 · rétention 3.
- **Avis :** il ouvre sur l'impact, que le film traite tard et avec prudence. La promesse n'est pas tenue.

**H4 — tension [62,5]**
- Notes : compréhension 4 · curiosité 3 · force narrative 3 · potentiel visuel 2 · crédibilité 4 · risque 3 · cohérence 3 · rétention 3.
- **Avis :** le conflit avec les banques est annoncé, mais le script ne le dramatise pas (SEQ-06 dure 32 s).

**H2 — historique [51]**
- Notes : compréhension 4 · curiosité 2 · force narrative 2 · potentiel visuel 2 · crédibilité 3 · risque 4 · cohérence 3 · rétention 2.
- **Avis :** « personne ne… » relève de la surenchère. À écarter, comme le moteur l'a déjà fait.

Le classement du moteur est globalement juste. Deux nuances :
- H3 est sous-évalué par rapport à H1 sur la force narrative ;
- H1 est surévalué sur la rétention.

### 2.2 Analyse de H1 et des 15 premières secondes

À 150 mots par minute, les 15 premières secondes contiennent environ 37 mots, c'est-à-dire tout le paragraphe de H1 : contexte, paradoxe, intention initiale et dénouement.

- **0–5 s** : « Au Kenya, envoyer de l'argent par téléphone est devenu un geste du quotidien. »
  - C'est une généralité sans image, sans lieu précis, sans enjeu.
  - Pour un public non kényan, ce n'est pas une surprise. Pour un public africain (dont la RDC), c'est une banalité.
  - **La première phrase ne retient pas.**
- **5–9 s** : « Pourtant, M-Pesa n'a pas été conçu pour ça. » C'est le bon déclic, la curiosité naît ici.
- **9–16 s** : « Il devait servir à rembourser des microcrédits. Ce sont ses premiers utilisateurs qui en ont décidé autrement. »
  - **Le hook répond à sa propre question avant que le spectateur ait eu le temps de se la poser.**
  - Le mystère est fermé à 16 s.
- **16–28 s** : « Cette histoire raconte comment… Et pourquoi… »
  - C'est un sommaire, procédé scolaire et très reconnaissable des scripts générés.
  - Seul « ce succès fait aussi débat » relance l'intérêt.

**Verdict :** H1 est honnête et clair, mais il garde le spectateur par la logique, pas par l'émotion. Il retient probablement un public déjà intéressé par la fintech. Il retient mal un public large.

### 2.3 Version améliorée proposée (sans déformer les faits)

Cette version fusionne H3 (scène concrète, F61, Vodafone) et H1 (paradoxe), et retient la réponse.

> Au Kenya, pour envoyer de l'argent à sa famille, on pouvait voyager pendant des jours. Ou confier ses billets à un chauffeur de bus. *(bip de SMS)* Aujourd'hui, quelques SMS suffisent. Le plus étrange, c'est que le service qui a rendu ça possible n'avait pas été conçu pour envoyer de l'argent. Il a fallu que ses premiers utilisateurs le détournent. Et que ses concepteurs acceptent de les suivre.

**Ce qui change :**
- le film ouvre sur une **scène** (F61, confirmé, source Vodafone) au lieu d'une généralité ;
- on dit que le service a été détourné, **sans dire de quoi** : le microcrédit reste la révélation de SEQ-03 ;
- le sommaire est supprimé ;
- la promesse critique peut passer en une phrase, à l'écran (« … et pourquoi ce succès fait débat ») ou en voix off.

**Points de vigilance :**
- « quelques SMS » repose sur F43 (fonctionnement par SMS) ;
- ne pas ajouter de durée (« quelques secondes ») : aucun fait ne la soutient ;
- la mention de la source Vodafone doit rester à l'écran pendant l'anecdote du chauffeur.

---

## 3. Structure

### 3.1 Longueurs

| Séquence | Durée | Faits | Constat |
|---|---|---|---|
| SEQ-01 Paradoxe | 28,4 s | 2 | trop long pour une accroche qui se résout à 16 s |
| SEQ-02 Matelas | 42,4 s | 3 | contexte juste, chiffres mal datés (voir §5) |
| SEQ-03 Subvention | 31,6 s | 3 | répète la révélation déjà faite |
| SEQ-04 Détournement | 39,2 s | 3 | cœur du film, **trop court** pour son importance |
| SEQ-05 Agents | 43,2 s | 3 | clair, pédagogique ; meilleure séquence |
| SEQ-06 Banques/régulateur | 32,4 s | 2 | conflit résolu en deux phrases |
| SEQ-07 Croissance | 42,8 s | 4 | liste de chiffres d'entreprise |
| SEQ-08 Chercheurs | 55,6 s | 4 | dense mais nécessaire |
| SEQ-09 Revers | **62,0 s** | **7** | la plus longue et la plus dense, en fin de film |
| SEQ-10 Conclusion | 44,8 s | 1 | moraliste, lien RDC plaqué |

Le premier acte (SEQ-01 à 04) dure 142 s pour une seule idée. Le dernier tiers (SEQ-08 et 09) entasse 11 faits en 117 s. **La courbe d'information est inversée** : lente quand le spectateur est frais, saturée quand il fatigue.

### 3.2 Défauts structurels

1. **Révélation répétée.** Le microcrédit est annoncé en SEQ-01, réexpliqué en SEQ-03 (« Mais au départ, l'idée n'a rien à voir avec les transferts »), puis montré en SEQ-04. SEQ-03 perd tout effet de surprise.
2. **Information révélée trop tôt.** Le sommaire de SEQ-01 annonce aussi le « débat ». Le revers de SEQ-09 est donc attendu, ce qui n'est pas un mal en soi, mais rend la structure prévisible.
3. **Transitions artificielles.** Plusieurs transitions sont des questions ou des annonces de l'auteur au spectateur :
   - « Face à ce vide, un acteur inattendu cherche justement des idées » ;
   - « C'est là qu'intervient un acteur inattendu » : l'adjectif « inattendu » est répété à une ligne d'écart ;
   - « Que retenir, alors, de cette histoire ? » ;
   - la transition SEQ-05→06 **duplique** la première phrase de SEQ-06.
4. **Pas de tension réelle en SEQ-06.** Les banques protestent, puis la Banque centrale « donne pourtant son feu vert ». L'obstacle disparaît en une phrase.
   - L'article Ecofin S24 capturé contient une piste plus dramatique : le communiqué de la Banque centrale du 27 janvier 2009, publié pour répondre à un débat public sur le cadre légal de M-Pesa, **après** le lancement.
   - C'est un vrai moment de crise, mais il n'est **pas encore enregistré comme fait**. Il faut l'ajouter au dossier avant tout usage.
5. **SEQ-07 et SEQ-08 se répondent bien** (« chiffres de l'entreprise » puis « ce que mesurent les chercheurs ») : c'est le meilleur mouvement du film. À garder.
6. **Personnage absent** : voir §1. La structure « transformation » gagnerait à suivre au moins un acteur (l'équipe projet nommée, un agent, un régulateur).
7. **Fin plaquée.** Le lien avec la RDC arrive dans les 20 dernières secondes, sans préparation hormis une mention en SEQ-07. Il sert le public LUKOJI mais n'est pas construit.

### 3.3 Modifications concrètes proposées

*(À appliquer dans une nouvelle version, pas sur l'original.)*

**SEQ-01**
- Ramener à environ 18 s avec le hook de §2.3.
- Supprimer le sommaire.

**SEQ-02**
- Garder le chauffeur de bus et les familles séparées.
- **Retirer les chiffres 22 % et 77 %** de ce contexte « avant M-Pesa ». Les déplacer en SEQ-08 comme état des lieux 2008, un an après le lancement (voir §5).

**SEQ-03**
- Faire de SEQ-03 la **vraie révélation** : la subvention, le prototype de microcrédit, Thika.
- Retirer « Mais au départ, l'idée n'a rien à voir… ». Le spectateur ne le sait pas encore si l'on applique §2.3.

**SEQ-04**
- Allonger légèrement : c'est le moment pivot.
- Laisser respirer « Le portable devient un coursier ».
- Déplacer les 41 % / 8 % (étude bien postérieure) en SEQ-08, ou les introduire explicitement comme une observation ultérieure (« Des années plus tard… »). Le « Plus tard » actuel est trop discret.

**SEQ-05** : garder. Corriger le chiffre des 400 agences (§5).

**SEQ-06** : soit dramatiser, avec le débat de 2009 après enregistrement du fait, soit fusionner avec SEQ-05 et assumer une séquence courte.

**SEQ-07** : garder **un seul** jeu de chiffres d'entreprise (2022, le plus récent) plus le 1,2 million de la première année. Supprimer 2016, qui crée en outre l'incohérence « 10 pays » puis « sept pays » sans explication.

**SEQ-08** : intégrer l'état des lieux 2008 (22 % / 77 %), puis FinAccess, puis Suri et Jack. Ordre chronologique des preuves.

**SEQ-09** : trois limites seulement, développées.
- **Coût** : 7 %, projet de plafonnement.
- **Domination** : la part de marché, correctement qualifiée, plus les sénateurs correctement datés.
- **Usages à risque** : paris et crédit.
- La thèse passe en SEQ-10 ou disparaît.

**SEQ-10**
- Supprimer « Au fond… n'est pas celle d'une technologie géniale ».
- Préparer la RDC dès SEQ-07 (« parmi les pays… la RDC ») et conclure sur une question concrète pour le public congolais.

---

## 4. Script (1 056 mots)

### 4.1 Constat d'ensemble

**Points forts :**
- phrases courtes : 82 phrases, la plus longue fait 26 mots ;
- vocabulaire simple, aucun cliché de la liste interdite ;
- attribution constante, prudence réelle sur les estimations.

**Points faibles :**
- **La voix est celle d'un exposé, pas d'un narrateur.** On explique beaucoup et on montre peu.
- **« Selon » ouvre 8 phrases.** L'attribution est juste, mais sa répétition en tête de phrase alourdit l'oreille. Il faut varier : « Vodafone raconte que… », « Chez Agence Ecofin, on lit que… », ou mettre l'attribution à l'écran et alléger la voix quand la source est affichée.
- **Le rythme est uniforme.** Presque toutes les phrases font 8 à 15 mots, sans phrase très courte de rupture, sauf « Pas un décompte. » et « Le portable devient un coursier. », qui sont justement les deux meilleures.
- **Peu d'émotion.** Aucune phrase ne donne à voir une personne précise.

### 4.2 Passages « IA » ou scolaires

Ce sont des formules reconnaissables, même si elles ne figurent pas dans la liste de clichés du moteur.

| Passage | Problème | Proposition |
|---|---|---|
| « Cette histoire raconte comment un détournement d'usage a changé la façon dont… Et pourquoi… » | Sommaire de dissertation. | Supprimer (voir §2.3). |
| « Pour comprendre, il faut revenir au Kenya du milieu des années deux mille. » | Formule de manuel. | « Kenya, milieu des années 2000. » (carton) puis entrer dans la scène. |
| « Le problème, c'est le chemin. » | Correct, un peu « copywriting ». | Garder ou remplacer par l'image : « Entre la ville et le village, l'argent voyage mal. » |
| « Face à ce vide, un acteur inattendu cherche justement des idées. » + « C'est là qu'intervient un acteur inattendu » | Double « inattendu », transition annoncée. | « À Londres, un ministère cherche justement ce genre de problème à résoudre. » (Le ministère britannique est sourcé ; ne pas ajouter de date.) |
| « Mais au départ, l'idée n'a rien à voir avec les transferts d'argent. » | Révèle et répète. | Supprimer si §2.3 est retenu. |
| « Et sur le terrain, quelque chose ne colle pas avec le plan. » | Bonne intention, formulation plate. | « Sur le terrain, les clients font autre chose. » |
| « Ce sont les chiffres de l'entreprise elle-même. Ils mesurent un succès commercial. Ils ne disent pas encore ce qui a changé dans la vie des gens. » | Juste, mais trois phrases pour une idée ; ton de cours. | « Ce sont les chiffres de Vodafone. Ils disent combien de clients, pas ce qui a changé pour eux. » |
| « Alors, qu'a vraiment changé M-Pesa ? » | Question rhétorique de transition. | La couper : la transition précédente pose déjà la question. |
| « Mais un service devenu aussi central attire aussi les critiques. » | Double « aussi », transition creuse. | Coupe franche sur « Ce succès a un revers. » |
| « D'autres usages inquiètent. » | Annonce vague. | Entrer directement : « Il y a aussi les paris en ligne. » |
| « Au fond, l'histoire de M-Pesa n'est pas celle d'une technologie géniale. … C'est l'histoire d'une équipe qui… » | Structure « ce n'est pas X, c'est Y », signature typique des textes générés. | « Le téléphone, le SMS, les petites boutiques : tout existait déjà. Ce qui était nouveau, c'est d'avoir regardé ce que les gens en faisaient. » |
| « Là comme ailleurs, la question n'est plus de savoir si… Elle est de savoir à quelles conditions, et au profit de qui. » | Chute rhétorique attendue. | Acceptable en dernière phrase, mais à ancrer : « En RDC aussi, la question se pose : à quelles conditions, et au profit de qui ? » |

### 4.3 Gloses qui dépassent les sources

Ce sont des corrections de fond, pas de style.

- **« L'argent remonte vers la maison familiale. »** (SEQ-04)
  - La source dit 41 % vers des parents, 8 % vers des enfants, et le MIT écrit « strongly suggests ».
  - « Maison familiale » est une interprétation imagée, présentée comme un constat.
  - **IMPORTANT** : « Autrement dit, l'argent circule surtout des enfants vers leurs parents, selon cette étude. »
- **« … de l'opérateur, jugé trop dominant »** (SEQ-09) : la source dit « jugé de plus en plus dominant ». « Trop » vient d'un autre passage, celui d'un rapport cité dans l'article. → « jugé de plus en plus dominant ».
- **« une infrastructure dont dépend une grande partie d'un pays »** (SEQ-10) : aucun fait ne quantifie cette dépendance. → remplacer par un fait sourcé (part de marché qualifiée) ou formuler en question.
- **« Les banques, elles, restent hors de portée pour beaucoup. »** (SEQ-02) : plausible, mais non sourcée en tant que telle. Le 22 % (mal daté) servait de preuve. Si le chiffre est déplacé, garder la phrase sous la forme de l'anecdote Vodafone.

### 4.4 Prononciation et lisibilité orale

- **Noms et sigles à prononcer** : « Tavneet Suri », « William Jack », « Thika », « Safaricom », « FSD Kenya » (dire « F-S-D Kenya », ou mieux « le programme FSD Kenya » à la première mention).
- **« M-Pesa »** : fixer une prononciation (« èm-pé-sa »), utilisée 10 fois.
- **Nombres longs** :
  - « plus de 287 400 agents » est imprononçable avec naturel ;
  - « 194 000 ménages » passe ;
  - « 29,5 millions » passe ;
  - recommandation : chiffres exacts **à l'écran**, voix plus légère (« des centaines de milliers d'agents »). Ce n'est pas un nouveau nombre, donc la règle « nombre ⊂ preuve » reste respectée.
- **Mots qui reviennent souvent** : « aussi » (4 fois, dont 2 dans la même phrase en SEQ-08→09), « selon » (8), « Vodafone » (5). « argent » revient dans presque toutes les séquences : c'est le sujet, mais varier avec « les billets », « la somme », « les fonds » en SEQ-05.

### 4.5 Passages qui pourraient être plus cinématographiques

- **SEQ-04** : le moment où l'équipe *voit* les usagers détourner le service. Vodafone (S6) raconte ce constat ; une citation courte de la source, lue ou affichée, vaudrait mieux que la paraphrase.
- **SEQ-05** : suivre **une** somme, de la main du client au comptoir jusqu'au retrait. Le script le fait déjà en partie ; il faut l'assumer comme un trajet continu.
- **SEQ-06** : faire entendre la controverse (débat public de 2009, voir §3.2) plutôt que la résumer.

---

## 5. Factuel

Ce que j'ai réellement consulté : le dossier factuel v2 (`bundle.json`), les extraits capturés le 27/11/2026 (`research/captures/2026-11-27-mpesa/captures.json`) et les métadonnées des sources.

**Je n'ai consulté aucune source originale au-delà de ces captures** :
- ni l'article de Science (Suri et Jack, 2016) ;
- ni le working paper de 2010 ;
- ni le rapport FinAccess ;
- ni les données de l'Autorité des communications ;
- ni les rapports annuels de Safaricom ;
- ni le texte de la thèse.

Mes doutes sur certains chiffres viennent de la cohérence interne des extraits, pas d'une contre-vérification externe. Quand je dis « à vérifier », c'est que **personne** ne l'a encore fait.

### 5.1 Faits à source unique (16), par ordre de gravité

**F38 — 22 % des adultes ont un compte bancaire (SEQ-02, « alors »)**
- Source : S33, MIT 2010.
- **Problème : chronologie fausse.** La source précise « Since its introduction in 2007… 38 percent of households have at least one M-PESA user… only 22 percent of adults have bank accounts ». L'enquête date de 2008. Le fait F38 du dossier dit « Avant M-Pesa », ce qui est faux.
- **BLOQUANT.** Corriger le fait (« En 2008, un an après le lancement… ») et le déplacer hors du contexte pré-M-Pesa.

**F39 — 77 % gardent leur argent « sous le matelas » (SEQ-02)**
- Source : S33, citant le working paper de Suri et Jack (vers 2010).
- **Problèmes :**
  - **chronologie** : données post-lancement (enquête 2008) présentées comme pré-M-Pesa ;
  - **figure de style prise au pied de la lettre** : le MIT écrit « under the mattress… so to speak ». Le storyboard (SC-011) montre des billets glissés sous un matelas.
- **BLOQUANT** pour la chronologie, **IMPORTANT** pour le visuel. Dire « gardent leur argent chez eux, “sous le matelas”, comme disent les chercheurs », dater 2008, et ne pas illustrer littéralement.

**F56 — Sénateurs, « Dès 2018 » (SEQ-09, SC-050 « 2018 »)**
- Source : S26, Agence Ecofin, article non daté dans la capture.
- **Problème : date très probablement fausse.**
  - L'article titre « menacent **à nouveau** ». Il renvoie à des articles liés datés du 09/03/2017 et du 20/02/2018, donc il est postérieur au 20/02/2018.
  - Son identifiant d'URL (`1811-82596`) se situe entre un article Ecofin de novembre 2019 (`0611-70837`) et un article de mai 2022 (`2405-97948`). Cela suggère le **18 novembre 2020**.
  - La date « 2018-11 » du dossier a été déclarée sans preuve.
  - « jugé trop dominant » ne figure pas dans la phrase qui attribue le jugement aux sénateurs (« de plus en plus dominante »).
- **BLOQUANT.** Vérifier la date exacte sur la page originale. En attendant, écrire « des sénateurs kényans ont, à plusieurs reprises, menacé… » sans année, et utiliser « de plus en plus dominant ».

**F54 — 90,8 % de parts de marché au 31 mars 2025**
- Source : S30, Agence Ecofin, citant l'Autorité des communications.
- **Problèmes :**
  - **périmètre inconnu** : part de marché de quoi ? Abonnés à l'argent mobile ? Valeur des transactions ? L'extrait ne le dit pas, et le camembert de SC-048 laisse croire à une part « de l'argent » en général ;
  - source secondaire d'une donnée publique primaire.
- **BLOQUANT** en l'état. Consulter le rapport statistique de l'Autorité des communications, préciser le périmètre (« des abonnements à l'argent mobile », si c'est le cas), sinon retirer.

**F47 — 30 000 agents contre « seulement 400 agences bancaires » (début 2012)**
- Source : S24, Agence Ecofin, article non daté, vers 2012.
- **Problèmes :**
  - **chiffre suspect** : 400 agences bancaires pour tout le Kenya en 2012 paraît très bas pour un système bancaire de cette taille. Il peut s'agir d'une coquille, d'un périmètre restreint ou d'une erreur de l'article. Je ne l'ai pas contre-vérifié ;
  - il n'est pas corroboré, et c'est le seul chiffre du film dont la vraisemblance pose question à première lecture ;
  - le même article contient « En 2011, 8 800 agents étaient déjà en activité… », ce qui semble concerner un autre périmètre (agents bancaires) et crée de la confusion.
- **BLOQUANT.** Corroborer, par exemple avec les données de supervision bancaire de la Banque centrale du Kenya pour 2011–2012. Sinon garder seulement « environ 30 000 points M-Pesa, selon Agence Ecofin » sans la comparaison, et modifier SC-025.

**F59 — « thèse publiée dans la Revue de la régulation »**
- Source : S34, OpenEdition.
- **Problème : mauvaise qualification.** La page est classée « Présentations de thèse » : c'est le résumé d'une thèse par son auteur, pas la thèse. Par ailleurs :
  - l'affirmation exacte est « Les monnaies locales visent les causes systémiques de la pauvreté, ce que les systèmes de monnaie mobile ne font pas » : c'est une comparaison avec les monnaies locales, que le script supprime ;
  - l'auteur n'est pas nommé.
- **IMPORTANT.** « Pour une thèse d'économie présentée dans la Revue de la régulation… » ; nommer l'auteur après vérification ; conserver la nuance « effets très indirects pour les plus pauvres ».

**F57 — Les paris sont « la deuxième source de revenus » de M-Pesa (présent)**
- Source : S28, Agence Ecofin, mai 2022, exercice clos le 31/03/2022.
- **Problème : présent de vérité générale** pour un constat daté de 2022.
- **IMPORTANT.** « En 2022, selon Agence Ecofin, les paris étaient devenus… ».

**F55 — Frais « jusqu'à 7 % » ; 23 → 10 KES d'ici 2028**
- Source : S25, Agence Ecofin, octobre 2025.
- **Problèmes :**
  - Ecofin rapporte le projet « **selon plusieurs médias locaux** ». C'est un **projet** annoncé, pas une mesure adoptée ;
  - le script dit « La Banque centrale veut faire baisser… », ce qui est acceptable, mais l'écran de SC-047 dit « OBJECTIF 2028 (PROJET) ». Il faut garder « projet » dans la voix aussi ;
  - « certains transferts » est bien conservé ; le maintenir ;
  - « coût moyen » : la source dit « en moyenne, un utilisateur dépense environ 23 KES par transaction ». Correct.
- **IMPORTANT.** « … selon des médias locaux cités par Agence Ecofin, la Banque centrale a annoncé un projet pour ramener ce coût… ». Corroborer par un communiqué de la Banque centrale ou la Stratégie nationale d'inclusion financière 2025-2028.

**F53 — 44,2 % des revenus de Safaricom (exercice 2025)**
- Source : S25, Agence Ecofin.
- **Problème :** chiffre d'origine probablement Safaricom (rapport annuel), non consulté. Pas de raison particulière de douter.
- **FACULTATIF.** Vérifier dans les résultats annuels de Safaricom de l'exercice 2025.

**F51 — Inclusion financière de 27 % (2006) à 83 % (2019)**
- Source : S27, Agence Ecofin, qui cite l'enquête FinAccess d'avril 2019.
- **Points d'attention :**
  - la source est secondaire, le rapport FinAccess n'a pas été consulté ;
  - la définition d'« inclusion financière » (accès formel) n'est pas précisée ;
  - le script fait bien la prudence (« cette courbe ne dit pas quelle part revient à M-Pesa »).
- **IMPORTANT.** Consulter le rapport FinAccess 2019 et préciser « accès formel » si c'est la définition. SC-037 annonce une « couverture du rapport FinAccess » mais pointe vers l'article Ecofin : à aligner.

**F11 — 194 000 ménages sortis de l'extrême pauvreté (~2 %)**
- Source : S7, MIT News 2016.
- **Points d'attention :**
  - le script omet le seuil (« moins de 1,25 $ par jour ») et la période (« depuis 2008 ») ;
  - l'étude originale (Science) n'a pas été lue ;
  - c'est un résultat très cité et globalement reconnu, mais aussi **discuté** dans la littérature (méthode, extrapolation). Le script le signale correctement (« estimations… Pas un décompte »).
- **IMPORTANT.** Ajouter « depuis 2008 » et le seuil à l'écran. Lire au moins le résumé de l'article de Science pour confirmer les chiffres.

**F12 — Effet plus fort pour les femmes ; 185 000 femmes de l'agriculture vers le commerce**
- Source : S7.
- **Problème :** le script dit « auraient quitté l'agriculture **pour le commerce** ». MIT parle de passage « from farming to business occupations » : « commerce » est une traduction un peu étroite.
- **FACULTATIF.** « … vers des activités commerciales ou indépendantes » ; vérifier sur l'original.

**F40 — 41 % vers des parents, 8 % vers des enfants**
- Source : S33.
- **Problèmes :**
  - le MIT écrit « strongly suggests » : la conclusion « remonte vers la maison familiale » est une glose (voir §4.3) ;
  - données de 2008, introduites par « Plus tard » : acceptable si l'on garde ce marqueur.
- **IMPORTANT** (glose).

**F46 — Les banques voient une « incursion »**
- Source : S24, non daté.
- **Problème :** source unique, mais formulation prudente et attribuée.
- **FACULTATIF.** Corroborer si possible ; sinon garder tel quel.

**F52 — Mesure par densité d'agents, extrapolation**
- Source : S7.
- Le fait est correct. Le script dit « ont suivi l'ouverture de points M-Pesa autour de chaque ménage » : formulation fidèle.
- **OK.**

**F58 — Le crédit mobile démocratise l'emprunt, mais pose la question de la protection**
- Source : S27, 2019.
- **Problème :** l'article ne dit pas exactement « protection des plus pauvres ». Il parle d'un secteur « très peu réglementé » (49 plateformes). Le script résume en « pose la question de la protection des plus pauvres » : interprétation raisonnable, mais à rapprocher du texte.
- **FACULTATIF.** « Le crédit sur mobile, très peu réglementé selon Agence Ecofin en 2019… ».

### 5.2 Faits « confirmés » : points à surveiller

- **F42, « 6 mars 2007 »** : le jour exact ne vient que de Vodafone (S32) ; Ecofin S29 confirme seulement l'année. L'extrait Ecofin S24 cite un communiqué de la Banque centrale disant « mars 2007, date de son lancement », ce qui corrobore le **mois**. → Garder « mars 2007 » dans la voix, ou attribuer le jour à Vodafone. **FACULTATIF.**
- **F10, F48, F49 (chiffres Vodafone)** : bien attribués (« selon Vodafone », « revendique »). Mais **« 10 pays » (2016) puis « sept pays » (2022)** se suivent sans explication : le spectateur croira à une erreur ou à un recul inexpliqué. → Supprimer l'un des deux jeux ou expliquer. **IMPORTANT.**
- **F41 (subvention DFID)** : confirmé par deux pages Vodafone. **Les deux viennent de la même organisation, intéressée.** Ce n'est pas une corroboration indépendante. Le fait F13 (même information via Wikipédia, interdit) montre que le moteur a bien perçu la fragilité, mais la classe mal : F41 « confirmé » et F13 « interdit » disent la même chose. → Requalifier F41 en « confirmé par une seule organisation », et chercher un document DFID ou une étude de cas indépendante. **IMPORTANT.**
- **F8, F9, F61 (récit des origines : Thika, détournement, chauffeur de bus)** : **tout le récit fondateur repose sur Vodafone**, qui a intérêt à une belle histoire d'innovation. Le film l'attribue implicitement (« Selon Vodafone » apparaît pour le chauffeur de bus, pas pour le détournement). → Ajouter une attribution explicite au moins une fois pour le récit des origines (« raconte Vodafone »). Idéalement, corroborer par une source indépendante : études de cas académiques, presse de l'époque. **IMPORTANT.**
- **F45 (conditions de la Banque centrale)** : correct. « sécurité des points de retrait » est une adaptation de « safety of products and agents » : acceptable.

### 5.3 Contrôle transversal

- **Dates** : 2008 (F38, F39, F40), novembre 2020 probable (F56), 2022 (F57) et 2019 (F58) sont mal ou pas rendues.
- **Chiffres** : 400 agences (F47) suspect ; 90,8 % (F54) sans périmètre.
- **Origines** : le récit des origines a une seule source, intéressée (Vodafone).
- **Intention initiale** (microcrédit) : sourcée (S6) mais non corroborée.
- **Rôles des acteurs** : Vodafone, Safaricom et DFID sont corrects. **L'actionnariat** (Vodafone actionnaire de Safaricom) n'est jamais expliqué, alors que le schéma SC-013 « ministère → Vodafone → Safaricom » le suppose.
- **Évolution historique** : la cession de M-Pesa par Vodafone (F60) n'est pas utilisée. Le spectateur peut croire que Vodafone possède toujours M-Pesa en 2022–2025. À clarifier en une phrase si F60 est retenu.
- **Effets socio-économiques** : bien nuancés (point fort du film).
- **Limites** : présentes mais en liste.
- **Domination** : « détient 90,8 % des parts de marché » est affirmé sans périmètre. C'est l'énoncé le plus fort du film et le moins qualifié.

---

## 6. Storyboard (58 scènes)

### 6.1 Constat d'ensemble

- **Répartition** :
  - 32 graphiques explicatifs (55 %) ;
  - 12 « authentiques » ;
  - 7 symboliques ;
  - 4 illustrations ;
  - 3 reconstitutions.
- **Production** : le film est d'abord une **suite de motion design** (10 cartes, 8 typographies animées, une dizaine de graphiques et d'infographies, 6 captures d'articles).
- **Fausse variété** : la règle « pas plus de 2 types identiques consécutifs » est respectée sur le papier, mais contournée en alternant des étiquettes qui produisent la même image. Par exemple, SC-046 à SC-049 donnent graphique / infographie / graphique / infographie : quatre écrans noirs à chiffre jaune d'affilée.
- **3D simulée** : 4 scènes (SC-004, 015, 033, 055), sans nécessité narrative. C'est la « 3D inutile » que la direction veut éviter.
- **Zoom lent** : une seule scène (SC-043), bonne discipline. En revanche, le **« surlignage » sur capture d'article** revient 6 fois et deviendra le tic visuel du film.

### 6.2 Scènes problématiques

| Scène | Problème | Gravité | Alternative |
|---|---|---|---|
| **SC-006** archive « Kenya milieu des années 2000 » | Image d'archive datée et libre de droits très difficile à trouver ; la « catégorie Wikimedia M-Pesa » proposée ne contiendra pas de photo de quartier de 2005. | IMPORTANT | Carte animée et typographie « KENYA, 2005 » ; ou photo Wikimedia datée et vérifiée, sinon rien. |
| **SC-008** gare routière, enveloppe au chauffeur | Classée « symbolique » mais c'est une **reconstitution** d'un fait précis (F61), avec « SOURCE : VODAFONE » à l'écran : le spectateur croira à une image d'archive. Elle exige aussi un tournage. | IMPORTANT | Illustration dessinée, assumée et mentionnée « ILLUSTRATION » ; ou plan de gare routière réel et daté, avec la citation Vodafone en texte. |
| **SC-009** agence bancaire fermée, « authentique » | Une photo réelle d'une agence quelconque utilisée comme **symbole** : c'est trompeur si elle est classée authentique. Source proposée (catégorie M-Pesa) incohérente. | IMPORTANT | Supprimer, ou classer « symbolique » avec la mention ; mieux : carte des agences bancaires si une donnée existe. |
| **SC-011** billets sous un matelas | Littéralise une métaphore (« so to speak ») et frôle le **cliché misérabiliste** que la direction artistique interdit. | IMPORTANT | Typographie : « 77 % » + citation « sous le matelas, pour ainsi dire » + date 2008. |
| **SC-020** flèche qui « remonte vers une maison » | Visualise la glose (§4.3). | IMPORTANT | Deux barres, sans maison. |
| **SC-025** 30 000 points contre 400 carrés | Rend visuellement spectaculaire un chiffre suspect (F47). | BLOQUANT tant que F47 n'est pas vérifié | Nuage de 30 000 points seul, si le chiffre est confirmé. |
| **SC-001, SC-016, SC-024** reconstitutions | Exigent un tournage (comptoir, silhouettes, boutique) : **pas faisable gratuitement** sans équipe au Kenya. Le téléphone à clavier « aujourd'hui » est cohérent au Kenya, mais l'image restera générique. | IMPORTANT | Illustration au trait (style LUKOJI, noir/blanc + orange) ou objets filmés sur table, sans prétendre au Kenya. |
| **SC-005, SC-021, SC-043** photos réelles | Dépendent d'une catégorie Wikimedia **non vérifiée** et de médiathèques de Safaricom/Vodafone (images de communication, droits incertains, contraire à « pas de promotion »). | IMPORTANT | Avant toute validation, constituer une **liste réelle** de fichiers Wikimedia (URL, auteur, licence, date, lieu). Sinon, remplacer par carte ou illustration. |
| **SC-043** commerçante + « ≈ 185 000 FEMMES » + zoom lent | Associer une personne réelle et identifiable à une statistique de sortie de pauvreté, c'est lui attribuer une histoire qu'on ne connaît pas (droit à l'image, dignité). | IMPORTANT | Séparer : chiffre sur fond noir ; photo éventuellement avant, sans surimpression. |
| **SC-028** façade de la Banque centrale | Source « catégorie M-Pesa » incohérente ; la photo existe probablement ailleurs sur Commons, mais à vérifier. | FACULTATIF | Chercher dans la catégorie « Central Bank of Kenya » ; noter la licence. |
| **SC-041** capture MIT, 3,6 s | Trop court pour lire quoi que ce soit : la capture devient décorative. | FACULTATIF | Prolonger à 5–6 s ou supprimer ; mettre la référence en IBM Plex Mono sur la scène suivante. |
| **SC-034** zoom sur la RDC, 2,8 s | Coup de zoom gratuit. | FACULTATIF | Fusionner dans SC-033 (la RDC s'allume avec les autres pays). |
| **SC-036** « SOURCE : VODAFONE » se transforme en « ? », 10,4 s | Effet graphique qui commente au lieu de montrer, et trop long. | FACULTATIF | 4 s maximum, ou coupe franche sur SEQ-08. |
| **SC-039** « PART DE M-PESA ? » | Utile, mais doublonne la voix. | FACULTATIF | Garder court. |
| **SC-045** noir + fil qui vibre, 3 s (dont 1 s de silence) | Bonne idée de rupture ; le fil qui « vibre » est décoratif. | FACULTATIF | Noir sec, son coupé, puis carton. |
| **SC-046 → SC-049** quatre écrans chiffrés consécutifs | Monotonie, « PowerPoint animé ». | IMPORTANT | Intercaler une capture de presse kényane réelle ou une image de terrain ; réduire à deux chiffres (§3.3). |
| **SC-048** camembert 90,8 % | Camembert d'une part dont on ignore l'objet (F54). | BLOQUANT tant que F54 n'est pas précisé | Barre simple avec le périmètre écrit. |
| **SC-050** capture « 2018 » | Date probablement fausse (F56). | BLOQUANT | Corriger la date avant usage. |
| **SC-051** interface de paris générique | Acceptable si dessinée ; une capture d'une vraie appli de paris ferait de la publicité. | FACULTATIF | Maquette neutre en gris, mention « ILLUSTRATION ». |
| **SC-052** notifications de crédit « de nuit » | Image d'ambiance générique, typique des banques d'images. | FACULTATIF | Citation de l'article (49 plateformes) en typographie. |
| **SC-054** trois objets gris côte à côte, 8,4 s | Abstrait et lent. | FACULTATIF | Réutiliser les images de SEQ-01, SEQ-05 et SEQ-04 en raccord (rappel visuel). |
| **SC-056** fils → colonnes de bâtiment + RÈGLES / CONTRE-POUVOIRS / PRIX, 12,4 s | Graphisme décoratif et métaphore appuyée, la plus « générée » du film. | IMPORTANT | Typographie simple sur noir, une ligne. |
| **SC-057, SC-058** RDC, rue de Kinshasa au crépuscule | Image symbolique sans source identifiée ; « crépuscule, enseignes » est un plan de banque d'images. | IMPORTANT | Si LUKOJI peut filmer à Kinshasa : plan réel, daté, sourcé ; c'est la meilleure option et elle est gratuite pour une équipe locale. Sinon, terminer sur la carte. |

### 6.3 Besoins réels de production

- **Cartes** : OpenStreetMap ou Natural Earth (domaine public pour Natural Earth ; ODbL avec attribution pour OSM). Faisable, gratuit.
- **Graphiques** : faisables en interne (Phase 3), mais il faut une **bibliothèque de 4 ou 5 gabarits maximum** pour éviter le « tout motion ».
- **Archives** : aucune n'est identifiée à ce jour. Il faut une recherche dédiée, avec URL, licence et auteur, **avant** la validation du storyboard :
  - Wikimedia Commons ;
  - Flickr Creative Commons ;
  - archives de la Banque mondiale ou du CGAP sous licence ouverte, si elles existent (non vérifié).
- **Tournage** : 3 reconstitutions et 2 plans de terrain. Soit c'est possible localement (Kinshasa), soit on les remplace par de l'illustration.

---

## 7. Direction artistique

« Le fil de l'argent » est **une bonne idée de motif** : simple, propre à la charte, signifiant (le flux), et capable de porter les transitions. La palette, la typographie et la règle « tout chiffre porte sa source » sont exactement ce qu'il faut. La catégorisation des images (authentique, illustration, reconstitution, symbolique) avec mention à l'écran est un vrai atout de crédibilité.

**Ce qui ne va pas :**

1. **Le motif devient le film.** Le fil apparaît dans presque toutes les séquences (naissance, ramification, tension, densification, colonnes). Sur 7 minutes, c'est une **répétition**, pas un langage. Le risque : un rendu « template de motion design » interchangeable.
2. **La direction ne dit pas d'où viennent les images réelles.** Elle exige une licence identifiée, mais n'en identifie aucune. Le storyboard compense par du graphique, ce qui tire le film vers l'abstraction.
3. **La « chaleur humaine » annoncée** (boutiques, gares routières, lumière de fin de journée) repose sur des images que le projet n'a pas. Promesse non tenue en l'état.
4. **Trop de mouvements de caméra simulés** : 3D simulée, parallaxe, travelling sur images fixes. Ce sont les signes typiques des montages « IA/stock » que l'éditeur veut éviter.

**Direction plus précise proposée** (ressources gratuites ou accessibles) :

- **Trois registres, pas plus :**
  1. **Documents réels** : captures d'articles, pages de rapports, communiqués, plein cadre, sans surlignage animé systématique. Un trait orange fixe sous la phrase citée suffit.
  2. **Cartes et chiffres** : une carte du Kenya unique, de plus en plus annotée au fil du film (on revient toujours à la **même** carte, ce qui crée la mémoire visuelle) ; un seul gabarit de chiffre (Archivo Black jaune, source en Plex Mono).
  3. **Terrain** : uniquement des images réelles, sourcées et datées ; s'il n'y en a pas, de l'**illustration au trait** (noir, blanc cassé, orange), dessinée par LUKOJI, toujours mentionnée « ILLUSTRATION ».
- **Le fil orange seulement aux moments de flux** : le premier transfert (SEQ-04), le mécanisme (SEQ-05), la conclusion. Trois apparitions, pas quinze.
- **Montage :**
  - plans fixes par défaut ;
  - coupe franche ;
  - aucun mouvement sur photo sauf justification (lecture d'un détail) ;
  - pas de 3D simulée ;
  - pas de parallaxe sur photo d'archive (elle déforme le document).
- **Son** : garder le bip SMS comme signature, mais **pas à chaque transition** (2 ou 3 fois). Les ambiances réelles ne sont possibles qu'avec des prises de son libres (Freesound, CC0/CC-BY) : à lister.
- **Interdits explicites à ajouter** : images de banques d'images « Afrique générique » ; photos de personnes identifiables associées à une statistique de pauvreté ; écrans de marques réelles (Safaricom, applis de paris) ; animations d'icônes « morphing ».

---

## 8. Corrections prioritaires

### BLOQUANT (avant toute validation de structure ou de script)

| # | Où | Correction |
|---|---|---|
| B1 | F38, F39 · SEQ-02 · SC-010, SC-011 | Corriger la chronologie : chiffres de **2008**, après le lancement. Réécrire les faits dans le dossier (nouvelle version de recherche), sortir 22 % / 77 % du contexte « avant M-Pesa », les dater à l'écran. |
| B2 | F56 · SEQ-09 · SC-050 | Vérifier la date de l'article des sénateurs (indice fort : novembre 2020, pas 2018). D'ici là, retirer l'année. Remplacer « trop dominant » par « de plus en plus dominant ». |
| B3 | F54 · SEQ-09 · SC-048 | Préciser le périmètre des 90,8 % (source primaire : Autorité des communications) ou retirer le chiffre. |
| B4 | F47 · SEQ-05 · SC-025 | Corroborer « 400 agences bancaires » ou supprimer la comparaison. |
| B5 | Storyboard · 12 scènes « authentiques » | Constituer la liste réelle des images (URL, auteur, licence, date, lieu) **avant** validation du storyboard. Toute scène sans image identifiée est reclassée (illustration, carte) ou supprimée. |

### IMPORTANT (avant production)

| # | Où | Correction |
|---|---|---|
| I1 | Hook / SEQ-01 / SEQ-03 | Ne plus révéler le microcrédit dans le hook (proposition §2.3) ; supprimer le sommaire ; supprimer la répétition en SEQ-03. |
| I2 | F59 · SEQ-09 · SC-053 | « Présentation de thèse », pas « thèse publiée » ; garder la nuance d'origine ; nommer l'auteur. |
| I3 | F57, F58 · SEQ-09 | Dater : « en 2022 » (paris), « en 2019 » (crédit). |
| I4 | F55 · SEQ-09 | Dire « projet » dans la voix ; mentionner « selon des médias locaux cités par Agence Ecofin » ; corroborer. |
| I5 | F40 · SEQ-04 · SC-020 | Retirer « L'argent remonte vers la maison familiale » et la maison du graphique. |
| I6 | SEQ-10 | Retirer « dont dépend une grande partie d'un pays » (non sourcé) et la structure « n'est pas… c'est… ». Préparer la RDC plus tôt. |
| I7 | SEQ-07 · F48/F49 | Un seul jeu de chiffres d'entreprise, ou expliquer « 10 pays » puis « sept pays ». |
| I8 | F8, F9, F41, F61 | Attribuer explicitement le récit des origines à Vodafone ; chercher une corroboration indépendante ; requalifier F41 (même organisation ≠ corroboration). |
| I9 | SEQ-09 | Réduire à 3 limites développées ; casser la suite de 4 écrans chiffrés. |
| I10 | F11 · SEQ-08 · SC-042 | Ajouter « depuis 2008 » et le seuil de 1,25 $/jour (au moins à l'écran) ; lire le résumé de l'article de Science. |
| I11 | Storyboard | Reconstitutions infaisables gratuitement → illustration au trait ; SC-008 reclassée ; SC-011, SC-043, SC-056, SC-058 revues (§6.2). |
| I12 | Direction artistique | Limiter le fil orange à 3 apparitions ; supprimer la 3D simulée ; carte unique récurrente ; interdits explicites (§7). |
| I13 | Personnage | Ajouter au moins un acteur nommé et sourcé (ex. Michael Joseph, présent dans S24 : à enregistrer comme fait). |
| I14 | Titre d'export | Le titre exporté « le prêt par SMS qui est devenu une révolution de l'argent mobile » est ambigu (on peut comprendre que M-Pesa était un service de prêt grand public, alors qu'il s'agissait d'un prototype de remboursement de microcrédits) et contient « révolution », terme de surenchère. Utiliser le titre du script : « M-Pesa : le détournement qui a changé l'argent au Kenya ». |

---

## 9. Corrections facultatives

| # | Où | Correction |
|---|---|---|
| F1 | Script | Varier les attributions : 8 phrases commencent par « Selon ». Déplacer une partie de l'attribution à l'écran. |
| F2 | Script | Insérer 3 ou 4 phrases très courtes de rupture (le modèle : « Le portable devient un coursier. »). |
| F3 | Script | « 287 400 agents » à l'écran, voix allégée. |
| F4 | Script | Fixer les prononciations (M-Pesa, Thika, Suri, FSD). |
| F5 | F42 | « mars 2007 » dans la voix, ou « 6 mars 2007, selon Vodafone ». |
| F6 | F12 | « vers des activités commerciales » plutôt que « le commerce ». |
| F7 | F60 | Une phrase sur la cession de M-Pesa par Vodafone (2020), pour que le spectateur sache qui possède le service aujourd'hui. |
| F8 | SEQ-06 | Dramatiser avec le débat public de janvier 2009 (communiqué de la Banque centrale cité par Ecofin S24), après enregistrement comme fait. |
| F9 | Transitions | Supprimer la transition SEQ-05→06 qui duplique la première phrase de SEQ-06 ; couper « Alors, qu'a vraiment changé M-Pesa ? ». |
| F10 | Storyboard | SC-034, SC-036, SC-041, SC-045, SC-051, SC-052, SC-054 (§6.2). |
| F11 | F53, F46 | Vérifier dans les sources primaires (rapport annuel Safaricom) ou corroborer. |
| F12 | Moteur (pour plus tard, hors de cette mission) | Le QC ne détecte pas les erreurs de date ou de contexte, les gloses, la fausse variété des types visuels, ni la faisabilité des archives. Le score de 97 ne doit pas être lu comme un indicateur de qualité éditoriale. *(Constat seulement : aucune modification du moteur n'a été faite.)* |

---

## 10. Décision recommandée

### **RÉVISER**

- **Pas « valider »** : 5 corrections bloquantes, dont une erreur de chronologie et une date très probablement fausse. Un spectateur kényan ou un vérificateur les relèverait.
- **Pas « suspendre »** : l'angle est juste, la recherche est réelle et réparable, la structure en dix séquences est une bonne base, et les meilleures idées (opposition chiffres de l'entreprise / chiffres des chercheurs ; « Pas un décompte ») méritent d'être produites.

**Ordre de travail recommandé :**

1. Recherche : corriger F38, F39, F56, F54, F47, F59 (nouvelle version du dossier factuel), et vérifier les points B2 à B4 sur les sources primaires.
2. Structure : appliquer le §3.3 (révélation retenue, SEQ-09 resserrée).
3. Script : nouvelle version à partir des corrections du §4.
4. Une fois le script validé par l'éditeur : storyboard, recherche d'images réelles (B5), puis direction artistique resserrée (§7).

**Rappels :**
- **La validation de chaque étape reste une décision humaine.** Cet audit n'en vaut pas une.
- L'historique montre que les 9 versions du script et les 2 du storyboard ont été produites en une vingtaine de minutes, le même jour, sous l'auteur « editeur ». Elles ont été écrites par l'agent, **sans relecture humaine**. Aucune validation n'existe à ce jour.

---

## Annexe — fichiers examinés

**Exports du projet** (`docs/stories/STO-20261127-001/`) :
- `script.md`
- `hooks.md`
- `storyboard.json` (58 scènes, lues intégralement via les champs voix off, visuel, sources visuelles, texte à l'écran, mouvement)
- `direction_artistique.md`
- `qc.md`
- `verification_factuelle.md`
- `bundle.json`

**Rapports et règles :**
- `docs/RAPPORT_PHASE2.md`
- `config/story.toml`
- `src/lukoji_engine/story/project.py` (statuts)

**Sources capturées** (extraits seulement) : `research/captures/2026-11-27-mpesa/captures.json`

**Historique** : `./bin/lukoji story versions STO-20261127-001` (lecture seule)

**Non consultés** :
- les sources originales hors captures (Science 2016, working paper 2010, FinAccess 2019, Autorité des communications, rapports Safaricom, texte de la thèse) ;
- le fichier `storyboard.md` ligne à ligne : son contenu est le rendu du même `storyboard.json`.
