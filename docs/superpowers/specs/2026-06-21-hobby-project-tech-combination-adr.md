# ADR: 兴趣作品路线下的技术组合决策

日期：2026-06-21

## 状态

采纳。

## 背景

《超GAG机器人大战》当前定位调整为“兴趣作品，但追求高完成度”。这降低了立即商业发行的版权与授权压力，但没有降低品质要求。相反，兴趣作品更容易因为范围、素材、系统复杂度和工具链选择而失控。

因此，技术组合不能只问“能不能商用”，还要问：

- 能不能把手感做到接近 SRW / Into the Breach / Wargroove 的清晰度。
- 能不能在 Codex 工作流里长期迭代。
- 能不能承载 ADV、探索小场景、地图态剧情、战术战斗、战后记录。
- 能不能在未来如果想转正或发布时，替换风险素材与外部依赖。

## 决策

采用：

```text
Godot 4 主工程
  + SRW Engine MV 参考实验室
  + MIT Godot 战棋项目的结构借鉴
  + 自研行动链与战斗内核
```

不采用：

```text
直接切到 RPG Maker MV / SRW Engine MV 作为最终底座
直接拷贝无明确 license 或 IP 同人项目代码与资产
```

## 组合方式

### 1. 主工程：Godot 4

Godot 保留为主工程。

理由：

- 能支持原生窗口、2D 斜45度地图、探索小场景、战术地图、cut-in 与后续更复杂的演出。
- GDScript 与 headless test 适合 Codex 自动化开发。
- 当前项目已有 Godot demo、测试脚本和截图流程，不应轻易推倒。

### 2. 机战语法参考：SRW Engine MV

SRW Engine MV 作为 reference lab，不作为主工程。

学习内容：

- `actor_command_window`
- `post_move_command_window`
- `battle_window`
- `actor_move`
- 精神、武器、战斗台词、地图攻击、战斗演出配置。

使用边界：

- 可研究状态机和数据表设计。
- 不直接复制代码或素材。
- 不迁移到 RPG Maker MV。

### 3. Godot战棋参考：MIT项目优先

优先参考：

- `ramaureirac/godot-tactical-rpg`
- `TylerMooney/Godot-4-Tactical-RPG-Tutorials`

学习内容：

- 地图光标。
- 可移动范围。
- 路径预览。
- 攻击范围。
- 单位行动菜单。
- camera / selection / movement service 分层。

### 4. 自研核心：Action Chain

《超GAG》的战斗核心自研，避免被通用战棋或 MV 插件结构限制。

核心链路：

```text
SelectUnit
  -> PreviewMove
  -> ConfirmMove
  -> PostMoveCommand
  -> SelectAttackTarget
  -> Forecast
  -> Resolve
  -> UnitDone
```

必须支持：

- 移动预览。
- 路径显示。
- 取消移动回到原格。
- 移动后不能再次移动。
- 移动后可攻击/待机。
- 攻击前必须预测。
- 攻击/待机后行动结束。

## 后果

好处：

- 能追求兴趣作品的完成度，不被商业化早期约束绑死。
- 工程主线保持 Godot，可继续在 Codex 里测试和截图。
- 可大胆研究 SRW Engine MV 的机战语法，又不继承它的生态负担。
- 未来转正时，代码与资产风险更容易清理。

代价：

- 不能马上获得一个完整现成系统。
- 需要自己重写行动链、战斗预测和地图事件。
- 短期会多一个 `experiments/oss_spikes` 层，需要定期决定哪些实验合并、哪些丢弃。

## 下一步

创建隔离实验：

```text
experiments/oss_spikes/srpg_action_chain/
```

目标：

- 用 Godot 4.7 自研一个 action-chain spike。
- 不引入外部素材。
- 不复制无明确 license 的代码。
- 通过 headless smoke test 验证核心规则。
- 生成一张截图验证基本交互面板。
