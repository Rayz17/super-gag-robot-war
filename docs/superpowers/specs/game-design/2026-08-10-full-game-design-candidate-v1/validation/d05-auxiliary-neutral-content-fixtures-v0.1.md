# D05 辅助玩法中性内容 Fixtures v0.1

> Status: `candidate_paper_fixtures / zero_build / zero_target_players / no_prototype_authorization / no_gameplay_acceptance`
>
> Scope: 只为 `P-EX1` / `P-EX2` / `P-EX3` / `P-HUB1` / `P-SET1` 提供可编程的中性初态、指令、分支、回写和断言。
>
> Canon boundary: 全部地点、人物、物件、任务、数值与结果均使用 `TEST_*` 匿名实体，不是 Canon，不映射或改写 C01-C03 已验收故事，不向 Reader、Runtime、Demo 或正式资产写入。

## 1. 实现边界与共用协议

本件把 [辅助玩法设计](../06-auxiliary-play-design.md) 第 13 节所说的“尚缺内容夹具”补到 M2 纸面数据深度。四内核、输出门和状态 Owner 仍分别以 [auxiliary-kernel-contracts.tsv](../data/auxiliary-kernel-contracts.tsv)、[auxiliary-output-gates.tsv](../data/auxiliary-output-gates.tsv) 与 [settlement-owner-prepare-commit-contracts.tsv](../data/settlement-owner-prepare-commit-contracts.tsv) 为准。

### 1.1 共用实现规则

- `fixture_version=d05_aux_neutral_v0.1`；不使用随机数、随机刷新、自由文本判定或隐藏成功率。
- 本文中的拓扑即中性 `TEST_GD2` 数据夹具，不是正式 GD2 地点包。未来 Build 必须生成真实 `content_hash`；值为 `PAPER_FIXTURE_ONLY` 时必须 fail-closed，不得冒充已封存包。
- 任一持久改变都先产生 Owner proposal，再由 `SYS-SETTLE` 原子提交；UI 、玩法脚本和事件动画不能直写其他系统状态。
- 相同 `transaction_id + payload_hash` 重放返回同一 receipt；相同 ID 不同 payload 拒绝为 `E_ID_COLLISION`；任一 Owner 拒绝则整组 `0 write` 。
- 通用终局语义只有 `clear / partial / withdraw`。`withdraw` 不是 Game Over：它必须说明已保留什么、未发生什么、从哪个检查点继续。
- 可见名称只是中性测试标签，不得被复制到角色、地点、收藏或世界规则 Canon 表。

### 1.2 五个 Fixture 的硬输出

| Fixture | 主内核 | 必须产生 | 具名中性 Future Consumer |
| --- | --- | --- | --- |
| `P-EX1` | `AUX_SPATIAL` | 访问对象、对象前后态或人物回应、路线摘要 | `TEST_CONSUMER_EX1_ROUTE_BRIEF` / `TEST_CONSUMER_EX1_PERSON_REPLY` |
| `P-EX2` | `AUX_EVIDENCE + AUX_COMMIT` | 三条有来源证据、假说态、实测轨迹、实体配置写请求 | `TEST_CONSUMER_EX2_LOAD_SETUP` / `TEST_CONSUMER_EX2_WORKORDER` |
| `P-EX3` | `AUX_EVIDENCE + AUX_SPATIAL` | 五节点以内的知识链、矛盾、保留未知、重访路线差分 | `TEST_CONSUMER_EX3_SIDE_ROUTE` / `TEST_CONSUMER_EX3_ARCHIVE_REVIEW` |
| `P-HUB1` | `AUX_COMMIT + AUX_ROUTE` | 五事件的选/未选、岗位冲突、一张已提交任务卡、一张未选结果 | `TEST_CONSUMER_HUB_MISSION_A` / `TEST_CONSUMER_HUB_MISSION_B` |
| `P-SET1` | `SERVICE_SETTLEMENT` | 三级幂等 receipt、Owner diff、玩家摘要、下一消费者 | `TEST_CONSUMER_SET_NEXT_ENCOUNTER` / `TEST_CONSUMER_SET_HUB` / `TEST_CONSUMER_SET_NEXT_CHAPTER` |

## 2. P-EX1《水线分馆集合》微型自由探索

### 2.1 目标与拓扑

- `activity_id=TEST_EX1_WATERLINE_ANNEX`，目标时长 `15-20m`，不战斗、不计分、无任务箭头。
- 入口就能看见东侧高处的 `ANCHOR_BLUE_LANTERN`；主目标是抵达蓝灯平台并向值守者回报“哪条路可供搬运车返回、需要满足什么条件，或哪条路应明确排除”。
- 路线事实池为 `FACT_EX1_UPPER_WALK_PEDESTRIAN_ONLY`、`FACT_EX1_WATER_MARK_HIGH`、`FACT_EX1_CART_NEEDS_DRY_ROUTE` 与 `FACT_EX1_TRACKS_CONFIRM_DRY_ROUTE`；每条主路都恢复恰好两个可复述事实，它们只描述当前空间与搬运条件，不是世界真相。

| 节点 | 可见地标 | 邻接 | 初态交互 |
| --- | --- | --- | --- |
| `EX1_N0_ENTRANCE` | 圆拱入口，可直视蓝灯 | `N1,N2` | 查看全局图牌；退出点 |
| `EX1_N1_UPPER_WALK` | 红布棚和悬挂路牌 | `N0,N3` | `ACTOR_EX1_MORI` 与倒置路牌 |
| `EX1_N2_SERVICE_LANE` | 黄轨条和停住的搬运车 | `N0,N3,N4` | `ACTOR_EX1_PEL` 与卡住的前轮 |
| `EX1_N3_TIDE_COURT` | 白色水尺墙 | `N1,N2,N5` | 观察高水痕；拍摄可选 |
| `EX1_N4_DRY_ARCADE` | 绿顶干廊 | `N2,N5` | 观察连续干燥轮辙 |
| `EX1_N5_BLUE_LANTERN` | 蓝灯集合台 | `N3,N4` | 向 `ACTOR_EX1_VALE` 提交路线判断 |

