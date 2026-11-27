# Rapport de validation — Phase 0 : fondations et kit de marque

Date d'exécution : 27 novembre 2026 · Environnement : Ubuntu 24.04, 4 processeurs, 15 Go de RAM, sans GPU,
FFmpeg 6.1.1, Python 3.13, Node 22 avec Chromium (Playwright).

## 1. Résultat global

| Livrable | État | Preuve |
|---|---|---|
| Kit de marque fonctionnel | ✅ | 15 ressources sous empreinte SHA-256, `brand-verify` OK |
| Module de filigrane | ✅ | `src/lukoji_engine/watermark.py` · 2 rendus réels conformes |
| Module de signature de fin | ✅ | `signature.py` + `scripts/render_signature.mjs` · 4 préréglages |
| Configurations par plateforme | ✅ | `config/platforms.toml` · 6 profils |
| Base de données initiale | ✅ | SQLite, migrations, cycle de vie à 12 statuts |
| Tests automatisés | ✅ | **27/27 réussis** (`python3 -m pytest -q`, 2 min 31 s) |
| Rendu vidéo réellement testé | ✅ | 1 vertical + 1 horizontal (`docs/validation/renders/`) |
| Rapport de validation | ✅ | ce document |
| Documentation | ✅ | README, MARQUE, ZONES_SECURITE, TRANSFERT |
| Commandes de reproduction | ✅ | `./scripts/run_phase0.sh` (exécuté de bout en bout : 4 min 02 s) |

## 2. Inspection et sécurisation

