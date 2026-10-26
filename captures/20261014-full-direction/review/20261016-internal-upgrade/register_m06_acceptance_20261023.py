"""Bind the user's M06 approval to the selected R2 source and A head only."""
from pathlib import Path
import csv, hashlib, json, zipfile

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
CANON=ROOT/'docs/superpowers/specs/data/canon'
RECEIPT='M06-design-fixed-20261023-r2.json'
def read(name): return json.loads((OUT/name).read_text())
def write(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def table(name):
    with (CANON/name).open() as f:
        r=csv.DictReader(f,delimiter='\t'); return r.fieldnames,list(r)
def save_table(name,fields,rows):
    with (CANON/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

record=read('M06-labor-identity-production-r2.json');item=record['items'][0]
assert sha(OUT/item['file'])==item['sha256']
if (OUT/RECEIPT).exists():
    receipt=read(RECEIPT)
    assert receipt['selected_master']['sha256']==item['sha256']
    print(json.dumps({'existing_receipt_preserved':RECEIPT},ensure_ascii=False))
    raise SystemExit(0)
fields,locks=table('character_mecha_art_locks.tsv')
lock_id='CML'+str(max(int(x['lock_id'][3:]) for x in locks if x['lock_id'].startswith('CML') and x['lock_id'][3:].isdigit())+1).zfill(3)
receipt=dict(date='2026-10-23',user_thread='01a13f08-23a0-74c2-b2f5-7913c7e81470',user_verbatim='行就这样',existing_batch='design-followthrough-r1.json',
    subject='M06 预算二号救援机',canon_entity='V353U032',authority_registration=lock_id,
    selected_master={'file':item['file'],'sha256':item['sha256'],'selected_regions':['左侧整机A','右上A头部设计','右下供能背架设计'],'excluded_regions':['B头型备选','C头型备选']},
    scope='采用预算二号R2整体方向与A作业盔头型：黄绿白职业机、双目/护颌、检修舱、防尘套、替换色左腿、救援夹具、卷盘和三制式供能背架。',
    technical_followup=['头部通讯模块的物理侧别在三视中统一，以主形/功能为准，不把现有透视错位锁成规格。','卷盘/线缆/接口/夹具与操纵舱的机构尺寸和连续工作另验。'],
    excluded_acceptance=['B/C头型及B作为A可动附件的机构','新增三视图','同件模型、动作、声音与运行验收','市政吊装机M07本批源稿'],
    source_record='M06-labor-identity-production-r2.json',reader='M06-labor-identity-r2.html',runtime_user_accepted=False,new_handoff_sent=False)
write(RECEIPT,receipt)
row={k:'' for k in fields}
row.update(lock_id=lock_id,subject_id='ART_M06_R2_A_SOURCE_SELECTED_20261023',subject_type='scoped_mecha_source_design',canonical_name='预算二号R2整机与A头型源设计确定',canon_entity_id='V353U032',package_id='PK_CORE_PUBLIC_WORKS',role_type='低费市政维修、救援与供能职业机',unit_or_mecha_link='V353U032',
    visual_lock=receipt['scope']+'主图左手持救援夹具，左腿为青绿替换件。正常成人厚实体态与头壳纵向体积保持；以回执所列图稿、采用区域及SHA为准。',
    current_art_reference=str((OUT/item['file']).relative_to(ROOT)),asset_status='R2_main_and_A_head_source_user_accepted',story_gate='SYSTEM-DESIGN;保持C03当前职业机职责，不推进剧情',
    must_not='不得回流R1圆盔连续眼窗与通用铠甲头型；不得将B/C备选一并视为采用；不得压扁头部、放大头部压短身体；须统一通讯模块侧别；不代签新三视、机构、模型或运行。',
    source_refs=str((OUT/RECEIPT).relative_to(ROOT))+';'+str((OUT/'M06-labor-identity-production-r2.json').relative_to(ROOT)),notes='用户以“行就这样”采用上一回复推荐的整机与A头型。主形/功能固定，已记透视侧别问题在三视工序修正；M07未扩大认可。')
locks.append(row);save_table('character_mecha_art_locks.tsv',fields,locks)
fields,overrides=table('authority_overrides.tsv')
overrides.append(dict(record_type='art_lock',record_id=lock_id,canon_level='working',lifecycle_status='active',version_scope='M06_R2_main_and_A_head_source_user_accepted_20261023',source_of_truth=str((OUT/RECEIPT).relative_to(ROOT)),supersedes='',last_confirmed='2026-10-23',owner='art',notes='仅当前整机/A头型及供能背架设计采用；B/C备选、透视错位、模型/运行不在认可范围。'))
save_table('authority_overrides.tsv',fields,overrides)
item['user_accepted']=True;item['acceptance_scope']=receipt['scope'];item['selected_head']='A'
record.update(status='user_accepted_main_and_A_head_source',source_acceptance_receipt=RECEIPT,source_design_user_accepted=True,authority_scope=receipt['scope'],selected_head='A',canon_changed=True)
for head in record['head_options']: head['user_accepted']=head['id']=='A'
record['limits'][0]='当前整机、A头型及背架外观已采用；B/C仅保留研究，头部透视侧别与机构在后续三视/制作中统一。'
record['experience']['next']='沿已采用A头型与R2整机补同形正侧背，统一通讯侧别；实际工作动作和运行另验。'
record['author_review']['subsequent_user_acceptance']=RECEIPT
write('M06-labor-identity-production-r2.json',record)
ledger=read('design-followthrough-r1.json')
ledger.update(latest_m06_source_acceptance=RECEIPT,latest_source_acceptance=RECEIPT)
ledger['production_focus'].update(current_step='用户以“行就这样”采用预算二号R2整机与A作业盔头型；已绑定源图、采用区域与哈希。',next=record['experience']['next'])
ledger['experience_record_m06_labor_identity_r2'].update(new_images_user_accepted=True,acceptance_receipt=RECEIPT,acceptance_scope=receipt['scope'],next=record['experience']['next'])
defect=next(x for x in ledger['defect_ledger'] if x['id']=='ART-M06-IP-IDENTITY-20261023')
defect.update(closed=True,closure_basis={'observer':'human user','quote':'行就这样','receipt':RECEIPT,'scope':'机设/IP语言与A头型采用'},remaining='头部通讯侧别与机构另在三视/制作工序修正；不扩大为运行认可。')
write('design-followthrough-r1.json',ledger)
status=ROOT/'docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md'
entry='- 2026-10-23用户以“行就这样”采用预算二号R2整机与A作业盔头型。'+lock_id+'绑定指定源图、区域与SHA；检修躯体、替换件及卷盘/三制式供能背架外观确定，B/C备选不一并采用。头部通讯模块透视侧别在后续三视统一，机构/模型/运行分别检查。来源：captures/20261014-full-direction/review/20261016-internal-upgrade/'+RECEIPT+'。\n\n'
text=status.read_text();status.write_text(text.replace('## 一、当前结论\n\n','## 一、当前结论\n\n'+entry,1))
reader=OUT/'M06-labor-identity-r2.html';s=reader.read_text()
s=s.replace('A为整机使用的研究头型；B为焊接护罩方向，C为救援传感器方向。尚未固定新头型或整机。','用户已采用本轮整机与A作业盔头型。B/C保留为未采用研究；通讯模块的透视侧别在后续同头三视中统一。')
s=s.replace('具体护盔、接口外形与夹具是本轮候选。','整机、A护盔、接口外观与夹具设计已采用。')
s=s.replace('新设计待采用，同模型多视、连续作业、声音与运行另验。','新设计已采用，同模型多视、连续作业、声音与运行另验。')
s=s.replace('</nav>','</nav><p class="scope" id="accepted-20261023">已确定：R2整机与A头型。<a href="'+RECEIPT+'">采用范围与后续三视修正项</a></p>',1)
reader.write_text(s)
verification=read('M06-labor-identity-verification-r2.json')
verification.update(M06_user_accepted=True,acceptance_scope=receipt['scope'],receipt=RECEIPT)
write('M06-labor-identity-verification-r2.json',verification)
manifest=read('M06-labor-identity-delivery-manifest-r2.json')
payload=list(dict.fromkeys([x['file'] for x in manifest['files']]+[RECEIPT]))
manifest.update(files=[dict(file=f,sha256=sha(OUT/f)) for f in payload],user_accepted=True,acceptance_scope=receipt['scope'],source_acceptance_receipt=RECEIPT)
write('M06-labor-identity-delivery-manifest-r2.json',manifest)
with zipfile.ZipFile(OUT/'M06-labor-identity-source-20261023-r2.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in payload+['M06-labor-identity-delivery-manifest-r2.json']: z.write(OUT/f,f)
with zipfile.ZipFile(OUT/'M06-labor-identity-source-20261023-r2.zip') as z:
    assert z.testzip() is None
    for x in manifest['files']: assert hashlib.sha256(z.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps(dict(receipt=RECEIPT,authority=lock_id,selected_head='A',source_sha256=item['sha256']),ensure_ascii=False))
