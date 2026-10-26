"""Append the user's background and design-to-model requirements to this handoff."""
import copy, csv, hashlib, html, json
from pathlib import Path
from brief_profiles import PROFILES, FORM_PARENTS, ORIGINALS, SOURCES

REVISION = '20261013-r2-background-orthographic'
MODEL_TEMPLATES = {'mecha','enemy','form','part','building'}
FILE_INFO = {
 'concept.png': ('01 设定与形象', '主设定图：展示角色性格、IP血统、主色块与完整轮廓；不是三视图', '长边3072–4096；姿势清楚、装备不互相遮断'),
 'design_master.png': ('02 结构母版', '选定的一套设计：中性姿态、完整身体、装备位置和材料分区', '长边3072–4096；无强透视、无爆光、无大面积遮挡'),
 'design_record.json': ('02 结构母版', '设计版本、来源、部件编号、对称/不对称、显示档、未解决问题及结构复核记录', '真实填写；与母版/各视图使用同一design_id和revision'),
 'design_views.png': ('03 正交视图', '前/右侧/后对齐总板；同一设计、相同单位比例；需要的左侧/顶视附旁', '总板长边4096–6144；标视向、地面线、中心线与主要关节高度'),
 'ortho_front.png': ('03 正交视图', '正面正交视图', '默认2048×3072；不透视、不作动态姿态；同设计单位/像素比例'),
 'ortho_right.png': ('03 正交视图', '机体自身右侧正交视图，不是画面右边的随意侧脸', '默认2048×3072；机翼/载具可3072×2048，须与其他视图同一比例'),
 'ortho_back.png': ('03 正交视图', '背面正交视图：背负结构、关节、收纳和接缝可读', '默认2048×3072；不得用另一张随意生图替代同一身体背面'),
 'ortho_left.png': ('03 正交视图', '因左右不对称追加的左侧正交视图', '与右侧同单位比例；不能简单镜像右臂/武器'),
 'ortho_top.png': ('03 正交视图', '俯视：宽度、纵深、翼/炮/载具布局', '默认3072²；与前/侧/后同单位比例，不独立拉伸填满画布'),
 'front.png': ('03 正交视图', '建筑/静物正立面', '长边3072–4096；所有立面共用地面线、层高和单位比例'),
 'side.png': ('03 正交视图', '建筑/静物右侧立面', '与正/背/顶的深宽高严格对应；有不对称时补左侧'),
 'back.png': ('03 正交视图', '建筑/静物背立面', '不可将正面复制成背面；设备、门窗、管线有来源'),
 'top.png': ('03 正交视图', '建筑/静物正交顶视平面', '与立面同尺度；屋顶厚度、楼梯、设备和缺口对应'),
 'assembly_and_parts.png': ('04 分件与状态', '楼层、外壳、屋顶、必要活动件的装配和轴示意', '3072–4096；只画建模/状态表达需要的结构，不做柜内接线工程图'),
 'damage_structure.png': ('04 分件与状态', '破损/倒塌改变的体积、断面与楼板；与完整母版重叠对照', '3072–4096；至少正面与顶视及必要侧剖；标明消失/留下/新露出的部分'),
 'head_and_connections.png': ('04 分件与状态', '头部正侧背、肩胯膝踝和武器连接', '关键形态/活动方向清楚；无需为每一对敌我单位调接触点'),
 'connections.png': ('04 分件与状态', '母体与分件接口、装配方向、展开/分离轴', '沿用母版零件编号和长度单位'),
 'transition_sheet.png': ('04 分件与状态', '同一套零件在形态A/中间态/形态B中的位置对应', '3072–4096；不凭空增减机翼、车轮、四肢或合体核心'),
 'mount_and_motion.png': ('04 分件与状态', '工具挂点、收纳、伸出/转轴和动作范围', '主体接口与器具根部均画出；发射方向明确'),
 'reuse_sources.json': ('04 分件与状态', '母件复用与差分来源表；明确哪些视图/部件来自同一母版', '记录实际源文件、design_id、revision、零件ID；不可写“差不多同款”'),
}

