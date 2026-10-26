# 141 · 公式台当前开发停点

更新：2026-09-09。工作区 `/Users/rayz/Documents/超gag机器人大战`；分支 `codex/srw-kernel-sandbox`。
**Candidate / not_canon / user_visual_acceptance=false；140 总目标仍进行中。**
旧交接已归档到 [_history/141-before-hp-alpha-2026-09-09.md](_history/141-before-hp-alpha-2026-09-09.md)。本文件只记录当前状态，不重载旧对话。

## 1. 接手顺序与授权

1. 完整读本文件与 [140 唯一执行目标](140-formula-lab-integrated-visual-production-goal.md)。137 制作框架、138 §2.3 七公式融合与逐公式参考按需查；不把 E/F 增量当七公式收口。
2. `chao-gag-canon` 边界已核验，C04 正式剧情生产链分开。保留大量共享修改/未跟踪文件，不 add/commit/reset/清理。
3. **HP 回执、第二轮运动录制、三张 alpha 修复已完成，不能按旧交接重做。** 先看 §3 当前证据和下一项，不把测试 PASS 当声画验收。
4. 用户明确批准紫机、白青机、靶机三张原图的本地蒙版修复。原 RGB 逐像素保留、仅 alpha；无付费、新身份/姿态、失败分件复用或正式美术验收授权。紫/白青同身份已接入，靶机单独保存。
5. E 挑战者与 F 灰色拦机实际为第四张 `mecha-si.png`；F 另一敌机保留金色既有图。不得用已修 `mecha-doll` 代替。灰炮机补充透明许可已提出，**尚未答复**，不得推定批准。
6. 模型按 140 §8.1 的质量与总消耗选择。当前 subagent 接口无 Spark；简单审计使用 Luna，发现来源解析不胜任后一次升级 Sol 修正，避免无限试错。复杂回执/代码 Sol，运动像素 Terra，Root 整合与最终判断。

金标仍为必做项：机战 Y／陷阵之志；金偶像／Obra Dinn；Outer Wilds；XCOM 2／Banner Saga；机战30；Citizen Sleeper／风花雪月／Hades。GF 是项目内效果图，开源实现不是商业体验参考。具体公式开工须把已核验参考帧、融合取舍和真实操作产物对照；不得用静帧证明未看过的交互/声音。

## 2. 当前入口：不要打开旧版本误判进度

唯一显式目录：`artifacts/formulas/production-lab-v1/current-packages.json`。
下表均相对 `artifacts/formulas/production-lab-v1/builds/`：

| 包 | 当前 flow.json 所在目录 | 已接上的体验 / 未完成 |
| --- | --- | --- |
| A | package-a-briefing-v1 | 实际试验现场前言→调查→同场结果对白；角色/完整声画未过 |
| B | package-b-onsite-v2 | 承力/交割试验→按实际成功、中止、未开始回应；非检查清单 |
| C | package-c-exploration-actors-v1 | 器材棚走近/观察/问人→路线计划对白；人物规格/动作未过 |
| D | package-d-exploration-actors-v1 | 跨三个空间观察→回台归档→路线计划；与 C 不是换地名 |
| E | package-e-registered-map-v1 | T0 7×5 固定擂台：注册场景→事件执行→真实结算 |
| F | package-f-registered-map-v1 | T2 9×5 限时穿越：注册通道→动态阻挡/撤出→真实结算 |
| G | package-g-environment-v2 | 地区图派巡访员→同源几何器材棚→实际报告；箱前/箱后深度遮挡已实录复核，后续队伍未出发 |
| H | package-h-environment-v1 | 同源旧仓三室→真实行走/归档开路→报告；窗口呈现与知识指向已定向修复 |
| I | package-i-hub-in-room-v1 | 自然返馆、走近闲聊/工作、一次提交、同室看后果 |
| J | package-j-hub-review-v1 | 真实试验约束复核，提交后原书页划出结论范围；同室查看与受阻原因已实玩修正 |

统一浏览器（仓库根目录）：

```sh
/opt/homebrew/bin/godot --path game-godot res://scenes/formula_lab/formula_lab_package_browser.tscn
```

直接包入口：

```sh
/opt/homebrew/bin/godot --path game-godot --windowed --resolution 1280x720 res://scenes/formula_lab/formula_lab_package.tscn -- --package "/Users/rayz/Documents/超gag机器人大战/artifacts/formulas/production-lab-v1/builds/package-e-registered-map-v1/flow.json"
```

重建用各包 `REBUILD.txt` 与 `source-map.json` 的真实输入；生成器 `scripts/formula_production_lab.py`，外层 `scripts/formula-desk`，走 `--candidate-lab`。输出用新目录，不能覆盖来源或抬升正式冻结门。

