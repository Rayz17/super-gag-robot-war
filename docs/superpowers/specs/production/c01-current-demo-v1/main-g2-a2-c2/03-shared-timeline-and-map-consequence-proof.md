# G2-A2-C2 共同时间线与地图内因果证明

## 同一时间线

预演侧从Resolver preview event log按出现顺序构造`event_sequence:[[event_id,timeslice], ...]`；执行侧另行遍历PerformanceDirector实际`active_plan` descriptors构造同形有序投影。两侧不复用adapter自报token，也不使用会按`event_id`稳定重排的对象数组。外部validator从raw payload分别重算并证明：

| 策略 | preview / execute重算token | 相邻事件交换负例token | 负例不同 |
|---|---|---|---|
| A | `f2c371076ce470393f8bff389b6317191053963c5920e0bd8ad8d081cbd44e6e` | `239d9d4a27b7cd5f77ca1e7bbf70b2e2ae743ea3db2d4868740e8547f57f3cc4` | 是 |
| B | `36d1216bc2176377b9929d87d518a7d81ec0a8e9c41cb81a807d17e841dbb2aa` | `a2596d6fe9a122fad3ee4b47d12516fff8931abc7b7ca779cf87552b7049c5c2` | 是 |

两路preview/execute各自重算token相等，而交换任意相邻事件后token必变，因而同时证明“同一顺序”与“顺序敏感”。PerformanceDirector仅扩展表现时长，不改逻辑timeslice；合同Full总表现时长为13,320ms，Skip为0ms，两者语义结果相等。实际A/B连续执行窗分别为13,334.692ms / 13,322.257ms。

| 时点 | 地图内表现 | 公开逻辑 |
|---|---|---|
| T1 | 应急车穿过落脚区 | `GS-R1-E1-VEHICLE` |
| T2 | 馆守Z自主挡开小体 | `GS-R1-E2-SWARM` |
| T3.00 / T3.25 | A两格正面承力；B先护撤离线、转身、一格错位承力与热排出 | `GS-R1-E3-CONTACT` |
| T4 | 城市炮侧甲命中 | `GS-R1-E4-CITY-GUN` |
| T5 | A路损42+设施受损；B路损24+设施保全；机体热与赤红蓄能 | `GS-R1-E5-ROAD-RED` |

T1–T5的首次出现均在commit之后，顺序严格递增；轮末仅推进一次。A/B map marks取自`session.resolved.world_result + PerformanceDirector.current_frame`，不靠独立数字结果表驱动。

## 城市炮 fail-closed 语义

`ALLY_C01_CITY_ARTILLERY.physical_shot_allowed`的缺省值已从`true`改为`false`。唯一开启条件是当前公开PerformanceDirector帧同时满足：

1. `event_id=GS-R1-E4-CITY-GUN`；
2. 处于T4明确物理表现phase；
3. 当前FX显式包含`artillery_beam`且`alpha>0`。

外部validator从原始gate trace重算：PUBLIC / EDIT / COMMIT_SUMMARY、A:T3.00、B:T3.25全为false；T4 anticipation仍false，A/B首次true都只在T4 motion；非T4事件及T5均false。15张交付actual frames均不位于T4物理炮击帧，全部`physical_shot_allowed=false`，且无`city_artillery_side_armor_hit`物理mark。逻辑真值`fired_hit_side_armor`仍保留，只是不再提前驱动屏幕实体炮击。

证据：[timeline-semantic-nonregression.json](receipts/timeline-semantic-nonregression.json)、[raw-screen-trace-validation.json](receipts/raw-screen-trace-validation.json)、[actual-input-frame-manifest.json](receipts/actual-input-frame-manifest.json)。
