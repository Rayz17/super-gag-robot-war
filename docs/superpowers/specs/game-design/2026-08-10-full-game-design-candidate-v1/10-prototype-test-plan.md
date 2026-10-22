# 原型、平衡、可用性与真人验收计划

> Status: candidate_validation_plan_defined / prototypes_and_human_evidence_pending
>
> Scope: D03-D09全部玩法、状态、章节适配、可访问性与生产门
>
> Rule: 自动测试证明“按规则运行”，真人测试证明“人能理解并觉得值得玩”，用户回执决定“是否继续投资和迁移”。三者不能互相代签。

## 一、主裁决

当前不能直接制作“前三章完整玩法”，也不能把C01E02 Demo当成基础战棋答案。验证必须先回答最危险、最便宜推翻的问题：

1. 不使用主角权能时，机器人身体、地形、目标、敌方意图和反应是否本身有趣；
2. 交替、短WEGO、混合和传统阵营回合中，哪些基础版本不成立、哪些值得进入shortlist；
3. shortlist各版承载同一最小核心C2后，哪一种才值得由用户选择、返修或全部退役；
4. 最终时制下的完整C2是否真正改变信息、路线、许可、同意和工程可行性，而不是换皮Buff；
5. 探索、工程和知识玩法是否轻、短、可复用，并把具体结果送回人物/世界；
6. Hub与三级结算是否形成长线闭环，而不是一堆菜单和资源；
7. 通用系统通过后，C01-C03的Accepted Story能否在不改人物选择和章末事实的前提下成为游戏。

因此D10不是“测试清单”，而是一套淘汰机制：任何原型无法产生两种有意义方案、玩家无法复述因果、第二个内容实例必须加新UI/新输入，或结果不回写共同状态时，都应删除、合并或回到最早设计层。

## 二、机制证据等级

本包沿用M0-M6作为“机制证据”，但它和旧multi-play文件中名为M1-M6的工程里程碑不是同一含义：

| 等级 | 必需证据 | 允许声称 | 不允许声称 |
| --- | --- | --- | --- |
| M0 名词 | 名称或问题存在 | 需要设计 | 有规则 |
| M1 边界 | 身份、职责、Canon禁止项、输入输出方向 | 设计边界清楚 | 玩家能操作 |
| M2 规则 | 动词、信息、选择、代价、反制、失败、回写、资产与原型问题完整 | 可提交隔离原型授权申请 | 有趣、可生产或已经获得测试授权 |
| M3 技术证明 | 纸面模拟、Schema、确定性/事务/非法输入等自动证据 | 规则可被实现并按合同运行 | 人能理解 |
| M4 内部可玩 | 版本化灰盒、内部QA、录像/日志、已知缺陷 | 可交冷启动测试 | 目标玩家喜欢 |
| M5 真人证据可裁决 | 冷启动目标玩家证据、复述、方案、偏好、失败样本与完整版本绑定 | 指定版本/范围可提交用户作保留、返修或淘汰裁决 | 已获用户批准、第二内容实例或量产成立 |
| M6 复用与集成 | 第二个数据化内容实例、长线状态/存档/回归、正式生产授权 | 系统可进入受控量产 | 全游戏或L6自动成立 |

若版本、规则、地图、教程、UI或视觉线索发生会影响理解的变化，旧M5不能自动覆盖新版本。

证据等级只描述“材料成熟到哪一步”，不授予下一步执行权。M5明确止于“真人证据可交用户裁决”。P1 A/B/C/D 的 M5 只允许淘汰或形成shortlist，不能选胜者；shortlist必须再经过最小核心C2 crossover，用户才可通过DEC-03-M作`select / revise / no_selection / retire_all`裁决。任何M2→M3/M4实现仍须先满足D12对应的`candidate_test_entry`决策回执、依赖门和隔离范围，并实例化[data/candidate-test-execution-envelope-schema.tsv](data/candidate-test-execution-envelope-schema.tsv)所定义的执行包络；本包当前没有有效回执或执行包络实例。

## 三、原型组合与依赖顺序

~~~mermaid
flowchart LR
    K["V0 共用测试核：快照/事务/日志/输入/回放"] --> SET["V0.5 Encounter/Operation/Chapter结算"]
    K --> P1["V1 D04-P1 基础战术A/B/C/D"]
    K --> EX1["A1 微型自由探索"]
    K --> EX2["A2 调查/工程实证"]
    K --> EX3["A3 知识重访"]
    P1 --> S["V1.5 P1只淘汰/shortlist"]
    S --> X["V2-X 最小核心C2可撤销crossover"]
    X --> D3["用户DEC-03-M：select/revise/no_selection/retire_all"]
    D3 --> P2["V2-Full 完整有限信息与角色C2"]
    P2 --> P3["V3 D04-P3 多阶段巨构"]
    EX1 --> HUB["A4 回馆一夜"]
    EX2 --> HUB
    EX3 --> HUB
    SET --> HUB
    D3 --> CH["C01-C03章节适配灰盒"]
    P2 --> CH
    P3 --> CH
    SET --> CH
    CH --> VS["开局垂直切片与量产证据"]
