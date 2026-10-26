#!/usr/bin/env python3
"""Build this local art handoff only. Never edit runtime, Canon or production ledgers."""
from pathlib import Path
import csv, hashlib, html, json, re, shutil, zipfile
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
from brief_pipeline import (REVISION, SOURCES, FILE_INFO, add_specs, extra_outputs,
 attach_profiles, profile_html, pipeline_html, delivery_info, export_backgrounds,
 guide_html, GROK_ADDENDUM, MAIN_ADDENDUM)

OUT = Path(__file__).resolve().parent
ROOT = next(p for p in OUT.parents if (p / 'game-godot/project.godot').is_file())
PLAN = ROOT / 'docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate/v5完整整改计划-20261008'
GAME = 'game-godot/'
SC = GAME + 'scripts/formula_lab/linked_campaign/'
A = GAME + 'assets/formula_lab/'
V6 = A + 'linked_campaign_v6/'
V4 = A + 'linked_campaign_v4/models/'
ROWS = []
REFS = []
GROUPS = {
 'M': '01 我方机体与既有剧情机体', 'F': '02 变形合体及装备',
 'E': '03 敌种与非我方单位', 'H': '04 人物头像立绘与表情',
 'B': '05 建筑设施与简单运动物件', 'T': '06 地形与材质',
 'S': '07 战场构图与剧情大图', 'X': '08 战斗特效',
 'C': '09 持续状态与环境响应', 'G': '10 棋盘提示图形',
 'U': '11 界面组件', 'I': '12 技能与功能图标',
 'N': '13 动作复用与必要定制'
}
SPECS = {
 'mecha': ('机体成套图', '设定图长边3072–4096；立绘2048×3072透明；半身2048²；头像1024²；可编辑分层源', ['design_views.png','head_and_connections.png','parts_and_palette.png','stand.png','bust.png','portrait.png','state_sheet.png','source.psd'], '二维外援完成造型、各用途图与分层；低模、UV、骨架适配和导出由接入方完成。若委托三维，则追加TECH-UNIT。'),
 'enemy': ('敌种成套图', '三视与动作设计长边3072；头像1024²；透明底；可编辑源', ['design_views.png','anatomy_and_palette.png','windup_attack_recover.png','damage_sheet.png','portrait.png','source.psd'], '同骨架可复用，但核心轮廓、攻击器官和准备姿态须能区分；三维接入追加TECH-UNIT。'),
 'form': ('形态与分件图', '结构板长边3072–4096；展示图2048×3072透明；可编辑源', ['design_views.png','connections.png','transition_sheet.png','stand.png','portrait.png','source.psd'], '与所属母版共用涂装和零件身份；形态切换/分件尺寸不能靠缩放糊弄。'),
 'part': ('武器与工具图', '结构图长边2048–3072；部件透明图2048²；可编辑源', ['design_views.png','mount_and_motion.png','condition_sheet.png','isolated.png','source.psd'], '关节、挂点与运动轴由图说明；游戏侧负责实际分件和事件驱动。'),
 'human': ('人物成套图', '全身2048×3072；对话2048²；头像1024²；统一眼线/下颌/脚点；透明底和分层源', ['identity_views.png','stand_neutral.png','stand_action.png','source.psd'], '各表情分别交对话半身和头像导出；共用一份脸与服装母版，导出数不等于独立重画数。'),
 'crowd': ('小单位与人群', '设定板3072；透明组合2048²；独立人物可拆', ['design_sheet.png','map_silhouettes.png','reaction_sheet.png','source.psd'], '约四分之一格面积只用于人/机器犬等微型显示档；实际占格仍由规则决定。'),
 'building': ('建筑设计与状态图', '长边3072–4096；立面/侧背/屋顶分开；透明物件与分层材质源', ['front.png','side.png','back.png','top.png','assembly_and_parts.png','materials_source.psd','tactical_view.png'], '图先行→低模体积→UV/贴图→必要活动件。损毁态有独立体积与断面；三维交付追加TECH-ENV。'),
 'terrain': ('地形结构与材质', '2048²可平铺表面；结构板3072；分层材质源；可见几何另做', ['surface_basecolor.png','edge_and_section.png','variation_sheet.png','state_sheet.png','source.psd'], '不把阴影/凹凸全画在平面；高度、破口、桥边保留几何。法线/粗糙度按具体模型制作，不能随机套图。'),
 'scene': ('场景构图与分层大图', '3840×2160；分层PSD/KRA；前中后景、角色/机体、光效独立', ['composition.png','color_key.png','final.png','layer_map.png','source.psd'], '地图构图图是搭场依据，不能整张贴为可旋转战场。剧情图留出字幕与镜头移动余量。'),
 'fx': ('效果设计与素材', '分镜长边2560；独立粒子/片元512–1024透明；源文件；动画说明', ['phase_sheet.png','elements.png','timing.json','source.psd'], '二维外援交设计、分层片元和时序；技术特效方做粒子/材质/拖尾。不是所有效果都画整张序列帧。'),
 'graphic': ('战术图形', 'SVG可编辑；48/96/192px验看；地面/世界/屏幕三种坐标说明', ['symbols.svg','state_sheet.png','in_context.png','placement.json'], '数值、方向、脚印、曲线长度由规则生成；外援设计图形语言，接入方实现实际几何与遮挡。'),
 'ui': ('界面组件', 'SVG或设计源；1440×900与1920×1080页面稿；1×/2×导出；9-slice边距', ['component.svg','states.png','layout_1440.png','layout_1920.png','layout.json'], '普通/悬停/选中/按下/不可用/焦点按适用状态交付。中文、数字、快捷键不烘焙到图片。'),
 'icon': ('独立图标', 'SVG；48/96/192px透明PNG；单色/双色读得清', ['icon.svg','icon_48.png','icon_96.png','icon_192.png'], '用动作动词和装备轮廓识别；费用、伤害和状态叠层由UI另画。'),
 'motion': ('共享动作设计', '关键姿态板与动作引用；专业动画方可交.blend/.glb及30/60fps预览', ['poses.png','events.json','reuse_notes.md'], '标准动作按骨架家族重定向；不按双方对象逐对制作。专属动作才做独立剪辑。')
}
add_specs(SPECS)

def assets(*paths):
 return [p for p in paths if p and (ROOT/p).is_file()]

def add(group, key, name, purpose, design, states='', current=None, hooks=None,
        template=None, scope='当前工务城及其已列专关', expressions=None, components=None):
 code=f'{group}{sum(r["group"]==group for r in ROWS)+1:02d}'
 template=template or {'M':'mecha','F':'form','E':'enemy','H':'human','B':'building','T':'terrain','S':'scene','X':'fx','C':'fx','G':'graphic','U':'ui','I':'icon','N':'motion'}[group]
 ROWS.append(dict(id=code,group=group,key=key,name=name,purpose=purpose,design=design,
  states=[s for s in states.split('；') if s], current_assets=current or [], code_hooks=hooks or [],
  template=template,scope=scope,expressions=expressions or [],components=components or [],
  reference={'M':'02-mech-hero.jpg','F':'02-mech-hero.jpg','E':'03-combat-readout.jpg','H':'04-pilot-portrait.jpg','B':'11-tactics-user-accepted.png','T':'11-tactics-user-accepted.png','S':'01-battlefield.jpg','X':'10-cutin-flash.jpg','C':'03-combat-readout.jpg','G':'03-combat-readout.jpg','U':'11-tactics-user-accepted.png','I':'03-combat-readout.jpg','N':'02-mech-hero.jpg'}[group]))
 return ROWS[-1]

mecha = [
 ('hero','无牌一号','游击体术','轻灵、可读的人形关节；拳脚是第一识别点，肩胯留活动空间；天冲拳要帅且完整，不为科技感乱加炮口','普通；蓄劲；护势；轻损；失能'),
 ('boxer','旧拳王','重心拳击','拳套/前臂、胸腹与低重心形成主轮廓；拳击手的肩胯关系明确；旧不等于污脏颗粒堆满','普通；接拳；重拳预备；轻损；失能'),
 ('guardian','馆守 Z','独臂守护、牵引、承重','保留馆守身份锚和当前剧情原右前臂毁损；不能为对称补出完整右拳。左臂的牵引/支撑构造读得清','普通；支撑；牵引；受损；失能'),
 ('brave','社勇王','勇者救援与破围','与勇拳核心、外部腿架和肩包使用同一设计；英雄大色块、拳甲和胸部焦点明确，不是一团金属碎件','普通；护路；终式预备；受损；失能'),
 ('king','完全版王者','2×2飞行重装','帅气对称头部；保留冗余武装的魅力；面罩去典型嘴部刻槽；右手/右前臂连接巨钻；双背炮有肩背轴且朝前；翼与推进包逻辑一致','全装备；部分卸装；轻装；蓄炮；受损；失能'),
 ('engineer','预算二号','精密快修与液压顶推','小而精悍的工程机身份；液压顶具、备件匣、工具臂可辨；不是拿枪换名字；和消防、吊装机明显不同','普通；顶推；焊补；备件耗尽；受损'),
 ('crane','市政吊装机','吊运、牵引、承重','吊臂根部、绞盘、配重与支脚可信；吊钩与操作者同源，不从空中凭空生成','收臂；展开；吊载；停机；受损'),
 ('leiling','雷翎','空中狙击与爆破导弹','狙击长轴和轻快飞行轮廓；光束发射器与导弹挂架分清；不能与白色样机共用同一剪影','普通；瞄准；低空；变形；受损'),
 ('police','灰崎警备劳务机','拘束、封路、警戒','警备头盔/观察结构、索具和折叠屏障；城市警备用途，不是军绿杂兵；靠结构区分于预算二号','普通；张索；立墙；撤回；受损'),
 ('fire','消防架桥机','涉水消防与临时通路','消防供液、架桥收纳、耐热护板三个用途分清；不强制继承旧版左前腿伤，不能整机刷灰冒充旧机','普通；涉水；泡沫；架桥；受损'),
 ('cargo','货柜领袖','变形护送、群盾、搬运','重新设计原创轮廓，不直接用现成变形金刚头胸；车体零件能在机体上追认；厚重可靠但不笨拙','机体；车辆；护场；吊运；受损'),
 ('mirror','镜星','棱镜标定与干扰','棱镜/感测器形成独有轮廓；工具性发光集中在作用器，避免霓虹通体发亮','普通；标定；干扰；失去导引；受损'),
 ('white','白色样机','贯穿射击与军刀近防','白色是身份色但大面积不用纯白；深色关节与少量识别色隔开环境；枪与刀的握持、收纳位置明确','普通；瞄准；军刀；受损；失能'),
 ('song','歌翼可变机','航空震荡与机动','机翼和人形在同一结构下成立；与雷翎的狙击型不同；震荡投弹器和飞行方向明确','人形；航空；投弹；起降；受损')]
portrait_manifest=json.loads((ROOT/V6/'portraits/manifest.json').read_text())['entries']
pmodel={p['unit']:p['model'].replace('res://',GAME) for p in portrait_manifest}
for key,name,role,design,states in mecha:
 cur=assets(pmodel.get(key,''),V6+f'portraits/{key}.png')
 add('M',key,name,role,design,states,cur,[SC+'catalog.gd',SC+'rounds/round_armaments.gd',SC+'campaign_world.gd',SC+'v5/rescue_data.gd'])
add('M','old_guardian','馆守Z轮式导览终端（旧守护者）','前章同一机魂的日常导览与对话形态','明确轮式底盘、导览屏与馆守的共同身份标识；是同一主体的远程终端，不是另一台独立机魂；不能用馆守Z整图缩放代替','普通；对话；受损',assets(A+'chapter_c02_v2/old-guardian.png'),['game-godot/scripts/formula_lab/chapter_c02/ui.gd'],scope='现有前章沿用素材；与M03同一主体')

