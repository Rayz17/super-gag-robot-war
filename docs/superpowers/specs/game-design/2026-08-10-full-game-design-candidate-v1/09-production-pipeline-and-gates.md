# 设定、故事、玩法与制作的新生产流程

> Status: candidate_workflow_defined / executable_gate_instances_and_user_approval_pending
>
> Scope: GD0-GD3 → L4/Reader → gameflow → Previs → Prototype → Runtime/Art → L6
>
> Authority: 本文只提出 Candidate 流程；不改现有 Canon、story-chain、Reader、Runtime 或 C01E02 Demo。

## 一、主裁决

当前需要修复的不是“再多写一份设定文档”，而是产品设计与故事生产之间缺少强制、可验证、可失效的接口。

以后必须同时运行三条不同生命周期：

1. **产品设计线**：先证明游戏怎样玩、角色和机器人能做什么、地点如何真实存在。
2. **故事创作线**：在已封存的物理与揭示边界内决定人物为什么行动、故事何时让读者知道什么。
3. **实现生产线**：在故事获得用户接受后，把已经成立的故事转换成 gameflow、连续 Previs、原型、资产和 Runtime。

三条线互相引用，但不能互相冒充：

- 设定齐全不等于故事好看；
- Reader通过不等于玩法好玩；
- Demo能运行不等于全游戏系统成立；
- 方向图获选不等于正式资产交付；
- 自动检查通过不等于用户验收。

C01E02 Demo不阻断本流程的产品设计和上游回补。制作人继续在隔离分支完成当前切片；只有带版本、录像、输入日志、测试者复述和明确范围的真人试玩结果，才可作为战术可读性证据回流，不能反过来锁定全游戏时制、数值、地图或长线系统。

## 二、双循环而不是一条瀑布

~~~mermaid
flowchart TD
    A["L1-L3：体验、全剧发动机、章责任"] --> B["GD0：产品与玩法合同"]
    B --> C["章级依赖发现：本章会消费什么"]
    C --> D["GD1：系统、角色能力、机器人身体"]
    C --> E["GD2：地点、建筑、城市、要塞与视觉"]
    D --> F["GD3：章级调用、Story-Play拓扑、BOM"]
    E --> F
    F --> G["设计Previs：比例、拓扑、身体动作、控制链"]
    G --> H{"依赖闭包与Stage20强门"}
    H -- "FAIL" --> C
    H -- "PASS" --> I["L4：因果、导演、物理与故事结构"]
    I --> J["L4.5前置承载边界：时长、模式、成本，不写最终gameflow"]
    J --> K["Writer安全上下文"]
    K --> L["纯剧情Reader与冷读"]
    L --> M{"用户故事验收"}
    M -- "修故事" --> I
    M -- "改上游事实" --> C
    M -- "接受" --> N["gameflow：把接受的故事转成玩家过程"]
    N --> O["连续玩法Previs：探索/战斗/演出/结算"]
    O --> P["规则灰盒与真人试玩"]
    P -- "规则失败" --> B
    P -- "章级适配失败" --> N
    P -- "通过" --> Q["资产Previs、Candidate BOM与视觉方向回执"]
    Q --> QA{"GATE-ASSET-AUTH：visual＋production授权回执是否齐全"}
    QA -- "FAIL" --> Q
    QA -- "PASS" --> R["有界正式资产制作并生成handoff候选"]
    R --> RH{"GATE-ASSET-HANDOFF：成品manifest/hash＋production验收回执"}
    RH -- "FAIL" --> R
    RH -- "PASS" --> RI["Runtime集成并生成候选构建"]
    RI --> RG{"GATE-RUNTIME：精确build/content manifest生产回执"}
    RG -- "FAIL" --> RI
    RG -- "PASS" --> S["Current候选构建、回归与玩法/视觉用户验收"]
    S --> T{"GATE-L6：正式交付证据是否齐全"}
    T -- "FAIL" --> S
    T -- "PASS" --> U["L6正式交付"]
