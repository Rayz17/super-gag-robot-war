"""Deliver the six native source views in the existing art batch."""
from pathlib import Path
import hashlib,json,zipfile
from html import escape
from PIL import Image

OUT=Path(__file__).resolve().parent
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='city-response-turnaround-production-r3.json'
READER='city-response-turnaround-r3.html'
REVIEW='city-response-turnaround-author-review-r3.json'
PACKAGE='city-response-turnaround-source-20261024-r3.zip'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

if (OUT/'city-response-user-correction-20261024-r4.json').exists():
    print(json.dumps({'historical_R3_preserved':True,'latest_feedback':'city-response-user-correction-20261024-r4.json'},ensure_ascii=False))
    raise SystemExit(0)

parent_record=read('city-response-source-production-r2.json')
receipt=read('city-response-design-fixed-20261023-r2.json')
parents={x['id']:x for x in parent_record['items']}
sources={
 'M09':[
  ('FRONT','正面','M09-front-r3b.png','exec-e5d09cb0-f76f-4677-b172-1962fa13675b.png'),
  ('SIDE','侧面','M09-side-r3c.png','exec-aef534a2-cb68-4975-ae21-308916dbcf9f.png'),
  ('REAR','背面','M09-rear-r3b.png','exec-202cf9b1-1991-4667-84c4-07a8d462cb36.png')],
 'M10':[
  ('FRONT','正面','M10-front-r3b.png','exec-10b2f01d-14a1-4865-8e0d-8fa90e48a456.png'),
  ('SIDE','侧面','M10-side-r3b.png','exec-628ea6ad-d4d3-4781-b683-a876a39a8c3f.png'),
  ('REAR','背面','M10-rear-r3.png','exec-705584f1-b3af-431e-abd8-281c8b337b2c.png')]
}
machines=[]
for ident,rows in sources.items():
    parent=parents[ident]
    assert parent['user_accepted'] and sha(OUT/parent['file'])==parent['sha256']
    views=[]
    for view,label,file,origin in rows:
        local='samples/'+file
        assert sha(OUT/local)==sha(GEN/origin), 'Native source must be preserved byte-for-byte'
        with Image.open(OUT/local) as im:size,mode=list(im.size),im.mode
        views.append(dict(id=view,label=label,file=local,sha256=sha(OUT/local),pixel_size=size,mode=mode,generated_source=str(GEN/origin),user_accepted=False,runtime_integrated=False))
    machines.append(dict(id=ident,name=parent['name'],canon_entity=parent['canon_entity'],parent={k:parent[k] for k in ['file','sha256','user_accepted']},views=views))
prompts=['city-response-turnaround-prompts-r3.json','city-response-front-corrections-r3b.json','city-response-derived-prompts-r3.json','city-response-view-corrections-r3.json']
review=dict(date='2026-10-24',reviewer='author',independent_review=False,actual_media=[v['file'] for m in machines for v in m['views']],comparison_media=[m['parent']['file'] for m in machines],observations={
 'M09':[
  '正面保持高头壳、琥珀顶灯、青色双目、灰白/蓝灰与细红反光标记；连续曲面肩胸与前臂、顺长腿壳延续R2父源。未压短大腿/胫甲或放大头部。',
  '正面背负观看者左三、右二；背面观看者左二、右三，加左手一面，共六面墙。背初稿中间多画两块，已实际删除，中央露出机械脊柱。',
  '背面后膝改黑色防尘套，脚踝有后跟连杆与短跟壳，删除误复用的正面膝甲/脚尖。',
  '侧面由双脚错开的斜侧稿收正；近手改持墙并按正面重校墙长与手高。墙是窄边，背负件相互遮挡，不能据侧面独立清点全部。脚跟等仍有手绘透视近似。'],
 'M10':[
  '三面保持高消防盔、可见下颌/嘴线、橙白驾驶室胸与成人厚实体态。正面风挡由初稿三块正窗改为两块，右腰两罐与左腰卷盘分开。',
  '近侧可辨髋轮和小腿双轮，前/后图外缘对应两髋轮加四胫轮；背面用胎面窄边，没有把圆轮毂转朝后。侧面部分髋轮被前臂遮挡。',
  '背面两包桥板、银色液压件及中央工程脊柱可辨；后腰观看者右侧双水罐、左侧卷盘，与正面物理侧别相同。',
  '侧稿原本双足前后错开，局部改为主要鞋轮廓重合、脚侧服务窗与低黑底；头盔和腿长未跟随重做。背面保留红色后灯/跟部，未重画一套前胸。'],
 'limits':['独立二维插画投影，不是同一三维模型的精密正交输出；头/腿/设备隐面尺寸仍需分件模型统一。','消防四个稳定支腿为父源车辆工作态的设备；本轮人形三视仅见折叠工具壳，未逐个展开或证明支腿收放、桥面承重及完整变形。']},source_parent_user_accepted=True,new_views_user_accepted=False,runtime_tested=False)
