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

## 4. 当前停点：L 非计分指导战生产、停拳与主体拒绝

上一轮 K 完整停点归档至 [_history/141-before-t1-production-2026-09-10.md](_history/141-before-t1-production-2026-09-10.md)。K 的 Full 219帧、修复后早K18帧、实际PCM、独立等价复核已闭合，见 `qa/tactical-t3-production-20260910/root-review.md`；不重做。

最新隔离入口 `builds/package-l-tactical-stationary-v1/flow.json`，主审 `qa/tactical-t1-production-20260910/root-review.md`。原 `package-l-tactical-coached-v1` 保留为未适配对照；L 不入 current。

- 已接入原 TAC_T1→同场真实 checkpoint，是区别于 E/T0、F/T2、K/T3 的第四个实质战术输入；同 L 的 Full/Skip 或摆位变体不重复计数。原预设的短时切教练未接入三轮场次，不能把地图教练头像当切控能力。
- 原配置 R1 正常规划后与靶机同拍争格，重拳距离2落空；97项路线证明及82原帧保留。没有预扣HP凑停止线。新 Reader/reading/setup 显式把靶机起点调到(3,2)、三轮站定并说明公开作用目标；新有界 `tactical_setup` 模块只开放起点及既有意图的路径/文字，HP/伤害/射程/目标格/停止线/拒绝/轮数不改。
- fresh 重建五JSON相同，source-map25行/22不同来源。Python四组37项；真实hold步骤登记清单修前4失败→20/20；人类教练目录头像的绘制/点击/结算60/60；E/F结算221/0。旧QA失败保留，不以数量替代像素。
- 人类尺教练原来误画金机，现仅指导战中无显式map profile的人类使用带框既有肖像位置标记；不是全身、承脚或新身份。靶机仍实际灰炮机，未扩大alpha许可。
- 原生 `gui-l-stationary-full-v1` R1 Full68/68帧，无K，真实靶10→6、学员16→14；Root看完4板。Root曾误读小窗14为16，已用1280原图及独立回执纠正，没有为误读改规则。
- `gui-l-completion-v1`112/112帧，R1早K、R2 Full停拳、R3先主体拒绝（草案未写）后玩家显式待机；最终学员12/16、教练4/4、靶6/10、垫2/2、指导清单2/3、包2/2、世界事实{}。148源前后稳定；112→44代表/4板Root全看，该输入两批录制含真实Master PCM，未试听/不签精确同步。
- 场内与SET已准确呈现“指导场结束 · 不计胜负”和实际2/3。Runner最终汇总也已按真实typed回执修为“指导场结束 · 清单2/3”与“本场检查点已确认”，35/35通过。旧111 PNG仍是SET禁用按钮，不能冒称最终汇总；新修复批00080已单独保存并亲看，真正2/2与准确文案的原PNG已补齐。
- **本轮Root逐帧新发现：legacy双侧HP/伤害字幕在prepare提前显示after。** 旧R1 Full34/35靶已6而40才contact，50学员已14而56才contact。根因是该分支绕过HealthPlayback；仅HUD已修，真实receipt/事件索引采before→接触after，无效包明示结算后值且无接触反馈。66项修前50失败→修后全过，必要既有131项通过。旧录制不追认时序通过。
- **修复后原生 `gui-l-hp-fixed-v1`81/81帧已闭合。** R1 Full：36/37 prepare靶仍10，38–40 approach仍10，41/42 contact才6；52/53 prepare学员16、54–57仍16，58 contact才14，字幕同阶段变化。R2/R3真早K，execute71/77→新绘制settle72/78，fast0/1/2；最终12/4/6、垫2/2、清单2/3、包2/2。01真实教练情报、79真实SET、80真实最终页；148源前后相同，81→51代表/5板Root全看，F10exit0（owned36943）。原时长无声片在hp-fixed-videos-v1，Full5.791573秒，其他两片为早K交接。PCM346.058667秒，独立实解连续/全finite/0drop，听感未验收；独立13/13见native-audit/hp-fixed-v1/report.md，跨旧completion只有Runner与HUD两源变化。
- 仍对照Y官方指令单焦点、ITB意图战场和GF_PLAN/CONTACT：L的场地偏小、蓝地板重复/天空拉伸、灰机残底、静态PNG缺承力与动作仍未过美术线。生产与实际停止/拒绝改善成立，用户视觉验收仍false。
- **下一可见制作刀已定位，尚未实施**：`qa/tactical-t1-production-20260910/environment-next-cut.md`。修正高反光道路裁片回退/重复尺度、960×108天空条非等比拉伸、装饰机骸脚点与阴影；显式局部board/execute装饰输入需补制作接线，不能声称现tactical_visuals已支持。真实7×6占格、blocked/训练垫/身份/姿态不改，不将装饰残骸解释成击毁回执。

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

- F已补进/退完全与部分遮挡的真实运动；只覆盖此路线/三台现有PNG/两版残骸，不等于任意路线或所有场景遮挡通过。原城市J/K摆位仍只证明校准。
- 城市沿街体量/灯光材质、近景execute的独立镜头、身体攻击/受击、角色规格/生活动作、声音均未收口。PNG位移不是动作，三图alpha批准不是新模型或角色动作批准。
- T5完整能力包含具名防线失败、现场取盾、条件反击、带伤损衔接；不能用三轮护线QA替代。三轮保护对象优先/防线优先提案仍待答，且旧解构“撤离后取盾”与新Reader“先取盾挡击后撤离”顺序冲突未裁决。方案在 `qa/tactical-t5-design-20260909/tac-t5-smallest-complete-design.md`。
- WR下一周期的具名主体、未选请求与第二次承担扣格方案仍待答；首次commit/arrival不代表完整多周期。不得按沉默实现。
- TAC_T4–T11、完整WR_T1/T2、其余六公式第二输入质量、角色存在感、声画与可编辑生产继续按140推进；capability_gap不是永久排除理由。

## 6. 已闭合工作：按证据查，避免重做

以下均相对 `artifacts/formulas/production-lab-v1/qa/`；更细进度在归档141与各主审文件。

| 已闭合增量 | 证据入口与边界 |
| --- | --- |
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

上一轮F深度GUI v1配置失败exit2、v2上限退出exit0、v3 F10 exit0；E/F标签、F强遮挡250帧、board-arm短验证与F-lookdev250帧、K Full/late-K/Skip-v2/修复后早K及L原配置/R1 Full/完成批/HP修复批均已F10排空exit0，全部已结束。没有需要用户解锁后继续的遗留窗口。先确认进程归属再操作；历史未接管headless PID79583以及旧Blender MCP不按旧PID直接kill。CUA选择已退出Godot可能打开项目管理器，须先核日志/handle。

后续报告只写实际改变、真实操作/原帧、剩余差距与必要决策点。140目标没有缩小，不代签用户视觉验收。