当前仍是受限模板组合、十份目录包，不是任意 Reader/地图编译器。G/H 仅先遣到场，不等于整队/重机旅行；新WR_T1/T2双路线生产夹具已在QA接通首次派遣→真实选中目的地，下一周期与所有下游消费未全部接入。全部预设覆盖、第二输入质量和编辑生产能力仍须按140继续扩展。

## 3. 已完成的工程与真实证据

完整审核索引：[ROUND-REVIEW.md](../../../../../artifacts/formulas/production-lab-v1/qa/tactical-package-capture-v1/review-20260908-hp-motion/ROUND-REVIEW.md)。以下目录均相对 `artifacts/formulas/production-lab-v1/qa/tactical-package-capture-v1/`。

| 项目 | 当前证据与范围 |
| --- | --- |
| HP 扣点与播放 | engine 冻结实际 before/after/max/loss；helper 验证同 packet 回执链。12 case；HUD 35 check。准备前值、contact 后值；过杀不按 raw amount 加回 |
| E 修前基线 | `gui-20260908-e-motion-r4`：141 帧，41 PASS，Root 全看；r2/r3 失败目录保留 |
| F 第二轮 | `gui-20260908-f-motion-r2`：391 帧，41 PASS，Terra 全看、Root 关键原帧 |
| 三图 alpha | `artifacts/formulas/visual-targets-v1/art/alpha-repair-20260909-v1/`；三图 RGB mismatch=0，灰/浅底完整轮廓双审。tide/lin新图隔离接入；catalog full crop与脚点同步，方向楔绘在机体后 |
| E 修后实录 | `gui-20260909-e-alpha-caption-v1`：147 帧，41 PASS，Root 全看13板。84准备HP6→85/86命中HP3；123准备3→124/125命中0 |
| F 修后实录 | `gui-20260909-f-alpha-caption-v1`：387 帧，41 PASS，Terra全看33板、Root关键帧与真手玩。推移完成才报距离；撤出329–330仍在/正在撤出，331起消失/已撤出 |
| 多敌 HUD | 固定 packet 顺序双敌姓名/HP、事件参与者高亮；仅空间地图多敌生效。9定向检查；早轮394帧审查发现idle双卡/presence缺失后已修；当前 `gui-20260909-f-objective-v3` 391帧/41PASS，sample/execute_begin全部三卡，Root定向实帧见 ROUND-REVIEW |
| 等待说明 | Root 实窗选择“停在最后安全点”，可见额外资源无消耗与公开时刻仍推进；消除了 cost reason 覆盖 preview 的重复“无”。未改动作/战斗规则 |

采集器使用自己的 Viewport、真实时钟、12fps目标＋阶段额外帧，没有给引擎注入位置/时间。独立 PNG 编码线程，有界512队列、溢出明确失败。E/F修后名义漏采0，队列清空。不是逐个渲染帧录像。

按实际采样时间合成的视频位于 `review-20260908-hp-motion/`：`e-alpha-v1-actual-time-no-audio.mp4`、`f-alpha-v1-actual-time-no-audio.mp4`，最大时间误差约0.5ms，**无音轨**。不要重编码旧失败输出或宣称试听通过。

`full-skip-health-comparison.json`、`post-alpha-consistency.json`：E/F实际战术回执、摘要、世界事实与交接基线及Full/Skip一致。E第二轮成功；F_EXIT第三轮84/90秒有代价成功，runnerHP12且已撤出、gate0/2。

Root 真正通过 CUA 操作：E摘要取消/提交/暂停恢复/同场结算；F三轮另一条保守路线，超移动力输入被拒绝且保留合法三步，最终停在(7,4)、HP12、仍在场、gate0/2，组合2/2完成但目标未达成。见 `manual-play.md` / `manual-f-play.md`。这是另一种真实后果，不是第二份关卡输入或用户盲测。

金标亲看：GF_PLAN/GF_CONTACT；机战Y 13:20 HP/对白层；陷阵之志04:50意图、05:05顺序和执行资料。当前注册空间/HP因果改善，但角色存在感、力量方向、材质、攻击/受击身体动作、声音仍未过；站立PNG移动不算动作。机战Y指令菜单等专帧仍缺，不因这轮检查关闭。

## 4. 当前下一刀与轨 B

