#!/usr/bin/env python3
"""Build the two source-art readers from the existing batch records."""
from pathlib import Path
import html
import json

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parents[3]


def esc(value):
    return html.escape(str(value), quote=True)


def read(name):
    return json.loads((OUT / name).read_text())


def figure(file, caption, *, cls=""):
    return f'<figure class="{cls}"><a href="{esc(file)}"><img src="{esc(file)}" alt="{esc(caption)}" loading="lazy"></a><figcaption>{caption}</figcaption></figure>'


CSS = """
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f4f1e8;color:#24363d;font:17px/1.75 system-ui,-apple-system,sans-serif}main{max-width:1450px;margin:auto;padding:42px 28px 70px}a{color:#226b70;text-underline-offset:3px}nav{display:flex;flex-wrap:wrap;gap:12px 24px}h1{font-size:38px;line-height:1.3;margin:22px 0}h2{font-size:29px;margin-top:48px}h3{font-size:22px}.kicker{font-size:14px;font-weight:750;letter-spacing:.09em;color:#246b6c}.notice{background:#fffdf7;border-left:5px solid #be8a36;padding:16px 24px;margin:24px 0}.notice p{margin:4px 0}.note{font-size:14px;color:#63716b}figure{margin:22px 0;background:#e0e5dd;padding:18px;border-radius:9px}figure img{display:block;width:100%;height:auto;max-height:1050px;object-fit:contain}figcaption{margin-top:14px;text-align:center;font-weight:650}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}.pair figure{margin:0}.pair img{height:400px}.source img{height:350px}.art img{min-height:450px}.scroll{overflow-x:auto}table{width:100%;border-collapse:collapse}th,td{border-bottom:1px solid #c9d2c9;padding:13px;text-align:left;vertical-align:top}th{white-space:nowrap}details{margin:24px 0;padding:16px;background:#ebece4;border-radius:7px}summary{font-weight:650;cursor:pointer}.links{display:flex;flex-wrap:wrap;gap:10px 24px}.card{margin:34px 0 54px;padding-top:12px;border-top:2px solid #c1cec4}@media(max-width:750px){main{padding:24px 16px}h1{font-size:29px}h2{font-size:25px}.pair{grid-template-columns:1fr}.pair img{height:auto;max-height:650px}.art img{min-height:0}figure{padding:10px}table{font-size:14px}}
"""


def page(title, body):
    return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{CSS}</style></head><body><main>{body}</main></body></html>\n'