三条合法主路是 `N0-N1-N3-N5`、`N0-N2-N4-N5` 与 `N0-N2-N3-N5`。`N2-N4` 只在完成 `HELP_EX1_CART` 或绕过车后可通行；绕过耗时 `90s`，帮助耗时 `60s` 并改变搬运车后态。

### 2.2 实体与初态

| ID | 初态 | 玩家可知 | 不允许推断 |
| --- | --- | --- | --- |
| `ACTOR_EX1_MORI` | 在 N1；路牌被风吹倒 | 说明上层通向水尺墙，但栈道只承行人、不承载车 | 不自动成为队友或 Canon 人物 |
| `ACTOR_EX1_PEL` | 在 N2；车轮被软垫卡住 | 车不能经积水路 | 不授予任何物件所有权 |
| `ACTOR_EX1_VALE` | 在 N5 等待口头回报；`REL_EX1_ROUTE_REQUEST=pending` | 接受“干廊可用”“水尺庭附条件可用”或“上层栈道只供行人”的有证据路线判断 | 不因路线不同判定唯一正解；回应状态由 Relationship Owner 写，不由探索 UI 直写 |
| `OBJ_EX1_CART` | `position=N2;wheel=blocked;custody=Pel` | 可帮助移走软垫 | 不可拾取或转为背包物品 |
| `OBJ_EX1_WATER_MARK` | `position=N3;state=visible` | 高水痕比当前地面高两格 | 不自动推断洪水原因 |
| `OBJ_EX1_TRACKS` | `position=N4;state=dry_continuous` | 轮辙尺寸与搬运车匹配 | 不自动证明该路永久安全 |

初始 `access={N0,N1,N2,N3,N5}`，`N4=blocked_by_cart_but_bypassable`，`visited={N0}`，`helped={}`，`route_summary=none`。地图不显示未访问节点名，只显示玩家已看见的地标轮廓。

### 2.3 指令流、合法选择与拒绝

1. `MOVE(adjacent_node)`：只接受邻接且 access 合法的节点。
2. `OBSERVE(anchor_or_object)`：记录具名对象及当前态；不把观察自动升为结论。
3. `TALK(actor)`：只读取该人物当前知道的事实与请求。
4. `HELP(OBJ_EX1_CART)`：只在 N2；完成后 `wheel=free`，触发 Pel 的结果回应。
5. `PHOTO(OBJ_EX1_WATER_MARK|OBJ_EX1_TRACKS)`：可选证据，不影响主目标可达。
6. `REPORT(route_judgement, supporting_observations)`：只在 N5；一条有来源现场事实可提交为 `local_risk_only` 的 partial，只有引用本路真正遇到的两条事实才可提交完整路线判断。A 路形成“上层栈道应排除、当前水尺庭需附水位条件”的判断；B 路形成“搬运车需要干路、干廊轮辙可证”的判断；C 路形成“服务道可到水尺庭，但必须满足当前水位低于痕线”的判断。三种有两事实支持的路线判断都合法，并分别把 `REL_EX1_ROUTE_REQUEST pending→answered_with_evidence`；一事实 partial 只改为 `needs_followup`。
7. `RETURN`：回到 N0 或已解锁的 N5 稳定返回点。

以下指令必须拒绝且不改状态：跨栏翻入未登记机房 `E_ACCESS_UNDESIGNED`；从非邻接节点瞬移 `E_NOT_ADJACENT`；取走搬运车 `E_CUSTODY`；无观察支持就提交“唯一安全路” `E_UNSUPPORTED_REPORT`；更改水痕为故事真相 `E_TRUTH_OWNER`。

### 2.4 结局、回写与消费

| 结局 | 条件 | 提交 | 不提交 |
| --- | --- | --- | --- |
| `clear` | 到达 N5；提交由本路两条现场事实支持的路线判断 | `visited_objects;route_summary;optional_help;optional_photo;future_consumers`，以及 `REL_EX1_ROUTE_REQUEST=answered_with_evidence` 的具名 Relation proposal | 通用奖励、隐藏真相、人物入队；帮助 Pel 仍是 optional，不决定 clear/partial |
| `partial` | 到达 N5；只提交一条有来源事实支持的 `local_risk_only`，或明确把判断留为 unresolved | 保留访问与来源；`route_summary=local_risk_only/unresolved`；`REL_EX1_ROUTE_REQUEST=needs_followup`；搬运车按真实帮助结果保持 blocked 或 free | 不锁主线，不伪造第二条事实或帮助结果 |
| `withdraw` | 在 N0 选择退出，或从已访问节点返回 N0 | 已确认的 `visited_objects` 和有来源的可选照片；检查点=N0；`REL_EX1_ROUTE_REQUEST` 保持 pending | 不生成 `route_summary`，不触发 N5 回应 |

`TEST_CONSUMER_EX1_ROUTE_BRIEF` 只读最后提交的路线摘要，用于下一个中性运输卡面；`TEST_CONSUMER_EX1_PERSON_REPLY` 读取 Vale 的 request state 与 Pel 是否获助，用于下次访问的人物／对象前后态。消费者 ID 不存在时输出门必须失败，不能留一条孤立收藏。

### 2.5 测试断言

- 断开任一个可选帮助后，主目标仍有两条以上合法路线；不允许主持人导航。
- A/B/C 三条路线都必须生成两条不同的可复述事实；少一条时只能提交具名 partial，不能生成 clear route receipt。
- 每个 clear 都必须通过 `REL_EX1_ROUTE_REQUEST pending→answered_with_evidence` 满足 `AOG_SPATIAL` 的 `object_changes_or_relation_change`；partial 写 `needs_followup`，withdraw 保持 pending，三者不得共用同一 output payload。
- 不观察水痕也可经轮辙提交干廊；不观察轮辙也可经水痕提交保守路线。
- `clear/partial/withdraw` 的 receipt hash 不同；同一结局重放 1000 次相同。
- UI 无任务箭头、闪烁收集物或隐藏小地图路线；导航只靠地标、邻接和玩家自己的记录。
- 任一不合法指令前后 `state_hash` 相同。

