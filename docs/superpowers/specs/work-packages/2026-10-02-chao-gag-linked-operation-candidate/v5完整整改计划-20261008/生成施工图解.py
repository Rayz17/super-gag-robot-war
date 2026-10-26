#!/usr/bin/env python3
"""Draw the fixed first-level specification from its authored fixtures.

These diagrams are design artifacts, not screenshots or runtime predictions.
"""
from pathlib import Path
import json, runpy

P=Path(__file__).resolve().parent
g=runpy.run_path(str(P/'绘制方案图解.py'))
raw,rect,text,lines,line,path,arrow,circle,grid,frame = [g[k] for k in ['raw','rect','text','lines','line','path','arrow','circle','grid','frame']]
C=g['C']; save=g['save']; fg=g['begin'].__globals__
D=json.loads((P/'首关施工基线.json').read_text())
F=json.loads((P/'招式图施工数据.json').read_text())['fixtures']
def begin(id,title,subtitle,h):
    g['begin'](id,title,subtitle,h)
    fg['parts']=[s.replace('整改设计示意 · 非实机 · 参数为示例','GW-RESCUE-R1 · 施工示意 · 非实机') for s in fg['parts']]
def tilemark(p,xy,foot,label,color,s=32,ghost=False):
    cx,cy=p(*xy);w,h=foot
    rect(cx-s/2+3,cy-s/2+3,s*w-6,s*h-6,'none' if ghost else color,color,r=4,sw=2,extra='stroke-dasharray="5 4"' if ghost else '')
    text(cx+s*(w-1)/2,cy+s*(h-1)/2+5,label,15,C['ink'] if ghost else '#fffdf5',650,'middle')
def coordgrid(x,y,cols,rows,s,tiles=None):
    q=grid(x,y,cols,rows,s,tiles)
    for i in range(cols):text(x+(i+.5)*s,y-9,str(i),12,C['muted'],anchor='middle')
    for j in range(rows):text(x-11,y+(j+.5)*s+4,str(j),12,C['muted'],anchor='middle')
    return q

begin('G16','三张题面：同一回合，六手有代价','10×8 × 3；坐标、占地、铁路与出生点直接读取首关配置。',1000)
labels={'A':'A 供能前庭 · H2','B':'B 跨渠桥座 · H1','C':'C 环下装卸站 · H0'}
for k,(bid,b) in enumerate(D['boards'].items()):
    x=34+k*374;y=181;s=32
    frame(x,110,344,397,bid,labels[bid]); tiles={tuple(t):C['water'] for t in b['water']}
    for t in b.get('bridge_cells',[]):tiles[tuple(t)]='#b8a6bf'
    q=coordgrid(x+18,y,10,8,s,tiles)
    if bid in ('B','C'):
        start=0 if bid=='B' else 2
        for j in (3,):
            a=q(start,j);z=q(9,j);line(a[0]-14,a[1]-8,z[0]+14,z[1]-8,C['wall'],2);line(a[0]-14,a[1]+8,z[0]+14,z[1]+8,C['wall'],2)
            arrow(z[0]-18,z[1],z[0]+12,z[1],C['gold'],3)
    if bid=='B':
        ix,iy=q(*b['interface']);circle(ix,iy,11,'none',C['gold'],3);text(ix,iy+5,'接',13,C['ink'],700,'middle')
    for a in b['objects']:
        col={'ally':C['teal'],'enemy':C['red'],'fixture':C['wall'],'train':C['purple'],'bridge':C['purple']}[a['kind']]
        if a['kind']=='bridge':tilemark(q,a['xy'],a['footprint'],'桥',col,s,True)
        else:tilemark(q,a['xy'],a['footprint'],a['label'],col,s)
    for v in D['ports']:
        if v['board']==bid:tilemark(q,v['xy'],[2,2],'口',C['gold'],s,True)
    for v in D['reinforcements']:
        if v['board']==bid:
            xx,yy=q(*v['xy']);circle(xx,yy,11,'none',C['purple'],2);text(xx,yy+4,'R'+str(v['round']),11,C['purple'],700,'middle')
    if bid=='A':arrow(*q(6,2),*q(6,1),C['gold'],4)
    if bid=='B':arrow(*q(3,3),*q(3,2),C['gold'],4)
    text(x+18,465,{'A':'王=2×2飞行；啮北侧就是深水','B':'接=地板接口；桥未对齐，不通车','C':'箱与酸各HP2；爆破也伤邻车2'}[bid],16,C['ink'],600)
    text(x+18,491,{'A':'民：每损1HP → 城防−1','B':'拆HP5 · 伤桥3；A炮再伤2','C':'灰关闸 → A炮停火；雷可清轨'}[bid],15,C['muted'])
