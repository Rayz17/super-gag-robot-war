from pathlib import Path
import json,html,shutil
P=Path(__file__).resolve().parent
r=json.loads((P/'brave-components-production-r11.json').read_text())
items={i['number']:i for i in r['selected_set']}
E=lambda s:html.escape(str(s),quote=True)
marks={
1:[(3,380,245,215,188)],
2:[(2,180,270,170,140),(2,1034,331,135,125),(4,614,210,203,208)],
5:[(6,180,225,720,255)],
8:[(1,295,225,230,200),(4,329,20,298,240)],
9:[(1,1080,76,350,260)],
11:[(7,319,330,150,146)]
}
def fig(n,cls=''):
 i=items[n];w,h=i['pixel_size']
 overlay=''
 for tag,x,y,bw,bh in marks.get(n,[]):
  overlay+=f'<g><rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="12"/><circle cx="{x+24}" cy="{y+24}" r="23"/><text x="{x+24}" y="{y+25}">{tag}</text></g>'
 overlay=f'<svg viewBox="0 0 {w} {h}" aria-hidden="true" class="marks">{overlay}</svg>' if overlay else ''
 return f'<figure class="{cls}"><a href="{E(i["file"])}" class="picture"><img src="{E(i["file"])}" alt="本次附件{n}：{E(i["title"])}" loading="lazy">{overlay}</a><figcaption><b>附件 {n} · {E(i["title"])}</b><p>{E(i["role"])}。</p></figcaption></figure>'
role_rows=''.join(f'<tr><td>{i["number"]}</td><td><a href="{E(i["file"])}">{E(i["title"])}</a></td><td>{E(i["role"])}</td></tr>' for i in r['selected_set'])
groups=''
for group in ['局部修图','补清部件对应','制作时归一']:
 rows=''
 for x in r['consistency_review']:
  if x['group']!=group:continue
  idx=int(x['id'].split('-')[-1])
  links='、'.join(f'<a href="{E(items[n]["file"])}">图{n}</a>' for n in x['images'])
  rows+=f'<article class="finding" id="{x["id"]}"><div class="finding-top"><span class="issue-number">{idx:02}</span><div><h3>{E(x["title"])}</h3><p class="refs">{links}</p></div></div><p><b>看到的差异：</b>{E(x["observation"])}</p><p class="action"><b>具体处理：</b>{E(x["correction"])}</p><p class="keep">{E(x["preserve"])}</p></article>'
 groups+=f'<section class="finding-group"><p class="eyebrow">{E(group)}</p>{rows}</section>'
