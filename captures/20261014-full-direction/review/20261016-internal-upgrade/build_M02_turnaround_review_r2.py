#!/usr/bin/env python3
"""Publish Old Boxer's three source views in the existing review batch."""
from pathlib import Path
import html
import json
import re

OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'M02-turnaround-production-r2.json').read_text())
items={x['id']:x for x in data['items']}
def esc(x):return html.escape(str(x),quote=True)
def figure(file,caption):
    return '<figure><a href="'+esc(file)+'"><img src="'+esc(file)+'" alt="'+esc(caption)+'"></a><figcaption>'+esc(caption)+'</figcaption></figure>'
css='''*{box-sizing:border-box}body{margin:0;background:#f4f1e8;color:#38352f;font:17px/1.8 system-ui,-apple-system,sans-serif}main{max-width:2100px;margin:auto;padding:30px 24px 65px}a{color:#806044;text-underline-offset:3px}nav,.links{display:flex;gap:12px 25px;flex-wrap:wrap}h1{font-size:36px;line-height:1.4}.tag{font-size:14px;color:#8d4138;font-weight:700}.intro{max-width:1150px}.three{display:flex;align-items:start;gap:16px;overflow-x:auto;padding-bottom:18px;scroll-snap-type:x proximity}.three figure{flex:0 0 auto;scroll-snap-align:start}.three img{height:900px;width:auto;max-width:none}figure{margin:18px 0;padding:12px;background:white;border-radius:8px}img{display:block;max-width:100%;height:auto}figcaption{text-align:center;font-size:15px;margin-top:10px}.source{max-width:850px}.note,details{font-size:14px;color:#6a665c}details{padding:20px;margin-top:28px;background:#eae6dd;border-radius:8px}summary{cursor:pointer;font-weight:650}@media(max-width:700px){main{padding:22px 12px}h1{font-size:28px}.three img{height:720px}}'''
body='<nav><a href="index.html#old-boxer-turnaround-r2">升级总页</a><a href="#views">三视对照</a><a href="#source">沿用母稿</a><a href="M05-turnaround-r12.html">王者三视</a></nav><p class="tag">旧拳王 · 三视设定 R2</p><h1>厚肩、重拳与同一副身体，正侧背对照</h1><p class="intro">沿当前旧拳王母稿补齐观察面：保留象牙白、土棕与深红，短颈重肩、红拳套和完整双腿。先将前探透视姿态展开为站直正面，再按同一身形补左侧与背面。</p><section id="views"><div class="three">'
if data.get('new_images_user_accepted'):
    body=body.replace('<section id="views">','<p class="intro">2026-10-21用户已认可本页当前三张源设计。<a href="mecha-source-batch-acceptance-20261021.json">采用范围</a> · <a href="M11-cargo-r1.html">下一批货柜领袖</a></p><section id="views">',1)
for key,label in [('FRONT','正面'),('SIDE','左侧'),('REAR','背面')]:
    body+=figure(items[key]['file'],label)
body+='</div></section><p class="intro">两只拳套按同一实际体积绘制；右侧棕色腿甲与红护膝、左侧象牙白替换甲保留。三面按原图比例显示，可横向滚动并点开大图。</p><h2 id="source">沿用当前母稿</h2><div class="source">'+figure(data['parent']['file'],'当前旧拳王母稿 · 用户表示沿此方向继续')+'</div>'
body+='<details><summary>本次实际检查与源稿</summary><ul>'+''.join('<li>'+esc(x)+'</li>' for x in data['author_review']['observed'])+'</ul><p>'+esc(' '.join(data['author_review']['limits']))+'</p><p class="links"><a href="M02-turnaround-production-r2.json">源图清单与检查</a><a href="M02-turnaround-prompts-r2.json">实际提示词</a><a href="M02-turnaround-verification-r2.json">来源核对</a><a href="M02-turnaround-direction-r2.json">本次要求</a><a href="mecha-source-decisions-20261019-r17.json">原方向采用范围</a></p><p>内置 image_gen 制作。本轮补绘图仍是源设计稿；同模型投影、动作和游戏运行分别制作验证。</p></details>'
(OUT/'M02-turnaround-r2.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>旧拳王｜正侧背三视图</title><style>'+css+'</style></head><body><main>'+body+'</main></body></html>\n')

page=OUT/'next-batch-mecha-20261019.html'
s=page.read_text()
section='<section id="old-boxer"><h2>旧拳王：正侧背三视 R2</h2><p>当前母稿方向保留，已补站直正面、左侧与背面，保留厚肩红拳套和替换装甲。</p>'+figure(items['FRONT']['file'],'旧拳王正面 · 本批三视源稿')+'<p><a href="M02-turnaround-r2.html"><b>查看旧拳王三视对照 →</b></a></p><details><summary>沿用的母稿</summary>'+figure(data['parent']['file'],'R1旧拳王母稿')+'</details></section>'
s=re.sub(r'<section id="old-boxer">.*?</section>',lambda m:section,s,count=1,flags=re.S)
page.write_text(s)

page=OUT/'design-followthrough-section.html'
s=page.read_text()
phase='<div class="phase" id="old-boxer-turnaround-r2"><p class="kicker">旧拳王 / 正侧背三视 R2</p><h3>沿现有造型，补齐同一身体的三个观察面</h3><p>象牙白、土棕、深红与厚肩红拳套保留；先校准站直正面，再画侧背，保留修补装甲的左右差异。</p><figure class="scene"><a href="M02-turnaround-r2.html"><img src="'+items['FRONT']['file']+'" alt="旧拳王三视的当前正面源稿" style="max-height:1000px;object-fit:contain"></a><figcaption>旧拳王正侧背已补绘</figcaption></figure><p><a href="M02-turnaround-r2.html">打开三视对照 →</a> · <a href="M02-turnaround-prompts-r2.json">实际提示词</a></p></div>\n'
if 'id="old-boxer-turnaround-r2"' in s:
    s=re.sub(r'<div class="phase" id="old-boxer-turnaround-r2">.*?</div>\s*',lambda m:phase,s,count=1,flags=re.S)
else:
    anchor='<div class="phase" id="next-mecha-batch-20261019">'
    assert anchor in s
    s=s.replace(anchor,phase+anchor,1)
page.write_text(s)
print('Published Old Boxer front/side/rear and existing-batch entry.')
