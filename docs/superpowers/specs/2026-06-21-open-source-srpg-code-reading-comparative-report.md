# 开源战棋 / SRPG / 机器人战棋源码研读与《超GAG》内核重构报告 v0.1

> 目的：把此前读过的 SRC、SRW Engine MV、Godot 战棋项目，与本轮新增研读的 Cosmos War、Unity2D FireEmblemLike Demo、SRPGcore、Sulis、MegaMek、Project-Tactics、yohk 等项目放到同一个比较框架里。本文不是“开源项目列表”，而是回答：它们的源码里哪些结构能真正帮助我们把《超GAG机器人大战》的 demo 从“网页式流程”重做成可玩的机战式 SRPG。

---

## 0. 总结论

当前最优路线不是直接 fork 某个开源项目，而是：

1. **Godot 继续作为主工程**：视觉、动画、场景、资源管线和未来可发布性都更适合。
2. **自研一个轻量 SRW-like 行动内核**：核心是阶段状态机、行动上下文、命令队列、目标系统、战斗预测、战斗事件、剧情触发，不是堆按钮。
3. **用 SRC / SRPGcore / SRW Engine MV 学“机战语法”**：它们证明 SRPG 的骨架不是移动和攻击，而是“单位行动链 + 事件标签 + 战斗前后对白 + 胜败条件 + 地图触发”。
4. **用 Unity2D Demo / Godot 教程项目学“输入与格子实现”**：它们短小，适合落实移动范围、路径预览、取消、待机、敌方 AI 回合。
5. **用 Sulis 学“内容驱动内核”**：区域、触发器、对话节点、脚本回调、能力数据和战斗状态分离，对《超GAG》的探索/剧情/战斗混合很有价值。
6. **用 MegaMek 学“机体领域模型”**：不能复用代码和数据，但它的阶段报告、武器挂载、护甲部位、命中原因列表、移动路径对象，很适合启发轻量机甲规则。
7. **用 Cosmos War 学“机器人题材轻量目标与单位生产”**：它粗糙但直接致敬机战，工厂、主机、防守、EX 技能和回合结束判定可作为小目标类型参考。

一句话：**《超GAG》要做的是一个 Godot 版的“内容事件驱动 SRW-like 内核”，不是网页流程，也不是直接搬 Fire Emblem 或 BattleTech。**

---

## 1. 研读证据矩阵

| 项目 | 本地路径 / 状态 | HEAD | 许可证与风险 | 源码研读可信度 | 对《超GAG》的直接价值 |
|---|---|---:|---|---|---|
| SRC / SRC# | `external_repos/SRC` | `4c717b2` | GPL，不能并入闭源/商业主工程 | 高，已有独立深读报告 | 事件 DSL、话结构、战斗事件、地图命令、胜败条件 |
| SRW Engine MV Plugins | `external_repos/SRW-Engine-MV-Plugins` | `af6f9fd` | README 标 MIT，但含第三方插件/IP同人风险 | 中高 | 机战式行动状态、移动后菜单、战斗预测、地图攻击 |
| Cosmos War / 宇宙机器人大战 | `external_repos/CosmosWar_GDI` | `99251f0` | Apache-2.0 | 中高 | 机器人战棋目标、工厂、AI 主机、EX 技能、回合自动推进 |
| Unity2D FireEmblemLike SRPG Demo | `external_repos/Unity2D-FireEmblemLike-SRPG-Demo` | `331b639` | GitHub 识别 MIT；本地 LICENSE 需复核 | 中高，主要用 `git show` 读取 | MVC、命令队列、移动撤销、BFS/A*、敌方 FSM |
| SRPGcore | `external_repos/SRPGcore` | `b0b0077` | MIT；RPG Maker 生态另有使用边界 | 高 | RPG Maker 地图转 SRPG、事件标签、阶段/子阶段、目标选择取消 |
| Sulis | `external_repos/sulis` | `06be535` | GPLv3，资产许可混合；不可直接复用 | 高 | YAML/Lua 内容内核、区域触发、对话节点、能力数据、路径与回合 |
| MegaMek | `external_repos/megamek` | `cd64969` | GPLv3；数据/资产 CC-BY-NC-SA；BattleTech IP 风险 | 中高 | 机体/武器/护甲/阶段报告/命中原因/移动路径领域模型 |
| Project-Tactics | `external_repos/Project-Tactics` | `fb78c5d` | MIT | 中 | ECS/FSM/Prefab/DataSet 架构，而非完整玩法 |
| yohk | `external_repos/yohk` | `f10f63b` | 禁商用/限制再分发 | 低到中，Blender 旧格式未读到脚本文本 | 控制方案、结束回合、撤销、extent 技能增幅概念 |
| godot-tactical-rpg | `external_repos/godot-tactical-rpg` | `cfe785e` | MIT | 中高 | Godot 服务层、选择层、战场控制、3D 战棋输入 |
| Godot-4-Tactical-RPG-Tutorials | `external_repos/Godot-4-Tactical-RPG-Tutorials` | `d962818` | MIT | 中高 | Godot 4 移动后菜单、取消、待机、范围层 |
| godot-2d-tactical-rpg-movement | `external_repos/godot-2d-tactical-rpg-movement` | `40023de` | 代码 MIT，资产 CC-BY-NC-SA | 中高 | 2D 格子、路径预览、移动动画 |
| Legends of Majestic Steel | `external_repos/LegendsOfMajesticSteel` | `7d648c3` | MIT | 中高 | 技能目标数据、AI 评分、战斗状态拆分 |
| godot-tactical-rpg-lite | `external_repos/godot-tactical-rpg-lite` | `473ba78` | 根 LICENSE 未见，谨慎参考 | 中高 | `BattleSession`、`GridService`、`ActionRequest`、目标系统 |
| project-3-srw-multiplayer | `external_repos/project-3-srw-multiplayer` | `c955ea8` | 未见明确许可，IP 同人风险 | 中 | SRW-like 玩家流程、攻击预测、防御方选择 |
| SRPGWar | 未找到可本地核验源码 | - | 不明 | 低 | 只能作为搜索线索，不能进入源码结论 |
| Project-Amber | 未找到可本地核验源码 | - | 不明 | 低 | 只能作为搜索线索，不能进入源码结论 |