~~~

### 3.1 可并行但不能越门

- R0共用测试核先用独立implementation包络到M3；P1另建包络，仅含A/B/C/D四个匿名Build，`max_total_builds=4`不包含R0；探索Spatial内核、Evidence内核和结算事务测试可在各自授权后并行；
- P-SET1先完成机器夹具和幂等/泄密门，再进行结算真人理解测试；它不必等待P1；
- P2的语义/UI纸面设计可并行；P1四版M5后只能形成shortlist，随后必须用独立implementation与human_run包络制作可撤销`D04-P2-CROSSOVER`；
- 完整`D04-P2`必须等crossover M5与用户DEC-03-M选择唯一时制后才可制作；crossover不得借P1包络、不得进入章节或保留跨Session状态；
- P3地图/持续状态纸面设计可并行，但必须等P1/P2规则冻结后才进Runtime；
- C01E02 Demo继续独立，只提供指定切片的人机交互证据；
- C01-C03内容适配只能在相应通用内核达到M5后进行；
- 正式资产、配音和高成本动画必须等内容实例M5及视觉方向回执。

## 四、共用测试协议

机器用例见 [data/playtest-cases.tsv](data/playtest-cases.tsv)，证据账见 [data/acceptance-evidence-registry.tsv](data/acceptance-evidence-registry.tsv)。

每次测试必须先冻结：

~~~text
test_run_id
case_ids
prototype_id
build_id
content_manifest_id
ruleset_version
map_or_scene_version
tutorial_version
ui_version
asset_authorization_state
source_snapshot_ids_and_hashes
participant_cohort
facilitator_script_version
telemetry_schema_version
known_issues
~~~

上述冻结清单仍只是批次定义，不是一场真人Session。每名参与者、每个连续Session必须另建一行 [human-playtest-session-instances.tsv](data/human-playtest-session-instances.tsv)，严格匹配112字段 [Session实例Schema](data/human-playtest-session-instance-schema.tsv)，并同时绑定已授权`human_run`包络、已通过Preflight、冻结Build/规则/地图/Case/主持/隐私hash、匿名参与者ID、首次接触资格、提示污染、行为/复述/偏好、退出/不适和全部证据artifact hash。[原结果Schema的39字段](data/playtest-session-result-schema.tsv)已由 [crosswalk](data/human-playtest-session-result-crosswalk.tsv) 无损纳入，不能再用一张无授权/无hash的结果表代替Session实例。

主持与隐私的逐字最低骨架、H0-H4提示污染规则、退出/删除处理、证据有效性和用户裁决边界见 [真人Session证据链合同](validation/d10-human-playtest-session-evidence-chain-v0.1.md)。当前实例表为空，[program status](data/human-playtest-program-status.tsv)为`0 participant / 0 session / not_run`；这不是待填的虚拟证据。运行 `python3 docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/scripts/check_d10_human_playtest_sessions.py` 校验零状态，`--self-test`只做内存故障注入，不接触真人或生成同意。

`playtest-cases.tsv.applicable_prototype_ids` 可以列多个真实Registry ID，表示同一测试定义必须逐原型执行；每次Session仍只能记录一个精确 `prototype_id`，且它必须属于该Case的适用列表。一次PASS不得覆盖整个列表。

对 `test_kind=automated` 的用例，`prototype-test-registry.tsv.machine_case_ids` 与 `playtest-cases.tsv.applicable_prototype_ids` 必须构成完全相等的 `(prototype_id, case_id)` 集合；任一方向单边登记均为不可执行合同。真人、章节冷测与无障碍用例只从 `playtest-cases.tsv` 绑定，不进入名称明确限定为机器用例的 `machine_case_ids`。从项目根目录运行 `python3 docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/scripts/check_d10_test_registry_bijection.py`，同时校验该双向不变量、ID唯一性、引用解析、TSV列宽和Prototype依赖DAG。

所有非仪器Prototype至少必须有一个非自动Case，且每个非自动Case必须进入证据账。否则即使Prototype表写了`sample_min`和`M5`，也没有可执行Session能让它达到该等级。三个章节接缝因此分别使用`HUM-PC01-SEAM`、`HUM-PC02-SEAM`、`HUM-PC03-SEAM`，不能再借八个单话Case或最终垂直切片代签。

`prototype-test-registry.tsv.dependency_refs` 只接受带类型引用：`prototype:<ID>@M0..M6`、`gate:<ID>`、`gate:<ID>@scope=<scope>`、`deliverable:<ID>`、`decision:<ID>@approved_for_candidate_test|approved_for_bounded_migration` 或 `evidence:<ID>`。自然语言依赖、斜杠合并ID和未登记别名一律不能解锁下游。

### 4.1 测试者分层

