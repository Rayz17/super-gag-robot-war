"""Start the next scoped aircraft design batch in the original source ledger."""
from pathlib import Path
from PIL import Image
import hashlib,json,html
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
DATE='2026-10-22'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record='aircraft-source-batch-20261022.json'
reader='aircraft-source-batch-20261022.html'
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
specs=[
 ('M08','雷翎','samples/M08-dual-form-r1b.png','exec-a6acf334-57d8-4cb6-8e89-785c28fc4078.png',
  'captures/20261014-full-direction/review/20261016-r3-wave3/images/6b48ef419fc2bba9bde11bd02b63ffc58524db2ad5f847638fa223afd02a9a13.jpg',
  ['M08-dual-form-prompt-r1.txt','M08-gun-forward-prompt-r1b.txt']),
 ('M14','歌翼可变机','samples/M14-dual-form-r1.png','exec-501c9ac0-a345-46e9-afb8-5d0279429a87.png',
  'captures/20261014-full-direction/review/20261016-r3-wave3/images/027e8d6cc3e77bd29c4e73218ec970113999abb98e0523c6aca21e24f3acac0b.jpg',
  ['M14-dual-form-prompt-r1.txt'])]
items=[]
for ident,name,file,gen,source,prompts in specs:
 assert sha(OUT/file)==sha(GEN/gen)
 with Image.open(OUT/file) as im:size=list(im.size);mode=im.mode
 items.append(dict(id=ident,name=name,file=file,sha256=sha(OUT/file),pixel_size=size,mode=mode,
     generated_source=str(GEN/gen),source_reference=source,source_reference_sha256=sha(PROJECT/source),
     prompts=prompts,role='人形/航空形态同源部件首轮候选',
     user_accepted=False,runtime_integrated=False,handoff_sent=False))
observations={
 'M08':['蓝紫涂装、独立长头壳、长枪与长腿保持；座舱紫色中心和翼根圆轴在两形态可追认。',
        '航空态清楚显示双喷口；人形可见近侧后腰发动机，另一侧因投影遮挡，仍需背视核对。',
        '初稿航空枪口朝后，R1b已朝机鼻方向安装；实际是机身近侧背部导轨，不宣称已画成提示词建议的腹部中线。',
        '机鼻尖、下摆分段与折叠腿架仍需结构图收敛；双态图不证明完整变形。'],
 'M14':['保留粉白和椭圆座舱胸，与雷翎蓝紫尖锐三角翼形成区分。',
        '航空态四喷口；人形上背成对挂舱及小腿后成对喷口可读，挂舱以短支架连接。',
        '翼面、座舱/下鼻尖和两组发动机去向比原候选更清楚；完整臂腿收纳与翼根扫掠仍未验证。',
        '未增加武器或第三可玩形态；新头鳍与全形仍为候选，未替换旧Working参考。']}
production=dict(date=DATE,revision='aircraft-source-batch-20261022-r1',asset='雷翎/歌翼双形态源设计首轮',
    existing_batch='design-followthrough-r1.json',previous_delivery='M11-delivery-manifest-r9.json',
    reader=reader,generation_mode='built-in image_gen',items=items,
    original_scope=['adoption-manifest.json#M08','adoption-manifest.json#F07','adoption-manifest.json#M14','adoption-manifest.json#F08','adoption-manifest.json#N13'],
    authority_boundary=dict(leiling_entity='V353U047',songwing_working_reference='CML023',
      existing_reference_unchanged='.superpowers/brainstorm/37837-1782033239/content/mecha_r04_r18_dual_forms_v2.png',
      scope='从原外援候选修订的源设计研究；不取代Working参考或绑定新原作角色。'),
    author_review=dict(reviewer='author',independent_review=False,
      actual_media=[x['source_reference'] for x in items]+[x['file'] for x in items],
      observations=observations,
      limits=['当前只有两台各一张双态候选；未完成三视、一个可信中间态、同模型节点或连续变形。',
              '正常游戏镜头、动作/声音、输入/性能均未验证，本轮没有运行替换。',
              '新图未获用户采用；货柜领袖已确定形象不受本批候选影响。']),
    prompt_index='aircraft-source-prompts-20261022.json',
    canon_changed=False,runtime_changed=False,handoff_sent=False)
write(record,production)
write('aircraft-source-prompts-20261022.json',dict(generation_mode='built_in_image_gen',
 outputs=[dict(id=x['id'],file=x['file'],inputs=[x['source_reference']],prompts=x['prompts']) for x in items],
 correction=dict(file='samples/M08-dual-form-r1-aft-gun-attempt.png',prompts=['M08-dual-form-prompt-r1.txt'],
    result='航空态枪口朝后，已由R1b局部修正；不作为当前候选。')))
parts=[
 ('M08','座舱与机鼻','胸/腹中心的紫色舱罩和分段鼻尖','前机身连续紫色舱罩/脊线','独立头部收纳、机鼻根位待细化'),
 ('M08','主翼与双发动机','上背翼根圆轴；背架发动机','同形蓝紫翼面与双尾喷口','需背视及一个可信中间态'),
 ('M08','长枪','自身右手下垂持枪','近侧机身背部导轨，枪口朝前','候选挂点须与翼面让位'),
 ('M14','椭圆座舱与机鼻','胸部深色长舱罩、短下鼻甲','粉白前机身与深色长舱罩','下鼻甲根位/臂收纳待验证'),
 ('M14','四发动机','上背2挂舱、小腿后2喷口','外翼根2挂舱、中央2发动机','挂架与翼轴须同模型校核')]
