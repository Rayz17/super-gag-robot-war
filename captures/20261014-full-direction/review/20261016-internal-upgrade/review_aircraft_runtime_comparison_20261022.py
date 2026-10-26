"""Compare the current Demo bodies with the rejected-to-replace first drafts."""
from pathlib import Path
import hashlib,html,json
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
CAPTURE=OUT/'aircraft-runtime-comparison-20261022'
DATE='2026-10-22'
RECORD='aircraft-runtime-comparison-20261022.json'
READER='aircraft-runtime-comparison-20261022.html'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads((CAPTURE/'runtime-model-captures.json').read_text())
for x in rows:
 file=PROJECT/'game-godot'/x['model'].removeprefix('res://')
 assert sha(file)==x['model_sha256'],file
 x['project_model']=file.relative_to(PROJECT).as_posix()
 x['capture_file']='aircraft-runtime-comparison-20261022/'+x['image']
 x['capture_sha256']=sha(OUT/x['capture_file'])
assets={k:[x for x in rows if x['id']==k] for k in ['leiling','song']}
findings={
 'M08':dict(name='雷翎',runtime_id='leiling',projection='Transformers / Starscream重涂喷气机谱系',
    projection_scope='项目档案只锁到喷气重涂谱系，未锁定为某个具体原作型号。',
    existing=['喙状窄头、深色红刃、背部放射翼形成鲜明大轮廓。',
              '深主色与红/象牙切面、黄胸核心已形成集中识别点。',
              '航空态有多层翼面与推进器群；具体数量与部件收纳仍需原结构工序校核。'],
    draft=['新稿独立头、长枪、紫色座舱和三角翼清楚，但整体更接近通用航空枪兵。',
           '没有提出比现用放射翼更强的轮廓记忆点，蓝紫近色使大色块层次偏弱。',
           '双喷口/翼根和枪轨可作为结构研究参考，不能据此证明整体更优。'],
    decision='保留现用人形/航空态机设，先做保形换色和材质对齐；新稿不作为整机替换母版。',
    colour_trial='维持深色航空机气质；以墨蓝/钴蓝建立清楚主块，朱红集中翼尖与少数动作部位，黄色收在胸部/传感器。具体比例待同构图色样比较。'),
 'M14':dict(name='歌翼可变机',runtime_id='song',projection='Macross / 超时空要塞可变战机与歌声支援谱系',
    projection_scope='项目R04星翼巡演的文化/可变战机投射，不照搬具体VF型号。',
    existing=['长双角、收尖面部、象牙白/红肩翼与垂翼裙甲，轮廓修长且醒目。',
              '黄色胸部核心与展开翼面形成较稳定的视觉中心。',
              '现用红白航空态与人形有同一套切色和流线关系。'],
    draft=['粉白座舱胸和四发动机分配更直白，但头胸和轮廓更普通。',
           '粉色没有当前歌翼颜色采用回执；从外援候选继续沿用，不等于符合本作当前美术方向。',
           '四挂舱可追认是结构研究收获，尚未证明比现用翼形更有角色特色。'],
    decision='保留现用头胸/肩翼/腿足和骨架，先统一红白涂装的色块与材质；新稿不作为整机替换母版。',
    colour_trial='维持象牙白为主，朱红集中胸肩与翼面，墨蓝/石墨负责关节和暗部；减少大面积冷纯白、金属碎高光与常驻划痕。')}
sources=[
 dict(file='docs/superpowers/specs/data/canon/entities.tsv',evidence='V353U047当前喷气重涂定位'),
 dict(file='docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv',evidence='CML023/R04星翼巡演当前美术参考与人物机体关系'),
 dict(file='docs/superpowers/specs/data/research/robot_culture_ip_roster_mapping_v0_1.tsv',evidence='IP005 Macross文化投射研究映射'),
 dict(file='docs/superpowers/specs/data/story/v35_3_playable_roster_expansion_v35_3.tsv',evidence='V353U016 Macross、V353U047 Starscream重涂映射；文化来源证据，不据旧首登行推进当前故事'),
 dict(file='game-godot/scripts/formula_lab/linked_campaign/campaign_world.gd',evidence='当前load_body/model_key原模型加载与cel材质绑定'),
 dict(file='game-godot/scripts/formula_lab/linked_campaign/rounds/round_world.gd',evidence='prepare_resources中的当前人形/航空态路径'),
 dict(file='docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md',evidence='Working画法：英雄色、墨线、大色块、最多两级阴影、非玩具反射')]
