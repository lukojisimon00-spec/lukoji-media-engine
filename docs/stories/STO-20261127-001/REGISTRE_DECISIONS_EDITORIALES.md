# Registre des décisions éditoriales — pilote M-Pesa

`STO-20261127-001` · titre de travail : **Quand les clients ont changé le produit** · mis à jour en phase 2.4 (27/11/2026)

Statuts :
- **APPLIQUÉE** : la décision est intégrée dans les fichiers ou dans la base ;
- **NON APPLIQUÉE** : volontairement laissée de côté, avec le motif ;
- **EN ATTENTE** : la décision appartient à l'éditeur.

**Aucune de ces décisions ne vaut validation** du script, de la structure ou du storyboard.

| # | Décision | Origine | Statut | Motif | Référence |
|---|---|---|---|---|---|
| D01 | Titre de travail : « Quand les clients ont changé le produit » | Éditeur, phase 2.4 | **APPLIQUÉE** | Mis à jour dans le script v2.2, dans la base (`story_projects.title`, changement journalisé dans `story_events`) et dans les exports v2.2 | `research/stories/mpesa/v2_2/script_v2_2.json` ; `v2_2/script.md` |
| D02 | Ne pas réécrire les exports historiques (v1, v2, v2.1) qui portent l'ancien titre | Phase 2.4 | **NON APPLIQUÉE** (volontaire) | Ce sont des versions conservées. Les réécrire effacerait l'historique | `docs/stories/STO-20261127-001/`, `…/v2/`, `…/v2_1/` |
| D03 | Titre du **sujet** de la phase 1 (`SUJ-20261127-002`) | Phase 2.4 | **NON APPLIQUÉE** | C'est la proposition éditoriale d'origine, pas le projet narratif. Le modifier réécrirait l'historique de la phase 1 | Table `subjects` |
| D04 | Hook H9, version prudente (« confier son argent à une compagnie de bus ») | Éditeur, phase 2.4 | **APPLIQUÉE** | H9 dans les hooks v5 et dans l'ouverture du script v2.2. Le premier moyen d'envoi (ami ou proche) n'est pas mentionné, mais la pratique n'est ni généralisée ni présentée comme majoritaire | `research/stories/mpesa/v2_2/hooks_v2_2.json` ; FC-02 dans `FACTCHECK_FINAL_V2.md` |
| D05 | Récit des origines conservé, explicitement attribué à l'équipe projet et à Vodafone | Éditeur, phase 2.4 | **APPLIQUÉE** | SEQ-03 : « Ce qui suit, on le connaît surtout par ceux qui l'ont mené » (article de 2007 de deux responsables du projet, texte de Michael Joseph publié par Vodafone en 2017) ; SEQ-04 : « D'après Michael Joseph » ; SEQ-10 : « Si l'on suit le récit de ses concepteurs » | Script v2.2 |
| D06 | Paris en ligne hors du script | Éditeur | **APPLIQUÉE** | Absents de la voix off, de la structure et des faits cités ; contrôle automatique ajouté | `v2_2/qc_consolidation.md` ; `tests/test_pilote_mpesa_v2.py` |
| D07 | Faits Agence Ecofin limités à ceux retenus dans le dossier factuel v4, avec attribution | Éditeur | **APPLIQUÉE** | F45, F46 et F55 (« Selon Agence Ecofin ») ; F58 (« selon Agence Ecofin »). Aucune nouvelle recherche | Script v2.2 ; FC-15, 17, 31, 32, 36 |
| D08 | SEQ-06 : reconstruire la tension après le retrait du communiqué de 2009 | Éditeur | **APPLIQUÉE** | Question posée (« est-ce encore du téléphone, ou déjà de la banque ? »), objection des banques, arbitrage du régulateur sous conditions, puis question laissée ouverte et reprise en SEQ-09. Aucun fait nouveau | Script v2.2, structure v6 (E6) |
| D09 | SEQ-08 : réduire la densité | Éditeur | **APPLIQUÉE** | De 202 à 146 mots (décompte du moteur). Retirés de la voix off : la répartition parents / enfants (F40, F68) et les 185 000 femmes. Conservés : le biais de définition de FinAccess, la méthode, « au moins 194 000 foyers », 2 %, le seuil de 1,25 $, l'effet plus fort pour les foyers dirigés par des femmes, et « estimation… pas un décompte » | Script v2.2 ; FC-21 à FC-30 |
| D10 | SEQ-09 : progression plutôt que catalogue | Éditeur | **APPLIQUÉE** | Ordre : coût pour les usagers → réponse annoncée du régulateur → poids pour l'opérateur → retour de la question de SEQ-06 (sénateurs) → nouveaux usages à risque | Script v2.2, structure v6 (E9) |
| D11 | SEQ-10 : lien avec la RDC sans comparaison inventée | Éditeur | **APPLIQUÉE** | Présence de M-Pesa en RDC attribuée à Vodafone ; « Ce film ne dit pas ce qu'il y a changé : l'histoire kényane ne se transpose pas telle quelle » ; question ouverte | Script v2.2 ; FC-20 |
| D12 | Thèse : citée avec son cadre (comparaison avec les monnaies locales) | Revue éditoriale | **APPLIQUÉE** | « compare les monnaies locales et l'argent mobile. Selon son auteur, seules les premières visent les causes systémiques de la pauvreté » : reprend la phrase de la source | Script v2.2 ; FC-38 |
| D13 | Structure : retirer les références aux faits retirés (F66, F51, F11, F53, F64, F65, F67) | Revue éditoriale | **APPLIQUÉE** | La structure v6 est reconstruite à partir du script ; aucun fait retiré n'est cité (contrôle automatique) | `research/stories/mpesa/v2_2/structure_v2_2.json` |
| D14 | Transition de SEQ-06 renvoyant au communiqué de 2009 | Revue éditoriale | **APPLIQUÉE** | Remplacée par « La question reste ouverte. En attendant, le service grandit. » | Script v2.2 |
| D15 | Durée dans l'en-tête du script | Revue éditoriale | **APPLIQUÉE** (export v2.2) | 984 mots (décompte du moteur), 399,0 s, environ 6,7 min, pauses comprises. L'export du **moteur** calcule la durée à partir des scènes du storyboard : avec le storyboard v7 obsolète, son en-tête resterait faux. C'est un comportement du moteur, signalé et non modifié ; d'où un export propre au pilote | `v2_2/script.md` ; `research/stories/mpesa/v2_2/consolidation_v2_2.py` |
| D16 | Rattachement des hooks, de la structure, du script et de la direction au dossier factuel v4 | Phase 2.4 | **APPLIQUÉE** | Hooks v5, structure v6, script v21, direction v5 (contenu de la direction inchangé) | `v2_2/qc_consolidation.md` |
| D17 | Préciser « dans sept pays » avant « 51 millions » (SEQ-07) | Revue éditoriale (§2) | **EN ATTENTE** | Hors du périmètre de révision fixé pour la phase 2.4 (SEQ-06, 08, 09, 10). La formulation actuelle (« …plus de 51 millions, servis par 600 000 agents, dans sept pays ») reste ambiguë à l'oral | Script v2.2, SEQ-07 |
| D18 | Témoignages d'usagers | Revue éditoriale | **EN ATTENTE** | Aucun témoignage n'est inventé ; il faut un tournage ou des archives sonores identifiées | — |
| D19 | Source indépendante sur les origines | Revue éditoriale | **EN ATTENTE** | Le récit reste celui de l'équipe projet et de Vodafone, désormais attribué comme tel | FC-04, FC-09 à FC-14 |
| D20 | Confirmer le projet de baisse des frais (23 → 10 KES) dans un document de la Banque centrale | Fact-check | **EN ATTENTE** | Avant diffusion | FC-32 |
| D21 | Relire Agence Ecofin et la présentation de thèse (auteur) | Fact-check | **EN ATTENTE** | Sites protégés ; aucune relecture possible depuis l'agent | FC-15, 17, 31, 36, 38 |
| D22 | Reconstruire le storyboard | Phase 2.4 | **NON APPLIQUÉE** (interdit en phase 2.4) | À faire après validation humaine du script et de la structure ; les scènes à reprendre sont listées dans le fact-check, plus celles touchées par la v2.2 | `FACTCHECK_FINAL_V2.md` ; `RAPPORT_PHASE_2_4.md` |
| D23 | Validation de la structure v6 et du script v2.2 | — | **EN ATTENTE** | Décision exclusivement humaine (`story approve`, par l'éditeur) | — |
