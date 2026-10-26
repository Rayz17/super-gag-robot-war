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

**最新隔离F包：`builds/package-f-occlusion-v2/flow.json`。** 原 `package-f-depth-v1` 与遮挡技术试样v1保留。新包是同一F的视觉生产变体，不计新实质关卡输入，未替换current F；实际三轮完成进/退强遮挡、结算详情与显式确认，2/2流程完成、两段均soft_failure。

```sh
/Applications/Godot.app/Contents/MacOS/Godot --path game-godot res://scenes/formula_lab/formula_lab_package.tscn -- --package '/Users/rayz/Documents/超gag机器人大战/artifacts/formulas/production-lab-v1/builds/package-f-occlusion-v2/flow.json'
```

重建用该包REBUILD.txt，在新目录produce；输入为 `inputs/reader-f-occlusion-v2.md`、`reading-f-occlusion-v2.json`、`tactical-visuals-f-occlusion-v2.json`。统一浏览仍使用 `formula_lab_package_browser.tscn`。

## 3. 已闭合：F深度进入真实生产与三轮回放

先读 `artifacts/formulas/production-lab-v1/qa/tactical-depth-production-20260909/root-review.md`。这是本轮整合判断与源码/测试/帧/重建的入口。

- 新 `scripts/formula_production_tactical_visuals.py` 接入主编译器；stage仅需 `tactical_visuals={pack_path,source_quote}`，原文须在本段Reader。pack显式绑定全部原unit_id，按UnitPlate实际catalog-first来源核身份；仅替换registered_plate和map_token_profile。PNG/注册/RGB/EXR有来源，不替换规则或位置。Python只PNG头/大小/SHA，不代替Godot decode/透明或视觉验收。
- F使用原工业通道blend同一次Cycles的2560×1440 RGB+float32 RGBA view-Z；逻辑1280、9×5、原相机/阻挡/地形/出口不变。两个实际承脚面4三角形，7地面EXR样本最大误差0.0004368m。源在 `artifacts/formulas/visual-targets-v1/art/tactical-corridor-depth-v1/`，stage_environment.py拒覆盖；fresh staging RGB/EXR字节相等，JSON只资源目录不同。隔离res目录为 `temp/scenes/corridor-t2-depth-v1/`。
- generic MapToken scope允许显式Tactical身份；白青使用已批修复完整PNG，灰/金使用既有PNG，不编辑像素。脚外开放朝向箭线减少盖脚；body/shadow同源EXR并按实际承脚高度，仍是**静态竖直平面代理、源机体相机未注册**。
- RegisteredScene稳态不再读完整文件或hash。240次resolve计数保持1/1/1，显式刷新2/2/2；同mtime编辑必须刷新或重启。缓存38/深度65/旧注册46通过。不要再重跑或每帧hash。
- 真实启动暴露并修了两个接线缺陷：helper CLI import失效；PackageRunner未认识新增unit_id/catalog_key/declared_path来源字段。26 Python、真实configure→begin 41、实际F BoardView67/8draw、MapToken165项通过。native v1 exit2无帧保留；直接adapter测试不等于包启动成功。
- v2真实两轮1200/1200，158源前后相同。普通F9把长等待也录入，到上限正常退出于第二轮结果；不能算整包完成。全帧88个相邻RGBA代表/6板已审，长静止段不算运动。两个旧无声实际PTS片保留。
- Root从v2原00000发现**未选单位0/1占位**，不是机体被扣至0HP；engine始终12/12。shell.begin在建立focus后同步真实view.ui，首draw反例3fail→8项全过。v3原00000直接显示穿越机12/12。旧shell/capture字节副本均匹配v2源，不能混写新旧证据。
- 新显式 `--tactical-clips`：F9在board/summary arm，只真实execute录制，首个返回结果端点自动停。21状态、旧walk8、互斥flags exit2；真实v3三段均自动停，未注入输入/位置/时钟。原普通/walk模式保留。
- **v3完整实玩** `gui-f-depth-manual-v3`：281/281、158源稳定、writer pending0/errors[]，Root键鼠完成三轮→终局→结算概览/详情→显式确认2/2，F10 exit0。235地图回放采样/705单位行源与显示脚点核对无异常；v2/v3前两轮真实单位和目标结果相等。
- 实际终局：穿越机(4,3)12/12，灰机(5,3)8/8，金机(7,3)8/8，均仍在场；闸门0/2，未在时限撤出。两段soft_failure，世界事实{}、无奖励/维修虚构。2/2不是目标成功。
- Terra全看v3的136代表/9板及首帧/端点/末页原图；Root全程实窗、亲看关键原PNG与金标。三个实际PTS无声片在 `f-depth-v3-videos/`，8.159552/7.451512/8.551780秒，误差≤0.5ms；只执行片段，不是整场连续录像/声音验收。
- **v3后仅一字符修正**：结算提示误写L查看状态，实窗Z打开/关闭成功；关闭v3并核158源后改L→Z，旧源及settlement-key-hint-fix.json保留。未为此重跑三轮，不说v3已显示改后文案。

