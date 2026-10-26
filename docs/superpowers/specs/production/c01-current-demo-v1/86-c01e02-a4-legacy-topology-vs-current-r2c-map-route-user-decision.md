# C01E02 旧A4拓扑 vs 当前R2C地图路线用户裁决

日期：2026-08-20  
任务ID：`U86_A4_LEGACY_VS_CURRENT_R2C_MAP_ROUTE_DECISION`  
状态：`USER_APPROVED_ROUTE_A_2026_08_20`  
权限：重大地图视觉／玩法空间路线裁决；批准只开放P87玩法对齐与联合注册前置，不直接开放美术生成或G2-A2 Scene

## 裁决结果

用户已批准：

> 保留R2C互动骨架，按当前玩法空间重做精品地图。不过请认真核对主策划session已经给出的玩法设计，尽可能做得好玩一些

正式回执见`87-c01e02-u86-route-a-user-approval-and-gameplay-alignment-reopen-receipt.md`。以下A／B内容保留为决策依据；生产现按A执行。

## 用户只需决定一件事

### A. 保留当前R2C玩法空间，重派生current-topology地图（制作人推荐）

保留已经闭合的：

- A/B第一轮规划、接触、post结果；
- Swarm01 `[22,9]`地面互斥；
- A/B第二轮动态占位、热量与余量；
- T1–T5、socket、音频与连续Session底座。

A4保留为用户批准的视觉／材质／建筑分层方法和遮挡donor，不再冒充当前exact世界。新Candidate地图派生必须按当前G2 terrain、对象与相机重建：

- 当前main road、protection/rescue zone与block拓扑；
- 盾`[14,10]`、出口`[31,7]`、警戒设施`[27,8]`；
- 应急车、三只小体、炮源及全部当前互动点；
- correct canvas origin `[-1760,-340]`与动态camera/crop；
- 与单位footpoint、遮挡mask、路线和socket做0px联合控制点验证。

代价：当前ImageGen Call01降History／质感donor；需要重做PLAN/CONTACT guide与current-topology整屏地图目标。剩余生成预算仍为`3/4`。

收益：保住当前已验证玩法，最终画面可以真正达到“同一世界、同一视角、同一交互”的精品标准，也最接近用户给出的目标截图。

### B. 保留旧A4世界拓扑，重开R2C玩法几何

以旧A4为exact地图：旧main road/rescue lane/block、盾`[11,10]`、出口`[31,4]`、警戒设施`[25,5]`等重新成为空间责任源；重新安排车辆、小体、BREAKER、馆守Z、A/B路线、接触与第二轮。

代价：80–84关于当前路线、对象位置、A/B后果与第二轮的签收大面积作废；resolver、performance、tests与视觉目标都要重做。

收益：可以原字节保留旧A4地图拓扑，但它的视觉完成度仍低于本次精品Demo目标，后续仍需美术升级。

## 制作人不接受的第三条路

不允许“先把当前单位marker叠在旧A4上，地图以后再修”。这会在同一屏出现两套盾位、出口、警戒设施、救援线与遮挡语义，正是本轮要消灭的问题。

## 建议回复

```text
批准A：保留当前R2C玩法空间，重派生current-topology地图。
```

或：

```text
选择B：保留旧A4拓扑，重开R2C几何。
```