## 3. P-EX2《偏载试验架》工程实证

### 3.1 问题、证据和假说

- `activity_id=TEST_EX2_ASYMMETRIC_GANTRY`，目标时长 `10-15m`。
- 可验证问题：“测试架在额定载荷下左偏摆动，是左缓冲件衰减不足，还是控制增益过高为主因？”
- 后台仅有求解器需要的物理数值，不存在世界观真相。玩家不看“正确答案”，只看证据、可预览安全包络和实体反馈。

| 证据 ID | 类型 / 来源 | 观测 | 可支持 | 置信 / 揭示边界 |
| --- | --- | --- | --- | --- |
| `EVID_EX2_WEAR` | 外观；左右缓冲件尺表 | 左压缩 45%，右 20% | `HYP_EX2_DAMPER_PRIMARY` | high；只证明静态差异 |
| `EVID_EX2_LOG` | 控制日志；带时间戳 | 增益从 0.65 调到 1.00 后首次出现偏摆 | `HYP_EX2_GAIN_PRIMARY` | medium；日志不证明唯一因果 |
| `EVID_EX2_HEAT` | 传感；上次额定脉冲 | 左温升 +18°C，右 +4°C | `HYP_EX2_DAMPER_PRIMARY` | high；只对当次载荷有效 |

| 假说 ID | 初态 | 可证伪预测 |
| --- | --- | --- |
| `HYP_EX2_DAMPER_PRIMARY` | `candidate` | 加左侧支撑插件后，保持标准增益也应在额定载荷稳定 |
| `HYP_EX2_GAIN_PRIMARY` | `candidate` | 不加插件、只降增益时，应在额定载荷稳定 |

### 3.2 三个变量与确定求解器

| 变量 | 合法值 | 语义 |
| --- | --- | --- |
| `brace` | `none / left_insert` | 插件使左有效阻尼 `+0.35` |
| `gain` | `reduced=0.65 / nominal=1.00 / high=1.20` | 反馈增益 |
| `load` | `low=40 / rated=80 / overload=110` | 试验脉冲；`overload` 始终不合法 |

初始 `left_damping=0.55`、`right_damping=1.00`。

```text
oscillation_score = 0.70 * gain + 0.004 * load - left_damping - brace_bonus

score <= 0.20  -> stable
0.20 < score <= 0.45 -> bounded_oscillation
score > 0.45 -> outside_safe_envelope
```

| 配置 | score | 是否允许执行 | 实体反馈 |
| --- | ---: | --- | --- |
| `left_insert + nominal + rated` | `0.12` | 允许 | 额定载荷稳定；直接验证缓冲件假说 |
| `none + reduced + low` | `0.065` | 允许 | 低载稳定；只是保守诊断步，不证明额定可用 |
| `none + reduced + rated` | `0.225` | 允许 | 可控振荡；证明降增益不足以完成额定验收 |
| `none + nominal + rated` | `0.47` | 拒绝 | 预测超包络，说明是哪三项数据导致，不只显红叉 |
| `none + high + rated` | `0.61` | 拒绝 | 同上 |
| 任何 `overload` | n/a | 拒绝 | `E_LOAD_OUTSIDE_TEST_SCOPE` |

### 3.3 玩家流程

1. `INSPECT` 三类证据；每条显示来源、时间和能/不能证明的事。
2. `ANNOTATE_SUPPORT(evidence,hypothesis)`；允许同一证据对多假说仅有间接支持。
3. `CONFIGURE(brace,gain,load)`；UI 显示公开公式、输入和结果带。
4. `PREVIEW_SAFETY`；超包络时禁止提交，但保留草案以供对比。
5. `RUN_TEST`；播放/跳过使用同一 result payload。
6. `REVISE_HYPOTHESIS`；只能根据新实测把假说改为 `likely / verified / disproved / unresolved`。
7. `COMMIT_REPORT` 或 `WITHDRAW`。

两种合法安全节奏是：A）读完三证据后直接用插件做额定试验；B）先低载降增益诊断，再用插件做额定试验。两者都可 `clear`，但 B 多一次时间成本。

以下为非法选择：没有来源就新增证据 `E_EVIDENCE_SOURCE`；试验前直接标 `verified` 为 `E_PROOF_MISSING`；执行超包络配置 `E_SAFETY_ENVELOPE`；把工程可行自动当成物主许可或主体同意 `E_OWNER_BOUNDARY`；用本场结论创建故事事实 `E_TRUTH_OWNER`。

### 3.4 结局与写回

| 结局 | 条件 | Owner proposal | Future consumer |
| --- | --- | --- | --- |
| `clear` | 额定载荷 `stable`；有实测支持的假说已分层 | `ST_EVIDENCE` 三条；`ST_HYPOTHESIS` 差分；`ST_BODY` 请求 `left_insert=installed_for_test`；`ST_RESULT` | `TEST_CONSUMER_EX2_LOAD_SETUP` 读可验证的额定配置 |
| `partial` | 只完成低载稳定或额定可控振荡 | 保留证据与 `unresolved/likely`；不写额定可用；生成工单 | `TEST_CONSUMER_EX2_WORKORDER` 要求更换或再测 |
| `withdraw` | 在实测前退出，或只保留不安全草案 | 保留已收证据和 `candidate` 假说；不扣材料，不写身体 | 同一活动检查点 |

### 3.5 测试断言

