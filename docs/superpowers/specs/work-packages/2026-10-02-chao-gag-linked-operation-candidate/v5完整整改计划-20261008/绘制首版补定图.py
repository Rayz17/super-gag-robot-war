from pathlib import Path
import json,html,textwrap
P=Path(__file__).resolve().parent
ROOT=next(a for a in P.parents if (a/'game-godot').exists())
D=json.loads((ROOT/'artifacts/formulas/production-lab-v1/qa/rescue-r1-20261009/case-configurations.json').read_text())
INK='#213c4e';TEAL='#347c82';RED='#bd5a50';GOLD='#b7803f';MUTED='#607581'
class SVG:
 def __init__(self,title,sub):
  self.s=['<svg xmlns="http://www.w3.org/2000/svg" width="1260" height="720" viewBox="0 0 1260 720"><defs><marker id="arr" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#347c82"/></marker></defs><rect width="1260" height="720" fill="#f4f2ea"/>']
  self.text(48,54,title,29,INK,True);self.text(48,92,sub,17,MUTED)
 def rect(self,x,y,w,h,fill,stroke='none',rx=8):self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
 def text(self,x,y,t,size=17,color=INK,bold=False):self.s.append(f'<text x="{x}" y="{y}" font-family="PingFang SC,Helvetica,sans-serif" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}">{html.escape(str(t))}</text>')
 def lines(self,x,y,words,width=30,size=18,color=INK):
  for line in words:
   for cut in textwrap.wrap(line,width=width):self.text(x,y,cut,size,color);y+=30
  return y
 def arrow(self,x,y,xx,yy):self.s.append(f'<path d="M{x},{y} L{xx},{yy}" fill="none" stroke="{TEAL}" stroke-width="3" marker-end="url(#arr)"/>')
 def finish(self,name):
  self.text(48,687,'GW-RESCUE-R1 · 配置 / 规则图解 · 非游戏美术截图',15,MUTED)
  (P/'图解'/f'{name}.svg').write_text(''.join(self.s)+'</svg>')
meta=[]
def add(n,title,sub,work):
 slug=f'G{n}-{title}';meta.append(dict(id=f'G{n}',name=title,file=f'图解/{slug}.png',svg=f'图解/{slug}.svg',caption=sub,doc='11-名场面与系统全链补定',anchor='runtime',work=work));return slug
rows=[
 ('signature_brave','把路打出来',['R1：三体蓄酸，给玩家一轮选择。','R1蓄力 → R2扇面清三体。','维护舱保持4耐久；准备期锁住站位。'],['F01','R03','V06']),
 ('signature_king','每一件都有用',['2×2身体，双线射界。','工程机推隔板 → 退离射线 → 双炮。','钻击改位置；卸炮失武器，不能白拿速度。'],['F02','R02','R03']),
 ('signature_leiling','留一条线给你',['主目标HP5，旁边护群体减伤1。','先拆护群，或用标定接力绕过护群。','标定不绕过独立护盾，不代表伤害＋1。'],['F07','R03','U03']),
 ('signature_engineer','算准这一寸',['工机贴桥，拆解威胁3伤。','先顶离接口，再吊开，最后机械复位。','补血不是接轨；托住与锁销是两种结果。'],['F05','R03','L01']),
 ('signature_police','留出救援通道',['索锁步，原地仍然会开火。','墙截线，也挡己方；受击后会被打碎。','和拳王配合6轮清场，维护舱剩2。'],['F03','R03','E03']),
 ('signature_cargo','谁也别落下',['爆箱旁边有维护舱。','中心护盾2 → 雷翎爆破 → 连爆清敌。','舱最终剩2：看完整链，不能只看第一伤。'],['F07','V03','R03']),
 ('signature_song','低空回声',['层2航空体和层0外敌投影重合。','地爆只伤中心、推四邻，空敌不受伤。','对空弹才打上层；先拆架位再飞过去。'],['S06','S07','R03'])]
