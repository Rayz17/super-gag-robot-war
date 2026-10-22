# 《超GAG机器人大战》开源SRPG/机战式项目调研 v0.1

> 调研时间：2026-06-21  
> 方法：GitHub 搜索、GitHub API 元信息、README/仓库树/关键脚本抽样。  
> 目标：判断是否存在可直接改造的机战式开源项目，以及哪些模块值得吸收进当前 Godot demo。

## 1. 结论先行

不建议现在直接抛弃当前 Godot 工程去“套一个开源项目”。

原因：

- 真正像机战的开源项目主要在 RPG Maker MV 生态，不适合当前 Godot 方向。
- Godot 的开源战棋项目更像 Fire Emblem / Advance Wars / 通用 tactics demo，能补地图、寻路、行动菜单、范围显示，但不自带 SRW 的 ADV/地图剧情/战斗演出语法。
- 有些项目没有明确 license，或者带明显 IP 同人素材，只能学习，不能作为商业底座。

推荐路线：

```text
当前Godot工程继续保留
  -> 吸收 Godot 战棋项目的地图/寻路/行动菜单架构
  -> 吸收 SRW Engine MV 的机战菜单状态机和数据驱动编辑器思想
  -> 重写为我们自己的可商用代码和资产
```

## 2. 机战式项目

### 2.1 SRW Engine MV Plugins

- 仓库：`https://github.com/tshadowknight/SRW-Engine-MV-Plugins`
- 技术栈：RPG Maker MV / JavaScript
- GitHub 元信息：8 stars，主语言 JavaScript，2026-06-19 更新。
- License 状态：GitHub API 未识别 license；README 写明项目自身插件为 MIT，但同时包含第三方插件，需逐项审计。

价值：

- 最像机战的开源资料源。
- 关键脚本中存在 `SRW_GameState.js`、`SRW_GridLayer.js`、`SRW_BattleCalc.js`、`SRW_BattleScene.js`、`SRW_MapAttackManager.js`。
- `SRW_GameState.js` 内部状态名非常有参考价值，例如：
  - `actor_command_window`
  - `post_move_command_window`
  - `battle_window`
  - `actor_move`
  - `spirit_activation`

局限：

- RPG Maker MV 依赖太重，不能作为 Godot 项目的直接底座。
- 代码规模和 MV 插件生态耦合较深，直接迁移成本高。
- 第三方插件 license 和素材边界需要审计。

建议用途：

- 作为“SRW状态机/菜单层级/编辑器数据结构”的参考。
- 不直接引入代码。

### 2.2 SRW Engine MV Docs

- 仓库：`https://github.com/tshadowknight/SRW_Engine_MV_Docs`
- 技术栈：Markdown 文档与图片资料。
- GitHub 元信息：3 stars，2026-05-03 更新。

价值：

- 包含 battle animation、battle scene、battle text、weapon effects、spirit、pilot/mech abilities 等文档。
- 有 `Map Menu`、`Before Battle`、`Unit Location on map` 等截图资源，适合研究 SRW 式编辑器和菜单表达。

局限：

- 没有可直接运行的 Godot 代码。
- 文档支持 Discord 社区，信息可能分散。

建议用途：

- 用来反推我们自己的数据表：武器、精神、战斗台词、地图事件、演出命令。

### 2.3 SRW Engine MV Public

- 仓库：`https://github.com/tearitco/SRW-Engine-MV-Public`
- 技术栈：RPG Maker MV 项目。
- GitHub 元信息：MIT，约 504MB。

价值：

- 可能是可运行 public 包，包含 UI、data、docs、js、img、audio 等完整 MV 工程结构。
- 适合本地另开隔离目录研究“实际项目如何组织配置和素材”。

局限：

- 体积大，带音频/图片/示例素材，商业项目不能直接吸收。
- MV 工程和 Godot 结构不同。

建议用途：

- 只做离线参考，不进入当前仓库。

### 2.4 Super Robot Wars Multiplayer Fan Game