rows=''.join('<tr>'+''.join('<td>'+html.escape(t)+'</td>' for t in row)+'</tr>' for row in parts)
figs=''.join(f'<section id="{x["id"]}"><h2>{x["name"]}</h2><figure><a href="{x["file"]}"><img src="{x["file"]}" alt="{x["name"]}人形与航空形态候选"></a></figure><p>{"；".join(observations[x["id"]][:3])}</p></section>' for x in items)
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>下一批｜雷翎与歌翼双形态候选</title><style>body{{margin:0;background:#eef0ed;color:#183142;font:16px/1.7 system-ui}}main{{max-width:1500px;margin:auto;padding:28px}}a{{color:#08617e}}nav{{display:flex;gap:24px;flex-wrap:wrap}}h1{{font-size:36px}}section{{margin-top:44px}}figure{{margin:18px 0;background:white}}img{{display:block;width:100%}}table{{border-collapse:collapse;background:white;width:100%}}td,th{{padding:12px;border-bottom:1px solid #d6dedb;text-align:left}}.scroll{{overflow:auto}}details{{margin-top:30px}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="M11-source-delivery-r9.html">货柜领袖已交付</a><a href="aircraft-source-prompts-20261022.json">内置生图提示词组</a></nav><h1>下一批：雷翎与歌翼</h1><p>先把人形和航空形态放在同一张候选板上，检查座舱、翼根、发动机和挂点。雷翎强调蓝紫、锐利与远射；歌翼保留粉白、轻快与巡演支援感。两张都是首轮候选。</p>{figs}<h2>本轮部件对应</h2><div class="scroll"><table><thead><tr><th>机体</th><th>部件</th><th>人形</th><th>航空态</th><th>仍需收敛</th></tr></thead><tbody>{rows}</tbody></table></div><p>双态图只完成造型与可见部件对应研究；三视、折叠中间态和连续变形仍需继续制作。</p><details><summary>来源与作者观察</summary><a href="{record}">源图记录</a> · <a href="aircraft-source-prompts-20261022.json">提示词索引</a><p>本轮不改变已确定的货柜领袖，也没有替换游戏运行资产。</p></details></main></body></html>'''
(OUT/reader).write_text(page)
ledger=read('design-followthrough-r1.json')
ledger['previous_production_focus_m11_r9']=ledger['production_focus']
ledger['production_focus']=dict(id='ART-AIRCRAFT-DUAL-FORM-R1-20261022',
 experience='在同一风格下辨认雷翎/歌翼，并能追认各自人形与飞行形态的关键部件。',
 current_scope='接原M08/F07、M14/F08与N13范围；本轮先画双态候选源设计，后续三视/结构不缩减。',
 source_basis=production['original_scope']+[record,'CML023','V353U047'],
 current_step='两张首轮双态候选已画并实看；雷翎航空枪向局部修正R1b。',
 finish_line='座舱/机鼻、主翼根、喷口与挂件对应可读，两台身份有区别；候选图不自动采用。',
 next='沿本组候选收敛头部/三视、隐面与一个可信折叠中间态，再制作同件模型。')
ledger['latest_aircraft_source_batch']=record
ledger['experience_record_aircraft_source_20261022']=dict(classification='experience',
 original_requirement=production['original_scope'],
 start='货柜领袖确定及修正三视交付后，接续原剩余机体清单。',
 input='逐台审原来源，用双态候选图解释座舱、主翼根、喷口和挂架；雷翎枪向错后实际局部修正。',
 visible_consequence='两台蓝紫/粉白身份有区别，关键部件更可追认；不能据此宣称变形工程完成。',
 actual_artifacts=[x['file'] for x in items],author_review=record+'#author_review',
 independent_review=False,user_acceptance=False,runtime_changed=False,
 next='三视与一个可信中间态/同件模型按原范围继续。')
defect=next((x for x in ledger['defect_ledger'] if x.get('id')=='ART-M08-RIFLE-DIRECTION-01'),None)
if defect is None:
 defect=dict(id='ART-M08-RIFLE-DIRECTION-01',defect='航空态长枪枪口与机鼻朝向相反。',attempts=[])
 ledger['defect_ledger'].append(defect)
if not defect['attempts']:
 defect['attempts']=[dict(files=['samples/M08-dual-form-r1-aft-gun-attempt.png'],observed=True,outcome='persists',result='作者看到枪口朝后。'),
    dict(files=['samples/M08-dual-form-r1b.png'],observed=True,outcome='author_observed_improvement',result='枪口改朝前，实际挂在近侧背部导轨，支架可读。')]
defect.update(current_source='samples/M08-dual-form-r1b.png',source_design_resolved=True,closed=False,
    remaining='枪轨、主翼和双发动机具体让位仍待模型核对。')
write('design-followthrough-r1.json',ledger)
decisions=read('user-art-decisions-20261016.json')
decisions['latest_aircraft_source_batch']=dict(date=DATE,record=record,reader=reader,
    scope='接续M11源交付后的雷翎/歌翼双态候选',new_images_user_accepted=False)
write('user-art-decisions-20261016.json',decisions)
# This is a later receipt for the exact R8 source, not a rewritten historical author judgement.
for n in ['M11-posture-production-r8.json','M11-posture-direction-r8.json']:
 d=read(n);d['later_user_acceptance_receipt']='M11-design-fixed-20261022.json'
 if n=='M11-posture-production-r8.json':
  d['new_images_user_accepted']=True
  for x in d['items']:x['user_accepted']=True
 else:d['new_image_user_accepted']=True
 write(n,d)
author=read('sample-author-review.json')
author['latest_aircraft_source_record']=record;write('sample-author-review.json',author)
print('Aircraft dual-form source batch started; current candidates saved in existing ledger.')

