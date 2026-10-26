"""Correct M09 derivatives and extend the retained M10 with vehicle/transform sheets."""
from pathlib import Path
import copy,hashlib,json,zipfile
from PIL import Image

OUT=Path(__file__).resolve().parent
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='city-response-refinement-production-r4.json'
READER='city-response-refinement-r4.html'
REVIEW='city-response-refinement-author-review-r4.json'
PACKAGE='city-response-refinement-source-20261024-r4.zip'
FEEDBACK='city-response-user-correction-20261024-r4.json'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(view,label,file,native):
    path=OUT/'samples'/file
    assert sha(path)==sha(GEN/native),'Native source must remain unchanged'
    with Image.open(path) as im:size,mode=list(im.size),im.mode
    return dict(id=view,label=label,file='samples/'+file,sha256=sha(path),pixel_size=size,mode=mode,generated_source=str(GEN/native),user_accepted=False,runtime_integrated=False)

parents={x['id']:x for x in read('city-response-source-production-r2.json')['items']}
for p in parents.values():assert p['user_accepted'] and sha(OUT/p['file'])==p['sha256']
m09=[asset('FRONT','修正正面','M09-front-r4c.png','exec-b9e1cb2b-a994-449a-9eac-1f02c8abb8bc.png'),asset('SIDE','同步侧面','M09-side-r4.png','exec-3b28cc38-1f0f-40dd-942e-fdb322f48302.png'),asset('REAR','同步背面','M09-rear-r4.png','exec-d19c5b74-42d3-4911-9e6b-346e7be2c5e8.png')]
old=read('city-response-turnaround-production-r3.json')
m10=copy.deepcopy(next(x for x in old['items'] if x['id']=='M10')['views'])
for v in m10:
    assert sha(OUT/v['file'])==v['sha256']
    v.update(retained_unchanged=True,user_feedback='消防架桥机这个问题不大；本轮保持人形。')
extras=[asset('VEHICLE','消防架桥车 · 载具三视','M10-vehicle-turnaround-r4.png','exec-8cd8316c-fae3-4218-94ab-f42556341a0c.png'),asset('TRANSFORM','部件对应与变形步骤','M10-transformation-sequence-r4.png','exec-e9333aae-f3b5-44ed-9551-5e4502168d6a.png')]
contract=dict(date='2026-10-24',status='visual_transformation_proposal',parent_robot_views=[v['file'] for v in m10],vehicle_sheet=extras[0]['file'],sequence_sheet=extras[1]['file'],components=[
 dict(id='A',part='驾驶室胸/头仓',robot='胸部两窗驾驶室，头部在其上方',vehicle='驾驶室保持朝前，头部下沉入车顶舱，躯干滑轨压缩'),
 dict(id='B',part='手臂与侧工具柜',robot='肩柜、前臂喷嘴与可用手掌',vehicle='拳掌收入前臂，臂体转入驾驶室后方两侧工具柜'),
 dict(id='C',part='髋轮/胫轮与底盘',robot='一对髋轮，两侧各双胫轮',vehicle='髋轮对应前轴；下肢向后折转，双胫轮从竖向对应后串列双轴，共三轴六轮'),
 dict(id='D',part='双桥板包',robot='背部两包纵向折叠桥板',vehicle='根部铰接转入车顶纵向收纳；作业时由托架与液压件举升/展开'),
 dict(id='E',part='消防水路',robot='右后腰双水罐，左后腰卷盘',vehicle='右侧驾驶室后双罐，左侧卷盘/泵组；水路保持同侧'),
 dict(id='F',part='稳定支腿',robot='后腰/底盘侧工具壳收纳',vehicle='四支腿按两侧各二展开；不变成机器人主腿')],steps=['01 人形与部件索引','02 头部/拳掌收纳，肩臂向车身侧后收合','03 躯干滑轨压缩，下肢折转，轮组落为三轴底盘','04 双桥板包转入水平托架','05 载具运输形态','06 四支腿稳定、桥面展开与水幕作业'],limits=['动作图用半透明叠影标示前后姿态，不能将叠影计为新增零件。','中间动作是本轮结构设计提案；驾驶舱净空、折转路径/碰撞、线束水路、承重与完整变形尚未以同件模型或连续运动验证。'],user_accepted=False)
