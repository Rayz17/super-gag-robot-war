"""Bind the user's R6 source-design acceptance and preserve downstream boundaries."""
from pathlib import Path
import csv, hashlib, json, zipfile

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
CANON=ROOT/'docs/superpowers/specs/data/canon'
RECEIPT='aircraft-design-fixed-20261023-r6.json'
QUOTE='好的，已确定的设计可以交付给主对话，然后进行下一批'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tsv_read(n):
    with (CANON/n).open(newline='') as f:
        reader=csv.DictReader(f,delimiter='\t');return reader.fieldnames,list(reader)
def tsv_write(n,fields,rows):
    with (CANON/n).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(rows)
if (OUT/RECEIPT).exists():raise SystemExit('Acceptance already registered; preserve receipt and continue handoff.')
r=read('aircraft-airframe-production-r6.json')
files=[]
for machine in r['items']:
    for item in machine['views']:
        assert sha(OUT/item['file'])==item['sha256']
        files.append(dict(asset=machine['id'],name=machine['name'],view=item['id'],file=item['file'],sha256=item['sha256'],scope='R6_current_source_design',source_design_fixed=True,user_accepted=True))
fields,locks=tsv_read('character_mecha_art_locks.tsv')
numeric=[int(x['lock_id'][3:]) for x in locks if x['lock_id'].startswith('CML') and x['lock_id'][3:].isdigit()]
start=max(numeric)+1
allocated={'M08':f'CML{start}','M14':f'CML{start+1}'}
receipt=dict(date='2026-10-23',revision='aircraft-source-acceptance-r6',authority='direct_user_message_in_this_chat',verbatim=QUOTE,existing_batch='design-followthrough-r1.json',scope='当前R6雷翎/歌翼正侧背6张源设计确定，可交付主对话；不扩大为模型、完整变形、声音或运行验收。',reader='aircraft-airframe-r6.html',files=files,authority_registration=allocated,prior_source_identity_preserved=['CML132','CML133','CML135','CML136','CML139','CML140'],excluded_history=['M08_R4_stocky_proportions','M08_R5_overthin_proportions','R6_failed_three_quarter_side_attempt'],handoff_authorized=True,next_batch_authorized=True,runtime_user_accepted=False,full_transformation_verified=False,dispatch_record='交接发送记录-20261016.json')
write(RECEIPT,receipt)
for ident,name,entity,package,visual in [
    ('M08','雷翎','V353U047','PK_GUEST_FIRESEED','R6当前正侧背：体态按歌翼实际比例，适中肩胸与四肢厚度；对称V形侧天线、蓝红额部、琥珀座舱、蓝白红四刃翼与右手长枪；以原图及哈希为准，不回流R4敦实或R5过细长比例。'),
    ('M14','歌翼','','R04','R6当前正侧背：保持原歌翼体态、双红侧天线、琥珀座舱和前向展开双声翼；明确圆角肩进气框、连续蒙皮/腿部机舱，减少装饰切面。声翼正面每侧一大一小扬声器，背面为红白外壳。')
]:
    row={k:'' for k in fields};row.update(lock_id=allocated[ident],subject_id=f'ART_{ident}_R6_SOURCE_SELECTED_20261023',subject_type='scoped_mecha_source_design',canonical_name=f'{name}R6当前三视源设计确定',canon_entity_id=entity,package_id=package,role_type='航空机源设计',unit_or_mecha_link=entity or '歌翼可变机',visual_lock=visual,current_art_reference=str((OUT/'aircraft-airframe-r6.html').relative_to(ROOT))+'#'+ident,asset_status='R6_current_source_views_user_accepted',story_gate='SYSTEM-DESIGN;不推进剧情',must_not='不得将源稿采用扩大为同件模型、完整变形、声音或运行验收；新派生不得压扁头部或擅改主形。',source_refs=str((OUT/RECEIPT).relative_to(ROOT))+';'+str((OUT/'aircraft-airframe-production-r6.json').relative_to(ROOT)),notes='用户明确确定设计、授权交付主对话与下一批；逐文件SHA绑定。')
    locks.append(row)