- 调换证据读取顺序不改公式或结果。
- 只看 `EVID_EX2_LOG` 不足以把任一假说提升到 `verified`。
- 两种安全节奏均可达 `clear`；未来人测若只能靠记固定配置过关，Fixture 失败。
- 不安全配置的拒绝日志必须包含公式输入和原因，不产生红叉猜答语法。
- `Full/Skip`、存读档和不同帧率的 `proof_receipt` 完全一致。

## 4. P-EX3《倒相信号间》知识重访

### 4.1 五节点知识夹具

- `activity_id=TEST_EX3_PHASE_ROOM`，同一小空间访问两次，总时长 `20-30m`。
- 空间只有 `ENTRY / CONSOLE / SIDE_PLATFORM / RETURN`四个物理节点；第二次不加门卡或新道具，只改变玩家已建立的可读规则。

| 知识节点 | source / observed_at | subject | claim | confidence | 与谁矛盾 |
| --- | --- | --- | --- | --- | --- |
| `KN_EX3_MARKS` | 现场凹槽 / Visit-1 T+00 | 三脉冲控制台 | 三段输入包含高低两种电平和 1/2 两种时长 | high | none |
| `KN_EX3_OLD_LOG` | 本地旧日志 / source T-20 | 上次成功输入 | 记录为 `LOW-2-HIGH` | high_as_record / medium_as_meaning | `KN_EX3_NOTE` |
| `KN_EX3_NOTE` | 现场纸卡 / source T-8 | 当前输入 | 写为 `HIGH-1-LOW` | medium | `KN_EX3_OLD_LOG` |
| `KN_EX3_CALIBRATION` | 外部校准公告 / 两访之间 T-10 | 信道标签 | T-10 之前的日志中 HIGH/LOW 标签互换，时长未变 | high | 修正旧日志语义，不删旧来源 |
| `KN_EX3_LIVE_ECHO` | 当前回波 / Visit-2 T+02 | 中段持续时间 | 平台反馈需要长脉冲 `2` | high | `KN_EX3_NOTE` 的 `1` |

假说只有两个：

- `HYP_EX3_NOTE_LITERAL`: 纸卡字面 `HIGH-1-LOW` 仍有效。
- `HYP_EX3_LOG_REINTERPRETED`: 旧日志需经标签倒相，正确当前序列是 `HIGH-2-LOW`。

### 4.2 两次访问的确定流程

**Visit 1**

1. 玩家可任意顺序 `OBSERVE` 前三节点，但不能自动消除矛盾。
2. `LINK` 只能建立 `supports / contradicts / same_subject / later_than` 四种有限关系。
3. 玩家可尝试 `HIGH-1-LOW`；结果是安全的 `no_route_change`，假说从 `candidate -> disproved_for_current_console`，纸卡来源仍保留。
4. 玩家提交 `unresolved` 记录并返回；系统不生成“去找钥匙”。

**Interlude**

5. 一个已登记的中性资料源向玩家投影 `KN_EX3_CALIBRATION`；这是带来源和时间的对照知识，不是 inventory item。

**Visit 2**

6. 玩家在同一 CONSOLE 读到 `KN_EX3_LIVE_ECHO`，将它与校准公告、旧日志相连。
7. `SUBMIT_INTERPRETATION(HIGH-2-LOW, evidence={OLD_LOG,CALIBRATION,LIVE_ECHO})` 合法；`APPLY` 后 SIDE_PLATFORM 从 `closed -> accessible`。
8. 结果仍保留 `UNKNOWN_EX3_WHY_NOTE_DIFFERS`：纸卡是简写、失误还是另一个版本，本 Fixture 不回答。

非法选择包括：篡改时间戳 `E_SOURCE_IMMUTABLE`；删掉矛盾证据 `E_EVIDENCE_HISTORY`；没有 `CALIBRATION` 就把倒相假说标为验证 `E_PROOF_MISSING`；把平台开启解释成任何 Canon 真相 `E_TRUTH_OWNER`；不引证就穷举脉冲 `E_BRUTE_FORCE_SUBMIT`。

### 4.3 结局、知识遮罩与回写

| 结局 | 条件 | 回写 | 路线后态 |
| --- | --- | --- | --- |
| `clear` | 第二访提交有三来源支持的 `HIGH-2-LOW` | 五知识节点、两假说结果、一条保留未知、route proposal | `SIDE_PLATFORM=accessible` |
| `partial` | 已建立倒相规则但不执行，或只证伪纸卡字面解 | 保留证据和假说态；不伪造 verified | `closed_but_understood` |
| `withdraw` | 任一访问从 RETURN 退出 | 只提交已观察节点和已有来源的链；保留访问号 | `closed` |

观察者遮罩：`PLAYER` 看已采集节点与自己假说；`ACTOR_EX3_REMOTE` 只看玩家显式分享的节点；`PUBLIC` 只看平台是否开放；`BACKEND_TEST_ORACLE` 只供自动断言，不得出现在任何 UI 投影。

`TEST_CONSUMER_EX3_SIDE_ROUTE` 只读 route receipt；`TEST_CONSUMER_EX3_ARCHIVE_REVIEW` 读矛盾未解和来源链，不把开门自动上升为所有人知道。

### 4.4 测试断言

- 删除 `KN_EX3_CALIBRATION` 后，第二条假说不可 verified；添加任何 inventory key 后自动检查失败。
- 知识节点始终 `<=5`；自由输入第六节点或第五种关系均拒绝。
- 第二访的物理拓扑只因合法知识 receipt 改变，不读等级、全局情报点或物品栏。
- `PLAYER / REMOTE / PUBLIC` 三个投影的 hash 必须不同，且全部不含 oracle-only 字段。

## 5. P-HUB1《三个时段的回馆夜》

### 5.1 初态、空间与人物

- `hub_cycle_id=TEST_HUB_CYCLE_01`，行动预算固定 `3`，完整目标时长 `15-20m`。
- 中性空间锚点为 `TEST_HUB_HALL / TEST_HUB_BAY / TEST_HUB_ARCHIVE / TEST_HUB_TERMINAL`；它们只测状态投影和快速切换，不定义万机馆正式建筑。
- 每个事件只能处理一次，未选事件不“每日刷新”。

