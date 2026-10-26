#!/usr/bin/env python3
"""Publish M11 source designs in the existing art batch reader."""
from pathlib import Path
import html
import json
import re

OUT = Path(__file__).resolve().parent
data = json.loads((OUT / 'M11-cargo-production-r1.json').read_text())
items = {x['id']: x for x in data['items']}
def esc(value):
    return html.escape(str(value), quote=True)
def figure(key, caption):
    file = esc(items[key]['file'])
    return '<figure><a href="' + file + '"><img src="' + file + '" alt="' + esc(caption) + '"></a><figcaption>' + esc(caption) + '</figcaption></figure>'

css = '''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f3f0e8;color:#233746;font:17px/1.8 system-ui,-apple-system,sans-serif}main{max-width:2100px;margin:auto;padding:32px 24px 70px}a{color:#316780;text-underline-offset:3px}nav,.links{display:flex;gap:10px 24px;flex-wrap:wrap}.tag{color:#a95619;font-size:14px;font-weight:700}h1{font-size:38px;line-height:1.35}h2{font-size:28px;margin-top:45px}.intro{max-width:1180px}.approved{border-left:4px solid #47745d;background:#e5e9dc;padding:14px 20px;font-size:15px}.views{display:flex;gap:16px;align-items:start;overflow-x:auto;padding-bottom:15px;scroll-snap-type:x proximity}.views figure{flex:0 0 auto;scroll-snap-align:start}.views img{height:900px;width:auto;max-width:none}figure{margin:18px 0;padding:12px;background:white;border-radius:8px}img{display:block;max-width:100%;height:auto}figcaption{font-size:15px;text-align:center;margin-top:10px}.vehicle{max-width:1650px}table{border-collapse:collapse;width:100%;max-width:1250px;background:#fff;font-size:16px}th,td{text-align:left;border-bottom:1px solid #d6dcd8;padding:14px 18px;vertical-align:top}th{background:#21384b;color:#fff}.table-wrap{overflow-x:auto}.note,details{font-size:14px;color:#52626a}details{padding:20px;margin-top:30px;background:#e4e8e3;border-radius:8px}summary{cursor:pointer;font-weight:650}.source-ref{max-width:950px}.source-ref img{max-height:600px;object-fit:contain}button{font:inherit;cursor:pointer;padding:8px 14px;border:1px solid #8095a0;border-radius:6px;background:white;color:#233746}.controls{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}.views.single{display:block}.views.single figure{max-width:900px}.views.single figure[hidden]{display:none}.views.single img{max-width:100%;height:auto;width:auto;max-height:1200px}@media(max-width:700px){main{padding:22px 12px}h1{font-size:29px}.views img{height:720px}th,td{padding:11px 13px}}'''
body = '<nav><a href="index.html#cargo-leader-r1">素材总入口</a><a href="#robot">机器人三面</a><a href="#vehicle">四轴货车</a><a href="#parts">部件对应</a><a href="#sources">原头部来源</a></nav>'
body += '<p class="tag">2026.10.21 · 下一批 / 货柜领袖 R1</p><h1>同一副四轴底盘，同一台货柜领袖</h1><p class="intro">沿已确定的额头摄像头、青色双眼与分节面甲，统一白甲、藏蓝车架和安全橙角锁。机器人保留完整大腿与长胫甲；车形使用一副四轴刚性底盘，货柜作为独立载荷卸下后再展开。</p>'
body += '<p class="approved">上一批已按用户意见固定：<a href="M02-turnaround-r2.html">旧拳王三面</a> · <a href="M05-turnaround-r12.html">王者素体／全装／双状态头部</a>。<a href="mecha-source-batch-acceptance-20261021.json">查看本次采用范围</a>。</p>'
body += '<h2 id="robot">机器人：正、侧、背</h2><p class="intro">风挡收到肩上，格栅成为胸板，货台收为浅背架。每侧四个公路轮位：肩后一个、前臂外后一个、小腿外后两个；小踝轴盖单独辨认。点开图片可看原尺寸。</p><div class="controls"><button type="button" data-view="all">三面并排</button><button type="button" data-view="FRONT">只看正面</button><button type="button" data-view="SIDE">只看左侧</button><button type="button" data-view="REAR">只看背面</button></div><div class="views" id="robot-views">'
for key, caption in [('FRONT', '正面 · 驾驶室格栅胸与风挡肩壳'), ('SIDE', '左侧 · 每侧四个公路轮位'), ('REAR', '背面 · 侧置轮胎胎面与折叠货台')]:
    body += figure(key, caption).replace('<figure>', '<figure data-key="' + key + '">', 1)
