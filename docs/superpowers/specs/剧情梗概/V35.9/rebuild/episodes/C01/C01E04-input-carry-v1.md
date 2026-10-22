# C01E04 Input Carry v1

> Status: `locked_input_from_C01E03_RT035`
>
> Upstream transaction: `C01E03:RT035:ATOMIC_SNAPSHOT:V01`
>
> Target episode: `C01E04 / 万机馆站起来`

## 1. 唯一动态状态入口

C01E04只允许读取C01E03 `RT035`一次提交的精确27键作为动态状态输入。不得从E02快照、旧章节摘要、V31台本或运行时残留拼接前态；缺键、多键、值冲突均不得进入E04。

除这27键外，运行时还必须读取硬正典规则`CANON-RULE-004`：七海在第一章只可远程、停权、只读和公开申诉，不可现场上舰或获得系统写权限。该规则是不可变运行约束，不是第28个动态状态键，不得写入或改造RT035。

| key | required value |
|---|---|
| `GZ_RIGHT_ARM_LOST` | `TRUE` |
| `GZ_CONTROL_STATE` | `FIRST_CONTROL_COMPLETE_SINGLE_ARM` |
| `GZ_RIGHT_ARM_LOCATION` | `OLD_SITE_L1_L2_COMPOSITE_BRIDGE` |
| `GZ_RIGHT_ARM_CARGO` | `FORBIDDEN` |
| `HAOSI_CORP_PUNISHMENT` | `ACTIVE` |
| `BRAVE_FIST_RECOVERY` | `CORPORATE_COMPLETE` |
| `BRAVE_FIST_DATA` | `STRIPPED` |
| `BRAVE_FIST_PROTOTYPE` | `RECOVERED_BY_CORPORATE` |
| `JICUN_MEMORY_FRAGMENT_00` | `ACQUIRED_LOW_CONFIDENCE` |
| `INDEX_DAMAGE_AS_FUNCTION_SAMPLE` | `ACQUIRED_BY_BAIHAN_SINGLE_LOCAL_SAMPLE` |
| `BAIHAN_RIGHT_SHOULDER` | `CRACKED` |
| `BAIHAN_INNER_RETRACTOR` | `SEVERED` |
| `E03_INHERITED_INSIDE_HUMANS` | `5` |
| `HAOSI_POST_SNAPSHOT_ENTRY` | `1` |
| `PEAK_ONSITE_HUMANS` | `6` |
| `BRIDGE_EVAC_HUMANS` | `5` |
| `FIVE_INSIDE_HUMANS` | `SAFE` |
| `HAOSI_SAFE_EXIT` | `TRUE` |
| `PEOPLE_CARGO` | `FORBIDDEN` |
| `B1_MOVING_SPINE` | `PHYSICALLY_LOCKED_BY_MILITARY` |
| `E03_ATOMIC_COMMIT` | `COMPLETE_AFTER_SIX_ANCHORS` |
| `C01_OUTSIDE_EVACUEES` | `29` |
| `E03_FIRE_HANDOFF_CARGO` | `2_SAFE` |
| `FIRE_SUPPLY_BURNED` | `TRUE` |
| `COMMERCIAL_DUCT_DAMAGE` | `LOCAL_BURNED_HEAT_LEAK` |
| `ARCHIVE_MAIN_VAULT_COOLING` | `EMERGENCY_LOW_PRESSURE_ACTIVE` |
| `FIRE_BRIDGE_LEFT_FRONT_LEG` | `OVERLOAD_PERSISTENT` |

## 2. 人口与载荷前态

- E04开场时，二十九名观众、E03继承五人和后入豪司全部在楼外安全区；E04不得再次生成受困者、救援倒计时或隐藏B1维修人员。
- 六锚评估后，消防队长只允许纪存、兜灯、唐胶、陆衡四名必要操作员实名有限返入四个保护岗位。四人佩戴定位器、经西侧维修隧道进入B1并随舰离开；他们是`REGISTERED_OPERATOR_CREW`，不是疏散人员、受困人员、地图步兵或载荷。
- 观众、豪司、两名消防接驳员和其他现场人员始终留在封锁线外；E04期末必须同时满足`E04_OPERATOR_CREW_COUNT=4_ONBOARD_PROTECTED_POSTS`与`E04_EVACUEE_PAYLOAD_COUNT=0`。
- 两件消防接驳货物已经安全交还城市消防线，不属于万机馆载荷。
- 人员永远不得出现在E04三选二枚举中。有效载荷仅为`life_support_equipment`、`unique_physical_collection`、`archive_server`。
- 豪司本人可在安全区余波中出现，但勇拳已经被企业回收，不能进入B1、战斗单位表或WBM001泊位。

## 3. 机体与设施前态

- 馆守Z为18米级、永久单臂、首控已完成；右肩缺口封闭，右臂留在旧馆L1/L2复合桥且禁止装载。
- 白函已经撤离且保留右肩开裂、内收索断裂；E04不得为了增加敌人再让完整白函无伤回场。
- B1移动脊柱已被六枚军方锚物理锁死；E04从解除实体锁开始，不能把它写成一个软件授权按钮。原值必须作为历史回执保存为`B1_MOVING_SPINE_PREVIOUS=PHYSICALLY_LOCKED_BY_MILITARY`，成功起航后当前值有意迁移为`B1_MOVING_SPINE=RELEASED_LOW_SPEED_CRUISE_AFTER_SIX_ANCHORS`。
- 供水热损、商业风道漏热、档案紧急冷却和消防架桥机左前腿过载都继续存在；起航不能战后自动修复。
- 万机馆开场仍是固定建筑。固定建筑、半身抬升和巡航展舰三态必须在本话内依次出现。

