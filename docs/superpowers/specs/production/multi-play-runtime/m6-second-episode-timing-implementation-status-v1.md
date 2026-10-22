# 《超GAG机器人大战》多玩法运行时 M6 第二 Episode / TIMING 复用状态 v1

> 日期：2026-07-15  
> 状态：`runtime_validation_passed + windows_export_artifact_passed`；候选运行时证据，不是正式 Episode 验收。  
> 对应蓝图：`2026-07-14-chao-gag-multi-play-implementation-blueprint-v2.md`。  
> 边界：验证第二地点、第二机体、第二 Episode 图和首个 `TIMING` 活动能复用同一因果运行时；不提升 V35.7/V35.8 候选 Canon，不把 C02E03 运行样例当成正式厚剧情、正式台本或资产锁。

## 1. 本轮结论

M6 已完成第二组内容复用证明：

- 地点从万机馆切换为 `LOC_MODEL_STREET` 旧件市维修棚。
- 机体从馆守 Z 切换为 `MECHA_OLD_BOXER_KING` 旧拳王机体。
- Episode 图切换为 `C02E03-MULTI-PLAY-M6-VALIDATION`，仍由同一 `EpisodeDirector -> ModeRouter -> RunStateStore` 编排。
- 模式仍为 `NARRATIVE -> SPATIAL -> TACTICAL -> NARRATIVE -> DESK`，没有复制第二套章节总控。
- `SPATIAL` 同场托管一个 `CONSTRAINT` 维修计划和一个 `TIMING` 身体反馈校准，并把两者合成为一次不可重复提交的 `ActivityOutcome`。
- 四档 `perfect / good / clear / fail` 都可继续进入战棋；偏差变成机体、地形、目标完整度和未结债务，不形成重试墙。

这证明“多玩法”的工程单位可以是同一个戏剧问题在不同玩家权能下被继续处理，而不是经营、修复、音游和战棋各自拥有一套永久状态。

## 2. 可玩因果链

```text
直播要求复刻冠军动作
  -> 纪存与唐胶先检查旧拳王身体
  -> 玩家在人尺度维修棚持续行走，检查右拳、膝轴、影子录像、仓门或直播终端
  -> 把有限零件分给承力链、动作记忆与坍塌余量
  -> 三段 TIMING 接住右拳加载、转髋传力与漏拍停拳
  -> 两项活动合成一个事务和两个 BattleSetupPatch
  -> 旧件市擂台在第二回合坍塌并翻成仓库救援图
  -> 战斗结果进入唐胶/纪存反应场
  -> 临时维修否决权和原速录像原则进入关系状态与纪存笔记
```

右拳护具在这条链中只作为动作/规则锚点，不是参战单位。真正进入 Tactical 的是旧拳王机体。

## 3. 四次可见消费

### 3.1 当场消费：机体身体状态

维修分配与三段校准各自生成一个有界 `HybridActivityResult`，复合提交后立刻改变 `MECHA_OLD_BOXER_KING` 的维修方案和身体反馈状态。未提交草案不会进入统一状态，也不会出现在笔记覆盖层。

### 3.2 冲突消费：同场战棋 Patch

声明式战斗 `C02-M6-OLD-BOXER-ARENA-FLIP` 同时读取两项活动的 Patch：

- 维修计划改变仓门完整度、危险格或最低动力状态。
- 身体校准改变旧拳王 EN、停拳窗口、伤员完整度或影子残留。
- 第二回合固定触发拳台坍塌：新增阻挡格并把主目标从赛场胜负转为伤员与仓门。

因此玩家在短玩法里承担的不是抽象分数，而是稍后能指认的单位、道路和保护目标。

### 3.3 人物消费：维修权限与关系

战后反应节点读取实际 `TIMING` 档位和 `BattleOutcome`，再决定唐胶与纪存如何说话。结算写入：

- `JICUN_TANGJIAO_REPAIR_TRUST`
- 旧拳王 `repair_veto_recognized`
- 一条新的现场笔记