forms=[
 ('king_light','完全版王者轻装本体','卸装后仍是同一冠军','拆下外装后头胸腰四肢仍完整；不能把轻装画成弱化丑版','装甲连接位外露；轻装站姿','king-modular.glb'),
 ('king_cannon','完全版王者双肩炮组','双线射击、卸下后场上操作','两炮各有背肩轴、炮口与前向；卸装保持同一外形和尺寸','挂载；前指；卸装；受损','king-cannon.glb'),
 ('king_shield','完全版王者合盾护板','护场与卸装','盾面内外、抓持/挂载点清楚；不遮断头部或成为假胸甲','展开；合拢；卸装；受损','king-shield.glb'),
 ('king_wing','完全版王者飞翼推进包','飞行及独立回收物','成对翼根与推进轴明确，安装在背部有承力结构；不要把羽翼漂浮在肩外','收束；飞行；卸装；受损','king-wing.glb'),
 ('king_drill','完全版王者右臂贯岩钻','近战推进及卸装','钻具根部连接右前臂，转子轴与推进方向同轴；禁止出现在裆部、膝外或无根悬空','静止；旋转；伸出；卸装；受损','king-drill.glb')]
for key,name,purpose,design,states,f in forms:
 add('F',key,name,purpose,design,states,assets(V6+'models/'+f),[SC+'v6/equipment_rules.gd'],template='form' if key=='king_light' else 'part')
for key,name,design in [('cargo_vehicle','货柜领袖车辆形态','轮轴、车头、货台与人形同一套零件；运输空间与乘员安全有实际位置'),('leiling_aircraft','雷翎航空形态','保留狙击炮轴与推进器，机翼展开不变成另一台机'),('song_aircraft','歌翼航空形态','机翼、座舱/感测区、弹舱与人形能对应；转型有中间姿态')]:
 add('F',key,name,'可变机的移动形态',design,'常态；转型中间态；受损',assets(V4+key+'.glb'),[SC+'campaign_world.gd',SC+'model_motion.gd'])
for key,name,design,filename in [('brave_core','完整勇拳核心机','完整有人机器人，有胸躯干四肢；不是只有拳头、空胸内胆或另一台凭空生成的小机','complete-core.glb'),('brave_combined','社勇王完整合体','原核心进入外部组件；保留主身份和零件来源，不能瞬间缩放拼出另一套身体','physical-combined.glb'),('brave_boots','社勇王外部腿架','左右脚甲与腿架有进入/闭合结构，地面独立状态仍能识别','boots.glb'),('brave_shoulders','社勇王肩背外部组件','肩包、背架和接口一体；与核心接入和分离位置一致','shoulders.glb')]:
 add('F',key,name,'合体专关与机体生命周期',design,'独立；合体中；合体后；分离；受损',assets(V6+'assembly/'+filename),[SC+'v5/rescue_cases.gd',SC+'v6/assembly_sequence.gd'])
for key,name,design,states in [('hydraulic','工程液压顶具','活塞、反力座和可收纳接口清楚；顶不动物体时回弹，不能变成刀','收纳；伸出；回弹'),('repair_tool','焊补工具与备件','焊枪/工具臂、备件匣、补片成套；按动作家族适配，不做每种柜内线路','取用；工作；收回'),('tether_tool','牵引与拘束索具','牵引钩和拘束爪共用材质但形状可分；线缆独立由引擎生成','发射；张紧；松脱'),('barrier_kit','折叠隔离墙套件','预算二号的预制墙段与灰崎的折叠警戒段分两种，不从地下魔法出现','收纳；展开；落地；损坏'),('bridge_kit','消防应急桥板','装载、展开、桥面与铰接端能对应；有限长度的实体','收纳；展开；接地；毁坏'),('projectile_kit','炮弹导弹与弹壳','爆破导弹、震荡弹、跨区炮弹用弹头/尾迹区分；具体伤害范围由规则显示','飞行；命中；残骸')]:
 add('F',key,name,'共享工具与产物',design,states,assets(V6+'tools/hydraulic-press.glb') if key=='hydraulic' else [],[SC+'v6/mounted_tool.gd',SC+'rounds/round_effects.gd'],template='part')

enemies=[
 ('claw','啮线体','近接方向攻击','大块头胸与咬切器官、强支撑肢；与我方标准单位有相近视觉分量，不能像小狗','claw'),
 ('mite','群生啮线幼体','数量压力与增援','小型单格档但保持敌体威胁感；与啮线体以头腹比例和攻击器官区分，不只是等比缩小','claw'),
 ('acid','喷酸体','锁格喷射与连爆局面','专用喷口、储液腹与姿态；不能继续借啮线体换名；酸液与火焰/炮弹不同','claw'),
 ('gun','远程架设体','跨区炮击','架设支脚、炮轴、蓄能器官可读；收起/架设/蓄力/出膛同一结构','gun'),
 ('wedge','重型楔入体','驻定切割与重型阻挡','2×2承力躯体和楔形切割器；重而不碎，击退时重量明确','wedge'),
 ('hover','掠渠体','悬浮袭扰','升力/浮行结构与瞄准方向明确；不靠全身发光表示飞行','hover'),
 ('screen','共振护群体','群体减伤来源','专用护群器官与范围中心轮廓；不能只拿掠渠体改颜色；护群生效和被打断可辨','hover'),
 ('worker','自动拆锁工机','受旧令驱动的市政作业机','保留城市工具机械身份；工作臂/切锁器具清楚，停机后不伪装击毁','worker'),
 ('tug','无人牵引工机','锁车与拖移','牵引杆/夹具和配重区别于拆锁机；机体与列车之间有连接来源','worker'),
 ('rival','断冠','2×2宿敌样本','按既有断冠设计做独立冠环、护板和支撑节点；不同方向暴露弱侧可视，不能继续借楔入体充数','wedge'),
 ('antiair','架设体对空装备变体','上层与空中压制','复用架设体身体，只增仰角炮架、跟踪器和对空预备姿态；不另造完全无关敌种','gun')]
for key,name,purpose,design,m in enemies:
 add('E',key,name,purpose,design,'普通；公开预备；发动；恢复；受损；击毁',assets(V4+m+'.glb'),[SC+'campaign_data.gd',SC+'v5/rescue_data.gd',SC+'v5/rescue_cases.gd',SC+'v6/full_data.gd'])

humans=[
 ('jicun','纪存','指挥、判断、跨区调配','中国青年男性外观的机魂实体；保留既有身份与终端；有主见和现场行动，不画成无特征网游少年',GAME+'assets/candidate/c02_short_plan/jicun_full_reference.png','平静；观察；判断；指挥；惊讶；担忧；愤怒克制；释然'),
 ('baiyuan','白鸢','战术预演与分镜','成年欧洲创作者；浅色发、成年骨相与体态、分镜工具；和七海在年龄气质/脸型/服装职责上区别',GAME+'assets/candidate/c02_short_plan/baiyuan_full_reference.png','平静；专注绘制；解释；质疑；嘴硬；意外；紧张；得意释然'),
 ('qihai','七海','权限核验、撤令与责任','日本成年女性；深色直发、成熟克制、秩序感；冷白服装使用柔和色块，不能整个人白得刺眼',A+'chapter_c02_v1/qihai.png','平静；核验；警告；质疑；决断；不悦克制；担忧；放松'),
 ('doudeng','兜灯','维修与安全制动','中国青年女性整备员；头灯、维修服、真实工具与手部劳动；不幼儿化；与其他对话人物共用头部显示尺度',A+'chapter_c02_v1/doudeng.png','平静；检查；专注维修；不耐烦；警告；惊讶；担忧；松口气'),
 ('luheng','陆衡','载荷判读与工程责任','中肯混合家庭设定；中深棕肤、卷曲或粗硬短发、工程服；不用族裔刻板替代个人特征','','平静；测算；解释；怀疑；指挥；焦急；沉重；释然'),
 ('haosi','豪司','勇拳驾驶、社勇王协商','日本成年试驾员；热血与职业责任并存，驾驶装/工牌有功能；不是通用偶像脸',GAME+'assets/portraits/portrait_haosi.png','平静；振奋；决意；担忧；争辩；承担责任；惊讶；庆幸'),
 ('tangjiao','唐胶','前章模型修复与生活角色','中国青年男性；工具围裙和手作生活气；和纪存明确不同；不沿用旧女性/中性误稿',A+'chapter_c02_v1/tangjiao.png','平静；检视；吐槽；解释；不满；惊讶；担心；欣慰'),
 ('zhaomei','赵梅','合作社组织者','保留既有年龄、脸部辨识与生活经历；成年成熟组织者，有行动力，不被画成通用慈祥路人',A+'chapter_c02_v2/zhaomei.png','平静；倾听；协调；质疑；严肃；担忧；坚定；微笑'),
 ('jiaojia','胶价王','赛事制作人与商业对手','主持/旧件买手的强识别轮廓和职业服装；表情有表演与算计，不简单丑角化；不能控制机魂主体',A+'chapter_c02_v2/jiaojia.png','营业笑容；介绍；盘算；不悦；惊讶；强撑；恼怒；收敛'),
 ('police_seat','警备驾驶席','专关通讯与撤回指令','有独立通讯头像与职业识别；未有具名身份时作为本地警备席设计，不套主角脸','','平静；报告；警告；确认；焦急；解除警戒'),
 ('workshop_staff','工房工程员','前章与现场配角','工具、工服和年龄方向与主角区分；具名化前不编造新个人设定','','平静；讲解；疑问；警告；担忧；庆幸')]
for key,name,purpose,design,pth,expr in humans:
 scope='现有前章沿用素材' if key in ['tangjiao','zhaomei','jiaojia','workshop_staff'] else '当前工务城及人物全链专关'
 r=add('H',key,name,purpose,design,'日常；工作/指令姿态；表情差分',assets(pth),[SC+'campaign_stage.gd',SC+'dialogue_presenter.gd',SC+'v6/people_rules.gd','game-godot/scripts/formula_lab/chapter_c02/ui.gd'],scope=scope,expressions=expr.split('；'))
 if key=='luheng':r['source_note']='身份参考在Canon的char_haosi_luheng_setting_v1.png；当前工务城未找到独立立绘绑定，按新增独立素材交付，不能把有指令入口当有头像。'
r=add('H','civilians','检修员与撤离人群','列车、居民楼和气氛反应','成人身形、工作装备与少量服装差异；不把群众全画成相同小人','等待；避险；招手；欢呼',[],[SC+'campaign_world.gd',SC+'campaign_stage.gd'],template='crowd')
r['source_note']='当前找到的是机体气泡与居民目标接口，未找到独立人群模型绑定。本项补齐设计与显示素材，后续需要接入场景；不宣称现成接口已包含人群演出。'
add('H','tiny_units','机器犬及人物地图小单位','微型显示规范与既有小单位后续复用','只制定人/犬等四分之一格面积档；不据此把常规猎巢敌体缩成小狗；有具体入场对象才建模','站立；移动；警觉',[],[SC+'unit_scale.gd'],template='crowd',scope='用户明确要求的通用显示素材规范；不新增本关角色')

