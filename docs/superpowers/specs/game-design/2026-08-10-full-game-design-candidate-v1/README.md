# 《超GAG机器人大战：万机残响》全游戏主策划包 Candidate v1

> Status: `candidate_game_design / product_direction_approved / integrated_master_available / no_canon_promotion / no_runtime_authority`
>
> Date: `2026-08-10`
>
> Owner: 主策划总线程
>
> Current Scope: 全游戏核心策划、白话操作样例、系统闭环与角色／全剧机制演进说明
>
> Parked Scope: 跨章设定母包、C01–C03逐章适配、Build／灰盒／真人测试、资产与Runtime生产；保留旧稿，但不计当前玩法进度

**当前工作：** 已把公共循环、短全队协同、规则精通、四战斗家族、名场面、活机群、人物组牌、巡访／深潜／返馆／关系、战报、LLM／Meta和全剧演进收束进唯一[核心玩法总案](00c-core-game-design-master-review.md)。当前只做总案内部一致性；C01—C03适配样板继续停放，待用户另行启动，不再继续生产并列总案。

**本轮不做：** 可玩原型、真人M5/M6、真实GD2地点／机体图、正式资产、正式Runtime和预算校准。它们是以后验证／制作工作，不是本轮策划评审的缺件。

**用户已用普通话接受核心产品方向，但未签制作或机器回执。** 当前只需读[核心玩法总案](00c-core-game-design-master-review.md)；需要核对连续流程时再看`00b`。05f、05c与其余短例是旧局部放大，若秒数、人物协作或提交规则与总案冲突，以总案为准。

若只读一份，直接读 [核心玩法总案｜主策划评审稿](00c-core-game-design-master-review.md)。

**与制作层的关系：** C01E02 Demo、灰盒、程序和试玩都不是本轮主线。本包先把核心设计讲清；以后若另行进入制作，才讨论怎样以版本化证据回流，不在当前策划稿里抢跑。

**工作顺序已修正：** 全游戏公共玩法骨架 → 跨章共用基础设定 → 用C01-C03验证公共系统 → 逐章适配。木桶街、货运环、万机馆等新增设定草案可以保留，但在公共玩法通过前全部停放，不计入玩法进度。

## 一、结论与本包任务

当前项目拥有已验收的 C01-C03 故事、若干 Candidate 玩法名词、可复用 Runtime 零件和一个 C01E02 Candidate Demo，但面向用户的全游戏核心策划仍需收束为一套统一、可读、可评审的玩法骨架。

静态 checker 的 PASS 只证明表格结构、引用和枚举没有漂移，不证明玩法已经实现或好玩。产品方向已获用户接受；技术成熟度仍是`zero_build / human_not_run / no_production_approval`，旧技术表也尚未全部按整合总案重基，不得报告“整包语义已全部对齐”或“已可制作”。项目级已知问题与迁移停止条件继续见 [project-level-p1-migration-handoff-v0.1.md](validation/project-level-p1-migration-handoff-v0.1.md)。

本包从产品层重新建立一套可供用户逐项裁决的游戏设计：

- 主玩法是可承担较高学习成本、但每轮只前台化2—3个关键判断的群像机战战术 RPG，而不是传统数值堆叠式 SRPG；
- 前线机体以身体、朝向、预备和名场面完成会战、三方、追逃与大动作；人物通过有限战术牌改变信息、路线、动作形状和共同动词；
- 故事重、刷级轻，但奖励优先给马上想试的新动词、机体、合奏、关系化学和万机馆变化，而不是只发协议与停止线；
- 探索、解谜、Hub 日常、收藏、关系事件和小游戏作为轻松调剂，但必须把结果送回人物、战斗或世界状态；
- C01-C03以后用于检验公共系统能否适配开局故事；当前纸案不能证明可玩或好玩。后续章节只做机制演化预测，不能反向伪造未写成的剧情事实。

这段产品方向来自用户在 2026-08-10 的明确要求。它是本包的设计输入；在用户审定并完成 L1-L3/Canon 迁移前，不自动成为 Working Canon。

### 面向用户与面向机器的文档边界

- 面向用户的正文必须先用一段完整游玩示例说明屏幕、输入、选择、代价、失败与回写。
- 规则表、状态表、Gate、Hash与checker是实现和防漂移附录，不再作为用户阅读入口。
- 如果一个系统只能用字段名解释、不能用普通语言演示一次实际游玩，它仍只是名词扩写，不算设计骨架。

## 二、权威与隔离规则

1. Hard/Working Canon 约束角色、机体、权限、地点和因果边界。
2. C01-C03 已验收 Reader 约束故事事实、人物选择和章末状态；精确路径、完整 SHA-256、回执 scope 与快照可恢复性统一解析到 [data/opening-accepted-story-bindings.tsv](data/opening-accepted-story-bindings.tsv)。其验收不包含玩法、Runtime、美术或 L6。C01/C03 当前字节与验收哈希匹配，但无可达 Git commit/archive 保存当时快照，因而恢复性仍显式为 `UNRESOLVED`；不得用当前工作文件冒充不可变快照。
3. 现有五循环、六系统、gameflow、L4.5、旧数值表和 Demo 都是研究输入，不是默认答案。
4. C01E02 Demo 继续由制作人独立制作；本包不改其入口、地图、脚本、资产或测试。真人试玩结果将作为战术系统的实证输入，而不是替全游戏系统做裁决。
5. 旧游戏框架已登记为 History，只能回收有用问题和亮点，不能恢复其旧章节、练级或经济假设。
6. 新机制、新能力、新地点和新资产均留在本目录的 Candidate 层；只有用户明确批准后，才另开迁移把结果写入 L0-L3、Canon、章节链或 Runtime。
7. 当前工作树存在大量并行改动。本包只写本目录，暂不改 `doc_registry.tsv`、设计图谱、Canon、Reader、story-chain 或 Demo。

## 三、原十二项产出物现在怎样排队

机器可读的范围、依赖、验收和状态见 [01-deliverable-registry.tsv](01-deliverable-registry.tsv)。

