#!/usr/bin/env python3
"""Present the current King head, chassis and accessory-package source designs."""
from pathlib import Path
import html
import json
import re

OUT = Path(__file__).resolve().parent


def read(name):
    return json.loads((OUT / name).read_text())


def figure(file, caption):
    f = html.escape(file, quote=True)
    c = html.escape(caption, quote=True)
    return f'<figure><a href="{f}"><img src="{f}" alt="{c}" loading="lazy"></a><figcaption>{c}</figcaption></figure>'


CSS = '''*{box-sizing:border-box}body{margin:0;background:#f4f1e8;color:#253940;font:17px/1.8 system-ui,-apple-system,sans-serif}main{max-width:1500px;margin:auto;padding:34px 26px 70px}a{color:#246b70;text-underline-offset:3px}nav,.links{display:flex;flex-wrap:wrap;gap:10px 24px}h1{font-size:38px;line-height:1.35}h2{font-size:29px;margin-top:46px}.tag{color:#2b6c6b;font-size:14px;font-weight:750;letter-spacing:.07em}.notice{border-left:5px solid #bb8c39;background:#fffdf6;padding:14px 24px;margin:24px 0}.pair,.refs{display:grid;grid-template-columns:1fr 1fr;gap:22px}.refs{grid-template-columns:repeat(3,1fr)}.pair img{height:830px}.refs img{height:430px}figure{margin:20px 0;background:#dfe5de;padding:16px;border-radius:8px}img{display:block;width:100%;height:auto;max-height:1100px;object-fit:contain}figcaption{text-align:center;margin-top:12px;font-size:15px;font-weight:650}.note{font-size:14px;color:#60736b}details{margin:24px 0;padding:18px;background:#e9ece3;border-radius:8px}summary{cursor:pointer;font-weight:650}.scroll{overflow-x:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #c4d1c5;padding:13px}@media(max-width:800px){main{padding:24px 16px}h1{font-size:29px}.pair,.refs{grid-template-columns:1fr}.pair img,.refs img{height:auto;max-height:850px}table{font-size:14px}}'''

prod = read('M05-modular-production-r4.json')
items = {x['id']: x for x in prod['items']}
head5 = read('M05-head-upward-L-production-r5.json') if (OUT/'M05-head-upward-L-production-r5.json').exists() else None
if head5:
    items['HEAD'] = head5
head6 = read('M05-head-riese-production-r6.json') if (OUT/'M05-head-riese-production-r6.json').exists() else None
if head6:
    items['HEAD'] = head6
fixed6 = read('M05-head-design-fixed-20261020.json') if (OUT/'M05-head-design-fixed-20261020.json').exists() else None
sync7 = read('M05-modular-head-sync-production-r7.json') if (OUT/'M05-modular-head-sync-production-r7.json').exists() else None
mask8 = read('M05-battle-mask-production-r8.json') if (OUT/'M05-battle-mask-production-r8.json').exists() else None
fin9 = read('M05-red-fin-production-r9.json') if (OUT/'M05-red-fin-production-r9.json').exists() else None
tri11 = read('M05-turnaround-production-r12.json') if (OUT/'M05-turnaround-production-r12.json').exists() else None
if sync7:
    for item in sync7['items']:
        items[item['id']] = item
