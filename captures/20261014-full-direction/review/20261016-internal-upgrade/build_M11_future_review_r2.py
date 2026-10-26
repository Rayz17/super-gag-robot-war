#!/usr/bin/env python3
"""Show M11's future vehicle, matching robot and antenna-free head."""
from pathlib import Path
import html
import json
import re

OUT = Path(__file__).resolve().parent
data = json.loads((OUT / 'M11-future-production-r2.json').read_text())
items = {x['id']: x for x in data['items']}
def esc(value):
    return html.escape(str(value), quote=True)
def fig(file, caption):
    return '<figure><a href="' + esc(file) + '"><img src="' + esc(file) + '" alt="' + esc(caption) + '"></a><figcaption>' + esc(caption) + '</figcaption></figure>'

css = '''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f2f0e9;color:#263e50;font:17px/1.8 system-ui,-apple-system,sans-serif}main{max-width:1800px;margin:auto;padding:32px 24px 70px}a{color:#315e7a;text-underline-offset:3px}nav,.links{display:flex;gap:10px 25px;flex-wrap:wrap}h1{font-size:38px;line-height:1.35}h2{font-size:28px;margin-top:44px}.tag{color:#a85b23;font-size:14px;font-weight:700}.intro{max-width:1140px}.vehicle{max-width:1650px}.robot{max-width:1050px}.head{max-width:1774px}figure{margin:18px 0;padding:12px;background:white;border-radius:8px}img{display:block;width:100%;height:auto}figcaption{font-size:15px;text-align:center;margin-top:10px}.switch{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}button{font:inherit;padding:8px 15px;background:white;color:#263e50;border:1px solid #8298a7;border-radius:6px;cursor:pointer}button[aria-pressed=true]{background:#263e50;color:white}figure[hidden]{display:none}.note,details{font-size:14px;color:#53666f}details{background:#e4e8e3;border-radius:8px;padding:20px;margin:30px 0}summary{font-weight:650;cursor:pointer}.table-wrap{overflow-x:auto}table{border-collapse:collapse;background:#fff;width:100%;max-width:1300px;font-size:16px}th,td{text-align:left;border-bottom:1px solid #d5ddd9;padding:13px 17px;vertical-align:top}th{background:#263e50;color:white}.history{border-left:3px solid #d3ad83;padding-left:15px}@media(max-width:700px){main{padding:22px 12px}h1{font-size:28px}th,td{padding:10px 12px}}'''
body = '<nav><a href="index.html#cargo-leader-future-r2">素材总入口</a><a href="#vehicle">未来车形</a><a href="#robot">对应人形</a><a href="#head">头部近景</a><a href="#parts">部件关系</a></nav><p class="tag">货柜领袖 · 新稿 R2</p><h1>流线电驱车形，对应同一台领袖机体</h1><p class="intro">参考 <a href="https://www.tesla.com/semi">Tesla Semi</a> 的流线驾驶室方向，将大弧面风挡、平滑前罩和包覆侧裙带回人形。保留白甲、藏蓝车架和安全橙；领袖感来自体量与神态，头部取消水平天线。</p>'
body += '<h2 id="vehicle">车形：大弧面风挡与流线前罩</h2><p class="intro">单片风挡、后倾前柱和低位细灯带取代旧方头与大格栅。仍是一副四轴刚性底盘，后方运载一个可卸货柜。</p><div class="switch"><button type="button" data-target="new" aria-pressed="true">新版流线车形</button><button type="button" data-target="old" aria-pressed="false">对照上一版</button></div><div class="vehicle" id="vehicle-compare">'
body += fig(items['VEHICLE']['file'], 'R2 · 流线电驱重载车 / 四轴 / 单个独立货柜').replace('<figure>', '<figure data-state="new">', 1)
body += fig('samples/M11-cargo-truck-r1.png', 'R1历史 · 旧方头与三层格栅，不作为新版车头').replace('<figure>', '<figure data-state="old" hidden>', 1)
body += '</div><h2 id="robot">人形：单片胸窗、前罩胸甲与导流肩壳</h2><p class="intro">整片弧面风挡成为上胸，下方对应车头蓝白前罩和细灯组。肩部改为圆弧导流壳，侧裙板对应前臂与长胫甲；八个轮位按原四轴追认。</p><div class="robot">' + fig(items['ROBOT']['file'], 'R2人形母稿 · 完整长腿与正常头壳体积') + '</div>'
body += '<h2 id="head">头部：去掉横向天线，保留自己的识别点</h2><p class="intro">中央橙框摄像头、青色双眼、银色分节面甲与内嵌竖灯通讯块。两侧不再伸出横杆，也不采用高耸双耳尖；额部保持低短摄像头脊。</p><div class="head">' + fig(items['HEAD']['file'], '同一新头部 · 正面与左侧向近景') + '</div>'
body += '<h2 id="parts">车形与人形的部件关系</h2><div class="table-wrap"><table><thead><tr><th>部件</th><th>车形</th><th>人形</th></tr></thead><tbody>'
for row in data['parts_mapping']:
    body += '<tr>' + ''.join('<td>' + esc(row[k]) + '</td>' for k in ['part', 'vehicle', 'robot']) + '</tr>'
