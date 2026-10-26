#!/usr/bin/env python3
"""Publish the current M01 head-position studies and retain earlier source history."""
from pathlib import Path
import html
import json

OUT = Path(__file__).resolve().parent
heads = json.loads((OUT / 'M01-head-position-production-r14.json').read_text())
body = json.loads((OUT / 'M01-family-production-r13.json').read_text())


def esc(x):
    return html.escape(str(x), quote=True)


def figure(file, caption, height=650):
    return f'<figure><a href="{esc(file)}"><img src="{esc(file)}" alt="{esc(caption)}" style="max-height:{height}px" loading="lazy"></a><figcaption>{caption}</figcaption></figure>'


css = '''*{box-sizing:border-box}body{margin:0;background:#f4f1e8;color:#253940;font:17px/1.75 system-ui,-apple-system,sans-serif}main{max-width:1450px;margin:auto;padding:40px 26px 70px}a{color:#246b70;text-underline-offset:3px}nav{display:flex;flex-wrap:wrap;gap:12px 24px}h1{font-size:37px;line-height:1.3}h2{font-size:28px;margin-top:48px}h3{font-size:24px}.tag{color:#2b6c6b;font-size:14px;font-weight:750;letter-spacing:.08em}.notice{border-left:5px solid #bb8c39;background:#fffdf6;padding:16px 24px;margin:24px 0}.grid,.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{padding:18px;background:#e9ede6;border-radius:10px}article.best{outline:3px solid #688e76}figure{margin:18px 0;background:#dfe5de;padding:12px;border-radius:7px}figure img{display:block;width:100%;height:auto;object-fit:contain}article img{height:530px;object-fit:contain}figcaption{text-align:center;margin-top:12px;font-size:15px;font-weight:650}.pair img{height:700px}.note{font-size:14px;color:#60736b}details{margin:24px 0;padding:18px;background:#e9ece3;border-radius:8px}summary{cursor:pointer;font-weight:650}table{width:100%;border-collapse:collapse}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #c4d1c5;padding:13px}.scroll{overflow-x:auto}.links{display:flex;flex-wrap:wrap;gap:10px 22px}@media(max-width:750px){main{padding:24px 16px}h1{font-size:29px}.grid,.pair{grid-template-columns:1fr}article img,.pair img{height:auto;max-height:670px}table{font-size:14px}}'''
intro = '''<nav><a href="index.html#next-design-m01-r14">升级总页</a><a href="#head-options">四个头冠方向</a><a href="#body">同系列整机对照</a><a href="next-batch-mecha-20261019.html">旧拳王与王者样例</a></nav><p class="tag">2026.10.19 · 无牌头冠位置 R14 / 整机家族 R13</p><h1>克制的量产机，闪光时也能有主角感</h1><div class="notice"><p>按最新意见重新找头顶天线的位置：长条冠脊暂不沿用，四个候选保持同一套连续视窗、封闭面甲和青绿白金色系。</p><p><b>作者优先建议D，B为可压短的备选。</b>这里是四种实际画出的探索，尚未由用户选定；不把提示词中的尺寸目标当作已达成。</p></div>'''
cards = ''
for item in heads['items']:
    cards += f'<article id="head-{item["id"]}" class="{"best" if item["id"] == "D" else ""}"><p class="tag">方向 {item["id"]}{" · 作者优先建议" if item["id"] == "D" else ""}</p><h3>{esc(item["title"])}</h3>{figure(item["file"], item["id"] + ' · ' + item["title"])}<p>{esc(item["observed"])}</p><p><b>{esc(item["author_judgment"])}</b></p><p class="note"><a href="{esc(item["file"])}">原图</a> · <a href="{esc(item["prompt"])}">实际提示词</a></p></article>'
