#!/usr/bin/env python3
"""Static source and local-link checks; never claims browser or runtime QA."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import hashlib,json,re,subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.refs=[];self.images=[];self.cards=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id'in a:self.ids.append(a['id'])
        for attr in ['href','src']:
            if a.get(attr):self.refs.append((tag,attr,a[attr]))
        if tag=='img':self.images.append(a)
        if tag=='article' and 'card' in a.get('class','').split():self.cards.append(a)

pages=[ROOT/'review-v2.html',OUT/'index.html']
pages += [OUT/name for name in ['M01-head-AE-r6.html','M01-turnaround-r12.html','next-batch-mecha-20261019.html','M01-family-head-review-r14.html','M05-style-match-r2.html','M05-modular-r4.html','M05-battle-mask-r8.html','M05-turnaround-r12.html','M02-turnaround-r2.html','M11-cargo-r1.html','M11-future-r2.html'] if (OUT/name).exists()]
parsed={}
if (OUT/'M11-structure-and-head-r4.html').exists():pages.append(OUT/'M11-structure-and-head-r4.html')
if (OUT/'M11-heroic-antenna-r5.html').exists():pages.append(OUT/'M11-heroic-antenna-r5.html')
if (OUT/'M11-turnaround-structure-r7.html').exists():pages.append(OUT/'M11-turnaround-structure-r7.html')
if (OUT/'M11-source-delivery-r9.html').exists():pages.append(OUT/'M11-source-delivery-r9.html')
if (OUT/'aircraft-source-batch-20261022.html').exists():pages.append(OUT/'aircraft-source-batch-20261022.html')
if (OUT/'aircraft-runtime-comparison-20261022.html').exists():pages.append(OUT/'aircraft-runtime-comparison-20261022.html')
if (OUT/'aircraft-existing-design-recolour-r2.html').exists():pages.append(OUT/'aircraft-existing-design-recolour-r2.html')
if (OUT/'aircraft-synthesis-r3.html').exists():pages.append(OUT/'aircraft-synthesis-r3.html')
if (OUT/'M14-music-support-r4.html').exists():pages.append(OUT/'M14-music-support-r4.html')
if (OUT/'M14-turnaround-r5.html').exists():pages.append(OUT/'M14-turnaround-r5.html')
if (OUT/'M08-turnaround-r4.html').exists():pages.append(OUT/'M08-turnaround-r4.html')
if (OUT/'M08-turnaround-r5.html').exists():pages.append(OUT/'M08-turnaround-r5.html')
if (OUT/'aircraft-airframe-r6.html').exists():pages.append(OUT/'aircraft-airframe-r6.html')
if (OUT/'confirmed-design-handoff-20261023.html').exists():pages.append(OUT/'confirmed-design-handoff-20261023.html')
if (OUT/'public-works-source-r1.html').exists():pages.append(OUT/'public-works-source-r1.html')
if (OUT/'M06-labor-identity-r2.html').exists():pages.append(OUT/'M06-labor-identity-r2.html')
if (OUT/'M06-turnaround-r3.html').exists():pages.append(OUT/'M06-turnaround-r3.html')
if (OUT/'city-response-source-r2.html').exists():pages.append(OUT/'city-response-source-r2.html')
if (OUT/'city-response-turnaround-r3.html').exists():pages.append(OUT/'city-response-turnaround-r3.html')
if (OUT/'city-response-refinement-r4.html').exists():pages.append(OUT/'city-response-refinement-r4.html')
if (OUT/'crane-mirror-source-r1.html').exists():pages.append(OUT/'crane-mirror-source-r1.html')
for p in pages:
    x=Page();x.feed(p.read_text());parsed[p.resolve()]=x
errors=[];local_links=0
for p in pages:
    x=parsed[p.resolve()]
    dup=[k for k,v in Counter(x.ids).items() if v>1]
    if dup:errors.append((str(p),'duplicate ids',dup))
    for tag,attr,value in x.refs:
        u=urlsplit(value)
        if u.scheme or u.netloc:continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
        if not target.exists():errors.append((str(p),value,'missing local file'));continue
        local_links+=1
        if u.fragment and target.suffix=='.html':
            if target not in parsed:
                y=Page();y.feed(target.read_text());parsed[target]=y
            if unquote(u.fragment) not in parsed[target].ids:errors.append((str(p),value,'missing anchor'))
    if any(not a.get('alt') for a in x.images):errors.append((str(p),'image missing alt'))
    for i,m in enumerate(re.finditer(r'<script(.*?)>(.*?)</script>',p.read_text(),re.S)):
        attrs,body=m.groups()
        if 'application/json' in attrs:
            try:json.loads(body.replace('<\\/','</'))
            except Exception as e:errors.append((str(p),'embedded JSON',str(e)))
        else:
            js=OUT/f'.static-check-{p.stem}-{i}.js';js.write_text(body)
            r=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
            if r.returncode:errors.append((str(p),'JS syntax',r.stderr))
            js.unlink()

manifest=json.loads((OUT/'adoption-manifest.json').read_text())
records=manifest['records'];byid={r['id']:r for r in records}
assert len(records)==298 and len(byid)==298
assert sum(r['changed_image'] for r in records)==43
for r in records:
    f=ROOT/r['image']
    if hashlib.sha256(f.read_bytes()).hexdigest()!=r['sha256']:errors.append((r['id'],'source hash mismatch'))
    if not r['retained'] or not r['internal_next']:errors.append((r['id'],'missing adoption decision'))
    if r['runtime_replaced'] or r['runtime_user_accepted']:errors.append((r['id'],'unwarranted acceptance/runtime flag'))
# Approval follows exact user-selected references, including the 2026-10-17
# H04/H07/H09 R2 identities; it never approves an external card by shared ID.
decisions=json.loads((OUT/'user-art-decisions-20261016.json').read_text())
approvals={r['id']:r for r in decisions['accepted_character_identities'] if r['identity_direction_accepted']}
assert sorted(r['id'] for r in records if r['identity_direction_accepted'])==sorted(approvals)
assert {'H01','H02','H03'}.issubset(approvals)
for ident,approval in approvals.items():
    source=(OUT/approval['current_reference_from_reader']).resolve()
    if hashlib.sha256(source.read_bytes()).hexdigest()!=approval['reference_sha256']:errors.append((ident,'approved identity source changed'))
    if byid[ident]['identity_accepted_reference_sha256']!=approval['reference_sha256']:errors.append((ident,'approval bound to a different drawing'))
    if byid[ident]['identity_acceptance_scope']!=approval['scope']:errors.append((ident,'approval scope changed'))
cards=parsed[pages[0].resolve()].cards
assert len(cards)==298
for c in cards:
    if c['data-verdict']!=byid[c['data-id']]['route']:errors.append((c['data-id'],'filter route mismatch'))
for id in ['M03','S11']:
    assert byid[id]['binding_corrected']
    old=json.loads((OUT/'latest-card-inventory.json').read_text())
    opposite=next(r for r in old if r['id']==('S11' if id=='M03' else 'M03'))
    assert byid[id]['image']==opposite['file']

report={'static_check_pass':not errors,'cards':298,'changed_sources':43,'local_references_checked':local_links,'route_counts':dict(Counter(r['route'] for r in records)),'binding_corrections':['M03','S11'],'javascript_syntax':'checked with node --check; not browser execution','browser_render_verified':False,'browser_reason':'Prior explicit file navigation rejection; no alternative browser/server workaround attempted.','runtime_assets_replaced':False,'runtime_or_all_asset_acceptance':False,'identity_directions_accepted':manifest['identity_directions_accepted_by_user'],'errors':errors}
(OUT/'r4-static-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
raise SystemExit(0 if not errors else 1)