write('M10-transformation-correspondence-r4.json',contract)
review=dict(date='2026-10-24',reviewer='author',independent_review=False,actual_media=[v['file'] for v in m09+extras],comparison_media=['samples/M09-curved-labor-r2.png','samples/M09-front-r3b.png','samples/M09-front-attempt-r4.png','samples/M09-front-proportion-r4b.png']+[v['file'] for v in m10],observations={
 'M09':['R4首稿从R2母稿重新推正面，腰胯收窄，但头部仍显大；后续局部把头部等比缩小并收肩，保留完整大腿/胫甲，不纵向压扁头壳。','当前正面头部保留巡逻盔、琥珀灯、蓝灰额板/白檐、黑视窗青眼与收尖护面，较R3减少下颌堆叠；是否完全达到用户要求仍待用户看稿，未代签修复通过。','正面背负三加二，背面二加三，另左手持一面，实际清点为六；中间比例稿的错层帽盖已局部清理。','侧背同步较小头部与较窄肩身，后膝和脚跟仍是后部结构；侧面保留手持墙窄边。独立插画之间仍有少量设备长度、关节高度与投影近似。'],
 'M10':['现有人形三张逐字节保持；载具源板是上方侧面、下方正/背，沿用两窗驾驶室、前轴加后串列双轴、双桥包与橙白柜体。','载具侧图可辨一前轮及后双轮、两只同侧水罐；正/背显示两包桥板端面。该绘制不证明零件尺寸严格同一。','变形图01标A/B/C/D/E，02有头仓与拳掌局部动作，03为下肢折转叠影，04为桥板转为水平的叠影，05落为载具，06有两侧四支点和桥面水幕。','中段滑轨、关节路径和折转净空没有实际机构验证；06为向车头方向铺桥的本轮视觉提案，不改变既有剧情职责。']},M10_humanoid_retained_unchanged=True,new_outputs_user_accepted=False,runtime_tested=False)
write(REVIEW,review)
machines=[]
for ident,views in [('M09',m09),('M10',m10)]:
    machines.append(dict(id=ident,name=parents[ident]['name'],canon_entity=parents[ident]['canon_entity'],parent={k:parents[ident][k] for k in ['file','sha256','user_accepted']},views=views,extras=extras if ident=='M10' else []))