## 4. 当前停点：HP准备与实际绘制停录已修，强遮挡运动已录

本轮整合证据：`artifacts/formulas/production-lab-v1/qa/tactical-render-boundary-20260909/root-review.md`（完成跨日到09-10，目录保留开工日）。此前E/F标签、真实命中及401帧证据仍在 `tactical-readability-20260909/root-review.md`，旧完整交接另存 [_history/141-before-render-boundary-2026-09-10.md](_history/141-before-render-boundary-2026-09-10.md)。

- 空事件准备阶段按ExecuteHUD已绑定当前快照显示HP，标记current_packet_snapshot，与顶栏同源；不读后续engine。非法空间/HP仍拒绝。新增23/23、HealthHUD35/35；本次原生三个准备帧都显示12/8/8，没有HP待核回归。
- BoardView只在实际draw记序号；MapHUD新bind已draw才确认返回UI。采集器分别记录live shell/rendered frame，33/33与walk8/8；旧E00109实时已settle但像素execute的反例完整保留。
- F既有blocked(4,4)内加同源工业残骸：原181对象/镜头/4承脚三角形不变，新29mesh均在原格内；v1平板试样保留，v2加厚度/筋/折边/底撑。源 `artifacts/formulas/visual-targets-v1/art/tactical-corridor-occlusion-v1/README-v2.md`；res为`corridor-t2-occlusion-v2`。同次2×RGB/EXR，CPU(1,3)/(2,3)/(3,3)可见100%/80.99%/0%；初始(1,2)94.18%，不叫完全无遮挡。
- 新编译包fresh重建5JSON字节相同；相对F-depth-v1 tactical实际只registered_plate一叶变化，单位/时钟/碰撞/路线/意图/目标/结果不变，结算preset字节相同，source-map33/33可追溯。不是新实质输入。
- **真实正常行走** `gui-f-occlusion-v2`：R1 Down/Right/Right至(3,3)，R2 Left/Left退(1,3)，R3原地，均选runner_hold；没有摆位/时钟/结果注入。250/250、186源稳定、writer pending0/errors[]，handle8334 F10 exit0。三轮→结算概览/详情→明确确认2/2，两段soft_failure、事实{}、最终HP12/8/8与闸门0/2。
- 00053/00100是部分遮挡，00056–89完全遮挡；00108仍C4部分可见，00116到B4才完整恢复。实际终点00090/00174/00246均新rendered settle、presented且本次子HUD已画，Root看过原图。不能用字幕目标格代替移动中的身体格。
- 独立全看250帧的123相邻RGBA代表/8板，完整映射保留；Root全程实窗、关键原PNG及ITB/GF_PLAN金标对照。720次HP核对一致；last-drawn标签与postdraw即时token最大差1.698451设计px/0.029698格，保留采样时点差异，不称锚点精确相等。
- 三个实际PTS无声MP4在 `f-occlusion-v2-videos/`，19.621025/22.997539/6.431309秒，最大误差0.499ms；首两段包含真实计划等待，各1终末重复帧有说明。新encoder按已呈现终点切片，旧encoder/原PNG不改。
- Root收尾另发现board arm被新board draw提前取消：34项1失败→仅限settle分支→34/34、walk8/8。另短实窗`gui-board-arm-v1`5帧/186源稳定，三次新board仍armed，唯一stop是F9显式取消，handle82503 F10 exit0。250帧用此前采集版本，字节副本`capture-before-board-arm.gd`保留；不冒称最终小修已重录整场。

## 5. 制作判断与后续差距

本轮实际读138§4.1/4.2、直看ITB意图战场与GF_PLAN，再对照F路线→执行→结果。空间仍保持整队一次提交/同场结果，未抄ITB单机即时行动或Y精神。Y指令菜单、声音等缺帧未补，不扩大验收。

