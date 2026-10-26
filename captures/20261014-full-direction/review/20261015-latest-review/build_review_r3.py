"""Bind the 2026-10-15 review to the images actually shown by review-v2.html.

This edits the requested reader only. It does not edit images, Canon or game assets.
The immutable before-file and previous structured review keep the r2 evidence.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
import csv
import hashlib
import html
import json
import re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
PAGE = ROOT / 'review-v2.html'
SNAPSHOT = json.loads((OUT / 'current-file-inventory.json').read_text())
BACKUP = OUT / 'before-review-r3-20261015.html'

def sha(data):
    return hashlib.sha256(data).hexdigest()

if not BACKUP.exists():
    raw = PAGE.read_bytes()
    if sha(raw) != SNAPSHOT['page_sha256']:
        raise SystemExit('Page changed since image inspection; review the new version before writing.')
    BACKUP.write_bytes(raw)
source = BACKUP.read_text()
# The evidence snapshot stays byte-for-byte intact; this separate reader fixes its base URL.
historical_reader = source.replace('<head>', '<head><base href="../../">', 1).replace(
    '<body>', '<body><div style="padding:16px;background:#f5e1b8;color:#654b21">历史页面快照：包含旧r2文字与当时混用的新版预览，不作为当前评审结论。<a href="review-v2.html#latest-review-r3">返回最新r3评审</a></div>', 1)
(OUT / 'before-review-r3-reader.html').write_text(historical_reader)
live_before = PAGE.read_bytes()
if live_before != BACKUP.read_bytes() and 'id="latest-review-r3"' not in live_before.decode():
    raise SystemExit('Unrecognized concurrent reader edits; preserve and reconcile first.')
last_build = OUT / 'r3-build-result.json'
if live_before != BACKUP.read_bytes() and last_build.exists():
    if sha(live_before) != json.loads(last_build.read_text())['page_sha256']:
        raise SystemExit('The r3 reader was edited after its last build; reconcile rather than overwrite.')

old_data = json.loads(re.search(
    r'<script type="application/json" id="asset-review-data">([\s\S]*?)</script>', source).group(1))
old_records = {r['id']: r for r in old_data['records']}
(OUT / 'previous-review-r2-data.json').write_text(json.dumps(old_data, ensure_ascii=False, indent=2) + '\n')
notes = list(csv.DictReader((OUT / 'review-notes-r3.tsv').open(), delimiter='\t'))
by_id = {r['id']: r for r in notes}
items = {r['id']: r for r in SNAPSHOT['items']}
assert len(notes) == len(by_id) == len(items) == 298
assert set(by_id) == set(items)
for r in notes:
    assert set(r) == {'id', 'verdict', 'use', 'problem', 'change', 'related', 'tags'}
    assert r['verdict'] in 'ABC'
    assert all(r[k] for k in r)
    assert set(r['related'].split(',')) <= set(items)
for r in items.values():
    assert sha((ROOT / r['file']).read_bytes()) == r['sha256'], f"Image changed: {r['id']}"
archive_dir = OUT / 'images'
archive_dir.mkdir(exist_ok=True)
for r in items.values():
    archived = archive_dir / (r['sha256'] + '.jpg')
    if not archived.exists():
        archived.write_bytes((ROOT / r['file']).read_bytes())
    assert sha(archived.read_bytes()) == r['sha256']
    r['preview_file'] = archived.relative_to(ROOT).as_posix()

counts = Counter(r['verdict'] for r in notes)
group_counts = {g: Counter(r['verdict'] for r in notes if r['id'][0] == g)
                for g in dict.fromkeys(r['group'] for r in items.values())}
groups = defaultdict(list)
for r in items.values():
    groups[r['sha256']].append(r['id'])
duplicates = [ids for ids in groups.values() if len(ids) > 1]
changed_ids = [i for i, r in items.items() if
               old_records[i].get('img') != r['file'] or
               old_records[i].get('image_sha256') != r['sha256']]
labels = {'A': '建议沿用设计方向', 'B': '保留可用部分，修改后用', 'C': '主体或核心语义重做'}
tag_labels = {'identity': '同源/设定', 'structure': '结构/功能', 'scale': '尺寸/占格',
              'style': '画法/精度', 'palette': '配色/层级', 'semantics': '规则/语义', 'motion': '动作/时序'}
esc = lambda s: html.escape(str(s), quote=True)
def links(ids):
    if isinstance(ids, str):
        ids = ids.split(',')
    return ' · '.join(f'<a href="#{i}">{i} {esc(items[i]["name"])}</a>' for i in ids)

def fig(i, caption, kind=''):
    r = items[i]
    return (f'<figure class="r3-figure {kind}"><a href="{esc(r["preview_file"])}" target="_blank" rel="noopener">'
            f'<img src="{esc(r["preview_file"])}" alt="{i} 当前来稿：{esc(r["name"])}" loading="lazy" width="1280" height="720"></a>'
            f'<figcaption><a href="#{i}"><strong>{i} {esc(r["name"])}</strong></a><p>{caption}</p>'
            f'<small>{esc(Path(r["file"]).name)}</small></figcaption></figure>')

def case(title, desc, figures, cols=3):
    return f'<div class="r3-case"><h3>{title}</h3><p>{desc}</p><div class="r3-comparison cols-{cols}">{figures}</div></div>'

today = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')
top = f'''
<section class="review-intro r3-intro" id="latest-review-r3" aria-labelledby="r3-title">
<p class="r3-kicker">2026-10-15 · 当前交付复核 r3 · 图像、文字、链接重新绑定</p>
<h2 id="r3-title">这批值得用。先保留好的画法与设计，再修掉跨图换人、换机和错误规则。</h2>
<p class="r3-lead">我的判断是：<strong>它已经提供了比现用资产更有吸引力的绘制方向，但还不是一套能不加区分地整包替换的素材。</strong>主要价值在英雄机体的大色块与轮廓、现代建筑的体量、人物的独立形象和部分图形后果表达。主要问题在同一主体跨图失去身份、组件/变形关系不成立、材质与UI画法跳档，以及太多对象被涂成同一组青白红。</p>
<p>按你这次的反馈，<strong>绘制风格、具体配色、设定/功能是否正确分开判断</strong>。喜欢某张的画法，不意味着它的头胸、车型、衣服、尺寸或技能含义可以随意改变；某张需要改设定，也不意味着要丢掉它已经画好的构图、质感与动势。</p>
<div class="r3-counts"><a href="#group-M" class="rv-A"><b>{counts['A']}</b> 项 · 建议沿用设计方向</a><a href="#group-B" class="rv-B"><b>{counts['B']}</b> 项 · 保留并具体修改</a><a href="#r3-rework" class="rv-C"><b>{counts['C']}</b> 项 · 主体/核心语义重做</a></div>
<p class="r3-small">按 <strong>298条任务</strong>计数，共295张独立图；M08/F07、M11/F06、M14/F08各共用一张成对设定页。A/B/C是本次设计评审建议，不是模型交付、游戏接入或新增用户认可。缺模型/PSD不作为这批单张方向稿的扣分理由。</p>
<nav class="review-jump" aria-label="最新评审目录"><a href="#r3-use">哪些可以用</a><a href="#r3-lineage">同源链与修改顺序</a><a href="#r3-examples">实际图面对照</a><a href="#r3-palette">配色与画法</a><a href="#r3-scale">尺寸与建筑</a><a href="#r3-interface">UI/特效怎么统一</a><a href="#r3-handoff">如何用于项目</a><a href="#r3-rework">28项重点返改</a><a href="#group-M">全部逐项意见</a></nav>
<div class="r3-alert"><strong>先纠正阅读页的版本问题：</strong>核对发现87条当前图文件/摘要与旧评审记录不匹配，80张卡片点击后会打开不同于预览的旧版。新版已经改掉的“坡顶砖屋”“没有飞机形态”“白鸢裸手黑衣”等问题，不应继续照旧退稿。本次已把当前图、放大链接、逐项意见和摘要绑定到同一文件；旧r2文字单独折叠保留。</div>

<section class="r3-section" id="r3-use"><h2>1. 能用什么：按用途取舍，不整包洗色，也不整包推翻</h2>
<div class="r3-decision-grid">
<div><h3>机体与人物</h3><p><strong>优先沿用：</strong>{links('M01,M02,M06,M07,M09,M10,M13')}；H01–H09人物方向基本可留。</p><p>有独立角色色与职业/谱系轮廓，适合进入结构母版、低模/贴图或立绘制作。M05保留满装冠军框架；M03/M04/M08/M11/M14保留新版改进，先修左右、核心/外挂、载具对应再派生。</p></div>
<div><h3>建筑与环境</h3><p><strong>优先来源：</strong>{links('B01,B04,B05,B06,B10,B24,B34')}；地面采用T01/T02/T03/T08/T09的厚度/材质方法。</p><p>本轮办公、工房和服务楼已经现代化，应保留。住宅要像能住人的楼，设备要像有工作原理的设施；小值班室、路灯本来可以保持人用尺度。</p></div>
<div><h3>效果与动作</h3><p><strong>优先语言：</strong>{links('X01,X02,X04,X05,X10,X13,X14,X19,X20,X25,X26')}；N01/N02/N04/N05/N08是共享动作参考。</p><p>提取击星、喷流、烟、泡沫、焊光的表达，别把代理机与背景一起带入。标准动作复用；体术和招牌动作重点做，同一事件由各对象处理自身状态。</p></div>
<div><h3>UI与事件图</h3><p><strong>优先骨架：</strong>{links('U01,U05,U06,U14,U17,U19')}；I04/I09/I12/I13/I15的简化方向较合适。</p><p>版式与图形后果有用，假头像/任务/数值不沿用。事件图保留镜位与三拍因果，先把人物、设备与机体对回母版；无法只换配色解决的主体另列C类。</p></div>
</div>
<p><strong>“画法可用”和“具体物件可用”要分开：</strong>S01–S04可以提供空间与材质方向，但临时小机和未对齐地图不直接采用；U03/U11可参考排版，但地图上的机体头像必须由机体头肩裁切，不能拿一组陌生人类头像代替。</p></section>

<section class="r3-section" id="r3-lineage"><h2>2. 最大问题是同源链断裂，先修母版，再修派生</h2>
<p>这里的同源不是要求大家长得一样。<strong>不同机体应有不同轮廓、色彩和动作；同一机体在站姿、部件、变形、招式和剧情图里，应仍是同一个身体。</strong>文字写“locked”“same parts”不能替代图中真实对应。</p>
<div class="table-scroll"><table><thead><tr><th>对象链</th><th>本次保留来源</th><th>必须修的内容</th><th>连带更新</th></tr></thead><tbody>
<tr><td>纪存 / 白鸢 / 七海</td><td>H01 / H02 / H03的脸、发型、衣装</td><td>S09/S10已有进步，局部校正；S21换回领口和成年骨相；S11/U09不是七海，主体重做</td><td>S09–S11、S21、U09/U10及人物专用图标</td></tr>
<tr><td>无牌 / 旧拳王</td><td>M01白青绿金灵巧机；M02厚护拳老拳手</td><td>N09/S13、N10的头胸身体已换掉；保留姿态，使用原机身</td><td>招牌动作、cut-in、头像、命中事件</td></tr>
<tr><td>馆守</td><td>M03新版巨神形；当前缺右拳与前臂事实</td><td>按自身左右纠正毁损侧；普通图不可恢复双拳，临时件不冒充后继完整手臂</td><td>M15终端、S08托桥、S18工房、索具</td></tr>
<tr><td>社勇王</td><td>F09完整机器人；M04橙白满合体方向</td><td>F10把核心画成拳头、N14变无头红模块，均退回；原头胸四肢保留，外挂有来源</td><td>F11/F12、S14、N11/N14、合体图标</td></tr>
<tr><td>完全版王者</td><td>M05满装框架与冗余；不改成清瘦通用机</td><td>M05当前钻盾左右相反；右钻左盾、两背肩各一前向炮、对称封闭面罩；F01等必须真从这套拆出</td><td>F01–F05、S12/S20、N12、装备状态</td></tr>
<tr><td>雷翎 / 歌翼</td><td>M08/F07、M14/F08各自成对候选</td><td>新版已有飞机，不再说“没有载具”；但座舱/主翼/发动机在人形仍未追认，不能只贴编号</td><td>N13各自中间姿态、形态头像/武器挂点</td></tr>
<tr><td>货柜领袖</td><td>M11/F06白深蓝橙重载车候选</td><td>先定货箱/车头/三轴轮组去向；N13军绿车、S19深蓝橙卡车不是本款</td><td>载具形态、搬运/护场、剧情事件</td></tr>
<tr><td>列车 / 桥 / 居民楼</td><td>B12+B13同车；B14同桥；B01–B03同城现代住宅</td><td>剧情图不换蒸汽车/复古水乡；破坏前后保持同桥同楼，临时托住不等于修好</td><td>S06/S08/S16、T04/T15、G21与结算图</td></tr>
</tbody></table></div>
<p>镜星M12可以保留感测器与紫色候选，但尚未明确的同模母体不能由我或外援擅自补定。保留各作品家族带来的体术、重装、载具生命与航空结构气质，同时独立设计头胸、徽记和关键装备；不能只改名字/换色。</p></section>

<section class="r3-section" id="r3-examples"><h2>3. 直接看当前图：改好了什么，仍错在哪里</h2>
'''

top += case('七海：不是统一笔触就能补救换人的问题',
            'H03的短发成年女性、白外套和证件是来源；S11/U09的文字声明与实际人物矛盾。',
            fig('H03', '保留人物来源：成年女性、侧分短发、红蓝内衬白外套。', 'source') +
            fig('S11', '三格均是男性深制服。保留取证→核验→撤令顺序，人物按H03重做。', 'reject') +
            fig('U09', '“七海”变束带长发男性，纪存也换军装；功能与伪数值同样要改。', 'reject'))
top += case('白鸢：新版确实改进，旧问题不能照抄',
            'S10已经补回手套与浅色衣服；需要校正的是年龄骨相、领口与跨场景服装，而非再按旧稿一概推翻。',
            fig('H02', '来源：成年骨相、银灰卷发、交叠内搭、黑手套、分镜本。', 'source') +
            fig('S10', '手套与服色已改对；局部修成年脸与同款领口，保留阅读构图。') +
            fig('S21', '暖光和卷发可留；高褶领、少女感与旧帆船港需修，不能默认为新常服。'))
top += case('完整核心不是一只拳头，也不是无头躯干',
            '不要求所有零件都物理精密变形，但完整勇拳的头胸四肢必须能在合体中持续追认。',
            fig('F09', '本版已有完整机器人，这是进步，保留此核心身份。', 'source') +
            fig('M04', '合体轮廓与列车肩包可留；胸外甲、膝钻等需要明确外件来源。') +
            fig('F10', '第一格写F09却画两只拳/前臂块，后面不能凭空长出头胸。', 'reject') +
            fig('N14', '红无头模块、蓝腿、黄肩不是当前橙白核心；完整身体关系重做。', 'reject'), 2)
top += case('王者：冗余是要保留的特征，左右与同款装备必须改对',
            '正面中机体自身右侧对应画面左侧。不能把标签的RIGHT当作已正确；也不能把整条派生链一律镜像，因为N12的右臂钻方向已经正确。',
            fig('M05', '保留满装框架；当前钻在自身左、盾在自身右，纠正安装侧并统一封闭面罩。', 'source') +
            fig('F01', '卸装图另换白胸、长红裙甲和头肩，并不是从M05拆掉外挂后的原身体。', 'reject') +
            fig('N12', '此版是单只右钻，并非双钻；但白胸红裙、缺盾/背包仍非M05。动作顺序可留。', 'reject'))
top += case('货柜领袖：不能在变形与剧情里变成第三辆车',
            '独立化后的白深蓝橙新车值得保留。形态迁移不用逐片动画，但主要车头/轮组/货箱的去向要说得通。',
            fig('M11', '新方向可留，先说明货箱能否分离以及三轴轮组去向。', 'source') +
            fig('N13', '末行换成军绿车型；前两行人形也未沿新版雷翎/歌翼。标签不能证明同源。', 'reject') +
            fig('S19', '剧情里又是一款车，且用流程图代替了实际搬运/保护事件；保留三拍因果重新画主体。', 'reject'))
top += case('建筑：新版现代化改进要保留，而不是继续拿旧式小屋当靶子',
            '统一的是画法、复杂度与城市语汇，不是把住宅、工房、泵站、补给箱做成一个青白盒子。',
            fig('B01', '住宅有楼层、生活细节和屋顶厚度，可作为建筑完成度来源。', 'source') +
            fig('B05', '当前已经是现代平顶办公楼，不是旧评语中的坡顶砖屋。', 'source') +
            fig('B10', '新大工房有机体工位/天车，保留尺度和开口。', 'source') +
            fig('B24', '补给设备的产品分区较好，取它的功能形与材质方法，不把这组颜色复制给全城。', 'source'), 2)
top += '''</section>
<section class="r3-section" id="r3-palette"><h2>4. 一致画法，不等于同一配色；科幻感也不是蓝灯越多越好</h2>
<p>当前的配色问题主要在<strong>分布与角色分工</strong>：太多躯干、屋面、工具、界面都青白红；另一些则全黑加青红光环。这样既会把英雄和背景融在一起，也会让火、电、标定、护盾、敌意互相抢解释权。</p>
<div class="table-scroll"><table><thead><tr><th>层级</th><th>本次具体修改建议</th><th>应保留的区别</th></tr></thead><tbody>
<tr><td>机体身份色</td><td>无牌白青绿金、拳王旧白/暖甲红拳、王者深蓝白红金、预算黄黑、雷翎蓝紫、歌翼粉白各自保留；英雄色不随所在地图统一漂青。</td><td>按每台的主色面积/肩胸焦点/黑关节关系锁定，不用敌红我蓝替代身份。</td></tr>
<tr><td>同城A供能前庭</td><td><span class="r3-swatch" style="--c:#aaa994"></span>混凝土米灰为大底，<span class="r3-swatch" style="--c:#4e7778"></span>钢青设备成块，局部朱红安全件；地面不铺满青色检修板。</td><td>干燥矿物面、直立电气装置、向上缆管，供电功能易认。</td></tr>
<tr><td>同城B跨渠桥座</td><td><span class="r3-swatch" style="--c:#768f9b"></span>冷蓝灰结构与<span class="r3-swatch" style="--c:#2c6474"></span>深青水域占大色域，暖窗/少量锈橙只作聚焦，不复制A的黄米甲板。</td><td>深度、水线、岸沿和重支座的横向受力；不是另一座复古水乡。</td></tr>
<tr><td>同城C装卸站</td><td><span class="r3-swatch" style="--c:#9d947f"></span>暖灰轨道面、<span class="r3-swatch" style="--c:#687991"></span>褪蓝货柜、<span class="r3-swatch" style="--c:#ac775c"></span>少量赭/陶土货物；用有色物件而非满屏饱和地格。</td><td>轨道、货柜、调度塔与列车构成空间节奏，入口/出口方向连续。</td></tr>
<tr><td>生活街区/其他关卡</td><td>可以另定本关色域、广告/店面与生活光色；S17保留温暖但加入模型文化，S21港口保留暖光却改现代设施。</td><td>不同关不必一套工业色；同城三个区共享建筑语汇，但不是同色复制。</td></tr>
<tr><td>战术语义色</td><td>移动线绿、选中青蓝、敌意红、结果短金强调、增援预告另形状/轮次；颜色均辅以线型/符号。危险色不涂满所有墙/设备。</td><td>场景涂装是固有色；战术色按悬停/瞄准/状态出现，能清楚区分来源。</td></tr>
</tbody></table></div>
<p class="r3-small">上方色片是修改方向的近似示意，不是新增项目Canon色值，也不是要求外援把已经好的图全部重染。</p>
<h3>画法/材质必须统一到什么程度</h3>
<p>M/H中较好的<strong>压力线、清楚主色块、有限硬阴影</strong>作为共同母语。B02/B07/B08/B17/B28、E07/E10、X29的产品渲染/写实细碎高光应收回；B03过于平面则补可读材质层。统一后仍应看得出涂装甲、裸金属、混凝土、玻璃、橡胶和液体区别，不能全塑料。地形的真实厚边、凹槽、台阶和断面由低模承担，贴图负责纹理，不再用平贴纸包办所有起伏。</p>
</section>

<section class="r3-section" id="r3-scale"><h2>5. 尺寸按战棋规格统一，建筑按功能保持常识</h2>
<div class="r3-comparison cols-2">''' + fig('H13', '当前图错误：人/宠物狗1×1、标准机体2×2；机器犬也未设计。需要重做这张规格图。', 'reject') + '''
<figure class="r3-figure"><div class="r3-size-demo" role="img" aria-label="规格示意：微型约四分之一格视觉，两档单格机，王者二乘二，特例三乘三">
<div class="size-row"><span class="size-grid one"><i class="mini-piece"></i></span><p><b>微型展示</b><br>人/机器犬/导览终端<br>约¼格视觉体量</p></div>
<div class="size-row"><span class="size-grid one"><i class="unit-piece small-piece"></i></span><p><b>1×1 较小 / 标准</b><br>两档外观，不逐米缩放<br>普通敌也进入同类规格</p></div>
<div class="size-row"><span class="size-grid two"><i class="unit-piece large-piece"></i></span><p><b>2×2 大型</b><br>例如完全版王者<br>完整足迹/落位外周</p></div>
<div class="size-row"><span class="size-grid three"><i class="unit-piece giant-piece"></i></span><p><b>3×3 / 巨构特例</b><br>按任务能力安排<br>更大者可仅露局部布景</p></div>
</div><figcaption><strong>按已有用户要求重画的说明示意</strong><p>方格仅示意显示档，不新增单位模型或改逻辑占格。微型外观小不等于缩掉鼠标可点范围；标准敌不可普遍缩成小狗。</p></figcaption></figure></div>
<p><strong>楼房不应小屋化。</strong>B01–B03是可住人的现代中层楼，应和标准机甲形成可信量级；B04/B05是较矮办公服务楼，B34是人用小屋，B33是人用街具，这些无需全部放大。B18/F17则相反：若要托机体/通重载车，不能直接把人行小设施叫重载设备。规格由用途、格位和正常镜头共同校对，不按米数一比一，也不以贴“未来”招牌解决功能比例。</p>
</section>

<section class="r3-section" id="r3-interface"><h2>6. UI、图标、效果：分工统一后，才会像同一个游戏</h2>
<p><strong>U19做共件语言，U05/U06做信息组织，不能将20张设计说明板同时搬进HUD。</strong>常态只留主目标、工作面、可行动机体与少量动作；随着光标探索出现对象摘要，瞄准时出现轨迹、位移/碰撞、预计掉血与取消的威胁，回合末才展开敌方/环境预告。生图中的假型号、等级、命中百分比、SSR、人物姓名都不是新机制。</p>
<div class="r3-comparison cols-2">''' + fig('G16', '当前白色满楼高笼子仍不符合要求；应改标准高度红色透明矮墙，受真实3D深度遮挡。', 'reject') + '''
<figure class="r3-figure"><svg class="r3-wall-demo" viewBox="0 0 640 360" role="img" aria-labelledby="wall-title wall-desc">
<title id="wall-title">目标光墙与建筑深度关系示意</title><desc id="wall-desc">红色目标墙只围脚印，低于楼体，远边被建筑遮住；近边透明，伤害条独立。</desc>
<rect width="640" height="360" fill="#e9eee9"/><path d="M80 267 342 171 564 257 305 348Z" fill="#b9c4bb"/>
<path d="M137 242 342 167 507 230 305 307Z" fill="#ddd9c8" stroke="#899b95" stroke-width="2"/>
<path d="M137 242v-59l205-75v59Z" fill="#da5c4b" fill-opacity=".2" stroke="#c94b3f" stroke-width="3"/>
<path d="M342 167v-59l165 63v59Z" fill="#da5c4b" fill-opacity=".2" stroke="#c94b3f" stroke-width="3"/>
<path d="M235 120 342 81 434 115 327 157Z" fill="#9eaa9f" stroke="#374c58" stroke-width="3"/>
<path d="M235 120v133l92 35V157Z" fill="#56777b" stroke="#374c58" stroke-width="3"/>
<path d="M327 157v131l107-40V115Z" fill="#365b66" stroke="#374c58" stroke-width="3"/>
<g stroke="#b9d1cd" stroke-width="7"><path d="m251 156 60 23m-60 6 60 23m-60 6 60 23"/><path d="m344 181 73-28m-73 57 73-28m-73 57 73-28"/></g>
<path d="M137 242v-59l168 65v59Z" fill="#e26956" fill-opacity=".28" stroke="#c94b3f" stroke-width="3"/>
<path d="M305 307v-59l202-77v59Z" fill="#e26956" fill-opacity=".2" stroke="#c94b3f" stroke-width="3"/>
<path d="M70 114 171 157" stroke="#c94b3f" stroke-width="5" stroke-dasharray="9 6"/><path d="m162 146 17 14-22 0" fill="#c94b3f"/>
<text x="34" y="52" fill="#244651" font-size="21">标准高度围脚印，不沿楼脸画线</text>
<text x="38" y="91" fill="#a34035" font-size="17">目标/方向/落点由规则生成</text>
<rect x="451" y="48" width="154" height="47" rx="5" fill="#173341"/><g fill="#e7ece7"><rect x="464" y="60" width="20" height="22"/><rect x="489" y="60" width="20" height="22"/></g><g fill="#e47b68"><rect x="514" y="60" width="20" height="22"/><rect x="539" y="60" width="20" height="22"/></g><path d="m514 80 19-18m6 18 19-18" stroke="#fff1dd" stroke-width="2"/><text x="572" y="77" fill="#f3d8ba" font-size="16">−2</text>
</svg><figcaption><strong>修改示意：同一套世界空间共件</strong><p>不要求与建筑通高。选择该敌/目标时加强红矮墙、弹道和预计损失；常态退为小标。此图说明设计关系，不冒充实机验证。</p></figcaption></figure></div>
<h3>图标先统一轮廓与语义，而非统一加青红圆环</h3>
<p>I组混了黑底霓虹人体、写实金框、白底几何、产品小插画。建议沿<strong>I04/I09/I12/I13/I15</strong>的单一清楚主形，统一笔画/留白/底板；每个功能用自己的动词形状。普通光束到首体停，贯穿必须穿过多个实体；空撞不能画成两个导弹对撞；变形不能变成无来源车轮；分离要保留完整核心。逐项意见已写到I01–I65，不以总评代替每项修改。</p>
<h3>动作与效果统一制作方法，不做两两命中调参</h3>
<p>N组画的是关键姿态参考，不是已经有了动画。走跑、射击、受击、操作设备先用共享家族；无牌天冲拳、拳王拳击及必要招牌动作定制。工具与武器用通用挂点/轴/规格参数，命中事件到来后攻击者、目标、建筑、地面各自处理状态。X组提取形状/时序，C组表达持续状态，G组画规则后果，三者不可互相替代或凭美术新增伤害。</p>
</section>

<section class="r3-section" id="r3-handoff"><h2>7. 怎么真正用到项目里</h2>
<div class="table-scroll"><table><thead><tr><th>接入去向</th><th>这批可提供什么</th><th>下一步具体制作</th></tr></thead><tbody>
<tr><td>单位与装备</td><td>通过同源修正后的M/E/F设计，保留各机体谱系与英雄色</td><td>先审实际源图与主要前侧背结构→低模→UV/图像投射后重绘贴图→必要绑定→共享动作适配；不能把带背景方向图直接当UV或GLB。</td></tr>
<tr><td>楼房/设施/列车</td><td>B/T的现代体量、材质层与功能轮廓</td><td>图像设计指导低模，厚边/凹槽/断面建实体，细窗/铭板用纹理。门闸、转台、吊臂、轮轴只做必要运动，列车简单移动，不做人物骨架。</td></tr>
<tr><td>人物/剧情图片</td><td>H与同源S图，保留构图和人物吸引力</td><td>沿冻结人像出同尺度头肩/半身与少量表情；事件图按准备—动作—结果拆少量层，微动/光色强调因果，无需每段做视频或重新设计人物。</td></tr>
<tr><td>战术UI/效果</td><td>U布局、I语义、G空间标记、X/C形状与时序</td><td>实际控件/矢量或材质共件重建，不用整张设计板作HUD。动态文字、血格、范围、路径来自同一预测/执行事件，减少动态保留含义。</td></tr>
</tbody></table></div>
<p><strong>修改顺序：</strong>先纠正母版与规则误解（馆守左右、王者左右/装备、完整核心、载具大件、微型规格、七海）；再将相关S/N/F/U派生图一次校回来源；随后统一材质、图标与区域配色。无需将好的母版重新抽图，也无需为每台标准走路/每对接触单独开发。</p>
<p><strong>推广前看一组真实同场样例：</strong>正常战棋镜头中同时放一个我方标准机、一个普通敌、一个2×2大机、现代住宅、供电件与微型人物，分别看关HUD/常态/悬停/瞄准/损坏。检查轮廓、楼机比例、材质、颜色主次、头像、受击与落位；没有解决主要缺陷就回到对应源图/结构，不靠加描边、改曝光或继续堆细节。</p>
<p class="r3-small">本轮完成的是当前交付的设计评审与读页修复，未替换主工程资产、未改Canon和原52包实施状态。正式制作/运行验收沿原台账继续，不能用这页93个A来宣称93件已进入游戏。</p>
</section>

<section class="r3-section" id="r3-rework"><h2>8. 需要优先退改的28项：原因与改法逐条可查</h2><div class="table-scroll"><table><thead><tr><th>条目</th><th>当前主要问题</th><th>本次具体修改</th></tr></thead><tbody>'''
for n in notes:
    if n['verdict'] == 'C':
        top += (f'<tr><td><a href="#{n["id"]}">{n["id"]} {esc(items[n["id"]]["name"])}</a></td>'
                f'<td>{esc(n["problem"])}</td><td>{esc(n["change"])}</td></tr>')
top += '</tbody></table></div><p>其余177项B类也都有独立修改意见；不是被省略或默认为可以直接进游戏。</p></section>'
top += '<details class="r3-section"><summary>各组本轮数量与含义</summary><div class="table-scroll"><table><thead><tr><th>组</th><th>A 沿用方向</th><th>B 修改后用</th><th>C 主体/语义重做</th></tr></thead><tbody>'
for g, c in group_counts.items():
    top += f'<tr><td><a href="#group-{g}">{g}</a></td><td>{c["A"]}</td><td>{c["B"]}</td><td>{c["C"]}</td></tr>'
top += '''</tbody></table></div></details>
<p class="r3-small">来源：当前页面逐项实际图文件；<a href="../../docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate/外援美术制作清单-20261012/index.html">原298项任务与背景/IP映射</a>；<a href="../../docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate/v5完整整改计划-20261008/给Astra的视觉总参考.html">用户视觉总参考</a>；当前Canon查询与用户最新尺寸/复用/事件要求。可对照<a href="review/20261015-latest-review/current-file-inventory.json">检查前图文件清单</a>、<a href="review/20261015-latest-review/latest-review-data.json">本轮逐项意见</a>与<a href="review/20261015-latest-review/before-review-r3-20261015.html">修改前完整页面快照</a>。该快照在子目录，需与原目录上下文核对旧相对图链；本页历史意见已就地保留。</p>
</section>
'''

css = '''
/* r3 current review: original imagery and historical r2 comments remain intact. */
.r3-kicker{font-size:12px;letter-spacing:.07em;color:#55727b;font-weight:750}.r3-intro>h2{font-size:29px;line-height:1.4;max-width:1100px}.r3-lead{font-size:17px;line-height:1.9}.r3-small{font-size:12px;color:#5a6e76;line-height:1.8}.r3-counts{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0}.r3-counts>a{padding:12px 18px;border:1px solid currentColor;border-radius:7px;background:#fffef9;text-decoration:none}.r3-counts b{font-size:25px;display:inline-block;margin-right:7px}.r3-alert{margin:22px 0;padding:16px 20px;border-left:5px solid #b97a2a;background:#f6ebd4;line-height:1.85}.r3-section{border-top:2px solid #d3ded7;margin-top:32px;padding-top:24px;scroll-margin-top:100px}.r3-section>h2{font-size:23px;margin:0 0 14px}.r3-section h3{font-size:18px}.r3-section p{line-height:1.85}.r3-section table{width:100%;border-collapse:collapse;table-layout:auto}.r3-section th,.r3-section td{padding:13px 12px;vertical-align:top;border:1px solid #ccd8d1;min-width:110px}.r3-section th{background:#e7eee8;text-align:left}.r3-section td:first-child{min-width:145px;font-weight:650}.r3-section tbody tr:nth-child(even){background:#f7f6ef}.r3-decision-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.r3-decision-grid>div{border:1px solid #cbd9d0;background:#f6f7ef;padding:8px 20px;border-radius:7px}.r3-case{margin:28px 0}.r3-case>h3{border-left:4px solid #176b73;padding-left:11px}.r3-comparison{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px;align-items:start}.r3-comparison.cols-2{grid-template-columns:repeat(2,minmax(0,1fr))}.r3-figure{margin:0;border:1px solid #cdd7d0;border-top:4px solid #a18a58;background:#fafaf3;border-radius:6px;overflow:hidden;min-width:0}.r3-figure.source{border-top-color:#34755c}.r3-figure.reject{border-top-color:#c15443}.r3-figure>a{display:block;background:#e7e9df}.r3-figure img{display:block;width:100%;height:auto;object-fit:contain}.r3-figure figcaption{padding:13px;line-height:1.75}.r3-figure figcaption p{margin:7px 0}.r3-figure small{display:block;overflow-wrap:anywhere;color:#61717b;font-size:11px}.r3-swatch{display:inline-block;width:18px;height:18px;border-radius:3px;background:var(--c);border:1px solid #82918c;vertical-align:middle;margin:0 3px}.r3-size-demo{padding:18px;background:#e5eae5;display:grid;grid-template-columns:1fr 1fr;gap:16px;min-height:288px}.size-row{display:flex;gap:12px;align-items:center}.size-row p{font-size:12px;margin:0;line-height:1.6}.size-grid{flex:none;display:block;position:relative;background:repeating-linear-gradient(0deg,transparent 0 27px,#879b9d 27px 28px),repeating-linear-gradient(90deg,transparent 0 27px,#879b9d 27px 28px);border:1px solid #879b9d}.size-grid.one{width:56px;height:56px;background-size:56px 56px}.size-grid.two{width:84px;height:84px;background-size:42px 42px}.size-grid.three{width:90px;height:90px;background-size:30px 30px}.mini-piece{position:absolute;width:11px;height:23px;bottom:10px;left:20px;background:#8c6560;border-radius:7px 7px 3px 3px}.unit-piece{position:absolute;background:#337489;clip-path:polygon(32% 0,68% 0,72% 16%,100% 23%,90% 69%,76% 69%,76% 100%,55% 100%,50% 72%,45% 100%,24% 100%,24% 69%,10% 69%,0 23%,28% 16%)}.small-piece{width:32px;height:42px;bottom:5px;left:11px}.large-piece{width:65px;height:69px;bottom:7px;left:9px;background:#b47d3f}.giant-piece{width:75px;height:76px;bottom:6px;left:6px;background:#776281}.r3-wall-demo{width:100%;height:auto;display:block}.history-intro{max-width:1368px;margin:20px auto;padding:14px 18px;border:1px dashed #b7c5bd;background:#eaece4}.history-intro>summary,.r3-history>summary{cursor:pointer;font-size:13px;font-weight:650;color:#687870}.history-intro .review-intro{margin:15px 0}.r3-history{margin-top:14px;border-top:1px dashed #ccd4ca;padding-top:10px}.r3-history .assessment{font-size:12px;line-height:1.7}.r3-history .family-review{font-size:12px}.r3-history .review-verdict{font-size:12px}.r3-history-notice{font-size:12px;line-height:1.7;color:#705f43;background:#f3eddf;padding:10px}.r3-binding{font-size:11px;color:#5e7279;overflow-wrap:anywhere;background:#edf2ed;padding:8px 10px;border-radius:4px;margin:5px 0 10px}.r3-tags{display:flex;flex-wrap:wrap;gap:5px;margin:7px 0}.r3-tags span{background:#e9eee6;padding:2px 6px;border:1px solid #d0d9cd;border-radius:4px;font-size:11px;color:#536a70}.r3-assessment{margin:10px 0}.r3-assessment dt{font-weight:750;color:#244955;margin-top:12px;font-size:13px}.r3-assessment dd{margin:4px 0 0;font-size:14px;line-height:1.85}.r3-production{margin-top:14px;background:#eef2eb;padding:10px;border-radius:4px;font-size:12px;line-height:1.8}.r3-production summary{cursor:pointer;font-weight:650}.r3-card-current{display:block}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.thumb img{object-fit:contain}.meta{padding:16px 18px}.review-intro{max-width:1368px}.review-verdict{margin-top:10px}.card{scroll-margin-top:115px}.source-status{font-size:11px;color:#6d7c7b}.r3-reset{font:inherit;padding:7px 10px;background:#edf2eb;border:1px solid #b9c9c3;border-radius:4px;cursor:pointer}.review-controls select{max-width:100%}#r3-issue-filter{min-width:160px}
@media(max-width:1050px){.r3-comparison{grid-template-columns:repeat(2,minmax(0,1fr))}.r3-intro>h2{font-size:25px}.r3-size-demo{grid-template-columns:1fr}.r3-section th,.r3-section td{padding:10px}}
@media(max-width:800px){.grid{grid-template-columns:1fr}.r3-decision-grid{grid-template-columns:1fr}.review-controls{position:relative}.r3-section{scroll-margin-top:14px}.card{scroll-margin-top:14px}.r3-section table{font-size:12px}.r3-counts>a{flex:1;min-width:180px}.r3-intro>h2{font-size:22px}.r3-lead{font-size:15px}}
@media(max-width:600px){.r3-comparison,.r3-comparison.cols-2{grid-template-columns:1fr}.r3-size-demo{grid-template-columns:1fr 1fr;padding:12px;gap:12px}.size-row{display:block}.size-row p{margin-top:7px}.r3-section>h2{font-size:20px}.r3-section td:first-child{min-width:105px}.meta{padding:14px}.r3-intro{padding:16px}.r3-figure figcaption{padding:12px}}
@media print{.history-intro,.r3-history,.r3-reset{display:none}.r3-section{break-inside:auto}.r3-figure{break-inside:avoid}.r3-comparison{grid-template-columns:repeat(2,minmax(0,1fr))}.r3-counts>a{color:#1a2a32}}
'''

css += '''
.r3-production{overflow-wrap:anywhere}.size-grid{background-image:linear-gradient(0deg,#879b9d 1px,transparent 1px),linear-gradient(90deg,#879b9d 1px,transparent 1px)}.mini-piece{width:22px;height:28px;left:16px;bottom:10px}
'''
top = top.replace('review/20261015-latest-review/before-review-r3-20261015.html',
                  'review/20261015-latest-review/before-review-r3-reader.html').replace(
    '该快照在子目录，需与原目录上下文核对旧相对图链；本页历史意见已就地保留。',
    '不可变源快照另行保存；本页历史意见已就地折叠保留。')
top = top.replace('旧r2文字单独折叠保留。', '本轮图像已保存逐字节相同的固定副本，后续incoming来稿更新不会静默换掉已评图片；旧r2文字单独折叠保留。')

handoff = {
    'M': '下一步：同源结构图指导低模/UV/贴图与必要骨架；标准动作家族适配，专属体术另做。当前方向图不是3D单位。',
    'H': '下一步：沿同脸同衣装出头肩/半身与少量表情，统一眼线和头高；文字另排。微型战棋人物使用相应显示档。',
    'E': '下一步：同源低模/UV与角色规格，必要准备/移动/攻击/受击状态；常规受击共享，不逐对制作接触。',
    'F': '下一步：沿修正母机提取同款部件与安装轴，必要收放状态；不把分件条目当重新设计另一台机体。',
    'B': '下一步：图像设计指导低模与UV贴图，厚边/断面建实体，细节用纹理；只给必要门轴/轮轴/转台运动。',
    'S': '下一步：人物/机体/设施对回母版，按事件拆少量独立层与状态；微动突出行动后果，文字/选择在游戏排。',
    'X': '下一步：提取特效形状与时序，效果/主体/背景分开；由事件与挂点驱动，不把整张插画当运行序列。',
    'G': '下一步：按规则生成世界/屏幕空间共件，动态格位/线/数值不烘焙；本图是表达示意而非实际命令结果。',
    'C': '下一步：局部覆盖层与原模型有限状态，关键缺件独立；持续/退出和瞬发分开，取同一规则结果。',
    'U': '下一步：采用可用版式重建真实控件，共用U19字阶/边角/状态；假人物/任务/数值不进入游戏机制。',
    'I': '下一步：统一图标轮廓/线宽/留白与U19底板；不带标签/编号/假透明棋盘格，实际小尺寸检查语义。',
    'T': '下一步：低模表达厚度/凹槽/断面，纹理表达材质；区域色域可不同，危险/可走范围来自规则。',
    'N': '下一步：沿真实母机重定向共享动作，必要招牌定制；攻击者/目标/设备各自响应事件，连续过程另验。',
}
current_records = []
def replace_card(match):
    card = match.group(0)
    i = re.search(r'data-id="([^"]+)"', card).group(1)
    r, n, old = items[i], by_id[i], old_records[i]
    group, verdict = r['group'], n['verdict']
    source_status = re.search(r'<span class="source-status"[^>]*>([\s\S]*?)</span>', card)
    source_status = source_status.group(1) if source_status else '制作者原标记'
    source_state = re.search(r'data-status="([^"]+)"', card).group(1)
    purpose = re.search(r'<p class="purpose">([\s\S]*?)</p>', card).group(1)
    spec = re.search(r'<details class="original-spec">[\s\S]*?</details>', card)
    original_spec = spec.group(0) if spec else ''
    hist_parts = []
    for pattern in (r'<div class="review-verdict[^>]*>[\s\S]*?</div>',
                    r'<dl class="assessment">[\s\S]*?</dl>',
                    r'<aside class="family-review">[\s\S]*?</aside>',
                    r'<details class="technical-spec">[\s\S]*?</details>'):
        hit = re.search(pattern, card)
        if hit:
            hist_parts.append(hit.group(0))
    was_pref = re.search(r'data-user-pref="([^"]+)"', card).group(1)
    tag_html = ''.join(f'<span>{tag_labels[t]}</span>' for t in n['tags'].split(','))
    changed = i in changed_ids
    binding = (f'本次实际查看：{Path(r["file"]).name} · {r["size"][0]}×{r["size"][1]} RGB JPEG · 已绑定本轮固定副本'
               + (' · 比旧记录已换图' if changed else ' · 文件与旧记录一致'))
    search = ' '.join([i, r['name'], verdict, labels[verdict], n['use'], n['problem'], n['change'],
                       n['related'], n['tags'], *(tag_labels[t] for t in n['tags'].split(','))])
    current_records.append(dict(
        id=i, group=group, name=r['name'], img=r['preview_file'], source_img=r['file'], size=r['size'], mode='RGB',
        image_sha256=r['sha256'], verdict=verdict, use=n['use'], content=n['problem'],
        revision=n['change'], related=n['related'].split(','), issue_tags=n['tags'].split(','),
        technical=handoff[group], design_review_only=True, changed_since_r2=changed,
        previous_record_img=old.get('img'), previous_record_sha256=old.get('image_sha256'),
        previous_verdict=r['card_verdict_before'], original_source_pref=was_pref == 'true',
        required_files=old.get('required_files', []), required_states=old.get('required_states', []),
        inspection='组内全部逐图联系表检查；关键母版/派生原图放大对照；未宣称运行或源文件齐套验收。'))
    requirements = ' / '.join(old.get('required_files', []))
    return (f'<article class="card" data-group="{group}" data-id="{i}" data-status="{esc(source_state)}" '
            f'data-verdict="{verdict}" data-user-pref="{was_pref}" data-changed="{str(changed).lower()}" '
            f'data-issues="{esc(n["tags"])}" data-current-search="{esc(search)}" id="{i}">'
            f'<a class="thumb" href="{esc(r["preview_file"])}" target="_blank" rel="noopener"><img src="{esc(r["preview_file"])}" '
            f'alt="{i} {esc(r["name"])} 当前交付" loading="lazy" width="1280" height="720"></a>'
            '<div class="meta"><div class="r3-card-current"><div class="row1">'
            f'<span class="id">{i}</span><span class="source-status" title="沿用制作者旧标签，不是本次认可">{source_status}</span></div>'
            f'<h3 class="name">{esc(r["name"])}</h3><p class="purpose">{purpose}</p>'
            f'<div class="r3-binding">{esc(binding)}</div><div class="review-verdict rv-{verdict}">{verdict} · {labels[verdict]}</div>'
            f'<div class="r3-tags">{tag_html}</div><dl class="r3-assessment"><dt>可以保留 / 用到哪里</dt><dd>{esc(n["use"])}</dd>'
            f'<dt>当前实际图面的问题</dt><dd>{esc(n["problem"])}</dd><dt>具体修改意见</dt><dd>{esc(n["change"])}</dd></dl>'
            f'<p class="review-links"><strong>必须一起对齐：</strong>{links(n["related"])}</p></div>'
            f'<details class="r3-production"><summary>如何进入项目制作 / 当前文件绑定</summary><p>{esc(handoff[group])}</p>'
            '<p>本轮是单张方向稿评审。以下原项完整制作清单用于后续分工，不据此要求每张方向图现在就补全模型或源文件。</p>'
            f'<p>原项文件位：{esc(requirements)}</p><p>本轮固定图：<a href="{esc(r["preview_file"])}">查看固定副本</a><br>来稿源路径：{esc(r["file"])}<br>'
            f'SHA-256：<code>{r["sha256"]}</code></p></details>'
            f'<p class="review-links"><a href="../../docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate/外援美术制作清单-20261012/index.html#{i}" target="_blank" rel="noopener">核对原派单 {i}</a></p>'
            + original_spec +
            '<details class="r3-history"><summary>历史r2意见（不用于当前图判定）</summary>'
            f'<p class="r3-history-notice">旧记录绑定：{esc(old.get("img", "未记录"))}。本页之前更换预览但未同步部分文字/链接，'
            '以下原文保留供追溯；当前图是否已修好，以本卡上方r3意见为准。</p>'
            + ''.join(hist_parts) + '</details></div></article>')

# Save complete r2 intro within an explicitly historical details element.
intro_match = re.search(r'<section class="review-intro" id="review-summary">[\s\S]*?</section>\s*<main>', source)
assert intro_match
old_intro = intro_match.group(0).rsplit('<main>', 1)[0]
intro_ids = re.findall(r'id="([^"]+)"', old_intro)
for ident in intro_ids:
    old_intro = old_intro.replace(f'id="{ident}"', f'id="history-r2-{ident}"').replace(
        f'href="#{ident}"', f'href="#history-r2-{ident}"')
historical_intro = ('<details class="history-intro" id="history-r2"><summary>展开：旧r2总评与旧改判记录（历史，不适用新版）</summary>'
                    '<p class="r3-history-notice">原文包含已被新版修正的问题，且曾与更新后的预览图混用。'
                    '仅保留评审历史，不把这里的否决或“用户确认”叙述当作本轮新决定。</p>' + old_intro + '</details>')
page = source[:intro_match.start()] + top + historical_intro + '<main>' + source[intro_match.end():]
page = re.sub(r'<article\b[^>]*>[\s\S]*?</article>', replace_card, page)
assert len(current_records) == 298
page = page.replace('</style>', css + '\n</style>', 1)
page = re.sub(r'<title>.*?</title>', '<title>超GAG 外援最新交付复核 r3 · 298项逐图意见</title>', page, count=1)
page = re.sub(r'<h1>.*?</h1>', '<h1>超GAG 外援美术 · 最新交付复核 r3</h1>', page, count=1)
page = page.replace('本次逐图评审：2026-10-15 · 复审r2：同源 / IP谱系 / 机甲科幻时代（Asia/Shanghai）',
                    '最新复核：2026-10-15 · r3：当前文件 / 同源 / 功能 / 配色 / 画法（Asia/Shanghai）')
page = re.sub(r'<div class="summary">[\s\S]*?</div>',
              f'<div class="summary">当前 <strong>298条 / 295张独立图</strong> · '
              f'A 沿用方向 {counts["A"]} / B 修改后用 {counts["B"]} / C 主体或语义重做 {counts["C"]}'
              '<br>逐项下方已补r3意见；制作者done / locked不代表本次认可。</div>', page, count=1)
page = page.replace('采用设计 · 补齐制作件</option>', 'A 建议沿用设计方向</option>').replace(
    '局部采用 · 修改/补全</option>', 'B 保留并具体修改</option>').replace(
    '返工 · 保留可取局部</option>', 'C 主体或核心语义重做</option>').replace(
    '用户偏好 / 明确保留来源</option>', '原页面保留来源</option>')
page = page.replace('<option value="PREF">', '<option value="CHANGED">只看换过图的87项</option><option value="PREF">', 1)
issue_options = '<option value="ALL">所有问题类型</option>' + ''.join(
    f'<option value="{k}">{v}</option>' for k, v in tag_labels.items())
page = page.replace('<span id="review-visible-count"',
                    '<label for="r3-issue-filter">问题</label><select id="r3-issue-filter">' + issue_options +
                    '</select><button type="button" class="r3-reset" id="r3-reset">清除筛选</button><span id="review-visible-count"', 1)
page = page.replace('显示 298 / 298 张', '显示 298 / 298 项')
def group_heading(match):
    g, heading = match.group(1), match.group(0)
    c = group_counts[g]
    return re.sub(r'<span class="gcount">.*?</span>',
                  f'<span class="gcount">本组{sum(c.values())}项 · A {c["A"]} / B {c["B"]} / C {c["C"]}</span>', heading)
page = re.sub(r'<section class="group" data-group="([A-Z])"[^>]*><header class="ghead">[\s\S]*?</header>', group_heading, page)
page = re.sub(r'<p class="foot">[\s\S]*?</p>',
              '<p class="foot">2026-10-15 最新交付复核r3 · 298项、295张独立图逐项检查。原图未改，旧r2总评与卡片意见折叠保留。'
              '搜索只检索当前意见，点击图片打开同一当前文件；原rebuild.py不能用无评审/旧文件数据覆盖本页。'
              '这是设计评审，不宣称主工程已替换、完成52包或新增用户认可。</p>', page, count=1)

script = r'''
(function(){
 const tabs=[...document.querySelectorAll('.tab')],groups=[...document.querySelectorAll('.group')],cards=[...document.querySelectorAll('.card')];
 const search=document.getElementById('review-search'),filter=document.getElementById('review-verdict-filter'),issue=document.getElementById('r3-issue-filter'),counter=document.getElementById('review-visible-count');
 let activeGroup='ALL';
 function apply(){
  const q=search.value.trim().toLowerCase(),v=filter.value,k=issue.value,exactId=/^[mhefbsxgcuitn]\d{2}$/i.test(q);let count=0;
  for(const c of cards){const show=(activeGroup==='ALL'||c.dataset.group===activeGroup)&&(v==='ALL'||c.dataset.verdict===v||(v==='PREF'&&c.dataset.userPref==='true')||(v==='CHANGED'&&c.dataset.changed==='true'))&&(k==='ALL'||c.dataset.issues.split(',').includes(k))&&(!q||(exactId?c.dataset.id.toLowerCase()===q:c.dataset.currentSearch.toLowerCase().includes(q)));c.hidden=!show;if(show)count++;}
  for(const g of groups)g.hidden=![...g.querySelectorAll('.card')].some(c=>!c.hidden);
  for(const t of tabs){const chosen=t.dataset.group===activeGroup;t.classList.toggle('active',chosen);t.setAttribute('aria-pressed',String(chosen));}
  counter.textContent='显示 '+count+' / 298 项';
 }
 function clear(){activeGroup='ALL';search.value='';filter.value='ALL';issue.value='ALL';apply();}
 for(const t of tabs)t.addEventListener('click',()=>{activeGroup=t.dataset.group;apply();});search.addEventListener('input',apply);filter.addEventListener('change',apply);issue.addEventListener('change',apply);document.getElementById('r3-reset').addEventListener('click',clear);
 function focusHash(){const id=decodeURIComponent(location.hash.slice(1));if(!id)return;const e=document.getElementById(id);if(!e)return;for(let p=e.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;if(e.classList.contains('card')||e.classList.contains('group')){activeGroup=e.dataset.group;search.value='';filter.value='ALL';issue.value='ALL';apply();}requestAnimationFrame(()=>e.scrollIntoView({block:'start'}));}
 window.addEventListener('hashchange',focusHash);apply();focusHash();
})();
'''
# Replace just the ordinary script, preserving old JSON separately below.
page = re.sub(r'<script>\s*\(function\(\)\{[\s\S]*?</script>', lambda _: '<script>' + script + '</script>', page, count=1)
source_files = [
    ROOT / 'style-lock/STYLE.md', ROOT / '_meta/identity-slim.json',
    Path('docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate/外援美术制作清单-20261012/README.md'),
    Path('docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate/v5完整整改计划-20261008/给Astra的视觉总参考.html'),
    Path('docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv'),
    Path('docs/superpowers/specs/data/canon/entities.tsv'),
]
data = dict(reviewed_at=today, timezone='Asia/Shanghai', review_revision='r3-current-file-review',
            scope='298 current task cards / 295 unique direction images', status='design_review_only',
            parent_review_page_sha256=sha(BACKUP.read_bytes()), notes_sha256=sha((OUT / 'review-notes-r3.tsv').read_bytes()),
            source_files_sha256={str(p): sha(p.read_bytes()) for p in source_files}, verdict_counts=dict(counts),
            changed_since_r2=changed_ids, changed_count=len(changed_ids), duplicate_image_groups=duplicates,
            user_feedback_basis='User broadly prefers style; palette/design-specific acceptance excluded; no new individual user acceptance inferred.',
            original_source_preference_scope='Retains prior page tags as historical source choices, not new acceptance.',
            current_image_files_unchanged=True, reviewed_images_frozen=True, runtime_assets_replaced=False, canon_changed=False,
            production_flow_status_changed=False, records=current_records)
encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
page = re.sub(r'<script type="application/json" id="asset-review-data">[\s\S]*?</script>',
              lambda _: '<script type="application/json" id="asset-review-data">' + encoded + '</script>', page, count=1)
review_day = today[:10]
page = page.replace('2026-10-15 · 当前交付复核 r3',
                    f'2026-10-15开始核对 · {review_day}更新 · 当前交付复核 r3').replace(
    '最新复核：2026-10-15 · r3', f'最新复核：{review_day} · r3').replace(
    '2026-10-15 最新交付复核r3', f'{review_day} 最新交付复核r3')

# This check protects a concurrently revised page, not just the initially inspected version.
if PAGE.read_bytes() != live_before:
    raise SystemExit('Concurrent page edit detected; no overwrite performed.')
tmp = PAGE.with_suffix('.r3-tmp.html')
tmp.write_text(page)
tmp.replace(PAGE)
(OUT / 'latest-review-data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
(OUT / 'r3-build-result.json').write_text(json.dumps(dict(
    reviewed_at=today, count=len(current_records), unique_images=len(groups), verdict_counts=dict(counts),
    changed_records=len(changed_ids), page_sha256=sha(PAGE.read_bytes()),
    original_page_sha256=sha(BACKUP.read_bytes()), duplicates=duplicates,
    image_files_unchanged=True, runtime_integration=False), ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(page=str(PAGE), counts=dict(counts), reviewed=len(current_records),
                      unique_images=len(groups), changed_records=len(changed_ids)), ensure_ascii=False))
