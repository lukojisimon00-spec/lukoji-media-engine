# Rapport éditorial — première recherche réelle (27 novembre 2026)

Cinq propositions issues de **recherches web réelles**, sur des pages **récupérées par le moteur**. Chaque citation
ci-dessous a été retrouvée **mot pour mot** dans la page source (57 extraits sur 57). Les statuts des faits et les
scores sont **calculés** par le moteur selon des règles publiées ([SCORE_EDITORIAL.md](../SCORE_EDITORIAL.md)) ;
les notes d'attrait (1 à 5) sont un jugement éditorial, justifié pour chaque critère.

> Aucune de ces propositions n'est validée. Rien n'est produit ni publié. La décision vous appartient :
> `./bin/lukoji sujets valider|rejeter|reporter SUJ-… --note "…"`.

## Vue d'ensemble

| # | Sujet | Territoire · famille | Temporalité | Priorité | Attrait | Solidité | Faits clés confirmés | Formats soutenus | État |
|---|---|---|---|---|---|---|---|---|---|
| 1 | M-Pesa : le prêt par SMS devenu révolution | Afrique de l'Est · innovation | intemporel | 54,2 | 79,5 | 79,7 | 4/5 | short, affiche | sain |
| 2 | Corridor de Lobito : le cuivre congolais vers l'Atlantique | **RDC** · géopolitique (sensible) | actualité | 43,5 | 79,5 | 76,0 | 3/5 | short, affiche | sain, recoupement renforcé |
| 3 | InkubaLM : une IA pour le swahili, le yoruba, le zoulou | Afrique australe · tech et IA | tendance | 41,4 | 62,5 | 81,7 | 5/6 | short, affiche | sain |
| 4 | Tulipomanie : la bulle qui n'a (presque) ruiné personne | Europe · histoire méconnue | historique | 37,0 | 79,0 | 61,7 | 2/4 | short, affiche | sain |
| 5 | Air Afrique : onze pays, une compagnie, une chute | Afrique de l'Ouest et centrale · échec d'entreprise | historique | 22,1 | 80,0 | 40,7 | 2/5 | short (documentaire non soutenu) | **⚠ insuffisamment documenté** |

Diversité obtenue : 5 territoires (dont 1 sujet RDC), 5 familles, 4 temporalités. Un seul sujet relève de l'actualité.

**Aucun sujet n'atteint aujourd'hui le seuil « documentaire »** (au moins 4 faits confirmés et 3 organisations A/B indépendantes). C'est le
résultat attendu d'une première passe de recherche : les documentaires demanderont une recherche approfondie dédiée.

## Lecture éditoriale (avis du chercheur, à discuter)

- **Le plus prêt : M-Pesa.** Récit clair (le pivot), chiffres sourcés, faible risque. Point faible : l'impact social
  ne repose que sur le compte rendu du MIT ; l'article de *Science* doit être lu avant toute affirmation chiffrée à l'écran.
- **Le plus pertinent pour la RDC : Lobito.** Financement et tracé confirmés par deux organisations. La question de fond
  (« la RDC en profitera-t-elle ? ») n'est pas encore documentée : c'est elle qui ferait la valeur du contenu. La lecture
  géopolitique (contrer la Chine) reste une **hypothèse attribuée**.
- **Le plus solide techniquement : InkubaLM**, mais toutes les sources techniques émanent de Lelapa AI. Bon pour un
  short informatif ; il faudrait une évaluation indépendante pour aller plus loin.
- **Le plus original : la tulipomanie.** Excellent pour l'esprit critique. Les chiffres de Goldgar (350 participants,
  37 acheteurs) restent **à vérifier** : la page qui les contient a refusé notre lecteur automatique.
- **Le plus fort narrativement, mais le moins documenté : Air Afrique.** Les causes de la faillite ne reposent que sur
  Wikipédia (mention « citation needed »). Les dates divergent : faillite en février 2002, liquidation le 25 avril 2002.
  Le moteur le classe donc en dernier, malgré l'attrait le plus élevé. C'est le comportement voulu.

## Méthode et limites de cette session

- Recherches : 10 requêtes réelles (voir `research/dossiers/2026-11-27.json`, bloc `session`).
- Lecture : 21 pages capturées par le moteur dans l'environnement « LUKOJI Recherche », plus la fiche Hugging Face
  récupérée dans cette session. Les textes sont conservés hors Git (droit d'auteur) ; leurs empreintes SHA-256 sont dans
  `research/captures/2026-11-27/captures.json`.
- Pages non lues : Safaricom Newsroom, History Today et Reviews in History (HTTP 403, refus des lecteurs automatiques).
  Elles sont enregistrées comme **non probantes**.
- Le moteur de recherche de l'agent refuse certains grands médias (Le Monde, RFI, BBC, Libération, Les Échos, Le Figaro,
  NYT, Guardian, AP, FT, The Economist, DW). La diversité des sources francophones en pâtit.
- Les collecteurs automatiques (Wikipédia, GDELT) ont échoué, même dans l'environnement ouvert (HTTP 429 et connexion
  interrompue). Ces échecs sont enregistrés, sans résultat inventé.
- Classements déclarés (domaines hors registre) : Vodafone (A), MIT News (B), DBSA (A), Engineering News (B),
  African Business (B), University of Chicago Press (A), Lelapa AI (A), Africanews (B). Chacun porte le signalement
  `categorie_source_declaree_a_revoir`.

---

## 1. M-Pesa : le prêt par SMS qui est devenu une révolution de l'argent mobile

`SUJ-20261127-002` · proposé · Innovations · afrique_est · intemporel

**Sujet.** La création de M-Pesa au Kenya (lancement en mars 2007) par Safaricom et Vodafone, et ses effets mesurés sur la pauvreté.

**Angle narratif.** Une innovation née d'un détournement d'usage : conçu pour rembourser des microcrédits, le service a été réorienté quand ses concepteurs ont vu les bénéficiaires envoyer l'argent à leurs proches. Leçon : observer ce que font les clients plutôt que suivre son plan.

**Pourquoi c'est intéressant.** L'argent mobile est central dans le quotidien de l'audience (RDC et Afrique) ; l'histoire illustre une leçon entrepreneuriale universelle (le pivot) avec un impact social mesuré par une étude scientifique.

**Accroche potentielle.** « Il devait servir à rembourser des microcrédits. Les Kényans l'ont utilisé autrement, et ont changé l'histoire de la banque. »

**Résumé du récit.** Vodafone et Safaricom testent à Thika un service de remboursement de microcrédits par téléphone. Les bénéficiaires envoient l'argent à des proches éloignés : l'équipe réoriente le produit vers le transfert de téléphone à téléphone, appuyé sur un réseau d'agents. Lancement en mars 2007 ; 1,2 million de clients en un an selon Vodafone. En 2016, une étude publiée dans Science estime que l'accès à l'argent mobile a sorti environ 2 % des ménages kényans de l'extrême pauvreté.

