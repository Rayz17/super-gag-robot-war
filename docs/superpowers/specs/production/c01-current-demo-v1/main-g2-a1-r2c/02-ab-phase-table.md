# STAGGERED_FRONT_CONTACT_V1 A/B阶段表

两路共同消费冻结公开意图：BREAKER从`[20,13] → [20,12] → [20,11]`向north冲锋；接触时馆守Z为south、BREAKER为north；共同接触法线`[0,1]`，共同approach／impulse`[0,-1]`。

| 阶段 | A｜BODY_INTERCEPT | B｜PROTECT_LANE_RESPONSE |
|---|---|---|
| 规划路线 | `[15,11]→[16,11]→[17,11]→[18,11]→[18,10]→[19,10]→[19,9]→[20,9]` | `[15,11]→[15,10]→[16,10]→[17,10]→[18,10]→[19,10]→[19,9]` |
| planning endpoint | `[20,9]` | `[19,9]` |
| T2 settle facing | `south`，已正面架住 | `east`，先执行护线侧推 |
| contact interaction-facing | `south` | 在`T3.25`显式转`south`，不覆盖T2玩家所见east |
| contact timeslice | `T3.00` | `T3.25` |
| 接触边 | guardian south → BREAKER north，全2格 | guardian south → BREAKER north，横向错1格、共享1格 |
| impact socket | `[20.5,10.5]` | `[20,10.5]` |
| 矩形闭合 | 相邻、不重叠、不隔空 | 相邻、不重叠、不隔空 |
| visual recoil | `[20,8.5]` | `[19,8.5]` |
| 下一轮Guardian离散anchor | `[20,9]` | `[19,9]`，明确不是`[19,8]` |
| post-contact BREAKER | `[21,11] / north` | `[21,10] / north` |
| T4 east side-armor socket | `[24,12.5]` | `[24,11.5]` |
| 炮源 | `[29,2]` | `[29,2]` |
| R1热量／余量 | `24 / 4` | `46 / 1` |
| R2目标结果 | `68 / 1` | `88 / 0` |

## 阶段字段

resolver与回执不再用单一`endpoint/final_facing`冒充全过程，现显式保存：

- `guardian_planning_endpoint`
- `guardian_settle_facing`
- `guardian_contact_anchor`
- `guardian_contact_facing`
- `guardian_visual_recoil_anchor`
- `guardian_post_contact_anchor`
- `breaker_contact_anchor`
- `breaker_post_contact_anchor`
- `breaker_post_contact_facing`
- `impact_socket_grid`
- `side_armor_socket_grid`
- `artillery_line`

T1车辆路线与馆守Z路线存在共享通道格，但事件回执固定`T1 vehicle_crosses → T2 guardian_staging → T2 swarm_deflects → T3 contact`，因此没有同时占位或时序穿插。

本表是Candidate R2C实现回读，不是制作人画面签收。
