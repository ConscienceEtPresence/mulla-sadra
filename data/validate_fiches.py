#!/usr/bin/env python3
# Valide les fiches (concepts/notions) et les parcours :
#  (1) contre les schémas JSON (fiche.schema.json / parcours.schema.json) si `jsonschema` dispo ;
#  (2) résout chaque référence dans le référentiel des Asfār (structure/vol*.json) → « Voir le chapitre » ;
#  (3) vérifie les liens croisés (prerequis / pour_aller_plus_loin / concepts_lies / notions / étapes de parcours).
import json, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STRUCT = os.path.join(HERE, "..", "structure")
# Clés STRUCTURELLES identifiant un nœud (safar/voyage exclu : dérivé du volume, champ séparé).
ADDR_KEYS = ("maslak","marhala","manhaj","fann","maqala","mawqif","bab","qism","taraf","fasl")

def load(p): return json.load(open(p, encoding="utf-8"))

# --- index du référentiel : (volume, adresse-normalisée) -> node ---
def build_index():
    idx = {}
    for f in sorted(glob.glob(os.path.join(STRUCT, "vol[1-9].json"))):
        for n in load(f).get("nodes", []):
            idx.setdefault(n["address"]["volume"], []).append(n)
    return idx

def resolve(idx, ref):
    """Appariement EXACT : le nœud dont l'adresse structurelle vaut exactement le spec
    (clés données = valeur ; clés non données = null). Résout aussi bien une division
    (ex. marhala1) qu'un faṣl précis, sans ambiguïté."""
    vol = ref.get("volume")
    cands = idx.get(vol, [])
    spec = {k: ref.get(k) for k in ADDR_KEYS}   # None si absent
    hits = [n for n in cands if all(n["address"].get(k) == spec[k] for k in ADDR_KEYS)]
    return hits

# --- ids de fiches connus (pour liens croisés) ---
def known_ids():
    ids = set()
    for f in glob.glob(os.path.join(HERE, "concepts", "*.json")) + glob.glob(os.path.join(HERE, "notions", "*.json")):
        ids.add(os.path.splitext(os.path.basename(f))[0])
    return ids

def main():
    idx = build_index()
    ids = known_ids()
    # jsonschema (optionnel)
    try:
        import jsonschema
        from jsonschema import RefResolver
        fiche_s = load(os.path.join(HERE, "fiche.schema.json"))
        parc_s  = load(os.path.join(HERE, "parcours.schema.json"))
        store = {fiche_s["$id"]: fiche_s, parc_s["$id"]: parc_s}
        HAVE = True
    except Exception:
        HAVE = False

    errs, warns, links = [], [], 0
    fiches = sorted(glob.glob(os.path.join(HERE, "concepts", "*.json")) +
                    glob.glob(os.path.join(HERE, "notions", "*.json")))
    for p in fiches:
        d = load(p); nm = os.path.relpath(p, HERE)
        if HAVE:
            try:
                jsonschema.validate(d, fiche_s, resolver=RefResolver(fiche_s["$id"], fiche_s, store))
            except jsonschema.ValidationError as e:
                errs.append(f"{nm}: schéma: {e.message}")
        # références → référentiel
        refs = list(d.get("references", [])) + list(d.get("developpements", [])) + list(d.get("premiere_apparition", []))
        for c in d.get("citations_cles", []):
            if c.get("reference"): refs.append(c["reference"])
        for r in refs:
            hits = resolve(idx, r)
            addr = "v%s " % r.get("volume") + " ".join(f"{k}{r[k]}" for k in ADDR_KEYS if r.get(k) is not None)
            if len(hits) == 1:
                links += 1
            elif not hits:
                errs.append(f"{nm}: référence NON résolue → {addr}")
            else:
                warns.append(f"{nm}: référence AMBIGUË ({len(hits)} nœuds) → {addr}")
        # liens croisés
        for key in ("prerequis","pour_aller_plus_loin","concepts_lies","notions"):
            for tid in d.get(key, []):
                if tid not in ids:
                    warns.append(f"{nm}: {key} → « {tid} » (fiche pas encore créée)")

    # parcours
    for p in sorted(glob.glob(os.path.join(HERE, "parcours", "*.json"))):
        d = load(p); nm = os.path.relpath(p, HERE)
        if HAVE:
            try:
                jsonschema.validate(d, parc_s, resolver=RefResolver(parc_s["$id"], parc_s, store))
            except jsonschema.ValidationError as e:
                errs.append(f"{nm}: schéma: {e.message}")
        for e in d.get("etapes", []):
            if e.get("ref") and e["ref"] not in ids:
                warns.append(f"{nm}: étape {e.get('ordre')} → « {e['ref']} » (fiche pas encore créée)")

    print(f"Fiches: {len(fiches)} | schéma: {'jsonschema' if HAVE else 'ABSENT (validation formelle sautée)'}")
    print(f"Références résolues dans le référentiel: {links}")
    for w in warns: print("  ⚠ ", w)
    for e in errs: print("  ✗ ", e)
    print("→", "OK ✅" if not errs else f"{len(errs)} ERREUR(S)")
    sys.exit(1 if errs else 0)

if __name__ == "__main__":
    main()
