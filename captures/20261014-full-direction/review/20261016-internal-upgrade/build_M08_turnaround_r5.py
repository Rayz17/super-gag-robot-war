"""Deliver Leiling's slender R3-based turnaround repair, preserving native images."""
from pathlib import Path
import hashlib, json, re, shutil, sys, zipfile
from PIL import Image

OUT=Path(__file__).resolve().parent
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='M08-turnaround-production-r5.json'
READER='M08-turnaround-r5.html'
PROMPTS='M08-turnaround-prompts-r5.json'
ZIP='M08-source-turnaround-20261022-r5.zip'
def read(name):return json.loads((OUT/name).read_text())
def write(name,data):(OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
master=next(x for x in read('aircraft-synthesis-production-r3.json')['items'] if x['id']=='M08')
assert sha(OUT/master['file'])==master['sha256']
items=[]
for ident,label,view,origin in [
    ('FRONT','正面','front',GEN/'exec-2ea271d5-2e61-46cd-b9b2-c26017f0ba1f.png'),
    ('SIDE','左侧面','side',Path(sys.argv[1])),
    ('REAR','背面','rear',Path(sys.argv[2]))
]:
    target=OUT/f'samples/M08-{view}-slender-r5.png'
    if target.exists():assert sha(target)==sha(origin)
    else:shutil.copyfile(origin,target)
    with Image.open(target) as im:size=list(im.size);mode=im.mode
    items.append(dict(id=ident,label=label,file=target.relative_to(OUT).as_posix(),sha256=sha(target),generated_source=str(origin),pixel_size=size,mode=mode,prompt=f'M08-{view}-slender-prompt-r5.txt',individual_new_image_user_accepted=False,runtime_integrated=False))
review=read('M08-turnaround-author-review-r5.json')
record=dict(revision='M08-turnaround-r5',date='2026-10-22',existing_batch='design-followthrough-r1.json',status='requested_proportion_repair_source_delivery',reader=READER,
    latest_user_feedback='你这个三视图好像也将雷零又做矮了呀。按设定图它不是比较秀气修长的吗',
    selected_master=master,items=items,previous_rejected_proportions=dict(record='M08-turnaround-production-r4.json',items=read('M08-turnaround-production-r4.json')['items']),
    generation_mode='built-in image_gen; return to original R3 proportions for a new front anchor, then match side/rear',
    proportion_method=dict(old='R4使用通用8至8.5头身绘制约束，肩胸与腿甲偏宽。',new='R3左侧全身为比例主依据，收窄肩胸和四肢、拉开长腰、提高髋线、延续长腿。',drawing_targets='约10个完整盔壳高、不含长天线；腿段约62-64%。仅绘制试值，不是生成结果精密量测或新Canon尺寸。',head='盔型保持纵向体积，必要时整头等比调整，禁止压扁。'),
    equipment_state=dict(wings='同一展开状态',rifle='始终机体右手；正面画面左、背面画面右、左侧面在远侧',design='沿R3头胸/翼甲/配色，不增减新装备'),
    author_review=review,limits=['二维绘制源图，侧向仍有少量插画透视；隐面和完整变形不由三张图独自证明。','新修正图按要求交付，尚无逐图新用户认可。'],new_turnaround_images_user_accepted=False,runtime_assets_modified=False,canon_changed=False,handoff_sent=False)
write(RECORD,record)
write(PROMPTS,dict(mode='built-in image_gen',source_master=dict(file=master['file'],sha256=master['sha256']),items=[dict(id=x['id'],file=x['prompt']) for x in items]))
figures=''.join(f'<figure id="{x["id"]}"><figcaption>{x["label"]}</figcaption><a href="{x["file"]}"><img src="{x["file"]}" alt="雷翎R5修长身形{x["label"]}"></a><p><a href="{x["file"]}">打开原尺寸</a></p></figure>' for x in items)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>雷翎｜修长身形三视R5</title><style>*{box-sizing:border-box}body{margin:0;background:#eae8df;color:#172f47;font:16px/1.8 system-ui}main{max-width:1800px;margin:auto;padding:26px}a{color:#145e91}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,43px);line-height:1.3}.views{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}figure{margin:0;background:#faf8f0}figcaption{padding:10px 14px;font-size:20px;font-weight:700}img{display:block;width:100%;height:auto}figure p{padding:0 14px}.note{font-size:14px;color:#586f7a}.scope{padding:12px 18px;border-left:4px solid #b74b3f;background:#faf5eb}.master{max-width:1300px}.compare{display:grid;grid-template-columns:1fr 1fr;gap:16px}.compare img{width:100%;height:660px;object-fit:contain}details{margin-top:25px}@media(max-width:800px){main{padding:16px}.views{grid-template-columns:1fr}.compare img{height:440px}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="M08-source-turnaround-20261022-r5.zip">下载源图与提示词包</a><a href="M08-turnaround-prompts-r5.json">实际内置生图提示词</a><a href="M14-turnaround-r5.html">歌翼三视</a></nav><h1>雷翎 · 修长身形三视</h1><p class="scope">按R3原设定恢复轻巧、秀气的身形：肩胸收窄，腰段拉开，髋线提高，四肢细长。头盔保持纵向体积，V形侧天线、座舱胸、刃翼和红白蓝涂装沿用。</p><div class="views">'''+figures+'''</div><p class="note">点击图片看原尺寸。三张为相同翼片展开状态，长枪始终在机体右手。此页为二维设定源稿。</p><details open><summary>本次比例依据：用户指定R3原设定</summary><img class="master" src="samples/M08-synthesis-r3.png" alt="用户指定的雷翎R3修长原设定"></details><details id="comparison"><summary>上一版与本次正面比较</summary><p>以相同图框高度比较；上一版身形偏敦实，不再作为当前身形依据。</p><div class="compare"><figure><figcaption>R4 · 比例已被指出偏敦实</figcaption><img src="samples/M08-front-r4.png" alt="R4历史正面身形"></figure><figure><figcaption>R5 · 本次修长比例</figcaption><img src="samples/M08-front-slender-r5.png" alt="R5修长身形正面"></figure></div></details><p class="note">侧向仍带少量插画透视，隐面与完整变形仍需同件模型核对。</p><p><a href="M08-turnaround-production-r5.json">源文件与实际查看记录</a></p></main></body></html>'''
(OUT/READER).write_text(page)
notice=f'<aside id="leiling-turnaround-r5" class="scope"><h2>雷翎三视已按R3修长身形重修</h2><p>上一版肩胸和腿甲偏宽，R4不再作为当前比例依据。</p><p><a href="{READER}">查看修长身形三视R5 →</a></p></aside>'
for name in ['aircraft-synthesis-r3.html','aircraft-runtime-comparison-20261022.html','M14-turnaround-r5.html','M08-turnaround-r4.html']:
    path=OUT/name;source=path.read_text()
    if 'id="leiling-turnaround-r4"' in source:source=re.sub(r'<aside id="leiling-turnaround-r4".*?</aside>',notice,source,count=1,flags=re.S)
    elif 'id="leiling-turnaround-r5"' not in source:source=source.replace('</nav>','</nav>'+notice,1)
    path.write_text(source)
ledger=read('design-followthrough-r1.json')
ledger['latest_m08_turnaround']=RECORD
ledger['production_focus'].update(current_scope='雷翎R3原稿比例修正三视R5；R4比例转历史，歌翼与其他已固定来源保持。',current_step='沿原稿重修正面，按新正面同步侧背，实际查看身形与视向后整理源图包。',next='本轮修正图与原R3比较；同件模型、完整变形及运行仍按原范围分别核对。')
defect=next(x for x in ledger['defect_ledger'] if x['id']=='ART-M08-TURNAROUND-PROPORTION-R5')
defect['attempts'].append(dict(files=[x['file'] for x in items],observed=True,outcome=review['proportion_outcome'],result=review['proportion_result'],evidence=RECORD))
defect['method_changes'][0].update(status='applied',applied_evidence=RECORD)
defect['remaining']='修正图已按源稿恢复细长观感；精确投影与隐面同件性仍需模型核对，新图未代签用户认可。'
ledger['experience_record_m08_turnaround_r5']=dict(classification='experience',record=RECORD,original_requirement=['M08','F07','V353U047'],start='用户以R3原稿指出R4三视做矮、失去秀气修长观感。',input='停止以R4体型作锚；由R3重修正面，保持原头纵向体积并收窄肩胸/四肢、提高髋线，再同步侧背。',visible_consequence='新正侧背及R4/R5正面对照，实际查看记录见源记录。',actual_artifacts=[x['file'] for x in items],independent_review=False,new_images_user_accepted=False,runtime_changed=False,next='新源图与同件模型、完整变形、运行分别判断。')
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_m08_turnaround']=RECORD;write('sample-author-review.json',author)
notes='雷翎R5：按用户指定R3原稿修正R4偏矮偏宽的身形，保留头型与配色，重绘正面并同步侧背。采用内置image_gen；包含原尺寸PNG、原母稿、实际提示词与记录。二维源图不代签同件模型或运行。\n'
(OUT/'M08-source-turnaround-notes-r5.txt').write_text(notes)
files=[x['file'] for x in items]+[master['file'],RECORD,PROMPTS,'M08-turnaround-author-review-r5.json','M08-source-turnaround-notes-r5.txt']+[x['prompt'] for x in items]
manifest=dict(revision='M08-turnaround-delivery-r5',files=[dict(file=f,sha256=sha(OUT/f)) for f in dict.fromkeys(files)],source_master_sha256=master['sha256'],runtime_replaced=False)
write('M08-turnaround-delivery-manifest-r5.json',manifest)
with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as package:
    for f in list(dict.fromkeys(files))+['M08-turnaround-delivery-manifest-r5.json']:package.write(OUT/f,arcname=f)
with zipfile.ZipFile(OUT/ZIP) as package:
    assert package.testzip() is None
    for x in manifest['files']:assert hashlib.sha256(package.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps(dict(reader=str(OUT/READER),source_package=str(OUT/ZIP),views=[x['file'] for x in items]),ensure_ascii=False))
