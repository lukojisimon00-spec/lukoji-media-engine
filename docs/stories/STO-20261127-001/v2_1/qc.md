# Rapport de contrôle qualité

**Statut : bloque** · score global 80.2/100 · bloquants 6 · alertes 3 · versions {'research': 4, 'hooks': 4, 'structure': 4, 'script': 16, 'storyboard': 7, 'visual': 3}

| Catégorie | Score | Bloquants | Alertes |
|---|---|---|---|
| factuel | 88 | 0 | 2 |
| narratif | 94 | 0 | 1 |
| script | 100 | 0 | 0 |
| visuel | 0 | 6 | 0 |
| duree | 100 | 0 | 0 |

## Indicateurs

- hook_choisi : H9
- hook_recommande : H1
- hook_score : 84.0
- script_mots : 936
- script_duree_s : 379.8
- sequences : 10
- scenes : 44
- storyboard_duree_s : 396.2
- types_visuels : 10

## factuel

- alerte [recherche] faits non utilisables comme faits dans le script (à vérifier ou contradictoires) : F13, F70, F71
- alerte [recherche] sources non vérifiées : S39, S43, S35, S46, S45, S38, S41, S44, S40, S37, S42, S36

## narratif

- alerte [hook H2] vocabulaire de surenchère : personne ne

## visuel

- **BLOQUANT** [séquence SEQ-02] les segments des scènes ne reconstituent pas exactement la voix off
- **BLOQUANT** [séquence SEQ-03] les segments des scènes ne reconstituent pas exactement la voix off
- **BLOQUANT** [séquence SEQ-06] les segments des scènes ne reconstituent pas exactement la voix off
- **BLOQUANT** [séquence SEQ-08] les segments des scènes ne reconstituent pas exactement la voix off
- **BLOQUANT** [séquence SEQ-09] les segments des scènes ne reconstituent pas exactement la voix off
- **BLOQUANT** [storyboard] storyboard construit sur une version périmée : {'script': 'construit sur v13, courante v16', 'visual': 'construit sur v2, courante v3'}

## Suggestions

- `voix_off_desynchronisee` : Redécouper les segments de voix off des scènes pour reconstituer exactement la séquence.