experience=dict(start='用户指出灰崎派生正面矮胖/头错，消防人形问题不大但缺载具与变形图。',input='从指定母稿重新推灰崎正面，局部修头身并同步侧背；以保留的人形和载具目标绘制对应步骤。',visible_consequence='灰崎新增三张修正源图；消防人形保持，新增载具三视板和六步变形/作业图。',next='当前修订进入看稿；按新图继续分件核对、机构/动作制作，不能把二维步骤图当成已验证连续变形。')
prompts=['city-response-refinement-prompts-r4.json','city-response-refinement-derived-prompts-r4.json','city-response-m09-sync-prompts-r4.json']
record=dict(date='2026-10-24',revision='city-response-refinement-r4',existing_batch='design-followthrough-r1.json',generation_mode='built-in image_gen',reader=READER,source_package=PACKAGE,user_feedback=FEEDBACK,parent_acceptance_receipt='city-response-design-fixed-20261023-r2.json',items=machines,prompt_set=prompts,author_review=REVIEW,transformation_correspondence='M10-transformation-correspondence-r4.json',historical_M09_derivatives=['samples/M09-front-r3b.png','samples/M09-front-attempt-r4.png','samples/M09-front-proportion-r4b.png'],experience=experience,new_outputs_user_accepted=False,runtime_assets_modified=False,handoff_sent=False)
write(RECORD,record)
def figures(views,name):return ''.join('<figure><figcaption>'+v['label']+'</figcaption><a href="'+v['file']+'"><img src="'+v['file']+'" alt="'+name+v['label']+'"></a></figure>' for v in views)
steps=''.join('<li>'+s+'</li>' for s in contract['steps'])
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>灰崎修正与消防载具 / 变形图</title><style>body{margin:0;background:#eeeae2;color:#233d49;font:16px/1.75 system-ui}main{max-width:1700px;margin:auto;padding:26px}nav{display:flex;gap:20px;flex-wrap:wrap}a{color:#16617a}h1{font-size:clamp(28px,4vw,42px);line-height:1.3}section{margin-top:32px;padding-top:18px;border-top:1px solid #c5cec9}.views{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}figure{margin:0;padding:10px;background:#fff}figcaption{font-weight:700;margin-bottom:8px}img{display:block;width:100%;height:auto}.sheet{margin:22px 0}.note,footer{font-size:14px;color:#59727b}details{margin:25px 0}.scope{background:#faf8ef;border-left:4px solid #d59c28;padding:12px 16px}@media(max-width:700px){main{padding:15px}.views{gap:6px}figure{padding:4px}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="#M09">灰崎修正三视</a><a href="#M10-vehicle">消防载具</a><a href="#M10-transform">变形图纸</a><a href="'''+PACKAGE+'''">原图与提示词</a></nav><h1>灰崎修正；消防补齐载具与变形图</h1><section id="M09"><h2>灰崎 · 头型与身形修正</h2><p>以你指定的<a href="samples/M09-curved-labor-r2.png">R2母稿</a>重新推正面，缩小头部时保持头壳高宽比，收拢肩胸并保留原有腿长；侧、背同步。交通墙仍为五面背负、一面左手持握。</p><div class="views">'''+figures(m09,'灰崎')+'''</div><details><summary>对照上一版正面</summary><div class="views">'''+figures([dict(label='用户指出矮胖 / 头型偏差的R3',file='samples/M09-front-r3b.png'),m09[0]],'灰崎正面比较')+'''</div></details></section><section id="M10-vehicle"><h2>消防架桥机 · 载具形态</h2><p>现有人形保持。载具三视对应橙白驾驶室胸、三轴轮组、双桥板包与消防设备。</p>'''+figures([extras[0]],'消防架桥机')+'''</section><section id="M10-transform"><h2>部件对应与变形步骤</h2><p>A驾驶室 / 头仓，B手臂工具柜，C下肢与轮组，D桥板，E水罐与卷盘，F稳定支腿。半透明叠影表示部件运动前后的姿态。</p>'''+figures([extras[1]],'消防架桥机')+'''<ol>'''+steps+'''</ol><p class="note">当前为结构设计图，折转净空、关节路径和桥面承重仍需同件机构核对。</p><details><summary>保留的人形三视</summary><div class="views">'''+figures(m10,'消防架桥机')+'''</div></details></section><footer>2026.10.24 · 内置生图。<a href="'''+RECORD+'''">源文件记录</a> · <a href="'''+REVIEW+'''">作者实际查看记录</a> · <a href="M10-transformation-correspondence-r4.json">部件对应表</a></footer></main></body></html>'''
(OUT/READER).write_text(page)
prior=OUT/'city-response-turnaround-r3.html';html=prior.read_text()
if 'subsequent-feedback-r4' not in html:
    html=html.replace('</nav>','</nav><p class="scope" id="subsequent-feedback-r4">后续修订：用户指出本页灰崎正面矮胖且头型偏差。<a href="'+READER+'">查看修正三视及消防载具 / 变形图</a>；本页保留历史交付。</p>',1)
prior.write_text(html)
ledger=read('design-followthrough-r1.json')
ledger.update(latest_city_response_refinement=RECORD,latest_city_response_turnaround=RECORD,latest_authorized_turnaround_delivery=RECORD)
ledger['production_focus'].update(current_step='已按母稿修正灰崎正面头身并同步侧背；消防人形保持，补载具三视和部件对应六步图。',next=experience['next'])
ledger['experience_record_city_response_refinement_r4']=dict(classification='experience',record=RECORD,original_requirement=[FEEDBACK,'M09','M10'],actual_artifacts=[v['file'] for v in m09+extras],**experience,author_review=REVIEW,independent_review=False,new_images_user_accepted=False,runtime_changed=False)
defect=next(x for x in ledger['defect_ledger'] if x['id']=='ART-M09-FRONT-IDENTITY-PROPORTION-R3')
if not any(x.get('evidence')==REVIEW for x in defect['attempts']):
    defect['attempts'].extend([dict(files=['samples/M09-front-attempt-r4.png'],observed=True,observer='author',outcome='partial',result='腰胯较收，但头部仍偏大；进一步改为局部等比缩头/收肩。'),dict(files=[v['file'] for v in m09],observed=True,observer='author',outcome='improved_in_source_drawings',result='头部等比缩小、肩身收拢，腿长保留；侧背同步。是否完全达到用户要求待看稿，不自动关闭。',evidence=REVIEW)])
defect.update(closed=False,remaining='用户尚未认可新派生；独立插画投影和部件尺寸仍需后续同件核对。')
write('design-followthrough-r1.json',ledger)
files=[v['file'] for v in m09+m10+extras]+[m['parent']['file'] for m in machines]+prompts+[RECORD,REVIEW,FEEDBACK,'M10-transformation-correspondence-r4.json','city-response-design-fixed-20261023-r2.json']
files=list(dict.fromkeys(files))
manifest=dict(date='2026-10-24',files=[dict(file=f,sha256=sha(OUT/f)) for f in files],new_outputs_user_accepted=False,M10_humanoid_retained_unchanged=True,runtime_assets_modified=False)
write('city-response-refinement-delivery-manifest-r4.json',manifest)
with zipfile.ZipFile(OUT/PACKAGE,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files+['city-response-refinement-delivery-manifest-r4.json']:z.write(OUT/f,f)
print(json.dumps({'new_source_images':5,'retained_M10_humanoid_views':3,'reader':str(OUT/READER),'package':str(OUT/PACKAGE)},ensure_ascii=False))
