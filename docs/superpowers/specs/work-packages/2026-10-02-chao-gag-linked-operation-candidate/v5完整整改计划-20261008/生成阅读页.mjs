import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {marked} from '/Users/rayz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';

const dir=path.dirname(fileURLToPath(import.meta.url));
const data=JSON.parse(await fs.readFile(path.join(dir,'计划数据.json'),'utf8'));
const docs=['00-总方案','01-核心机制与操作','02-美术与逐招演出','03-机体与人物体系','04-战场与立体机制','05-施工与验收','06-从方案到可实现设计','07-首关施工规格','08-图形与手感施工表','09-人物指令与机魂施工规格','10-专关与成长对照规格','11-名场面与系统全链补定','12-首版交付与验证'];
const names=['总方案','核心机制与操作','美术与逐招演出','机体与人物体系','战场与立体机制','施工与验收','从方案到可实现设计','首关施工规格','图形与手感施工表','人物指令与机魂','专关与成长对照','名场面与系统补定','首版交付与验证'];
docs.push('13-建筑比例与材质重做');names.push('建筑比例与材质重做');
const readingOrder=[0,13,12,7,8,11,9,10,1,2,3,4,5,6];
const layer=JSON.parse(await fs.readFile(path.join(dir,'人物与成长施工合同.json'),'utf8'));
const figures=JSON.parse(await fs.readFile(path.join(dir,'图解清单.json'),'utf8'));
const books=JSON.parse(await fs.readFile(path.join(dir,'逐项分册清单.json'),'utf8'));
const implementation=JSON.parse(await fs.readFile(path.join(dir,'首版施工证据.json'),'utf8'));
const outputName=s=>s===docs[0]?'index.html':s+'.html';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const phases=['0 · 留存与复现','1 · 可信的一手棋','2 · 整场可读可操作','3 · 三战场值得调度','4 · 立体与空地组合','5 · 人物与机体身份','6 · 全量集成验收'];

let work='';
for(let phase=0;phase<phases.length;phase++){
 work+=`\n### ${phases[phase]}\n\n| 工作包 / 负责专业 | 交付内容与范围 | 验收重点与反例 | 证据与结论 | 完整包依赖 |\n|---|---|---|---|---|\n`;
 for(const t of data.tasks.filter(x=>x.stage===phase)){
  const gate=layer.task_gates[t.id];
  const done=implementation.work_packages[t.id];
  work+=`| <a id="${t.id}"></a>**${t.id} ${t.title}**<br>${t.owner} | ${t.deliverable}<br><strong>结论档：</strong>${gate.tiers.join('、')}<br><strong>首关子集：</strong>${gate.first_slice} | ${t.acceptance}<br><details><summary>必须保留的反例</summary>${gate.counterexample}</details> | ${done.first_version}<br><a href="${done.report_url||"12-首版交付与验证.html"}">${done.evidence?"查看实现证据":"查看尚未实施范围"}</a>。<br><strong>完整包未关闭。</strong> | ${t.dependencies.join('、')||'—'} |\n`;
 }
}
const workPath=path.join(dir,docs[5]+'.md');
let source=await fs.readFile(workPath,'utf8');
if(source.includes('<!-- WORK_PACKAGES -->')) source=source.replace('<!-- WORK_PACKAGES -->',`<!-- WORK_PACKAGES_START -->\n${work}\n<!-- WORK_PACKAGES_END -->`);
else source=source.replace(/<!-- WORK_PACKAGES_START -->[\s\S]*?<!-- WORK_PACKAGES_END -->/,`<!-- WORK_PACKAGES_START -->\n${work}\n<!-- WORK_PACKAGES_END -->`);
await fs.writeFile(workPath,source);