1. **当前主线**：玩法与竞品研究矩阵。
2. **当前主线**：产品体验宪章与核心循环。
3. **当前主线**：全游戏公共系统关系、状态职责与轻经济的白话解释；技术图表只作附录。
4. **已进入整合总案**：短全队协同、四战斗家族、规则精通、名场面三档、活机群、人物五牌与完整操作样例。
5. **已进入整合总案**：城市巡访、残响深潜、任务型调查、返馆／手修／布展、多边关系、收藏、战报与结算。
6. **停放**：C01-C03 逐话适配蓝图与灰盒需求；公共系统通过后才重开。
7. **本轮只评公共原则**：只判断“一章最多一个新维度、后期重组旧系统、常显界面有上限”；22章逐章机制分配与生命周期预测继续停放。
8. **停放**：L0-L3 世界、角色、机体、城市、建筑和空间回补；只保留现有债务清单与草案。
9. **治理附录**：Story→预生产→Reader→gameflow→Previs→Runtime/资产门禁；当前不据此启动逐章生产。
10. **未来验证附录**：公共原型、可用性、趣味、平衡和真人测试计划；不属于本轮交付。
11. **本轮只评非数字范围纪律**：地点套件、机体身体资产、顶层UI和后果分支怎样复用已进入总案；体量、人月、资产预算和人员分工仍待以后校准。
12. **当前主线**：用户可读的方向页、批注入口、决策账与主策划总案。

## 四、阶段与停止门

| 阶段 | 主要交付 | 通过条件 | 未通过时 |
| --- | --- | --- | --- |
| G0 证据基线 | 当前状态、来源账、缺口账、评价框架 | 权威分层清楚；不再把名词、文档、代码、Demo、验收混成一档 | 补证据，不开始设计 |
| G1 外部研究 | 类型图谱、机制拆解、迁移/禁用判断 | 每个参考有可迁移机制、适配原因、风险和官方来源 | 扩充或淘汰样本 |
| G2 产品骨架 | 体验宪章、核心循环、系统/状态/经济图 | 玩家动词、输入输出、长期回报和失败后果闭合 | 返回 G1/G2 |
| G3 基础战术 | 短全队协同、身体、预备、行动意图与四类战斗题型 | 不开气势和人物强牌时仍有多种强解；允许合法规则利用 | 不允许用名场面或特殊能力掩盖弱战棋 |
| G4 活机群与人物组牌 | 机体欲望／拒绝／请战、人物五牌两用、共同动词与名场面三档 | 换人换打法；主体会制造局面但不替玩家解题；普通动作不走审批链 | 返修能力边界、行动经济或人物主体性 |
| G5 辅助循环 | 探索、Hub、关系、收藏、结算等 | 轻松、短、可复用；结果进入共同状态契约 | 删除一次性小游戏或断链系统 |
| G6 开局蓝图 | C01-C03 可玩结构、地图与预演需求 | 故事胜利等于玩法胜利；地点和机体不由 gameflow 临时发明 | 回补 Stage20/L0-L3 |
| G7 全剧与生产 | 演化路线、回补计划、RACI、预算 | 机制解锁随角色和剧情成长；资产与团队可承受 | 降范围或改复用策略 |
| G8 用户审定 | 可读总案与方向决策账 | 产品方向已获用户普通话接受；未决细节仍标Candidate；制作、Canon、Runtime另行授权 | 不静默迁移Canon／Runtime，不把纸案当试玩证据 |

## 五、本轮反“只有名词”标准

任何系统条目只有同时回答以下问题，才可从“概念”进入“可原型规则”：

- 玩家在 5-30 秒内具体做什么；
- 看见哪些有来源、有时效、有置信度的信息；
- 在哪些至少两个有意义方案之间选择；
- 消耗什么、承担什么、可能失去什么；
- 敌人、环境或角色怎样反制；
- 操作如何体现某个角色或机体，而不是换皮通用技能；
- 结果怎样写回战斗、关系、资源、地点或后续章节；

以后若进入制作，再另答：怎样用最小灰盒验证趣味，以及怎样通过真人证据进入正式生产。它们不作为本轮策划说明的前置。

文档完整、字段齐全、自动检查 PASS、代码能启动或作者自测，都不能替代真人玩法验收。

## 六、当前文件

### 用户阅读入口