| 实体 | 初态 / 资源 | 冲突边界 |
| --- | --- | --- |
| `ACTOR_HUB_ENGINEER` | available；熟悉牵引绞盘 | 只能参与 E1 或 E2 之一；若占用则不作为任务可选队员 |
| `ACTOR_HUB_COURIER` | available；熟悉短航线 | 参与 E1 后不作为任务可选队员 |
| `ACTOR_HUB_ARCHIVIST` | available；保管借展记录器 | 只能参与 E3 或 E4 之一；若占用则不作为任务可选队员 |
| `ACTOR_HUB_QUARTERMASTER` | available | 只参与 E5，不占两张任务卡的必需岗位 |
| `ACTOR_HUB_FIELD_LEAD` | available | 两张任务卡的固定必需岗位；不参与五事件，防止无任务可提交死局 |
| `BODY_HUB_TOW_RIG` | `winch=degraded;frame=normal` | 只能由 E2 产生修理 proposal |
| `OBJ_HUB_RECORDER` | `owner=TEST_LOCAL_LIBRARY;custody=TEST_HUB;display=withheld` | 展示、研究、归还分开；任一选择不转移所有权 |
| `ST_RESOURCE` | `common_material=2;repair_capacity=1;action_slots=3` | 关系、同意、人物时间不可用材料购买 |

返馆后免费强制回执在 `<=90s` 内显示三处变化：牵引绞盘壳体弯曲；借展柜由透明改为封签；路线板出现一条过期 40 分钟的报告。查看不消耗行动格，也不自动解决事件。

### 5.2 五个实际事件

| ID / 类型 / 地点 | 参与者 / cost | 玩家合法选择 | 精确结果与未选结果 | Future consumer |
| --- | --- | --- | --- | --- |
| `E1_BOUNDARY_TALK` / 关系 / Hall | Engineer+Courier / 1 | A 承诺今后任何高负荷先说安全包络；B 只承诺不隐藏未知；C 延期 | A 写 `PROMISE_PREVIEW_ENVELOPE`；B 写 `BOUNDARY_STATE_UNKNOWNS`；C 写窗口延期；未选则下一任务仍显示“未谈清” | `TEST_CONSUMER_HUB_MISSION_A` 的风险表达 |
| `E2_REPAIR_WINCH` / 维修 / Bay | Engineer / 1 | A 用 2 材料彻修 `winch=normal`；B 用 1 材料临修 `winch=limited_to_low_load`；C 不开工 | A/B 均需试验通过才提交；C 不扣材料；未选保持 degraded | `TEST_CONSUMER_HUB_MISSION_A` 的可用动词 |
| `E3_CURATE_RECORDER` / 展陈 / Archive | Archivist / 1 | A 保留封存；B 展示获准的外观与来源；C 发起归还请求 | 只改 reveal/display/return_request；不公开内容、不改 owner；未选继续 withheld | `TEST_CONSUMER_HUB_MISSION_B` 的保管条件 |
| `E4_TRACE_DELAYED_REPORT` / 调查 / Archive | Archivist / 1 | A 追时间戳；B 校验路线来源；C 保留 unresolved | A 把报告时效从 stale 缩到 `observed_at=T-40m`；B 证明安全路线仍可用；C/未选保留未知 | 两张任务卡的 `information_sources` |
| `E5_PREPARE_ONE_KIT` / 准备 / Terminal | Quartermaster / 1 | A 预留 `KIT_LOAD_SENSOR`；B 预留 `KIT_SEALED_CASE`；C 不预留 | A 只服务 Mission A；B 只服务 Mission B；两件不可同时装入唯一工具位 | 已选任务的部署与结算 |

冲突图为 `E1 ! E2`、`E3 ! E4`；行动格为 `sum(slot_cost)<=3`。合法投资组合示例：`E1+E3+E5`、`E1+E4+E5`、`E2+E3+E5`、`E2+E4+E5`。它们不是固定解；只证明三格下不存在“清空五事件”路线。

非法选择：同时提交 E1/E2 或 E3/E4 `E_ACTOR_CONFLICT`；第四格 `E_ACTION_BUDGET`；用材料购买关系结果 `E_DOMAIN_CURRENCY`；未经 E3 转移 recorder 所有权 `E_CUSTODY`；把同一可选人物同时排到 Hub 事件和任务 `E_ROSTER_TIME_CONFLICT`。

### 5.3 两张完整任务卡