for n,(key,title,notes,work) in enumerate(rows,29):
 d=D[key];v=SVG(f'{n-28:02d} / {title}',d['goal']);X,Y,C=78,166,49
 v.rect(48,127,552,457,'#e3e7df')
 for x in range(10):v.text(X+x*C+18,Y-16,x,13,MUTED)
 for y in range(8):
  v.text(56,Y+y*C+28,y,13,MUTED)
  for x in range(10):v.rect(X+x*C,Y+y*C,C-2,C-2,'#eae9df','#ccd3cc',2)
 for t in d['terrain']:
  if t['board']!='A':continue
  x,y=t['cell'];color={'deep_water':'#6fabb6','wall':'#52677b'}.get(t['kind'],'#c8be9c');v.rect(X+x*C,Y+y*C,C-2,C-2,color,'none',2)
 for f in d['fixtures']:
  if f['board']!='A':continue
  x,y=f['cell'];fp=f.get('footprint',[1,1]);w,h=fp
  v.rect(X+x*C+3,Y+y*C+3,C*w-8,C*h-8,'#d8ba85',GOLD,4)
  name={'cabin':'舱','cover':'隔板','bridge':'桥','load':'爆箱','fuel':'补给'}.get(f['id'],'设施')
  v.text(X+x*C+6,Y+y*C+27,name,13,INK,True)
 def arrow_cell(a,b):v.arrow(X+(a[0]+.5)*C,Y+(a[1]+.5)*C,X+(b[0]+.5)*C,Y+(b[1]+.5)*C)
 for a,b in {
  'signature_brave':[((2,3),(3.65,3)),((3.5,3),(4,2)),((3.5,3),(4,4))],
  'signature_king':[((3.1,3),(5.5,3)),((3.1,4),(5.5,4)),((4,4),(4,5))],
  'signature_leiling':[((2.5,3),(5.5,3)),((2,5),(5.4,4))],
  'signature_engineer':[((4,3),(4,2)),((4,2),(2,2))],
  'signature_police':[((6,3),(8,3)),((8,3),(8,4))],
  'signature_cargo':[((2,5),(4.6,4)),((5,4),(5,3)),((5,4),(6,4))],
  'signature_song':[((4,3),(4,2)),((4,5),(4,6)),((1,4),(3.5,4))]
 }.get(key,[]):arrow_cell(a,b)
 if key=='signature_police':
  v.rect(X+8*C+4,Y+4*C+4,40,40,'#d7b788',GOLD,3);v.text(X+8*C+8,Y+4*C+29,'墙',17,INK,True)
 a=0;e=0;air_marks=[]
 for u in d['units']:
  if u['board']!='A':continue
  x,y=u['cell'];w,h=u.get('footprint',[1,1]);air=u.get('layer',0)==2
  ally=u['side']=='ally';color=TEAL if ally else RED;a+=int(ally);e+=int(not ally)
  xx=X+x*C+5;yy=Y+y*C+5
  if air:
   air_marks.append((xx,yy,e,u['hp']))
  else:
   v.rect(xx,yy,w*C-12,h*C-12,color,'#f4f2ea',5);v.text(xx+5,yy+25,('友' if ally else '敌')+str(a if ally else e),13,'#fff8e9',True)
   v.text(xx,yy+h*C-7,str(u['hp'])+'HP',11,INK)
 for xx,yy,e,hp in air_marks:
  ax=xx+85;ay=yy-44
  v.s.append(f'<path d="M{xx+19},{yy+19} L{ax},{ay}" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="4 4"/>')
  v.s.append(f'<path d="M{ax},{ay-12} l16,20 l-16,-5 l-16,5 Z" fill="{RED}" stroke="#f4f2ea" stroke-width="2"/>')
  v.text(ax+22,ay,'空'+str(e),12,RED,True);v.text(ax+22,ay+16,str(hp)+'HP',11,INK)
 if key=='signature_song':
  v.text(655,569,'北侧撞墙受1伤、原地；空层3HP不变。',16,GOLD)
 v.text(655,158,'这一局要让玩家发现什么',23,TEAL,True)
 y=v.lines(655,207,notes,25,19)
 v.text(655,y+29,'对照真实对象',21,TEAL,True);y+=63
 ai=0;ei=0
 for u in d['units']:
  if u['board']!='A':continue
  ally=u['side']=='ally';ai+=int(ally);ei+=int(not ally)
  v.text(655,y,('友'+str(ai) if ally else '敌'+str(ei))+'  '+u['name']+'  '+str(u['hp'])+'HP',16,TEAL if ally else RED);y+=27
 v.text(78,624,'蓝框 / 我方    朱红 / 外敌    金色 / 设施    水蓝 / 深水',15,MUTED)
 slug=add(n,title,'起局坐标由运行配置导出；右侧路线经合法命令验证。',work);v.finish(slug)
# Rival timeline, exact sample order rather than a generic AI portrait.
v=SVG('08 / 断冠：它记住一次真实交棒','2×2身体影响推移和射线；反制只来自已经发生的事件。')
for i,(t,lines) in enumerate([('R1 · 观察',['拆侧撑：重量5→3','预算二号推东 → 雷翎直射','记两条事件，暂不减伤']),('R2 · 公布',['同两台、同方向再交棒','护板只挡1伤，一轮一次','仍会受推，不是技能免疫']),('R3/R4 · 换法',['绕到下侧，把断冠顶北','射线离开维护舱','舱4/4，撑过R4完成'])]):
 x=48+i*407;v.rect(x,165,375,300,'#e0e9e3','#b7cbc6');v.text(x+24,208,t,24,TEAL,True);v.lines(x+24,260,lines,19,19)
 if i<2:v.arrow(x+376,318,x+404,318)