- 闸门完整度时序已补：真实 objective_hit 回执、冻结的同packet objectives_after、纯helper验证；schema2现场callout持续显示2/2→1/2→0/2，prepare不报终值。最新 `gui-20260909-f-objective-v3`：391帧/41PASS，398PNG/398、名义漏采0、源指纹稳定；Root原帧0/217/260/382/390确认空段保留、标签可读和终局已毁。260为首次损坏，334准备撤出、336离场/presence变更，382为0/2。最新一刀为定向像素复核和全sample控件回读，不冒充重新全看391帧。无声视频 `review-20260908-hp-motion/f-objective-v3-actual-time-no-audio.mp4`。这只是现场状态标记，尚无实体破损/攻击动作。
- 下一项：近身身体/姓名遮挡、身体攻击/受击与声音仍弱；先结合既有金标找一项可在现有授权内闭合的真实体验问题，再继续其他公式及第二输入。不要重复本轮蒙版、采集器或HP链。灰炮机破碎受补充许可限制。无须等许可才能继续已有授权 UI/玩法/其他公式工作。
- 溯源生成器已补 bounded dependency superset：resolver代码、catalog、相关unit的payload/catalog声明及同basename cutout变体。不复刻Godot选择逻辑、不声称某变体实际启用。7 Python测试通过，包含catalog冲突不漏si、孤儿图排除、字节变化更新hash。`track-b-source-dependencies.json`为当前E/F清单；**现有包未重新生成**，下一次新目录重建自动带上。不是全资产自包含或任意输入证明。
- 世界路线 `sortie` 180×62矮宽槽的紫机高翼可能裁切，尚须实际窗口检查；已核对的 iso_token/execute_stand/aar 几何不能覆盖此槽。
- 其余公式仍按140做两套可区分输入、实玩与参考；T4–T11、WR_T1/T2、完整编辑生产与下游消费不能从当前T0–T3等受限预设推定完成。C/D朝向步态及对白、I/J正式生活动作、人物身份/风格仍欠。

### 4.1 G/H真实试玩与世界路线生产增量

本轮新证据根：`artifacts/formulas/production-lab-v1/qa/world-route-production-20260909/`。先读该目录 `manual-g-review.md`、`manual-h-and-branches.md`，不用重新查旧对话。

- **G/H实玩已完成**：G先问维护员的侧门完整3/3；H真实前厅→陈列廊→回台成卡→后场→再回台→坡道计划汇报完整3/3。不是直接注入知识；部分重复长路使用已有J完成行走快捷键，不能算自然运动实录。Root亲看机战30任务列表/地区图、Outer Wilds船日志与Popochiu多边形参考并对照实玩，连续商业交互/音效证据缺口仍保留。
- **探索输入/反馈已修**：RoomShell仅Exploration opt-in真polygon点击，空白LMB不再advance当前焦点；观察覆盖层鼠标/J保留。21新输入检查+224距离+G-only到场46检查。知识本ready未filed明确待到配置整理台成卡；拒绝门显示真实原因/下一步，零事实零轮数，20检查。原生修后PNG已亲看，命中旧误点不再走错。
- **观察排版已修**：正文20px/页脚16px；H整理长知识段曾压到页脚，现按字形宽度换行，当前段完整、近期上下文至多四行、适当向上增高、页脚独立。3张长文/解锁/下一步实帧全看；最终短页脚“整理只更新知识记录。路线仍须提交；整队出发和现场作业尚未执行。”在该组截图后替换，不能混写为同一冻结采样。
- **G v4已生成并切入Candidate目录**：新reader/reading-v4与新build，旧v3保留。派遣/探索preset与v3字节一致，结果只改“后续队伍还没出发”。Root另实玩不问维护员的正门路线，实际对白保留未问状态，结尾新句可读、3/3；不是新增第二份关卡输入。
- **WR_T1/T2生产首段已扩展**：`world_routes:[{route,departure}]`＋扁平`World+(Exploration→Narrative)*`，每对携带`world_route_binding:{source_stage_id,route_id}`。按真实commit选择分支，live route写入typed departure/arrival和WORLD_ROUTE_COMMITMENT，未选分支不实例化；不是通用图DSL。保留源cycle_plan，编译器显式first_commit_arrival_handoff＋`GAP_WORLD_ROUTE_NEXT_CYCLE_CONSUMER_UNWIRED`，不能写完整两周期已接好。
- 新可启动夹具：该QA根的`package-wr_t1-two-route/flow.json`与`package-wr_t2-two-route/flow.json`，来源与重建见`branch-fixture-README.md`及各REBUILD。未加入current-packages。Root实测T2列表→地图同一选择、撤回免费、第二条真到旧仓；实测T1第二条完整结束后重玩第一条真到器材棚。
- **整合返工已闭合**：合法2卡/1blocked/1committable不再因只有3stage被拒；blocked不产回执。结果进度按已选路径计算，名称按真实stage_id查，不再3/5或错显器材棚。199检查完整第二条结束，Root原生T1正确3/3＋三连间探索；源WR原生两周期705、Python schema/负例均有报告。简短派遣提示最后去掉实现术语，parse通过。
- **不能误读“有条件”**：Root先前曾口头误说不能提交，已更正并记证。有条件允许带shortfall提交路线计划，不可提交才拒绝；实体门通行要求成卡另算。T2原生只成一张卡、未到后场仍可提交有条件侧门，对白没有补入坡道/例行封闭事实；T1零观察正门计划也保持真实缺口。不要把站点未全满等同失败或擅自改为搜满清单。