styles='''
:root{--paper:#f2f0e6;--card:#fffdf6;--ink:#21363f;--muted:#66767b;--orange:#cf582b;--line:#ccd3cd;--teal:#246c6b}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.75 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}html{scroll-padding-top:80px}
header,main,footer{max-width:1320px;margin:auto;padding:30px}header{padding-top:48px}.eyebrow{color:var(--orange);font-size:13px;letter-spacing:.12em;font-weight:800}h1{font-size:clamp(30px,4vw,50px);line-height:1.22;margin:10px 0 20px}h2{font-size:30px;line-height:1.35;margin:8px 0 16px}h3{font-size:23px;line-height:1.4;margin:0 0 6px}p{margin:9px 0 18px}a{color:var(--teal);text-underline-offset:4px}section{padding:28px 0 38px;border-bottom:1px solid var(--line)}nav{position:sticky;top:0;z-index:5;display:flex;justify-content:center;gap:22px;flex-wrap:wrap;background:#21363ff5;padding:13px 20px}nav a{color:#fff8e9;text-decoration:none}nav a:focus-visible,a:focus-visible{outline:3px solid #e9a248;outline-offset:4px}.lead{max-width:1000px;font-size:21px}.summary{padding:18px 23px;background:#e5eae0;border-left:5px solid var(--teal);border-radius:5px}.summary p:last-child{margin-bottom:0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}.core-grid{grid-template-columns:.68fr 1.32fr}.wide{grid-column:1/-1}figure{margin:17px 0 8px;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}.picture{display:block;position:relative;background:#fffef7}.picture img{width:100%;height:auto;display:block}.hero-image .picture img{max-height:880px;object-fit:contain}.grid .picture img{height:460px;object-fit:contain}.grid .marks{display:none}.grid figure.annotated .picture img{height:auto}.grid figure.annotated .marks{display:block}.core-grid .picture img{height:560px}figcaption{border-top:1px solid var(--line);padding:15px 19px;font-size:15px;line-height:1.6}figcaption b{font-size:18px}figcaption p{margin:7px 0 0}.marks{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.marks rect{fill:#f58c2020;stroke:#de5a2b;stroke-width:5}.marks circle{fill:#c84925;stroke:#fff7e7;stroke-width:3}.marks text{fill:white;font:bold 29px sans-serif;text-anchor:middle;dominant-baseline:central}.finding{border:1px solid var(--line);background:var(--card);padding:24px 27px;border-radius:9px;margin:16px 0 22px}.finding-top{display:flex;gap:19px;align-items:start}.issue-number{font-size:25px;color:var(--orange);font-weight:800;line-height:1.4;min-width:37px}.refs{font-size:14px;margin:0}.action{background:#edf0e6;border-left:4px solid var(--teal);padding:13px 18px;margin:15px 0}.keep{font-size:15px;color:var(--muted);margin-bottom:0}.finding-group{border:0;padding:13px 0}.finding-group>.eyebrow{font-size:18px;letter-spacing:0}table{border-collapse:collapse;width:100%;font-size:16px;background:var(--card)}th,td{padding:13px 16px;text-align:left;border:1px solid var(--line);vertical-align:top}th{background:#e5eae0}.table-scroll{overflow-x:auto}.note{font-size:15px;color:var(--muted)}details{background:var(--card);border:1px solid var(--line);padding:17px 22px;margin-top:20px;border-radius:7px}summary{font-weight:700;cursor:pointer}footer{font-size:14px;color:var(--muted);padding-bottom:60px}
@media(max-width:820px){header,main,footer{padding:24px 17px}.grid,.core-grid{grid-template-columns:1fr}.grid .picture img,.core-grid .picture img{height:auto;max-height:760px}.grid .marks{display:block}.finding{padding:20px 18px}nav{font-size:15px;gap:13px}.lead{font-size:19px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>社勇王｜本次选定图集与一致性评审</title><style>{styles}</style></head><body>
<header id="selected-set-r11"><p class="eyebrow">超 GAG · 社勇王 / 勇拳 · 2026.10.18 R11</p><h1>整体采用这一套，剩下做局部对齐</h1><p class="lead">你本次选定的 <b>11 张原图</b>收为同一套设计基准。整机头身比、巨拳、轰炸机框架、长发、列车臂壳和履带腿沿用；本轮只核对微调与同一部件在不同图中的对应。</p><div class="summary"><p><b>结论：</b>造型方向成立。需要局部改图的有头部状态、发动机尾端和侧胸机鼻；需要补清的是背包、列车臂壳两态、钻机到腿足的归属。胸标及材质在制作时归一。</p><p>圈号对应下方评审项。原图文件全部保留，本页仅叠加评审标记；本轮没有重新生成或暗换图。</p></div><p class="note">图10负责整机终态，图11负责勇拳主体，图6核对原核心三视；图7/8/9负责过程，最终外形向整机对齐。</p></header>
<nav><a href="#combined">选定整机</a><a href="#core">勇拳与面罩</a><a href="#vehicles">三个载具</a><a href="#review-r11">8项具体评审</a><a href="#source-index">11张职责表</a></nav>
<main>
<section id="combined"><h2>整机沿图10，侧面与背面沿图1、2</h2><p>保持高身材与巨拳的重量，不把肩翼改薄，不为解释分件另画一副腿。图1、2的局部问题向同一套整机对齐。</p>{fig(10,'hero-image')}<div class="grid">{fig(1,'annotated')}{fig(2,'annotated')}</div></section>
<section id="core"><h2>完整勇拳核心保留，面罩由轰炸机加载</h2><p>图11定主体、图6核对正侧背。图9的来源和装载方式保留；额部终态只需向图10统一。拳甲继续强化，列车臂壳不替代巨拳。</p><div class="grid core-grid">{fig(11,'annotated')}{fig(6)}</div><div id="mask-loading-r9">{fig(9)}</div></section>
<section id="vehicles"><span id="bomber"></span><h2>轰炸机：主体与两侧翼架分别活动</h2><p>图3固定单体造型，图8固定分件和肩部让位思路。双竖翼、肩甲斜三角体积、进气朝前的轴向保留。</p>{fig(3)}{fig(8)}
<div id="train"><h2>列车：两节各对应一臂，收拢与展开分开表达</h2><p>图4固定车型；图7负责开壳。图10的待机轮廓继续保留，用同一套壳体的两个状态连起来，不做两辆不同车型。</p>{fig(4)}{fig(7)}</div>
<div id="drill"><h2>钻机：载具造型与整机腿足分别固定，再补归属</h2><p>图5固定单体，图10固定腿长和安装形状，图1、2补侧后。接下来只补一张部件归属示意，防止又从载具推导出不同的长腿。</p>{fig(5)}</div></section>
<section id="review-r11"><span id="review"></span><span id="corrections-r9"></span><span id="corrections-r10"></span><h2>具体修哪里，哪些只是缺少说明</h2><p>以下结论来自作者实际查看这11张图。<b>已经看见的差异</b>与<b>尚未交代的对应关系</b>分开；没有把正常遮挡、透视或发光状态一律判错。</p>{groups}<div class="summary"><p><b>修订次序：</b>先局部修头部状态、发动机尾口和胸鼻；再用小示意补双口背包、臂壳两态和钻机分件归属。只处理这些明确部位，不重新生成整机方案。</p><p>不用制作精密机械折变或逐对碰撞参数；可见部件的数量、朝向、比例与归属必须自洽，随后由事件驱动各组件切换状态。</p></div></section>
<section id="source-index"><h2>11张图分别负责什么</h2><div class="table-scroll"><table><thead><tr><th>附件</th><th>用途</th><th>本次采用范围</th></tr></thead><tbody>{role_rows}</tbody></table></div><p class="note">本次选择确立整体设计基准，不把尚未画出的局部修订、精确模型、动画或运行验收写成完成。</p>
<details><summary>此前修订与本轮未选的补充稿</summary><p>R9长腿稿仍停用。R10腿部细图未包含在你本次列出的11张中，保留作补充候选，不自行替换图10。</p><div id="leg-redraw-r10"><a href="samples/F11-leg-proportion-redraw-r10.png">查看R10腿部细图</a></div><div id="drill-source-terminal-r9"></div><p><a href="brave-components-reader-history-r10.html">查看本次选择前的R10阅读页</a> · <a href="brave-components-production-r10.json">R10来源记录</a> · <a href="brave-components-production-r11.json">当前11张来源与评审记录</a></p></details></section>
</main><footer><a href="index.html#brave-components-r8">返回美术升级总页</a> · <a href="brave-components-production-r11.json">当前来源与具体评审</a><p>本轮完成图集选择记录与一致性评审；原图未重绘、运行资产未更换，未发送新的交接。</p></footer></body></html>'''
old=P/'brave-components-r8.html';history=P/'brave-components-reader-history-r10.html'
if not history.exists():shutil.copy2(old,history)
old.write_text(page)
print('Selected-set reader updated: 11 original images, source roles, marked differences and 8 concrete recommendations.')