content = intro + '<h2 id="head-options">先比较主冠位置与体量</h2><div class="grid">' + cards + '</div>'
content += '''<p class="note">四张镜位和面甲局部有少量漂移，供选方向，不是同模型精确投影。耳侧的小天线仍有上翘幅度，主冠选定后将统一为此前要求的直线后向；当前耳侧细节尚不固定。</p><h2 id="body">无牌与王者：共享结构，保留角色层级</h2><p>王者是旧系列的钦定主角机，保留更臃肿的全装、华丽冠饰和过度武装。无牌是同系列量产基础体，本作的重要角色；以利落的身体、简洁胸甲和拳技姿态显出自己的力量。</p><div class="pair">'''
content += figure(body['file'], 'R13颈下候选：长腿、小头、金色打击护轨；头冠已被要求继续修改', 900)
content += figure('samples/M05-full-loadout-r1b.png', '王者：豪华全装备的同系列对照；该新样例尚未单独确认', 900)
content += '''</div><div class="scroll"><table><thead><tr><th>共同家族</th><th>无牌</th><th>完全版王者</th></tr></thead><tbody><tr><td>胸甲与凹入散热口</td><td>朴素中央护甲、少量散热块</td><td>厚甲、冠军饰纹和更多武器挂点</td></tr><tr><td>阶梯肩甲与圆形连接</td><td>轻装肩壳、关节外露，利于体术</td><td>重肩、炮轴、层翼和根部推进器</td></tr><tr><td>四肢倒角与关节</td><td>长腿紧凑靴，双臂打击护轨成为记忆点</td><td>厚甲、右臂钻、左盾及腿侧武器舱</td></tr></tbody></table></div><p class="note">并排用于造型比较，不是工程比例图；无牌16米、王者20米的设定不变。旧企划中的护甲交接关系是胸甲家族相通的现有剧情依据，没有新增剧情。</p>'''
content += '<details><summary>头冠重选前的动作气质草图</summary><p>这张在最新头冠反馈前已发起生成，只用来观察同一基础体的拳线、身体对角和画面分量。头部仍是已要求继续修改的R13，不能据此锁定。拳势也未构成完整动作或命中验证。</p>' + figure('samples/M01-hero-pose-r13.png', '气质草图 · 旧冠待替换，未作为完成版逆转天冲拳', 1000) + '</details>'
content += '<details><summary>为什么退回上一版整机</summary><p>R12大圆头、低颈、短腿和厚鞋叠出了矮钝的机器河童观感，圆护具式胸肩也缺少与王者的同系关系。旧三视图保留作历史，不再作为本轮全身派生依据。</p>' + figure('samples/M01-turnaround-r12b.png', '用户要求整体重做的R12三视图，仅作对照') + '</details>'
content += '''<h2>选定头冠后再固定三视图</h2><p>先按选中的冠型压好体量和侧天线朝向，再补同一头部的正面与侧面；合回颈下候选并检查动作身份，随后重做整机正侧背。当前不在四种未选头型上批量派生。</p><p class="links"><a href="M01-head-position-production-r14.json">四方向来源与逐图意见</a><a href="M01-family-production-r13.json">整机与动作来源</a><a href="M01-head-position-direction-r14.json">用户最新头冠要求</a><a href="M01-M05-series-direction-20261019.json">两机家族与角色层级</a><a href="M01-family-and-head-prompts-r13-r14.json">本批实际提示词</a></p><p class="note">内置 image_gen 制作。新图尚未获用户选定，未替换游戏运行或发送本批新图交接。馆守Z沿用现有；社勇王与六名人物固定29文件保持。</p>'''
if (OUT/'M01-synthesis-head-production-r15.json').exists():
    synthesis=json.loads((OUT/'M01-synthesis-head-production-r15.json').read_text())
    latest='''<section id="synthesis-r15"><p class="tag">2026.10.19 · 当前综合样例R15</p><h1>低额块、方正盔体与高位侧后双天线</h1><div class="notice"><p>按用户“考虑一下天威勇士和擎天柱的头型综合”，先以倍功夫/Baikanfu和经典G1擎天柱作具体取样，重新组织无牌头部。</p><p>中央长冠脊改为低额块，主天线移到上颞部偏后；无牌的青白金、琥珀视窗与封闭面甲保持。本张是新候选，尚未确认。</p></div>'''
    latest+=figure(synthesis['file'],'R15综合新稿 · 两侧主天线、低中央额块与方正盔体',930)
    latest+='''<div class="scroll"><table><thead><tr><th>实际参考</th><th>本次取的结构</th><th>转成无牌的表达</th></tr></thead><tbody><tr><td><a href="https://tamashiiweb.com/item/12128/">Bandai官方Baikanfu图</a></td><td>作者观察：收紧的眉额与脸框、高位侧后天线的结构关系。</td><td>低额块、干练眉沿、贴近面甲的颊框。</td></tr><tr><td><a href="https://www.hasbropulse.com/product/transformers-retro-g1-optimus-prime/G01535L00">Hasbro官方经典擎天柱图</a></td><td>作者观察：方正盔体、抬高的颞侧壳与闭合面罩轮廓。</td><td>更平的盔顶、上颞侧块与成对直线主天线。</td></tr><tr><td>当前M01与M05项目源稿</td><td>无牌脸部/色系，王者的同系列装甲折面。</td><td>青白金、连续琥珀视窗、白面甲和同系颈下保持。</td></tr></tbody></table></div><details><summary>实际使用的官方参考原图</summary><div class="pair">'''
    latest+=figure('refs/M01-r15-baikanfu-official-detail.jpg','Bandai商品原图 · 本次只参考头部',600)
    latest+=figure('refs/M01-r15-optimus-official-2.jpg','Hasbro商品原图 · 本次只参考头部',600)
    latest+='''</div><p class="note">具体取样版本由作者先作理解；用户只提出两个头型的综合方向，并未指定某款商品。</p></details><p>新稿已移除中轴长条冠脊；两根主天线都有可辨根部，盔顶及侧块更方正。天线长度、后倾角和前后根位仍需选定后在同一头部模型中校核；本张不替代正侧背投影。</p><p class="links"><a href="samples/M01-synthesis-head-r15.png">新稿原图</a><a href="M01-synthesis-head-prompt-r15.json">内置生图实际提示词</a><a href="M01-synthesis-head-production-r15.json">来源与作者观察</a><a href="M01-synthesis-reference-sources-r15.json">官方参考来源绑定</a></p></section>'''
    content=latest+'<details><summary>此前R14四方向、R13整机与家族对照（均未由用户选定）</summary>'+content+'</details>'