| 层 | 用途 | 可否通过人类门 |
| --- | --- | --- |
| 设计者自测 | 找崩溃、明显死路、脚本错 | 否 |
| 内部非设计者QA | 检查任务是否可完成、日志是否可信 | 否 |
| 类型熟悉冷启动玩家 | 判断深度、可读性和策略空间 | 是，必须记录其类型经验 |
| 类型不熟悉但目标受众玩家 | 判断教学、信息负担和故事吸引力 | 是 |
| 无障碍专项测试者 | 判断视觉、听觉、动作、认知替代方案 | 对对应范围是 |
| 用户 | 决定产品方向、保留/返修/淘汰和投资 | 必须，但不能替目标玩家样本 |

每个最低6人方向性样本优先包含：

- 2名常玩SRPG/策略游戏者；
- 2名偏剧情、但接受中高复杂度战术者；
- 2名主要玩叙事/冒险、愿意学习主玩法者。

“冷启动”必须同时满足：未读设计文档、未玩该原型、未看该场录像/答案、不是作者/制作人/QA/项目组成员。项目成员只计仪器烟测。

### 4.2 样本口径

- 单一规则灰盒的方向性冷测最低6名目标玩家；这是小样本停止门，不是统计学终审；
- 第二个内容实例最低5名新冷启动玩家，不能只让已经学会第一例的人复测；
- 重大时制A/B/C/D的第一印象需要每版至少6次真正的首次接触，优先24名不同玩家；
- 可另用至少8名回访玩家做平衡不完全区组比较，但回访数据不能计入“冷启动理解”；
- P2 crossover对每个shortlist carrier另需至少6名未参加P1冷启的新玩家，并以至少8名回访者做平衡顺序比较；
- 迭代后影响规则、UI或教程的版本至少补一批未见旧版的新玩家；
- 开局垂直切片进入量产前，建议12-18名目标玩家覆盖类型熟悉/不熟悉、键鼠/手柄和至少一轮无障碍配置。

### 4.3 共用指标与预注册裁决

| ID | 维度 | 定义 |
| --- | --- | --- |
| U-COMPLETE | 可用性 | 无主持人代做时完成Primary或进入合法partial/withdraw |
| U-RESCUE | 可用性 | 主持人提示次数、等级和位置 |
| U-INPUT | 可用性 | 误操作、撤销、模式迷失、错误目标 |
| L-CAUSE | 学习 | 能解释三个关键结果为何发生 |
| L-TRANSFER | 学习 | 能把规则用于未见小变体 |
| S-DIVERSITY | 策略 | 真正不同的行动图/代价族，不把数值微调当第二解 |
| F-REPLAY | 趣味 | 固定故事结局下仍愿换方案再玩 |
| F-BODY | 产品身份 | 机器人具有质量、姿态和功能身体的1-7分 |
| F-AGENCY | 代理权 | 过程选择确实改变代价/状态的1-7分 |
| B-PLAN | 负担 | 教学后每脉冲规划中位时长 |
| R-FREE | 复述 | 0-5自由复述分 |
| R-STORYPLAY | 适配 | 能分清固定故事结果与玩家改变的过程 |
| T-STATE | 技术 | 存读档、Full/Skip、重放和事务hash一致 |

自由复述评分：0无法说明；1只记输赢/动画；2说出目标和结果；3说出自己的关键选择；4说出物理/信息/人物因果链；5还能说出伤损、责任、保管或下一消费者。不能用画面喜好抵消因果看不懂，也不能用完成率抵消只有一条强制路线。

日常原型仍不强制合成一个总分。唯独多Scheduler比较必须在看数据前冻结权重与硬阈值，避免事后挑指标：P1权重为`L-CAUSE .22 / S-DIVERSITY .18 / F-BODY .18 / B-PLAN .12 / F-REPLAY .10 / U-COMPLETE .08 / R-FREE .07 / production cost .05`；P2 crossover另用`L-CAUSE .20 / F-AGENCY .20 / B-PLAN .15 / S-DIVERSITY .15 / U-COMPLETE .10 / F-BODY .10 / R-FREE .05 / production cost .05`。权重只在全部硬门通过者间形成shortlist／比较取舍，不得把未过硬门者靠加权平均救回，也不得自动产生胜者。精确机器口径见 [time-system-neutrality-contract.tsv](data/time-system-neutrality-contract.tsv)。

### 4.4 主持规则

主持人在任务开始后不得：

- 解释最佳路线、敌方规则、角色权能含义或失败原因；
- 指着UI告诉玩家下一步；
- 把沉默解释为理解；
- 在复述前替玩家补因果；
- 用“这只是灰盒”否定玩家对清晰度和节奏的真实反应。

允许的帮助只有已登记的分级提示。每次提示必须记录触发时刻、玩家卡住的状态和提示层级；需要主持人口头解释核心规则即视为教程失败。

首批三人出现以下任一情况，立即暂停该版本，不继续浪费样本：

