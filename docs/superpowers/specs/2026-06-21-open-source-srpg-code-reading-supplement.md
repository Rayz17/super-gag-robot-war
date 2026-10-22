# 开源 SRPG / 机战式项目源码研读补充报告 v0.1

> 目的：补齐此前“参考项目”调研中不够严谨的一块。此前部分项目只做到项目级筛选、README/结构/许可判断，并没有真正读到源码级逻辑；SRC 已经单独完成深读。本报告把其他几个参考项目也按“能否指导我们重做 Godot demo”的标准拆开：读了哪些源码、学到什么、不能照搬什么、下一步该怎样落地。

---

## 0. 结论先行

目前应采用的路线不是“找一个开源项目直接改名改皮”，而是：

1. **Godot 主工程继续保留**：但必须重建玩法内核，当前 demo 的问题不是美术问题，而是缺少严肃的 SRPG 行动状态机、剧情/探索/战斗的流程内核、目标系统和战斗预测系统。
2. **SRC / SRW Engine MV 作为机战式规则老师**：学习它们如何处理“单位选择 -> 移动 -> 移动后菜单 -> 攻击/待机/取消 -> 战斗预测 -> 反击/防御 -> 结算 -> 行动结束”。
3. **Godot Tactical RPG Lite 作为小型可玩架构参考**：学习 `BattleSession`、`BattleFlow`、`ActionRequest`、`CombatResult`、`Objective`、`GridService` 这类边界。
4. **GDQuest + TylerMooney 教程作为移动预览/取消/行动菜单参考**：它们的价值是短小、清楚，正好修复我们 demo 里“移动后无法优雅取消/待机/继续行动”的基本问题。
5. **Legends of Majestic Steel 作为高级技能、目标选择、AI 评分参考**：尤其是 `TargetingData`、技能效果组合、威胁范围、AI 评分。
6. **ramaureirac/godot-tactical-rpg 作为服务层/输入层/镜头层参考**：它是 3D 战棋，不能直接套，但它把控制、选择、竞技场、单位服务拆分得比较清楚。
7. **project-3-srw-multiplayer 作为“SRW-like 玩家流程”参考**：它是非正式同人原型，不适合复制，但 README 和引擎代码明确写出了移动后取消、攻击预测、防御方选择等机战式流程。

一句话：**我们要自研“超GAG行动内核”，但它不应凭空写，而应吸收这些项目里已经证明过的边界。**

---

## 1. 源码研读范围与证据

| 项目 | 本地路径 | Commit | 文件数 | 源码级研读状态 | 许可/复用边界 |
|---|---:|---:|---:|---|---|
| SRW Engine MV Plugins | `external_repos/SRW-Engine-MV-Plugins` | `af6f9fd` | 331 | 已读核心状态机、战斗计算、菜单、战斗演出、地图攻击 | README 标 MIT，但含第三方插件；只学习结构，不直接复制 |
| godot-tactical-rpg | `external_repos/godot-tactical-rpg` | `cfe785e` | 178 | 已读 3D 战棋服务层、选择流程、单位服务、竞技场服务 | MIT；可学习架构，但方向偏 3D |
| Godot-4-Tactical-RPG-Tutorials | `external_repos/Godot-4-Tactical-RPG-Tutorials` | `d962818` | 1528 | 已读第 6 章菜单系统、移动/攻击范围、取消/待机流程 | MIT；可作为 Godot 4 参考 |
| godot-2d-tactical-rpg-movement | `external_repos/godot-2d-tactical-rpg-movement` | `40023de` | 124 | 已读移动、路径预览、格子/坐标资源、移动动画 | 代码 MIT，资产 CC-BY-NC-SA；可学代码结构，不用资产 |
| LegendsOfMajesticSteel | `external_repos/LegendsOfMajesticSteel` | `7d648c3` | 562 | 已读状态机、回合队列、技能/目标/AI/地图占据 | MIT；Godot 3 风格，适合参考系统拆分 |
| godot-tactical-rpg-lite | `external_repos/godot-tactical-rpg-lite` | `473ba78` | 240 | 已读战斗会话、行动系统、GridService、AI、目标系统 | 未见根 LICENSE；只作学习参考 |
| project-3-srw-multiplayer | `external_repos/project-3-srw-multiplayer` | `c955ea8` | 907 | 已读 README 流程、JS 引擎、状态 flag、单位/机体/武器模型 | 同人/IP项目，无明确开源许可；严禁复制代码 |
| SRC / SRC# | `external_repos/SRC` | 已在独立报告登记 | 已在独立报告登记 | 已单独完成深读报告 | GPL/历史工程边界；见 `DOC_SRC_CODE_READING` |

