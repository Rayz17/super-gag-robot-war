#!/usr/bin/env python3
"""Check source coverage, dependency topology and local document links.

This validates the plan package, not the game or the quality of the design.
"""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import csv
import hashlib
import json
import re
import runpy
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'game-godot/project.godot').is_file())
data=json.loads((HERE/'计划数据.json').read_text())
errors=[]
def require(ok,msg):
    if not ok: errors.append(msg)
source=ROOT/data['source']
source_lines=source.read_text().splitlines()
for name,digest in data['source_hashes'].items():
    p=source.parent/name
    require(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,'source changed: '+name)

tasks={t['id']:t for t in data['tasks']}
require(len(tasks)==len(data['tasks'])==52,'work package IDs/count')
visiting=set();visited=set()
def visit(id):
    if id in visiting:errors.append('dependency cycle: '+id);return
    if id in visited:return
    visiting.add(id)
    for dep in tasks[id]['dependencies']:
        require(dep in tasks,'unknown dependency '+dep)
        if dep in tasks:
            require(tasks[dep]['stage']<=tasks[id]['stage'],f'later dependency {id} -> {dep}')
            visit(dep)
    visiting.remove(id);visited.add(id)
for t in tasks.values():
    for key in ['owner','deliverable','acceptance','source','status']: require(bool(t[key]),t['id']+' missing '+key)
    for p in t['code_targets'].split(';'):
        if p.startswith('game-godot/'):require((ROOT/p).is_file(),'missing source code: '+p)
    require(t['status']=='待实施；本次交付为计划','incorrect implementation status: '+t['id'])
    visit(t['id'])

counts=Counter(r['group'] for r in data['coverage'])
expected={'章节索引':168,'美术12项':12,'场景资产12类':12,'造型8条':8,'配色3方案':3,'语义色10项':10,'空间基础9条':9,'空间机制12条':12,'演出通用12条':12,'逐招定制13条':13,'实测招式18招':18,'原设计系统20项':20,'七台招牌重建':7,'精神首批8条':8,'精神扩展2条':2,'卡组12项':12,'人物关系12项':12,'空地20项':20,'敌人8项':8,'示意错误15项':15,'SML规格35项':35,'操作16项':16,'手感19项':19,'bug13项':13,'Top15':15,'Top外4项':4,'对照维度':11,'敌招5类':5}
require(counts==expected,'source group count mismatch: '+str(counts-Counter(expected)))
ids=[r['id'] for r in data['coverage']]
require(len(ids)==len(set(ids)),'duplicate source IDs')
used=set()
for r in data['coverage']:
    for key in ['action','acceptance','decision','source_ref','work_packages']:require(bool(r[key]),r['id']+' empty '+key)
    require(1<=r['source_line']<=len(source_lines),r['id']+' invalid source line')
    for id in r['work_packages']:
        require(id in tasks,r['id']+' unknown task '+id);used.add(id)
require(used==set(tasks),'unmapped work packages '+str(set(tasks)-used))
headings={i for i,l in enumerate(source_lines,1) if re.match(r'^#{2,4} ',l)}
require(headings=={r['source_line'] for r in data['coverage'] if r['group']=='章节索引'},'missing original heading')
for prefix,n in [('S',19),('M',13),('L',3),('O',16),('H',19),('G',12),('SP-M',12),('SP-BASE',9)]:
    for i in range(1,n+1):require(prefix+str(i) in ids,'missing '+prefix+str(i))
for prefix,n in [('MV',18),('FX',15),('ART',12),('DG-SYS',20),('BUG',13),('TOP',15)]:
    for i in range(1,n+1):require(f'{prefix}{i:02}' in ids,'missing '+f'{prefix}{i:02}')