**Potentiel visuel.** Motion design (flux d'argent entre téléphones, carte des agents), chiffres animés, iconographie de téléphones simples ; peu d'archives nécessaires.

**Formats.** short (soutenu), affiche (soutenu), documentaire (non soutenu — ≥ 4 faits confirmés et ≥ 3 organisations A/B)

**Score** (aide au tri, formule v1.0) : priorité **54.2** · attrait 79.5 · solidité 79.7 · faits clés confirmés 4/5 · risque factuel 2/5 · risque juridique 1/5 · difficulté 2/5

| Critère | Note | Justification |
|---|---|---|
| potentiel_narratif | 4/5 | Pivot clair et retournement de situation. |
| interet_public | 5/5 | L'argent mobile concerne directement l'audience. |
| originalite | 3/5 | Histoire connue dans l'écosystème tech, moins du grand public francophone. |
| potentiel_visuel | 3/5 | Très adapté au motion design, peu d'images réelles fortes. |
| potentiel_hook | 5/5 | Accroche contre-intuitive : un produit utilisé autrement que prévu. |
| pertinence_lukoji | 5/5 | Innovation africaine, leçon entrepreneuriale directe. |
| difficulté | 2/5 | Récit simple, chiffres clairs, motion design suffisant. |
| risque juridique | 1/5 | Aucune mise en cause ; marques citées dans un cadre informatif. |

**Signalements :** `format_non_soutenu:documentaire`, `categorie_source_declaree_a_revoir`

**Faits confirmés**

- *confirmé* (fait, cle) — M-Pesa a été lancé en mars 2007.  
  motif : source primaire (A) consultée : Vodafone
  - soutient — [Vodafone](https://www.vodafone.com/news/newsroom/digital-society/m-pesa-created) (A) : « In March 2007, we launched M-Pesa and the rest is history! » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Wikipédia](https://en.wikipedia.org/wiki/M-Pesa) (C) : « The full commercial launch was initiated in March 2007. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, cle) — Le service a d'abord été conçu pour des microcrédits, testé à Thika ; les bénéficiaires envoyaient l'argent à des proches éloignés.  
  motif : source primaire (A) consultée : Vodafone
  - soutient — [Vodafone](https://www.vodafone.com/news/newsroom/digital-society/m-pesa-created) (A) : « Originally we worked on the idea of microfinance loans using mobile phones, and trialled a prototype service in Thika, north of Nairobi. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Vodafone](https://www.vodafone.com/news/newsroom/digital-society/m-pesa-created) (A) : « What we found in practice was that people who received the loans were sending the money to other people hundreds of miles away. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, cle) — L'équipe a réorienté le système vers le transfert d'argent d'un téléphone à l'autre, appuyé sur un réseau d'agents.  
  motif : source primaire (A) consultée : Vodafone
  - soutient — [Vodafone](https://www.vodafone.com/news/newsroom/digital-society/m-pesa-created) (A) : « So we took a chance, and re-engineered the loans system to focus squarely on transmitting money from one phone to another. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Vodafone](https://www.vodafone.com/news/newsroom/digital-society/m-pesa-created) (A) : « We wanted to have a ‘branch’ on every street corner, so we needed to recruit a huge network of agents. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (declaration, cle) — Selon Vodafone, M-Pesa comptait 1,2 million de clients à la fin de sa première année.  
  motif : source primaire (A) consultée : Vodafone
  - soutient — [Vodafone](https://www.vodafone.com/news/newsroom/digital-society/m-pesa-created) (A) : « At the end of the first year we had achieved 1.2 million customers » — extrait retrouvé dans la page récupérée par le moteur

**Faits restant à vérifier ou à recouper**

- *rapporté par une seule source fiable — à recouper* (chiffre, cle) — Selon une étude publiée dans Science (Suri et Jack, 2016), l'accès à l'argent mobile a sorti environ 194 000 ménages kényans (environ 2 %) de l'extrême pauvreté.  
  motif : une seule source fiable (MIT News (Massachusetts Institute of Technology)) — à recouper
  - soutient — [MIT News (Massachusetts Institute of Technology)](https://news.mit.edu/2016/mobile-money-kenyans-out-poverty-1208) (B) : « Published in today’s issue of Science, the study estimates that, since 2008, access to mobile-money services increased daily per capita consumption levels of 194,000 — or 2 percent — of Kenyan households, lifting them out of extreme poverty (living on less than $1.25 per day). » — extrait retrouvé dans la page récupérée par le moteur
- *rapporté par une seule source fiable — à recouper* (chiffre, secondaire) — L'effet a été plus fort pour les ménages dirigés par des femmes ; environ 185 000 femmes sont passées de l'agriculture au commerce.  
  motif : une seule source fiable (MIT News (Massachusetts Institute of Technology)) — à recouper
  - soutient — [MIT News (Massachusetts Institute of Technology)](https://news.mit.edu/2016/mobile-money-kenyans-out-poverty-1208) (B) : « But there’s an interesting gender effect: Female-headed households saw far greater increases in consumption than male-headed households. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [MIT News (Massachusetts Institute of Technology)](https://news.mit.edu/2016/mobile-money-kenyans-out-poverty-1208) (B) : « Moreover, mobile-money services have helped an estimated 185,000 women move from farming to business occupations. » — extrait retrouvé dans la page récupérée par le moteur
- *à vérifier* (fait, secondaire) — Le pilote a bénéficié d'un financement du ministère britannique du Développement international (DFID).  
  motif : uniquement des sources complémentaires (C) : insuffisant pour confirmer
  - soutient — [Wikipédia](https://en.wikipedia.org/wiki/M-Pesa) (C) : « DFID amended the terms of reference for its grant to Vodafone, and piloting began in 2005. » — extrait retrouvé dans la page récupérée par le moteur

**Sources**

- **[A]** Vodafone — [M-Pesa: creating the leading mobile money service](https://www.vodafone.com/news/newsroom/digital-society/m-pesa-created) · publiée n.d. · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Récit à la première personne d'un dirigeant de Vodafone : chiffres non audités, intérêt commercial ; date non affichée dans le texte capturé. | catégorie déclarée (A) : Témoignage direct de l'entreprise co-créatrice du service (source primaire, mais intéressée). — domaine hors registre, à revoir
- **[B]** MIT News (Massachusetts Institute of Technology) — [Study: Mobile-money services lift Kenyans out of poverty](https://news.mit.edu/2016/mobile-money-kenyans-out-poverty-1208) · publiée 2016-12-08 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : L'article original (Science, 2016) n'a PAS été consulté ; chiffres = estimations du modèle des auteurs. | catégorie déclarée (B) : Compte rendu par l'université de l'autrice d'une étude publiée dans Science. — domaine hors registre, à revoir
- **[C]** Wikipédia — [M-PESA — Wikipedia (EN)](https://en.wikipedia.org/wiki/M-Pesa) · publiée 2009-02-20 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Encyclopédie collaborative ; date détectée = création de l'article.

**Risques**

- Le chiffre de 194 000 ménages est une estimation modélisée ; l'article original de Science n'a pas été consulté.
- Les chiffres d'adoption viennent de Vodafone (source intéressée).
- Le blog LUKOJI a déjà traité l'argent mobile (licence de Wave en RDC) : l'angle « pivot » doit rester distinct.

---

## 2. Corridor de Lobito : pourquoi le cuivre congolais pourrait partir vers l'Atlantique

`SUJ-20261127-003` · proposé · Géopolitique · rdc · actualite

**Sujet.** Le corridor ferroviaire de Lobito, qui relie Kolwezi (RDC) au port angolais de Lobito, et son financement bouclé en juillet 2026 par la DBSA sud-africaine et la DFC américaine.

**Angle narratif.** Une voie ferrée qui redessine la carte d'exportation des minerais congolais : ce que le corridor promet (une sortie vers l'Atlantique), qui le finance et l'exploite, et la question que posent les médias africains : la RDC en profitera-t-elle ?

**Pourquoi c'est intéressant.** Sujet d'actualité qui touche directement l'économie de la RDC (cuivre et cobalt du Katanga), avec des enjeux d'emploi, de souveraineté et de rivalités entre puissances.

**Accroche potentielle.** « Pendant des décennies, le cuivre de Kolwezi est parti vers l'océan Indien. Un chemin de fer veut l'envoyer vers l'Atlantique. »

**Résumé du récit.** Le chemin de fer relie Kolwezi au port de Lobito : environ 1 289 km en Angola et 450 km en RDC, exploités par le concessionnaire Lobito Atlantic Railway (Trafigura, Mota-Engil, Vecturis). Le 31 juillet 2026, la DBSA et la DFC américaine annoncent le bouclage d'un financement de 786 millions de dollars. Les premières livraisons de cuivre et de cobalt d'EGC sont annoncées. Le projet est soutenu par les États-Unis et l'Europe ; la question des retombées pour la RDC reste ouverte et devra être documentée.

**Potentiel visuel.** Cartes animées des routes d'exportation (Atlantique contre océan Indien), images de trains et de port (à sourcer sous licence), infographies de financement.

**Formats.** short (soutenu), affiche (soutenu), documentaire (non soutenu — ≥ 4 faits confirmés et ≥ 3 organisations A/B)

**Score** (aide au tri, formule v1.0) : priorité **43.5** · attrait 79.5 · solidité 76.0 · faits clés confirmés 3/5 · risque factuel 3/5 · risque juridique 2/5 · difficulté 3/5

| Critère | Note | Justification |
|---|---|---|
| potentiel_narratif | 4/5 | Enjeu géographique clair et décision économique majeure. |
| interet_public | 5/5 | Concerne directement l'économie congolaise. |
| originalite | 3/5 | Très couvert par la presse spécialisée, peu par les médias grand public francophones. |
| potentiel_visuel | 4/5 | La carte suffit à raconter l'histoire. |
| potentiel_hook | 4/5 | Inversion de la route du cuivre. |
| pertinence_lukoji | 5/5 | RDC, investissement et infrastructures. |
| difficulté | 3/5 | Données techniques nombreuses et dispersées ; images de terrain à obtenir sous licence. |
| risque juridique | 2/5 | Entreprises et États nommés dans un cadre factuel ; la lecture géopolitique doit rester attribuée. |

**Signalements :** `famille_sensible:recoupement_renforce`, `format_non_soutenu:documentaire`, `categorie_source_declaree_a_revoir`

**Faits confirmés**

- *confirmé* (chiffre, cle) — Le 31 juillet 2026, la DBSA et la DFC américaine ont annoncé le bouclage financier de 786 millions de dollars pour le projet ferroviaire du corridor de Lobito.  
  motif : sujet sensible : 2 organisations indépendantes (Creamer Media (Engineering News), Development Bank of Southern Africa (DBSA))
  - soutient — [Development Bank of Southern Africa (DBSA)](https://www.dbsa.org/press-releases/dbsa-supports-financial-close-lobito-railway-project) (A) : « International Development Finance Corporation (DFC) have reached financial close on USD 786 million in the landmark Lobito Corridor Railway Project » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Creamer Media (Engineering News)](https://www.engineeringnews.co.za/article/lobito-corridor-railway-project-angolademocratic-republic-of-congo-update-2026-10-02) (B) : « announced financial close on $786-million in the Lobito Corridor railway project in July 2026 » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, cle) — Le corridor relie le Copperbelt de la RDC (Kolwezi) et de la Zambie au port de Lobito, en Angola, ouvrant une sortie vers l'Atlantique.  
  motif : sujet sensible : 2 organisations indépendantes (Creamer Media (Engineering News), Development Bank of Southern Africa (DBSA))
  - soutient — [Development Bank of Southern Africa (DBSA)](https://www.dbsa.org/press-releases/dbsa-supports-financial-close-lobito-railway-project) (A) : « linking the Copperbelt regions of the Democratic Republic of Congo and Zambia to the Port of Lobito in Angola, providing a western export gateway to the Atlantic Ocean for the two landlocked countries. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Creamer Media (Engineering News)](https://www.engineeringnews.co.za/article/lobito-corridor-railway-project-angolademocratic-republic-of-congo-update-2026-10-02) (B) : « The Lobito Atlantic Railway links Kolwezi, in the Democratic Republic of Congo (DRC) Copperbelt, to the Port of Lobito, in Angola. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, cle) — Le projet est porté par une coentreprise de Trafigura et Mota-Engil.  
  motif : sujet sensible : 2 organisations indépendantes (Creamer Media (Engineering News), Development Bank of Southern Africa (DBSA))
  - soutient — [Development Bank of Southern Africa (DBSA)](https://www.dbsa.org/press-releases/dbsa-supports-financial-close-lobito-railway-project) (A) : « The project is a joint venture between Mota-Engil and Trafigura » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Creamer Media (Engineering News)](https://www.engineeringnews.co.za/article/lobito-corridor-railway-project-angolademocratic-republic-of-congo-update-2026-10-02) (B) : « a consortium comprising Trafigura, Mota-Engil and Vecturis. » — extrait retrouvé dans la page récupérée par le moteur

**Faits restant à vérifier ou à recouper**

- *rapporté par une seule source fiable — à recouper* (chiffre, cle) — La ligne comprend environ 1 289 km en Angola (Lobito–Luau) et 450 km en RDC (Luau–Kolwezi), exploités via un accord d'accès avec la SNCC.  
  motif : sujet sensible : une seule organisation (Creamer Media (Engineering News)), 2 requises
  - soutient — [Creamer Media (Engineering News)](https://www.engineeringnews.co.za/article/lobito-corridor-railway-project-angolademocratic-republic-of-congo-update-2026-10-02) (B) : « The corridor comprises the 1 289 km Angola section between Lobito and Luau, on the Angola-DRC border, and a 450 km DRC section between Luau and Kolwezi operated under a track access agreement with the Société Nationale des Chemins de Fer du Congo (SNCC). » — extrait retrouvé dans la page récupérée par le moteur
  - nuance — [Creamer Media (Engineering News)](https://www.engineeringnews.co.za/article/lobito-corridor-railway-project-angolademocratic-republic-of-congo-update-2026-10-02) (B) : « together with the 1 300 km Angola railway from the Port of Lobito to Luau. » — extrait retrouvé dans la page récupérée par le moteur
- *rapporté par une seule source fiable — à recouper* (fait, cle) — Le projet bénéficie du soutien des États-Unis et de l'Europe.  
  motif : sujet sensible : une seule organisation (African Business (IC Publications)), 2 requises
  - soutient — [African Business (IC Publications)](https://african.business/2026/06/resources/lobito-corridor-leads-drc-transport-agenda) (B) : « The Lobito Corrirdor project to export DRC minerals to global markets has the backing of the US and Europe, but will it benefit the country? » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Wikipédia](https://en.wikipedia.org/wiki/Lobito_Corridor) (C) : « The project is supported via the G7 Partnership for Global Infrastructure and Investment (PGI) by the United States and the European Union through its Global Gateway initiative. » — extrait retrouvé dans la page récupérée par le moteur
- *rapporté par une seule source fiable — à recouper* (fait, secondaire) — La concession angolaise de 30 ans a été attribuée en 2022 au consortium qui inclut aussi Vecturis.  
  motif : sujet sensible : une seule organisation (Creamer Media (Engineering News)), 2 requises
  - soutient — [Creamer Media (Engineering News)](https://www.engineeringnews.co.za/article/lobito-corridor-railway-project-angolademocratic-republic-of-congo-update-2026-10-02) (B) : « LAR operates under a 30-year concession awarded by the Angolan government in 2022. » — extrait retrouvé dans la page récupérée par le moteur
- *rapporté par une seule source fiable — à recouper* (fait, secondaire) — EGC, entreprise publique qui achète le cobalt artisanal, et Trafigura ont conclu une première livraison de cuivre et de cobalt via le corridor.  
  motif : sujet sensible : une seule organisation (Creamer Media (Engineering News)), 2 requises
  - soutient — [Creamer Media (Engineering News)](https://www.engineeringnews.co.za/article/cobalt-and-copper-sourced-from-drc-artisanal-miners-to-be-transported-on-lobito-corridor-2026-02-09) (B) : « Entreprise Générale du Cobalt (EGC) and Trafigura have agreed the first delivery of copper and cobalt on the corridor. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Creamer Media (Engineering News)](https://www.engineeringnews.co.za/article/cobalt-and-copper-sourced-from-drc-artisanal-miners-to-be-transported-on-lobito-corridor-2026-02-09) (B) : « EGC is a State-owned entity mandated to purchase cobalt from artisanal producers in the DRC » — extrait retrouvé dans la page récupérée par le moteur
- *hypothèse (jamais présentée comme un fait)* (hypothese, secondaire) — Les États-Unis et l'Union européenne chercheraient, via ce corridor, à réduire la domination chinoise sur le secteur minier régional.  
  motif : type « hypothèse » : jamais confirmée par construction
  - soutient — [Wikipédia](https://en.wikipedia.org/wiki/Lobito_Corridor) (C) : « By supporting a westward-oriented export corridor, the US and EU are hoping to gain easier access to critical raw materials and to diminish the Chinese dominance in the region's mining sector. » — extrait retrouvé dans la page récupérée par le moteur

**Sources**

- **[A]** Development Bank of Southern Africa (DBSA) — [The DBSA Supports Financial Close of Landmark Lobito Corridor Railway Project](https://www.dbsa.org/press-releases/dbsa-supports-financial-close-lobito-railway-project) · publiée 2026-07-31 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Source partie prenante (prêteur) ; la date technique de la page (2021) est erronée, la date retenue est celle du texte : 31 juillet 2026. | catégorie déclarée (A) : Communiqué officiel de la banque de développement partie prenante au financement. — domaine hors registre, à revoir
- **[B]** African Business (IC Publications) — [Lobito Corridor leads DRC’s transport agenda](https://african.business/2026/06/resources/lobito-corridor-leads-drc-transport-agenda) · publiée 2026-06-16 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Seul le chapeau est lisible dans la capture (corps de l'article probablement réservé aux abonnés). | catégorie déclarée (B) : Magazine économique panafricain établi. — domaine hors registre, à revoir
- **[B]** Creamer Media (Engineering News) — [Lobito Corridor railway project, Angola/Democratic Republic of Congo – update](https://www.engineeringnews.co.za/article/lobito-corridor-railway-project-angolademocratic-republic-of-congo-update-2026-10-02) · publiée 2026-10-02 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Fiche de suivi de projet ; incohérence interne sur la longueur de la section angolaise (1 289 km puis 1 300 km). | catégorie déclarée (B) : Presse économique sud-africaine spécialisée dans les infrastructures et les mines. — domaine hors registre, à revoir
- **[B]** Creamer Media (Engineering News) — [Cobalt and copper sourced from DRC artisanal miners to be transported on Lobito corridor](https://www.engineeringnews.co.za/article/cobalt-and-copper-sourced-from-drc-artisanal-miners-to-be-transported-on-lobito-corridor-2026-02-09) · publiée 2026-02-09 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Même éditeur que la fiche d'octobre : ne compte pas comme organisation indépendante. | catégorie déclarée (B) : Presse économique sud-africaine spécialisée dans les infrastructures et les mines. — domaine hors registre, à revoir
- **[C]** Wikipédia — [Lobito Corridor — Wikipedia (EN)](https://en.wikipedia.org/wiki/Lobito_Corridor) · publiée 2025-12-06 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Encyclopédie collaborative : lecture géopolitique à recouper.

**Risques**

- Sujet classé géopolitique (sensible) : chaque fait clé exige deux organisations indépendantes.
- La lecture « contrer la Chine » ne repose que sur Wikipédia : à attribuer, jamais à affirmer.
- Les retombées locales et les critiques (habitants de Kolwezi) ne sont pas encore documentées par une source lue.
- La DBSA est partie prenante (prêteur).

---

## 3. InkubaLM : une IA sud-africaine pensée pour le swahili, le yoruba ou le zoulou

`SUJ-20261127-005` · proposé · Technologie et intelligence artificielle · afrique_australe · tendance

**Sujet.** InkubaLM, petit modèle de langage publié en 2024 par le laboratoire sud-africain Lelapa AI pour cinq langues africaines, et sa version compressée issue d'un concours en 2025.

**Angle narratif.** Plutôt que la course aux modèles géants, une start-up africaine parie sur une IA petite, frugale et entraînée sur des langues africaines : ce que cela change, et ses limites (licence non commerciale, évaluations partielles, langues de la RDC comme le lingala absentes).

**Pourquoi c'est intéressant.** L'IA en langues africaines est un enjeu d'accès et de souveraineté ; le swahili, parlé dans l'est de la RDC, est couvert, mais pas le lingala : un angle directement utile pour l'audience.

**Accroche potentielle.** « Les grandes IA parlent mal les langues africaines. Une équipe sud-africaine a construit la sienne, assez petite pour tourner sur un ordinateur portable. »

**Résumé du récit.** En 2024, Lelapa AI publie InkubaLM, un modèle de 0,4 milliard de paramètres entraîné sur 2,4 milliards de tokens, dont 1,9 milliard en isiZulu, yoruba, swahili, isiXhosa et haoussa. Le laboratoire le présente comme le premier petit modèle multilingue open source pour les langues africaines. Licence non commerciale, évaluations limitées à quatre tâches. En 2025, un concours organisé avec Zindi en réduit la taille de 75 %, selon Africanews.

**Potentiel visuel.** Motion design (tokens, langues, carte des locuteurs), interface de démonstration à filmer ; peu d'images réelles.

**Formats.** short (soutenu), affiche (soutenu)

**Score** (aide au tri, formule v1.0) : priorité **41.4** · attrait 62.5 · solidité 81.7 · faits clés confirmés 5/6 · risque factuel 2/5 · risque juridique 1/5 · difficulté 3/5

| Critère | Note | Justification |
|---|---|---|
| potentiel_narratif | 3/5 | Histoire d'innovation, moins de tension dramatique. |
| interet_public | 4/5 | L'IA intéresse fortement, l'angle linguistique est concret. |
| originalite | 4/5 | Peu couvert par les médias francophones. |
| potentiel_visuel | 2/5 | Sujet abstrait, tout reste à créer en motion design. |
| potentiel_hook | 4/5 | Contraste entre IA géantes et IA frugale africaine. |
| pertinence_lukoji | 4/5 | Tech et innovation africaines ; lien avec les langues de la RDC. |
| difficulté | 3/5 | Sujet technique à vulgariser sans erreur ; visuels à créer entièrement. |
| risque juridique | 1/5 | Informations publiques sur un produit ; revendications attribuées à l'entreprise. |

**Signalements :** `categorie_source_declaree_a_revoir`

**Faits confirmés**

- *confirmé* (chiffre, cle) — InkubaLM compte 0,4 milliard de paramètres.  
  motif : source primaire (A) consultée : Lelapa AI
  - soutient — [Lelapa AI](https://arxiv.org/html/2408.17024v2) (A) : « This paper introduces InkubaLM, a small language model with 0.4 billion parameters » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Lelapa AI](https://huggingface.co/lelapa/InkubaLM-0.4B) (A) : « we trained this InkubaLM with a parameter size of 0.4 billion and a vocabulary size of 61788. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, cle) — Il couvre l'isiZulu, le yoruba, le swahili, l'isiXhosa et le haoussa, ainsi que l'anglais et le français.  
  motif : source primaire (A) consultée : Lelapa AI
  - soutient — [Lelapa AI](https://huggingface.co/lelapa/InkubaLM-0.4B) (A) : « Language(s) (NLP): isiZulu, Yoruba, Swahili, isiXhosa, Hausa, English and French. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (chiffre, cle) — Il a été entraîné sur 2,4 milliards de tokens, dont 1,9 milliard dans cinq langues africaines.  
  motif : source primaire (A) consultée : Lelapa AI
  - soutient — [Lelapa AI](https://lelapa.ai/blog/inkubalm-small-language-model) (A) : « InkubaLM-0.4B is a 400-million parameter autoregressive language model trained from scratch using 2.4 billion total tokens. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Lelapa AI](https://huggingface.co/lelapa/InkubaLM-0.4B) (A) : « InkubaLM has been trained from scratch using 1.9 billion tokens of data for five African languages » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (declaration, cle) — Lelapa AI le présente comme le premier petit modèle de langage multilingue open source pour les langues africaines.  
  motif : source primaire (A) consultée : Lelapa AI
  - soutient — [Lelapa AI](https://arxiv.org/html/2408.17024v2) (A) : « we introduce InkubaLM, the first open-source small multilingual language model for African languages » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Africanews (groupe Euronews)](https://www.africanews.com/2025/05/31/african-ai-talent-shrinks-continents-first-multilingual-language-model-by-75) (B) : « Africa’s first multilingual Small Language Model (SLM), InkubaLM, has been reduced in size by an impressive 75%, without compromising performance. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, cle) — Sa licence (CC BY-NC 4.0) interdit l'usage commercial.  
  motif : source primaire (A) consultée : Lelapa AI
  - soutient — [Lelapa AI](https://huggingface.co/lelapa/InkubaLM-0.4B) (A) : « License: CC BY-NC 4.0. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (declaration, secondaire) — Selon Lelapa AI, le modèle peut fonctionner sur CPU, y compris sur un ordinateur portable.  
  motif : source primaire (A) consultée : Lelapa AI
  - soutient — [Lelapa AI](https://lelapa.ai/blog/inkubalm-small-language-model) (A) : « The model supports CPU, GPU, and multi-GPU deployment, making it viable for resource-constrained environments including laptop computers. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, secondaire) — Ses évaluations se limitent à quatre tâches, et de plus grands modèles le dépassent sur certaines.  
  motif : source primaire (A) consultée : Lelapa AI
  - soutient — [Lelapa AI](https://huggingface.co/lelapa/InkubaLM-0.4B) (A) : « The model is evaluated only in sentiment analysis, machine translation, AfriMMLU, and AfriXNLI tasks » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Lelapa AI](https://lelapa.ai/blog/inkubalm-small-language-model) (A) : « though larger models like Gemma-7B and LLaMA 3-8B showed superior performance. » — extrait retrouvé dans la page récupérée par le moteur

**Faits restant à vérifier ou à recouper**

- *rapporté par une seule source fiable — à recouper* (chiffre, cle) — En 2025, un concours organisé avec Zindi (490 participants de 61 pays) a réduit sa taille de 75 %, selon Africanews.  
  motif : une seule source fiable (Africanews (groupe Euronews)) — à recouper
  - soutient — [Africanews (groupe Euronews)](https://www.africanews.com/2025/05/31/african-ai-talent-shrinks-continents-first-multilingual-language-model-by-75) (B) : « Out of 490 participants from 61 countries, the top winners, all from Africa—demonstrated the continent’s growing strength in AI innovation. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Africanews (groupe Euronews)](https://www.africanews.com/2025/05/31/african-ai-talent-shrinks-continents-first-multilingual-language-model-by-75) (B) : « has been reduced in size by an impressive 75%, without compromising performance. » — extrait retrouvé dans la page récupérée par le moteur

**Sources**

- **[A]** Lelapa AI — [InkubaLM: A small language model for low-resource African languages (arXiv v2)](https://arxiv.org/html/2408.17024v2) · publiée 2024-09-03 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Prépublication non relue par des pairs ; auteurs = équipe de Lelapa AI (pas une source indépendante).
- **[A]** Lelapa AI — [lelapa/InkubaLM-0.4B · Hugging Face](https://huggingface.co/lelapa/InkubaLM-0.4B) · publiée 2024-09-05 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Fichiers du modèle derrière une acceptation de conditions ; la fiche ne donne pas de chiffres de benchmark. | catégorie déclarée (A) : Fiche technique publiée par Lelapa AI sur son dépôt officiel (publication originale). — domaine hors registre, à revoir
- **[A]** Lelapa AI — [InkubaLM: A Small Language Model for Low-Resource African Languages](https://lelapa.ai/blog/inkubalm-small-language-model) · publiée 2024-10-25 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Communication de l'entreprise elle-même. | catégorie déclarée (A) : Billet officiel du laboratoire auteur du modèle (source primaire, intéressée). — domaine hors registre, à revoir
- **[B]** Africanews (groupe Euronews) — [Africa’s First Multilingual Small Language Model Gets Even Smaller - Thanks to Top African Innovator](https://www.africanews.com/2025/05/31/african-ai-talent-shrinks-continents-first-multilingual-language-model-by-75) · publiée 2025-05-31 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Ton proche d'un communiqué (citations des PDG de Lelapa AI et de Zindi) ; chiffres non recoupés indépendamment. | catégorie déclarée (B) : Chaîne d'information panafricaine du groupe Euronews. — domaine hors registre, à revoir

**Risques**

- Toutes les sources techniques émanent de Lelapa AI (arXiv, fiche Hugging Face, blog) : aucune évaluation indépendante consultée.
- La réduction de 75 % « sans perte de performance » est une affirmation des organisateurs, relayée par Africanews.
- La prépublication arXiv n'est pas relue par des pairs.

---

## 4. Tulipomanie : la plus célèbre bulle de l'histoire a-t-elle vraiment ruiné la Hollande ?

`SUJ-20261127-004` · proposé · Histoires méconnues · europe · historique

**Sujet.** La « tulipomanie » néerlandaise de 1636-1637 et la remise en cause de son récit populaire par l'historienne Anne Goldgar.

**Angle narratif.** Démonter un mythe cité dans toutes les formations à l'investissement : la ruine collective racontée par Charles Mackay en 1841 ne résiste pas aux archives ; la vraie crise fut une crise de confiance et de contrats non honorés. Leçon : vérifier les histoires que tout le monde répète.

**Pourquoi c'est intéressant.** Sujet intemporel, contre-intuitif, qui forme l'esprit critique de l'audience face aux récits de « bulles » (cryptomonnaies, actions) ; diversifie les territoires de LUKOJI.

**Accroche potentielle.** « On vous a raconté que des tulipes avaient ruiné un pays. Une historienne a fouillé les archives : elle n'a trouvé personne qui ait fait faillite. »

**Résumé du récit.** Entre 1636 et février 1637, certains bulbes de tulipes atteignent des prix extraordinaires aux Provinces-Unies, puis le marché s'effondre. En 1841, Charles Mackay popularise l'image d'un pays entier ruiné. Au XXIe siècle, Anne Goldgar étudie les archives : peu de participants, des répercussions économiques mineures ; le krach a surtout ébranlé la confiance et l'honneur commercial, dans un marché de contrats à terme sans recours judiciaire.

**Potentiel visuel.** Peintures et gravures du Siècle d'or néerlandais (souvent dans le domaine public), catalogues de tulipes de 1637, typographie animée « mythe contre archives ».

**Formats.** short (soutenu), affiche (soutenu), documentaire (non soutenu — ≥ 4 faits confirmés et ≥ 3 organisations A/B)

**Score** (aide au tri, formule v1.0) : priorité **37.0** · attrait 79.0 · solidité 61.7 · faits clés confirmés 2/4 · risque factuel 3/5 · risque juridique 1/5 · difficulté 2/5

| Critère | Note | Justification |
|---|---|---|
| potentiel_narratif | 4/5 | Retournement : le mythe contre les archives. |
| interet_public | 4/5 | Les « bulles » passionnent l'audience intéressée par l'investissement. |
| originalite | 5/5 | Angle de démystification rare dans les médias francophones. |
| potentiel_visuel | 4/5 | Peintures du Siècle d'or et catalogues d'époque. |
| potentiel_hook | 5/5 | Accroche contre-intuitive très forte. |
| pertinence_lukoji | 3/5 | Leçon d'économie et d'esprit critique, hors Afrique. |
| difficulté | 2/5 | Iconographie largement libre de droits ; récit compact. |
| risque juridique | 1/5 | Sujet historique, aucune personne vivante mise en cause. |

**Signalements :** `format_non_soutenu:documentaire`, `categorie_source_declaree_a_revoir`

**Faits confirmés**

- *confirmé* (fait, cle) — Les prix des tulipes se sont effondrés en février 1637.  
  motif : source primaire (A) consultée : University of Chicago Press
  - soutient — [Smithsonian Magazine](https://www.smithsonianmag.com/history/there-never-was-real-tulip-fever-180964915/) (B) : « But by February 1637, the bottom fell out of the market. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [University of Chicago Press](https://press.uchicago.edu/Misc/Chicago/301259.html) (A) : « In early February 1637, the bottom fell out of the market. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (declaration, cle) — Selon Anne Goldgar, le krach a ébranlé la confiance et l'honneur plus que l'économie ; elle dit n'avoir trouvé personne qui ait fait faillite.  
  motif : source primaire (A) consultée : University of Chicago Press
  - soutient — [University of Chicago Press](https://press.uchicago.edu/Misc/Chicago/301259.html) (A) : « The crash in prices undermined not the economy, but people’s confidence in honor and good judgment. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [Smithsonian Magazine](https://www.smithsonianmag.com/history/there-never-was-real-tulip-fever-180964915/) (B) : « “There weren’t that many people involved and the economic repercussions were pretty minor,” Goldgar says. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, secondaire) — Les ventes se faisaient par contrats de paiement et de livraison futurs, car les bulbes restaient en terre.  
  motif : source primaire (A) consultée : University of Chicago Press
  - soutient — [University of Chicago Press](https://press.uchicago.edu/Misc/Chicago/301259.html) (A) : « Because for most of the year the bulbs were in the ground, sales came to take the form of contracts for future payment and delivery. » — extrait retrouvé dans la page récupérée par le moteur

**Faits restant à vérifier ou à recouper**

- *rapporté par une seule source fiable — à recouper* (fait, cle) — Le récit populaire de la ruine générale vient largement du livre de Charles Mackay paru en 1841.  
  motif : une seule source fiable (Smithsonian Magazine) — à recouper
  - soutient — [Smithsonian Magazine](https://www.smithsonianmag.com/history/there-never-was-real-tulip-fever-180964915/) (B) : « wrote Scottish journalist Charles Mackay in his popular 1841 work Extraordinary Popular Delusions and the Madness of Crowds. » — extrait retrouvé dans la page récupérée par le moteur
- *à vérifier* (chiffre, cle) — Selon Goldgar, environ 350 personnes seulement ont participé au commerce et 37 ont payé plus de 300 florins pour un bulbe.  
  motif : aucune preuve
- *rapporté par une seule source fiable — à recouper* (fait, secondaire) — Des marchands ont bien payé des prix très élevés pour certains bulbes.  
  motif : une seule source fiable (Smithsonian Magazine) — à recouper
  - soutient — [Smithsonian Magazine](https://www.smithsonianmag.com/history/there-never-was-real-tulip-fever-180964915/) (B) : « merchants really did engage in a frantic tulip trade, and they paid incredibly high prices for some bulbs. » — extrait retrouvé dans la page récupérée par le moteur
- *contradictoire — sources en désaccord* (fait, secondaire) — La tulipomanie a provoqué l'effondrement de l'économie néerlandaise (récit populaire).  
  motif : 1 source(s) A/B contredisent (Smithsonian Magazine)
  - contredit — [Smithsonian Magazine](https://www.smithsonianmag.com/history/there-never-was-real-tulip-fever-180964915/) (B) : « But the trade didn’t affect all levels of society, and it didn’t cause the collapse of industry in Amsterdam and elsewhere. » — extrait retrouvé dans la page récupérée par le moteur
- *à vérifier* (chiffre, secondaire) — Le bulbe Semper Augustus aurait atteint 10 000 florins.  
  motif : uniquement des sources complémentaires (C) : insuffisant pour confirmer
  - soutient — [Wikipédia](https://en.wikipedia.org/wiki/Tulip_mania) (C) : « The Semper Augustus was the most expensive tulip during the mania,[4] which at its peak sold for ƒ10,000 » — extrait retrouvé dans la page récupérée par le moteur

**Sources**

- **[A]** University of Chicago Press — [Tulipmania: Money, Honor, and Knowledge in the Dutch Golden Age by Anne Goldgar, an excerpt](https://press.uchicago.edu/Misc/Chicago/301259.html) · publiée n.d. · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Extrait partiel du livre ; date de mise en ligne non indiquée. | catégorie déclarée (A) : Extrait du livre de l'historienne, publié par son éditeur universitaire (publication originale, 2007). — domaine hors registre, à revoir
- **[B]** Smithsonian Magazine — [There Never Was a Real Tulip Fever](https://www.smithsonianmag.com/history/there-never-was-real-tulip-fever-180964915/) · publiée 2017-09-18 · consultée 2026-11-27 · page_verifiee · disponible
- **[C]** Wikipédia — [Tulip mania — Wikipedia (EN)](https://en.wikipedia.org/wiki/Tulip_mania) · publiée 2003-03-30 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Encyclopédie collaborative ; reprend en partie le récit classique.

**Risques**

- Les chiffres de Goldgar (environ 350 participants, 37 acheteurs à plus de 300 florins) ne sont connus que par un résumé de recherche : à vérifier dans le livre ou dans l'article de History Today.
- Ne pas remplacer un mythe par un autre : la thèse de Goldgar est elle-même discutée par certains historiens.

---

## 5. Air Afrique : onze pays, une compagnie, et pourquoi le rêve s'est écrasé

`SUJ-20261127-001` · proposé · Échecs d'entreprises · afrique · historique

**Sujet.** L'histoire d'Air Afrique, compagnie aérienne multinationale fondée en 1961 par onze États africains et liquidée en 2002.

**Angle narratif.** Raconter Air Afrique comme une leçon de gouvernance partagée : ce qui arrive quand onze actionnaires publics possèdent une même entreprise, de l'ambition panafricaine des Indépendances à la liquidation, et ce que sa disparition a coûté en liaisons aériennes.

**Pourquoi c'est intéressant.** Sujet panafricain et francophone, encore vivant dans la mémoire des passagers et des anciens salariés ; il éclaire les débats actuels sur les compagnies régionales et l'intégration africaine, et offre une leçon universelle sur la gouvernance à plusieurs actionnaires.

**Accroche potentielle.** « En 1961, onze pays africains ont mis leurs avions en commun. Quarante et un ans plus tard, un tribunal d'Abidjan a tout liquidé. »

**Résumé du récit.** 1961 : à Yaoundé, onze États créent une compagnie commune pour leurs liaisons extérieures. Pendant quarante ans, Air Afrique dessert l'Afrique et l'Europe (168 lignes directes en 2001). Les plans de sauvetage se succèdent, jusqu'au projet d'une « Nouvelle Air Afrique » où Air France prendrait une place prépondérante. En 2002, la compagnie est déclarée en faillite puis liquidée ; une trentaine de liaisons disparaissent. Reste à documenter solidement les causes de l'échec.

**Potentiel visuel.** Archives (avions, affiches, billets), cartes animées du réseau de 2001 et des lignes disparues, frise chronologique. Attention : la plupart des photos d'archives sont sous droits.

**Formats.** documentaire (non soutenu — ≥ 4 faits confirmés et ≥ 3 organisations A/B), short (soutenu)

**Score** (aide au tri, formule v1.0) : priorité **22.1** · attrait 80.0 · solidité 40.7 · faits clés confirmés 2/5 · risque factuel 3/5 · risque juridique 2/5 · difficulté 4/5 · **⚠ non prioritaire**

| Critère | Note | Justification |
|---|---|---|
| potentiel_narratif | 5/5 | Arc complet : ambition, apogée, crises, sauvetages ratés, chute. |
| interet_public | 4/5 | Mémoire collective forte en Afrique francophone. |
| originalite | 3/5 | Sujet déjà traité en série par Jeune Afrique ; l'angle « gouvernance à onze actionnaires » reste peu exploité. |
| potentiel_visuel | 4/5 | Cartes et archives très parlantes, mais droits à négocier. |
| potentiel_hook | 4/5 | Contraste fort entre l'unité de 1961 et la liquidation de 2002. |
| pertinence_lukoji | 5/5 | Entrepreneuriat, gestion et leçons d'échec en Afrique francophone. |
| difficulté | 4/5 | Récit riche mais archives visuelles sous droits et causes de la faillite encore à documenter par des sources primaires. |
| risque juridique | 2/5 | Évoquer la gestion de dirigeants identifiables exige des formulations attribuées ; aucune accusation nominative n'est prévue. |

**Signalements :** `insuffisamment_documente`, `format_non_soutenu:documentaire`

**Faits confirmés**

- *confirmé* (fait, cle) — Air Afrique a été fondée en 1961 à Yaoundé par onze États africains.  
  motif : 2 sources secondaires fiables indépendantes (Jeune Afrique, OpenEdition)
  - soutient — [Jeune Afrique](https://www.jeuneafrique.com/1131024/economie-entreprises/qui-a-tue-air-afrique-4-6/) (B) : « Le 28 mars 1961, à Yaoundé, onze pays posent les jalons de leur compagnie commune. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [OpenEdition](https://journals.openedition.org/belgeo/11279?lang=en) (B) : « fondée en 1961 par le traité de Yaoundé, signé par onze États de l’Afrique de l’ouest et centrale » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, cle) — Sa faillite a fait disparaître des liaisons aériennes que d'autres compagnies n'ont pas reprises.  
  motif : 2 sources secondaires fiables indépendantes (Jeune Afrique, OpenEdition)
  - soutient — [Jeune Afrique](https://www.jeuneafrique.com/1147592/economie-entreprises/apres-la-mort-dair-afrique-des-liaisons-aeriennes-orphelines/) (B) : « Si certaines ont été reprises, une trentaine, comme Conakry-Monrovia, Abidjan-Zurich ou Kinshasa-Cotonou, ont disparu. » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [OpenEdition](https://journals.openedition.org/belgeo/11279?lang=en) (B) : « whose bankruptcy in 2002 led to the disappearance of intra- and extra-African air links which were not taken over by other air companies. » — extrait retrouvé dans la page récupérée par le moteur
- *confirmé* (fait, secondaire) — En 2001, un projet de « Nouvelle Air Afrique » prévoyait une place prépondérante d'Air France au capital (35 % selon Belgeo).  
  motif : 2 sources secondaires fiables indépendantes (Jeune Afrique, OpenEdition)
  - soutient — [Jeune Afrique](https://www.jeuneafrique.com/1131024/economie-entreprises/qui-a-tue-air-afrique-4-6/) (B) : « projet de création d’une Nouvelle Air Afrique, avec une place prépondérante d’Air France au capital, esquissé en 2001 » — extrait retrouvé dans la page récupérée par le moteur
  - soutient — [OpenEdition](https://journals.openedition.org/belgeo/11279?lang=en) (B) : « La France propose alors la création d’une nouvelle compagnie Air Afrique dont Air France apporterait 35 % du capital » — extrait retrouvé dans la page récupérée par le moteur

**Faits restant à vérifier ou à recouper**

- *rapporté par une seule source fiable — à recouper* (fait, cle) — La liquidation judiciaire a été prononcée le 25 avril 2002 par le tribunal de commerce d'Abidjan.  
  motif : une seule source fiable (Jeune Afrique) — à recouper
  - soutient — [Jeune Afrique](https://www.jeuneafrique.com/1131024/economie-entreprises/qui-a-tue-air-afrique-4-6/) (B) : « Le 25 avril 2002, le tribunal de commerce d’Abidjan prononçait la liquidation judiciaire de la compagnie, après quarante et un ans d’exercice. » — extrait retrouvé dans la page récupérée par le moteur
  - nuance — [OpenEdition](https://journals.openedition.org/belgeo/11279?lang=en) (B) : « Après diverses tergiversations, Air Afrique est définitivement déclarée en faillite en février 2002. » — extrait retrouvé dans la page récupérée par le moteur
- *rapporté par une seule source fiable — à recouper* (chiffre, cle) — En 2001, Air Afrique desservait une trentaine de pays et exploitait 168 lignes directes.  
  motif : une seule source fiable (Jeune Afrique) — à recouper
  - soutient — [Jeune Afrique](https://www.jeuneafrique.com/1147592/economie-entreprises/apres-la-mort-dair-afrique-des-liaisons-aeriennes-orphelines/) (B) : « En 2001, à la veille de sa faillite, Air Afrique assurait la desserte d’une trentaine de pays d’Afrique et du monde et exploitait 168 lignes directes » — extrait retrouvé dans la page récupérée par le moteur
- *à vérifier* (fait, cle) — Mauvaise gestion, corruption et crise du transport aérien après le 11 septembre 2001 ont conduit à la crise finale.  
  motif : uniquement des sources complémentaires (C) : insuffisant pour confirmer
  - soutient — [Wikipédia](https://en.wikipedia.org/wiki/Air_Afrique) (C) : « Mismanagement, corruption, and the downturn in the aviation industry after the 11 September 2001 attacks led the airline to a crisis that ended with its liquidation in early 2002. » — extrait retrouvé dans la page récupérée par le moteur

**Sources**

- **[B]** Jeune Afrique — [Qui a tué Air Afrique ? (4/6)](https://www.jeuneafrique.com/1131024/economie-entreprises/qui-a-tue-air-afrique-4-6/) · publiée 2021-03-31 · consultée 2026-11-27 · page_verifiee · disponible
- **[B]** Jeune Afrique — [Après la mort d’Air Afrique, des liaisons aériennes orphelines](https://www.jeuneafrique.com/1147592/economie-entreprises/apres-la-mort-dair-afrique-des-liaisons-aeriennes-orphelines/) · publiée 2021-04-04 · consultée 2026-11-27 · page_verifiee · disponible
- **[B]** OpenEdition — [Marginalisation et dépendance aérienne de l’Afrique sub-saharienne (Belgeo)](https://journals.openedition.org/belgeo/11279?lang=en) · publiée n.d. · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Article académique ; date de publication non détectée automatiquement.
- **[C]** Wikipédia — [Air Afrique — Wikipedia (EN)](https://en.wikipedia.org/wiki/Air_Afrique) · publiée 2005-06-24 · consultée 2026-11-27 · page_verifiee · disponible
  - limites : Encyclopédie collaborative ; la phrase sur les causes porte la mention [citation needed]. Date détectée = création de l'article.

**Risques**

- La date de fin diverge selon les sources (faillite en février, liquidation le 25 avril 2002) : à présenter avec précision.
- Les causes (mauvaise gestion, corruption, 11 septembre) ne reposent pour l'instant que sur Wikipédia, avec un [citation needed].
- Jeune Afrique a publié une série de six épisodes en 2021 : l'angle doit s'en distinguer.

---