---

## 2. 直接结论：下一版 demo 应该吸收什么

### 2.1 必须先补“行动内核”，再谈 UI 美术

当前 demo 的根因不是素材少，而是缺少下面这条机战式行动链：

```text
unit_select
  -> command_menu
  -> move_preview
  -> moving
  -> post_move_command
  -> weapon_select
  -> target_select
  -> combat_forecast
  -> resolve_battle
  -> action_end
  -> objective_check
```

每个状态都要有明确入口、出口、取消路径和 UI 显示层。攻击范围没有敌人时，系统不能进入目标选择；移动后不能再次移动；待机和攻击才消耗行动；结束阶段是全局命令，不是单位命令。

### 2.2 必须做“剧本事件内核”，否则战斗没有意义

SRC、SRPGcore、Sulis 都说明了同一件事：SRPG 的战斗不是孤立小游戏。每个行动都应该能触发事件：

```text
话开始
地图开始
回合开始
单位行动开始
进入区域
攻击前
战斗后
HP 阈值
击坠
目标损坏
胜利
失败
战后记录
```

《超GAG》的探索、剧情、战斗要通过这个事件内核串起来。例如玩家在探索里调查了留言墙，就应生成战斗中的保护目标、专属台词、支援指令或战后变量，而不是只显示一段文字。

### 2.3 必须建立“内容数据层”

建议不要把角色、武器、关卡、台词写死在场景脚本里。下一版应至少有这些数据表：

```text
units/*.yml
pilots/*.yml
weapons/*.yml
episodes/*.yml
maps/*.yml
events/*.yml
conversations/*.yml
objectives/*.yml
```

Godot 场景负责表现，数据负责规则，事件负责串联。

### 2.4 不建议直接复用源码

可复用的主要是思想和结构，不是代码：

- GPL 项目：SRC、Sulis、MegaMek 不应直接复制代码。
- 同人/IP 项目：SRW Engine MV、project-3-srw-multiplayer 只可学习流程。
- 引擎不匹配项目：Cosmos War、Project-Tactics、MegaMek 不适合拿来改。
- MIT 教程项目：可参考实现方式，但也建议重写，保持 Godot 主工程口径统一。

---

## 3. 项目深读笔记

## 3.1 SRC / SRC#：最重要的是“话结构 + 事件 DSL”

独立报告见：

- `docs/superpowers/specs/2026-06-21-src-code-design-reading-report.md`

核心价值：

| 领域 | SRC 的做法 | 《超GAG》应吸收 |
|---|---|---|
| 一话生命周期 | Prologue / Start / Turn / Victory / Defeat / Epilogue | 每一话都必须有固定结构，不允许碎片跳转 |
| 事件标签 | 回合、攻击、攻击后、破坏、全灭、进入、会话、使用后 | 建立轻量事件触发系统 |
| 战斗前后对白 | 战斗本身触发角色关系和剧情 | 攻击/击坠/保护对象受损都能触发台词 |
| 单位数据 | 驾驶员、机体、武器、能力、道具、地形分离 | 角色和机体解耦，支持魔改投射 |
| 地图命令 | 全局地图菜单与单位命令分开 | 结束阶段、作战目的、系统放全局菜单 |

对第一章 demo 的启发：第一话不是“前厅 -> 战斗 -> 下一话”的页面流，而应是：

```text
Prologue 火灾冷开场
Start 闭馆、封存、万机馆空间建立
Explore 前厅/留言墙/展柜/0号侧廊
MapStart 封存线落下，目标对象上图
Turn 1 教学行动
AttackBefore 第一台封存机接近留言墙
DamageThreshold 留言墙/展柜受损
Destroy 第一台敌机被击破
Victory 保住或损坏多少对象
Epilogue 馆守Z胸牌亮起，火灾谜团延后
```

## 3.2 SRW Engine MV：机战式行动链的直接样本

已读重点：

- `SRW_GameState.js`
- `SRW_BattleCalc.js`
- `SRW_GridLayer.js`
- `SRW_BattleScene.js`
- `SRW_MapAttackManager.js`
- `SRW_Menus.js`

关键发现：

