"""Publish the paired airframe-line revision using native generated PNGs."""
from pathlib import Path
import hashlib, json, re, shutil, zipfile
from PIL import Image

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
RECORD='aircraft-airframe-production-r6.json'
READER='aircraft-airframe-r6.html'
PROMPTS='aircraft-airframe-prompts-r6.json'
ZIP='aircraft-airframe-source-20261023-r6.zip'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
generated=read('aircraft-airframe-generated-files-r6.json')
review=read('aircraft-airframe-author-review-r6.json')
refs=[]
for file,role in [
    ('samples/M14-front-r5.png','用户指定的体态比例基准；雷翎仅取比例，歌翼保留自身比例'),
    ('samples/M08-synthesis-r3.png','雷翎身份/主形/配色母稿'),
    ('samples/M14-music-support-r4.png','已采用歌翼R4主形、音乐模块与配色母稿'),
    ('samples/M14-side-r5b.png','侧向投影与部件状态参考'),
    ('samples/M14-rear-r5b.png','歌翼背面/声翼背壳参考'),
    ('samples/M08-rear-r4b.png','雷翎隐面连接参考，不作为比例依据'),
    ('samples/M08-side-r4b.png','雷翎侧面局部修正的相机与遮挡依据，不作为比例依据')
]:refs.append(dict(file=file,role=role,sha256=sha(OUT/file)))
assert refs[1]['sha256']=='54347f96fab0cd383baa6178ab49b4ea43c3645df2fa85eaaa3c294636bc77c3'
assert refs[2]['sha256']=='928a96c6ba11c3235a4674fa76c0c95da5e3bdc3b65e93262c891c5b920a1e14'
history=generated.get('history',[])
for attempt in history:
    origin=Path(attempt['generated_source']);target=OUT/attempt['file']
    if target.exists():assert sha(target)==sha(origin)
    else:shutil.copyfile(origin,target)
    attempt['sha256']=sha(target)
items=[]
for ident,name in [('M08','雷翎'),('M14','歌翼')]:
    views=[]
    for view,label in [('front','正面'),('side','左侧面'),('rear','背面')]:
        origin=Path(generated[ident][view]);target=OUT/f'samples/{ident}-{view}-airframe-r6.png'
        if target.exists():assert sha(target)==sha(origin)
        else:shutil.copyfile(origin,target)
        with Image.open(target) as im:size=list(im.size);mode=im.mode
        extra=['M08-side-view-airframe-correction-prompt-r6b.txt'] if ident=='M08' and view=='side' else []
        views.append(dict(id=view.upper(),label=label,file=target.relative_to(OUT).as_posix(),sha256=sha(target),generated_source=str(origin),pixel_size=size,mode=mode,prompt=f'{ident}-{view}-airframe-prompt-r6.txt',additional_prompts=extra,user_accepted=False,runtime_integrated=False))
    items.append(dict(id=ident,name=name,views=views,front=views[0],role='保留主形的航空结构线修订；雷翎体态按歌翼基准',new_images_user_accepted=False))
web_sources=[dict(url='https://macross.jp/pages/series?title=macross',role='官方VF-1J/1S三态资料'),dict(url='https://macross.jp/pages/series?title=macrossf',role='官方VF-25可变战机三态资料'),dict(url='https://macross.jp/pages/series?title=macrossdelta',role='官方音乐支援与可变战机资料')]
record=dict(revision='aircraft-airframe-r6',date='2026-10-23',existing_batch='design-followthrough-r1.json',status='requested_airframe_line_revision_source_delivery',reader=READER,
    user_direction=dict(body_reference='歌翼三视比例正确；雷翎按此即可，R5过瘦过长。',forms='两台整体形态不错，保留主形。',surface='减少过度高达化的装饰切面，增强可变战机航空结构语言。'),
    method_change=dict(old='用8头身/10头身、缩窄肩宽和加长腿等数字反向拉比例。',new='直接使用歌翼实际图像为体态锚；身份/体态/航空表面分工，先校正正面再同步侧背。',status='applied',evidence=[x['front']['file'] for x in items]),
    generation_mode='built-in image_gen',source_refs=refs,primary_reference_links=web_sources,reference_interpretation='三态/功能为官方资料；整流罩、进气道和简化蒙皮的具体取舍是本轮设计判断，并未向生图工具输入官方图像。',items=items,historical_attempts=history,
    author_review=review,authority_scope='歌翼R4已采用主形/哈希保留；R6表面修订按最新要求派生，不自动签署新图、人物、故事、模型或运行。',
    limits=['六张为二维绘制源设定，侧向带少量插画透视，细部隐面与同件模型仍需核对。','本次未重画航空态，旧航空母稿只作来源；新表面与完整变形的对应尚未由模型证明。'],canon_changed=False,runtime_assets_modified=False,handoff_sent=False)