m01 = read("M01-turnaround-production-r12.json")
body = '''<nav><a href="index.html#next-design-m01-r12">升级总页</a><a href="M01-head-AE-r6.html">已确认头部</a><a href="next-batch-mecha-20261019.html">下一批：旧拳王与王者</a></nav>
<p class="kicker">2026.10.19 · 无牌一号 · 整机三视图 R12b</p><h1>把已确认头部补回同一台无牌</h1>
<div class="notice"><p><b>头部设计已确认。</b>按本次“补上无牌三视图”的要求，沿现有颈下机体完成正、侧、背面。新整机图供本轮看稿。</p><p>馆守Z继续沿用现有资产；社勇王与人物固定批次保持。</p></div>
'''
body += figure(m01["file"], "正面 / 朝左侧面 / 背面 · 三视图源稿", cls="art")
body += '''<h2>本次统一的部位</h2><div class="scroll"><table><thead><tr><th>部位</th><th>当前表达</th><th>派生时保持</th></tr></thead><tbody>
<tr><td>头冠与侧天线</td><td>前视两道黄槽，中间为白色实体；侧视近侧槽可见。两侧天线直线后收。</td><td>背面是后脑与颈后结构；不把眼窗、面罩或额部小黄块转到后脑。</td></tr>
<tr><td>胸肩与腰</td><td>象牙白胸桥、青绿胸壳、左胸扣与金色斜撑；腰部留出转动空间。</td><td>同一套肩甲厚度与胸壳体积，保持竞技体术轮廓。</td></tr>
<tr><td>前臂与拳</td><td>金色打击护轨、紧凑拳套和可辨腕口。</td><td>金色护轨是前臂构件；不另加手持武器，也不放大成社勇王巨拳。</td></tr>
<tr><td>腿与鞋</td><td>前侧胫甲与后侧小腿分开；背面显示后膝、跟腱和鞋跟。</td><td>侧视用同一前后厚度落地，背面不露朝观众的脚尖。</td></tr>
</tbody></table></div>
<p class="note">这是绘制的结构参考，未由同一三维模型输出；隐面厚度、关节活动和模型同位仍需后续校核。源图也尚未做游戏用切边与导入检查。</p>
<h2>已确认的头部依据</h2><div class="pair">'''
body += figure("samples/M01-head-twin-side-grooves-r11.png", "前视R11：双槽与白中脊已确认")
body += figure("samples/M01-head-center-groove-three-quarter-r9b.png", "三分之四母稿：原图保持")
body += '''</div><p><a href="M01-head-design-fixed-20261019.json">本次头部确认范围</a>。此前单中槽解释及错误模型已经废止。</p>
<details><summary>作者检查中发现并修正的背面朝向错误</summary><p>初稿把前脸、前胫甲和脚趾混进背面。本次只修右侧背视，前面及侧面保留。当前背面已经显示后脑、后膝、小腿后甲与鞋跟。</p>'''
body += figure("samples/M01-turnaround-r12-draft-rear-wrong.png", "未选初稿 · 背面朝向错误，仅保留检查记录")
body += '''</details><h2>文件与来源</h2><div class="links"><a href="samples/M01-turnaround-r12b.png">三视图原图</a><a href="M01-turnaround-production-r12.json">来源与部位检查</a><a href="M01-turnaround-prompt-r12.json">整机三视实际提示词</a><a href="M01-turnaround-rear-fix-prompt-r12b.json">背面修正实际提示词</a></div><p class="note">本次使用内置 image_gen 制作。新三视图未代签用户认可，尚未替换游戏运行资源或发送新一批交接。</p>'''
if (OUT/'M01-head-position-production-r14.json').exists():
    body='<div class="notice" id="r12-rework-notice"><p><b>历史R12整机已被用户要求重做：</b>矮圆、机器河童观感及与王者不同系列。<a href="M01-family-head-review-r14.html">当前头部与颈下候选在此 →</a></p></div>'+body
(OUT / "M01-turnaround-r12.html").write_text(page("无牌一号｜历史整机正侧背 R12b", body))

