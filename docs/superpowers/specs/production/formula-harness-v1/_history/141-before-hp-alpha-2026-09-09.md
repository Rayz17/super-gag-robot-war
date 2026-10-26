# 141 · 公式台新任务开发交接

交接日期：2026-09-08。工作区：`/Users/rayz/Documents/超gag机器人大战`。
分支：`codex/srw-kernel-sandbox`。状态：Candidate / not_canon / 七公式用户视觉验收未完成。
用户因上下文/额度负担换任务。本轮只收拢与交接，没有继续实施下列未完成工作。

## 1. 新任务先做什么

1. 完整读本文件与 [140 唯一执行目标](140-formula-lab-integrated-visual-production-goal.md)，依项目 `chao-gag-canon` 技能核对 Candidate 边界。
2. 核验当前目录和少量相关代码；保留共享工作树，不因旧任务停止而清理文件。
3. 先补 **实际命中 HP 回执与显示时序**，再跑 E/F 第二轮真实运动采集并逐帧看效果。不要先补报表、重做全部场景或重开旧失败分件路线。
4. 按 140 §8.1 动态选择 subagent 模型，不固定 Sol/Astra；简单可验证任务在质量与接口支持允许时优先 `gpt-5.3-codex-spark`，复杂任务直接选胜任模型。主对话负责设计、整合与最终判断；每刀有文件所有权、证据和停止点。
5. 紫/白青/靶机透明修复仍待明确许可，可与 HP 工作分开；其他已有授权无需重新问一遍。

本文件是交接时核验的快照，不是新任务已验证状态。137 为制作框架，138 §2.3 为七公式融合依据，139 为旧历史；按需查，不全量重载。

**金标不能省略：** 140 §4/§4.1 已补齐商业游戏逐公式分工与对照要求：机战 Y／陷阵之志；金偶像／Obra Dinn；Outer Wilds；XCOM 2／Banner Saga；机战30；Citizen Sleeper／风花雪月／Hades。Dialogue Manager、Popochiu 是开源实现参考，GF 是项目内效果图，不能混称或互相替代。具体公式开工时必须取 138 对应案例、融合取舍和已核验帧，与实际产物比交互/演出差距；“138 按需读”不等于可以不参照金标。这里只恢复既有参考，不新增 Canon/正式美术授权，也不让旧 Hub 强制开场覆盖自然返馆裁决。

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
| G | package-g-world-exploration-v3 | 地区图明确派巡访员→实际 C 探索→报告 |
| H | package-h-world-exploration-v3 | 地区图派巡访员→实际 D 探索→报告 |
| I | package-i-hub-in-room-v1 | 自然返馆、走近闲聊/工作、一次提交、同室看后果 |
| J | package-j-hub-in-room-v1 | 实际试验结果约束返馆安排→同室后果；无强制 Arrival 立牌 |

统一浏览器（仓库根目录）：

```sh
/opt/homebrew/bin/godot --path game-godot res://scenes/formula_lab/formula_lab_package_browser.tscn
```

直接包入口：

```sh
/opt/homebrew/bin/godot --path game-godot --windowed --resolution 1280x720 res://scenes/formula_lab/formula_lab_package.tscn -- --package "/Users/rayz/Documents/超gag机器人大战/artifacts/formulas/production-lab-v1/builds/package-e-registered-map-v1/flow.json"
```

重建用各包 `REBUILD.txt` 与 `source-map.json` 的真实输入；生成器 `scripts/formula_production_lab.py`，外层 `scripts/formula-desk`，走 `--candidate-lab`。输出用新目录，不能覆盖来源或抬升正式冻结门。

当前仅七种受限组合、十份包，不是任意 Reader/地图编译器。G/H 仅先遣到场，不等于整队/重机旅行；WR_T1/T2、下一周期与所有下游消费未全部接入。全部预设覆盖、第二输入质量和编辑生产能力仍须按 140 继续扩展。

## 3. 最近一轮的真实停点：不要把“派过单”算作完成

| 项目 | 实际状态 | 下一步 |
| --- | --- | --- |
| E/F 注册环境与同场结算 | 已接入、已有实际 GUI 帧；不是金标验收 | 保留，继续修运动/声画 |
| 注册网格降噪 | 代码与定向单测通过，尚未实窗复拍 | 随 E/F r2 检查 |
| 连续运动采集器 | 代码完成；修复后逻辑 14/14、check-only clean | r2 尚未录制 |
| HP 命中回执/显示 | **未开始**，没有半成品 helper/HUD 接线 | 下一项实现 |
| 紫/白青/靶机透明修复 | 问题已定位，**许可未答复** | 不因换任务视为批准 |
| 双人共骨架静态板 | 比例可核对，维护员身份/画风失败 | 不动画、不默认替换 |