~~~

### 2.1 写作前只做“依赖闭包”

不要求22章的全部城市和机体先做到最终设计。每章只需先完成会影响以下事项的对象：

- 故事因果与人物选择；
- 空间路线、尺度、通行与控制权；
- 机器人身体、动作、接口、损坏与同意；
- 玩家代理、目标、失败和持久后果；
- 后台真相、角色知识与本章揭示；
- 独立地图、Rig、UI、动画和长期资产。

普通生活细节、无因果作用的背景角色、装饰和不改变成本的道具仍是作者自由字段。

### 2.2 Previs必须拆成三种

| 类型 | 发生时点 | 回答的问题 | 最小证据 | 不能替代 |
| --- | --- | --- | --- | --- |
| 设计Previs | Reader前，GD2/GD3封存时 | 地点、身体、大动作和控制链是否真实可成立 | 比例轮廓、俯视灰盒、剖面/前后态、动作关键帧、控制图、真实文件哈希 | 连续玩法、镜头节奏、正式美术 |
| 连续玩法Previs | Reader故事验收后 | 玩家怎样从一个故事单位走到下一个，何处操作、失败、结算 | 可点击流程、地图走查、低模animatic或Godot捕获、Full/Skip结果 | 系统规则真人验证、正式资产 |
| 资产Previs | 规则原型通过后 | 哪些画面、Rig、UI和动画值得正式投入 | 视觉方向板、尺寸/材质/镜头测试、BOM、用户方向回执 | Sprite Master、正式Rig、Runtime授权 |

“文字写着可以画”不属于三种Previs中的任何一种。

## 三、标准章级生产顺序

### A. 章责任与依赖发现

输入为当前L3章责任、前章Accepted出口和GD0产品合同。章策只列：

- 本章必须改变的状态；
- 本章必须回答的故事问题；
- 玩家应该亲手经历的结果；
- 会影响因果、路线、权限、身体、揭示或资产的对象；
- 允许作者自由发挥的范围。

此时不得写具体战斗解法，不得为填场面临时创造城市、设施、机体部件或角色能力。

### B. GD1/GD2回补

系统主设、机体设计、世界/关卡和美术共同完成当前依赖闭包。每项必须有来源、所有者、状态、版本、内容哈希、真实视觉或原型证据和用户决策范围。

若某项只有名字或概念，状态只能是 open 或 blocked，不能写 sealed。

### C. GD3章级绑定与设计Previs

GD3不复制设定，只绑定已封存的ID、版本和哈希，并声明：

- Story beat与玩家动词的候选映射；
- Episode、Operation、Encounter与结算层级；
- 本章新建与复用资产；
- 地图状态和关键动作；
- 必须揭示、必须暂隐、作者自由字段；
- 真实设计Previs文件。

只要存在block、哈希过期、缺图、缺控制链或缺责任人，就不能进入Stage20封存。

### D. L4与Reader

L4决定人物欲望、因果、场面顺序和故事结果。前置L4.5只提供承载边界：本话大约哪些段落可能是ADV、探索、战斗或动画，以及时间和资产上限；它不能预写最终gameflow，更不能让玩法名词污染Reader。

Writer只收到自动投影的安全上下文，不收到后台秘密、未来章节真相、战斗公式、Action ID、资产术语或未到揭示时点的事实。

L4的“设计安全上下文”和Episode Reader主笔的 `CTX-WRITER` 是两个不同产物。L4只能读L3、前章Accepted出口、sealed GD3、passed `GATE-S20/S21` 及 `CTX-ENTITY`等实体/设计边界，不得绕过章级预生产证据，也不得读取一份尚未有当前L4便无法编译的 `CTX-WRITER`。L4通过后，`GATE-REVEAL` 才可绑定sealed L4、揭示快照和当前状态生成同范围的 `CTX-WRITER`，用于逐话纯剧情Reader。

