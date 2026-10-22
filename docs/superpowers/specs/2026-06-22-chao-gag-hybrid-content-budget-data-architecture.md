# 《超GAG机器人大战：万机残响》多玩法内容预算与数据架构约束 v0.1

> 承接 [多元游玩体验策划](./2026-06-22-chao-gag-hybrid-play-experience-design.md)、[机体数值成长关卡平衡 Bible](./2026-06-22-chao-gag-mecha-stats-growth-balance-bible.md) 和 `chao-gag-canon` 工作流。  
> 本文回答一个制作层问题：经营、探索、修复、谈判和短玩法加入后，如何防止线索、道具、变量、剧情和战斗修正网络失控。

---

## 0. 结论

多玩法可以做，但必须采用**章节封闭内容图**，而不是全局自由内容网。

核心规则：

```text
每章 = 一个小内容图
小内容图 = 少量线索 + 少量可带回物 + 少量变量变化 + 少量战斗修正
跨章内容 = 必须登记为 LongArc，并进入 canon 或 design_graph
小玩法输出 = 统一 HybridActivityResult，不允许各玩法自造结果格式
```

本轮新增五张机器可读表：

| 表 | 用途 |
| --- | --- |
| `content_node_types.tsv` | 定义线索、证据、道具、变量、战斗修正、长期弧线等节点类型 |
| `hybrid_activity_budget_rules.tsv` | 定义不同小玩法的节点、变量、战斗修正和 canon 引用上限 |
| `chapter_content_budget_matrix.tsv` | 定义十二章每章的内容预算上限 |
| `hybrid_result_contract.tsv` | 定义所有小玩法统一输出 `HybridActivityResult` 的字段和限制 |
| `canon_integration_rules.tsv` | 定义什么内容必须进入 canon、gameplay、story 或 design_graph |

---

## 1. 复杂度边界

### 1.1 禁止全局自由网络

不允许每个线索、道具、角色请求都自由连接到任意章节。  
允许的连接只有四种：

| 连接类型 | 生命周期 | 例子 | 是否需要 canon |
| --- | --- | --- | --- |
| `local` | 当前活动内消耗 | 修好右臂线路，1-2开局获得援护 | 否，除非引入新实体 |
| `chapter` | 当前章内回收 | C02修复模型，主战作为非致命证物 | 否，但需登记到章节预算表 |
| `arc_touch` | 轻触长期弧线 | 黑展柜共鸣 +1、远星理解提示 | 是，必须有 canon 或 graph 节点 |
| `long_arc` | 多章持续追踪 | 远星理解度、路线债、原典改写倾向 | 是，必须进入 canon/design_graph |

### 1.2 每章只允许一个主内容图

一章可以有多个小玩法，但只能服务一个主内容图。  
例如 C01 的主内容图是：

```text
喜欢万机馆 -> 发现清算压力 -> 保护留言墙/展品 -> 黑展柜轻触
```

不能同时展开“法务阴谋大网、黑展柜大谜团、经营系统全开、模型支线、豪司正式入队、火灾真相”六条网。

### 1.3 变量少而硬

每章变量分三层：

| 层级 | 上限 | 说明 |
| --- | --- | --- |
| 章节主变量 | 1 | 本章要证明什么，例如 C01 的万机馆家感 |
| 次级变量 | 1 到 2 | 本章具体压力，例如清算压力、资料完整度 |
| 长期变量轻触 | 0 到 2 | 黑展柜、远星理解、路线债等，只能轻触 |

如果一个小玩法需要新增 3 个以上变量，优先砍玩法或合并变量。

---

## 2. 内容图数据模型

### 2.1 ContentNode

所有经营、探索、修复、谈判、深潜中的内容，都先视为节点：

```text
ContentNode
- node_id
- chapter_id
- owner_activity_id
- node_type
- display_name
- canon_refs
- reveal_condition
- payoff_target
- lifespan
- budget_cost
```

`node_type` 必须来自 `content_node_types.tsv`。

### 2.2 ContentEdge

边只表达必要关系，不做无限图谱：

```text
ContentEdge
- from_node_id
- to_node_id
- relation_type
- condition
- output
```

推荐关系：

- `reveals`
- `consumes`
- `modifies`
- `unlocks`
- `foreshadows`
- `pays_off`

禁止关系：

- `related_to`
- `maybe_affects`
- `lore_link`
- `future_use_unknown`

这些模糊关系会把内容网变成记忆垃圾场。

### 2.3 HybridActivityResult

所有小玩法只允许通过统一结果结构影响战斗和剧情：

```text
HybridActivityResult
- activity_id
- score_band
- resource_delta
- variable_delta
- battle_modifiers
- unlocked_flags
- pressure_delta
- canon_refs
- source_nodes
- consumed_nodes
- soft_fail
- ui_summary
```

字段限制见 `hybrid_result_contract.tsv`。

---

## 3. 每章预算

默认商业版普通章节预算：

| 项目 | 普通章上限 |
| --- | --- |
| 必做混合玩法段 | 1 到 2 |
| 可选混合玩法段 | 0 到 1 |
| 线索节点 | 4 到 6 |
| 可带回物 | 3 到 5 |
| 证据节点 | 1 到 3 |
| 战斗修正 | 2 到 4 |
| 变量变化 | 2 到 4 |
| 长期弧线轻触 | 0 到 2 |
| 新 canon 实体 | 0 到 2 |

