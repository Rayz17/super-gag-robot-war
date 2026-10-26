# C01 Demo E02 交互成立合同

> 状态：`CANDIDATE_INTERACTION_AUTHORITY / E02_ONLY / NO_CANON_OR_RUNTIME_PROMOTION`
>
> 日期：`2026-08-27`
>
> 范围：C01 Current Demo 的 E02 地面规划交互。不改已验收 Reader，不升 Runtime / Default / Canon，不宣称视觉验收。E03 / E04 本批不改动词。

## 1. 这份合同立什么

19 号制作人合同把已验收剧情转成了棋盘上的身体动作，没有立「玩家怎么下棋」。本文件补上那一层：**C01 Demo E02 的交互提供方式。**

不是新发明一套全作玩法，也不是把总案整包塞进 Demo。语言来自已经写过的 C01 瘦身和 E02 限域转译：

- 总案：`docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/00c-core-game-design-master-review.md`
- C01 瘦身：同目录 `00d-c01-c03-common-system-adaptation.md`
- Demo 限域：`87-c01e02-u86-route-a-user-approval-and-gameplay-alignment-reopen-receipt.md`、`88-c01e02-r2c-fun-first-current-topology-map-and-interaction-contract.md`

本文件只收束并拥有 **E02 玩家怎样看盘、选中单位、出菜单和信息卡、编排、看见预期、再激发**。手感学自复刻案例；**收哪一层、不收哪一层以 `134` §4 为准**。本文只保光标、选中、一层取消这些铬。词只用 C01 瘦身动词。

**玩法权威见 `133-c01-e02-gameplay-establishment-contract.md`。体验绑定见 `134-c01-e02-play-experience-binding-design.md`。本文只拥有交互铬。** 菜单词必须由 133 写成可结算的动作 / 预备 / 朝向 / 终点责任；不得再把选中、菜单或 SUMMARY 当成玩法交差。与 134 冲突时（拦截自动写死合法一手、五条对等菜单、SUMMARY 才揭晓接触），以 134 为准。

## 2. 权威分层

冲突时按这次序：

1. Canon Hard / Working
2. 已验收 C01 Reader 与用户创作验收回执
3. `133-c01-e02-gameplay-establishment-contract.md` 的 E02 可结算玩法
4. `134-c01-e02-play-experience-binding-design.md` 的看盘／落子／确认体验绑定
5. **本文：E02 交互铬**（光标、选中、信息卡、一层取消、`1/2` 不得出击）
6. `128-c01-full-breaker-operation-demo-product-objective-and-execution-plan.md` 的 Operation 范围、美术锚、表现三级、系统级禁令
7. `19-current-demo-inplace-rebase-producer-contract.md` 的故事顺序、滚动图、占地、检查点、一次性盾拍
8. History（含「1/2 自动铺路并出击」「合法方案跳过 SUMMARY」「拦截/保护只写入建议草稿」「拦截自动写死 A 族合法一手」）

00c 是语言源，不因本文自动升 Canon 或获得 Build 权。19 不再拥有交互权威。128 §3 体验表里「查看公开意图；画路线；定朝向；选动作／预备；摘要；提交」升回交互真值；§12 / §13 把 `1/2` 写成主动词的句子降为 History。

## 3. 玩家每一轮做什么

玩家叫法与落子顺序以 `134` 为准。本文仍拥有光标、选中、信息卡和一层取消。下面是铬层清单，不是体验真值。

```text
看盘：敌方意图、撤离线和黄字目标长在地上；光标常亮
→ 光标/点到单位：先出信息卡（谁、朝向、这面能否挡）
→ 确认选中馆守Z：进入这一手；右栏按 134 只留拦截 / 保护 / 看预期
→ 检查 BREAKER / 车 / 小体：只有信息卡，没有编排菜单
→ 点地画短路；A 只落格。朝向在终点玫瑰上拧，不占对等菜单
→ 拦截 / 保护按 134 点亮题目，按 133 写入责任；采用建议或自摆后才算写下解
→ LOCK 看见接触质量、谁承担代价、撤离/道路和功能损伤（只锁盘上已见之物）
→ 确认后共同结算
→ 局势写回，再转下一轮
```

三个判断始终回到地上：

1. 哪台机体现在能到达危险点？
2. 它到达后朝哪边，才能用完整身体阻挡或保护？
3. 谁承担代价：正面迎撞，还是先护撤离线？

时制保持现网共同结算。不是「我方回合打完再进入对方回合」。敌方本轮计划在提交前冻结，不能读未提交草稿。

## 4. 各层只做什么

### PUBLIC：只看盘

