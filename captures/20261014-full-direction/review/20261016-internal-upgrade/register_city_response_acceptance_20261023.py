"""Bind the user's adoption to the exact M09/M10 R2 masters, then continue views."""
from pathlib import Path
import csv,hashlib,json,zipfile

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
CANON=ROOT/'docs/superpowers/specs/data/canon'
RECEIPT='city-response-design-fixed-20261023-r2.json'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(n):
    with (CANON/n).open() as f:
        r=csv.DictReader(f,delimiter='\t');return r.fieldnames,list(r)
def save(n,fields,rows):
    with (CANON/n).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

source=read('city-response-source-production-r2.json')
for item in source['items']:assert sha(OUT/item['file'])==item['sha256']
if (OUT/RECEIPT).exists():
    old=read(RECEIPT)
    for item in old['files']:assert sha(OUT/item['file'])==item['sha256']
    print(json.dumps({'existing_receipt_preserved':RECEIPT},ensure_ascii=False));raise SystemExit(0)
fields,locks=table('character_mecha_art_locks.tsv')
number=max(int(x['lock_id'][3:]) for x in locks if x['lock_id'].startswith('CML') and x['lock_id'][3:].isdigit())
scopes={
 'M09':'采用灰崎R2源板：当前巡逻盔头型、灰白/蓝灰/红反光标记、成人身形与连续曲面外壳；六面平板交通墙，手持一面、背负五面。',
 'M10':'采用消防架桥机R2源板：橙白双足工程人形与消防架桥载具，驾驶室胸、六轮组、成对折叠桥板、消防水路；四稳定腿用于车辆作业支撑。'
}
files=[]
for index,item in enumerate(source['items'],1):
    lock_id=f'CML{number+index:03d}'
    file={k:item[k] for k in ['id','name','file','sha256','canon_entity']}
    file.update(authority_registration=lock_id,scope=scopes[item['id']]);files.append(file)
    row={k:'' for k in fields}
    row.update(lock_id=lock_id,subject_id=f"ART_{item['id']}_R2_SOURCE_SELECTED_20261023",subject_type='scoped_mecha_source_design',canonical_name=item['name']+'R2整机源设计确定',canon_entity_id=item['canon_entity'],package_id='PK_CORE_PUBLIC_WORKS',role_type=item['role'],unit_or_mecha_link=item['canon_entity'],visual_lock=scopes[item['id']]+'以回执指定源图与SHA为准，派生保持头壳纵向体积和当前身形。',current_art_reference=str((OUT/item['file']).relative_to(ROOT)),asset_status='R2_source_design_user_accepted',story_gate='SYSTEM-DESIGN;保持当前市政职业职责，不推进剧情',must_not='不得回流被否定四足主形或旧碎面壳体；不得压扁头部、放大头部压短身体；不把新增三视、变形机构、模型或运行自动视为采用。',source_refs=str((OUT/RECEIPT).relative_to(ROOT))+';'+str((OUT/'city-response-source-production-r2.json').relative_to(ROOT)),notes='用户“可以，出三视图”采用当前两张R2父源并要求直接制作；新派生图单独交付，不要求再次确认父源。')
    locks.append(row)
save('character_mecha_art_locks.tsv',fields,locks)
fields,overrides=table('authority_overrides.tsv')
for item in files:
    overrides.append(dict(record_type='art_lock',record_id=item['authority_registration'],canon_level='working',lifecycle_status='active',version_scope=item['id']+'_R2_source_user_accepted_20261023',source_of_truth=str((OUT/RECEIPT).relative_to(ROOT)),supersedes='',last_confirmed='2026-10-23',owner='art',notes='仅当前R2父源外观采用；新派生三视、机构/模型/运行分别检查。'))