| 机制 | 价值 |
---|---|
| `actor_command_window` / `actor_move` / `post_move_command_window` / `actor_target` / `battle_window` 等子状态 | 证明机战式战斗必须是强状态机 |
| 移动后菜单 | 解决“移动后是否攻击/待机/取消”的核心手感 |
| 战斗预测缓存 | 攻击前必须展示命中、伤害、反击等承诺后果 |
| 地图攻击管理 | 后续做大范围梗武器、舞台机关、法务封存线可参考 |
| 死亡队列 / 奖励显示 | 战斗结算要串奖励、台词、目标，而不是即时消失 |

不要吸收的部分：

- 过重的 SRW 数值公式。
- RPG Maker MV 特有窗口和插件耦合。
- 同人项目里的具体 IP 数据。

## 3.3 SRPGcore：RPG Maker 插件里的“SRPG 状态语法”

已读重点：

- `SRPG_core.js`
- 插件注释中的事件 note tags、插件命令、脚本命令。
- `Game_System` 的 battle phase / sub phase。
- `Game_Temp` 的移动表、射程表、主动事件、目标事件、原始位置。
- `Scene_Map` 的 `normal`、`actor_move`、`actor_target`、`battle_window`、取消处理。
- `Window_SrpgPrediction` 的攻防预测。

最有价值的结构：

```text
battlePhase:
  initialize
  actor_phase
  auto_actor_phase
  enemy_phase

subBattlePhase:
  normal
  actor_move
  actor_target
  actor_command_window
  battle_window
  enemy_command
  enemy_move
  enemy_action
  invoke_action
  after_battle
```

SRPGcore 对当前 bug 的启发非常直接：

| 当前问题 | SRPGcore 的对应经验 | 《超GAG》修正 |
---|---|---|
| 攻击范围无目标会卡死 | 无效目标不会消耗行动，会回到选择状态 | 攻击按钮先检查可攻击目标列表 |
| 移动后不能退出 | 保存原始位置，取消可回滚 | `ActionContext.original_cell` 必须存在 |
| 结束回合不清楚 | actor phase 和 menu phase 分开 | 阶段结束放全局菜单 |
| 战斗无预测 | 预测窗口同时显示攻防双方行动 | 做轻量 `CombatForecast` |
| 剧情和战斗脱节 | RPG Maker 事件可作为单位、敌人、地形事件 | Godot 地图对象也应能挂事件标签 |

SRPGcore 的事件 note tag 也提醒我们：不要把“角色/敌人/机关/触发点”做成完全不同系统。统一为地图事件对象更灵活：

```text
MapEvent
  kind: actor | enemy | npc | objective | trigger | terrain_event
  unit_id?
  event_tags[]
  position
  enabled_conditions
```

## 3.4 Cosmos War：机器人战棋轻量目标与单位生产

已读重点：

- `README.md`
- `src/CosmosWar_GDI/Unit.cs`
- `src/CosmosWar_GDI/EXSkill.cs`
- `src/CosmosWar_GDI/CWMath.cs`
- `src/CosmosWar_GDI/Scene.cs`
- `src/CosmosWar_GDI/AIScripts/AIBase.cs`
- `src/CosmosWar_GDI/mapsettingsyntax.txt`

关键机制：

| 机制 | 源码观察 | 可迁移价值 |
---|---|---|
| 单位模型 | `Unit` 含生命、护甲、伤害、移动、费用、阵营、工厂/主机标识、等级、技能 | 可作为轻量机器人单位字段参考 |
| EX 技能 | 不同技能有射程与额外伤害 | 适合做《超GAG》的“标志性小演出技能” |
| 工厂与主机 | 工厂生产，AI 主机是关键目标 | 可用于保护/占领/截断敌补给目标 |
| 回合结束 | 当前阵营所有可动单位行动后自动推进 | 基础规则可学，但《超GAG》要加全局菜单 |
| AI 委托 | 选择单位、目标优先级、工厂生产策略拆成委托 | 可以做简单可解释 AI |
| 无目标处理 | EX 无目标时警告并回命令面板 | 直接对应当前 demo 的卡死 bug |

问题：

- `Scene` 类过大，输入、绘制、规则、动画混在一起。
- 普通攻击是碰撞式，攻击者与防御者位置处理很奇怪，不适合机战。
- 缺少剧情/事件/预测/反击。

结论：Cosmos War 不是主工程参考，但它适合给《超GAG》第一章加一些轻量目标：

```text
保护“万机馆核心展柜”
占住“临时修复工位”
阻止“封存工厂”每回合刷机
破坏“清算主机”让敌方停止接收命令
```

## 3.5 Unity2D FireEmblemLike SRPG Demo：命令队列、撤销和移动预览

已读重点：

- `BattleWorldManager.cs`
- `BattlePlayerUnit.cs`
- `BattleEnemyUnit.cs`
- `CommandManager.cs`
- `MoveCommand.cs`
- `ShowPathCommand.cs`
- `ShowSkillAreaCommand.cs`
- `SkillCommand.cs`
- `WaitCommand.cs`
- `_BFS.cs`
- `AStar.cs`
- `ModelBase.cs`
- `Hero.cs`
- `Enemy.cs`
- `SkillManager.cs`
- `SkillHelper.cs`
- `MapManager.cs`