kits = read('M05-module-catalog-r4.json')
body = '''<nav><a href="index.html#king-modular-r4">升级总页</a><a href="#head">L角头部</a><a href="#chassis">素体与全装</a><a href="#packages">配件包整理</a><a href="M05-style-match-r2.html">上一轮画法对照</a></nav><p class="tag">2026.10.19 · 全装王者 · 头部与配件包 R4</p><h1>同一台王者，叠上多套豪华配件包</h1><div class="notice"><p>图四的脸作为依据，皇冠仍有五组主构件：两侧四瓣对称，内侧两瓣较长；中间改成向前伸的L型犄角，尖端有一枚朝回的鱼叉倒钩。</p><p>全装保留有用的冗余。素体本身仍是厚重、华丽的旧系列主角机，配件按明确接口逐层挂上。本轮新图供看稿，尚未固定为最终设计。</p></div><h2 id="head">先把头脸与朝向读清</h2>'''
body += figure(items['HEAD']['file'], '当前L角头部 · 正面 / 左侧观察；中轴朝前，四瓣成对')
body += '''<p>正面中轴是朝向观众的短缩端面；侧面显示先竖起、再前伸的L形和倒钩。保留海军蓝盔体、浅色双眼、白色重下颌、红下巴和金色脸框。头壳本体保留正常纵向体积。</p><details><summary>脸部依据与此前直冠探索</summary>'''
body += figure('refs/M05-user-face-D-r3.png', '用户指定图四 · 脸部依据')
body += figure('samples/M05-head-three-long-r3b.png', '此前三长两短直冠 · 随后按新要求改为中央L角，不作当前中轴形态')
body += '''</details><h2 id="chassis">素体与全装分开看</h2><div class="pair">'''
body += figure(items['CORE']['file'], '王者素体 · 同一头胸身份、完整双手和基础身体')
body += figure(items['FULL']['file'], '王者全装整理稿 · 挂上外甲、翼推进、重炮、钻盾和弹仓')
body += '''</div><p>素体保留双矩形胸部散热口、冠军胸徽、红色腹部、金色圆关节及宽靴。右臂钻拆下后恢复手部，左盾通过前臂挂点装卸；肩、背和腿侧各有自己的承载位置。</p><h2 id="packages">配件包按六组组织</h2>'''
body += figure(items['KITS']['file'], '配件包方向图 · 用于识别分组；精确数量、隐面和接口仍以逐组结构稿继续固定')
rows = ''.join('<tr><td>'+html.escape(p['id']+' '+p['name'])+'</td><td>'+html.escape('、'.join(p['components']))+'</td><td>'+html.escape(p['mount'])+'</td><td>'+html.escape(p['role'])+'</td></tr>' for p in kits['packages'])
body += '<div class="scroll"><table><thead><tr><th>生产分组</th><th>主要零件</th><th>挂载位置</th><th>视觉作用</th></tr></thead><tbody>'+rows+'</tbody></table></div>'
body += '''<p class="note">这些名称和分组是本轮设计整理，未新增剧情装备或运行数值。头冠通讯器保留可拆带座；“素体图”仍戴冠以便比较同一身份。</p><h2>三个过度设计参考里，适合加强的部分</h2><div class="refs">'''
body += figure('refs/M05-user-overdesign-A-r3.png', '图一：多路武装与后背承载分层')
body += figure('refs/M05-user-overdesign-B-r3.png', '图二：外挂大幅超出本体，形成外扩轮廓')
body += figure('refs/M05-user-overdesign-C-r3.png', '图三：厚重外甲包住本体，前后体量分层')
body += '''</div><p>本轮取三点：让背肩重炮、翼架和低位推进舱分出前后层次；让肩胸缘、腰裙和胫外甲显出“套在素体外”的厚度；在头脸周围留净空，使皇冠仍是视觉中心。配件先成组，再安排大小层次，保留王者自己的钻、盾、炮、翼和配色。</p><h2>实际检查与仍需收敛的位置</h2>'''
review = (sync7 or head6 or head5 or prod)['author_review']
if sync7 and sync7.get('new_body_images_user_accepted'):
    review = dict(review, limits=['R7素体与全装源设计已获后续用户认可；精确多视、模型和运行仍另记。'] + review['limits'][1:])
