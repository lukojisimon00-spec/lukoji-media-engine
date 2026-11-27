# LUKOJI MEDIA ENGINE

Moteur de production des **contenus propres de LUKOJI** (vidéos courtes, affiches, documentaires),
média entrepreneurial — *INNOVER · CRÉER · IMPACTER*.

> Périmètre : uniquement les contenus publiés par LUKOJI sur ses propres réseaux.
> Les commandes clients, devis et livrables relèvent de **CLIENT STUDIO** (espace distinct).

**État : phase 0 terminée** (fondations et kit de marque). Voir [`docs/RAPPORT_PHASE0.md`](docs/RAPPORT_PHASE0.md).

## Prérequis

| Outil | Version testée | Rôle |
|---|---|---|
| FFmpeg / FFprobe (avec libx264, AAC) | 6.1.1 | encodage, incrustation, mesures |
| Python | 3.13 (≥ 3.11) | moteur (dépendances : Pillow, numpy ; tests : pytest) |
| Node.js + Playwright (Chromium) | 22 | rendu du SVG officiel et de la signature animée |

Aucun service payant, aucune clé API n'est nécessaire pour la phase 0.

## Démarrage

```bash
./scripts/run_phase0.sh          # reproduit toute la validation : base, kit, rendus réels, QC, tests
python3 -m pytest -q             # 27 tests (unitaires + bout en bout, ~2 min 30)
python3 -m pytest -q -m "not e2e"  # tests rapides uniquement
```

## Commandes (`./bin/lukoji …`)

| Commande | Effet |
|---|---|
| `db-init` | crée / migre la base SQLite (`var/lukoji.sqlite3`) |
| `brand-build` | écrit `brand/manifest.json` (SHA-256 des originaux), enregistre les ressources, génère les découpes de signature |
| `brand-verify` | vérifie qu'aucun original n'a été modifié (code retour ≠ 0 sinon) |
| `profiles` | liste les profils de sortie et leurs zones sûres |
| `watermark IN OUT --profile P [--kind short] [--signature court] [--avoid x,y,l,h] …` | filigrane + signature, sidecar JSON, enregistrement en base |
| `signature --profile P --preset court` | rend la signature seule |
| `qc VIDEO [--json rapport.json]` | contrôle qualité complet (code retour 1 si bloquant) |
| `sheet VIDEO planche.png [--times 1,5,9]` | planche visuelle avec zones sûres et boîte du filigrane |
| `content list|add|move|history` | registre des contenus et cycle de vie |

Exemple — vidéo courte destinée aux 4 plateformes, sous-titres réservés entre y=1180 et y=1400 :

```bash
./bin/lukoji watermark montage.mp4 var/out/short.mp4 --profile vertical_universal --kind short \
    --avoid 65,1180,865,220
./bin/lukoji qc var/out/short.mp4
```

## Arborescence

```
brand/originals/   logos officiels, copies octet pour octet, en lecture seule (+ symbole SVG officiel)
brand/fonts/       Archivo Black, IBM Plex Mono (licence OFL)
brand/manifest.json  empreintes SHA-256 des originaux
config/            engine.toml (chemins, encodage), brand.toml (marque, filigrane, signature),
                   platforms.toml (profils, zones sûres)
src/lukoji_engine/ config, paths, log, db, geometry, assets, media, watermark, signature, qc, cli
scripts/           render_svg.mjs, render_signature.mjs (Chromium), run_phase0.sh
tests/             suite pytest
docs/              MARQUE.md, ZONES_SECURITE.md, RAPPORT_PHASE0.md, TRANSFERT.md, validation/
var/               (non versionné) base, journaux, caches, rendus
```

## Documentation

- [Règles de marque : filigrane, signature, formats](docs/MARQUE.md)
- [Zones de sécurité par plateforme](docs/ZONES_SECURITE.md)
- [Rapport de validation phase 0](docs/RAPPORT_PHASE0.md)
- [Transfert vers le dépôt GitHub](docs/TRANSFERT.md)
