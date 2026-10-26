# 141 · 公式台当前开发停点

更新：2026-09-10。工作区 `/Users/rayz/Documents/超gag机器人大战`；分支 `codex/srw-kernel-sandbox`。
**Candidate / not_canon / user_visual_acceptance=false；140 总目标仍进行中。**

## 1. 接手顺序与边界

完整读本文件与 [140 唯一执行目标](140-formula-lab-integrated-visual-production-goal.md)。137按生产接口、138按当前公式案例/实际参考帧查；不重载旧对话。较早轮次的完整交接原样归档至 [_history/141-before-f-depth-production-2026-09-09.md](_history/141-before-f-depth-production-2026-09-09.md)，下文给出具体证据入口，不需每轮重读归档。

- 保留共享工作树的大量修改/未跟踪文件；没有add/commit/reset/清理。chao-gag-canon边界已核，不推进C04正式剧情、Canon、默认Demo或正式Runtime。
- **HP命中回执/显示、E/F第二轮真实运动、紫/白青/靶机三张alpha修复均已完成，不重做。** 三图原RGB逐像素保留；无新身份/姿态/付费/失败分件复用或美术验收授权。
- **E挑战者与F拦机甲实际为第四灰炮机 mecha-si.png，F拦机乙为金机 mecha-ye.png。** 不得按payload残留doll声明换身份；已修mecha-doll不替代它们。第四灰机追加蒙版许可仍待答，金机新蒙版也不在已批三图内。
- 失败白青Blender母型、分件R1/R2、双人共骨架静态身份试验均保持停止；不继续新姿态/动作/动画/默认替换。环境Blender制作按140§5既有授权继续，不逐场申请。
- 模型按140§8.1依实际接口、能力与总token成本选择，不固定Sol/Astra；当前collaboration接口无Spark，不重试或另建用户任务绕过。简单有界工作选胜任的低阶模型；一次纠正后仍不胜任就升级。Root负责实际操作、整合与最终判断。
- 金标与实际试玩对照不得省略；机器通过、实际画面、用户视觉验收和正式晋升分别报告。每公式至少两个实质不同输入，不是每Tier两个，也不能以同关两种打法顶替。

## 2. 当前包与新隔离入口

唯一Candidate目录是 `artifacts/formulas/production-lab-v1/current-packages.json`，本轮未改。以下相对其builds目录：

| 包 | 当前目录 | 现有范围 |
| --- | --- | --- |
| A | package-a-briefing-v1 | 实际现场前言→调查→同场结果对白 |
| B | package-b-onsite-v2 | 承力/交割试验→成功/中止/未开始的实际回应 |
| C | package-c-exploration-actors-v1 | 器材棚走近/观察/问人→路线计划 |
| D | package-d-exploration-actors-v1 | 跨三空间观察→回台归档→计划 |
| E | package-e-registered-map-v1 | T0固定擂台→执行→真实结算 |
| F | package-f-registered-map-v1 | T2限时穿越→动态阻挡/撤出→结算 |
| G | package-g-environment-v2 | 巡访派遣→同源器材棚→真实报告 |
| H | package-h-environment-v1 | 三室行走/归档开路→报告 |
| I | package-i-hub-in-room-v1 | 自然返馆→走近闲聊/安排→同室后果 |
| J | package-j-hub-review-v1 | 真实试验约束复核→原书页标记→同室查看 |

**最新隔离F包：`builds/package-f-lookdev-v1/flow.json`。** 原depth与occlusion-v1/v2全部保留。新包改善工业通道材质/光照及残骸破折，是同一F的视觉变体，不计新实质输入、未替换current F。实际同路线三轮与结算已完成，2/2流程、两段soft_failure；仍未过美术线。

```sh
/Applications/Godot.app/Contents/MacOS/Godot --path game-godot res://scenes/formula_lab/formula_lab_package.tscn -- --package '/Users/rayz/Documents/超gag机器人大战/artifacts/formulas/production-lab-v1/builds/package-f-lookdev-v1/flow.json'
```

重建用该包REBUILD.txt，在新目录produce；输入为 `inputs/reader-f-lookdev-v1.md`、`reading-f-lookdev-v1.json`、`tactical-visuals-f-lookdev-v1.json`。统一浏览仍使用 `formula_lab_package_browser.tscn`。