### 3.1 E/F 已完成的工程增量

- 场景注册 schema 2：`candidate_tactical_orthographic_v1`，执行声明 `map_event_time_v1`。
- 同源 Blender 几何→PNG/注册，连续地面、屋顶实体、初始障碍/出口；事件阻挡不烘焙。
- 规划、执行、结算共用仿射镜头（当前 1.55），保留旧 schema 1 的 T3/SET 适配。
- 生产器拒绝声明但丢失/不匹配场景，报告可执行缺口；实际重新生成 E/F 并更新当前目录。
- E 实际成功于第 2 轮。F 有代价成功于第 3 轮，84/90 秒；runner HP12、alive=true、withdrawn=true，两个阻挡体存活 HP8、gate 0/2。
- 新旧包关键游戏结果一致；新包 Full/Skip 终局一致。不能据此宣称动画或游戏趣味通过。
- Root 亲看实际规划、摘要、执行入口、结算总览/详情。**03 执行截图只是 plan-locked 入口，不是命中帧。**

环境与证据（仓库相对路径）：

- `artifacts/formulas/visual-targets-v1/blender/tactical-pair-v1/revised-v2/build_environments_v2.py` 及同目录 t0/t2 输出。
- `revised-v2/qa/geometry-audit-producer-fixed.json`：格心落地、有限地面与 1/1.55 视域核对；不等于任意平移的全部遮挡证明。
- `game-godot/assets/formula_lab/temp/scenes/arena-t0-candidate-v1/` 与 `corridor-t2-candidate-v1/`。
- `artifacts/formulas/production-lab-v1/qa/tactical-package-capture-v1/gui-20260908-e-registered-map-v1/`、`gui-20260908-f-registered-map-v1/`：每包 7 PNG / 34 项检查。
- 同 QA 根目录 `headless-20260908-e-registered-skip-v1/`、`headless-20260908-f-registered-skip-v1/` 为 Skip 对照。
- 该轮局部门：map mode 63/0、旧 presentation 74/0、注册 v2 38/0、旧 tactical 29/0、旧 SET 18/0、生产 Python 5 项、browser 68 项，Godot Canon report/strict 通过。不要为接手重复跑全套。

### 3.2 已落盘但尚未合并实录证明的代码

网格：`game-godot/scripts/formula_lab/shells/tactical/tactical_board_view.gd`；
专测：`game-godot/tests/formula_lab/tactical_registered_grid_test.gd`。
schema2 先画阻挡填充，每条共享边只画一次（T0 82、T2 104）；规划灰青 .38/1.05px、执行 .20/.9、结算 .12/.8。旧场景、坐标与规则未改；仅专测通过，**无新像素判断**。

运动采集：
`game-godot/tests/formula_lab/production_tactical_package_capture.gd` 与
`production_tactical_motion_capture_logic_test.gd`（同目录）。
可选 `--capture-motion`；保留原七检查点与 Driver 输入，用自己 Viewport、真实时钟采样，不写世界时间或位置。
目标采样 12fps，阶段/presentation id/clip 改变时额外捕获；记录实际时间、迟到/漏采、阶段和脚点。idle_wait/presentation_only 单列合法阶段；headless 运动模式拒绝。
当前 14/14 逻辑通过，只证明采集逻辑；`health_playback` 仅可选透传，运行时尚未实现。

r1 已结束并保留：
`.../gui-20260908-e-motion-r1/`（47 运动帧）、
`.../gui-20260908-f-motion-r1/`（122 运动帧）。
原 Driver/七检查点通过，但错误的“每帧都必须 active”断言使整轮 exit1；后来修了断言/阶段捕获，**r2 未跑**。r1 有真实移动，约 95ms 的接触未被稳定采到；不能从修过代码推定新捕获已成功。

## 4. 下一刀：HP 时序与 E/F r2

目标是“画面在接触时才呈现本次伤害”，不改数值/战斗规则，不从结果编造伤害前状态。

