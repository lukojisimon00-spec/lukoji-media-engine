# Schéma `lukoji.storyboard/1.0` (export pour le Video Engine)

Fichier : `storyboard.json` produit par `./bin/lukoji story export`. Schéma JSON : [`schemas/storyboard.schema.json`](../schemas/storyboard.schema.json).
Validation sans dépendance : `lukoji_engine.story.export.validate_storyboard_json()`.

**Règle de consommation** : le Video Engine ne doit rendre que les exports dont `projet.statut` vaut `ready_for_phase3`.
Les autres exports sont des **brouillons de relecture**.

| Clé | Contenu |
|---|---|
| `schema` | `"lukoji.storyboard/1.0"` |
| `projet` | `id` (STO-…), `titre`, `sujet` (SUJ-…), `format`, `profil_rendu` (profil de `config/platforms.toml`), `statut`, `versions` (version de chaque élément utilisé) |
| `rythme` | `mots_par_minute`, `pause_entre_sequences_s`, `duree_totale_s` |
| `direction_artistique` | document complet du Visual Director |
| `sequences[]` | `id`, `titre`, `etape`, `voix_off`, `debut_s`, `fin_s`, `duree_voix_s`, `objectif`, `emotion`, `transition`, `faits[]` (F…), `sources[]` (S…) |
| `scenes[]` | `id`, `sequence`, `ordre`, `debut_s`, `fin_s`, `duree_s` (temps **absolus**, croissants), `voix_off` (segment exact), `visuel` (voir ci-dessous), `mouvement` {`camera`, `graphique`}, `animation[]`, `texte_ecran[]`, `sources_visuelles[]`, `recherche[]`, `transition`, `son` {`ambiance`, `effets[]`}, `risques_representation`, `instructions_montage`, `raison_narrative` |
| `faits[]` | faits cités : `ref`, `texte`, `statut`, `usage` |
| `sources[]` | sources citées : `ref`, `organisation`, `categorie` (A/B/C), `titre`, `url`, `date_publication` |

Le bloc `visuel` contient :
- `type` : l'un des 16 types de `config/story.toml` ;
- `authenticite` : `authentique`, `illustration`, `reconstitution`, `graphique_explicatif`, `image_generee` ou `symbolique` ;
- `mention_ecran` : texte obligatoire à afficher pour `illustration`, `reconstitution`, `image_generee` et `symbolique` ;
- `description`, `sujet`, `composition`, `cadrage`.

Garanties vérifiées à l'export :
- la concaténation des `voix_off` des scènes d'une séquence est **exactement** la voix off de la séquence ;
- `fin_s − debut_s = duree_s` ;
- les débuts sont croissants ;
- toute scène est rattachée à une séquence existante.