body += '<ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in review['observed'])+'</ul>'
body += '<p>'+' '.join(html.escape(x) for x in review['limits'])+'</p>'
body += '''<details><summary>来源、实际提示词及下一工序</summary><p class="links"><a href="M05-modular-direction-r4.json">用户要求</a><a href="M05-module-catalog-r4.json">配件分组</a><a href="M05-modular-production-r4.json">源稿与实际检查</a><a href="M05-modular-prompts-r4.json">全部实际提示词</a><a href="M05-modular-verification-r4.json">来源核对</a></p><p>内置 image_gen 制作；后续在选定母稿上统一正侧背、各组接口和卸装状态。手绘方向图不代替同一模型投影或活动让位检查。</p></details><p class="note">本批接续原美术设计台账。新图未发送主玩法对话，未改游戏运行；无牌已确认头部、旧拳王当前方向、馆守现有资产和固定29张源图保持。</p>'''
if head5:
    for old,new in [
        ('2026.10.19 · 全装王者 · 头部与配件包 R4','2026.10.20 · 全装王者 · 朝上独角仙L角 R5'),
        ('中间改成向前伸的L型犄角，尖端有一枚朝回的鱼叉倒钩','中间改为朝上刺出的独角仙式L角：短根座前探后，长角身上挑，主尖朝上，顶端保留朝回倒钩'),
        ('当前L角头部 · 正面 / 左侧观察；中轴朝前，四瓣成对','当前R5朝上L角 · 正面 / 左侧；短底座前探、长段朝上，四瓣成对'),
        ('正面中轴是朝向观众的短缩端面；侧面显示先竖起、再前伸的L形和倒钩。','正面显示中轴向上的长角身；侧面显示短底座前探后向上折起，主尖朝上，倒钩朝回。'),
        ('<h2 id="chassis">素体与全装分开看</h2>','<h2 id="chassis">R4颈下与配件参考</h2><div class="notice"><p>下方两张仍含已被指出错误的水平前刺中角，仅保留颈下与配件候选。当前头角看上方R5，整机头角尚未同步。</p></div>'),
        ('王者素体 · 同一头胸身份、完整双手和基础身体','R4素体颈下参考 · 旧中角待同步'),
        ('王者全装整理稿 · 挂上外甲、翼推进、重炮、钻盾和弹仓','R4全装颈下参考 · 旧中角待同步'),
    ]:
        body=body.replace(old,new)
    body += '<p class="links"><a href="M05-head-upward-L-direction-r5.json">本次朝向纠正</a><a href="M05-head-upward-L-production-r5.json">当前头部来源</a><a href="M05-head-upward-L-prompt-r5.json">朝上角实际提示词</a><a href="M05-head-upward-L-front-prompt-r5b.json">前视投影修正提示词</a></p>'
if head6:
    rest = body[body.index('<h2 id="chassis">'):]
    rest = rest.replace('当前头角看上方R5', '当前头角看上方R6')
    rest = re.sub(r'<p class="links"><a href="M05-head-upward-L-direction-r5.json">.*?</p>', '', rest)
    body = '''<nav><a href="index.html#king-modular-r4">升级总页</a><a href="#head">当前头部</a><a href="#chassis">颈下参考</a><a href="#packages">配件包</a></nav><p class="tag">2026.10.20 · 王者头部 R6</p><h1>厚根上挑额角，细侧天线分层</h1><div class="notice"><p>用户否定上一版直立箭头角，指定参考古铁巨神的头部天线和角。本轮保留图四脸、海军蓝盔体及白红金配色，改用连贯上挑的刀刃角，并收细两对侧天线。</p><p>正面中角居中；侧面表达前后弧度与倒钩。当前为独立头稿，素体与全装的旧角仍待同步。</p></div><h2 id="head">当前头部正面与侧面</h2>'''
    body += figure(head6['file'], 'R6头部候选 · 正面中轴收正，侧面显示上挑刀刃角')
    body += '''<p>借用的是额角根部、逐渐收尖的轮廓和主角／侧天线层次，保留王者自己的脸与皇冠身份。两张手绘视图供判断造型，尚不是同一模型的精确投影。</p><p><a href="https://www.kotobukiya.co.jp/product/detail/p4934054101573/">古铁巨神官方产品页</a> · <a href="M05-head-riese-direction-r6.json">参考来源与本次要求</a> · <a href="M05-head-riese-prompt-r6.json">实际提示词</a> · <a href="M05-head-riese-front-prompt-r6b.json">前视修正提示词</a> · <a href="M05-head-riese-production-r6.json">实际源稿检查</a></p><details><summary>图四脸部依据与已否定的R5角</summary>'''
    body += figure('refs/M05-user-face-D-r3.png', '用户指定脸部依据，继续有效')
    body += figure('samples/M05-head-upward-L-r5b.png', 'R5执行已被用户否定，不作当前角形')
    body += '</details>' + rest
if fixed6:
    body=body.replace('当前为独立头稿，素体与全装的旧角仍待同步。','用户已指定采用这张R6b头部源图；造型与原色沿该图固定。')
    body=body.replace('当前头部正面与侧面','已选定头部正面与侧面').replace('R6头部候选 · 正面中轴收正，侧面显示上挑刀刃角','R6b头部源设计已选定 · 原图保持')
    body=body.replace('两张手绘视图供判断造型，尚不是同一模型的精确投影。','认可范围为指定头部源设计；手绘多视仍不是同一模型的精确投影。')
    body=body.replace('<h2 id="head">','<p><a href="M05-head-design-fixed-20261020.json">本次指定图与认可范围</a></p><h2 id="head">',1)