核心动作不是“好感 +1”，而是纪存保留原速录像、拒绝把停拳剪成胜利；唐胶因此取得一次临时维修否决权。

### 3.4 Desk 消费：玩家承担可回看的原则

结算不是自动播放摘要。玩家在纪存的 Desk 中重新看到维修方案、原速录像、战场结果与唐胶的否决权，再主动确认“保留原速、不替旧拳王剪出一次体面的胜利”。确认后，原则、关系变化和现场笔记一并写入统一状态；拒绝时仍可返回证据链检查，不以隐藏分数替代玩家承诺。

## 4. 交互与保存

维修棚使用连续人尺度移动：方向键/WASD、十字键或左摇杆按住即可持续行走，靠近热点后用 Enter/E/A 调查。至少检查两个部位后进入维修分配；重复调查只回看现场说明，不重复结算。

M6 相关场景已不再直接读取 `KEY_*`。`InputIntentTranslator -> InputRouter -> ModeScene` 把键鼠和手柄翻译为共享意图：导航、确认、取消、信息、笔记本、子活动主/次操作和阶段菜单。进入 `CONSTRAINT/TIMING` 时，`activity` 输入上下文压住底层 `SPATIAL` 移动；返回探索后恢复。战棋中 `W` 只能是向上导航，不再同时表示撤离；`E/Start` 先打开阶段菜单，结束阶段或撤离都需要再次确认。

未完成状态可保存并精确恢复：

- 玩家位置。
- 已检查热点。
- `CONSTRAINT` 卡片/责任槽安排。
- `TIMING` 当前阶段、指针、按住时长和既有尝试。
- 复合结果是否已形成、是否已正式提交。

正式提交后事务 ID `M6:C02:WORKSHOP:COMPOSITE:V01` 最多出现一次；拒绝提交会重新开放原草案，不会清空选择。

M6 可视入口现内置本地盲测回执，不上传数据。每次运行会在 `user://chao_gag_playtests/` 写入独立 JSON，并刷新 `latest-m6.json`。回执 v2 记录：

- 各节点访问次数与停留时间。
- 手动存档、恢复和笔记覆盖层使用次数。
- 每次正式事务的结果、活动档位、Patch 和未结债务数。
- 最终活动档位、战斗结果、关系边 ID、事务顺序和完成/中退状态。
- 运行系统、启动时手柄数量，以及键盘、鼠标、手柄在各输入上下文和五个 M6 节点中的已接受意图次数。
- `TIMING` 使用的按下/松开次数，但不保存原始键序列、手柄名称、VID/PID、用户路径或网络信息。

它只能提供定位证据，不能把开发者自测冒充真人盲测。

## 5. 主要实现资产

- Episode 图：`game-godot/content/episodes/runtime_validation/m6/graph.m6.json`
- Manifest：`game-godot/content/episodes/runtime_validation/m6/manifest.m6.json`
- 维修活动：`game-godot/content/activities/constraint/c02_old_boxer_repair_plan_validation.json`
- 时机活动：`game-godot/content/activities/timing/a003_old_boxer_missed_beat_validation.json`
- 战斗定义：`game-godot/content/episodes/runtime_validation/m6/battle/c02_m6_old_boxer_arena_flip.json`
- 维修棚宿主：`game-godot/scripts/modes/multi_play/c02_m6_old_boxer_workshop_mode.gd`
- 战后反应：`game-godot/scripts/modes/multi_play/c02_m6_old_boxer_reaction_mode.gd`
- 可视入口：`game-godot/scenes/multi_play_m6_validation.tscn`
- 自动验证：`game-godot/scripts/multi_play_timing_m6_smoke_test.gd`
- 本地盲测回执：`game-godot/scripts/core/validation/multi_play_playtest_recorder.gd`
- 回执自动验证：`game-godot/scripts/multi_play_playtest_recorder_smoke_test.gd`
- 共享输入翻译：`game-godot/scripts/core/input/input_intent_translator.gd`
- 输入自动验证：`game-godot/scripts/multi_play_input_intent_smoke_test.gd`
- Windows 真机验收器：`scripts/windows-m6-platform-acceptance.ps1`
- Windows 验收手册：`production/multi-play-runtime/m6-windows-controller-acceptance-runbook-v1.md`
- 内容 Bundle 构建链：`production/multi-play-runtime/m6-content-bundle-build-chain-status-v1.md`
- Narrative / Desk 生产壳：`production/multi-play-runtime/m6-narrative-desk-production-shell-implementation-status-v1.md`
- 共享人物演出：`game-godot/scripts/core/presentation/narrative_director.gd`
- 共享责任工作台：`game-godot/scripts/core/desk/desk_workbench.gd`
- 统一启动器：`game-godot/scenes/startup_router.tscn`
- 启动合同自动验证：`game-godot/scripts/startup_router_smoke_test.gd`

