# 当前产品基线与缺口

> Status: `historical_evidence_snapshot / read_only_audit / 2026-08-10 / superseded_for_public_direction`
>
> Verdict: `NO_UNIFIED_PLAYABLE_GAME_LOOP`
>
> 2026-08-11阅读注：这份文件保留当时的缺口快照，不再作为当前产品方向入口。请先读 [用户阅读入口](00-user-reading-guide.md)。本文第6.2节的“Episode持续边界”是旧内部分层；当前玩家前台只采用Encounter、Operation、Chapter三级结算口径。木桶街、货运环、万机馆等设定回补也已停放，不计入玩法成熟度。

## 一、主策划裁决

用户的判断成立，而且需要用比“已有一部分但不够”更严格的表述：

**当前不是一套完整玩法等待补全，而是已验收故事、Candidate 玩法词汇、可复用 Runtime 零件和单话脚本切片并存；它们尚未组成一套全游戏规则，更没有形成经真人验证的核心循环。**

因此本包不会把“已有 SRPG、探索、经营、关系”等名称当成系统资产。除通用状态、存档、场景对象、提交回执、演出队列等技术骨架外，战棋决策模型、角色权能、编队、成长、Hub、探索、战略、收藏和结算都要重新证明。

## 二、证据成熟度标尺

| 级别 | 名称 | 证明了什么 | 没有证明什么 |
| --- | --- | --- | --- |
| M0 | 名词/愿望 | 项目想要某类体验 | 没有规则、操作或闭环 |
| M1 | Candidate 概念 | 有边界、输入输出或设计方向 | 未证明决策有趣、彼此兼容 |
| M2 | 可原型规则 | 动词、状态、费用、失败、反制和反馈可以实现 | 未证明代码正确或玩家看得懂 |
| M3 | 可运行零件 | 单个状态机、场景、AI、存档或交互能运行 | 未证明它们组成一场好玩的游戏 |
| M4 | 可玩切片 | 玩家能从开始走到局部结束 | 未证明可复用、平衡、长线成立 |
| M5 | 真人玩法验收 | 目标玩家能理解、做选择并愿意继续 | 只对该版本、该范围有效 |
| M6 | 产品闭环验收 | 主循环、辅助循环、成长和章节持续状态共同成立 | 仍需正式内容与商业质量生产 |

项目现有“passed”“Working”“Current”描述必须映射回这套证据标尺；Canon 权威和制作成熟度是两条轴。

## 三、当前产品真相

### 3.1 故事生产

- L1、L2、H0、L3 是 Working；它们锁定体验、总发动机、世界边界和 22 章结构责任。
- C01-C03 的 Reader 已由用户明确接受；验收回执均排除 Runtime、美术和 L6，C03还明确保留游戏流程、镜头和数值继续优化。
- 看板当前为 L4 `4/22 passed`、L5 `3/22 complete`、用户验收 `3/22 accepted`、L6 `0/22 complete`；C04 唯一合法故事阶段是 `episode_e03`。
- 这证明前三章故事可作为玩法输入，不证明前三章已成为游戏。

证据：

- `docs/superpowers/specs/剧情梗概/V35六层创作生产看板.md:9-44`
- `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C01/C01-用户创作验收回执.md:8-18`
- `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C02/C02-用户创作验收回执.md:8-18`
- `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C03/C03-用户创作验收回执.md:8-18`

### 3.2 现有玩法文档

- 五个长线循环和六个系统家族全部标作 `candidate_*`；每项大多只有一行核心循环和输入输出。
- L4.5、story-play topology 和 Candidate gameflow 能提供场面、Operation、状态继承和成本线索，但没有统一定义回合、行动经济、信息、AI、伤损、编队、成长、难度和教程。
- 旧框架 `2026-06-18-chao-gag-game-framework-design.md` 已在 registry 登记为 History。
- `upgrade_paths.tsv`、旧 Credits/PP/Full Custom Bonus 和十二章练度预算属于旧式传统 SRPG 候选，既与当前 22 章结构漂移，也与“重故事、轻练级、角色权限型能力”方向冲突。

证据：

- `docs/superpowers/specs/data/story/v35_series_gameplay_architecture_v1.tsv:1-6`
- `docs/superpowers/specs/data/story/v35_series_gameplay_system_families_v1.tsv:1-7`
- `docs/superpowers/specs/data/design_graph/doc_registry.tsv:4,794,816`
- `docs/superpowers/specs/data/gameplay/upgrade_paths.tsv:1-13`
- `docs/superpowers/specs/data/gameplay/mission_balance_targets.tsv:1-15`

### 3.3 可运行证据