- 两人无法解释同一个关键结果；
- 两人把误操作当成战术失败；
- 三人都走同一强制动作序列；
- 一个决策脉冲连续两次超过6分钟；
- 同步或权限结果必须由主持人逐帧/逐句解释；
- 出现坏档、不可恢复输入、状态hash漂移或故事固定事实被改写。

## 五、V1：基础战术四时制中立筛选

### 5.1 冷启动设计

P1-A、P1-B、P1-C、P1-D使用完全相同的14×10中性世界初态、三台我方、五个敌方、疏散车、样本、地形、动作结果、目标、AI Doctrine和未知信息预算。Scheduler及其原生命令／最小UI可以不同；信息内容、教程预算与底层语义不能不同。

这里的“同一底层语义”还包括世界时钟，而不只是一张相同地图。四版必须实现 [scheduler-clock-adapter-contracts.tsv](data/scheduler-clock-adapter-contracts.tsv) 的四个Adapter，并把 [d04-p1-adapter-event-vectors.tsv](data/d04-p1-adapter-event-vectors.tsv) 的28条纸面向量变成可执行用例：四个周期都恰好是32秒，自主对象每周期只走四个微刻度，桥基础tick、Deadline、观察刷新、Reaction过期和挥发资源重置各按合同发生一次。当前这些仍是`zero_build`纸面向量；在生成逐Adapter结果hash前，P1不得进入真人冷测，也不得用“相同动作Tempo”代替世界时钟公平性。

第一阶段为24个独立首次接触单元：

- A显意图交替激活：6名；
- B短脉冲WEGO：6名；
- C交替锁计划＋同步执行：6名。
- D传统阵营回合：6名。

第二阶段以至少8名回访玩家做平衡不完全区组，每人体验另外两版，用于比较偏好、身体交错感和工程成本；回访结果不能覆盖第一阶段理解数据。实现顺序固定为共享核→D→A→C→B；参与者和主阈值分析只见`TS-HARBOR / TS-EMBER / TS-LANTERN / TS-QUARTZ`，映射在主阈值分类锁定后才揭示。各版教程统一最多8分钟、12个引导输入、2次上下文提示、0次策略提示。

### 5.2 任务脚本

1. 无说明观察战场30秒，说出主目标和敌人可能要做什么；
2. 完成首个合法移动/朝向/动作/反应预留；
3. 在四个决策脉冲内让至少两辆疏散车撤离；
4. 选择是否保护桥或阻止样本被带走；
5. 失败或部分成功后，根据日志指出一个可改变的决定；
6. 完成后复述三次关键接触、一个身体状态和一个地形作用；
7. 询问是否愿意立即换一种方案再玩，不展示其他版本名字。

### 5.3 通过与淘汰

必须同时满足：

- 每版至少5/6能复述主目标、敌方意图和三次关键因果；
- 至少两类策略分别被两名以上玩家独立发现；
- 学会后的单脉冲决策中位数不超过3分钟，且没有玩家因“不知道当前能做什么”停滞超过90秒；
- 至少4/6愿意立即换方案复玩；
- 反应、朝向、功能损伤和撤离中至少三项被玩家主动用于决策，而不是只看伤害；
- Forecast与实际差异均能由提交时未知或过期信息解释；
- P1综合理解、节奏、方案多样、身体感、失误归因、复玩意愿和实现成本，只淘汰或形成shortlist，不按新奇度或单一胜率选胜者。

P1输出严格限定为`shortlist_two / shortlist_three / shortlist_four / no_winner / revise_top_two / retire_all`。只有前三种shortlist结果绑定carrier ID与证据hash后可进入crossover；`no_winner / revise_top_two / retire_all`都停止于P1、解锁0项，返修后须重跑受影响的P1证据。若四版都只产生同一路线、玩家主要等待动画，或关闭C2后无趣，D04必须退回基础规则，禁止进入crossover；`D04-P1-SHORTLIST`不得解锁章节、完整P2或DEC-03-M选择。

## 六、V2-X：最小核心C2 carrier/crossover

`D04-P2-CROSSOVER`让P1 shortlist中的每种Scheduler分别承载同一六项核心动作：`C2_RELAY_CONTACT / JICUN_ROUTE / BAIYUAN_PREVIEW / QIHAI_VERIFY_AUTH / LUHENG_VERIFY / SOUL_RESPONSE`。各carrier复用同一16×12镜像图、来源、许可、同意、反制、资源与窗末后态，只允许Scheduler原生语法/UI不同。

- 入口：`D04-P1-SHORTLIST@M5`且结果为`shortlist_two / shortlist_three / shortlist_four`，再加`DEC-03-A + DEC-04-A + GATE-GD1`；不要求也禁止伪造DEC-03-M；
- 每carrier至少6名新冷启，另至少8名回访者做平衡顺序对照；
- 每次Session后所有carrier patch必须清空且`reset_hash`相同；任一状态、教程、信息量或角色效果不等价立即停止；
- 通过只意味着可提交DEC-03-M。用户结果允许`select / revise / no_selection / retire_all`；只有`select`与真实DR-DEC03-M才解锁完整P2，其余结果均不解锁下游。
- 共用真值／六项C2语义漂移使全部carrier证据失效；单版adapter／UI漂移只使该carrier失效；`revise`后须重跑受影响证据，`no_selection / retire_all`解锁0项。

