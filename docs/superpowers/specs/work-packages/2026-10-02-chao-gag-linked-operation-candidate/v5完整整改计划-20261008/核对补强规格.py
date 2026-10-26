#!/usr/bin/env python3
"""Validate design contracts and reference vectors. Does NOT run the game or browser."""
from pathlib import Path
from collections import Counter
import copy, hashlib, itertools, json, re, runpy

P=Path(__file__).resolve().parent
L=json.loads((P/'人物与成长施工合同.json').read_text())
D=json.loads((P/'计划数据.json').read_text())
R=json.loads((P/'首关施工基线.json').read_text())
S=runpy.run_path(str(P/'补强设计源.py'))
errors=[]; count=0
def need(condition,message):
    global count
    count+=1
    if not condition:errors.append(message)

need(hashlib.sha256((P/L['review_source']['file']).read_bytes()).hexdigest()==L['review_source']['sha256'],'review source digest')
need(L['status']=='design_contract_only_not_implemented','design must not claim implementation')
need(D['second_review']['runtime_evidence_count']==0,'runtime evidence must stay empty')
need({s['id'] for s in L['spirits']}=={f'SPIRIT-{i}' for i in range(1,11)},'ten spirit IDs')
fixtures={f['id']:f for f in L['fixtures']}
spirits={s['id']:s for s in L['spirits']}
for s in L['spirits']:
    for k in ['owner','target_filter','phase','effect','result_fields','failure','case','consume']:
        need(bool(s[k]),s['id']+' missing '+k)
    need(s['case'] in fixtures,s['id']+' no concrete case')
    need(s['uses']==(0 if s['id']=='SPIRIT-4' else 1),s['id']+' unresolved use count')
    need(all(s['cost'][k]==0 for k in ['main','move','sp','energy']),s['id']+' UI reintroduced shared SP/action cost')
for a in L['attendance']:
    owners=Counter(spirits[x]['owner'] for x in a['abilities'] if spirits[x]['uses'])
    # 豪司 and his partnered consent ability refer to the same attendance slot.
    normalized=Counter()
    for owner,n in owners.items():normalized['豪司' if owner.startswith('豪司') else owner]+=n
    need(all(n<=2 for n in normalized.values()),a['id']+' exceeds 2 abilities per person')
    for owner in normalized:
        need(any(p.startswith(owner) for p in a['people']),a['id']+' absent ability owner '+owner)
need(L['attendance'][0]['abilities']==R['people_layer']['first_abilities']==['SPIRIT-1','SPIRIT-4'],'R1 ability subset changed')
need(not R['people_layer']['deck_or_growth_enabled'] and not L['growth']['first_level_enabled'],'experimental economy leaked into R1')
need(len(L['consents'])==7 and len(L['signatures'])==7,'identity/signature inventory')
for c in L['consents']:
    need(all(c[k] for k in ['identity','trigger','hard','soft','alternative','spirit','case']),c['id']+' incomplete consent card')
need('豪司＋社勇王主体AI' in L['consents'][0]['identity'],'invented Brave subject')
for c in L['consents'][-2:]:need('not_applicable' in c['soft'],c['id']+' invented personality')
known_moves={f'MV{i:02}' for i in range(1,19)};known_fx={f'FX{i:02}' for i in range(1,16)}
for s in L['signatures']:
    need(set(s['moves'])<=known_moves and set(s['fx'])<=known_fx,s['id']+' unknown move/FX')
need(set(m for s in L['signatures'][:6] for m in s['moves'])==known_moves,'six signatures fail to cover 18 moves')

# Independently recompute the new social-consent vignette using the declared R1 board.
objects={o['id']:o for o in R['boards']['A']['objects']}
def cells(o):
    x,y=o['xy'];w,h=o['footprint']
    return {(x+i,y+j) for i in range(w) for j in range(h)}
actor=(5,3); alternative=(5,2);target=tuple(objects['biter']['xy'])
fan={(7,2),(7,3),(7,4)}
need(tuple(objects['shelter_n']['xy']) in fan and objects['shelter_n']['hp']==3,'soul fixture does not endanger R1 shelter')
need(sum(abs(x-y) for x,y in zip(actor,alternative))==1,'counterproposal move cost')
need(sum(abs(x-y) for x,y in zip(alternative,target))==1,'counterproposal punch not adjacent')
occupied=set().union(*(cells(o) for o in objects.values() if o['id']!='brave'))
need(alternative not in occupied,'counterproposal lands in occupied cell')
need(objects['biter']['hp']-2==2,'counterproposal damage arithmetic')
need(R['costs']['lift']['max_mass']==3 and R['costs']['lift']['range']==2 and R['costs']['lift']['drop_distance_from_load']==3,'lift source disagreement')
need(R['costs']['beam']['damage']==2 and R['costs']['beam']['mark_after_hit']['ignore_aura_reduction']==1,'beam source disagreement')
need(R['costs']['pin']['max_mass']==3 and R['costs']['pin']['disables']=='active_move_only','pin must not silently disarm')

# Reference RNG test vectors are for future implementation, not evidence of Godot parity.
def next32(state):
    if not state:raise ValueError('zero seed')
    state ^= (state<<13)&0xffffffff
    state ^= state>>17
    state ^= (state<<5)&0xffffffff
    return state&0xffffffff
def shuffle(seed,ids):
    a=list(ids);state=seed
    for i in range(len(a)-1,0,-1):
        n=i+1; limit=(1<<32)-((1<<32)%n)
        while True:
            state=next32(state)
            if state<limit:break
        j=state%n;a[i],a[j]=a[j],a[i]
    return a,state
