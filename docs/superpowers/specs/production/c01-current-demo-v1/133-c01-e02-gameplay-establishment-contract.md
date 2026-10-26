# C01 Demo E02 玩法成立合同

> 状态：`CANDIDATE_GAMEPLAY_AUTHORITY / E02_ONLY / NO_CANON_OR_RUNTIME_PROMOTION`
>
> 日期：`2026-08-27`
>
> 范围：C01 Current Demo 的 E02 地面规划**可结算玩法**。不改已验收 Reader，不升 Runtime / Default / Canon，不宣称视觉验收。E03 / E04 本批不改动词。

## 1. 这份合同立什么

132 只拥有「怎么看盘、选中、出菜单」。菜单词当时停在建议草稿，不能交差为玩法。

本文补上那一层：**玩家每一轮真正在下的棋，必须能被 Resolver 结算。**

语言源（Candidate，不因本文升 Canon 或获得全作 Build 权）：

- `docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/00c-core-game-design-master-review.md`（短全队协同、朝向、预备、身体功能、非歼灭）
- 同目录 `00d-c01-c03-common-system-adaptation.md`（C01：移动、朝向、阻挡、保护、非歼灭目标）

本批只收 **C01 Demo E02 限域**。不整包 00c。不搬机战六指令、人物牌、气势条、请战、完整机魂审批。

## 2. 权威分层

冲突时按这次序：

1. Canon Hard / Working
2. 已验收 C01 Reader 与用户创作验收回执
3. **本文：E02 玩法结算真值**
4. `134-c01-e02-play-experience-binding-design.md` 的看盘／落子／确认体验绑定
5. `132-c01-e02-interaction-establishment-contract.md` 的光标 / 选中 / 信息卡 / 一层取消 / `1/2` 不得出击
6. `128-c01-full-breaker-operation-demo-product-objective-and-execution-plan.md` 的 Operation 范围、美术锚、表现三级
7. `19-current-demo-inplace-rebase-producer-contract.md` 的故事顺序、滚动图、占地、检查点、一次性盾拍
8. History（含「拦截/保护只写入建议草稿」「只有菜单没有结算」「拦截自动写死 A 族合法一手」）

00c 仍是 Candidate 语言源。选中层字段（`focus_unit_id`、`unit_menu_open`）仍是输入层，不进 Resolver。

## 3. 玩家每一轮真正在下的棋

```text
看盘（132 铬 + 134 冻结意图）
→ 选中馆守Z，点亮拦截或保护（134）；本文写入动作或预备
→ PLACE：玩家摆短路与朝向；接触质量在盘上显形
→ LOCK 锁住已见的接触、谁承担代价、撤离/道路、功能损伤
→ 确认后共同结算
→ 局势写回下一轮
```

菜单不得替玩家写死合法一手。采用建议或自摆之后，本文才按路族、朝向质量和责任结算。

时制保持现网共同结算。敌方本轮计划在提交前冻结。合法方案仍必须走 SUMMARY。

E02 玩家只编排馆守Z。BREAKER / 应急车 / 小体只检查出卡。

## 4. 可结算规则

### 4.1 朝向有用

馆守Z 到达后朝哪边，才用完整身体挡住冲线或护住撤离线。

| 责任 | 正面朝向 | 正面结果 | 侧向 | 背向 |
| --- | --- | --- | --- | --- |
| 拦截 | 南（对着北向冲线） | 完整身体挡冲线 | 偏挡：接触成立，BREAKER 更深，馆守Z 更热 | 挡失败，本轮不写成功策略 |
| 保护 | 东（对着东门撤离线） | 完整身体护车道 | 偏挡：车仍可能过，BREAKER 更深，机动更伤 | 护失败，本轮不写成功策略 |

Resolver 必须读玩家写入的 `final_facing` / `settle_facing`，不能只改字段、不改接触判定。正面质量由责任决定，不是固定南向字段校验。