## 七、V2-Full：有限信息与完整角色C2

完整P2只复用DR-DEC03-M选择的唯一身体／时制规则核，使用两张布局镜像的同构地图，验证全部25项动作、Contact、通信、中继、带宽、四类权能和敌方干扰。最低12名新玩家分别体验C2开启/关闭，地图与次序交叉平衡；C2关闭时永远保留较慢、较危险但合法的身体路线。Crossover的六动作证据不能代签本阶段。

### 7.1 任务

1. 在八项分类题中把信息标为事实、估计、建议路线、权限状态、主体回应或未知，并指出来源/时间；
2. 在只允许三个C2席位、每脉冲两次介入的条件下完成救援；
3. 经历一次干扰、一次假接触、一次权限缺失和一次机魂条件接受/拒绝；
4. 至少一次选择“不使用”看似可用的权能；
5. 在两种命令顺序中选择并承担不同代价；
6. 复述谁提案、谁核验、谁授权、谁同意、谁用身体执行。

P2真人研究拆成同一批参与者的两个Session，不把25动作×四情境硬塞进一场45–60分钟任务：

- Session A为45–60分钟的C2开／关镜像战术与责任链复述；
- Session B为25–35分钟的平衡不完全区组动作语义测试，每人最多分配7个动作、每个动作至少3人，四个fixture使用短题而非再打一遍完整地图；
- 两场可分日执行；任一参与者出现明显疲劳、连续漏题或主持救援后，该人的Session B标`needs_review`，不得用“已完成25动作覆盖”掩盖无效样本；
- 25/25四情境自动可达是M3机器证据，真人层只判断动作语义、责任、忍住理由与缺席替代能否被理解，两者不得互相代签。

### 7.2 门槛

- 至少10/12在八项分类中答对七项，并指出来源和过期条件；
- 至少10/12能区分提案者、核验者、授权者、同意主体和执行者；
- 至少8/12主动忍住一次虽可点击但不划算的C2；
- 四类权能中至少三类在不同玩家方案中成为真实取舍；
- 至少三种不同席位组合形成合法结果；
- C2开启后的教学后规划中位时间相对关闭图增幅不超过30%；
- 至少8/12的F-AGENCY不低于5/7；
- 每类权能都出现“该用、该忍住、被克制”的证据；
- 条件预演偏差时至少5/6能从日志解释，不评价为作者作弊；
- 没有人把纪存理解成遥控、白鸢理解成确定未来、七海理解成万能权限、工程实证理解成提示答案；
- 没有权能成为每脉冲固定必按，去掉任一席位仍有更贵/危险但合法的替代。

失败优先返回GD1动作语义或信息UI；不能靠加教程文字掩盖能力本身重叠。

## 八、V3：多阶段巨构Operation

使用中性TEST_STRUCTURE_A，不绑定天空铸环或Current剧情。最低8名已掌握P1/P2的玩家；三个连续Encounter验证接近/选路、外部结构、内部/撤离；四种“缺一席位”配置各至少两次。保存部署、伤损、能源/弹药、Contact、权限/同意、结构节点、敌方学习和未偿目标。

门槛：

- 至少6/8达到clear或设计允许的partial；
- 至少两条跨阶段策略各被两名玩家完成，且三种终局方案均至少完成一次；
- 至少7/8能指出两项第一阶段选择怎样改变后两阶段；
- 不依靠HP阈值换皮，所有巨构变化可追溯到玩家提交动作；
- 任一阶段存取后所有Operation状态逐项一致；
- 任一主角席位不是唯一脚本钥匙；
- Full/Skip、暂停/恢复和重载的业务结果一致；
- 每个缺一席位配置至少有一次非脚本卡死完成；
- 第三个脉冲后规划中位数不超过4分钟；
- F-BODY和巨构尺度感中位数不低于5/7；
- 至少6/8愿意继续下一Operation。

若P3只是三张连续地图、阶段间只带一个分数或高潮过场替玩家完成，退回Operation/地图身体设计。

## 九、辅助玩法原型

### A1 微型自由探索

- 6名冷启动；15-20分钟；
- 至少5/6靠地标完成主目标，至少两条浏览路线被独立使用；
- 至少4/6记住一个具名人物、两个空间/机械事实；
- 无箭头也能找到集合点；跌落/迷路只有近点重置；
- 输出evidence、place familiarity和一个后续可见消费者。

### A2 调查/工程实证

- 6名冷启动；15-22分钟；
- 至少5/6说清三类证据如何支持/否定两种方案；
- 错案后知道下一步取证或调整，不评价为猜作者答案；
- 至少两种安全节奏成立；
- unsafe方案被权利人/物理证据阻止并解释；
- 输出finding、verified constraint、cost和未来消费者。

