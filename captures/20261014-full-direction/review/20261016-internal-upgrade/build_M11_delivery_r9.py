"""Publish the approved M11 master and its corrected source turnarounds."""
from pathlib import Path
from PIL import Image
import csv, hashlib, html, json, re, zipfile
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
BASE=OUT.relative_to(PROJECT).as_posix()+'/'
DATE='2026-10-22'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
master='samples/M11-posture-r8.png'
acceptance='M11-design-fixed-20261022.json'
record='M11-turnaround-delivery-production-r9.json'
reader='M11-source-delivery-r9.html'
native={
 'FRONT':('M11-front-r9.png','exec-68c6b2e4-a55c-4839-aee2-bd20d651756b.png'),
 'SIDE':('M11-side-r9.png','exec-6dc764f3-ef58-4892-a677-28e9b2585f80.png'),
 'REAR':('M11-rear-r9.png','exec-9dc1108b-929e-4b71-a6aa-33fa9f138d40.png')}
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
items=[]
for ident,(name,gen) in native.items():
 f='samples/'+name
 assert sha(OUT/f)==sha(GEN/gen)
 with Image.open(OUT/f) as im:size=list(im.size);mode=im.mode
 items.append(dict(id=ident,file=f,sha256=sha(OUT/f),pixel_size=size,mode=mode,
     generated_source=str(GEN/gen),prompts=['M11-'+ident.lower()+'-prompt-r9.txt'],
     role={'FRONT':'正面：露出装甲颈部、降低肩线与胸甲上沿','SIDE':'左侧：肩颈与R8一致，恢复原背架厚度','REAR':'背面：露出颈后支架，纵向象牙白货台背架'}[ident],
     derived_from_approved_master=True, user_accepted=False, source_delivery_authorized=True,
     runtime_integrated=False,handoff_sent=False))
receipt=dict(date=DATE,revision='M11-design-fixed-20261022',
 authority='direct_user_message',verbatim='货柜领袖就确定这个形象吧，三视图修正后可以交付然后开始下一批',
 existing_batch='design-followthrough-r1.json',
 selected_master=dict(file=master,sha256=sha(OUT/master),user_accepted=True,
     generated_source=str(GEN/'exec-f415d834-8d6c-408a-a1ef-4234fda981f8.png')),
 selected_head_receipt='M11-head-selected-and-turnaround-r6.json',
 acceptance_scope='确定R8货柜领袖整体形象：正常纵向头壳、双耳侧钝头天线、前凸颏甲、露颈沉肩、厚重白蓝橙车壳、长腿及折叠货台背架。',
 authorized_work=['据R8修正人形正侧背并整理交付','交付后接续下一批源设计'],
 corrected_turnarounds=[dict(file=x['file'],sha256=x['sha256'],status='authorized_derived_source_delivery',individual_new_image_user_accepted=False) for x in items],
 runtime_user_accepted=False, full_transformation_verified=False,handoff_sent=False)
write(acceptance,receipt)
previous=read('M11-turnaround-structure-production-r7.json')
review=dict(reviewer='author',independent_review=False,actual_media=[master]+[x['file'] for x in items],
 observed=['三视均露出短实颈部，肩顶降低；正面不再把颏甲压在胸窗边缘。',
           '保留高头壳、额相机、双侧白色钝头天线、分片面甲与前凸颏甲。',
           '长大腿/小腿及厚实足掌保持；没有压短身体或增加轮位。',
           '侧面保留R8矩形背架厚度，背面改为象牙白纵向三片货台及四角橙锁。',
           '每侧肩1、前臂1、小腿2轮位，背面仅主要露胎缘。'],
 limits=['独立绘制三视仍有轻微投影/板缝差异，不等于同模型严格正交。',
         '形象母稿获用户明确采用；三张修正稿按授权交付，没有代签逐图新验收。',
         '沿用R7车形/结构参考，未以旧草模证明R8肩颈展开行程、整机碰撞或受力。'])
production=dict(date=DATE,revision='M11-turnaround-delivery-production-r9',
 asset='货柜领袖形象确定与肩颈修正三视交付',canon_entity='V353U043',
 existing_batch='design-followthrough-r1.json',reader=reader,direction_record=acceptance,
 generation_mode='built-in image_gen',items=items,
 approved_master=receipt['selected_master'],user_acceptance_receipt=acceptance,
 selected_head_reference=previous['selected_head_reference'],
 body_context=previous['body_context'],vehicle_context=previous['vehicle_context'],
 layout_study={**previous['layout_study'],'applicability':'prior_R7_envelope_only_not_R8_neck_stroke_or_shoulder_clearance'},
 previous_production='M11-posture-production-r8.json',prompt_index='M11-turnaround-prompts-r9.json',
 author_review=review,source_delivery_ready=True,new_images_user_accepted=False,
 runtime_changed=False,handoff_sent=False,delivery_zip='M11-source-delivery-20261022-r9.zip')