| Schema field | `MISSION_HUB_A_SPILLWAY` | `MISSION_HUB_B_RETURN_RECORDER` |
| --- | --- | --- |
| `mission_id` | `TEST_MISSION_HUB_A@v0.1` | `TEST_MISSION_HUB_B@v0.1` |
| `authority_status` | `candidate_game_design` | `candidate_game_design` |
| `need_and_primary_verb` | `stabilize TEST_NORTH_SPILLWAY_RELAY / OBJ_STABILIZE` | `deliver OBJ_HUB_RECORDER to TEST_LOCAL_LIBRARY / OBJ_DELIVER_WITH_CUSTODY` |
| `location_and_design_pack` | `TEST_LOC_NORTH_RELAY / TEST_GD2_RELAY_v0.1 / PAPER_FIXTURE_ONLY` | `TEST_LOC_LIBRARY_DOCK / TEST_GD2_LIBRARY_v0.1 / PAPER_FIXTURE_ONLY` |
| `route_options` | `ROUTE_A_SHORT=2t, higher_load; ROUTE_A_DRY=3t, lower_load` | `ROUTE_B_DIRECT=2t, public; ROUTE_B_BACK=3t, custody_check` |
| `time_and_deadline` | `travel 2-3t; deadline 4t; return 2t` | `travel 2-3t; deadline 3t; return 2t` |
| `information_sources` | `REPORT_DELAYED observed_at=T-40m confidence=medium; E4 may validate route` | `CUSTODY_NOTE observed_at=T-1h confidence=high; contents remain unknown` |
| `expected_modes` | `world 3m; exploration 8m; engineering 8m; settlement 4m` | `world 3m; exploration 10m; relationship_or_custody 5m; settlement 4m` |
| `required_presence` | `ACTOR_HUB_FIELD_LEAD + BODY_HUB_TOW_RIG` | `ACTOR_HUB_FIELD_LEAD + OBJ_HUB_RECORDER in legal custody` |
| `optional_assignments` | Engineer: rated repair action; Courier: short-route familiarity | Archivist: source explanation; Courier: direct route |
| `opportunity_cost` | optional actor cannot have been used by E1/E2/E4 as applicable; selecting A leaves B to named executor | optional actor cannot have been used by E1/E3/E4; selecting B leaves A to named executor |
| `known_risks` | degraded/limited winch cannot take higher_load; delayed report may make short route stale | direct route exposes unapproved recorder exterior to public; unsealed transport risks custody rejection, not item loss |
| `withdraw_and_failure` | withdraw to hub with relay unchanged; partial isolates relay but does not recalibrate; no random death | withdraw keeps custody; partial delivers late and creates new return appointment; no ownership transfer |
| `possible_outputs` | relay state; tow-rig body state; route report; repair debt | custody receipt; relationship response; recorder location; reveal unchanged |
| `unselected_executor` | `TEST_TEAM_LOCAL_DIKE`, capability=isolate_only | `TEST_TEAM_LIBRARY_COURIER`, capability=delayed_pickup |
| `unselected_outcome_band` | deterministic `partial`: isolate at T+4, recalibration remains future Need | deterministic `delay`: pickup at T+2, current custody continues |
| `future_consumers` | `TEST_CONSUMER_HUB_MISSION_A;TEST_CONSUMER_SET_HUB` | `TEST_CONSUMER_HUB_MISSION_B;TEST_CONSUMER_EX3_ARCHIVE_REVIEW` |
| `human_acceptance` | `none / pending` | `none / pending` |

`PAPER_FIXTURE_ONLY` 为显式阻断值；未来实现者可按本表搭数据场，但未生成真实包 hash 前不得进 Build 验收。

### 5.4 操作流、结局与回写

1. `REVIEW_CHANGES`：免费查看三处变化。
2. `PREVIEW_EVENT`：显示参与者、知识范围、行动格、冲突和未选结果。
3. `DRAFT_EVENT_CHOICE`：可在整组提交前取消；不扣格、不跳时间。
4. `PREPARE_HUB_BATCH`：所有 Owner 验证岗位、资源、保管和揭示。
5. `COMMIT_HUB_BATCH`：一次提交已选事件；未选事件生成具名延期/保持回执。
6. `COMPARE_MISSION_CARDS`：两张卡都显示已提交 Hub 结果的差分。
7. `COMMIT_MISSION_AND_DEPART`：只选一张；另一张在同一事务中登记预告的 unselected outcome。

| 结局 | 条件 | 状态结果 |
| --- | --- | --- |
| `clear` | 已选任务通过全部 Owner prepare，且 `departure_limitation_codes={}` | `ST_HUB_ACTION/ST_ROSTER/ST_ROUTE/ST_RESOURCE` 与各事件 Owner diff 原子提交；另一卡生成 unselected receipt |
| `partial` | 已选任务通过全部 Owner prepare、可以合法出发，且 `departure_limitation_codes` 至少含一项具名限制 | 依然出发；在卡面和结算中携带已预告限制，不偷换成 clear |
| `withdraw` | 在任务提交前退回 Hub | 已提交的 Hub batch 保留；任务、路线、出击岗位与时间不提交；可继续同一 cycle |

终局按固定优先级判定，避免同一状态同时满足 clear 与 partial：先判 `withdraw_before_mission_commit`；再做 Owner prepare，失败时留在 Hub 并返回拒绝码、不是任何终局；prepare 通过后，若 `departure_limitation_codes` 非空则必为 `partial`，只有空集才是 `clear`。本 Fixture 允许的限制码只有 `LIM_WINCH_LOW_LOAD`、`LIM_ROUTE_STALE`、`LIM_OPTIONAL_ACTOR_UNAVAILABLE`、`LIM_REQUIRED_KIT_MISSING` 与 `LIM_PUBLIC_CUSTODY_EXPOSURE`，每项都必须在出发前由对应事件／任务卡输入确定。合法岗位、路线和保管只是 clear/partial 的共同前提，不再足以单独判 clear。

### 5.5 测试断言

- 列表始终恰好 5 个事件与 2 张任务卡；行动预算恰好 3，不能通过资源增加。
- 冲突图阻止 E1/E2 和 E3/E4 同时提交；即使三格未用满，也不允许同一人并行多岗。
- 任意合法 Hub 组合后至少一张任务卡可由 `ACTOR_HUB_FIELD_LEAD` 提交，不存在被选项锁死的必败状态。
- 选 A 时 B 必须产生固定的未选执行者和结果，反之亦然；无随机惩罚。
- 所有提交前冲突在卡面可见；不得在点击出发后才告知角色已被占用。
- 对同一 prepare snapshot，`departure_limitation_codes={}` 与非空互斥；分类器只能返回一个 terminal ID。删掉任一限制来源后必须确定性重算，不能由结算页人工改名。

## 6. P-SET1《信标回收行动》三级结算回放

### 6.1 中性章节初态

`chapter_id=TEST_CHAPTER_SETTLE_01`，`operation_id=TEST_OPERATION_BEACON_01`，包含两个 Encounter。该章没有剧情文本，只有一条用来防止玩法覆写的合成 hard guard：`TEST_HARD_GUARD_ROUTE_OPEN_IF_OPERATION_RECEIPT_VALID`。