---

## 2. SRW Engine MV Plugins：机战式状态机和战斗计算的直接参照

### 2.1 读过的关键源码

- `plugins/SRW_GameState.js`
- `plugins/SRW_BattleCalc.js`
- `plugins/SRW_GridLayer.js`
- `plugins/SRW_BattleScene.js`
- `plugins/SRW_MapAttackManager.js`
- `plugins/SRW_Menus.js`
- `plugins/SRW_Editor.js`
- `plugins/src/js/...`

### 2.2 关键发现

这个项目最有价值的不是画面，而是它把机战的“子阶段”写得非常具体。`SRW_GameState.js` 里能看到一组命名状态，例如：

- `actor_command_window`
- `actor_move`
- `post_move_command_window`
- `actor_target`
- `actor_map_target`
- `battle_window`
- `enemy_command`
- `enemy_move`
- `enemy_attack`
- `process_death_queue`
- `rewards_display`

这说明机战式战斗不是“点击单位后自由执行按钮”，而是**强状态机**。每一步都知道自己来自哪里、能去哪里、取消后回哪里。

最关键的是 `actor_move` 与 `post_move_command_window`：

- 移动前记录原位置。
- 选择有效格子后进入移动后状态。
- 移动后不直接结束行动，而是打开移动后菜单。
- 取消时回滚原坐标、清空移动范围、高亮和移动边界。
- 只有攻击、待机、特殊行动结算后，单位才进入行动结束。

这正是我们当前 demo 最大 bug 的根因：**没有 ActionContext，也没有 post-move command state**。因此单位移动之后还能乱动、攻击范围没有目标时卡死、玩家不知道下一步可以干什么。

### 2.3 战斗计算可学内容

`SRW_BattleCalc.js` 很重，但边界很清楚：

- `isTargetInRange` 用最小/最大射程和曼哈顿距离判断。
- 命中率由驾驶员、机体、武器、地形、体型、精神、状态共同计算。
- 伤害计算支持地形、体型、驾驶员/机体数值、武器威力、精神、屏障、暴击。
- 支持援护攻击、援护防御、Twin 攻击、战斗预测缓存。

我们不需要复制复杂数值，但必须保留三件事：

1. **战斗预测窗口是战斗的一部分，不是 UI 装饰。**
2. **攻击前必须可见目标、命中、伤害、反击/防御后果。**
3. **战斗结算应输出结构化结果，供剧情事件、击坠台词、奖励、目标判断消费。**

### 2.4 对超GAG的落地

应建立：

```text
BattlePhase
  player_phase
  unit_select
  command_menu
  move_preview
  moving
  post_move_command
  weapon_select
  target_select
  battle_forecast
  defense_select
  battle_resolve
  action_end
  objective_check
  enemy_phase
  scenario_event
```

以及：

```text
ActionContext
  actor_id
  original_cell
  current_cell
  moved_path
  selected_command
  selected_weapon
  selected_target
  forecast
  can_cancel_move
  has_committed
```

当前 demo 必须补这个，否则 UI 再漂亮也不会像游戏。

---

## 3. Godot-4-Tactical-RPG-Tutorials：移动后菜单、取消和范围层

### 3.1 读过的关键源码

- `6 - Menu System/GameBoard/GameBoard.gd`
- `6 - Menu System/GameBoard/Pathfinder.gd`
- `6 - Menu System/Units/Unit.gd`
- `6 - Menu System/Menus/ActionMenu.gd`
- `6 - Menu System/UnitOverlay/UnitOverlay.gd`

### 3.2 关键发现

这个教程项目虽然不是完整游戏，但它把我们现在最缺的“手感基础”写出来了：

- `_active_unit`
- `_walkable_cells`
- `_attackable_cells`
- `_prev_cell`
- `_prev_position`
- `ActionMenu`
- `Wait`
- `Cancel`

流程大致是：

1. 选择单位。
2. 显示移动范围。
3. 移动到目标格。
4. 打开行动菜单。
5. 选择 `Wait` 则单位行动结束。
6. 选择 `Cancel` 则调用 `_reset_unit()` 回到原位置。

