"""Extend CML143 to the exact three source views accepted by the user."""
from pathlib import Path
import csv,hashlib,json,zipfile

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
CANON=ROOT/'docs/superpowers/specs/data/canon'
RECEIPT='M06-turnaround-design-fixed-20261023-r3.json'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(n):
    with (CANON/n).open() as f:r=csv.DictReader(f,delimiter='\t');return r.fieldnames,list(r)
def save(n,fields,rows):
    with (CANON/n).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

record=read('M06-turnaround-production-r3.json')
for item in record['items']:assert sha(OUT/item['file'])==item['sha256']
if (OUT/RECEIPT).exists():
    old=read(RECEIPT)
    assert [(x['file'],x['sha256']) for x in old['files']]==[(x['file'],x['sha256']) for x in record['items']]
    print('M06 accepted three-view receipt preserved');raise SystemExit(0)
receipt=dict(date='2026-10-23',user_thread='01a13f08-23a0-74c2-b2f5-7913c7e81470',user_verbatim='没问题，下一批',existing_batch='design-followthrough-r1.json',subject='M06 预算二号当前正侧背三视',authority_registration='CML143',
    parent_acceptance='M06-design-fixed-20261023-r2.json',source_record='M06-turnaround-production-r3.json',reader=record['reader'],
    files=[{k:x[k] for k in ['id','label','file','sha256']} for x in record['items']],
    scope='采用本轮指定正面R3、左侧面R3c和背面R3源设计，保持R2整机/A头型；右耳通讯、左替换小腿、左手救援夹具及卷盘/三接口背架以指定图稿为当前来源。',
    next_batch_authorized=True,next_batch=['M09灰崎警备劳务机','M10消防架桥机'],excluded=['早期斜侧R3与投影未修侧面R3b','B/C头型','市政吊装机本批未完成多视','同件模型、完整机构、连续工作动作、声音或运行验收'],runtime_user_accepted=False,new_handoff_sent=False)
write(RECEIPT,receipt)
fields,rows=table('character_mecha_art_locks.tsv');row=next(x for x in rows if x['lock_id']=='CML143')
row.update(canonical_name='预算二号R3当前正侧背源设计确定',current_art_reference=str((OUT/record['reader']).relative_to(ROOT)),asset_status='R3_current_front_side_rear_source_designs_user_accepted')
row['visual_lock']+='；2026-10-23用户采用R3正面、R3c左侧面与R3背面：右耳通讯模块、左小腿替换件、左手夹具、右腰工具箱/左腰耦合器及卷盘三接口按当前三视对应。'
row['must_not']=row['must_not'].replace('须统一通讯模块侧别；不代签新三视、机构、模型或运行。','后续派生须保持当前通讯模块侧别；不代签新增图、机构、模型或运行。')
row['source_refs']+=';'+str((OUT/RECEIPT).relative_to(ROOT))+';'+str((OUT/'M06-turnaround-production-r3.json').relative_to(ROOT))
row['notes']+='；当前R3三视已由用户以“没问题，下一批”采用，旧斜侧不回流；下一批M09/M10，M07未扩大认可。'
save('character_mecha_art_locks.tsv',fields,rows)
fields,rows=table('authority_overrides.tsv');row=next(x for x in rows if x['record_type']=='art_lock' and x['record_id']=='CML143')
row.update(version_scope='M06_R3_current_source_views_user_accepted_20261023',source_of_truth=str((OUT/RECEIPT).relative_to(ROOT)),last_confirmed='2026-10-23',notes='当前正R3/侧R3c/背R3三张源图用户采用，R2/A主形保持；模型/机构/运行另验。')
save('authority_overrides.tsv',fields,rows)
for item in record['items']:item.update(user_accepted=True,user_acceptance_receipt=RECEIPT)
record.update(new_images_user_accepted=True,source_design_user_accepted=True,status='current_source_views_user_accepted',parent_source_acceptance_receipt='M06-design-fixed-20261023-r2.json',source_acceptance_receipt=RECEIPT,canon_changed=True)
record['limits'][1]='当前指定三张源图已获用户采用；不扩大为同件模型、机构、连续工作或运行验收。'
write('M06-turnaround-production-r3.json',record)
ledger=read('design-followthrough-r1.json');ledger.update(latest_m06_turnaround_acceptance=RECEIPT,latest_source_acceptance=RECEIPT)
ledger['experience_record_m06_turnaround_r3'].update(new_images_user_accepted=True,acceptance_receipt=RECEIPT,acceptance_scope=receipt['scope'])
defect=next(x for x in ledger['defect_ledger'] if x['id']=='ART-M06-SIDE-PROJECTION-R3')
defect.update(closed=True,closure_basis={'observer':'human user','quote':'没问题，下一批','receipt':RECEIPT,'scope':'当前三视源图采用，不代签模型投影或机构'})
focus=ledger['production_focus'];focus['source_basis']=[x for x in focus['source_basis'] if x!='TERM_C01E02_FIRE_BRIDGE_FULL_MAP_PACKAGE']
focus['source_basis'] += ['docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C01-闭馆以后万机出击.md#消防架桥机','docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C03-章节连续阅读稿.md#灰崎/消防机']
write('design-followthrough-r1.json',ledger)
status=ROOT/'docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md';s=status.read_text()
entry='- 2026-10-23用户以“没问题，下一批”采用预算二号当前正R3、侧R3c和背R3三张源图。CML143当前参考转至本轮三视，R2/A主形父源保持；早期斜侧、B/C备选、模型/机构/运行不扩大认可。下一批接M09/M10职业机源设计。来源：captures/20261014-full-direction/review/20261016-internal-upgrade/'+RECEIPT+'。\n\n'
status.write_text(s.replace('## 一、当前结论\n\n','## 一、当前结论\n\n'+entry,1))
page=OUT/record['reader'];s=page.read_text();s=s.replace('</nav>','</nav><p class="scope" id="accepted-r3-20261023">当前三视已由用户采用。<a href="'+RECEIPT+'">具体文件与范围</a></p>',1);page.write_text(s)
manifest=read('M06-turnaround-delivery-manifest-r3.json');files=list(dict.fromkeys([x['file'] for x in manifest['files']]+[RECEIPT]))
manifest.update(files=[dict(file=f,sha256=sha(OUT/f)) for f in files],new_images_user_accepted=True,source_acceptance_receipt=RECEIPT)
write('M06-turnaround-delivery-manifest-r3.json',manifest)
with zipfile.ZipFile(OUT/'M06-turnaround-source-20261023-r3.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files+['M06-turnaround-delivery-manifest-r3.json']:z.write(OUT/f,f)
with zipfile.ZipFile(OUT/'M06-turnaround-source-20261023-r3.zip') as z:
    assert z.testzip() is None
    for x in manifest['files']:assert hashlib.sha256(z.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps({'receipt':RECEIPT,'source_views':len(receipt['files']),'authority':'CML143'},ensure_ascii=False))