关键结构：

```text
GameState:
  Idle
  Enter
  PlayerTurn
  EnemyTurn
  GameOver

CommandManager:
  willDoCommandQueue
  undoCommandStack
  curCommand
```

行动流程：

1. 选择英雄。
2. BFS 显示移动范围。
3. 点击格子后用 A* 生成路径。
4. `MoveCommand` 沿路径移动。
5. 移动后打开行动菜单。
6. 攻击显示技能范围。
7. `SkillCommand` 结算技能。
8. `model.IsStop = true` 后该单位结束行动。
9. 敌方阶段用 Wait / AIMove / Skill 命令串起来。

对《超GAG》的价值：

| 能学 | 为什么 |
---|---|
| 命令队列 | 动画、移动、技能、等待、回合切换可以顺序播放，避免状态跳变 |
| 撤销栈 | 移动后取消可以回滚 |
| BFS + A* 分层 | 范围和路径是两件事 |
| 敌方 FSM | 第一章敌人可以先做简单“接近目标/攻击保护物/攻击我方” |
| MVC + 事件中心 | 适合提醒我们不要让 UI 按钮直接改全部状态 |

问题：

- 更像 Fire Emblem，不是 SRW；没有移动后武器差异、反击选择、战斗预测。
- 空目标/技能无目标的恢复路径不如 SRPGcore 清楚。
- Unity 实现不能直接迁移到 Godot。

建议吸收：**CommandQueue + ActionContext + GridService**，不要吸收它的战斗复杂度。

## 3.6 Godot-4 Tactical RPG Tutorials / GDQuest / Godot Lite：Godot 落地参考

这些项目已在补充报告中读过，合并结论如下：

| 项目 | 最有用的地方 | 对《超GAG》的用法 |
---|---|---|
| Godot-4-Tactical-RPG-Tutorials | `GameBoard`、`Pathfinder`、`ActionMenu`、移动后 `Wait/Cancel` | 直接作为 Godot 4 行动菜单和取消流程参考 |
| godot-2d-tactical-rpg-movement | `Grid`、`UnitPath`、平滑移动、路径预览 | 战斗格子移动与探索小场景移动都可借鉴 |
| godot-tactical-rpg-lite | `BattleSession`、`BattleFlow`、`ActionRequest`、`CombatResult`、`Objective`、`GridService` | 作为《超GAG》自研内核的模块命名和边界参考 |
| godot-tactical-rpg | 选择服务、竞技场服务、镜头/输入拆分 | 如果做 3D/斜 45 度表现，可借鉴服务层和相机逻辑 |
| Legends of Majestic Steel | 技能目标数据、AI 评分、威胁范围、状态机 | 做中期技能系统和敌方意图时参考 |

对下一版 demo 的直接要求：

```text
BattleSession
  owns: units, map, objectives, turn, phase, event_bus

GridService
  owns: occupancy, passability, range, path

ActionContext
  owns: selected unit, original cell, moved path, command, weapon, target, forecast

PresentationQueue
  owns: camera move, dialogue bubble, cut-in, hit animation, result banner
```

## 3.7 Sulis：内容驱动内核的范本

已读重点：

- `sulis_state/src/game_state.rs`
- `sulis_state/src/turn_manager.rs`
- `sulis_state/src/path_finder.rs`
- `sulis_state/src/distance_finder.rs`
- `sulis_state/src/range_indicator.rs`
- `sulis_state/src/ai.rs`
- `sulis_module/src/ability.rs`
- `sulis_module/src/area.rs`
- `sulis_module/src/conversation.rs`
- `sulis_module/src/ai.rs`
- 若干 campaign / area / conversation / Lua 数据样例。

关键价值：

| 领域 | Sulis 的做法 | 《超GAG》应吸收 |
---|---|---|
| 世界状态 | `GameState` 管区域、队伍、任务、选中对象、路径、回调 | 建立全局 `RunState`，不要把关卡变量散在 UI |
| 回合管理 | `TurnManager` 管实体、效果、表面、光环、回调、战斗激活 | 战斗单位、地图机关、持续效果都进入同一回合内核 |
| 区域触发 | `OnCampaignStart`、`OnAreaLoad`、`OnPlayerEnter` 等 | 探索小场景必须有触发器 |
| 对话节点 | 节点、speaker 切换、response、脚本回调 | ADV 和战斗台词共用 Conversation 数据 |
| 能力数据 | AP、冷却、范围、AI data、脚本、升级 | 武器/支援/地图技能统一为能力数据 |
| 路径与距离 | 支持对象尺寸、占据、可见、障碍 | 机体大小和保护对象体积可以轻量支持 |

Sulis 对《超GAG》的最大启发是：**探索、对话、战斗不要做成三个互不认识的系统**。它们应共享变量、触发器和对象 ID。

示例数据方向：

```yaml
episode: ep01
areas:
  - id: hall_front
    triggers:
      - on: player_enter
        event: show_closing_broadcast
  - id: message_wall
    triggers:
      - on: inspect
        object: wall_notes
        set_flag: knows_message_wall_value

battle:
  map: ep01_hall_battle
  objectives:
    - protect: message_wall
      if_flag: knows_message_wall_value
```

