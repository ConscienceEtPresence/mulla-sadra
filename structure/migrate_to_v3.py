#!/usr/bin/env python3
# Migration reproductible : ancien schéma -> schéma v3 (schema.json).
# Corrige la contradiction ocr_unverified / title:verified, dédouble l'arabe,
# structure les pages, uniformise l'adresse, harmonise les certitudes,
# ajoute record_status et une provenance complète (annotation + md5).
import json, sys, os

MD5 = {1: "78273f84afd20372c0826a6a5eec6358", 2: "07b63253fe50c18850b305eedf29268b"}
SRC = {1: "…volume arabe 1.pdf", 2: "…volume arabe 2.pdf"}
CONF = {"verified": "verified", "probable": "probable", "tentative": "tentative", "na": "tentative", None: "tentative"}

def parse_pages(p):
    p = p or {}
    ps = p.get("pdf") if isinstance(p.get("pdf"), int) else None
    prs = pre = None
    pr = p.get("printed")
    if pr:
        s = str(pr)
        if "-" in s:
            a, b = s.split("-", 1)
            prs, pre = int(a), int(b)
        elif s.isdigit():
            prs = int(s)
    return {"pdf_start": ps, "pdf_end": None, "printed_start": prs, "printed_end": pre, "pdf_page_basis": "viewer_1based"}

def address(vol, h):
    h = h or {}
    def num(x): return (h.get(x) or {}).get("num") if isinstance(h.get(x), dict) else None
    return {
        "volume": vol,
        "safar": 1 if h.get("safar") else None,
        "maslak": 1 if h.get("maslak") else None,
        "muqaddima": bool(h.get("muqaddima")),
        "marhala": num("marhala"), "manhaj": num("manhaj"),
        "fann": num("fann"), "maqala": num("maqala"),
        "mawqif": num("mawqif"), "bab": num("bab"),
        "fasl": num("fasl"),
    }

def migrate(n, vol):
    ov = n.get("verification", {}) or {}
    oc = n.get("certainty", {}) or {}
    t = n.get("title", {}) or {}
    body = bool(ov.get("body_heading"))
    node = {
        "id": n["id"], "type": n["type"],
        "voyage": (n.get("voyage") or {}).get("num"),
        "address": address(vol, n.get("hierarchy", {})),
        "title": {
            "arabic_raw_ocr": t.get("arabic_diplomatic") or t.get("arabic_exact"),
            "arabic_diplomatic": None,
            "arabic_normalized": t.get("arabic_normalized"),
            "translit": t.get("translit"),
            "literal_fr": t.get("literal_fr"),
            "pedagogical_fr": t.get("pedagogical_fr"),
        },
        "pages": parse_pages(n.get("pages")),
        "theme_fr": n.get("theme_fr", ""),
        "textual_basis": n.get("textual_basis", "uncertain"),
        "editorial_role": n.get("editorial_role", "reconstructed"),
        "pedagogical_role": n.get("pedagogical_role", "none"),
        "title_verification": {
            "source_capture": "ocr",
            "toc_heading_matched": bool(ov.get("toc")),
            "body_heading_matched": body,
            "arabic_transcription_verified": False,
        },
        "section_verification": {
            "next_section_located": bool(ov.get("next_section_located")),
            "section_bounds_verified": bool(ov.get("section_bounds_verified")),
            "intermediate_pages_checked": bool(ov.get("intermediate_pages_checked")),
        },
        "certainty": {
            "hierarchy": oc.get("hierarchy", "unverified"),
            "pdf_page": oc.get("pdf_page", "unverified"),
            "printed_page": oc.get("printed_page", "unverified"),
        },
        "record_status": "located" if body else "extracted",
        "concepts": [],
        "annotation": {
            "author_type": "ai", "agent": "claude-mulla-sadra", "date": "2026-07-23",
            "source_file": SRC[vol], "source_file_md5": MD5[vol], "human_review": False,
        },
    }
    for c in n.get("concepts", []):
        j = c.get("justification", {}) or {}
        node["concepts"].append({
            "concept_id": c["id"], "relation": c["relation"],
            "relation_status": "to_confirm",
            "concept_association": CONF.get(j.get("confidence"), "tentative"),
            "evidence": {"type": j.get("evidence_type") or "title", "ref": j.get("ref") or "", "note": j.get("note")},
        })
    if node["concepts"]:
        node["record_status"] = "concept_annotated"
    for k in ("note", "fusul_count", "fusul_detail"):
        if k in n: node[k] = n[k]
    return node

here = os.path.dirname(os.path.abspath(__file__))
for vol in (1, 2):
    path = os.path.join(here, f"vol{vol}.json")
    d = json.load(open(path, encoding="utf-8"))
    d["nodes"] = [migrate(n, vol) for n in d["nodes"]]
    d["schema_version"] = "v3"
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"vol{vol}.json migré -> v3 ({len(d['nodes'])} nœuds)")
