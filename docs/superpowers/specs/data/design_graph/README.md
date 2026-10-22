# 《超GAG机器人大战：万机残响》设定图谱数据说明 v0.1

本目录服务于 [设定与策划图谱索引](../../2026-06-19-chao-gag-design-graph-index.md)，用于管理当前工作区里规划、设定、人物、剧情、参战、台本和研究资料之间的关系。

## 文件

| 文件 | 用途 |
| --- | --- |
| `doc_registry.tsv` | 文档登记表，记录每个文档负责什么、消费什么、更新策略是什么 |
| `canonical_terms.tsv` | 标准术语表，记录当前口径、别名、禁用误称和源头文档 |
| `graph_nodes.tsv` | 图谱节点表，记录核心概念、角色、章节、参战包、变量和资料节点 |
| `graph_edges.tsv` | 图谱关系表，记录节点之间的承载、依赖、镜像、回收、派生关系 |
| `consistency_watchlist.tsv` | 口径风险表，记录已暴露的漂移、冲突、待同步项 |

角色内在与声音数据位于 [character_voice](../character_voice/README.md)，用于把人物功能转成真实对白和场景反应。

## 使用顺序

1. 涉及V35创作生产时，先查生成的`剧情梗概/V35六层创作生产看板.md`，只选择唯一活动章。
2. 再查该章`V35.9/rebuild/manifests/Cxx-story-chain.tsv`与`--next`，确认唯一合法产物。
3. 查 `canonical_terms.tsv`，确认标准术语和禁用说法。
4. 查 `graph_nodes.tsv`与`graph_edges.tsv`，确认元素、来源和依赖。
5. 如果发现旧文档与新口径不一致，在 `consistency_watchlist.tsv` 增加或更新风险项。
6. 最后回到具体源头文档补正文，并重新生成看板与下游。

## 维护规则

- 任何新增主角、反派、参战包、结局变量、支线包、核心哲学术语，都必须登记节点。
- 任何调整第一主角、世界真相、参战规模、结局路线、技术路线，都必须更新标准术语或风险清单。
- 研究报告只登记为资料来源，不直接进入游戏内命名。

## 当前V35入口

- `N_V35_SIX_LAYER_UPPER_INTEGRATION_PREMISE_20260720` 是当前逐章总纲的唯一上位桥接入口。它把体验宪章、总发动机、机制基线和六层根因接成七段宏观推进，但不预设章数、章点或人物结局。
- `N_V35_SIX_LAYER_OUTLINE_PREMISE_V1` 是对应的六行机器前提表，供章级开题和一致性审计读取，不替代创作。
- `N_V35_2_INTEGRATED_OUTLINE` 与旧十八章审定稿已降为History素材源，只负责打捞结构、高光、机体、IP、关系和分支，不再提供当前章表。
- `N_V35_3_STORY_SCALE_NAMING` 是V35.2的候选覆盖层，补齐八项关键决策、72台可操作收藏、八个来客包和多文化命名。
- `N_V35_4_SLOT_BRANCH_LIFECYCLE` 是逐章施工层，提供82作者槽、九组单周目路线、72机逐槽生命周期和关键命运传播。
- `N_V35_SLOT_PIPELINE_ADAPTER` 是执行适配层，在逐话写作前把V35.4解析成slot、route、fleet、lifecycle和decision输入，并写五张运行账本。
- `N_V35_5_OPENING_PRESSURE_BOARD` 是第一批逐章压力板，负责C01-C03的10槽11话映射、六站十八锚、18台首控节奏、巡展航图、百机祭四阶段目标和六条玩家悬念阶梯；配套九张V35.5施工表。
- 新逐章总纲先读取六层融合前提，再按需从V35.1至V35.8打捞素材和制作合同。逐章Pressure Board与Episode Loop仍需启用适配器；V35.3/V35.4/V35.5不直接升格Living Canon，也不替代逐话厚梗概、资产和运行账本。

## 当前V35.9 Story-First入口