这与机战非常接近。它还用 `UnitOverlay` 把移动格和攻击格分层显示，避免我们现在 demo 中“地图、菜单、高亮、角色互相打架”的问题。

### 3.3 对超GAG的落地

短期最应该吸收：

- 移动前保存原格子和原世界坐标。
- 移动后必须进入菜单，而不是留在自由移动状态。
- `Cancel` 只取消尚未提交的移动。
- `Wait`/`待机` 才让单位灰掉并结束行动。
- `UnitOverlay` 作为地图表现层，UI 菜单不要挡住地图关键格。

---

## 4. GDQuest 2D Tactical RPG Movement：干净的格子移动和路径预览

### 4.1 读过的关键源码

- `godot4/GameBoard/GameBoard.gd`
- `godot4/GameBoard/UnitPath.gd`
- `godot4/GameBoard/Grid.gd`
- `godot4/Units/Unit.gd`

### 4.2 关键发现

GDQuest 的项目很小，但它是一个干净的移动范式：

- `Grid` 作为格子/世界坐标转换资源。
- `GameBoard` 维护单位占据格和可行走格。
- flood fill 计算可走范围。
- `UnitPath` 根据鼠标/光标预览路径。
- `Unit.walk_along(path)` 用 `Path2D`/`PathFollow2D` 做平滑移动。

这对我们的探索/战斗都重要。用户已经指出：“探索阶段人物应该是在小场景里走动，而不是整张大地图拖格子”。GDQuest 的这套适合小场景移动，也适合战斗地图上的路径预览。

### 4.3 对超GAG的落地

我们可以把移动拆成两种：

| 场景 | 移动表现 | 技术模型 |
|---|---|---|
| 探索小场景 | 角色在房间/展区里连续走动，靠近热点触发调查/对话 | 小地图导航点 + 碰撞区 + 热点 |
| 战斗场景 | 单位按格移动，有移动范围、路径预览、行动后菜单 | GridService + ActionContext + UnitOverlay |

这可以解决现在 demo 的“探索像网页，战斗像按钮”的断裂。

---

## 5. godot-tactical-rpg-lite：最接近可玩战斗骨架的小型架构

### 5.1 读过的关键源码

- `battle/battle_session.gd`
- `combat/action_request.gd`
- `combat/combat_resolver.gd`
- `combat/combat_result.gd`
- `scenes/autoloads/battle_flow.gd`
- `scenes/autoloads/player_action_manager.gd`
- `scenes/autoloads/enemy_action_manager.gd`
- `scenes/state_machine/player_turn_state.gd`
- `scenes/state_machine/enemy_turn_state.gd`
- `scenes/actions/BaseAction.gd`
- `scenes/actions/move_action.gd`
- `scenes/actions/attack_action.gd`
- `grids/grid_service.gd`
- `objectives/defeat_all_enemies_objective.gd`
- `scenes/units/unit.gd`
- `ai/ai_decision.gd`

### 5.2 关键发现

它的核心边界适合我们：

```text
BattleSession
  player_units
  enemy_units
  objectives
  battle_active
  victory/defeat evaluation

BattleFlow
  NONE
  PLAYER_TURN
  ENEMY_TURN
  FINISHED

BaseAction
  action_id
  action_name
  action_point_cost
  show_action_grid()
  execute()
  finish_action()

ActionRequest -> CombatResolver -> CombatResult
```

它的价值在于：**战斗不是 UI 事件堆，而是 Session + Flow + Action + Resolver + Objective 的组合。**

当前 demo 最大的问题之一，就是缺少这层结构。结果就是：

- 流程不知道现在是剧情、探索、战斗还是菜单。
- 行动不知道是否已经提交。
- 战斗目标不知道什么时候判定。
- 角色出现和剧情切换没有被任务目标绑定。

### 5.3 对超GAG的落地

我们应建立自己的：

```text
GagBattleSession
GagBattleFlow
GagAction
GagActionRequest
GagCombatResolver
GagCombatResult
GagObjective
```

并给第一章 demo 至少实现这些目标类型：

- `ReachAreaObjective`：到达某展厅/防火门/核心控制台。
- `ProtectUnitObjective`：保护纪存、七海或馆守Z。
- `SurviveTurnsObjective`：撑过若干回合直到展馆应急系统上线。
- `DefeatAllObjective`：击退清算部无人机/异常机魂。
- `InvestigateHotspotObjective`：探索阶段调查指定热点。
- `ScriptedEventObjective`：触发剧情事件后切到下一个场景。