if sync7:
    body=body.replace('>颈下参考</a>', '>素体与全装</a>')
    body=body.replace('<h2 id="chassis">R4颈下与配件参考</h2><div class="notice"><p>下方两张仍含已被指出错误的水平前刺中角，仅保留颈下与配件候选。当前头角看上方R6，整机头角尚未同步。</p></div>','<h2 id="chassis">同一头型合回素体与全装</h2><p>下方两张已采用选定R6b头型；本轮只同步头部，颈下身体与装备延用。新整机图不扩大原头稿认可范围。</p>')
    body=body.replace('R4素体颈下参考 · 旧中角待同步','R7素体同步稿 · 保留双手与基础身体').replace('R4全装颈下参考 · 旧中角待同步','R7全装同步稿 · 保留钻盾、双炮、层翼与四个腿侧弹仓')
    body+='<p class="links"><a href="M05-modular-head-sync-production-r7.json">整机同步来源与实际检查</a><a href="M05-modular-head-sync-prompts-r7.json">内置生图实际提示词</a><a href="M05-head-sync-verification-r7.json">本轮来源核对</a></p>'
if mask8:
    body=body.replace('新整机图不扩大原头稿认可范围。','R7素体与全装源设计已采用；新增红鳍与闭合面罩尚未合回这两张。')
    body='<div class="notice"><p><b>最新追加：战斗面罩与红色中线鳍。</b><a href="M05-battle-mask-r8.html">查看普通脸／战斗面罩及转换示意 →</a></p><p>R7源稿与R8面罩已采用；本页保留基础头型和整机来源。新增红鳍双状态图见新页。</p></div>'+body
    body=body.replace('>当前头部</a>', '>基础头型</a>')
if tri11:
    body='<div class="notice"><p><b>当前：恢复腿身比例的素体与全装三视。</b><a href="M05-turnaround-r12.html">查看正、侧、背及两状态头部 →</a></p><p>按最新反馈弃用R10矮壮比例，分别绘制各视角。下方保留已采用的R7整机与配件来源。</p></div>'+body
doc = f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>王者｜当前头部、素体与配件包</title><style>{CSS}</style></head><body><main>{body}</main></body></html>\n'
(OUT/'M05-modular-r4.html').write_text(doc)

p = OUT/'design-followthrough-section.html'
s = p.read_text()
start = s.index('<div class="phase" id="next-mecha-batch-20261019">')
end = s.index('<div class="phase" id="brave-components-r8">', start)
phase = '''<div class="phase" id="next-mecha-batch-20261019"><span id="king-modular-r4"></span><p class="kicker">全装王者 / L角、素体与配件包 R4</p><h3>王者的素体和六组配件，按同一头脸重新组织</h3><p>图四脸部、四瓣对称侧冠和中央前伸L角；倒钩从左侧可辨。素体与全装分开画，保留厚重华丽、右钻左盾、背肩双炮、分层翼及腿侧弹仓。</p><figure class="scene"><a href="M05-modular-r4.html#head"><img src="samples/M05-head-L-harpoon-r4b.png" alt="全装王者中央前伸L角与鱼叉倒钩，正面及左侧对照" style="max-height:720px;object-fit:contain"></a><figcaption>当前头部方向 · 新图待看</figcaption></figure><div class="direction-refs two"><figure class="direction-ref"><a href="M05-modular-r4.html#chassis"><img src="samples/M05-core-body-r4.png" alt="王者素体候选" style="height:650px;object-fit:contain"></a><figcaption>素体</figcaption></figure><figure class="direction-ref"><a href="M05-modular-r4.html#chassis"><img src="samples/M05-modular-full-r4.png" alt="王者全装配件整理候选" style="height:650px;object-fit:contain"></a><figcaption>全装整理稿</figcaption></figure></div><p><a href="M05-modular-r4.html"><b>看头部、素体、配件包与加强意见 →</b></a> · <a href="M05-modular-prompts-r4.json">实际提示词</a></p><p>旧拳王沿当前样例继续，无牌R16头部保持；馆守及固定29源不动。王者新稿待看，确认后再集中交接。</p></div>\n'''
if head5:
    phase=phase.replace('samples/M05-head-L-harpoon-r4b.png',head5['file']).replace('全装王者 / L角、素体与配件包 R4','全装王者 / 朝上独角仙L角 R5').replace('王者的素体和六组配件，按同一头脸重新组织','中央角改为向上刺出，保留独角仙般的上挑轮廓').replace('中央前伸L角','中央朝上L角').replace('全装王者中央前伸L角','全装王者中央朝上L角').replace('倒钩从左侧可辨。','短底座前探后上挑，主尖朝上，倒钩从侧面可辨；下方R4整机旧中角待同步。').replace('<figcaption>素体</figcaption>','<figcaption>素体颈下参考 · 中角待同步</figcaption>').replace('<figcaption>全装整理稿</figcaption>','<figcaption>全装颈下参考 · 中角待同步</figcaption>')
