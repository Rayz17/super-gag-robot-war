# G2-A2-C1 路线族、公开 API 玩家链与哈希隔离证明

## 路线族

- A 为 21 条等价单调最短路，7 步；B 为 15 条，6 步。
- hero A/B 仅作 GF/回归基准；直接点终点生成的 UP-first BFS 与另一条同族路线均成功。
- 错步数、错终点、错朝向、错动作均 fail closed。
- A/B 各 20 次确定性：各自唯一结果哈希；R2/R3 逻辑未改。

机器证据：[route-family.json](receipts/route-family.json)、[10-route-family.log](logs/10-route-family.log)。

## 无 fixture 玩家链

A/B 均从空草稿开始，源码与执行证据均不调用 fixture，不直接改 Session draft。链路仅经公开 API：

`PUBLIC_SITUATION → EDITABLE_DRAFT → append → facing → action/reaction → COMMIT_SUMMARY → return_to_edit → undo → append → COMMIT_SUMMARY → 0.7s hold → JOINT_RESOLUTION → ROUND_RESULT`

| 方案 | 输入等价 | authored_by_input | fixture_load_count | commit_count | preview/execute |
|---|---|---:|---:|---:|---|
| A | keyboard/mouse | true | 0 | 1 | same Resolver |
| B | controller | true | 0 | 1 | same Resolver |

机器证据：[public-player-chain.json](receipts/public-player-chain.json)、[11-public-player-chain.log](logs/11-public-player-chain.log)。

## R2C-C1 旧 B R1 哈希隔离热修

前置字段级复算证明，哈希载荷唯一差异为：

`events[2].facts.phase_readback.route_family`

| 状态 | B hero R1 round_result_hash |
|---|---|
| 字段混入 T1–T5 事件 | `63e94b9203b555ffe719ab29fe5b7236845403e5c2124a406c1e487a6e63a67a` |
| 仅移出该字段 | `c3b307b9698d645598594cb6674c86779a13420b9934cf562f379d112d1f41fa` |

world、ledger、settlement counts 逐项相同。修复只从事件哈希载荷移出该字段；`round_receipt.route_family_*` 与 `plan_summary.route_family` 仍保留机器证据。旧测试期望未改。

- 修复前反事实证据：[route-family-event-hash-diff-pre-fix.json](receipts/route-family-event-hash-diff-pre-fix.json)
- 修复后反向注入复算：[route-family-event-hash-isolation-post-fix.json](receipts/route-family-event-hash-isolation-post-fix.json)
- 原 C1 20 次回归：[r2c-c1-determinism-nonregression.json](receipts/r2c-c1-determinism-nonregression.json)
- 用户点名日志：[34-r2c-c1-ground.log](logs/34-r2c-c1-ground.log)

最终 B hero 旧签名精确恢复：R1=`c3b307…f41fa`，R2=`f09de0…6480a6`，各 20 次唯一。