# The initial 52-package plan is preserved; an independent delivery ledger
# records implemented slices without claiming full-package acceptance.
implementation=json.loads((HERE/'首版施工证据.json').read_text())
require(set(implementation['work_packages'])==set(tasks),'delivery ledger misses a work package')
for id,row in implementation['work_packages'].items():
    require(row.get('full_package_closed') is False,id+' incorrectly closed full package')
    require(bool(row.get('first_version')) and bool(row.get('status')),id+' empty delivery account')
# A title-to-task mapping alone is not an item-level design.
specific={r['id']:r for r in data['coverage'] if r['group']!='章节索引'}
authored=runpy.run_path(str(HERE/'逐项设计源.py'))['DETAILS']
books=json.loads((HERE/'逐项分册清单.json').read_text())
figures=json.loads((HERE/'图解清单.json').read_text())
require(set(specific)==set(authored) and len(specific)==331,'authored item coverage')
require(len(books)==9 and sum(b['count'] for b in books)==331,'detail book count')
require(len(figures)==39 and len({f['id'] for f in figures})==39,'original figure count')
for id,r in specific.items():
    d=r.get('detailed_design',{})
    require(d==authored.get(id),id+' published design differs from source')
    for key in ['analysis','adoption','design','player_expression','verification','example']:
        minimum=5 if key=='adoption' else 12
        require(isinstance(d.get(key),str) and len(d[key].strip())>=minimum,id+' incomplete design field '+key)
    require(r.get('action')==d.get('design') and r.get('acceptance')==d.get('verification'),id+' stale coverage summary')
    group=set(d.get('shared_with',[]))
    require(id in group,id+' missing shared design identity')
    for other in group:
        require(other in authored and authored[other]==d,id+' inconsistent shared design '+other)
    require(bool(r.get('implementation_targets')),id+' no implementation entry point')
    require(set(r.get('design_figures',[])) <= {f['id'] for f in figures},id+' unknown figure')
for f in figures:
    require(set(f['work']) <= set(tasks),f['id']+' unknown work package')
    svg=HERE/f['svg'];png=HERE/f['file']
    require(svg.is_file() and png.is_file(),f['id']+' missing image source/render')
    if svg.is_file():
        try: ET.parse(svg)
        except ET.ParseError as e: errors.append(f['id']+' malformed SVG '+str(e))
    if png.is_file():
        raw=png.read_bytes()
        require(raw[:8]==b'\x89PNG\r\n\x1a\n',f['id']+' invalid PNG')
        if len(raw)>=24:
            w,h=struct.unpack('>II',raw[16:24]);require(w>=1600 and h>=600,f['id']+' insufficient render dimensions')

