#!/usr/bin/env python3
"""Publish King core, full-equipment and two-state head turnarounds."""
from pathlib import Path
import html
import json

OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'M05-turnaround-production-r10.json').read_text())
items={item['id']:item for item in data['items']}
def esc(value):return html.escape(str(value),quote=True)
def figure(item,caption):
    file=esc(item['file'])
    return '<figure><a href="'+file+'"><img src="'+file+'" alt="'+esc(caption)+'"></a><figcaption>'+esc(caption)+'</figcaption></figure>'

css='''*{box-sizing:border-box}body{margin:0;background:#f4f1e8;color:#253940;font:17px/1.8 system-ui,-apple-system,sans-serif}main{max-width:2300px;margin:auto;padding:30px 26px 70px}nav,.links{display:flex;gap:12px 26px;flex-wrap:wrap}a{color:#246b70;text-underline-offset:3px}h1{font-size:36px;line-height:1.4}h2{font-size:28px;margin-top:48px}.tag{font-size:14px;color:#7e5827;font-weight:700}figure{margin:20px 0;padding:12px;background:#fffdf8;border-radius:8px}img{display:block;width:100%;height:auto;max-height:1250px;object-fit:contain}figcaption{text-align:center;margin-top:12px;font-size:15px}.note{font-size:14px;color:#5d7169}details{margin:35px 0;padding:20px;background:#e9ece3;border-radius:8px}summary{cursor:pointer;font-weight:650}.text{max-width:1300px}@media(max-width:750px){main{padding:22px 12px}h1{font-size:28px}figure{padding:4px}}'''
body='''<nav><a href="index.html#king-modular-r4">升级总页</a><a href="#full">全装</a><a href="#core">素体</a><a href="#head">两状态头部</a><a href="M05-battle-mask-r8.html#deployment">面罩转换</a></nav><p class="tag">王者 · 三视设定 R10</p><h1>同一台王者，素体、全装与头部正侧背对照</h1><p class="text">沿已采用的藏蓝白红金机体、金色五构件皇冠与红色中线鳍展开。整机每组从左到右为正面、左侧、背面；素体使用普通脸，全装使用闭合战斗面罩。</p><h2 id="full">全装：右钻、左盾、双炮与四个腿侧弹仓</h2>'''
body+=figure(items['FULL'],'全装正面 / 左侧 / 背面 · 战斗面罩闭合')
body+='''<p class="text">正面显示炮口与盾面，背面显示炮尾和盾内挂架。右臂钻在正面画面左侧、背面画面右侧；两侧翼组与低位推进舱沿同一套外挂展开。</p><h2 id="core">素体：保留完整双手与基础身体</h2>'''
body+=figure(items['CORE'],'素体正面 / 左侧 / 背面 · 普通脸与同一红色头鳍')
body+='''<p class="text">卸去钻盾、炮翼和腿侧弹仓后，保留同一头胸、基础肩甲、身体比例和金色圆关节。背部露出基础承载结构与挂点。</p><h2 id="head">头部：普通脸与战斗面罩共用头盔</h2>'''
body+=figure(items['HEAD'],'上排普通脸、下排战斗面罩；每排为正面 / 左侧 / 背面')
body+='''<p class="text">红鳍在侧面展开三角鳍面，在正面被金色中角遮住；背面只见薄鳍边缘，后方仍有更高的金色中角。面罩开合不改变头盔后壳、皇冠与耳罩。</p><details><summary>本次实际检查与仍需收敛的结构</summary>'''
body+='<ul>'+''.join('<li>'+esc(x)+'</li>' for x in data['author_review']['observed'])+'</ul>'
body+='<p>'+' '.join(esc(x) for x in data['author_review']['limits'])+'</p>'
body+='''<p class="links"><a href="M05-red-fin-design-fixed-and-turnaround-r10.json">本次源图采用与三视授权</a><a href="M05-turnaround-production-r10.json">源稿与实际检查</a><a href="M05-turnaround-prompts-r10.json">全部实际提示词</a><a href="M05-turnaround-verification-r10.json">来源核对</a><a href="M05-modular-r4.html#packages">配件分组来源</a><a href="M05-battle-mask-r8.html">此前头部与转换示意</a></p><p>内置 image_gen 制作。新三视稿用于继续核对结构，尚不是同一模型的精确投影；背面隐藏结构、装卸让位与运行分别验证。接续原美术批次，未自动发送交接。</p></details>'''
(OUT/'M05-turnaround-r10.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>王者｜素体、全装与双状态头部三视图</title><style>'+css+'</style></head><body><main>'+body+'</main></body></html>\n')
print('Published King core/full/head three-view reader.')