---

## 6. Legends of Majestic Steel：技能、目标选择和 AI 的高级参考

### 6.1 读过的关键源码

- `src/game/Game.gd`
- `src/state/StateMachine.gd`
- `src/state/State.gd`
- `src/state/states/NextTurnState.gd`
- `src/state/states/ActorStartTurnState.gd`
- `src/state/states/PlayerPickActorActionState.gd`
- `src/control/Pathfinding.gd`
- `src/control/WalkRange.gd`
- `src/control/WalkRangeFactory.gd`
- `src/control/AIActorTurn.gd`
- `src/control/AIScoredAction.gd`
- `src/core/maps/Map.gd`
- `src/core/maps/TurnQueue.gd`
- `src/core/skills/Skill.gd`
- `src/core/skills/TargetingData.gd`
- `src/core/skills/SkillEffectGroup.gd`
- `src/core/actors/Actor.gd`

### 6.2 关键发现

它不是机器人游戏，也不是机战流程，但系统层很成熟：

- `StateMachine` 管理战斗流程。
- `TurnQueue` 采用速度/先攻队列，而不是我方阶段/敌方阶段。
- `WalkRangeFactory` 支持真实可走范围、可见范围、多格单位。
- `TargetingData` 保存可选目标、预计伤害、预计状态变化、AOE。
- `SkillEffectGroup` 支持技能效果的组合与序列。
- `AIScoredAction` 会给技能、移动、击杀、防御地形、距离做评分。

### 6.3 对超GAG的落地

这里最值得吸收的是 `TargetingData` 概念。我们的武器不该只是：

```text
range + damage
```

而应该是：

```text
GagTargetingData
  valid_targets
  affected_cells
  predicted_damage
  predicted_hit
  predicted_counter
  predicted_status
  predicted_story_triggers
  danger_after_action
```

这样才可以做：

- 机战式战斗预测。
- Into the Breach 式“敌人意图可见”。
- 剧情战中的“打这台机会触发某人台词/逃跑/觉醒”。
- 地图兵器、推拉、保护、牺牲、援护、防御等玩法。

此外，它对多格单位的处理也很重要。超GAG里会有：

- 人形角色
- 小型机器人
- Q版机体
- 正比例巨大机体
- 展馆装置/建筑物
- 地外超体或大型敌人

因此战斗内核应预留 `footprint`，不要假设所有单位都是 1x1。

---

## 7. ramaureirac/godot-tactical-rpg：服务层、选择层、3D镜头层参考

### 7.1 读过的关键源码

- `data/modules/tactics/level/tactics_level.gd`
- `data/modules/tactics/level/pawn/pawn.gd`
- `data/models/view/control/tactics/service/t_ctrl_serv.gd`
- `data/models/view/control/tactics/service/selection.gd`
- `data/modules/tactics/level/arena/tactics_arena.gd`
- `data/models/world/combat/arena/service/service.gd`
- `data/models/world/combat/arena/tile_service/service.gd`
- `data/models/world/combat/participant/pawn/service/pawn_serv.gd`
- `data/models/world/combat/participant/pawn/service/movement.gd`
- `data/models/world/combat/participant/pawn/service/combat.gd`

### 7.2 关键发现

这个项目是 Godot 4.3 的 3D 战棋模板。它最有价值的不是战斗规则，而是组织方式：

- `Models`：集中放资源和纯逻辑。
- `Modules`：放可复用节点。
- `Services`：用 `RefCounted` 承担具体逻辑。
- `TacticsControlsService` 组合输入、UI、镜头、选择。
- `TacticsControlsSelectionService` 处理选单位、选移动格、选攻击目标、取消、等待。
- `TacticsArenaService` 管理 tile、邻接、可达、可攻击、目标选择。
- `TacticsPawnMovementService` 处理移动动画、路径、速度。

### 7.3 对超GAG的落地

它提示我们，Godot 项目不要把逻辑都塞进场景节点。建议拆成：

```text
res://gag/core/
  battle_session.gd
  battle_flow.gd
  action_context.gd
  combat_resolver.gd
  scenario_kernel.gd

res://gag/grid/
  grid_service.gd
  pathfinder.gd
  overlay_service.gd

res://gag/units/
  unit_actor.gd
  unit_data.gd
  pilot_data.gd
  weapon_data.gd

res://gag/presentation/
  battle_camera.gd
  dialog_presenter.gd
  cutin_presenter.gd
  sfx_bus.gd

res://gag/ui/
  command_menu.gd
  weapon_menu.gd
  battle_forecast_panel.gd
  objective_panel.gd
```

