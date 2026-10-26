"""Deliver Songwing R4-derived front/side/rear source drawings, preserving native files."""
from pathlib import Path
import hashlib,html,json,shutil,sys,zipfile
from PIL import Image
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='M14-turnaround-production-r5.json'
READER='M14-turnaround-r5.html'
RECEIPT='M14-design-fixed-20261022.json'
PROMPTS='M14-turnaround-prompts-r5.json'
ZIP='M14-source-turnaround-20261022-r5.zip'
def read(name):return json.loads((OUT/name).read_text())
def write(name,d):(OUT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=read(RECEIPT)
master=receipt['selected_master']
assert sha(OUT/master['file'])==master['sha256']
items=[]
for ident,label,filename,path,prompts in [
 ('FRONT','正面','M14-front-r5.png',GEN/'exec-ec73a73a-01f9-4365-aad9-e03487d0c1b7.png',['M14-front-prompt-r5.txt']),
 ('SIDE','右侧面','M14-side-r5b.png',Path(sys.argv[1]),['M14-side-prompt-r5.txt','M14-side-view-correction-prompt-r5b.txt']),
 ('REAR','背面','M14-rear-r5b.png',Path(sys.argv[2]),['M14-rear-prompt-r5.txt','M14-rear-view-correction-prompt-r5b.txt'])]:
    target=OUT/'samples'/filename
    if target.exists():assert sha(target)==sha(path)
    else:shutil.copyfile(path,target)
    with Image.open(target) as im:size=list(im.size);mode=im.mode
    items.append(dict(id=ident,label=label,file=target.relative_to(OUT).as_posix(),sha256=sha(target),generated_source=str(path),pixel_size=size,mode=mode,prompts=prompts,role='authorized derived source drawing',individual_new_image_user_accepted=False,runtime_integrated=False))
history=[]
for label,name in [('SIDE_ATTEMPT','exec-bcbcb8f2-ee29-4ec3-95b4-ec4568194273.png'),('REAR_ATTEMPT','exec-4acafc4e-672b-4de3-a447-3ded1a837484.png')]:
    origin=GEN/name;target=OUT/f'samples/M14-{label.lower()}-r5.png'
    if not target.exists():shutil.copyfile(origin,target)
    assert sha(target)==sha(origin)
    history.append(dict(id=label,file=target.relative_to(OUT).as_posix(),sha256=sha(target),status='historical_failed_view_attempt'))
state=dict(music_module='deployed forward',front='扬声器振膜朝机体前方',side='按相同展开状态显示侧向厚度、挂点与舱罩前凸',rear='显示声翼红白外壳和支架，扬声器振膜不反向面对后方',base='用户采用R4主形、头部、长腿与暖象牙/朱红/石墨涂装')
record=dict(revision='M14-turnaround-r5',date='2026-10-22',existing_batch='design-followthrough-r1.json',status='authorized_source_turnaround_delivery',reader=READER,source_receipt=RECEIPT,selected_master=master,source_lock=receipt['authority_registration']['source_lock'],generation_mode='built-in image_gen; front anchor followed by side/rear and targeted view corrections',items=items,historical_attempts=history,equipment_state=state,
 author_review=dict(reviewer='author',independent_review=False,actual_media=[x['file'] for x in items],observations=['正面保持R4头盔/双红天线、琥珀座舱、长腿和双声翼，一大一小振膜朝前。','侧面修正后双足前后错位减少，头胸/舱罩前凸、背部支架、声翼厚度与小腿发动机可见。侧向仍属绘制设定图，带少量透视。','背面显示声翼红白外壳与支架、头盔后壳、脊柱和后跟；修正了初稿脚尖朝后镜头的问题。','三图主形/配色/声翼方向可追认；隐面细部和精确尺寸不由三张生成插画证明。']),
 limits=['本次人形正侧背为同一源设计的绘制设定图，细小隐面仍不等于同件三维正交投影。','R4原母稿已采用；三张新绘制按授权交付，不代签逐图新用户认可、完整变形、实听或运行。','航空形态仍沿已采用R4源板，本次没有重画另一套机设。'],runtime_assets_modified=False,character_roles_changed=False,canon_migration_scope='R4 source acceptance CML140/CML023 only; new drawings separate',handoff_sent=False)
write(RECORD,record)
write(PROMPTS,dict(mode='built-in image_gen',approved_master=master,front_anchor=items[0],items=[dict(id=x['id'],files=x['prompts']) for x in items]))
sections=''.join(f'<figure id="{x["id"]}"><figcaption>{x["label"]}</figcaption><a href="{x["file"]}"><img src="{x["file"]}" alt="歌翼R5{x["label"]}，沿已采用R4声翼展开主形"></a><p><a href="{x["file"]}">打开原尺寸</a></p></figure>' for x in items)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>歌翼｜音乐传播版正侧背三视R5</title><style>*{box-sizing:border-box}body{margin:0;background:#eeeae0;color:#193345;font:16px/1.8 system-ui}main{max-width:1760px;margin:auto;padding:26px}a{color:#09657c}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,43px);line-height:1.3}.views{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}figure{margin:0;background:#faf8f0}figcaption{padding:10px 14px;font-size:20px;font-weight:700}img{display:block;width:100%;height:auto}figure p{padding:0 14px}.note{font-size:14px;color:#536b75}.scope{padding:12px 18px;border-left:4px solid #cc5946;background:#faf5eb}details{margin-top:28px}.master{max-width:1200px}@media(max-width:800px){main{padding:16px}.views{grid-template-columns:1fr}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="M14-source-turnaround-20261022-r5.zip">下载源图与提示词包</a><a href="M14-turnaround-prompts-r5.json">实际内置生图提示词</a><a href="M14-music-support-r4.html">已采用R4原设计</a></nav><h1>歌翼音乐传播版 · 正侧背三视</h1><p class="scope">沿用户采用的R4主形派生，保持头型、长腿、座舱胸和红白涂装。三张统一为声翼向前展开状态：正面看振膜，背面看外壳与支架。</p><div class="views">'''+sections+'''</div><p class="note">点击图片查看原尺寸。侧背在首稿后修正视向；本页为二维设定源稿，完整机构与同件模型仍分别验证。</p><details><summary>已采用的R4母稿与声翼闭合状态</summary><img class="master" src="samples/M14-music-support-r4.png" alt="用户采用的R4音乐传播版母稿，含闭合/展开与航空形态"></details><p><a href="M14-design-fixed-20261022.json">采用回执</a> · <a href="M14-turnaround-production-r5.json">三视源文件与查看记录</a></p></main></body></html>'''
(OUT/READER).write_text(page)
receipt['derived_turnarounds']=[dict(file=x['file'],sha256=x['sha256'],status='authorized_derived_source_delivery',individual_new_image_user_accepted=False) for x in items]
receipt['turnaround_record']=RECORD
write(RECEIPT,receipt)
for name in ['M14-music-support-r4.html','aircraft-synthesis-r3.html','aircraft-runtime-comparison-20261022.html']:
    p=OUT/name;s=p.read_text()
    note=f'<aside id="songwing-turnaround-r5" class="scope"><h2>歌翼R4已采用，正侧背三视已出</h2><p><a href="{READER}">查看三视与下载源图包 →</a></p><p>沿同一主形派生，三视统一声翼朝向；模型与运行另行验证。</p></aside>'
    if 'id="songwing-turnaround-r5"' not in s:p.write_text(s.replace('</nav>','</nav>'+note,1))
ledger=read('design-followthrough-r1.json')
ledger['latest_m14_turnaround']=RECORD
ledger['production_focus'].update(current_step='歌翼R4已采用，正侧背三张源图已生成并修正侧背视向，准备核对交付。',current_scope='已采用歌翼R4的三视源设计派生；雷翎、人物和运行不变。',next='完成源图查看、文件核对与源图包交付；后续同件模型/动作/音频仍依原范围。')
ledger['experience_record_m14_turnaround_r5']=dict(classification='experience',record=RECORD,original_requirement=['M14','F08','N13','CML023','CML140'],start='用户以“这版可以。出具三视图”采用R4。',input='固定R4母稿与哈希，先生成正面为尺度参考，再生成侧背并修正相机/脚尖/声翼朝向。',visible_consequence='同一主形的正侧背源图；声翼状态可追认，具体图面复核见本记录。',actual_artifacts=[x['file'] for x in items],author_review=RECORD+'#author_review',independent_review=False,derived_images_user_accepted=False,base_source_user_accepted=True,runtime_changed=False,next='新源图与模型/完整变形/实听分别判断。')
defect=next((x for x in ledger['defect_ledger'] if x.get('id')=='ART-M14-TURNAROUND-VIEW-R5'),None)
if defect is None:
    defect=dict(id='ART-M14-TURNAROUND-VIEW-R5',defect='侧面转角/脚位与背面脚尖方向失准，不能仅靠套用原正面交付三视。',attempts=[dict(files=[x['file'] for x in history],observed=True,outcome='persists',result='侧面带转角和错位双足，背面初稿复制前脚尖；声翼背壳朝向已正确。',evidence=RECORD),dict(files=[x['file'] for x in items if x['id']!='FRONT'],observed=True,outcome='improved_in_source_drawings',result='侧面双足投影更重合，背面改为紧凑后跟和背部脊柱；仍非精密正交工程图。',evidence=RECORD)],method_changes=[dict(status='applied',old='用原母稿和正面直接生成完整侧背。',new='以实际失败图作编辑目标，分别限定侧向投影与背部脚跟/脊柱结构，保留已正确声翼背壳。',reason='实际观察到视向问题，按局部视向修改而不重造主体。',applied_evidence=RECORD)],closed=False,remaining='明显反向问题已在源图修正；少量插画透视和隐面细节仍在同件模型阶段核对。')
    ledger['defect_ledger'].append(defect)
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_m14_turnaround']=RECORD;write('sample-author-review.json',author)
notes='歌翼R4已由用户采用。此包为沿同一主形绘制的正侧背源图、原母稿、采用回执、实际内置生图提示词和源记录。三视为声翼向前展开状态；背面看外壳。新绘制图不代签模型、完整变形、声音或运行。\n'
(OUT/'M14-source-turnaround-notes-r5.txt').write_text(notes)
files=[x['file'] for x in items]+[master['file'],RECORD,RECEIPT,PROMPTS,'M14-source-turnaround-notes-r5.txt']+[p for x in items for p in x['prompts']]
manifest=dict(revision='M14-turnaround-delivery-r5',files=[dict(file=f,sha256=sha(OUT/f)) for f in dict.fromkeys(files)],approved_master_sha256=master['sha256'],runtime_replaced=False)
write('M14-turnaround-delivery-manifest-r5.json',manifest)
with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for f in list(dict.fromkeys(files))+['M14-turnaround-delivery-manifest-r5.json']:z.write(OUT/f,arcname=f)
with zipfile.ZipFile(OUT/ZIP) as z:
    assert z.testzip() is None
    for x in manifest['files']:assert hashlib.sha256(z.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps(dict(reader=str(OUT/READER),source_package=str(OUT/ZIP),views=[x['file'] for x in items],runtime_changed=False),ensure_ascii=False))