song=next(x for x in locks if x['lock_id']=='CML023')
song.update(current_art_reference=str((OUT/'aircraft-airframe-r6.html').relative_to(ROOT))+'#M14',asset_status='songwing_R6_current_source_views_user_accepted')
song['visual_lock']+='；2026-10-23用户确定R6当前正侧背，保留上述主形与比例，采用圆角肩进气框、连续蒙皮与腿部机舱的航空结构线。'
song['source_refs']+=';'+str((OUT/RECEIPT).relative_to(ROOT))
song['notes']+='；R4保留身份/音乐功能母稿，R6为当前三视表面来源；模型/运行另验。'
next(x for x in locks if x['lock_id']=='CML140')['notes']+='；2026-10-23 R6当前三视另见'+allocated['M14']+'，原R4保留身份/功能父源。'
tsv_write('character_mecha_art_locks.tsv',fields,locks)
fields,overrides=tsv_read('authority_overrides.tsv')
for ident in allocated:
    overrides.append(dict(record_type='art_lock',record_id=allocated[ident],canon_level='working',lifecycle_status='active',version_scope=f'{ident}_R6_source_views_user_accepted_20261023',source_of_truth=str((OUT/RECEIPT).relative_to(ROOT)),supersedes='',last_confirmed='2026-10-23',owner='art',notes='用户确定当前R6源设计及交付，逐SHA绑定；模型/完整变形/运行另验。'))
o=next(x for x in overrides if x['record_type']=='art_lock' and x['record_id']=='CML023');o.update(version_scope='R04_songwing_R6_source_views_current_20261023',source_of_truth=str((OUT/RECEIPT).relative_to(ROOT)),last_confirmed='2026-10-23',notes='歌翼R6当前三视源设计已确定；R4保留身份/音乐父源，不迁移人物、剧情或运行。')
tsv_write('authority_overrides.tsv',fields,overrides)
for machine in r['items']:
    machine['new_images_user_accepted']=True
    for item in machine['views']:item['user_accepted']=True
    machine['front']=machine['views'][0]
r.update(status='user_accepted_source_designs_fixed',source_acceptance_receipt=RECEIPT,source_design_user_accepted=True,authority_scope=receipt['scope'])
write('aircraft-airframe-production-r6.json',r)
ledger=read('design-followthrough-r1.json');ledger.update(latest_aircraft_source_acceptance=RECEIPT,latest_source_acceptance=RECEIPT);ledger['production_focus'].update(current_step='R6六张当前源设计已由用户确定，正在集中整理已确认源稿并交付主对话。',next='完成交付后接M06预算二号与M07市政吊装机源设计。');write('design-followthrough-r1.json',ledger)
status=ROOT/'docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md'
status.write_text(status.read_text()+'\n\n## 2026-10-23 雷翎/歌翼R6源设计确定与美术交付\n\n用户明确“'+QUOTE+'”。'+allocated['M08']+'/'+allocated['M14']+'以逐文件SHA固定当前六张三视源设计；CML023当前参考更新至歌翼R6，CML140的R4身份/音乐父源保留。只迁移本批美术来源与交付授权，不迁移人物、剧情、完整变形或运行验收。接续`design-followthrough-r1.json`；下一批为原清单M06/M07市政职业机源设计。\n')
reader=OUT/'aircraft-airframe-r6.html';s=reader.read_text();notice='<aside id="source-accepted-20261023" class="scope">用户已确定本批六张源设计，当前稿可交付主对话继续制作。<a href="aircraft-design-fixed-20261023-r6.json">采用清单与范围</a></aside>';reader.write_text(s.replace('</nav>','</nav>'+notice,1))
manifest=read('aircraft-airframe-delivery-manifest-r6.json');payload=[x['file'] for x in manifest['files']]+[RECEIPT];manifest['files']=[dict(file=f,sha256=sha(OUT/f)) for f in dict.fromkeys(payload)];manifest['source_acceptance_receipt']=RECEIPT;write('aircraft-airframe-delivery-manifest-r6.json',manifest)
with zipfile.ZipFile(OUT/'aircraft-airframe-source-20261023-r6.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in list(dict.fromkeys(payload))+['aircraft-airframe-delivery-manifest-r6.json']:z.write(OUT/f,arcname=f)
print(json.dumps(dict(receipt=RECEIPT,registered=allocated,current_source_files=len(files)),ensure_ascii=False))