**该轮提出的下一刀（G部分现见4.2，H继续）**：G倒架、H旧机臂/合页白痕/限宽架的可见道具与知识文本不符，报告点及后场脚点有浮空感；侧门与合页命中区域重叠，键盘可分辨但鼠标门中部被portal抢。应按既有环境制作授权从真实道具、几何/脚点及可点区域一起修，再实玩；不要仅收窄到尚不存在的铰链图、改文字掩盖物件缺失或再做已过HP/蒙版。WR下一周期、未选对象后续消费和其他七公式缺口继续按140推进，不以capability_gap永久排除。

### 4.2 器材棚同源环境与深度遮挡

本节 QA 根仍为 `qa/world-route-production-20260909/`。**current-packages G 已切入 `package-g-environment-v2`；旧 v4 与失败的环境 v1 均保留，未切正式 Demo/Canon。**

- 新环境 v1 按同一 Blender 相机生成器材棚背景、真实翻倒料架/储物箱/地面报告板、磨痕、地面多边形、三块阻挡边界和热点/走近点。脚点、点击区与可见几何来自同一 scene；Python 生产 adapter 与 Godot 注册背景 schema2 已接通，`package-g-environment-v1` 为隔离实验包，不是当前目录默认包。
- Root 实窗经四次正常点击自然行走完成磨痕→倒架→维护员→报告，未用 J 跳完行走；实际三事实、侧门方案和后续六句对白，3/3。`gui-g-shed-geometry-v1/capture.json`：1123 采样帧全部落盘、0 错误、源指纹前后稳定。145 个 RGBA 直接等价 run 覆盖所有变化，10 联系板审查；详细 `g-shed-geometry-v1-motion-review.md`。四个 `g-walk-*-actual-time-no-audio.mp4` 是按实际采样时间剪出的行走短片，非整场连续录像、无声音；约 0.5ms 时间误差。保留首个 25fps 时间基诊断片，不当正确时序证据。
- **Root 否决遮挡**：原帧 00562/00878，人物脚在矮箱斜前沿外，却被整箱遮挡层盖掉头和身体。单个中心脚点 Y 排序不能处理这种斜视几何；draw 回执及脚点 blocker 检查通过不抵销此 FAIL。料架段最低 0.07px 边界余量也仍只是 point-foot 判定，不能声称身体净宽通过。
- 当前返工合同 `projected-depth-v3-contract.md`：保留 v1 所有资产/包/录制，另建 `exploration-environment-v2`。相同相机真实 Z pass 导出 float32 RGBA EXR；5 个裸地面像素中心最大误差 0.0008032m，背景与 v1 解码 RGBA 完全相同。数据及源哈希在新 builder 旁 `shed-projection-review.json`；Camera Data→Emission 的内部半浮点方案已弃用。新角色模型/姿态/身份不在本轮。
- **v3实现与真实复录已闭合该遮挡缺陷**：Godot保持原Sprite矩形、材质颜色/alpha和接触影fill+1.2px描边，逐像素比较场景深度；旧schema2兼容但仍是失败方法。Godot v3 17、v2兼容17、pointer21、parse通过；Python15测试、真实v2编译/21来源hash通过。`gui-g-shed-depth-v2` 722/722、645源前后稳定、104walking帧；147像素等价run/10板覆盖全变化。Root实窗四腿、观察/日志/报告/六句N与3/3，并亲看新00422/00579等价脚点，原箱前吞头/躯干已消失。
- **真箱后反例也实录**：新`gui-g-shed-depth-v2-back-route`从北墙直接点维护员绕箱后，69/69、645源稳定；67代表/5板覆盖全部变化。Root原00051/00054/00058可见先遮下半身、绕出恢复。该补录没有观察或提交，最终事实[]，不冒充另一次完整3/3。实际加载Texture的7像素与EXR解码相同，见`depth-texture-probe.json`；非只查磁盘文件格式。
- 六个`g-depth-*-actual-time-no-audio.mp4`均按实际PTS编码，误差<0.5ms、无声；4腿及2补录不是整场连续视频。Root结论和金标对照在`g-shed-depth-v2-root-review.md`；独立逐帧在`g-shed-depth-v2-motion-review.md`。物理接地/遮挡改善不等于角色风格、动作或用户视觉验收。
- 新采集器显式`--walk-clips`：F9 arm后只按真实walking与settling状态录制，到实际收步结束自动停。两腿69帧已实窗验证，8状态测试通过，仍不注入行动/位置/时间。旧722帧用的采集器原样保存在QA的`production_manual_package_capture-frozen-depth-v2.gd`，SHA与该轮源登记一致；不可把新脚本哈希混写到旧证据。

