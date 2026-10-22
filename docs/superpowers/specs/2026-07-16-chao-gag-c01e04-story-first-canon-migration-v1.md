# C01E04 Story-First Canon Migration v1

> Status: `canon_migration_applied_story_production_contract_accepted_candidate_runtime_parity_complete`
>
> Scope: `C01E03 RT035 -> C01E04 RT054 -> C02E01`
>
> Reconstruction source: `V35.9/rebuild/episodes/C01/C01E04-万机馆站起来-v1.md`

## 1. Reason

旧E04包含移动底盘、火锁、风险标记和七海申诉等可用材料，但同时留下隐藏维修班、人命载荷、抽象零号诱惑、一句Cutscene起航和多份并行状态源。E03已经用RT035提交全部人员安全、馆守Z永久断臂、勇拳回收、白函双伤和设施损伤；E04必须从这份精确快照继续，而不能重造需要营救的人或清空前话代价。

独立Story、Gameplay、Canon三席审读又揭示四个第二轮问题：四名返入者被误写成仍在馆外；E04重复E03“拒绝私有捷径+再切一根轨”的语法；零号没有当前伤害；皇影替玩家免费纠错。当前迁移已经吸收这些问题。

## 2. Applied Changes

| Migration | Current decision | Downstream lock |
|---|---|---|
| `C01MIG016` / `V358MIG054` | E04唯一动态输入为E03 RT035精确27键。疏散人员和两件消防货物已安全；纪存、兜灯、唐胶、陆衡作为四名必要操作员受消防监督返入保护岗位并随舰，零疏散载荷。零号旧路先取回三枚活动核心，随后把跌跌设备化、灰掉分布式停止权并要求纪存永久独占管理；纪存实测停止失败后物理拔桥 | 禁止隐藏维修班、人员/消防货物/右臂载荷、只听诱惑便拒绝、四名操作员再次被写成馆外或三类全保 |
| `C01MIG017` / `V358MIG055` | 万机馆拥有固定建筑、半身抬升、受损巡航三种生产态与一次提前位移过渡；E01模型病院、留言墙、真机台成为身体地标。馆守Z先主动调整左肩承重点，再等待兜灯硬停。皇影黑框卡死右锁泊臂并加剧失衡；旧拘束只阻止扩张，玩家自行排障 | 禁止把过渡态报成第四套完整资产、自动Cut-in变形、馆守ZE04复臂/飞拳、皇影免费纠错/停舰/可控、删除小机或让火锁人格化 |
| `C01MIG018` / `V358MIG056` | 陆衡因E03结构传感已在邻区待命，六锚位移使23:17工单升级；他带证件和消防领入回执到场，先承认固定建筑模型算错，再用跌跌失败振动修正。七海全程远程停权，在城市/军方值守席前把申请收窄为四操作员、零疏散载荷、精确两类货载、东行低速并避开医院电网；她承担停职延长。旧V31与C01E04-01..08历史化 | 禁止陆衡无来源或永不犯错；禁止七海现场上舰、私下放水或恢复写权限；旧E04不得提交当前首登和状态 |
| `C01MIG019` / `V358MIG057` | 锚点、载荷、半身抬升和城市走廊失败只回各自本地检查点且零持久写；36小时债只由成功离开旧址产生。RT054一次提交：RT035中26个非迁移值保持，B1旧值另存`PREVIOUS`、当前值转为六锚解除后低速巡航；C02精确读取三类载荷状态、四操作员、零疏散载荷和B1历史/当前双值 | 禁止把战术失败写成36小时永久惩罚、宣称27键连B1当前态都不变、用抽象载荷别名代替三类状态，或让C02重新选择目的地和人员状态 |

## 3. Unique Input

`C01E04-input-carry-v1.md`锁定RT035全部27键。运行时精确读取一次，缺键、多键或值冲突均不得进入E04。`CANON-RULE-004`是七海远程停权边界，不伪造第28个动态键。

不可重置事实包括：

- 二十九名观众、E03五人、豪司和两件消防接驳货物均安全。
- 馆守Z永久单臂，右臂留在旧址构成L1/L2复合桥且禁止装载。
- 勇拳企业回收、数据剥离；白函带右肩裂与断索撤离。
- 供水热损、商业风道漏热、档案紧急冷却、消防架桥机左前腿过载继续存在。
- `B1_MOVING_SPINE=PHYSICALLY_LOCKED_BY_MILITARY`是E04开场状态，不是期末仍不变的当前值。

## 4. RT054 Atomic Output