## 3. 已闭合底座：不重做

原完整交接归档至 [_history/141-before-lookdev-2026-09-10.md](_history/141-before-lookdev-2026-09-10.md)。以下主审有对应源码、失败反例、测试和原帧；只按当前问题查。

- `qa/tactical-depth-production-20260909/root-review.md`：tactical_visuals进入主编译器；同源2×RGB/EXR、实际承脚面、catalog-first真实身份绑定、缓存、原生configure/begin缺陷、首draw HP0/1占位、F9显式执行采集均已修。F-depth-v3真实281帧/2-of-2，结算Z提示后来单字修正另有记录。
- `qa/tactical-render-boundary-20260909/root-review.md`：空事件准备HP来自已绑定当前快照；MapHUD新bind实际draw后才确认返回。23/35/34定向检查及walk8通过；旧E live-settle/pixels-execute反例保留。board arm提前取消在该轮末另修、5帧短实窗验证；最新lookdev250帧已经使用这个最终采集版本。
- 上述旧F-occlusion-v2同路线实录250帧/186源稳定，三轮进退强遮挡，最终12/8/8、闸门0/2、两soft_failure/事实{}；旧帧索引90/174/246不得套入新录制。独立123代表、实际PTS三片及分版本源均保留。
- registered机体仍是静态竖直PNG平面代理，源机体相机未注册。虚拟脚点/深度正确不是身体姿态、动作、光照或美术通过。

## 4. 当前停点：L / T1 相机生产、真实点选与同场交接

本轮开始时的布景停点已原样归档至 [_history/141-before-t1-camera-2026-09-10.md](_history/141-before-t1-camera-2026-09-10.md)。旧 L 生产/Full停拳/HP时序见 `qa/tactical-t1-production-20260910/root-review.md`；布景81帧与被否决v4恢复见 `qa/tactical-t1-environment-20260910/root-review.md`，不重做。K Full219/早K18也已闭合。

**最新隔离 L 入口 `builds/package-l-camera-v1/flow.json`**；本轮主审 `qa/tactical-t1-camera-20260910/root-review.md`。仍是第四个实质战术输入L的显示变体，不增加输入计数或替换current。T1短时切教练/人类尺控制尚未实现，头像不是控制体验。