### A3 知识重访

- 6名冷启动；两次访问合计20-30分钟；
- 至少5/6说明第二次为何可通过，答案不能只是拿到钥匙；
- 能区分Fact、Inference、Contradiction和仍未知；
- 错误连接不制造假Canon，已学事实不清空；
- 结论在后续对话/路线/档案中被可见消费。

### A4 回馆一夜

- 3个行动格、5个候选事件、2张任务卡；
- 至少5/6能复述每个行动的机会成本，以及谁在做什么；
- 没有人认为必须清空全馆、跑遍房间或每日刷新；
- 至少两种优先序都能进入合法下一任务；
- 关系、维修、展陈、调查或准备至少三类结果在后续可见。

### A5 三级结算

- Encounter只提交战术事实，Operation清行动目标，Chapter写Roster/泊位/权限/世界路线；
- 同一结果重放100次不重复奖励、债务或知识；
- 至少5/6能区分“做成、未成、带回、欠下、谁以后消费”；
- Phase Checkpoint不得被识别或显示为Mission Clear；
- 信息卡不能把后台真相泄漏给玩家或所有角色。

三类辅助玩法首例达到M5后，必须分别通过 `P-EX1-R2`、`P-EX2-R2`、`P-EX3-R2`，用纯数据和既有内核制作第二个≤5-15分钟中性实例；对应真人Case为 `HUM-EX1-R2`、`HUM-EX2-R2`、`HUM-EX3-R2`。若需要新输入、主UI、存档域或结算页，则不能升M6。三个R2由DEC-06 Candidate测试授权覆盖，不得借C01-C03章节实例或其他决策回执替代。

## 十、章节适配验证

通用系统M5后按风险而非章号平均制作：

| 原型 | 只回答 | 上游失败返回 |
| --- | --- | --- |
| PC01-E01-EX1 | 固定导览中是否仍有轻松真实的空间选择 | GD2/探索内核 |
| PC01-E02 | Accepted救援/起身/战斗能否成为同一冲突；吸收Demo人机证据 | gameflow/P1，不改Reader |
| PC01-E04-CARRIER | 万机馆作为场景身体/护送目标是否可读，不误升自由母舰控制 | 万机馆GD2/GD3 |
| PC02-E01-QUALIFIER | 非致死、限时、两路线竞技是否有策略 | P1目标/AI |
| PC02-E03-KNOWLEDGE | 身体连续性证据与机魂来源未知能否清楚分开 | Evidence/Reveal/GD2 |
| PC02-E05-GIANT | C02E05巨构救援是否不堆同屏、不靠脚本高潮 | P3/GD2 |
| PC03-E03-C2 | 信息/许可/同意/叫停转折是否公平且不夺角色权利 | P2/GD1/gameflow |
| PC03-E04-VERIFY | 无敌军工程校准是否轻松且有两种节奏 | A2/GD2 |

三章另设连续接缝门：

- **PC01-SEAM**：至少5/6明白E01只下达撤离命令、E02才完成；E02→E03地图/小体/伤损不重置；关闭C2仍有两种基础战术；0人从UI误解为E04可自由驾驶万机馆。
- **PC02-SEAM**：至少5/6分别复述赛事3:2、事故结果和实体交割；Tournament Clear不治疗/回Hub/重置地图；若救援仍被复述为固定按钮列，适配失败。
- **PC03-SEAM**：至少5/6区分白鸢估计、本地知识、工程验证、权限和主体决定；停止第二锤来自可追溯新证据；工具不被理解为掉落装备；E01-E04工具/伤损/人物/馆体/城市状态连续。

接缝门各自使用一批至少6名未见该章灰盒的新玩家，Case不得复用单话冷测编号：C01=`HUM-PC01-SEAM`、C02=`HUM-PC02-SEAM`、C03=`HUM-PC03-SEAM`。同一人可在完成接缝后继续贡献整章疲劳观察，但必须在Session账中把“接缝判定”和“额外长测”分开，不能把前八个单话Case的人数相加冒充6名连续试玩者。

三个Seam通过后，每章再以至少6名未见章灰盒的玩家做不中断连续试玩，检查全章疲劳、一次只教一个新判断、整章因果复述和三级结算。

每个内容实例均需：

- Accepted Story hash和故事回执范围；
- GD1/GD2/GD3快照；
- Story unit→Operation/Encounter/玩家动词/Outcome映射；
- 实际地图/Previs/build版本；
- 至少两种玩家独立方案；
- Full/Skip同结果；
- 录像、输入日志、复述、方案分类和用户玩法/视觉回执；
- 明确排除对Reader、Canon、正式资产或全章L6的越权提升。

## 十一、自动与技术回归

### 11.1 当前技术种子