- 人类总入口：`N_STORY_WORKSPACE_HUMAN_INDEX_V1`，对应仓库`docs/README.md`。普通阅读、章节制作、状态查询和Canon查询先从这里分流，不再按文件名版本号猜当前稿。
- 导航生成器：`N_STORY_WORKSPACE_INDEX_BUILDER_V1`。它从上位层Registry、章节Registry、当前生产批次和C01-C05 Story Chain生成十二份README；任何状态或路径变化后须重建并执行`--check`。
- 全剧机器入口：`N_V35_LAYERED_PRODUCTION_DASHBOARD_V1`。它由上位层registry、二十二章registry和当前活动章story-chain生成，负责回答L1-L6进行到哪里、哪章可动、缺什么和下一门。人工状态日志不得覆盖它。
- 总导航：`N_V359_REBUILD_INDEX`，对应`剧情梗概/V35.9/rebuild/README.md`。
- Reader生产入口：`N_V359_READER_INDEX`，机器阶段门为`N_V35_STORY_CHAIN_GATE_V1`。C01与C02当前Reader已有用户验收；C03因用户否决混合Reader方法已从`episode_e01`起失效，C04以后保持冻结或History。任何上游改动仍须先失效对应下游并重新封存。
- 当前Episode写作还受`N_STORY_READER_GAMEPLAY_SEPARATION_V2`约束：先生成纯剧情Reader，通过冷读后再派生独立游戏流程解构，最后按需生成可公开情报；三者不得混排。阶段性玩家知识入口`N_V35_CURRENT_OPEN_INFORMATION_SYSTEM_20260726`继续区分Canon后台真相、角色认知和玩家可理解信息，但资料卡不能承担主线解释。
- 第四层逐章总纲入口：`N_V35_SERIES_LAYER4_CHAPTER_OUTLINE_CONTRACT_20260721`。每章必须依次完成对齐、预生产、三板、完整总纲、逐话结构表、状态账、四视角章审和累计连续性回执；通过`write-performance`后停下审定。章级演出承载属于L4.5，不能提前生成。
- C04与C05当前章包及Episode Reader已按新story-chain封存，故事仍保持Candidate并等待用户审阅。旧V35.9 C04 v4、十二切片、四副测试体在C04预显影和沈砺驾驶黑头机等口径均列History，不可直接回流。
- 当前可作为正式前情的L5是C01四话与C02五话；C03旧四话、C04/C05旧Reader均不是当前创作依据。旧V35.10“正式Episode Packet”仍为0，两套口径不得混算。不得用合同绿灯、机器零命中或内部合订验收替代用户的故事审定。

## 当前全剧上位层

- `N_V35_THEME_PLAYER_FANTASY_EXPERIENCE_CHARTER_20260718`：第一层Working，锁定八类玩家幻想、G.A.G.玩梗、机战精神、核心群像、情绪与Meta体验合同。
- `N_V35_STORY_WORLD_MASTER_ENGINE_20260718`：第二层Working，以“连接与控制”组织六层因果链和七段宏观波形；章节结构保持OPEN。
- `N_V35_WORLD_MECHANISM_CREATIVE_INTERFACE_BASELINE_20260719`：横向H0底盘，从Current Canon与成熟候选中归并世界机制和写作接口，补清白框/清噪/索引、二十七年远征前线、三代通信、远征G.A.G.锚、世界运行和机构权限，并以`CURRENT / STABILIZE / OPEN / PROHIBITED`保留权威差异。
- `N_V35_TERMINAL_SIX_LAYER_ROOT_MECHANISMS_20260720`：根机制Working、剧情桥段Candidate；把无声地基、远征原罪、归乡灾潮、未发生者战争、万机皇胎和最后的宇宙分配为六种不同职责，并以一条因果链合流。
- `N_V35_SIX_LAYER_UPPER_INTEGRATION_PREMISE_20260720`：第三层之后、逐章总纲之前的唯一桥接层；处理冲突裁决、人物使命、机体/IP/玩法接口、揭示预算和旧高光迁移。
- `N_V35_DEEP_SPACE_EXPEDITION_FRONT_V1`：机器可读远征分期，固定持续外防、旧锚和通信代际，保留具体舰名、战略巨构、成员命运与R06配置为OPEN/Candidate。
- `N_V35_TOP_THREE_LAYER_ADJUDICATION_20260719`：三层审定报告；建议第一层整体通过、第二层发动机通过/章表保留候选、第三层作为Working Reference并逐项迁移。
- `N_V35_SERIES_STRUCTURE_MASTER_BOARD_20260720`：G5-02后的当前创作L3，二十二章、86话Working上界；A机器人大战母结构、B章间行动接力和C双后代深轴已迁入，具体逐场剧情、Roster细节、命运、关系和资产仍由L4逐章裁决。
- 根宇宙机制、远征宇宙桥和六层存在/区别/因果已经显式迁移Working；具体舰队、章数、章点、R06命运、终局机体外形和人物结局仍为Candidate/OPEN。逐章总纲先读体验宪章、总发动机、机制基线和六层融合前提，再读取Current Canon、章节Pack与制作合同；不得把`STABILIZE`或`OPEN`项提前升为Working。
