# 《超GAG机器人大战》多玩法运行时 M4 战术接入状态 v1

> 日期：2026-07-14  
> 状态：候选运行时实现回执  
> 上游：`2026-07-14-chao-gag-multi-play-implementation-blueprint-v2.md`  
> 边界：证明 Tactical adapter 与跨模式因果回流；不裁决 C01 正式采用3回合或6回合，不改变 V35 正式 Episode 进度。

---

## 1. 本轮实现结论

M4 已从占位 `TacticalModeScene` 推进为可运行的声明式战术模式：

```text
Spatial ActivityOutcome
  -> battle_setup_patches
  -> BattleSetupResolver
  -> DeclarativeBattleSession
  -> TacticalModeScene
  -> BattleOutcome
  -> StateTransaction / RunStateStore
  -> success / costly_success / failure / withdrawal aftermath
  -> Desk
```

同一适配器可以装载3回合冻结候选和6回合既有制作口径。回合数、单位、武器、目标、障碍、中段事件与撤离权限均来自内容数据，不由程序分支硬编码。

## 2. 数据合同

### BattleSetup

战斗定义至少包含：

- `battle_id`、`variant_id`、`turn_limit`。
- 地图宽高与初始阻挡格。
- 玩家、敌方单位及武器。
- 必须保护目标与可形成有代价胜利的次要目标。
- 中段事件、撤离权限和可消费的 patch catalog。

`BattleSetupResolver` 从 `RunStateStore.episode_memory.battle_setup_patches` 读取上游结果，只应用战斗定义显式允许的补丁。当前现实机器区会提交 `PATCH_C01_FAILURE_BLOCK_LINE_B`，进入战斗后改变阻挡格和撤离目标完整度；相同 patch ID 只应用一次。

### BattleOutcome

结算记录包含：

- 战斗与版本 ID。
- `success / costly_success / failure / withdrawal`。
- 实际回合、敌方残留、存活单位。
- 各保护目标最终完整度。
- 已触发中段事件与已消费 setup patch。
- 地图行动记录和玩家可读摘要。

`withdrawal` 是一等结果，不伪装成取消或普通软失败；它进入专属撤离剧情，并创建未完成保护责任。

## 3. 战术交互

独立 `TacticalModeScene` 当前提供：

1. 斜45度地图、光标、单位状态和目标完整度。
2. BFS 可达范围与避障路径；不可穿过展台和单位。
3. 单位命令、移动预览、取消移动、待机。
4. 武器列表、合法目标列表、射程覆盖和战斗预测。
5. 敌方行动意图与目标连线。
6. 即使尚有可行动单位也能主动结束阶段。
7. 数据驱动增援、阻挡变化和回合事件。
8. 主动撤离并承担后续后果。
9. 结果确认页；玩家确认后才提交并返回剧情。
10. 战斗中途精确存取，包括回合、单位位置、命令子状态、攻击草稿和可撤销移动上下文。

## 4. C01 验证内容包

- `game-godot/content/episodes/c01/e01/battle/c01_e01_v3510_candidate_3t.json`
- `game-godot/content/episodes/c01/e01/battle/c01_e01_legacy_protection_6t.json`
- `game-godot/content/episodes/c01/e01/graph.m4.json`
- `game-godot/content/episodes/c01/e01/manifest.m4.json`
- `game-godot/scenes/c01_multi_play_m4_validation.tscn`

验证图将 Tactical 的四类结果分别送入成功、有代价、失败和撤离即时反应，再汇入 Desk。当前默认加载3回合冻结候选只为缩短运行时验证，不代表版本裁决。

## 5. 修正的底层问题

1. `ObjectiveSystem.failure_reached()` 原来遇到第一个存活目标就提前返回，后续保护物即使归零也不会失败；现已检查全部保护目标。
2. `all_players_done()` 原来漏掉 `MOVED_READY`，可能错误判断全员结束；现已区分仍可行动的移动后单位。
3. `GridService` 原来只按曼哈顿距离涂范围，路径可能穿过障碍；现改为 BFS 可达范围和最短合法路径。
4. Narrative 与 Desk 原来使用固定 M1 事务 ID；现由 Episode 节点提供或按 node ID 生成，允许同一话多次进入叙事/结算节点而不冲突。

## 6. 验证证据

`multi_play_tactical_m4_smoke_test.gd` 覆盖：

- 3回合与6回合定义共用适配器。
- Spatial patch 改变 Tactical 几何与目标状态且只应用一次。
- 移动后存档、恢复、取消回原位。
- 提前结束阶段与敌方行动。
- 数据驱动增援。
- 成功、有代价胜利、失败、撤离四种结果。
- Episode 分支、Tactical 返回 Narrative、BattleOutcome 幂等提交。

2026-07-14 本阶段完成时全量 `scripts/godot-test.sh` 通过 26 个脚本，新增通过标志：

```text
MULTI_PLAY_TACTICAL_M4_SMOKE_OK
```

## 7. 尚未完成

1. C01 正式战斗版本裁决及正式 Episode Packet。
2. 战斗演出播放器与新 Tactical adapter 的正式武器演出联调。
3. 更完整的地形代价、援护、反击、精神/燃魂和机体尺寸规则。
4. 敌方 AI 仍以公开意图与目标推进为主，尚未形成多种敌人策略模板。
5. 正式战斗 UI 美术、音效、镜头停顿、伤害数字和角色 cut-in。
6. M5 的 `CONSTRAINT` 已在后续回执验证；`TIMING`、`SIGNAL` 与 M6 跨地点/机体/Episode 复用仍未完成。
7. 真人时长、手柄、Windows EXE 和平台压力测试。

## 8. 下一步

M5 的 `CONSTRAINT` 已完成并续记于 `m5-constraint-implementation-status-v1.md`。下一步必须用非万机馆地点和非馆守 Z 机体完成 M6 复用门禁，并在正式 Episode 中补足人物反应的第三次可见消费。
