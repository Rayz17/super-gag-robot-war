"""Publish the requested Leiling source turnarounds without changing runtime assets."""
from pathlib import Path
import hashlib, html, json, shutil, sys, zipfile
from PIL import Image

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parents[3]
GEN = Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD = 'M08-turnaround-production-r4.json'
READER = 'M08-turnaround-r4.html'
PROMPTS = 'M08-turnaround-prompts-r4.json'
ZIP = 'M08-source-turnaround-20261022-r4.zip'
def read(name): return json.loads((OUT/name).read_text())
def write(name, data): (OUT/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def native_copy(origin, target):
    if target.exists(): assert sha(target) == sha(origin), str(target)
    else: shutil.copyfile(origin, target)

master = next(x for x in read('aircraft-synthesis-production-r3.json')['items'] if x['id']=='M08')
assert sha(OUT/master['file']) == master['sha256']
views = []
for ident, label, filename, origin, prompts in [
    ('FRONT', '正面', 'M08-front-r4.png', GEN/'exec-57b51851-917b-43a8-945a-ff5fffdd5695.png', ['M08-front-prompt-r4.txt']),
    ('SIDE', '左侧面', 'M08-side-r4b.png', Path(sys.argv[1]), ['M08-side-prompt-r4.txt', 'M08-side-view-correction-prompt-r4b.txt']),
    ('REAR', '背面', 'M08-rear-r4b.png', Path(sys.argv[2]), ['M08-rear-prompt-r4.txt', 'M08-rear-view-correction-prompt-r4b.txt'])
]:
    target = OUT/'samples'/filename
    native_copy(origin, target)
    with Image.open(target) as im: size=list(im.size); mode=im.mode
    views.append(dict(id=ident, label=label, file=target.relative_to(OUT).as_posix(), sha256=sha(target), generated_source=str(origin), pixel_size=size, mode=mode, prompts=prompts, individual_new_image_user_accepted=False, runtime_integrated=False))

history=[]
for ident, filename in [('SIDE_ATTEMPT','exec-7eaddb29-fd61-4d36-8e12-86c2b222abf2.png'),('REAR_ATTEMPT','exec-9ac8b271-ffd0-4426-92f8-d1bcf7fcf310.png')]:
    origin=GEN/filename;target=OUT/f'samples/M08-{ident.lower()}-r4.png'
    native_copy(origin,target)
    history.append(dict(id=ident,file=target.relative_to(OUT).as_posix(),sha256=sha(target),status='historical_view_attempt'))

review=read('M08-turnaround-author-review-r4.json')
record=dict(revision='M08-turnaround-r4',date='2026-10-22',existing_batch='design-followthrough-r1.json',status='requested_source_turnaround_delivery',reader=READER,
    authority=dict(turnaround_request_verbatim='雷翎的呢？',source_basis='用户正面反馈后的R3综合稿；本次补派生三视，不扩大源图或运行认可。',new_turnaround_images_user_accepted=False),
    selected_master=master,generation_mode='built-in image_gen; front anchor then side/rear with targeted view corrections',items=views,historical_attempts=history,
    equipment_state=dict(wings='同一展开状态；侧面观察厚度与翼根，正背观察刃翼轮廓',rifle='仅一把，始终为机体右手持握；正面在画面左，背面在画面右，左侧面在远侧',hidden_structure='背部脊柱、闭合肩后壳与双小腿发动机为本轮补画的隐面；仍需同件模型核对'),
    author_review=review,limits=['本批为二维绘制设定源图，隐面分件、精确投影和完整变形仍需同件模型核对。','未改变歌翼已采用R4来源、人物身份、故事、当前模型或运行加载。'],runtime_assets_modified=False,canon_changed=False,handoff_sent=False)
write(RECORD,record)
write(PROMPTS,dict(mode='built-in image_gen',source_master=dict(file=master['file'],sha256=master['sha256']),items=[dict(id=x['id'],files=x['prompts']) for x in views]))

figures=''.join(f'<figure id="{x["id"]}"><figcaption>{x["label"]}</figcaption><a href="{x["file"]}"><img src="{x["file"]}" alt="雷翎{x["label"]}三视源图"></a><p><a href="{x["file"]}">打开原尺寸</a></p></figure>' for x in views)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>雷翎｜正侧背三视R4</title><style>*{box-sizing:border-box}body{margin:0;background:#eae8df;color:#172f47;font:16px/1.8 system-ui}main{max-width:1800px;margin:auto;padding:26px}a{color:#145e91}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,43px);line-height:1.3}.views{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}figure{margin:0;background:#faf8f0}figcaption{padding:10px 14px;font-size:20px;font-weight:700}img{display:block;width:100%;height:auto}figure p{padding:0 14px}.note{font-size:14px;color:#586f7a}.scope{padding:12px 18px;border-left:4px solid #b74b3f;background:#faf5eb}.master{max-width:1200px}details{margin-top:25px}@media(max-width:800px){main{padding:16px}.views{grid-template-columns:1fr}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="M08-source-turnaround-20261022-r4.zip">下载源图与提示词包</a><a href="M08-turnaround-prompts-r4.json">实际内置生图提示词</a><a href="M14-turnaround-r5.html">歌翼三视</a></nav><h1>雷翎 · 正侧背三视</h1><p class="scope">沿R3综合稿补齐，保留对称V形侧天线、座舱胸、修长身形和红白蓝刃翼。三张为相同展开状态，长枪始终在机体右手。</p><div class="views">'''+figures+'''</div><p class="note">点击图片看原尺寸。背部隐面与侧向结构为本次补画的二维设定，精确机构和完整变形仍需同件模型核对。</p><details><summary>R3原综合稿：整机、头部与航空形态</summary><img class="master" src="samples/M08-synthesis-r3.png" alt="雷翎R3原综合设计"></details><p><a href="M08-turnaround-production-r4.json">源文件与查看记录</a></p></main></body></html>'''
(OUT/READER).write_text(page)

for name in ['aircraft-synthesis-r3.html','aircraft-runtime-comparison-20261022.html','M14-turnaround-r5.html']:
    path=OUT/name;source=path.read_text()
    note=f'<aside id="leiling-turnaround-r4" class="scope"><h2>雷翎正侧背三视已补齐</h2><p><a href="{READER}">查看雷翎三视与下载源图包 →</a></p></aside>'
    if 'id="leiling-turnaround-r4"' not in source:path.write_text(source.replace('</nav>','</nav>'+note,1))

ledger=read('design-followthrough-r1.json')
ledger['latest_m08_turnaround']=RECORD
ledger['production_focus'].update(experience='比较与收敛雷翎/歌翼的故事/IP识别点、画法与三视源设计。',current_scope='雷翎沿R3补正侧背三视；歌翼已交付R5三视保持。',current_step='雷翎正面及修正侧背三视已绘制、实际查看，源图与提示词包已整理。',next='沿同一主形继续同件模型与完整变形验证；新源图、模型、动作与运行认可分别保留。')
ledger['experience_record_m08_turnaround_r4']=dict(classification='experience',record=RECORD,original_requirement=['M08','F07','V353U047'],start='雷翎R3综合方向获正面反馈，歌翼三视交付后用户追问雷翎。',input='固定R3原稿哈希，先正面，再派生侧背并针对实际视向问题修正。',visible_consequence='正面、左侧面和背面源图，长枪持握侧与翼/肩后壳可对照。',actual_artifacts=[x['file'] for x in views],author_review=RECORD+'#author_review',independent_review=False,new_turnaround_images_user_accepted=False,runtime_changed=False,next='当前新源图与同件模型/动作/完整变形分别核对。')
ledger['defect_ledger']=[x for x in ledger['defect_ledger'] if x.get('id')!='ART-M08-TURNAROUND-VIEW-R4']
ledger['defect_ledger'].append(dict(id='ART-M08-TURNAROUND-VIEW-R4',defect='侧面初稿仍有转角；背面肩壳与骨盆误沿正面表面。',attempts=[dict(files=[x['file'] for x in history],observed=True,outcome='persists',result='侧面同时露出双腿前甲和前胸；背面肩壳复用了前进气口，中央骨盆是前裆样式。',evidence=RECORD),dict(files=[x['file'] for x in views if x['id']!='FRONT'],observed=True,outcome=review['correction_outcome'],result=review['correction_result'],evidence=RECORD)],method_changes=[dict(status='applied',old='原综合稿加正面派生侧背。',new='以各失败图为编辑目标，修正左右侧投影描述；背面仅改肩壳/上背/骨盆，保留已正确轮廓。',reason='实际视图未达到初稿提示词，改为局部可比修正。',applied_evidence=RECORD)],closed=False,remaining='隐面细节与精确投影仍需同件模型核对。'))
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_m08_turnaround']=RECORD;write('sample-author-review.json',author)

notes='雷翎三视源图：沿R3综合稿补正面、左侧面与背面，翼片为同一展开状态，长枪始终在机体右手。包含原母稿、实际内置生图提示词和源记录。二维设定不代签同件模型、完整变形或运行。\n'
(OUT/'M08-source-turnaround-notes-r4.txt').write_text(notes)
files=[x['file'] for x in views]+[master['file'],RECORD,PROMPTS,'M08-source-turnaround-notes-r4.txt','M08-turnaround-author-review-r4.json']+[p for x in views for p in x['prompts']]
manifest=dict(revision='M08-turnaround-delivery-r4',files=[dict(file=f,sha256=sha(OUT/f)) for f in dict.fromkeys(files)],source_master_sha256=master['sha256'],runtime_replaced=False)
write('M08-turnaround-delivery-manifest-r4.json',manifest)
with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as package:
    for f in list(dict.fromkeys(files))+['M08-turnaround-delivery-manifest-r4.json']:package.write(OUT/f,arcname=f)
with zipfile.ZipFile(OUT/ZIP) as package:
    assert package.testzip() is None
    for x in manifest['files']:assert hashlib.sha256(package.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps(dict(reader=str(OUT/READER),source_package=str(OUT/ZIP),views=[x['file'] for x in views],runtime_changed=False),ensure_ascii=False))