if (OUT/'M01-head-proportion-production-r16.json').exists():
    proportion=json.loads((OUT/'M01-head-proportion-production-r16.json').read_text())
    history=content.replace('id="synthesis-r15"','id="synthesis-r15-history"')
    latest='''<section id="head-proportion-r16"><span id="synthesis-r15"></span><p class="tag">2026.10.19 · 当前头部比例修正R16</p><h1>补回头壳本体的纵向体积</h1><div class="notice"><p>用户表示综合方向看着还行，同时指出头部反复被压扁。此前作者把“小头、克制”落实成了低盔顶和宽耳甲，导致头壳矮宽。</p><p>本次保持综合结构，只修头壳的高宽、额部/颞侧/下颌体积，收紧侧部；当前新稿尚待用户看稿。</p></div>'''
    latest+=figure(proportion['file'],'R16局部比例修正 · 综合结构与配色保留',1030)
    latest+='<details><summary>修正前后：比较头壳，不把天线算进头高</summary><div class="pair">'
    latest+=figure('samples/M01-synthesis-head-r15.png','R15原稿 · 用户指出头被压扁',700)
    latest+=figure(proportion['file'],'R16修正 · 头壳更竖向、颞侧收紧',700)
    latest+='''</div><p>比较下颌至真实盔顶的高度，以及耳甲外缘之间的宽度。两张都是原始比例显示，没有拉伸原图；裁切与镜位仍有差别，不能当作同模型正投影。</p></details><p>低中央额块、高位侧后双天线、连续琥珀视窗、白面甲和青白金保持。后续“小头”通过头部相对身体整体缩小实现，保留头壳自身的正常纵向比例。</p><p class="links"><a href="samples/M01-head-proportion-r16.png">修正稿原图</a><a href="M01-head-proportion-prompt-r16.json">内置生图实际提示词</a><a href="M01-head-proportion-production-r16.json">来源与实际对比</a><a href="M01-head-proportion-direction-r16.json">用户反馈与修正范围</a></p></section>'''
    if proportion.get('user_accepted'):
        latest=latest.replace('当前头部比例修正R16','当前已确认头部R16').replace('本次保持综合结构，只修头壳的高宽、额部/颞侧/下颌体积，收紧侧部；当前新稿尚待用户看稿。','用户最新明确“这个我觉得可以了”，当前R16头部源设计固定：保留正常纵向头壳体积、低额块、侧后双天线、琥珀视窗及白面甲。下一步先合回R13颈下，再检查整机比例和多视图。').replace('R16局部比例修正 · 综合结构与配色保留','R16头部源设计已确认 · 整机、模型与运行分别验证')
        latest+='<p><a href="mecha-source-decisions-20261019-r17.json">本次认可及具体来源</a> · <a href="M05-style-match-r2.html">王者画法统一样例与新旧对照</a>。旧拳王沿当前样例继续；无牌R13全身图的旧头型不得回流。</p>'
    content=latest+'<details><summary>此前综合结构、参考拆解与头冠探索</summary>'+history+'</details>'
doc = f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>无牌｜综合头型与头部比例修正</title><style>{css}</style></head><body><main>{content}</main></body></html>\n'
(OUT / 'M01-family-head-review-r14.html').write_text(doc)