1. 在 `tactical_round_engine.gd` 的实际扣血位置冻结 `hp_receipt`：
   `unit_id / hp_before / hp_after / hp_max / applied_damage`。禁止用“最终 HP＋伤害”倒推，过杀会错。
2. 新建纯表现辅助（建议名 `formula_lab_health_playback.gd`，**当前不存在**），用回执链与该 packet 的 units_after 校验；支持多次命中、过杀、缺/坏回执、旧记录回退，不修改 engine/world。
3. HUD 仅在 spatial/map 模式按准备阶段显示之前值、接触后显示之后值；伤害文字不抢跑。旧无回执明确使用已结算回退；输出可审的 `health_playback`。
4. 先真实引擎＋helper/HUD 定向测试，再用新采集器录 E/F r2，检查 HP、接触、身份、回到地图与 Full/Skip 同结果。网格降噪同时实看。
5. 实录仍粗糙就列可见问题继续修，不能宣布整段通过；透明许可未答复时保留明确缺陷。

主要实现路径（前缀 `game-godot/scripts/formula_lab/`）：
`formula_lab_package_runner.gd`、
`shells/tactical_lab_shell.gd`、
`shells/tactical/tactical_round_engine.gd`、
`shells/tactical/tactical_board_view.gd`、
`widgets/formula_lab_execute_hud.gd`、
`widgets/formula_lab_execute_presentation.gd`、
`widgets/formula_lab_spatial_playback.gd`、
`formula_lab_registered_scene.gd`、`formula_lab_tactical_camera.gd`、
`tactical_settlement_receipt.gd`、`shells/production_settlement_lab_shell.gd`。

录制命令（完成上面实现后再运行，输出目录尚不存在）：

```sh
/opt/homebrew/bin/godot --path game-godot --windowed --resolution 1280x720 --script res://tests/formula_lab/production_tactical_package_capture.gd -- --capture-motion --case E --mode full --package "/Users/rayz/Documents/超gag机器人大战/artifacts/formulas/production-lab-v1/builds/package-e-registered-map-v1/flow.json" --out-dir "/Users/rayz/Documents/超gag机器人大战/artifacts/formulas/production-lab-v1/qa/tactical-package-capture-v1/gui-20260908-e-motion-r2"
```

F 用 `--case F_EXIT`，换 F 包与 `gui-20260908-f-motion-r2`。预计 E 20–35s、F 40–70s；保留并轮询同一 handle，不自动重启。视频按实际采样时间合成，不能用恒定帧率掩盖丢帧，也不能声称录到了未采集音频。

## 5. 美术问题、失败路线与待答许可

**透明问题已定位在现有衍生资产，不是新地图 shader：**

- 原图 `game-godot/assets/formula_lab/temp/mecha/mecha-tide.png`、`mecha-lin.png`、`mecha-doll.png` 都是 1024² RGB，身体基本完整但有背景。
- `temp/cutouts/` 内 tide 有暗底/穿孔，lin 有棋盘背景/穿孔，doll 裁掉脚部。
- `formula_lab_placeholder_art.gd` 约 494–519 行优先使用这些 precut；UnitPlate 正在显示已有坏衍生图。
- `white-local-parts-v1/source-alpha-r2/source-cutout.png` 虽局部 mask 更好，但属于失败分件路线，不自动复用。
- 本轮一次紫机内置出图仍返回无 alpha 的烘焙棋盘背景且改动细节，已否决、未复制/接入；不要继续同一路反复出图。

未答复的原问题（换任务不构成许可）：
> 是否允许对现有紫机、白青机及靶机的原图做本地透明蒙版修复？只保留原 RGB、清除背景并逐张检查完整轮廓，检查合格后用于公式台候选；不新增设计、姿态或动画，不复用失败分件，不调用付费服务，也不代表正式美术验收。

其他边界：

- T3 新重击音效可作为候选默认方向；全段未验收。
- 白青 Blender 母型和本地分件 R1/R2 身份/姿态失败，停止扩展，无第二机/动画/默认替换授权。
- 双人静态板在 `artifacts/formulas/visual-targets-v1/art/hub-halfq-pair-spec-v1/blender-pair-v1/`，见 README 与 `revised-v2/pair-front-review.png`。
- 共用骨架、实际四头身比例改善了不一致，但维护员像巡访员换色，未过身份与风格。原批准仅正面静态，不扩动作/动画/default；不能声称人物最终选 Blender。
- I/J 正式生活动作（归档、坐下休息、清点工具）仍缺；C/D 的朝向、步态、同屏画法与对白衔接也要继续精修。
- I/J 可见证据：`artifacts/formulas/production-lab-v1/qa/hub-package-capture-v1/i-natural-final.mp4` 与 `j-natural-final-r2.mp4`，各有 9 个实帧；证明自然返馆流程，不证明身体表演通过。
- E/F 当前环境仍低于 GF，机体攻击/受击动作、打击感、声音与字幕节奏未完成。不能因空间比旧版好就忽略身份或内容错误。