building_rows='''refuge-habitat|有人避难楼|现代机甲城市的居民目标|5–7层住宅体量；入口/窗带/楼板让人读懂尺度；完整楼顶、受损露层、倒塌残壁各自可信|完好；受损；毁坏
shelter-illustrated|渠岸住宅|B区居民与街区|沿渠立面、后侧与屋顶成套；破损后保留内部楼板厚度和断面，不再用完整屋顶盖残楼|完好；受损；毁坏
shelter-c|环站公寓|C区居住目标|货运站旁现代公寓，与工业仓库可区分；保持同城材料关系|完好；受损；毁坏
office-a|供能前庭办公楼|A区体量与遮挡|现代公共设施办公，首层服务入口、窗带、检修层明确；不是小屋|完好；受损；毁坏
office-b|渠岸办公楼|B区街区体量|钢蓝/矿物材质辅助色；不可与可保护住宅混同|完好；受损；毁坏
office-c|装卸站调度楼|C区调度设施|观察窗朝向轨道；入口与站台对应；红色点缀有用途|完好；受损；毁坏
switchgear-illustrated|公共供电柜|接电与断电操作|柜体/母排/隔离刀与指示灯分件；开关动作和能量方向可见，不做内部修线模拟|完好；工作；断电；受损；毁坏
relay|远程馈电柜与中继|切线取消跨区炮|与公共供电柜以端子/接口轮廓区分；不能只靠文字标识|完好；供电；隔离；受损；毁坏
substation|变电设施|供能建筑和基础设施|设备阵列有承重平台、隔离距离与检修通道；不以小圆柱堆砌冒充变电站|完好；受损；毁坏
workshop|维修工房|工程场所与整备背景|可进出的工业门、天车梁、工位尺度与机体匹配|完好；受损；毁坏
terminal|车站终端与控制台|现场读取和操作|倾斜控制面、硬件按钮和信号灯；动态字由UI绘制，不画伪文字|完好；可操作；已完成；受损；毁坏
train-front|撤离列车车头|首要保护对象与行车方向|驾驶端和尾端一眼不同；现代轨道救援列车，不是玩具小屋加轮；车轮/车灯可简单运动|完好；停车；行驶；受损；毁坏
train|撤离列车车厢|24人撤离的可见载体|与车头同一列车；窗、门、走行部和连接器保持比例；载人与空置可表达|完好；载人；停车；行驶；受损；毁坏
bridge|跨渠桥面与桥锁|修复、支撑、通车|断口、铰链、锁座、支撑端点真实成套；桥面未接通与已承重结构不同|断开；临时支撑；锁固；受损；坍塌
deck|上层检修栈桥|多层战场与承重|楼板厚度、下方梁架、栏杆与缺口；俯视和旋转都读得懂高度|完好；受损；毁坏
anchor|支撑锚点与支座|承重与宿敌侧撑|安装位置、拉力/压力方向清楚；损坏后确实断开承力构造|完好；受力；断裂
crane|固定吊机|场景机构与吊运|塔身、吊臂、绞盘、吊钩分件；回转轴与吊运范围一致|收起；作业；停机；受损；毁坏
elevator|升降平台|上下层输送|轨道、驱动和平台有连续空间关系；不是贴图电梯|下层；运行；上层；受损；毁坏
turntable|轨道转台|转向与载物|桥盘厚度、圆坑、环轨和驱动机构真实；中心轴固定，转90度边界可读|静止；旋转；就位；受损；毁坏
sluice-drive|水闸驱动与闸门|水位调节|门体与侧壁/轨道连接；开启和关闭不是只改水色|关闭；开启；受损；毁坏
pumpstation|泵站|深渠与排水场景|进出水管、泵房和平台有工程逻辑；与办公楼不同|完好；运行；停机；受损；毁坏
crate|货柜与吊点周转箱|推移、搬运、挡炮与清轨|标准货柜与较小周转箱两尺寸；吊点、门面、顶面有对应关系|完好；吊起；受损；破碎
wall|实体隔离墙|移动/射线阻挡|施工预制段与警备折叠段两种来源；底座接地、毁坏后留真实空隙|收纳；展开；完好；受损；毁坏
fuel|燃料与补给接口|补给及空地任务|罐体、接头、防护围边；可爆与不可爆对象用结构区别，不能都画同一桶|可用；耗尽；受损；毁坏
capacitor|隔离电容|爆炸连锁|电容外壳与连接端、泄放口明确；危险器材不与普通居民物件混淆|稳定；临界；爆裂
rift|猎巢入口|公开增援与封闭|裂口/侵入结构有实体边缘；蓄动、出现、封住三个过程；不只红圈贴纸|休眠；预告；增援；封闭；摧毁
portal|承运交接点|跨战场转运|地面导向、吊运/承运装置与出口一致；不是科幻传送魔法门|开放；繁忙；阻塞；关闭
equipment_bay|整备复装工位|可拆装备回装|停靠线、支架、工具臂和被放置部件匹配；非通用浮空按钮|空闲；占用；维修；受损
cable|电缆与母排连接段|供电链路|绝缘外层、端子、线槽与断点；通断有可见反馈，不用长霓虹线当实体|完好；通电；断裂
support_strut|临时支杆与承重架|支撑/交接通桥|上端接触、底座和斜撑方向清楚；卸载后保留现场物件|收纳；安装；受力；损坏
signal|轨旁信号与站台设施|行车方向和可用路线|独立信号灯/道岔指示/站台边缘；不能与敌方攻击红色闪烁争夺注意|停止；放行；故障
skyline|城市柱环与远景巨构|三战场属于同一城市|柱环贯穿A/B/C；桥、站与供能设施有地理关系；巨构远处降低对比|日常；局部事故；恢复
street_kit|道路街具与边界套件|前中后景、尺度和可读边界|护栏、灯柱、楼梯、检修口、栏板、管桥按用途成套；保持可走空间|完好；受损
service_hut|检修室和值班室|小型功能建筑|允许小尺度但必须标明用途；不能拿小屋作为主居民楼；人尺度入口正常|完好；受损；毁坏'''
for line in building_rows.splitlines():
 key,name,purpose,design,states=line.split('|')
 cur=assets(*[V6+f'environment/{key}-{i}.glb' for i in range(3)])
 if key=='street_kit':cur=assets(V6+'layouts/canal-street.glb')
 add('B',key,name,purpose,design,states,cur,[SC+'v6/full_art.gd',SC+'fixture_art.gd',SC+'environment_art.gd',SC+'rounds/presentation_layout.gd'])

terrains='''concrete|承重混凝土地坪|常态步行面|中明度矿物色、板缝与有厚度边缘；低对比表面纹理，不能照片噪点盖住角色
painted_steel|涂装金属甲板|工业地面|成片涂装与检修板分区；边缘和螺栓不铺满全地面
grating|格栅与排水槽|材料差别|格栅真实深度与暗腔；密纹在正常镜头不闪烁
rail|轨道与道岔|列车路线|轨、枕木/扣件、路基和岔口；方向连续、不可跨地图倒转
conveyor|输送带|自动位移地形|运行方向与规则一致；纹理流动朝实际输送方向
rubble|碎石与残骸地面|额外移动代价|少量大块碎料、可见低起伏；与不可通行残墙区分
shallow_water|浅水|涉水地形|可见渠底、岸沿和水线；涉水单位不误显示坠落
deep_water|深渠与深水|坠落/淹没风险|有渠壁、水面高度和连续深度；不要死黑坑或镜面摄影水
pit|深坑与结构缺口|不支撑地面|可见侧壁/梁断口，边缘脚印清楚；不把黑方块直接贴地
oil|油面与可燃物|燃烧连锁|局部油膜形状与暗反光；低对比，不与水混同
burnt|燃后地面|持续状态结果|烧痕、少量残烟与材质变化；火消失后仍有结果但不永久遮格
electrical|带电地面|电击危害|导电材料/破缆来源、边界与短放电；持续危险标记另由UI处理
upper|可行走屋顶与平台|上层/净空|屋顶有厚度、可走面和栏杆缺口；不能与背景屋顶混同
slope|坡道与阶梯|高度连接|起终点、坡向、梁支撑有实体；显示高差但不制造虚假阻挡
bridge_debris|塌桥断面与沉落物|通路被毁|断梁、桥板和水花/落尘接口；不能仍保留完整桥面贴图
material_families|统一表面材料家族|建筑/机体/场地材质衔接|涂装金属、裸金属、混凝土、玻璃、橡胶、发光件分家；同画法不同材质，避免全塑料'''
for line in terrains.splitlines():
 key,name,purpose,design=line.split('|')
 add('T',key,name,purpose,design,'常态；边缘接缝；适用状态变化',assets(V6+'materials/industrial-cel-families-r2.png',V6+'materials/industrial-drawn-atlas-v2.png'),[SC+'ground_relief.gd',SC+'v6/terrain_cel.gdshader',SC+'v6/kit_material.gdshader'])

scenes='''city_master|工务城三战场总构图|同城联动一眼成立|固定既有地理C车站在西、B桥在东、A供电在上方；柱环连贯，色彩与物件分区|command-ring-kinetic.png
yard_a|A供能前庭正常战棋画面|先看清供电和威胁|鼠尾草绿/钢青绿设备与矿物墙；机体英雄色独立；用实际棋格摆机体敌人建筑，非空场海报|
canal_b|B跨渠桥座正常战棋画面|支撑、深渠和桥路选择|钢蓝、矿物青水、现代住宅；桥面与渠壁有厚度，留看清推落及托桥的空间|
station_c|C环下装卸站正常战棋画面|清轨与列车保护|褪蓝与朱红货运设备；车头方向、轨道出口、货箱阻塞读得清|
command|指挥廊与部署背景|开场/部署|三工作面与城市事故有关联；为左侧菜单留安静区，不把HUD画进背景|command-ring-kinetic.png
passengers|列车与待救检修员|救援目标情绪|让人看到乘员、受阻列车和临近危险；可分离人群/列车/背景做轻动效|story-car-kinetic.png
power_on|母线接通与链路点亮|操作后的跨区因果|接电源头→桥→车站；能源流和终端状态拆层，不能只有全屏发光|story-link-kinetic.png
bridge_hold|托桥与列车通过|机体救援的大魄力场景|明确支撑机、桥承力位置、列车和居民；不违背馆守缺臂或货柜形态|
jicun_dispatch|纪存多方调度特写|主角能力表达|视线/手势与三处实际事件同方向；终端信息以UI后置，不能代替人物行动|
baiyuan_previs|白鸢预演特写|预演与改线表达|分镜、视线与路线草案形成动作；预测是可被推翻的方案，不画成神谕|
qihai_revoke|七海核验撤令特写|权限全链|证据、决定、撤令反馈连续；克制的档案峰值层，身份不换装漂移|
king_drill|王者右臂巨钻冲击图|招牌Cut-in|巨钻从右手/右前臂接出，双炮朝前；对称帅气头与冗余武装，避开裆部误读|
hero_sky|无牌天冲拳冲击图|体术招牌|从脚底、转髋、肩到拳形成一条发力线；拳接触点明确；特效不遮拳体|
brave_assembly|社勇王合体关键镜头|完整核心与外组件组合|核心、腿架、肩包各自有来源；3–5关键姿态可转成短演出|
rival_reveal|断冠宿敌出场|宿敌压迫感与可破弱侧|独立冠环/护板；留可视反制点，非堆尖刺黑团|
outcome|救援成功与失守后果|胜败可理解|成功见通桥离站与乘员；失败按真实对象分列车受损/居民楼毁坏/路线中断，不通用烟花|
c02_street|模型街与港口街景|前章既有背景换装|两地构图与用途不同；现代工业生活街区，比例与人物吻合；不再中古皇城街景|
c02_workshop|模型病院与三号工房|前章生活与工程场所|模型桌、工具、人尺度空间；实际巨机工房另分区，不能把模型直接画成巨机|
c02_cargo|货柜领袖事件图|前章事件不只对白|有行为、阻碍和结果的剧情画面；与新原创机设相同|
c02_champion|完全版王者冠军展示与卸甲|前章节目与自主救场|竞技冠军冗余帅气与卸装后的同一主体；保留自主性，不画遥控傀儡|
c02_baiyuan|白鸢作品与现场事件|前章作品/人到场的区分|作品痕迹与本人在场分开；不借新图更改既有出场时间|'''
for line in scenes.splitlines():
 key,name,purpose,design,pic=line.split('|')
 cur=assets(V6+'backgrounds/'+pic) if pic else []
 if key=='c02_cargo':cur=assets(A+'chapter_c02_v2/cargo-story.png')
 if key=='c02_baiyuan':cur=assets(A+'chapter_c02_v2/baiyuan-event.png')
 if key=='c02_champion':cur=assets(A+'chapter_c02_v2/king-drill.png',A+'chapter_c02_v2/king-cannon.png')
 add('S',key,name,purpose,design,'构图稿；色稿；分层成稿',cur,[SC+'rounds/round_stage.gd',SC+'dialogue_presenter.gd','game-godot/scripts/formula_lab/chapter_c02/map.gd'],scope='现有前章沿用素材' if key.startswith('c02_') else '当前工务城及其已列专关')

