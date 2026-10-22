# C01E04 Runtime / Graybox 确定性纸演 r1

> Status: `superseded_by_r2_after_city_entry_arm_budget_counterexample`

> Checker: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_c01e04_runtime_graybox.py`
>
> Result: `PASS`
>
> Runtime: `RT001..RT057`

## 1. 输入与唯一时序

- `RT001`逐项读取E03 `RT035`精确27键；人员、右臂、勇拳、白函和设施伤痕无重置。
- 主链不可交换：`RT017六锚全解 -> RT020-028载荷物理提交 -> RT029向东提前位移 -> RT032半身检查点 -> RT038半身完成 -> RT039城市检查点 -> RT045东门完成 -> RT047受损巡航 -> RT048余波 -> RT054原子提交`。
- `RT054`是唯一含`COMMIT_SINGLE_TRANSACTION_C01E04`的行；此前所有新跨话状态均为`LOCAL_STAGED_UNTIL_RT054`。

## 2. 三种载荷组合

纸演共同前提：P4三次身体动作、P5代表路线三次东移；初始`body_heat=0 / structure=3`。档案分支每次身体动作消耗1冷却，P4结束使用一次机器犬档案冷却`+2`。

| 组合 | P4结束 | 分支消费 | P5结束 | 结果 |
|---|---|---|---|---|
| LIFE_PHYSICAL | heat3 / structure3 | 生活全局降热一次：3->0；P5首动作热成本0；实体缓冲吸收一次关键冲击的heat2/structure1 | heat2 / structure3 / archive=N/A | PASS |
| LIFE_ARCHIVE | heat3 / archive3 | 档案冷却3->5；生活降热3->0；P5首动作热成本0 | heat2 / archive2 / structure3 | PASS |
| PHYSICAL_ARCHIVE | heat3 / archive3 | 档案冷却3->5；实体缓冲吸收一次关键冲击 | heat6 / archive2 / structure3 | PASS |

三路均满足`body_heat<8 / structure>0`；档案冷却只在档案分支检查且均`>0`。实体缓冲从不允许非法Mask，生活降热和档案冷却都必须消耗地图支援动作。

## 3. 城市Mask

代表路线只有三条推进边：

`CITY_START --MOVE_EAST--> EAST_1 --MOVE_EAST--> EAST_2 --MOVE_EAST(right arm retracted)--> EAST_GATE`

唯一可选转体为：

`EAST_1 --ROTATE_HALF(both arms retracted)--> EAST_1_ROT --ROTATE_HALF--> EAST_1`

转体态不能直接东移；`EAST_GATE`右锁臂必须收回。所有基础Mask和左右锁臂Overlay均在GB028列出，西侧捷径、医院、两管线和应急区继续是硬禁区。

## 4. 四类失败恢复

| 失败 | 回点 | 全量恢复 |
|---|---|---|
| RT049锚点失败 | ANCHOR_LOCAL | 固定馆体、六锚、初始双方位置、writer、Owner、火锁、热量、结构、无分支资源 |
| RT050载荷失败 | LOADOUT_LOCAL | 固定馆体、载荷内轨/旧址、P1末敌机态、组合、空分支旗与未初始化资源 |
| RT051半身失败 | HALF_RISE_LOCAL | 提前位移态、已清卡锁臂、P4双方位置、分支资源基线；皇影不重复播放 |
| RT052城市失败 | CITY_LOCAL | 半身城市起点、双方位置、writer、资源剩余、火锁、三类城市伤害和一次性七海窗口 |

四路均有真实重入行，清除目标模式/Owner行动标记，不复制七海签名、皇影Cut-in或任何永久输出。

## 5. 原子输出

- 三个Bundle各有两项`CARRIED_OPERATIONAL`、一项`OLD_SITE_PUBLIC_UNCARRIED`。
- `ARCHIVE_PRIORITY_COLD_BACKUP`按`ARCHIVE_BACKUP_MAP`解析：只有`LIFE_PHYSICAL`为`COMPLETE_AT_OLD_SITE`，档案随舰的两路为`NOT_APPLICABLE_CARRIED`。
- `RT055`同时断言26个E03动态值不变、B1旧值转存、当前值有意迁移、四操作员随舰、零疏散人员载荷、七海不在现场、皇影不可控。

当前纸演没有发现合法路线软锁、无条件冷却误败、失败后状态漂移、人员回装或半套持久化。