## 3.8 MegaMek：机体领域模型与阶段报告

已读重点：

- `README.md`
- `LICENSE`
- `megamek/common/enums/GamePhase.java`
- `server/AbstractGameManager.java`
- `server/totalWarfare/TWPhaseEndManager.java`
- `common/moves/MovePath.java`
- `common/units/Entity.java`
- `common/ToHitData.java`
- `common/equipment/WeaponType.java`
- `common/equipment/Mounted.java`
- `common/equipment/WeaponMounted.java`
- `common/weapons/handlers/WeaponHandler.java`

MegaMek 太硬核，不适合作为《超GAG》的玩法基准，但它在“机体是复杂对象”这件事上很值得读。

可借鉴的抽象：

| MegaMek 概念 | 轻量转译到《超GAG》 |
---|---|
| `GamePhase` 分为部署、主动权、移动、射击、格斗、结束、报告 | 《超GAG》可保留玩家/敌方阶段，但增加 `Report`/`Event` 层 |
| `MovePath` 是独立对象，不是 UI 临时变量 | 移动路径应独立，可预览、验证、动画播放 |
| `Entity` 包含类型、热量、护甲部位、装备列表、移动模式 | 机体应有 `Frame`、`Tags`、`ArmorProfile`、`Mounts`，但简化 |
| `WeaponType` 有武器类型、热量、伤害、射程、旗标 | 武器数据应有射程、能量、post_move、类型、演出标签 |
| `Mounted` / `WeaponMounted` 保存装备状态 | 标志性武器可以有本关使用次数、冷却、损坏状态 |
| `ToHitData` 保存命中值和修正原因 | 战斗预测应显示“为什么是这个命中/伤害” |
| `WeaponHandler` 输出报告 | 战斗结算应输出 `CombatReport`，供 UI 和剧情事件消费 |

推荐的轻量机体模型：

```yaml
unit_frame:
  id: guardian_z
  size: L
  move: 4
  hp: 4200
  en: 100
  armor: 900
  mobility: 55
  tags: [museum_guardian, super_robot, old_frame]
  weapons:
    - id: lamp_punch
      range: [1, 1]
      power: 1500
      post_move: true
      en_cost: 5
      tags: [melee, comic_impact]
    - id: archive_beam
      range: [2, 4]
      power: 1900
      post_move: false
      en_cost: 15
      tags: [beam, museum_light]
```

不要吸收：

- BattleTech 级别的部位破坏、热量、弹药、机组规则。
- GPL 代码和 BattleTech 数据。
- 过重的桌游判定。

## 3.9 Project-Tactics：架构，而非玩法

已读重点：

- `src/Libs/Fsm/Fsm.h`
- `src/Libs/Fsm/FsmBuilder.cpp`
- `src/Libs/Ecs/EntityComponentSystem.h`
- `src/Libs/Ecs/Entity.h`
- `src/Apps/OpenTacticaPrototype/State/GameState.cpp`
- `src/Apps/OpenTacticaPrototype/Component/CharacterComponent.cpp`
- `src/Apps/OpenTacticaPrototype/System/DataSetSystem.cpp`
- `src/Apps/OpenTacticaPrototype/DataSet/CharacterDataSet.cpp`
- `resources/OpenTacticaPrototype/data/game/datasets/main_characters.json`

关键价值：

- FSM builder 让状态转移显式化。
- ECS + Prefab + DataSet 说明角色实例可以从数据生成。
- `BattleSystem::advanceTick` 用 speed 增加 charge time，达到阈值行动，适合参考但不适合机战回合制第一版。

对《超GAG》的结论：

不采用 C++/ECS 框架，但吸收两个原则：

1. **状态机必须可读**：不要把 phase 写成零散 bool。
2. **单位/角色/关卡从数据生成**：Godot 场景只做表现节点，不做唯一真相。

## 3.10 yohk：控制与 extent 机制

已读重点：

- `README.txt`
- `LICENSE.txt`
- `releasedCommands.json`
- 用 Blender 4.4.3 后台检查 `.blend`，未读到可用文本脚本块。

价值有限，但有两个想法可保留：

| 机制 | 启发 |
---|---|
| `W` 撤销/退出，`X` 结束回合，`F/G` 切换可行动单位 | 键鼠/手柄快捷操作要早设计 |
| extent：消耗更多 SP 增强技能范围/效果 | 可作为《超GAG》的“梗力加码”机制，按住或选择加码，增加范围/演出/副作用 |

许可限制较强，不可用其代码或资产。

## 3.11 SRPGWar / Project-Amber：暂不进入源码结论

用户提供的搜索摘要里提到 SRPGWar 和 Project-Amber，但本轮未找到可本地核验的公开源码仓库。处理原则：

- 不把搜索摘要当作源码事实。
- 后续如果用户提供仓库 URL，可以单独补读。
- 当前报告不基于它们做架构决策。

---

## 4. 横向比较：到底该学谁

## 4.1 阶段状态机