if (OUT/'aircraft-design-fixed-20261023-r6.json').exists():
    accepted=read('aircraft-design-fixed-20261023-r6.json')
    bound={x['file']:x['sha256'] for x in accepted['files']}
    for machine in items:
        for view in machine['views']:
            assert bound.get(view['file'])==view['sha256'], 'Accepted source changed; requires a new design decision'
            view['user_accepted']=True
        machine['new_images_user_accepted']=True
        machine['front']=machine['views'][0]
    record.update(status='user_accepted_source_designs_fixed',source_acceptance_receipt='aircraft-design-fixed-20261023-r6.json',source_design_user_accepted=True,authority_scope=accepted['scope'])
write(RECORD,record)
write(PROMPTS,dict(mode='built-in image_gen',items=[dict(id=x['id'],views=[dict(view=v['id'],files=[v['prompt']]+v['additional_prompts']) for v in x['views']]) for x in items],reference_roles=refs))
def figure(v,name):return f'<figure id="{name}-{v["id"]}"><figcaption>{name} · {v["label"]}</figcaption><a href="{v["file"]}"><img src="{v["file"]}" alt="{name}R6航空结构线{v["label"]}"></a><p><a href="{v["file"]}">原尺寸源图</a></p></figure>'
pair=''.join(figure(x['front'],x['name']) for x in items)
sections=''.join(f'<section id="{x["id"]}"><h2>{x["name"]} · 正侧背</h2><p>'+('体态参照歌翼，保留V形侧冠、长枪与红白蓝刃翼。' if x['id']=='M08' else '保留原体态、双红天线、座舱胸与声翼，减少肩腿的碎切面。')+'</p><div class="views">'+''.join(figure(v,x['name']+'三视') for v in x['views'])+'</div></section>' for x in items)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>雷翎与歌翼｜体态与航空结构线R6</title><style>*{box-sizing:border-box}body{margin:0;background:#eae8df;color:#172f47;font:16px/1.8 system-ui}main{max-width:1800px;margin:auto;padding:26px}a{color:#145e91}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,43px);line-height:1.3}h2{margin-top:38px}.pair,.views{display:grid;gap:18px}.pair{grid-template-columns:repeat(2,minmax(0,1fr));max-width:1250px;margin:auto}.views{grid-template-columns:repeat(3,minmax(0,1fr))}figure{margin:0;background:#faf8f0}figcaption{padding:10px 14px;font-size:20px;font-weight:700}img{display:block;width:100%;height:auto}figure p{padding:0 14px}.scope{padding:12px 18px;border-left:4px solid #b74b3f;background:#faf5eb}.note{font-size:14px;color:#586f7a}.refs{max-width:1200px}details{margin-top:25px}@media(max-width:800px){main{padding:16px}.views{grid-template-columns:1fr}.pair{gap:8px}.pair figcaption{font-size:16px}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="#M08">雷翎三视</a><a href="#M14">歌翼三视</a><a href="aircraft-airframe-source-20261023-r6.zip">源图与提示词包</a></nav><h1>保留主形 · 体态与航空结构线修订</h1><p class="scope">雷翎体态以歌翼为基准，恢复适中的肩胸和四肢厚度。歌翼保留原比例。两台共同减少装饰性菱形切面和碎折线，让座舱、进气道、翼根与发动机舱更明确。</p><div class="pair">'''+pair+'</div>'+sections+'''<details><summary>体态依据：用户认可的歌翼原三视正面</summary><img class="refs" style="max-width:650px" src="samples/M14-front-r5.png" alt="体态比例基准：歌翼原三视正面"></details><details><summary>原主形与声翼来源</summary><img class="refs" src="samples/M08-synthesis-r3.png" alt="雷翎原主形"><img class="refs" src="samples/M14-music-support-r4.png" alt="已采用歌翼音乐传播原主形"></details><p class="note">这是二维源设定修订；精确投影、隐面与完整变形仍由同件模型核对。原歌翼R4采用记录保留，六张新增图按本次要求派生。</p><p><a href="aircraft-airframe-prompts-r6.json">实际内置生图提示词</a> · <a href="aircraft-airframe-production-r6.json">源记录与实际查看结果</a></p></main></body></html>'''
(OUT/READER).write_text(page)
notice=f'<aside id="aircraft-airframe-r6" class="scope"><h2>当前：体态参照歌翼，航空结构线修订R6</h2><p>雷翎R5过瘦过长已退出；两机主形保留，六张三视源稿已按新正面同步。</p><p><a href="{READER}">查看两机修订三视 →</a></p></aside>'
for name in ['aircraft-synthesis-r3.html','aircraft-runtime-comparison-20261022.html','M08-turnaround-r4.html','M08-turnaround-r5.html','M14-turnaround-r5.html']:
    path=OUT/name;s=path.read_text()
    if 'id="aircraft-airframe-r6"' not in s:
        s=re.sub(r'<aside id="leiling-turnaround-r5".*?</aside>',notice,s,count=1,flags=re.S) if 'id="leiling-turnaround-r5"' in s else s.replace('</nav>','</nav>'+notice,1)
    path.write_text(s)
ledger=read('design-followthrough-r1.json')
ledger['latest_aircraft_airframe_revision']=RECORD
ledger['production_focus'].update(current_scope='雷翎体态参照歌翼，两机主形保留，六张三视航空结构线修订R6。',current_step='两张正面完成体态/表面调整，侧背已同步并实际查看；原尺寸PNG与提示词包整理完成。',next='当前源图供对照；同件模型、航空态对应、完整变形与运行仍按原范围验证。')
defect=next(x for x in ledger['defect_ledger'] if x['id']=='ART-M08-TURNAROUND-PROPORTION-R5')
defect['attempts'].append(dict(files=[v['file'] for v in items[0]['views']],observed=True,outcome=review['proportion_outcome'],result=review['proportion_result'],evidence=RECORD))
defect['method_changes'][-1].update(status='applied',applied_evidence=RECORD)
defect['remaining']='已直接引用歌翼体态而非数字反向拉伸；新图用户认可、精确投影与同件模型仍分别保留。'
view_defect=next(x for x in ledger['defect_ledger'] if x['id']=='ART-M08-TURNAROUND-VIEW-R4')
view_defect['attempts'] += [dict(files=[x['file'] for x in history],observed=True,outcome='persists',result='R6侧面初稿误成三分之四转角。',evidence=RECORD),dict(files=[items[0]['views'][1]['file']],observed=True,outcome='improved_in_source_drawings',result='以旧侧向投影只约束视角并编辑初稿；双足/双腿更重叠、翼片侧投影变薄，仍有少量插画透视。',evidence=RECORD)]
view_defect['method_changes'].append(dict(status='applied',old='新正面加跨机体侧面派生，转角再次漂移。',new='回到实际侧向投影约束相机和遮挡，身形仍由新正面负责，不复用旧比例。',reason='跨机体侧面参考不足以约束同物侧投影。',applied_evidence=RECORD))
ledger['defect_ledger']=[x for x in ledger['defect_ledger'] if x.get('id')!='ART-AIRCRAFT-SURFACES-R6-20261023']
ledger['defect_ledger'].append(dict(id='ART-AIRCRAFT-SURFACES-R6-20261023',defect='两机整体主形可用，但肩胸腿的装饰折角/切面过于铠甲化，航空结构语言不足。',attempts=[dict(files=['samples/M14-front-r5.png','samples/M08-front-slender-r5.png'],observed=True,outcome='persists',result='用户指出形态不错但线条太高达化。'),dict(files=[v['file'] for x in items for v in x['views']],observed=True,outcome=review['surface_outcome'],result=review['surface_result'],evidence=RECORD)],method_changes=[dict(status='applied',old='复杂装甲切面/菱形腿甲作为完成度。',new='保留身份主形，改为进气道、舱盖、翼根/整流罩和发动机舱主导结构线；歌翼更强、雷翎保留自身喷气远射特征。',applied_evidence=RECORD)],closed=False,remaining='源图已调整；同件模型与航空态映射仍另验。'))
ledger['experience_record_airframe_r6']=dict(classification='experience',record=RECORD,original_requirement=['M08','F07','M14','F08','N13','V353U047','CML140'],start='用户认可歌翼比例和两机主形，否定R5矫枉过正及过度高达化线条。',input='以歌翼实际比例作锚，分别修正两台正面，再同步侧背的蒙皮/进气道/翼根/发动机舱。',visible_consequence='六张修订三视及同页正面对照，音乐模块与长枪侧别仍可核对。',actual_artifacts=[v['file'] for x in items for v in x['views']],independent_review=False,new_images_user_accepted=False,runtime_changed=False,next='新图、同件模型、完整变形、运行分别判断。')
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_aircraft_airframe_revision']=RECORD;write('sample-author-review.json',author)
notes='雷翎与歌翼R6：雷翎体态以歌翼实际三视为基准，放弃极端10头身反调；两机主形/配色/头冠/长枪或音乐模块保留，简化装饰切面并增强航空结构线。工具为内置image_gen。六张PNG为二维源设定，新图不代签同件模型、完整变形或运行。\n官方三态/功能资料：\n'+'\n'.join(x['url'] for x in web_sources)+'\n'
(OUT/'aircraft-airframe-notes-r6.txt').write_text(notes)
files=[v['file'] for x in items for v in x['views']]+[x['file'] for x in refs]+[v['prompt'] for x in items for v in x['views']]+[f for x in items for v in x['views'] for f in v['additional_prompts']]+[RECORD,PROMPTS,'aircraft-airframe-author-review-r6.json','aircraft-airframe-notes-r6.txt']
manifest=dict(revision='aircraft-airframe-source-r6',files=[dict(file=f,sha256=sha(OUT/f)) for f in dict.fromkeys(files)],runtime_replaced=False)
write('aircraft-airframe-delivery-manifest-r6.json',manifest)
with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for f in list(dict.fromkeys(files))+['aircraft-airframe-delivery-manifest-r6.json']:z.write(OUT/f,arcname=f)
with zipfile.ZipFile(OUT/ZIP) as z:
    assert z.testzip() is None
    for x in manifest['files']:assert hashlib.sha256(z.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps(dict(reader=str(OUT/READER),source_package=str(OUT/ZIP),views=6,runtime_changed=False),ensure_ascii=False))
