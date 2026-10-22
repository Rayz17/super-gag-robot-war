# C01E03 Runtime / Graybox 纸演 r2

> Status: `local_paper_run_r2_pending_independent_gameplay_recheck`
>
> Scope: 双层区域级Graybox、选择消费者、失败回路与原子快照；不代替引擎实装
>
> Inputs: `C01E03-断臂成桥-v1.md` / `C01E03-runtime-contract-v1.tsv` / `C01E03-graybox-constants-v1.tsv` / `C01E03-asset-state-matrix-v1.tsv`
>
> Supersedes for current review: r1只保留为首轮历史证据

## 1. 本轮修复目标

r1证明了人口、双层拓扑和“断臂成桥”的基础可行性，但没有证明四件制作级问题：失败点能否真的回到有后继的检查点、两项战术选择是否被后续动作消费、桥面是否能按离散步数完整走完，以及结算是否为可机器比对的精确集合。r2只处理这些根因，不改写本话故事高潮。

## 2. 开局与几何硬断言

- 开局继承人口恒为L2五人：纪存、唐胶、兜灯、消防接驳员A、消防接驳员B。
- 豪司在`RT007`从西门进入L1勇拳锚位，现场峰值为六；他从不进入L2，也不成为第六名过桥者。
- 楼外二十九人和消防架桥机操作员没有战场格，不参与人口增减。
- 白函第一脚在`RT003`关闭`OLD_STAIR`，建立真实`SETUP_LOCAL`。此后唯一L2到L1边是切臂后开放的三段桥，且只允许单向通过。
- 次梁连续足迹为`L1(4..12,9)`；勇拳从`L1(3,9)`最多移动一格接触`L1(4,9)`，SEG3固定接触`L1(12,9)`。两个接触点都在同一连续梁上，交接过程不存在跨空支撑。
- 右臂复合桥使用5.0m前臂、1.4m滑架和双索，跨4.2m水平净距与0.9m标高差；L2、L1两端搭接均不少于0.8m。

## 3. 五次结构钟与两个支援分支

### 3.1 固定结算点

| Tick | 剧情/玩法出口 | 基础热量 | 基础位移 | 结算后允许进入 |
|---|---|---:|---:|---|
| T1 | 馆守Z抬肩12度 | +2 | +1 | 七海电话、豪司入场 |
| T2 | 勇拳固定承梁，豪司身后西路闭合 | +1 | +1 | 通道选择 |
| T3 | 标尺机对所选通道作出可见反应 | +1 | +0 | 私有整肩预览与公开复核 |
| T4 | `ARM_ON_CRADLE`，载荷交接完成 | +1 | +1 | 右臂滑轨冲击 |
| T5 | 右臂撞框，白函锁住回收轨 | +2 | +2 | 路线补位动作、探索入口 |

基础合计为`heat=7 / displacement=5`。结构钟只在以上五个出口增加；对白、Cut-in、检查点和危险预览不暗扣Tick。T5之后若不做路线补位，或者任何动作把钟推进T6，直接进入`RT037 -> SETUP_LOCAL -> RT004`。

### 3.2 跌跌垫片优先

1. `RT004`锁定`DIEDIE_PAD_ROUTE`。
2. T2、T4各抵消1位移，T5结束得到`heat=7 / displacement=3`。
3. 热量警报要求原本未获优先的兜灯执行`RT040`肩部冷却液泄放，消耗1动作，得到`heat=6 / displacement=3`。
4. 只有`RT040`完成，状态才从`SUPPORT_ROUTE_RESPONSE_REQUIRED`进入`SUPPORT_ROUTE_STABILIZED`，继而允许建立探索检查点。

### 3.3 机器犬软管优先

1. `RT004`锁定`DOG_HOSE_ROUTE`。
2. T1、T5各抵消2热量，T5结束得到`heat=3 / displacement=5`。
3. 位移警报要求原本未获优先的跌跌执行`RT041`重新压实底垫，消耗1动作，得到`heat=3 / displacement=4`。
4. 只有`RT041`完成，才可进入探索检查点。

两条路线不是警告颜色差异：优先对象、T1-T5遥测、T5后的补位角色、动作Clip和对白回报均不同；最终固定伤痕相同。

## 4. 两个通道分支的可见消费者

### 4.1 上层设备通道