| 目标能力 | 最佳参考 | 结论 |
---|---|---|
| SRW-like 行动子阶段 | SRW Engine MV、SRPGcore、SRC | 必须实现强状态机 |
| 简洁 Godot 状态落地 | Godot-4 Tutorials、godot-lite | 用 Godot signals / resources 实现 |
| 复杂相位报告 | MegaMek | 只学报告对象，不学全规则 |
| 显式 FSM 架构 | Project-Tactics | 状态表要文档化 |

推荐状态表：

```text
BattlePhase
  SCENARIO_EVENT
  PLAYER_UNIT_SELECT
  PLAYER_COMMAND
  PLAYER_MOVE_PREVIEW
  PLAYER_MOVING
  PLAYER_POST_MOVE_COMMAND
  PLAYER_WEAPON_SELECT
  PLAYER_TARGET_SELECT
  PLAYER_FORECAST
  PLAYER_RESOLVE
  PLAYER_ACTION_END
  ENEMY_THINKING
  ENEMY_RESOLVE
  OBJECTIVE_CHECK
  PHASE_REPORT
```

## 4.2 行动上下文与取消

| 问题 | 正确答案 |
---|---|
| 移动后为什么不能再移动？ | 因为单位从 `READY` 进入 `MOVED_READY`，移动命令被禁用 |
| 移动后能否取消？ | 只要未攻击/待机提交，就可回滚到 `original_cell` |
| 攻击无目标怎么办？ | 不进入 `TARGET_SELECT`，提示并留在命令菜单 |
| 什么时候消耗行动？ | 攻击确认结算、待机、部分支援/特殊命令 |
| 结束回合在哪？ | 全局地图菜单，不在单位菜单 |

推荐数据结构：

```text
ActionContext
  unit_id
  original_cell
  current_cell
  path
  moved: bool
  command_id
  weapon_id
  target_id
  forecast: CombatForecast
  committed: bool
```

## 4.3 地图、范围、路径

| 能力 | 参考 | 《超GAG》设计 |
---|---|---|
| 移动范围 | Unity2D BFS、GDQuest flood fill | `GridService.get_move_cells(unit)` |
| 路径预览 | Unity2D A*、GDQuest UnitPath、MegaMek MovePath | `MovePath` 独立对象 |
| 攻击范围 | SRW Engine、SRPGcore、Legends | `TargetingData` 独立于 UI |
| 地图对象 | SRC/SRPGcore/Sulis | 单位、NPC、目标、触发点统一有 map object id |
| 小场景探索 | Sulis area / trigger | 不用战斗大地图探索，拆房间 |

## 4.4 战斗预测与结算

| 层 | 必需内容 |
---|---|
| 预测输入 | 攻击者、武器、目标、地形、距离、支援、状态 |
| 预测输出 | 命中、伤害、剩余 HP、反击可能、击破概率/意图解除 |
| 结算输出 | 命中结果、伤害、击破、目标状态、资源消耗、触发事件列表 |
| UI 表达 | 预测窗口、目标高亮、危险线、短 cut-in、结果报告 |

轻量 `CombatForecast`：

```yaml
attacker: guardian_z
target: seal_drone_01
weapon: lamp_punch
hit_rate: 88
damage: 1500
target_hp_after: 300
counter:
  possible: true
  hit_rate: 42
  damage: 400
reasons:
  - "距离 1：格斗适性正常"
  - "敌方处于封存线展开中：回避下降"
```

## 4.5 剧情事件系统

最值得合并的是 SRC + SRPGcore + Sulis：

```yaml
events:
  - id: ep01_start
    trigger: map_start
    actions:
      - dialogue: ep01_map_opening
      - show_objective: protect_message_wall

  - id: ep01_wall_threat
    trigger: enemy_enter_area
    actor: seal_drone
    area: message_wall_zone
    once: true
    actions:
      - dialogue: ep01_wall_threat_line
      - add_objective_timer: message_wall 2

  - id: ep01_first_attack
    trigger: before_attack
    attacker: guardian_z
    target_tag: seal_drone
    once: true
    actions:
      - cutin: guardian_z_first_punch
      - dialogue: ep01_guardian_first_attack

  - id: ep01_victory
    trigger: objective_complete
    objective: defeat_seal_squad
    actions:
      - dialogue: ep01_after_battle
      - set_flag: guardian_z_awake
```

这能解决“剧情没头没尾”的问题，因为战斗不是打完才回剧情，而是每个关键战术节点都在讲剧情。

## 4.6 AI 与敌方意图

不需要第一版做复杂 AI，但必须显示敌方意图。参考来源：

- Unity2D Demo：敌方阶段队列化行动。
- Cosmos War：目标优先级和工厂生产策略。
- Legends：AI 评分。
- Sulis：AI 脚本回调。

第一版敌方 AI：

```text
如果存在“保护目标”且敌方是封存单位：
  优先接近保护目标
  若目标在射程内，攻击保护目标
否则：
  若可击破我方，攻击我方
  否则靠近最近我方
```

地图上显示：

```text
敌方意图线：封存无人机 -> 留言墙
预计伤害：留言墙 -1 完整度
可打断：击破/推开/封锁路径
```

这是 Into the Breach 值得学的地方：玩家要先看到坏结果，再用回合行动阻止它。

---

## 5. 《超GAG》推荐技术组合

## 5.1 保持 Godot 主工程