const css=`
:root{--ink:#243742;--muted:#586e78;--paper:#f4f2eb;--panel:#fffefa;--line:#d3ddd9;--teal:#176b73;--amber:#a96120;--accent:#dc674d}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC",sans-serif;line-height:1.85;font-size:16px}a{color:var(--teal);text-decoration-thickness:1px;text-underline-offset:3px}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--accent);outline-offset:3px}.skip{position:absolute;top:-80px}.skip:focus{top:10px;background:white;padding:10px;z-index:9}.shell{display:grid;grid-template-columns:245px minmax(0,1fr);max-width:1600px;margin:auto}.sidebar{position:sticky;top:0;height:100vh;overflow:auto;background:#e5ece8;border-right:1px solid #c4d5d0;padding:30px 20px}.brand{font-size:14px;letter-spacing:.12em;color:var(--teal);font-weight:750}.date{font-size:12px;color:var(--muted);margin:7px 0 24px}.nav a{display:block;text-decoration:none;padding:9px 12px;border-radius:7px;margin:4px 0}.nav a.active{background:var(--teal);color:white}.nav a:hover{box-shadow:inset 0 0 0 1px var(--teal)}.status{border-top:1px solid var(--line);margin-top:25px;padding-top:15px;color:var(--muted);font-size:13px}.status strong{color:var(--amber)}main{padding:42px clamp(24px,4vw,65px) 80px;min-width:0}article{max-width:1100px;margin:auto}h1{font-size:clamp(28px,3vw,39px);line-height:1.4;letter-spacing:-.03em;margin:0 0 18px}h2{font-size:25px;margin:55px 0 20px;border-top:2px solid var(--line);padding-top:24px;line-height:1.5}h3{font-size:20px;margin:30px 0 12px;color:var(--teal)}p,ul,ol{margin:14px 0}li{margin:7px 0}strong{font-weight:690}blockquote{margin:22px 0;background:#e6efeb;padding:14px 25px;border-left:4px solid var(--teal);border-radius:0 8px 8px 0}code{font-family:ui-monospace,monospace;font-size:.87em;background:#e8ece6;padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:9px;margin:20px 0;background:var(--panel)}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.7}th{text-align:left;padding:13px 14px;background:#dce8e3;color:#204c53;font-weight:700}td{vertical-align:top;padding:13px 14px;border-top:1px solid var(--line)}td:first-child{min-width:145px;font-weight:560}tr:nth-child(even) td{background:#f8f8f1}img{max-width:100%;height:auto;border-radius:8px;border:1px solid var(--line)}article>p:has(img){max-width:800px;margin:25px auto}figure{margin:25px 0}figcaption,.caption{font-size:13px;color:var(--muted)}details{margin:18px 0;padding:15px 20px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}summary{cursor:pointer;color:var(--teal);font-weight:650}.toc{background:#edf0e8;border:1px solid var(--line);border-radius:8px;padding:16px 22px;margin:28px 0;font-size:14px}.toc a{display:inline-block;margin:3px 14px 3px 0}.foot{margin-top:45px;padding-top:20px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}.filters{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:var(--paper);padding:12px 0;z-index:3}input,select{font:inherit;border:1px solid #90aaa8;border-radius:7px;background:var(--panel);padding:9px 12px;color:var(--ink)}input{flex:1;min-width:220px}.count{font-size:13px;color:var(--muted)}.source-note{font-size:13px;color:var(--muted)}.badge{font-size:12px;padding:3px 7px;background:#dcece5;border-radius:4px;white-space:nowrap}.ledger-card{border:1px solid var(--line);background:var(--panel);border-radius:9px;padding:18px 20px;margin:12px 0}.ledger-card h3{margin:0 0 8px;font-size:17px}.ledger-card p{margin:8px 0;font-size:14px}.row{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.ledger-card summary{font-size:13px}.ledger-card details{padding:10px 14px}.task-links a{display:inline-block;margin-right:10px}.footer-nav{display:flex;justify-content:space-between;gap:15px;margin-top:30px}svg{max-width:100%;height:auto}
@media(max-width:1000px){.shell{grid-template-columns:205px minmax(0,1fr)}.sidebar{padding:25px 12px}main{padding:32px 22px 55px}table{min-width:650px}}
@media(max-width:720px){.shell{display:block}.sidebar{position:static;height:auto;padding:16px 18px;border-right:0;border-bottom:1px solid var(--line)}.date{margin-bottom:10px}.nav{display:flex;gap:5px;overflow:auto}.nav a{white-space:nowrap;font-size:13px;padding:7px 10px}.status{display:none}main{padding:26px 18px 50px}body{font-size:16px}h2{font-size:22px;margin-top:40px}.filters{position:static}h1{font-size:28px}td,th{padding:11px}.toc a{display:block}}
@media print{.sidebar,.filters,.footer-nav,.skip{display:none}.shell{display:block}main{padding:0}body{background:white;font-size:10pt}h1{font-size:22pt}h2{font-size:16pt;break-after:avoid}h3{break-after:avoid}.table-wrap{overflow:visible;border-radius:0}table{min-width:0!important;font-size:9pt}tr{break-inside:avoid}a{color:inherit}details{break-inside:avoid}.ledger-card{break-inside:avoid}}
`;