- **Dépôt** : `lukoji-media-engine` n'existe pas encore sur GitHub, ou n'est pas accessible à la session (tentative d'ajout refusée : « not found »). Le travail est donc préparé dans `/home/user/lukoji-media-engine`, en **dépôt Git local** (branche `main`). Transfert : voir `docs/TRANSFERT.md`.
- **Autres projets** : `lukoji-blog` et `Motion-design-` n'ont été **que lus**. `git status` est vide et le dernier commit est inchangé dans les deux dépôts (`f0e68cc`, `489c51a`).
- **Aucune dépense, aucun secret** : aucun service payant utilisé, aucune clé lue ni écrite. `.env` est exclu de Git et `.env.example` ne contient aucune valeur.
- **Installations** : aucun paquet système ou Python installé. Seules les deux polices OFL ont été téléchargées depuis le dépôt officiel `google/fonts`, après avoir vérifié leur absence.

### Identification des ressources de marque

- **Symbole SVG officiel** : `lukoji-blog/symbole.svg` (viewBox 320×670, trait 16, extrémités rondes), copié octet pour octet (même SHA-256 `38496199…`). Validé contre le PNG officiel du symbole : **IoU 0,991**, ratio 0,4288 contre 0,4290, même épaisseur relative de trait.
- **Horizontal** : `horizontal_{noir,blanc}_transparent_2800x800.png`. **Vertical** : `vertical_slogan_{noir,blanc}_transparent_2400x1600.png`. **Carré** : `avatar_*_1000.png`.
- Les 14 fichiers fournis = 12 visuels distincts (2 doublons exacts, documentés).
- **Vidéos de test** : réel `lukoji-blog/pubs/reseaux/2026-11-20-reel-ta-premiere-pub.mp4` (1080×1920, 30 i/s, 24,6 s) et `Motion-design-/time-capital/renders/le-temps-est-ton-capital.mp4` (1920×1080, 30 i/s, 20,0 s). Aucun test synthétique n'a été nécessaire pour les rendus réels.

## 3. Tests réels

### Test vertical 1080×1920 — `docs/validation/renders/test_vertical_1080x1920.mp4`

- Source coupée à 19,35 s, juste avant sa propre signature d'origine, pour tester la nôtre.
- Profil `vertical_universal` (TikTok + Reels IG/FB + Shorts), signature `court`.
- **Placement** : haut-gauche et haut-droite **rejetés**, car ils masqueraient le titre « CE QU'ON FAIT POUR TOI » pendant [3,5–5,0], [5,25–8,25] et [9,25–11,75] s. Position retenue : **bas-gauche [65, 1361, 218, 59]**.
- **Couleur adaptative** : blanc (0–3 s, fond 0,07) → noir (3–17,75 s, fond 0,96) → blanc (17,75–19,35 s).
- **QC : CONFORME, 41/41 contrôles.**

| Contrôle | Mesure |
|---|---|
| Format | 1080×1920, ratio 0,5625, H.264 High, yuv420p, 30/1 i/s, AAC 48 kHz stéréo, faststart |
| Durée | 20,700 s (19,35 + 1,6 − 0,25 de fondu), 621 images |
| Filigrane présent et conforme (corrélation avec la composition attendue) | 0,9997 à 0,9999 sur 9 instants |
| Position exacte (décalage du pic de corrélation) | (0, 0) aux 9 instants |
| Visibilité (écart de luminance logo/fond) | 0,785 à 0,793 |
| Non-masquage du contenu | densité max 0,006 (seuil 0,012), aucune zone masquée |
| Ratio du logo vs source officielle | écart 0,05 % |
| Contenu hors logo non altéré | dérive de luminance 0,0018 |
| Signature présente, sans filigrane, dans la zone sûre | écart 1,0/255 avec l'image de référence · boîte [154, 576, 773, 768] |
| Audio (information) | −14,3 LUFS, crête −4,0 dBTP |

### Test horizontal 1920×1080 — `docs/validation/renders/test_horizontal_1920x1080.mp4`

- Profil `youtube_16x9`, type `documentaire`, donc signature `documentaire` (3,5 s).
- **Placement** : haut-droite [1584, 54, 240, 65]. Le minuteur « 23:44:27 » de la source est plus bas, à y ≥ 160, et n'est pas touché.
- **QC : CONFORME, 36/36 contrôles.** Corrélation 0,9998–0,9999, décalage (0, 0), visibilité 0,80, densité max 0,0066, ratio du logo à 0,12 % d'écart, durée 23,267 s, −16,3 LUFS.

### Pièces visuelles (`docs/validation/`)

- `planche_test_vertical.png`, `planche_test_horizontal.png` : images clés, zones sûres des plateformes (contours colorés) et boîte du filigrane (orange).
- `zoom_filigrane_x3.png` : le logo agrandi ×3. Il est net, sans bavure, avec l'ombre douce sur la version blanche ; la version noire est propre sur fond clair.
- `signature_court_sequence.png`, `signature_*_image_finale.png` : la signature ; l'image finale correspond au logo vertical officiel.
- `planche_test_vertical_v1_defaut.png` : **premier rendu défectueux, conservé comme preuve** (voir §5).

## 4. Tests automatisés (27)

```
python3 -m pytest -q   →   27 passed in 151.08s
```

| Fichier | Couverture |
|---|---|
| `test_config_geometry.py` (9) | palette officielle, surcharges d'environnement, géométrie, recadrages 4:5/3:4, zones sûres distinctes par plateforme, intersection du profil maître, zone réservée YouTube |
| `test_brand_assets.py` (7) | manifeste intègre, **détection d'un original modifié**, ratio du logo < 0,5 %, SVG ≡ PNG officiel (IoU ≥ 0,97), découpes de signature identiques pixel à pixel |
| `test_db.py` (5) | migrations idempotentes, cycle de vie complet et historique, **publication impossible sans validation**, type « client » refusé (CLIENT STUDIO hors périmètre), versions des ressources |
| `test_e2e_watermark.py` (6) | rendu synthétique conforme ; évitement d'un bloc de texte ; couleur blanc→noir ; enregistrement en base ; **QC refuse une vidéo sans filigrane** ; **QC refuse un logo étiré de 12 %** ; pas de signature sous 12 s |

## 5. Défaut trouvé et corrigé pendant la phase

La première version notait chaque position par la **moyenne** de la densité de contours sur toute la durée.
Un titre présent seulement de 3,5 à 11,75 s était dilué dans cette moyenne, et le filigrane l'a recouvert
(rendu n° 1, visible sur `planche_test_vertical_v1_defaut.png`). Le premier QC ne mesurait pas ce cas et l'avait déclaré conforme.

Corrections :
1. Le placement exige désormais qu'une position soit dégagée **à chaque instant** (pas de 0,25 s, seuil calibré sur ce rendu).
2. Les quatre coins de la zone sûre sont candidats.
3. Nouveau contrôle **bloquant** `filigrane_ne_masque_pas_le_contenu`, indépendant du placement. Relancé sur le rendu défectueux, il le **refuse** en listant les trois intervalles masqués. Ce rendu est conservé en base avec le statut `echec`.

Autre correction : à petite taille, l'arrondi seul écartait le ratio du logo de 0,81 %. Le moteur choisit désormais le couple
largeur × hauteur entier le plus fidèle (± 3 px) : l'écart tombe à 0,05–0,12 %.

## 6. Base de données (état après exécution)

`var/lukoji.sqlite3` (non versionné, recréé par `run_phase0.sh`) : 24 ressources (15 originaux + 9 dérivés versionnés), 3 contenus de test, 5 rendus (1 `echec`, 4 `conforme`), 232 résultats de contrôle.
Tables : `assets`, `contents`, `content_events`, `renders`, `qc_results`, `schema_migrations`.

## 7. Limitations connues

1. **Zones de sécurité non vérifiées sur appareil.** Ce sont des valeurs prudentes. Il faudra une capture réelle par plateforme pour les confirmer.
2. **Détection de contenu sous le filigrane = heuristique de contours.** Elle détecte bien le texte et les graphiques, mais un **visage peu contrasté** ou un grand aplat important ne sera pas détecté. La parade actuelle consiste à déclarer la zone (`--avoid`). Une vraie détection de visages (OpenCV, gratuit) est proposée pour la phase 3.
3. **Pas de détection d'un logo déjà présent dans la source.** Le réel de test contient son propre petit logo en haut à gauche, dans la bande masquée par TikTok et Reels. Les contenus produits par le moteur n'en auront pas.
4. **Audio** : mesuré seulement (LUFS, crête). La normalisation et le mixage relèvent de la phase 3.
5. **Signature** : rendue image par image dans Chromium (≈ 3 à 8 s par préréglage, mise en cache). Elle dépend de Playwright, qui est pré-installé ici et qu'il faudra installer ailleurs.
6. **Rendus de test** : les deux MP4 (8 et 16 Mo) sont versionnés pour la revue. À l'avenir, les rendus iront vers un stockage externe (Drive ou objet), pas dans Git.
7. Les sources de test viennent de dépôts voisins. Elles servent uniquement aux tests internes, et `run_phase0.sh` les ignore proprement si elles sont absentes.

## 8. Prochaine étape recommandée

1. **Validation humaine** des deux rendus : taille du filigrane (220 px ≈ 20 % de la largeur), opacité 0,88, préférence de position, durée de signature 1,6 s.
2. **Créer le dépôt GitHub** `lukoji-media-engine` (vide, privé) et pousser ce travail (`docs/TRANSFERT.md`).
3. Faire **une capture d'écran par plateforme** avec un rendu publié en privé, pour passer les zones à `verifie_sur_appareil = true`.
4. Ensuite seulement, **phase 1** (recherche et propositions de sujets), après votre accord.
