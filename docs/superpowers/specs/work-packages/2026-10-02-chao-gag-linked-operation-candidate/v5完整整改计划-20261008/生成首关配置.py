#!/usr/bin/env python3
"""Write explicit design fixtures. This is not a Godot game build or a balance solver."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent

def obj(id,xy,hp,kind,**kw):return dict(id=id,xy=xy,hp=hp,kind=kind,footprint=[1,1],**kw)
def unit(id,xy,hp,move,label,**kw):
 r=obj(id,xy,hp,'ally',move=move,label=label,main=1);r.update(kw);return r
A=[unit('brave',[2,3],8,4,'勇',energy=2),unit('king',[2,5],8,5,'王',footprint=[2,2],flying=True,shield=2,ammo=2),obj('power',[4,3],4,'fixture',label='电'),obj('shelter_n',[7,2],3,'fixture',label='民'),obj('shelter_s',[9,6],3,'fixture',label='民'),obj('gun',[7,4],5,'enemy',label='炮',mass=3,setup_cell=[7,4]),obj('biter',[6,2],4,'enemy',label='啮',mass=2)]
B=[unit('engineer',[2,4],5,5,'预',spares=3),unit('cargo',[2,6],8,4,'货'),obj('dismantler',[3,3],5,'enemy',label='拆',mass=3,protected=True),obj('larva_b',[2,5],2,'enemy',label='幼',mass=1),dict(id='bridge',xy=[4,3],hp=4,kind='bridge',label='桥',footprint=[2,2],blocking=False,aligned=False)]
C=[unit('police',[5,5],6,4,'灰',spares=3),unit('leiling',[2,5],5,6,'雷',flying=True,ammo=6),obj('feeder',[6,4],3,'fixture',label='闸'),obj('crate',[4,3],2,'fixture',label='箱',mass=1,destroyed_state='removed'),dict(id='train',xy=[2,3],footprint=[2,1],hp=6,kind='train',label='车'),obj('acid',[5,3],2,'enemy',label='酸',mass=1),obj('larva_c',[2,6],2,'enemy',label='幼',mass=1)]
D={'version':'GW-RESCUE-R1','status':'candidate_build_contract_not_implemented','city_hp':7,'deadline_round':6,'passengers':24,'train_speed':4,'train_head_index':1,'boards':{
'A':{'size':[10,8],'height':2,'water':[[6,0],[6,1]],'objects':A,'palette':['#819b8a','#c8bea8','#b37b49']},
'B':{'size':[10,8],'height':1,'water':[[x,y] for x in [4,5] for y in range(8)],'objects':B,'palette':['#968dab','#69a5b0','#596f85'],'bridge_cells':[[x,y] for x in [4,5] for y in [3,4]],'interface':[3,4]},
'C':{'size':[10,8],'height':0,'water':[],'objects':C,'palette':['#b46e5b','#7997ac','#c89650']}},
'city_loss_rules':[{'objects':['shelter_n','shelter_s'],'trigger':'actual_hp_damage','amount_per_hp':1},{'objects':['power','bridge'],'trigger':'first_disabled_per_asset_id','amount':2}],
'phase_order':['player','enemy','environment','work','arrival','transport','reinforcement','refresh'],
'ground_transfer':{'main':1,'moves_after':0,'arrival':'current_round_arrival','main_after':0},'air_transfer':{'main':1,'moves_after':0,'arrival':'now','main_after':0},
'ports':[{'board':'A','xy':[7,6]},{'board':'B','xy':[7,0]},{'board':'B','xy':[0,6]},{'board':'C','xy':[8,6]}],
'backups':[{'board':'B','xy':[7,6]},{'board':'A','xy':[0,0]},{'board':'C','xy':[0,0]}],
'round1_intents':[{'order':1,'source':'dismantler','target':'bridge','damage':3,'binding':'contact'},{'order':2,'source':'gun','target':'bridge','damage':2,'binding':'setup_and_power'},{'order':3,'source':'biter','target':'shelter_n','damage':1,'binding':'relative_east'},{'order':4,'source':'larva_b','target':'engineer','damage':2,'binding':'relative_north'},{'order':5,'source':'acid','target':'train','damage':2,'binding':'world_cell_3_3_lob'},{'order':6,'source':'larva_c','target':'leiling','damage':1,'binding':'relative_north'}],
'reinforcements':[{'round':2,'board':'A','xy':[8,1],'count':1,'hp':2},{'round':2,'board':'C','xy':[6,1],'count':1,'hp':2},{'round':3,'board':'B','xy':[8,4],'count':1,'hp':2}],
'opening_paths':[{'unit':'brave','board':'A','to':[3,3],'max_cost':1},{'unit':'police','board':'C','to':[5,4],'max_cost':1},{'unit':'king','board':'A','to':[5,3],'max_cost':5},{'unit':'engineer','board':'B','to':[3,4],'max_cost':1},{'unit':'cargo','board':'B','to':[3,4],'path':[[2,6],[3,6],[3,5],[3,4]],'after_engineer_vacates':True,'max_cost':3},{'unit':'leiling','board':'C','to':[4,5],'max_cost':2}],
'opening_expected':{'city_hp':7,'bridge_hp':4,'train_hp':4,'municipal_loss':0,'head_index':5,'head':['C',7,3]},
'no_action_round1_expected':{'city_hp':4,'bridge_hp':0,'train_hp':4,'head_index':1},
'costs':{'jack':{'main':1,'range':1,'force':3,'push_distance':1,'damage':0},'drill':{'main':1,'range':1,'force':4,'push_distance':2,'damage':3},'missile':{'main':1,'ammo':1,'range':5,'damage':2,'splash_damage':2,'push_distance':0},'repair':{'main':1,'spares':1,'repair':3},'wall':{'main':1,'spares':1,'range':2,'hp':3}},
'critic_source_sha256':hashlib.sha256((P/'对Astra-v5整改计划的批评与建议.html').read_bytes()).hexdigest()}
for board in D['boards'].values():
 for u in board['objects']:
  if u['kind']=='ally':
   u['mass']={'brave':3,'king':5,'engineer':2,'cargo':4,'police':3,'leiling':2}[u['id']]
   u['capabilities']=['manipulator']+(['repair_tool'] if u['id']=='engineer' else [])
   if u['id'] in ('brave','king','cargo'):u['brace_capacity']={'brave':4,'king':6,'cargo':6}[u['id']]
   if u['id']=='cargo':u['lift_capacity']=3
D['costs']['realign']={'main':1,'spares':1,'range':1,'repair_cap':3,'requires':['repair_tool','powered','alignment_needed'],'works_at_full_hp':True}
D['costs']['beam']={'main':1,'ammo':1,'range':6,'damage':2,'stops_at':'first_entity','mark_after_hit':{'until':'enemy_end','beneficiary':'next_other_ally_direct_attack','ignore_aura_reduction':1,'uses':1,'ignores_personal_armor_or_shield':False}}
D['costs']['pin']={'main':1,'range':3,'max_mass':3,'damage':0,'disables':'active_move_only','until':'enemy_end'}
D['costs']['lift']={'main':1,'range':2,'max_mass':3,'drop_distance_from_load':3,'collision_and_support_check':True}
D['costs']['guard']={'main':1,'range':2,'center':'selected_occupied_cell','neighborhood':'four_cardinal_cells','until':'transport_end','center_shield':2,'cardinal_neighbor_shield':1,'multi_cell_rule':'maximum_once','all_factions':True}
D['people_layer']={'contract':'GW-SYSTEM-CONTRACT-20261009','first_abilities':['SPIRIT-1','SPIRIT-4'],'consent':'free_before_commit','scenario_fixtures':['GW-R1-COMMS','GW-R1-PREVIEW','GW-R1-SOUL'],'deck_or_growth_enabled':False}
D['bridge_load']={'deck':2,'train':2,'permanent_support':6}
D['reinforcement_rule']={'move':3,'damage':1,'on_block':'occupant_damage_1_delay_once_then_cancel','on_broken_surface':'cancel','acts':'next_round'}
D['train_path']=[['C',x,3] for x in range(2,10)]+[['B',x,3] for x in range(10)]+[['EXIT',x,3] for x in range(2)]
D['timing_60hz']=[dict(mv=f'MV{i:02}',contact=c,result=r,input=a) for i,c,r,a in [(1,[14],31,46),(2,[18,21,24],40,62),(3,[22],34,48),(4,[27,31],40,64),(5,[19],46,64),(6,[28],42,58),(7,[18],36,48),(8,[18,60],60,78),(9,[],42,54),(10,[24],36,50),(11,[14,22,30,38],38,48),(12,[9,15],27,39),(13,[35,41,47,53],53,66),(14,[18,30],30,42),(15,[24,44],44,58),(16,[16],22,36),(17,[34,38],44,58),(18,[],30,42)]]
(P/'首关施工基线.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')

F=[]
def fixture(n,title,actor=(1,3),foot=(1,1),targets=(),area=(),moves=(),range_cells=(),notes=(),kind='damage'):
 F.append({'id':f'FX{n:02}','title':title,'board':[9,7],'actor':list(actor),'footprint':list(foot),'targets':[{'xy':list(xy),'label':lab} for xy,lab in targets],'area':[list(x) for x in area],'moves':[{'from':list(a),'to':list(b),'label':lab} for a,b,lab in moves],'range':[list(x) for x in range_cells],'notes':list(notes),'kind':kind})
fixture(1,'贯岩钻：邻接四格机，推足两格',(1,2),(2,2),[((3,2),'敌')],[(3,2)],[((3,2),(5,2),'推2')],notes=['王者脚印：(1,2)(2,2)(1,3)(2,3)','目标(3,2) → 经过(4,2) → 终点(5,2)','右臂钻接触目标受击点；不是裆部冒钻。'])
fixture(2,'破围终式：三格一起承担后果',targets=[((3,2),'敌'),((3,3),'友'),((3,4),'物')],area=[(3,2),(3,3),(3,4)],moves=[((3,y),(4,y),'推1') for y in [2,3,4]],notes=['三格各伤4；下翼为可搬货箱，非地基','例局三目标HP6，伤4后各余2可推1','三处接触18/21/24帧，不能只演中心。'])
fixture(3,'双肩炮：两条完整射程，各自首体止步',(1,2),(2,2),[((5,2),'敌'),((7,3),'友')],[(5,2),(7,3)],range_cells=[(x,y) for y in [2,3] for x in range(3,9)],notes=['上行有效至(5,2)，下行至(7,3)','潜在范围x3…8，各6格；阻挡后只留虚线','两炮从肩部挂点出发，各打首物体3伤。'])
fixture(4,'小舞台：命中点由例局生成',targets=[((2,3),'近'),((7,3),'远')],area=[(2,3),(7,3)],notes=['此图比较两个独立例局，不是同时打两人','近接触(2,3)；无中间阻挡时远接触(7,3)','T=10；世界中心(25,表面高,35)/(75,表面高,35)。'])
fixture(5,'邻接动作：目标就在下一格',targets=[((2,3),'目标')],area=[(2,3)],notes=['1×1根在(1,3)；目标在(2,3)','拳、顶推、维修、支撑按不同动词呈现','2×2钻按FX01最邻近边，不按中心测一格。'])
fixture(6,'光束：满六格范围，不打穿首实体',targets=[((6,3),'敌'),((7,3),'友')],area=[(6,3)],range_cells=[(x,3) for x in range(2,8)],notes=['潜在格(2…7,3)，首敌在(6,3)','保留被遮挡的友(7,3)，但不标伤害','移走首敌后，下一次试算才改为击中友军。'])
fixture(7,'变形：自身脚印，无攻击目标',(2,3),targets=[],area=[(2,3),(3,3)],notes=['货柜：1×1 → 横向2×1，验(3,3)及扫掠','雷翎：仍1×1，换翼架与移动状态','不画向外攻击箭头，不显示0伤害。'],kind='form')
fixture(8,'拘束：脚印不动，不能把炮线抹掉',targets=[((4,3),'敌'),((7,3),'桥')],area=[(4,3)],notes=['敌(4,3)保持；锁步(4,3)→(5,3)','没有位移箭头，没有扣血数字','若仍能打(7,3)，红色承诺线必须保留。'],kind='pin')
fixture(9,'吊运：抓取和落位是两个参数',targets=[((3,3),'箱')],area=[(3,3),(6,3)],moves=[((3,3),(6,3),'吊3')],notes=['机(1,3)抓(3,3)：距离2','载荷原位(3,3)到落位(6,3)：距离3','画吊起→落地，落点净空承重同时检查。'],kind='lift')
fixture(10,'群盾：中心2，相邻四格有对象才加1',targets=[((3,3),'2'),((2,3),'1'),((4,3),'1'),((3,2),'1'),((3,4),'1')],area=[(3,3),(2,3),(4,3),(3,2),(3,4)],notes=['中心(3,3)盾+2；四邻对象各+1','敌我同效；空格不生成护盾实体','多格对象只取本效果的最高一次。'],kind='shield')
fixture(11,'造墙与维修：产物和补血分开',targets=[((2,3),'修'),((3,3),'墙')],area=[(2,3),(3,3)],notes=['此图比较两种独立动作，不一起生成','墙落空格(3,3)，HP3，三锚三灯','维修邻(2,3)，HP1/4→4/4，显示+3。'],kind='work')
fixture(12,'爆破导弹：十字伤害，不吹飞',actor=(1,5),targets=[((4,3),'敌'),((3,3),'友')],area=[(4,3),(3,3),(5,3),(4,2),(4,4)],notes=['五格各2伤；友(3,3)明确标误伤','爆心(4,3)，四邻的HP也在对应格响应','没有推箭头；旧外推tip必须删除。'])
fixture(13,'持续支撑：连接支点，保持站位',targets=[((2,3),'桥')],area=[(2,3)],notes=['贴邻支点，不隔空挥拳','开始22/24/28帧接触，依机体不同','离开会断支撑；三机用各自真实构件。'],kind='brace')
fixture(14,'双炮释放：仍沿已保存方向',(1,2),(2,2),[((5,2),'敌'),((7,3),'友')],[(5,2),(7,3)],range_cells=[(x,y) for y in [2,3] for x in range(3,9)],notes=['读ChargeState的锁向，不能把自己当目标','本招各−3；敌方阶段损失单独列出','准备已耗弹1；释放仅主行动1，一击提交。'])
fixture(15,'顶推入水：三项后果分别可见',targets=[((2,3),'市')],area=[(3,3)],moves=[((2,3),(3,3),'推1')],notes=['工机(2,3) → 深水(3,3)','直接伤0；落水击毁；市政损失+1','攻击取消是另一项后果，不能替代损失。'],kind='water')
for f in F:
 if f['id'] in ('FX01','FX02'):
  for t in f['targets']:t.update(hp=6,mass=2,pushable=True)
(P/'招式图施工数据.json').write_text(json.dumps({'version':D['version'],'status':'diagram_fixtures_not_runtime_results','fixtures':F},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'boards':len(D['boards']),'fixtures':len(F),'timing_profiles':len(D['timing_60hz'])}))
