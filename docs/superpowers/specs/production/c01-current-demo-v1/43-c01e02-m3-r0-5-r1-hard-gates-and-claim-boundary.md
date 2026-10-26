# C01E02 M3-R0.5｜R1 硬门与证据声称边界

> 日期：2026-08-18
>
> 状态：`active producer audit / mandatory completion-report disclosure`
>
> 作用：限制 R0.5 能证明什么，并阻止表现 PASS 覆盖玩法因果缺口

## 1. 审计结论

现有 M3-R0 可以作为**单场景试玩基线**，但不能作为“可直接进入 R1 的通用共同回合内核”。R0.5 只验证角色 UI、信息表达和共同结算演出是否已经达到可判断性；不修 resolver，也不证明两种战法已由通用因果系统产生。

无论 R0.5 画面、声音和用户试玩评价多好，以下 P1 证据缺口都继续成立：

1. `FrozenIntentSet` 的具体动作、目标与时点尚未真正驱动 resolver；prepared reaction 当前只检查终点是否落进固定 `reaction_rect`。
2. 玩家只能选择终点；BFS 自动替换为唯一最短路，尚无可编辑短路线或 waypoint。
3. 提交摘要没有完整复述 route/终点、final facing、main action 或 trigger→response、保护对象、接触组与预计时点。
4. `world_mutation_count=1` 与 `settlement_counts=1` 是 resolver 硬编码；现有测试只反查常量。`_route_hash` 实际哈希 `route_style`，不是玩家真实 route。

## 2. R0.5 允许与禁止的结论

### 允许

- `R0.5 presentation judgeability validated`
- 玩家能否理解角色、威胁、操作对象、摘要和事件顺序
- Full/Skip/fallback 是否在同一个冻结 R0 结果上保持表现等价
- 当前两个预设成功草案在镜头、动作与结果表达上是否容易区分

### 禁止

- `general common-turn kernel validated`
- `two tactics causally proven by resolver`
- `FrozenIntentSet fully drives settlement`
- `editable route system complete`
- `receipt evidence is independently derived`
- `R1 ready` 或任何同义说法

M0、A6、A7、M1 的完成报告和 U1/U2 卡都必须保留这一区分。机器 PASS、视觉 PASS 与用户喜欢都不能自动关闭 38 号看板中的 R1 硬门。

## 3. M0 边界

M0 不得修改：

- `shared_round_resolver.gd`
- R0 `sandbox_profile.json`
- BFS、route hash、settlement count 或 FrozenIntentSet 语义

M0 只可：

- 在玩家界面更完整地**展示当前草案已有字段**；
- 明确标注当前路径是系统预览路径，而非玩家逐段编辑结果；
- 在完成报告的 `Known P1 Evidence Gaps` 节逐条复制本文件第 1 节；
- 把所有因果改造留给未来独立任务，不用表现层伪造“玩家编辑过路线”。

## 4. 车辆称谓修正

R0 `sandbox_profile.json` 把本轮车辆称为“最后应急车”，与已验收 Reader 的时序冲突：真正最后一辆车是在挡住赤红冲击后才通过，并触发撤离线清空；R0.5 停点更早，`rescue_lane` 仍 active。

处理规则：

- 不修改冻结 R0 profile 或已验收 Reader；
- R0.5 玩家显示层使用“应急车”或“收尾应急车”；
- 不得显示“最后应急车已通过”“撤离线清空”或同义结果；
- 38 号 `R1_VEHICLE_COPY_GATE` 负责后续正式 Candidate 文案收敛。

## 5. A7 资产经济性裁决

当前两种成功草案仍与硬编码 resolver 高度耦合。在身份与通用因果接口通过前，不为三种路面末态投入批量精修。

A7 当前顺序改为：

1. 通过 41 号身份锁板门；
2. 只制作一张最能验证馆守 Z/BREAKER 身份和重量的代表性 Cut-in，优先 `GIANT_CONTACT`；
3. 制作可跨未来路线复用的接触尘土、炮击命中、红光蓄能 FX 与核心 UI/世界音色；
4. 用具名几何继续表示另外两种路面结果；
5. 三种路面末态的批量精修延后到 `R1_FROZEN_INTENT_CAUSALITY_GATE` 与 `R1_EDITABLE_ROUTE_GATE` 通过后。

42 号文件继续保留三种路面槽的未来 packing，不代表当前 A7 已获批生产它们。

## 6. 完成报告强制段落

M0 与后续联合完成报告必须包含：

```text
Claim level: presentation judgeability only
General common-turn causality: NOT PROVEN
Editable route/waypoints: NOT IMPLEMENTED
Commit summary completeness: INCOMPLETE IN FROZEN R0
Derived mutation/settlement evidence: NOT PROVEN
Actual route hash: NOT IMPLEMENTED
R1 readiness: BLOCKED BY PRODUCTION BOARD HARD GATES
```

缺少这一段时，报告不得标记 complete。
