# Design-L0–L3 设定回补与章级输入合同

> Status: `candidate_backfill_architecture_and_priority_register_complete / object_design_and_visual_approval_pending`
>
> Purpose: 规定“什么必须在写剧情和 gameflow 之前存在”，并用 C01-C03 Accepted Story、C04当前阻断点和C01-C22机制演化建立实际回补账。
>
> Machine registers: [全量回补账](data/setting-backfill-register.tsv)、[开篇GD2依赖闭包账](data/opening-gd2-dependency-closure.tsv)
>
> First master pack: [setting/wanji-master-pack-v0.1.md](setting/wanji-master-pack-v0.1.md)

## 一、为什么要增加设计底盘，而不是再加一个叙事层

现有叙事 L1-L3 分别负责体验宪章、全剧发动机和 22 章结构责任。它们回答“玩家为什么喜欢”“故事为什么持续发生”“每章必须把什么状态送到下一章”，但不会自动产出：

- 战棋回合、信息、行动经济和角色权能；
- 机器人身体、控制者、执行链、尺度和动作词汇；
- 城市、要塞、建筑和万机馆的平面、剖面、流线、损毁态；
- 章级地图、玩法承载、低保真 Previs 和资产 BOM。

因此本包暂以 `Design-L0` 至 `Design-L3`，稳定简称 `GD0` 至 `GD3`，建立一条与叙事层交叉校验的产品设计底盘。它不是新增 Story L3.5，也不自动改动现有六层生产链。

## 二、四层职责

| 设计层 | 所有者 | 回答的问题 | 最小交付 | 变更后的失效范围 |
| --- | --- | --- | --- | --- |
| GD0 产品与玩法合同 | 制作人＋主策 | 这是一款怎样玩的游戏，哪些玩法主次，长期状态怎样闭合 | 产品定位、核心循环、模式转换、持久状态、内容预算、非目标、验收法 | 核心循环/模式/体量改变时，GD1-GD3及所有消费它的章级设计重审 |
| GD1 系统、角色与机器人行动底盘 | 主策＋战斗/机体设计 | 玩家让谁做什么；谁解释、同意、拒绝和执行；身体如何改变世界 | 系统Registry、战术动作合同、角色权能矩阵、核心机体档案、成长和反制 | 控制权、能力、尺度、允许/禁止动作改变时，相关章 Stage20+ 失效；已写进故事则 Reader/验收也失效 |
| GD2 世界、地点、建筑与资产底盘 | 世界＋关卡＋美术 | 地点如何真实存在、怎样生活和作战、如何复用和损坏 | 地点Registry、外观/平面/剖面、流线、尺度、状态差分、地形规则、模块和视觉哈希 | 拓扑/通行/容量/形态改变时，消费章 GD3 与 Stage20+ 失效；故事可见事实变化时 Reader 同步失效 |
| GD3 章级游玩与资产合同 | 章策＋主笔＋关卡/导演 | 本章调用哪些已成立设计；哪些是新建；玩家如何经历；成本是否可做 | Cxx章级设计合同、来源追踪、Story-Play拓扑、地图灰盒、关键动作Previs、资产BOM | 来源、玩家代理、地图或大动作变化时 Stage20 起重编；只改数值/表现时只失效玩法/资产下游 |

### 2.1 不是“全世界先做完”，而是“本章依赖先闭合”

新方法不要求先把22章每座城市和每台机体做到最终美术，再允许写故事。它要求在章级写作开始前完成当前依赖闭包：

```text
本章固定故事问题
→ 会影响因果/路线/权限/身体/资产/揭示的对象清单
→ 这些对象的GD1/GD2最小档案与真实低保真图
→ GD3绑定与0个block
→ 才进入Stage20、Reader和gameflow
```

写作者仍可自由创造普通背景人物、无因果作用的生活道具、装饰和不改变成本的环境细节。下列内容不能临时创造：

- 具名城市、要塞、建筑、关键房间和形态；
- 核心机体、部位、工具、接口、动作和损伤；
- 角色能力、权限、同意、控制与停止方式；
- 改变路线、胜负、揭示或后续资产的装置/规则；
- 需要独立Rig、地图、UI、动画或长期状态的新概念。

因此这里解决的是“有计划的留白”，不是把Writer变成抄设定器，也不是允许Writer继续承担产品设计。

### 2.2 SSOT边界：档案只引用，不复制第二份真相

GD0-GD3不是第二套Canon和第二套Runtime状态库：