const extraCss=`
.nav-label{font-size:12px;font-weight:750;letter-spacing:.07em;margin:24px 12px 10px;color:var(--muted)}.nav small{float:right;font-size:11px;opacity:.7}.detail-reading{background:#dfece5;border:1px solid #adcbc0;border-radius:10px;padding:20px 24px;margin:28px 0}.detail-reading ul{columns:2;column-gap:30px;font-size:14px;padding-left:20px}.detail-reading li{break-inside:avoid}.design-item{padding:16px 0 35px;border-bottom:2px solid var(--line);scroll-margin-top:24px}.design-item h3{font-size:22px;line-height:1.5}.design-item>p{max-width:960px}.design-example{border-left:4px solid var(--amber);background:#f1e7d1;border-radius:0 8px 8px 0;padding:15px 22px;margin:21px 0}.design-example p{margin:6px 0 0}.implementation{font-size:14px;overflow-wrap:anywhere}.implementation a{word-break:break-word}.item-toc{font-size:14px}.item-toc ul{columns:2}.item-toc li{break-inside:avoid}figure img{display:block;width:100%;max-height:none;background:#f0f0e7}figure figcaption{padding:10px 4px 0;line-height:1.7}figure a:has(img){display:block}figure{margin:28px 0 35px}figure strong{color:var(--teal)}button{font:inherit;padding:10px 18px;border:1px solid var(--teal);border-radius:6px;background:#e0eee7;color:var(--ink);cursor:pointer}.read-detail{font-weight:700}.ledger-card{scroll-margin-top:20px}.design-item blockquote{font-size:16px}.design-item .source-note{font-size:13px}.design-item:target{border-left:5px solid var(--teal);padding-left:20px;background:#f8f9ef}.nav a.active{font-weight:700}
@media(max-width:720px){.detail-reading ul,.item-toc ul{columns:1}.design-item h3{font-size:20px}.nav-label{display:none}.detail-reading{padding:14px 17px}figure{margin:22px -4px}figure img{border-radius:5px}.design-example{padding:12px 15px}.design-item:target{padding-left:12px}}
`;
function shell(title,body,active,extra=''){
 const productionFlowNotice = `<blockquote id="production-flow-entry"><strong>当前制作流程已接入</strong>：保留52包和331条设计，按实际体验施工，分别核对规则、原生输入、画面、动作和声音。<a href="05-施工与验收.html#production-flow-current">读执行办法</a> · <a href="制作流程.json">执行数据</a> · <a href="实施进度-20261010.json">当前台账</a>。结构检查通过不代表游戏或美术验收。</blockquote>`;
 const nav=readingOrder.map(i=>`<a href="${encodeURI(outputName(docs[i]))}"${active===i?' class="active" aria-current="page"':''}>${String(i).padStart(2,'0')}　${names[i]}</a>`).join('')+`<a href="图解总览.html"${active==='figures'?' class="active" aria-current="page"':''}>${figures.length} 张原创图解</a><a href="覆盖核对.html"${active==='coverage'?' class="active" aria-current="page"':''}>搜索 331 条具体设计</a><div class="nav-label">逐项展开 · 9 册</div>`+books.map(b=>`<a href="${encodeURI(b.slug+'.html')}"${active===b.slug?' class="active" aria-current="page"':''}>${esc(b.name)} <small>${b.count}</small></a>`).join('');
 return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(title)} · 工务城整改计划</title><style>${css}${extraCss}</style></head><body><a class="skip" href="#main">跳到正文</a><div class="shell"><aside class="sidebar"><div class="brand">超 GAG / 工务城</div><div class="date">完整整改计划 · 10.10 实施更新</div><nav class="nav" aria-label="分册导航">${nav}</nav><div class="status"><strong>10月10日更新</strong><br>新美术规范、三区色板与背景已接入。<br><a href="13-建筑比例与材质重做.html">当前实机与模型</a><br>三面救援与独立试演继续整改。<br><a href="12-首版交付与验证.html">实机、验证与剩余项</a><br>完整52包仍需逐项验收。<br><br>来源：Grok v5、批评稿及补全清单<br>首批：六机、三面救援<br>报告条目：可按原编号核对</div></aside><main id="main"><article>${productionFlowNotice}${body}<div class="foot">来源：项目内 Grok v5 报告及配套原稿。图中“设计示意”不代表游戏已经实现。第11册为补定设计，第12册为实现与验证，第13册为新美术标准落地与建筑重做。是否好玩仍需真实玩家判断，不能用测试通过代替。</div></article></main></div>${extra}</body></html>`;
}
for(let i=0;i<docs.length;i++){
 let md=await fs.readFile(path.join(dir,docs[i]+'.md'),'utf8');
 let html=marked.parse(md);
 for(const d of docs)html=html.replaceAll(`href="${d}.md"`,`href="${outputName(d)}"`);
 html=html.replaceAll('href="报告逐项覆盖.tsv"','href="覆盖核对.html"');
 let toc=[];let h=0;
 html=html.replace(/<h2>([\s\S]*?)<\/h2>/g,(_,s)=>{h++;const id=`section-${h}`;toc.push(`<a href="#${id}">${s.replace(/<[^>]+>/g,'')}</a>`);return `<h2 id="${id}">${s}</h2>`;});
 html=html.replace(/<h2 id="section-1">/,`<nav class="toc" aria-label="本页目录">${toc.join('')}</nav><h2 id="section-1">`);
 html=html.replace(/<table>[\s\S]*?<\/table>/g,s=>`<div class="table-wrap" tabindex="0" role="region" aria-label="可横向查看的表格">${s}</div>`);
 const rank=readingOrder.indexOf(i),prev=readingOrder[rank-1],next=readingOrder[rank+1];
 html+=`<div class="footer-nav">${prev!==undefined?`<a href="${outputName(docs[prev])}">← ${names[prev]}</a>`:'<span></span>'}${next!==undefined?`<a href="${outputName(docs[next])}">接着读：${names[next]} →</a>`:'<a href="覆盖核对.html">检查报告条目 →</a>'}</div>`;
 await fs.writeFile(path.join(dir,outputName(docs[i])),shell(names[i],html,i));
}
// Detailed pages keep the six design fields open; only source/code scaffolding collapses.
for(const b of [...books,{slug:'图解总览',name:'原创图解',figures:[]}]){
 const md=await fs.readFile(path.join(dir,b.slug+'.md'),'utf8');
 let html=marked.parse(md).replace(/<table>[\s\S]*?<\/table>/g,s=>`<div class="table-wrap" tabindex="0">${s}</div>`);
 html+=`<div class="footer-nav"><a href="index.html">← 回到总方案</a><a href="覆盖核对.html">按原报告编号检索 →</a></div>`;
 await fs.writeFile(path.join(dir,b.slug+'.html'),shell(b.name,html,b.slug==='图解总览'?'figures':b.slug));
}
const groups=[...new Set(data.coverage.map(r=>r.group))];
const scopes=['首关依赖','系统恢复专关','全量／对照'];
const intro=`<h1>先看首关要做什么，再查完整覆盖</h1><p><strong>331 条具体记录，${data.detail_summary.authored_designs} 组关联设计，9 册逐项展开。</strong>不是331个独立开发任务。默认只显示首关依赖：${layer.scope_counts['首关依赖']}条；系统恢复专关${layer.scope_counts['系统恢复专关']}条；全量／对照${layer.scope_counts['全量／对照']}条。每条只归一档，扩展余项保留；首关通过不代表全量完成。</p><p>每条包含分析、采纳、设计、局面和反例。168个章节索引可单独查。本页保留完整实施规格。关联工作包的首版子集已接入，但不能据此将每个完整条目标为通过；具体证据与未做项见第12册。</p><div class="detail-reading"><a href="12-首版交付与验证.html">首版实现与验证</a> · <a href="07-首关施工规格.html">首关固定题面</a> · <a href="09-人物指令与机魂施工规格.html">人物指令与六机招牌</a> · <a href="10-专关与成长对照规格.html">专关与卡组实验</a> · <a href="图解总览.html">${figures.length}张原创图解</a> · <a href="逐项设计.tsv">下载逐项设计</a></div><div class="filters"><input type="search" id="query" aria-label="搜索报告条目" placeholder="编号或问题，如 SPIRIT-2、推位、FX08"><select id="scope" aria-label="筛选交付范围">${scopes.map((s,i)=>`<option value="${s}"${i===0?' selected':''}>${s}（${layer.scope_counts[s]}）</option>`).join('')}<option value="all">全部331条</option><option value="index">仅章节索引168条</option></select><select id="group" aria-label="筛选分类"><option value="">本范围的全部分类</option>${groups.filter(g=>g!=='章节索引').map(g=>`<option>${esc(g)}</option>`).join('')}</select></div><p class="count" id="count" aria-live="polite"></p><div id="rows"></div><button id="more" type="button">再显示30条</button><details><summary>来源快照与下载</summary><p><a href="报告逐项覆盖.tsv">来源覆盖</a> · <a href="整改工作包.tsv">52个工作包</a> · <a href="人物与成长施工合同.json">补强合同与范围</a> · <a href="计划数据.json">全部数据</a></p>${Object.entries(data.source_hashes).map(([k,v])=>`<p>${esc(k)}<br><code>${v}</code></p>`).join('')}<p>补强清单：<code>${layer.review_source.sha256}</code></p><p>原始来源未改动；校验通过不代替玩法、画面或操作验收。</p></details>`;
const payload=JSON.stringify(data).replaceAll('<','\\u003c');
const script=`<script type="application/json" id="plan-data">${payload}</script><script>
const data=JSON.parse(document.getElementById('plan-data').textContent);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const scope=document.getElementById('scope');
const q=document.getElementById('query'),g=document.getElementById('group'),rows=document.getElementById('rows'),count=document.getElementById('count'),more=document.getElementById('more');
const items=new Map(data.coverage.map(r=>[r.id,r]));let limit=30;
function link(id){const r=items.get(id);return r?.detail_page?'<a href="'+esc(r.detail_page)+'">'+esc(id)+'</a>':esc(id);}
function card(r){
 const header='<div class="row"><span class="badge">'+esc(r.id)+'</span><span class="source-note">'+esc(r.group)+' · '+esc(r.source_ref)+' · 原稿第 '+r.source_line+' 行</span></div><h3>'+esc(r.display_title||r.title)+'</h3>';
 if(r.group==='章节索引')return '<section class="ledger-card">'+header+'<p>'+esc(r.index_note)+'</p><p class="task-links">'+(r.detail_items||[]).map(link).join(' · ')+'</p></section>';
 const d=r.detailed_design;
 const delivery=r.delivery;
 return '<section class="ledger-card">'+header+'<p><span class="badge">'+esc(r.scope)+'</span> · <a href="'+esc(r.spec_ref)+'">施工规格</a> · '+esc(delivery.cases.join('、'))+'</p><p><strong>判断：</strong>'+esc(d.analysis)+'</p><p><strong>决定：</strong>'+esc(d.adoption)+'</p><p><strong>设计：</strong>'+esc(d.design)+'</p><p class="design-example"><strong>局面：</strong>'+esc(d.example)+'</p><p class="source-note">完整条目尚未验收；<a href="12-首版交付与验证.html">查看关联首版实现与证据</a>。'+esc(delivery.remainder)+'</p><p><a class="read-detail" href="'+esc(r.detail_page)+'">读完整设计：操作、画面、反例与施工入口 →</a></p><p class="task-links">'+r.work_packages.map(id=>'<a href="05-施工与验收.html#'+id+'">'+id+' '+esc(data.tasks.find(t=>t.id===id).title)+'</a>').join('')+'</p></section>';
}
function matches(r,term){
 if(scope.value==='index')return r.group==='章节索引'&&(!term||[r.id,r.title,r.source_ref].join(' ').toLowerCase().includes(term));
 if(r.group==='章节索引'||(scope.value!=='all'&&r.scope!==scope.value)||(g.value&&r.group!==g.value))return false;
 return !term||[r.id,r.title,r.group,r.scope,r.source_ref,JSON.stringify(r.detailed_design||{})].join(' ').toLowerCase().includes(term);
}
function render(){const term=q.value.toLowerCase().trim();const list=data.coverage.filter(r=>matches(r,term));count.textContent='范围：'+scope.options[scope.selectedIndex].text+'。找到 '+list.length+' 条，显示 '+Math.min(limit,list.length)+' 条。';rows.innerHTML=list.slice(0,limit).map(card).join('');more.hidden=limit>=list.length;g.disabled=scope.value==='index';}
function selectExactId(){const target=items.get(q.value.trim().toUpperCase());if(target){scope.value=target.group==='章节索引'?'index':target.scope;g.value='';}}
q.addEventListener('input',()=>{limit=30;selectExactId();render()});g.addEventListener('change',()=>{limit=30;render()});scope.addEventListener('change',()=>{limit=30;g.value='';render()});more.addEventListener('click',()=>{limit+=30;render()});
const requestedScope=new URLSearchParams(location.search).get('scope');if(['all','index','首关依赖','系统恢复专关','全量／对照'].includes(requestedScope))scope.value=requestedScope;
if(location.hash){q.value=decodeURIComponent(location.hash.slice(1));selectExactId();}render();
</script>`;
await fs.writeFile(path.join(dir,'覆盖核对.html'),shell('逐项设计检索',intro,'coverage',script));
console.log(JSON.stringify({pages:docs.length+books.length+2,tasks:data.tasks.length,sourceRecords:data.coverage.length,authoredItems:data.detail_summary.specific_items}));