Reader获得内部冷读和用户故事验收后，Accepted Story成为后续改编的固定输入。验收回执必须明确只接受哪些故事事实，不能顺带把玩法、美术或Runtime升级为已验收。

### E. gameflow与连续玩法Previs

gameflow从Accepted Story出发，逐个故事单位选择：

- 纯叙事；
- 轻探索/调查/工程实证；
- 战术Encounter；
- 过场或大动作；
- Operation或Chapter结算。

玩法可以决定过程、证据完整度、代价、伤损和局部路线，但不得改写Accepted人物选择与章末事实。若无法改编，必须提出显式故事迁移请求，不能暗改Reader或用过场强推结果。

### F. 原型、资产与Runtime

规则原型先在中性测试场证明系统有趣，再用章节适配灰盒证明故事和玩法相容。真人gameplay回执只解锁Candidate BOM和资产方向评审。GATE-ASSET-AUTH用visual回执与绑定Candidate asset manifest、预算和排除项的production授权回执，解锁有界正式制作；制作完成后，GATE-ASSET-HANDOFF再用成品路径/hash、QA与绑定最终asset manifest的production验收回执接受handoff。两门不能共用一张“既授权制作又验收成品”的循环回执。

Runtime构建必须携带内容清单、规则版本、来源哈希、正式/候选身份和资产授权状态。Candidate Demo、History Runner和正式发行构建不能共享一个含糊入口。

## 四、十七道门

机器可读定义见 [data/game-design-gate-registry.tsv](data/game-design-gate-registry.tsv)。
实际章/话/构建不能直接在这张定义表上写passed；每一个门实例必须另按 [data/game-design-gate-instance-schema.tsv](data/game-design-gate-instance-schema.tsv) 保存真实输入、hash、checker和回执。

| 门 | 核心问题 | 必须有人作出的判断 |
| --- | --- | --- |
| GATE-GD0 | 产品主循环、系统主次、状态和体量是否闭合 | 用户批准产品方向与非目标 |
| GATE-GD1 | 玩家动词、能力、身体、权限、同意和反制是否成立 | 主策与用户批准机制语义 |
| GATE-GD2 | 地点/建筑/机体外观、拓扑、尺度、状态和流线是否成立 | 用户看真实图选择方向 |
| GATE-GD3 | 本章是否只调用已存在设计，且预算可做 | 章策、主笔、关卡与制作人共同签封 |
| GATE-S20 | 章级预生产模型是否完整解释依赖、身体、地点、大动作与制作边界 | 制作人确认模型与设计证据闭合 |
| GATE-S21 | 机器实体动作表是否与Schema、来源和Stage20逐项一致 | 制作人确认0个block |
| GATE-L4 | 人物、因果、物理和章末状态是否独立成立 | 故事主编与冷读者 |
| GATE-REVEAL | Writer上下文是否只含当下可知且必要内容 | 故事主编确认暂隐与必揭示 |
| GATE-READER | 纯剧情Reader是否自然、清楚、有戏 | 冷读、人类声线审查 |
| GATE-U-STORY | 用户明确接受哪些故事事实 | 用户，范围必须逐项记录 |
| GATE-GAMEFLOW | Accepted Story是否被公平转成玩家过程 | 主策、主笔、关卡共同走查 |
| GATE-PREVIS | 连续体验是否可读、可做、值得做 | 用户看连续画面/灰盒，而非只看文字 |
| GATE-PROTOTYPE | 机制是否有趣、可理解、可复用 | 真人冷启动试玩与指定build/ruleset的gameplay回执；只解锁Candidate BOM |
| GATE-ASSET-AUTH | 方向、Candidate BOM和有界正式制作范围是否锁定 | 指定图包的visual回执＋指定Candidate asset manifest/预算的production授权回执，二者都通过 |
| GATE-ASSET-HANDOFF | 已完成资产是否与授权范围一致并可正式交接 | 成品文件/hash/许可/QA＋绑定最终asset manifest的production验收回执 |
| GATE-RUNTIME | Current故事、规则、资产和构建身份是否一致 | QA＋绑定精确build/content manifest的production回执 |
| GATE-L6 | 故事、玩法、视觉、可访问性和发行证据是否齐全 | 用户正式交付验收 |