for x in sources:x['sha256']=sha(PROJECT/x['file'])
decision=dict(date=DATE,revision='aircraft-runtime-comparison-20261022',
    existing_batch='design-followthrough-r1.json',
    authority='direct_user_comparison_request_and_author_asset_review',
    latest_user_request='比较歌翼、雷翎的IP投射、系列/画法与现用Demo机设；若新设计不能更有记忆点/特色，优先现用资产调整配色。',
    author_verdict='两张新稿未显示足以替换当前Demo机设的优势；保留现用机设，后续先做保形配色/材质对齐。',
    projection_relation='来自两个不同IP谱系；应共享本作绘制语言，不应强行改成同机架或仅因一批制作而当成同系列。',
    runtime_models=rows,source_evidence=sources,findings=findings,
    author_review=dict(reviewer='author',independent_review=False,
      actual_media=[x['capture_file'] for x in rows]+['samples/M08-dual-form-r1b.png','samples/M14-dual-form-r1.png'],
      material_findings=['新雷翎近似蓝紫铺满、细碎高光和面板密度偏均匀。',
        '新歌翼粉白色权未经采用，造型趋于通用轻型机。',
        '现用模型机设更强，但旧贴图仍有常驻划痕、冷灰/硬白切换和局部碎反射，需按Working画法做有限材质清理。']),
    comparison_limits=['现用资产由当前游戏加载器独立取图，几何/原贴图未改；新稿是白底二维设定图。二者不具备相同光照、相机或材质条件，不据此量化实机换色效果。',
      '本轮没有重新游玩整段Demo、执行原生输入、复核连续变形或动作声音。',
      '没有修改现用模型、贴图、骨架、动作或运行入口；保形色样尚未制作。'],
    new_drafts_recommended_as_replacements=False,runtime_modified=False,canon_changed=False,
    main_thread_messaged=False,reader=READER)
write(RECORD,decision)
sections=[]
for ident,d in findings.items():
 current=next(x for x in assets[d['runtime_id']] if not x['aircraft'])
 plane=next(x for x in assets[d['runtime_id']] if x['aircraft'])
 draft='samples/M08-dual-form-r1b.png' if ident=='M08' else 'samples/M14-dual-form-r1.png'
 sections.append(f'''<section id="{ident}"><h2>{d['name']}</h2><p>{d['projection']}。{d['projection_scope']}</p><div class="pair"><figure><a href="{current['capture_file']}"><img src="{current['capture_file']}" alt="{d['name']}现用Demo人形模型"></a><figcaption>现用Demo模型 · 原几何与原涂装</figcaption></figure><figure><div class="draftbody"><img src="{draft}" alt="{d['name']}上一轮新稿的人形区域"></div><figcaption>上一轮新稿人形区域 · 原图未改</figcaption></figure></div><table><tr><th>现用设计保留价值</th><th>新稿未形成优势之处</th></tr>{''.join('<tr><td>'+html.escape(a)+'</td><td>'+html.escape(b)+'</td></tr>' for a,b in zip(d['existing'],d['draft']))}</table><p class="verdict">{d['decision']}</p><p>{d['colour_trial']}</p><details><summary>航空态与完整新稿</summary><div class="pair"><figure><img src="{plane['capture_file']}" alt="现用航空态"><figcaption>现用航空态</figcaption></figure><figure><img src="{draft}" alt="完整双态候选"><figcaption>完整新稿，保留为结构研究</figcaption></figure></div></details></section>''')
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>雷翎/歌翼｜现用Demo与新稿比较</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#edf0ed;color:#183142;font:16px/1.75 system-ui}}main{{max-width:1480px;margin:auto;padding:26px}}a{{color:#08617e}}nav{{display:flex;gap:22px;flex-wrap:wrap}}h1{{font-size:36px;line-height:1.3}}h2{{margin-top:45px}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}figure{{margin:16px 0;background:white}}img{{display:block;width:100%;height:auto}}figcaption{{padding:10px 14px;font-size:14px}}.draftbody{{aspect-ratio:1;overflow:hidden;background:white}}.draftbody img{{height:100%;width:auto;max-width:none}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{width:50%;padding:13px;text-align:left;border-bottom:1px solid #d5ded8;vertical-align:top}}.verdict{{border-left:4px solid #d6822b;background:#fff8e8;padding:16px}}.note{{color:#526a73;font-size:14px}}details{{margin:24px 0}}@media(max-width:760px){{.pair{{grid-template-columns:1fr}}main{{padding:18px}}}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="#M08">雷翎</a><a href="#M14">歌翼</a><a href="{RECORD}">来源与实际查看记录</a></nav><h1>保留现用机设，先做配色与材质对齐</h1><p>比较结果：上一轮新稿在机设记忆点上没有超过现用Demo资产。头胸、翼形和腿足先保留；后续仅从同一机体的色块、暗部、描线和反射开始比较。</p><p>雷翎投射Transformers喷气重涂谱系，歌翼投射Macross可变战机/歌声支援谱系。它们来自不同系列，应该保留各自机械语法，共享本作的动能赛璐璐画法。</p><p class="note">左图取自当前游戏加载的模型，右图为新稿局部；光照、背景与相机不同。本页比较造型和色块组织，不冒充同镜头换色前后验收。</p>{''.join(sections)}<h2>后续采用范围</h2><p>现用头胸、翼形、身体比例与骨架/动作继续保留。新稿的座舱/翼根/喷口对应作为研究材料；“部件解释更直白”不足以决定替换整机。此前头部参考建议也不再作为新头重画任务。</p><p>画法按项目Working标准：有线压的深墨蓝轮廓、各自英雄色、4—7个大色块、最多两级硬阴影、哑光大面；减少均匀小刻线、碎反光和常驻划痕。统一画法不要求同配色，也不把两台全部洗成灰蓝。</p><p class="note">本轮只做比较，未改运行资产；新色样尚未制作。模型完整变形与连续动作仍按原任务验证。</p></main></body></html>'''
(OUT/READER).write_text(page)
old=OUT/'aircraft-source-batch-20261022.html'
s=old.read_text()
if 'id="runtime-comparison-result"' not in s:
 note=f'<aside id="runtime-comparison-result"><h2>最新比较：新稿不作为替换母版</h2><p>当前Demo机设更有记忆点，先保留现用头胸/翼形/骨架，后续比较配色与材质。<a href="{READER}">查看现用模型与本轮新稿对照</a>。</p></aside>'
 s=s.replace('<h1>',note+'<h1>',1);old.write_text(s)