effects='''jab|轻拳命中|短促接触和截击|小而清楚的硬边冲击核+方向短线，不要所有拳都爆炸|impact_core；direction_streak
heavy_punch|重拳与勾拳|重量、冲击与位移|预备受力、较大的方向冲击、地面尘和后移；与轻拳节奏有差异|impact_core；debris；dust
kick|正蹬与回旋踢|前推/侧推方向|腿部轨迹与接触核分离；旋踢扇轨不能暗示整扇面均伤害|trail；impact_core
sky|天冲拳|招牌体术高潮|发力上升线、拳体和穿破层分清；接触后迅速收束回棋盘|charge；trail；impact_core；afterglow
slash|军刀斩击|刀具与近防|刀尖轨迹、斩痕和少量火花；不拿能量球代刀光|blade_trail；spark；hit_mark
drill|右臂巨钻|钻入与推进|沿钻轴的碎屑/摩擦火花；接触材料有变化，不能爆点落在身体中心|rotor_streak；spark；debris
beam|首体阻挡光束|直线打到首个实体|炮口、亮核、外晕、终点刻印分层；终点后没有伤害射线|muzzle；beam_core；beam_glow；hit_mark
pierce|贯穿光束|穿过规则允许的目标|贯穿线和每个命中脉冲分层；被墙截断处终止，不能视觉无限贯穿|muzzle；beam_core；entry_hit；exit_hit
twin_cannon|双肩炮齐射|双条实际炮线|两炮各自起点和后坐；两条线不合成中央激光|muzzle_pair；beam_core；smoke
missile|爆破导弹|飞行、中心及邻格爆破|可见弹体尾迹、地影、首爆与邻区爆片；范围随真实结果生成|exhaust；impact_core；blast_ring；smoke
shockwave|震荡空爆|爆心伤害与四邻吹离|外推冲击环与方向风迹；不把没有伤害的四邻都画成爆炸受伤|blast_core；wind_arc；push_streak
artillery|跨区炮弹|来源、越区飞行与落点|炮口→飞行弹→目标标记→着地爆炸同一方向；不能无源落雷|muzzle；trail；landing_flash；debris
acid|酸液喷射|锁格酸液命中|液滴/弧线/落地喷溅区别于光束和火球；残留只在规则有持续酸时出现|droplet；splash；contact
tether|牵引索|钩爪张紧与拉回|发射点和附着点明确；受力线随双方位置变化，不画成推箭头|hook_flash；cable_detail；tension
pin|拘束索|锁步但保留开火|环扣/索紧表达移动受限；不盖掉敌方仍有效的攻击轨迹|clasp；cable_detail；lock_pulse
mark|棱镜标定|后续攻击的标定来源|一次扫描→目标刻印；不要长期占满全身轮廓|scan_arc；target_mark
jam|导引干扰|取消未发攻击|导引器官短错相、承诺轨迹断开；不是通用电击伤害|interference；break_pulse
shield|护盾施加与吸收|单体/群体护场|展开、命中吸收、破盾三段；轮廓薄且可看见单位|surface；edge；absorb；break_shard
foam|泡沫灭火与护场|消防的通用效果|喷射形状、落地泡沫与火焰退去；不能用蓝盾复制替代|spray；foam_patch；steam
repair|焊补与恢复|工具动作及真实耐久恢复|焊点、小飞溅、补片完成信号；没有恢复不播假加血|weld；spark；finish_pulse
jack|液压顶推|无直接伤害的施力|活塞受力、地面尘、位移/碰撞分别表达；无伤不白闪血光|pressure；dust；recoil
deploy|造墙架桥与产物落地|物件从机体到地面|抛出/展开/接地短尘与卡扣；产物本体来自独立模型|launch；landing_dust；latch
transform|变形锁扣与推进|形态过渡|机械锁止、短推进流，不用大烟遮住整个变形失败|latch；exhaust
assembly|合体接口|组件连接次序|引导、接合火花、锁定灯依接口依次发生；不全屏闪白掩盖结构|guide；latch；seam_light
collision|单位碰撞与撞墙|接触对象和二次伤害|单位/金属/混凝土三材质片元；撞击点贴实际边界|impact_core；metal_debris；stone_debris
water_fall|落水与坠坑|位置变化及失能|入水水花/泡沫或坑内落尘；飞行免疫时不能播溺亡|splash；foam；fall_dust
kill|击破与残骸|机体失能和敌体击破|机械件脱落与短烟，异形裂解另套；不把所有对象同一烟球盖掉|metal_break；alien_break；smoke
chain|连锁引爆与接力|一手影响多个对象|按因果顺序跳转，次级爆炸缩短；保留最终落点与血格可见|relay_streak；secondary_blast
flight|起飞悬停降落|飞行身份|推进方向、地面扬尘/降落接地同一力向；不用悬空无声飘移|thruster；ground_dust；landing
megastructure|巨构震动与断裂|跨场景设施后果|局部接缝开裂、碎落、远处灯列变化；不是整座城乱摇|structural_dust；fracture；signal_wave'''
for line in effects.splitlines():
 key,name,purpose,design,components=line.split('|')
 add('X',key,name,purpose,design,'预备；作用；结果；收束',[],[SC+'combat_vfx.gd',SC+'rounds/round_effects.gd',SC+'rounds/round_feedback_view.gd',SC+'v6/action_sequence.gd'],components=components.split('；'))

states='''charge|蓄力准备|准备态可被打断|身体姿态+武器聚能，主焦点在发射/施力端；阶段图标单独交
guard|护势与持续支撑|持续行为没有结束|受力姿态、接地与设备承重反馈；不当成普通瞬发技能
fire|持续燃烧|地形和对象燃烧|火舌与烟分层、基部贴附目标，正常镜头可见但不遮满盘面
smoke|烟雾与余烟|遮挡/气氛分工|有规则遮挡的烟界与纯余烟区别；不能美术烟擅加规则
electric|漏电与短路|危险来源|局部断线火花与地面电弧；与安全通电流分家
power|通电与断电|设施可用性|灯列/能量接口状态变化，不把整栋楼刷成发光体
shutdown|停机与撤令|可保全的市政单位|机械静止、工作灯退去、锁定解除；与击毁残骸截然不同
immobilized|拘束与受阻|不能移动|索具或受阻部位可辨，开火武器仍保持可用表达
jammed|干扰中|攻击承诺取消|导引点短失锁与UI取消符号，避免错误表达持续扣血
marked|被标定|后续攻击关系|简洁标记有来源，不给整片场地永久描边
armor|护甲与破甲|伤害差异|装甲受力/破甲裂层有限表达；损失数字由游戏绘制
damaged|轻损重损与失能|机体状态|状态覆盖层不随每个姿势重画全身；重要缺件有独立模型
spawn|增援预告与入场|有时间可反制|入口积聚、露头、出场分开；不和已入场敌人混淆
closed|入口封闭|增援被取消|实体封口/关闸反馈，后续预告消失；不是关灯算封闭
objective|目标完成与仍阻塞|跨区后果|接电/通桥/行车分开图形；保留未解决条件，别泛用绿色勾
scrap|残骸可回收|资源与障碍|可回收部件、不可走大残骸和纯装饰碎屑有区别'''
for line in states.splitlines():
 key,name,purpose,design=line.split('|');add('C',key,name,purpose,design,'进入；保持；解除；减少动态模式',[],[SC+'rounds/round_feedback_view.gd',SC+'v6/full_art.gd',SC+'rounds/round_effects.gd'])

graphics='''hover|自由探索悬停|光标发现对象|贴实际脚印，强度低于选中；不盖对象主体
selected|选中足迹|选中了谁|1×1/2×2/3×3完整脚印；微型外观不缩掉实际选择范围
move_range|可达范围|能走到哪里|轻底/边界清楚；多格单位按真实合法终点显示
route|连续路径|将怎样走|方向箭头从起点流向终点；绕障路径与费用一致
landing|终点与落位|到达后占哪里|完整占格与朝向；高层落点标高度
invalid|不可用目标|为什么不能做|阻挡点或缺少条件就近标出；不弹大菜单
melee|近战与扇面|真实受影响目标|范围按规则而非挥动刀光猜；主目标与余波区分
ray|直射轨迹|第一遮挡物与终点|起点有武器来源，遮挡后虚线/截断符号；世界空间深度正确
pierce|贯穿轨迹|多对象受影响|贯穿目标逐一标示，停止点明确
lob|投射弧线|投掷与炮弹落点|明显弧线和落点；飞行弧与地面影响区域分开
blast|爆炸范围|连爆与友伤|中心/邻接/二级连爆分层；盾保护不隐藏受影响事实
push|推拉位移|目标去哪|大箭头、落点影与步数；前推/侧推/拉回不同方向
collision|碰撞结果|谁撞谁与损失|接触处撞击符号、双方损失及停止格
fall|落水坠坑|地形后果|落点危险符号与消失/失能反馈，飞行豁免明确
hp|预计耐久变化|将失去或恢复多少|损失段闪烁与保留段稳定，恢复另色/纹理；不是只有漂浮数字
threat_wall|敌方目标光墙|建筑正在被瞄准|标准高度红色半透明墙罩脚印，深度遮挡正确；不能2D框线穿过楼脸
intent|敌方承诺方向与顺序|敌人即将干什么|顺序徽标与设施编号分层；悬停明显轨迹、目标、HP变化
cancelled|被取消的威胁|这一手避免了什么|旧轨迹淡去/断开、被保住对象的损失归零；不只写一句文字
reinforcement|增援位置与时间|会从哪出来|格位、敌种剪影与轮次分开；未入场不画成已站在格子上
cross_board|跨区因果线|哪边影响哪边|源设施→目标区域/对象，状态变化沿线发生；全城总览与局部提示同语义
convoy|撤离路线与阻塞|保护哪段路|车头朝向、C→B→东出口连续；阻塞点/下一可走段清楚
height|上层承重与净空|高低空间规则|层号、垂直连接、承重危险；不会贴到楼体假平面
equipment|吊运变形合体包络|空间和载荷限制|载荷/新形态完整脚印、扫掠障碍、落位方向；合法与失败可分
cost|移动行动与资源费用|一手的代价|图标+数值留位，移动/主行动/弹药/备件不同符号
area_tools|修理支撑导引作用区|非伤害技能范围|支撑接口、维修邻接、护群来源可见；不套攻击箭头'''
for line in graphics.splitlines():
 key,name,purpose,design=line.split('|');add('G',key,name,purpose,design,'默认；悬停；预览；执行；减少动态/色觉适配',[],[SC+'rounds/round_overlay.gd',SC+'rounds/round_cursor.gd',SC+'rounds/intent_visual.gd',SC+'rounds/tactical_feedback.gd'])