理由：

- 能做真正游戏窗口、输入、动画、镜头、资源管理。
- 适合 2D / 斜 45 度 / 像素或 Q 版表现。
- 可以逐步扩展到 Steam 级项目。
- 不被 RPG Maker / Unity 项目结构锁死。

## 5.2 新建玩法内核模块

建议模块：

```text
res://core/battle/
  battle_session.gd
  battle_phase_machine.gd
  action_context.gd
  command_queue.gd
  grid_service.gd
  targeting_service.gd
  combat_forecast.gd
  combat_resolver.gd
  objective_system.gd
  ai_planner.gd

res://core/scenario/
  episode_flow.gd
  scenario_event_bus.gd
  event_condition.gd
  event_action.gd
  conversation_runner.gd
  content_db.gd

res://core/presentation/
  presentation_queue.gd
  camera_director.gd
  battle_cutin_player.gd
  map_dialogue_player.gd

res://data/
  units/
  pilots/
  weapons/
  episodes/
  maps/
  events/
  conversations/
```

## 5.3 最小可玩闭环

下一版 demo 不追求数量，先追求闭环正确：

```text
ADV 开场
  -> 探索小场景：前厅、留言墙、展柜
  -> 地图态剧情：敌人意图出现
  -> 战斗：2 我方 + 4 敌方 + 2 保护目标
  -> 战斗事件：首次攻击、保护对象受威胁、七海插话
  -> 胜利/失败分支
  -> 战后记录
```

每个战斗单位必须支持：

- 选择。
- 查看移动范围。
- 预览路径。
- 移动。
- 移动后菜单。
- 攻击无目标安全返回。
- 武器选择。
- 目标选择。
- 战斗预测。
- 结算。
- 待机。
- 行动结束。
- 全员行动后结束阶段。

## 5.4 第一章容量目标

用户反馈“几分钟打完连小品都不算”是对的。第一章 demo 若要有审阅价值，应至少达到：

| 内容 | 最低量 |
---|---:|
| ADV / 地图态剧情节点 | 30-50 个短节点 |
| 探索小场景 | 4-6 个 |
| 可调查热点 | 20-30 个 |
| 关键角色登场 | 5-8 人 |
| 我方单位 | 3-4 台/人 |
| 敌方单位 | 12-18 个，分 2-3 种 |
| 战斗关卡 | 2 个完整关卡 + 1 个短教学遭遇 |
| 战斗事件 | 每关 8-15 个 |
| 战后记录 | 至少按保护对象和探索旗标分 3 档反馈 |

容量不是简单加对白，而是让探索旗标、战斗目标、角色关系互相回写。

---

## 6. 当前 demo 应立即修正的设计清单

## 6.1 战斗规则

| 优先级 | 项目 | 标准 |
---|---|---|
| P0 | 单位行动状态 | `READY -> MOVED_READY -> DONE` 必须成立 |
| P0 | 移动后菜单 | 移动后只能攻击/待机/资料/取消移动，不能再次移动 |
| P0 | 攻击无目标 | 不进入目标选择，提示后回命令菜单 |
| P0 | 全局结束阶段 | 全员 DONE 后开放阶段结束；后续可做提前结束二次确认 |
| P0 | 预测窗口 | 攻击前必须显示命中/伤害/反击/剩余 HP |
| P1 | 敌方意图 | 每个敌人显示要攻击谁/保护目标危险 |
| P1 | 战斗事件 | 首次攻击、保护目标受威胁、击坠、胜利触发对白 |
| P1 | UI 不遮挡地图 | 菜单固定右侧或底部，地图可 pan/聚焦 |

## 6.2 探索规则

| 优先级 | 项目 | 标准 |
---|---|---|
| P0 | 小场景切分 | 前厅、留言墙、展柜、0号侧廊分场景 |
| P0 | 角色走动 | 探索不是格子战斗地图，角色在小场景移动 |
| P0 | 热点有后果 | 调查至少改变 flags、目标说明、战斗台词或支援 |
| P1 | 场景转场 | 每次切战斗前有地图态剧情说明空间变化 |
| P1 | 角色进入 | 新角色先在场景中行动，再进入台词/战斗职责 |

## 6.3 剧本规则

| 优先级 | 项目 | 标准 |
---|---|---|
| P0 | 一话结构 | Prologue / Start / Explore / MapStart / Battle / Victory / Epilogue |
| P0 | 目标来源 | 战斗目标必须来自探索或剧情中已认识对象 |
| P1 | 角色声音 | 台词由角色当下利益和处境推动，不由设定自我说明 |
| P1 | 结果回写 | 胜利后按保护对象、探索旗标、战斗表现回写关系 |

---

## 7. 建议的重构计划

### 第一步：写玩法内核规格与状态机测试

产物：

- `battle_phase_machine.gd`
- `action_context.gd`
- 单元测试或调试脚本：验证移动、取消、攻击无目标、待机、回合结束。

验收：

- 不接 UI，也能用脚本跑完一回合。
- 攻击无目标不会进入死状态。
- 单位行动一次后不能再行动。

### 第二步：做 1 个 SRW-like 战斗垂直切片

产物：