deck=L['deck'];ids=[c['id'] for c in deck]
need(len(ids)==len(set(ids))==16,'deck size/instances')
need(Counter(c['source'] for c in deck)==Counter({x:2 for x in ['brave','king','engineer','cargo','police','leiling','纪存','白鸢']}),'deck source count')
need({c['id'] for c in deck if c['exhaust']}=={'E1','W2'},'exhaust cards changed')
need({c['id'] for c in L['card_cases']}=={f'CARD-{i:02}' for i in range(1,13)},'twelve independent card cases')
for c in L['card_cases']:need(bool(c['steps']) and bool(c['fail']),c['id']+' missing steps/failure')
for v in L['experiment']['opening_vectors']:
    a,state=shuffle(v['seed'],ids)
    need(a[:3]==v['hand'] and state==v['rng_after_shuffle'],'seed vector '+str(v['seed']))
    need(sorted(a)==sorted(ids),'shuffle created/deleted card')
    frozen={'draw':a[3:],'hand':a[:3],'rng':state,'discard':[],'exhaust':[]}
    before=copy.deepcopy(frozen)
    for _ in range(100):shuffle(frozen['rng'],copy.deepcopy(frozen['draw']))
    need(frozen==before,'reference preview mutates real deck')
try:shuffle(0,ids);need(False,'zero seed should fail')
except ValueError:pass
orders=list(itertools.permutations(['A','A_plus','B']))
assignments=[]
for p in range(12):
    seed_indices=[p%6,(p+1)%6]
    assignments.append({'participant':p+1,'group':'new' if p<6 else 'experienced','seeds':[4101+i for i in seed_indices],'orders':[list(orders[p%6]),list(reversed(orders[p%6]))]})
need(set(Counter(s for a in assignments for s in a['seeds']).values())=={4},'not exactly four participants per seed')
need(set(Counter(tuple(a['orders'][0]) for a in assignments).values())=={2},'mode order not balanced')
need(L['experiment']['stage_goal']['minimum_head_index']==13 and R['train_head_index']+3*R['train_speed']==13,'three-round goal timing')
need(L['growth']['xp_thresholds']==[6,14],'growth thresholds')
xp=0;totals=[]
for m in L['growth']['three_missions']:xp+=m['xp'];totals.append(xp)
need(totals==[4,10,14],'growth curve')
need(L['growth']['starting_credits']-L['growth']['shop']['upgrade_card']-L['growth']['shop']['remove_card']==1,'independent shop arithmetic')
need(L['growth']['starting_credits']+4+6+3==17,'three-mission no-spend balance')

# Scope is a delivery boundary; no assignment is a runtime pass.
specific={r['id']:r for r in D['coverage'] if r['group']!='章节索引'}
need(set(specific)==set(L['delivery_assignments']),'scope omitted a source record')
need(Counter(a['scope'] for a in L['delivery_assignments'].values())==Counter(L['scope_counts']),'scope counts')
for id,a in L['delivery_assignments'].items():
    need(a['scope'] in S['SCOPES'] and a['status']=='待实施',id+' invalid scope/state')
    need(all(v is None for v in a['evidence'].values()),id+' has invented runtime evidence')
    need(specific[id]['scope']==a['scope'] and specific[id]['spec_ref']==a['spec_ref'],id+' stale publication')
for c in L['card_cases']:need(L['delivery_assignments'][c['id']]['scope']=='全量／对照',c['id']+' became first-level prerequisite')
nodes={n['id']:n for n in L['first_dependency_nodes']};done=set()
for n in L['first_dependency_nodes']:
    need(set(n['requires'])<=done,n['id']+' invalid/cyclic ordering');done.add(n['id'])
need('P04' not in {i for n in nodes.values() for i in n['items']},'P04 blocks R1')
need(set(L['task_gates'])==set(S['TASK_COUNTEREXAMPLES'])=={t['id'] for t in D['tasks']},'52 task counterexamples')
for t in D['tasks']:
    g=L['task_gates'][t['id']]
    need(g['counterexample']!=t['acceptance'] and len(g['counterexample'])>=22,t['id']+' counterexample merely relabeled acceptance')
    need(t['delivery_gates']==g,t['id']+' stale task gates')
    if g['first_slice']!='不进入首关施工子集':need('首关依赖' in g['tiers'],t['id']+' missing first-slice conclusion tier')
    need(all(v is None for v in g['evidence'].values()),t['id']+' invented task evidence')
need(set(x['id'] for x in L['readability'])=={'READ-A','READ-B','READ-C'},'three visual questions')
for r in L['readability']:need(all(r[k] for k in ['cells','shape','height','overlay','test']),r['id']+' only an asset inventory')
page=(P/'覆盖核对.html').read_text()
need('value="首关依赖" selected' in page,'coverage default not first level')
need("scope.value!=='all'&&r.scope!==scope.value" in page and 'selectExactId()' in page,'scope filter or ID handoff missing')
need('选择到范围出现 p95≤100ms' not in (P/'01-核心机制与操作.md').read_text(),'old selection latency still competes')
detail=runpy.run_path(str(P/'逐项设计源.py'))['DETAILS']
need('载荷≤4' not in detail['MV08']['design'],'old lift limit still in authored text')
need('其他友机' in detail['MV16']['design'],'mark lacks source exclusion')
report={'status':'pass' if not errors else 'fail','scope':'paper contracts and independent reference arithmetic; no Godot run or browser validation','checks':count,'spirits':10,'vignettes':len(fixtures),'deck_vectors':len(L['experiment']['opening_vectors']),'participant_assignment':assignments,'delivery_scopes':L['scope_counts'],'runtime_evidence':0,'errors':errors}
(P/'补强规格核对结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='participant_assignment'},ensure_ascii=False))
raise SystemExit(1 if errors else 0)