### 4.3 H三房间环境、实录与反馈返工

- 新 `exploration-environment-h-v1` 的单一 `.blend` 保留三具名房间 Collection/共享正交镜头；三室 RGB、真实 float32 Z EXR 和注册同源。首版保存在 QA 的 `h-environment-first-pass-evidence/`，未覆盖抹去。
- Root亲看后修正了门框擦痕、脚座近缘真实浅孔、内露细合页销，以及坡道撞墙/卡扣像紧螺钉四处语义冲突；所有 `from_*` 改为对应门内安全脚点。修正版可进运行时检查，白痕仍偏描线、整体材质/人物统一性未验收。旧 UV 仅历史坐标，不是新几何目标。
- `package-h-environment-v1` 已从实际 Reader/reading 生成，25来源逐一匹配；Root完成下述审核后已切入H的Candidate目录，旧world-exploration-v3保留。独立headless探针24路径、10次门前实际步进后显式转场、三室RGBAF深度加载均通过；默认开放gate的导航探针不证明知识门槛。
- 首次新H GUI仅初帧，无完整运动证据：Engine持续步进、键位正常，但后续绘制信号停顿，使旧采集循环的F8/F10一并等待。649源前后相同，自有进程已结束。独立诊断副本只强制真实绘制后，原生J暂选、F8与F10恢复，2/2帧；这是定位证据，不是三房间试玩。详见 `h-environment-root-review.md`。
- 新`gui-h-environment-v1-walk`已完成派遣→三室→两次归档→CLEAR计划→七句同場交接→3/3。507/507 PNG、649源前后相同；14段真实walking/settling，Terra全看500 RGBA代表/32板、Root实际操作与关键原图。该轮Viewport画面/回执相符，但helper6611的`force_draw(false)`导致部分原生窗口滞后，不能写全程窗口呈现通过。
- 呈现返工已完成：旧helper存`frozen-before-present-watchdog.gd`，新版fbe42显式`force_draw(true)`并保留独立F10退出、真实postdraw时钟。`gui-h-present-watchdog-manual-probe`关闭自然绘制后，Root亲见暂选/确认/入场/一腿走停，55/55、538forced+1natural、649源不变，F10恢复后退出。旧507与新55不可混写源码或报告字段。
- Root修了两处实玩问题：已有观察的拒门提示改为真实待归档状态，门槛不变；已归档知识卡的图片尊重`points_to`。41语义检查；普通窗口`gui-h-feedback-points-v1`实际观察/拒门/回台归档/知识本4帧，649源相同，已见坡口指向。第二卡记事板映射由语义测试验证，未重复完整H录制。
- 14无声真实PTS短片：1–9在`h-environment-v1-walk-videos`，10–14在补充目录`h-environment-v1-walk-videos-supplement-legs10-14`。第10段307.41秒真实等待未压缩；首版编码失败保留，禁B-frame重排后<0.51ms、全部source+1帧。详见Root/motion/timing三份H review。
- Root已复看138§6的Outer Wilds船日志、Popochiu热点实帧及GF_PLAN，具体对照点在H主审记录。通用联系板/真实PTS编码脚本已以G补录复核，可换录制目录复用。
- WR下一周期方案在 `next-cycle-design.md`。已向用户提出最小闭环裁决：报告后回同任务池、未选请求下周期可再承担、第二次仅承担扣一格不伪造抵达；**仍待答，未实现**。140完整目标与其余缺口继续，不以capability_gap永久排除。

### 4.4 J纸面复核、同室查看与拒绝反馈（已完成的前一停点）

QA根 `qa/hub-review-production-20260909/`；先读 `j-review-root-review.md`。**J已切入 `package-j-hub-review-v1`，旧包和失败证据保留。** J_NOTICE/I_ARCHIVE此前已做，不重复实现。