- 1 张小战斗地图。
- 2 我方、4 敌方、2 保护对象。
- 右侧信息坞 + 地图光标 + 移动范围 + 攻击范围 + 预测窗口。

验收：

- 玩家能完整完成 3 回合。
- 敌方意图可见。
- 战斗胜败条件可触发。

### 第三步：接入剧情事件

产物：

- `scenario_event_bus`
- 事件 YAML。
- 地图态剧情、攻击前对白、击坠对白、保护对象受损对白、胜利对白。

验收：

- 同一场战斗因玩家保护/失误产生不同战后记录。

### 第四步：接入探索小场景

产物：

- 前厅、留言墙、展柜、0号侧廊 4 个小场景。
- 热点 flags。
- 探索结果改变战斗目标说明/支援/台词。

验收：

- 不探索也能过，但理解更少、支援更少。
- 探索后战斗里的目标有情感来源。

### 第五步：补美术与演出

优先顺序：

1. Q 版单位 sprite。
2. 地图 tileset / 场景背景。
3. 角色半身立绘。
4. 标志性 pose 收藏图。
5. 攻击 cut-in 和短动画。

美术要服务交互：先让玩家看清局面，再让画面漂亮。

---

## 8. 源码项目对《超GAG》的“可借鉴清单”

| 借鉴项 | 推荐来源 | 是否应立即做 |
---|---|---|
| 一话事件结构 | SRC | 是 |
| 地图事件标签 | SRC / SRPGcore / Sulis | 是 |
| 强状态机 | SRW Engine MV / SRPGcore | 是 |
| 移动后菜单 | SRW Engine MV / Godot-4 Tutorial | 是 |
| 攻击无目标恢复 | SRPGcore / Cosmos War | 是 |
| 命令队列 | Unity2D Demo / Sulis | 是 |
| 战斗预测 | SRW Engine MV / SRPGcore / MegaMek | 是 |
| 敌方意图 | Into the Breach 思路 + Unity/Cosmos AI | 是 |
| 内容 YAML | Sulis | 是 |
| 机体装备挂载 | MegaMek | 后续简化做 |
| 工厂/主机目标 | Cosmos War | 第一章可用 |
| extent 技能加码 | yohk | 第二章后考虑 |
| ECS/Prefab | Project-Tactics | 只吸收数据生成原则 |
| 完整 BattleTech 规则 | MegaMek | 不做 |
| 完整 SRC 兼容脚本 | SRC | 不做 |

---

## 9. 资料来源

本地源码：

- `external_repos/SRC`
- `external_repos/SRW-Engine-MV-Plugins`
- `external_repos/CosmosWar_GDI`
- `external_repos/Unity2D-FireEmblemLike-SRPG-Demo`
- `external_repos/SRPGcore`
- `external_repos/sulis`
- `external_repos/megamek`
- `external_repos/Project-Tactics`
- `external_repos/yohk`
- `external_repos/godot-tactical-rpg`
- `external_repos/Godot-4-Tactical-RPG-Tutorials`
- `external_repos/godot-2d-tactical-rpg-movement`
- `external_repos/LegendsOfMajesticSteel`
- `external_repos/godot-tactical-rpg-lite`
- `external_repos/project-3-srw-multiplayer`

项目链接：

- [SRC](https://github.com/7474/SRC)
- [SRW Engine MV Plugins](https://github.com/tshadowknight/SRW-Engine-MV-Plugins)
- [Cosmos War / CosmosWar_GDI](https://github.com/coder-murphy/CosmosWar_GDI)
- [Unity2D FireEmblemLike SRPG Demo](https://github.com/THenry173/Unity2D-FireEmblemLike-SRPG-Demo)
- [SRPGcore](https://github.com/Ohisama-Craft/SRPGcore)
- [Sulis](https://github.com/Grokmoo/sulis)
- [MegaMek](https://github.com/MegaMek/megamek)
- [Project-Tactics](https://github.com/Project-Tactics/Project-Tactics)
- [yohk](https://github.com/Kiva-Entertainment/yohk)
- [godot-tactical-rpg](https://github.com/ramaureirac/godot-tactical-rpg)
- [Godot-4-Tactical-RPG-Tutorials](https://github.com/tyler-mooney/Godot-4-Tactical-RPG-Tutorials)
- [godot-2d-tactical-rpg-movement](https://github.com/GDQuest/godot-2d-tactical-rpg-movement)
- [Legends of Majestic Steel](https://github.com/Legends-of-Majestic-Steel/LegendsOfMajesticSteel)
- [godot-tactical-rpg-lite](https://github.com/Bozar/godot-tactical-rpg-lite)
- [project-3-srw-multiplayer](https://github.com/Gianfranco1999/project-3-srw-multiplayer)

关联本地设计文档：

- `docs/superpowers/specs/2026-06-21-src-code-design-reading-report.md`
- `docs/superpowers/specs/2026-06-21-open-source-srpg-code-reading-supplement.md`
- `docs/superpowers/specs/2026-06-21-srw-manual-rules-playflow-redesign.md`
- `docs/superpowers/specs/2026-06-21-chao-gag-srpg-interaction-design-audit.md`
- `docs/superpowers/specs/2026-06-21-hobby-project-tech-combination-adr.md`