for k,(title,ss) in enumerate([
    ('A不接电，B少一种解',['母线(4,3)未接：预算不能复位桥。','货柜可临时撑起，但被占住主行动。','先接电，下一轮可修桥释放货柜。']),
    ('B不架桥，C车到此为止',['车由C向东进入B，停B(3,3)。','下一格B(4,3)必须有H1桥面。','撑桥可通车；维修可解除持续占用。']),
    ('C不断线，A必须另花一手',['闸(6,4)不断：A炮继续打B桥2伤。','王者可推炮离架设点，但留下啮线体。','去C断炮，王者便可救A避难所。'])]):
    xx=34+k*374;rect(xx,534,344,167,C['card'],C['line']);text(xx+16,565,title,21,weight=700);lines(xx+16,598,ss,16,step=30)
rect(34,729,1092,108,'#244d58');text(54,760,'首轮六手：接电 → 断炮 → 钻敌入水 → 顶推保工机 → 撑桥 → 爆破清轨',23,'#fffdf5',650)
text(54,796,'结果：城防 7 / 桥 4 / 车 4 / 市政损失 0；车头到 C(7,3)。车受友伤2，是明示代价。',21,'#d8e9db')
text(34,877,'图例',20,weight=700)
for k,(lab,col) in enumerate([('我方',C['teal']),('有敌意',C['red']),('物件',C['wall']),('桥/列车',C['purple']),('深水',C['water']),('泊位/推',C['gold'])]):
    xx=111+k*164;rect(xx,858,22,22,col,r=3);text(xx+30,876,lab,18)
text(34,925,'地图是规则平面，不是最终场景；桥的高差、排洪槽断面、货箱吊环须做成可辨认的3D结构。',19,C['muted'])
save('G16','首关三张题面','一套明确的摆位，而不是关系词。蓝绿我方、砖红敌意、金色推移/泊位；图中替代解的费用见正文。','07-首关施工规格','## 3.',['L01','L02','F05'])

begin('G17','冲突按规则裁，动画不能抢先占格','每一根事件完成派生因果后，才处理下一根；不按帧率与数组遍历碰运气。',1040)
stages=['玩家','敌方','环境','工程','抵达','运输','增援','刷新']
for i,s in enumerate(stages):
    x=34+i*139;rect(x,112,120,52,C['teal'] if s=='抵达' else C['card'],C['line']);text(x+60,145,str(i+1)+' '+s,21,'#fffdf5' if s=='抵达' else C['ink'],650,'middle')
    if i<7:arrow(x+124,138,x+135,138,C['muted'],2)
