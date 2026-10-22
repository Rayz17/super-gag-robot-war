# 《超GAG机器人大战：万机残响》玩法数据说明 v0.1

本目录承接 [多元游玩体验策划](../../2026-06-22-chao-gag-hybrid-play-experience-design.md)，用于把“SRPG之外的多元玩法”拆成可追踪、可实现、可回流到战斗和剧情的数据。

跨文档口径、节点关系和风险清单见 [设定图谱数据说明](../design_graph/README.md)。

## 文件

| 文件 | 用途 | 当前规模 |
| --- | --- | --- |
| `hybrid_activity_catalog.tsv` | 多玩法活动目录，记录每个活动的类型、输入、时长、故事用途、产出、失败态和制作风险 | 18 个活动 |
| `chapter_hybrid_activity_matrix.tsv` | 十二章多玩法装配矩阵，说明每章使用哪些活动、为什么需要、如何影响 SRPG | 12 章 |
| `hybrid_loop_templates.tsv` | 可复用玩法模板表，定义开馆、深潜、修复、路线、谈判、调谐、节奏、轻格斗等模板 | 16 个模板 |
| `content_node_types.tsv` | 内容节点类型表，定义线索、证据、道具、变量、战斗修正、长期弧线和 canon 引用节点 | 14 类节点 |
| `hybrid_activity_budget_rules.tsv` | 混合玩法活动预算规则，定义不同活动的热点、线索、道具、变量、战斗修正和 canon 引用上限 | 11 条规则 |
| `chapter_content_budget_matrix.tsv` | 十二章内容预算矩阵，限制每章混合玩法段、线索、证据、变量、长期弧线和新 canon 实体规模 | 12 章 |
| `hybrid_result_contract.tsv` | 小玩法统一输出契约，定义所有活动进入剧情、资源和 SRPG 的 `HybridActivityResult` 字段 | 12 个字段 |
| `canon_integration_rules.tsv` | Canon 集成规则表，规定新增角色、机体、地点、玩法根规则和实现改动何时必须进入 canon/图谱 | 12 条规则 |
| `unit_archetypes.tsv` | 机体原型表，记录队伍职责、数值预算、武器型谱、弱点和适用关卡 | 12 类原型 |
| `weapon_patterns.tsv` | 武器型谱表，记录武器动词、资源消耗、反制方式、改装钩子和平衡禁区 | 20 类武器型谱 |
| `upgrade_paths.tsv` | 成长改装路线表，记录机体、武器、机魂、驾驶员、关系和设施的升级边界 | 12 条路线 |
| `encounter_templates.tsv` | 关卡目标模板表，记录守、撤、截、诱、护、拆、说得、同步、封锁、传递等任务结构 | 14 类模板 |
| `mission_balance_targets.tsv` | 十二章平衡目标表，记录部署规模、回合数、敌方预算、三套队伍验收和隐藏目标 | 12 章 |
| `meta_runtime_architecture_contract_v0_1.tsv` | 世界内Meta实现合同；记录存档、跨周目残响、版本外壳、终端Shell、事件路由和安全恢复组件 | 12 个组件 |

## 使用顺序

1. 先查 `../canon/entities.tsv` 和 `canon_integration_rules.tsv`，确认新增内容是否触发正典登记。
2. 若涉及非 SRPG 玩法，先查 `chapter_content_budget_matrix.tsv`，确认本章还剩多少线索、道具、变量和长期弧线预算。
3. 再查 `content_node_types.tsv`，确认新增内容属于哪类节点，以及生命周期是否应局限在活动、本章或长期弧线。
4. 再查 `hybrid_activity_budget_rules.tsv`，确认该活动模板的热点、产物、变量、战斗修正和 canon 引用上限。
5. 再查 `hybrid_loop_templates.tsv`、`hybrid_activity_catalog.tsv` 和 `chapter_hybrid_activity_matrix.tsv`，确认是否复用旧模板、活动是否有故事用途、失败态和 SRPG 影响。
6. 写事件脚本或 Godot 实现时，所有小玩法都要输出 `hybrid_result_contract.tsv` 定义的统一 `HybridActivityResult`。
7. 若设计机体、武器或改装，查 `unit_archetypes.tsv`、`weapon_patterns.tsv` 和 `upgrade_paths.tsv`，确认定位、战术动词和成长边界。
8. 拆关卡时查 `encounter_templates.tsv`，先选任务动词，再摆敌人。
9. 查 `mission_balance_targets.tsv`，按低改、正常、高改三套队伍设验收标准。
10. 若某个活动不能输出资源、变量、战斗修正或叙事许可，优先删掉或改成纯演出。
11. 实现终端异常、假删档、版本切换或馆外档案前，查`meta_runtime_architecture_contract_v0_1.tsv`和`../story/meta_event_safety_boundaries_v0_1.tsv`；真实数据层必须与Meta表现层分离。

## 设计原则

- SRPG/战棋仍是章节主冲突承载层。
- 多玩法必须服务万机馆、机魂、参战包主题或战斗准备。
- 经营、探索、修复、谈判和短玩法采用章节封闭内容图，不做全局自由内容网。
- 一章最多新增一个新模板，其他内容优先复用旧模板。
- 跨章内容必须登记为长期弧线轻触，并进入 canon 或 design_graph。
- 小玩法失败不默认 Game Over，而是转成清算压力、损伤、少量战斗劣势或台词后果。
- 数值平衡采用三套队伍验收：低改队可通主线、正常队可完成多数副目标、高改队挑战隐藏目标但不能无视地图规则。
- 敌人健康度优先来自意图、目标压力和机制，不来自单纯堆 HP。