class Doc(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[];self.inline=[];self.in_script=False;self.details=[];self.visible_images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='details':self.details.append('open' in a)
        if tag=='img' and all(self.details):self.visible_images.append(a.get('src',''))
        if 'id' in a:self.ids.append(a['id'])
        for key in ['href','src']:
            if key in a:self.links.append(a[key])
        if tag=='script':self.in_script=a.get('type','')!='application/json'
    def handle_endtag(self,tag):
        if tag=='script':self.in_script=False
        if tag=='details' and self.details:self.details.pop()
    def handle_data(self,s):
        if self.in_script:self.inline.append(s)
parsed={}
for p in HERE.glob('*.html'):
    if p.name in {'对Astra-v5整改计划的批评与建议.html','给Astra的补强与补全清单.html','给Astra的视觉禁令与审美参考.html','给Astra的视觉总参考.html'}:continue  # Unmodified inputs, not generated reading pages.
    d=Doc();d.feed(p.read_text());parsed[p.resolve()]=d
    require(len(d.ids)==len(set(d.ids)),'duplicate anchor in '+p.name)
    require('lang="zh-CN"' in p.read_text(),'missing lang '+p.name)
    require('viewport' in p.read_text(),'missing viewport '+p.name)
for p,d in parsed.items():
    for link in d.links:
        parts=urlsplit(link)
        if parts.scheme or parts.netloc:continue
        target=(p.parent/unquote(parts.path)).resolve() if parts.path else p
        require(target.is_file(),f'{p.name}: missing link {link}')
        if parts.fragment and target.suffix=='.html':
            require(target in parsed and unquote(parts.fragment) in parsed[target].ids,f'{p.name}: missing anchor {link}')
require(len(parsed)==25,'expected 25 generated reading pages including architecture implementation review')
for b in books:
    expected_ids={id for id,r in specific.items() if r['group'] in b['groups']}
    p=(HERE/(b['slug']+'.html')).resolve()
    require(p in parsed and len(expected_ids)==b['count'],'missing or incorrect book '+b['slug'])
    if p in parsed:
        actual_ids=set(re.findall(r'<section class="design-item" id="([^"]+)"',p.read_text()))
        require(actual_ids==expected_ids,b['slug']+' item set mismatch')
for id,r in specific.items():
    parts=urlsplit(r['first_level_reference']); target=(HERE/unquote(parts.path)).resolve()
    require(target in parsed and parts.fragment in parsed[target].ids,id+' missing first-level specification anchor')
    parts=urlsplit(r['detail_page']);target=(HERE/unquote(parts.path)).resolve()
    require(target in parsed and parts.fragment in parsed[target].ids,id+' missing detailed design anchor')
for f in figures:
    p=(HERE/('index.html' if f['doc']=='00-总方案' else f['doc']+'.html')).resolve()
    require(p in parsed and f['file'] in {unquote(src) for src in parsed[p].visible_images},f['id']+' diagram not visible in primary chapter')
search_page=(HERE/'覆盖核对.html').read_text()
match=re.search(r'<script type="application/json" id="plan-data">(.*?)</script>',search_page,re.S)
require(bool(match),'missing search data')
if match:require(json.loads(match.group(1))==data,'search data is stale')
node=shutil.which('node') or '/Users/rayz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
require(Path(node).is_file(),'Node unavailable for static script syntax check')
if Path(node).is_file():
    for p,d in parsed.items():
        if not d.inline:continue
        result=subprocess.run([node,'--check'],input='\n'.join(d.inline),text=True,capture_output=True)
        require(result.returncode==0,p.name+' inline script syntax: '+result.stderr.strip())
for p in HERE.glob('*.md'):
    require('<!-- WORK_PACKAGES -->' not in p.read_text(),'unexpanded work packages')
    for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        if '://' in link or link.startswith('#'):continue
        target=(p.parent/unquote(link.split('#')[0])).resolve()
        require(target.is_file(),f'{p.name}: missing Markdown link {link}')
for file,count in [('整改工作包.tsv',52),('报告逐项覆盖.tsv',499),('逐项设计.tsv',331)]:
    with (HERE/file).open() as f: require(len(list(csv.DictReader(f,delimiter='\t')))==count,'TSV count '+file)

report={'plan_check':'pass' if not errors else 'fail','source_hashes_verified':len(data['source_hashes']),'work_packages':len(tasks),'coverage_records':len(data['coverage']),'chapter_headings':len(headings),'specific_designs':len(specific),'unique_authored_designs':len({json.dumps(d,ensure_ascii=False) for d in authored.values()}),'detail_books':len(books),'original_figures':len(figures),'html_pages':len(parsed),'checks':['source hashes','expected source IDs','six authored design fields per specific item','published source consistency','declared shared designs','exact detail book contents','acyclic dependencies','phase ordering','existing code paths','local file links','HTML anchors','visible primary-chapter diagrams','SVG syntax and PNG dimensions','embedded search data','inline JavaScript syntax only','TSV counts'],'limitations':['This is a static plan check, not game implementation or player acceptance.','Browser security review rejected local-page inspection. HTML layout and interactive search were not browser-tested; no alternate access route was attempted.','Raster diagrams were visually reviewed separately; this script does not judge diagram clarity or design quality.'],'errors':errors}
(HERE/'计划核对结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
