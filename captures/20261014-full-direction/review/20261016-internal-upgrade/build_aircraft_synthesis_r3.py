"""Publish story/IP-led synthesis studies and supersede the rejected recolour route."""
from pathlib import Path
import hashlib, html, json, shutil
from PIL import Image

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='aircraft-synthesis-production-r3.json'
READER='aircraft-synthesis-r3.html'
PROMPTS='aircraft-synthesis-prompts-r3.json'
def read(name):return json.loads((OUT/name).read_text())
def write(name,d):(OUT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source(file,role,base=OUT):
    p=base/file
    return dict(file=p.relative_to(PROJECT).as_posix(),sha256=sha(p),role=role)

rows=[('M08','雷翎','exec-ebcbbb49-df98-4005-af0d-604a8fb5ac17.png'),('M14','歌翼','exec-b9633ea7-71ed-4816-b9cd-376bf1f07583.png')]
refs={
 'M08':[source('refs/M08-user-head-reference-20261022.png','用户指定头型灵感；采用侧部开放V形天线，不采用橙色或文字'),source('samples/M08-dual-form-r1b.png','前建议稿的关节、航空胸与武器结构及绘制完成度'),source('aircraft-runtime-comparison-20261022/leiling_robot.png','现用机设的红白蓝对比、刃翼节奏；旧头胸/腿不锁死'),source('samples/M04-front-backpack-fins-r7.png','本系列插画完成度，仅取画法')],
 'M14':[source('samples/M14-dual-form-r1.png','前建议稿的座舱胸、翼根和绘制完成度；舍弃粉色和单顶鳍'),source('aircraft-runtime-comparison-20261022/song_robot.png','现用白红、修长身形、肩翼与成对天线节奏；不照搬整机'),source('samples/M04-front-backpack-fins-r7.png','本系列插画完成度，仅取画法')]}
items=[]
for ident,name,filename in rows:
    origin=GEN/filename;target=OUT/f'samples/{ident}-synthesis-r3.png'
    if target.exists():assert sha(target)==sha(origin), 'Refuse to replace different generated source'
    else:shutil.copyfile(origin,target)
    with Image.open(target) as im:size=list(im.size);mode=im.mode
    items.append(dict(id=ident,name=name,file=target.relative_to(OUT).as_posix(),sha256=sha(target),generated_source=str(origin),pixel_size=size,mode=mode,
        role='综合整机、同设计头部近景与航空态候选',source_refs=refs[ident],prompt=f'{ident}-synthesis-design-prompt-r3.txt',user_accepted=False,runtime_integrated=False))

decisions={
 'M08':dict(projection='Transformers喷气重涂机谱系；用户头型参考只作为造型灵感，不改变IP归属。',story='C02已接受的同模重涂有独立机魂；雷翎当前实体职责为远射/侦察/机动换位。',
    keep=['现用深色机身、朱红/象牙切面与刃翼节奏。','前建议稿的座舱胸、航空关节和长枪对应。'],
    change=['采用用户参考启发的开放V形侧天线与分层护颊，替换旧中脊细角头。','巨大水滴黄胸核改为琥珀座舱胸，双进气肩框形成航空来源。','腿足改为干净分段与独立踝，缩减旧臃肿小腿；保留长腿和厚实机甲体量。'],
    observed=['整机与头部近景均为同一对蓝/象牙V形天线、红中央传感器和琥珀眼。','实际为宽主翼与较窄稳定翼的组合，翼根连接可见；并非旧模型整机转绘。','航空态双后发动机可见，长枪靠机身挂装且枪口朝机鼻；完整收纳/轴系尚未验证。']),
 'M14':dict(projection='Macross可变战机/歌与护航谱系，保留航空机械关系而非只贴歌姬配色。',story='隼真的稳定人物职责是从抢镜飞行员到保护别人的声音；本轮仅指导造型，不推进任何章节。',
    keep=['现用白红、修长身形与翼展轮廓。','前建议稿的座舱/机鼻胸甲、可读翼根、关节与航空腿架。'],
    change=['重画为完整航空头盔、琥珀光学面和后侧成对红天线，替换长前角与单顶鳍两种旧方案。','水滴胸核改为舱罩胸，长垂翼甲收为能让开手肘的前臂翼片。','可变翼/腿部推进器承担护航机记忆点，暖象牙/朱红配色取代粉白。'],
    observed=['整机与头部近景的白盔、红眉/双天线、琥珀光学面一致，头颈和长腿体积可读。','主翼根和前臂翼片可读，较旧长裙甲更接近航空构件。','生成航空态仍有额外挂舱/推进器，未完全落实提示词的两主发动机精简方案；上背与小腿的对应需背视继续校核，不声明全部为通讯舱。'])}

project_sources=[
 source('docs/superpowers/specs/data/canon/entities.tsv','雷翎当前实体职责',PROJECT),
 source('docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/episodes/C02/C02E02-Reader-v1.md','已接受C02重涂飞行队；不同主体共享大部分造型件',PROJECT),
 source('docs/superpowers/specs/data/character_layer/pilot_cast.tsv','隼真/莉歌的稳定人物职责，不采用旧登场章节',PROJECT),
 source('docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv','CML023 Working参考仍在，当前新增仅候选',PROJECT),
 source('docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md','本作共同画法',PROJECT)]
record=dict(revision='aircraft-synthesis-r3',date='2026-10-22',existing_batch='design-followthrough-r1.json',
 user_feedback='R2完全倒回项目现用资产，未综合参考头与前建议稿的画法；要求按故事和IP重新取舍，Macross特征可保留但风格需改善。',
 generation_mode='built-in image_gen; one sheet per mecha, original references combined deliberately',
 status='candidate_story_ip_led_synthesis',reader=READER,items=items,design_decisions=decisions,project_sources=project_sources,
 external_research=[dict(url='https://macross.jp/pages/series?title=macross',title='MACROSS OFFICIAL SITE / 超時空要塞マクロス',used='歌曲/机体/关系与Fighter-Gerwalk-Battroid可变结构关系',accessed='2026-10-22'),dict(url='https://macross.jp/pages/series?title=macross7',title='MACROSS OFFICIAL SITE / マクロス7',used='歌声与战机并存，声乐功能要服务具体角色而非装饰',accessed='2026-10-22')],
 author_review=dict(reviewer='author',independent_review=False,actual_media=[x['file'] for x in items],observations={k:v['observed'] for k,v in decisions.items()},
   judgement='本轮实际综合新头、旧识别点和前建议稿航空结构/完成度，撤回整机回退只换色的路线。具体新稿待用户看稿。'),
 scope_limits=['源设计改稿，不改既有故事事实、设定米数或当前运行模型。','同页三图为生成插画，主要可见锚点经作者对照，不能作为同件模型/正交三视/完整折变证明。','歌翼额外挂舱的形态数量与去向尚未收敛；提示词的方案不冒充实际完成。'],
 runtime_assets_modified=False,canon_changed=False,main_thread_messaged=False)
write(RECORD,record)
write(PROMPTS,dict(mode='built-in image_gen',items=[dict(id=x['id'],prompt=x['prompt'],source_refs=x['source_refs']) for x in items]))

sections=[]
for x in items:
    d=decisions[x['id']]
    lis=lambda values:''.join('<li>'+html.escape(v)+'</li>' for v in values)
    sections.append(f'''<section id="{x['id']}"><h2>{x['name']}</h2><p class="lead">{d['projection']}</p><a href="{x['file']}"><img class="board" src="{x['file']}" alt="{x['name']}R3综合整机、头部近景与航空态候选"></a><div class="pair"><div><h3>保留的长处</h3><ul>{lis(d['keep'])}</ul></div><div><h3>本轮真正改变</h3><ul>{lis(d['change'])}</ul></div></div><p>故事取舍：{d['story']}</p><details><summary>实际图面核对与尚未收敛处</summary><ul>{lis(d['observed'])}</ul></details></section>''')
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>雷翎与歌翼｜故事与IP综合设计R3</title><style>*{box-sizing:border-box}body{margin:0;background:#eeeae0;color:#193345;font:16px/1.8 system-ui}main{max-width:1580px;margin:auto;padding:28px}a{color:#09657c}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,44px);line-height:1.3}h2{font-size:30px;margin-top:36px}.board{display:block;width:100%;height:auto;background:#faf8f0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:26px}.scope{border-left:4px solid #cd5946;background:#faf6eb;padding:12px 18px}.lead{font-size:19px}.note{font-size:14px;color:#546c75}section{padding-top:8px;border-top:1px solid #bdc9c7;margin-top:30px}details{margin:20px 0}li{margin:8px 0}@media(max-width:700px){main{padding:18px}.pair{grid-template-columns:1fr}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="#M08">雷翎新头与整机</a><a href="#M14">歌翼可变机</a><a href="aircraft-synthesis-prompts-r3.json">实际内置生图提示词</a></nav><h1>把新头、旧识别点和前建议稿真正综合</h1><p class="scope">上一轮只换色的整机回退路线已被用户反证。本轮按故事与IP选择结构，保留长处并重画头胸、翼面和腿架；两台共享绘制语言，保留各自机械身份。</p>'''+''.join(sections)+'''<h2>依据与后续</h2><p>雷翎采用同模重涂但有独立主体的故事职责；歌翼采用隼真从抢镜到保护歌声的角色方向。Macross的歌声与可变机关系、Fighter/Gerwalk/Battroid结构可见<a href="https://macross.jp/pages/series?title=macross">官方系列资料</a>；这次只画人形和航空态，不据此新增已完成的可玩形态。</p><p>当前为源设计候选，未修改现用模型、骨架、动作或运行。头部与整机同页核对，歌翼挂舱归属与后续三视仍需收敛。</p><p><a href="aircraft-synthesis-production-r3.json">逐项取舍与实际观察</a> · <a href="aircraft-runtime-comparison-20261022.html">此前比较记录</a> · <a href="aircraft-existing-design-recolour-r2.html">R2回退换色稿（历史）</a></p></main></body></html>'''
(OUT/READER).write_text(page)

for filename in ['aircraft-runtime-comparison-20261022.html','aircraft-existing-design-recolour-r2.html','aircraft-source-batch-20261022.html']:
    p=OUT/filename;s=p.read_text()
    note=f'<aside id="latest-synthesis-r3" class="scope"><h2>最新：故事与IP综合设计R3</h2><p>用户否定整机回退只换色；已综合指定头型、旧识别点与前建议稿。<a href="{READER}">查看本轮雷翎与歌翼 →</a></p><p>下方保留此前方案及当时判断，已不作为当前整机约束。</p></aside>'
    if 'id="latest-synthesis-r3"' not in s:p.write_text(s.replace('</nav>','</nav>'+note,1))
for filename in ['aircraft-runtime-comparison-20261022.json','aircraft-existing-design-recolour-production-r2.json']:
    d=read(filename);d['later_user_correction_and_synthesis']=RECORD;d['current_design_route']=False;write(filename,d)

ledger=read('design-followthrough-r1.json')
ledger['latest_aircraft_synthesis']=RECORD
ledger['production_focus'].update(current_step='两台R3综合稿已出并实看，含整机、匹配头部与航空态；雷翎实际换头，歌翼按护航/可变战机重新取舍。',current_scope='两台机体综合源设计候选；不再锁死R2旧头胸/翼面，也不改原运行资产。',finish_line='故事与IP身份、画法、头胸翼腿记忆点在同一方案成立；具体源稿与模型/运行分别判断。',next='沿本轮综合方案看稿并收敛歌翼附加挂舱和三视，不再单纯复制旧机设换色。')
ledger['experience_record_aircraft_synthesis_r3']=dict(classification='experience',original_requirement=['M08','F07','M14','F08','N13'],record=RECORD,start='用户反证R2回退旧资产，没有综合指定头型与较好建议稿。',input='核对当前故事职责、Macross官方资料与既有三组图像；逐台明确保留/舍弃后综合生图。',visible_consequence='雷翎新V形头/航空胸/长枪与刃翼同稿；歌翼白红、航空头盔、座舱胸与可动翼腿同稿；画法恢复前建议稿的体积与关节完成度。',actual_artifacts=[x['file'] for x in items],author_review=RECORD+'#author_review',independent_review=False,user_acceptance=False,runtime_changed=False,next='源稿看稿与局部结构收敛；模型/正常镜头未由本轮验证。')
defect=next(x for x in ledger['defect_ledger'] if x['id']=='ART-AIRCRAFT-IDENTITY-ADVANTAGE-02')
for attempt in defect['attempts']:
    if attempt.get('evidence')=='aircraft-existing-design-recolour-production-r2.json':
        attempt.setdefault('previous_author_result',attempt['result'])
        attempt.setdefault('previous_author_outcome',attempt['outcome'])
        attempt.update(outcome='persists',user_counterevidence=record['user_feedback'],result='表面清理成立，但用户反证综合机设/风格问题仍存在；没有采用指定头型。')
if not any(x.get('evidence')==RECORD for x in defect['attempts']):
    defect['attempts'].append(dict(files=[x['file'] for x in items],observed=True,outcome='changed_in_source_candidate_user_review_pending',result='R3实际变更头胸翼腿并综合故事/IP，不再整机回退；具体图面观察见本记录。',evidence=RECORD))
if not any(x.get('applied_evidence')==RECORD for x in defect['method_changes']):
    defect['method_changes'].append(dict(status='applied',old='先把现用整机当作不可改约束，仅重绘涂装。',new='按故事/IP选择锚点；用户头型+前建议稿结构/画法+现用轮廓长处，逐台综合并加头部近景核对。',reason='R1与R2均有实际用户反证，继续单纯重绘或单纯保形不能解决同一设计问题。',applied_evidence=RECORD,retest='实际新头是否进入整机、旧/新长处是否同时可见、IP机械语法是否可读；源稿与三维验证分开。'))
defect.update(closed=False,remaining='本轮新稿具体采用待用户判断；歌翼额外挂舱/背部映射、三视与同模型/正常镜头仍未验证。')
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_aircraft_synthesis']=RECORD;write('sample-author-review.json',author)
user=read('user-art-decisions-20261016.json');user['latest_aircraft_synthesis_feedback']=dict(date='2026-10-22',feedback=record['user_feedback'],requested_head_reference='refs/M08-user-head-reference-20261022.png',R2_accepted=False,execution_record=RECORD,new_drawings_accepted=False);write('user-art-decisions-20261016.json',user)
print(json.dumps(dict(reader=str(OUT/READER),items=[x['file'] for x in items],runtime_changed=False),ensure_ascii=False))