- Canon继续拥有实体身份、世界真相与Hard/Working/Candidate/History权威；`OPEN`不是Canon层，而是`design_status=open`；
- `system-state-contracts.tsv`继续拥有当前地点、身体、Roster、权限、同意、知识和Hub动态状态；
- `tactical-action-contracts.tsv`与`authority-action-contracts.tsv`继续唯一拥有玩家输入、前置、费用、效果、反制、失败和UI；
- GD1机体/能力/世界机制档案只保存静态身体、角色承诺、硬边界与上述合同的稳定引用；
- GD2地点档案保存默认功能、静态拓扑、合法接口、状态变体和视觉资产引用，当前开放/损伤/控制者来自状态快照；
- 揭示账只保存“原子事实 × 知识主体 × 章话边界”的投影，`truth_source_ref`指向Canon或Accepted Story，不复制第二份答案；
- GD3只绑定这些ID、版本与hash，不重复规则和真相。

统一状态词：

```text
authority_level = hard | working | candidate | history
design_status = open | draft | blocked | sealed | invalidated | retired
```

任何`open/blocked`引用、过期hash、缺视觉证据或缺回执都不能被GD3、Reader、gameflow或Runtime消费。

## 三、GD0 最小字段

```text
product_id
authority_status
experience_pillars
non_goals
primary_loop
secondary_loops
mode_transitions
persistent_state_domains
story_play_ratio
platform_and_input
content_and_asset_budget
prototype_strategy
human_acceptance
owner
version
```

GD0不允许只写“SRPG＋探索＋经营”。每种模式必须有玩家动词、输入输出、失败、时长、复用和与主循环的连接。

## 四、GD1 最小字段

以下字段是审查问卷，不是另一张动作/状态SSOT。机体、角色能力和世界机制分别使用：

- [data/mecha-dossier-schema.tsv](data/mecha-dossier-schema.tsv)
- [data/character-capability-dossier-schema.tsv](data/character-capability-dossier-schema.tsv)
- [data/world-rule-dossier-schema.tsv](data/world-rule-dossier-schema.tsv)

每个系统、角色能力或关键机体至少能回答：

```text
design_id
authority_status
source_refs
player_role
player_verb
information_input
controller
interpreter
consent_or_refusal_owner
executor_body
world_output
cost
counterplay
failure_result
visible_proof
scale_and_mobility
allowed_actions
forbidden_actions
unlock_and_growth
state_read_write
chapter_consumers
prototype_and_acceptance
```

实际实例必须以`canon_entity_id / action_ids / state_contract_ids / reveal_track_ids / visual_pack_ref / prototype_evidence_refs / acceptance_receipt_ref / version / content_hash`为骨架。当前热量、损伤、装备、驾驶绑定和开放状态不写入静态档案。

能力执行链必须完整闭合：

```text
玩家输入
→ 有限信息
→ 角色解释/提案
→ 权限或机魂同意检查
→ 现实执行身体
→ 地图/目标/伤损/关系变化
→ 费用、反制与持久后果
```

画稿、名字、记忆、资料和“系统决定”都不能跳过解释者、控制者与执行身体。

## 五、GD2 地点参考档案

字段定义见 [data/location-dossier-schema.tsv](data/location-dossier-schema.tsv)。每个长期地点必须至少交：

1. 日常功能、使用者、材质、光线、声景和文化锚；
2. 5-8个玩家可辨认分区、邻接、门禁和视线；
3. 人、0.5-3米小机、5-12米中型机、15-30米主力机、舰体和货物的不同路线；
4. 平时、封闭、战斗、损毁、修复/扩建等状态差分；
5. 探索节点、战棋区域、ADV站位、动画镜头和Hub功能；
6. 谁能控制门、电、武器、维修、移动、广播和停机；
7. 哪些事实后台已定，哪些画面何时向玩家揭示；
8. 可复用模块、独特资产、未来章节消费和资产等级；
9. 外观、平面、剖面、比例、状态图和关键动作草图的真实文件路径与哈希。

Mermaid、ASCII和文字表可以用于早期逻辑推演，但 Heavy 地点进入章级封存前必须有可直接审阅的低保真视觉文件；“能够画成”不等于已交付。

## 六、万机馆首个参考包范围

完整审计、WMP-00–15交付、消费者和用户看图项见 [setting/wanji-master-pack-v0.1.md](setting/wanji-master-pack-v0.1.md)。两张逻辑示意图为：

- [万机馆统一剖面问题图](setting/visuals/wanji-cutaway-schematic-v0.1.svg)
- [C01–C05身体形态与玩家控制梯度](setting/visuals/wanji-control-gradient-v0.1.svg)

当前证据数量为6层、30地点节点、19展区、8类泊位；它们是重要Hard锚点，但仍不是统一建筑/舰体设计。

现有 `wanji_floors.tsv`、`wanji_locations.tsv` 和 `wanji_carrier_berths.tsv` 作为事实底座，但首个 GD2 包仍需完成：

