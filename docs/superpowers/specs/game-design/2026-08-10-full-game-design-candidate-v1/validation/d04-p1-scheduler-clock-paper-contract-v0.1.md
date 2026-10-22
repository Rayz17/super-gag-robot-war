# D04-P1 四时制世界时钟适配纸面合同 v0.1

> Status: `candidate_paper_contract / zero_build / zero_runtime / human_not_run / user_not_decided`
>
> Scope: 只定义 `D04-P1-A/B/C/D` 如何把各自原生命令边界映射到同一个八秒世界周期。它不选择时制，不证明公平，也不授权原型制作。

## 1. 这条合同补什么

动作持续时间相同，不代表世界时间已经相同。若 A 每激活一台单位就让撤离车走一次，D 每个阵营阶段让桥梁结算一次，而 B/C 每八秒只结算一次，那么四版实际上拥有不同 Deadline、不同桥梁寿命和不同敌方观察年龄。

因此 [scheduler-clock-adapter-contracts.tsv](../data/scheduler-clock-adapter-contracts.tsv) 把以下内容从 Scheduler 中剥离为共同世界合同：

- 一个世界周期恒为 `8.0s`；
- A 的一轮交替激活、B 的一个全队时间窗、C 的一轮交替锁计划、D 的我方加敌方两个阶段，都只关闭一个世界周期；
- 自主单位只执行 `t=2/4/6/8s` 四个微刻度，不能按激活数或阵营数重复推进；
- 桥梁基础增量、Deadline、Observation Snapshot、Intent 冻结、Reaction 过期和挥发资源重置都只在约定边界发生一次；
- A/D 的先后提交和可见局部后态、B 的全队草拟、C 的锁定顺序仍是被测变量，不被伪装成共同结果。

## 2. 共同周期账

```text
cycle_open(k)
  -> freeze eligible units, autonomous routes, observation snapshot, enemy intents
  -> scheduler-native commits append duration-stamped events
  -> scheduler close condition reached
  -> replay one 0..8s cycle event log with autonomous microticks 2/4/6/8
  -> apply named contact/environment markers
  -> apply bridge/environment base tick once
  -> evaluate cycle deadline/objectives once
  -> capture next observation snapshot
  -> expire reaction and volatile cycle state
  -> world_time += 8s; cycle += 1; stable receipt/save boundary
```

在 A/D 中，单位提交后可以显示并锁定该单位的局部后态，后续单位可以据此选择；但车辆、桥、Deadline 和 Intent 刷新尚未发生。它们必须等整个周期关闭后，从同一份带真实动作时长的事件日志重放。这样保留了 A/D 的原生先后承诺，同时不会按单位数额外推动世界。

B/C 直接从时间轴或锁定计划产生同一种事件日志。四版若在共同 `ALL_WAIT` 输入下产生不同 `world_event_hash`，立即停止比较；非空计划因 Scheduler 顺序造成的差异则必须归入 `declared_non_equivalence`，不能偷改世界 tick 来抵消。

## 3. 七组纸面事件向量

[d04-p1-adapter-event-vectors.tsv](../data/d04-p1-adapter-event-vectors.tsv) 为每个 Adapter 登记同样七组向量，共 `4 × 7 = 28` 行：

| 断言类 | 初态与计划 | 四版都必须得到 |
| --- | --- | --- |
| world clock / autonomous | `time=0, cycle=0, clear lane, ALL_WAIT` | 只推进到 `time=8, cycle=1`；自主对象走四个微刻度 |
| environment base | 危险格周期末被占用 | 桥基础 tick 恰好一次，`stress 0→1` |
| named markers | 占用 `+1`、Breaker推进 `+2`、已完成 Brace `-2` | 周期末净 `stress 0→1`，不按激活/阶段重复 |
| observation / intent | Intent 已在开窗冻结，玩家随后移动 | 本周期 `intent_revision_count=0`；闭窗后才生成下一快照 |
| reaction / volatile reset | 预留反应但未触发 | 闭窗时过期一次；不因A/D多个提交重复重置 |
| 32s deadline | `time=24, cycle=3` 且只有一辆完成撤离 | 第四次闭窗才评估一次并进入 `retry_required` |
| mid-cycle restore | 已有两个锁定事件的中段快照 | 恢复后的闭窗 hash 与直跑相同；world tick 仍只有一次 |

这些向量只是机器 Fixture 输入，不是自动测试已通过的证据。真正 Build 必须把 `pre_state_ref / normalized_plan_ref / expected_delta / post_state_ref` 编译成可执行状态并记录 ruleset、adapter、build 和结果 hash。

## 4. Save、提前退出和边界异常

- 跨 Adapter 对照只使用 `cycle_open` 或 `cycle_close` 稳定存档；中段存档可用于本版恢复，但必须保存事件日志、提交游标、eligible set、冻结 Intent 与尚未应用的 world ticks。
- 周期内任何单位被移除都不减少本周期开窗时冻结的必需槽；其槽转为具名 `WAIT_REMOVED`。周期中新到单位只从下一周期开启主动槽。
- 在零提交前 Withdraw 不推进世界；一旦本周期已有提交，Withdraw 先封存当前周期并按八秒推进一次，不能通过反复撤回来冻结 Deadline。
- 提前达到稳定 `retry_required` 时封存当前周期，不能再加一个额外八秒 tick。

## 5. 进入 Build 前停止门

以下任一未满足，P1 仍只能称为“Scheduler与世界时钟纸面合同”，不得称“公平可实现”或“实现就绪”：

1. 四个 Adapter 对28行向量全部生成可执行用例；
2. 四版 `ALL_WAIT` 的 `world_time / autonomous / environment / observation / deadline / volatile reset` hash一致；
3. 四版在第四周期只于 `32s` 评估一次 Deadline；
4. 桥基础 tick 每周期最多一次，Breaker/Brace 等具名 marker 只消费一次；
5. Intent 在周期内不因 A/D 后续提交重算，下一快照年龄一致；
6. 中段恢复与直跑的闭窗状态、事件日志、objective结果完全相同；
7. 任何故意保留的世界时钟差异已登记为新的实验变量并重新获得比较方案裁决，不能继续冒充共享真值。

当前状态仍为 `zero_build / human_not_run / presented_no_decision`。
