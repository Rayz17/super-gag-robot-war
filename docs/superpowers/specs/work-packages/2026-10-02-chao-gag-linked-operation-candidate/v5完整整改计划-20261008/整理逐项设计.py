#!/usr/bin/env python3
"""Publish authored item decisions. Refuse incomplete coverage rather than fill generic prose."""
from pathlib import Path
from collections import Counter
from html import escape
import csv,json,re,runpy

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'game-godot/project.godot').is_file())
data=json.loads((HERE/'计划数据.json').read_text())
DETAILS=runpy.run_path(str(HERE/'逐项设计源.py'))['DETAILS']
figs=json.loads((HERE/'图解清单.json').read_text())
first_level=json.loads((HERE/'首关施工基线.json').read_text())
layer=json.loads((HERE/'人物与成长施工合同.json').read_text())
fx_fixtures={f['id']:f for f in json.loads((HERE/'招式图施工数据.json').read_text())['fixtures']}
specific=[r for r in data['coverage'] if r['group']!='章节索引']
assert {r['id'] for r in specific}==set(DETAILS), 'Missing or extra authored item'
tasks={t['id']:t for t in data['tasks']}
books=[
 ('条目01-操作界面与体验维度',['操作16项','bug13项','对照维度'],['G01','G02'],'从光标的每一步，到玩家为什么会觉得难懂、难玩。'),
 ('条目02-美术场景与语义色',['美术12项','场景资产12类','造型8条','配色3方案','语义色10项'],['G05','G06'],'材质、体块、配色、界面语义逐层处理，保留机体自己的涂装。'),
 ('条目03-动作节奏与打击反馈',['演出通用12条','SML规格35项','手感19项'],['G07','G04'],'每项要落到动作时点、物体响应、声音、操作与验证。'),
 ('条目04-十八招与错误示意',['实测招式18招','逐招定制13条','示意错误15项'],['G03','G08'],'18招、13组演出建议、15项错图按来源分别回应；重叠处明确关联。'),
 ('条目05-敌人战斗与综合建议',['敌人8项','敌招5类','Top15','Top外4项'],['G12','G13'],'敌人如何出题、如何保持承诺；综合建议哪些采纳、哪些调整。'),
 ('条目06-高度机构与空地',['空间基础9条','空间机制12条','空地20项'],['G09','G10','G11'],'从占地和结构面，到吊装、支撑、飞行、迫降与跨区。'),
 ('条目07-机体主体与系统恢复',['原设计系统20项','七台招牌重建','人物关系12项'],['G15','G08'],'把机设、人物与装备恢复成可组合的底层体系。'),
 ('条目08-十条人物指令',['精神首批8条','精神扩展2条'],['G15'],'每条明确人物边界、目标、费用、效果和不能做什么。'),
 ('条目09-卡组与成长对照',['卡组12项'],['G04'],'确定指令与随机牌组分开验证；不让抽牌成为基本动作的门槛。'),
]
bygroup={g:b[0] for b in books for g in b[1]}
assert set(bygroup)=={r['group'] for r in specific}
fields=[('analysis','问题为什么成立'),('adoption','采纳与调整'),('design','具体设计'),('player_expression','玩家怎样操作、看见后果'),('example','放进局面里怎么用'),('verification','怎样验证，哪些反例必须过')]

figures={f['id']:f for f in figs}
def figure(f):
    return f'<figure id="fig-{f["id"]}"><a href="{f["file"]}"><img src="{f["file"]}" alt="原创方案图解：{f["name"]}" loading="lazy"></a><figcaption><strong>{f["id"]} · 原创设计示意。</strong> {f["caption"]} <a href="{f["svg"]}">查看矢量图</a></figcaption></figure>'