body += '</tbody></table></div><p class="note">本轮先呈现新版车形、人形母稿和头部近景。新机体侧背与连续变形将沿选定造型继续制作，旧R1侧背保留历史。</p>'
body += '<details><summary>本轮检查、参考与提示词</summary><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in data['author_review']['observed']) + '</ul><p>' + esc(' '.join(data['author_review']['limits'])) + '</p><p class="links"><a href="M11-future-production-r2.json">三张源稿与检查记录</a><a href="M11-future-prompts-r2.json">内置生图实际提示词组</a><a href="M11-future-verification-r2.json">文件来源核对</a><a href="M11-future-direction-r2.json">用户本次要求</a><a href="M11-cargo-r1.html">R1历史图稿</a><a href="https://www.tesla.com/sites/default/files/downloads/2022_SEMI_Emergency_Response_Rescue_Sheet_en.pdf">Tesla官方车体辨识图</a></p><p>外形参考不迁移品牌、技术参数或剧情能力。当前三张为新源设计，供本轮看稿。</p></details>'
script = '''document.querySelectorAll('[data-target]').forEach(button=>button.addEventListener('click',()=>{const value=button.dataset.target;document.querySelectorAll('#vehicle-compare figure').forEach(figure=>{figure.hidden=figure.dataset.state!==value;});document.querySelectorAll('[data-target]').forEach(other=>other.setAttribute('aria-pressed',String(other===button)));}));'''
(OUT / 'M11-future-r2.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>货柜领袖｜未来电驱双形态 R2</title><style>' + css + '</style></head><body><main>' + body + '</main><script>' + script + '</script></body></html>\n')

page = OUT / 'design-followthrough-section.html'
s = page.read_text()
phase = '<div class="phase" id="cargo-leader-future-r2"><p class="kicker">货柜领袖 / 未来双形态 R2</p><h3>流线电驱车形，同步人形与无水平天线头部</h3><p>参考Tesla货车方向，改单片弧面风挡、平滑前罩与导流覆壳；人形同步胸肩，头部采用中央摄像头、分节面甲与内嵌通讯块。</p><figure class="scene"><a href="M11-future-r2.html"><img src="' + items['VEHICLE']['file'] + '" alt="货柜领袖R2流线未来四轴货车"></a><figcaption>新版车形、人形母稿与头部近景</figcaption></figure><p><a href="M11-future-r2.html">打开本轮三张新稿 →</a> · <a href="M11-future-prompts-r2.json">实际提示词组</a></p></div>\n'
if 'id="cargo-leader-future-r2"' in s:
    s = re.sub(r'<div class="phase" id="cargo-leader-future-r2">.*?</div>\s*', lambda _: phase, s, count=1, flags=re.S)
else:
    anchor = '<div class="phase" id="cargo-leader-r1">'
    assert anchor in s
    s = s.replace(anchor, phase + anchor, 1)
page.write_text(s)
print('Published M11 future vehicle, robot and head reader in existing batch.')
