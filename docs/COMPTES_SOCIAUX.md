# Comptes sociaux officiels LUKOJI MEDIA

Source unique : [`config/social.toml`](../config/social.toml). Ces comptes sont les **destinations
officielles** du moteur pour les phases de publication.

| Plateforme | Lien officiel | Identifiant | Formats destinés |
|---|---|---|---|
| YouTube | https://www.youtube.com/@Lukoji-officiel | `@Lukoji-officiel` | documentaires (samedi 18h00), Shorts |
| Facebook | https://www.facebook.com/share/1MKZxLR4Jz/ | — (lien de partage) | Reels, affiches |
| Instagram | https://www.instagram.com/lukoji_officiel | `lukoji_officiel` | Reels, affiches |
| TikTok | https://www.tiktok.com/@lukoji_officiel | `@lukoji_officiel` | vidéos courtes |

Routage éditorial : vidéos courtes vers les 4 comptes · affiches vers **Facebook et Instagram uniquement** ·
documentaires vers YouTube.

## Règles

- **Aucun secret** dans ce fichier : jetons, mots de passe, clés et identifiants OAuth sont interdits.
  Le chargeur (`src/lukoji_engine/social.py`) refuse la configuration s'il détecte une clé ou une valeur suspecte.
- Validation **hors ligne** uniquement : https, domaine officiel de chaque plateforme, forme du chemin,
  identifiant présent dans l'URL, profils de rendu existants, routage cohérent.
- Phase 0 : `publication = "desactivee"` pour tous les comptes. Aucune API n'est connectée et aucune publication n'est tentée.

## Modifier un compte

1. Éditer `url` (et `identifiant`) dans `config/social.toml`.
2. Lancer `./bin/lukoji social` (affiche les comptes et les valide ; code retour 1 en cas de problème).
3. Lancer `python3 -m pytest -q tests/test_social.py`. Le test `test_official_links_are_recorded_exactly`
   fige les liens officiels : le mettre à jour en même temps, volontairement.

## Point d'attention : Facebook

Le lien fourni (`/share/1MKZxLR4Jz/`) est un **lien de partage**, qui redirige vers la Page. Il est valide
comme destination à afficher. En revanche, la publication par l'API Graph (phase 6) aura besoin de l'**identifiant
de la Page**. Il sera relevé lors de la connexion, ou vous pouvez fournir dès maintenant l'URL directe de la Page
(`https://www.facebook.com/<nom-de-la-page>`).