- 仓库：`https://github.com/MagentaReds/project-3-srw-multiplayer`
- 技术栈：Node.js / Express / Socket.io / jQuery / EJS。
- GitHub 元信息：15 stars，无明确 license。

价值：

- README 明确是基于 GBA《Super Robot Wars OG2》的多人同人项目。
- 有 `game/map.js`、`game/unit.js`、`statesAndFlags.js`、`public/assets/js/grid.js`。
- 可参考多人同步、服务端状态和单位数据。

局限：

- 无 license，不能直接复用。
- Web 技术栈和当前 Godot 不合。
- 明确同人 IP 项目，商业边界不适合。

建议用途：

- 只看“回合状态同步”和“地图/单位数据结构”，不直接采用。

## 3. Godot战棋项目

### 3.1 ramaureirac/godot-tactical-rpg

- 仓库：`https://github.com/ramaureirac/godot-tactical-rpg`
- 技术栈：Godot / GDScript。
- GitHub 元信息：MIT，921 stars，108 forks，2026-06-18 更新。

价值：

- 目前最值得认真研究的 Godot 战棋工程。
- 目录结构有清晰的 tactics camera、cursor、selection、movement、map level、data model。
- 支持多个 Godot 版本分支，README 指向 wiki。
- 可作为“Godot 工程组织方式”和“地图/单位/镜头/选择服务拆分”的参考。

局限：

- 更偏通用 tactical RPG，不是 SRW。
- 工程较大，直接迁移会吞掉我们当前叙事/演出方向。

建议用途：

- 建议开一个技术 spike：只吸收它的架构思想，尤其是 camera/control/service 分层。
- 不建议直接把当前 demo 替换成它。

### 3.2 GDQuest Tactical RPG Movement

- 仓库：`https://github.com/gdquest-demos/godot-2d-tactical-rpg-movement`
- 技术栈：Godot / GDScript。
- GitHub 元信息：176 stars，38 forks，license 识别为 NOASSERTION。

价值：

- 小而清楚，专注网格移动。
- README 明确特性：网格移动、地图光标、显示可移动区域、路径预览、确认/取消移动。
- 关键脚本：`GameBoard.gd`、`Pathfinder.gd`、`UnitPath.gd`、`Cursor.gd`。

局限：

- license 需进一步确认；若无明确 license，只能学习不能拷代码。
- 原版偏 Godot 3，用于 Godot 4 需改。

建议用途：

- 极适合学习“移动预览/取消移动”这一块。
- 我们当前 demo 最缺的正是“移动是一个可预览、可取消、可承诺的动作链”，而不是瞬移。

### 3.3 TylerMooney/Godot-4-Tactical-RPG-Tutorials

- 仓库：`https://github.com/TylerMooney/Godot-4-Tactical-RPG-Tutorials`
- 技术栈：Godot 4 / GDScript。
- GitHub 元信息：MIT，25 stars，2026-06-18 更新。

价值：

- 基于 GDQuest demo 扩展到 Godot 4。
- README 标明已加入：扩展移动、队伍碰撞、攻击范围、镜头控制、hover范围显示、单位行动菜单雏形、主菜单雏形。
- License 是 MIT，比 GDQuest 原仓库更适合参考实现。

局限：

- Combat phases、combat、inventory 等仍在 planned/partial 阶段。
- 更像教程分步项目，不是完整游戏底座。

建议用途：

- 当前最适合作为“移动/攻击范围/单位菜单”的短期技术参考。
- 可以开一个 isolated spike，对照实现我们自己的 Godot 4 action chain。

### 3.4 Legends of Majestic Steel

- 仓库：`https://github.com/AaronWizard/LegendsOfMajesticSteel`
- 技术栈：Godot / GDScript。
- GitHub 元信息：MIT，39 stars，2026-05-17 更新。

价值：

- 是一个真正的 Strategy RPG 项目，不只是教程。
- README 中提到基于 speed stat 的角色逐个行动、移动范围高亮、点击角色执行动作。
- 可参考技能、UI图标、回合节奏、状态/能力系统。