- 移动前旧会展馆、低矮巡航展舰、战场母舰和未来可变堡垒四种轮廓关系；
- L1/L2/L3/B1/B2、外部甲板和锁泊的统一剖面；
- 观众、居民、维修、货运、出击、避难和损毁隔离七套流线；
- 主展厅、机库脊柱、重型架、中型泊位、外锁泊和0号侧廊的尺度对照；
- 生活/开馆/整备/结算/关系/收藏/灾害/战斗八类系统插槽；
- 各章扩建、损毁、封闭和解锁账；
- 玩家第一小时能看见、C01E04才揭示、后续才揭示的空间揭示账；
- Hub探索灰盒、战棋状态图、关键界面、展舰启动和馆体受击的连续 Previs。

在用户选择视觉和空间方向前，这些内容均为 Candidate；不得从现有文字表推断正式外观。

## 七、GD3 章级合同字段

```text
chapter_id
story_authority_hashes
gd0_contract_id
gd1_system_and_mecha_ids
gd2_location_ids
chapter_player_promise
story_unit_to_play_mapping
episode_operation_encounter_topology
roster_entry_exit_state
available_player_verbs
encounter_objectives_and_failures
map_topology_and_state_variants
large_actions
new_vs_reuse_asset_bom
previs_paths_and_hashes
prototype_evidence
open_design_gaps
story_writer_free_fields
locked_fields
approvers
```

GD3的作用是把章责任转换成“调用已存在的产品设计”。如果关键动作没有 `system_id + player_verb + objective + visible_proof`，只能标 `open_design/block`；不能留给 Reader 或 gameflow 临时发明。

## 八、Stage20 八条硬门

1. **依赖封存门**：Stage20必须绑定GD0-GD3 ID、状态和内容哈希；缺 owner、未封存或哈希过期即阻断。
2. **禁止临时创造门**：具名角色、机体、能力、关键物件、地点、建筑和形态必须有合法 `source_id`；普通背景物除外。新关键概念退回GD1/GD2登记。
3. **机器人执行链门**：关键机体和能力必须闭合玩家输入、控制、解释、同意/拒绝、执行身体、输出、代价、可见证明和禁止动作。
4. **建筑空间可用门**：主要地点必须有连接、流线、准入、尺度容量、机体进出、战棋区域、状态差分和复用模块；仅有名称或小说描述不得通过。
5. **真实视觉证据门**：新地点/新机体至少交俯视灰盒、尺度轮廓和关键动作草图；Heavy章另交剖面/前后态、控制链、4-8格奇观草图、SRPG阶段灰盒和资产边界，记录路径与哈希。
6. **玩法承载门**：关键故事动作必须映射到 `system_id + mode + player_verb + objective + visible_proof`；无成立系统时标 `block/open_design`。
7. **资产与复用门**：每个新专名、装置和形态必须证明独特画面/玩法/情绪价值、复用窗口、资产级别、BOM和负责人；否则改用普通名或既有模块。
8. **零阻断与分级失效门**：所有必填字段、来源、视觉哈希和审批均通过且 `block=0` 才能封存；上游变化按事实影响范围失效，不允许暗补sidecar。

## 九、分级失效规则

| 变化 | 最早返回层 | 必须失效 |
| --- | --- | --- |
| 产品主循环、模式主次、持久状态改变 | GD0 | GD1-GD3、所有消费章设计与原型；是否失效故事由因果审计决定 |
| 角色权限、机体控制、能力因果、尺度或禁止动作改变 | GD1 | 相关GD3和Stage20+；若Reader已表现则Reader、章审和用户验收 |
| 地点拓扑、容量、路线、形态、损毁或控制权改变 | GD2 | 相关GD3和Stage20+；若为故事可见事实则Reader、章审和用户验收 |
| 玩家目标、地图、Encounter、代理权或大动作改变但故事结果不变 | GD3 | 导演/战斗/物理/Story-Play拓扑、gameflow、Runtime/资产；Reader经同义检查后可保留 |
| 纯数值、AI权重或不改轮廓的表现细化 | 玩法/资产下游 | 对应原型、平衡、Runtime或资产，不自动失效Reader |

## 十、实际回补账与优先级

机器账见 [data/setting-backfill-register.tsv](data/setting-backfill-register.tsv)。当前登记53项，分成：

- GD0产品/预算合同；
- 全局战术、信息/权限/同意、Roster权利；
- 万机馆、馆守Z、勇拳、BREAKER；
- 木桶街赛事、无牌一号、旧拳王、完全版王者、约九米转子；
- 工务城本地C2、职业工务机、社勇王、衡令、城梁一号；
- C01-C03地点/机体视觉包与GD3绑定；
- C04天空铸环阻断包；
- 三项权威/工程债和三章揭示账；
- 长期Hub、回访、共享Rig与开篇BOM。

优先级含义：

