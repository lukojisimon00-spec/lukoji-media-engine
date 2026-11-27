# Atelier 3.1 — Collecte documentaire (pilote M-Pesa, STO-20261127-001)

Collecte du 27/11/2026 (UTC). Le détail par source (URL finale, code HTTP, horodatage, taille, SHA-256, MIME, pages, auteurs, date, mentions de licence, captures avec page/zone, citation exacte, scène et dimensions) est dans `manifeste_collecte.json`.

## Méthode
- Les originaux ont été téléchargés avec `curl -L` dans un dossier temporaire hors dépôt (`/tmp/collecte`). Ils ont été hachés en SHA-256 et **ne sont pas versés** au dépôt : aucun PDF, aucun texte intégral.
- PDF : `pdfinfo` et `pdftotext` servent aux métadonnées et au repérage des passages. `pdftotext -bbox-layout` donne la position du texte. Les pages sont rendues à 200 dpi (`pdftoppm -r 200`), puis recadrées sur le passage avec une marge de 40 px (Pillow). Les couvertures et pages de titre sont des vignettes à 72 dpi.
- Web : les captures sont faites avec Playwright/Chromium (fenêtre 1440 px, deviceScaleFactor 2), en découpant l'élément du DOM qui contient le passage. L'empreinte de chaque page est celle du HTML brut renvoyé à curl. Les pages sont dynamiques, donc cette empreinte peut changer.
- Photos (R04, R06, R11) : seules les métadonnées ont été relevées, via l'API `en.wikipedia.org` (`prop=imageinfo`, `extmetadata`). Aucune photo n'a été téléchargée.
- Aucune image n'a été générée. Aucune protection n'a été contournée.

## Échecs et réserves
- **R14 (OpenEdition)** : ÉCHEC. La page anti-robots « Anubis » refuse l'accès. Une seule tentative a été faite, sans insister.
- **R29** : la page éditeur MIT n'a pas pu être consultée. `doi.org` est bloqué par le proxy réseau (403) et `direct.mit.edu` renvoie 403. Le DOI `10.1162/itgg.2007.2.1-2.63` vient de RePEc et n'a pas été vérifié chez l'éditeur. Le PDF utilisé est une copie hébergée par l'Université de Zurich.
- **R31 (Safaricom)** : l'URL a été retrouvée par recherche web. Le navigateur headless reçoit un 403 (CloudFront), alors qu'une requête curl simple obtient 200. Les captures sont donc un rendu local du HTML obtenu par curl, sans JavaScript, et la mise en forme peut différer de la page publique. Le PDF du communiqué renvoie 403 ; je n'ai pas insisté.
- **R11 (photo Kinshasa)** : voir le statut dans le manifeste. L'API a renvoyé 429 (limitation de débit) à plusieurs reprises.
- **Redirections** : R24 mène à `/news/newsroom/people/…`. R30 mène à la rubrique `opinion/columnists`. Pour R30, la date affichée est le 17/11/2020, alors que l'URL porte 2020-11-18.
- Pour les PDF, les numéros de page sont donnés en index PDF. Pour R29, la pagination de la revue (p. 63-81) est indiquée en plus.