2026-08-10只读运行的五组smoke在Godot 4.7下通过：SRW Kernel确定性战斗、统一状态/事务/模式/存读档M1、本地匿名试玩记录器、C01E02五个稳定点恢复、旧Schema/Build/Fingerprint只读拒绝。它们可作为R0夹具，但不能证明D03-D06系统成立。

当前仍有关键缺口：

- RunStateStore是v1浅层Dictionary合并，缺owner、from-state、版本竞争、资源守恒和整笔预验证；
- OutcomeValidator主要验形状，未完整验证resource_changes语义；
- 通用SaveService直接写最终JSON，缺原子替换、备份恢复、内容hash和正式迁移；
- CombatResolver仍是简单确定伤害，不是WEGO事件队列、反应、碰撞和未知结果带；
- EnemyIntent直接读取完整单位态，没有Perception/Observation Snapshot；
- C01E02 deterministic_signature不覆盖完整战场、事件队列、损毁、意图和全部标志；
- 现有Recorder缺计划、Forecast、Resolve、AI观察、C2、目标变化和策略分类。

这些是“可复用种子”，不是“系统已经有一部分玩法”的证据。

### 11.2 强制自动矩阵

自动测试只负责可确定事实：

1. 相同初态＋相同计划连续重放100次，ResolutionLog和状态hash一致；
2. 每个决策脉冲存档再恢复，结果与未中断执行一致；
3. 非法路径、目标、费用、权限、同意、资源和冲突计划100%被拒绝，并有稳定原因码；
4. Forecast与Resolve共用规则核；差异只能来自提交时未知/过期状态；
5. Full/Skip、动画暂停/恢复和不同帧率不改变业务结果；
6. Encounter/Operation/Chapter事务幂等，重复提交不重复奖励、债务、关系或知识；
7. 资源不为负、预留不超额、状态迁移合法、删除/tombstone和回滚可审计；
8. Contact的来源、时间、置信度、共享范围和过期在存读档后保持；
9. 权限与同意绑定具体动作/对象/时窗，撤回后旧动作不能执行；
10. History/Candidate/未来秘密不能进入Current Writer、UI或Build投影；
11. gameflow的固定入口/出口与Accepted Story seed逐项一致；
12. build manifest的故事、ruleset、资产授权和来源hash一致。

补充压力门：

- 每个PR关键case重复100次；里程碑规则核以10,000次生成/重放验证0个语义hash分歧；
- Dictionary插入顺序、实体加载顺序、等距候选顺序至少扰动1,000种排列；
- 支持平台以同一输入trace重放，权威语义hash一致，表现帧无需字节一致；
- 存档在临时写、flush、rename、清理各点故障注入，必须100%保留最后完整档；
- 截断、乱码、缺字段、错类型、Schema/Build/Fingerprint不匹配全部fail-closed且不改原文件；
- 同事务ID同payload返回原receipt且不重写；同ID异payload必须报collision；
- 多域事务最后一项非法时整笔拒绝，前后state hash相同；
- 10,000个生成case验证资源非负/容量/唯一装备/岗位冲突/硬故事事实；
- Forecast隐藏世界双生测试：玩家投影相同，Forecast输出必须相同；
- AI改变其感知不到的后台真值后，Intent/plan hash必须不变；读取玩家未提交草案计数为0；
- Full/Short/Skip的事务ID与最终语义hash一致；
- 核心动作键鼠/手柄可达率100%，焦点陷阱0，每个未提交态都有取消路径。

测试核应分别计算truth_state_hash、observer_projection_hash、plan_hash、forecast_basis_hash、event_queue_hash和post_resolve_state_hash；不能再用不完整的单一签名代替全状态语义。

自动门失败时不得安排真人测试；真人反馈不能用来“接受”确定性、存档或状态污染Bug。

## 十二、平衡不是先调胜率

原型期优先观察：

- 方案多样性：是否只有一条路线/一项权能/一个单位是必选；
- 行动价值：某动词是否长期不被使用或无条件优于其他动作；
- 信息价值：玩家是否愿意为确认信息付成本，还是直接赌；
- 资源轨迹：能源、带宽、反应、维修和Hub行动是否形成真实取舍；
- 失败分布：失败来自误读、风险选择、执行错误还是作者未说明规则；
- 时间分布：观察、计划、执行、等待、重试各占多少；
- 身体表达：玩家是否用姿态、占位、保护、牵引、损伤，而不只追伤害；
- 故事同义：高效打法是否反而违背人物权利或固定故事结果；
- 长线回写：不同策略是否留下可读而不失控的伤损、债务、关系和世界状态。

不以50%胜率作为统一目标。教学关可以高完成率，开放战术原型可以多种partial；关键是失败原因公平、继续态有尊严、替代策略存在。

样本达到30局后使用以下报警线，不自动触发削数值：

