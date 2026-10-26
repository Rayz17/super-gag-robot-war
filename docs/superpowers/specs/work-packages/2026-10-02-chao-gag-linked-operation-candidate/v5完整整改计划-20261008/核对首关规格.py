#!/usr/bin/env python3
"""Paper-spec consistency check. Does not invoke Godot or prove game behavior."""
from pathlib import Path
from collections import deque
from copy import deepcopy
from itertools import permutations
import hashlib,json,math

P=Path(__file__).resolve().parent
D=json.loads((P/'首关施工基线.json').read_text())
F=json.loads((P/'招式图施工数据.json').read_text())['fixtures']
checks=[];errors=[]
def check(ok,name,details=None):
    checks.append({'name':name,'pass':bool(ok),'details':details})
    if not ok:errors.append(name)
def cells(xy,foot=(1,1)):
    return {(xy[0]+x,xy[1]+y) for x in range(foot[0]) for y in range(foot[1])}
def allobjects(d):return {o['id']:(bid,o) for bid,b in d['boards'].items() for o in b['objects']}
def occupied(d,bid,exclude=None):
    return set().union(set(),*(cells(o['xy'],o['footprint']) for o in d['boards'][bid]['objects'] if o['id']!=exclude and o.get('blocking',True) and o['hp']>0))
def route(d,id,to):
    bid,u=allobjects(d)[id];b=d['boards'][bid];size=b['size'];blocks=occupied(d,bid,id);water={tuple(x) for x in b['water']}
    def fit(pos,end=False):
        cs=cells(pos,u['footprint'])
        if any(x<0 or y<0 or x>=size[0] or y>=size[1] for x,y in cs):return False
        if u.get('flying') and not end:return True
        return not cs&blocks and (u.get('flying') or not cs&water)
    end=tuple(to);start=tuple(u['xy'])
    if not fit(end,True):return None
    todo=deque([[start]]);seen={start}
    while todo:
        p=todo.popleft()
        if p[-1]==end:return p
        x,y=p[-1]
        for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]:
            v=(x+dx,y+dy)
            if v not in seen and fit(v):seen.add(v);todo.append(p+[v])
    return None
def move(d,id,to,cost=None):
    r=route(d,id,to);u=allobjects(d)[id][1]
    check(r is not None,id+' route '+str(to),r)
    if r is None:return
    n=len(r)-1;check(n<=u['move'],id+' movement budget',{'required':n,'remaining':u['move']})
    if cost is not None:check(n==cost,id+' stated cost '+str(to),n)
    u['xy']=list(to);u['move']-=n
def act(d,id,name):
    u=allobjects(d)[id][1];check(u['main']==1,id+' main action '+name);u['main']=0
def adjacency(d,a,b):
    aa=allobjects(d)[a][1];bb=allobjects(d)[b][1]
    return min(abs(x-u)+abs(y-v) for x,y in cells(aa['xy'],aa['footprint']) for u,v in cells(bb['xy'],bb['footprint']))

check(hashlib.sha256((P/'对Astra-v5整改计划的批评与建议.html').read_bytes()).hexdigest()==D['critic_source_sha256'],'critique source unchanged')
for bid,b in D['boards'].items():
    taken=set()
    for o in b['objects']:
        cc=cells(o['xy'],o['footprint']);check(all(0<=x<b['size'][0] and 0<=y<b['size'][1] for x,y in cc),bid+'/'+o['id']+' within map')
        if o.get('blocking',True):check(not cc&taken,bid+'/'+o['id']+' no initial overlap');taken|=cc
    for p in D['ports']+D['backups']:
        if p['board']==bid:check(not cells(p['xy'],[2,2])&taken,bid+' full arrival footprint '+str(p['xy']))
    for w in D['reinforcements']:
        if w['board']==bid:check(tuple(w['xy']) not in taken,bid+' announced spawn initially empty')

