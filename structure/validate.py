#!/usr/bin/env python3
# Validation des volN.json : (1) contre schema.json si `jsonschema` est dispo,
# (2) + contrôles de cohérence maison (toujours exécutés).
import json, os, sys, glob

here = os.path.dirname(os.path.abspath(__file__))
def load(f): return json.load(open(os.path.join(here, f), encoding="utf-8"))

schema = load("schema.json")
concept_ids = {c["id"] for c in load("concepts.json")["concepts"]}

ENUM = {
    "type": schema["properties"]["type"]["enum"],
    "textual_basis": ["explicit", "inferred", "uncertain"],
    "editorial_role": ["canonical", "reconstructed"],
    "pedagogical_role": ["core", "optional", "none"],
    "record_status": ["extracted", "located", "text_verified", "concept_annotated", "human_validated"],
    "certainty": ["verified", "probable", "unverified"],
    "relation": ["traite_explicitement", "etablit_demontre", "prepare_mobilise"],
    "concept_association": ["verified", "probable", "tentative"],
}

try:
    import jsonschema
    HAVE_JS = True
except Exception:
    HAVE_JS = False

def check_file(path):
    errs = []
    d = json.load(open(path, encoding="utf-8"))
    nodes = d.get("nodes", [])
    ids = set()
    for n in nodes:
        nid = n.get("id", "?")
        # schéma formel si dispo
        if HAVE_JS:
            try: jsonschema.validate(n, schema)
            except jsonschema.ValidationError as e:
                errs.append(f"{nid}: schema: {e.message}")
        # cohérence maison (toujours)
        if nid in ids: errs.append(f"{nid}: id dupliqué")
        ids.add(nid)
        for k in ("type", "textual_basis", "editorial_role", "pedagogical_role", "record_status"):
            if n.get(k) not in ENUM[k]: errs.append(f"{nid}: {k}={n.get(k)!r} hors vocabulaire")
        cert = n.get("certainty", {})
        for k in ("hierarchy", "pdf_page", "printed_page"):
            if cert.get(k) not in ENUM["certainty"]: errs.append(f"{nid}: certainty.{k} invalide")
        # contradiction interdite : arabic non relu mais annoncé transcrit
        tv = n.get("title_verification", {})
        if tv.get("arabic_transcription_verified") and n["title"].get("arabic_diplomatic") is None:
            errs.append(f"{nid}: transcription 'verified' mais arabic_diplomatic absent")
        # un faṣl doit avoir un parent (marhala|fann|mawqif|bab)
        a = n.get("address", {})
        if n.get("type") == "fasl" and not any(a.get(x) for x in ("marhala", "fann", "mawqif", "bab", "maqala", "maqsad", "maslak")):
            errs.append(f"{nid}: faṣl sans parent")
        # pages ordonnées
        ps, pe = a and n["pages"].get("pdf_start"), n["pages"].get("pdf_end")
        if ps and pe and ps > pe: errs.append(f"{nid}: pdf_start>pdf_end")
        prs, pre = n["pages"].get("printed_start"), n["pages"].get("printed_end")
        if prs and pre and prs > pre: errs.append(f"{nid}: printed_start>printed_end")
        # concepts : existence + vocabulaires
        for c in n.get("concepts", []):
            if c.get("concept_id") not in concept_ids: errs.append(f"{nid}: concept inconnu {c.get('concept_id')!r}")
            if c.get("relation") not in ENUM["relation"]: errs.append(f"{nid}: relation invalide")
            if c.get("concept_association") not in ENUM["concept_association"]: errs.append(f"{nid}: concept_association invalide")
    return len(nodes), errs

total_err = 0
for path in sorted(glob.glob(os.path.join(here, "vol*.json"))):
    n, errs = check_file(path)
    tag = "OK" if not errs else f"{len(errs)} ERREUR(S)"
    print(f"{os.path.basename(path)} : {n} nœuds — {tag}" + ("" if HAVE_JS else "  [jsonschema absent -> contrôles maison seuls]"))
    for e in errs: print("   -", e)
    total_err += len(errs)
sys.exit(1 if total_err else 0)