PIPELINE_TEXT = '''# 背景、IP与设定图到三视图的制作要求

本补充自2026年10月13日生效，纳入原298项清单，不另立一份资产范围。《给Astra的视觉总参考》保持原样。补充的是外援制作时必须知道的身份，以及能让后续模型真正照图实现的结构资料。

## 先知道在画谁

每台机体先读本项的“IP映射、映射确定程度、项目背景、应保留特征、项目改造、不能画错、来源”。人物先读真实姓名/文化背景、职业、性格和与机体的关系。背景不能从旧头像猜，也不能只用“白色科幻机器人”等泛词开画。

人物与机体背景取当前Canon。Roster和IP研究表在这里用于查设计血统，其旧章节安排、尚未采纳技能或入队规则不自动有效。项目原创人物不硬配外部角色；未锁定单一机型的作品家族不硬写成一对一原型。

有明确IP来源时，生图提示词必须同时写：作品/谱系名；实际参考的原机例图；至少三项识别特征；本作身份与职业；本作改变的结构；用户明确不能画错的部位。原IP例图解释“像哪一族”，固定美术参考解释“用什么画法”。两者都要用，不能用统一机甲风洗掉各IP，也不能直接复制原作整机后改名。

已核实的官方参考链接列在各项；下载包中的项目旧图只用于身份辨认。Real Steel等已在项目确认来源但本包未附官方原机图的对象，制作前须另找实际图像参考并在回传里记录网址/出处和用途，不能谎称已经看图。不可自行将“参考某角色”写成该项目人物的正式身份。

## 一条完整的制作顺序

1. **设定图**：先画出本项的身份、气质、完整轮廓、主色块、武装和正常战棋距离的可读性。交concept.png。已有明确方向只深化该方向，不重新海选画风。
2. **结构母版**：把选定设计整理成中性站姿/收纳姿态，确定头胸、关节、四肢、装备与接口，交design_master.png和design_record.json。这里的“定稿”指制作者冻结一个可追溯设计版本，不等于用户已经认可。
3. **同源正交三视图**：根据这一个母版制作正、右侧、背三张独立图，以及对齐总板design_views.png。所有视图必须是同一身体、同一装甲分区、同一装备和同一设计版本。
4. **分件与状态**：补头部、关节、武器挂点、收纳和活动轴；变形/合体有零件迁移表；损毁有实际断面和残留结构。只解决可见形态与动画所需信息，不做无法在游戏感知的精密接触工程。
5. **建模**：接入方或受委托的三维外援按上述资料搭低模；先在正常镜头核对整体体积，再看三视叠合、旋转预览、接缝和必要活动件，发现源图互相矛盾先修设计，不让模型随意猜。
6. **UV、贴图与材质**：形体稳定后展开实际UV，把设定图的造型、图案和材质转入真实网格；分别交底色和实际使用的材质通道。正面插画不能冒充UV贴图；复杂受光不永久烘焙到基色。
7. **绑定与演出接入**：标准动作按骨架家族重定向；无牌天冲拳、旧拳王体术等才定制关键动作。静物仅必要轴；列车整体移动、转台旋转、柜体灯光/状态反馈即可。动作事件由双方各处理自己的状态，不建立机体×目标的逐对接触参数。

Grok只承担二维时，步骤1–4是必交，步骤5–7明确留给项目接入方。若它同时承接模型/蒙皮/动作，则追加技术附包；不能把二维包写成“三维已完成”。

## 三视图怎样才有用

- 同一中性A姿或既有骨架适配姿势；脚底同基线，头顶、肩、肘、腕、胯、膝、踝高度对齐。非人形用中心体、支撑点、关节和攻击器官代替人体标尺。
- 不作透视缩短、广角、低角度、跨步动作或强光遮形。每张独立图保持同一像素/设计单位比例，留白可以不同；不能把三个视图各自拉满画布，导致侧面厚度忽大忽小。
- “右侧”指对象自身右侧。前图与背图的左右不可混淆。主色和部件编号逐面一致，左右不对称必须画明。没有画到的背面、底面和挂点写成缺件，不能让建模猜。
- 可用全高1000设计单位建立共同标尺；真实设定米数用于背景，战棋显示按微型、小型单格、标准单格、2×2、3×3与巨构局部档。敌我同档使用相近视觉份量。
- 镜像只可用于确定对称的结构。馆守的缺右臂、王者的右臂钻、非对称吊臂不能镜像偷换。王者额角在正/侧/顶视交叉核对，双炮前向与肩背转轴必须一致。
- 允许生成草稿后用编辑、绘制、模型投影辅助统一视图；“提示词相同”不是同一设计的证据。明显不同的头型、胸甲、膝盖、炮数或翼根必须先修正。

## 哪些对象要补哪些图

| 对象 | 必需结构资料 | 复用边界 |
|---|---|---|
| 可建模机体、常规敌体 | 设定、母版、正/右/背、对齐板、头关节/器官/挂点 | 同一母版派生立绘、头像和损伤，不各生一台 |
| 非对称机体与武器 | 上述资料，加左侧；背包/巨钻/宽翼另加顶视 | 左右差异必须标注，不用镜像抹掉 |
| 变形机 | 每个已列形态的正/侧/背/顶与中间态、零件迁移表 | 两形态同一机体，不凭空换零件；不新增未委托形态 |
| 合体机 | 完整核心、外部组件和合体各自视图；装配和分离方向 | 社勇王核心始终完整；重叠交付可从母版导出，不重复设计收费 |
| 建筑、电力/工程设施、列车 | 设定、母版、前/侧/背/顶、层高/底座/部件、战棋角度 | 静物不用人形骨架；列车只拆需要动的部分 |
| 受损楼房与破坏设施 | 完整母版加破损结构板、必要正面/顶视/侧剖及状态图 | 屋顶/楼层实际缺失，禁止在残楼盖一整张完整屋顶 |
| 武器、工具、可拆包 | 正/侧/背，必要顶视、挂点与轴 | 从所属机体分件导出并补被遮挡面；不重新设计另一把武器 |
| 地形与材质 | 平面、边缘断面、可见高度和状态资料 | 纯表面材质不强迫画机体三视；破口与立面要有结构 |
| 人物头像/立绘/表情 | 人物母版、头部角度、服装与表情一致性 | 纯二维用途不做无用三维附包；实际要建模的地图人物另补其简化三视 |
| 光效、图标、HUD | 时序、分层、尺寸、状态和坐标说明 | 不强套设定—三视—建模流程 |

## 建模前的结构复核

制作者对母版与正/侧/背图逐项看：零件数量、主色分区、左右差异、关节位置、武器根部、遮挡面、变形迁移。回传design_record.json写明每项实际检查结果、采用版本和仍不确定处，并附同页对齐图。结构不一致时继续修图，不把“模型师自行理解”当作交付。

这项内部检查不是每批让用户来补漏。源图仍有问题就留needs_revision，不把未做或未看过的检查写成通过。用户最终美术认可、项目建模接收和游戏体验验收分别保留，不代签。

三维附包必须含source_design.json：design_id、revision、依据的母版与各视图文件路径及sha256、实际省略或改动说明。模型turntable与对齐对照证明形体继承；实际动画、声音和游戏使用由主对话继续验收。文件数量与自动校验不等于好看。

## 交付位置与版本

保持原编号，最终交incoming/编号/。修订过程放grok-delivery/iterations/编号/版本/，不要覆盖可回溯的旧版本。共享家族在reuse_sources.json注明母版、具体零件和派生关系；三视图、头像与立绘必须指向同一个design_id/revision。

Grok最终在grok-delivery/回传清单.json、制作报告.md和review/index.html中标清：二维设计完成到哪一步、是否做过模型、哪些结构仍待解决。阅读页每项展示IP/背景要点、参考→设定→三视对照→成品，不只排一墙漂亮成图。主对话据此先检查再接入，不能直接拿新插画覆盖GLB或材质。
'''

