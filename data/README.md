# Données de l'édition numérique — modèle stable

Deux couches de contenu scientifique, un contrat de schéma **stable** (à ne plus faire dériver).

## Types de fiches
- **`concepts/`** — termes atomiques (wujud, mahiyya, quwwa, fiʿl, jawhar, ʿaraḍ, ʿilla, maʿlūl, nafs, ʿaql, ḥaraka…). Identité + définition + renvois.
- **`notions/`** — doctrines (aṣālat al-wujūd, tashkīk, ḥaraka jawhariyya…). Fiches riches (5 niveaux, comparaisons, erreurs, etc.).

Les deux suivent **un seul schéma** : `fiche.schema.json` (champ `type` = `concept` | `notion`).
Les parcours de lecture suivent `parcours.schema.json` (dossier `parcours/`).

## Le lien qui fait la valeur : `references` → référentiel
Chaque renvoi pointe **exactement** dans le référentiel des Asfār (`../structure/vol*.json`), avec le même vocabulaire d'adresse (`volume, maslak, marhala, manhaj, fann, maqala, mawqif, bab, qism, taraf, fasl`). `validate_fiches.py` **résout** chaque référence vers un nœud réel → le site pourra afficher « Voir le chapitre » automatiquement. Le voyage/safar n'est pas une clé d'appariement (dérivé du volume).

## Provenance — la distinction en 3 niveaux (obligatoire à terme)
Champ `niveau_confiance` sur tout contenu éditorial :
- **`atteste`** — directement attesté par les Asfār (accompagné d'une `reference`) ;
- **`synthese_editoriale`** — synthèse rédigée par l'éditeur ;
- **`comparaison`** — mise en perspective avec d'autres auteurs / l'histoire de la philosophie ;
- (`hypothese` — piste non tranchée.)

Bloc `validation` sur chaque fiche : `texte_verifie / traduction_verifiee / vocalisation_verifiee / concepts_valides / niveau`.

## Qui écrit quoi
- **Brahms (éditeur)** : tout le contenu doctrinal (définitions, importance, difficultés, erreurs, questions, comparaisons, citations).
- **Structure/IA** : le schéma, les squelettes de fiches, la résolution des références, la validation. Aucun contenu doctrinal inventé.

## Valider
```
python3 data/validate_fiches.py
```
Vérifie : conformité au schéma + résolution des références dans le référentiel + liens croisés (avertit si une fiche liée n'existe pas encore).

## Modèles déjà en place
- `notions/asalat-al-wujud.json` — modèle **notion** (9 blocs éditoriaux + références résolues).
- `concepts/wujud.json` — modèle **concept** (identité + définition, blocs doctrinaux à rédiger).
- `parcours/debutant.json` — modèle **parcours**.

## À réconcilier (dette connue du référentiel)
`vol1.json` : les fuṣūl du Manhaj 1 (branche « m1-mn1 », `maslak=null`) ne sont pas nichés sous `maslak1` comme les marâhil (`maslak=1`). Les références s'écrivent donc différemment selon la branche. À homogénéiser lors d'une passe de réconciliation du pilote.
