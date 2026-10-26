#!/usr/bin/env python3
"""Author the plan's diagrams as editable SVG. Numbers are design examples, not game proof."""
from pathlib import Path
from html import escape
import json, math

HERE=Path(__file__).resolve().parent
OUT=HERE/'图解'
OUT.mkdir(exist_ok=True)
C={'ink':'#233d4b','muted':'#607682','paper':'#f0f0e7','card':'#fffdf5','line':'#cedbd3','teal':'#197a82','cyan':'#55b5bb','green':'#429771','red':'#cd604b','gold':'#d2a253','purple':'#8879ae','water':'#67a4b1','floor':'#c0c9bb','wall':'#607986'}
parts=[]; manifest=[]
def raw(s): parts.append(s)
def rect(x,y,w,h,fill=None,stroke=None,r=8,sw=1,extra=''):
 raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill or C["card"]}" stroke="{stroke or "none"}" stroke-width="{sw}" {extra}/>')
def text(x,y,s,size=22,color=None,weight=400,anchor='start'):
 raw(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color or C["ink"]}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')
def lines(x,y,ss,size=20,color=None,step=31,weight=400):
 for i,s in enumerate(ss):text(x,y+i*step,s,size,color,weight)
def line(x,y,x2,y2,color=None,sw=3,dash=None):
 raw(f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{color or C["teal"]}" stroke-width="{sw}" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def path(d,color=None,sw=3,fill='none',extra=''):
 raw(f'<path d="{d}" fill="{fill}" stroke="{color or C["teal"]}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def arrow(x,y,x2,y2,color=None,sw=4,dash=None):
 color=color or C['teal']; line(x,y,x2,y2,color,sw,dash)
 a=math.atan2(y2-y,x2-x); n=10+sw
 p1=(x2-n*math.cos(a-.43),y2-n*math.sin(a-.43));p2=(x2-n*math.cos(a+.43),y2-n*math.sin(a+.43))
 raw(f'<polygon points="{x2},{y2} {p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="{color}"/>')
def poly(points,fill,stroke=None,sw=2):
 raw(f'<polygon points="'+ ' '.join(f'{x},{y}' for x,y in points)+f'" fill="{fill}" stroke="{stroke or fill}" stroke-width="{sw}" stroke-linejoin="round"/>')
def circle(x,y,r,fill,stroke=None,sw=2):raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')
def badge(x,y,label,color=None):
 circle(x,y,16,color or C['teal']);text(x,y+7,label,19,'#fffdf5',700,'middle')
def begin(id,title,subtitle,h=760):
 global parts
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1160" height="{h}" viewBox="0 0 1160 {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}。整改设计示意，非实机截图。</desc><g font-family="PingFang SC,Noto Sans CJK SC,sans-serif">']
 rect(0,0,1160,h,C['paper'],r=18);text(34,47,id+'  '+title,30,weight=700);text(34,81,subtitle,19,C['muted']);text(1126,h-20,'整改设计示意 · 非实机 · 参数为示例',16,C['muted'],anchor='end')
def save(id,name,caption,doc,anchor,work):
 raw('</g></svg>'); filename=f'{id}-{name}'
 (OUT/(filename+'.svg')).write_text(''.join(parts))
 manifest.append({'id':id,'name':name,'file':'图解/'+filename+'.png','svg':'图解/'+filename+'.svg','caption':caption,'doc':doc,'anchor':anchor,'work':work})
def grid(x,y,cols=6,rows=4,s=44,tiles=None,fill=None):
 tiles=tiles or {}
 for r in range(rows):
  for c in range(cols):rect(x+c*s,y+r*s,s,s,tiles.get((c,r),fill or '#d9dfd2'),'#afc0b8',r=0)
 return lambda c,r:(x+(c+.5)*s,y+(r+.5)*s)
def unit(p,c,r,label='我',color=None,s=44,foot=1,ghost=False):
 x,y=p(c,r); w=s*foot-9;cx=x+(foot-1)*s/2;cy=y+(foot-1)*s/2
 rect(cx-w/2,cy-w/2,w,w,'none' if ghost else (color or C['teal']),color or C['teal'],r=6,sw=3,extra='stroke-dasharray="6 5"' if ghost else '')
 if not ghost:text(cx,cy+7,label,19,'#fffdf5',700,'middle')
 return(cx,cy)
def cursor(x,y):poly([(x,y),(x+4,y+27),(x+11,y+20),(x+21,y+21)],'#fffdf5',C['ink'],2)
def shield(x,y,color=None,scale=1):
 raw(f'<g transform="translate({x} {y}) scale({scale})">');path('M-13 -16 L13 -16 L12 2 Q8 15 0 20 Q-8 15 -12 2 Z',color or C['gold'],3,fill='#f7e8c3');raw('</g>')
def hp(x,y,full,lost=0,sw=15):
 for i in range(full):rect(x+i*(sw+4),y,sw,7,C['red'] if i>=full-lost else C['teal'],r=1)
def frame(x,y,w,h,n,title):
 rect(x,y,w,h,C['card'],C['line'],r=12);badge(x+26,y+29,str(n))
 units=sum(1 if ord(c)>255 else .56 for c in title)
 text(x+52,y+36,title,min(22,(w-72)/units),weight=650)
def mech(x,y,color=None,scale=1,pose='idle'):
 raw(f'<g transform="translate({x} {y}) scale({scale})">');color=color or C['teal']
 line(-9,12,-18,40,C['ink'],9);line(10,12,22,40,C['ink'],9);rect(-28,37,20,8,C['wall'],r=2);rect(13,37,21,8,C['wall'],r=2)
 rect(-20,-25,40,38,color,C['ink'],r=6,sw=2);rect(-10,-47,20,20,'#f3edd8',C['ink'],r=5);line(-6,-37,7,-37,C['cyan'],4)
 if pose=='tool':line(-21,-16,-34,8,C['ink'],9);line(23,-16,46,-11,C['ink'],10);line(46,-11,62,-11,C['gold'],8)
 elif pose=='punch':line(-23,-15,-34,7,C['ink'],9);line(23,-15,55,-15,C['ink'],10);rect(52,-24,18,18,C['red'],C['ink'],r=3)
 else:line(-23,-16,-31,9,C['ink'],9);line(23,-16,31,9,C['ink'],9)
 raw('</g>')
def iso_box(x,y,w,d,h,top='#bccbbd',left='#82968e',right='#617d81'):
 # x,y denotes the upper back corner; width and depth use isometric vectors.
 a=(x,y);b=(x+w,y+w*.42);c=(x+w-d,y+(w+d)*.42);e=(x-d,y+d*.42)
 poly([e,c,(c[0],c[1]+h),(e[0],e[1]+h)],left,C['ink'],1)
 poly([b,c,(c[0],c[1]+h),(b[0],b[1]+h)],right,C['ink'],1)
 poly([a,b,c,e],top,C['ink'],1)
 return a,b,c,e

# G01 — layout is a designed board, not a wireframe menu inventory.
begin('G01','画面先让出棋盘，后果画在发生的位置','常驻只留任务、回合与队伍；详细信息跟着当前对象。',800)
rect(34,108,1092,627,'#d8e0d6',C['line'],r=16)
rect(50,123,1058,58,'#254c59',r=8);text(70,159,'回合 02',22,'#fffdf5',700);text(210,159,'城防  5   预计 −1',22,'#f5e4b7')
text(566,159,'A 供能',20,'#c2dad4');rect(692,133,144,37,C['gold'],r=5);text(764,159,'B 跨渠桥',20,C['ink'],650,'middle');text(865,159,'C 装卸站',20,'#c2dad4')
rect(55,197,235,61,C['card'],r=7);text(71,222,'当前阻塞：桥下拆解者',19,weight=650);text(71,246,'解除威胁，列车才能通行',16,C['muted'])
tiles={(c,r):'#78a8ae' for c in (5,6) for r in range(5)}
for c in (5,6):tiles[(c,2)]='#b4a2b8'
p=grid(310,221,8,5,65,tiles)
for c,r in [(0,0),(1,0),(6,0),(7,0),(7,4)]:
 x,y=p(c,r);rect(x-24,y-24,48,48,'#71838c',C['ink'],r=3);line(x-20,y-10,x+20,y-10,'#a7b9b3',3)
unit(p,2,3,'我',s=65);unit(p,3,2,'敌',C['red'],65);unit(p,3,1,'',C['teal'],65,ghost=True)
bx,by=p(4,2);rect(bx-26,by-26,52,52,'#b4a2b8',C['ink'],r=3);text(bx,by+7,'桥',21,C['ink'],700,'middle');hp(bx-28,by-42,4,2,10)
sx,sy=p(2,3);ex,ey=p(3,3);arrow(sx+27,sy,ex-8,ey,C['green'],5);ex,ey=p(3,2);gx,gy=p(3,1);arrow(ex,ey-22,gx,gy+10,C['gold'],7)
arrow(ex+28,ey,bx-27,by,C['red'],3,'5 5');line(ex+44,ey-8,ex+56,ey+8,C['red'],4);line(ex+56,ey-8,ex+44,ey+8,C['red'],4)
cursor(gx+29,gy+27)
rect(650,467,320,112,C['card'],C['teal'],r=8,sw=2);text(671,499,'液压顶推 · 无直接伤害',20,weight=650);text(671,529,'桥来袭伤害  5 → 2',23,C['teal'],700);text(671,558,'本轮仍有跨区炮 2 伤害',17,C['red'])
rect(55,622,547,80,'#284d59',r=7);rect(68,633,58,58,'#f3e0b2',r=4);mech(97,666,C['teal'],.49);text(140,651,'预算二号',21,'#fffdf5',650);text(140,680,'移动 2 / 5    主行动 ●',17,'#c4dad4')
for i,(label,col) in enumerate([('1 维修',C['card']),('2 顶推',C['gold']),('3 造墙',C['card'])]):
 rect(337+i*81,640,75,42,col,r=4);text(375+i*81,668,label,15,C['ink'],600,'middle')
rect(885,632,208,54,C['card'],C['teal'],r=6);text(989,666,'结束回合 · 余 3 行动',17,C['ink'],600,'middle')
badge(69,288,'1');lines(95,295,['任务只留下一步','点标题定位实物'],18,step=27)
badge(939,226,'2');lines(964,232,['顺位与轨迹','来自实际意图'],17,step=26)
badge(950,399,'3');lines(975,405,['瞄准时才显示','本招结果'],17,step=26)
text(55,765,'① 常驻少    ② 悬停看对象    ③ 瞄准看差值    ④ I 展开规则',20,C['teal'],650)
save('G01','棋盘与HUD','这是界面布局草图，机体方块仅代表站位，不是美术目标。看信息分别出现在哪里；桥损伤与城防损失使用不同量纲。','00-总方案','opening',['U03','U04','A04'])

begin('G02','四个状态，就能完成一次普通行动','普通命令：悬停看后果，点击执行；右键退一层。Ctrl 手势始终只控制相机。',890)
for i,(title,desc) in enumerate([
 ('自由探索',['未选中时：悬停敌人看轨迹','不用点击，也不用先打开资讯窗。']),
 ('点己方，默认走位',['光标决定落点；绿色线实时绕障','点合法格直接走过去。']),
 ('选招后，光标预演',['敌机虚影、推距、桥的损失一起变','无误伤等额外风险，点目标就执行。']),
 ('动作结束，回到棋盘',['接地、位移、血条与威胁划除同步','已用主行动；有余格仍可移动。'])]):
 x=32+(i%2)*560;y=113+(i//2)*337;frame(x,y,536,314,i+1,title)
 p=grid(x+25,y+70,6,3,44);unit(p,1,2,'我');unit(p,3,1,'敌',C['red']);unit(p,4,1,'桥',C['purple']);unit(p,2,1,'障',C['wall']);
 ex,ey=p(3,1);bx,by=p(4,1)
 if i>=2:
  ox,oy=p(1,2);rect(ox-17,oy-17,34,34,'#d9dfd2',r=0);unit(p,3,2,'我')
 if i==0:arrow(ex+20,ey,bx-20,by,C['red'],4);cursor(ex+16,ey-22)
 if i==1:
  # The solid object blocks the direct diagonal; route follows empty cells.
  a=p(1,2);b=p(2,2);c=p(3,2);line(*a,*b,C['green'],5);arrow(*b,*c,C['green'],5);cursor(c[0]+6,c[1]+5)
 if i==2:
  gx,gy=unit(p,3,0,'',C['teal'],ghost=True);arrow(ex,ey-13,gx,gy+8,C['gold'],6);arrow(ex+19,ey,bx-19,by,C['red'],3,'5 5');text(x+320,y+123,'桥来袭伤害',19,C['muted']);text(x+320,y+159,'5 → 2',30,C['teal'],700);cursor(ex+12,ey+13)
 if i==3:
  # Redraw the old square as empty; the moved unit occupies the new cell.
  xx,yy=p(3,1);rect(xx-17,yy-17,34,34,'#d9dfd2',r=0);unit(p,3,0,'敌',C['red']);text(x+315,y+124,'已取消一条威胁',18,C['teal'],700);text(x+315,y+158,'主行动 ○',21,C['muted'])
 lines(x+26,y+243,desc,19,step=30)
rect(32,800,1096,51,'#dce7df',r=8);text(53,832,'需要多一步的只有：选择吊运落点、误伤/致败确认；普通移动不再套确认菜单。',21,C['ink'],600)
save('G02','鼠标四态','沿四幅小棋盘读操作：观察 → 选中走位 → 瞄准 → 结果。绿色线是行走路线；金色箭头是目标被推的方向，两者不可混用。','01-核心机制与操作','## 5. 鼠标交互状态机',['U01','U02'])

begin('G03','六种招式，必须画出六种空间结果','方块是规则示意；方向、第一遮挡、范围和终点都由真实动作合同生成。',1030)
names=['推移：方向与距离都要准确','拘束：锁步，仍可能开火','贯穿：打穿单位，停在实体墙','爆破：中心与四邻受伤，不外推','群盾：中心 2 点，相邻对象 1 点','吊运：先抓载荷，再选落点']
caps=['箭头两格；撞墙/落水另列后果。','锁步用绳圈；保留仍然有效的红炮线。','首个敌人不是终点，墙才截断射线。','四邻标损伤；别画成震荡弹的推箭头。','敌我同效；盾挡伤害不等于挡推落。','两次选参；合法净空与载重都要检查。']
for i in range(6):
 x=32+(i%2)*560;y=112+(i//2)*294;frame(x,y,536,276,i+1,names[i]);p=grid(x+23,y+74,8,3,47)
 if i==0:
  unit(p,1,1,'我',s=47);a=unit(p,2,1,'敌',C['red'],47);b=unit(p,4,1,'',C['teal'],47,ghost=True);arrow(a[0]+15,a[1],b[0]-9,b[1],C['gold'],7)
 elif i==1:
  unit(p,1,1,'我',s=47);a=unit(p,3,1,'敌',C['red'],47);b=unit(p,6,1,'桥',C['purple'],47);circle(*a,26,'none',C['gold'],3);line(x+98,a[1],a[0]-28,a[1],C['gold'],3);arrow(a[0]+28,a[1],b[0]-21,b[1],C['red'],4)
 elif i==2:
  a=unit(p,0,1,'我',s=47);unit(p,2,1,'敌',C['red'],47);unit(p,4,1,'敌',C['red'],47);b=unit(p,6,1,'墙',C['wall'],47);arrow(a[0]+18,a[1],b[0]-23,b[1],C['cyan'],6);text(x+387,y+123,'截断',16,C['muted'])
 elif i==3:
  for c,r in [(3,0),(2,1),(3,1),(4,1),(3,2)]:
   xx,yy=p(c,r);rect(xx-21,yy-21,42,42,'#efbea8',C['red'],r=2);text(xx,yy+7,'−2',18,C['red'],650,'middle')
  unit(p,0,1,'我',s=47);circle(*p(3,1),12,'none',C['red'],3)
 elif i==4:
  unit(p,3,1,'领',s=47)
  for c,r,lab,col in [(3,0,'敌',C['red']),(2,1,'桥',C['purple']),(4,1,'友',C['teal'])]:
   xx,yy=unit(p,c,r,lab,col,47);shield(xx+16,yy-13,scale=.55)
  xx,yy=p(3,1);shield(xx+15,yy-15,scale=.7);text(x+387,y+121,'中心×2',15,C['muted'])
 elif i==5:
  a=unit(p,2,1,'箱',C['gold'],47);unit(p,1,1,'吊',s=47);b=unit(p,5,1,'',C['teal'],47,ghost=True);path(f'M{a[0]} {a[1]-22} Q{(a[0]+b[0])/2} {y+70} {b[0]} {b[1]-22}',C['purple'],4);arrow(b[0],b[1]-32,b[0],b[1]-7,C['purple'],4);badge(a[0],a[1]-33,'1',C['gold']);badge(b[0],b[1]-33,'2',C['purple'])
 text(x+24,y+251,caps[i],18,C['muted'])
save('G03','六类招式的正确示意','对应报告 FX01–15。用箭头只表示实际位移；拘束、爆破、施盾和吊运不共用一张“冲向敌人”的示意图。','01-核心机制与操作','## 2. 建立通用的对象—动作—后果体系',['F01','U03','V06'])

begin('G04','行动额度、跨回合准备和动画时长分开','此图解释当前整改采用的逐机回合；移动额度并不与攻击动画秒数相加。',690)
for j,(x,w,title,col) in enumerate([(245,285,'第 N 回合 · 玩家阶段',C['teal']),(545,220,'敌方与环境',C['red']),(780,340,'第 N+1 回合',C['teal'])]):
 rect(x,115,w,46,col,r=6);text(x+w/2,145,title,20,'#fffdf5',650,'middle')
for y,title,sub in [(217,'普通机体','移动与主行动分账'),(341,'蓄力武器','准备与释放各占主行动'),(468,'持续支撑','保持站位，直到明确解除')]:text(34,y,title,23,weight=650);text(34,y+31,sub,16,C['muted'])
for x,w,label in [(245,75,'走 2'),(330,100,'出手 ●'),(440,90,'再走 3')]:rect(x,190,w,69,'#d8e6dd',C['line']);text(x+w/2,232,label,21,C['ink'],600,'middle')
text(257,287,'示例：移动 5 用完；主行动用完',17,C['muted'])
rect(245,317,285,64,'#ecd6a7');text(387,355,'准备 ● · 扣物资一次',22,C['ink'],650,'middle');line(532,347,775,347,C['gold'],5,'7 5');rect(780,317,340,64,'#bcd7ce');text(950,355,'释放 ● · 不重复扣物资',22,C['ink'],650,'middle')
rect(245,444,285,64,'#d8d0e6');text(387,483,'开始支撑 ● · 锁定站位',20,C['ink'],650,'middle');arrow(540,478,1110,478,C['purple'],5);text(796,438,'跨阶段持续生效',18,C['purple'],650);text(795,523,'解除前：预告失去支撑的后果',17,C['muted'])
rect(34,572,1086,62,C['card'],C['line']);text(55,610,'播放 1.2 秒、快进或跳过，只改变观看时长；不改变费用、伤害和最终站位。',21,C['teal'],650)
save('G04','行动与时间','上排用 5 格移动额度举例，不把它作为所有机体统一数值；下两排显示跨回合的真实代价。','01-核心机制与操作','## 1. 行动预算必须一句话讲清楚',['F01','F04'])

begin('G05','同一座工务城，三种材料与空间气质','共用制作精度和信息层级，环境与机体各自保留配色。下图是配色与体块样板。',780)
specs=[('A · 供能前庭','#819b8a','#c8bea8','#b37b49',['鼠尾草绿','暖混凝土','铜与陶瓷']),('B · 跨渠桥座','#968dab','#69a5b0','#596f85',['灰紫桁架','矿物青水面','冷色阴影']),('C · 环下装卸站','#b46e5b','#7997ac','#c89650',['瓦红箱体','蓝灰甲板','吊机涂装'])]
for i,(title,a,b,c,labels) in enumerate(specs):
 x=32+i*376;rect(x,112,348,595,C['card'],C['line'],r=12);text(x+22,153,title,24,weight=650)
 iso_box(x+140,340,167,112,35,b,'#87988f',c)
 if i==0:
  iso_box(x+110,223,74,53,117,a,'#6a857b','#4c6872');iso_box(x+203,290,36,31,62,'#e4d7b6','#b0ad95','#87918b')
  for k in range(4):line(x+64,282+k*14,x+105,300+k*14,'#b9c5b3',4)
 elif i==1:
  iso_box(x+134,275,165,72,22,a,'#706c86','#585c76')
  for k in range(3):poly([(x+93+k*54,337),(x+118+k*54,281),(x+145+k*54,356)],'none','#686680',5)
  for k in range(3):line(x+94,397+k*9,x+188,418+k*9,'#c1dfdc',2)
 else:
  iso_box(x+140,296,127,51,57,a,'#945e52','#774f49');iso_box(x+171,252,104,45,44,'#829da9','#637d91','#506577')
  for k in range(5):line(x+110+k*22,326+k*9,x+110+k*22,359+k*9,'#725c54',2)
 mech(x+245,392,'#c7654b',.64)
 for k,col in enumerate((a,b,c)):
  rect(x+22+k*98,464,89,32,col,r=5);text(x+22+k*98,520,labels[k],14,C['muted'])
 lines(x+22,577,['角色红白涂装独立保留','只有操作信息局部发光','阴影分层，不把全图压暗'],18,step=31)
save('G05','三战场配色与体块','此图确定材质分区、明暗和主色关系，不充当最终场景概念图。小红白机体用于检查环境衬托；不能把机体全部染成场景色。','02-美术与逐招演出','## 1.',['A01','A02','A03'])

begin('G06','地面要有结构，贴图只负责它擅长的细节','板厚、排水槽、支座和断口用几何；粗糙度、磨损与标线由材质补足。',760)
frame(32,111,526,452,1,'目前的问题：一个平面承担所有层次');frame(580,111,546,452,2,'改造：从剪影到材质逐层建立')
iso_box(218,272,217,154,12,'#c4c3ad','#9caa9c','#748b88')
for i in range(1,4):line(218+i*50,272+i*21,64+i*50,337+i*21,'#858f82',2)
text(61,481,'画上线条，仍然没有沟槽和断面。',21,C['muted'])
raw('<g transform="translate(0 -28)">')
iso_box(784,314,217,154,63,'#b6c3b3','#7b928b','#567581');iso_box(784,273,217,154,22,'#bcc9b9','#92a69a','#698686')
for j in range(3):
 for i in range(4):iso_box(788+i*51-j*49,256+i*21+j*21,48,45,11,['#b7c5b4','#c7ccba','#aabfaf'][(i+j)%3],'#92a69a','#758e88')
path('M764 389L960 471',C['ink'],10);path('M764 389L960 471','#7798a0',4)
for k in range(4):line(960-k*44,475-k*18,960-k*44,511-k*18,'#52707b',5)
arrow(1036,259,939,349,C['teal'],3);text(1017,238,'板厚',19,C['teal'],650)
arrow(1081,439,940,438,C['teal'],3);text(1030,418,'排水槽',19,C['teal'],650)
raw('</g>')
text(611,544,'厚度与层次，关掉 HUD 仍看得见。',21,C['muted'])
for x,n,t,d in [(34,'1','剪影 / 体积','地块边缘、台阶、断裂和悬挑'),(405,'2','结构 / 功能','接缝、支座、轨枕、散热和排水'),(776,'3','材质 / 痕迹','金属与混凝土差异、受力与磨损')]:
 badge(x+17,601,n);text(x+43,608,t,21,weight=650);text(x,644,d,18,C['muted'])
text(34,705,'装饰高低不自动改变通行；可站层、深坑和障碍有独立规则标识。',20,C['teal'],650)
save('G06','地面从平面到结构','改造焦点是几何和材质分工：不能仅换颜色，也不能把地面变成无纹理的光滑积木。','02-美术与逐招演出','## 2. 12 类场景资产逐项整改',['A02','A01'])

begin('G07','造墙要演出“从哪里来、怎样落地、何时可用”','预算二号的预制段发射为例；时间是初调样本。机械关节传力，不做整机橡皮挤压。',740)
for i,(title,tt) in enumerate([('工具展开','0.00 s'),('预制段发射','0.25 s'),('落地与锚固','0.60 s'),('挡线与就绪','1.10 s')]):
 x=32+i*282;frame(x,112,250,408,i+1,title);text(x+22,188,tt,20,C['muted']);line(x+17,414,x+230,414,C['wall'],3)
 mech(x+62,373,C['teal'],1.02,'tool')
 if i==0:rect(x+110,350,29,17,C['gold'],C['ink'],r=2)
 if i==1:
  rect(x+154,305,58,24,C['gold'],C['ink'],r=3);path(f'M{x+123} 351Q{x+152} 295 {x+186} 312',C['gold'],4);arrow(x+125,350,x+163,321,C['gold'],3)
 if i>=2:
  poly([(x+152,406),(x+160,357),(x+207,357),(x+220,406)],'#9caeaa',C['ink'],3)
  for dx in [160,184,209]:line(x+dx,401,x+dx,420,C['gold'],4)
 if i==2:
  for dx,dy in [(-18,0),(12,-16),(20,8)]:line(x+184+dx,420+dy,x+184+dx*1.5,420+dy*1.6,C['gold'],3)
 if i==3:
  arrow(x+229,343,x+209,364,C['red'],4);text(x+183,450,'耐久 ●●●',15,C['teal'],650,'middle')
 text(x+125,490,['机关打开','看得到运动轨迹','接地 / 尘与锚','射线在墙前终止'][i],17,C['muted'],anchor='middle')
text(34,574,'一个接触事件，同步四层反馈',25,weight=650)
for i,(t,c) in enumerate([('模型落地',C['teal']),('地面扬尘',C['gold']),('金属冲击声',C['purple']),('预告射线截断',C['red'])]):
 x=34+i*281;rect(x,602,250,56,c,r=7);text(x+125,638,t,21,'#fffdf5',650,'middle')
text(34,704,'造物尚未落地时不提前刷新成实体；快进和跳过仍到达同一规则终态。',20,C['muted'])
save('G07','工程招式四段分镜','对应 MV13 和报告 JC01。先做一招完整样板，再用同样的清晰程度分别制作维修、支撑、拘束和吊运；不是复制同一个攻击动画。','02-美术与逐招演出','## 4. 动画的 11 层，不靠单一大爆炸补救',['V01','V02','V06'])

begin('G08','同一座桥遇险，换机体就换一种解法','不靠技能名字区分谱系；比较它改变了什么，以及留下什么代价。',740)
configs=[('预算二号 · 顶推',['推离接触点，停止这一条拆解','敌机仍活着，下轮还需处理。']),('白色样机 · 光束',['换到桥侧，沿纵线清除敌人','穿透线不可继续打到桥。']),('货柜领袖 · 施盾',['吸收部分伤害，维持站位','消耗盾值，敌方仍会攻击。'])]
for i,(title,ss) in enumerate(configs):
 x=32+i*376;frame(x,114,348,531,i+1,title);p=grid(x+22,197,6,5,50)
 ex,ey=unit(p,2,2,'敌',C['red'],50);bx,by=unit(p,3,2,'桥',C['purple'],50)
 if i==0:
  unit(p,2,3,'我',s=50);gx,gy=unit(p,2,1,'',C['teal'],50,ghost=True);arrow(ex,ey-18,gx,gy+4,C['gold'],6);arrow(ex+21,ey,bx-21,by,C['red'],3,'5 5');line(ex+25,ey-7,ex+39,ey+7,C['red'],3)
 if i==1:
  ax,ay=unit(p,2,4,'我',s=50);arrow(ax,ay-22,ex,ey-65,C['cyan'],6);line(ex-13,ey-13,ex+13,ey+13,'#ffe5b5',4);line(ex+13,ey-13,ex-13,ey+13,'#ffe5b5',4)
 if i==2:
  unit(p,4,2,'领',s=50);shield(bx,by,scale=1.15);arrow(ex+23,ey,bx-20,by,C['red'],4)
 lines(x+22,492,ss,18,step=31);text(x+22,596,['无伤控位','射线杀伤','防护保全'][i],26,C['teal'],700)
text(34,695,'同一套“目标—效果—对象属性”规则，让友机、敌机、货箱、建筑都能成为组合材料。',20,C['muted'])
save('G08','换机体就换解法','这是针对同一威胁的三种编队样本，不是三招必做的固定流程。解法差别来自装备和对象属性；底层不判断机体名字。','03-机体与人物体系','## 2. 全部 14 台备选的职责',['R01','R03','L03'])

begin('G09','尺寸和飞行，必须真正改变可走的位置','小型与标准均占 1×1；王者占 2×2。飞越资格与落位资格分别检查。',760)
for i,t in enumerate(['标准 1×1：能穿过窄口','重型 2×2：需要完整走廊','飞行 2×2：越障后仍需四格']):
 x=32+i*376;frame(x,114,348,545,i+1,t);tiles={(c,2):C['wall'] for c in range(6) if c!=2};p=grid(x+22,201,6,6,50,tiles)
 if i==0:
  a=unit(p,2,4,'我',s=50);b=unit(p,2,0,'',C['teal'],50,ghost=True);arrow(a[0],a[1]-22,b[0],b[1]+12,C['green'],5)
 if i==1:
  unit(p,1,4,'王',s=50,foot=2);cx,cy=p(2,2);circle(cx,cy,25,'none',C['red'],3);line(cx-16,cy+16,cx+16,cy-16,C['red'],4)
 if i==2:
  a=unit(p,1,4,'王',s=50,foot=2);b=unit(p,3,0,'',C['teal'],50,foot=2,ghost=True);path(f'M{a[0]} {a[1]-35}Q{x+130} 253 {b[0]} {b[1]}',C['purple'],5,extra='stroke-dasharray="7 6"');arrow(b[0]-20,b[1]+21,b[0],b[1],C['purple'],5)
 lines(x+22,560,[['按格扣移动','绕路仍可抵达目标'],['一格缺口不能挤过','不能只检查中心格'],['这里假定矮墙可飞越','高墙、顶棚另查净空']][i],20,step=33)
text(34,707,'小体型用统一战棋规格体现；不按原设米数把不同 IP 缩放成一堆大小不一的零件。',20,C['muted'])
save('G09','占地与飞行','中图证明 2×2 不只是放大模型；右图也不意味着所有飞行都能无视障碍。低空、高空、顶棚与防空按能力分别判断。','03-机体与人物体系','## 3. 七台重点机体的特色建议如何吸收',['F02','S06','R02'])

begin('G10','三个工作面，属于同一座城市','按真实地理关系组织总览：C 装卸站在西，B 桥在中部，撤离口在东；A 位于北侧。',800)
path('M65 593Q92 119 588 148Q1032 176 1094 641','#cbd4c8',30)
text(87,155,'共同的大柱环 / 远景高架',19,C['muted']);arrow(1089,264,1089,190,C['ink'],3);text(1088,175,'北',18,C['ink'],650,'middle')
iso_box(577,179,213,113,46,'#96ad91','#728d7b','#517377');text(558,276,'A 供能前庭',25,C['ink'],700)
iso_box(207,435,216,123,52,'#b98267','#9a6a58','#6b7174');text(166,548,'C 装卸站',26,C['ink'],700)
iso_box(607,440,195,112,52,'#a197b2','#7a7592','#5e687f');text(570,549,'B 跨渠桥',26,C['ink'],700)
iso_box(971,451,141,86,37,'#b4c4a6','#8ba58c','#658583');text(920,565,'撤离口',25,C['ink'],700)
path('M245 600L993 600',C['wall'],17);path('M245 600L993 600','#efe6c9',4);arrow(850,600,1013,600,C['gold'],7)
rect(257,562,100,34,'#e0b765',C['ink'],r=6,sw=2);for_wheels=[274,339]
for x in for_wheels:circle(x,600,8,C['ink'])
text(363,639,'列车始终沿同一路线向东，切区不倒转方向',21,C['ink'],650)
arrow(512,326,295,448,C['teal'],6);text(336,360,'供电 → 可行车',19,C['teal'],650)
arrow(669,329,648,440,C['teal'],6);text(689,390,'供电 → 永久抢修',19,C['teal'],650)
path('M222 404Q167 229 439 213',C['purple'],4,extra='stroke-dasharray="8 6"');arrow(414,214,448,215,C['purple'],4);text(79,316,'C 断馈电',19,C['purple'],650);text(69,345,'A 敌炮停火',19,C['purple'],650)
arrow(372,477,512,477,C['purple'],5);text(377,451,'调度 / 供料',18,C['purple'],650)
rect(34,686,1092,62,C['card'],C['line'],r=8)
text(54,711,'镜头语言：源头动作 → 沿连接传递 → 目标响应',21,C['teal'],650);text(54,738,'远区只开短缩略窗；点它才切主视角。玩家拖镜头时不抢控制。',18,C['muted'])
save('G10','工务城三区关系','这是战役空间关系草图，不是三个浮岛的美术。实体高架和大柱环要跨图对应；箭头区分供电、调度与车行方向。','04-战场与立体机制','## 3. 三个区在同一座城市里',['L02','U05','A02'])

begin('G11','桥上、桥下与支撑：用剖面说明因果','同一个 XY 可以有两个结构面，但目标、威胁和净空必须分别能看见、点得到。',790)
rect(33,112,1094,374,C['card'],C['line'],r=12)
rect(68,391,750,60,'#b2d0cc',r=0);path('M70 410Q165 390 262 410T470 410T680 410T812 410','#6a9eaa',3)
rect(100,243,637,30,'#a99daf',C['ink'],r=0,sw=2)
for x in [158,625]:rect(x,273,43,112,'#778d89',C['ink'],r=2,sw=2)
for x in [210,310,410,510]:poly([(x,279),(x+48,325),(x+98,279)],'none','#687d85',4)
rect(390,241,57,33,C['card'],C['gold'],r=1,sw=3);mech(354,202,C['teal'],.78)
rect(327,382,220,8,'#77938e',r=0);line(337,384,337,273,C['wall'],2);line(537,384,537,273,C['wall'],2)
mech(407,353,C['red'],.60);arrow(408,312,410,274,C['red'],4)
text(80,219,'桥面 h2',19,C['muted']);text(78,362,'检修层 h1',19,C['muted']);text(81,437,'水面 / 低层 h0',19,C['muted'])
line(448,256,834,230,C['gold'],2);text(850,220,'检修口有真实开口',19,C['ink'],650);text(850,248,'有工具才可向下操作',17,C['muted'])
line(440,345,834,336,C['red'],2);text(850,326,'桥底威胁默认可见',19,C['red'],650);text(850,354,'遮挡时用轮廓 / 剖切',17,C['muted'])
text(780,444,'旋转相机用来理解空间，',17,C['muted']);text(780,467,'不应成为发现死因的前提。',17,C['muted'])
for i,(title,sub) in enumerate([('① 支点遭破坏','支撑线标明缺了哪一段'),('② 受力面失效','圈出受影响的完整脚印'),('③ 坠落 / 支撑补救','落点、伤害、连锁先预演')]):
 x=34+i*371;text(x,532,title,23,weight=650);rect(x+26,585,255,16,'#afa3b4',r=0);rect(x+68,601,22,52,'#78918b',r=0);mech(x+182,557,C['teal'],.54)
 if i==0:line(x+67,626,x+91,649,C['red'],5);line(x+91,626,x+67,649,C['red'],5)
 if i==1:rect(x+135,580,108,24,'none',C['red'],r=0,sw=3,extra='stroke-dasharray="6 4"')
 if i==2:arrow(x+184,603,x+184,661,C['red'],4);line(x+242,637,x+264,603,C['green'],5);text(x+252,667,'撑',17,C['green'],650,'middle')
 text(x,713,sub,18,C['muted'])
save('G11','桥梁剖面与支撑连锁','对应 SP-M2/M4。图中工具通过真实检修口作用，桥板不透明穿透。下排是可选的风险链，不能不经预告让整片平台随机坍塌。','04-战场与立体机制','## 4. 九条空间基础规则',['S01','S02','S03'])

begin('G12','丰富来自可组合的局面，不靠把空格全部塞满','示例：一张局部 8×6 棋盘，同时给出推位、挡线、贯穿、封口与保护的机会。',785)
tiles={(4,r):'#78a8ae' for r in range(6)};tiles[(4,2)]='#b4a4b5';p=grid(46,147,8,6,74,tiles)
for c,r,lab,col in [(1,4,'拳',C['teal']),(6,4,'射',C['teal']),(3,2,'拆',C['red']),(6,1,'护',C['red']),(6,2,'轻',C['red']),(6,3,'轻',C['red']),(2,2,'箱',C['gold']),(4,2,'桥',C['purple'])]:unit(p,c,r,lab,col,74)
cx,cy=p(1,0);rect(cx-30,cy-29,60,58,'none',C['purple'],r=6,sw=3,extra='stroke-dasharray="6 5"');text(cx,cy+8,'+2',25,C['purple'],700,'middle')
ax,ay=p(3,2);bx,by=p(4,2);arrow(ax+26,ay,bx-26,by,C['red'],4)
ax,ay=p(6,1);circle(ax,ay,68,'none',C['red'],2);ax,ay=p(6,4);bx,by=p(6,2);arrow(ax,ay-29,bx,by-27,C['cyan'],4)
for i,(yy,title,ss) in enumerate([(167,'持续拆解者',['推开便失去接触','也可以修桥、施盾、击毁']), (292,'护群体与轻敌',['排成线提供贯穿价值','先移护群，再贯穿清群']), (417,'已公示增援口',['第 3 回合末：轻敌 ×2','堵口代价提前显示']), (542,'安全空地仍有价值',['留绕路、落位和护送空间','危险不是越多越好'])]):
 badge(696,yy-4,str(i+1),[C['red'],C['gold'],C['purple'],C['teal']][i]);text(725,yy+3,title,24,weight=650);lines(725,yy+40,ss,20,step=31)
text(46,652,'浅色空地 = 安全站位   水面 = 能力相关危险   桥 = 任务 / 承重对象',18,C['muted'])
rect(34,685,1092,55,C['card'],C['line']);text(54,719,'同一局面用三种编队解题；比较实际取消的威胁、资源和保全结果。',22,C['teal'],650)
save('G12','地形敌群与增援','布局仅用于说明选择密度，不是将全部地图锁死成 8×8。轻敌可以形成多目标回报，重敌制造持续问题；刷怪入口与到达轮次公开。','04-战场与立体机制','## 1. 关卡先画“选择”，再画地板',['E01','E02','L01'])

begin('G13','施工按完整体验推进，美术和手感从第一步就做','每个阶段横向整合；规则过测不能替代输入体验、画面和声音检查。',785)
stages=[('0','复现','版本 / 困难局面'),('1','一手可信','预演 = 结算'),('2–3','整场 / 三区','动作 + 多解任务'),('4–5','空间 / 身份','立体 + 人物组合'),('6','整体验收','三任务 + 首玩')]
for i,(n,t,sub) in enumerate(stages):
 x=215+i*182;rect(x,115,164,80,C['teal'],r=8);text(x+82,143,n+' · '+t,19,'#fffdf5',650,'middle');text(x+82,176,sub,15,'#d6e4df',anchor='middle')
lanes=[('规则与任务',C['teal'],['留存快照','通用效果 / 占地','敌种 / 增援 / 链路','多层 / 空地 / 人物','第二任务复用']),('操作与反馈',C['purple'],['输入复现','光标 / 路线 / 目标','HUD / 敌方回放','层选择 / 协同预演','无讲解首玩']),('美术与演出',C['gold'],['资产审计','地面 + 四招样板','三区 / 14 机 / 18 招','机构 / 变形 / 特写','正常镜头 + 声音'])]
for j,(title,col,ss) in enumerate(lanes):
 y=231+j*114;text(34,y+30,title,24,col,700)
 for i,s in enumerate(ss):
  x=215+i*182;rect(x,y,164,66,C['card'],col,r=7,sw=2);text(x+82,y+39,s,15,C['ink'],600,'middle')
  if i<4:arrow(x+166,y+33,x+179,y+33,col,2)
for x in [470,652,834,1016]:line(x,201,x,574,'#99aca6',2,'4 6')
rect(34,600,1092,120,'#dce7df',C['line'],r=10);text(56,638,'每道关口都检查同一件事：玩家的一手到底改变了什么？',26,C['teal'],700)
text(56,674,'规则结果  ＋  真实鼠标操作  ＋  棋盘反馈  ＋  动作与音效  ＋  玩家复述',21,C['ink'],600)
save('G13','实施顺序与验收','这张图说明并行的制作方向和集成顺序，不表示任务已开始或已验收。52 个工作包的具体依赖仍以施工表为准。','05-施工与验收','## 1. 第一轮施工从哪里开始',['Q01','Q02','Q03'])

begin('G14','通用机制怎样驱动四种呈现','以“顶推工机”为例：不是四处各写一份解释，而是一份模拟结果被四个界面读取。',850)
for i,(title,sub) in enumerate([('对象与装备',['脚印 / 质量 / 身份','工具 / 主行动 / 资源']),('玩家命令',['发起者 + 目标 + 方向','路线 + 状态版本']),('一次规则模拟',['校验 → 伤害 → 位移','碰撞 → 坠落 → 连锁'])]):
 x=34+i*373;frame(x,123,346,140,i+1,title);lines(x+26,205,sub,20,step=29)
 if i<2:arrow(x+347,195,x+370,195,C['teal'],3)
arrow(950,265,950,311,C['teal'],4)
rect(34,318,1092,161,'#dce7df',C['teal'],r=10,sw=2);text(57,355,'结果账：谁改变了谁，在哪个阶段，为什么',26,C['teal'],700)
lines(57,392,['本手：工机被推一格 → 离开桥接口 → 本轮拆解取消','另一条承诺：A 敌炮仍在 → 桥来袭伤害由 5 降到 2','每条记录都有对象、前后值、来源和父事件；市政保全没有损失。'],20,step=30)
for i,(title,sub) in enumerate([('招式小图',['显示推距和落点','不是读取一个force画箭头']),('鼠标预览',['桥来袭 5 → 2','区分本手与敌方阶段']),('执行与回看',['受力 → 滑移 → 停下','状态与血条在事件点同步']),('任务与结算',['拆解已停 / 炮仍威胁','告诉玩家下一手还缺什么'])]):
 x=34+i*277;arrow(x+127,483,x+127,523,C['teal'],3);frame(x,533,261,182,i+1,title);lines(x+21,621,sub,17,step=30)
text(34,783,'技能或任务换名字，不影响结果。改变的是数据与局面，不是新增一段特例代码。',21,C['muted'])
save('G14','通用机制与呈现','这是拟建的责任划分，展示一份可追溯结果如何服务玩家；不表示现有代码已完成重构。','06-从方案到可实现设计','## 1. 通用规则的责任边界',['F01','F04','U03'])

begin('G15','一台机体的特色从哪里来','同一套规则可以组合不同身体、武器、主体与关系，不把机体ID写成玩法分支。',845)
layers=[('身体','占地 / 质量 / 净空 / 移动','王者 2×2；过窄桥或降落都不同'),('装备','炮 / 钻 / 盾 / 翼及真实挂点','卸掉外翼，就失去对应飞行资格'),('动作','形状 / 效果 / 费用 / 时刻','双炮封两线；右臂钻强推两格'),('控制主体','驾驶者 / 机魂 / 双主体','社勇是豪司与主体 AI，两者能协商'),('意愿与关系','接受条件 / 援护 / 明确成本','拒绝在提交前；合作不免费刷行动'),('人物与成长','有限指令 / 装载 / 成长来源','保全、救援和战斗都能形成成长')]
for i,(title,sub,case) in enumerate(layers):
 y=123+i*105;rect(34,y,1092,86,C['card'],C['line'],r=9);badge(62,y+40,str(i+1));text(91,y+45,title,24,C['teal'],700);text(276,y+38,sub,21,weight=650);text(276,y+68,case,19,C['muted'])
text(34,796,'玩家不用同时读六层：战斗只呈现当前选择相关的条件，其余进入整备与悬停详情。',20,C['muted'])
save('G15','机体六层体系','从通用对象到机体身份的配置分工。参数和招式是玩法候选，人物事实遵守现有实体资料。','03-机体与人物体系','## 1. 一台机体的六层定义',['R01','P01','P05'])

(HERE/'图解清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'svg_count':len(manifest),'directory':str(OUT)},ensure_ascii=False))