高复杂章节可以稍微放宽，但必须降低新系统数量。终局可以回收更多旧节点，但**不允许新增新模板**。

十二章细分见 `chapter_content_budget_matrix.tsv`。

---

## 4. 活动预算

### 4.1 微事件

用于修一次零件、按一次合体锁、截住一句话。

预算：

- 0 到 1 个线索。
- 0 到 1 个可带回物。
- 1 个直接输出。
- 不新增长期变量。
- 不新增 canon 实体。

### 4.2 开馆经营

不是完整模拟经营。一次开馆只允许：

- 最多 3 个展岛选择。
- 最多 2 个岗位角色。
- 最多 3 个访客事件。
- 最多 4 条结算结果。
- 最多 2 个战斗修正。

### 4.3 残响深潜

一次深潜只允许：

- 最多 6 个热点。
- 最多 3 个可带回物。
- 最多 2 个证据节点。
- 最多 1 个长期弧线轻触。
- 最多 2 个战斗修正。

### 4.4 章节短玩法

章节专属玩法只能表达本章主题，不允许开新大网：

- 每章最多新增 1 个新模板。
- 单次活动最多输出 2 个变量变化。
- 单次活动最多输出 2 个战斗修正。
- 若需要新 canon 实体，必须先写 `entities.tsv`。

完整规则见 `hybrid_activity_budget_rules.tsv`。

---

## 5. Canon 集成

`chao-gag-canon` 在这里承担“门卫”，不是替代玩法数据表。

### 5.1 必须进 canon 的内容

| 内容 | 例子 |
| --- | --- |
| 新说话角色 | 新档案官、新驾驶员、新孩子 |
| 新可玩/敌对机体 | 新机体、Boss、隐藏机体 |
| 新阵营/组织 | 新清算分部、新圣堂分派 |
| 新地点 | 新展区、城市区域、残响域关键层 |
| 新谜团术语 | 黑展柜、远星信号、索引天使子概念 |
| 玩法根规则 | 多元游玩体验体系、机体平衡体系、内容预算体系 |

### 5.2 不必进 canon 的内容

| 内容 | 去哪里 |
| --- | --- |
| 一次性维修件 | `content_node_types.tsv` + 章节活动数据 |
| 章节内消耗线索 | 章节内容图 |
| 小数值奖励 | `HybridActivityResult` |
| 普通访客事件 | 开馆活动数据 |
| 一次性战斗修正 | `battle_modifiers` |

### 5.3 查询顺序

写剧情、台本或实现前：

```text
1. canon-query: 查实体、场景、根概念、运行规则
2. data/gameplay: 查活动、模板、预算和结果契约
3. data/story: 查章节诊断、场景矩阵和流程
4. design_graph: 查跨文档关系和风险
```

---

## 6. 第一章切片预算

C01 允许比普通章稍密，因为它是教学章，但必须收束：

| 内容 | 上限 | 推荐 |
| --- | --- | --- |
| 必做混合玩法 | 2 | 闭馆探索 + 微修复 |
| 可选混合玩法 | 1 | 极简开馆结算 |
| 线索节点 | 5 | 留言墙、右臂、防火、七海清单、0号异响 |
| 可带回物 | 4 | 维修件、旧纸条、封存清单片段、防火记录 |
| 战斗修正 | 3 | 留言墙耐久、右臂援护、防火减伤 |
| 变量变化 | 4 | 万机馆家感、清算压力、黑展柜共鸣、观众信任 |
| 长期弧线轻触 | 2 | 黑展柜、企业信任 |
| 新 canon 实体 | 0 | 现有 canon 已覆盖第一章关键实体 |

不能加入：

- 七年前火灾录像。
- 豪司初始入队。
- 完整经营系统。
- 黑展柜真相解释。
- 新敌方大阵营。

---

## 7. 删除规则

当内容超预算时，按这个顺序删：

1. 没有战斗、变量或角色后果的道具。
2. 只解释设定、不改变玩家行动的线索。
3. 和本章核心命题无关的访客事件。
4. 新增但没有 canon 必要性的 NPC。
5. 第二个以上长期弧线轻触。
6. 第三个以上战斗修正。

保留优先级：

1. 玩家当下能理解目标的线索。
2. 能改变 SRPG 起手条件的结果。
3. 能让角色更像自己的小动作。
4. canon 已登记、后续一定回收的长期弧线。

---

## 8. 实现检查

后续主程序实现时，每个章节包至少输出：

```text
ChapterContentBudgetReport
- chapter_id
- hybrid_segments_count
- clue_nodes_count
- carry_items_count
- evidence_nodes_count
- battle_modifiers_count
- variable_delta_count
- long_arc_touch_count
- new_canon_entity_count
- over_budget_fields
- intentionally_over_budget_reason
```

严格规则：

- 超预算必须写原因。
- 超预算原因不能是“以后可能有用”。
- 新 canon 实体数量超预算时，先拆章或延期登场。
- `HybridActivityResult` 字段超出契约时，优先删输出而不是扩字段。