| 级别 | 含义 | 当前动作 |
| --- | --- | --- |
| P0 | 阻断对应章节的正式gameflow、连续Previs、美术、Runtime；未来章还阻断Reader | 先做档案、图、灰盒和用户回执 |
| P1 | 不阻断匿名规则灰盒，但阻断后续回访、长期Hub、资产预算或正式量产 | 在首个正式垂直切片/相关后章前完成 |
| P2 | 远期内容包与终局复用 | 只保留依赖和预算槽，不提前定细节 |

缺GD1/GD2不会自动推翻已经验收的Reader。对C01-C03先阻断下游并补兼容设计；只有实体设计证明可见故事事实无法成立，或用户决定迁移该事实时，才失效Reader和验收链。

## 十一、Writer / Reader安全上下文

Reader安全地点卡不得再手写第二份。它应由：

```text
GD2地点包
+ 当前ST_LOCATION / ST_BODY / ST_ROSTER
+ 当前reveal snapshot
→ 自动生成Writer-safe context
```

可直接给主笔：

- 当前已公开的普通地点名、日常功能、可见分区和连接；
- 当前画面可见的开放、损毁、危险、人物/机体位置；
- 本场人物确实知道的控制关系；
- `must_show / may_imply / must_hide`指令；
- 锁定字段和不改变因果的自由字段。

只给`entity_model / causality`，不直接给正文主笔：

- 完整承重、机体进出、控制/同意链和硬限制；
- 为避免因果矛盾必须存在但本场不得说出的后台规则。

只留制作侧或game-adaptation：

- system/action/state ID、成本、冷却、公式、AI反制和UI；
- 未来能力、秘密区域、未揭示接口和完整答案；
- 资产路径、hash、BOM、Previs、原型证据与审批回执。

揭示字段定义见 [data/reveal-ledger-schema.tsv](data/reveal-ledger-schema.tsv)。开放资料页只能消费玩家已经通过剧情或操作取得的知识，不能替Reader推进揭示或补因果。

## 十二、前三章追溯债与C04当前阻断

### 12.1 C01时序注释漂移

Accepted Reader锁定馆守Z在E02起身；Hard地点备注仍残留E03首次完整行动，story-chain战斗预案注释还写“社勇王出击”。新设计包一律读取Accepted Reader时序，另开非语义Canon/manifest更正票，不让旧注释进入Writer context。

### 12.2 C02“约九米转子”工程债

C02 Reader多次明确约九米，并已获得用户故事验收。新流程不能静默删数字，也不能把它当已验证机设。GD2必须实际证明：

```text
约九米直径
→ 运输架与重量
→ 港口龙门吊
→ 泊位吊机
→ B1货运升降台净空
→ 主循环安装包络
→ 旧转子锁存
```

若成立，补齐工程/视觉档案；若不成立，带着替代尺寸和对比图请求用户批准回改Reader。这是“剧情先临时发明设定”的直接债务样本。

### 12.3 C03旧预生产阶段漂移

Current Accepted Reader的顺序是E01换梁/拆三锁/工具被夺，E02追回四工具，E03缆索反转；旧预生产仍保存另一套阶段。C03 GD2/GD3必须以Accepted Reader重绘，旧表只作History证据。

### 12.4 C04不能继续靠Writer补铸环

C04当前只有天空环/工坊/B1等文字空间和0条真实`previs_asset`；专用预生产校验不通过。E03继续前必须完成天空铸环Master Pack、可撤回C2链、主要机体/接口包、真实低保真图与用户方向回执。否则会重复前三章的设计债。

## 十三、D08当前交付状态

已完成：

- GD0-GD3职责、SSOT边界和失效规则；
- 地点、机体、角色能力、世界机制与揭示五类门禁问卷；
- 53项实际回补账和优先级；
- 万机馆首个Master Pack审计；
- 两张可审阅的逻辑SVG；
- C01-C03追溯债和C04停止门。

尚未完成、不能伪称已成立：

- 万机馆正式外观、总平、剖面、生活/动力/损管空间；
- 木桶街、工务城、天空铸环的真实地图包；
- 核心机体的比例/三视/剖面/动作Previs；
- 三个地点/战术灰盒和用户视觉/试玩回执；
- Canon/manifest/Runtime迁移。

因此D08现在是“可执行的回补计划和首包问题图完成”，不是“世界设定已经补完”。

## 十四、当前流程缺口

现行 story-chain 中 `preproduction_model` 主要依赖 `series_alignment`，没有绑定跨章 GD0-GD3 SSOT。现有章级表也只有泛化 `source_ref` 和 `asset_tier`，没有强制设计包、视觉文件哈希或用户视觉审批。因此制度上要求“预生产先做”，机械门禁却仍可能放过纯文字包。

本包后续在 D09 中给出具体 manifest/schema/checker 迁移方案。在用户批准流程前，本文件只作为 Candidate 合同，不修改现行脚本。