- 新reading-v2＋frontbench注册-v2，从原Reader第17行编译`review_record_scope_marks`。原摊开书页约50.5×32.2px，未提交不覆盖；真实J_REVIEW完成且`record_reviewed=true`才叠两道暗红划线/范围括线。无新动作、印章、承载数值或扩大结论。缺失注册书页面明确拒绝，不落回旧过程几何。
- 首轮Root实际承力成功→复核2格＋告示1格→提交→2条N→3/3，16/16帧。纸面变化正确，但00012再次查看正文空白；保留失败。根因是in-room普通闲聊override误接管post-cycle TALK，四处委托现有基类已修，67定向检查通过。
- `gui-j-review-fixed-manual-v1`：20/20帧。真实承力成功→只复核2格→可读正文/重复查看→告示未改的实际对白→3/3；正常重玩→试验前Esc离场→复核被拒→只告示1格→未复核书页/正文→另一组对白→3/3。两组post_cycle世界分别不变，负例上游无事实写入，不能把阶段完成当试验成功。
- 反例发现拒绝原因虽已生成却未显示，受阻卡仍称“加入草案”；drawer已显示现有公开原因，卡写“条件未满足”。第一次长副标题被Root否决并保留3帧；最终缩短并测实际字体宽度，48/48。`gui-j-review-refusal-width-v1`原生4/4帧，Root亲看完整提示/原因/关闭后0格。
- 四轮640来源各自前后相同，所有PNG落盘/队列清空/errors[]；这些是F8定向检查点，没有F9连续运动或声音声明。修后00007原图仍是重开面板而即时mode已为room，00010原图重玩确认而state结束；F8紧跟行动有相邻呈现/回读状态差，未定根因，不宣称同帧同步。Root已纠正只凭readback的旧说法；最终4帧F8后独立观察再行动无此差异。Root所有自有GUI已结束。
- Python合同9/9；按REBUILD新目录重建，flow/三preset/gap-report/source-map六个JSON逐字节一致，16来源匹配。旧八路线测试驱动因未打开in-room drawer读取空slots而失败，未算PASS；不为测试驱动改产品。
- Root亲看138§9的Hades同室物件/Citizen Sleeper地点卡并对照实际三种安排。此次补足物件结果和读得懂的因果，人物统一风格、生活动作、声画仍未过；140总目标没有缩小。

**后续不能重复J纸面、E/F HP或G/H遮挡**：继续选择140范围内的新体验缺口与第二输入/生产能力。TAC_T4–T11目前只有四件套中的场景/能力契约，没有对应可启动preset；不能以通用inspect测试替代完整T5。应先核实际契约与已有内核，对需要核心规则裁决的增量给方案；WR下一周期与第四灰机alpha问题仍待答，未得到批准。

### 4.5 T5范围核对与备用目标修复（已完成的前一停点）

- 具体方案：`qa/tactical-t5-design-20260909/tac-t5-smallest-complete-design.md`。Root已按当前代码纠正旧能力表、失实140文件名和“每Tier两个输入”的额外门槛；战术已有E/F两份不同输入，不把一个T5的两种打法另计为第二输入。
- 只使用现有Lab身份与已授权Candidate城市环境，仍保留全队一次提交。先前向用户请求的“保护对象优先/防线优先”是**三轮首段Candidate方案，仍待答**，不代表完整T5。Root核对旧解构第53行已有具名失败规则：Boss越北侧防线、撤离清空前撤离线被突破、主力失去行动能力。因此“保护对象优先”是额外改编提案；另一选项也不能被实现成任何敌人在任何线任意时刻越线都失败。T5新规则未实现，不扩大正式身份/新动作授权。
- 完整T5还必须覆盖现场取得重盾、条件反击和带伤损阶段衔接，不以护线三轮或城市火力代替。又发现来源顺序差异：旧 `story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/gameflow/C01-游戏流程解构-v1.md` 写撤离清空后取盾；较新 `C01-C03-prose-refinement-2026-09-09/C01-纯剧情章节Reader-修订稿.md` 实写先取盾挡击、后清空撤离、再持盾南向反击。已纠正方案中过度统一的顺序；保留两份来源，未擅改Reader或裁决具体适配门槛。
- 既有 `fallback_objective_id` 的真实两轮失败已保存在 `qa/tactical-fallback-objective-20260909/before-fix-report.json`：旧实现只换effect目标ID，仍打旧格。第一轮修后28项通过；confirmed同步公开/实际目标格，estimated只重映射原候选并保留其他候选，unknown不公开所选目标ID/格。旧before报告中的两项“拒绝estimated/unknown”属于已否决收窄方案，不算产品缺陷。
- QA夹具 `package-fallback-objective` 有新目录拒覆盖builder与24项source-map，重建flow/presets/source-map字节相同。它继承F的身份/动作/地图，但新闸门属于QA变换，不声称由继承Reader创作；不纳入current、不计新生产输入或T5。
- Root正常操作 `gui-fallback-manual-v1` 两轮runner_hold：7/7 PNG、128来源稳定、writer清空；原闸门1→0、第二轮备用2→1、两个段落均soft_failure，未伪造穿越成功。Root逐张原图及ITB两张金标直接对照，详见该目录 `root-review.md`。真实F情报帧00004暴露新版面板漏显示source原因，保留为UI FAIL。
- Sol已补当前情报面板：公开source实际340px换行并优先显示，16项UI测量和邻接log/finalintel通过。Terra完成仅fallback声明的原/备用格歧义校验，`before-cell-ambiguity-report.json`真实两项失败→`after-cell-ambiguity-report.json`32/32通过；普通无fallback同格选择仍保持。最终engine SHA `3956478d3bf3cd52e3bf47de049d30d6683194252e547a3e52f4db9a52d1c213`，board SHA `cecaf3b4e0ec873320f63b046294845e1bce6d462bad0f0108adb183958b7daa`。
- **最终实窗已完成**：`gui-fallback-fixed-manual-v1`6/6、128来源稳定、writer清空；Root正常完成同一局两轮，00002公开来源完整两行且不盖关闭入口，00003关情报后11项世界/草案状态相同，00004备用闸门2→1，00005两个段落均目标未达成。23数值核对通过，Root逐张原图及金标对照；640缩放字号仍小，不代签整体视觉。初始Mac锁定后经用户解锁继续原局，最终F10结束owned session31465 exit0。
- Root另按REBUILD在新目录重建，4份JSON逐字节相同，并用最终engine复跑UI16项。Terra独立直看最终6张原图，无本次来源裁切/关闭入口遮挡，见 `independent-final-visual-review.md`。总审 `qa/tactical-fallback-objective-20260909/fallback-root-review.md`；首录7张UI失败证据与旧28项report均保留。该定向修复不再重复，继续140完整体验缺口；T5核心新规则及WR下一周期仍待答，不能把本QA冒充T5完成。

