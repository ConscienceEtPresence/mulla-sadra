import json, unicodedata, sys
def norm(s):
    s=''.join(c for c in s if not unicodedata.combining(c))
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه').replace('ى','ي')
def set_fasl(volfile, nid, arabic, pdf_page, printed_page, note):
    d=json.load(open(volfile))
    n=next((x for x in d['nodes'] if x['id']==nid), None)
    if not n: print('ABSENT', nid); return
    n['title']['arabic_raw_ocr']=arabic
    n['title']['arabic_normalized']=norm(arabic)
    n['title_verification']['source_capture']='manual'   # transcrit à la main depuis l'image (par l'IA)
    n['title_verification']['toc_heading_matched']=True
    n['title_verification']['body_heading_matched']=True
    n['title_verification']['arabic_transcription_verified']=False  # pas de relecture humaine
    n['pages']['pdf_start']=pdf_page
    n['pages']['printed_start']=printed_page
    n['pages']['pdf_page_basis']='viewer_1based'
    n['certainty']['pdf_page']='verified'
    n['certainty']['printed_page']='verified'
    n['record_status']='text_verified'
    n['editorial_role']='canonical'
    n['capture_method']='visual_image_read_ai'
    n['verification_note']=note
    json.dump(d, open(volfile,'w'), ensure_ascii=False, indent=2)
    print('OK', nid, '| p.PDF', pdf_page, '| impr.', printed_page)
if __name__=='__main__':
    set_fasl('vol3.json','v3-marhala7-f9',
      'في أن القدرة ليست نفس المزاج كما زعمه بعض الأطباء', 19, 20,
      'Lecture visuelle image PDF p.19 (impr.20) ; en-tête rouge « فصل (9) » lisible, précédé de f8 (p.18) et suivi de f10 « في الحركة والسكون » sur la même page. confirmed_fasl.')