只有六锚解除、精确两类非人载荷固定、第三类公开留置、馆守Z单臂支援与硬停有效、四操作员保护框完好、五Owner检查全绿、火锁未满、结构与热量合法、城市关键区/管线/医院无损并通过东门，`RT054`才一次提交。

关键输出：

```text
WANJI_SITE_LOST=TRUE
WBM001_ACTIVE=CRUISE_CARRIER_WITH_DAMAGE
ZERO_SHORTCUT_REFUSED=TRUE
ZERO_SHORTCUT_CURRENT_HARM=DIEDIE_RECLASSIFIED_AND_DISTRIBUTED_STOP_GRAYED_THEN_RESTORED
WANJI_LOADOUT_EXACT_TWO_OF_THREE=TRUE
WANJI_LOADOUT_BUNDLE_ID=LIFE_PHYSICAL|LIFE_ARCHIVE|PHYSICAL_ARCHIVE
PEOPLE_CARGO=FORBIDDEN
E04_REGISTERED_OPERATOR_CREW=JICUN+DOUDENG+TANGJIAO+LUHENG
E04_OPERATOR_CREW_COUNT=4_ONBOARD_PROTECTED_POSTS
E04_EVACUEE_PAYLOAD_COUNT=0
B1_MOVING_SPINE_PREVIOUS=PHYSICALLY_LOCKED_BY_MILITARY
B1_MOVING_SPINE=RELEASED_LOW_SPEED_CRUISE_AFTER_SIX_ANCHORS
ROUTE_MODEL_STREET_SURVIVAL_LOCK=36_HOURS
QIHAI_FIRELOCK_DELAY_RECORD=PUBLIC_40_SECONDS_WITH_REVIEW_AND_SUSPENSION_EXTENSION
GZ_BASIC_RESIDENT=CHEST_BEARING_SINGLE_ARM
BLACK_SHOWCASE_SHADOW=FIRST_VISIBLE_RESTRAINED_NO_CONTROL
TEMPORARY_OPEN_STATUS=ACTIVE
```

三个Bundle都必须逐类输出：

| Bundle | Life Support | Unique Physical Collection | Archive Server | Archive Backup |
|---|---|---|---|---|
| `LIFE_PHYSICAL` | `CARRIED_OPERATIONAL` | `CARRIED_OPERATIONAL` | `OLD_SITE_PUBLIC_UNCARRIED` | `COMPLETE_AT_OLD_SITE` |
| `LIFE_ARCHIVE` | `CARRIED_OPERATIONAL` | `OLD_SITE_PUBLIC_UNCARRIED` | `CARRIED_OPERATIONAL` | `NOT_APPLICABLE_CARRIED` |
| `PHYSICAL_ARCHIVE` | `OLD_SITE_PUBLIC_UNCARRIED` | `CARRIED_OPERATIONAL` | `CARRIED_OPERATIONAL` | `NOT_APPLICABLE_CARRIED` |

## 5. Runtime And Production Contract

- 单一16x12斜45度棋盘经历`FIXED_BUILDING -> PREMOVED_ONE_SECTION -> HALF_RISE -> CRUISE_CARRIER_WITH_DAMAGE`；前三项中固定、半身、巡航是生产态，提前位移只是中间过渡。
- 纪存、兜灯、唐胶、陆衡是四名受保护的随舰操作员；旧守护者是非人Owner。五者均不作为普通步兵上格。
- 跌跌、机器犬和固定夹具是地图行动体；馆守Z是主动表意、受兜灯硬停约束的单臂支援体。
- 风险无人机先公开路径、目标和预计火锁增量，再行动。玩家通过占位、遮蔽、诱导、冷却与馆体重投影处理，不要求普通HP全灭。
- 每个地图行动体每回合一次；待机、取消、无目标退出和结束回合始终可用。
- 三类载荷各有真实消费者：生活维持控制热扩散，实体馆藏提供配重/缓冲，档案服务器预告意图但消耗冷却。
- 四个本地检查点是`ANCHOR_LOCAL`、`LOADOUT_LOCAL`、`HALF_RISE_LOCAL`、`CITY_LOCAL`。RT049-052完整恢复相应快照；退出RT054前重读RT035。
- 半身承重结束后，两侧锁泊臂以一次可见`CORRIDOR_FOLD`同步收成道路姿态，结算热量与条件档案冷却，再建立`CITY_LOCAL`。收臂资源失败回`HALF_RISE_LOCAL`；城市失败恢复已含收臂成本的`CITY_LOCAL`，不得重复付费。
- 资产矩阵有56行并显式区分`PERSISTENT_INPUT`、`LOCAL_STAGED_UNTIL_RT054`、`PERSISTENT_AFTER_RT054`、非持久规则和场景道具。

