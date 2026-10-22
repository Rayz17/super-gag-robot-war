# 《超GAG机器人大战》多玩法运行时 M5 约束活动状态 v1

> 日期：2026-07-14  
> 状态：候选运行时实现回执  
> 上游：`2026-07-14-chao-gag-multi-play-implementation-blueprint-v2.md`  
> 边界：证明首个活动语法可以跨宿主复用并向战棋交付因果结果；不把 C05、C08、C11 拼成正式连续剧情，不改变 V35 正式进度，也不宣称 `TIMING`、`SIGNAL` 或 M6 已完成。

---

## 1. 本轮实现结论

M5 已实现首个可复用活动语法 `CONSTRAINT`：

```text
同一个 ConstraintActivityController
  -> A008 撤退路线规划（Desk 权限）
  -> A006 清算白名单谈判（Narrative 权限）
  -> A012 舰内灾害调度（Spatial 权限）
  -> HybridActivityResult
  -> ActivityOutcome / StateTransaction
  -> BattleSetupPatch
  -> Tactical 地形、目标、权限与资源
  -> BattleOutcome / Desk 回看
```

程序没有为路线、谈判和灾害分别建立永久系统。三者共享槽位、对象卡、相容/冲突、后果预览、可撤销草案和一次正式提交，只由内容数据改变对象、责任和后果。

## 2. 交互语法

活动界面固定为三个阅读层：

1. **可用对象**：证据、人员、路线、机体能力或设施。
2. **必须承担的责任**：必需槽与可选槽；槽位声明可接受标签。
3. **提交后果**：完成度、风险、冲突原因和后续可见变化。

玩家可以：

- 用键盘或鼠标选择对象与责任。
- 在正式提交前任意替换、移除或清空草案。
- 看到不相容原因和组合冲突，而不是提交后才被系统判错。
- 在 `fail / clear / good / perfect` 任一档正式提交；失败档也是继续承担后果的路线，不是重考。
- 提交后不能再次改写同一活动事务。

评分不再把“完美”硬编码为必须填写可选槽。内容可以用 `perfect_requires_optional` 声明活动自身规则；因此三项都是必需责任的灾害调度无需伪造第四个可选任务也能到达 `perfect`。

## 3. 结果合同

`HybridActivityResult` 进入 `RunStateStore.episode_memory.activity_results`，使用既有内容预算合同：

- 必需：`activity_id`、`score_band`、`ui_summary`。
- 可选：资源、变量、战斗修正、解锁标志、Canon 引用、来源节点、消费节点和软失败说明。
- 数量上限由 `HybridActivityResultValidator` 检查；单个活动不能私自扩张结果字段。

控制器再把结果包装为 `ActivityOutcome`，经 `OutcomeValidator -> StateTransaction -> RunStateStore` 一次提交。它可以写入：

- 事实、权限、关系边、承诺与债。
- 资源/变量/压力变化。
- `BattleSetupPatch`。
- 延迟人物反应请求。
- 玩家可读摘要。

活动不拥有第二套存档或永久状态。

## 4. 三个复用实例

| 实例 | 责任结构 | 主要冲突 | 验证用途 |
| --- | --- | --- | --- |
| `A008` 撤退路线 | 市民口、追击阻断、可选补给线 | 高可见撤离路与赤色诱饵同时暴露市民 | 证明地图路线、护送能力和补给可以用同一语法安排 |
| `A006` 法务谈判 | 事实依据、具名担责、可选限制条款 | 用馆方反证同时让七海担保，会把责任推回她身上 | 证明谈判不是选一句好话，而是交换权限和束缚 |
| `A012` 灾害调度 | 动力、防火、失联人员三项必需责任 | 防火门关闭与高速扫舱不能同时成立 | 证明无可选槽的危机仍能复用语法而不被模板扭曲 |

三份内容是运行时验证定义。它们来自 C05、C08、C11 的活动类型，但验证图不建立三章之间的正式故事连续性。C01 图也没有被注入 `A006` 或 `A012`。

## 5. 战棋因果消费

专用验证战 `M5-CONSTRAINT-HANDOFF` 的 patch catalog 同时支持三个活动的四档结果。当前完美路线会产生：

- `PATCH_M5_ROUTE_PERFECT`：提高撤离节点完整度，并登记三线撤离方案。
- `PATCH_M5_LEGAL_PERFECT`：开放带支援的临时白名单，提高护送单位 EN。
- `PATCH_M5_CRISIS_PERFECT`：保住最低动力，提高馆守 Z 验证单位 EN 与动力母线完整度。