lines(34,205,['同一事件内部：取命中前目标集合 → 聚合伤害 → 死亡与结构失效 → 强制位移 → 落位后果。'],19)
for i,(title,ss) in enumerate([
    ('01 同批两机争一格',['A力量4，B力量3：A占目标，B留原位。','同力按来源/目标固定生成序号，不掷骰。','争格本身不额外扣血；已受攻击伤害保留。']),
    ('02 预约遇到倒塌或强推',['炮先打塌主泊位，或已有实体被推入该格。','抵达阶段重验：用声明的备用位，否则等待。','预约不是一堵墙；不会挤走现在站着的人。']),
    ('03 大机不切成四份落位',['2×2四格中有一格占用：整个提案失败。','换位只属于明确的交换动作，整体提交。','普通同时离开不自动允许互相穿过原位。'])]):
    yy=253+i*225;frame(34,yy,1092,205,i+1,title)
    q=grid(59,yy+67,5,3,35)
    if i==0:
        tilemark(q,[1,1],[1,1],'A',C['teal'],35);tilemark(q,[3,1],[1,1],'B',C['red'],35);tilemark(q,[2,1],[1,1],'',C['gold'],35,True)
        arrow(*q(1,1),*q(2,1),C['gold'],4);arrow(*q(3,1),*q(2,1),C['red'],2,'4 4')
    elif i==1:
        tilemark(q,[1,0],[2,2],'预约',C['gold'],35,True);xx,yy2=q(2,1);rect(xx-16,yy2-16,32,32,C['ink'],r=0);text(xx,yy2+6,'×',24,C['red'],700,'middle');arrow(*q(3,1),*q(4,1),C['gold'],4)
    else:
        tilemark(q,[1,0],[2,2],'大机',C['teal'],35,True);tilemark(q,[2,1],[1,1],'占',C['red'],35)
    lines(285,yy+85,ss,22,step=38)
text(34,977,'预览必须给出同一个胜出者、同一组停步理由、同一个备用泊位；暂停/快进只改变播放时长。',20,C['teal'],650)
save('G17','同阶段冲突裁决','逐机提交之外，另处理同批强推、完整脚印和在途抵达；预留格不等于现实占格。','07-首关施工规格','## 7.',['F02','F04','U05'])

begin('G18','选中100ms，顶推650ms：反馈有固定时钟','60Hz；顿帧包含在总时长中；无伤顶推不做伤害白闪。',860)
frame(34,113,1092,215,1,'选中机体 · 6帧 / 100ms')
for i,(lab,sub) in enumerate([('F0 收到点击','状态版本与对象命中'),('F1 选中音','范围开始出现'),('F3 接令姿态','躯干+0.015格 / 膝伸2°'),('F6 稳定选中','足底圈85%→100%完成')]):
    xx=62+i*267;rect(xx,182,245,113,'#e4eee6',C['line']);text(xx+13,213,lab,20,weight=700);text(xx+13,246,sub,15,C['muted']);text(xx+13,278,'脚底与规则根节点不移动',15,C['teal'])
frame(34,354,1092,306,2,'液压顶推 · F0至F39 / 650ms')
x0=82;ww=994
for f in [0,9,15,18,27,39]:
    xx=x0+f/39*ww;line(xx,416,xx,560,C['line'],1);text(xx,587,'F'+str(f),17,C['muted'],anchor='middle')
for a,b,lab,col in [(0,9,'抵近工具',C['teal']),(9,15,'顶住/冲程',C['gold']),(15,18,'受力',C['red']),(18,27,'推1格',C['purple']),(27,39,'收杆恢复',C['teal'])]:
    xx=x0+a/39*ww;w=(b-a)/39*ww;rect(xx,444,w-3,74,col,r=3);text(xx+w/2,488,lab,14,'#fffdf5',650,'middle')
text(60,625,'F9工具接触 ｜ F15受力反馈 ｜ F27目标落位 ｜ F39可继续下令',21,weight=650)
rect(34,688,1092,113,C['card'],C['line']);lines(55,722,['音画/血条与有效接触误差≤1帧；主动作总时长误差≤2帧。','只有撞到实体才派生碰撞伤；空地上推1格，不冒“−0”，不放爆炸。'],22,step=37)
save('G18','输入与顶推时序','选择和零伤顶推的可测时点；其余18招的接触、结果与恢复帧见同册表格。','08-图形与手感施工表','## 2.',['U01','V01','V02'])