## 4. 人物与权限前态

- 纪存已取得低置信身体记忆片段，但不知道来源；E04新记忆只能补一段供电/开灯动作感，不能给出完整路线或身份答案。
- 七海仍被停权且第一章不得本人到场；她只能使用普通语音、官方风险频道、只读回执和公开申诉。该边界来自`CANON-RULE-004`，不扩充27键输入。
- 唐胶与兜灯已经共同完成仍可修主筋的主动切离；E04关系推进应通过永久展轨、缺臂承重和共享工具继续，不回到互相不认识的吐槽状态。
- 陆衡在E03馆体位移后已被城市传感器调到相邻街区待命，E04六锚同时入土使工单在23:17升级为现场响应；他凭派单时间戳、工程证和消防领入回执正式首登。他只承担工程损伤评估、城市承压和载荷包络，不抢C03现实机魂主线；第一版固定建筑模型必须被跌跌的失败振动证伪并由他公开修订。
- 旧守护者继续以导览流程、馆内小机调度和广播照顾人，不变成万能舰载AI。

## 5. 本话必须新增

1. 六锚与待拆固定风险状态可见化。
2. 陆衡有来源地到场并把签名写入当前移动包络。
3. 零号旧路先成功回收三枚活动机魂核心，再当场把跌跌重分类为高速运输设备、灰掉兜灯与旧守护者的停机权，并要求纪存永久绑定为单一管理员；低速载人壳空白栏只作历史阴影。纪存实测硬停失效后拔除桥接片，恢复分布式停机权并关闭路线。
4. 全员安全后精确完成三类非人员载荷二选三，第三类进入公开未带走清单。
5. 七海面对城市/军方值守席，把公开民用紧急运输申诉收窄为四名登记操作员、零名疏散人员载荷、恰好两类非人员载荷、东行低速且避开医院电网；产生东侧消防锁延迟、停职延长和个人审查记录。
6. 玩家通过固定建筑、半身抬升、巡航态三阶段让万机馆脱离旧址。
7. 馆守Z先于命令主动露出左肩支撑点，再在兜灯硬停权保留下完成单臂胸前承重，并锁为后续常驻支援。
8. 皇影首次可见，黑框卡死右侧锁泊臂并加剧失衡；旧拘束只阻止扩张。它无控制、无战斗、无解释，也不得替玩家纠错。
9. 旧址、公共身份、第三类载荷和具体城市责任永久失去；三十六小时锁定木桶旧件市。

## 6. 不得提前或回退

- 不得让馆长远程驾驶万机馆，不得把纪存写成唯一万能舰长，不得在C01正式启动自由G.A.G.暴走。
- 不得打开零号侧廊、解释旧灾变、确认纪存身份、确认皇影主人关系或建立稳定远星通信。
- 不得恢复馆守Z右臂、勇拳、消防供水、商业风道、档案完整态或白函伤痕。
- 不得用一段自动变形Cut-in替代三阶段地图动作，也不得用菜单数值结算载荷取舍。
- 不得让七海现场上舰、私下无记录放水、恢复系统写权限或因感情取消风险定义。
- 不得通过完美探索、隐藏条件或刷数值让三类载荷全保。

## 7. 期末最低输出

- `WANJI_SITE_LOST`
- `JICUN_BURN_01`
- `WBM001_ACTIVE`
- `JICUN_MEMORY_FRAGMENT_01`
- `CURATOR_OLD_ROUTE_SHADOW`
- `ZERO_SHORTCUT_REFUSED`
- `ZERO_SHORTCUT_SLOW_HULL_FIELD=BLANK_NOT_ZERO`
- `ZERO_SHORTCUT_CURRENT_HARM=DIEDIE_RECLASSIFIED_AND_DISTRIBUTED_STOP_GRAYED_THEN_RESTORED`
- `WANJI_LOADOUT_EXACT_TWO_OF_THREE`
- `WANJI_LOADOUT_BUNDLE_ID=LIFE_PHYSICAL|LIFE_ARCHIVE|PHYSICAL_ARCHIVE`
- `ROUTE_MODEL_STREET_SURVIVAL_LOCK=36_HOURS`
- `WBM001_MOBILE_RISK_ID`
- `QIHAI_FIRELOCK_DELAY_RECORD`
- `E04_REGISTERED_OPERATOR_CREW=JICUN+DOUDENG+TANGJIAO+LUHENG`
- `E04_OPERATOR_CREW_COUNT=4_ONBOARD_PROTECTED_POSTS`
- `E04_EVACUEE_PAYLOAD_COUNT=0`
- `B1_MOVING_SPINE_PREVIOUS=PHYSICALLY_LOCKED_BY_MILITARY`
- `B1_MOVING_SPINE=RELEASED_LOW_SPEED_CRUISE_AFTER_SIX_ANCHORS`
- `GZ_BASIC_RESIDENT`
- `BLACK_SHOWCASE_SHADOW=FIRST_VISIBLE_RESTRAINED_NO_CONTROL`
- `TEMPORARY_OPEN_STATUS`