save('authority_overrides.tsv',fields,overrides)
receipt=dict(date='2026-10-23',user_thread='01a13f08-23a0-74c2-b2f5-7913c7e81470',user_verbatim='可以，出三视图',existing_batch='design-followthrough-r1.json',source_record='city-response-source-production-r2.json',files=files,scope='当前M09/M10两张R2整机源设计采用，并直接授权制作两机正侧背。',excluded_acceptance=['新派生三视图','被否定M10四足主形与旧M09碎面躯体','同件变形机构、模型、动作、声音或运行','M07未交付多视'],runtime_user_accepted=False,handoff_sent=False)
write(RECEIPT,receipt)
for item in source['items']:item.update(user_accepted=True,acceptance_scope=scopes[item['id']],source_acceptance_receipt=RECEIPT)
source.update(status='R2_masters_user_accepted_turnarounds_authorized',source_design_user_accepted=True,source_acceptance_receipt=RECEIPT,canon_changed=True)
source['limits'][0]='两张当前R2父源由用户“可以，出三视图”采用；新增正侧背另作派生源图交付。'
source['experience']['next']='直接绘制两机同形正侧背；按实际图核对头身比、交通墙数量/侧别、消防轮组/桥板/水路。'
write('city-response-source-production-r2.json',source)
ledger=read('design-followthrough-r1.json')
ledger.update(latest_source_acceptance=RECEIPT,latest_city_response_source_acceptance=RECEIPT)
ledger['production_focus'].update(experience='玩家能从市政职业机外观分辨灰崎的封路/隔离与消防机的车辆稳定支撑/铺桥/降温职责。',current_step='当前两张R2整机由用户采用；正面比例和部件核对进行中，接续正侧背制作。',next=source['experience']['next'])
ledger['experience_record_city_response_r2'].update(new_images_user_accepted=True,acceptance_receipt=RECEIPT,acceptance_scope=receipt['scope'],next=source['experience']['next'])
for defect in ledger['defect_ledger']:
    if defect['id'] in ['ART-M09-CURVED-SURFACES-20261023','ART-M10-QUAD-MAIN-SILHOUETTE-20261023']:
        defect.update(closed=True,closure_basis={'observer':'human user','quote':'可以，出三视图','receipt':RECEIPT,'scope':'当前R2整机源设计采用'},remaining='同形三视继续制作，隐面机构与模型/运行分别验证。')
write('design-followthrough-r1.json',ledger)
review=read(source['author_review']);review['subsequent_user_acceptance']=RECEIPT;write(source['author_review'],review)
verification=read('city-response-verification-r2.json');verification.update(new_images_user_accepted=True,receipt=RECEIPT,acceptance_scope=receipt['scope']);write('city-response-verification-r2.json',verification)
reader=OUT/'city-response-source-r2.html';html=reader.read_text()
html=html.replace('</nav>','</nav><p class="scope">当前两张R2源板已由用户采用。正在直接制作正、侧、背源图。<a href="'+RECEIPT+'">采用范围</a></p>',1)
html=html.replace('当前是新源板；具体新图与变形/承重机构、模型、动作和运行分别判断。采用方向后直接补三视。','当前两张R2源板已采用；新派生三视与变形/承重机构、模型、动作和运行分别判断。')
reader.write_text(html)
status=ROOT/'docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md'
entry='- 2026-10-23用户以“可以，出三视图”采用灰崎曲面职业机与消防双足工程变形机两张R2父源，'+','.join(x['authority_registration'] for x in files)+'按指定文件和SHA登记；直接接续两机正侧背。六墙、轮组/桥板/稳定支腿在派生中逐图核对，机构/模型/运行分开检查。来源：'+str((OUT/RECEIPT).relative_to(ROOT))+'。\n\n'
status.write_text(status.read_text().replace('## 一、当前结论\n\n','## 一、当前结论\n\n'+entry,1))
manifest=read('city-response-delivery-manifest-r2.json')
payload=list(dict.fromkeys([x['file'] for x in manifest['files']]+[RECEIPT]))
manifest.update(files=[dict(file=f,sha256=sha(OUT/f)) for f in payload],new_images_user_accepted=True,source_acceptance_receipt=RECEIPT)
write('city-response-delivery-manifest-r2.json',manifest)
with zipfile.ZipFile(OUT/'city-response-source-20261023-r2.zip','w',zipfile.ZIP_DEFLATED) as z:
    for file in payload+['city-response-delivery-manifest-r2.json']:z.write(OUT/file,file)
print(json.dumps({'receipt':RECEIPT,'locks':[x['authority_registration'] for x in files]},ensure_ascii=False))
