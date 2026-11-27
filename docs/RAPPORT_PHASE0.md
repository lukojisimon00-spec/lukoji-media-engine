# Rapport de validation finale — Phase 0 : fondations et kit de marque

**Statut : VALIDÉE.** Les tests complets ont été exécutés (43/43, dont les 8 tests vidéo longs), deux rendus
réels sont conformes et ont été examinés visuellement, et la reproductibilité est prouvée à partir d'un clone neuf du dépôt GitHub.

Date : 27 novembre 2026. Environnement : Ubuntu 24.04, 4 processeurs, 15 Go de RAM, sans GPU, FFmpeg 6.1.1,
Python 3.13.18, Node 22.23 et Chromium (Playwright).

---

## 1. Dépôt Git et synchronisation

| Vérification | Résultat |
|---|---|
| Dépôt | `lukojisimon00-spec/lukoji-media-engine` |
| Branche de travail | `ccr-3b5e8ca0-t16yir`, qui suit `origin/ccr-3b5e8ca0-t16yir` |
| État avant validation | arbre propre, local = GitHub (`68182c4`) |
| Commits | `1eb7eab` fondations · `68182c4` comptes sociaux · `a2f5e96` correctifs de validation · commit final de clôture (ce rapport) |
| Projets externes | `lukoji-blog` et `Motion-design-` : `git status` vide, dernier commit inchangé (`f0e68cc`, `489c51a`). **Aucune modification.** |

## 2. Tests automatisés — exécution complète

`python3 -m pytest -v` → **43 passed in 171.50 s**. La sortie intégrale est dans `docs/validation/pytest_final.txt`.

| Fichier | Tests | Résultat |
|---|---|---|
| `test_brand_assets.py` | manifeste intègre · originaux présents et SVG officiel · **détection d'un original modifié** · ratio minimal · ratio du logo officiel · SVG ≡ PNG officiel (IoU ≥ 0,97) · découpes de signature exactes au pixel · **image finale de la signature ≡ logo vertical officiel** · clé de cache indépendante de l'emplacement | 9/9 ✅ |
| `test_config_geometry.py` | palette officielle · surcharge par variable d'environnement · rectangles · recadrages 4:5 et 3:4 · zones sûres positives · **zones distinctes par plateforme** · profil maître = intersection · ancrages dans la zone sûre · zone réservée YouTube | 9/9 ✅ |
| `test_db.py` | migrations idempotentes · cycle de vie et historique · **publication impossible sans validation** · type « client » refusé · versions des ressources | 5/5 ✅ |
| `test_e2e_watermark.py` (vidéo) | rendu conforme · évitement du texte et **bascule à 6,000 s exactement** · enregistrement en base · **QC refuse une vidéo sans filigrane** · **QC refuse un logo étiré de 12 %** · pas de signature sous 12 s · **logo visible sur chaque image** · **empreinte visible dans la zone sûre de chaque plateforme** | 8/8 ✅ |
| `test_social.py` | liens officiels exacts · configuration valide et sans secret · publication désactivée · routage · lien Facebook de partage · 7 configurations invalides refusées | 12/12 ✅ |

## 3. Reproductibilité