v.rect(48,502,1180,125,'#efe1c7');v.lines(72,538,['边界：鼠标预演不进入记忆；单机连打不构成交棒；换向后不能暗中改承诺。','两格身体只推一格，未必清出整条射线——必须看完整足迹。'],54,19)
v.finish(add(36,'断冠的观察与破解','真实事件、下一轮发布及换向反例。',['P06','F03','E01']))
v=SVG('09 / 合体：身体和伤势都守恒','实物组件 → 2×2共同身体 → 原组件；没有复制HP或行动。')
for i,(label,hp) in enumerate([('核心',6),('腿架',3),('背肩',3)]):
 v.rect(60,153+i*127,225,100,'#dce9e4',TEAL);v.text(85,190+i*127,label,22,TEAL,True);v.text(85,226+i*127,f'真实对象 · HP{hp}',18)
v.arrow(302,326,413,326);v.rect(433,161,310,317,'#d6e0e9','#688198');v.text(460,208,'社勇王 · 2×2',25,INK,True);v.lines(460,257,['HP6＋3＋3＝12','三者行动全部消耗','受4伤：背肩3＋腿架1','合体后HP8'],16,21)
v.arrow(760,326,850,326)
for i,(label,hp,color) in enumerate([('核心',6,TEAL),('腿架',2,TEAL),('背肩',0,RED)]):
 v.rect(870,153+i*127,320,100,'#e5e7df',color);v.text(895,190+i*127,label+f' · HP{hp}',22,color,True);v.text(895,226+i*127,'原ID / 原伤势'+(' / 失能' if hp==0 else ''),18)
v.text(60,609,'分离位置不合法 → 整次拒绝、零消耗；分离成功 → 各成员本轮行动与移动均为0。',21,INK)
v.finish(add(37,'合体的身体账','伤势分配示意取自规则反例，不是未经发生的战斗战报。',['R02','P05','F02']))
v=SVG('10 / 七海：最终必须让车真的开过去','Q17旧签名与D17现场钥匙分开；权限线不吞掉机械替代线。')
names=[('R1 现场回执','邻接柜，主行动1'),('R1 锁轨事实','列车被挡 → E17'),('R2 记录＋核验','同令、同柜、本人签名'),('R2 工作阶段','持有人解除旧令'),('R3 现场开锁','机械手＋主行动1'),('R3 真实行车','剩余3格 → 过关')]
for i,(title,body) in enumerate(names):
 col=i%3;row=i//3;x=48+col*409;y=151+row*160;v.rect(x,y,369,123,'#dce9e4',TEAL);v.text(x+20,y+42,title,22,TEAL,True);v.text(x+20,y+83,body,17)
 if col<2:v.arrow(x+372,y+61,x+400,y+61)
v.s.append('<path d="M1240,210 V293 H232 V310" fill="none" stroke="#347c82" stroke-width="3" marker-end="url(#arr)"/>')
v.rect(48,502,1180,126,'#eee0c8',GOLD);v.text(70,542,'机械替代 / 不必先点完七海',23,GOLD,True);v.lines(70,581,['R1 工程机到(4,6) → 把制动架顶到(4,4) → 车同轮走完4格。','两条路线同用轨道、占用和胜利条件；没有对白传送。'],60,18)
v.finish(add(38,'七海到真实行车','串联真实事件、回执、工作阶段和车辆移动。',['P02','P03','F05']))
v=SVG('11 / 空地：看平面，也看能否作用到这一层','同格投影不等于同一个目标；先看弹种，再看落点。')
v.rect(48,144,530,440,'#dce8e9','#91afba');v.text(74,188,'层2 / 航空',24,TEAL,True);v.text(74,425,'层0 / 地面',24,GOLD,True)
v.s.append('<path d="M120,230 H520 M120,475 H520" stroke="#90a5ac" stroke-width="3"/>');v.s.append('<path d="M332,258 V449" stroke="#607581" stroke-width="2" stroke-dasharray="7 7"/>')
v.s.append('<path d="M331,196 l38,45 l-38,-12 l-38,12 Z" fill="#bd5a50"/>');v.rect(309,441,46,48,RED)
v.text(377,226,'追踪弹：只打这里',17,RED);v.text(377,474,'地爆：只打这里',17,GOLD)
v.text(72,549,'高度标、投影线与层筛选共同表达，不只换颜色。',16)
v.text(630,177,'燃料B：3 → 2 → 1 → 0',25,TEAL,True);v.lines(630,226,['每个空中轮末−1；起降各花1移动。','燃料1时提前画出迫降候选。','距离≤2，完整承重且没有占用。','按距离 → y → x选择，不随机。','合法迫降受1伤；无落位直接失能。'],26,20)
v.rect(630,438,580,151,'#eee0c8',GOLD);v.lines(651,477,['A版不计燃料，棋盘和敌人完全相同。','主战役不加燃料条。是否值得保留B，','要看人的决策与节奏，不靠规则测试代签。'],26,19)
v.finish(add(39,'空地形状与迫降','平面和高度的命中区别，燃料与迫降规则。',['S06','S07','F02']))
f=json.loads((P/'图解清单.json').read_text());f=[x for x in f if int(x['id'][1:])<29]+meta;(P/'图解清单.json').write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
print('authored',len(meta),'diagrams')