uis='''mission|精简目标条|我在保护什么、缺什么|优先目标与一条当前阻碍；三条链路可展开；不堆长任务清单
board_tabs|三战場切换|本区/异区还有行动|地域小图/色块、名称、余行动、重要风险层次分明
unit_strip|机体头像条|可行动者与选中|头肩专用图；行动可用/耗尽/受损/跨区状态，别再全身缩图
skills|快捷招式条|选机后的直接操作|招式图标、按键、费用留位；普通动作不嵌套多层菜单
inspect|光标资讯浮窗|自由探索信息|短摘要与按住详细的展开稿；位置避开光标和受影响单位
consequence|这一手后果|立即结果和取消威胁|血格/位移/碰撞/链路变化优先，文字只补原因
end_round|结束回合预告|不作为的后果|未用主行动、将受损对象、增援分段；实际与下轮预告不混
overview|全城总览|跨战场联动|三块真实地图关系、源/目标设施、列车进度和可点击焦点
comms|通讯与人物指令|人物的独特作用|人物专用头像、当前可用原因、目标；未满足条件不装成主按钮
dialogue|对话舞台|说话者和听者|统一眼线与头大小，活动方/听者明暗适度；入场和表情不乱缩放
deployment|出击编队|单位职责和战场需求|角色头像/体型/移动方式/主要动词；分区出击限制清楚
roster|机体图鉴与装备|机体技能体系|母版和游戏模型同身份；武器挂点、变形与大格足迹可读
cards|构筑修饰与成长|可选专关的技能变化|基础动作与修饰关系明确；只做有来源的卡，不创设新数值
accessibility|设置与无障碍|字体/动态/色觉/键位|大字号不溢出；焦点、不可用和按键录入都可区分
onboarding|首次提示|学会光标探索与一手结果|简短手势示意，随当前编队；不写死无牌一号
results|胜败与结算|救了谁、损了什么|居民、设施、资源、声誉和额外目标用图形分层；不只大段文本
replay|预演回看控制|看清动作因果|播放/快进/暂停/退出清楚，不把常驻时间轴铺满底部
title|标题与入口|进入当前可玩内容|按冲击档做品牌和构图；菜单区域安静，主入口明确
buttons|按钮面板与提示共件|统一现代界面语言|深墨蓝平面、有限边线、适度强调；避免金框套娃/灰蓝渐变/廉价机械花边
bubbles|机魂与群众气泡|气氛与短提示|短、靠近说话者、不会遮盖攻击线；战术信息优先'''
ui_parts={
 'mission':['mission','header'], 'board_tabs':['area-a','area-b','area-c'],
 'unit_strip':['selected','command'], 'skills':['command','selected'],
 'inspect':['inspect'], 'consequence':['decision'], 'end_round':['risk','danger'],
 'overview':['panel','header'], 'comms':['panel','tag'], 'dialogue':['dialogue'],
 'deployment':['panel','selected'], 'roster':['panel','paper'], 'cards':['paper','selected'],
 'accessibility':['panel','command'], 'onboarding':['tag','inspect'],
 'results':['panel','paper'], 'replay':['command','primary'],
 'title':['primary','command'], 'buttons':['command','hover','pressed','disabled','selected'],
 'bubbles':['tag']}
for line in uis.splitlines():
 key,name,purpose,design=line.split('|')
 cur=assets(*[A+'linked_campaign_rounds/ui/'+p+'.svg' for p in ui_parts[key]])
 r=add('U',key,name,purpose,design,'普通；悬停；选中；按下；不可用；键盘焦点',cur,[SC+'rounds/round_skin.gd',SC+'rounds/round_hud.gd',SC+'v6/full_ui.gd',SC+'dialogue_presenter.gd'])
 r['source_note']='这里列出本类界面使用的共享皮肤候选；完整布局由接入代码生成，不能把某个SVG当作整张界面。'

# Every base capability's icon is a distinct deliverable, not one vague "skill icons" row.
icon_sets='''jab|截击直拳|短直拳与撤步
kick|正蹬推位|脚掌向前的推力
round_kick|转轴回旋踢|旋转腿与侧推
sky|天冲拳|上冲拳的标志轮廓
hook|摆身勾拳|弧线拳路与横向重心
heavy|蓄势重拳|上举拳与落点
counter|正面接拳|接拳防御姿态
tether|牵引|钩索向内拉
brace|持续支撑|手臂/支杆托结构
brave|护路破甲拳|拳与自护轮廓
final|破围终式|拳与规则扇面
guard|护场|护罩覆盖对象
cannon|双肩炮|并列两炮
drill|贯岩钻|右臂钻头
beam|首体光束|射线到首个实体停止
pierce|贯穿光束|射线穿两体
saber|军刀|刀刃与短斩
missile|爆破导弹|弹体与爆片
shockwave|震荡空爆|中心弹与外推箭头
jam|导引干扰|感测器失锁
mark|棱镜标定|棱镜和目标标记
wall|部署隔离墙|墙体与落地底座
bridge|铺设桥板|折叠桥展开
repair|备件抢修|工具与补片
jack|液压顶推|活塞向外
lift|吊移|钩与载荷
transform|变形|同一机体两形态
foam|泡沫灭火|喷嘴与泡沫
pin|拘束索|爪锁移动
operate|操作设备|手柄与机械开关
read|读取记录|终端与记录页
isolate|接回母线|断接头连通
seal|关闭入口|闸门闭合
rotate|转台|圆盘旋转九十度
transfer|跨区转场|两区域之间承运
reload|装填|弹匣与装入方向
recover|回收|完整可回收部件
detach|卸装|原部件从挂点拆出
reinstall|复装|部件回到原挂点
combine|合体|核心与外部组件
separate|分离|合体释放原组件
takeoff|起飞|上升与推进
land|降落|下降与接地
refuel|补给|接头与燃料
dive|俯冲|下向飞行体
air_ram|空撞|飞行方向与接触
bomb|投弹|机下弹体落点
strafe|扫射|飞行轨迹与射击
airlift|空中投送|飞行载荷
observe|观察|观察器与区域
survey|勘测|工具与结构读数
connect|接线|两个端子连通
lock_support|锁固支撑|锚点与锁扣
elevate|升降|平台与上下箭头
drain|排水|闸口与水位下降
restart|重启|机械启动循环
listen|纪存倾听|机魂/通讯来源
archive_plan|白鸢补页|分镜本与备用线
revoke|七海撤令|有效指令被撤销
record_evidence|七海取证|证据页与来源
hard_stop|兜灯硬停|机械制动
load_reading|陆衡载荷判读|支撑结构与载荷
soul_boost|豪司共鸣|驾驶者与机体响应
negotiate|豪司协商|两个主体达成条件
withdraw_charge|警备撤回|准备动作被取消'''
for line in icon_sets.splitlines():
 key,name,design=line.split('|');add('I',key,name,'技能/操作入口和对象检查',design,'普通；选中；不可用；悬停',[],[SC+'catalog.gd',SC+'rounds/round_armaments.gd',SC+'v6/people_rules.gd',SC+'v6/full_ui.gd'])

motions='''idle|共享待机|标准动作复用|适度呼吸/重心、机械活动；正常战棋镜头看得出，频率不拖沓；重型/轻型/多足分家
locomotion|共享奔跑与转向|标准动作复用|连续沿合法路径移动；直路连续跑，遇障才绕；停步不逐格刹车
air_move|共享飞行与起降|标准动作复用|离地、巡航、转弯、接地；推进与身体方向一致
gunner|共享射击|标准动作复用|瞄准→武器发射事件→后坐→恢复；步枪、肩炮按挂点适配
operate|共享手部操作|标准动作复用|手部示意+设备状态反馈；不做打开柜门/内部接线细节
work|共享维修与液压施力|标准动作复用|同动作家族按工具微调；施力方向和回弹清楚
carry|共享搬运吊运支撑|标准动作复用|提取、移动、放下与承压；载荷共用高度档，不做单位两两接触表
reaction|共享受击与失衡|标准动作复用|方向、轻重、倒地、复原分别响应同一事件
hero_martial|无牌拳脚与天冲拳|体术定制|直拳/正蹬/回旋踢/天冲拳分动作；支撑脚、转髋和手型明确
boxer_boxing|旧拳王拳击组|体术定制|勾拳、接拳、重拳有不同重心与节奏，不换名共用一招
brave_signature|勇拳与社勇王招牌拳|体术招牌定制|核心/合体动作保留人格与发力；终式和普通拳区分
king_drill_motion|王者钻击装备适配|共享重击加装备层|右前臂驱动钻轴、旋转和推进；按武器适配，不另建每敌人的动作
form_transition|车辆/航空变形|形态专用设计|每套形态只做一次合理中间姿势/锁止；不必追求每个零件完美变形动画
combine_motion|社勇王合体/分离|招牌演出设计|保留完整核心，组件真实进场/接合/落位；分离恢复原身份'''
for line in motions.splitlines():
 key,name,purpose,design=line.split('|');add('N',key,name,purpose,design,'准备；作用事件；结果；恢复',[],[SC+'v6/action_library.gd',SC+'v6/action_sequence.gd',SC+'v6/assembly_sequence.gd'],scope='动作资源方可选专业委托；二维外援只需动作设计；标准动作必须优先复用')

def digest(p):
 return hashlib.sha256(p.read_bytes()).hexdigest()

def copy_reference(path, dest):
 src=ROOT/path if not isinstance(path,Path) else path
 if not src.is_file():return ''
 target=OUT/dest;target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(src,target)
 REFS.append({'source':str(src.relative_to(ROOT)),'delivered':dest,'sha256':digest(src),'use':'参考，未修改原图'})
 return dest

def relative(p):return str(p.relative_to(ROOT))