| Owner / 状态 | 初态 |
| --- | --- |
| `SOG-NARR / ST_OPERATION` | `encounter=E1;phase=P0;resolution=pending`；不允许 Phase 当 Mission Clear |
| `SOG-BODY / ST_BODY` | `BODY_SET_TERN.winch=normal;integrity=normal` |
| `SOG-BODY / ST_EQUIPMENT` | `OBJ_SET_CASE.owner=TEST_LOCAL_OWNER;custody=TEST_LOCAL_OWNER;installed_state=none` |
| `SOG-WORLD / ST_ROUTE` | `ROUTE_SET_RETURN.open=false;deadline=T+4` |
| `SOG-EXPL / ST_EVIDENCE` | `EVID_SET_SIGNAL_STRENGTH=uncollected` |
| `SOG-NARR / ST_KNOWLEDGE` | `PLAYER/ACTOR_A/ACTOR_B/PUBLIC` 都不知信号来源；`BACKEND_TEST_ORACLE` 保有 `CLAIM_SET_ORIGIN=maintenance_drone` |
| `SOG-REL / ST_CONSENT` | `CONSENT_SET_SCAN` 只绑定“扫描信标外壳”，不授予带走或公开内容 |
| `SOG-C2 / ST_AUTHORITY` | `AUTH_SET_CASE_LOAN_OFFER`：grantor=`TEST_LOCAL_OWNER`，grantee=`TEST_OPERATION_PARTY`，scope=`temporary_sealed_custody_until_T+4;transport_to_TEST_HUB;return_required`，truth/player projection=`active/signed`；不含 ownership、公开内容或转授权 |
| `SOG-SETTLE / ST_RESOURCE` | `operation_supply=3` |

E2 接触记录盒时必须先出现两个并列选择：`LEAVE_CASE_LOCAL` 保持 owner/custody 均为 `TEST_LOCAL_OWNER`；`ACCEPT_TEMPORARY_CUSTODY` 才可请求临时带回。本文三条主 Trace 中的 clear/partial 明确选择后者，但该选择只有经过以下 prepare 链才合法：

1. `SOG-C2` 核验 `AUTH_SET_CASE_LOAN_OFFER` 的 grantor、scope、期限与目标物，产生 `PREP_SET_CASE_AUTH`；
2. `SOG-BODY` 核验唯一实例、当前 custody、封签与目的地，产生 `PREP_SET_CASE_BODY`，其 proposal 只含 `custody TEST_LOCAL_OWNER→temporary_party`，owner 保持不变；
3. `SOG-REL` 对玩家明确接受的归还义务 prepare `PROMISE_SET_RETURN_CASE`；扫描 consent 不参与这一步，也不能替代它；
4. 三张 prepared receipt 的 `proposal_hash` 一致时由 `SYS-SETTLE` 原子 commit。任一缺失、过期或拒绝，盒子留 local、归还承诺不生成，其他资源／身体 diff 也不得部分提交。

因此“拿到盒子”不是 E2 clear/partial 的默认奖励；它是有具名 owner offer、玩家选择、三 Owner prepare 和原子回执的可选结果。

### 6.2 固定 Partial Trace：Encounter → Operation → Chapter

本表是人类测试的主回放：一个 Encounter clear，一个 Encounter partial，以便三级结算都有真实内容，而不是三张重复奖励页。

| 级别 / receipt | 必须读取 | 只在该级提交的 diff | 玩家摘要 | Future consumer |
| --- | --- | --- | --- | --- |
| `ENCOUNTER E1 / TX_SET_E1_CLEAR` | E1 objective；信标外壳变化；补给消耗；扫描同意 | `E1 resolution=clear`; `supply 3->2`; 玩家与 ACTOR_A 获得“信号强度高”证据；下一场携带 | “信标已稳定；用了 1 补给；来源仍不知。” | `TEST_CONSUMER_SET_NEXT_ENCOUNTER` |
| `ENCOUNTER E2 / TX_SET_E2_PARTIAL` | E1 receipt；E2 objective；绞盘与保管变化；`PREP_SET_CASE_AUTH/BODY` 与玩家接受归还义务；敌方实际可观察动作 | `E2 resolution=partial`; `winch normal->limited`; 在同事务中提交三张 prepared receipt，使 `case custody local->temporary_party` 但 owner 不变；记录对方观察过 tow 动作 | “记录盒依有效借管回执临时带回；牵引绞盘限制；对方看到牵引动作。” | `TEST_CONSUMER_SET_HUB` |
| `OPERATION / TX_SET_OP_PARTIAL` | 两个 Encounter receipts；回程；借管 authority receipt；保管；维修需求 | `operation=partial`; `ROUTE_SET_RETURN false->true`; 延续已提交的 `PROMISE_SET_RETURN_CASE`，另生成 `WORKORDER_SET_WINCH` 与一个 Hub 可见回应窗口；不在此层补造 custody | “做成：稳定信标。带回：有期限借管的记录盒。欠下：修绞盘、归还盒子。” | `TEST_CONSUMER_SET_HUB` |
| `CHAPTER / TX_SET_CH_PARTIAL` | Operation receipt；hard guard；角色/机体/地点/路线/知识/保管/对方观察的完整表 | 提交合成 hard result `TEST_ROUTE_AVAILABLE=true`；保持 owner/custody 分离；等级不变；信号来源仍为 unknown；下一 Need=归还与复核 | “章结果：返程开放。身体债：绞盘受限。保管债：盒子待还。未知：信号来源。” | `TEST_CONSUMER_SET_NEXT_CHAPTER` |

Encounter 不能写持久世界开放、章结果或全章关系总结；Operation 不能投票改变 hard guard；Chapter 不重扣两个 Encounter 的补给，也不把 temporary custody 写成 ownership。

### 6.3 Clear / Partial / Withdraw 三组数据