任何门都必须保存：输入版本、内容哈希、检查结果、可见证据、人类回执、通过范围、未决项、下游解锁和失败回退点。

### 4.1 门定义与门实例不可混用

门定义只说明“所有章节都应检查什么”。门实例才表示“C04这一次是否真的通过”。实例至少要记录：

- gate_order、exact_position、depends_on_instance_ids和scope_instance；
- 每个actual_input_path及其SHA-256；
- 实际checker入口、参数、版本、退出码和报告路径；
- profile、所需类型/数量、文件存在/MIME/尺寸/hash结果和zero-block结果；
- receipt_authority_kind。产品决策门绑定decision_id、candidate_test_authorization/bounded_migration阶段和精确decision receipt set；单个故事/视觉/玩法/资产/构建门绑定gate receipt template与scope化set instance；
- requirement_ids、subject IDs、receipt phases、all/any要求，以及逐一对应的receipt_type、路径、hash、scope和cross-phase reuse检查；
- checked_at、checked_by、当前状态、失效原因和invalidation_targets。

缺任一实际证据时，实例只能是missing或blocked，不能从定义表中的candidate_defined推断passed。

### 4.2 五种用户回执必须分开

范围合同见 [data/user-acceptance-scope-contracts.tsv](data/user-acceptance-scope-contracts.tsv)：

- 产品方向回执只批准主循环、模式主次、系统语义、角色能力方向、体量与明确非目标；
- 故事回执只提升明确列出的Reader事实；
- 玩法回执只提升指定ruleset/build/map的理解、趣味和操作结论；
- 视觉回执只提升指定对象、方向和衍生设计范围；
- 生产回执只提升指定资产handoff、构建或L6范围。

visual回执永远不授权正式asset handoff或Runtime；gameplay回执永远不授权正式BOM。GATE-ASSET-AUTH需要visual与production授权两个独立回执，只允许有界正式制作；GATE-ASSET-HANDOFF另需绑定成品manifest的production验收回执；GATE-RUNTIME还需另一个绑定精确build/content manifest的production回执。

十五项产品决策的两阶段集合见 [data/decision-receipt-sets.tsv](data/decision-receipt-sets.tsv)，只回答“是否允许这类Candidate测试或有界迁移”。单个Reader、图包、Previs、规则build、资产包、Runtime build与L6的操作回执模板见 [data/gate-receipt-set-templates.tsv](data/gate-receipt-set-templates.tsv)。后者必须为每个scope/version生成独立set instance；`authorization`、`handoff`、`runtime`、`delivery`不得复用同一receipt path或hash。DEC-12视觉方向或DEC-14切片投资裁决不能替代任何单个资产/构建门。

C01-C03现有故事回执不得拿来填GD0、GD2、试玩、视觉或正式资产门。

## 五、内容寻址来源DAG与Writer安全投影

机器登记见 [data/source-context-projection-registry.tsv](data/source-context-projection-registry.tsv)。
快照、上下文请求、编译清单、gameflow、Previs和Build的字段合同见 [data/production-snapshot-schema.tsv](data/production-snapshot-schema.tsv)。

来源关系应是一张由ID、版本和内容hash连接的有向无环图，而不是若干手写摘要：

~~~text
Canon / Accepted Story / sealed GD0-GD2
→ authority_snapshot + design_snapshot + reveal_snapshot
→ GD3 / Stage20 entity_model projection
→ sealed Stage20/21 snapshot
→ scene_plan projection
→ Writer draft projection
→ Accepted Reader snapshot
→ gameflow projection
→ Previs / Prototype / Asset / Runtime manifests
~~~

