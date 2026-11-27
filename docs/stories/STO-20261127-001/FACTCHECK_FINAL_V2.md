# Fact-check final — pilote M-Pesa, script v2

`STO-20261127-001` · vérification du 27/11/2026 · script examiné : **v2** (moteur v13). Script corrigé : **v2.1** (moteur v16).

**Statut : NON VALIDÉ.** Le projet reste en `structure_draft` et aucune validation humaine n'a été enregistrée. Ce document éclaire une décision éditoriale humaine ; il ne certifie pas la vérité du documentaire.

## Méthode

- **Sources lues.** Une session en lecture seule (environnement « LUKOJI Fact-check », approuvé par l'utilisateur) a lu les documents avec curl et pdftotext. Elle n'a gardé que de courts extraits.
- **Résultats de recherche.** Ils ont servi à trouver les documents ; aucun n'est compté comme une source consultée.
- **Protections.** Aucune n'a été contournée : Cloudflare, page anti-robots « Anubis », erreur 403.
- **Niveaux de corroboration** :
  - **primaire lue** : le document original lui-même a été lu ;
  - **corroborée** : au moins deux organisations indépendantes, lues ;
  - **même sphère** : plusieurs documents liés à la même organisation (par exemple Vodafone et l'équipe projet de Vodafone) ;
  - **source unique** : une seule organisation ;
  - **non vérifiée** : aucune source primaire lue.
- **Décisions** :
  - `KEEP` : conserver tel quel ;
  - `KEEP_WITH_ATTRIBUTION` : conserver, avec l'attribution présente dans la voix off ;
  - `REFORMULATE` : formulation corrigée dans le script v2.1 ;
  - `REMOVE` : retiré du script v2.1 ;
  - `PENDING_VERIFICATION` : non utilisé tant que ce n'est pas vérifié.

## Sources réellement consultées pendant ce fact-check

| Réf. | Document | Date | Accès |
|---|---|---|---|
| Science 2016 | Suri & Jack, « The long-run poverty and gender impacts of mobile money », *Science* 354(6317), p. 1288-1292 | 09/12/2016 | Copie hébergée par FinDev Gateway, lue (science.org bloqué par Cloudflare) |
| Supplément Science | Supplementary materials (Jack & Suri), copie sur jefftk.com | 11/2016 | Lu |
| NBER w16721 | Jack & Suri, « Mobile Money: The Economics of M-PESA » | 01/2011 | Lu (nber.org) |
| FinAccess 2006 | « Financial Access in Kenya – Results of the 2006 National Survey », FSD Kenya et Financial Access Partnership | 10/2007 | Lu (hébergé par la Banque centrale du Kenya) |
| FinAccess 2019 | « 2019 FinAccess Household Survey », Banque centrale du Kenya, KNBS et FSD Kenya | 04/2019 | Lu |
| Hughes & Lonie 2007 | « M-PESA: Mobile Money for the “Unbanked” », *Innovations* (MIT Press) 2(1-2) | 2007 | Lu (copie miroir de l'Université de Zurich) |
| CGAP 2009 | Morawczynski & Pickens, « Poor People Using Mobile Financial Services », CGAP / Banque mondiale | 08/2009 | Lu |
| Vodafone 2017 | « M-Pesa: creating the leading mobile money service », signé Michael Joseph | 06/03/2017 | Lu |
| Vodafone 2022 | « M-Pesa – Africa's leading fintech platform – marks 15 years » | 07/03/2022 | Lu |
| Safaricom FY25 | Communiqué web des résultats de l'exercice 2025 | 09/05/2025 | Lu (le PDF renvoie HTTP 403) |
| The Star | « Senators reignite push to split Safaricom » | 17/11/2020 | Lu |
| FSD Kenya | « Digital credit audit report » | 09/2019 | Lu |
| Banque centrale du Kenya | Page des communiqués ; communiqué du 26/01/2009 (Zain) | 26/01/2009 | Lu |

**Inaccessibles ou introuvables** :
- **science.org** : Cloudflare.
- **journals.openedition.org** : protection anti-robots « Anubis ». La présentation de thèse ne repose que sur la capture « extraits seulement » de la phase 1.
- **agenceecofin.com** : Cloudflare. Les faits Ecofin ne reposent que sur les captures de la phase 1.
- **Safaricom** : PDF du communiqué FY25 (HTTP 403) et rapport annuel de l'exercice 2022 (paris en ligne), non trouvé.
- **Communiqué de la Banque centrale sur M-PESA de janvier 2009** : introuvable.
- **Stratégie nationale d'inclusion financière 2025-2028** (objectif de 23 → 10 KES) : non recherchée dans une source primaire.
- **direct.mit.edu** : non essayé.

## Registre

| ID | Affirmation (script v2) | Séq. | Source principale | Source secondaire | Réellement consultée | Date | Corroboration | Limites | Décision |
|---|---|---|---|---|---|---|---|---|---|
| FC-01 (F61, F73) | « on pouvait voyager pendant des jours » | SEQ-01 | Vodafone 2017 (« travel for days to get home ») | CGAP 2009 (« could take over a week ») | Vodafone 2017, CGAP 2009 | 2017 ; 2009 (terrain 2007-2008) | **corroborée** (CGAP indépendant) | CGAP : femmes rurales à Kibera et Bukura, voyage vers la ville ou le bureau de poste ; terrain en partie postérieur au lancement, mais il décrit la pratique antérieure | **KEEP** |
| FC-02 (F61, F72, F73) | « Ou confier ses billets à un chauffeur de bus » | SEQ-01 | Vodafone 2017 (« give the money to a bus driver ») | FinAccess 2006, tableau 8.5 : « Through a bus or matatu company » (21,6 % des receveurs, 29,4 % des envoyeurs) ; Hughes & Lonie (« disguised parcels by bus ») | Les trois | 2017 ; 2007 ; 2007 | **corroborée** | « Chauffeur » : Vodafone seule ; FinAccess dit « compagnie de bus ou de matatu ». L'image du matatu de 2025 ne démontre rien : elle reste mentionnée comme image d'illustration | **KEEP** |
| FC-03 (F43) | « Aujourd'hui, quelques SMS suffisent » | SEQ-01 | Vodafone 2017 | Hughes & Lonie | Vodafone 2017 | 2017 | même sphère | Fonctionnement de base, peu contestable | **KEEP** |
| FC-04 (F8, F76) | « ses concepteurs ne l'avaient pas inventé pour ça » | SEQ-01 | Hughes & Lonie : « the standard loan repayments for which we had designed the system » | Vodafone 2017 | Les deux | 2007 ; 2017 | même sphère (équipe Vodafone) | Aucune source indépendante de Vodafone sur l'intention initiale | **KEEP** |
| FC-05 (F51 → F74) | « En 2006, selon Agence Ecofin qui la cite, seuls 27 % des Kényans ont accès à des produits ou des services financiers » | SEQ-02 | FinAccess 2019 : formel 26,7 % en 2006 (série harmonisée) | FinAccess 2006 original : « 26.4% are formally served » (banque et assurance 18,9 %, coopératives et microfinance 7,5 %) | Les deux | 2019 ; 2007 | **primaire lue** | Il s'agit d'accès FORMEL, chez les adultes de 18 ans et plus ; 35,2 % utilisaient des services informels en 2006. L'écart 26,4 / 26,7 vient d'un reclassement non expliqué | **REFORMULATE** → « seuls 26,7 % des adultes kényans utilisent un service financier formel, comme une banque ou une assurance » |
| FC-06 (F41, F77) | « le ministère britannique… cherche des entreprises… pour les personnes qui n'ont pas de compte » ; « Selon Vodafone, l'entreprise… obtient une subvention » | SEQ-02 | Vodafone 2017 et 2022 | Hughes & Lonie : Financial Deepening Challenge Fund du DFID, près d'un million de livres égalé par Vodafone | Les trois | 2017 ; 2022 ; 2007 | même sphère | Aucun document du DFID lu | **KEEP_WITH_ATTRIBUTION** |
| FC-07 (F42) | « le projet se monte avec l'opérateur Safaricom » | SEQ-03 | Vodafone 2022 | Hughes & Lonie ; Agence Ecofin 2023 (capture) | Vodafone 2022, Hughes & Lonie | 2022 ; 2007 | corroborée | — | **KEEP** |
| FC-08 (F62) | « Michael Joseph, ancien directeur général de Safaricom, raconte la suite dans un texte publié par Vodafone » | SEQ-03 | Vodafone 2017 (signature « Vodafone Group's Director of Mobile Money ») | Agence Ecofin (capture : « l'ancien PDG de Safaricom ») | Vodafone 2017 ; Ecofin via la capture de la phase 1 | 2017 | source unique pour « ancien DG » | Fonction chez Safaricom attestée par Ecofin seule dans ce dossier | **KEEP** |
| FC-09 (F8, F76) | « L'équipe travaille sur le microcrédit : verser de petits prêts par téléphone, et les faire rembourser » | SEQ-03 | Hughes & Lonie (partenaire : Faulu Kenya, institution de microfinance) | Vodafone 2017 | Les deux | 2007 ; 2017 | même sphère | — | **KEEP_WITH_ATTRIBUTION** (« explique-t-il ») |
| FC-10 (F8 → F76) | « Le prototype est testé à Thika, au nord de Nairobi » | SEQ-03 | Hughes & Lonie : pilote lancé le 11/10/2005 dans le centre de Nairobi, à Mathare et à Thika | Vodafone 2017 (Thika seule) | Les deux | 2007 | même sphère | Thika n'était qu'un des trois lieux | **REFORMULATE** → « testé à partir d'octobre 2005, à Nairobi et à Thika, au nord de la capitale » |
| FC-11 (F8) | « Ceux qui reçoivent un prêt envoient l'argent à d'autres personnes, parfois à des centaines de kilomètres » | SEQ-04 | Vodafone 2017 (« hundreds of miles away ») | Hughes & Lonie : « we observed several other applications » (crédit de communication envoyé à des proches « as a kind of informal remittance », argent pour un billet de bus) | Les deux | 2017 ; 2007 | même sphère | Hughes & Lonie ne disent pas explicitement que les PRÊTS étaient renvoyés à des centaines de kilomètres ; c'est le récit de 2017 | **KEEP_WITH_ATTRIBUTION** (séquence attribuée à Michael Joseph) |
| FC-12 (F63) | « « Alors nous avons pris un risque », raconte Michael Joseph » | SEQ-04 | Vodafone 2017 : « So we took a chance » | — | Vodafone 2017 | 2017 | primaire lue (citation) | Traduction ; l'original doit rester à l'écran | **KEEP_WITH_ATTRIBUTION** |
| FC-13 (F9) | « Le système de prêts est reconstruit autour d'une seule fonction » | SEQ-04 | Vodafone 2017 | — | Vodafone 2017 | 2017 | source unique | — | **KEEP_WITH_ATTRIBUTION** |
| FC-14 (F43, F44) | Mécanisme des agents ; « petites boutiques familiales » | SEQ-05 | Vodafone 2017 | Hughes & Lonie (agents) | Vodafone 2017 | 2017 | même sphère | — | **KEEP_WITH_ATTRIBUTION** (« raconte Vodafone ») |
| FC-15 (F45) | Conditions de la Banque centrale avant le lancement | SEQ-06 | Agence Ecofin (capture) | Vodafone 2017 (enregistrement des clients) | Captures seulement (Ecofin non relu) | n.d. | source unique | Aucun document de la Banque centrale lu sur ce point | **KEEP_WITH_ATTRIBUTION** (« selon Agence Ecofin » ajouté) |
| FC-16 (F7) | « M-Pesa est lancé en mars 2007 » | SEQ-06 | Vodafone 2022 (« Launched on 6 March 2007 ») | Vodafone 2017 ; Hughes & Lonie | Vodafone 2017 et 2022 | 2022 | corroborée | — | **KEEP** |
| FC-17 (F46) | « des banques y voient une incursion dans leur métier » | SEQ-06 | Agence Ecofin (capture) | — | Capture seulement | n.d. | source unique | Banques non nommées | **KEEP_WITH_ATTRIBUTION** |
| FC-18 (F66, F83) | « Le débat devient public. Le 27 janvier 2009, la Banque centrale publie un communiqué pour rassurer. … « la réglementation traîne généralement derrière l'innovation » » | SEQ-06 | Agence Ecofin (capture) | Banque centrale : le seul communiqué de janvier 2009 trouvé (26/01) porte sur **Zain** (« CBK DOES NOT REGULATE MOBILE PHONE PROVIDERS SUCH AS ZAIN ») | Page des communiqués de la Banque centrale, communiqué du 26/01/2009 | 26/01/2009 | **contredite / introuvable** | Citation introuvable dans une source primaire. Selon des résultats de recherche non lus, c'est le Trésor qui aurait jugé le service sûr en janvier 2009, après un audit demandé fin 2008 | **REMOVE** |
| FC-19 (F10) | « Vodafone annonce 1,2 million d'utilisateurs à la fin de la première année » | SEQ-07 | Vodafone 2017 (capture) | — | Capture | 2017 | source unique (entreprise) | Chiffre non audité | **KEEP_WITH_ATTRIBUTION** |
| FC-20 (F49) | « En 2022, l'entreprise en revendique plus de 51 millions, servis par 600 000 agents, dans sept pays. Parmi eux, la RDC » | SEQ-07, SEQ-10 | Vodafone 2022 : « 51 million customers across seven countries », « 600,000 agents across Kenya, Tanzania, Mozambique, the Democratic Republic of Congo, Lesotho, Ghana and Egypt » | — | Vodafone 2022 | 07/03/2022 | source unique (entreprise) | Chiffres non audités | **KEEP_WITH_ATTRIBUTION** |
| FC-21 (F51 → F75) | « En 2019, la part des Kényans qui ont accès à des services financiers atteint 83 %. … cette courbe ne dit pas quelle part revient à M-Pesa » | SEQ-08 | FinAccess 2019 : « Formal financial inclusion has risen to 82.9 percent, up from 26.7 percent in 2006 » | — | FinAccess 2019 | 04/2019 (terrain octobre-décembre 2018) | primaire lue | 2006 et 2019 sont comparables dans la série harmonisée du rapport de 2019, mais **l'argent mobile y est lui-même classé comme finance formelle** : la hausse inclut mécaniquement M-Pesa | **REFORMULATE** → « 82,9 % d'adultes qui utilisent un service financier formel … l'argent mobile y est lui-même compté comme de la finance formelle » |
| FC-22 (F11 → F78) | « les économistes Tavneet Suri et William Jack, depuis 2008 » | SEQ-08 | Science 2016 : « Between 2008 and 2014, we conducted five rounds of a household panel survey » | NBER w16721 (enquête de septembre 2008) | Les deux | 2016 ; 2011 | primaire lue | — | **KEEP** |
| FC-23 (F40) | « 41 % des transferts étudiés partent vers des parents, 8 % vers des enfants » | SEQ-08 | MIT News 2010 (capture) | NBER w16721, tableau 9 « Destination of remittance » : parents 44 % et enfants 10 % (1er passage), 35 % et 16 % (2e passage) | Les deux | 2010 ; 2011 | **incohérente** | Les chiffres du MIT ne figurent pas dans le working paper ; la base du tableau n'est pas explicitée | **REFORMULATE** → « bien plus souvent vers des parents que vers des enfants » (sans chiffres) |
| FC-24 (F68) | « Selon eux, cela suggère que des enfants partis travailler soutiennent leurs parents » | SEQ-08 | MIT News 2010 (« strongly suggests ») | — | Capture | 2010 | source unique | Interprétation des chercheurs rapportée par la presse universitaire | **KEEP_WITH_ATTRIBUTION** |
| FC-25 (F52, F79) | « Ils comparent les familles selon le nombre d'agents installés près de chez eux » | SEQ-08 | Science 2016 : « the number of agents within 1 km of the household » (variation 2008-2010) | Supplément | Les deux | 2016 | primaire lue | Les auteurs revendiquent une identification causale (déploiement des agents jugé exogène, test de falsification) | **KEEP** |
| FC-26 (F11 → F78) | « aurait fait sortir de l'extrême pauvreté quelque 194 000 foyers, soit 2 % des ménages du pays » | SEQ-08 | Science 2016 : résumé « lifted 194,000 households, or 2% of Kenyan households, out of poverty » ; corps du texte « at least 194,000 households out of extreme poverty » | Supplément : « a back of the envelope calculation … numbers are a lower bound » | Les deux | 2016 | primaire lue | Extrapolation nationale présentée comme borne basse ; panel avec attrition (35 % hors Nairobi, Nairobi abandonné après 2011) ; le résumé dit « poverty », le corps du texte « extreme poverty » | **REFORMULATE** → « Leur estimation, qu'ils présentent comme un minimum : … 194 000 foyers » |
| FC-27 (F78) | « Le seuil retenu : 1,25 dollar par jour et par personne » | SEQ-08 | Science 2016 : « less than $1.25 per day (a common measure of extreme poverty) » | Supplément : « USD 1.25 per person per day » | Les deux | 2016 | primaire lue | Aucune mention de parité de pouvoir d'achat (conversion apparemment au taux nominal) | **KEEP** |
| FC-28 (F12, F78) | « L'effet serait plus fort pour les foyers dirigés par des femmes » | SEQ-08 | Science 2016 : effet « more than twice that average » | — | Science | 2016 | primaire lue | — | **KEEP_WITH_ATTRIBUTION** (conditionnel) |
| FC-29 (F12, F78) | « Environ 185 000 femmes auraient quitté l'agriculture pour des activités commerciales » | SEQ-08 | Science 2016 : « induced 185,000 women to switch into business or retail as their main occupation » ; résumé « moved out of agriculture and into business » | — | Science | 2016 | primaire lue | Estimation extrapolée | **KEEP_WITH_ATTRIBUTION** |
| FC-30 | « Ce sont des estimations, obtenues par extrapolation. Pas un décompte. » | SEQ-08 | Science 2016 et supplément | — | Les deux | 2016 | primaire lue | Note : les auteurs présentent leur résultat comme **causal** (estimation causale puis extrapolation), pas comme une simple corrélation | **KEEP** |
| FC-31 (F55) | « certains transferts coûtent près de 7 % du montant envoyé » | SEQ-09 | Agence Ecofin, octobre 2025 (capture) | — | Capture seulement | 10/2025 | source unique (secondaire) | Barème tarifaire de Safaricom non lu | **KEEP_WITH_ATTRIBUTION** (« Selon Agence Ecofin ») |
| FC-32 (F55) | « Des médias kényans rapportent un projet de la Banque centrale : ramener le coût moyen d'environ 23 shillings à 10 shillings par transaction, d'ici 2028 » | SEQ-09 | Agence Ecofin (capture), qui cite « plusieurs médias locaux » | — | Capture seulement | 10/2025 | source unique (secondaire de secondaire) | Document de la Banque centrale non lu ; c'est un projet, pas une mesure adoptée | **KEEP_WITH_ATTRIBUTION** — à confirmer par la Stratégie nationale d'inclusion financière avant diffusion |
| FC-33 (F53 → F80) | « Sur l'exercice 2025, il pèse 44,2 % des revenus de Safaricom, selon la même agence » | SEQ-09 | Safaricom FY25 : « M-PESA … KES 161.1 billion, contributing 44.2% of Kenya’s service revenue » | Agence Ecofin (capture) | Safaricom (web) | 09/05/2025 | primaire lue | C'est la part des revenus de SERVICES au KENYA (environ 43,4 % des revenus de services du groupe, selon un calcul de la session de vérification) | **REFORMULATE** → « selon Safaricom, il représente 44,2 % de ses revenus de services au Kenya » |
| FC-34 (F64 → F81) | « En novembre 2020, des sénateurs kényans menacent à nouveau de séparer M-Pesa des activités télécoms de Safaricom, qu'ils jugent de plus en plus dominante » | SEQ-09 | The Star, 17/11/2020 : « Safaricom should be declared dominant and split into two firms, senators have said. » (comité TIC du Sénat ; Petronilla Were, Irungu Kang'ata, Enock Wambua) | Agence Ecofin (capture : « menace à nouveau de séparer les activités télécoms et de mobile money ») | The Star (lu) ; Ecofin (capture) | 17/11/2020 | **corroborée** | Ce n'est pas une menace formelle mais une demande, assortie d'une proposition de scission ; l'article de The Star est publié en rubrique Opinion/Columnists | **REFORMULATE** → « réclament à nouveau que Safaricom soit déclarée dominante, et que ses activités télécoms soient séparées de M-Pesa » |
| FC-35 (F65) | « Sur l'exercice clos en mars 2022, les paris en ligne étaient devenus la deuxième source de revenus de M-Pesa » | SEQ-09 | Agence Ecofin, mai 2022 (capture) | — | Capture seulement | 05/2022 | source unique (secondaire) | Affirmation forte non vérifiée dans les comptes de Safaricom ; elle paraît peu compatible avec la répartition habituelle des revenus de M-PESA (non vérifié) | **PENDING_VERIFICATION** — retirée du script v2.1 |
| FC-36 (F58) | « Le crédit sur mobile … a démocratisé l'emprunt, mais il soulève la question de la protection des plus pauvres » | SEQ-09 | Agence Ecofin, 2019 (capture) | — | Capture seulement | 11/2019 | source unique | — | **KEEP_WITH_ATTRIBUTION** (« selon Agence Ecofin » ajouté) |
| FC-37 (F67 → F82) | « En 2019, FSD Kenya comptait déjà 49 plateformes de prêt, dans un secteur très peu réglementé » | SEQ-09 | FSD Kenya, « Digital credit audit report » : « approximately 110 mobile apps » en septembre 2018 ; « from 14 in 2017 to 49 in 2018 » (applications publiées) | Agence Ecofin (capture) | FSD Kenya (lu) | 09/2019 | primaire lue | « 49 » = applications publiées en 2018, pas un total ; « très peu réglementé » est la formulation d'Ecofin, non vérifiée dans le rapport | **REFORMULATE** → « En septembre 2018, FSD Kenya recensait déjà environ 110 applications de prêt sur téléphone » |
| FC-38 (F59) | « Selon son auteur, l'argent mobile ne s'attaque pas aux causes systémiques de la pauvreté » | SEQ-10 | Revue de la régulation (OpenEdition), présentation de thèse : « Les monnaies locales visent les causes systémiques de la pauvreté, ce que les systèmes de monnaie mobile ne font pas. » | — | Capture de la phase 1 seulement (relecture bloquée par « Anubis ») | n.d. | primaire (capture) | Auteur non nommé (non relevé) | **KEEP_WITH_ATTRIBUTION** — nom de l'auteur à relever |
| FC-39 | « Le téléphone, le SMS, les petites boutiques : tout existait déjà » | SEQ-10 | Vodafone 2017 ; Hughes & Lonie (agents) | — | Les deux | — | interprétation éditoriale | Conclusion éditoriale de LUKOJI | **KEEP** (à assumer comme lecture éditoriale) |
| FC-40 | « un service devenu aussi central appelle des règles, des contre-pouvoirs et des prix surveillés » | SEQ-10 | — | — | — | — | opinion éditoriale | Ce n'est pas un fait : c'est la position du film | **KEEP** (décision humaine) |

## Bilan

| Décision | Affirmations |
|---|---|
| **KEEP** | FC-01, 02, 03, 04, 07, 08, 16, 22, 25, 27, 30, 39, 40 |
| **KEEP_WITH_ATTRIBUTION** | FC-06, 09, 11, 12, 13, 14, 15, 17, 19, 20, 24, 28, 29, 31, 32, 36, 38 |
| **REFORMULATE** | FC-05, 10, 21, 23, 26, 33, 34, 37 |
| **REMOVE** | FC-18 (communiqué et citation de la Banque centrale, janvier 2009) |
| **PENDING_VERIFICATION** | FC-35 (paris en ligne), retirée de la voix off |

- **Vérifiés dans une source primaire lue** :
  - Suri & Jack : FC-22, 25, 26, 27, 28, 29, 30 ;
  - FinAccess : FC-05, 21 ;
  - Safaricom : FC-33 ;
  - FSD Kenya : FC-37 ;
  - Vodafone : FC-12, 20 (déclarations et chiffres de l'entreprise).
- **Corroborés par au moins deux organisations indépendantes** : FC-01, FC-02 (hook H9), FC-07, FC-16, FC-34.
- **Toujours à source unique ou même sphère, conservés avec attribution** : le récit des origines (Vodafone et l'équipe projet), les faits Agence Ecofin (FC-15, 17, 31, 32, 36) et la présentation de thèse.

## Le hook H9 est conservé

- **Voyages de plusieurs jours** : corroborés par Vodafone (2017) et par CGAP (2009 ; plus d'une semaine pour des femmes rurales).
- **Argent confié aux bus** : la pratique est documentée par l'enquête nationale FinAccess 2006 (envois par une compagnie de bus ou de matatu : 21,6 % des receveurs et 29,4 % des envoyeurs) et par Hughes & Lonie (colis déguisés envoyés par bus). Le mot « chauffeur » vient de Vodafone seule.
- **Contexte** : Kenya, période antérieure au lancement de 2007 (FinAccess 2006 : douze mois précédant l'enquête d'août-septembre 2006).
- **Image** : la photo du matatu de 2025 reste une image d'illustration et ne prouve pas la pratique. La preuve est la source, qui doit apparaître à l'écran.

**Variante possible**, si l'éditeur préfère la formulation la plus étroitement sourcée : « Ou confier ses billets à une compagnie de bus, et attendre. » Elle n'est pas appliquée.

## Corrections apportées

**Script v2.1** (moteur v15 ; ré-attaché en v16 sans changement de contenu) : uniquement les corrections factuelles listées ci-dessus, plus des attributions ajoutées en SEQ-06 et SEQ-09. Durée : 936 mots, environ 6,3 minutes.

**Hooks, structure, direction** : ré-attachés au dossier factuel v4, **contenu inchangé** (hooks v4, structure v4, visual v3).

**Storyboard v7 : non modifié**, comme demandé. Il est désormais **obsolète** : le QC du moteur relève 6 bloquants, tous liés à ce décalage. Scènes à reprendre après validation du script :

| Scène | Correction à prévoir |
|---|---|
| SC-04, SC-05 | Libellés « accès FORMEL », 26,7 %, source FinAccess |
| SC-10 | Carte : Nairobi **et** Thika |
| SC-18 à SC-22 | Nouveau découpage de SEQ-06 ; SC-21 et SC-22 (communiqué de 2009) à supprimer ; R18 n'est plus nécessaire |
| SC-26, SC-27 | 82,9 %, libellé « formel », mention de l'argent mobile classé formel |
| SC-28 | Retirer les barres 41 % / 8 % |
| SC-31 | Ajouter « estimation minimale » |
| SC-36 | Libellé « 44,2 % des revenus de services au Kenya », source Safaricom |
| SC-37 | Formulation des sénateurs, sources The Star et Agence Ecofin |
| SC-38 | Supprimer l'illustration des paris en ligne |
| SC-39, SC-40 | Source du crédit ; « environ 110 applications (septembre 2018) », source FSD Kenya |

## Ce que ce fact-check ne permet pas de dire

- Le récit du détournement repose sur Vodafone et sur l'équipe projet ; aucune source indépendante ne le corrobore.
- Les conclusions causales de Suri & Jack sont celles des auteurs. Elles ont été discutées dans la littérature, mais ces discussions n'ont pas été examinées ici.
- Les faits Agence Ecofin n'ont pas pu être relus, faute d'accès au site.