- [00-user-reading-guide.md](00-user-reading-guide.md)：先读什么、哪些术语可以忽略、四阶段正确工作顺序。
- [00c-core-game-design-master-review.md](00c-core-game-design-master-review.md)：唯一整合玩法总案；汇总产品幻想、公共循环、主战棋、规则精通、四战斗家族、名场面、活机群、人物组牌、非战棋母型、成长奖励、世界记忆、LLM／Meta、C01–C03职责与全剧演进。
- [00d-c01-c03-common-system-adaptation.md](00d-c01-c03-common-system-adaptation.md)：未来C01–C03适配职责的可选预览；不计入本轮评审，不展开逐话关卡或新增设定。
- [00a-public-gameplay-direction-review.md](00a-public-gameplay-direction-review.md)：用一次约45分钟的中性游玩概括返馆、任务、调查、战术、结算与再次返馆；这是可选的短方向摘要，不取代00c。
- [00b-full-game-common-gameplay-skeleton.md](00b-full-game-common-gameplay-skeleton.md)：00c的连续两周期示例；用同一批中性人物、机体、物件与两张任务逐屏走完循环，但不另定义系统边界、提交位置或持久写回。
- [05f-first-neutral-tactics-v0.3-decision-ladder.md](05f-first-neutral-tactics-v0.3-decision-ladder.md)：旧基础战术局部例；保留两条责任战法和逐轮因果，具体秒数、回合与提交边界以00c为准。
- [05c-robot-combat-c2-public-decision-pack.md](05c-robot-combat-c2-public-decision-pack.md)：旧角色协作局部例；保留信息来源、主体回应和名场面素材，当前人物五牌两用与普通动作不审批规则以00c为准。
- [06a-auxiliary-play-walkthroughs.md](06a-auxiliary-play-walkthroughs.md)：当前轻探索完整操作例；用地标、交谈和路线报告改变后续入口。
- [06c-first-return-hub-brief.md](06c-first-return-hub-brief.md)：Hub完整操作例；先用十步走完变化简报、三格排班、两套安排与出发包读取，再展开标准维修末尾的承载确认、部分恢复和身体功能写回。
- [06d-first-investigation-engineering-brief.md](06d-first-investigation-engineering-brief.md)：00b的调查专项放大例；观察实体、比较证据、配置安全试验，并让时间／工具差异立刻进入下一任务。
- [06b-long-term-systems-player-walkthroughs.md](06b-long-term-systems-player-walkthroughs.md)：编队、成长、经济、关系、收藏、世界图和三级结算的正式白话展开。
- [07-series-mechanic-evolution.md](07-series-mechanic-evolution.md#玩家到后期实际多做了什么)：总案早中后期演进的可选展开；普通段只说明后期玩家多承担什么，详细22章预测账仍停放。

以下是第二遍参考或退役材料，不再承担首次解释责任，也不提供独立规则真值：

- [02a-player-readable-full-game-loop-example.md](02a-player-readable-full-game-loop-example.md)：被00b取代的早期45分钟串联例，只作History参考。
- [04c-two-return-minimum-long-loop-brief.md](04c-two-return-minimum-long-loop-brief.md)：被00b取代的平行两次返馆压缩例，只作差错追踪与旧问题素材。
- [05b-main-tactics-rules-in-plain-language.md](05b-main-tactics-rules-in-plain-language.md)：05f的白话概念索引，不拥有独立玩家流程。
- [05e-neutral-tactics-rule-cards.md](05e-neutral-tactics-rule-cards.md)：05f的八张规则技术附录；提供合法／非法／同刻例和停止门。
- [05g-common-tactical-resolver-paper-spec.md](05g-common-tactical-resolver-paper-spec.md)：05f的Resolver技术附录；说明一个局部8秒账、对象合并、八项OPEN与十个纸面案例。
- [05a-main-tactics-player-walkthrough.md](05a-main-tactics-player-walkthrough.md)：早期操作演示，地图／时距已经失效，只作History证据。
- [05d-first-neutral-tactics-graybox-brief.md](05d-first-neutral-tactics-graybox-brief.md)：被否决的v0.2作者回放，只保留中后段无决定等失败证据。
- [04b-public-failure-continuation-walkthrough.md](04b-public-failure-continuation-walkthrough.md)：另一张K-17纸面失败续行例，与当前05f地图不同，只作辅助参考。

### 策划、实现与审计附录

下面文件用于追溯规则、实现接口和防止数据漂移。用户不需要按顺序读完，也不应从这些表的数量判断玩法成熟度。

- [04a-two-cycle-public-gameplay-closed-loop.md](04a-two-cycle-public-gameplay-closed-loop.md)：已停用的23步旧长稿，仅用于诊断旧屏幕顺序、时间和结算语义；不得作为当前实现输入。

- [00-current-baseline-and-gaps.md](00-current-baseline-and-gaps.md)：当前产品真相、缺口与风险。
- [01-deliverable-registry.tsv](01-deliverable-registry.tsv)：十二项产出物、依赖与验收。
- [02-mechanic-evaluation-framework.md](02-mechanic-evaluation-framework.md)：所有玩法共用的设计与研究标尺。
- [03-source-authority-register.tsv](03-source-authority-register.tsv)：当前输入的权威、用途和禁用推论。
- [research/01-comparative-gameplay-research.md](research/01-comparative-gameplay-research.md)：35条官方页面级样本与跨类型综合；15条关键一手证据已有页面／手册章节定位，但没有保存页面正文或可恢复快照，不能冒充未来可恢复的逐段引文证据。
- [research/comparative-mechanic-matrix.tsv](research/comparative-mechanic-matrix.tsv)：外部机制拆解矩阵。
- [research/mechanic-synthesis-decisions.tsv](research/mechanic-synthesis-decisions.tsv)：保留、重写、原型、边界与淘汰裁决。
- [research/source-evidence-ledger.tsv](research/source-evidence-ledger.tsv)：15条关键一手来源的定位、支持主张、禁止推论与捕获层级；只支撑Candidate假设。
- [research/source-response-fingerprints.tsv](research/source-response-fingerprints.tsv)：15条关键来源的本次HTTP响应指纹；13条记录真实响应体SHA-256，2条如实记录连接失败，不保留正文，不是可恢复引文归档。
- [validation/d01-official-source-response-fingerprint-audit-v0.1.md](validation/d01-official-source-response-fingerprint-audit-v0.1.md)：动态页、PDF、响应哈希漂移、失败抓取与不保留正文的证据边界。
- [scripts/check_d01_source_response_fingerprints.py](scripts/check_d01_source_response_fingerprints.py)：只读校验15行与来源账一对一、官方HTTPS来源、抓取时间、成功哈希及失败项不得伪造哈希。
- [research/synthesis-evidence-coverage.tsv](research/synthesis-evidence-coverage.tsv)、[scripts/check_d01_synthesis_evidence_coverage.py](scripts/check_d01_synthesis_evidence_coverage.py)：将22/22条综合取舍逐项追到样本、locator与本次响应结果；无locator者强制保留为`hypothesis_only`，失败响应不得冒充本次复核。
- [03-product-experience-charter.md](03-product-experience-charter.md)：产品身份、玩家节奏、统一循环、成长和失败合同。
- [04-full-game-system-graph.md](04-full-game-system-graph.md)：系统职责、共享状态、事务、经济和模式转换。
- [data/core-loop-payload-bindings.tsv](data/core-loop-payload-bindings.tsv)、[scripts/check_d02_d03_core_loop_payload_bindings.py](scripts/check_d02_d03_core_loop_payload_bindings.py)：把4条会话35步的207项输入、111项提交输出、13个结算回执与下一消费者逐项闭合；仍只是静态payload合同。
- [data/economy-invariant-paper-cases.tsv](data/economy-invariant-paper-cases.tsv)、[validation/d03-economy-invariant-paper-cases-v0.1.md](validation/d03-economy-invariant-paper-cases-v0.1.md)、[scripts/check_d03_economy_invariants.py](scripts/check_d03_economy_invariants.py)：9个战术／Hub／Operation／全局资源不变量纸例，覆盖拒绝零写入、幂等重放、唯一物件和禁止关系／同意兑换；不是数值经济模型。
- [data/runstate-v2-enum-type-registry.tsv](data/runstate-v2-enum-type-registry.tsv)、[data/runstate-v2-field-schema.tsv](data/runstate-v2-field-schema.tsv)、[data/runstate-v2-domain-registry.tsv](data/runstate-v2-domain-registry.tsv)、[data/state-transaction-v2-op-schema.tsv](data/state-transaction-v2-op-schema.tsv)、[data/runstate-v2-r0-p1-fixture-coverage.tsv](data/runstate-v2-r0-p1-fixture-coverage.tsv)与[data/runstate-v2-r0-p1-fixtures.json](data/runstate-v2-r0-p1-fixtures.json)：RunState v2／StateTransaction v2的47类型、35记录Schema、26域、7事务op与4个R0/P1参考案例。这些只是实现前M2纸面合同，不是用户阅读主入口，也不是Build、Runtime迁移或玩法证据。
- [validation/d03-runstate-v2-paper-contract-v0.1.md](validation/d03-runstate-v2-paper-contract-v0.1.md)、[scripts/check_d03_runstate_v2_contracts.py](scripts/check_d03_runstate_v2_contracts.py)：纸面线格式、owner prepare/commit、幂等、零写入拒绝、唯一物件与投影删改的技术附录与参考检查器；当前明确为`M2_only / zero_build / zero_human`。
- [05-srpg-c2-core-design.md](05-srpg-c2-core-design.md)：四种中立Scheduler、机器人身体、信息战、主角团C2、敌方AI、P1 shortlist、最小C2 crossover与P2/P3纸面Fixture。
- [data/d04-p1-v0.2/README.md](data/d04-p1-v0.2/README.md)、[scripts/check_d04_p1_v0_2.py](scripts/check_d04_p1_v0_2.py)：首个14×10中性战术的哈希绑定声明事件账与静态回放检查。只允许报告`HASH_BOUND_DECLARED_EVENT_LEDGER_PASS`；公共解算器、合法策略、存读档、Build和趣味全部未证明，当前为`IMPLEMENTATION_NO_GO`。
- [data/scheduler-clock-adapter-contracts.tsv](data/scheduler-clock-adapter-contracts.tsv)、[data/d04-p1-adapter-event-vectors.tsv](data/d04-p1-adapter-event-vectors.tsv)、[validation/d04-p1-scheduler-clock-paper-contract-v0.1.md](validation/d04-p1-scheduler-clock-paper-contract-v0.1.md)：A/B/C/D四种时制各自的提交边界映射到同一战内8秒语义结算周期，并以28条纸面向量约束32秒任务截止、自主单位、环境、观察年龄、反应、资源与存档语义；它不等于Hub时间格或世界航行时间，且仍是零Build、零运行证据。
- [06-auxiliary-play-design.md](06-auxiliary-play-design.md)：三类探索、四种微交互、万机馆Hub、关系、收藏、世界图和三级结算。
- [data/prototype-paper-fixture-registry.tsv](data/prototype-paper-fixture-registry.tsv)：D04–D05的11行纸面Fixture登记覆盖15个原型节点；其中3行仅为D05 R2纸面preflight，明确保持`no_replication_evidence`；全部为`zero_build / human_not_run`。
- [validation/d04-p2-p3-neutral-paper-fixtures-v0.1.md](validation/d04-p2-p3-neutral-paper-fixtures-v0.1.md)：有限信息/C2与三Encounter巨构Operation的中性初态、路线、缺席回退和停止门；非Build、非C04设定。
- [validation/d05-auxiliary-neutral-content-fixtures-v0.1.md](validation/d05-auxiliary-neutral-content-fixtures-v0.1.md)：P-EX1/2/3、P-HUB1、P-SET1的首例可编程中性内容样例；仍无Build与真人证据。
- [data/auxiliary-replication-freeze-contracts.tsv](data/auxiliary-replication-freeze-contracts.tsv)、[data/auxiliary-second-instance-paper-fixtures.json](data/auxiliary-second-instance-paper-fixtures.json)、[validation/d05-auxiliary-second-instance-paper-fixtures-v0.1.md](validation/d05-auxiliary-second-instance-paper-fixtures-v0.1.md)：三个D05家族的第二实例纸面数据、首例切片哈希和静态复用断言；只完成paper preflight，不是R2/M6证据。
- [chapters/C01-C03-playable-blueprints.md](chapters/C01-C03-playable-blueprints.md)：投影前三章13话已经验收的固定故事结果，并另附Candidate可玩过程、整项任务、局部策略与生产门；后者不属于故事验收或当前总案真值。
- [chapters/c01-c03-episode-play-contracts.tsv](chapters/c01-c03-episode-play-contracts.tsv)：逐话模式、目标、代理、状态与GD2缺口。
- [chapters/c01-c03-story-state-seeds.tsv](chapters/c01-c03-story-state-seeds.tsv)：跨话固定事实、人物/身体/地点/知识/权限状态种子。
- [data/opening-accepted-story-bindings.tsv](data/opening-accepted-story-bindings.tsv)：C01-C03 验收故事的可解析 binding ID、章/单话 Reader 路径与完整 SHA-256、回执 path/hash/scope、当前匹配与不可变快照缺口。
- [chapters/c01-c03-playable-units.tsv](chapters/c01-c03-playable-units.tsv)：可控单位、盟友请求、场景主体、敌方意图及同意边界。
- [chapters/c01-c03-previs-needs.tsv](chapters/c01-c03-previs-needs.tsv)：前三章真正需要制作并由用户看图裁决的地点、身体、地图与连续Previs。
- [data/opening-chapter-paper-fixture-registry.tsv](data/opening-chapter-paper-fixture-registry.tsv)：C02E04决赛/事故Checkpoint与C02E05救援Clear的3个机器可校验Candidate纸面合同；仅MATCH四条接触式可静态算术重算，全部`zero_build / not_run`。
- [data/c02-paper-equipment-state-ledger.tsv](data/c02-paper-equipment-state-ledger.tsv)：借用推进模块与王者全装逐实例的owner/version/custody/installed_state/condition连续账。
- [data/c02-action-authority-consent-paper-ledger.tsv](data/c02-action-authority-consent-paper-ledger.tsv)：E04/E05自主支援的请求/回应/撤回receipt，以及E05动作级撤销/授权链；不生成按钮服从或永久权限。
- [validation/d06-c02e04-e05-paper-fixtures-v0.1.md](validation/d06-c02e04-e05-paper-fixtures-v0.1.md)：将`0:2`透明Story Showcase、三分战术逆转、事故存档和三阶段救援写成可否证纸面过程；E04事故/E05救援仍缺GD2与物理resolver，不替代Build或真人验收。
- [data/opening-previs-graybox-bom.tsv](data/opening-previs-graybox-bom.tsv)：20个Previs源×6类交付的120行开篇BOM，区分GD2逻辑/方向、连续Previs、章灰盒、资产Previs/BOM与授权后正式资产。
- [data/opening-previs-artifact-class-contract.tsv](data/opening-previs-artifact-class-contract.tsv)：六类BOM的四项阻断矩阵、scope实例规则、回执模板和必需instance/version/hash绑定；当前全部实例状态明确为OPEN。
- [data/opening-design-subject-coverage.tsv](data/opening-design-subject-coverage.tsv)：28条开篇GD2债务主体到W1逻辑、W5 Candidate资产BOM和W6正式资产行的一对一追溯账，明示新建/复用边界，并同步15条可解析Current Canon锚点与13条显式无单一实体值。
- [validation/d06-opening-previs-graybox-bom-audit-v0.1.md](validation/d06-opening-previs-graybox-bom-audit-v0.1.md)：开篇BOM的阶段、主体覆盖、证据类别与授权/交接防循环审计。
- [07-series-mechanic-evolution.md](07-series-mechanic-evolution.md)：C01-C22每章唯一新判断、九阶段复杂度、教程、敌方反制和终局回收路线。
- [data/series-mechanic-unlock-spine.tsv](data/series-mechanic-unlock-spine.tsv)：22章机制教学、复用、反制、持久输出、原型门和禁区。
- [data/series-mechanic-lifecycle-ledger.tsv](data/series-mechanic-lifecycle-ledger.tsv)：C01-C22逐机制的教学、独立使用、纯数据第二实例、延迟掌握、反制、退役/合并和缺席回退账；当前1 proposed、18 open、3 blocked，不能当全剧玩法封板。
- [data/series-mechanic-lifecycle-governance.tsv](data/series-mechanic-lifecycle-governance.tsv)：22机制逐行的primary/collaborating owner、状态、来源、消费者、决策、章链接入、阻断与退役拆分；当前22/22均未接实时章链。
- [data/series-system-lifecycle-coverage.tsv](data/series-system-lifecycle-coverage.tsv)：12系统的主机制、协作机制或横向非章级机制身份，防止NARR/EXPL/ARCH/PRESENT在演进账中消失。
- [data/series-mechanic-second-instance-ledger.tsv](data/series-mechanic-second-instance-ledger.tsv)：22个第二实例的fixture、ruleset、schema、内容hash、隔离与污染账；当前22/22无hash、18/22污染或阻断。
- [data/series-mechanic-stage-evidence.tsv](data/series-mechanic-stage-evidence.tsv)：22机制×首次出现/第二实例/延迟掌握共66个阶段证据绑定，禁止不同阶段原型互相代签。
- [data/series-mechanic-fragment-ledger.tsv](data/series-mechanic-fragment-ledger.tsv)：按独立输入、状态与可教学性拆分机制碎片；checker当前动态推导7个复合风险，不使用固定章名单。
- [data/series-mechanic-chapter-activity-ledger.tsv](data/series-mechanic-chapter-activity-ledger.tsv)：70行章×机制活跃/复用/掌握/计划复习、组合对象与UI surface交叉账；C16/C17/C20累计栈超过4。
- [data/series-counterplay-ladder.tsv](data/series-counterplay-ladder.tsv)：从公开直取目标到终局重组的九阶公平反制合同。
- [data/series-entity-access-spine.tsv](data/series-entity-access-spine.tsv)：17类角色/机体的首见、试控、正式Roster、Hub岗位、所有权与能力上限分层。
- [data/series-roster-coverage-crosswalk.tsv](data/series-roster-coverage-crosswalk.tsv)：29包/77条Candidate继承记录的逐条权威分层、D07接入处置、章窗、所有/控制、动作合同门与资产档交叉账；当前为4条精确映射、72条OPEN、1条History废弃，不是最终Roster批准。
- [data/series-roster-nonlegacy-package-gaps.tsv](data/series-roster-nonlegacy-package-gaps.tsv)：更新的44行Candidate分配里、不在旧29包/77记录中的15个key；当前1个可包级映射但缺逐机记录、12个OPEN、1个motif非Roster、1个退役储备。
- [scripts/build_series_roster_coverage_crosswalk.py](scripts/build_series_roster_coverage_crosswalk.py)：从三77表、29包生命周期、44行Candidate分配、Canon authority manifest和17行接入脊柱重建/校验上述两账。
- [08-l0-l3-setting-backfill.md](08-l0-l3-setting-backfill.md)：GD0-GD3职责、万机馆参考包与Stage20硬门。
- [data/setting-backfill-register.tsv](data/setting-backfill-register.tsv)：53项GD0-GD3实际回补对象、优先级、阻断、视觉/原型和用户决策门。
- [data/opening-gd2-dependency-closure.tsv](data/opening-gd2-dependency-closure.tsv)：BF0020–BF0037开篇GD2债务与10条GD1/主体支撑的28行依赖闭包账；9条债务→设计主体映射、15条Current Canon实体锚点和13条显式无单一实体值分列保存；当前28/28均阻断，不是已完成设定。
- [validation/opening-gd2-dependency-closure-audit-v0.1.md](validation/opening-gd2-dependency-closure-audit-v0.1.md)：回补对象、设计主体、可解析Current Canon锚点／无单一实体哨兵及阻断审计。
以下万机馆条目均是停放的Candidate设定／示意，不覆盖00c的Current物理边界，也不构成C05故事事实、未来形态批准或玩法进度：

- [setting/wanji-master-pack-v0.1.md](setting/wanji-master-pack-v0.1.md)：万机馆6层/30节点/19展区/8泊位的Candidate证据整合、WMP-00–15交付和C01-C22消费者。
- [setting/visuals/wanji-cutaway-schematic-v0.1.svg](setting/visuals/wanji-cutaway-schematic-v0.1.svg)：万机馆统一剖面与人/机/货流线问题图。
- [setting/visuals/wanji-control-gradient-v0.1.svg](setting/visuals/wanji-control-gradient-v0.1.svg)：从C01场景身体到候选未来多格母舰玩法的控制梯度示意；不证明C05事实。
- [data/mechanic-evaluation-schema.tsv](data/mechanic-evaluation-schema.tsv)：机制卡字段定义。
- [data/location-dossier-schema.tsv](data/location-dossier-schema.tsv)：城市、要塞、建筑和长期场景档案字段。
- [data/mecha-dossier-schema.tsv](data/mecha-dossier-schema.tsv)：核心机体静态身体/控制/接口/视觉与验收门禁问卷。
- [data/character-capability-dossier-schema.tsv](data/character-capability-dossier-schema.tsv)：角色能力档案及动作合同引用边界。
- [data/world-rule-dossier-schema.tsv](data/world-rule-dossier-schema.tsv)：Canon世界规则的设计投影与跨章验证门。
- [data/reveal-ledger-schema.tsv](data/reveal-ledger-schema.tsv)：原子事实、知识主体、章话边界与Reader/gameflow可见性投影。
- [09-production-pipeline-and-gates.md](09-production-pipeline-and-gates.md)：GD依赖闭包、L4/Reader、gameflow、三类Previs、原型、资产、Runtime与L6的新双循环生产法。
- [data/game-design-gate-registry.tsv](data/game-design-gate-registry.tsv)：GD0至L6十七道门的定义、证据、用户判断、回退和禁止升级；资产制作授权与成品handoff分门。
- [data/game-design-gate-instance-schema.tsv](data/game-design-gate-instance-schema.tsv)：每个章/话/资产/构建门实例必须保存的路径、hash、checker、回执和失效字段。
- [data/gate-receipt-set-templates.tsv](data/gate-receipt-set-templates.tsv)：单个Reader、图包、Previs、规则build、资产包、Runtime与L6的scope化回执模板；与15项产品决策集分离。
- [data/source-context-projection-registry.tsv](data/source-context-projection-registry.tsv)：entity、scene、Writer、gameflow、Previs、production和Runtime的来源准入/删减规则。
- [data/production-snapshot-schema.tsv](data/production-snapshot-schema.tsv)：内容寻址快照、上下文请求、编译清单、揭示、gameflow、Previs和Build manifest字段。
- [data/invalidation-routing-rules.tsv](data/invalidation-routing-rules.tsv)：产品、系统、角色、身体、地点、揭示、Reader、玩法、视觉、Demo变化的分级失效。
- [data/user-acceptance-scope-contracts.tsv](data/user-acceptance-scope-contracts.tsv)：产品方向、故事、玩法、视觉和生产五类用户回执的可提升范围与禁止推论。
- [10-prototype-test-plan.md](10-prototype-test-plan.md)：P1 A/B/C/D四时制中立筛选、shortlist、可撤销C2 crossover、完整P2/P3、辅助玩法、Hub、结算、章节适配、自动回归与真人冷测计划。
- [data/prototype-test-registry.tsv](data/prototype-test-registry.tsv)：30个技术核、规则、shortlist/C2 crossover、辅助首例/复用例、章内与接缝原型节点的typed依赖、唯一问题、样本、硬门、失败返回和下游解锁。
- [data/playtest-cases.tsv](data/playtest-cases.tsv)：57个自动、真人、复用、无障碍、章节与垂直切片用例；其33个非自动用例逐条入证据账。
- [scripts/check_d10_test_registry_bijection.py](scripts/check_d10_test_registry_bijection.py)：校验30原型/52依赖边DAG、57用例、指标与证据账可解析性，并强制167组自动 `(prototype_id, case_id)` 双向一致及A/B/C/D中立比较。
- [scripts/check_candidate_contracts.py](scripts/check_candidate_contracts.py)：只读重放包级TSV/本地链接、系统边、状态owner、模式转换、Episode token、Operation边界与Accepted Story binding静态合同；C01/C03缺可达归档保持WARN。
- [scripts/check_d05_auxiliary_second_instances.py](scripts/check_d05_auxiliary_second_instances.py)：校验三个D05第二实例纸面包复用冻结动作/UI/Outcome/状态域、canonical hash与`zero_build / human_not_run / no_replication_evidence`；`--self-test`只证明静态守卫能拒绝故障，不证明R2/M6。
- [scripts/check_d06_c02_paper_fixtures.py](scripts/check_d06_c02_paper_fixtures.py)：只读校验3个C02纸面合同、19个逐事件Accepted Story locator、状态域、装备/权限/同意、事务/存档点与零Build边界；`--self-test`故意制造418项漂移并要求全部拒绝。只静态重算MATCH四条接触式，不声称E04事故/E05救援物理可解。
- [scripts/check_candidate_release.py](scripts/check_candidate_release.py)：当前包唯一推荐的只读发布入口；依次运行中央、D01来源与综合证据、D02 payload、D03经济不变量/RunState v2、授权/preflight、首批裁决包、D05、D06、D09、D10原型与真人Session合同、D11与Roster检查，全部执行并返回首个非零退出码。
- [data/playtest-metric-contracts.tsv](data/playtest-metric-contracts.tsv)：可用性、学习、策略、身体感、代理权、负担、复述、故事适配、状态与无障碍指标。
- [data/playtest-session-result-schema.tsv](data/playtest-session-result-schema.tsv)：每次版本化真人Session的参与者、构建、提示、行为、复述、遥测与隐私字段。
- [data/human-playtest-session-instance-schema.tsv](data/human-playtest-session-instance-schema.tsv)、[data/human-playtest-session-instances.tsv](data/human-playtest-session-instances.tsv)、[data/human-playtest-session-result-crosswalk.tsv](data/human-playtest-session-result-crosswalk.tsv)、[data/human-playtest-hint-level-contracts.tsv](data/human-playtest-hint-level-contracts.tsv)、[data/human-playtest-program-status.tsv](data/human-playtest-program-status.tsv)：112字段Session证据链、旧结果crosswalk、H0-H4提示污染与当前零状态。这是M2测试治理附录，不是面向用户的玩法说明。
- [validation/d10-human-playtest-session-evidence-chain-v0.1.md](validation/d10-human-playtest-session-evidence-chain-v0.1.md)、[scripts/check_d10_human_playtest_sessions.py](scripts/check_d10_human_playtest_sessions.py)：检查冷启动/盲态、复述顺序、提示污染、隐私、退出删除、版本hash和用户验收边界；当前是`0 participants / 0 Sessions / 0 authorized human_run / 0 passed preflight / not_run`，不得写成M5/M6。
- [data/acceptance-evidence-registry.tsv](data/acceptance-evidence-registry.tsv)：当前M2/M4证据与全部待执行M5/M6证据账，机器、真人和用户结果分栏。
- [11-scope-budget-production-plan.md](11-scope-budget-production-plan.md)：一个机制/生产校准阶段，加C01垂直切片、22章最低可售与Ideal三档产品范围，及单位产能、里程碑、RACI和止损门。
- [data/scope-tier-budget.tsv](data/scope-tier-budget.tsv)：Stage0校准与三档产品的时长、玩法量、团队、人月和解锁门；全部总量仍为未校准候选。
- [data/scope-cost-scenarios.tsv](data/scope-cost-scenarios.tsv)：低／基准／高PM、日历、平均FTE和八工种分配的成对场景；禁止跨列任意拼接。
- [data/chapter-scope-allocation.tsv](data/chapter-scope-allocation.tsv)：把D07的22章成本信号映射到6桥接/7标准/9支柱、24–30战术和7个A3生产簇的顶层Candidate分配。
- [data/asset-budget.tsv](data/asset-budget.tsv)：地点Kit、地图态、机体、UI、动画、音频与文本的数量帽、计费边界、互斥配对、复用和校准门；不与单位毛工时上限直接相乘。
- [data/production-raci.tsv](data/production-raci.tsv)：产品、Canon、系统、原型、GD1-GD3、Writer、gameflow、Previs、Demo、Runtime、资产、QA和发行的唯一写入与交接责任。
- [data/production-role-registry.tsv](data/production-role-registry.tsv)：RACI与生产测量共用的稳定role ID、权威、禁止自批、最小交接和替补要求。
- [data/risk-register.tsv](data/risk-register.tsv)：核心玩法、范围、设定债、资产、状态、门禁、Demo、视觉、本地化、资金和发行的19项风险与止损路由。
- [data/scope-milestone-gates.tsv](data/scope-milestone-gates.tsv)：从范围校准到RC的8个未校准里程碑及机器、真人、用户退出门。
- [data/production-measurement-schema.tsv](data/production-measurement-schema.tsv)：把主动、审查、返工、阻塞、修复、招募和范围化回执拆开的生产实测字段。
- [data/production-work-unit-schema.tsv](data/production-work-unit-schema.tsv)、[data/production-work-unit-registry.tsv](data/production-work-unit-registry.tsv)、[data/production-measurement-instances.tsv](data/production-measurement-instances.tsv)：定义可接受生产单位、多人贡献去重和投入实例；当前后两张实例账均为0行。
- [data/budget-calibration-contracts.tsv](data/budget-calibration-contracts.tsv)：单位P50/P80、复用、返工、阻塞、缺陷、视觉吞吐、预算可信度和Demo抵扣合同。
- [data/project-p80-model-inputs.tsv](data/project-p80-model-inputs.tsv)：全项目P80的可重算输入Schema；当前无U2样本，仅有表头，禁止把范围先验冒充P80。
- [data/budget-calibration-status.tsv](data/budget-calibration-status.tsv)、[scripts/check_d11_budget_calibration.py](scripts/check_d11_budget_calibration.py)：机器派生当前0单位、0投入、0个P50/P80；Scope 2仍为1455–2060分钟并被1800分钟上限阻断，P80明确为`NOT_CALCULABLE`。
- [12-user-decision-log-and-master-plan.md](12-user-decision-log-and-master-plan.md)：内部决策账与历史执行附录；当前唯一玩法总案仍是00c，旧15项编号和条件路线只用于追溯，不形成第二份公开总案。
- [12a-first-decision-signoff-sheet.md](12a-first-decision-signoff-sheet.md)：已冻结的旧DEC-01/02/03/11技术授权附录；因公开时制方向已改为B主推荐／A备选，当前不可签署或形成回执。
- [data/first-decision-signoff-pack.tsv](data/first-decision-signoff-pack.tsv)、[data/first-decision-signoff-freeze.tsv](data/first-decision-signoff-freeze.tsv)：前者保存旧四项包的精确历史内容，后者以内容hash覆盖其旧`ready_for_signature`字段，只允许追溯，禁止回执、执行包络、Build、真人Session或迁移。
- [data/user-game-design-decisions.tsv](data/user-game-design-decisions.tsv)：每项推荐、替代、证据、回执范围、禁止提升、延期默认和失效触发。
- [data/decision-receipt-sets.tsv](data/decision-receipt-sets.tsv)：每项决策按Candidate测试授权/证据后迁移分成两个可解析集合，并绑定全部requirement ID。
- [data/decision-receipt-requirements.tsv](data/decision-receipt-requirements.tsv)：Candidate测试授权与证据后迁移分相；每个合法回执类型、scope、path、hash和all条件独立成行。
- [data/decision-receipt-instance-schema.tsv](data/decision-receipt-instance-schema.tsv)：决策规范hash、选项token、接受/拒绝/延期条款、用户消息、唯一locator、替代与失效的结构化回执实例Schema；当前实例0。
- [data/candidate-test-execution-envelope-schema.tsv](data/candidate-test-execution-envelope-schema.tsv)：每次Candidate实现或真人Session的精确subject hash、可写路径、Build/日历/人时/现金/样本上限、数据边界、停止条件与独立用户授权绑定；当前实例0。
- [data/execution-envelope-authorization-receipt-schema.tsv](data/execution-envelope-authorization-receipt-schema.tsv)：独立于方向回执的执行包络授权回执，必须同时定位`envelope_id + authorization_subject_sha256`；当前实例0。
- [data/candidate-test-budget-pool-schema.tsv](data/candidate-test-budget-pool-schema.tsv)：R0与P1可分包，但必须共享一个累计日历/人时/现金池，阻止两个包络各自取得一份上限；当前实例0。
- [data/prototype-execution-preflight-requirements.tsv](data/prototype-execution-preflight-requirements.tsv)：将方向回执实例、scope化passed Gate实例、上游Build证据、精确执行包络/预算池与来源hash组合成原型执行前的AND合同；通用Gate定义或决策状态不能代替实例。
- [scripts/check_candidate_authorization_contracts.py](scripts/check_candidate_authorization_contracts.py)：对回执、包络、共享预算池与Prototype preflight执行故障注入；当前所有实例账均为0行，不得运行原型。
- [13-goal-completion-audit.md](13-goal-completion-audit.md)：按用户原目标十二项区分候选策划、实体设计、Build、真人与用户批准的真实完成度。
- [validation/project-level-p1-migration-handoff-v0.1.md](validation/project-level-p1-migration-handoff-v0.1.md)：两个现行项目级P1的失败命令、消费者影响、修复选择与反向测试；只读交接，不是Canon或story-chain修改授权。
- [data/goal-deliverable-evidence-matrix.tsv](data/goal-deliverable-evidence-matrix.tsv)：十二项产出物的证据、缺口、下一门与完成状态机器账。
- [data/system-state-contracts.tsv](data/system-state-contracts.tsv)：长期状态域、所有者、写入者和验收。
- [data/system-node-contracts.tsv](data/system-node-contracts.tsv)：每个系统的玩家幻想、动词、生命周期和读写责任。
- [data/system-edge-contracts.tsv](data/system-edge-contracts.tsv)：系统间数据载荷、提交、回滚和失效合同。
- [data/economy-flows.tsv](data/economy-flows.tsv)：战内、章间资源与非货币状态边界。
- [data/mode-transition-contracts.tsv](data/mode-transition-contracts.tsv)：各玩法模式的进入、退出、提交和阻断条件。
- [data/episode-mode-token-contracts.tsv](data/episode-mode-token-contracts.tsv)：把Story-in-Hub、真实Hub Cycle、Setpiece、Aux、Tactical和各级Checkpoint/Settlement token归一到唯一mode/owner/boundary。
- [data/settlement-owner-prepare-commit-contracts.tsv](data/settlement-owner-prepare-commit-contracts.tsv)：十个状态owner对同一proposal先prepare、后由结算原子提交或整组拒绝的合同。
- [data/core-loop-paper-walkthrough-traces.tsv](data/core-loop-paper-walkthrough-traces.tsv)：三条Accepted Opening会话与一条中性Hub会话的逐步内部静态trace。
- [data/opening-state-transaction-paper-trace.tsv](data/opening-state-transaction-paper-trace.tsv)：C01→C03十二段Operation/Chapter事务与跨章桥接守卫。
- [validation/d02-d03-core-loop-paper-walkthrough-v0.1.md](validation/d02-d03-core-loop-paper-walkthrough-v0.1.md)：D02–D03结构断点、修复与合法声明；目标玩家为0，不是玩法验收。
- [data/tactical-action-contracts.tsv](data/tactical-action-contracts.tsv)：基础身体动作、时序、预览、反应与持久输出。
- [data/tactical-tempo-equivalence.tsv](data/tactical-tempo-equivalence.tsv)：四时制共用动作秒数到P1-A/D Tempo及P1-B/C 8秒窗的逐动作等价合同。
- [data/tactical-resolution-kernel.tsv](data/tactical-resolution-kernel.tsv)：四个Scheduler adapter共用的计划校验、接触、力/功能差值、状态合并、中止和因果日志 seed kernel。
- [data/time-system-neutrality-contract.tsv](data/time-system-neutrality-contract.tsv)：锁定A/B/C/D共同world/action/objective/AI/未知信息预算、各自原生UI/命令语法、匿名标签、教程预算、预注册权重/硬阈值、shortlist与C2 crossover结果边界。
- [validation/d04-p1-neutral-rules-paper-fixture-v0.1.md](validation/d04-p1-neutral-rules-paper-fixture-v0.1.md)：P1-A/B/C/D共用的14×10地图、单体菜单、离散身体带、操作状态机和两类预计解；仅纸面Fixture，非Build或玩法验收。
- [validation/d07-series-lifecycle-paper-audit-v0.2.md](validation/d07-series-lifecycle-paper-audit-v0.2.md)：规范化D07生命周期审计；覆盖12系统、70行活动栈、阶段证据、第二实例污染、七个动态复合风险、计划复习和22/22实时章链未接线；零Build、零真人证据、零L3迁移。
- [data/authority-action-contracts.tsv](data/authority-action-contracts.tsv)：角色能力到玩家输入、稳定成本资源、权限、同意、物理执行路由与反制。
- [data/authority-owner-sentinels.tsv](data/authority-owner-sentinels.tsv)：`shared_c2`与`MACHINE_SOUL_ACTOR`两个本地类型哨兵的实例解析与禁止推论；其余owner必须解析到Canon实体。
- [data/authority-action-test-matrix.tsv](data/authority-action-test-matrix.tsv)：25个角色/C2动作逐项“该用、忍住、受克制、角色缺席替代”fixture与P2用例映射。
- [data/enemy-intent-contracts.tsv](data/enemy-intent-contracts.tsv)：敌方目标、感知、承诺、条件变招与反制。
- [data/tactical-objective-contracts.tsv](data/tactical-objective-contracts.tsv)：非歼灭目标、局部失败与故事回写。
- [data/time-system-ab-test.tsv](data/time-system-ab-test.tsv)：同图对照交替激活、短WEGO、交替锁计划＋同步执行和传统阵营回合的四时制原型门。
- [data/auxiliary-loop-contracts.tsv](data/auxiliary-loop-contracts.tsv)：辅助玩法动词、信息模型、失败、回写、复用和删除门。
- [data/auxiliary-kernel-contracts.tsv](data/auxiliary-kernel-contracts.tsv)：Spatial、Evidence、Commit、Route四个复用内核及收藏/结算支持层。
- [data/auxiliary-output-gates.tsv](data/auxiliary-output-gates.tsv)：按玩法家族规定主输出、证据是否必需、后续消费者与删除/降级门。
- [data/auxiliary-replication-freeze-contracts.tsv](data/auxiliary-replication-freeze-contracts.tsv)：P-EX1/2/3首例章节切片哈希及动作、逻辑UI、Outcome、状态域冻结合同。
- [data/auxiliary-second-instance-paper-fixtures.json](data/auxiliary-second-instance-paper-fixtures.json)：三个`TEST_*`第二实例canonical纸面数据；全部新增系统计数为0且证据状态为`no_replication_evidence`。
- [data/auxiliary-asset-tiers.tsv](data/auxiliary-asset-tiers.tsv)：A0-A3辅助玩法资产边界、复用和升级门。
- [data/hub-action-contracts.tsv](data/hub-action-contracts.tsv)：有限回馆行动、空间、岗位冲突与后续消费者。
- [data/relationship-event-contracts.tsv](data/relationship-event-contracts.tsv)：具名关系事件、边界、承诺、许可与防刷规则。
- [data/settlement-contracts.tsv](data/settlement-contracts.tsv)：Encounter、Operation、Chapter三级结算。
- [data/mission-card-schema.tsv](data/mission-card-schema.tsv)：世界图任务卡的目标、路线、时效和未选结果字段。
- [data/collection-entry-schema.tsv](data/collection-entry-schema.tsv)：收藏来源、保管、知识层、揭示与未来回收字段。

当前只在本包内增量修订用户可读的公共策划、白话操作例与范围纪律。中性原型规格、测试证据、前三章蓝图、设定母包和22章预测账全部冻结为以后附录，不继续增量生产；用户完成公共玩法方向评审后，才按“跨章基础→C01-C03验证→逐章适配”决定下一步。