安全卡是编译产物，不是第二份真相。任何上游hash变化都必须让所有消费它的上下文实例变为stale；重新编译后只有语义影响审计决定是否需要重写故事。

### 5.1 同一个来源对不同角色产生不同投影

| 消费者 | 应收到 | 不应收到 |
| --- | --- | --- |
| entity_model | 静态真相、身体、尺度、控制、硬限制、状态入口/出口 | 未获权威的候选答案 |
| scene_plan | 当前可见空间、人物位置、动作可行性、场面必须证明什么 | 最终对白和作者声线 |
| writer/draft | 当下状态、可见锚点、路线、必揭示、暂隐、锁定/自由字段 | Action ID、数值公式、资产级、未来秘密、后台全知说明 |
| gameflow | Accepted Story单位、合法系统/动作、地图、目标、Outcome合同 | 改写固定人物选择的自由 |
| asset production | Accepted Story、approved gameflow/ruleset、原型证据、用户方向回执、passed `GATE-ASSET-AUTH`、授权Candidate BOM/Rig/UI/VFX/音频与预算上限 | 未获制作授权的对象；尚未生成的handoff或Runtime回执 |
| runtime/integration | Accepted Story、approved gameflow/ruleset、passed `GATE-ASSET-HANDOFF`、最终asset manifest与精确来源hash | 仅获制作授权但尚未验收handoff的资产；History/Candidate入口 |

`CTX-PRODUCTION` 用于资产制作，只能依赖 `GATE-ASSET-AUTH`；`CTX-RUNTIME` 用于集成，必须依赖制作结束后的 `GATE-ASSET-HANDOFF`。两者不得共用一个编译产物，也不得让资产制作反向依赖它尚未生成的handoff。

### 5.2 编译必需字段

每份上下文快照至少保存：

~~~text
context_id
consumer_phase
chapter_id
episode_id
source_ids
source_versions
source_hashes
authority_levels
visibility_profile
admitted_fields
redacted_fields
must_surface
must_not_surface
locked_fields
free_fields
generated_at
compiler_version
context_hash
~~~

编译器发现未登记来源、History来源进入Current、Candidate来源伪装Working、哈希漂移、缺失可见性或未来秘密泄漏时必须FAIL，不能静默跳过。

`draft` 模式还必须绑定同范围、同 `source/reveal/policy hash` 且状态为 `passed` 的 `GATE-REVEAL` 实例。该门通过前只允许生成不含Writer可读内容的 dry-run manifest/hash；门实例通过后才能生成 `CTX-WRITER` 产物。决策回执、reveal snapshot 存在或lint单项PASS都不得代替该实例。

## 六、分级失效，不一刀切回滚

机器规则见 [data/invalidation-routing-rules.tsv](data/invalidation-routing-rules.tsv)。

核心原则：

1. **改上游设计不自动废弃全部故事。** 先判断是否改变玩家已看见的事实、因果、人物选择或章末状态。
2. **改变故事固定事实也不能只修gameflow。** 必须回到Reader并重新取得相应范围的用户接受。
3. **纯玩法改动不应污染Reader。** 时制、数值、AI和不改变故事结果的地图细化只失效原型、gameflow、Previs和Runtime。
4. **视觉细化不越过已批准轮廓和尺度时，只失效资产下游。**
5. **所有失效必须由来源依赖图自动传播，并保留旧版本History。** 禁止在sidecar里暗补事实后继续声称上游passed。

## 七、故障注入回放

新门禁必须能主动抓住当前已经发生过的问题：