s=deepcopy(D)
move(s,'brave',[3,3],1);check(adjacency(s,'brave','power')==1,'power accessible in R1');act(s,'brave','power')
move(s,'police',[5,4],1);check(adjacency(s,'police','feeder')==1,'feeder accessible in R1');act(s,'police','cut feeder')
move(s,'king',[5,3],5);check(adjacency(s,'king','biter')==1,'four-cell king reaches biter');act(s,'king','drill')
biter=allobjects(s)['biter'][1];biter['hp']-=D['costs']['drill']['damage'];check(biter['hp']==1,'biter survives impact before water');check((6,1) in map(tuple,s['boards']['A']['water']),'drill first push enters water');biter['hp']=0
move(s,'engineer',[3,4],1);check(adjacency(s,'engineer','dismantler')==1,'jack touches worker');act(s,'engineer','jack')
worker=allobjects(s)['dismantler'][1];check(D['costs']['jack']['force']>=worker['mass'],'jack sufficient force');worker['xy']=[3,2]
check(adjacency(s,'dismantler','bridge')>1,'pushed worker loses contact')
move(s,'engineer',[2,3],2);check(allobjects(s)['engineer'][1]['xy']!=[2,4],'engineer vacates frozen larva target')
move(s,'cargo',[3,4],3);check(adjacency(s,'cargo','bridge')==1,'cargo reaches brace after worker vacates');act(s,'cargo','brace')
move(s,'leiling',[4,5],2);act(s,'leiling','missile')
area={(4,3),(3,3),(5,3),(4,2),(4,4)}
affected=[]
for o in s['boards']['C']['objects']:
    if cells(o['xy'],o['footprint'])&area:
        affected.append(o['id']);o['hp']=max(0,o['hp']-2)
check(set(affected)=={'train','crate','acid'},'missile really hits train, crate and acid',affected)
objects=allobjects(s);actual={'city_hp':7,'bridge_hp':objects['bridge'][1]['hp'],'train_hp':objects['train'][1]['hp'],'municipal_loss':int(worker['hp']==0),'head_index':D['train_head_index']+D['train_speed'],'head':D['train_path'][D['train_head_index']+D['train_speed']]}
check(actual==D['opening_expected'],'stated R1 six-action receipt',actual)

# Validate the preserved-train alternative under a different deployment.
a=deepcopy(D);aa=allobjects(a);cargo=deepcopy(aa['cargo'][1]);police=deepcopy(aa['police'][1]);cargo['xy']=[5,5];police['xy']=[2,6]
a['boards']['B']['objects']=[police if x['id']=='cargo' else x for x in a['boards']['B']['objects']]
a['boards']['C']['objects']=[cargo if x['id']=='police' else x for x in a['boards']['C']['objects']]
move(a,'brave',[3,3],1);act(a,'brave','power');move(a,'king',[5,4],4);check(adjacency(a,'king','gun')==1,'alternative king touches gun');act(a,'king','drill gun')
gun=allobjects(a)['gun'][1];gun['hp']-=3
check(all((x,4) not in occupied(a,'A','gun') for x in [8,9]),'gun two-cell displacement clear');gun['xy']=[9,4]
move(a,'engineer',[3,4],1);check(not allobjects(a)['bridge'][1]['aligned'] and 'repair_tool' in allobjects(a)['engineer'][1]['capabilities'],'full-HP realignment is qualified, not an invalid heal');act(a,'engineer','repair/align');allobjects(a)['engineer'][1]['spares']-=1
move(a,'leiling',[4,6],3);act(a,'leiling','beam crate');allobjects(a)['crate'][1]['hp']=0
check(not occupied(a,'C','leiling')&{(4,5),(4,4)},'beam reaches crate before any blocking body')
move(a,'cargo',[4,3],3);check(adjacency(a,'cargo','train')==1,'alternative cargo can shield train');act(a,'cargo','shield train')
check(gun['xy']!=gun['setup_cell'],'alternative gun loses setup')
alternative={'city_hp':7-1,'bridge_hp':4-3,'train_hp':6-max(0,2-2),'head_index':5}
check(alternative=={'city_hp':6,'bridge_hp':1,'train_hp':6,'head_index':5},'preserve train deployment receipt',alternative)

# Loss conversion is intentionally separate from raw damage.
bridge=4;city=7
for damage in [3,2]:
    was=bridge;bridge=max(0,bridge-damage)
    if was>0 and bridge==0:city-=2