- 修前独立实际滚轮录制2/2确认active=false、zoom1，旧提示确实无效。只实际测过滚轮，不谎称实际中键拖动。新staging输入仅增加严格三键 `board.view_camera={mode:interactive_source_plane,default_zoom:1.55,texture_filter:linear}`，只限T1 board；execute侧/非法值/缺consumer原子拒绝。来源为 reader-l-camera-v1 / reading-l-camera-v1 / tactical-staging-l-camera-v1。
- 复用原world camera：背景/格/体/路线/意图同变换，点击逆变换；HUD文字屏幕尺寸，规划/摘要/返回/SET同一锚点。近景演出不应用该相机。没有改逻辑占格、伤损、动作、原图或复用失败v4地毯。
- Runner只在真实TAC完成且回执匹配时保存独立显示字典；新SET先验证原engine/receipt，再创建新BoardView并导入同源视点。结束/失败/重启清理。显示不写权威结算或world_facts；既有Shell.finish的阶段readback诊断可如实留相机快照，不把它当新游戏事实。
- fresh produce/rebuild五JSON字节一致；source-map36行/32不同源，含六个相机/交接consumer。54项制作检查、73项相机定向、36项旧相机、221项旧真实结算和26项新Runner跨实例检查通过。默认世界像素不变，仅去失效提示/按钮；默认与显式的prepare/contact均与改前原图相同。首轮测试前置/浮点/诊断范围错误均保留，未为通过而改规则。
- **新 `gui-l-camera-v1`79/79原帧，151录前/录后源相同。** 0/1初始zoom1.55；2实际滚轮到1.736；3换锚点缩回1.55并改变focus；4点中教练情报；5实际复位；6再次放大。7点相邻格route1、8点起点撤回route0；未提交世界移动。6至77全部地图阶段保留zoom1.736/focus[655.649719,348.770844]/anchor[600,355]和同一源。
- R1本批选非致死肩顶，09/10摘要→11–66真实Full→67/68自然返回；42–43准备、44–46接近、47接触、48–53反冲/余波，靶由(3,2)推到(3,1)，HP保持16/10。69为R2重拳主体拒绝；玩家明确改垫区预备，70/71摘要，72返回fast1。R3明确wait，73/74摘要、75终态fast2。不能套旧重拳批HP；本批最终16/4/10、垫2/2、清单2/3。
- **R2/R3未采到中间execute帧**：J/K太接近，采集器明确记录execute_not_observed_before_rendered_return。只有真实摘要、回执与独立F8返回，不能称两段运动录像，也不以旧批补缺。R1严格encoder片段10–67含14.994449秒真实提交等待，共20.082642秒；仅一次额外末帧重复0.092353秒，PTS误差≤0.498ms。R2/R3无片段。
- 76实际新SET、77详情保留真实世界和非默认视点，78真正最终页2/2/清单2/3；Root在F10前亲看78原PNG。writer pending0/errors[]，owned session86776 exit0，窗口已结束。新的26项跨实例测试另证新BoardView/原engine/相机一致与坏源拒绝。
- Root完整RGBA把79折42代表/37精确重复，全部4板及09/47/78原图已亲看。音频735.093333秒、35,284,480帧/48kHz双声道float32、68,162块、全finite/0drop；含规划等待，未试听/逐样本同步验收。独立机械审核15/15通过，见本QA `native-audit-v1/report.md`；原生SET只直接证明同engine来源和相机，跨View实例由26项headless验证。保存原帧77forced/2natural，沿用既有watchdog换缓冲，不称60fps性能或连续屏录；不代视觉验收。
- CUA公开drag只能左键，故实际中键手势仍无录像；73项仅验证实际Shell的合成中键事件。下一次需要运动早K证据时，提交与K分开，并先见到新绘制execute，不能像本批同一工具内紧接输入。
- 重新对照Y单焦点指令、ITB场上意图、GF_PLAN与GF_CONTACT：主体拉近、真实取景可用且跨SET稳定；地面更显软糊粗糙、教练引线长、多黄框、静态图平移/身体触点分离/灰机残底/蓝台面仍未过美术线。用户视觉验收false。
- 下一步查本QA `t1-human-control-next-cut.md` 的只读定位，补完整体验，避免继续同一L装饰试色。新教练控制/新姿态没有因相机通过自动获准；T4/T5/WR核心待答方案与原alpha许可边界不变。

### 上一轮F同源环境增量（已完成，按需查）

入口：`artifacts/formulas/production-lab-v1/qa/tactical-lookdev-20260910/root-review.md`。

- 环境源 `artifacts/formulas/visual-targets-v1/art/tactical-corridor-lookdev-v1/`，隔离res `corridor-t2-lookdev-v1`。增加墙面腰线/柱脚、地面低频材质变化、冷填光/暖灯、原blocked(4,4)内残骸破折/斜撑/底片。原相机、9×5、四承脚三角形、规则/占格不变，无新机体姿态或alpha。
- 失败预览保留：v1平滑且像门；v2一度改到未绑定同名材质；v2b修好实际`.001`绑定后出现Wave粗糙度波纹而否决；v2c仅去Wave，保留Noise粗糙度0.70–0.88，Root允许作为Candidate进入原生比较。最终同次32sample的2560×1440 RGB/float32 RGBA view-Z，scene SHA `58e3cd367589e7546ea1c43f99a22b66a4f074da9bce6fb76d7c517d6fc9c08c`。
- fresh produce五JSON与新包字节相同；相对occlusion-v2完整tactical payload仅registered_plate一叶变化，三机PNG/profile、规则、结算相同；source-map33行均可追。源/导出/.blend/重建说明均在环境目录，不复用失败机体资产。
- **真实正常操作** `gui-f-lookdev-v1`：R1 Down/Right/Right至(3,3)，R2 Left/Left退(1,3)，R3原地，均runner_hold，正常摘要/J三次提交；结算详情、明确确认2/2，F10排空exit0（owned41056）。250/250、214源前后相同、writer pending0/errors[]。实际最终12/8/8、闸门0/2、两soft_failure/世界事实{}；三轮限定状态与旧路线相等，完整capture不相等。
- 新执行首帧2/88/175，实际已呈现返回87/173/246。**R2缺同轮执行前规划原PNG**：88前是R1结果87；实际菜单/摘要操作不补造缺失原图。R1/R3有规划原帧；下一次录制应将每轮摘要F8与提交分开完成，不为此重录本轮全部运动。
- 全250帧相邻RGBA折为117代表/133重复、8联系板。独立稿错用旧00053、误称00114首次全显露，原稿保留；Root接管看完8/8板、复核关键原图后纠正：新00044/48部分，00053/56/87全遮；00105仍C4部分、00113/14已B4全显露，不声称首次露出瞬间。字幕目的地不能代替身体当前格。
- 720标签与health packet核值相符，另3仅终值比较，不作绘制源证明。723次post-draw锚差最大1.772216设计px/display-cell差0.030989，54次显示位置不同于结算位置；不称两个采样时点同帧精确相等。
- 旧严格encoder实际exit1拒R2；新QA review工具只从真实execute起保留缺口。三片在`f-lookdev-v1-review-videos/`：R1 21.664458秒（含13.824589秒实际规划等待）、R2 7.407058秒execution-only、R3 6.448780秒；各1真实末帧重复，PTS误差≤0.500ms。编码前后capture/250PNG/旧encoder共252输入相同；原PNG仍为像素权威。