| 用例 | 故障 | 应在哪一门失败 | 正确处置 |
| --- | --- | --- | --- |
| FI-C01-ENTITY | story-chain或制作备注仍写社勇王，而Accepted C01实际为勇拳 | 来源语义/实体绑定检查 | 修正非语义登记并重算hash；不改Accepted Reader |
| FI-C01-C02-ROTOR-9M | C01 Accepted出口已经说九米级测试转子，C02落实为约九米冠军转子，但没有运输架、吊点、B1净空、安装包络等GD1/GD2工程证据 | GD1/GD2/GD3 | 保留Accepted事实并阻断正式地图/资产；若工程否定九米，展示替代方案并由用户授权故事迁移 |
| FI-C03-SEQUENCE | 当前story-chain所绑定的Stage21仍写城梁一号C03E03进入，Accepted Reader已在E01完成换梁 | GD3来源hash、story-state seed与Episode状态顺序比较 | 重建GD3/Stage20/21/gameflow；若只重绑既有事实，以语义等价回执保留Reader |
| FI-C04-SCHEMA | 预生产表使用不合法状态、类型和资产级却被manifest标passed | GATE-S21专用schema检查 | Stage21退回blocked，Stage20/21实例均不得解锁导演板 |
| FI-S20-S21-BYPASS | L4门实例只绑sealed GD3，没有同范围passed `GATE-S20/S21` | GATE-L4依赖检查 | L4实例blocked；先补真实设计Previs、Stage20模型与Stage21专用语义门 |
| FI-C04-PREVIS | Heavy章只有文字声称“可画”，0个真实previs文件 | GATE-GD2与GATE-PREVIS | 补比例、地图、剖面/前后态、控制图、4-8关键帧并验证文件/hash |
| FI-SOURCE-MISSING | GD1/GD2/GD3未登记进Runtime/Writer来源表 | 来源编译门 | 编译FAIL，登记来源、阶段与可见字段后再生成上下文 |
| FI-SECRET-LEAK | Writer卡含未来真相、战斗公式或资产术语 | GATE-REVEAL | 阻断draft并重新投影 |
| FI-L4-WRITER-CYCLE | `GATE-L4` 把需要当前sealed L4才能编译的 `CTX-WRITER` 当作自己的前置输入 | 来源DAG与GATE-L4/REVEAL依赖检查 | 编译FAIL；L4只读实体/设计安全包，L4通过后再由GATE-REVEAL解锁CTX-WRITER |
| FI-PRODUCTION-CYCLE | 资产制作上下文反向依赖“制作完成后才可产生”的handoff或Runtime回执 | 来源DAG与GATE-ASSET-AUTH/HANDOFF依赖检查 | 编译FAIL；资产制作只读授权实例，Runtime集成才读已验收handoff |
| FI-DEMO-PROMOTION | Candidate Demo内部PASS被写成正式玩法/资产验收 | GATE-PROTOTYPE/GATE-ASSET-AUTH/GATE-ASSET-HANDOFF/GATE-RUNTIME | 要求真人证据、用户回执和正式handoff，保持Candidate身份 |

最低自动回归要求：

- 故障注入样例必须全部按预期FAIL；
- 修复后只解锁预期的下游，不得误升用户验收；
- 任一来源内容变化都导致context_hash改变；
- 同一快照重复编译字节一致；
- `GATE-L4` 必须绑同范围passed `GATE-S20/S21`，且不得依赖 `CTX-WRITER`；只有passed `GATE-L4` 和sealed L4 snapshot才能进入 `GATE-REVEAL`；
- 来源与门实例依赖保持DAG，`CTX-PRODUCTION` 不得依赖 `GATE-ASSET-HANDOFF`或Runtime回执；
- History来源不能进入Current draft、gameflow或Runtime；
- 文件存在、MIME、尺寸、SHA-256和manifest引用一致；
- Heavy profile所需Previs类型和数量满足配置，而非仅关键词出现。

定义层依赖顺序可用以下只读命令重跑：

```bash
python3 docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/scripts/check_d09_gate_dependency_order.py
```

该命令只证明门/上下文定义不越级、不循环；它不创建门实例、不执行故障注入、不代表任何用户回执或Current流程迁移。

### 7.1 现行工具实测

2026-08-10只读回放得到：

