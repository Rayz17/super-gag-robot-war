"""Register only the exact user-selected M11 head; new drawings stay Candidate."""
import csv,json,re
from pathlib import Path
BASE='captures/20261014-full-direction/review/20261016-internal-upgrade/'
receipt=BASE+'M11-head-selected-and-turnaround-r6.json'
direction=BASE+'M11-head-aspect-chin-direction-r7.json'
def load(f):
 with f.open() as h:r=csv.DictReader(h,delimiter='\t');return r.fieldnames,list(r)
def save(f,fields,rows):
 with f.open('w') as h:w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
f=Path('docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv');fields,rows=load(f)
subject='ART_M11_SELECTED_HEAD_20261021';selected=next((r for r in rows if r['subject_id']==subject),None)
numeric=[int(r['lock_id'][3:]) for r in rows if re.fullmatch(r'CML[0-9]+',r['lock_id'])]
lock=selected['lock_id'] if selected else f'CML{max(numeric)+1:03d}'
if selected is None:selected={k:'' for k in fields};rows.append(selected)
selected.update({'lock_id':lock,'subject_id':subject,'subject_type':'scoped_mecha_head_source','canonical_name':'货柜领袖用户指定原眼形头部源稿','canon_entity_id':'V353U043','package_id':'PK_GUEST_FIRESEED','role_type':'指定头部源认可与颏甲局部优化授权','unit_or_mecha_link':'V353U043','visual_lock':'用户附eac75eab原图明确采用；保留原高宽比、原眼形、额部相机、三块面甲和双侧钝头天线。按最新要求增加短厚前凸勇者颏甲；不得用作者平眼R5b或R6扁头替代。整机头身比按R2长腿尺度，头部不横向放宽或纵向压扁。','current_art_reference':BASE+'samples/M11-selected-head-r6.png','asset_status':'exact_head_source_user_accepted_new_drawings_separate','story_gate':'SYSTEM-DESIGN;不迁移剧情/载具人格','must_not':'不得压扁指定头型或放大头部压短身体;不得取消天线或恢复蛇罩宽冠;新增颏甲/三视/结构/模型/运行不得自动认可','source_refs':receipt+';'+direction+';'+BASE+'M11-turnaround-structure-production-r7.json','notes':'原图是此前作者标为attempt的R5稿，用户最新明确选择优先于作者偏好。认可绑定原附图及哈希；新增具体图稿未采用。'})
for r in rows:
 if r['lock_id']=='CML137':
  r['visual_lock']='未来电驱货车及对应人形、摄像头后视方向保持；可见双天线不取消，不用独立顶单鳍/水平天线。用户指定原眼形eac75eab头稿由'+lock+'约束；保留其原高宽比，身体按R2长腿尺度，新增勇者式前凸颏甲，并补三视及可变结构。新增源稿未自动采用。'
  r['current_art_reference']=direction;r['asset_status']='selected_head_locked_turnaround_structure_authorized_new_drawings_candidate';r['source_refs']=receipt+';'+direction+';'+BASE+'M11-turnaround-structure-production-r7.json';r['notes']='原头源认可与方向分开；作者平眼版不回流。三视独立绘制；头仓草模只核局部包络，未证明整机装配/受力。'
 if r['lock_id']=='CML028':
  r['visual_lock']='R18包身份保持；货柜领袖原v4头稿仅追溯，当前用户指定eac75eab头部由'+lock+'约束，最新颏甲/比例/三视与可变方向由CML137约束；旧横鳍、平眼版、蛇罩宽冠和扁头稿不得回流。'
  if receipt not in r['source_refs'].split(';'):r['source_refs']+=';'+receipt
save(f,fields,rows)
f=Path('docs/superpowers/specs/data/canon/authority_overrides.tsv');fields,rows=load(f)
for r in rows:
 if r['record_type']=='art_lock' and r['record_id']=='CML137':r['version_scope']='M11_head_aspect_chin_turnaround_structure_direction_20261021';r['source_of_truth']=direction;r['notes']='用户指定原头/原比例并要求勇者颏甲、R2头身比、三视和可变优化；指定源由'+lock+'绑定，新增源图与局部草模未自动认可。'
if not any(r['record_type']=='art_lock' and r['record_id']==lock for r in rows):rows.append({'record_type':'art_lock','record_id':lock,'canon_level':'hard','lifecycle_status':'active','version_scope':'M11_exact_eac75eab_head_source_user_selected_20261021','source_of_truth':receipt,'supersedes':'','last_confirmed':'2026-10-21','owner':'art','notes':'仅用户附图原头源与哈希认可；颏甲/三视/结构获授权制作，具体新图、模型和运行另判。'})
save(f,fields,rows)
f=Path(receipt);x=json.loads(f.read_text());x['authority_registration']={'exact_head_source_lock':lock,'direction_lock':'CML137','scope':'original attached head only; generated chin/turnarounds/structure separate'};f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
f=Path('docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md');s=f.read_text();entry='- 2026-10-21用户附eac75eab原眼形头稿明确采用，授权整机三视与可变结构；随后指定R2长腿头身比，再纠正头被压扁，要求保留原头比例并加勇者式前凸颏甲。'+lock+'只绑定原附图头部与哈希；CML137更新比例/颏甲/三视方向。R7新增7张源稿和头仓同件草模未自动采用，局部包络不代表整机装配/受力通过。原剧情活动点、载具人格、固定源与运行保持。来源：'+receipt+'；'+direction+'。\n\n'
if entry not in s:s=s.replace('## 一、当前结论\n\n','## 一、当前结论\n\n'+entry,1)
f.write_text(s)
print('Registered exact user-selected head:',lock)