if head6:
    phase = '<div class="phase" id="next-mecha-batch-20261019"><span id="king-modular-r4"></span><p class="kicker">王者头部 R6 / 古铁巨神结构参考</p><h3>厚根上挑额角，细侧天线分层</h3><p>上一版直立箭头角已被用户否定；新稿保留图四脸与原色，先独立处理额角和两对侧天线。正面中轴收正，侧面表达弧度。</p><figure class="scene"><a href="M05-modular-r4.html#head"><img src="'+head6['file']+'" alt="王者R6头部正侧候选" style="max-height:820px;object-fit:contain"></a><figcaption>当前头部候选，待用户看稿</figcaption></figure><p><a href="M05-modular-r4.html#head">查看当前头部及参考 →</a> · <a href="M05-modular-r4.html#chassis">R4颈下与配件参考 →</a></p><p>整机旧角尚待同步；无牌已确认头部、旧拳王当前方向、馆守及固定29源保持。</p></div>\n'
if fixed6:
    phase=phase.replace('当前头部候选，待用户看稿','R6b指定头部已选定').replace('整机旧角尚待同步；','已按选定头型同步R7素体与全装源稿；整机新图与运行另记。')
    phase=phase.replace('R4颈下与配件参考 →','R7素体与全装同步稿 →')
if fin9:
    current_mask=next(x for x in fin9['items'] if x['id']=='MASK')
    phase='<div class="phase" id="next-mecha-batch-20261019"><span id="king-modular-r4"></span><p class="kicker">王者 / 战斗面罩与红色头鳍</p><h3>一顶头盔，两种面部状态</h3><p>面罩已采用；在金色主角后、头盔中线追加红鳍，普通脸与战斗面罩保留同一头盔。正面红鳍被金色中角遮住，侧面展开鳍面。</p><figure class="scene"><a href="M05-battle-mask-r8.html"><img src="'+current_mask['file']+'" alt="王者红鳍与战斗面罩正侧源稿" style="max-height:820px;object-fit:contain"></a><figcaption>新增红鳍双状态源稿 · 面罩沿已采用设计</figcaption></figure><p><a href="M05-battle-mask-r8.html">普通脸／战斗面罩与转换示意 →</a> · <a href="M05-modular-r4.html#chassis">R7素体与全装源稿 →</a></p><p>R7源设计与R8面罩已采用；新增红鳍图供看稿，整机尚未合入红鳍与闭合面罩。</p></div>\n'
if tri11:
    current_front=next(x for x in tri11['items'] if x['id']=='FULL_FRONT')
    phase='<div class="phase" id="next-mecha-batch-20261019"><span id="king-modular-r4"></span><p class="kicker">王者 / 素体与全装三视 R12</p><h3>恢复长腿身形，再看正、侧、背</h3><p>R9红鳍双状态头部已采用。当前三面恢复腿身比例，并同步右肘前屈/钻头朝前；背包加中央喷口和双燃料罐。</p><figure class="scene"><a href="M05-turnaround-r12.html"><img src="'+current_front['file']+'" alt="王者全装正面，恢复腿身比例" style="max-height:1050px;object-fit:contain"></a><figcaption>当前R12三视源稿 · 新图待看</figcaption></figure><p><a href="M05-turnaround-r12.html#full">全装三视 →</a> · <a href="M05-turnaround-r12.html#core">素体三视 →</a> · <a href="M05-turnaround-r12.html#head">两状态头部 →</a></p><p>已采用源设计保留；R10矮壮稿退出当前来源，新三视未充作模型或运行验收。</p></div>\n'
p.write_text(s[:start]+phase+s[end:])