def add_specs(specs):
 for template in MODEL_TEMPLATES:
  label,size,names,boundary=specs[template]
  extra=['concept.png','design_master.png','design_record.json','reuse_sources.json']
  if template!='building': extra+=['ortho_front.png','ortho_right.png','ortho_back.png']
  specs[template]=(label,size,list(dict.fromkeys(extra+names)),boundary+' 必须先完成同源设定母版和正交结构交接，详见背景与三视图制作规范。')

def extra_outputs(row):
 names=[]
 if row['template'] in {'mecha','enemy','form','part'}:
  if row['key'] in {'guardian','king','crane','police','cargo','king_light','king_drill','brave_core','brave_combined'}:
   names.append('ortho_left.png')
  if row['template'] in {'enemy','form','part'} or row['key'] in {'king','crane','leiling','cargo','mirror','song','old_guardian'}:
   names.append('ortho_top.png')
 if row['template']=='building':
  if any(s in row['states'] for s in ['受损','毁坏','坍塌','断裂']):names.append('damage_structure.png')
 return names

def attach_profiles(rows):
 key_to_id={r['key']:r['id'] for r in rows if r['group'] in {'M','E','H'}}
 for r in rows:
  if r['group'] in {'M','E','H'}:
   assert r['key'] in PROFILES, (r['id'],r['key'])
   r['identity']=copy.deepcopy(PROFILES[r['key']])
  elif r['group']=='F':
   parents=FORM_PARENTS[r['key']]
   ps=[PROFILES[k] for k in parents]
   r['identity']={
    'ip_mapping':'；'.join(dict.fromkeys(p['ip_mapping'] for p in ps)),
    'mapping_status':'继承所属主体；共享工具可跨列出的使用者，部件不算新角色',
    'background':' / '.join(key_to_id[k]+'：'+PROFILES[k]['background'] for k in parents),
    'retain_features':'沿用对应母机的造型血统、涂装、零件身份和当前剧情状态。'+r['design'],
    'project_design':'从母机结构设计派生，补独立状态和原先遮挡的表面。使用reuse_sources.json关联同一设计版本；不因拆成清单项而重画另一套。',
    'avoid':'合体、变形与拆卸不能凭空更换头胸或增减零件；不可从母体单张动作图猜背面。',
    'source_refs':list(dict.fromkeys(tuple(s) for p in ps for s in p['source_refs'])),
    'original_reference_keys':list(dict.fromkeys(k for p in ps for k in p['original_reference_keys'])),
    'parent_items':[key_to_id[k] for k in parents],
   }
  else: continue
  r['identity']['original_references']=[dict(key=k,title=ORIGINALS[k][0],url=ORIGINALS[k][1],look_for=ORIGINALS[k][2]) for k in r['identity']['original_reference_keys']]
  r['identity']['source_refs']=[dict(source=k,path=SOURCES.get(k,''),locator=selector) for k,selector in r['identity']['source_refs']]
  r['identity']['brief_revision']=REVISION