- OPERATION 短面仍先盖住活地图，写今晚守什么、败了怎样。关掉卡之后才看盘。
- 地上必须能读出：BREAKER 冲线、东门车道、小体扑线、黄字目标。字只给已经看得见的东西起名。
- `1/2`、点右栏、点黄字 A/B **不得写计划、不得进 SUMMARY、不得出击**。它们最多画出建议幽灵廊。
- 方向 / 鼠标移光标。光标或点击压在单位占地或立绘上，就出信息卡。Enter / 空格 / Start / A = 确认当前层：选中光标下的单位，不直接进 EDIT。
- Q / P / Tab 在场上可读单位间切换。

### 选中：信息卡 + C01 菜单

- 选中馆守Z（点身体/立绘、光标在它身上确认）：信息卡留下，右栏弹出菜单 `拦截` / `保护` / `看预期`。画路和朝向回到地上，见 134。
- 选中 BREAKER、应急车、小体：只有信息卡，不给编排菜单。
- 菜单不是机战六指令。没有精神、气势、待机、攻击。
- 拦截 / 保护 → 按 134 点亮题目，按 133 写入可结算责任，不写死路和朝向，停在 EDIT。看预期 → 仅一手齐了才能进 SUMMARY。
- Esc / B：LOCK 回 PLACE；PLACE 有路先撤一笔；只剩责任回未选责任的选中；选中回看盘。

### EDIT：才编排

- 玩家在地上画路、定朝向；菜单只点亮拦截或保护。
- `1/2` 按 134：未点责任时点亮题目；已有责任时采用当前题目的建议。停在 EDIT。不得跳过 SUMMARY。
- 手柄 A 只落格。不搬六指令。不把 A 改成出击。
- 第二、三轮同一语法：未画路时按 1 不得直接铺官方取盾/侧压并出击。建议可以给幽灵廊。

### SUMMARY：必须经过

- 合法方案也不得从 EDIT 直接出击。
- 同一屏看见接触、朝向、A/B 代价、第二轮余量。
- Esc / 手柄 B 回 EDIT。Start / Enter 只在 SUMMARY 激发。

### 机体反馈：只做潜伏身体状态

C01 不塞人物牌、气势条、请战、完整意愿审批。信息卡只写名字、朝向、占地和一行身体/意图句，例如「正面才能挡住冲线」「先护线会更热」「冲线从南边来」。C01 菜单是编排入口，不是拒绝菜单，也不是六指令。

## 5. `1/2` 的新身份

看懂盘之后可作建议，不能一键替代编排。

| 状态 | `1/2` / 右栏 / 黄字 A/B 可以做什么 | 不可以做什么 |
| --- | --- | --- |
| OPERATION 卡开着 | 无 | 关卡、选打法、写计划 |
| PUBLIC | 画出建议幽灵廊；移光标看信息卡 | 写计划、进 EDIT、进 SUMMARY、出击 |
| EDIT | 填入可改的草稿 | 跳过 SUMMARY、直接出击 |
| SUMMARY | 无 | 改写已提交预期 |

A/B 仍是两条真实责任族（主动迎撞 / 先护撤离线），不是两个剧情按钮。Resolver 继续按终点、朝向、动作认路线族，不要求复刻隐藏标准路。

## 6. 本文明确不做

- 不改 Reader 事实、检查点字段、盾拍一次性授权
- 不引入人物牌、气势条、请战、完整机魂审批
- 不把时制改成传统我方/敌方阶段
- 不搬机战六指令，不把 EDIT 里的 A 改成出击
- 不在本批改 E03 / E04 动词
- 不升 Runtime / Default / Canon，不宣称视觉验收
- 不把 B5 西向馆守 / 越黄线混进本条

## 7. 体验门

盖住字，只看地图，玩家仍能说出：

1. BREAKER 要从哪条线冲过来；
2. 车要从东门哪条车道先过；
3. 馆守Z该画到哪一带，朝哪边才能挡或护。

内部 PASS 和 headless 测例不能代替这扇门。`user_visual_acceptance=false`。

## 8. 现网落地

- 输入：`game-godot/scripts/c01_breaker_demo/e02_full_input_controller.gd`
- HUD：`game-godot/scripts/c01_breaker_demo/c01_gf_operation_hud.gd`
- 地图：`game-godot/scripts/c01_breaker_demo/c01_ground_map_view.gd`
- Session / Resolver 的 `PUBLIC → EDIT → SUMMARY` 和路线族验收保留；拆掉的是「1/2 自动铺路并跳过 SUMMARY」。

改完用 `./scripts/godot-run.sh` 走序章 → OPERATION → 看盘面 → 光标/点中单位出卡 → 选中馆守Z出菜单 → 点亮拦截或保护 → 采用或自摆 → SUMMARY → 出击。不宣称视觉验收。体验绑定见 134。