for r in specific:
    if 'previous_summary' not in r:r['previous_summary']={k:r.get(k,'') for k in ['decision','action','acceptance']}
    r['display_title']={'G10':'敌方阶段：固定分段节奏、暂停与快进','ASSET-07':'现代居民楼 shelter'}.get(r['id'],r['title'])
    detail=DETAILS[r['id']]
    r['detailed_design']=detail
    r['action']=detail['design']
    r['acceptance']=detail['verification']
    r['decision']=detail['adoption']
    r['detail_page']=bygroup[r['group']]+'.html#'+r['id']
    r['design_figures']=next(b[2] for b in books if b[0]==bygroup[r['group']])
    if r['id'] in fx_fixtures:
        r['first_level_reference']='08-图形与手感施工表.html#'+r['id']
        r['design_figures']=r['design_figures']+['G'+str(19+(int(r['id'][2:])-1)//3)]
    elif re.fullmatch(r'MV\d\d',r['id']):
        r['first_level_reference']='08-图形与手感施工表.html#'+r['id']
    elif r['group'] in ['操作16项','手感19项','演出通用12条','SML规格35项','逐招定制13条']:
        r['first_level_reference']='08-图形与手感施工表.html#section-1'
    else:
        r['first_level_reference']='07-首关施工规格.html#section-1'
    r['implementation_targets']=list(dict.fromkeys(p for id in r['work_packages'] for p in tasks[id]['code_targets'].split(';')))
    r['implementation_dependencies']=sorted({dep for id in r['work_packages'] for dep in tasks[id]['dependencies']})
    r['implementation_stage']=min(tasks[id]['stage'] for id in r['work_packages'])
    r['delivery']=layer['delivery_assignments'][r['id']]
    r['scope']=r['delivery']['scope']
    r['spec_ref']=r['delivery']['spec_ref']
    r['first_level_reference']=r['spec_ref'] # compatibility alias, no longer a generic footer
    if r['id'].startswith('SPIRIT-'):r['design_figures']=['G24','G25']
    if r['id'].startswith('SIG-'):r['design_figures']=['G26']
    if r['id'].startswith('CARD-'):r['design_figures']=['G28']

source_lines=(ROOT/data['source']).read_text().splitlines()
headings=[(r,len(source_lines[r['source_line']-1].split(' ')[0])) for r in data['coverage'] if r['group']=='章节索引']
for n,(r,level) in enumerate(headings):
    end=next((other['source_line'] for other,lvl in headings[n+1:] if lvl<=level),len(source_lines)+1)
    children=[x['id'] for x in specific if r['source_line']<=x['source_line']<end]
    r['detail_items']=children
    r['heading_level']=level
    r['index_note']='本章节的具体建议分见 '+str(len(children))+' 条设计。' if children else '来源、方法或章节说明；保留原文索引，不伪造独立开发项。'

man=[]
for slug,groups,figure_ids,desc in books:
    selected=[r for g in groups for r in specific if r['group']==g]
    md=[f'# {slug.split("-",1)[1]}：逐项分析与实施设计',desc,
        f'本册 {len(selected)} 条源记录。编号沿用原报告/覆盖表；同一问题跨章节出现时保留对应，不把它算成重复开发。**以下是设计规格，不是游戏完成记录。**',
        '[回到总方案](index.html) · [首关确定规格](07-首关施工规格.html) · [帧表与15项图形](08-图形与手感施工表.html) · [按编号搜索全部条目](覆盖核对.html)',
        '> 10月9日第二轮补强：每条已注明首关依赖／系统恢复专关／全量对照、具体规格与测试局。数字、帧数、人物费用在正文已对齐；证据仍未提供，未把文档覆盖称作游戏通过。',
        '<details class="item-toc"><summary>本册条目目录</summary>\n\n'+ '\n'.join(f'- [{r["id"]} · {r.get("display_title",r["title"])}](#{r["id"]})' for r in selected)+'\n\n</details>']
    if slug.startswith('条目09'):
        md.extend(['## 卷首：P04何时开，怎样裁决',
          '**配置A的角色卡恢复不依赖本实验。** P02/P03/P05实跑通过后开启GW-DECK-P04-v1：六机stock、07三面局面，种子4101—4106，固定16实例，比较A确定指令、A_plus公开修饰池、B随机手牌。12人按交叉顺序测试，各做2种子×3模式、每局3轮。',
          '| 测量 | 采纳门槛 |\n|---|---|\n| 基础能力/预测一致 | 因抽不到牌而无法基本行动0次；预演不一致0次 |\n| 操作 | 额外点击均值≤4、p90≤6；时间≤A的1.20倍 |\n| 牌与决策 | 无效牌≤20%；有效选择较A增加≥20% |\n| 随机价值 | 种子达成率差≤15个百分点；至少8/12更愿重玩B而非A_plus |',
          '全部门槛通过才让B进入下一压力关；只有A_plus受益则保留确定构筑；否则搁置随机性。没有实验实测值，不写“卡组已恢复”。[完整牌表、分母和顺序](10-专关与成长对照规格.html#section-2) · [成长6/14阈值与三关归因](10-专关与成长对照规格.html#section-5)。成长版本GW-GROWTH-P04-v1不进首关。下列12条都有固定手顺及失败样子。'])
    if slug.startswith('条目08'):
        md.extend(['## 卷首：同一能力、同一次数、真实出席',
          '本册十条已替换方向句：目标、费用、phase、结果字段、失败原因和验收局均落实。首关只启用SPIRIT-1与免费SPIRIT-4；其余按P02/P05专关。人物头像/通讯双页签/目标旁入口共用ability_instance_id，机体招式栏不再复制精神。[出席与卡面字段](09-人物指令与机魂施工规格.html#section-1)。'])
    if slug.startswith('条目07'):
        md.extend(['## 卷首：人物与招牌以规则验收',
          '六机招牌已定最小规则、18招/FX对应和R03后续完整合同；机魂的四态、替案Command与安全底线见[意愿施工表](09-人物指令与机魂施工规格.html#section-4)。预算/歌翼的主体资料不足不填假人格。六机盲辨须10人60答，身份≥48/60、每机≥7/10，因果≥54/60；没有实测前全部待实施。'])
    if slug.startswith('条目02'):
        md.extend(['## 卷首：造型怎样让三道题被读懂',
          'A(4,3)瓷柱电柜连接公共母线，(6,0/1)深槽有真实侧壁；B低桥与岸轨错位、锁销缩回，缺电/缺对齐/损坏各有不同轮廓；C(6,4)窄高隔离柜的专线连接A炮，轨道由C向东去B。选中才显示对应线、箭头与损失，环境颜色不代替信息色。[精确高度、像素指标和五态首玩验证](07-首关施工规格.html#readability)。'])
    for id in figure_ids:md.append(figure(figures[id]))
    for g in groups:
        md.append(f'## {g}')
        for r in selected:
            if r['group']!=g:continue
            v=r['detailed_design']
            md += [f'<section class="design-item" id="{r["id"]}">',f'### {r["id"]} · {r.get("display_title",r["title"])}',
                   f'<p class="source-note">来源：{escape(r["source_ref"])} · 原稿第 {r["source_line"]} 行。工作包：'+ ' / '.join(r['work_packages'])+'</p>',
                   f'> **处理决定：** {v["adoption"]}',f'**分析。** {v["analysis"]}',f'**具体设计。** {v["design"]}',f'**操作与画面。** {v["player_expression"]}',
                   f'<div class="design-example"><strong>局面例子</strong><p>{escape(v["example"])}</p></div>',f'**验证与反例。** {v["verification"]}']
            if r.get('display_title',r['title'])!=r['title']:md.append('<details><summary>保留的原报告题名（非本版施工值）</summary>'+escape(r['title'])+'</details>')
            md.append('**交付范围：** '+r['scope']+'。**具体规格：** [打开对应合同]('+r['spec_ref']+')。**验证局：** '+ '、'.join(r['delivery']['cases'])+'。\n\n'+r['delivery']['minimum']+'；'+r['delivery']['remainder']+'。实机配置、录屏与反例证据：**未提供**。')
            if r['id'] in fx_fixtures:
                fx=fx_fixtures[r['id']]
                md.append('<div class="design-example"><strong>这张图的具体改法</strong><p>'+escape('；'.join(fx['notes']))+'</p><p>施放者锚点 '+escape(str(fx['actor']))+'，脚印 '+escape(str(fx['footprint']))+'。<a href="08-图形与手感施工表.html#'+r['id']+'">查看命中格、落点与施工图</a></p></div>')
            shared=[id for id in v['shared_with'] if id!=r['id']]
            if shared:
                md.append('**同一问题的相关条目：** '+ ' · '.join(f'[{id}]({bygroup[next(x["group"] for x in specific if x["id"]==id)]}.html#{id})' for id in shared)+'。各条保留原报告位置，共用此设计，不重复开发。')
            wps='\n'.join(f'- [{id} · {tasks[id]["title"]}](05-施工与验收.html#{id})：{tasks[id]["owner"]}；依赖 '+('、'.join(tasks[id]['dependencies']) or '无前置工作包') for id in r['work_packages'])
            code='\n'.join('- '+(f'[{p}]('+str(ROOT/p)+')' if p.startswith('game-godot/') else escape(p)) for p in r['implementation_targets'])
            md.append('<details class="implementation"><summary>准备怎么施工：工作包、依赖与代码入口</summary>\n\n'+wps+'\n\n这些是拟修改入口，不表示已经完成修改。共同的命令、事件和呈现责任见[实现设计册](06-从方案到可实现设计.html)。\n\n'+code+'\n\n</details>')
            if r.get('source_status') or r.get('source_acceptance'):
                md.append('<details><summary>报告原观察与原验收建议</summary>\n\n'+escape(r.get('source_status',''))+'\n\n'+escape(r.get('source_acceptance',''))+'\n\n这是原报告的观察/建议；本轮采用的规格和验证方法以上文为准。\n\n</details>')
            md.append('</section>')
    (HERE/(slug+'.md')).write_text('\n\n'.join(md)+'\n')
    man.append({'slug':slug,'name':slug.split('-',1)[1],'count':len(selected),'groups':groups,'figures':figure_ids,'description':desc})

data['detail_summary']={'specific_items':len(specific),'authored_designs':len({json.dumps(v,ensure_ascii=False) for v in DETAILS.values()}),'design_fields':[k for k,_ in fields],'detail_books':len(books),'original_figures':len(figs),'first_level':first_level['version'],'scope_counts':layer['scope_counts'],'status':'首关与人物/机魂/招牌/实验合同已补齐；游戏待实施，证据未提供'}
(HERE/'计划数据.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(HERE/'逐项分册清单.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n')
with (HERE/'逐项设计.tsv').open('w') as f:
    columns=['id','group','title','source_ref','source_line']+[k for k,_ in fields]+['work_packages','detail_page','scope','spec_ref']
    writer=csv.DictWriter(f,fieldnames=columns,delimiter='\t');writer.writeheader()
    for r in specific:
        writer.writerow({**{k:r[k] for k in columns if k in r},**{k:r['detailed_design'][k] for k,_ in fields},'work_packages':' / '.join(r['work_packages'])})
with (HERE/'报告逐项覆盖.tsv').open('w') as f:
    cols=['id','group','title','source_line','source_ref','decision','action','acceptance','work_packages','scope','spec_ref','status']
    w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader()
    for r in data['coverage']:w.writerow({k:' / '.join(r[k]) if isinstance(r.get(k),list) else r.get(k,'') for k in cols})
with (HERE/'整改工作包.tsv').open('w') as f:
    cols=['id','title','stage','dependencies','owner','deliverable','acceptance','code_targets','status','conclusion_tiers','evidence','counterexample']
    w=csv.DictWriter(f,fieldnames=cols,delimiter='\t');w.writeheader()
    for t in data['tasks']:
        g=t['delivery_gates'];w.writerow({**{k:' / '.join(t[k]) if isinstance(t.get(k),list) else t.get(k,'') for k in cols if k in t},'conclusion_tiers':' / '.join(g['tiers']),'evidence':'未提供；configuration/recording/counterexample=null','counterexample':g['counterexample']})

# Put new diagrams at the point of discussion. Re-running replaces generated inserts only.
for doc in ['00-总方案','01-核心机制与操作','02-美术与逐招演出','03-机体与人物体系','04-战场与立体机制','05-施工与验收','06-从方案到可实现设计','07-首关施工规格','08-图形与手感施工表','09-人物指令与机魂施工规格','10-专关与成长对照规格']:
    file=HERE/(doc+'.md');s=file.read_text()
    s=re.sub(r'\n?<!-- PLAN_FIGURE_START -->[\s\S]*?<!-- PLAN_FIGURE_END -->\n?','\n',s)
    s=re.sub(r'\n?<!-- DETAIL_BOOKS_START -->[\s\S]*?<!-- DETAIL_BOOKS_END -->\n?','\n',s)
    for f in [x for x in figs if x['doc']==doc]:
        block='\n\n<!-- PLAN_FIGURE_START -->\n'+figure(f)+'\n<!-- PLAN_FIGURE_END -->\n'
        if f['anchor']=='opening':
            pos=s.index('\n\n');s=s[:pos]+block+s[pos:]
        else:
            match=re.search(r'^'+re.escape(f['anchor'])+r'.*$',s,re.M)
            assert match, (doc,f['anchor'])
            s=s[:match.end()]+block+s[match.end():]
    related={'00':range(9),'01':[0,4],'02':[1,2,3],'03':[6,7,8],'04':[4,5],'05':range(9),'06':range(9),'07':[],'08':[],'09':[],'10':[]}[doc[:2]]
    intro='\n\n<!-- DETAIL_BOOKS_START -->\n<div class="detail-reading"><strong>逐项设计入口</strong>\n\n'+ '\n'.join(f'- [{man[i]["name"]}：{man[i]["count"]}条]({man[i]["slug"]}.html)' for i in related)+'\n\n每条包含原因、采纳决定、具体规格、操作/画面、局面例子、验证反例及施工入口。\n\n</div>\n<!-- DETAIL_BOOKS_END -->\n'
    first_h2=re.search(r'^## ',s,re.M); pos=first_h2.start() if first_h2 else len(s)
    if related:s=s[:pos]+intro+s[pos:]
    # Source evidence should be visible; only item directory / code details remain collapsible.
    if doc=='02-美术与逐招演出':s=s.replace('<details>','<details open>')
    file.write_text(re.sub(r'\n{4,}','\n\n\n',s))

index=['# 原创图解：按要解释的问题查图','这些图是本方案新绘的规则、布局、流程和分镜示意。它们不充当实机截图，也不充当最终场景美术稿。原报告截图在相关正文里保留为问题证据。','[回到总方案](index.html) · [逐项设计搜索](覆盖核对.html)']
for f in figs:
    index += [f'## {f["id"]} · {f["name"]}',figure(f), '对应工作包：'+ ' · '.join(f'[{id}](05-施工与验收.html#{id})' for id in f['work'])]
(HERE/'图解总览.md').write_text('\n\n'.join(index)+'\n')
print(json.dumps(data['detail_summary'],ensure_ascii=False))