---

## 8. project-3-srw-multiplayer：同人 SRW-like 流程和 Get/Do 请求边界

### 8.1 读过的关键源码

- `README.md`
- `game/gameEngine.js`
- `game/statesAndFlags.js`
- `game/map.js`
- `game/unit.js`
- `game/tile.js`
- `models/unit.js`
- `models/mech.js`
- `models/pilot.js`
- `models/weapon.js`

### 8.2 关键发现

它的 README 明确描述了非常机战的玩家行动流程：

```text
点击当前单位
  -> Move / Attack / Spirit
Move
  -> 显示可移动格
  -> 移动后出现 Attack / Standby / Cancel
Cancel
  -> 回到起点
Attack
  -> 选择武器
  -> 显示射程
  -> 选择目标
  -> 显示命中率/伤害
防御方选择 Attack / Evade / Defend
战斗结算
下一个单位/玩家
```

`gameEngine.js` 里还有一个很值得借鉴的边界：请求分为 `Get` 和 `Do`。

- `Get`：只拿数据，不改变状态。例如获取可移动格、可攻击目标、行动菜单。
- `Do`：真正改变状态。例如执行移动、执行攻击、结束行动。

这对我们非常重要。当前 demo 很容易因为“打开菜单/点格子/切 UI”就改变了状态，所以玩家一旦点错就卡死。应改成：

```text
GetMoveRange(unit_id) -> cells
PreviewMove(unit_id, cell) -> path, warnings
DoMove(unit_id, cell) -> action_context updated
GetPostMoveCommands(action_context) -> commands
DoCancelMove(action_context) -> rollback
DoStandby(action_context) -> commit/end action
GetWeaponTargets(action_context, weapon_id) -> targets
GetBattleForecast(action_context, weapon_id, target_id) -> forecast
DoBattle(action_context) -> combat_result
```

### 8.3 法务与质量边界

这个项目是同人 SRW 多人游戏，包含明显 IP 指向且未见明确开源许可证。只能作为“流程观察”和“数据词汇参考”，不能复制代码或资产。

---

## 9. 横向对比：这些项目共同暴露出的 demo 问题

| 当前 demo 问题 | 源码项目给出的答案 | 我们应补的模块 |
|---|---|---|
| 移动后还能继续乱动 | SRW Engine MV / TylerMooney 都有 post-move state | `ActionContext` + `post_move_command` |
| 攻击范围无目标会卡死 | SRW Engine MV 有 target state cancel；project-3 有 Get/Do | `target_select` 可取消，`GetWeaponTargets` 不改状态 |
| 不知道怎么结束回合 | SRW-like 流程有 Wait/Standby/End Phase | `UnitActionState` + `EndPhaseCommand` |
| 菜单挡地图 | TylerMooney 用 overlay 分层，SRW菜单不遮关键选择 | `UnitOverlay` + 边缘式 HUD |
| 剧情/探索/战斗割裂 | SRC 有事件内核，Tactical Lite 有 BattleSession | `ScenarioKernel` + `BattleSession` |
| 人物突然出现 | 剧情事件没有绑定场景目标 | `ScenarioBeat` 绑定 `Objective` |
| 战斗没有机战味 | 缺少武器选择、预测、反击/防御、援护 | `WeaponMenu` + `BattleForecast` + `DefenseResponse` |
| 敌人没有意图 | Into the Breach 方向应结合 Legends TargetingData | `EnemyIntent` + `TargetingData` |
| 没有容量感 | 章节流程不是任务链，只是界面切换 | `EpisodeFlow` -> `Scene` -> `Objective` -> `BattleEvent` |

---

## 10. 建议的超GAG核心架构

### 10.1 顶层流程

```text
EpisodeRunner
  -> ScenarioKernel
      -> DialogScene
      -> ExplorationScene
      -> BattleScene
      -> ManagementScene
      -> IntermissionScene
```

### 10.2 剧情/探索/战斗统一事件

```text
ScenarioEvent
  id
  trigger
  conditions
  actions
  presentation
  next
```

触发条件示例：

```text
on_dialog_line_finished
on_hotspot_investigated
on_unit_reaches_cell
on_unit_hp_below
on_enemy_defeated
on_turn_start
on_turn_end
on_battle_result
on_objective_completed
```