## 5. 制作判断与后续差距

Root对照实际新旧原帧、ITB意图战场与GF_PLAN：新版墙面层次和单位/标签分离改善，但地面偏重复软斑、残骸仍像孤立挡板，机体接地/光照和整体材质密度未达到金标。只接受为可复用环境生产的可见增量，不签美术或用户视觉验收；环境仍可继续打磨，不能无限停在F同输入变体。

**Y菜单本体静态缺帧已补。** 2026-09-10直看官网系统页的636×358原图；右侧单列胶囊指令、唯一黄色焦点、场上当前单位与底部驾驶员/机体信息确实可见。来源、SHA及范围在`artifacts/formulas/case-survey/references-srwy-official-20260910/`；138§4.2已纠正旧菜单形状推测。只关闭静态菜单本体缺帧，操作/按键/声音/节奏仍未证明，140目标与旧缺帧清单没有因此被偷改成完成。

**T4下一核心方案待答，未实现。** 实际CLI返回`unknown_preset: TAC_T4`，当前连configure/begin都未到。`qa/tactical-t4-design-20260910/candidate-decision.md`建议中性0:0先三分、双方合法得分/输分、复位保留伤损与资源，敌方只依据实际观察到的执行receipt在下一轮公开换装备反制。Root已给用户一处核心确认：此方案或“敌方自己不重复招式”；不凭沉默落产品状态机、不移植parked C02固定0:2→3:2、不据此批准新机体姿态。`disclosure=happened`仅表示发生，不证明特定敌方看见。其他已授权打磨与140全目标继续。

**T1短人类段范围待确认，未实现。** `qa/tactical-t1-camera-20260910/t1-human-control-next-cut.md`核到active_band仅过滤我方可编辑，巨机敌方队列不会因此自动暂停，不能直接把R2改成human。Root建议R1真实结算后插入不占回合的中性Lab教练走近观察→交回R2段，只观察真实状态、不改变伤损/停止线/清单；所需人体走停/转向纳入140已有单人有界试验。阶段任务与中性身份合为一个待确认范围；不得用头像平移冒充尺度控制或据相机通过推断新姿态批准。

- F已补进/退完全与部分遮挡的真实运动；只覆盖此路线/三台现有PNG/两版残骸，不等于任意路线或所有场景遮挡通过。原城市J/K摆位仍只证明校准。
- 城市沿街体量/灯光材质、近景execute的独立镜头、身体攻击/受击、角色规格/生活动作、声音均未收口。PNG位移不是动作，三图alpha批准不是新模型或角色动作批准。
- T5完整能力包含具名防线失败、现场取盾、条件反击、带伤损衔接；不能用三轮护线QA替代。三轮保护对象优先/防线优先提案仍待答，且旧解构“撤离后取盾”与新Reader“先取盾挡击后撤离”顺序冲突未裁决。方案在 `qa/tactical-t5-design-20260909/tac-t5-smallest-complete-design.md`。
- WR下一周期的具名主体、未选请求与第二次承担扣格方案仍待答；首次commit/arrival不代表完整多周期。不得按沉默实现。
- TAC_T4–T11、完整WR_T1/T2、其余六公式第二输入质量、角色存在感、声画与可编辑生产继续按140推进；capability_gap不是永久排除理由。

