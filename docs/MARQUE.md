# Kit de marque LUKOJI — règles appliquées par le moteur

Source de vérité : `config/brand.toml`. Toute modification des valeurs passe par ce fichier.

## 1. Ressources

### Originaux (`brand/originals/`, en lecture seule, SHA-256 dans `brand/manifest.json`)

| Clé | Fichier | Usage |
|---|---|---|
| `symbole_svg` | `symbole_officiel.svg` | **Source vectorielle officielle** du symbole (copie de `lukoji-blog/symbole.svg`). Tout rendu du symbole en dérive. |
| `symbole_noir` / `symbole_blanc` | `symbole_*_transparent_800x1600.png` | Référence raster ; sert à valider le SVG (IoU 0,991). |
| `horizontal_noir` / `horizontal_blanc` | `horizontal_*_transparent_2800x800.png` | **Filigrane** (symbole + LUKOJI), format horizontal. |
| `horizontal_blanc_ombre` | `horizontal_blanc_ombre_720x240.png` | Précédent officiel de l'ombre portée douce. |
| `vertical_slogan_noir` / `vertical_slogan_blanc` | `vertical_slogan_*_2400x1600.png` | Format vertical avec slogan ; **base de la signature de fin**. |
| `avatar_noir_sur_blanc` / `avatar_blanc_sur_noir` | `avatar_*_1000.png` | Format carré 1:1 (avatars). |
| `presentation_positif` / `presentation_negatif` / `planche_declinaisons` | planches 2400x1600 | Références visuelles, non utilisées en production. |

Les 14 fichiers fournis contenaient 12 visuels distincts : deux paires étaient des doublons octet pour octet,
regroupées dans `uploads` de `brand.toml`.

### Format par usage

| Besoin | Ressource |
|---|---|
| Horizontal (filigrane, en-têtes) | `horizontal_blanc` / `horizontal_noir` |
| Vertical (signature, affiches verticales) | `vertical_slogan_blanc` / `vertical_slogan_noir` |
| Carré (avatars, pastilles) | `avatar_blanc_sur_noir` / `avatar_noir_sur_blanc` |
| Symbole seul, toute taille | `symbole_svg` (rendu vectoriel) |

### Dérivés autorisés (générés dans `var/cache/brand`, versionnés en base)

