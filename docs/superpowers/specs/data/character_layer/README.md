# 《超GAG机器人大战：万机残响》人物层数据说明 v0.1

本目录承接 [下一阶段细化计划与参战人物层审计](../../2026-06-19-chao-gag-next-detailing-plan-character-layer.md)，目标是把“参战包/机体/梗点”推进到可编剧、可装配、可原型验证的人物层。

剧情层数据见 [剧情数据说明](../story/README.md)。人物层回答“谁在场、谁和谁有话可说”；剧情层回答“这些人在哪些场景里被压力、选择和后果推着变化”。

跨文档口径、节点关系和风险清单见 [设定图谱数据说明](../design_graph/README.md)。

角色内在、声音规则和台词诊断见 [角色声音数据说明](../character_voice/README.md)。人物层给出角色功能，声音层负责把功能转成角色视角下的反应。

## 文件

| 文件 | 用途 | 当前规模 |
| --- | --- | --- |
| `character_archetypes.tsv` | 人物原型词根表，记录梗点来源、原创化方式和法务边界 | 80 个原型 |
| `pilot_cast.tsv` | 首批参战人物表，覆盖核心包、隐藏代表机体包、AI、NPC、反派和生活锚点 | 76 名人物/机体角色 |
| `character_interactions.tsv` | 跨人物互动边，记录战前对话、援护、说得、临时敌对、终局回收 | 60 条互动 |
| `gag_hooks.tsv` | 可触发人物梗点表，区分表层笑点、深层功能、玩法效果和法务边界 | 60 条梗点 |
| `chapter_character_matrix.tsv` | 十二章人物装配矩阵，说明每章谁在场、推进什么关系、触发哪些互动 | 12 章 |
| `demo_character_slice.tsv` | 90 分钟 Demo 人物切片，按登场顺序列出人物、梗点、情感和玩法验证 | 15 段 |

## 使用顺序

1. 用 `character_archetypes.tsv` 判断一个人物梗点是否有合法且有戏的来源。
2. 用 `pilot_cast.tsv` 选出某个章节或 Demo 的登场人物。
3. 用 `character_interactions.tsv` 查人物之间是否已有互动边。
4. 用 `gag_hooks.tsv` 把互动边转成战斗、船内、说得或演出触发。
5. 用 `chapter_character_matrix.tsv` 检查章节装配是否有足够人物戏。
6. 用 `demo_character_slice.tsv` 约束垂直切片范围，避免 Demo 过载。
7. 用 `../story/story_scene_matrix.tsv` 把章节人物装配转成具体场景、玩法目标和资产需求。
8. 用 `../character_voice/character_dossiers_core.tsv` 和 `../character_voice/character_voice_rules.tsv` 检查对白是否来自角色，而不是来自设定框架。

## 设计原则

- 梗点必须绑定人物伤口、关系变化或战斗功能。
- 参战人物不能只是原型标签，每个核心包至少需要主驾驶、宿敌/对手、支援/整备/舰桥、生活锚点。
- 隐藏机体不是单纯奖励，而是玩家理解主题后的回应。
- TARS（《星际穿越》）这类 AI/陪伴型角色保留为支援和情感线，不占巨大代表机体名额。
- Megazord/麦克佐德、Voltes V/波鲁吉斯V、Voltron/百兽王进入隐藏代表机体池，负责全球巨大合体机器人文化。
