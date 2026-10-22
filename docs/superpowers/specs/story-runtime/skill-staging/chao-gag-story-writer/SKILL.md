---
name: chao-gag-story-writer
description: Use for creative development and prose work in 超GAG机器人大战 when a task needs genuinely dramatic story pitches, character-led episode design, causal preflight, readable Episode Reader prose, natural dialogue, mecha/IP dramaturgy, relationship and comedy writing, structural rewriting, or absolute story review. Use after chao-gag-canon has established current facts. This skill owns creative authorship; chao-gag-writing-pipeline remains the outer production orchestrator.
---

# 超GAG创意编剧

## 目的

这个Skill帮助一个主笔写出真正有戏、有人、有机器人快感的故事。它不替Canon裁定事实，也不把生产合同平均塞进正文。

创作顺序是：

```text
L1/L2/L3中的体验、总发动机与本章职责
-> 合法人物/机体索引和上章真实出口
-> 三种不同的戏剧选择
-> 选定或融合一案
-> 按需检索素材
-> 按需准入现有L4/L4.5迁移参照
-> 选中人物/机体/场景的稳定建模
-> 独立因果与常识预演
-> 场面链与演出承载
-> 一个主笔顺序创作
-> 冷读与机战审稿
-> 用户确认后回写
```

## 与现有Skill的边界

- 先使用`chao-gag-canon`确认权威层和事实边界，再由Story Runtime v3按阶段查询当前所需切片。
- `chao-gag-writing-pipeline`负责阶段、文件、状态、缓存、回写和跨话循环。
- 本Skill负责创意提案、戏剧设计、正文和创作质量判断。
- 不把完整Canon、合同、旧Reader、坏句案例或审稿意见交给创意主笔。
- 更好的戏若需要改变Working事实，在正文外提出迁移，不用解释性台词绕过去。
- 设定不是一次性前置输入。选案、素材、建模、场面、正文和审稿可多次查询，但每次只取当前问题所需知识。
- L4/L4.5/L5以`chapter_layer_source_registry_v3.tsv`登记。`ideation`不读旧章纲答案；选案后只按`admitted_layer_source_ids`逐项准入。旧同章Reader必须等冷读完成才可揭盲。

## 模式路由

一次Agent调用只执行一种模式。

### `ideation`

读取：

- Runtime v3 `ideation`包的`06-writer-view.md`中所给L1体验、L2总发动机、L3本章位置和上章出口；默认不读同包的调试TSV与完整切片；
- 本章合法人物索引及核心欲望，不读全量档案；
- 合法机体、对手和长期奖励索引；
- 必须保留的未来峰值与少量不可静默改动的硬事实；
- `references/ideation-and-character-sandbox.md`。

输出三种结构真正不同的方案，不写正文。每案先用白话说清：谁想做什么，谁如何阻止，为什么现在必须战斗，玩家赢了得到什么。然后再写奇观、反转和关系转折。

主笔拥有否决旧章引擎、旧高光和Working场面的权力，但必须列出迁移项。`Creative First`意味着戏剧选择先行，不意味着修辞先出奇。

### `research-admission`

只在一个方案被选中后运行。读取Runtime v3 `research`包，围绕已选戏剧问题检索IP剧情、名台词/名场面、模玩生态、关系、喜剧和What-if素材。输出「采用、变形采用、暂不使用」及理由。不得因为检索到素材就全部塞入。

### `entity-model`

在选案后、因果预演前运行。读取Runtime v3 `entity_model`包，对每个选中人物、机体、对手、地点和关键物件确认：

- 是否真的存在，以何种方式在场；
- 当前欲望、恐惧、手段、知识和声线；
- 控制什么，不能控制什么；
- 与谁的关系已到哪一步；
- 场前位置、场后位置和下次生命周期；
- 可自由发挥的空白，以及需要迁移的Working事实。

重要角色必须复用稳定人物模型，不得每话重造人设。局部NPC使用轻量场景卡。新具名实体需说明现有角色为什么无法承担、资产代价和未来去向。

### `causality`

由独立Agent执行。读取选定方案、已通过的实体建模、Runtime v3 `scene_plan`包和`references/causality-preflight.md`。需要对照现有章纲、因果板、战斗预案或L4.5时，先从章级层源索引选择具体ID，不能把整个目录全塞进上下文。

输出因果骨架、知识与控制关系、空间时间问题、最简单替代方案检查及写作交接。不得润色对白、添加金句、创造新技术名词或暗中改写方案。能用常识机制解决的问题，不得叠加世界规则。

### `draft`

由一个主笔负责。读取：

- 选定方案；
- 已解决阻塞问题的精简因果骨架；
- Runtime v3 `draft`包中本场明确活跃人物的当场欲望、关系状态和正面声线；
- 已准入素材；
- `references/drafting-reader.md`；
- 按需读取机战、关系或喜剧参考。

不读取负面案例、旧审稿、候选补丁或本场不在场人物的全量档案。先写开场或第一完整场做局部熔断；白话因果、空间或人声失效就停，不带着错误语调写完整话。