## 6. 已验证门禁

2026-07-14 已通过：

```text
/opt/homebrew/bin/godot --headless --path game-godot \
  --script res://scripts/multi_play_timing_m6_smoke_test.gd

MULTI_PLAY_TIMING_M6_SMOKE_OK
```

同轮还通过：

- Godot 4.7 全项目编辑器脚本扫描。
- `scripts/godot-test.sh` 全量运行回归，包括 M1、M4、M5、M6 与盲测回执。
- 四档 `TIMING` 结果、一次性提交和拒绝后恢复。
- 两项活动合成一个事务、两个 Patch。
- 第二 Episode 四模式结构和旧件市/旧拳王 Canon 引用。
- 维修棚中途存档/恢复。
- 五节点完整流转和四次可见消费；Spatial 对象状态、Tactical 继承、人物关系与 Desk 承诺均可复核。
- 本地回执写入、幂等结束、节点计时、存取/笔记计数和最终因果摘要。
- Godot 窗口从开场、维修棚、约束分配、`TIMING = fail`、Tactical 撤退、人物反应、Desk 到统一档案的完整可视流程。

同轮生成一份 `scripted_ui_validation_not_human_blind_test` 本地回执：五个节点各访问一次、五个事务各提交一次，`CONSTRAINT = perfect`、`TIMING = fail`、两个 Patch、`BattleOutcome = withdrawal`、两项未结债务和 `JICUN_TANGJIAO_REPAIR_TRUST` 均在最终摘要中可见。脚本化操作总时长约 42.3 秒，只证明回执与窗口流程接线，不代表真人首玩时长或可理解性。

2026-07-15 又通过了两项平台门禁：