batch=read('aircraft-source-batch-20261022.json')
batch['later_runtime_comparison']=RECORD
batch['recommended_as_replacement']=False
batch['status']='first_drafts_retained_as_structure_studies_not_current_redesign_masters'
write('aircraft-source-batch-20261022.json',batch)
ledger=read('design-followthrough-r1.json')
ledger['latest_aircraft_runtime_comparison']=RECORD
ledger['production_focus']['current_step']='已对当前加载的人形/航空态与新稿实看比较：现用机设更有记忆点，新稿不作替换母版。'
ledger['production_focus']['experience']='在保留现用雷翎/歌翼机设的条件下，确认IP谱系与项目画法，先比较色块与材质。'
ledger['production_focus']['current_scope']='当前为现用模型/新稿比较；不重做头胸/翼形，不修改运行资产或其他会话台账。'
ledger['production_focus']['next']='以现用几何和同一姿势/机位制作有限配色材质对照；仅真实识别缺陷才触发局部机设修改。'
ledger['experience_record_aircraft_runtime_comparison_20261022']=dict(
 classification='experience',original_request=decision['latest_user_request'],record=RECORD,
 actual_media=decision['author_review']['actual_media'],
 start='用户指出新稿无特色、配色偏离且未胜过Demo现用机设。',
 input='查询IP来源和游戏加载链，原游戏渲染器只读取现用模型，完整身形/航空态与新稿逐台对照。',
 visible_result='现用轮廓更强，新稿主要是结构研究收获；停止将新稿作为下一母版继续派生。',
 next='保形配色/材质对照，待实际同镜头看图；不沿新稿重做三视。',
 author_review=RECORD+'#author_review',independent_review=False,main_thread_messaged=False,runtime_changed=False)
defect=next((x for x in ledger['defect_ledger'] if x.get('id')=='ART-AIRCRAFT-IDENTITY-ADVANTAGE-02'),None)
if defect is None:
 defect=dict(id='ART-AIRCRAFT-IDENTITY-ADVANTAGE-02',defect='重画稿未比现用Demo机设更有记忆点，且配色/细节层级偏离项目画法。',attempts=[])
 ledger['defect_ledger'].append(defect)
if not defect['attempts']:
 defect['attempts'].append(dict(files=['samples/M08-dual-form-r1b.png','samples/M14-dual-form-r1.png'],observed=True,
    outcome='persists',result='对现用完整模型比较，新稿未形成替换优势，保留为结构研究。',evidence=RECORD))
defect.update(closed=False,method_changes=[dict(status='planned',
 old='沿外援候选继续重画完整机设，再补变形部件解释。',
 new='先保留现用模型，做同几何/机位配色材质对照；需要时再局部改形。',
 reason='用户反证且实看比较未见整机优势，不为重做而重做。',
 evidence=RECORD,retest='现用、保形换色两版本同模型同机位/光照并看；色样未做不能记为改善。')],
 remaining='保形色样与材质统一尚未实际制作；本轮不宣称改善已完成。')
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_aircraft_runtime_comparison']=RECORD
write('sample-author-review.json',author)
decisions=read('user-art-decisions-20261016.json')
decisions['latest_aircraft_comparison_feedback']=dict(date=DATE,record=RECORD,
    request='若新稿不能超过现用机设的记忆点/特色，优先现用资产换色。',
    author_recommendation='保留现用机设，先做配色/材质对照。',new_body_redesign_selected=False)
write('user-art-decisions-20261016.json',decisions)
print(json.dumps(dict(reader=str(OUT/READER),existing_models_checked=len(rows),runtime_assets_modified=False),ensure_ascii=False))

