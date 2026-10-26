# A30 Call01｜BREAKER EAST Section 2 硬门失败回执

> 状态：`STOPPED_AFTER_EAST_HARD_GATE_FAIL`
>
> `user=false / runtime=false / default=false / canon=false`

## 本轮实际执行

- 使用内置 ImageGen：`1` 次（EAST）。
- 随机重抽：`0`。
- SOUTH：`0` 次；WEST：`0` 次。
- 现有 NORTH 未覆盖、未改字节。

## 停线原因

1. **方向极性失败**：要求 EAST 头端朝画面右下；生成结果的唯一红缝却位于主体质心左下侧，红缝从头端迁移到近尾侧，不能证明正确朝向。
2. **Alpha 失败**：生成结果为 `1254×1254 RGB`，棋盘背景烘焙进 RGB，没有透明通道；内部封闭负空间同样无法成立。

这是身份/极性/alpha 三项硬门中的两项失败。按 Wave A 合同，本轮不得二次生成 EAST，不得继续 SOUTH/WEST，不得以抠图或移动红缝修补，更不得写入 Godot、Runtime、Default 或 Canon。

## 保留证据

- 失败 raw：`call01/generation-raw/BREAKER_A30_CALL01_EAST_RAW_FAIL.png`
- 对照 QA：`call01/qa/BREAKER_A30_CALL01_EAST_HARD_GATE_FAIL_QA.png`
- 机器读回：`call01/receipts/BREAKER_A30_CALL01_EAST_HARD_GATE_FAIL.json`

失败 raw 只作 History/诊断证据，禁止成为任何后续正向设计、精灵或动作输入。