def profile_html(row):
 p=row.get('identity')
 if not p:return ''
 e=html.escape
 links=''.join(f'<li><a href="{e(x["url"])}" target="_blank" rel="noopener">{e(x["title"])}</a> — {e(x["look_for"])}</li>' for x in p['original_references'])
 parent=' / '.join(f'<a href="#{x}">{x} 母机背景</a>' for x in p.get('parent_items',[]))
 source=''.join(f'<li><code>{e(x["path"] or x["source"])}</code> · {e(x["locator"])}</li>' for x in p['source_refs'])
 return f'''<div class="identity-panel"><p><strong>IP映射：</strong>{e(p['ip_mapping'])}</p><p class="caption">{e(p['mapping_status'])}</p><p><strong>本作背景：</strong>{e(p['background'])}</p><p><strong>保留的识别与性格：</strong>{e(p['retain_features'])}</p><p><strong>本作设计落点：</strong>{e(p['project_design'])}</p><p><strong>不能画错：</strong>{e(p['avoid'])}</p>{parent}<details><summary>背景出处与原IP看图入口</summary><ul>{links or '<li>本包未附该项官方图像入口。按明确IP来源补实际参考，并在回传记录；原创项不硬配其他作品角色。</li>'}</ul><ul class="file-list">{source}</ul><p><a href="source-notes/背景与IP来源摘录.json">查看随包来源摘录</a> · <a href="背景与三视图制作规范.html#sources">怎样区分当前身份、旧Roster与视觉参考</a></p></details></div>'''

def pipeline_html(row):
 if row['template'] not in MODEL_TEMPLATES:return ''
 return '<p class="pipeline-inline"><strong>必交制作链：</strong>设定 → 结构母版 → 同源正交视图 → 分件/状态 → 建模交接。<a href="背景与三视图制作规范.html#turnaround">看对齐与验收要求</a>；不是三张独立生图拼板。</p>'

def delivery_info(row,filename):
 if filename in FILE_INFO:return FILE_INFO[filename]
 return ('05 用途成品与状态','',None)

