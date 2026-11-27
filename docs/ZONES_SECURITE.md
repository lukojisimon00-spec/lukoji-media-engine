# Zones de sécurité par plateforme

Configuration : `config/platforms.toml`. Toutes les valeurs y sont modifiables, aucune n'est codée en dur.
Marges en pixels sur le canevas indiqué. **Zone sûre** = zone où l'interface de l'application ne
recouvre pas l'image. Elle est intersectée avec les **aperçus recadrés** (grille du profil, fil d'actualité).

> **Statut : valeurs de travail prudentes, NON vérifiées sur appareil** (`verifie_sur_appareil = false`).
> Elles proviennent des recommandations publiques des plateformes et des pratiques de production
> courantes. Les interfaces varient selon le téléphone, la version de l'application et la langue.
> Action recommandée : faire une capture d'écran réelle par plateforme et ajuster `platforms.toml`.

## Vertical 9:16 (1080×1920)

| Plateforme | Haut | Bas | Gauche | Droite | Aperçu recadré | Zone sûre résultante [x, y, l, h] |
|---|---|---|---|---|---|---|
| TikTok | 160 | 480 | 60 | 140 | — | [60, 160, 880, 1280] |
| Instagram Reels | 250 | 500 | 65 | 130 | grille de profil 3:4 | [65, 250, 885, 1170] |
| Facebook Reels | 230 | 500 | 60 | 130 | fil d'actualité 4:5 | [60, 285, 890, 1135] |
| YouTube Shorts | 180 | 450 | 60 | 150 | — | [60, 180, 870, 1290] |
| **Maître multi-plateformes** (`vertical_universal`) | — | — | — | — | intersection des 4 | **[65, 285, 865, 1135]** |

Ce qui occupe les marges :
- **TikTok** : onglets « Suivis / Pour toi », LIVE et recherche en haut ; colonne J'aime, commentaires, partages et disque à droite ; pseudo, légende, son et barre de navigation en bas.
- **Instagram Reels** : titre « Reels » et caméra en haut ; actions à droite ; compte, légende et audio en bas. La grille du profil montre un recadrage central 3:4.
- **Facebook Reels** : interface proche d'Instagram. Le fil d'actualité peut recadrer en 4:5 au centre.
- **YouTube Shorts** : recherche, caméra et menu en haut ; actions à droite ; titre, chaîne, bouton « S'abonner » et son en bas.

Les coordonnées diffèrent pour chaque plateforme (test `test_platforms_have_distinct_safe_zones`).
Le profil maître garantit qu'**un seul export** est sûr partout. Le filigrane y est placé dans la bande
centrale 4:5, donc il reste visible même dans les aperçus recadrés.

Positions du filigrane dans le profil maître. Le logo fait 218×59 ; son empreinte visible, ombre de la version blanche comprise, fait 226×63. C'est l'empreinte qui touche le bord de la zone sûre :

| Ancre | Logo [x, y, l, h] | Empreinte visible |
|---|---|---|
| haut-gauche (préférée) | [68, 286, 218, 59] | [65, 285, 226, 63] |
| haut-droite | [707, 286, 218, 59] | [704, 285, 226, 63] |
| bas-gauche | [68, 1358, 218, 59] | [65, 1357, 226, 63] |
| bas-droite | [707, 1358, 218, 59] | [704, 1357, 226, 63] |

**Application réelle, vérifiée au pixel** : le QC calcule l'empreinte visible à partir de l'image réelle du logo et vérifie qu'elle tient dans la zone sûre de **chaque** plateforme (`zone_securite_<plateforme>`, avec les marges restantes). Il compare aussi le rendu à la source pour prouver qu'aucun pixel n'est modifié hors de cette empreinte (`aucune_modification_hors_empreinte`).

Les coins bas se situent **au-dessus** des légendes des applications. Les sous-titres du moteur (phase 3)
seront déclarés comme zones réservées : le filigrane ne pourra donc jamais les recouvrir.

## YouTube 16:9 (1920×1080)

| Haut | Bas | Gauche | Droite | Réservé | Zone sûre |
|---|---|---|---|---|---|
| 54 | 150 | 96 | 96 | coin bas-droit [1500, 760, 420, 320] | [96, 54, 1728, 876] |

- Marges latérales et haute : « title safe » à 90 %. Bas : barre de progression et contrôles du lecteur.
- Coin bas-droit réservé : filigrane de chaîne YouTube et éléments d'écran de fin.
- Haut-gauche : titre et avatar au survol en lecteur intégré, d'où l'ancrage préféré **haut-droite**.
- Le teaser des fiches peut apparaître brièvement en haut à droite. Si des fiches sont utilisées, imposer `--anchor top_left`.

## Ajouter ou ajuster une plateforme

1. Ajouter `[profiles.nom]` dans `platforms.toml` (canvas, fps, orientation, marges, apercus, reserve).
2. Pour l'inclure dans l'export unique, l'ajouter à `union_of` du profil maître.
3. Lancer `./bin/lukoji profiles` puis `python3 -m pytest -q`.