| Trace | Encounter receipts | Operation receipt | Chapter receipt |
| --- | --- | --- | --- |
| `SET_TRACE_CLEAR` | E1 clear；E2 clear（绞盘 normal，盒子临时保管） | clear；回程开；无维修债；有归还债 | hard guard 合法封章；下一 Need=归还 |
| `SET_TRACE_PARTIAL` | 使用 6.2 的 E1 clear + E2 partial | partial；回程开；有维修与归还债 | hard guard 仍封章；partial 过程差分保留 |
| `SET_TRACE_WITHDRAW` | E1 withdraw；只保留已观察信号强度；不取盒子 | withdraw；返回来路；无保管或维修债 | 不触发；`E_CHAPTER_HARD_RESULTS_MISSING`，保留 Operation 检查点 |

### 6.4 知识遮罩矩阵

| Claim | Encounter 后 PLAYER | Encounter 后 ACTOR_A | Encounter 后 ACTOR_B | Operation 后 PUBLIC | Chapter 后 PUBLIC | Oracle |
| --- | --- | --- | --- | --- | --- | --- |
| `CLAIM_SET_SIGNAL_STRONG` | observed + source | observed + source | unknown | unknown | 可公开为“信标可用”，不显原始数值 | true |
| `CLAIM_SET_CASE_RECOVERED` | 仅在三 prepare 已 commit 后为 observed | 同左 | Operation 后收到 summary | `temporary_custody_under_AUTH_SET_CASE_LOAN_OFFER` | 同左 | true |
| `CLAIM_SET_ORIGIN` | unknown | unknown | unknown | unknown | unknown | `maintenance_drone` |
| `CLAIM_SET_ENEMY_LEARNED_TOW` | 只显“动作可能被观察” | 同左 | unknown | unknown | 只在合法伏笔/战后条件满足时显示 | true |

任一层的玩家摘要、Full 演出、Skip 演出、存档 snapshot 与事件日志都不得含 `CLAIM_SET_ORIGIN` 的 oracle value。

### 6.5 幂等、原子性与负向断言

| 用例 | 操作 | 预期 |
| --- | --- | --- |
| `IDEMPOTENT_SAME` | 同 `transaction_id + payload_hash` 重放 1000 次 | 返回同 receipt ID / commit hash；state version 只 +1；补给只 -1 |
| `ID_COLLISION` | 同 ID 把 E2 `partial` 改为 `clear` | `E_ID_COLLISION`；0 write；原 receipt 不变 |
| `CUSTODY_WITHOUT_PREPARE` | 省略任一 `PREP_SET_CASE_AUTH/BODY/PROMISE` 或不选择 ACCEPT 就请求 temporary custody | `E_PREPARED_OWNER_MISSING` 或 `E_CUSTODY_CHOICE_MISSING`；盒子保持 local；整组 0 write |
| `OWNER_REJECT` | 尝试把盒子 owner 改成 party | `SOG-BODY/ARCH reject E_CUSTODY`；整组 0 write；资源/身体也不部分提交 |
| `PHASE_IS_NOT_CLEAR` | 以 `phase=P1_done` 直接请求 Operation settlement | `E_ENCOUNTER_RECEIPT_MISSING` |
| `OUT_OF_ORDER_CHAPTER` | 没有 Operation receipt 封章 | `E_OPERATION_RECEIPT_MISSING` |
| `KNOWLEDGE_LEAK` | 向三个非 oracle observer 生成投影 | `CLAIM_SET_ORIGIN` value 字段数必须为 0 |
| `FULL_SKIP_EQUIV` | 同一 result 分别 Full / Skip | `state_hash;receipt_hash;event_queue` 全部相同 |
| `REBUILD` | 从空状态按 commit order 重放 | rebuild hash = stable snapshot hash |
| `CONSERVE` | 回放所有三组 Trace | 资源不负；唯一盒子只有一个 custody；无重复岗位；hard guard 不被 score 覆写 |

## 7. 给未来实现者的五张任务卡

这些是获得用户 Candidate 原型授权后才能开始的任务，本文本身不提供授权。

| 原型 | 最小实现物 | 必须先自动通过 | 不得偷换的人测问题 |
| --- | --- | --- | --- |
| P-EX1 | 6 节点、3 路线、3 人物、2 可观察事实、clear/partial/withdraw receipts | 可达、无非法瞬移、输出门、幂等、静态无障碍 | 玩家是否靠地标导航且记住人物/事实 |
| P-EX2 | 证据板、3 变量求解器、安全预览、物理反馈、report receipt | 公式确定性、不安全阻断、Owner 分离、Full/Skip 等价 | 玩家是否真能解释证据与修正，而不是背配置 |
| P-EX3 | 同场两访、5 知识节点、2 假说、1 矛盾、observer projections | 揭示防泄、无 inventory key、节点上限、路线只读 knowledge receipt | 第二次改变是否被理解为知识因果 |
| P-HUB1 | 5 事件、2 任务卡、3 行动格、冲突预览、unselected executor | 冲突图、不死锁、事务原子性、任务 schema、无障碍 | 玩家是否能复述谁在哪、放弃什么与下一场差异 |
| P-SET1 | 三 Trace、三层 UI、Owner prepare/commit、知识遮罩、重放工具 | 全部 6.5 断言与既有 AUTO-SET/AUTO-TX/AUTO-KNOWLEDGE 门 | 玩家是否能分清做成、没成、带回、欠下和下一消费者 |

## 8. 仍然未完成

- 没有 Build、代理场景、UI、状态核、自动测试、真实 `content_hash`、录像、目标玩家数据或用户玩法验收。
- 五个 Fixture 只表明内容输入足以进入程序拆分，不表明有趣、好懂、无障碍或可复用。
- P-EX1/2/3 仍需第二个纯数据实例；未证明“不新增顶层代码、输入、主 UI 和存档域”前，不得宣称辅助系统成立。
- 只有用户批准对应 Candidate 原型范围和执行包后，才能把这些数据实现、进人测或用结果影响系统取舍。