def export_backgrounds(root,out,rows,copy_reference):
 records=[]
 for r in rows:
  if 'identity' in r: records.append({'id':r['id'],'name':r['name'],**r['identity']})
 (out/'背景与IP映射.json').write_text(json.dumps({'revision':REVISION,'note':'本委托的来源摘要和设计解释；不写回Canon。IP例图不是项目机型定稿。','items':records},ensure_ascii=False,indent=2))
 with (out/'背景与IP映射.csv').open('w',encoding='utf-8-sig',newline='') as f:
  fields=['编号','对象','IP映射','确定程度','本作背景','应保留特征','本作设计','不能画错','母机','来源','原作图像入口']
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for p in records:
   w.writerow(dict(zip(fields,[p['id'],p['name'],p['ip_mapping'],p['mapping_status'],p['background'],p['retain_features'],p['project_design'],p['avoid'],' / '.join(p.get('parent_items',[])),'\n'.join(s['path']+' # '+s['locator'] for s in p['source_refs']),'\n'.join(x['url'] for x in p['original_references'])])))
 excerpts={}
 for key in ['canon','roster','ip','locks']:
  path=root/SOURCES[key]
  selectors={s['locator'] for p in records for s in p['source_refs'] if s['source']==key}
  with path.open() as f: selected=[r for r in csv.DictReader(f,delimiter='\t') if any(s in r.values() for s in selectors)]
  excerpts[key]={'source':SOURCES[key],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'use':'只读取本包引用的条目；旧Roster时序不代表当前剧情','rows':selected}
 (out/'source-notes/背景与IP来源摘录.json').write_text(json.dumps(excerpts,ensure_ascii=False,indent=2))
 for key in ['authority','culture']:
  copy_reference(root/SOURCES[key],'source-notes/'+Path(SOURCES[key]).name)
 (out/'背景与三视图制作规范.md').write_text(PIPELINE_TEXT)
 (out/'设计版本记录模板.json').write_text(json.dumps({
  'template_only':True,'asset_id':'填写实际编号','design_id':'填写稳定设计ID','revision':'r01',
  'identity_and_ip':{'project_background_source':[],'original_ip_family':'','mapping_certainty':'','reference_images_actually_used':[], 'features_preserved':[], 'project_changes':[]},
  'design_files':{'concept':'concept.png','master':'design_master.png','aligned_sheet':'design_views.png','orthographic':[]},
  'space':{'unit':'设计单位，例如全高1000','pixels_per_design_unit':None,'pose':'','right_means':'对象自身右侧','ground_line_px':None,'landmark_heights':{},'display_class':'','dcc_forward_axis':'','dcc_up_axis':''},
  'parts':[],'asymmetry':[],'form_links':[],'open_questions':[],
  'structural_review':{'reviewer':'填写实际检查者','date':'','status':'not_reviewed','parts_consistent':None,'landmarks_aligned':None,'mounts_clear':None,'asymmetry_correct':None,'evidence_files':[]},
  'project_intake':'not_reviewed','user_art_acceptance':'not_recorded',
 },ensure_ascii=False,indent=2))
 return len(records)