1. **Découpe** sans retouche de pixels (ex. logotype et slogan extraits du logo vertical ; test : égalité pixel à pixel).
2. **Rendu du SVG officiel** : géométrie intacte ; seule la couleur du trait peut prendre une couleur de la palette (#FFFFFF / #0B0B0B).
3. **Redimensionnement proportionnel** (Lanczos, alpha prémultiplié). La taille entière retenue minimise l'écart de ratio (< 0,5 %).
4. **Ombre portée douce** sous la version blanche (précédent officiel `horizontal_blanc_ombre`).

Interdits : redessiner, recolorer hors palette, étirer, recomposer le logotype en police, remplacer le logo.

### Palette

| Nom | Hex | Usage |
|---|---|---|
| Noir | `#0B0B0B` | fond principal, logo positif |
| Blanc | `#FFFFFF` | logo négatif, textes sur fond sombre |
| Fond clair | `#F6F6F3` | fond clair éditorial |
| Gris | `#BDBDBD` `#9A9A9A` `#555555` | textes secondaires, filets |
| Jaune · Orange · Orange intense | `#FFD23F` `#FF8A00` `#FF5A00` | **accents motion design uniquement** |

### Typographies (`brand/fonts/`, licence OFL)

- **Archivo Black** : titres.
- **IBM Plex Mono** (Regular, Medium, SemiBold, Bold) : labels, sources, rubriques, textes techniques.

## 2. Filigrane (vidéos des réseaux LUKOJI)

| Paramètre | Valeur par défaut | Réglage |
|---|---|---|
| Variante | `lockup` (logo horizontal officiel) | `--variant symbole` = symbole SVG seul |
| Taille | 220 px de large en 9:16 (≈ 20 % de la largeur) · 240 px en 16:9 (12,5 %) | `brand.toml › watermark.layouts` |
| Opacité | 0,88 | `--opacity` (0,2–1,0) |
| Couleur | `adaptive` : blanc sur fond sombre, noir sur fond clair, **par segment** | `--color white|black` |
| Apparition | fondu de 0,3 s au début | `fade_in` |
| Ombre | douce, sous la version blanche uniquement | `shadow = auto|on|off` |
| Présence | tout le contenu principal ; **absent de la signature** | — |

### Règles de placement

1. Le logo est rendu à sa taille finale **avant** FFmpeg. FFmpeg ne fait que le superposer, donc aucune déformation n'est possible.
2. Candidats : coins de la **zone sûre** du profil, dans l'ordre de préférence. En 9:16 : haut-gauche, haut-droite, bas-gauche, bas-droite. En 16:9 : haut-droite, haut-gauche.
3. Un candidat est **exclu** s'il chevauche :
   - une zone réservée de la plateforme (par exemple le filigrane de chaîne YouTube) ;
   - une zone réservée du contenu (`--avoid` : sous-titres, texte clé, visage), avec 16 px de marge ;
   - du **détail à un instant quelconque**. La densité de contours est mesurée toutes les 0,25 s sur toute la durée ; seuil 0,012 (texte mesuré ≈ 0,02 ; fond ≤ 0,006).
4. Parmi les candidats dégagés, le premier dans l'ordre de préférence l'emporte (à égalité, le plus calme).
5. Si **aucun** coin n'est dégagé, le rendu est produit mais signalé (`clear=false`), et le contrôle qualité le **refuse**. Il faut alors une validation humaine : déplacer le texte du montage ou imposer une position.
6. La couleur suit la luminance du fond **sous les tracés du logo**, avec une hystérésis de 0,50 à 0,62 et des segments d'au moins 0,75 s, pour éviter tout clignotement.

## 3. Signature de fin « LUKOJI »

La signature **reconstitue exactement le logo vertical officiel**, avec les positions relatives du fichier `vertical_slogan_*` et une mise à l'échelle uniforme :

1. le symbole se trace (SVG officiel, animation du trait) ;
2. le logotype LUKOJI apparaît (découpe du PNG officiel) ;
3. le slogan apparaît.

| Préréglage | Durée | Contenu | Usage par défaut |
|---|---|---|---|
| `aucune` | 0 s | — | affiches, contenus < 12 s |
| `flash` | 1,0 s | symbole + logotype | formats très rythmés |
| `court` | 1,6 s | symbole + logotype + slogan | **vidéos courtes** |
| `documentaire` | 3,5 s | idem, plus posé | **documentaires YouTube** |

- Enchaînement : fondu de 0,25 s avec la fin du contenu ; l'audio principal s'éteint en 0,4 s.
- **Non imposée** : `--signature aucune`. Elle est automatiquement omise si le contenu fait moins de 12 s, pour ne pas ralentir le rythme.
- Thème `negatif` (blanc sur #0B0B0B) par défaut ; `positif` (noir sur blanc) disponible.
- Le contenu de la signature doit tenir dans la zone sûre du profil (contrôle `signature_dans_zone_sure`).

## 4. Formats de sortie

| Profil | Canevas | i/s | Codec | Usage |
|---|---|---|---|---|
| `vertical_universal` | 1080×1920 (9:16) | 30 | H.264 High 4.1, yuv420p, AAC 48 kHz stéréo 192 k, faststart | vidéo courte unique pour TikTok, Reels IG/FB, Shorts |
| `tiktok`, `instagram_reels`, `facebook_reels`, `youtube_shorts` | 1080×1920 | 30 | idem | déclinaison par plateforme si nécessaire |
| `youtube_16x9` | 1920×1080 (16:9) | 30 | idem | documentaires |

Qualité : CRF 18, preset `medium`, image clé toutes les 2 s, BT.709 en plage limitée.
Une source d'un autre format est mise à l'échelle **sans déformation**, avec des bandes #0B0B0B si nécessaire.