write(REVIEW,review)
experience=dict(start='两张R2整机已采用，三视必须延续现有头身与职业设备。',input='分别绘制正面，再以修正正面和R2父源派生侧/背；局部修数量、侧别和后部结构。',visible_consequence='两机各有完整独立正侧背；灰崎六墙、后膝和脚跟修正，消防两窗驾驶室/六轮/双桥包/双水罐可以前后对照。',next='沿这六张源图与已定父源继续分件、模型及工作动作核对；当前新增图未代签用户认可。')
history=[
 dict(id='M09',files=['samples/M09-front-attempt-r3.png'],result='背包初稿仅四个墙模块，改为三加二。'),
 dict(id='M10',files=['samples/M10-front-attempt-r3.png'],result='正窗与两侧水罐不符，局部统一两窗/右双罐左卷盘。'),
 dict(id='M09',files=['samples/M09-side-attempt-r3.png','samples/M09-side-attempt-r3b.png','samples/M09-rear-attempt-r3.png'],result='修正斜侧持墙/墙长、背包多画两墙与背面误用前膝脚尖。'),
 dict(id='M10',files=['samples/M10-side-attempt-r3.png'],result='侧稿脚部错开，局部收正侧向与脚轮廓。')]
record=dict(date='2026-10-24',revision='city-response-turnaround-r3',existing_batch='design-followthrough-r1.json',generation_mode='built-in image_gen',reader=READER,source_package=PACKAGE,status='six_source_views_delivered_after_parent_adoption',parent_acceptance_receipt='city-response-design-fixed-20261023-r2.json',items=machines,prompt_set=prompts,author_review=REVIEW,experience=experience,historical_attempts=history,new_views_user_accepted=False,runtime_assets_modified=False,handoff_sent=False)
write(RECORD,record)
notes={'M09':'保留巡逻盔、连续曲面壳体与原身形。左手持一面交通墙，背负五面。','M10':'保留高消防盔、橙白驾驶室胸与双足工程体态。成对桥板收于背后，水罐与卷盘分侧。'}
sections=''
for m in machines:
    pictures=''.join('<figure><figcaption>'+v['label']+'</figcaption><a href="'+v['file']+'"><img src="'+v['file']+'" alt="'+escape(m['name']+v['label'])+'" loading="eager"></a><a class="small" href="'+v['file']+'">打开原图</a></figure>' for v in m['views'])
    sections+='<section id="'+m['id']+'"><h2>'+m['name']+'</h2><p>'+notes[m['id']]+' <a href="'+m['parent']['file']+'">已定整机母稿</a></p><div class="views">'+pictures+'</div></section>'
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>灰崎与消防架桥机 · 三视图</title><style>body{margin:0;background:#eeece5;color:#243b49;font:16px/1.7 system-ui}main{max-width:1700px;margin:auto;padding:26px}a{color:#155c78}nav{display:flex;flex-wrap:wrap;gap:20px}h1{font-size:clamp(28px,4vw,42px);line-height:1.3}section{border-top:1px solid #c6cec9;margin-top:32px;padding-top:16px}.views{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}figure{margin:0;background:#fff;padding:10px;min-width:0}figcaption{font-weight:700;margin-bottom:8px}img{display:block;width:100%;height:auto}.small,footer{font-size:14px}footer{margin-top:32px;color:#5c7077}@media(max-width:700px){main{padding:15px}.views{gap:6px}figure{padding:4px}.small{font-size:12px}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="#M09">灰崎</a><a href="#M10">消防架桥机</a><a href="'''+PACKAGE+'''">下载六张原图与提示词</a></nav><h1>灰崎与消防架桥机 · 三视图</h1><p>沿已确认的整机母稿制作，保留头部、配色与身形。点击任一视图查看完整原图。</p>'''+sections+'''<footer>2026.10.24 · 内置生图。当前交付为二维设定三视，细部投影和机构尺寸在分件阶段继续核对。<p><a href="'''+RECORD+'''">源文件与制作记录</a> · <a href="'''+REVIEW+'''">实际查看记录</a> · <a href="city-response-design-fixed-20261023-r2.json">母稿采用范围</a></p></footer></main></body></html>'''
(OUT/READER).write_text(page)
ledger=read('design-followthrough-r1.json')
ledger.update(latest_city_response_turnaround=RECORD,latest_authorized_turnaround_delivery=RECORD)
ledger['production_focus'].update(current_step='已完成两机六张独立三视源图，按实际查看结果局部修正墙数、侧向、后膝/脚跟及风挡/水罐对应。',next=experience['next'])
ledger['experience_record_city_response_turnaround_r3']=dict(classification='experience',record=RECORD,original_requirement=['用户：可以，出三视图','M09','M10','city-response-design-fixed-20261023-r2.json'],actual_artifacts=[v['file'] for m in machines for v in m['views']],**experience,author_review=REVIEW,independent_review=False,new_images_user_accepted=False,source_parent_user_accepted=True,runtime_changed=False)
defect_id='ART-CITY-TURNAROUND-EQUIPMENT-PROJECTION-R3'
if not any(x['id']==defect_id for x in ledger['defect_ledger']):
    ledger['defect_ledger'].append(dict(id=defect_id,defect='本轮独立派生出现墙数量、侧面投影/墙长与后膝脚跟、消防窗罐位置不一致。',attempts=[dict(files=[f for x in history for f in x['files']],observed=True,observer='author',outcome='persists',result='初稿的具体数量和投影错误见历史图及作者记录。'),dict(files=[v['file'] for m in machines for v in m['views']],observed=True,observer='author',outcome='improved_in_source_drawings',result='逐区修正后六墙/两窗/罐与卷盘侧别可辨，背膝脚跟及侧脚收正；插画近似仍在。',evidence=REVIEW)],method_changes=[dict(status='applied',old='独立整图派生一次后直接采用。',new='先校正正面，以具体失败图作局部编辑目标；墙长/手高另加正面图与像素范围校对。',applied_evidence='city-response-view-corrections-r3.json')],closed=False,remaining='二维投影仍有近似，隐面尺寸、机构与模型/动作另验。'))
write('design-followthrough-r1.json',ledger)
parent_reader=OUT/'city-response-source-r2.html';html=parent_reader.read_text()
if 'city-turnaround-delivered-r3' not in html:
    html=html.replace('</nav>','</nav><p class="scope" id="city-turnaround-delivered-r3">两机正、侧、背源图已完成：<a href="'+READER+'">查看六张三视图</a>。</p>',1)
html=html.replace('正在直接制作正、侧、背源图。','已按请求补齐正、侧、背源图。')
parent_reader.write_text(html)
files=[v['file'] for m in machines for v in m['views']]+[m['parent']['file'] for m in machines]+prompts+[RECORD,REVIEW,'city-response-design-fixed-20261023-r2.json']
manifest=dict(date='2026-10-24',files=[dict(file=f,sha256=sha(OUT/f)) for f in files],native_source_preserved=True,source_parent_user_accepted=True,new_views_user_accepted=False,runtime_assets_modified=False)
write('city-response-turnaround-delivery-manifest-r3.json',manifest)
with zipfile.ZipFile(OUT/PACKAGE,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files+['city-response-turnaround-delivery-manifest-r3.json']:z.write(OUT/f,f)
print(json.dumps({'views':6,'reader':str(OUT/READER),'package':str(OUT/PACKAGE)},ensure_ascii=False))