body += '</div><h2 id="vehicle">车形：四轴载柜货车</h2><div class="vehicle">' + figure('VEHICLE', '单副刚性底盘 · 四轴 · 一个可卸货柜') + '</div>'
body += '<h2 id="parts">两种形态的部件对应</h2><div class="table-wrap"><table><thead><tr><th>部件</th><th>货车形态</th><th>机器人形态</th></tr></thead><tbody>'
for row in data['parts_mapping']:
    body += '<tr>' + ''.join('<td>' + esc(row[k]) + '</td>' for k in ['part', 'vehicle', 'robot']) + '</tr>'
body += '</tbody></table></div><p class="note">这是本批的结构提案。铰链路径、零件净空和连续变形将随同模型制作核对。</p>'
body += '<h2 id="sources">头部身份沿现有 v4</h2><div class="source-ref"><a href="../../../../.superpowers/brainstorm/37837-1782033239/content/mecha_r18_cargo_leader_face_v4.png"><img src="../../../../.superpowers/brainstorm/37837-1782033239/content/mecha_r18_cargo_leader_face_v4.png" alt="货柜领袖既有v4头部来源"></a></div><p class="intro">保留上方原头部的中央橙框摄像头、分离双眼、分节面甲与短横向颞鳍。旧来源下方的整车和身体用于追溯，本轮四张新稿见上方。</p>'
body += '<details><summary>源稿检查与制作记录</summary><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in data['author_review']['observed']) + '</ul><p>' + esc(' '.join(data['author_review']['limits'])) + '</p><p class="links"><a href="M11-cargo-production-r1.json">图稿与部件记录</a><a href="M11-cargo-prompts-r1.json">实际提示词组</a><a href="M11-cargo-verification-r1.json">文件与来源核对</a><a href="design-followthrough-r1.json">原批次记录</a></p><p>使用内置 image_gen。当前四张为新源设计稿，等待本轮看稿。</p></details>'
if (OUT / 'M11-future-production-r2.json').exists():
    body=body.replace('<p class="tag">','<p class="approved"><a href="M11-future-r2.html">查看最新R2：未来车形、对应人形与无水平天线头部 →</a>。本页R1保留历史，旧侧背不作为R2当前几何。</p><p class="tag">',1)
    body=body.replace('2026.10.21 · 下一批 / 货柜领袖 R1','2026.10.21 · 历史 / 货柜领袖 R1')
script = '''document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{const key=button.dataset.view;const group=document.getElementById('robot-views');group.classList.toggle('single',key!=='all');group.querySelectorAll('figure').forEach(figure=>{figure.hidden=key!=='all'&&figure.dataset.key!==key;});document.querySelectorAll('[data-view]').forEach(other=>other.setAttribute('aria-pressed',String(other===button)));}));'''
(OUT / 'M11-cargo-r1.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>货柜领袖｜四轴双形态与三面源稿</title><style>' + css + '</style></head><body><main>' + body + '</main><script>' + script + '</script></body></html>\n')

# Place the current source batch in the existing shared reader section.
page = OUT / 'design-followthrough-section.html'
s = page.read_text()
phase = '<div class="phase" id="cargo-leader-r1"><p class="kicker">2026.10.21 / 下一批 · 货柜领袖</p><h3>四轴双形态，机器人正侧背</h3><p>沿固定v4头脸统一白蓝橙货运躯体，核对每侧四轮位、驾驶室与独立货柜。旧拳王和王者上一批源稿已按本次意见固定。</p><figure class="scene"><a href="M11-cargo-r1.html"><img src="' + items['VEHICLE']['file'] + '" alt="货柜领袖当前四轴货车源稿"></a><figcaption>同一底盘 · 单个独立货柜</figcaption></figure><p><a href="M11-cargo-r1.html">打开双形态与三面图 →</a> · <a href="M11-cargo-prompts-r1.json">提示词组</a> · <a href="mecha-source-batch-acceptance-20261021.json">上一批采用范围</a></p></div>\n'
if (OUT / 'M11-future-production-r2.json').exists():
    phase=phase.replace('2026.10.21 / 下一批 · 货柜领袖','2026.10.21 / 历史R1 · 货柜领袖').replace('<h3>四轴双形态，机器人正侧背</h3>','<h3>R1历史：四轴底盘与独立货柜</h3>').replace('打开双形态与三面图 →','查看R1历史结构 →')
if 'id="cargo-leader-r1"' in s:
    s = re.sub(r'<div class="phase" id="cargo-leader-r1">.*?</div>\s*', lambda _: phase, s, count=1, flags=re.S)
else:
    anchor = '<div class="phase" id="old-boxer-turnaround-r2">'
    assert anchor in s
    s = s.replace(anchor, phase + anchor, 1)
page.write_text(s)
print('Published M11 current source reader and existing-batch entry.')