- 同一决策类单一动作占比>70%：检查支配策略；
- C2合法窗口使用率>85%或<5%：检查必按/废技；
- 学会后Pulse中位>180秒或P90>360秒：检查规划负担；
- 看过Forecast后仍有>10%结果无法解释：检查预测/日志；
- 70%以上对局结束时某关键资源仍>80%上限，或50%以上对局中段前耗尽：检查资源意义；
- continuation_break>25%：检查目标、提示和检查点；
- 单一路线>70%且另一合法方案<20%：检查方案多样性。

至少20%录像由两名观察者独立编码策略族；一致率<80%或κ<0.7时先修分类规则，不能用不可靠标签调平衡。

## 十三、可用性与无障碍

所有原型从第一版就验证：

- 关键颜色同时有形状、图标、文字和声音，不靠红绿；
- 键鼠与手柄能完成全部核心动词；焦点顺序稳定；
- 所有短时窗口可暂停、延长或改为确认式；
- 字幕、战斗日志、信息来源、行动顺序和失败原因可回看；
- 动画可加速/跳过，Full/Skip业务结果一致；
- 简洁/标准/专家信息层只改变显示密度，不改变规则；
- 输入重映射、按住/切换、震动/闪烁/相机晃动有替代；
- UI缩放和常见分辨率下目标、来源、置信度、同意和权限不截断；
- 轻玩法首次理解后可委托/自动完成，关键第一次实证不能无反馈跳过；
- 教程不要求记隐藏公式、专有名词或上一章台词。

无障碍不是最后一轮补丁。若暂停、日志和非颜色编码会改变底层时制或信息模型，必须在P1/P2阶段修正。

## 十四、叙事、Canon与揭示一致性

每个章节原型另跑五项：

1. 玩家胜利与Accepted Story胜利同义；
2. 玩家不能替角色/机魂作已锁定同意，也不能凭玩法失败改写固定生死/去向；
3. gameflow没有临时创造机体能力、建筑、房间、装置或世界规则；
4. 玩家、角色和公开世界只获得由故事/操作真正挣得的知识；
5. partial、withdraw和retry都映射到合法故事继续态。

任何一项失败，返回Reader迁移、GD1/GD2、GD3或gameflow中最早责任层；不得在Runtime补一条变量把冲突藏起来。

## 十五、遥测、隐私与证据

默认记录：

- 时间戳化输入、选择、撤销、提交、提示与菜单路径；
- 每脉冲初态、ActionDraft、Forecast、Resolve事件和状态hash；
- 目标/路线/权能/信息卡使用及非使用；
- 停滞、重开、局部重试、退出和完成；
- 方案分类、完成/partial/withdraw、资源与持久结果；
- 主持人提示；
- 事后复述、信心、偏好、困惑和继续意愿。

录像、屏幕和语音必须取得参与者同意；可只录屏/输入而不录人脸。参与者使用假名ID，联系信息与测试数据分开；报告只引用聚合结果和必要匿名片段。证据保留期、访问人和删除方式在每次招募前说明。

逐项同意不能由方向回执、implementation包络或主持人口头概括代签。实际采集范围写入Session的`consent_scope_tokens`，受限同意记录只以opaque ref+hash绑定；H2-H4提示、自由复述前定向提问、破盲、退出与不适必须进入同一Session证据链。单个Session永远固定`claim_boundary=evidence_only_no_user_acceptance`，只有聚合证据包经用户作范围化gameplay回执后，证据账才可记录用户裁决。

## 十六、证据账与决策路由

任何“通过”必须能追到：

~~~text
evidence_id
claim_scope
prototype/build/content/rules/map/tutorial/ui版本
source hashes
case IDs
自动报告
参与者与样本口径
录像/输入/遥测/复述路径
结果与失败样本
限制与不可推论
设计采纳/返修/淘汰决定
用户receipt
消费者与失效条件
~~~

结果只有五种：

- evidence_only：只新增证据，不改设计状态；
- candidate_for_review：达到预设门，等待用户；
- revise：返回明确Owner和最早设计层；
- retire_or_merge：不值得继续；
- approved_for_bounded_migration：用户只批准指定版本和消费者。

禁止只写“测试通过”或“玩家觉得不错”。

## 十七、D10完成定义

本文和两张机器表完成，只代表验证计划成立。D10真正完成必须满足：

- P1 A/B/C/D四版均有版本化灰盒与M5；P1只形成合法shortlist；每个shortlist carrier的最小C2 crossover有M5；用户DEC-03-M已作`select/revise/no_selection/retire_all`之一；仅在select后，完整P2与P3才分别有版本化灰盒和M5；
- A1-A5首例均有M5证据，三大辅助家族各有第二个数据化实例；
- C01-C03八个高风险适配至少完成用户选定的开局垂直切片范围；
- 所有自动正确性、状态、存档、揭示和build身份门通过；
- 无障碍专项测试完成；
- 证据账无缺失hash、未知版本或验收scope混用；
- 用户明确作出保留、返修、合并、淘汰和投资决定；
- D11只消费真实测得的开发速度、资产量、任务时长和缺陷率，不把候选估算当事实。