通过后，超长单话按完整戏剧场拆分，但仍由同一主笔顺序创作。每场只继承必要前情、上一场已确认出口状态和少量原文尾部。

### `reader-review`

独立Agent只读正文、玩家已知前情、Runtime v3 `review_scope=cold_reader`事实切片、`references/absolute-review.md`普通读者/编剧部分和`references/human-voice-semantic-gate.md`。先白话复述自己读到的事件，再评价。不得读L4/L4.5、旧同章Reader、作者意图或后台答案来替正文补意义。

### `mecha-review`

独立Agent读正文、玩家已知前情、必要机体事实、玩法边界和`references/absolute-review.md`机器人文化/游戏部分。需要核对章级目标和制作承载时使用独立的`review_scope=design`包；不得把该包交给冷读席。检查机体是否真在演戏、IP精神是否可感、战斗是否可玩，不按素材数量打勾。

### `rewrite`

原主笔读取正文与合并后的根因简报，并读取`references/rewrite.md`。最多进行一次完整重写。

- 局部问题做局部修正。
- 动机、因果、高潮、人物选择或战斗目的失效时，重写完整场面。
- 因果根因先回到`causality`；发动机失效则回到`ideation`。
- 不在正文中临场添加技术机制、新人物或便利工具解围。

## 端到端单话流程

1. 外层Pipeline生成Runtime v3 `ideation`请求。
2. `ideation`主笔提出三案，每案先过白话落地门。
3. Showrunner选择或融合一案，只按功能融合。
4. `research-admission`按问题检索并选用素材。
5. `entity-model`确认人物、机体、场景、对手和关键物件的存在、反应、控制、知识与生命周期。
6. `causality`使用`scene_plan`阶段包预演选定方案。
7. 生成精简作家Brief，并运行：

```bash
python3 scripts/check_creative_freedom.py <writer-brief.md> --strict
```

8. `draft`主笔先通过开场/第一场熔断，再顺序写完Reader。
9. `reader-review`使用`cold_reader`视野，`mecha-review`/逻辑制作席使用`design`视野，分别做绝对审稿。
10. 合并为一个根因简报。因果类问题先回因果门。
11. 原主笔最多执行一次`rewrite`。
12. 冷读完成后才可用`review_scope=benchmark`揭盲旧同章Reader做成本与增量比较。
13. 未参与写作的Agent只回归已修根因；问题被转移给新角色、事故或机制即判失败。
14. 用户确认后，外层Pipeline才运行`writeback`阶段，替换Current Reader、回写状态或提交Canon迁移。

## 主笔Prompt的自由边界

作家Brief必须区分：

- **已锁事实**：不能无声改动的当前真相；
- **戏剧要求**：这一话必须解决的观众问题；
- **主笔可改写范围**：地点细节、场面顺序、高潮解法、关系表现等开放项；
- **开放问题**：要求主笔创造答案，不把答案写进Prompt；
- **未来保留**：本话不能提前消费的峰值；
- **准入素材**：可使用而非必须逐项点名的材料；
- **建模空白**：既有事实未规定、应由演戏填写的部分；
- **迁移候选**：为更好故事需要上游重审的Working事实。

Prompt不得预写高潮的完整动作顺序、人物最终台词或「正确答案」。确定性脚本只能发现明显泄题、身份/位置/控制权冲突和上下文污染，不能判断故事好坏。

## 创作所有权

- 一个单话只能有一个正文主笔。
- 不允许多个Agent并行写若干片段再拼成Reader。
- 角色、机体和对手都可以反抗提案；若只有作者希望事情发生，先重做方案。
- 主角不能只执行正确流程。他需要欲望、诱惑、能力、代价和一次只有他能作出的选择。
- 主要机体不是议题证物。它们必须拥有身体欲望、舞台动作和可延续的生命。
- 关系、喜剧、泪点与IP投射必须改变同一条主因果，不能成为外挂段落。

## 质量裁决

绝对审稿只允许三个结论：

- `PASS_FOR_USER_READ`：具备独立吸引力，可交用户首读，但不等于用户验收。
- `REWRITE_ONCE`：发动机成立，存在可归并的结构或表达根因。
- `RESTART_FROM_IDEATION`：欲望、冲突、高潮或机战主体性失效。

「比旧稿好」「字段齐全」「Canon无冲突」「正则零命中」都不能单独获得通过。

## 按需参考

- 创意方案与角色反抗：`references/ideation-and-character-sandbox.md`
- 因果、常识与空间预演：`references/causality-preflight.md`
- Reader场面、对白与信息控制：`references/drafting-reader.md`
- 机器人动画、IP与战斗戏剧：`references/mecha-ip-dramaturgy.md`
- 成人关系、生活与GAG喜剧：`references/relationship-comedy.md`
- 绝对读者和机战审稿：`references/absolute-review.md`
- 项目人类声线语义门：`references/human-voice-semantic-gate.md`
- 单轮重写：`references/rewrite.md`

不要一次加载全部参考。只加载当前模式需要的文件。