1. `RT009`选择`UPPER_EQUIPMENT_ROUTE`并结算T3。
2. `RT042`让白函标尺机瞄准`CARGO_ENTRY_CLAMP`；唐胶用材料工具拨开标尺。
3. `CARGO_PUMP`因此提前放到桥口，第一组“设备+接驳员A”成本由6降为5。
4. 本路线没有人员失足恢复；唐胶若在臂中踏错，进入切后失败而不是免费纠正。

### 4.2 下层人员缓冲位

1. `RT009`选择`LOWER_PERSON_ROUTE`并结算T3。
2. `RT043`让标尺机瞄准`PERSON_BUFFER_EDGE`；跌跌顶住缓冲边缘。
3. `CARGO_PUMP`没有提前放置，第一组“设备+接驳员A”成本为6。
4. 本路线获得一次明确恢复：唐胶可在`RT045`从`ARM_MID`滑回`L2_OVERLAP`，再经`RT046-047`重新进入臂中并安全退出。恢复只可使用一次，增加2 Tick。

两条路线在`LANE_BRANCH_RESOLVED`汇合，但敌方目标、响应角色、设备起始位置、桥面成本和一次性恢复规则都已被消费。

## 5. 支撑交接与飞拳

交接必须依次满足：

1. `RT012`: SEG3保持反折托梁，四足零位移，Owner=`SEG3`。
2. `RT013`: 勇拳接触并预载，Owner=`SEG3+BRAVE_FIST`。
3. `RT014`: `BRAVE_FIST_BEAM_CLAIMED=TRUE`，Owner=`BRAVE_FIST`。
4. `RT015`: SEG3绕固定关节转成托槽，Owner仍为`BRAVE_FIST`。
5. `RT016`: 右臂落入托槽并结算T4，尚未飞出。
6. `RT017`: 馆守Z只执行一次滑轨冲击并结算T5；白函锁轨，右臂进入`ARM_SUSPENDED_RECOVERABLE`。

任何前置Owner不成立，指令不可确认；若测试构建强制制造无Owner帧，则`RT037`回到`SETUP_LOCAL`。勇拳接触点与SEG3接触点均落在`GB031`同一梁足迹内。

## 6. 探索输入：有效、缺项与强制错误

### 6.1 有效路线

1. `RT019`建立`EXPLORE_ENTRY_LOCAL`。
2. `RT020`依次排除上方空腔、外甲梁、热脆第三筋，耗3个搜索Tick。
3. `RT021`的低置信身体记忆只给隐藏隔板位置，耗时0，不授予通行权。
4. 第四Tick前必须同时满足：唐胶敲击=`SHORT_SHORT_LONG`、勇拳载荷=`LOAD_CENTER`、跌跌垫片=`GREEN`。
5. 三项`READY`后，`RT022`耗第4 Tick生成`FOURTH_RIB_VERIFIED=TRUE`，进入`PRECUT_LOCAL`。

### 6.2 缺项预览

任一输入为`NOT_READY`时，界面点名缺项但成本为0，玩家可修正后再次验证。不存在因“查看失败原因”而暗耗最后一格的软锁。

### 6.3 强制错误

测试构建强制以任一`NOT_READY`输入结算，会消耗第4 Tick并进入`RT038`。回滚结果必须是`EXPLORE_ENTRY_LOCAL`、右臂悬置可修、外部姿态恢复、搜索钟归零，然后可从`RT020`重新走到成功，不写任何结算键。

## 7. 三种完整桥面预算

所有人和设备都按`L2_OVERLAP -> ARM_MID -> L1_SLIDER_OVERLAP -> CLEAR`留下回执。设备令牌占用整桥，第二枚设备不得与第一枚重叠。

| 路线 | 唐胶 | 泵+接驳员A |消防设备+接驳员B | 兜灯 | 纪存 | 合计/上限 |
|---|---:|---:|---:|---:|---:|---:|
| `UPPER_NORMAL` 上层设备，正常 | 3 | 5 | 6 | 3 | 3 | 20/23 |
| `LOWER_NORMAL` 下层人员，正常 | 3 | 6 | 6 | 3 | 3 | 21/23 |
| `LOWER_WITH_ONE_RECOVERY` 下层人员，触发一次恢复 | 5 | 6 | 6 | 3 | 3 | 23/23 |

唐胶正常路径为`RT026 -> RT044`，共3 Tick；恢复路径为`RT026 -> RT045 -> RT046 -> RT047`，共5 Tick。其后`RT027-030`依次完成两枚设备/两名接驳员、兜灯和纪存。豪司始终在L1勇拳锚位，馆守Z左臂在桥开放前已锁定，过桥期间只等长承力。

