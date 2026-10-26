# WR 多周期：机制现状与第二周期内容编写提案（2026-09-16，待裁决 ④）

## 机制现状（代码核实，非待建）

`formula_lab_world_route_cycle.gd` 已实现：
- `cycle_limit=2`（两个周期）、`initial_tick` 与世界时钟一致性校验；
- 每条路线节点必须显式编写 **chosen / unchosen 两条后续分支**，各含
  `version / owner / request_status / condition / commit_state / commit_note / alternative` 七个文本字段；
- `undefined_evolution = hold`：未定义的后续演化**保持上一状态，不叠加惩罚**；
- 「不可提交」路线的 chosen 分支允许为空对象 = 无授权许可，该分支不可达。

即：**裁决 ④ 不是机制选型，而是第二周期后续内容（chosen/unchosen 文本行）的编写授权**。
门禁缺口 `WR_CAP_MAP_NEXT_ROUND_UNVERIFIED`（下一轮到访未在图内验证）与
`WR_CAP_MAP_POST_CYCLE2_UNAUTHORED`（周期 2 之后无编写内容）对应的就是这块内容账。

## 三个编写方案（对应 pending-decisions ④ A/B/C）

- **A 催办制**：未选请求的 unchosen 分支写「保留主体 → 升级催办」文本行，
  周期 2 开场时地图上出现具名催办事件（例：值班员请求 → 值班员亲自到棚口催办）。
  编写量：每条未选路线 1 行 + 1 段结果对白引用。
- **B 挂起制**：unchosen 分支写「维持保留、无主动动作」文本行（现状即此语义，只需显式成文）。
  编写量：每条未选路线 1 行。
- **C 混合**：硬阻断类（限宽架/坡道）走 A 催办，普通巡访类走 B 挂起。
  编写量：按请求类型分流，约 A+B 各半。

## 与 G/H 包的关系

G（器材棚 T0→T1）与 H（旧仓 T3→T4）已各演示一次周期循环。第二周期内容编写可在任一包的
下个版本进行，不需改机制代码；`POST_CYCLE2_UNAUTHORED` 缺口在选定方案并编写后关闭。

## 落地动作（选定后）

1. 按选中方案在下一 WR 包的 `cycle_plan.nodes[*].unchosen`（或 chosen）编写后续文本行；
2. 门禁用例补充：断言周期 2 后未选分支的文本行进入 readback、且不触发世界惩罚；
3. 原生录制一段「周期 2 开场」的地图状态帧作为证据。

## 预拟文本行（以 H 路线 WR_LAB_OLD_STORE 的 unchosen 分支为例，七字段对齐 WR_T2 既有格式）

**A 催办制（周期 2 开场出现具名催办事件）：**

| 字段 | 内容 |
| --- | --- |
| version | v2-escalated |
| owner | 值班员 |
| request_status | escalated |
| condition | 重机通行请求已挂催办；值班员将到棚口亲自核对。 |
| commit_state | 有条件 |
| commit_note | 周期 2 开场可见催办事件；拒绝需具名并留下替代安排。 |
| alternative | 改走侧门需先与维护员打招呼。 |

**B 挂起制（维持保留，无主动动作）：**

| 字段 | 内容 |
| --- | --- |
| version | v2-held |
| owner | 值班员 |
| request_status | held |
| condition | 请求保留原状；重机通行仍未安排。 |
| commit_state | 有条件 |
| commit_note | 未承接前不安排重机；不设时限，不追加后果。 |
| alternative | 随时可承接；承接前状态不变。 |

**C 混合制**：硬阻断类请求（重机通行/限宽架）用 A 的催办行；普通巡访类（归档/察看）用 B 的挂起行。每条请求按其类型分流，编写量为 A、B 之和的对应子集。

选定后：把选中方案的字段行写入下一 WR 包 `cycle_plan.nodes[WR_LAB_OLD_STORE].unchosen`（及对应新请求节点），补门禁用例断言周期 2 readback 含该行且无惩罚叠加。