这样第一章不会再像网页翻页，而是：

```text
剧情说到火灾前夜
  -> 玩家进入万机馆探索
  -> 调查展岛/消防门/失效导览机
  -> 七海/纪存/馆守Z通过目标触发登场
  -> 异常无人机出现
  -> 进入保护战
  -> 击退或撑回合
  -> 馆守Z启动
  -> 战斗结果触发不同对白
  -> 进入下一话
```

### 10.3 战斗状态机

```text
BattleSession
  battle_id
  map_id
  phase
  turn_count
  active_unit_id
  units
  objectives
  scenario_events

BattleStateMachine
  scenario_event
  player_phase_start
  unit_select
  command_menu
  move_preview
  moving
  post_move_command
  weapon_select
  target_select
  battle_forecast
  defense_select
  battle_animation
  battle_result
  action_end
  objective_check
  enemy_phase_start
  enemy_intent_preview
  enemy_action
```

### 10.4 行动上下文

```text
ActionContext
  unit_id
  start_cell
  current_cell
  selected_action
  selected_weapon
  selected_target
  move_path
  committed_move
  committed_attack
  preview_data
  rollback_snapshot
```

状态规则：

- 只要 `committed_attack == false`，移动可以取消。
- 只要进入 `battle_animation`，行动不能取消。
- `Wait/Standby` 会提交移动并结束单位行动。
- `Attack` 会在战斗结算后结束行动，除非有特殊技能允许二动或 Hit & Away。
- `Get` 型请求不改变 `ActionContext`。
- `Do` 型请求必须进入日志，方便回放、调试和剧情触发。

### 10.5 战斗预测

```text
BattleForecast
  attacker
  defender
  weapon
  hit_rate
  crit_rate
  expected_damage
  counter_possible
  counter_weapon
  terrain_effect
  support_attack
  support_defense
  story_flags
```

第一章 demo 可先简化数值，但 UI 必须有预测。没有预测，就不像 SRPG，更不像机战。

---

## 11. 具体项目吸收优先级

### 第一优先：立刻改 demo

1. SRW Engine MV 的命名战斗子阶段。
2. Godot-4-Tactical-RPG-Tutorials 的移动后菜单和取消回滚。
3. godot-tactical-rpg-lite 的 `BattleSession` / `BattleFlow` / `ActionRequest` / `CombatResult`。
4. GDQuest 的路径预览和平滑移动。

### 第二优先：让 demo 变得像完整游戏

1. SRC 的轻量剧本事件内核。
2. Tactical Lite 的 Objective 结构。
3. project-3 的 Get/Do 请求边界。
4. Legends 的 TargetingData 和敌人意图。

### 第三优先：长期品质

1. Legends 的技能效果组合。
2. ramaureirac 的服务层拆分和镜头/输入组织。
3. SRW Engine MV 的援护、防御方选择、地图兵器、奖励结算。

---

## 12. 对当前技术路线的修正

此前“Godot 主线 + 参考开源项目”的方向仍然成立，但必须更明确：

```text
不是：
  Godot 里做几个场景 + UI按钮 + 对话框

而是：
  Godot 里实现一个 SRW-like 战术角色扮演内核
  再把剧情、探索、战斗、管理作为这个内核的不同表层
```

技术组合应更新为：

```text
Godot 4 主工程
  + 自研 GagScenarioKernel
  + 自研 GagBattleSession
  + 自研 GagActionContext
  + 自研 GagGridService
  + 自研 GagCombatResolver
  + 自研 GagPresentationBus

参考但不复制：
  SRC / SRW Engine MV：机战流程、事件、状态机
  Tactical RPG Lite：Godot 小型战斗架构
  GDQuest/Tyler：移动预览、取消、菜单
  Legends：技能、目标、AI
  project-3：SRW-like 请求边界
```

---

## 13. 下一步实施清单

### 13.1 先写玩法企划补丁

新增或重写：

- 第一章 demo 玩法流程企划。
- 战斗操作规范。
- 探索小场景规范。
- 剧情事件触发规范。
- 管理界面入口与退出规范。

### 13.2 再改 Godot demo 内核

最小可接受版本应做到：