## 8. 三类失败回路必须能重新成功

### 8.1 切前结构/Owner失败

`RT037 -> SETUP_LOCAL -> RT004`。回滚恢复五人L2、豪司未入场、右臂连接、白函开场切区本地态；重新选择支援后存在一条通往`RT035`的合法路径。

### 8.2 探索超时/强制错误

`RT038 -> EXPLORE_ENTRY_LOCAL -> RT020`。回滚恢复右臂悬置可修、外部姿态与搜索钟；重新输入三项`READY`后存在一条通往`RT035`的合法路径。

### 8.3 切后超载/人员截断/支撑丢失

`RT039 -> POSTCUT_LOCAL -> RT026`。回滚保留本局已切右臂的戏剧前提，但先关闭再重开桥面，馆守Z左臂恢复为已锁定挡梁，五人和两设备回到L2，桥为空；重新执行任一20/21/23 Tick序列后存在一条通往`RT035`的合法路径。

三条失败路径都没有结算键，也没有无后继终点。

## 9. 精确27键原子提交

只有`RT035`可写以下集合，且必须一次同时写入：

```text
GZ_RIGHT_ARM_LOST=TRUE
GZ_CONTROL_STATE=FIRST_CONTROL_COMPLETE_SINGLE_ARM
GZ_RIGHT_ARM_LOCATION=OLD_SITE_L1_L2_COMPOSITE_BRIDGE
GZ_RIGHT_ARM_CARGO=FORBIDDEN
HAOSI_CORP_PUNISHMENT=ACTIVE
BRAVE_FIST_RECOVERY=CORPORATE_COMPLETE
BRAVE_FIST_DATA=STRIPPED
BRAVE_FIST_PROTOTYPE=RECOVERED_BY_CORPORATE
JICUN_MEMORY_FRAGMENT_00=ACQUIRED_LOW_CONFIDENCE
INDEX_DAMAGE_AS_FUNCTION_SAMPLE=ACQUIRED_BY_BAIHAN_SINGLE_LOCAL_SAMPLE
BAIHAN_RIGHT_SHOULDER=CRACKED
BAIHAN_INNER_RETRACTOR=SEVERED
E03_INHERITED_INSIDE_HUMANS=5
HAOSI_POST_SNAPSHOT_ENTRY=1
PEAK_ONSITE_HUMANS=6
BRIDGE_EVAC_HUMANS=5
FIVE_INSIDE_HUMANS=SAFE
HAOSI_SAFE_EXIT=TRUE
PEOPLE_CARGO=FORBIDDEN
B1_MOVING_SPINE=PHYSICALLY_LOCKED_BY_MILITARY
E03_ATOMIC_COMMIT=COMPLETE_AFTER_SIX_ANCHORS
C01_OUTSIDE_EVACUEES=29
E03_FIRE_HANDOFF_CARGO=2_SAFE
FIRE_SUPPLY_BURNED=TRUE
COMMERCIAL_DUCT_DAMAGE=LOCAL_BURNED_HEAT_LEAK
ARCHIVE_MAIN_VAULT_COOLING=EMERGENCY_LOW_PRESSURE_ACTIVE
FIRE_BRIDGE_LEFT_FRONT_LEG=OVERLOAD_PERSISTENT
```

`RT035`结束态和`RT036`开始态必须同为`C01E03_ATOMIC_TRANSACTION_COMMITTED`。`RT036`只读，要求Episode结算区与Runtime集合精确相等：无缺项、无额外项、无同键冲突值。

## 10. 资产与表现覆盖

- 唯一完整新Boss身体仍为白函；馆守Z、勇拳、SEG3只做有限状态/Clip。
- 馆守Z右臂保留五种碰撞状态：连接、托槽、悬置可修、复合桥、旧址永久桥。
- 两个标尺机目标态分别覆盖设备夹具和人员缓冲边缘。
- 低压泵、消防设备均有weight2桥面Token与三段回执。
- 五名过桥者复用角色Token和脚步Clip，另补一段下层路线失足/退回Clip。
- 桥面HUD显示三段占用、整桥设备预留和一次性恢复，不制作新的全屏菜单。

## 11. 本地主控结论

r2已把首轮Gameplay复核指出的七类问题落实为状态、几何、输入、消费者、预算、资产和提交集合。该结论只表示编剧/制作主控认为文件已具备复验条件；必须由原Gameplay独立席重新运行和审查后，才能把本话生产状态改为PASS。