write(record,production)
write('M11-turnaround-prompts-r9.json',dict(generation_mode='built_in_image_gen',
 selected_master=receipt['selected_master'],outputs=[dict(file=x['file'],prompts=x['prompts']) for x in items],
 inputs=dict(primary_design_master=master,view_guides=['samples/M11-front-r7b.png','samples/M11-side-r7c.png','samples/M11-rear-r7.png'],
 head_reference='samples/M11-selected-head-r6.png')))
figs=''.join('<figure><a href="{0}"><img src="{0}" alt="{1}"></a><figcaption>{1}</figcaption></figure>'.format(x['file'],x['role']) for x in items)
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>货柜领袖｜确定形象与修正三视交付</title><style>body{{margin:0;background:#edf0ed;color:#183142;font:16px/1.7 system-ui}}main{{max-width:1560px;margin:auto;padding:26px}}a{{color:#08617e}}nav{{display:flex;gap:24px;flex-wrap:wrap}}h1{{font-size:36px}}.views{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}figure{{margin:16px 0;background:white}}img{{display:block;width:100%;height:auto}}figcaption{{padding:12px;font-size:14px}}.master{{max-width:620px}}details{{margin:28px 0}}@media(max-width:760px){{.views{{grid-template-columns:1fr}}}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="M11-source-delivery-20261022-r9.zip">下载交付包</a><a href="M11-turnaround-prompts-r9.json">内置生图提示词组</a></nav><h1>货柜领袖：形象确定，三视修正交付</h1><p>沿用户确定的R8形象保持露颈沉肩、原头型、勇者颏甲、长腿和厚重车壳。正、侧、背统一肩颈关系与货台背架；货柜领袖本轮源设计可交付。</p><div class="views">{figs}</div><details><summary>已确定的R8形象母稿</summary><figure class="master"><img src="{master}" alt="用户确定的R8货柜领袖形象"><figcaption>用户2026-10-22明确确定；后续派生沿此稿。</figcaption></figure></details><details><summary>车形、头部与结构参考</summary><p>保留此前车形三视与原头部参考；头仓和底盘结构仍是有限范围研究，不是完整变形工程交付。</p><a href="samples/M11-vehicle-views-r7.png">车形三视参考</a> · <a href="samples/M11-selected-head-r6.png">指定头部源稿</a> · <a href="M11-turnaround-structure-r7.html#structure">此前结构研究</a></details><p><a href="{acceptance}">用户形象确认及授权范围</a> · <a href="{record}">源稿清单与作者核对</a></p><p>三视为源设计绘制稿；模型、连续变形与运行另行验证。</p></main></body></html>'''
(OUT/reader).write_text(page)
notes='''# 货柜领袖源设计交付 · 2026-10-22

当前形象：用户已确定的M11-posture-r8.png。三视按该形象修正肩颈、胸甲上沿与背架，使用front/side/rear-r9三张。头像沿selected-head-r6设计；颏甲以当前整机为准。

白蓝橙、连续单片胸窗、双耳侧钝头天线、前凸颏甲、长腿和折叠货台背架保持。每侧四轮位：肩后1、前臂外后1、小腿外后2；轮轴为左右向。独立货柜先卸下，不穿到背上。

当前母稿、修正三视与提示词位于本包。车形及旧结构仅作支持参考；本包不包含可编辑三维模型、绑定、动画、PSD分层或游戏运行替换。三视是独立绘制源稿，局部投影/板缝尚不等于精密同模正交。

形象母稿已获用户认可，三视是据此完成的授权交付；本记录不代签新增逐图或模型/运行验收。
'''
(OUT/'M11-delivery-notes-r9.md').write_text(notes)
filemap={master:'master/M11-approved-master-r8.png',
 'samples/M11-selected-head-r6.png':'references/M11-selected-head-r6.png',
 'samples/M11-vehicle-views-r7.png':'references/M11-vehicle-views-r7.png',
 acceptance:acceptance,record:record,'M11-turnaround-prompts-r9.json':'prompts/index.json',
 'M11-delivery-notes-r9.md':'README.md'}
for x in items:filemap[x['file']]='turnaround/'+Path(x['file']).name
for ident in native:filemap['M11-'+ident.lower()+'-prompt-r9.txt']='prompts/'+ident.lower()+'.txt'
package_files=[dict(file=k,archive_path=v,sha256=sha(OUT/k)) for k,v in filemap.items()]
write('M11-delivery-manifest-r9.json',dict(date=DATE,files=package_files,master_user_accepted=True,
    source_delivered=True,runtime_delivered=False))
with zipfile.ZipFile(OUT/production['delivery_zip'],'w',zipfile.ZIP_DEFLATED) as z:
 for src,dst in filemap.items():z.write(OUT/src,dst)
 z.write(OUT/'M11-delivery-manifest-r9.json','manifest.json')
with zipfile.ZipFile(OUT/production['delivery_zip']) as z:assert z.testzip() is None

ledger=read('design-followthrough-r1.json')
ledger['latest_m11_cargo']=record
ledger['latest_m11_user_feedback']=acceptance
ledger['latest_m11_source_delivery']=dict(record=record,manifest='M11-delivery-manifest-r9.json',
    zip=production['delivery_zip'],reader=reader,source_delivered=True,master_user_accepted=True,runtime_delivered=False)
ledger['experience_record_m11_turnaround_r9']=dict(classification='experience',parent_batch='design-followthrough-r1.json',
    original_request=receipt['verbatim'],source=acceptance,
    start='用户确定R8形象，要求修正三视后交付。',
    input='以R8为形象母稿，旧三视仅作视角向导，分别重绘正侧背。',
    visible_result='颈部露出/肩线下降、背架纵向三片、轮位与长腿可对照。',
    author_review=record+'#author_review',independent_review=False,
    source_delivery='M11-delivery-manifest-r9.json',runtime_changed=False,
    next='接续原清单航空可变机源设计；模型与连续变形留原结构待办。')
for d in ledger['defect_ledger']:
 if d.get('id')=='ART-M11-NECK-POSTURE-07':
  d['user_selected_master_receipt']=acceptance
  d['current_sources']=[x['file'] for x in items]
  if not any(x.get('evidence')==record for x in d['attempts']):
   d['attempts'].append(dict(files=[x['file'] for x in items],observed=True,
       outcome='author_observed_improvement',result='三视按已确定R8肩颈同步，背架恢复同一体量。',evidence=record))
  d['source_design_resolved']=True;d['closed']=False
  d['remaining']='三维颈部展开行程及肩架/胸甲净空仍属模型工序；源图修正已交付。'
ledger['production_focus']['current_step']='R8形象已由用户确定；R9修正三视已交付源设计包。'
ledger['production_focus']['next']='按原剩余清单开始雷翎/歌翼航空可变机候选设计；不改已确定M11形象。'
write('design-followthrough-r1.json',ledger)
decisions=read('user-art-decisions-20261016.json')
decisions['latest_M11_direction'].update(date=DATE,record=acceptance,current_reader=reader,
    approved_master=master,whole_body_master_user_accepted=True,
    corrected_turnaround_source_record=record,source_delivered=True,
    individual_new_turnaround_images_user_accepted=False)
decisions['current_next_mecha_batch'].update(current_M11_reader=reader,
    M11_master_user_accepted=True,M11_source_delivery='M11-delivery-manifest-r9.json',
    next_source_batch='雷翎与歌翼航空可变机同源双形态候选')
write('user-art-decisions-20261016.json',decisions)
author=read('sample-author-review.json');author['latest_M11_source_record']=record
write('sample-author-review.json',author)

# Register exact body source separately from newly drawn turnarounds.
def load_tsv(p):
 with p.open() as h:r=csv.DictReader(h,delimiter='\t');return r.fieldnames,list(r)
def save_tsv(p,fields,rows):
 with p.open('w') as h:w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
p=PROJECT/'docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv'
fields,rows=load_tsv(p);subject='ART_M11_WHOLE_BODY_SELECTED_20261022'
selected=next((x for x in rows if x['subject_id']==subject),None)
if selected is None:
 lock='CML'+str(max(int(x['lock_id'][3:]) for x in rows if re.fullmatch(r'CML[0-9]+',x['lock_id']))+1)
 selected={k:'' for k in fields};rows.append(selected)
else:lock=selected['lock_id']
selected.update(lock_id=lock,subject_id=subject,subject_type='scoped_mecha_source_design',
 canonical_name='货柜领袖R8整机形象源设计固定',canon_entity_id='V353U043',package_id='PK_GUEST_FIRESEED',
 role_type='全尺寸载具人格/作业变形/护送领袖',unit_or_mecha_link='V353U043',
 visual_lock=receipt['acceptance_scope'],current_art_reference=BASE+master,
 asset_status='user_selected_whole_body_master_authorized_corrected_source_delivery',
 story_gate='SYSTEM-DESIGN;不推进正式故事',must_not='不得压扁头型、缩短长腿或恢复缩脖子体态;不得将独立货柜穿到背上;源设计交付不等于模型/动作/运行验收',
 source_refs=BASE+acceptance+';'+BASE+record,notes='仅R8原形象及哈希为用户明确采用；R9三视按授权修正交付，未冒充逐图新用户验收。')
r=next(x for x in rows if x['lock_id']=='CML137')
r18=next(x for x in rows if x['lock_id']=='CML028')
old_reference=r18['current_art_reference']
if old_reference and old_reference!=BASE+master and old_reference not in r18['source_refs'].split(';'):
 r18['source_refs']+=';'+old_reference
r18['current_art_reference']=BASE+master
r18['visual_lock']='R18包身份保持；货柜领袖用户确定R8整机形象由'+lock+'固定，原头由CML138固定，三视/可变方向由CML137约束。旧v4头稿、平眼、无天线宽冠、扁头和缩脖子稿仅历史，不再派生。'
r.update(current_art_reference=BASE+acceptance,
 visual_lock='未来电驱货车/摄像头后视与可见双侧天线方向保持。CML138固定原头；'+lock+'固定用户确定R8整机形象。R9正侧背按露颈沉肩、长腿及原背架修正后交付。',
 asset_status='whole_body_master_user_selected_corrected_turnaround_source_delivered',
 source_refs=BASE+acceptance+';'+BASE+record,
 notes='原头与整机已确定。修正三视按授权源设计交付；模型、颈部展开/肩架净空、全机变形另行验证。')
save_tsv(p,fields,rows)
p=PROJECT/'docs/superpowers/specs/data/canon/authority_overrides.tsv';fields,rows=load_tsv(p)
r=next(x for x in rows if x['record_type']=='art_lock' and x['record_id']=='CML137')
r.update(source_of_truth=BASE+acceptance,last_confirmed=DATE,
 version_scope='M11_selected_R8_master_corrected_turnaround_source_delivery_20261022',
 notes='用户确定R8形象并授权三视修正后交付/下一批；'+lock+'固定整机源，新增绘制与模型/运行分别判断。')
if not any(x['record_type']=='art_lock' and x['record_id']==lock for x in rows):
 rows.append(dict(record_type='art_lock',record_id=lock,canon_level='hard',lifecycle_status='active',
 version_scope='M11_exact_R8_whole_body_source_selected_20261022',source_of_truth=BASE+acceptance,
 supersedes='',last_confirmed=DATE,owner='art',notes='用户明确固定R8整体形象及哈希；三视修正交付获授权，模型/动作/运行未签认。'))
save_tsv(p,fields,rows)
receipt['authority_registration']=dict(whole_body_master_lock=lock,head_lock='CML138',direction_lock='CML137')
write(acceptance,receipt)
p=PROJECT/'docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md';s=p.read_text()
entry='- 2026-10-22用户明确确定货柜领袖R8形象，要求三视修正后交付再开始下一批。'+lock+'固定指定整机母稿，CML137更新交付方向；R9正侧背已按肩颈/背架修正，源设计包见'+BASE+'M11-delivery-manifest-r9.json。修正图按授权交付，未代签模型/连续变形或运行。原剧情活动点与已固定源保持。\n\n'
if entry not in s:s=s.replace('## 一、当前结论\n\n','## 一、当前结论\n\n'+entry,1)
p.write_text(s)
# Acceptance registration changes its bytes; build the final package after all source writes.
package_files=[dict(file=k,archive_path=v,sha256=sha(OUT/k)) for k,v in filemap.items()]
write('M11-delivery-manifest-r9.json',dict(date=DATE,files=package_files,master_user_accepted=True,
    source_delivered=True,runtime_delivered=False))
with zipfile.ZipFile(OUT/production['delivery_zip'],'w',zipfile.ZIP_DEFLATED) as z:
 for src,dst in filemap.items():z.write(OUT/src,dst)
 z.write(OUT/'M11-delivery-manifest-r9.json','manifest.json')
with zipfile.ZipFile(OUT/production['delivery_zip']) as z:assert z.testzip() is None
print(json.dumps(dict(reader=str(OUT/reader),zip=str(OUT/production['delivery_zip']),lock=lock),ensure_ascii=False))