- C04 manifest把Stage20和Stage21分别标为passed，并保存了hash；
- 通用packet checker对C04 Stage20返回PASS；
- 专用check_chapter_preproduction_model.py对同一C04 Stage21直接FAIL：全表仍用candidate状态，且包含schema不接受的character_group和mecha_group；
- C04目录没有真实图片、SVG、PDF、animatic或灰盒捕获，表内也没有previs_asset行；
- Stage21 preproduction_table不在check_v35_story_chain.py的PACKET_CONSISTENCY_STAGES集合；
- 专用preproduction checker在现行生产脚本中没有调用点；即使表内存在block，它目前也只计数并返回PASS；
- 普通story-chain audit验证的是文件存在、顺序和封存hash，不会重跑首次封存时的语义门；
- C03当前Stage21错序同时通过了通用checker、专用checker和story-chain，因为它们没有比较Accepted Reader或story-state seed的Episode顺序。

因此实施时还必须增加EPISODE_STATE_ORDER_MISMATCH一类跨层错误；“字段合法、0 block、hash新鲜”仍不等于语义正确。

## 八、Session分工与交接

Session不能按“每个人写一份大文档”分配，而应按权威和状态写入权分配：

| Session | 独占写入 | 可只读消费 | 必交回执 |
| --- | --- | --- | --- |
| 产品/系统主设 | GD0、系统Registry、动作/状态合同、机制版本 | Canon、Reader、研究、Demo证据 | 规则diff、原型问题、失效范围 |
| 世界/地点/机体 | GD1/GD2静态档案与设计Previs | Canon、系统合同、章依赖 | 图路径/hash、尺度/流线、控制链、用户看图项 |
| 章节故事 | L4、Writer安全Reader | sealed GD包、前章Accepted出口 | 故事事实diff、揭示快照、冷读与用户故事回执 |
| 游戏改编/关卡 | gameflow、地图灰盒、连续玩法Previs | Accepted Reader、系统/地点包 | Story unit映射、Outcome、试玩版本 |
| 制作人/Runtime | 原型实现、BOM、正式handoff、build manifest | 封存设计、视觉方向、测试证据 | 构建身份、来源hash、资产授权、回归与试玩包 |
| QA/冷测 | 只写证据Registry和缺陷 | 指定版本构建与测试脚本 | 录像、输入日志、复述、失败分类、不可复现说明 |

单个字段只能有一个权威写入者。其他Session以变更请求提交，不直接改对方SSOT。

交接包至少包含：

~~~text
handoff_id
from_session
to_session
scope
source_ids_and_hashes
deliverables
known_open_items
forbidden_inferences
expected_consumer
acceptance_method
rollback_or_invalidation_route
receipt_status
~~~

## 九、C01E02 Demo的隔离与回流

制作人无需等全游戏骨架完成才继续Demo，主策也无需等Demo完成才设计产品。两者并行，但只有窄接口：

### Demo可回流

- 输入与相机是否顺手；
- 单位、地形、目标和敌方意图是否看得懂；
- 命令路径和撤销是否清楚；
- 压力、失败原因和下一步是否可复述；
- Full/Skip、存读档和分辨率等技术结果；
- 已加载资产的具体构建身份与授权范围。

### Demo禁止回流为全局规则

- 当前地图尺寸、单位数量、HP、伤害、回合数；
- 护盾取得、架势、冲击、盾击的专用脚本链；
- 当前IGOUGO时制；
- C01E02剧情角色与敌人配置；
- Candidate运行时已加载某资产，就推定正式资产handoff完成；
- 内部M2/M2.4 PASS，就推定真人玩法或用户视觉验收完成。

所有回流必须绑定 build_id、content_manifest_id、ruleset_version、asset_authorization_state、tester、录像/日志和测试范围。静态生产Registry、运行时加载状态和用户回执是三条不同证据，不得合并成一个“完成”标签。

### 9.1 2026-08-10当前双层状态

最新M2.4证据不是“仍无任何真实图”，也不是“正式资产已经完成”。两层状态同时成立：