`BattleSetupResolver` 只消费战斗定义显式认识的 patch；`BattleOutcome.applied_patch_ids` 再记录实际消费项。由此可以追溯“战场为什么是现在这样”，也不会让未知活动字段静默改变战斗。

同时修正了 `TacticalModeScene` 的 C01 硬编码：事务 ID、结果事实、版本事实、债务 ID 与反应前缀现在都可由 Episode 节点声明。M5 验证不会污染 `C01_TACTICAL_VARIANT_USED`。

## 6. 存档、撤销与幂等

M5 已验证：

- 未提交草案保存后可恢复对象、槽位和光标。
- 恢复后的草案仍可移除、清空和重新安排。
- 正式提交后控制器拒绝再次构造结果。
- 同节点提交若因结果合同错误被拒绝，拒绝回执会解锁草案并显示原因，玩家不会卡在不可提交状态。
- 即使旧候选结果被直接再次送给 `EpisodeDirector`，`OutcomeValidator` 与事务账本也会拒绝重复提交。
- 模式切换后只有统一状态中的 `activity_results`、patch、债和摘要继续存在，活动 UI 私有草案不会冒充世界事实。

## 7. 运行时内容包

- `game-godot/scripts/core/activity/activity_controller.gd`
- `game-godot/scripts/core/activity/constraint_activity_controller.gd`
- `game-godot/scripts/core/activity/hybrid_activity_result_validator.gd`
- `game-godot/scripts/modes/multi_play/constraint_activity_host_mode.gd`
- `game-godot/content/activities/constraint/*.json`
- `game-godot/content/episodes/runtime_validation/m5/graph.m5.json`
- `game-godot/content/activities/constraint/m5_constraint_consumption_battle.json`
- `game-godot/scenes/multi_play_m5_validation.tscn`

`ConstraintActivityHostMode` 是当前通用全屏宿主壳。它在验证图中分别受 Desk、Narrative 和 Spatial 的节点权限托管；正式 Episode 仍需验证控制器嵌入既有场景、保留人物/空间物件和活动输入压栈，而不是每次都切到抽象全屏板。

## 8. 验证证据

`multi_play_constraint_m5_smoke_test.gd` 覆盖：

- 三份定义共用一个控制器类。
- 相容、不相容、冲突和风险评分。
- 草案撤销、重置、快照和 Episode 级恢复。
- `fail / clear / good / perfect` 四档结果合同。
- 单次提交与重复事务拒绝。
- 错误 completion contract 被拒绝后，原活动可继续修改并重新提交。
- 同一场景在 Desk、Narrative、Spatial 三种权能节点下复用。
- 三项活动结果进入统一 ledger。
- 三枚 patch 被 Tactical 消费并写回 BattleOutcome。
- 跨章节验证不泄漏 C01 战术事实。
- C01 M4 图未引入 A006/A012。

2026-07-14 全量 `scripts/godot-test.sh` 通过 27 个脚本，新增通过标志：

```text
MULTI_PLAY_CONSTRAINT_M5_SMOKE_OK
```

Godot 4.7 全项目脚本扫描和 M5 场景无头启动通过；桌面运行首屏已检查对象卡、责任槽、后果预览、冲突区与提交区的可读性。

## 9. 尚未完成

1. `TIMING` 与 `SIGNAL` 仍只有设计语法，没有运行时控制器。
2. M5 验证链的第三次回收目前是 Desk 档案，不是由角色欲望和关系历史驱动的正式人物场。
3. 通用全屏宿主尚未嵌入一个正式 Narrative/Spatial 场景并保留背景人物、空间对象和镜头。
4. 正式音效、焦点动画、手柄、无障碍和鼠标拖连线未完成。
5. 还没有第二地点、第二机体、第二正式 Episode 的 M6 复用证明。
6. M5 当轮未做 Windows 导出；后续 M6 已完成 Windows x86_64 导出制品验证，但 Windows 真机、实体手柄、真人盲测和长时存档压力测试仍未完成。
7. 本回执不裁决 C01 的3回合/6回合版本，也不提升 V35 正式 Episode 数量。

## 10. 下一步

M6 不应继续增加抽象模板，应该选择一个非万机馆地点、一台非馆守 Z 机体和一个真正的第二 Episode：

1. 把 `ConstraintActivityController` 作为子活动嵌入实际空间或人物场，不使用通用全屏壳替代全部演出。
2. 选一段需要机械身体反馈的行动实现首个 `TIMING`，并与同一 Episode 的 `CONSTRAINT` 结果交叉消费。
3. 让活动结果至少经历即时物件变化、战术冲突和人物关系回收三次可见消费。
4. 用第二地点/机体完成保存、退出、回读、软失败、战斗和结算闭环，再进入真人盲测与平台导出。
