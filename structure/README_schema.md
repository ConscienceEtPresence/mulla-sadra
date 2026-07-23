> **v3 — le contrat faisant foi est `schema.json`** (ce fichier est explicatif).
> `record_status: human_validated` est **strictement réservé** à une relecture par un humain identifié (Brahms ou un relecteur nommé) — jamais atteint par une double lecture de l'IA.
> Provenance : `source_file_sha256` (préféré au md5). « Contrôles personnalisés réussis » ≠ « validé contre schema.json » (validation formelle jsonschema à exécuter).

# Référentiel canonique JSON — structure des *Asfār*

**Ce n'est pas (encore) une base de données** : c'est un **référentiel canonique en JSON**, source de vérité pour l'extraction éditoriale. On décidera plus tard de son import éventuel (SQLite / PostgreSQL / CMS / lecture directe par le site). Toute table Markdown ou page de site en sera une **vue générée**.

## Portée d'un « nœud »
**Chaque unité de structure est un nœud adressable, y compris chaque Faṣl.** L'adresse cible est :
`volume → (maslak) → marḥala | fann | mawqif | bāb → manhaj → faṣl`.
→ Chaque faṣl a son propre enregistrement et son `id`.

> ⚠ `vol1.json` actuel = **charpente partielle** (l'ossature + les 9 fuṣūl du Manhaj 1, entièrement normalisés). Il ne prétend PAS indexer tout le volume : le Manhaj 2 (22 fuṣūl), le Manhaj 3, et les marâhil 2-3 restent à ajouter, un enregistrement par faṣl. Le Volume 1 complet comptera ~50-60 faṣl-nœuds.

## Fichiers
- `asfar_index.json` — cadre : œuvre, 4 voyages, 9 volumes (avec statut de rattachement).
- `vol1.json` … `vol9.json` — nœuds de structure par volume.

## Schéma d'un nœud
```json
{
  "id": "v1-m1-mn1-f5",
  "volume": 1,
  "type": "fasl",                 // safar|maslak|muqaddima|marhala|manhaj|fann|maqala|mawqif|bab|fasl
  "voyage": { "num": 1 },
  "hierarchy": { "safar": "…", "maslak": "…", "marhala": {"num":1}, "manhaj": {"num":1}, "fasl": {"num":5} },

  "title": {
    "arabic_diplomatic": "في أن تخصص الوجود بما ذا",   // transcription FIDÈLE à l'édition (telle que saisie ; cf source_method)
    "arabic_normalized": "في ان تخصص الوجود بما ذا",     // sans diacritiques, alif/hamza/ta-marbuta normalisés — pour la recherche
    "translit": "fī anna takhaṣṣuṣ al-wujūd bi-mādhā",   // norme unique (voir plus bas)
    "literal_fr": "Par quoi l'existence se détermine",
    "pedagogical_fr": "Ce qui distingue une existence d'une autre : le degré"   // étiquette du SITE, distincte du texte
  },
  "arabic_source_method": "ocr_unverified",   // manual | ocr_corrected | ocr_unverified

  "pages": { "pdf": 27, "printed": "44-45" },
  "theme_fr": "…résumé NEUTRE, sans interprétation pédagogique…",

  "textual_basis":   "explicit",     // explicit | inferred | uncertain   (rapport au TEXTE)
  "editorial_role":  "canonical",    // canonical | reconstructed         (rôle ÉDITORIAL)
  "pedagogical_role":"core",         // core | optional | none            (rôle PÉDAGOGIQUE du site)

  "verification": {
    "toc": true,                       // présent dans le fihris
    "body_heading": true,              // intitulé retrouvé au début d'une page du corps
    "next_section_located": false,     // début de la division SUIVANTE repéré
    "section_bounds_verified": false,  // début + début-suivant cohérents (section bornée)
    "intermediate_pages_checked": false// pages intermédiaires réellement inspectées
  },
  "certainty": {                       // certitude TEXTUELLE vs ÉDITORIALE, par axe
    "title": "verified", "hierarchy": "verified",
    "pdf_page": "verified", "printed_page": "probable", "concept": "verified"
  },

  "concepts": [
    {
      "id": "tashkik",
      "relation": "etablit_demontre",  // traite_explicitement | etablit_demontre | prepare_mobilise
      "justification": {               // OBLIGATOIRE : une relation est une ANNOTATION éditoriale, pas une donnée du sommaire
        "evidence_type": "title+body", // title | body_passage | page_range | title+body
        "ref": "titre f5 « تخصص الوجود بما ذا » ; corps p.27 (impr. 44-45)",
        "note": "le chapitre établit que la détermination se fait par degrés d'intensité",
        "annotator": "assistant",
        "confidence": "probable"       // verified | probable | tentative
      }
    }
  ]
}
```

## Vocabulaires contrôlés
- **type** : safar · maslak · muqaddima · marhala · manhaj · fann · maqala · mawqif · bab · fasl.
- **arabic_source_method** : `manual` (saisi/relu à la main) · `ocr_corrected` (OCR relu) · `ocr_unverified` (OCR brut). *Tant que = `ocr_unverified`, ne jamais présenter le titre comme définitif.*
- **textual_basis** : `explicit` · `inferred` · `uncertain`.
- **editorial_role** : `canonical` · `reconstructed`.
- **pedagogical_role** : `core` · `optional` · `none`.
- **verification** (booléens ; méthode par points de contrôle) : `toc` · `body_heading` · `next_section_located` · `section_bounds_verified` · `intermediate_pages_checked`.
- **certainty** (par axe) : `verified` · `probable` · `unverified`.
- **concepts[].relation** : `traite_explicitement` · `etablit_demontre` · `prepare_mobilise` — **toujours** accompagnée de `justification` (evidence_type, ref, note, annotator, confidence).

## Norme unique de translittération (fixée)
Translittération **académique simplifiée** (proche DIN-31635 / IJMES), appliquée partout :
- Voyelles longues : **ā ī ū**. Diphtongues : aw, ay.
- Emphatiques & spéciales : **ṣ ḍ ṭ ẓ ḥ** ; **ʿ** = ʿayn ; **ʾ** = hamza.
- Digrammes : **th, dh, kh, sh, gh** (jamais ṯ/ḏ…). *j* pour ج.
- Article **al-** invariable (assimilation non notée : *al-shams*, pas *ash-shams*). *tāʾ marbūṭa* = **-a** (état construit **-at**).
- Majuscule : noms propres, débuts, Dieu (*al-Ḥaqq*). Titres d'ouvrages en *italique*.
- **Formes fixées** (à réutiliser telles quelles) : *safar, faṣl, marḥala, manhaj, mawqif, bāb, fann, maqāla ; wujūd, māhiyya, aṣālat al-wujūd, tashkīk, ʿilla, maʿlūl, nafs, maʿād, wājib al-wujūd ; Mullā Ṣadrā*.
- **À proscrire** : circonflexes (û, â), doublons (Sadra/Ṣadrā, Fasl/Faṣl). Une seule graphie par mot.

> Tant que la charpente des neuf volumes n'est pas terminée : **aucune adresse conceptuelle définitive, aucune page publique figée.** Le Volume 1 est un **prototype technique**.