| Exécution | Résultat |
|---|---|
| Clone **neuf** depuis GitHub (`a2f5e96`), sans `var/`, base ni cache → `./scripts/run_phase0.sh` | code retour **0**, 4 min 17 s, 2 rendus conformes, 41/41 tests (avant l'ajout des 2 tests de signature) |
| Dépôt principal, code définitif → `./scripts/run_phase0.sh` | code retour **0**, 4 min 12 s, 2 rendus conformes, **43/43 tests** |

Le script enchaîne : contrôle des outils → base → kit de marque → vérification d'intégrité → profils → comptes sociaux → rendu vertical et QC → rendu horizontal et QC → planches → tests.

## 4. Rendus produits et contrôle qualité

### 4.1 Vertical 1080×1920 — `docs/validation/renders/test_vertical_1080x1920.mp4`

Source : réel LUKOJI du 20 novembre 2026, en lecture seule, coupé à 19,35 s juste avant sa propre signature. Profil `vertical_universal` (TikTok, Reels Instagram et Facebook, Shorts). Signature `court`.

**QC : CONFORME, 43 contrôles sur 43.**

| Contrôle | Mesure exacte |
|---|---|
| Format | 1080×1920, H.264 High, yuv420p, 30,000 i/s (réel et moyen), AAC 48 kHz stéréo, faststart |
| Durée / images | 20,700 s / 621 images (19,35 + 1,6 − 0,25 de fondu) |
| Placement | bas-gauche, logo [68, 1358, 218, 59], empreinte visible avec ombre [65, 1357, 226, 63] |
| Coins rejetés | haut-gauche et haut-droite : « masquerait du contenu pendant [3,5–5,0], [5,25–8,25], [9,25–11,75] s » |
| Couleur | blanc 0–2,900 s → noir 2,900–17,667 s → blanc 17,667–19,35 s (bascules sur l'image exacte de la coupe) |
| Présence et conformité du logo (corrélation avec la composition attendue) | 0,9998 à 0,9999 sur 9 instants |
| Position exacte | décalage (0, 0) aux 9 instants |
| Visibilité **image par image** | 581 images contrôlées, **0 invisible** |
| Non-masquage | densité de contours max 0,0062 (seuil 0,012), aucune zone masquée |
| Zones sûres, au pixel (marges restantes g/h/d/b) | TikTok 5/1197/649/20 · Reels IG 0/1107/659/0 · Reels FB 5/1072/659/0 · Shorts 5/1177/639/50 |
| Modifications hors empreinte | 0, 0, 2, 45 et 17 pixels isolés (bruit d'encodage ; limite 103) |
| Contenu non altéré | dérive de luminance 0,0019 |
| Ratio du logo | 218×59, écart 0,05 % avec la source officielle |
| Signature | présente (écart 1,006/255 avec la référence), sans filigrane, contenu [154, 576, 773, 768] dans la zone sûre |
| Audio (information) | −14,3 LUFS, crête −4,0 dBTP |

### 4.2 Horizontal 1920×1080 — `docs/validation/renders/test_horizontal_1920x1080.mp4`

Source : `Motion-design-/time-capital/renders/le-temps-est-ton-capital.mp4`, en lecture seule. Profil `youtube_16x9`, type documentaire, signature `documentaire` (3,5 s).

**QC : CONFORME, 38 contrôles sur 38.**

| Contrôle | Mesure exacte |
|---|---|
| Format | 1920×1080, H.264 High, yuv420p, 30,000 i/s, AAC 48 kHz stéréo, faststart |
| Durée / images | 23,267 s / 698 images |
| Placement | haut-droite, logo [1578, 55, 240, 65], empreinte [1575, 54, 249, 70] ; le minuteur « 23:44:27 » de la source n'est pas touché |
| Couleur | blanc sur toute la durée (fond 0,05, contraste 0,95) |
| Corrélation / position | 0,9998 à 0,9999 / (0, 0) sur 7 instants |
| Visibilité image par image | 600 images, 0 invisible |
| Zone sûre YouTube (g/h/d/b) | 1479/0/0/806 · hors du coin bas-droit réservé |
| Modifications hors empreinte | 0, 0, 14, 2 et 5 pixels isolés |
| Ratio du logo | 240×65, écart 0,12 % |
| Signature | présente (0,994/255), contenu [623, 205, 674, 670] dans la zone sûre |
| Audio (information) | −16,3 LUFS, crête −4,2 dBTP |

### 4.3 Examen visuel

Les rendus ont été regardés, pas seulement mesurés.

| Pièce | Constat |
|---|---|
| `planche_test_vertical.png` / `planche_test_horizontal.png` | Filigrane discret, lisible, jamais sur un texte. Signature centrée, identique au logo officiel. Contours colorés = zones sûres de chaque plateforme. |
| `zoom_filigrane_x3.png` | Logo **net** à ×3, sans bavure ni crénelage. Proportions officielles. Ombre douce discrète sous la version blanche. Version noire propre sur fond clair. |
| `bascules_couleur_image_exacte.png` | 2,867 → 2,900 s et 17,633 → 17,667 s : le logo change de couleur **sur l'image de la coupe**, sans aucune image invisible. |
| `signature_court_sequence.png`, `signature_*_image_finale.png` | Tracé du symbole → logotype → slogan. L'image finale reproduit le logo vertical officiel : ratio 1,0065 contre 1,0060, IoU 0,958 en 9:16 et 0,954 en 16:9. |
| Opacité 0,88 | Le blanc apparaît légèrement adouci (luminance 0,79 sur fond noir) : présent sans être agressif. |

## 5. Kit de marque, journaux, base, configurations, comptes

| Vérification | Résultat |
|---|---|
| Originaux vs **fichiers envoyés par LUKOJI** | **13/13 identiques octet pour octet** (12 PNG + `symbole.svg` du blog) |
| `brand-verify` (SHA-256 du manifeste) | intègre · 13 originaux en lecture seule (`-r--r--r--`) |
| Base SQLite | `integrity_check` = ok, aucune clé étrangère orpheline, schéma v1. Historique conservé : les rendus refusés par les nouveaux contrôles y figurent en `echec`. |
| Configurations | `engine`, `brand`, `platforms` et `social` se lisent sans erreur ; aucun secret (les seules occurrences des mots sont des commentaires d'avertissement) |
| Journal `var/logs/engine.jsonl` | JSON Lines : début et fin de chaque commande (paramètres, durée, code), placement (coins rejetés et raisons), couleurs, synthèse QC (statut, échecs) |
| Comptes sociaux | `lukoji social` valide · 12/12 tests · 4 liens identiques à ceux fournis · publication désactivée · aucune API connectée |

## 6. Problèmes détectés et corrections

| # | Problème (détecté pendant la phase 0) | Gravité | Correction | Preuve |
|---|---|---|---|---|
| 1 | Placement noté par une **moyenne** dans le temps : un titre visible 3,5 à 11,75 s était recouvert (1er rendu) | Bloquant (règle de marque) | Une position doit être dégagée **à chaque instant** (pas de 0,25 s) ; 4 coins candidats ; contrôle QC bloquant de non-masquage | `planche_test_vertical_v1_defaut.png` ; QC du 1er rendu : ÉCHEC avec les 3 intervalles |
| 2 | Ratio du logo écarté de 0,81 % par arrondi à petite taille | Mineur | Choix du couple entier le plus fidèle (± 3 px) → 0,05 à 0,12 % | test `test_fit_size_minimises_ratio_error` |
| 3 | **Bascules de couleur décalées** de 2 à 3 images après la coupe (pas d'analyse de 0,25 s) : logo invisible 5 à 6 images | Visible à l'écran | Affinage de chaque bascule à l'image exacte ; bornes d'activation à la demi-image | QC image par image : ancien rendu 5 images invisibles → ÉCHEC ; nouveau rendu 0 sur 581 |
| 4 | **L'ombre du logo débordait de 3 à 6 px** hors de la zone sûre (Reels IG/FB, YouTube) : le placement ignorait l'ombre | Bloquant | Placement sur l'**empreinte visible** (logo + ombre) ; contrôle au pixel par plateforme | QC de l'ancien rendu : Reels IG marge −3 px → ÉCHEC ; nouveau : 0 px, dans la zone |
| 5 | Pas de preuve mesurée qu'aucun pixel n'était modifié hors du logo | Lacune de QC | Contrôle `aucune_modification_hors_empreinte` (comparaison réelle source / rendu) | 0 à 45 pixels isolés, bruit d'encodage |
| 6 | Journaux trop pauvres (11 lignes INFO, sans commandes, durées ni résultats QC) | Exploitation | Traçage des commandes, du placement, des couleurs et des synthèses QC | `var/logs/engine.jsonl` |
| 7 | Clé de cache de la signature dépendante du chemin absolu du dépôt | Mineur | Clé calculée sur le contenu des images | test `test_signature_cache_key_is_location_independent` |
| 8 | Avertissement « débit trop bas » sur une vidéo synthétique à aplats (encodage CRF) | Faux positif | Débit passé en information | — |
| 9 | Script : faux « FFmpeg sans libx264 » (`grep -q` avec `pipefail`) | Script | Test de l'encodeur sans pipe | `run_phase0.sh` code 0 |

## 7. Limitations restantes (non bloquantes pour la phase 0)

1. **Zones de sécurité non vérifiées sur téléphone.** Ce sont des valeurs prudentes, appliquées et contrôlées au pixel, mais non confirmées par une capture réelle de chaque application.
2. **Visages peu contrastés** : la détection par contours repère le texte et les graphismes, pas un visage peu contrasté. Parade : `--avoid`. Une détection de visages (OpenCV, gratuit) est prévue en phase 3.
3. **Sources de test** : le réel vertical contient déjà son propre petit logo en haut à gauche, d'où deux logos dans ce test. Les contenus produits par le moteur n'en auront pas.
4. **Audio mesuré seulement** (−14,3 et −16,3 LUFS). La normalisation et le mixage relèvent de la phase 3.
5. **Rendus de test versionnés** (8 et 16 Mo) pour la revue. Les futurs rendus iront dans un stockage externe.
6. **Facebook** : le lien est un lien de partage ; l'identifiant de la Page sera nécessaire en phase 6.

## 8. Conclusion

Les livrables de la phase 0 sont présents, testés et documentés : kit de marque, filigrane, signature,
configurations par plateforme, base SQLite, comptes sociaux, QC automatisé (43 contrôles en vertical) et 43 tests.
Les deux rendus réels sont conformes et ont été examinés visuellement.
**La phase 1 n'a pas été commencée. Aucune API de publication n'est connectée.**