## 6. 已闭合工作：按证据查，避免重做

以下均相对 `artifacts/formulas/production-lab-v1/qa/`；更细进度在归档141与各主审文件。

| 已闭合增量 | 证据入口与边界 |
| --- | --- |
| L/T1相机制作、点选与跨实例SET | tactical-t1-camera-20260910/root-review.md；79原帧/151源/42代表，实际滚轮/复位/点选；R2/R3无中间运动帧，视觉未过 |
| L/T1布景制作与实际闭环 | tactical-t1-environment-20260910/root-review.md；81原帧/151源/47代表，v4失败已撤回；仍未过美术线 |
| K/T3生产、真实PCM与快进交接 | tactical-t3-production-20260910/root-review.md、native-audit/skip-fixed-v1-review.md；Full219/早K18，源码差异与等价结果已核，视觉/听感未通过 |
| E/F HP命中、多敌HUD、闸门完整度、三张alpha与真实第二轮 | tactical-package-capture-v1/review-20260908-hp-motion/ROUND-REVIEW.md；Full/Skip真实账一致，无音轨，不等于动作/声音或视觉通过 |
| G/H派遣→行走/观察/归档/报告 | world-route-production-20260909/manual-g-review.md、manual-h-and-branches.md；G/H均实际3/3，后续队伍未出发 |
| G器材棚箱前/箱后深度、H三室同源环境/呈现watchdog/拒门反馈 | 同目录 g-shed-depth-v2-root-review.md、h-environment-root-review.md；原始失败/新PNG/实际PTS分开，完整运动已审，不重做 |
| J试验后复核/原书页范围标记、同室看正文、未试验拒绝 | hub-review-production-20260909/j-review-root-review.md；四轮真实操作、源稳定、重建一致；人物生活动作/声画未过 |
| 备用目标ID+格同步与情报source换行 | tactical-fallback-objective-20260909/fallback-root-review.md；旧失败保留，最终两轮6原帧/128源/23核对；不是T5 |
| 城市同源2×背景/EXR、镜头缩放平移与占格 | tactical-city-environment-20260909/root-review.md；完整重建、原生镜头四轮完成，城市仍blockout |
| 战术body/接触影城市原生摆位校准 | tactical-depth-integration-20260909/root-review.md；完整/部分/全遮挡18原帧、shader与脚点反例修复；仅摆位，不是运动/生产输入 |

## 7. 工具与进程

Godot `/Applications/Godot.app/Contents/MacOS/Godot` 4.7；Blender `/Applications/Blender.app/Contents/MacOS/Blender` 4.4.3；ffmpeg `/opt/homebrew/bin/ffmpeg`；PIL Python `/Users/rayz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`。

新capture必须fresh目录，录制期间冻结相关源码，保存同一进程handle；F8检查点、F9 arm、F10排空退出。要保留每轮规划原帧时，先在摘要单独F8并核采集，再F9/提交，避免快速输入同一呈现周期漏掉待录原帧；最终汇总同理，F8后核实真正保存的PNG，再F10退出。只在冻结边界做必要hash，不每帧hash或反复全项目审计。相邻RGBA比较用于离线全帧审阅，不改原PNG。

上一轮F深度GUI v1配置失败exit2、v2上限退出exit0、v3 F10 exit0；E/F标签、F强遮挡250帧、board-arm短验证与F-lookdev250帧、K Full/late-K/Skip-v2/修复后早K及L原配置/R1 Full/完成批/HP修复批/布景v1批/相机v1批均已F10排空exit0，全部已结束。没有需要用户解锁后继续的遗留窗口。先确认进程归属再操作；历史未接管headless PID79583以及旧Blender MCP不按旧PID直接kill。CUA选择已退出Godot可能打开项目管理器，须先核日志/handle。

后续报告只写实际改变、真实操作/原帧、剩余差距与必要决策点。140目标没有缩小，不代签用户视觉验收。