# Current phase replaces only M01's own phase; all frozen and next-batch sections stay.
p = OUT / 'design-followthrough-section.html'
s = p.read_text()
start = s.index('<div class="phase" id="next-design-m01-')
end = s.index('<div class="phase" id="next-mecha-batch-20261019">', start)
anchors = ''.join(f'<span id="next-design-m01-r{x}"></span>' for x in range(4, 14))
thumbs = ''.join(f'<figure class="direction-ref"><a href="M01-family-head-review-r14.html#head-{x["id"]}"><img src="{x["file"]}" alt="无牌方向{x["id"]}：{x["title"]}" style="height:390px;object-fit:contain"></a><figcaption>{x["id"]} · {x["title"]}</figcaption></figure>' for x in heads['items'])
phase = f'''<div class="phase" id="next-design-m01-r14">{anchors}<p class="kicker">当前R14 / 头冠位置重新探索</p><h3>无牌要有同系量产身份，也要有闪光时的主角感</h3><p>R12矮圆整机已被用户要求重做。R13拉开头身与腿长、统一王者家族胸肩，但头顶天线仍需修改，现已画出四种主冠位置。作者优先D，B为压短后的备选；尚未替用户选定。</p><div class="direction-refs two">{thumbs}</div><p><a href="M01-family-head-review-r14.html"><b>看四方向大图、逐图意见及同系列整机对照 →</b></a> · <a href="M01-family-and-head-prompts-r13-r14.json">实际提示词</a></p><p>选主冠后再统一侧天线、头部多视图及整机。馆守沿用现有；社勇王与人物固定源图保持。</p></div>\n'''
if (OUT/'M01-synthesis-head-production-r15.json').exists():
    older_phase=phase.replace(anchors,'').replace('id="next-design-m01-r14"','id="head-options-r14-history"')
    new_anchors=''.join(f'<span id="next-design-m01-r{x}"></span>' for x in range(4,15))
    phase=f'''<div class="phase" id="next-design-m01-r15">{new_anchors}<p class="kicker">当前R15 / 天威勇士与擎天柱结构综合</p><h3>中央低额块，高位侧后双天线，收紧方正盔体</h3><p>按最新参考方向，以倍功夫/Baikanfu和经典G1擎天柱的头部结构重新综合；保持无牌青白金、琥珀视窗、白面甲与王者同系颈下。</p><figure class="scene"><a href="M01-family-head-review-r14.html#synthesis-r15"><img src="samples/M01-synthesis-head-r15.png" alt="无牌R15综合头部：低额块、方正盔体和高位侧后双天线" style="max-height:850px;object-fit:contain"></a><figcaption>综合新稿R15 · 尚待用户看稿</figcaption></figure><p><a href="M01-family-head-review-r14.html#synthesis-r15"><b>看大图、参考拆解与实际来源 →</b></a> · <a href="M01-synthesis-head-prompt-r15.json">实际提示词</a></p><p>天线长度/倾角及前后根位仍需选定后固定；当前不把新图当作已认可的头型或运行资产。</p></div><details><summary>此前R14四种头冠探索</summary>{older_phase}</details>\n'''
if (OUT/'M01-head-proportion-production-r16.json').exists():
    for x in range(4,15):phase=phase.replace(f'<span id="next-design-m01-r{x}"></span>','')
    old_phase=phase.replace('id="next-design-m01-r15"','id="head-synthesis-r15-history"')
    new_anchors=''.join(f'<span id="next-design-m01-r{x}"></span>' for x in range(4,16))
    phase=f'''<div class="phase" id="next-design-m01-r16">{new_anchors}<p class="kicker">当前R16 / 保留综合结构，只修头部纵向比例</p><h3>头壳恢复纵向体积，耳甲与眉沿收紧</h3><p>用户认为综合方向还行，同时指出头被压扁。此前作者用低盔顶和宽侧部处理“小头”，本次修正这个比例方法，保留低额块、侧后双天线及无牌脸部/色系。</p><figure class="scene"><a href="M01-family-head-review-r14.html#head-proportion-r16"><img src="samples/M01-head-proportion-r16.png" alt="无牌R16头部比例修正，恢复头壳纵向体积并收紧颞侧" style="max-height:900px;object-fit:contain"></a><figcaption>局部修正R16 · 新图尚待用户看稿</figcaption></figure><p><a href="M01-family-head-review-r14.html#head-proportion-r16"><b>看原图与修正前后对照 →</b></a> · <a href="M01-head-proportion-prompt-r16.json">实际提示词</a></p></div><details><summary>此前R15综合结构与R14头冠探索</summary>{old_phase}</details>\n'''