# Keep the earlier two-machine entry useful without hiding the retained R2 art.
p = OUT/'next-batch-mecha-20261019.html'
if p.exists():
    s = p.read_text()
    current = '<section id="complete-king"><h2>全装王者：L角、素体与配件包R4</h2><p>图四脸、对称侧冠与中轴前伸L角；头部、素体、全装和六组配件分别整理。</p>'+figure(items['FULL']['file'], '全装整理R4 · 具体新稿待看')+'<p><a href="M05-modular-r4.html"><b>打开当前头部、素体与配件图 →</b></a></p><p class="note">本轮新图尚未确认或发送。模型、多视图和运行分别验证。</p></section>'
    if head5:
        current='<section id="complete-king"><h2>王者当前头部：朝上独角仙L角R5</h2><p>短底座前探后向上折起，主尖朝上；图四脸和两对侧冠保持。R4整机旧中角待同步。</p>'+figure(head5['file'],'R5朝上角修正 · 具体新图待看')+'<p><a href="M05-modular-r4.html#head">查看当前头部与此前来源 →</a></p></section>'
    if head6:
        current = '<section id="complete-king"><h2>王者当前头部：上挑刀刃角R6</h2><p>按古铁巨神角与天线参考重新组织，保留图四脸和王者原色。R5执行已否定，整机旧角待同步。</p>'+figure(head6['file'], 'R6新头部候选，待看稿')+'<p><a href="M05-modular-r4.html#head">查看当前头部及来源 →</a></p></section>'
    if fixed6:
        current=current.replace('R6新头部候选，待看稿','R6b头部已选定').replace('R5执行已否定，整机旧角待同步。','R6b指定头部已选定，R5执行已否定。')
    if sync7:
        current=current.replace('</section>',figure(items['FULL']['file'],'R7全装头部同步稿 · 整机新图另记')+'<p><a href="M05-modular-r4.html#chassis">查看素体与全装同步稿 →</a></p></section>')
    if fin9:
        current='<section id="complete-king"><h2>王者：普通脸、战斗面罩与红色头鳍</h2><p>R7源设计与R8面罩已采用。新增红鳍在头顶中线，普通／战斗两状态共用头盔。</p>'+figure(next(x['file'] for x in fin9['items'] if x['id']=='MASK'), '红鳍与战斗面罩 · 新增红鳍图供看稿')+'<p><a href="M05-battle-mask-r8.html">查看双状态与转换示意 →</a> · <a href="M05-modular-r4.html#chassis">素体与全装源稿 →</a></p></section>'
    if tri11:
        current='<section id="complete-king"><h2>王者：恢复原稿身形的三视 R12</h2><p>完整大腿、长胫甲与正常头部体积保留，素体和全装逐面绘制。</p>'+figure(next(x['file'] for x in tri11['items'] if x['id']=='FULL_FRONT'),'R11全装正面 · 新三视源稿')+'<p><a href="M05-turnaround-r12.html">查看素体、全装与头部三视 →</a></p></section>'
    s = re.sub(r'<section id="complete-king">.*?</section>', lambda m: current, s, count=1, flags=re.S)
    s = s.replace('旧拳王沿用，王者小幅统一画法', '旧拳王沿用，王者整理素体与配件包')
    s = s.replace('王者R2保持身份与全装，只统一绘制语言。', '王者R4进一步优化头部并拆分素体和配件包，具体新稿待看。')
    if head5:
        s=s.replace('王者R4进一步优化头部并拆分素体和配件包，具体新稿待看。','王者R5头部改为朝上独角仙L角；R4整机旧中角尚待同步。')
    if head6:
        s=s.replace('王者R5头部改为朝上独角仙L角；R4整机旧中角尚待同步。','王者R6参考古铁巨神重做角与天线；整机旧中角尚待同步。')
    if sync7:
        s=s.replace('王者R6参考古铁巨神重做角与天线；整机旧中角尚待同步。','王者R6b头部已选定，R7素体与全装已同步该头型。')
    if fin9:
        s=s.replace('王者R6b头部已选定，R7素体与全装已同步该头型。','王者已采用R7源设计与R8面罩，最新追加头顶中线红鳍。')
    p.write_text(s)
p = OUT/'M05-style-match-r2.html'
if p.exists():
    s = p.read_text()
    if 'id="latest-modular-r4"' not in s:
        s = s.replace('<main>', '<main><div class="notice" id="latest-modular-r4"><p><b>当前王者设计已推进至R4：</b><a href="M05-modular-r4.html">L角头部、素体、全装与配件包 →</a>。下方R2保留作画法比较与来源历史。</p></div>', 1)
    if head5:
        s=s.replace('当前王者设计已推进至R4','当前王者头部已推进至R5')
    if head6:
        s=s.replace('当前王者头部已推进至R5','当前王者头部已推进至R6')
    p.write_text(s)
print('Published current King modular review and existing batch entry.')
