from pathlib import Path
import json,html,shutil,ast
P=Path(__file__).resolve().parent
r=json.loads((P/'brave-components-production-r12.json').read_text())
fixed=r.get('source_design_fixed',False)
items={x['number']:x for x in r['current_set']}
originals={x['number']:x for x in r['selected_set']}
E=lambda x:html.escape(str(x),quote=True)
tree=ast.parse((P/'build_brave_selected_review_r11.py').read_text())
styles=next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='styles' for t in n.targets))
styles+='.current-label{display:inline-block;padding:3px 10px;border-radius:4px;background:#dce9df;color:#28635f;font-size:13px;margin-right:10px}.source-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}.source-grid .picture img{max-height:800px;object-fit:contain}.swatches{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}.swatches span{display:block;padding:14px 10px;border:1px solid #bec8c4;border-radius:6px;text-align:center;font-size:15px}.swatches i{display:block;height:35px;border:1px solid #76847c;border-radius:4px;margin-bottom:8px}.new-set>figure{margin-bottom:32px}@media(max-width:820px){.source-grid{grid-template-columns:1fr}.swatches{grid-template-columns:repeat(3,1fr)}}'
def media(file,title,caption,label='本轮新绘',cls=''):
 return f'<figure class="{cls}"><a class="picture" href="{E(file)}"><img src="{E(file)}" alt="{E(title)}" loading="lazy"></a><figcaption><span class="current-label">{E(label)}</span><b>{E(title)}</b><p>{E(caption)}</p></figcaption></figure>'
def fig(n,cls=''):
 x=items[n]
 label='原选图保持'
 cap=x['role']
 if x.get('baseline_file'):
  label='复用局部修正版' if x.get('source_mode','').startswith('reuse_') else '本轮新绘'
  cap=x.get('observed',cap)
  compare=f' <a href="{E(x["baseline_file"])}">对照原选附件{n}</a>'
 else:compare=''
 return media(x['file'],f'附件{n}对应 · {x["title"]}',cap,label,cls).replace('</figcaption>',compare+'</figcaption>')
changes=''
for x in r['consistency_review']:
 links=' · '.join(f'<a href="{E(q)}">图稿{i+1}</a>' for i,q in enumerate(x['actual_media']))
 changes+=f'<tr id="{x["id"]}"><td><b>{E(x["title"])}</b></td><td>{E(x["actual_work"])}</td><td>{links}<br><span class="note">'+('本批源图设计已由用户固定' if fixed else '作者已查看；新修订待确认')+'</span></td></tr>'
sources=''
for n,x in originals.items():
 current=items[n]
 sources+=f'<tr><td>{n}</td><td><a href="{E(x["file"])}">{E(x["title"])} · 原选图</a></td><td>{E(x["role"])}</td><td><a href="{E(current["file"])}">当前图</a></td></tr>'