if (OUT/'mecha-source-decisions-20261019-r17.json').exists():
    phase=phase.replace('当前R16 / 保留综合结构，只修头部纵向比例','当前R16 / 头部源设计已确认').replace('局部修正R16 · 新图尚待用户看稿','R16头部已确认 · 先合回颈下再补视图')
    phase=phase.replace('用户认为综合方向还行，同时指出头被压扁。此前作者用低盔顶和宽侧部处理“小头”，本次修正这个比例方法，保留低额块、侧后双天线及无牌脸部/色系。','用户最新确认当前R16可以。头壳纵向体积、低额块、侧后双天线及无牌脸部/色系固定；先合回R13颈下并检查整机，不再重选头型或沿R13旧头派生。')
p.write_text(s[:start] + phase + s[end:])

# Stable old head entry now shows the current choice first and folds dated R11 history.
p = OUT / 'M01-head-AE-r6.html'
s = p.read_text()
if all(f'id="current-head-r{x}"' not in s for x in [14,15,16]):
    start = s.index('<main>') + len('<main>')
    end = s.rindex('</main>')
    old = s[start:end]
    new = '<div id="current-head-r14"><p class="tag">2026.10.19 · 最新：头冠位置重新探索R14</p><h1>改找克制但偏主角感的头冠</h1><div class="notice"><p>用户认为R13头顶天线的位置仍不理想；旧长双槽冠脊形态重新开放。已画四种位置，作者建议D、B备选，尚未选定。</p><p><a href="M01-family-head-review-r14.html"><b>打开四方向与同系列整机对照 →</b></a></p></div></div>'
    s = s[:start] + new + '<details><summary>此前R11局部确认及修正历史（当前主冠位置已重新开放）</summary>' + old + '</details>' + s[end:]
    p.write_text(s)
if (OUT/'M01-synthesis-head-production-r15.json').exists():
    start=s.index('<main>')+len('<main>')
    end=s.index('<details><summary>此前R11局部确认',start)
    new='''<div id="current-head-r15"><p class="tag">2026.10.19 · 当前综合头型R15</p><h1>天威勇士与擎天柱的结构综合</h1><div class="notice"><p>新稿采用中央低额块、方正盔体与高位侧后双天线，保留无牌青白金及连续琥珀视窗。具体新图尚未确认。</p><p><a href="M01-family-head-review-r14.html#synthesis-r15"><b>打开综合新稿及两组实际参考 →</b></a></p></div></div>'''
    s=s[:start]+new+s[end:]
    p.write_text(s)
if (OUT/'M01-head-proportion-production-r16.json').exists():
    start=s.index('<main>')+len('<main>')
    end=s.index('<details><summary>此前R11局部确认',start)
    new='''<div id="current-head-r16"><p class="tag">2026.10.19 · 当前头部比例修正R16</p><h1>综合方向保留，补回正常头高</h1><div class="notice"><p>用户指出头部被压扁。已只修头壳纵向体积和侧部展宽，低额块、双侧后位天线、琥珀视窗及青白金保持；新修正稿尚待看稿。</p><p><a href="M01-family-head-review-r14.html#head-proportion-r16"><b>打开新稿与修正前后对照 →</b></a></p></div></div>'''
    if (OUT/'mecha-source-decisions-20261019-r17.json').exists():
        new=new.replace('当前头部比例修正R16','当前已确认头部R16').replace('综合方向保留，补回正常头高','R16头部源设计已确认').replace('用户指出头部被压扁。已只修头壳纵向体积和侧部展宽，低额块、双侧后位天线、琥珀视窗及青白金保持；新修正稿尚待看稿。','用户最新明确当前可以，R16指定头部固定。低额块、侧后双天线、正常头壳比例与琥珀视窗/白面甲保持；整机先合回颈下，再补多视图。')
    s=s[:start]+new+s[end:]
    s=s.replace('无牌｜白色中脊与双侧黄槽 R11','无牌｜综合头型与头部比例修正')
    p.write_text(s)
p = OUT / 'M01-turnaround-r12.html'
s = p.read_text()
if 'id="r12-rework-notice"' not in s:
    s = s.replace('<h1>', '<div class="notice" id="r12-rework-notice"><p><b>本整机版已被用户要求重做：</b>矮圆、机器河童观感及与王者不同系列。<a href="M01-family-head-review-r14.html">当前R13身体候选与R14头冠四方向在此 →</a></p></div><h1>历史稿：', 1)
    p.write_text(s)
print('Published M01 family/head review R14 and updated stable entrypoints.')