### 4.6 城市环境、2×注册图与原生镜头校准（已完成的前一停点）

- 依据140§5既有授权制作独立18×14城市Candidate环境，不烘焙单位/车辆/盾/伤损、不复用F走廊或失败机体、不接current、不计新生产输入或T5完成。完整源 `artifacts/formulas/visual-targets-v1/art/tactical-city-environment-v1/full-export-v3/`：冻结builder、blend、2560×1440 RGB、同相机float32 Z EXR、几何、8项source-map与REBUILD。旧失败预览/导出保留。
- QA根 `artifacts/formulas/production-lab-v1/qa/tactical-city-environment-20260909/`，先读 `root-review.md`。Root直接看Y道路事件/地图ADV、GF_PLAN并对照预览与原生帧：地面、路口净空、窗框改善；孤立盒状体量、空平广场、材料/光照仍只是定位blockout，城市视觉未通过。
- RegisteredScene schema2允许严格2× raster，逻辑1280投影不变；拉伸图及schema1 2×拒绝。before失败→after46项通过；镜头36项通过，仅修正过时execute采样断言。stager输出 `game-godot/assets/formula_lab/temp/scenes/tactical-city-environment-v1/`，fresh staging三文件字节相同。Root按冻结builder完整重建：RGB解码像素、EXR全部14,745,600个float值和几何/注册语义相同；原文件hash因元数据等不同，strict scene正确更新RGB hash，不写全包字节一致。
- 新 `tests/formula_lab/tactical_environment_manual_inspector.gd` 复用F8/F10/writer与TacticalCamera，只实例化环境。GUI-v1三帧保留缩放后hover不刷新；v2两帧保留OS鼠标轮询在窗口外。改用真实viewport事件坐标按新镜头重算后，v3七帧完成1.0/1.55/2.2、北/东南平移与复位，Root逐张直看；全景00002明确是(9,7)。
- v3另发现JSON浮点数组与整型Array.has不匹配，把(5,3)误标地面。实际Godot probe复现，仅修检查器Vector2i占格集合；v4四帧补证(5,3)建筑占格、(3,3)厅口地面、43格红层。v3占格FAIL保留。Terra独立全看v3/v4；62项数值对照通过，每轮122来源稳定、writer无遗漏，全部自有GUI F10 exit0。仅检查点，不证明连续运动/声音/导航/身体遮挡。
- 下一工程缺口：同源深度还未进入战术body/shadow；`tactical-depth-integration-design.md`只读草案尚未实现/签准。须核实际脚点/铺装高度与像素坐标，不能用Y排序代替身体遮挡；同时继续城市沿街体量/材料层次。T5具名防线胜负及旧/新来源取盾顺序、WR下一周期、第四灰机alpha仍待答。不要重复HP、E/F录制、G/H或J已闭合内容。

### 4.7 战术同源body/接触影接入与原生遮挡校准（当前停点）

