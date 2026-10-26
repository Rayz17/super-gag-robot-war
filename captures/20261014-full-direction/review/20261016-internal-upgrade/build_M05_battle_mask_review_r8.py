#!/usr/bin/env python3
"""Present the same King helmet in normal and battle-mask source states."""
from pathlib import Path
import html
import json

OUT = Path(__file__).resolve().parent
def read(name): return json.loads((OUT/name).read_text())
def esc(value): return html.escape(str(value), quote=True)
def figure(file, caption, hidden=False):
    return '<figure'+(' hidden' if hidden else '')+'><a href="'+esc(file)+'"><img src="'+esc(file)+'" alt="'+esc(caption)+'"></a><figcaption>'+esc(caption)+'</figcaption></figure>'

mask = read('M05-battle-mask-production-r8.json')
fin = read('M05-red-fin-production-r9.json')
items = {x['id']:x for x in fin['items']}
css = '''*{box-sizing:border-box}[hidden]{display:none!important}body{margin:0;background:#f4f1e8;color:#253940;font:17px/1.8 system-ui,-apple-system,sans-serif}main{max-width:1500px;margin:auto;padding:28px 26px 70px}a{color:#246b70;text-underline-offset:3px}nav{display:flex;gap:24px;flex-wrap:wrap}h1{font-size:36px;line-height:1.4}h2{font-size:27px;margin-top:42px}.tag{font-size:14px;color:#7e5827;font-weight:700}figure{margin:20px 0;padding:18px;background:#dfe5de;border-radius:8px}img{display:block;width:100%;height:auto;max-height:1000px;object-fit:contain}figcaption{text-align:center;font-size:15px;margin-top:10px}.switch{display:flex;gap:12px;margin-top:25px}button{font:inherit;padding:9px 24px;border:1px solid #8e7446;border-radius:6px;cursor:pointer;background:#fffdf7;color:#253940}button[aria-pressed=true]{background:#33495a;color:#fff;border-color:#33495a}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.note,details{font-size:14px;color:#5c6f69}details{margin-top:35px;padding:18px;background:#e9ece3;border-radius:8px}summary{font-weight:650;cursor:pointer}.links{display:flex;gap:10px 24px;flex-wrap:wrap}@media(max-width:700px){main{padding:24px 14px}h1{font-size:28px}.steps{grid-template-columns:1fr}figure{padding:7px}}'''
body = '''<nav><a href="index.html#king-modular-r4">升级总页</a><a href="M05-modular-r4.html#chassis">素体与全装</a><a href="#deployment">面罩转换</a></nav><p class="tag">王者 · 红色头鳍与双状态面部</p><h1>同一顶头盔，普通脸与战斗面罩切换</h1><p>按标注在金色主角后方、头盔正中增加红色鳍。侧面展开三角鳍面；正面由更高的金色中角遮住，保持同一片鳍的朝向。面罩沿已采用的象牙白折面设计，眼睛、皇冠与耳罩共用。</p><section id="states"><div class="switch" role="group" aria-label="查看两种面部状态"><button type="button" data-state="normal" aria-pressed="false">普通脸</button><button type="button" data-state="mask" aria-pressed="true">战斗面罩</button></div><div id="normal" hidden>'''
body += figure(items['NORMAL']['file'], '普通脸 · 红鳍保留，面罩收入两颊后')
body += '</div><div id="mask">'+figure(items['MASK']['file'], '战斗面罩 · 同一红鳍与头盔，护甲覆盖口鼻')+'</div></section>'
body += '''<p class="note">R7素体／全装与R8面罩源设计已采用；新增红鳍两状态图供看稿。整机R7尚未合入红鳍与闭合面罩。</p><h2 id="deployment">从两侧伸出，再向中央合拢</h2>'''
body += figure(mask['sequence']['file'], '收纳的普通脸 → 两半护罩伸出 → 中央合拢；局部裁切有意不展示头顶')
body += '''<div class="steps"><p><b>收纳</b><br>护罩藏在两侧颊甲后，保留原有白脸与表情。</p><p><b>伸出</b><br>两半护罩沿颊侧短连杆前移，口鼻仍可从中央间隙看见。</p><p><b>合拢</b><br>护罩在中轴对接，形成折面脊线；红色下巴作为外露锁扣。反向运动恢复普通脸。</p></div><p class="note">这张图说明零件来源与开合方向。收纳体积、滑移／转轴轨迹和活动避让还需结构稿或模型核对，当前没有转换动画或运行接入。</p><details><summary>已采用源稿、位置标注与实际制作记录</summary>'''
body += figure('refs/M05-user-red-fin-position-r9.png', '用户红线位置标注 · 头顶中线新增红鳍')
body += figure(mask['file'], '已采用R8面罩源稿 · 新增红鳍前')
body += '''<p>借用<a href="https://www.hasbropulse.com/product/transformers-one-mdlx-optimus-primeorion-pax/HPM6100000">奥利安／擎天柱普通脸与战斗面罩</a>的状态识别效果；王者的双侧合拢结构是本轮设计方案。</p><p class="links"><a href="M05-battle-mask-direction-r8.json">追加面罩要求</a><a href="M05-mask-and-fin-direction-r9.json">面罩采用与红鳍标注</a><a href="M05-battle-mask-production-r8.json">面罩与转换源稿</a><a href="M05-red-fin-production-r9.json">红鳍双状态源稿</a><a href="M05-battle-mask-prompt-r8.json">面罩提示词</a><a href="M05-mask-deploy-prompt-r8.json">转换提示词</a><a href="M05-red-fin-prompt-r9.json">红鳍提示词</a><a href="M05-red-fin-final-prompts-r9.json">遮挡与普通脸提示词</a><a href="M05-mask-fin-verification-r9.json">本轮来源核对</a></p><p>内置 image_gen 制作，接续原美术台账。新图未自动发送到其他对话。</p></details>'''
if fin.get('user_accepted'):
    body=body.replace('新增红鳍两状态图供看稿。','R9红鳍双状态头部源设计已采用。')
if (OUT/'M05-turnaround-production-r10.json').exists():
    body=body.replace('整机R7尚未合入红鳍与闭合面罩。','当前三视设定已将红鳍与面罩合回整机。')
    body='<p><a href="M05-turnaround-r10.html">查看最新素体、全装和双状态头部三视图 →</a></p>'+body
if (OUT/'M05-turnaround-production-r12.json').exists():
    body=body.replace('整机R7尚未合入红鳍与闭合面罩。','当前三视稿已合入红鳍与面罩，按用户反馈恢复整机腿身比例。')
    body='<p><a href="M05-turnaround-r12.html">查看当前素体、全装与头部三视 →</a></p>'+body
script = '''document.querySelectorAll('button[data-state]').forEach(button=>button.addEventListener('click',()=>{const state=button.dataset.state;document.getElementById('normal').hidden=state!=='normal';document.getElementById('mask').hidden=state!=='mask';document.querySelectorAll('button[data-state]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));}));'''
doc = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>王者｜普通脸、战斗面罩与红色头鳍</title><style>'+css+'</style></head><body><main>'+body+'</main><script>'+script+'</script></body></html>\n'
(OUT/'M05-battle-mask-r8.html').write_text(doc)
print('Published King normal/mask states and deployment detail.')
