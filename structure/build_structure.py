#!/usr/bin/env python3
# Construit volN.json (schéma v3) depuis un fihris OCRisé — PARSEUR À PILE
# (emboîtement variable : fann>qism>bab/maqala>fasl, fann>mawqif>fasl, marhala>manhaj>fasl…).
# Usage : build_structure.py <vol> <safar> <fihris.txt> <sha256> <src_name> [--expect "fann1,fann2,..."]
import sys, re, json, unicodedata, os
from collections import defaultdict

vol=int(sys.argv[1]); safar=int(sys.argv[2]); fih=sys.argv[3]; SHA=sys.argv[4]; SRC=sys.argv[5]
expect=[]
if "--expect" in sys.argv: expect=[x for x in sys.argv[sys.argv.index("--expect")+1].split(",") if x]
here=os.path.dirname(os.path.abspath(__file__))

def norm(s):
    s=''.join(c for c in s if not unicodedata.combining(c))
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه').replace('ى','ي')
def clean(s): return re.sub(r"\(\(?\)?\)?","",re.sub(r"\s+"," ",s)).strip()
ORD={"اول":1,"اولى":1,"اولي":1,"اوليه":1,"ثاني":2,"ثانيه":2,"ثالث":3,"ثالثه":3,"رابع":4,"رابعه":4,"خامس":5,"خامسه":5,
 "سادس":6,"سادسه":6,"سابع":7,"سابعه":7,"ثامن":8,"ثامنه":8,"تاسع":9,"تاسعه":9,"عاشر":10,"عاشره":10,
 "حاديعشر":11,"حاديهعشره":11,"ثانيعشر":12,"ثانيهعشره":12,"ثالثعشر":13,"رابععشر":14,"خامسعشر":15,
 "سادسعشر":16,"سابععشر":17,"ثامنعشر":18,"تاسععشر":19,"عشرون":20}
def ordinal(tok):
    t=re.sub(r'[^ء-ي ]',' ',norm(tok)).strip()
    if t.startswith("ال"): t=t[2:]
    return ORD.get(t.replace(" ",""))
KW={"مرحله":"marhala","منهج":"manhaj","فن":"fann","مقاله":"maqala","موقف":"mawqif","باب":"bab","مقصد":"maqsad","مسلك":"maslak","طرف":"taraf","قسم":"qism"}
PREC={"maslak":1,"marhala":2,"fann":2,"maqsad":2,"qism":3,"mawqif":3,"manhaj":3,"bab":4,"maqala":4,"taraf":5}
ADDRF=["maslak","marhala","fann","qism","mawqif","manhaj","maqala","bab","taraf"]
div_re=re.compile(r"(مرحل[ةه]|منهج|فنّ?|مقال[ةه]|موقف|باب|مقصد|مسلك|طرف|قسم)\s+(\S+(?:\s+عشر[ةه]?)?)(.*)")
fasl_re=re.compile(r"(?:فصل|نصل|مصل|لصل|فضل|نضل|مص|فص|نص|صل)\s*\(\s*(\d+)\s*\)\s*(.*)")

stack=[]; nodes=[]; anomalies=[]; seen=set(); fusul=[]
def address(fasl=None):
    a={"volume":vol,"safar":safar,"muqaddima":False,"fasl":fasl}
    for f in ADDRF: a[f]=None
    for t,n in stack: a[t]=n
    return a
def path_id():
    return f"v{vol}-"+"-".join(f"{t}{n}" for t,n in stack)
def base(nid,typ,ar,addr):
    return {"id":nid,"type":typ,"voyage":safar,"address":addr,
      "title":{"arabic_raw_ocr":clean(ar) if ar else None,"arabic_diplomatic":None,
        "arabic_normalized":norm(clean(ar)) if ar else None,"translit":None,"literal_fr":None,"pedagogical_fr":None},
      "pages":{"pdf_start":None,"pdf_end":None,"printed_start":None,"printed_end":None,"pdf_page_basis":"viewer_1based"},
      "theme_fr":"","textual_basis":"explicit","editorial_role":"canonical","pedagogical_role":"none",
      "title_verification":{"source_capture":"ocr","toc_heading_matched":True,"body_heading_matched":False,"arabic_transcription_verified":False},
      "section_verification":{"next_section_located":False,"section_bounds_verified":False,"intermediate_pages_checked":False},
      "certainty":{"hierarchy":"probable","pdf_page":"unverified","printed_page":"unverified"},
      "record_status":"extracted","concepts":[],
      "annotation":{"author_type":"ai","agent":"claude-mulla-sadra","date":"2026-07-23","source_file":SRC,"source_file_sha256":SHA,"human_review":False}}

for raw in open(fih,encoding="utf-8"):
    line=raw.strip()
    dm=div_re.search(line)
    if dm:
        typ=KW.get(norm(dm.group(1))); num=ordinal(dm.group(2))
        if typ and num is not None:
            p=PREC[typ]
            while stack and PREC[stack[-1][0]]>=p: stack.pop()
            stack.append((typ,num))
            nid=path_id()
            if nid not in seen:
                seen.add(nid); nodes.append(base(nid,typ,line,address()))
            continue
    fm=fasl_re.search(line)
    if fm and stack:
        n=int(fm.group(1)); nid=path_id()+f"-f{n}"
        if nid in seen: continue
        seen.add(nid); nodes.append(base(nid,"fasl",fm.group(2),address(n)))
        fusul.append((tuple(stack),n))

json.dump({"_doc":f"Volume {vol} — structure canonique (fihris, parseur à pile). extracted, sans concepts.","volume":vol,"schema_version":"v3","source_pdf":SRC,"nodes":nodes},
          open(os.path.join(here,f"vol{vol}.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# ---- RAPPORT DE COMPLÉTUDE (règle 5) ----
tops=[n for n in nodes if n["type"] in ("marhala","fann","mawqif","bab","maqsad","maslak")]
obtenu=[f"{n['type']}{n['address'][n['type']]}" for n in tops]
per=defaultdict(list)
for st,n in fusul: per[st].append(n)
print(f"=== RAPPORT VOL {vol} (safar {safar}) ===")
print(f"attendu : {expect or '(non précisé)'}")
print(f"obtenu  : {obtenu}")
manq=[e for e in expect if e not in obtenu]
print(f"MANQUANTES : {manq or 'AUCUNE ✅'}")
print(f"fuṣūl total : {len(fusul)} ; par parent :")
sauts=[]
for st in sorted(per,key=lambda s:[x[1] for x in s]):
    nums=sorted(per[st]); miss=sorted(set(range(1,max(nums)+1))-set(nums))
    lbl="/".join(f"{t}{n}" for t,n in st)
    print(f"   {lbl}: f{nums[0]}-{nums[-1]} ({len(nums)})"+(f"  SAUTS {miss}" if miss else ""))
    if miss: sauts.append((st,miss))
print(f"titres non vérifiés (body_heading=false) : {sum(1 for n in nodes if not n['title_verification']['body_heading_matched'])}/{len(nodes)}")
print(f"anomalies : {anomalies or 'aucune'}")
