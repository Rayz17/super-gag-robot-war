# C01E02｜R2C-C1 R1／R2非回归证明

结论：A路只改变主小体地面锚点；B路签收hash原样保持；A/B第二轮路线、成本、接触、时序与音频均未回退。

## 确定性与旧签收对照

| 策略 | 回合 | 旧R2C round-result hash | C1 round-result hash | 20次结果 |
|---|---:|---|---|---|
| A | R1 | `e1c2b4224f36d51e177f34334d3b0f09b016e46baf07c0c3786923df88b3eef7` | `b4511d8fe51af415611c4e4f0c26e6226c1c0816b2c256726c8844de1615ad50` | 单一稳定hash |
| A | R2 | `d77a6d2bd35163af7496c2afbed1ea7fdd9fb6b52f6ead4d144359a993dcd838` | `e74b7ec9e936d61b78578597a03c3debea593bdfff2133de8b741c18b2ed5d2d` | 单一稳定hash |
| B | R1 | `c3b307b9698d645598594cb6674c86779a13420b9934cf562f379d112d1f41fa` | 同左 | 精确保持，20次稳定 |
| B | R2 | `f09de07bb6b0b32c1a44e7ca1d5e24a6cbc3bac498010cb92490b781bd6480a6` | 同左 | 精确保持，20次稳定 |

A的R1 hash因唯一坐标纠偏而变化；A的R2 hash因第二轮读取纠偏后的第一轮世界hash而随之变化。逻辑结果与成本没有第二项变化。

旧／新A路冻结mutation字段递归差异仅为：

```text
swarm_positions.ENEMY_C01_RIFT_SWARM_01: [21,9] -> [22,9]
```

B路冻结mutation字段差异为空。完整机器对照见`02-ground-occupancy-proof.json`与`04-determinism-receipt.json`。

## R1冻结值

- A：馆守Z`[20,9] south`，视觉recoil`[20,8.5]`，post-BREAKER`[21,11]`，heat`24`，margin`4`，road damage`42`，警戒设施`damaged`。
- B：馆守Z`[19,9]`，T2 east／T3 south，视觉recoil`[19,8.5]`，post-BREAKER`[21,10]`，heat`46`，margin`1`，road damage`24`，警戒设施`active`。
- T1→T5事件顺序保持；A T3 socket`[20.5,10.5]`；B T3 socket`[20,10.5]`；T4 east side socket分别为`[24,12.5]`／`[24,11.5]`。
- R1音频边界保持：T3 contact=`600ms`、pre-contact silence lead=`110ms`、四层同帧启动；T4 contact=`300ms`。

## R2动态占地与结果

```text
A route = [20,9] [19,9] [18,9] [17,9] [16,9] [15,9] [14,9] [14,10] [15,10] [16,10] [17,10]
A       = 10 steps / heat 68 / remaining margin 1
A deny  = [20,10] rejected by post-BREAKER [21,11] 3x3

B route = [19,9] [18,9] [17,9] [16,9] [15,9] [14,9] [14,10] [15,10] [16,10] [17,10]
B       = 9 steps / heat 88 / remaining margin 0
B deny  = [20,9] rejected by post-BREAKER [21,10] 3x3
```

A/B的preview与execute在20轮R1及其对应20轮R2中逐字段一致。主小体仍按缺省`blocks_route=false`排除于动态阻挡列表，第二轮只消费BREAKER的真实3×3占地。