1. 第一话从开场剧情进入万机馆探索。
2. 玩家可控制角色在小场景中走动，调查热点。
3. 调查触发角色登场、旁白、疑问、目标变化。
4. 火灾/异常事件自然触发。
5. 进入第一场教学战。
6. 战斗可选单位、移动、取消、待机、攻击、选择目标、查看预测。
7. 攻击无目标时能返回武器/行动菜单。
8. 所有我方单位行动结束后可结束回合。
9. 敌方行动前显示意图。
10. 达成目标后回到剧情，进入下一场景。

### 13.3 再补表现层

表现顺序应是：

1. 地图信息清楚。
2. 角色/单位状态清楚。
3. 当前目标清楚。
4. 可行动作清楚。
5. 选择后果清楚。
6. 演出爽点再加。

不能再用“先画 UI，再补流程”的方式。

---

## 14. 必须避免的误区

1. **不要把 Godot 当网页播放器。** 场景、输入、状态、资源、信号要成为游戏结构。
2. **不要用 UI 按钮假装战棋。** 战棋的核心是格子、路径、范围、承诺、取消、预测、结算。
3. **不要用剧情文本替代场景目标。** 玩家要知道自己为什么调查、为什么战斗、为什么转场。
4. **不要把美术当遮羞布。** 当前问题不是“还不够好看”，而是“游戏内核还没站起来”。
5. **不要直接复制参考项目。** 许可、IP、引擎版本、工程质量都不允许我们这样做。

---

## 15. 当前对 demo 的技术诊断

现在的 demo 更像“带游戏皮的页面流”，根因是：

- 缺 `ScenarioKernel`：剧情节点不是事件系统，只是切界面。
- 缺 `BattleSession`：战斗没有会话生命周期。
- 缺 `BattleStateMachine`：行动阶段没有封闭规则。
- 缺 `ActionContext`：移动、攻击、取消没有同一份上下文。
- 缺 `Objective`：玩家不知道当前目标和战斗胜负条件。
- 缺 `Get/Do` 边界：预览和提交混在一起，容易卡死。
- 缺 `TargetingData`：攻击范围、目标、预测、敌人意图都不成体系。
- 缺 `PresentationBus`：对话、旁白、转场、战斗台词无法跟游戏事件自然连接。

所以，下一版不应只是补贴图和按钮，而应先重做内核。

---

## 16. 推荐的代码重构目标名

建议 Godot 项目下一轮直接建立这些文件或等价模块：

```text
game-godot/chao-gag-robot-wars/core/scenario/scenario_kernel.gd
game-godot/chao-gag-robot-wars/core/scenario/scenario_event.gd
game-godot/chao-gag-robot-wars/core/battle/battle_session.gd
game-godot/chao-gag-robot-wars/core/battle/battle_state_machine.gd
game-godot/chao-gag-robot-wars/core/battle/action_context.gd
game-godot/chao-gag-robot-wars/core/battle/battle_objective.gd
game-godot/chao-gag-robot-wars/core/combat/action_request.gd
game-godot/chao-gag-robot-wars/core/combat/combat_resolver.gd
game-godot/chao-gag-robot-wars/core/combat/combat_result.gd
game-godot/chao-gag-robot-wars/core/grid/grid_service.gd
game-godot/chao-gag-robot-wars/core/grid/pathfinder.gd
game-godot/chao-gag-robot-wars/core/grid/targeting_data.gd
game-godot/chao-gag-robot-wars/ui/battle/command_menu.gd
game-godot/chao-gag-robot-wars/ui/battle/weapon_menu.gd
game-godot/chao-gag-robot-wars/ui/battle/battle_forecast_panel.gd
game-godot/chao-gag-robot-wars/ui/common/objective_panel.gd
```

这不是为了“工程洁癖”，而是为了让剧情、探索、战斗、管理能在同一套规则上跑起来。

---

## 17. 最终判断

你追问“其他几个参考项目的源码是不是也没读”，这个问题是成立的。此前确实不应把项目级调研说成源码级研读。

现在补读后的判断是：**Godot 仍然是正确主线，但必须用 SRC/SRW Engine MV 的机战流程意识，加上 Godot 战棋项目的状态/行动/目标架构来重做。**

下一版 demo 的目标不应是“多几个界面”，而应是：

```text
玩家能完整走完第一章的一段剧情
  -> 明确目标
  -> 探索小场景
  -> 触发剧情
  -> 进入战斗
  -> 按机战式流程行动
  -> 看懂预测和敌人意图
  -> 达成目标
  -> 回到剧情
  -> 带着问题进入下一话
```

做到这一点，才开始谈美术补强和付费级质感。
