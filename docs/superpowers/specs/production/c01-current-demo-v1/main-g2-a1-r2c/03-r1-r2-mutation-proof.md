# R1→R2 world mutation与动态路线证明

机器明细：`receipts/contact-staging.json`。

## 第一轮离散写回

| 字段 | A | B |
|---|---:|---:|
| `guardian_position` | `[20,9]` | `[19,9]` |
| `guardian_heat` | `24` | `46` |
| `breaker_depth` | `11` | `10` |
| BREAKER entity anchor | `[21,11]` | `[21,10]` |
| `road_damage` | `42` | `24` |
| `warning_facility_state` | `damaged` | `active` |
| primary swarm post | `[21,9]` | `[22,8]` |
| `remaining_timing_margin` | `4` | `1` |
| impact socket | `[20.5,10.5]` | `[20,10.5]` |
| east side socket | `[24,12.5]` | `[24,11.5]` |

第二轮`frozen_intent_set`与resolver从上述world重新读取Guardian起点、热量、BREAKER anchor／3×3 footprint、路损、设施、小体位置与余量；赤红冲击的动态源分别为`[21,11]`和`[21,10]`。

## 第二轮动态占地

A合法路线：

`[20,9]→[19,9]→[18,9]→[17,9]→[16,9]→[15,9]→[14,9]→[14,10]→[15,10]→[16,10]→[17,10]`

B合法路线：

`[19,9]→[18,9]→[17,9]→[16,9]→[15,9]→[14,9]→[14,10]→[15,10]→[16,10]→[17,10]`

route planner的`can_place / path_between / legal_anchors / route_is_placeable`统一消费上一轮活体`blocks_route=true`实体的anchor与footprint。preview与execute调用同一resolver；A穿入`[20,10]`、B穿入`[20,9]`的反例均在两条路径上返回`dynamic_entity_footprint_overlap`及实际重叠格。

## 计算闭环

A：

- 动态占地下由路径搜索得到`efficient_steps=10`；
- 长裂`[19,9] / [18,9] / [17,9]`逐格计费，`timing_cost=3 / heat_cost=6`；
- `heat = 24 + 10×2 + 18 + 6 = 68`；
- `margin = 4 - (10-10) - 3 = 1`。

B：

- 动态占地下由路径搜索得到`efficient_steps=9`；
- 一格小体压力`[18,9]`计费，`timing_cost=1 / heat_cost=6`；
- `heat = 46 + 9×2 + 18 + 6 = 88`；
- `margin = 1 - (9-9) - 1 = 0`。

两路均验证`exact_route_valid=true`、`dynamic_conflicts=[]`、`target_metrics_valid=true`。这些数值来自同一resolver公式和world回读，不是手填结果。

## T4几何

side-armor窗口由post-contact BREAKER矩形派生：`east_socket = [anchor.x + footprint.x, anchor.y + footprint.y/2]`。resolver同时检查post facing为north、炮源`[29,2]`位于socket东侧、炮线非零且socket匹配策略合同，才设置`side_armor_exposed=true`。路裂、接触flash/debris与red charge继续复用T3 impact socket。