city-=1
no_action={'city_hp':city,'bridge_hp':bridge,'train_hp':6-2,'head_index':1}
check(no_action==D['no_action_round1_expected'],'no-action first round loss mapping',no_action)
check(len(D['train_path'])==20 and len({tuple(x) for x in D['train_path']})==20,'20 distinct rail nodes')
distance=len(D['train_path'])-1-D['train_head_index'];rounds=math.ceil(distance/D['train_speed'])
check(distance==18 and rounds==5 and rounds+1==D['deadline_round'],'train travel and one-round delay budget',{'distance':distance,'rounds':rounds})
check(D['phase_order'].index('environment')<D['phase_order'].index('arrival')<D['phase_order'].index('transport'),'collapse before arrival before transport')

# Design reference for proposal ordering; not a replacement for engine integration tests.
def claims(proposals,static):
    claimed=set(static);result={}
    for p in sorted(proposals,key=lambda p:(-p['force'],p['source_order'],p['target_order'])):
        footprint=cells(p['to'],p.get('foot',[1,1]));ok=not footprint&claimed
        result[p['id']]=('land' if ok else 'stay')
        if ok:claimed|=footprint
    return result
ps=[dict(id='a',to=[2,2],force=4,source_order=2,target_order=4),dict(id='b',to=[2,2],force=3,source_order=1,target_order=3)]
check(all(claims(list(pp),set())=={'a':'land','b':'stay'} for pp in permutations(ps)),'force wins independent of input array order')
ps[1]['force']=4
check(all(claims(list(pp),set())=={'b':'land','a':'stay'} for pp in permutations(ps)),'equal-force fixed source order')
check(claims([dict(id='large',to=[1,1],foot=[2,2],force=4,source_order=1,target_order=1)],{(2,2)})=={'large':'stay'},'four-cell claim atomic')
def arrival(primary,backup,blocked,broken):
    for name,xy in [('primary',primary),('backup',backup)]:
        if xy is not None and not cells(xy,[2,2])&(blocked|broken):return name
    return 'wait'
check(arrival([1,1],[6,1],set(),{(2,2)})=='backup','collapsed reserved footprint chooses valid backup')
check(arrival([1,1],[6,1],{(1,1),(6,1)},set())=='wait','physical occupancy beats reservation; unit waits')

fx={f['id']:f for f in F}
for f in F:
    allcells=cells(f['actor'],f['footprint'])|{tuple(t['xy']) for t in f['targets']}|{tuple(t) for t in f['area']+f['range']}
    for m in f['moves']:allcells|={tuple(m['from']),tuple(m['to'])}
    check(all(0<=x<f['board'][0] and 0<=y<f['board'][1] for x,y in allcells),f['id']+' geometry within fixture')
check(len(fx['FX03']['range'])==len(fx['FX14']['range'])==12,'two six-cell cannon ranges')
check(set(map(tuple,fx['FX02']['area']))=={(3,2),(3,3),(3,4)},'three-cell finisher')
check(len(fx['FX06']['range'])==6,'beam six-cell range')
check(len(fx['FX12']['area'])==5 and not fx['FX12']['moves'],'missile five cells without displacement')
check(not fx['FX08']['moves'],'pin has no displacement')
for id,n in [('FX01',2),('FX09',3),('FX15',1)]:
    m=fx[id]['moves'][0];check(sum(abs(a-b) for a,b in zip(m['from'],m['to']))==n,id+' displacement/lift distance '+str(n))
check(len(D['timing_60hz'])==18,'eighteen timing profiles')
for t in D['timing_60hz']:check(all(0<=c<=t['result']<t['input'] for c in t['contact']) and t['result']<t['input'],t['mv']+' contact-result-input order')

report={'status':'pass' if not errors else 'fail','scope':'paper specification only; no Godot simulation or player acceptance','version':D['version'],'count':len(checks),'checks':checks,'errors':errors,'limits':['No claim that the new scene, rules or animations are implemented.','Round-one geometry and arithmetic are checked; this is not an exhaustive solution or full six-round AI balance search.','Enemy targeting, replay, input latency and audio/animation tolerances require later engine tests and real play.']}
(P/'首关规格核对结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','scope','version','count','errors']},ensure_ascii=False))
raise SystemExit(bool(errors))
