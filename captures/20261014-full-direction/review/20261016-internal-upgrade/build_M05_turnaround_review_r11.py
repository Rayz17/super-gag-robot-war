#!/usr/bin/env python3
"""Show individually drawn King views at a common displayed body height."""
from pathlib import Path
import html
import json

OUT = Path(__file__).resolve().parent
data = json.loads((OUT/'M05-turnaround-production-r11.json').read_text())
items = {x['id']: x for x in data['items']}
def esc(x): return html.escape(str(x), quote=True)
def figure(item, caption):
    f = esc(item['file'])
    return '<figure><a href="'+f+'"><img src="'+f+'" alt="'+esc(caption)+'"></a><figcaption>'+esc(caption)+'</figcaption></figure>'
def views(prefix, state):
    return '<div class="three">'+''.join(figure(items[prefix+'_'+key], label+' · '+state) for key,label in [('FRONT','正面'),('SIDE','左侧'),('REAR','背面')])+'</div>'
css = '''*{box-sizing:border-box}body{margin:0;background:#f4f1e8;color:#253940;font:17px/1.8 system-ui,-apple-system,sans-serif}main{max-width:1900px;margin:auto;padding:32px 24px 70px}a{color:#246b70;text-underline-offset:3px}nav,.links{display:flex;gap:12px 25px;flex-wrap:wrap}h1{font-size:36px;line-height:1.4}h2{margin-top:45px;font-size:27px}.tag{font-size:14px;color:#7e5827;font-weight:700}.intro{max-width:1200px}.three{display:flex;gap:16px;overflow-x:auto;align-items:start;padding-bottom:18px;scroll-snap-type:x proximity}.three figure{flex:0 0 auto;scroll-snap-align:start}.three img{height:900px;width:auto;max-width:none}figure{margin:15px 0;background:#fff;padding:10px;border-radius:8px}img{display:block;max-width:100%;height:auto}figcaption{text-align:center;font-size:14px;margin-top:9px}.head{max-width:1500px}.note{font-size:14px;color:#60736b}details{padding:18px;margin:30px 0;background:#e9ece3;border-radius:8px}summary{cursor:pointer;font-weight:650}.compare{display:flex;gap:15px;overflow-x:auto}.compare figure{flex:0 0 auto}.compare img{height:680px;width:auto;max-width:none}@media(max-width:700px){main{padding:22px 12px}h1{font-size:27px}.three img{height:720px}.compare img{height:560px}}'''
body = '<nav><a href="index.html#king-modular-r4">升级总页</a><a href="#full">全装三视</a><a href="#core">素体三视</a><a href="#head">头部两状态</a></nav><p class="tag">王者 · 三视设定 R11</p><h1>恢复原稿身形，再看正、侧、背</h1><p class="intro">沿已采用的藏蓝白红金机体与红鳍头盔，保留完整大腿、长胫甲和正常头部体积。素体与全装分别使用普通脸、闭合战斗面罩。每个视角单独绘制，按原图比例显示；可横向滚动并点开大图。</p>'
body += '<h2 id="full">全装：同一身体，叠上钻、盾、炮与翼</h2>'+views('FULL','战斗面罩闭合')
body += '<p class="intro">正面右钻在画面左侧、左盾在右侧；背面左右随朝向对换。炮口、炮尾与盾面、盾内挂架分别对应。腿侧保留四个外挂弹仓，沿已选整机的三孔开口绘制。</p>'
body += '<h2 id="core">素体：双手与基础身体</h2>'+views('CORE','普通脸')
body += '<p class="intro">裙甲下露出大腿，膝关节、长胫甲和脚踝分开读清。卸装后保留基础肩甲、胸部双散热口与冠军徽记；背面显示基础承载结构。</p>'
body += '<h2 id="head">头部：同一顶头盔的两个状态</h2><div class="head">'+figure(items['HEAD'],'上排普通脸，下排战斗面罩；各排为正面 / 左侧 / 背面')+'</div>'
body += '<p class="intro">五个金色冠件与一片红色中线鳍共用。侧面显示红鳍鳍面，背面显示薄边；面罩只改变口鼻覆盖状态。</p>'
body += '<details><summary>原稿比例对照与本次检查</summary><div class="compare">'
body += figure({'file':'samples/M05-core-head-sync-r7.png'},'已采用 R7 素体来源')
body += figure(items['CORE_FRONT'],'R11 正面比例修正')
body += '</div><ul>'+''.join('<li>'+esc(x)+'</li>' for x in data['author_review']['observed'])+'</ul>'
body += '<p>'+esc(' '.join(data['author_review']['limits']))+'</p><p class="links"><a href="M05-turnaround-production-r11.json">实际源稿与检查</a><a href="M05-turnaround-prompts-r11.json">实际提示词</a><a href="M05-turnaround-verification-r11.json">来源核对</a><a href="M05-red-fin-design-fixed-and-turnaround-r10.json">已采用头部与三视要求</a><a href="M05-battle-mask-r8.html#deployment">面罩转换示意</a><a href="M05-modular-r4.html#packages">配件分组</a></p><p class="note">内置 image_gen 制作。新三视仍为绘制源稿，未充作同一模型精确投影或运行验收；R10矮壮稿退出当前来源，原稿保留。</p></details>'
(OUT/'M05-turnaround-r11.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>王者｜恢复身形的素体与全装三视</title><style>'+css+'</style></head><body><main>'+body+'</main></body></html>\n')
print('Published individually calibrated King front/side/rear reader.')