def write_csv(name, rows, fields):
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def outputs(row):
 template=row['template'];names=list(SPECS[template][2])
 if template=='human':
  for i,expr in enumerate(row['expressions']):names += [f'bust_{i+1:02d}.png',f'portrait_{i+1:02d}.png']
 if template=='building':
  for s in row['states']:
   if s in ['受损','毁坏','坍塌','断裂']:names.append({'受损':'damaged','毁坏':'destroyed','坍塌':'collapsed','断裂':'broken'}[s]+'.png')
  names.append('operations.png')
 if template=='fx':
  for part in row['components']:names.append(part+'.png')
 return list(dict.fromkeys(names+extra_outputs(row)))

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 attach_profiles(ROWS)
 # Copy exact user references. Nothing in the approved visual direction is rewritten.
 copy_reference(PLAN/'给Astra的视觉总参考.html','reference/给Astra的视觉总参考.html')
 for dirname in ['target-look','existing-style','target-look-hardcore-deprecated']:
  for path in (PLAN/dirname).glob('*'):
   if path.is_file():copy_reference(path,'reference/'+dirname+'/'+path.name)
 source_files=[ROOT/'AGENTS.md',ROOT/'docs/superpowers/specs/production/游戏制作方法与工程约定.md',ROOT/'docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md',ROOT/'docs/superpowers/specs/production/art-direction-v0.3/visual-standard-20261010.json',PLAN/'02-美术与逐招演出.md',PLAN/'08-图形与手感施工表.md',PLAN/'09-人物指令与机魂施工规格.md',PLAN/'11-名场面与系统全链补定.md']
 for src in source_files:copy_reference(src,'source-notes/'+src.name)
 background_count=export_backgrounds(ROOT,OUT,ROWS,copy_reference)
 guide_html(OUT)
 (OUT/'给Grok的背景与三视图补充指令.md').write_text(GROK_ADDENDUM)
 (OUT/'给主对话的资产接收补充指令.md').write_text(MAIN_ADDENDUM)
 for r in ROWS:
  r['current_assets']=[{'path':p,'exists':(ROOT/p).is_file(),'sha256':digest(ROOT/p) if (ROOT/p).is_file() else None} for p in r['current_assets']]
  r['code_hooks']=[p for p in r['code_hooks'] if (ROOT/p).is_file()]
  r['thumbnail']=''
  for asset in r['current_assets']:
   if Path(asset['path']).suffix.lower() in ['.png','.jpg','.webp']:
    r['thumbnail']=copy_reference(asset['path'],f'current/{r["id"]}-{Path(asset["path"]).name}');break
  r['deliverables']=outputs(r)
  r['return_directory']=f'incoming/{r["id"]}/'
 # Explicit old character art is included as identity evidence, not as style targets.
 for file in ['char_haosi_luheng_setting_v1.png','char_tangjiao_doudeng_qihai_v3.png']:
  copy_reference(ROOT/'.superpowers/brainstorm/37837-1782033239/content'/file,'reference/identity/'+file)
 # Current identity anchors remain references, not ready-made separable runtime assets.
 with (ROOT/SOURCES['locks']).open() as f:
  locks=list(csv.DictReader(f,delimiter='\t'))
 for r in ROWS:
  if r['group']!='H' or 'identity' not in r:continue
  entity_ids={s['locator'] for s in r['identity']['source_refs'] if s['source']=='canon'}
  for lock in locks:
   if lock['subject_id'] not in entity_ids:continue
   p=lock['current_art_reference']
   if p and (ROOT/p).is_file():
    dest='reference/identity/'+Path(p).name
    if not any(ref['delivered']==dest for ref in REFS):copy_reference(p,dest)
    r['identity']['identity_reference']=dest
 # A compact visual comparison at normal camera; use existing saved evidence only.
 evidence=ROOT/'artifacts/formulas/production-lab-v1/qa/B16-20261012/continuation-r2/intent-07/intent'
 for file in ['01-normal-A.png','02-hud-off-A.png','10-damaged-hud-off.png','10-collapsed-hud-off.png']:
  copy_reference(evidence/file,'current/context/'+file)
 code_sources=sorted({p for r in ROWS for p in r['code_hooks']})
 # Static resource trace. Literal reference != proof of actual runtime loading.
 reachable=set();todo=[GAME+'scenes/formula_lab/linked_campaign/round_campaign.tscn',GAME+'scripts/formula_lab/chapter_c02/shell.gd']
 while todo:
  p=todo.pop()
  if p in reachable or not (ROOT/p).is_file():continue
  reachable.add(p)
  if Path(p).suffix not in ['.gd','.tscn','.tres','.godot','.gdshader']:continue
  txt=(ROOT/p).read_text(errors='replace')
  for path in re.findall(r'[\"\'](res://[^\"\'\n]+)[\"\']',txt):
   dest=path.replace('res://',GAME)
   if (ROOT/dest).is_file():todo.append(dest)
 inventory={}
 for p in reachable:
  if Path(p).suffix.lower() in ['.png','.jpg','.jpeg','.webp','.svg','.glb','.ttf','.otf','.mp4','.webm']:
   inventory[p]='入口递归静态引用；不等同本轮运行加载证明'
 families=[A+'linked_campaign_v1',A+'linked_campaign_v2',A+'linked_campaign_v4',A+'linked_campaign_v6',A+'linked_campaign_rounds',A+'chapter_c02_v1',A+'chapter_c02_v2']
 for folder in families:
  for p in (ROOT/folder).rglob('*'):
   if p.is_file() and p.suffix.lower() in ['.png','.jpg','.jpeg','.webp','.svg','.glb']:
    inventory.setdefault(relative(p),'动态资源目录候选；包含旧版/导出副本，不能逐文件按新对象重复计价')
 for r in ROWS:
  for a in r['current_assets']:inventory[a['path']]='本清单已绑定对象；见制作项'
 mapped={}
 for r in ROWS:
  for a in r['current_assets']:mapped.setdefault(a['path'],[]).append(r['id'])
 inv=[]
 for p,note in sorted(inventory.items()):
  fp=ROOT/p;inv.append({'项目路径':p,'绑定制作项':'、'.join(mapped.get(p,[])),'盘点口径':note,'字节':fp.stat().st_size,'sha256':digest(fp)})
 write_csv('现有资源静态盘点.csv',inv,['项目路径','绑定制作项','盘点口径','字节','sha256'])
 master=[];delivery=[];mapping=[]
 for r in ROWS:
  master.append({'编号':r['id'],'类别':GROUPS[r['group']],'对象':r['name'],'用途':r['purpose'],'范围':r['scope'],'设计要求':r['design'],'状态':'；'.join(r['states']),'表情':'；'.join(r['expressions']),'规格包':SPECS[r['template']][0],'交付规格':SPECS[r['template']][1],'现用文件':'\n'.join(a['path'] for a in r['current_assets']),'接入代码':'\n'.join(r['code_hooks']),'回传目录':r['return_directory']})
  identity=r.get('identity',{})
  master[-1].update({'IP映射':identity.get('ip_mapping','不适用／场景功能素材'),'映射确定程度':identity.get('mapping_status',''),'本作背景':identity.get('background',''),'识别与性格':identity.get('retain_features',''),'设计改造':identity.get('project_design',''),'背景来源':'\n'.join(s['path']+' # '+s['locator'] for s in identity.get('source_refs',[])),'制作链':'设定→结构母版→正交视图→分件与状态→建模交接' if r['template'] in ['mecha','enemy','form','part','building'] else '按用途制作；不强套三视/建模'})
  for f in r['deliverables']:
   role='可编辑源' if f.endswith('.psd') else ('规则/时序说明' if f.endswith(('.json','.md')) else '图形/原画导出')
   expr=''
   hit=re.match(r'(bust|portrait)_(\d+)\.png',f)
   if hit:expr=r['expressions'][int(hit[2])-1]
   stage,meaning,size=delivery_info(r,f)
   delivery.append({'制作项':r['id'],'对象':r['name'],'阶段':stage,'相对交付路径':r['return_directory']+f,'内容':meaning or expr or role,'分辨率与格式':size or SPECS[r['template']][1],'交付边界':SPECS[r['template']][3]})
  mapping.append({'编号':r['id'],'对象':r['name'],'当前资源':'\n'.join(a['path'] for a in r['current_assets']) or '无独立文件或由代码生成，按下列接入位置新增','接入位置':'\n'.join(r['code_hooks']),'替换方式': '二维图按用途映射；三维需模型/UV/骨架/挂点适配；不是无检查覆盖旧文件','回传根':r['return_directory']})
 write_csv('逐项制作清单.csv',master,list(master[0]))
 write_csv('逐文件交付清单.csv',delivery,list(delivery[0]))
 write_csv('接入替换映射.csv',mapping,list(mapping[0]))
 technical=[]
 for r in ROWS:
  if r['group'] in ['M','F','E']:
   package='TECH-UNIT'
   files='model_source.blend；model.glb；rig_map.json；socket_map.json；materials.json；uv/<材质ID>.png；textures/<材质ID>_basecolor.png；preview_turntable.mp4'
   extra='需要时另交normal/roughness/emission/mask；每张贴图对应同名UV和实际材质槽；需保留骨架/挂点。若仅换现有蒙皮，先取得当前网格和UV，不能随意重排UV或骨骼。'
   if r['template']=='part' or r['key']=='old_guardian':
    files='model_source.blend；model.glb；socket_map.json；parts_and_pivots.json；materials.json；uv/<材质ID>.png；textures/<材质ID>_basecolor.png；preview_turntable.mp4'
    extra='只设挂点和必要活动轴，确有骨骼变形才加骨架映射；不强套人形骨架。工具/终端沿用母体同版本设计；只换皮时按当前真实UV。'
  elif r['group'] in ['B','T']:
   package='TECH-ENV'
   files='model_source.blend；intact.glb；materials.json；uv/<材质ID>.png；textures/<材质ID>_basecolor.png；parts_and_pivots.json；preview_turntable.mp4'
   extra='按本项状态另交damaged.glb/destroyed.glb及活动件；地面可沿用已验证结构，只换UV材质；其他贴图通道按画面需要。避免将破损物件继续盖完整屋顶。'
  elif r['group'] in ['X','C']:
   package='TECH-FX'
   files='effect_source/；effect.tscn；textures/；timing.json；parameters.json；preview_normal.mp4；preview_reduced_motion.mp4'
   extra='保留启动/生效/保持/结束事件及配色、尺度、世界/屏幕空间参数；序列帧按需交帧表、pivot、混合方式，不能只交一段成片。'
  elif r['group']=='N':
   package='TECH-MOTION'
   files='motion_source.blend；animation_library.glb；retarget_map.json；events.json；preview_normal.mp4；reuse_notes.md'
   extra='标准动作先复用授权资源并记录来源；按骨架家族适配，命中事件由各单位处理，不制作双方逐对接触参数。专属招式才单独制片。'
  else:continue
  if r['group'] in ['M','F','E','B','T']:
   files='source_design.json；'+files
   extra+=' source_design.json记录design_id、revision、母版/视图或地形断面的路径与sha256；模型须与该版本源图对照。'
  technical.append({'编号':r['id'],'对象':r['name'],'附包':package,'适用条件':'仅在委托外援同时承担此项技术制作时追加；若只交二维，以下由项目接入方完成','交付目录':r['return_directory']+'technical/','必要文件':files,'条件文件和限制':extra,'源模型与代码':'\n'.join(a['path'] for a in r['current_assets']) or '\n'.join(r['code_hooks'])})
 write_csv('技术附包清单.csv',technical,list(technical[0]))
 (OUT/'incoming').mkdir(exist_ok=True)
 (OUT/'incoming/交付说明.txt').write_text('每个制作项建立同编号子目录，例如M05。按逐文件交付清单.csv；需要建模的对象先完成设定、结构母版、同源正交视图与分件状态。参考设计版本记录模板.json填写design_record.json。只在承接技术制作时追加technical/；模型记录真实source_design.json。正式回传报告放grok-delivery/，原始版本放grok-delivery/iterations/。不要覆盖项目现用文件，也不要把二维图写成三维完成。\n')
 (OUT/'制作清单.json').write_text(json.dumps({'scope':'工务城主工程及既有前章沿用素材；固定美术方向，不改游戏或施工状态','date':'2026-10-12','updated':'2026-10-13','revision':REVISION,'items':ROWS,'specs':SPECS},ensure_ascii=False,indent=2))
 (OUT/'参考与源文件索引.json').write_text(json.dumps(REFS,ensure_ascii=False,indent=2))
 (OUT/'来源快照.json').write_text(json.dumps({'captured_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),'project':str(ROOT),'entry':GAME+'scenes/formula_lab/linked_campaign/round_campaign.tscn','launcher':'工务城-v5接上归途.command','inspection':'静态源文件与资源清单；本侧会话未运行或改动游戏','sources':[{'path':p,'sha256':digest(ROOT/p)} for p in code_sources],'item_count':len(ROWS),'delivery_file_slots':len(delivery),'resource_inventory':len(inv)},ensure_ascii=False,indent=2))
 # A return sample is a schema, not a claim that new assets exist.
 (OUT/'回传模板.json').write_text(json.dumps({'brief_revision':REVISION,'template_only':True,'artist':'填写实际制作者','items':[{'id':'M05','design_id':'king-design-填写版本','revision':'r01','files':[],'expected_examples':['incoming/M05/concept.png','incoming/M05/design_master.png','incoming/M05/design_record.json','incoming/M05/ortho_front.png','incoming/M05/ortho_right.png','incoming/M05/ortho_back.png','incoming/M05/design_views.png'],'source_tool':'填写软件或生成服务及版本','references_actually_used':[],'stage_status':{'concept':'not_started','master':'not_started','orthographic':'not_started','parts_and_states':'not_started','model':'not_commissioned','uv_materials':'not_commissioned','rig_animation':'not_commissioned','runtime_intake':'not_started'},'structural_review_file':'','missing':[],'notes':'按真实交付填写；不能以文件存在代替结构一致或游戏验收'}]},ensure_ascii=False,indent=2))
 counts=Counter(r['group'] for r in ROWS)
 intro=f'''# 超GAG美术外援逐项制作清单

本清单共{len(ROWS)}个制作项，逐文件表列出{len(delivery)}个交付文件位。文件位包括源文件、差分导出和说明，不等于{len(delivery)}张独立原画，也不等于工作量报价。所有项目为委托要求，未宣称已制作或已验收。

方向固定为用户指定的《给Astra的视觉总参考》。该参考及正反靶图原样随包提供，不重画、不另选风格。当前工程色值是旧实现解释，不要求外援照抄。旧定稿素材可重绘；人物身份、机体关系和有来源的缺肢/形态事实保留。

先打开index.html，并读背景与三视图制作规范.html。背景与IP映射.json/CSV按{background_count}项机体、形态、敌体和人物给出来源、身份、保留特征和改造要求。逐项制作清单.csv安排对象；逐文件交付清单.csv按制作阶段给出具体文件名；技术附包清单.csv逐对象列出可选的模型、UV贴图、蒙皮骨架、动作和效果制作件；接入替换映射.csv供项目接入；现有资源静态盘点.csv包含动态目录候选，不能把导出副本和旧版再计成新对象。

本包已按2026-10-13最新要求补强。原IP图像用于理解造型血统，固定视觉总参考用于决定画法；两者不能互相替代。身份与IP摘录见source-notes/背景与IP来源摘录.json，旧Roster的入队时序不自动成为当前剧情。M15更正为馆守Z轮式导览终端，与M03同一主体，不新增战斗机体。给Grok的完整制作提示词.md是首次外援委托的唯一提示词入口，已整合全部要求；旧补充稿仅指向该入口。给主对话的资产接收补充指令.md用于素材完成后的接入交接。本包没有自动发送消息。

所有要转三维的机体、敌体、形态/武器、建筑与设施，先设定→结构母版→同一设计的正/侧/背正交图→必要顶/左视和分件状态→建模。二维外援须完成到结构交接；不是只交一张漂亮设定让模型猜。头像、表情、UI和纯效果按自身用途制作，不套无用三视。设计复核写入design_record.json，模板是设计版本记录模板.json；技术模型另以source_design.json绑定真实母版和视图版本。

## 范围

工务城14台出击机体、其变形/可拆/合体形态、所有已用敌种与专关变体、人物全链、环境与地图、战术图形、UI、效果，以及用户明确要求一并重做的既有前章立绘/事件素材。前章和专关在每项标明；不会据此新造未入场机体或重写剧情。本包不把全项目所有历史草图、未入场roster和废弃版本视作当前生产对象。

## 分工

二维外援：按每项完成设计、分层原画、图标及图形源。可以只接二维包。
三维/动画/技术特效外援：若另行委托，按TECH-UNIT/TECH-ENV/TECH-FX追加可编辑制作件。
项目接入：提供最终UV模板/骨架接口，完成低模、贴图投射/重绘、骨架重定向、材质、事件挂点、加载映射、实机音画与操作检查。不得把这些未做工作算作已经批量替换。

## 回传

解压包根的incoming/下，每项一个编号文件夹。保持逐文件清单中的文件名；PSD允许以KRA或兼容分层源替代，在回传模板.json注明。所有源图不带水印、假文字、背景烘焙或未经说明的模糊裁切。外援只需交新件，不能覆盖项目game-godot现用资源。

例如：incoming/M05/concept.png、design_master.png、ortho_front.png、ortho_right.png、ortho_back.png、design_views.png、design_record.json，以及同目录的portrait.png与source.psd；M05是完全版王者。王者另需左侧/顶视说明非对称钻臂和背炮。批量接收通过资产编号映射，由项目方接入。

## 规格补充

TECH-UNIT：可编辑.blend（或可交换DCC源）+GLB+纹理+骨架/挂点映射。站立原点在地面中心；说明前向、单位制；网格、UV、材质、武器与可动件分开。保留绑姿与骨骼名称，标准动作优先重定向。纹理按真实UV模板交付，sRGB底色、线性法线/粗糙度/遮罩分别标明；不要把灯光和投影永久烘焙到底色。

TECH-ENV：可编辑低模源+GLB+UV/纹理。完整前侧背顶；破损是真断面/楼层/残骸。只给需要运动的门闸、吊臂、转台、车轮分轴，不套完整机体骨架。不把所有楼房用同一方盒贴面替代。采用图片设计后建模，预算按主镜头决定，不靠高面数或统一降精度过关。

TECH-FX：可编辑粒子/材质/序列源，启动/作用/保持/退出分段；声明混合模式、帧率、pivot、世界或屏幕空间、颜色语义和减少动态版本。二维序列仅在适用时提供；轨迹、脚印、数值由规则生成，不能烘焙到图片。

TECH-MOTION：可编辑动作源、动作库GLB、重定向映射和事件表；先复用有许可的标准动作。记录准备、推进、发射/接触、受击、恢复事件；专属体术另做。蒙皮绑定与材质贴图分别列出，不将这两种工作混成一项“蒙皮”。

## 同场审查

先按固定参考检验一组人、我方、敌方、现代楼房与攻击效果在正常镜头同场是否协调，再展开同类数量。此步骤不重选画风，也不缩减完整清单。统一检查：轮廓/主色块、不同角色脸与年龄、建筑机体比例、受损结构、头像裁切、微型/标准/大格显示、前侧背旋转、动态效果是否遮战术信息。

设计图好看不等于入游戏通过。至少检查1440×900与1920×1080、关HUD/正常/悬停/瞄准/损毁、普通与降低动态。实际文本另排；角色眼线/头部显示尺寸统一；相机和灯光不能把新源图又压回灰板或白曝。最终认可仍由用户决定。

## 当前证据边界

本清单由当前代码、资产清单、已给视觉参考和用户要求整理；未启动游戏，未改主工程、Canon、共享施工台账或认可状态。现有资源盘点为静态引用/动态目录候选，不能当作逐帧运行加载记录。未找到独立人像的条目明确要求补画。源路径与摘要供接入方核对当前版本；主线程后续变化不应被本包覆盖。
'''
 (OUT/'README.md').write_text(intro)
 render_html(counts,len(delivery),len(inv))
 # Minimal portable bundle: handoff material only, no large model binaries or old runtime.
 bundle=OUT.parent/(OUT.name+'.zip')
 with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(OUT.rglob('*')):
   rel=p.relative_to(OUT)
   # Never repack external artists' live work into the outbound brief or touch it.
   if rel.parts[0]=='grok-delivery' or (rel.parts[0]=='incoming' and str(rel)!='incoming/交付说明.txt'):continue
   if p.is_file() and p.suffix!='.py' and '__pycache__' not in str(p):z.write(p,str(Path(OUT.name)/rel))
 print(json.dumps({'items':len(ROWS),'groups':dict(counts),'delivery_file_slots':len(delivery),'static_resources':len(inv),'portable_zip':str(bundle),'zip_mb':round(bundle.stat().st_size/1024/1024,2)},ensure_ascii=False))

def render_html(counts,delivery_count,inventory_count):
 esc=html.escape
 nav=''.join(f'<a href="#group-{g}">{esc(label)} <span>{counts[g]}</span></a>' for g,label in GROUPS.items())
 parts=[]
 for g,label in GROUPS.items():
  cards=[]
  for r in (x for x in ROWS if x['group']==g):
   spec=SPECS[r['template']]
   thumb=f'<figure><img loading="lazy" src="{esc(r["thumbnail"])}" alt="{esc(r["name"])}现有素材"><figcaption>现有素材 · 仅辨认对象 · 不是画风靶图</figcaption></figure>' if r['thumbnail'] else '<div class="no-thumb">以设计要求和固定靶图制作<br><small>当前为3D/程序表现，或尚缺独立原画</small></div>'
   current=''.join(f'<li><code>{esc(a["path"])}</code></li>' for a in r['current_assets']) or '<li>无独立平面文件，或当前由程序构建；本次应制作独立设计源。</li>'
   outputs_=''.join(f'<li><code>{esc(r["return_directory"]+f)}</code></li>' for f in r['deliverables'])
   expr=f'<p><strong>具体表情：</strong>{esc(" / ".join(r["expressions"]))}</p>' if r['expressions'] else ''
   identity_ref=r.get('identity',{}).get('identity_reference','')
   identity_link=f'<p><a href="{esc(identity_ref)}">当前身份锚图（本次可重绘，不作为运行切片）</a></p>' if identity_ref else ''
   cards.append(f'''<article class="card" id="{r['id']}" data-group="{g}"><div class="card-top"><span class="asset-id">{r['id']}</span><small>{esc(r['scope'])}</small></div><h3>{esc(r['name'])}</h3><p class="purpose">{esc(r['purpose'])}</p>{profile_html(r)}{identity_link}<div class="card-body">{thumb}<div><p><strong>具体设计：</strong>{esc(r['design'])}</p><p><strong>要覆盖的状态：</strong>{esc(' / '.join(r['states']))}</p>{expr}<p><strong>规格：</strong>{esc(spec[1])}</p><p class="worksplit">{esc(spec[3])}</p><a class="ref-link" href="reference/target-look/{r['reference']}" target="_blank">查看对应方向参考 ↗</a></div></div>{pipeline_html(r)}<details><summary>逐文件交付 · {len(r['deliverables'])}个文件位（含源与差分导出）</summary><ul class="file-list">{outputs_}</ul></details><details><summary>现有资源和实际接入位置</summary><ul class="file-list">{current}</ul><p>{esc(r.get('source_note',''))}</p><ul class="file-list">{''.join('<li><code>'+esc(p)+'</code></li>' for p in r['code_hooks'])}</ul></details></article>''')
  parts.append(f'<section class="asset-group" id="group-{g}"><h2>{esc(label)}<span>{counts[g]}项</span></h2><div class="cards">'+''.join(cards)+'</div></section>')
 html_=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>超GAG美术外援逐项制作清单</title><style>
*{{box-sizing:border-box}}:root{{--ink:#253747;--paper:#f4f1e9;--muted:#5e6b73;--line:#ced5d3;--accent:#aa4437}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.7 -apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft Yahei',sans-serif}}a{{color:#175d71;text-underline-offset:3px}}aside{{position:fixed;inset:0 auto 0 0;width:270px;padding:26px 20px;overflow-y:auto;background:#172e3b;color:#e9e2d2}}aside h1{{font-size:20px;line-height:1.5;margin:0 0 8px}}aside p{{color:#aebfc5;font-size:13px}}aside a{{display:flex;justify-content:space-between;padding:8px 3px;color:#e5e9e5;text-decoration:none;font-size:14px}}aside a:hover{{color:#f1bd73}}aside span{{color:#bdc8c8}}main{{max-width:1440px;margin:0 auto 0 270px;padding:40px 40px 80px}}header h1{{font-size:36px;line-height:1.3;margin:10px 0 18px}}p{{margin:.6em 0}}.eyebrow{{color:#956043;letter-spacing:2px;font-size:13px}}.lead{{font-size:20px;max-width:950px}}.banner{{background:#e2e9e3;border-left:5px solid #478373;padding:18px 24px;margin:22px 0}}.downloads{{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}}.downloads a{{background:#233f4d;color:#f5f0e5;border-radius:5px;padding:9px 14px;text-decoration:none}}.reference-grid{{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:14px;margin:20px 0}}figure{{margin:0}}figure img{{display:block;width:100%;max-height:250px;object-fit:contain;background:#e2e5df}}figcaption{{font-size:12px;color:var(--muted);padding-top:6px}}.reference-grid img{{height:220px;object-fit:cover}}h2{{font-size:24px;margin:38px 0 15px;scroll-margin-top:100px}}h2 span{{font-size:14px;color:var(--muted);margin-left:16px}}.contract{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.contract>div{{background:#e9e7df;border-radius:6px;padding:16px 20px}}.contract h3{{margin:0;font-size:18px}}.toolbar{{position:sticky;top:0;z-index:3;background:#f4f1e9f5;backdrop-filter:blur(8px);padding:15px 0;display:flex;gap:10px;flex-wrap:wrap;border-bottom:1px solid var(--line)}}input,select,button{{font:inherit;border:1px solid #a7b5b6;border-radius:4px;background:#fffdf8;color:var(--ink);padding:9px 12px}}input{{flex:1;min-width:240px}}button{{cursor:pointer}}.cards{{display:grid;grid-template-columns:1fr;gap:18px}}.card{{background:#fffdf8;border:1px solid var(--line);border-radius:8px;padding:22px;scroll-margin-top:95px}}.card-top{{display:flex;justify-content:space-between;gap:20px}}.asset-id{{font-size:14px;font-weight:750;color:var(--accent)}}small{{color:var(--muted)}}.card h3{{font-size:23px;margin:6px 0 0}}.purpose{{color:#53717d;margin:0 0 15px}}.card-body{{display:grid;grid-template-columns:210px 1fr;gap:22px}}.card-body img{{height:210px}}.no-thumb{{border:1px dashed #b2bdb9;padding:20px;align-self:start;color:#607575;font-size:14px}}.worksplit{{font-size:14px;color:var(--muted)}}.ref-link{{font-size:14px}}details{{border-top:1px solid #dde2dc;margin-top:14px;padding-top:11px}}summary{{cursor:pointer;font-weight:600}}code{{font:12px/1.6 ui-monospace,SFMono-Regular,monospace;overflow-wrap:anywhere}}.file-list{{padding-left:20px;columns:2;column-gap:25px}}.file-list li{{break-inside:avoid}}.caption{{color:var(--muted);font-size:14px}}.hidden{{display:none!important}}.counts{{display:flex;gap:28px;padding:14px 0}}.counts strong{{font-size:26px;display:block}}.counts span{{font-size:13px;color:var(--muted)}}.notice{{border-left:4px solid #b58b49;padding:10px 18px;background:#ece5d6}}footer{{margin-top:40px;font-size:13px;color:var(--muted)}}@media(min-width:1700px){{main{{max-width:1500px}}.cards{{grid-template-columns:1fr 1fr}}.card-body{{grid-template-columns:150px 1fr}}}}@media(max-width:1050px){{aside{{position:static;width:auto}}aside nav{{display:flex;flex-wrap:wrap;gap:0 15px}}aside a{{font-size:12px}}main{{margin:0;padding:25px 20px}}.reference-grid{{grid-template-columns:1fr 1fr}}.reference-grid figure:first-child{{grid-column:1/-1}}.contract{{grid-template-columns:1fr}}}}@media(max-width:600px){{header h1{{font-size:27px}}.lead{{font-size:17px}}.card-body{{grid-template-columns:1fr}}.card-body figure{{max-width:240px}}.file-list{{columns:1}}.card{{padding:16px}}.toolbar{{top:0}}.reference-grid img{{height:160px}}}}@media print{{aside,.toolbar,.downloads{{display:none}}main{{margin:0;padding:0}}.card{{break-inside:avoid}}details{{display:block}}.cards{{display:block}}}}
</style><aside><h1>美术外援<br>逐项制作清单</h1><p>2026年10月12日<br>固定参考 · 具体对象 · 可回传文件</p><nav><a href="#brief">制作要求</a><a href="#delivery">格式与回传</a>{nav}</nav></aside><main><header id="brief"><div class="eyebrow">超GAG机器人大战 / 美术制作委托</div><h1>把现用素材做成参考里的那种游戏</h1><p class="lead">方向沿用《给Astra的视觉总参考》。本次重做具体资产，包括过去勉强定稿的素材；参考图本身保持原样，不再探索另一套画风。</p><div class="counts"><div><strong>{len(ROWS)}</strong><span>逐项制作对象</span></div><div><strong>{len(GROUPS)}</strong><span>制作类别</span></div><div><strong>{delivery_count}</strong><span>文件位，含源与差分导出</span></div></div><div class="banner">每项都有用途、具体设计、所需状态、尺寸格式、逐文件名称和现有接入位置。数量用于核对交付，不能按文件位当独立原画报价。三维模型和程序特效的转换工作另有明确分工。</div><div class="downloads"><a href="逐项制作清单.csv" download>逐项制作清单 CSV</a><a href="逐文件交付清单.csv" download>逐文件交付清单 CSV</a><a href="接入替换映射.csv" download>接入替换映射</a><a href="README.md">制作说明</a><a href="reference/给Astra的视觉总参考.html">原视觉总参考</a></div><div class="reference-grid"><figure><img src="reference/target-look/11-tactics-user-accepted.png" alt="用户指定战棋方向"><figcaption>固定战棋方向。借鉴画法、色块与机战气质；不照搬图中机设、伪文字或满屏HUD。</figcaption></figure><figure><img src="reference/target-look/04-pilot-portrait.jpg" alt="人物方向"><figcaption>固定人物方向。角色保持各自身份、年龄和职业。</figcaption></figure><figure><img src="reference/target-look/10-cutin-flash.jpg" alt="冲击演出方向"><figcaption>固定冲击档。用于标题、重要过场、招牌Cut-in。</figcaption></figure></div></header>
<section><h2>外援拿到后怎么做</h2><div class="contract"><div><h3>二维制作与技术接入分开</h3><p>外援可以只交设计、分层原画、图标和效果素材。项目方负责低模、UV、骨架动作适配、粒子材质、加载与实际游戏检查。若外援也做三维/动画，则按下面技术附包交可编辑源。</p></div><div><h3>先验证能准确执行，再展开数量</h3><p>第一组M05王者、E01啮线体、H01纪存、B01避难楼、X06钻击和G16目标光墙，在同一正常镜头下对参考检查。它们是批量前的执行校准，不是重新选风格或只交样板。</p></div><div><h3>比例和损毁必须讲常识</h3><p>敌我共用微型/小型单格/标准单格/2×2/3×3及巨构局部档；常规敌人不做成小狗。居民楼有楼层、入口、屋顶和真实断面。破楼不能仍盖完整楼顶，材质细节不能冒充几何。</p></div><div><h3>不能继续被旧实现带偏</h3><p>工程JSON里的颜色是旧实现解释，不要求照抄；参考规定的方向才是依据。各机体保留自己的英雄涂装，场景与战术标记分工；不以统一染青灰实现“统一”。</p></div></div><p class="notice">当前范围：工务城主流程、已列专关、14台出击机体及其形态，以及用户要求一并重做的前章沿用角色和事件素材。每项标明范围；不把全项目历史草图和未入场Roster偷偷算进本轮报价。</p></section>
<section id="delivery"><h2>统一交付格式和回传方法</h2><p>每项回传至 <code>incoming/编号/</code>，文件名按逐文件CSV。例：<code>incoming/M05/design_views.png</code>、<code>incoming/M05/portrait.png</code>。同时填写<a href="回传模板.json">回传模板.json</a>，注明制作者、版本、源文件和缺件。不要直接覆盖主工程资产。</p><div class="contract"><div><h3>二维图与表情</h3><p>无水印、无伪文字；透明边干净；源图2K–4K，运行降采样由项目方处理。头像是专门头肩构图。表情与立绘固定眼线、下颌和脚点，不随画布空白改变显示大小。PSD可用兼容分层KRA替代。</p></div><div><h3>TECH-UNIT 机体三维附包</h3><p>可编辑模型源、GLB、真实UV纹理、骨架和武器挂点。注明单位、前向、地面原点。保留绑姿、材质与部件身份。常规动作复用，签名体术定制。概念图不是现有UV贴图，纹理要等模板确定后制作。</p></div><div><h3>TECH-ENV 场景附包</h3><p>设计图→低模体积→UV与贴图；可见凹凸、断面、层高保留实体。门闸/转台/吊臂/列车只做必要活动轴。完整、受损、毁坏共用空间基准，不能用染黑完整模型替代破坏。</p></div><div><h3>TECH-FX 效果附包</h3><p>交可编辑效果源与元素、透明混合方式、时序、坐标空间及减少动态版本。弹道、落点、实际伤害和数字仍由游戏结果生成。常态不满屏闪光，高潮只服务一个主要动作。</p></div></div><p class="caption">当前项的“状态”是需要制作的视觉差分，不是实施进度。这里不维护第二份施工台账。标准动作项按家族复用，不能将每台机体×每种对手重复报价。</p></section>
<div class="toolbar"><input id="search" type="search" aria-label="搜索制作项" placeholder="搜索编号、对象、状态、具体要求…"><select id="group" aria-label="筛选类别"><option value="">全部类别</option>{''.join(f'<option value="{g}">{esc(label)}</option>' for g,label in GROUPS.items())}</select><button id="clear">清除</button><span id="result" aria-live="polite">{len(ROWS)}项</span></div>
{''.join(parts)}
<footer><p>本包静态核对了当前入口与资源。<a href="现有资源静态盘点.csv">资源盘点</a>共{inventory_count}条，包含动态目录候选和导出副本；不能把目录存在当作实机加载，不能把副本重复计价。<a href="来源快照.json">来源快照</a>记录本轮读到的文件摘要。</p><p>本侧会话未改运行工程、Canon、共享台账或用户认可。接入和视觉效果尚未发生；逐项制作规格是本包交付内容。最终按实机同场结果检查。</p></footer></main><script>
const cards=[...document.querySelectorAll('.card')],groups=[...document.querySelectorAll('.asset-group')],search=document.querySelector('#search'),select=document.querySelector('#group');
const textIndex=cards.map(c=>c.textContent.toLocaleLowerCase());
function filter(){{const q=search.value.trim().toLocaleLowerCase(),g=select.value;let n=0;cards.forEach((c,i)=>{{const show=(!g||c.dataset.group===g)&&(!q||textIndex[i].includes(q));c.classList.toggle('hidden',!show);if(show)n++}});groups.forEach(s=>s.classList.toggle('hidden',![...s.querySelectorAll('.card')].some(c=>!c.classList.contains('hidden'))));document.querySelector('#result').textContent=n+'项';}}
search.addEventListener('input',filter);select.addEventListener('change',filter);document.querySelector('#clear').addEventListener('click',()=>{{search.value='';select.value='';filter()}});
</script></html>'''
 html_=html_.replace('<a href="README.md">制作说明</a>', '<a href="技术附包清单.csv" download>模型·贴图·动作附包</a><a href="README.md">制作说明</a>')
 html_=html_.replace('<a href="#delivery">格式与回传</a>', '<a href="背景与三视图制作规范.html">背景与三视图规范 ↗</a><a href="#delivery">格式与回传</a>')
 html_=html_.replace('<a href="README.md">制作说明</a>', '<a href="背景与三视图制作规范.html">设定→三视→建模要求</a><a href="背景与IP映射.csv">背景与IP表</a><a href="给Grok的完整制作提示词.md">给Grok的完整提示词</a><a href="README.md">制作说明</a>')
 html_=html_.replace('</style>', '.identity-panel{margin:18px 0;padding:16px 20px;border-left:4px solid #4d8278;background:#eef1e9}.identity-panel p{font-size:15px}.identity-panel details{font-size:14px}.pipeline-inline{padding:12px 16px;background:#e9e6d8;border-radius:4px}</style>')
 html_=html_.replace('<section id="delivery">', '<section id="design-chain"><h2>先把人物与机体设计清楚，再交给建模</h2><p>本次已将IP映射、项目背景、原作识别特征和必须保留的身份逐项展开。需要建模的对象必须交<strong>设定图 → 结构母版 → 同源正交三视 → 分件与状态</strong>；建筑另有顶视，非对称与可变形对象补专用视图。三张独立生成、结构各不相同的图不算三视图。</p><p><a href="背景与三视图制作规范.html#turnaround">查看对齐示意与各类别交付要求</a> · <a href="设计版本记录模板.json">设计版本与实际结构复核模板</a> · <a href="给主对话的资产接收补充指令.md">后续主对话接收说明</a></p><p class="caption">保留298项编号：M15是M03馆守Z的轮式导览终端，不是第15台独立战斗机体。旧定稿可重绘，用户指定的美术方向保持原样。</p></section><section id="delivery">')
 html_=html_.replace('2026年10月12日<br>', '2026年10月12日编制 · 13日核对<br>')
 html_=html_.replace('<div class="contract"><div><h3>二维图与表情</h3>', '<p class="caption">外援若同时做模型、UV贴图、蒙皮骨架、动画或技术特效，按<a href="技术附包清单.csv">逐对象技术附包</a>追加；只承接二维时，这些制作件由项目方负责。</p><div class="contract"><div><h3>二维图与表情</h3>')
 (OUT/'index.html').write_text(html_)

if __name__=='__main__':main()