m02 = read("M02-master-production-r1.json")
m05 = read("M05-full-loadout-production-r1.json")
body = '''<nav><a href="index.html#next-mecha-batch-20261019">升级总页</a><a href="M01-turnaround-r12.html">无牌三视图</a><a href="#old-boxer">旧拳王</a><a href="#complete-king">完全版王者</a></nav><p class="kicker">2026.10.19 · 下一批机体源图样例</p><h1>旧拳王的拳重，王者的全装备</h1>
<div class="notice"><p>沿原计划继续两台机体，保持各自身份和色系，用当前KINETIC_CEL画法统一线条、明暗和细节密度。</p><p>这两张是新样例，先看主体方向；确认后再按同一母稿补结构图、三视图和派生资源。</p></div>
<article class="card" id="old-boxer"><p class="kicker">M02 · 旧拳王</p><h2>短颈重肩、厚拳套，保留老拳手的分量</h2><p>沿现有象牙白、土棕和深红配色，保留紧凑头盔、短红额块和厚重拳套。N10只提供拳重与拳击表现参考，头胸仍按M02本身。</p>'''
body += figure(m02["file"], "M02新样例 · 画面前探拳带有透视放大，左右拳真实尺寸不按此差值制作", cls="art")
body += '''<div class="scroll"><table><thead><tr><th>沿用</th><th>本次调整</th><th>下一步</th></tr></thead><tbody><tr><td>旧拳王头胸与色系；完整自主机体身份。</td><td>短颈、宽肩、厚拳与腕部连接；收敛表面碎线和损耗纹理。</td><td>看稿后按同一母稿补无透视三视图，固定拳套厚度、支撑重心与关节活动。</td></tr></tbody></table></div>
<details><summary>实际参考：身份母稿与拳重参考分开</summary><div class="pair source">'''
body += figure(m02["source_refs"][0]["file"], "M02：头胸、身体与配色依据")
body += figure(m02["source_refs"][1]["file"], "N10：只参考拳重，不采用其另一套头胸")
body += '''</div></details><p class="links"><a href="samples/M02-old-boxer-master-r1.png">新样例原图</a><a href="M02-master-prompt-r1.json">实际提示词</a><a href="M02-master-production-r1.json">来源与作者看稿</a></p></article>
<article class="card" id="complete-king"><p class="kicker">M05 · 完全版王者</p><h2>恢复武器密度，让每件装备有清楚的挂点</h2><p>沿最新藏蓝、象牙白、绯红与金色形象，补回多层机械翼、翼根推进器与腿侧发射舱。自身右臂大钻、左臂盾，两门主炮从背肩轴座向前，头胸保持可辨。</p>'''
body += figure(m05["file"], "M05全装备新样例 · 画面左侧是机体自身右臂钻，右侧是自身左臂盾", cls="art")
body += '''<div class="scroll"><table><thead><tr><th>部位</th><th>当前表达</th><th>结构稿继续固定</th></tr></thead><tbody><tr><td>右臂钻 / 左盾</td><td>大钻连接右前臂马达与腕口，白盾接左前臂；腿和胯不长钻。</td><td>腕口、盾握持/挂扣、钻的待机与使用角度。</td></tr><tr><td>两门主炮</td><td>两座圆形俯仰轴，炮体背肩安装、平行前向。</td><td>炮轴上下活动范围，与头冠和翼根让位。</td></tr><tr><td>分层翼与武器舱</td><td>分层机械翼、根部小翼/推进器，腿外侧发射舱。</td><td>翼层分组与折收顺序，避免炮、翼和盾互相穿插。</td></tr><tr><td>头部与盾徽</td><td>保留王者冠饰、封闭面甲和冠军装饰语言。</td><td>在头部放大稿固定冠片数量、额前短冲角及统一盾徽。</td></tr></tbody></table></div>
<details><summary>实际参考：新版主体、F04层翼、原工程装备分量</summary><div class="pair source">'''
body += figure(m05["source_refs"][0]["file"], "最新M05：主体、头部家族与配色依据")
body += figure(m05["source_refs"][1]["file"], "F04：层翼、翼根和背包结构依据")
body += '''</div><p>原工程右臂钻图只参考武器分量、腕部接口与肩炮支撑，未采用旧画法或另一套胸部配色。</p></details>
<details><summary>首稿画幅问题及本次修正</summary><p>首稿上左两片翼尖被裁掉。已保持同一台机体和装备，缩小画面内构图并补尖端。当前外轮廓完整，部分尖端仍较靠边，游戏导出将另留安全边。</p>'''
body += figure("samples/M05-full-loadout-r1-draft-cropped.png", "未选首稿 · 两处上左翼尖裁切")
body += '''</details><p class="links"><a href="samples/M05-full-loadout-r1b.png">全装备样例原图</a><a href="M05-full-loadout-prompt-r1.json">全装备实际提示词</a><a href="M05-full-loadout-framing-prompt-r1b.json">画幅修正实际提示词</a><a href="M05-full-loadout-production-r1.json">来源与作者看稿</a></p></article>
<p>本批接着固定结构与视图，再做同源派生。馆守Z继续沿用现有，社勇王与六名角色的固定源图不随本批变化。</p><p class="note">内置 image_gen 制作；这两张尚未由用户确认。三维模型、运动让位、透明边缘和游戏运行分别检查。新样例暂未发送主玩法对话。</p><p><a href="mecha-batch-prompts-20261019.json">本批完整提示词索引</a> · <a href="index.html#next-mecha-batch-20261019">回原升级计划</a></p>'''
(OUT / "next-batch-mecha-20261019.html").write_text(page("下一批机体｜旧拳王与完全版王者", body))
if (OUT/'M05-style-unification-production-r2.json').exists():
    import runpy
    runpy.run_path(str(OUT/'build_M05_style_review_r2.py'), run_name='__main__')
print(json.dumps({"readers": ["M01-turnaround-r12.html", "next-batch-mecha-20261019.html"]}, ensure_ascii=False))
