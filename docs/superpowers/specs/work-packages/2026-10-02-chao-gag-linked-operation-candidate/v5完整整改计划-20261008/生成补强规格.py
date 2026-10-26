#!/usr/bin/env python3
"""Publish authored people/identity contracts and the bounded experiment plan."""
from pathlib import Path
from collections import Counter
import json,runpy,hashlib
P=Path(__file__).resolve().parent
S=runpy.run_path(str(P/'补强设计源.py')); L=S['layer_data']()
source=P/'给Astra的补强与补全清单.html'
L['review_source']={'file':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
data=json.loads((P/'计划数据.json').read_text())

def table(headers,rows):
 def cell(v):return str(v).replace('|','／').replace('\n','<br>')
 return '| '+' | '.join(headers)+' |\n|'+ '|'.join('---' for _ in headers)+'|\n'+'\n'.join('| '+' | '.join(cell(v) for v in row)+' |' for row in rows)+'\n'
def link(id,page='09-人物指令与机魂施工规格'):
 return f'[{id}]({page}.html#{id})'

# One primary delivery gate per report record. Broader records retain an explicit later remainder.
first_groups={'操作16项','bug13项','美术12项','造型8条','语义色10项','演出通用12条','手感19项','SML规格35项','实测招式18招','逐招定制13条','示意错误15项'}
first_ids={'COLOR-2','SP-BASE1','SP-BASE4','SP-BASE7','SP-BASE9','AIR-01','AIR-02','AIR-04','AIR-18','AI-P1','AI-P2','AI-P3','AI-P4','AI-P5','AI-P6','AI-P7','ENEMY-3413','ENEMY-3414','ENEMY-3415','DG-SYS01','DG-SYS02','DG-SYS03','DG-SYS04','DG-SYS05','DG-SYS07','DG-SYS08','DG-SYS09','DG-SYS11','DG-SYS17','DG-SYS18','PERSON-01','PERSON-02','PERSON-05','SPIRIT-1','SPIRIT-4'}
first_ids.update(f'ASSET-{i:02}' for i in [1,2,3,4,5,6,7,8,10,11,12])
first_ids.update(f'SIG-{i}' for i in range(1,7))
system_groups={'原设计系统20项','七台招牌重建','人物关系12项','精神首批8条','精神扩展2条'}
assignments={}
for r in data['coverage']:
 if r['group']=='章节索引':continue
 id=r['id'];g=r['group']
 scope='首关依赖' if g in first_groups or id in first_ids else '系统恢复专关' if g in system_groups and id not in {'DG-SYS16','DG-SYS20','PERSON-04','PERSON-09','PERSON-10','PERSON-12'} else '全量／对照'
 ref=r.get('first_level_reference','07-首关施工规格.html#section-1')
 cases=['GW-RESCUE-R1'] if scope=='首关依赖' else ['Q02-FULL']
 if g=='卡组12项' or id=='PERSON-04':ref='10-专关与成长对照规格.html#'+('CARD-11' if id=='PERSON-04' else id);cases=['P04-DECK-01','P04-GROW-01/02/03']
 if id.startswith('SPIRIT-'):
  s=next(x for x in L['spirits'] if x['id']==id);ref='09-人物指令与机魂施工规格.html#'+id;cases=[s['case']]
 if id.startswith('SIG-'):
  ref='09-人物指令与机魂施工规格.html#'+id;cases=['R03-SIGNATURE-'+id.split('-')[1].zfill(2)]
  if scope=='首关依赖':cases=['GW-RESCUE-R1','GW-R1-SOUL'] if id=='SIG-1' else ['GW-RESCUE-R1']
 if id in {'DG-SYS01','DG-SYS02','DG-SYS03','DG-SYS04','PERSON-01','PERSON-02','PERSON-05'}:
  ref='09-人物指令与机魂施工规格.html#section-'+('2' if id in {'DG-SYS01','DG-SYS02'} else '4');cases=['GW-R1-COMMS','GW-R1-SOUL']
 if scope=='系统恢复专关' and cases==['Q02-FULL']:
  cases=['P05-CONSENT-01','R03-SIGNATURE-01/07']
 if g in {'美术12项','场景资产12类','造型8条','语义色10项'} and scope=='首关依赖':cases=['READ-A','READ-B','READ-C'];ref='07-首关施工规格.html#readability'
 minimum='仅首关六机/三面/18招与对应规则；不包含同条目描述的14机、完整机构或长线故事' if scope=='首关依赖' else '本条完整系统在所列专关验证' if scope=='系统恢复专关' else '完整扩展或有结论的对照试验；不阻塞首关'
 remainder='若本条有扩展（全员、卸装、三形态、全空地），须在原工作包另关；首关通过不关闭扩展' if scope=='首关依赖' else '按工作包完整验收范围核销，不凭本页合同算完成'
 assignments[id]={'scope':scope,'spec_ref':ref,'cases':cases,'minimum':minimum,'remainder':remainder,'status':'待实施','evidence':{'config':None,'recording':None,'counterexample':None}}
L['delivery_assignments']=assignments
L['scope_counts']=dict(Counter(a['scope'] for a in assignments.values()))
L['first_dependency_nodes']=[
 {'id':'R1-BASE','items':['Q01','F01','R01','P01'],'requires':[],'output':'版本、六机身份、装备/费用与出席配置'},
 {'id':'R1-SIM','items':['F02','F03','F04','F05','F06','F07'],'requires':['R1-BASE'],'output':'统一结果、损失分账、冲突、合法路线、接口与传输'},
 {'id':'R1-INPUT','items':['U01','U02','U03','U04','U05','U06','U07','U08','U09'],'requires':['R1-SIM'],'output':'鼠标直操、只在风险时确认、语义预览、撤回回看和Ctrl镜头'},
 {'id':'R1-ART','items':['A01','A02','A03','A04'],'requires':['R1-BASE','R1-SIM'],'output':'六机和三面美术子集，READ-A/B/C题面可读；非12机构全部'},
 {'id':'R1-MOTION','items':['V01','V02','V03','V04','V05','V06','V07'],'requires':['R1-ART','R1-SIM'],'output':'18招/15图/输入时点/音画/来源正确的通讯切入'},
 {'id':'R1-PEOPLE','items':['P02','P03','P05','R03'],'requires':['R1-INPUT','R1-BASE'],'output':'只实现SPIRIT-1/4、配置A共用实例、社勇免费意愿与六机招牌最小集'},
 {'id':'R1-MISSION','items':['E01','E02','E03','L01','L02','S01','S02','R02'],'requires':['R1-SIM','R1-INPUT','R1-ART'],'output':'三道题/波次/同城方向/2×2与两形态子集；不含全卸装或全高度机构'},
 {'id':'R1-EVIDENCE','items':['Q02','Q03'],'requires':['R1-MISSION','R1-PEOPLE','R1-MOTION'],'output':'五类实机证据＋通讯/意愿反例＋六机盲辨；未提供以前保持待实施'},
]

L['task_gates']={}
for t in data['tasks']:
 mapped=[id for id,a in assignments.items() if t['id'] in next(r['work_packages'] for r in data['coverage'] if r['id']==id)]
 tiers=sorted({assignments[id]['scope'] for id in mapped},key=S['SCOPES'].index)
 if any(t['id'] in n['items'] for n in L['first_dependency_nodes']):
  tiers=sorted(set(tiers)|{'首关依赖'},key=S['SCOPES'].index)
 L['task_gates'][t['id']]={'tiers':tiers,'first_slice':next((n['output'] for n in L['first_dependency_nodes'] if t['id'] in n['items']),'不进入首关施工子集'),'evidence':{'configuration':None,'recording':None,'counterexample':None},'counterexample':S['TASK_COUNTEREXAMPLES'][t['id']],'status':'待实施'}

(P/'人物与成长施工合同.json').write_text(json.dumps(L,ensure_ascii=False,indent=2)+'\n')

md=['# 人物指令与机魂：谁在帮忙，谁有权拒绝，怎样落到棋盘',
 '本册落实[第二轮补强清单](给Astra的补强与补全清单.html) A1、A2、A4、A5。设计版本 `'+S['VERSION']+'`。首关行动预算、回合顺序和18招时钟保持07/08的规定；新增的是原稿缺少的字段、固定条件和验收局。**这是可施工的Candidate设计，尚未接入Godot。**',
 '来源强弱明确区分：实体资料只约束身份与已有能力；fable5与报告里的精神名称、审批章和卡组是设计提案；本册补定的次数、范围、处罚、场景坐标是本次设计选择，不冒充已接受剧情。',
 '查证入口：[人物／机体登记表](../../../data/canon/entities.tsv)按下面entity_id检索；[fable5整合设计§4.2](../../../game-design/2026-08-10-full-game-design-candidate-v1/external-reviews/fable5/11-v3.1-integrated-gameplay-and-character-design.md)为精神名称和人物岗位的提案来源；原报告§7与第二轮清单为整改要求。D7指这份fable5设计，不是正式剧情授权。',
 table(['实体锚点','资料明确的原话／约束','本次才补定的设计'],[
 ['V353U024 / SOCIAL_BRAVE_AI_REFUSAL','“承担完整合体、巨大工具、主体选择和AI拒绝”；当前主体为社勇王AI','危险扇面四态判定、固定伤害、实名财物例局'],
 ['MECHA_C02_COMPLETE_KING','“基础身体、外翼、盾组、钻进组件和背负式重炮都有真实战术价值”','战棋2×2规格、炮钻参数、唯一部件对象和重装费用'],
 ['V353U047','“远射、侦察和机动换位路线机”','护群标定接力及精瞄/改快射，不采用奇数轮禁火'],
 ['V353U032','“以廉价替代件完成高价值工程”；预算进入成本','备件1修3、零伤顶推、唯一回收支架'],
 ['V353U033','“非致命控制、封路和警戒单位”','索锁步不禁炮、实体警戒墙、保全计奖'],
 ['V353U043','“作业变形、护送和领袖支援主力”；已有身体和独立人格','护场格形、载荷/乘员ID、落位和载客限制']]),
 '社勇第一次正式拒绝在故事里还有“先完成一次漂亮勇者行动”的前提；GW-R1-SOUL仅是动作沙盒，不能直接替代那一场戏，也不改已接受Reader。其他原案梗缺少出处时，均在相应行标为报告提案或本版原创。',
 '## 1. 先钉住出席表与首关范围',
 table(['验证关','实际出席／岗位','带入能力','范围说明'],[[r['id'],'、'.join(r['people']),'、'.join(r['abilities']),r['note']] for r in L['attendance']]),
 '同一人在同一验证局最多两条限次精神。首关纪存一条、白鸢一项免费预演；豪司保留驾驶与双主体身份，但不同时塞入全部精神。七海、兜灯、陆衡出场由各自专关显式配置，离场后不留可用按钮或冒用台词。预算二号没有明确主体来源，不能补一个想象中的驾驶员。灰崎警备CH048的当前实体资料指向C11，不能仅凭报告映射让她变成工务城已到场人物；此处用“当班警备驾驶席”的测试资格验证规则。',
 '## 2. 一张确定指令卡，三个入口共用一次机会',
 '卡是同一能力的呈现方式。人物头像下方展开1—2张卡；战场通讯保留“人物能力／精神指令”双页签，分别筛选常驻信息与有限指令；目标旁的小通讯按钮只是跳到适用于该目标的同一张卡。**技能栏只放机体装备动作；不会再放一份同名精神。**',
 table(['字段','类型／固定语义','首关例子'],[
 ['card_id','稳定显示ID，不拥有独立余额','CARD-JICUN-LISTEN'],['source_person_id / attendance_id','真实出席者与本局岗位','CH_JICUN / GW-RESCUE-R1'],['ability_instance_id','任务＋人物＋能力的唯一实例；三区共享','run17:CH_JICUN:SPIRIT-1'],['effect_ref / target_filter','指向下面精神合同，不在UI里另写伤害逻辑','SPIRIT-1 / 通讯与自愿条件'],['cost / uses','主行动、移动、精神点均0；有限次数单独1→0','0主行动；本战1次'],['phase / scope','提交阶段与传递到哪个区','玩家阶段；已连通的B'],['disabled_reason','第一条真实失败原因＋定位缺条件对象','工单未核验，点此查看'],['preview_hash / command_fingerprint','读取集合＋命令参数；过期必须重算','禁止重用上一次目标的许可'],['portrait / short_cue','头肩头像；同尺寸立绘，来源是实际说话者','纪存，不用全身图作头像']]),
 '操作顺序：点头像→选指令→鼠标到目标预演→左键目标提交。目标旁入口可少一步；仅不可逆财物损失才弹一次风险确认。右键先退选目标，再收卡；没有“点卡、安排、确认、返回战场”四层按钮。选卡不锁住地图检查；Ctrl仍独占镜头。卡内三行足够：“停工机／桥来袭 −3／本战1次”；资格细节按I展开。',
 '有限指令原子提交：校验出席、通讯、目标、意愿和版本→克隆状态模拟→显示差值→提交时再校验同版本→写效果和扣次一次→播放。双击同command_id只返回原回执；同帧两种入口竞争同能力实例，只有首个合法提交成功。已经生效再要求取消不退款；完整回合重置才一起恢复世界、事件、证据与次数。SPIRIT-6作为命令附着，与被协商攻击同时扣次。',
 '原字段 `sp=4`、“同轮只能选一人”、延后一拍不能直接迁入；这里不存在共享SP条，也不让基本预演收费。',
 '## 3. 十条精神的完整合同',
 '以下每条都有确定目标、次数、阶段、结果字段和反例。字段是拟新增通用能力结果字段，必须由模拟器产生事件；UI不得直接修改SimulationResult来伪造预测。精神/卡共同走 `EvaluateCommand → SimulationResult`。基础意图、地形、承重、意愿及失败原因始终免费。']
for s in L['spirits']:
 md += [f'<a id="{s["id"]}"></a>\n### {s["id"]} · {s["name"]} / {s["owner"]}',
 table(['要素','施工值'],[['来源与改编',s['source']],['验收去向',s['scope']+' / '+s['case']],['目标资格',s['target_filter']],['费用','不限次、免费' if not s['uses'] else '每场/任务1次；主行动0、移动0、共享SP0；成功提交扣次'],['生效阶段',s['phase']],['确定效果',s['effect']],['模拟输出','；'.join('`'+x+'`' for x in s['result_fields'])],['失败反馈',s['failure']]])]
md += ['## 4. 机魂四态与反提案：在点击之前说明白',
 table(['返回值','使用条件','玩家下一步'],[['accept','已通过全部主体与安全条件','正常预演和提交'],['conditional','原命令可以被接受，但列出的可完成条件还没满足','看到具体缺项；完成后重验，不预扣次数'],['reject','人员安全或其他明确底线不可越过','原命令不可提交；仍可给安全替案，不以精神强制通过'],['counterproposal','原方案当前不被同意，但存在已验证的替代Command','点替案回到正常地图瞄准；不是免费多做一手']]),
 '返回 `ConsentResult{state, subjects, public_predicates, reason_code, counterproposals[], cost_delta, snapshot_hash, command_fingerprint}`。反提案必须包含actor、skill、target、path、facing、resource_cost；不能只有一句“换条路”。若底层物理/资源不合法，先返回ValidationFailure，不借机魂台词掩盖寻路错误。主体未建档时不调用四态求值，结果consent=null、has_consent_subject=false，界面标not_applicable；基础能力和安全规则仍正常检查。未知资料不等于愿意，涉及人员的未知状态按通用安全校验拒绝。',
 '人类玩家看见的是“会打伤避难所，社勇不同意”＋地图上受伤对象＋“移1格改打单拳”按钮。它不是强制大段吵架演出。接受反提案走新Command，正常扣它实际需要的移动/主行动；仅沿用同等费用时才写“费用不变”。已付的终式准备成本不倒退。',
 '同状态、同命令、同费用必须返回同一个同意结果。提交期间把费用、效果和consent_token一起提交；提交后不随机反悔。有新事件破坏先决条件，旧预览立即标“局面已变”，重新预演后才允许下一次提交。',
 table(['意愿卡／主体','公开触发与底线','条件与可执行替案','精神与验证局'],[[r['id']+' / '+r['unit']+'<br>'+r['identity'],r['trigger']+'；'+r['hard'],r['soft']+'；'+r['alternative'],r['spirit']+'<br>'+r['case']] for r in L['consents']]),
 '意愿不奖励“故意造成分歧”。不采“败选一方下轮气势+1”的可刷方案，也不采满气势强制必杀/奇数轮禁火。预算与歌翼的not_applicable是资料边界，不是声称完整机魂系统已恢复。',
 '## 5. 六机招牌定稿与后续完整规则',
 '六机不是六个不同颜色的伤害数。各自至少改变射界、位移、保护或保全方式之一。首关最小集使用已有18招；全装卸装、审批流程等进入紧随的R03专关，不能再只留一句“未来恢复”。']
for s in L['signatures']:
 md += [f'<a id="{s["id"]}"></a>\n### {s["id"]} · {s["unit"]}',table(['要素','合同'],[['文档锚点',s['source']],['首关可辨规则',s['rule']],['如何在画面认出',s['tell']],['范围与验证',s['minimum']],['18招／FX引用',' · '.join(f'[{x}](08-图形与手感施工表.html#{x})' for x in s['moves']+s['fx']) or '后续独立制作，不冒用现有18招'],['后续完整合同',s['later']]])]
md += ['盲测方法固定：10名未参与开发者先看六机各一段不超过20秒的身份与工具介绍，然后将机名、数值标题和专属配色遮掉，随机播放六段效果预览，每人六题、共60答。先说影响对象/位移/取消威胁，再从六机选身份。因果答对≥54/60、身份答对≥48/60、每机≥7/10；原始答案、误认对与录像全部保存。测试名称是“经短介绍后的辨识”，不是从零猜名字。当前没有受试结果。',
 '## 6. 一局怎么验：首关与人物专关手顺',
 '以下都是固定测试初态，不是自动生成的剧情，也不是实际通过记录。GW-R1-SOUL是首关动作沙盒可重放快照，不改07开局路线；它在首关交付中验证意愿，正常六手路线依然成立。']
for f in L['fixtures']:
 md += [f'<a id="{f["id"]}"></a>\n### {f["id"]} · {f["board"]}',table(['初态','玩家手顺','必须出现的结果','必须失败的反例'],[[f['setup'],f['steps'],f['expect'],f['negative']]])]
md += ['其他意愿专关最小初态：P05-CONSENT-02王者2×2锚(1,2)，翼落格(3,2)被占/空两版本，离开水面仍有/无飞行两版本；03雷翎(1,2)吊载于邻格，目的(6,2)满员，备用(6,3)合法/塌落；04货柜(2,2)2×1载4人，邻接卸客格全占/开放一格；05警备(1,3)索住(3,3)工机，旁(3,4)为深水，有人/无人两版本；06预算资料不设置soul_id而维修正常；07歌翼身份未定时不出现虚构精神或人格台词。均为9×7独立图，每例只切一个条件；具体承重和动作费用复用已声明合同。',
 '## 7. 旧实现怎样接回，哪些规则不能复用',
 table(['现有代码／资产','复用部分','必须迁移／禁止照搬'],[
 ['stage_battle/tactics/squad_comms.gd','通讯双页签、头像/半身立绘容器、短对白队列','去掉共享sp、delay拍数、同轮人物名额；改读同一个AbilityInstance'],
 ['candidate/c02_short_plan/combat_comms.gd','头像裁切方式、人物卡布局、选中/可用/失败状态','旧CARDS效果不是当前合同；白鸢预演由每场1次改免费系统能力'],
 ['round_rules.gd / tactical_contract.gd','现有逐机命令与效果解析入口','接ValidateAbility/EvaluateConsent/CommandModifier；不在人物UI直接写HP或返主行动'],
 ['round_loadout.gd','credits/reputation、已有模块、按run_id防重复领取','P04扩展贡献ID/XP/交易快照，首关stock配置不被成长自动修改'],
 ['model_motion.gd / round_skill_stage.gd','原18招与3D舞台','按08时钟接署名/同意/护盾结果，人物能力不会再生成半透明残留机体']]),
 'P03确定指令的整局验收：使用P02-PERMIT-01的三人出席表，所有入口共用实例；从头像发动“记录在案”，目标旁再次打开时显示已耗尽；从双页签请求撤令，棋盘预演work解锁但保留物理开关。换掉七海后两张卡移除，基础武器和免费预演仍在。不出现抽牌、能量或弃牌区。录屏和同一事件回执齐全后才能称配置A已恢复。']
(P/'09-人物指令与机魂施工规格.md').write_text('\n\n'.join(md)+'\n')

md=['# 专关、成长与范围收口：每个系统怎样证明，何时采用',
 '本册落实第二轮清单A3、B2、C，也为A1/A4/A5提供后续验证关。随机牌组仍是报告提出的对照建议；人物确定指令和机魂规则先做。此处给出能实际执行的实验、数字和退出条件，**不表示实验已运行，也不把它们塞进首关。**',
 '## 1. 首关之后的顺序与专关出口',
 table(['出口','进入条件','完整交付／反例','对外可说的结论'],[
 ['GW-RESCUE-R1','07/08配置＋本册依赖闭包','六手/换防/首玩/18招/泊位坍塌；另有通讯和意愿反例','只有真实证据齐才说“首关可玩”'],
 ['P02＋P03','首关实际通过，通用Ability接口稳定','09十条精神专关；共享实例扣次；确定卡三入口；全部失败句','分别说精神或配置A已恢复；不捎带随机牌组'],
 ['P05＋R03','人物身份与共享结果源完成','双主体四态、六机招牌、卸装/支架/变形全流程；身份空缺明确保留','逐系统验证，不用一句台词等同机魂完成'],
 ['P04-DECK-01','P02/P03/P05已实跑通过','固定种子/编队、A/A_plus/B、测量表、完整去留裁决','“配置B对照已运行，采用/搁置原因是…”'],
 ['GW-GROWTH-P04-v1','P04测试隔离配置','三关贡献曲线、交易、重复领取/友伤刷奖反例','成长对照通过，不倒改首关stock'],
 ['Q02-FULL / Q03-FULL','其余14机、机构全集、全空地、R03/P04遗留完成','全量配置、操作/画面/声音、人类首玩与第二任务','全部各自关闭后才说全量完成']]),
 'P02/P03是工作包号，带后缀的是测试关ID。R1只取对应工作包的一小部分，不要求先完成P04；原52个包保持完整范围，新增的是可验收子集，未把晚期依赖硬塞给首关。',
 '## 2. P04对照实验：把随机性的价值单独测出来',
 '<a id="P04-DECK-01"></a>',
 table(['项目','固定实验规格'],[
 ['版本／局面','GW-DECK-P04-v1；07六机三面、原装stock、冻结开局意图；每局3轮；只改牌组seed，不把敌人难度一起改变'],
 ['阶段目标','第3轮transport后：车头路径序号≥13、城防≥1、列车HP≥1、桥可通行四项同时满足；失败或中止计未达成。不是要求三轮救出24人'],
 ['种子','4101、4102、4103、4104、4105、4106。各种子同初态配对比较；敌人后续按相同确定性AI从实际局面发布意图，发布后仍冻结'],
 ['A','主版：确定人物能力，无随机牌，基本动作完整'],
 ['A_plus','同B的16实例全部公开，每轮3能量选择兼容修饰；每实例每轮至多用1次，E1/W2消耗不刷新，不抽牌。W2因无抽牌池灰态，不暗换其他增益；分辨收益来自修饰工具还是随机性'],
 ['B','16固定实例、每轮抽3、能量补3、手牌上限5、末轮弃未用、每招最多附1；消耗区本场不洗回'],
 ['人员／顺序','12人：6名未玩当前demo、6名熟悉者；每人分配2种子×3模式共6局，分两次完成。六种A/A_plus/B排列每种2人，第二种子反向；参与者p=0…11使用种子序号p%6和(p+1)%6，恰好每个种子4人使用；记录第几次接触题面，学习效应单独报'],
 ['引导一致','只解释目标和基本操作，不教解题；三模式给等长练习；不会只挑会玩的人统计'],
 ['随机与快照',L['experiment']['rng']],
 ['版本锁','计划、规则、地图、牌表、UI、演出和输入版本写入每次日志；中途改参数则新的v2重新配对，不能混算']]),
 '同一局面里，A能用工程或火力解决基本任务，B可以用窄幅导弹保车或侧推省路线。这些是待验证假设。不能因为B有更多按钮就把它判成更丰富。',
 '抽牌复现约定：初始数组严格按下表B1、B2…W2顺序，Fisher-Yates从末端交换，最终数组第0项为牌顶。以下向量由本页纸面参照程序计算，供未来实现交叉比对；不是游戏已抽出的牌。',
 table(['seed','首抽3张（有序）','洗牌后rng_state'],[[v['seed'],' / '.join(v['hand']),v['rng_after_shuffle']] for v in L['experiment']['opening_vectors']]),
 table(['指标','采集方法','采用门槛'],[
 ['基础能力／信任','空牌是否挡移动/武器/任务；预演与执行差异','必要动作因缺牌失败0次；数值与目标不一致0次'],
 ['额外点击','相同seed/回合相对A，计开栏、选牌、附着、选目标、取消、确认、切区的额外次数；按键也算操作','平均≤4，p90≤6；不能把选牌＋选目标算一次'],
 ['无效牌率','每个抽到的实例在本轮任何合法基础动作上都无兼容目标，或状态已使其必定零收益，才记无效；分母为全部抽到实例','≤20%；高耗但可用、不想用的牌另记，不偷换分母'],
 ['有效选择','两条成本/结果不同且均可实施的方案，经两人独立标注，归入伤害/位置/保护/资源/调度；换卡名不算新解','B较A的每轮有效选择中位数增加≥20%；争议样本列出'],
 ['节奏','从获得控制到结束玩家阶段，含阅读/找牌/取消；与同seed的A配对','平均回合时长≤A的1.20倍；新手/熟悉者分开报'],
 ['种子依赖','各seed三轮阶段目标达成率、资源和失败原因；不是整场救援胜率','最好/最差达成率差≤15个百分点，必要牌缺失导致失败0次'],
 ['想再玩','同人玩完三种再选，不先告诉推荐答案','至少8/12更愿重玩B而非A_plus；公布理由与原始计数']]),
 '裁决：全部硬门通过且有效选择、节奏、重玩偏好同时达标，B才进入下一轮压力关；若A_plus增加选择而B没有额外收益，主版保留确定构筑，随机性搁置；若只增加阅读/操作，两者都退回A。每seed只有4人，达成率一档就是25个百分点，15点筛查意味着本批必须同档；超出时只写“本批不能采纳”，不据此断言随机性导致失败。可以另立扩大样本的v2，不把未达标记录删掉。小样本只决定下一轮投资，不证明总体玩家偏好。当前所有实测单元为空，不生成虚构百分比。',
 '## 3. 固定16张对照牌与消耗规则',
 '六台机各2张共12；纪存、白鸢各2张共4；合计16。没有再加“每驾驶员1张”却仍叫16。实际装载是16个实例，不是无上限贡献池。缺席来源的牌不能装；同名最多2实例。本对照也禁止任何再行动牌。',
 table(['实例／来源','名字／费用','兼容动作','实际改写'],[[r['id']+' / '+r['source'],r['name']+' / '+str(r['energy'])+('能量·消耗' if r['exhaust'] else '能量'),r['tags'],r['effect']] for r in L['deck']]),
 '附着牌只预约，命令成功原子提交时才同时扣牌能量、牌实例与动作成本。合法换牌释放旧预约并预约新牌；非法换牌保留原预约并显示原因；右键撤瞄准退未提交预约。已生效的通讯牌不退款。普通牌进弃牌，E1/W2进消耗区，跨区不算新战；抽空时只洗弃牌。超过手牌5时先显示新增牌，再由玩家公开弃至5，不能静默丢牌。W2的“抽1弃1”与手满弃牌合并为一次弃选，不能弃两次。',
 '## 4. CARD-01至12：逐条可跑手顺与失败样子']
for r in L['card_cases']:
 md += [f'<a id="{r["id"]}"></a>\n### {r["id"]} · {r["name"]}',f'**对照局步骤：** {r["steps"]}。',f'**失败样子：** {r["fail"]}。',f'**证据：** 配置/seed、连续操作录屏、事件回执、反例截图。当前待实施，不能以纸面检查代替。']
md += ['## 5. 成长与既有credits/reputation怎样挂钩',
 '版本 `GW-GROWTH-P04-v1`，不在GW-RESCUE-R1启用。初始credits4、reputation0。原有七类整备模块继续使用现有费用，不新造一套牌币；以下新增的是贡献归因与试验曲线。',
 table(['来源','credits','reputation','个人/机组XP','去重与归因'],[[r['condition'],r['credits'],r['reputation'],r['xp'],r['scope']] for r in L['growth']['reward_rules']]),
 '正向贡献必须指向真实取消的威胁、实际保住的对象或完成的任务边。'+L['growth']['attribution']+' 个人每任务XP上限8。友伤再修、反复立墙拆墙、回看/重放同事件不计；同一损失只记一份声誉责任，不叠加“市政毁损＋实名”双罚。负声誉可以为负，不能被截成0逃避责任。',
 '账户归属：有人机记实际驾驶/作业者，机魂自驾记该主体；预算的身份未定时记机组熟练度，不编造人物等级。换驾驶只在战前，能力来自实际出席与适配；不允许换人刷新次数。受伤/失能但参与完成救援者保留实际贡献。',
 table(['验证场','贡献示例','累计XP／解锁','资金与交易验证'],[
 ['P04-GROW-01','完成2＋实际保全2','4，未到6','奖励新增4；余额4→8，同run_id重复领取仍8'],
 ['P04-GROW-02','完成2＋全救贡献2＋设施保护2','10，跨过6','本关奖励6，未消费余额8→14；解锁一个兼容协作模块使用资格，仍须购买，不自动装备'],
 ['P04-GROW-03','完成2＋解除公开威胁2','14，跨过14','本关奖励3，未消费余额14→17；再选不同战术方向资格；B可选兼容牌，A不被强塞随机牌']]),
 '第一档可选的具体形状：具有shield装备可选择“集中护场”模块（只保护所选格对象，盾2→3，取消该格四邻）；具有jack可选“侧向液压头”（推1改选垂直侧向，力量不增）；具有beam可选“标记中继”（标记可沿现有通讯到他区一次，仍只有下一次直接命中消耗）。均占唯一模块位，购买2credits，不能与原模块叠满；没有相应装备则不出选项。第二档解锁剩余兼容形状或保留原装，不增加主行动。它们是P04设计选择，非既有代码能力。',
 '交易使用独立4credits初态验收，不从上面17余额接算。删一个牌实例1credit，升级一级2credits；C2升级明确为轻载落距4→5，抓距仍2，过程净空照查。三选一奖励先入收藏，满16时必须替换一张才装入；也可放弃领1credit。事务记录transaction_id、前后现金、实例版本、装载变化。确认只用于永久花费；普通战斗不增加商店式二次确认。',
 '## 6. 首关依赖闭包与331条的三种去向',
 '覆盖数量不是通过数量。现在每条源记录都有首要验收去向、具体规格、测试局和空证据字段。综合条目中只完成首关子集时，扩展仍留在原工作包，不能整条打勾。168个来源章节索引单列，不当开发项。',
 table(['去向','源记录数','通过所需要的证据'],[[k,v,'仍全部待实施；具体测试局见过滤后的覆盖表'] for k,v in L['scope_counts'].items()]),
 table(['首关节点','只做哪些原工作包的子集','前置','本节点出口'],[[n['id'],' / '.join(n['items']),' / '.join(n['requires']) or '无',n['output']] for n in L['first_dependency_nodes']]),
 '上表是首关集成的依赖图。原工作包Q02/Q03全量出口仍依赖P04等；其R1子集只依赖本表R1-EVIDENCE，解决“要先做完全部系统才能验首关”的循环。每个工作包须分别登记子集证据与剩余范围，不能因子集通过改整包为完成。',
 '<!-- FIRST_ITEMS_START -->\n'+table(['报告分组','首关必须对照的ID'],[[g,' · '.join(f'[{r["id"]}]({r["detail_page"]})' for r in data['coverage'] if r['group']==g and assignments.get(r['id'],{}).get('scope')=='首关依赖')] for g in dict.fromkeys(r['group'] for r in data['coverage']) if any(r['group']==g and assignments.get(r['id'],{}).get('scope')=='首关依赖' for r in data['coverage'])])+'\n<!-- FIRST_ITEMS_END -->',
 '默认[覆盖核对](覆盖核对.html)只显示首关依赖；选择“系统恢复专关”或“完整范围331条”才展开其他内容。分类表示交付范围，不表示通过。',
 '## 7. 三档结论与每包证据',
 '每个原工作包增加结论档、证据和反例栏。证据字段现在是null，页面显示“未提供”，不创建看似已通过的录屏链接。实际交付须填配置、连续录屏、输入日志和失败反例；计划检查结果仅归入文档检查。',
 table(['结论','必须能点开的东西','不能替代它的东西'],[['首关可玩','07§9五类实机材料、R1通讯/意愿、六机辨识和READ-A/B/C首玩','331回应、JSON通过、只有截图'],['某系统已恢复','该系统字段表＋至少一局完整录屏＋负例；身份缺口已处理','标题写重建、撤回假恢复、一句角色台词'],['全量完成','14机/全机构/空地/形态/成长各项证据，B的采纳或搁置裁决','首关六机通过、实验跑完就宣布卡组成为主玩法']]),
 '## 8. 旧措辞与冲突的定点清理',
 table(['位置／旧说法','本轮替换','允许保留的范围'],[
 ['03与条目08“每场1次候选”“燃魂初始样本+2”','09逐条次数、目标、phase、结果字段；燃魂每目标每招仅+2一次','来源原话可以引用，不作为施工值'],
 ['条目07“处理决定”与07“梗规则尚未恢复”','六机最小集＋R03各完整合同；状态仍待实施','尚未接入游戏这一事实保留'],
 ['01/04“敌群2–3、每两轮增援”“起飞费用待比较”','首关引用07固定2敌和R2/R3波次；空域燃料/可切高度费用归全量专关','压力对照参数单独列在全量范围'],
 ['06“伤害样本”、U08选择范围≤100ms','统一声明首关伤害处理顺序；选中6帧/范围p95≤80ms按08','新任务的回归例局可以叫样本'],
 ['条目03/04浮动动作毫秒','18招结果时间按08固定；原报告题名保留并显式标来源','引用来源题名不冒充当前时点'],
 ['MV08旧逐招写载荷≤4，而首关配置≤3','正文统一载荷≤3、抓距2、落距3；标定改为其他友机下一次直击减护群1','更重吊载另配专用装备，不扩大首关'],
 ['CARD-01/08/11“16张首测／再行动例外／成长待选”','P04固定16实例，禁止再行动；6/14阈值、4/6/4三关曲线','随机性取舍必须等待实际对照结果']]),
 '首关同名参数不留两套并列值。完整扩展尚未定的平衡值必须标“非本关验收项”，不能靠全书统一页脚把矛盾藏起来。']
(P/'10-专关与成长对照规格.md').write_text('\n\n'.join(md)+'\n')
print(json.dumps({'spirits':len(L['spirits']),'consent_cards':len(L['consents']),'signature_contracts':len(L['signatures']),'fixed_cases':len(L['fixtures']),'scopes':L['scope_counts'],'runtime_evidence':0},ensure_ascii=False))