- 通用状态、幂等事务、存档、Episode 提交/恢复、空间对象和 Desk 确认壳是可复用技术骨架。
- 通用战斗核仍是固定矩形网格、BFS、简单目标判定和简化伤害的沙盒零件；它没有证明本作需要的战术深度。
- 当前默认入口指向 C01E02 Candidate Demo。其构建身份明确为 `candidate_runtime_demo`，只绑定 C01E02。静态正式Registry仍是 `approved_handoffs=[] / runtime_art_loaded=false`；但最新M2.4 Candidate活动回执已在该Runner内验证并加载A4 MAP-B五个槽位，运行观测为 `validated=5 / loaded=5 / probes=5 / runtime_art_loaded=true`。这两层证据不能互相替代。
- C01E02 当前是围绕馆守Z取得盾、架势、拦截、冲击和盾击的脚本化切片；它不能证明一般编队、主角团权能、长期成长或全章节闭环。
- Demo 内部完成报告仍要求制作人/用户真人试玩。没有任何长线玩法达到 M5。

证据：

- `game-godot/scripts/core/state/run_state_store.gd:7-143`
- `game-godot/scripts/core/battle/battle_session.gd:37-80`
- `game-godot/scripts/core/battle/combat_resolver.gd:4-37`
- `game-godot/scripts/core/battle/grid_service.gd:4-84`
- `game-godot/scripts/core/battle/targeting_service.gd:4-34`
- `game-godot/scripts/core/startup/startup_target_selector.gd:4-15`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-m2-4/05-completion-report.md:1-37`
- `game-godot/content/candidate_runtime_demo/c01/e02/generated/build_identity.json:2-28`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/candidate_tactical_session.gd:5-41,186-279`
- `docs/superpowers/specs/production/c01-current-demo-v1/19-current-demo-inplace-rebase-producer-contract.md:129-139`

## 四、系统成熟度盘点

| 系统 | 当前最高证据 | 当前可保留 | 必须重新设计/证明 |
| --- | --- | --- | --- |
| 战棋核心 | M3 零件；M4 单话脚本切片 | 网格、选择、状态、Intent/Forecast接口、演出与存档管线 | 回合与信息模型、行动经济、反应、地形、多格体、目标/失败、AI、难度、教程、通用关卡语法 |
| 主角团 C2 权能 | M1 候选人物能力 | Canon 权限上限、人物职责、BattlePatch接口思路 | 导航、视野、引导、预演、机魂、授权、工程验证的操作、费用、反制、失败与组合 |
| 编队与部署 | M1 名词/容量方向 | 机体生命周期、泊位与驾驶关系边界 | Roster、岗位、出击成本、受伤替换、机体同意、部署UI与地图容量 |
| 装备与库存 | M1；通用资源字典 M3 | 事务容器、部件依赖和泊位语义 | 装备实例、库存容量、任务借出、损坏/修复、功能成长、无刷级经济 |
| 探索与解谜 | 空间运行 M3；玩法 M1 | 房间、稳定对象、状态快照 | 移动/观察/取证/机体沟通/环境规则、谜题语法、失败与返回、轻松节奏 |
| Hub/万机馆经营 | 空间事实 M1-M2；系统 M1 | 楼层、地点、泊位、展区、容量表 | 日程、岗位、维修、开馆、资源、关系事件、设施变化和界面闭环 |
| 关系事件 | 状态字段 M3；规则 M1 | relationship_edges与人物Canon | 事件调度、许可、组合技、冲突/和解、不可刷取的成长和结算反馈 |
| 收藏/图鉴 | 内容分类 M1-M2 | 藏品、展区、谱系和终端语义 | 解锁、展陈、剧透层、机体欲望、玩家偏爱和玩法回报 |
| 工程/制造 | M1 候选循环 | 模型→工程→全尺寸→主体确认的因果边界 | 材料/工时、试作、失败、接口、UI、资产复用与长线成本 |
| 世界地图/战略 | M1 名词 | 22章目的地、延迟通信、舰队/泊位边界 | 节点、时标、路线、任务调度、未选路线结果、外部机群与信息保真 |
| 章节结算 | Desk/事务壳 M3；产品规则 M1 | 预览→确认→提交、持久状态 | 战果、伤损、关系、资源、世界债务、奖励、返航、Mission Clear层级 |
| 小游戏 | 16个模板 M1；两种语法 M3 | Constraint/Timing等通用交互语法 | 哪些值得保留、每类核心乐趣、短时长、无惩罚调剂与共同结果契约 |

## 五、万机馆与上游设定缺口

用户所说“万机馆没有完整参考档案”基本成立，但要区分“没有事实表”和“没有可供创作/制作使用的完整设计”。

现有 Canon 已登记楼层、连接、泊位、尺度、开放状态和部分用途：