~~~yaml
registry_baseline:
  approved_handoffs: []
  runtime_art_loaded: false
  meaning: 静态注册基线没有正式资产promotion

active_candidate_observation:
  validated_handoff_count: 5
  loaded_slot_count: 5
  resource_probe_count: 5
  runtime_art_loaded: true
  meaning: Candidate Runner按冻结receipt加载了A4 MAP-B五个字节级副本

formal_runtime_promotion: not_authorized
human_joint_playtest: awaiting
~~~

所以应把结论写成：M2.4 Candidate实现与自动门已通过，真实A4五槽在该Runner内加载，其他槽仍fallback；当前停在制作人与用户联合试玩前，不能提升为正式Runtime、完整动态地图美术或全游戏战棋验收。

## 十、C04恢复门

C04当前不能因story-chain显示episode_e03为下一点就直接续写。恢复E03前至少完成：

1. 天空铸环GD2 Master Pack：总体轮廓、尺度、横/竖两态、5-8分区、路线、控制权、前后/损毁态；
2. 真实设计Previs：比例板、俯视灰盒、剖面/状态图、控制链、4-8幅关键画面、SRPG阶段灰盒；
3. 主要机体、独臂百相、七号、三地方旗舰和断冠的GD1动作/控制/接口边界；
4. 可撤回C2链：提案→工程核验→权限/机魂同意或拒绝→提交→身体执行；
5. C04 GD3重新绑定Current四话结构、状态和资产BOM；
6. 专用预生产checker、文件/hash/profile和来源编译全部通过；
7. 用户看图批准地点、机体和关键动作方向；
8. 对E01/E02做兼容审计。只有GD包改变已呈现事实或因果时才失效重写，不自动废弃已经通过的单话。
9. 以同范围、同来源hash的新GD3/S20/S21实例和当前L4生成 `GATE-L4` 兼容实例；兼容审计改变因果、物理、人物选择或章末状态时，返回L4并按影响失效，不得强制标PASS；
10. 只有同范围 `GATE-L4` 兼容实例PASS后，才可编译并送审C04 E03 `GATE-REVEAL`实例；只有REVEAL实例PASS才生成Candidate `CTX-WRITER`。

## 十一、实施顺序

本包获用户原则批准后，脚本和正式Registry迁移仍需另行授权。建议顺序：

1. 先增加门Registry、来源投影、失效路由和回执Schema；
2. 把Stage20模型证据检查与Stage21专用preproduction checker分别接入实际门；Stage21加入PACKET_CONSISTENCY_STAGES，普通audit和before-stage也重跑语义门；
3. 给专用checker增加strict-zero-block、来源权威、设计版本/hash、真实previs文件和跨Episode状态顺序检查；
4. 为实际文件增加存在、hash、MIME、尺寸和profile数量检查；
5. 把GD0-GD3、reveal和Accepted Story登记进来源Registry，并要求每行绑定gate实例与回执scope；
6. 生成Writer-safe、gameflow-safe和production-safe三种上下文；编译前验证gate实例，普通check重验而非只比较旧hash；
7. 用上述十一项C01-C04/流程故障注入样例做回归；
8. 先补万机馆、木桶街、工务城、天空铸环四个GD2包；
9. C04依次通过GD/S20/S21、同范围L4兼容门和REVEAL门后再续E03；
10. C05起按新流程原生生产，不再事后补设定。

## 十二、完成定义

D09文档与机器Registry完成，只代表流程设计可供裁决。新流程真正成立必须同时满足：

- 用户批准角色分工、门顺序、Accepted Story与gameflow的先后关系；
- 专用脚本门禁已接入实际story-chain；
- C01-C04故障注入全部按预期失败/修复；
- 至少一章从依赖发现走到Writer安全Reader；
- 至少一章从Accepted Reader走到连续Previs和真人玩法验收；
- 没有任何自动PASS、内部PASS或Candidate构建被误写成用户接受或正式L6。