局限：

- 行动顺序不是 SRW 的我方阶段/敌方阶段。
- 风格是 fantasy/metal，不适合直接视觉继承。

建议用途：

- 学习“完整游戏项目如何组织能力/行动/UI反馈”。
- 不作为 SRW-like 主底座。

### 3.5 Godot Tactical RPG Lite

- 仓库：`https://github.com/godotlabsio/godot-tactical-rpg-lite`
- 技术栈：Godot / GDScript。
- GitHub 元信息：7 stars，无明确 license。

价值：

- README 明确强调 clean battle loop。
- 文件结构很理想：`battle_session.gd`、`combat_resolver.gd`、`action_request.gd`、`grid_service.gd`、`objectives`。
- 很适合学习“战斗会话/行动请求/战斗结算/目标判定”的模块划分。

局限：

- 无明确 license，不能直接用代码。
- 似乎是 full version 的 public lite edition，商业复用需非常谨慎。

建议用途：

- 学架构命名和边界，不直接拷。

### 3.6 Code Geass SRPG

- 仓库：`https://github.com/henrylewis2004/Code-Geass-SRPG`
- 技术栈：Godot / GDScript。
- GitHub 元信息：GPL-3.0，约 918MB。

价值：

- 机器人/动画 IP 同人 SRPG，视觉方向可能有参考。

局限：

- GPL-3.0 不适合直接并入闭源/商业项目。
- 明确使用 Code Geass IP，同人素材不能用。
- 体积巨大。

建议用途：

- 只看公开截图和操作说明，不碰代码/素材。

## 4. 对当前项目的技术判断

### 4.1 不能直接“找个机战开源项目改”

SRW Engine MV 是最像的，但它属于 RPG Maker MV 体系。直接换底座会导致：

- Godot 视觉验证流程全部作废。
- 当前已做的剧本/探索/地图态剧情/战斗演出要重写。
- 商业化 license 和素材边界更难控制。

所以它适合做“机战语法教科书”，不是工程底座。

### 4.2 当前Godot demo应该吸收的四个模块

第一优先级：

- GDQuest/TylerMooney 的移动预览、路径显示、取消移动。
- TylerMooney 的攻击范围和单位行动菜单。
- SRW Engine MV 的 `post_move_command_window` 思想。
- Godot Tactical RPG Lite 的 `BattleSession / ActionRequest / CombatResolver / Objective` 边界。

第二优先级：

- ramaureirac 的 camera/control/service 工程分层。
- SRW Engine MV Docs 的战斗台词、武器效果、演出命令数据结构。

暂不做：

- 多人联网。
- RPG Maker MV 迁移。
- GPL/IP同人项目代码复用。

## 5. 推荐下一步 Spike

建立一个隔离实验目录：

```text
experiments/oss_spikes/srpg_action_chain/
```

目标不是复制项目，而是用我们自己的代码实现三件事：

```text
1. 可取消移动预览
   选单位 -> 显示移动范围 -> 光标移动显示路径 -> 确认后进入移动后命令

2. 移动后命令窗口
   已移动单位不能再次移动，只能攻击/待机/取消到移动前位置

3. 战斗请求对象
   ActionRequest -> Forecast -> Resolve -> BattleResult
```

成功标准：

- 不使用外部素材。
- 不复制无明确 license 的代码。
- Godot 4.7 能跑。
- 可以替换当前 `srw_slice_model.gd` 的行动链，而不破坏剧情/地图态对话。

## 6. 推荐最终工程路线

```text
当前 Godot demo
  -> 保留剧情/地图态演出方向
  -> 重写 action chain 为可预览/可取消/可承诺
  -> 抽出 BattleSession / ActionRequest / Objective
  -> 再接探索小场景
  -> 再接第一章完整流程
```

这条路比“直接改一个开源游戏”慢一点，但商业边界、安全性和定制叙事能力都更好。