- QA根 `artifacts/formulas/production-lab-v1/qa/tactical-depth-integration-20260909/`，先读 `root-review.md`。当前只接真实BoardView的显式MapToken；不计新生产输入、运动、T5或用户视觉验收。原图与身份不改，静态竖直平面代理并不等于机体源镜头注册/新动作。
- 同源 `tactical-city-environment-v1/depth-contract-v1/` 从冻结blend的7个实际承脚网格导出62向上三角形/48斜面，10点独立投影校验；Root fresh重建contact-contract/check-report字节一致、render_calls=0。场景逻辑1280、RGB/EXR2560×1440；按实际铺装高度承脚，不能采屋顶当脚点。
- 注册层schema2新增严格可选projected_depth；初版17测试绿仍有UV分母、重复加高和影平面符号等错误。独立55反例22失败→Astra修订65通过，旧schema2 46通过。Layer 108通过；真实BoardView组合58项/14实际draw回调通过（保留误用v1夹具和no-engine启用flag残留失败，Root已修清零）。camera固定后36项通过；早期parse失败的24项footer不是PASS。
- 最终QA staged资源 `game-godot/assets/formula_lab/temp/scenes/tactical-city-depth-v3/`；fresh `-rebuild` RGB/EXR字节一致、JSON只输出资源目录不同。stager仍是QA，不是生产编译器。白青机取已批准alpha修复的完整1024原图，最低脚尖虚拟点不是新美术/3D接受。
- 原生v1因缺intent占位拒绝无帧；v2六帧发现朝向盖脚；v3九帧确认(9,12)完整、合法(2,6)部分、(1,6)全遮挡及1.55/2.2缩放，00008网格盖body；v4三帧把注册网格/朝向/选择标记放到body下（580marks）。Root直接看全部18原PNG、Terra独立看v3/v4全12；各轮来源145/145/146稳定，writer无漏，全部自有GUI F10 exit0。
- 原始PNG配对检查：前景/部分ROI差2774/2804，全遮挡0。排除body alpha后的脚下条带前景28/34、部分52/54像素只变暗，有限证明contact-shadow实际输出；未签艺术可读性，影子偏暗且cyan朝向干扰脚点。Root实际对照ITB意图战场与GF_PLAN：遮挡工程成立，城市盒状/材料/灯光和源机体镜头仍距目标明显。
- native v4之后仅补no-engine _depth_active/_depth_registration清零，58组合回归已覆盖；不能说v4实录运行过该后置修复。最终代码绑定 `final-source-hashes.json`。没有活跃Root GUI；所有headless/Blender进程句柄已正常结束。
- 下一刀：改善影子/脚下标记可读性，并以真实可通行路径的事件时间回放和连续实录验证遮挡，不把J/K摆位冒充运动；再推进深度输出的生产编译与完整输入。E/F旧UnitPlate未全接；近景execute仍有独立镜头契约。T5/WR/第四灰机待答保持；140完整目标与Candidate边界不变。

## 5. 文件、工具与停止路线

主要代码前缀 `game-godot/scripts/formula_lab/`：
`shells/tactical/tactical_round_engine.gd`、`shells/tactical/tactical_board_view.gd`、`shells/tactical_lab_shell.gd`；
`widgets/formula_lab_{health,objective,spatial}_playback.gd`、`widgets/formula_lab_execute_hud.gd`；
`formula_lab_placeholder_art.gd`、`formula_lab_unit_plate.gd`、`formula_lab_registered_scene.gd`。
测试前缀 `game-godot/tests/formula_lab/`，采集器 `production_tactical_package_capture.gd`。新capture目录必须唯一，录制期间冻结相关源码，保留同一进程handle；视频在采集结束后再合成。

Godot `/opt/homebrew/bin/godot` 4.7；ffmpeg `/opt/homebrew/bin/ffmpeg`；PIL Python `/Users/rayz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`。本地透明用 macOS Vision 与 alpha-only 脚本，原RGB不变；不是新生成图。

Root本轮H/J、备用目标及城市四轮自有GUI、采集、视频编码、Blender重建/EXR对比与定向测试均已结束；当前没有Root持有的活跃Godot窗口，H环境不再渲染。下一任务先核验进程所有权。旧PID79583为长时间headless briefing test，不属本轮确认所有权；旧blender-mcp45400/45401也保留。PID仅历史证据，不按数字直接kill。

失败白青Blender母型/分件R1/R2停止；双人正面静态板维护员身份/画风未过，不做第二机/动作/动画/默认替换；无新授权。T3重击音效仅候选方向，全段未验收。三图alpha许可不扩大这些范围。

## 6. 完成判断

报告只写：实际改了什么、哪份实录/操作证明、仍欠什么、下一步与需用户决定的事项。140七公式体验＋可复用内容生产仍是全部目标。任何局部PASS、代理完成、参考静帧或交接更新均不代签用户视觉验收，也不晋升Canon。
