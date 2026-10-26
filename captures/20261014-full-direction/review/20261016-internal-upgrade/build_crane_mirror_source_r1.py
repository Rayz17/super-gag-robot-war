"""Continue the existing art batch with crane views and a Mirror Star source proposal."""
from pathlib import Path
import hashlib,json,zipfile
from PIL import Image

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='crane-mirror-source-production-r1.json'
READER='crane-mirror-source-r1.html'
REVIEW='crane-mirror-author-review-r1.json'
PACKAGE='crane-mirror-source-20261024-r1.zip'
def rd(n):return json.loads((OUT/n).read_text())
def wr(n,x):(OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source(view,label,file,native):
    local='samples/'+file
    assert sha(OUT/local)==sha(GEN/native)
    with Image.open(OUT/local) as im:size,mode=list(im.size),im.mode
    return dict(id=view,label=label,file=local,sha256=sha(OUT/local),pixel_size=size,mode=mode,generated_source=str(GEN/native),user_accepted=False,runtime_integrated=False,handoff_sent=False)

crane=[source('FRONT','正面 · 收拢行驶','M07-front-r2b.png','exec-48281e95-c64f-4825-997b-0ab90a4cbb70.png'),source('SIDE','右侧 · 收拢行驶','M07-side-r2.png','exec-a933cb50-9f37-4f87-bec8-1bf09d2cd06c.png'),source('REAR','背面 · 收拢行驶','M07-rear-r2.png','exec-d9274a33-254f-4cfb-9ac4-4c0ea1270705.png')]
mirror=source('MASTER','整机 / 头部 / 棱镜收放 / 航空形态试案','M12-mirror-airframe-master-r1.png','exec-b87b36f2-4941-4007-a670-f0c73c298794.png')
ref_defs=[('M07','samples/M07-public-works-master-r1b.png','已有吊装机主形与作业/行驶两态；本轮保留设计补收拢态多视'),('M12','refs/M12-mirror-original-20261024.jpg','现有镜星菱形独眼头、紫白配色和棱镜识别'),('M12','samples/M08-front-airframe-r6.png','已定雷翎航空机架组织供共架试案，不改M08源，也不宣布已定同模'),('M12','samples/M09-curved-labor-r2.png','项目墨线/色块/旧化画法参考，不取机体头型、颜色或职业')]
refs=[dict(id=i,file=f,sha256=sha(OUT/f),role=role) for i,f,role in ref_defs]
items=[dict(id='M07',name='市政吊装机',canon_entity='V353U031',parent=refs[0],views=crane,source_scope='沿R1b主形补收拢行驶态多视，源设计尚未代签采用'),dict(id='M12',name='镜星',canon_entity='V353U046',file=mirror['file'],sha256=mirror['sha256'],views=[mirror],family_status='M08_airframe_shared_skeleton_proposal_not_Canon',source_scope='保留旧头与颜色，尝试航空共架与可收放干扰棱镜；当前家族选择仍为试案')]
review=dict(date='2026-10-24',reviewer='author',independent_review=False,actual_media=[v['file'] for v in crane+[mirror]],comparison_media=[r['file'] for r in refs]+['samples/M07-front-axis-attempt-r2.png'],observations={
 'M07':['母稿的履带、驾驶舱、吊臂、卷盘、后配重与青绿/象牙白/红结构色保持，三张均为支腿收拢的行驶态。','首正稿下车向前而吊臂横摆，已局部收成朝前短缩的吊臂端部；吊钩缩至前收纳位，侧面可辨支架承接。','正面驾驶舱在观看者左、卷盘在右；背面小驾驶舱后缘在右、卷盘在左，对应车辆右舱/左卷盘。背面不再出现大正面风挡和吊钩。','背面近侧为象牙白/红后配重，根部液压件朝后可见；吊臂前后轴与下车一致，但独立图仍有少量斜角和分件尺度差。'],
 'M12':['菱形独眼头、紫白色块和棱镜记忆点保留；整机采用舱罩胸、肩进气道与机翼根/发动机组织，体现本轮航空共架试案。','主图左臂棱镜处于收拢态；右侧OPEN局部可辨四片三角反射面、中央发射/感测件、黑色支杆和前臂铰接，没有原稿式悬空宝石。','CLOSED/OPEN局部的红/青标识板与小型翻转铰边可辨；这是表达敌我识别翻转的硬件外观设计，尚未验证屏显、机构或战术效果。','右下航空形态能追认舱罩、紫白翼面、成对发动机和收拢传感器舱；未由同件模型验证。'],
 'limits':['M07三视是独立二维插画投影，精确吊臂轴、滑轮穿索、支腿净空和承载仍需分件/机构核对。','现行C02 Reader只明确三盒共模与地方飞行队，没有直接锁定镜星母体。M12与M08共架是本轮设计试案，不能倒写为已定故事/Canonical家族。','本轮未改主工程、模型、动作、声音或运行。']},new_images_user_accepted=False,runtime_tested=False)
wr(REVIEW,review)
experience=dict(start='灰崎/消防源设计已发主对话；M07多视仍欠，镜星只有旧紫色棱镜稿且母体关系未确定。',input='保留吊装母稿补收拢态正侧背；核对镜星当前身份和旧稿，选择航空机架共架试案，并给棱镜实物连接/收放。',visible_consequence='四张新源图可查看：吊装行驶态设备对应，镜星整机/独眼头/干扰棱镜两态/航空形态同页。',next='当前新稿留本会话看方向；选定后再补镜星同形多视/部件与动作，三视和源设计不代替机构或运行验收。')
prompts=['crane-mirror-source-prompts-r1.json','crane-mirror-derived-prompts-r1.json','crane-mirror-rear-prompt-r1.json']
record=dict(date='2026-10-24',revision='crane-mirror-source-r1',existing_batch='design-followthrough-r1.json',reader=READER,source_package=PACKAGE,generation_mode='built-in image_gen',basis='crane-mirror-design-basis-r1.json',items=items,source_refs=refs,prompt_set=prompts,author_review=REVIEW,experience=experience,historical_attempts=[dict(id='M07',file='samples/M07-front-axis-attempt-r2.png',reason='吊臂横摆/吊钩垂落，与行驶态前后轴不一致',current_source=False)],source_design_user_accepted=False,canon_changed=False,runtime_assets_modified=False,handoff_sent=False)
wr(RECORD,record)
def figs(views,name):return ''.join('<figure><figcaption>'+v['label']+'</figcaption><a href="'+v['file']+'"><img src="'+v['file']+'" alt="'+name+v['label']+'"></a></figure>' for v in views)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>下一批：市政吊装机与镜星</title><style>body{margin:0;background:#eeece4;color:#243e4b;font:16px/1.75 system-ui}main{max-width:1700px;margin:auto;padding:26px}a{color:#185f79}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,42px);line-height:1.3}section{border-top:1px solid #c6ceca;margin-top:32px;padding-top:18px}.views{display:grid;grid-template-columns:1fr 1.35fr 1fr;gap:12px;align-items:center}figure{margin:0;background:#fff;padding:10px}figcaption{font-weight:700;margin-bottom:8px}img{display:block;width:100%;height:auto}.scope{background:#faf8ee;padding:12px 16px;border-left:4px solid #bc9b37}.note,footer{color:#5c717a;font-size:14px}details{margin-top:24px}@media(max-width:700px){main{padding:15px}.views{grid-template-columns:1fr;gap:12px}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="#M07">市政吊装机</a><a href="#M12">镜星</a><a href="'''+PACKAGE+'''">下载原图与提示词</a></nav><h1>下一批：市政吊装机与镜星</h1><p class="scope">灰崎与消防的最新8张源图已发送给主对话「战斗主玩法打磨」。本页是接续的新稿，先留本会话看方向。</p><section id="M07"><h2>市政吊装机 · 收拢行驶态三视</h2><p>沿<a href="samples/M07-public-works-master-r1b.png">现有主形</a>补多视：双履带、右侧驾驶舱、左侧卷盘、后配重、吊臂和四稳定支腿保留。吊臂沿行进轴收拢，吊钩进入前支架。</p><div class="views">'''+figs(crane,'市政吊装机')+'''</div><details><summary>原有作业与行驶姿态</summary><a href="samples/M07-public-works-master-r1b.png"><img src="samples/M07-public-works-master-r1b.png" alt="吊装机原主形与作业姿态"></a></details></section><section id="M12"><h2>镜星 · 菱形独眼与可收放干扰棱镜</h2><p>保留原稿的紫白色和光学头型，将棱镜做成前臂连接设备，画出收拢/展开状态。舱罩、进气道、翼根和发动机按航空机架组织。</p>'''+figs([mirror],'镜星')+'''<p class="scope">本轮尝试与雷翎共用航空骨架。当前资料没有直接锁定镜星的母体，这一关系仍是设计试案；雷翎已确定的源图保持。</p><details><summary>原稿与共架参考</summary><p>镜星<a href="refs/M12-mirror-original-20261024.jpg">原稿</a>；雷翎<a href="samples/M08-front-airframe-r6.png">已定航空身体参考</a>。取头型/颜色、身体组织与绘制风格的来源分别记录。</p></details></section><footer><p>2026.10.24 · 内置生图。当前为二维源设计，机构/连续变形/承载与运行分别核对。</p><a href="'''+RECORD+'''">源文件记录</a> · <a href="'''+REVIEW+'''">实际查看记录</a> · <a href="crane-mirror-design-basis-r1.json">设计依据与共架边界</a> · <a href="city-response-main-handoff-20261024.json">上一批发送清单</a></footer></main></body></html>'''
(OUT/READER).write_text(page)
l=rd('design-followthrough-r1.json');l['latest_crane_mirror_source']=RECORD
l['production_focus'].update(current_step='已交付吊装机收拢态三视与镜星新源板；前视轴线已局部修正，来源/共架边界和实际观察见本批。',next=experience['next'])
l['experience_record_crane_mirror_r1']=dict(classification='experience',record=RECORD,original_requirement=['用户：灰崎和消防架桥机你是不是已经发给主对话了，如果是我们就继续下一批吧','M07原多视缺口','M12','V353U031','V353U046'],actual_artifacts=[v['file'] for v in crane+[mirror]],**experience,author_review=REVIEW,independent_review=False,new_images_user_accepted=False,runtime_changed=False)
d=next(x for x in l['defect_ledger'] if x['id']=='ART-M07-TRAVEL-BOOM-AXIS-R2')
if not any(x.get('evidence')==REVIEW for x in d['attempts']):d['attempts'].append(dict(files=[v['file'] for v in crane],observed=True,observer='author',outcome='improved_in_source_drawings',result='前视改为沿前后轴短缩的端部，侧面保留同轴收拢与钩架，背面为根部/配重而非前端钩。独立插画仍有少量透视和分件尺度差。',evidence=REVIEW))
d.update(closed=False,remaining='源图方向改善；精确同件投影、卷索/支腿净空和承载另验。')
wr('design-followthrough-r1.json',l)
files=[v['file'] for v in crane+[mirror]]+[r['file'] for r in refs]+prompts+[RECORD,REVIEW,'crane-mirror-design-basis-r1.json']
files=list(dict.fromkeys(files));manifest=dict(date='2026-10-24',files=[dict(file=f,sha256=sha(OUT/f)) for f in files],user_accepted=False,handoff_sent=False,runtime_assets_modified=False)
wr('crane-mirror-delivery-manifest-r1.json',manifest)
with zipfile.ZipFile(OUT/PACKAGE,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files+['crane-mirror-delivery-manifest-r1.json']:z.write(OUT/f,f)
print(json.dumps({'new_images':4,'reader':str(OUT/READER),'package':str(OUT/PACKAGE),'new_batch_sent':False},ensure_ascii=False))