## 6. Character, Cargo And Mystery Boundaries

- 纪存不是再次用“拒绝按钮”证明正确；他先允许零号有效取回核心，亲手经历停止权失效，再拔掉物理桥并承担临时管理员责任。
- 唐胶为小满画歪的感叹号、留言墙原件和模型病院修复件争取；兜灯选择生活维持，即使馆守Z维修史只能留在仍亮旧址；纪存放弃自己最整齐的数字记录。取舍必须伤到具体的人和已见物件。
- 唐胶不再重复E03永久切轨；档案室通过非破坏性解耦留在旧址亮灯。
- 陆衡先用错误模型失败，再用工况和振动修正；他只签当前移动包络，不认证神话。
- 七海没有上舰。她的程序动作保留风险定义，同时把可允许范围压到最窄并承担具名处分；关系余温只留在冷饭袋和未接来电。
- 馆守Z在命令前主动露出左肩承重点，随后等待兜灯可执行硬停。
- 皇影只有局部三拍：睁眼、黑框卡右锁臂、拘束止扩张；它不替玩家修锁，不建立主人关系。
- 零号不开深层门，不解释G.A.G.或封印真相；远星只出现一次`OPEN -> CLOSE -> OPEN`错序半帧。

## 7. Updated Sources

迁移根包括Episode、Input Carry、Runtime、Graybox、Asset Matrix、Canon entities/scenes/art locks、V35.5传播、V35.8 migrations、C02入口、PB、canonical terms和设计图谱。V31与旧`C01E04-01..08`仍可显式追溯创意，但不得提交当前人物、首登、状态、玩法或资产事实。

## 8. Validation State

- 独立Story、Gameplay、Canon三席问题已经吸收进第二轮正文和合同。
- `scripts/check_c01e04_runtime_graybox.py`当前通过：27输入键、57 Runtime行、40 Graybox行、56 Asset行、三精确Bundle、四检查点、三生产态加一过渡、结束回合/待机/取消/无目标退出均被检查。
- Gameplay/Production独立席已在`14-gameplay-production-final-recheck-r3.md`手算三Bundle三步主路、生活分支五步转体、两类回滚与误败前置禁用并判定`PASS`；整话最终回执见`15-final-acceptance.md`。
- V35.8生成器已在源头写入`V358MIG054-057`，重生成不会删除迁移。
- C02入口已经读取精确Bundle、四操作员、零疏散载荷和B1双值。
- Canon/图谱迁移已应用；C01E04 checker、Canon smoke与Godot strict当前通过。
- Godot七节点E04已经加入B1人尺度工程巡检与独立精确二选三Constraint台；六阶段82动作候选战只读取已选Bundle，不再二次选择。新增四动作把F锚保持、系统保持回执、P3操作员追踪和P6五Owner确认从旧聚合动作中拆开。P1/P4/P5现在是至少十一回合的真实玩家/敌方循环，包含唯一主动Writer轮转、地图相邻安全格诱导、当前意图与剩余路线预测、档案下一意图、医院/管线/关键城市独立损伤、A-F物理锚、三段载荷、皇影先于半身、独立万机馆本体行动句柄、五岗位每回合动作、纪存可存档恢复的一次馆体撤回、旧守护者定向调度、显式武装实体缓冲、三步半身Mask、道路收臂、三步东移、可逆转体、锁臂展开/收回、三分支资源与RT049-052完整回滚。敌方结算以Session三机回执驱动0.72秒确定性位移、重定向/屏蔽/压线/配重吸收几何和可跳过结算侧栏，不重复计算规则。RT054局部事实合并、E01-E04连续Runner、十帧战术视觉与四帧预战多玩法视觉证据见`2026-07-16-chao-gag-c01e04-godot-implementation-evidence-v1.md`。
- 当前剧情、受众、生产设计合同与Canon已放行；Godot逐行候选矩阵当前为`57 VERIFIED_CURRENT / 0 PARTIAL_CURRENT / 0 NOT_IMPLEMENTED`。原十二条精确缺口已由四状态拆卸卡、锚点保持与F夹具回执、馆守Z下沉Mask/三格屏护、独立载荷工位与逐步碰撞回执、两格配重位移、具名未带走物、四操作员独立追踪、五Owner动作和逐格城市预测直接闭合，详见`2026-07-17-chao-gag-c01e04-godot-runtime-parity-audit-v1.md`。正式逐帧Sprite、SFX、E04正式美术、真人完整手玩、存档迁移和平台验收仍未闭合；57/57仅指候选Runtime逻辑，不等于正式试玩Production完成。