E/F名字、HP、格位、准备快照与实际绘制终点已修，不重做。下一可见增量先改善同源工业环境的材质/光照、低对比接触影和孤立残骸的场景关系，以本次源与真实路线对照；不再堆采集门禁。随后继续140七公式完整能力与第二实质输入主线。

- 本次F已补进/退完全与部分遮挡的真实运动；只覆盖此路线/三台现有PNG/新残骸，不等于任意路线或所有场景遮挡通过。原城市J/K摆位仍只证明校准。
- 城市沿街体量/灯光材质、近景execute的独立镜头、身体攻击/受击、角色规格/生活动作、声音均未收口。PNG位移不是动作，三图alpha批准不是新模型或角色动作批准。
- T5完整能力包含具名防线失败、现场取盾、条件反击、带伤损衔接；不能用三轮护线QA替代。三轮保护对象优先/防线优先提案仍待答，且旧解构“撤离后取盾”与新Reader“先取盾挡击后撤离”顺序冲突未裁决。方案在 `qa/tactical-t5-design-20260909/tac-t5-smallest-complete-design.md`。
- WR下一周期的具名主体、未选请求与第二次承担扣格方案仍待答；首次commit/arrival不代表完整多周期。不得按沉默实现。
- TAC_T4–T11、完整WR_T1/T2、其余六公式第二输入质量、角色存在感、声画与可编辑生产继续按140推进；capability_gap不是永久排除理由。

## 6. 已闭合工作：按证据查，避免重做

以下均相对 `artifacts/formulas/production-lab-v1/qa/`；更细进度在归档141与各主审文件。

| 已闭合增量 | 证据入口与边界 |
| --- | --- |
| E/F HP命中、多敌HUD、闸门完整度、三张alpha与真实第二轮 | tactical-package-capture-v1/review-20260908-hp-motion/ROUND-REVIEW.md；Full/Skip真实账一致，无音轨，不等于动作/声音或视觉通过 |
| G/H派遣→行走/观察/归档/报告 | world-route-production-20260909/manual-g-review.md、manual-h-and-branches.md；G/H均实际3/3，后续队伍未出发 |
| G器材棚箱前/箱后深度、H三室同源环境/呈现watchdog/拒门反馈 | 同目录 g-shed-depth-v2-root-review.md、h-environment-root-review.md；原始失败/新PNG/实际PTS分开，完整运动已审，不重做 |
| J试验后复核/原书页范围标记、同室看正文、未试验拒绝 | hub-review-production-20260909/j-review-root-review.md；四轮真实操作、源稳定、重建一致；人物生活动作/声画未过 |
| 备用目标ID+格同步与情报source换行 | tactical-fallback-objective-20260909/fallback-root-review.md；旧失败保留，最终两轮6原帧/128源/23核对；不是T5 |
| 城市同源2×背景/EXR、镜头缩放平移与占格 | tactical-city-environment-20260909/root-review.md；完整重建、原生镜头四轮完成，城市仍blockout |
| 战术body/接触影城市原生摆位校准 | tactical-depth-integration-20260909/root-review.md；完整/部分/全遮挡18原帧、shader与脚点反例修复；仅摆位，不是运动/生产输入 |

## 7. 工具与进程

Godot `/Applications/Godot.app/Contents/MacOS/Godot` 4.7；Blender `/Applications/Blender.app/Contents/MacOS/Blender` 4.4.3；ffmpeg `/opt/homebrew/bin/ffmpeg`；PIL Python `/Users/rayz/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`。

新capture必须fresh目录，录制期间冻结相关源码，保存同一进程handle；F8检查点、F9 arm、F10排空退出。只在冻结边界做必要hash，不每帧hash或反复全项目审计。相邻RGBA比较用于离线全帧审阅，不改原PNG。

上一轮F深度GUI v1配置失败exit2、v2上限退出exit0、v3 F10 exit0；E/F标签、本轮F强遮挡250帧与board-arm短验证窗口均已F10排空exit0，全部已结束。没有需要用户解锁后继续的遗留窗口。先确认进程归属再操作；历史未接管headless PID79583以及旧Blender MCP不按旧PID直接kill。CUA选择已退出Godot可能打开项目管理器，须先核日志/handle。

后续报告只写实际改变、真实操作/原帧、剩余差距与必要决策点。140目标没有缩小，不代签用户视觉验收。
