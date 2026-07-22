# Mullā Ṣadrā — Les quatre voyages de l'existence

Site public du **monde spirituel** (compte GitHub `ConscienceEtPresence`), famille de
Jaspers / L'essence retrouvée / lavoiedudedans. Objectif : présenter la pensée de
**Mullā Ṣadrā** *de l'intérieur*, dans sa cohérence propre — entrer dans son univers,
pas en faire l'histoire comparée des doctrines.

*Titre de travail — modifiable. Domaine non encore attribué.*

## Principes

- **Statique multipage**, sans framework. Déployable sur GitHub Pages.
- **Bilingue FR / EN en miroir** : les pages anglaises vivent sous `en/`, mêmes noms de fichiers.
- **Charte de la famille** : parchemin clair, bandeaux nuit, or (`assets/css/base.css`).
- **Cinq degrés de profondeur** par notion (Saisir · Par l'expérience · Le raisonnement · Le texte · Le système).
- **Terminologie** toujours quadrilingue : arabe vocalisé · translittération scientifique · français · anglais.
- **Droits d'auteur** : synthèses et traductions *originales*, citations courtes attribuées.
  Jamais recopier une traduction publiée (Corbin, Jambet…).
- Le texte arabe **de l'édition** est toujours distingué de la **vocalisation ajoutée**
  (travail éditorial interprétatif, à vérifier — jamais généré à l'aveugle).

## Structure

```
index.html · notions/ · auteur.html · glossaire.html      (FR)
en/…                                                       (EN, miroir)
assets/css/base.css        charte commune
assets/js/lang.js          mémoire de préférence FR/EN
assets/js/notion.js        profondeur (5 niveaux) + infobulles de termes
assets/js/glossaire.js     filtre du glossaire
assets/js/pulse.js         analytics anonyme (Firebase la-voie-du-dedans, SITE='mullasadra')
data/terminologie.json     base terminologique (source unique — future génération)
data/reseau.json           graphe des notions (carte + panneaux « réseau »)
data/notions/*.json        fiches-notions structurées (graines du générateur)
```

## État (v1 — fondations)

- Accueil, **notion pilote `aṣālat al-wujūd`** (5 niveaux complets), auteur, glossaire — FR + EN.
- Pages écrites à la main à partir des `data/*.json`. Un **générateur JSON→HTML** viendra
  industrialiser les notions suivantes (source unique = `data/`).

## À faire

- **Vérifier la référence** du passage arabe (Niveau IV) : installer un OCR arabe
  (`tesseract-ara`) ou pointer la page dans le PDF de la Partie 1. Actuellement marquée « à vérifier ».
- Vérifier la vocalisation ajoutée.
- Carte conceptuelle interactive (porte « Explorer »), pages Voyages / Œuvre, notions suivantes.
- Figer : titre définitif, domaine, translittération, date de mort de l'auteur.
- Icônes PWA (`assets/icons/`), image d'ouverture (`og`).

## Firebase

`la-voie-du-dedans` — **analytics seulement** (`analytics/mullasadra/jours/{date}`), comme
Jaspers et L'essence retrouvée. Aucune donnée personnelle, aucun cookie.