- `docs/superpowers/specs/data/canon/wanji_floors.tsv`
- `docs/superpowers/specs/data/canon/wanji_locations.tsv`
- `docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv`

这些表能防止无限机库和基本拓扑错误，却仍缺少一个统一的“万机馆参考档案”：

1. 外形、剖面、尺度和移动/展舰形态；
2. 每层 5-8 个可见分区、邻接和人/机/货物流线；
3. 生活、维修、开馆、战斗、灾害和封闭状态；
4. 角色岗位、控制权、机魂边界和停机链；
5. 章节前后损毁、扩建和视觉连续性；
6. 可复用探索地图、战棋地图、背景、动画和UI资产；
7. 当前能展示什么、未来何时揭示什么；
8. 真实低保真平面、剖面、比例、状态图和连续 Previs，而不只是文字说“可以画”。

同样的回补原则适用于每章关键城市、要塞、巨构、主战机体和新能力。剧情总纲决定“为什么去”；章级预生产必须先回答“那里真实存在什么、谁能操作什么、怎样移动和损坏”；Reader只决定玩家何时看见，不应临时造设定。

## 六、第一批从零设计清单

### 6.1 战棋主玩法

1. 回合结构、同时/交错执行和行动承诺窗口。
2. 不完整战报、来源、时效、置信度、盲区和敌方欺骗。
3. 移动、姿态、攻击、保护、救援、撤退、变形、合体和非致死停机。
4. 反应、警戒、截击、援护、碰撞、推拉、破坏与地形变化。
5. 大小机体、多格单位、舰体、城市设施和地图边缘支援。
6. 纪存、七海、白鸢、工程组及后续角色的战场权能。
7. 驾驶员、机魂、支援席、权限主体和玩家代理边界。
8. 目标、失败后果、撤退、分支和 Mission Clear。
9. 敌方 Intent、学习、干扰、权限夺取和信息反制。
10. 低刷级成长、装备功能、关系协议、伤损和章节持续状态。

### 6.2 辅助玩法

1. 万机馆 Hub 日程、岗位、维修、开馆、展陈和关系事件。
2. 轻量场域探索、环境谜题、机体沟通和物件调查。
3. 模型/工程试作、小游戏语法和失败保留。
4. 世界地图、延迟通信、任务选择和未选路线结果。
5. 收藏、图鉴、剧透层、展陈反馈和偏爱表达。
6. Encounter、Operation、Chapter三级持续与结算；Episode只保留为内部内容组织边界，不新增一次玩家结算。

## 七、当前阻断与并行关系

- 不需要等待制作人完成 C01E02 Demo 才开始全游戏设计；Demo 是战术节奏、输入、镜头和可读性的并行实验。
- 在新战棋基础循环通过 G3 前，不把 C01E02 脚本链泛化成全游戏战斗规则。
- 在万机馆和前三章关键地点完成低保真设定包前，不为它们投入正式连续资产，也不让后续 Reader/gameflow 静默新增结构。
- 当前知识库检查失败：`scene_entity_presence.tsv` 的 `PRES_C01E01_RIFT_SWARM` 使用 `remote_contact`，而检查器允许集合没有该值。此项是当前数据/门禁债，不由本策划包静默修复。
- 当前工作树有大量并行变更；所有基线结论都以 2026-08-10 的只读检查为时间戳。

## 八、2026-08-10 实测

| 检查 | 结果 | 含义 |
| --- | --- | --- |
| `python3 scripts/report_v35_layered_pipeline.py --check` | PASS | 六层看板与机器状态一致 |
| `check_v35_story_chain.py ... C04 ... --next` | `NEXT: episode_e03`，下游旧件 invalidated | 只说明故事链合法位置，不说明产品骨架完成 |
| `python3 scripts/check_story_knowledge_base.py` | FAIL：`Invalid presence mode: PRES_C01E01_RIFT_SWARM` | 知识库当前不能声称全绿 |
| C01E02双层资产状态 | 静态Registry为`approved_handoffs=[] / runtime_art_loaded=false`；M2.4 Candidate活动回执为`validated=5 / loaded=5 / probes=5 / runtime_art_loaded=true` | 五槽加载只证明指定Candidate Runner的活动回执；不是正式资产handoff、正式Runtime或产品闭环 |

## 九、G0退出条件

G0 只有在以下条件满足时结束：

- 十二项产出物有路径、依赖、验收人和明确状态；
- 所有设计统一采用机制评价卡；
- Current/Working/Candidate/History和M0-M6不再混用；
- C01-C03、Demo、Runtime与万机馆输入范围被登记；
- 已知冲突、数据门禁债和工作树隔离规则被记录。

本文件完成后，下一步进入 G1 外部研究，而不是直接凭直觉写战棋技能表。