## 6. 工具、工作树与在途状态

- Godot `/opt/homebrew/bin/godot` 4.7；Blender `/Applications/Blender.app/Contents/MacOS/Blender` 4.4.3；ffmpeg `/opt/homebrew/bin/ffmpeg`；Python `python3`。
- 当前工作树大量共享修改/未跟踪文件；Formula Lab 多数文件未跟踪，git diff 不能代表完整交付。保留，不 add/commit/reset/清理。
- 原相关 Sol 工作已收拢，无其拥有的活采集进程；本交接只做文档整理/审读，不继续运行时实现。
- 交接抽查时旧用户 GUI PID63285 已不在；不是本轮关闭的。勿按旧 PID 操作。
- PID79583 当时仍是约 18 小时的旧 `production_package_briefing_test.gd` headless Godot（PPID97977）。不属于本轮可确认所有权，不随意 kill；重启同名测试前先核验活性与所有者。
- 旧 blender-mcp 45400/45401 也不属本轮，保留。PID 只是时点证据，新任务必须重新核验，不能用旧数字直接杀进程。
- 不把本目标接回 C04 章内容；剧情任务有自己的生产链。新任务也不要因收到剧情回执自动停下 Formula Lab 转去章审。

## 7. 交付节奏与完成判断

建议下一任务第一轮只完成 §4：主对话先确定 HP 回执/显示合同，再按能力与总消耗选择 1–2 个 subagent，分工内核/纯辅助与 HUD/定向测试，约定 API 与文件所有权。简单查找、机械修改、现成测试优先评估 Spark；复杂因果与视觉身份审核不强制先试 Spark。主对话组织实帧审查并保留整合责任；并行互相阻塞时改为一个任务，不为拆分而拆分。

第一轮回报只回答：哪些代码已落盘、实际 HP/接触与旧版比改善了什么、哪些帧证明、还有什么未过、下一刀/用户需决定什么。
此后按 140 推进其余公式与轨 B，不把 E/F 收口当全部目标完成。任何机器 PASS 不代签用户视觉验收。

## 8. 新任务启动提示词

> 在当前工作区继续公式台开发。先完整读取 141-formula-lab-fresh-session-handoff.md 和 140-formula-lab-integrated-visual-production-goal.md；137/138 按需查，不重载旧对话。按 140 的七公式体验＋可复用内容生产完整目标执行，金标参考与实际试玩对照不得省略。先核验 141 停点，完成 HP 命中回执/显示与 E/F 第二轮真实运动录制，逐帧审核后继续打磨。主对话可按任务及模型实际能力，选择任何当前 subagent 接口支持的模型，不固定 Sol/Astra；保证质量、能力适配且可调用时，简单任务尽量优先 gpt-5.3-codex-spark。以包含上下文、推理、工具输出与返工的总 token/额度消耗最小为目标，复杂任务直接选胜任模型，发现不胜任及时升级，不无限试错。主对话负责整合与最终判断。保留工作树和 Candidate 边界，不重做已完成内容，不复用被否决资产。待答透明修复许可不当作已批准；重大决策给我方案和确认点。先简短报告核实状态、交接差异与首轮分工，然后直接开始可执行工作。

历史精简前目标见 [140 原文归档](_history/140-before-handoff-2026-09-08.md)，只追溯时读，不再作为“当前下一步”。

交接文档校核：140 原文归档与精简前快照逐字一致（SHA-256 `ce55c107f4c32d920bdfc7ae6c192a47f5fe7582d87b3732f8b02ab8628eda37`）；140/141 文档链接、十个当前 flow、关键证据路径均存在；HP helper 与 E/F r2 目录确认尚不存在。Sol 独立审读确认七公式/轨 B 与小试批准范围未缩减或扩大，并补回显式模型分工与既有环境授权。本轮只修改目标/交接/入口说明，未 stage/commit，未以文档校核冒充运行时复测。
