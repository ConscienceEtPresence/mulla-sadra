# Référentiel canonique des Asfār — état (2026-07-23)

Source de vérité JSON de la structure des 9 volumes (al-Ḥikma al-mutaʿāliya fī l-asfār al-arbaʿa).
**Ce dossier est un fichier de travail — NE PAS publier de page publique figée à partir de lui tant que la validation textuelle n'est pas plus avancée.**

- **626 nœuds** = 65 grandes divisions + 559 fuṣūl + 2 (safar/muqaddima). Tous valident contre `schema.json`.
- **Statut : `structure_audited`** (charpente auditée). **Vérifié au corps : 14 fuṣūl sur 559** seulement.
- Aucun volume `text_verified`. Vol1/Vol2 = `text_partially_verified`.
- Phase 2b (relecture visuelle) : anomalies vol3 m7 f9/f20, vol4 fann1 f7, vol6 mawqif1 f1 résolues ; vol5 fann4 corrigé (voir `redirects_vol5.json`) ; 6 cas `unresolved` documentés (champs `anomaly_status`/`anomaly_note` dans les JSON).
- Le SITE ne lit pas encore ce référentiel : jonction « Lire les Asfār » + liens notions↔adresses = travail à venir.
- Outils : `build_structure.py` (parseur fihris), `validate.py` (validation schéma + cohérence). Détails : `README_schema.md`.