- 键盘与合成手柄事件共用输入意图，包括 A/B/X/Y、View、Start、D-pad 和左摇杆；子活动压栈、长按/松开、阶段菜单二次确认已自动验证。这是代码路径证据，不等于实体手柄人工验收。
- 用 Godot `4.7.stable.official.5b4e0cb0f` 官方 Windows x86_64 release 模板重新生成 `outputs/windows/chao-gag-m6-validation.exe`。`file` 识别为 `PE32+ executable (GUI) x86-64`，大小 137,283,648 bytes，SHA-256 为 `0eca9ef3e740b3140e0a339edcddedcd50727414becaed427fe8a3216cc82f7a`。从 EXE 偏移 109,049,856 读取 28,233,776 bytes 的嵌入 PCK，与独立导出包逐字节一致，SHA-256 同为 `1a5af21211a290abce7cd328fe0e6b833b1e23bbd13d7ab0dc5ff5af8fd1ccb5`；包内 58 个必需路径、统一启动器、回执 v2、M6 图/活动/战斗、共享 Narrative/Desk 壳、StableObject、LocationScene、Spatial NPC、InteractionDirector、NarrativeOverlay、BattlePresentationCatalog/Director/Player、TacticalUnitVisualRenderer、九个地图视觉、八个程序化 profile、旧拳王表现清单/地图图/Pose、P4 两个体验验证器、三张背景、两张人物图、五节点转场、演出/同物连续性/Spatial/体验结构编译合同以及 `runtime_validation_only` 边界均通过。M6 bundle 的源指纹为 `b838cddf609cc4b1eaf7d70677d9415c83906378a6682d8f027d6889409aa34c`；包内状态明确为 `structure_pass_capacity_pending`。
- 已实现 `scripts/windows-m6-platform-acceptance.ps1` 与配套验收手册。它会先校验制品哈希，再要求新鲜 Windows 回执、五节点/五事务完成、实体手柄在五节点及五种输入上下文均留下意图，并收集中文字体和布局人工确认。工具状态为 `ready_for_external_validation`，尚无外部验收回执。
- M1/M4/M5/M6 已改由确定性 Episode bundle 驱动；M6 的 Graph、`CONSTRAINT`、`TIMING` 和战斗定义形成自包含引用闭包。构建器会阻断未知场景、未声明资源、战斗对象越界及活动 Patch 无消费者，运行入口不再主要依赖散装源 JSON。
- M6 五个节点已加入声明式因果转场；覆盖层显示地点、时间、上一事实与下一责任，切换期间冻结 Mode 并阻断全局输入。五个唯一 ID、跳过恢复、bundle 缺失阻断和 1280×720 中文像素排版均已验证。该层只改善交接可理解性，不替代真人理解门禁。
- M6 维修棚六个对象已生成稳定 `Area2D` 节点；`InteractionOffer` 负责首轮、重复、条件解锁与显式活动入口，统一对象状态跨存档进入 Tactical。右拳、膝轴、影子录像、仓门、直播终端和零件盘均有具名战术映射，缺失映射会阻断 Bundle 构建。

## 7. 尚未证明

M6 仍不等于多玩法架构已成为 Working Canon。以下门禁未完成：

1. Windows 真机启动、中文字体、`user://` 存档/回执和完整流程验证；验收器已经就绪，但本机无 Wine/Windows 运行环境，当前只能宣称 Windows 导出制品通过。
2. 外部真人盲测，包括可理解性、实际时长、实体手柄与软失败接受度。
3. 正式 C02E03 Pressure Board、厚剧情、台本、角色语音和资产生产验收。
4. `SIGNAL` 第三类活动语法。
5. 正式过场、音乐、机体动画、人物立绘与可售卖级视觉表现。

2026-07-15 已补入三张 M6 候选背景、纪存/唐胶人物图、共享 Narrative 演出和主动 Desk 工作台，并通过像素/状态验证；这些只缩小了验证界面与生产界面的距离，仍未构成正式 C02 分层资产、表情差分、机体动画、声音或美术验收，所以上述生产门禁保持未通过。

因此当前正确状态是：**M1-M6 运行时证明与 Windows 导出制品通过；Windows 真机、实体手柄、真人盲测、生产与内容验收未通过，蓝图继续保持候选实现方案。**

## 8. 下一步

最高价值顺序应为：

1. P4 已接入 Bundle Compiler；下一步取得真人首玩容量和五项普通语言理解回执，不能用结构 PASS 替代。
2. Spatial 候选生产层已补齐房间/返回点/动态 NPC/NarrativeOverlay，P3/P3b 已补旧拳王候选地图图、Pose、Cut-in、状态演出及九实体 A 档地图识别；下一步补正式地图分层、碰撞、步行动画，以及 Tactical 正式 Sprite、动作与音效资产。
3. 把 M6 可视流程交给真人从头玩一遍并收集 `latest-m6.json`；结合访谈记录卡点、误读和是否记住“停拳”与最后承担的责任。
4. 在 Windows 真机运行 `scripts/windows-m6-platform-acceptance.ps1`，验证最新 EXE 的启动、字体、存档、回执与实体手柄，并形成可复核验收回执。
5. 选择通过 Pressure Board 与 Reader 的正式 Episode 做 P5 生产验收；`SIGNAL` 继续关闭。
6. 将通过盲测的因果链移植到正式单话生产包，不直接把验证台词和候选运行美术升格。