new_bomber=media('samples/M04-bomber-backpack-assembly-r12.png','原头加载面罩，独立背包补齐双格栅','灰色核心保留双橙角原头；面罩来自中央机身内舱。独立背包现在有上下两口；右侧终态和下方肩翼让位保留。')
backpack=media('samples/M04-backpack-fold-map-r12.png','后机身下模块翻出，形成上下双格栅','左：后下侧露出折收模块。中：同一模块翻出并调整朝向。右：双口进入同一橙黑背包，双鳍仍在两侧。此图补部件归属，不替代精确模型。')
train_rest=media('samples/F12-train-protective-cradle-r12c.png','收近状态：单车头、U形护套、内侧开放','只从原选展开图的安装面板局部编辑开合。车头在肘后，平方连接端朝拳；护套不是封闭车厢，巨拳独立露出。')
train_open='''<figure><a class="picture" href="samples/F12-subtrain-assembly-r8b.png"><svg viewBox="805 445 730 570" role="img" aria-label="原选展开图右下安装状态局部"><image href="samples/F12-subtrain-assembly-r8b.png" width="1536" height="1024"/></svg></a><figcaption><span class="current-label">原选展开态</span><b>两片侧壳打开，原前臂与拳不动</b><p>直接显示你选定图7右下局部，不重新推导另一只前臂。两态的开合关系以下方可编辑示意为准；绘制图不声称同模型精准同位。</p></figcaption></figure>'''
state=media('F12-shell-state-framework-r12.png','壳体、小翼和腕环的状态关系','剖面示意固定同一原臂、两片外壳和小翼。发光环留在原腕位置；合体时主要被外甲遮住，动作时才增亮。','本轮绘制的结构示意')
drill=media('F11-component-routing-r12.png','钻机五组部件，对应到既定腿形','前履带组转为主小腿，后组进入足侧/足跟；座舱窗面折入内后侧，白壳沿原分缝转为胫甲。右侧沿原选腿局部，仅说明归属，不重画腿长。','本轮绘制的部件归属图')
material=''.join(f'<span><i style="background:{color}"></i>{label}</span>' for label,color in [('象牙白涂装','#e8e0ce'),('暖橙涂装','#dc7127'),('石墨结构','#343d43'),('蓝黑玻璃','#234e67'),('金属钻头','#8e989d'),('腕部／眼部能量','#42c6db')])
page=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>社勇王｜局部修订与部件对应 R12</title><style>{styles}</style></head><body>
<header id="selected-set-r11"><p class="eyebrow">超 GAG · 社勇王 / 勇拳 · 2026.10.18 R12</p><h1>沿选定造型，把局部和部件对应补齐</h1><p class="lead">保持你选定的11张整体基准。本轮补出双格栅背包、原头与面罩的装配，列车护套和展开状态，以及钻机到腿足的归属；侧胸钝鼻、尾喷口、面罩额部和无胸标主体采用复核过的局部修正版。</p><div class="summary"><p><b>先看新内容：</b>下面先展示本轮补图，再看侧背与核心。每张标明“本轮新绘”“结构示意”“复用局部修正版”或“原选图保持”。</p><p>新图已做作者检查，等待你确认。它们是设计源图，未替换游戏模型或运行资产，也未发送新的交接。</p></div></header>
<nav><a href="#redraw-r12">本轮修订</a><a href="#train">臂壳两态</a><a href="#drill">钻机到腿</a><a href="#local-body">侧背／核心</a><a href="#review-r11">8项对照</a><a href="#source-index">原图与当前图</a></nav>
<main>
<section id="redraw-r12" class="new-set"><span id="bomber"></span><h2>面罩来自轰炸机，背包也沿同一机身展开</h2>{new_bomber}{backpack}
<div id="mask-loading-r9"><h2>额部统一：原头与外罩分别保留自己的颜色</h2>{fig(9)}</div></section>
<section id="train"><h2>列车臂壳：收近成护套，左右打开作炮击态</h2><p>两节各对应一臂；车头退向肘后，原中间连接端朝拳。先保留同一完整核心前臂和巨拳，再切外壳状态。</p><div class="source-grid">{train_rest}{train_open}</div>{state}</section>
<section id="drill"><h2>钻机归属画清，不再另生一副腿</h2>{drill}<p class="note">五组编号给出本轮具体设计：钻架→膝，前履带→小腿，后组→足侧/跟，座舱→内后侧，车壳→分段胫甲。隐藏面和铰链净空仍留待模型制作核对。</p></section>
<section id="local-body"><h2>钝机鼻、尾喷口与无胸标核心</h2><p>这三张是此前已绘制的局部修正版，本轮重新与原选图逐项核对后复用；没有把它们写成刚刚新生成。</p><div class="source-grid">{fig(1)}{fig(2)}</div><div class="source-grid" id="core">{fig(11)}{fig(6)}</div></section>
<section id="materials"><h2>同一材质家族，保留各机组的色块分工</h2><div class="swatches">{material}</div><p>色块只说明共同材质角色，最终明暗仍跟随所选原图。轰炸机主翼偏石墨、列车偏白、钻机橙白；玻璃与能量光分开，腕环不变成全臂亮蓝条。</p><p class="note">本段规范的是设计图与状态表达；没有声称已经实现游戏材质、发光动画或声音。</p></section>
<section id="review-r11"><span id="review"></span><span id="corrections-r9"></span><span id="corrections-r10"></span><h2>上一轮8项意见，实际落在哪里</h2><div class="table-scroll"><table><thead><tr><th>原问题</th><th>本轮实际处理</th><th>对应图稿</th></tr></thead><tbody>{changes}</tbody></table></div><p class="note">这些是作者实际看图后的记录，不代签用户认可，也不等于严格三视、隐藏面或连续动作验证。</p></section>
<section id="source-index"><h2>原选图与当前修订逐一对应</h2><div class="table-scroll"><table><thead><tr><th>原附件</th><th>原选文件</th><th>负责内容</th><th>当前修订</th></tr></thead><tbody>{sources}</tbody></table></div><details id="combined"><summary>整体主稿及三个载具母版保持</summary>{fig(10)}{fig(3)}{fig(4)}{fig(5)}</details>
<details><summary>原评审、失败尝试与制作输入</summary><p><a href="brave-components-reader-history-r11.html">R11原图集及评审</a> · <a href="brave-components-production-r12.json">R12实际图稿、来源与作者观察</a></p><p><a href="brave-bomber-backpack-assembly-prompt-r12.json">装配图实际提示</a> · <a href="brave-backpack-fold-map-prompt-r12.json">背包折叠图实际提示</a> · <a href="brave-train-local-closing-prompt-r12c.json">臂壳局部收拢实际提示</a>。以上均使用内置Imagegen；既有修正版的提示来源亦保存在R12记录中。</p><p><a href="F11-component-routing-r12.svg">钻机归属可编辑示意</a> · <a href="F12-shell-state-framework-r12.svg">臂壳状态可编辑示意</a>。</p><p>两张带长车厢或额外车头的尝试已停用：<a href="samples/F12-train-two-states-r12a-rejected.png">第一次</a>、<a href="samples/F12-train-two-states-r12b-rejected.png">第二次</a>。之后改为单面板局部编辑与状态示意，未将失败稿混入当前清单。</p><div id="leg-redraw-r10"><p><a href="samples/F11-leg-proportion-redraw-r10.png">R10腿部候选</a>仍只留历史补充，不替换选定整体图。</p></div><div id="drill-source-terminal-r9"></div></details></section>
</main><footer><a href="index.html#brave-components-r8">返回美术升级总页</a> · <a href="brave-components-production-r12.json">当前修订来源记录</a><p>本轮是源图局部修订与对应补图。原11张基准保留；新图确认、模型制作与运行验收分别记录。</p></footer></body></html>'''
old=P/'brave-components-r8.html';history=P/'brave-components-reader-history-r11.html'
if fixed:
 page=page.replace('<h1>沿选定造型，把局部和部件对应补齐</h1>','<h1>本批设计已固定，后续沿这套源图制作</h1>')
 page=page.replace('新图已做作者检查，等待你确认。它们是设计源图，未替换游戏模型或运行资产，也未发送新的交接。','2026.10.18 用户确认本批设计先固定。整机、四机组件及本轮局部修正版均列入当前设计基准；<a href="source-design-freeze-20261018.html">查看含六名角色的固定清单</a>。模型、动作与运行分别验证；本次未发送交接。')
 page=page.replace('这些是作者实际看图后的记录，不代签用户认可，也不等于严格三视、隐藏面或连续动作验证。','作者看图记录与用户确认分别保存：上述源图设计已固定；严格同模型视图、隐藏面和连续动作仍由后续制作验证。')
 page=page.replace('本轮是源图局部修订与对应补图。原11张基准保留；新图确认、模型制作与运行验收分别记录。','本轮源图设计已固定。原选图留历史追溯，当前局部修正版优先；模型制作与运行验收分别记录。')
 if r.get('handoff_sent'):
  page=page.replace('模型、动作与运行分别验证；本次未发送交接。','已集中交给“战斗主玩法打磨”；模型、动作与运行分别验证。<a href="source-design-freeze-handoff-20261018.md">交接内容</a>。')
if not history.exists():shutil.copy2(old,history)
old.write_text(page)
print('R12 source reader generated with current images, original comparisons and explicit provenance.')

