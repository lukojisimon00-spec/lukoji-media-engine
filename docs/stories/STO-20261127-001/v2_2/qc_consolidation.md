# Contrôle de cohérence — consolidation v2.2

**23 contrôles ok ou alertes · 0 bloquant(s).** Ces contrôles sont techniques et documentaires : ils ne valent **pas** validation éditoriale.

| Catégorie | Contrôle | Résultat | Détail |
|---|---|---|---|
| alignement | chaque séquence a son étape, avec les mêmes faits | ok |  |
| alignement | transitions identiques dans le script et la structure | ok |  |
| versions | hooks, structure et script rattachés au dossier factuel courant | ok | dossier v4 · hooks {'research': 4} · structure {'research': 4, 'hooks': 5} · script {'research': 4, 'hooks': 5, 'structure': 6} |
| versions | script rattaché aux hooks et à la structure courants | ok | script basé sur {'research': 4, 'hooks': 5, 'structure': 6} |
| versions | versions antérieures conservées : script [9, 13, 16] | ok |  |
| versions | versions antérieures conservées : structure [2, 3, 4] | ok |  |
| versions | versions antérieures conservées : research [2, 3, 4] | ok |  |
| versions | versions antérieures conservées : hooks [2, 3, 4] | ok |  |
| versions | versions antérieures conservées : storyboard [2, 7] | ok |  |
| factuel | faits connus, utilisables, attribués ; chaque nombre présent dans un fait ou une preuve (contrôle du moteur) | ok |  |
| factuel | aucun fait retiré cité (script et structure) | ok |  |
| factuel | absent de la voix off : communiqué de la Banque centrale de 2009 | ok |  |
| factuel | absent de la voix off : paris en ligne | ok |  |
| factuel | absent de la voix off : « chauffeur de bus » (version non prudente du hook) | ok |  |
| factuel | absent de la voix off : chiffres retirés | ok |  |
| titre | titre du projet en base | ok | Quand les clients ont changé le produit |
| titre | titre du script | ok | Quand les clients ont changé le produit |
| hook | H9 prudent choisi et identique à l'ouverture du script | ok |  |
| duree | durée calculée sur les mots (150 mots/min + pauses) dans la cible 6-8 min | ok | 984 mots (décompte du moteur) · 399.0 s · 6.7 min |
| base | intégrité de la base | ok | ok |
| base | aucune validation enregistrée | ok | 0 |
| base | statut inchangé : structure_draft | ok | structure_draft |
| storyboard | storyboard non reconstruit (v7, obsolète par décision) | ok | à reprendre après validation du script et de la structure |