def guide_html(out):
 # A small schematic teaches alignment; it is deliberately not a target art design.
 svg='''<svg viewBox="0 0 900 270" role="img" aria-label="正面、右侧、背面须共用头顶肩胯膝脚底线"><rect width="900" height="270" fill="#edf0ec"/><g stroke="#80998f" stroke-dasharray="6 6"><path d="M30 44H865 M30 93H865 M30 150H865 M30 204H865 M30 241H865"/></g><g fill="#527184" stroke="#203e50" stroke-width="2"><g transform="translate(160)"><rect x="-17" y="44" width="34" height="39"/><path d="M-43 93H43L33 151H-33Z"/><rect x="-62" y="93" width="16" height="77"/><rect x="46" y="93" width="16" height="77"/><path d="M-31 153H-5V241H-42V228H-29V204Z M5 153H31L29 204V228H42V241H5Z"/></g><g transform="translate(435)"><rect x="-17" y="44" width="35" height="39"/><path d="M-20 93H24L20 150H-17Z"/><rect x="-9" y="93" width="16" height="77"/><path d="M-16 153H18L14 204V227H32V241H-16Z"/></g><g transform="translate(710)"><rect x="-17" y="44" width="34" height="39"/><path d="M-43 93H43L33 151H-33Z"/><rect x="-62" y="93" width="16" height="77"/><rect x="46" y="93" width="16" height="77"/><path d="M-31 153H-5V241H-42V228H-29V204Z M5 153H31L29 204V228H42V241H5Z"/></g></g><g fill="#233f4e" font-family="sans-serif" font-size="17" text-anchor="middle"><text x="160" y="26">正面</text><text x="435" y="26">自身右侧</text><text x="710" y="26">背面</text></g></svg>'''
 # Render the authored Markdown into a lightweight standalone HTML without dependencies.
 e=html.escape; parts=[];table=False;lst=False
 for line in PIPELINE_TEXT.splitlines():
  if not line.strip():
   if lst:parts.append('</ul>');lst=False
   if table:parts.append('</tbody></table></div>');table=False
   continue
  def inline(s):return __import__('re').sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',e(s))
  if line.startswith('# '):parts.append('<h1>'+inline(line[2:])+'</h1>')
  elif line.startswith('## '):
   name=line[3:];ident='turnaround' if '三视图怎样' in name else ('sources' if '先知道' in name else '')
   parts.append(('<h2 id="'+ident+'">' if ident else '<h2>')+inline(name)+'</h2>')
   if ident=='turnaround':parts.append(svg+'<p class="caption">比例检查示意，不是机体设定稿。实际图需包含真实轮廓与装备；关节、装甲、左右侧必须逐项对应。</p>')
  elif line.startswith('|'):
   if set(line.replace('|','').strip()) <= {'-',' '} :continue
   cells=[inline(x.strip()) for x in line.strip('|').split('|')]
   if not table:parts.append('<div class="table-scroll"><table><tbody>');table=True
   parts.append('<tr>'+''.join('<td>'+x+'</td>' for x in cells)+'</tr>')
  elif line.startswith('- '):
   if not lst:parts.append('<ul>');lst=True
   parts.append('<li>'+inline(line[2:])+'</li>')
  else:parts.append('<p>'+inline(line)+'</p>')
 if lst:parts.append('</ul>')
 if table:parts.append('</tbody></table></div>')
 (out/'背景与三视图制作规范.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>背景与三视图制作规范</title><style>body{margin:0;background:#f4f1e9;color:#253747;font:17px/1.85 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}main{max-width:1040px;margin:auto;padding:35px 26px 90px}h1{font-size:32px}h2{margin-top:45px;font-size:24px}a{color:#176378}strong{color:#305d6c}li{margin:12px 0}svg{width:100%;height:auto}table{border-collapse:collapse;min-width:660px}td{padding:14px;border:1px solid #c6d0cb;vertical-align:top}tr:first-child{font-weight:bold;background:#dce4de}.table-scroll{overflow-x:auto}.caption{font-size:14px;color:#5d6e74}.flow{display:flex;gap:10px;flex-wrap:wrap;padding:20px 0}.flow span{padding:10px 16px;background:#dfe8df;border-bottom:3px solid #558673}nav{display:flex;flex-wrap:wrap;gap:14px}code{overflow-wrap:anywhere}</style><main><nav><a href="index.html">返回逐项清单</a><a href="背景与IP映射.csv">背景/IP表</a><a href="设计版本记录模板.json">设计记录模板</a><a href="给Grok的完整制作提示词.md">Grok完整委托提示词</a></nav><div class="flow"><span>身份/IP</span><span>设定</span><span>结构母版</span><span>同源三视</span><span>分件/状态</span><span>建模</span><span>材质/动作</span></div>'''+''.join(parts)+'</main></html>')

GROK_ADDENDUM = '# 已整合为首次委托提示词\n\n外援任务尚未发送给Grok。请只使用[给Grok的完整制作提示词](给Grok的完整制作提示词.md)，其中已包含首次委托、背景/IP、三视图、质量要求和交付位置；无需再单独发送本补充稿。\n'

MAIN_ADDENDUM = '''接收美术外援补强包，继续当前主任务，不重置现有批次或完整整改范围。

先读项目AGENTS.md和制作方法，按当前任务要求运行preflight；再读外援美术制作清单-20261012内更新的README、背景与三视图制作规范、背景与IP映射、逐文件清单，以及grok-delivery的回传清单/制作报告/review页面。保持用户指定视觉总参考。

先核对每项IP血统与本作背景，再核对设定母版和正/侧/背是否为同一设计。查看装备挂点、左右不对称、变形/合体对应、建筑完整与破损断面。M15是馆守Z终端，不是新角色；王者右臂钻与双肩背炮方向必须符合用户要求。不要因文件齐全就认定三视结构正确。

二维成品、可建模结构交接、已制作模型、游戏接入是四个不同状态。三维未做就按同源三视完成低模→UV/真实贴图→必要绑定和动作，不能再从单张立绘猜模型；已有合格模型优先复用。新图不能直接冒充UV贴图或覆盖GLB。标准动作使用家族复用，只有招牌体术定制；单位各自响应事件，不做双方逐对精确接触。静物只保留必要活动件。

按原接入映射在主工程逐批替换，保持当前相机、占格/显示档和既有功能；正常战棋镜头核对配色、建筑比例、轮廓、材质层次、头像与立绘一致性，连续检查行动、特效和状态变化。沿用主台账记录真实结果，不把外援收货当完整52包整改完成，不替用户签好看或好玩。缺件保留精确编号和恢复位置，继续其他可做部分。
'''