### 4.2 拦截 vs 保护是两条责任

不是两个建议草稿标签。

| | 拦截 / 迎撞 | 保护 / 护线 |
| --- | --- | --- |
| 写入 | 主动作 `BODY_INTERCEPT`，清预备 | 预备 `PROTECT_LANE_RESPONSE`，清主动作 |
| 未画路时 | 点亮 A 族终点带 `[20,9]` 与南向扇；采用建议后才写入朝南的路 | 点亮 B 族终点带 `[19,9]` 与东向扇；采用建议后才写入朝东的路 |
| 已画路时 | 只改动作 / 责任，不抢路；盘上立刻按新题目改口，见 134 §8 | 只改预备 / 责任，不抢路；盘上立刻按新题目改口，见 134 §8 |
| 代价 | 馆守Z 用防护承力吃冲线；热较低；路损更重 | 馆守Z 用机动换护线；热更高；BREAKER 更接近目标 |
| 结算必须读出 | 谁挡了冲线、防护承力怎样 | 谁护了车道、机动怎样 |

可继续用现网 A/B 路线族。责任动词必须写入不同动作或预备；路与朝向按 134 在采用建议或自摆后才算写下。R2 / R3 仍写本轮唯一主动作；责任标签继续区分谁承担。

### 4.3 动作 + 预备反应可结算

EDIT 里选**一个**主要动作或**一条**预备。C01 瘦身动词：

- R1：`BODY_INTERCEPT` 或 `PROTECT_LANE_RESPONSE`（例如「小体踏入撤离线就侧推」）
- R2：`TAKE_SHIELD_BLOCK_RED`
- R3：`SIDE_PRESS_SHIELD_BASH`

不要搬机战六指令。不要人物牌 / 气势条 / 请战 / 完整机魂审批。

### 4.4 非歼灭结算

重点不是击破数。SUMMARY 与 RESULT 必须能读出：

1. 谁撤出了（应急车是否过东门）
2. 哪条路仍可用（撤离线 / 冲线是否被挡）
3. 机体留下什么功能损伤：机动 / 作用 / 防护承力（C01 看得见的一层）
4. 这些字段写回下一轮快照

不要伪造 Reader 结局。不要把 P1 写成 Mission Clear。

### 4.5 时制与单位

- 共同结算。提交前敌方计划冻结。
- 合法方案必须 SUMMARY。
- 只编排馆守Z。

## 5. 本文明确不做

- 不改 Reader 事实、检查点字段语义、盾拍一次性授权
- 不改 E03 / E04 动词（测试 helper 只跟 E02 入口）
- 不把 B5 西向馆守 / 越黄线混进本条
- 不宣称视觉验收
- 不升 Canon / Runtime / Default
- 不把选中层送进 Resolver

## 6. 现网落地

- 输入：`e02_full_input_controller.gd`（132 选中层保留；菜单动词写玩法状态）
- Session：`e02_player_session.gd`（`responsibility` 只作计划标签）
- Resolver：`e02_player_resolver.gd`（朝向质量、责任、功能损伤；不另起平行引擎）
- HUD / 地图：复用右栏与教练区；文案改棋手语法；对照 `scratch/srw-y-mode-recreation/`
- Runner：只接线

## 7. 本批落地回执（2026-08-27）

Candidate 已接到现网。不升 Canon / Runtime / Default。

- 菜单「拦截 / 保护」写入动作或预备与责任；路和朝向按 134 由采用或自摆写下。Resolver 先补责任正面走原 A/B 族，再用玩家真实朝向 overlay 接触质量与功能损伤
- 测例：`game-godot/tests/c01_breaker_demo/e02_gameplay_establishment_test.gd`；体验绑定：`e02_experience_binding_test.gd`
- 实帧：`game-godot/captures/c01_e02_gameplay_hud/current/`（窗口 capture，`user_visual_acceptance=false`）

`user_visual_acceptance=false`。