def fx_grid(f,x,y):
    s=32;tiles={tuple(t):'#edc5ae' for t in f['area']}
    if f['kind']=='water':tiles={tuple(t):C['water'] for t in f['area']}
    if f['kind']=='shield':tiles={tuple(t):'#eee0b1' for t in f['area']}
    if f['id'] in ('FX04','FX11'):
        for i,t in enumerate(f['targets']):
            yy=y+23+i*108;text(x,yy-10,'例'+str(i+1)+'：'+('近/远独立' if f['id']=='FX04' else ['维修','造墙'][i])+'，只截y=3行',14,C['muted'])
            q=grid(x,yy,9,1,s);tilemark(q,[1,0],[1,1],'我',C['teal'],s);tilemark(q,[t['xy'][0],0],[1,1],t['label'],C['gold'] if i==0 else C['purple'],s)
            arrow(*q(1,0),*q(t['xy'][0],0),C['gold'],2)
            for j in range(9):text(x+(j+.5)*s,yy+48,str(j),12,C['muted'],anchor='middle')
        return
    q=coordgrid(x,y,9,7,s,tiles)
    if f['range']:
        for yy in sorted({a[1] for a in f['range']}):
            rr=[a for a in f['range'] if a[1]==yy];a=q(*rr[0]);b=q(*rr[-1]);line(a[0],a[1],b[0],b[1],C['muted'],2,'4 5')
            ts=[t for t in f['targets'] if t['xy'][1]==yy]
            if ts:
                end=min(ts,key=lambda t:t['xy'][0]);arrow(a[0]-s/2,a[1],*q(*end['xy']),C['red'],4)
    tilemark(q,f['actor'],f['footprint'],'我',C['teal'],s)
    if f['kind']=='form':tilemark(q,f['actor'],[2,1],'',C['gold'],s,True)
    for t in f['targets']:
        col=C['gold'] if f['kind'] in ('shield','work','brace') else C['red'] if t['label'] in ('敌','市') else C['wall']
        tilemark(q,t['xy'],[1,1],t['label'],col,s)
        if f['kind']=='pin':
            xx,yy=q(*t['xy'])
            if t['label']=='敌':circle(xx,yy,21,'none',C['gold'],3)
    if f['kind']=='pin':
        arrow(*q(4,3),*q(7,3),C['red'],3,'4 4');text(x+5*s,y+3*s-6,'仍可开火',14,C['red'])
    if f['kind']=='brace':
        a=q(*f['actor']);b=q(2,3);line(a[0]+13,a[1]+10,b[0]-13,b[1]+10,C['gold'],5)
    for m in f['moves']:
        a=q(*m['from']);b=q(*m['to']);tilemark(q,m['to'],[1,1],'',C['gold'],s,True)
        if f['kind']=='lift':
            path(f'M{a[0]} {a[1]-12} Q{(a[0]+b[0])/2} {a[1]-85} {b[0]} {b[1]-12}',C['gold'],4);arrow(b[0]-6,b[1]-29,b[0],b[1]-12,C['gold'],3)
        else:
            dx=b[0]-a[0];dy=b[1]-a[1];length=(dx*dx+dy*dy)**.5
            arrow(a[0]+dx/length*16,a[1]+dy/length*16,*b,C['gold'],4)

for group in range(5):
    n=19+group;ident='G'+str(n);lo=group*3+1;hi=lo+2
    begin(ident,f'FX{lo:02}–FX{hi:02} · 格子图逐张施工','图中均为明确例局；敌我同效，数字、足迹、阻挡和接触点由同一结果源生成。',1060)
    for r,f in enumerate(F[group*3:group*3+3]):
        yy=110+r*302;frame(34,yy,1092,283,f['id'][2:],f['title'])
        fx_grid(f,69,yy+55)
        lines(405,yy+93,f['notes'],20,step=42)
        text(405,yy+235,'→ '+{'pin':'锁步环，不画位移','lift':'真实吊载弧线','shield':'逐对象标盾，不做伤害红闪','work':'产物/修复各自独立','form':'自身形态，不是攻击','brace':'支点与持续姿态','water':'环境致死与市政损失分行'}.get(f['kind'],'命中、位移与范围分别画'),19,C['teal'],650)
    save(ident,f'FX{lo:02}-{hi:02}格子图',f'FX{lo:02}至FX{hi:02}的施工例局；坐标源为招式图施工数据.json，旧模板不再负责猜效果。','08-图形与手感施工表',f'### FX{lo:02}–FX{hi:02}',['U03','V06','F04'])

(P/'图解清单.json').write_text(json.dumps(fg['manifest'],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'figures':len(fg['manifest']),'new_figures':8}))
