# C01E04 Runtime / Graybox 确定性纸演 r2

> Checker: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_c01e04_runtime_graybox.py`
>
> Scope: 修复`RT039/GB029`城区入口双臂态、三Bundle热量/冷却预算与可选转体可达性。

## 1. 唯一城市入口真相

P4结束时，两侧锁泊臂保持展开，完成半身承重。七海的东锁延迟获批后，进入城区玩家回合前播放一次可见的`CORRIDOR_FOLD`：两臂同步收回道路姿态，热量`+1`；若携带档案服务器，冷却`-1`。这是一段有成本的阶段转换，不占P5玩家回合。

`CITY_LOCAL`在转换后建立，固定为：

- `body=CITY_START_HALF_RISE`
- `arms=BOTH_RETRACTED`
- `heat=POST_CORRIDOR_FOLD_CAPTURED`
- `archive=POST_CORRIDOR_FOLD_IF_ACTIVE_ELSE_N/A`
- `city_turn=0`

城市失败回滚到这份转换后的快照，不重复支付收臂成本，也不复制七海回执。

若收臂本身令`body_heat>=8`或活动档案冷却归零，则`CITY_LOCAL`尚未建立，直接回滚`HALF_RISE_LOCAL`；不存在卡在两个检查点之间的状态。

## 2. 三Bundle黄金路线

共同路线为三次玩家身体动作：`CITY_START -> EAST_1 -> EAST_2 -> EAST_GATE`。P4有三次必做身体动作；档案分支在P4使用一次机器犬档案冷却，生活分支在P4使用一次全局降热。`LIFE_ARCHIVE`的两项机器犬动作分布在不同P4回合。

| Bundle | P4支援后 | 道路收臂 | 三次东移后 | 结果 |
|---|---|---|---|---|
| `LIFE_PHYSICAL` | heat0 / structure3 | heat1 | heat3 / structure3 | PASS |
| `LIFE_ARCHIVE` | heat0 / archive5 | heat1 / archive4 | heat3 / archive1 / structure3 | PASS |
| `PHYSICAL_ARCHIVE` | heat3 / archive5 | heat4 / archive4 | heat7 / archive1 / structure3 | PASS |

三路均满足`body_heat<8`、`structure>0`；档案路均满足`archive_cooling>0`。实体缓冲仍以一次敌方关键冲击作为独立消费者，不能把非法占格变合法。

## 3. 可选转体不是假按钮

五回合路线为：

`CITY_START -> EAST_1 -> EAST_1_ROT -> EAST_1 -> EAST_2 -> EAST_GATE`

- `LIFE_PHYSICAL`在P4降热后，收臂与五次P5动作结束为`heat5`，合法。
- `LIFE_ARCHIVE`在P4分别完成生活降热与档案冷却，进入P5后于首动作结算后使用本阶段档案冷却，五次动作结束为`heat5 / archive1`，合法。
- `PHYSICAL_ARCHIVE`没有生活降热，五动作转体路线会过热；UI应按已选Bundle把它显示为高热不可完成方案，而不是允许运行到确定性误败。

一侧锁泊臂的展开/收回也可形成同样的两动作防守循环：展开回合遮住对应侧一次活动标记，收回后继续东移。所有基础移动都要求双臂已收回。

## 4. 结论

`RT039`、`GB009/021/028/029/033`、资产状态和检查器现在共享同一入口状态与费用口径。上一版r1只计三次东移、漏算两次收臂，已历史化；r2把收臂压成一次公开同步转换并完整计入三Bundle预算。
