---
name: chao-gag-story-writer
description: Use for creative development and prose work in 超GAG机器人大战 when a task needs genuinely dramatic story pitches, character-led episode design, causal preflight, pure-story Episode Reader prose, natural dialogue, mecha/IP dramaturgy, story-to-game adaptation, relationship and comedy writing, structural rewriting, or absolute story review. Use after chao-gag-canon has established current facts. This skill owns creative authorship; chao-gag-writing-pipeline remains the outer production orchestrator.
---

# 超GAG创意编剧

## 目的

这个Skill帮助一个主笔写出真正有戏、有人、有机器人快感的故事。它不替Canon裁定事实，也不把生产合同平均塞进正文。

创作顺序是：

```text
L1/L2/L3中的体验、总发动机与本章职责
-> 合法人物/机体索引和上章真实出口
-> 按真实分歧提出并选择故事方向
-> 选定或融合一案
-> 按需检索素材
-> 按需准入现有L4/L4.5迁移参照
-> 选中人物/机体/场景的稳定建模
-> 简洁故事梗概与玩法概念共同构思
-> 必要因果、尺度与知识核对
-> 最不确定的完整场面试写
-> 一个主笔顺序创作纯剧情Reader
-> 普通读者冷读与人物声线审稿
-> 独立进行游戏流程解构与机战审稿
-> 按需生成可公开情报
-> 用户确认后回写
```

## 与现有Skill的边界

- 当前方法以`chao-gag-writing-pipeline`的2026-09-05入口和项目`2026-09-05-chao-gag-author-first-writing-method-v1.md`为准。旧逐话配额、压力板生成剧情和多轮补强不再适用。
- 先使用`chao-gag-canon`确认权威层和事实边界，再由Story Runtime v3按阶段查询当前所需切片。
- `chao-gag-writing-pipeline`负责阶段、文件、状态、缓存、回写和跨话循环。
- 本Skill负责创意提案、戏剧设计、正文和创作质量判断。
- 不把完整Canon、合同、旧Reader、坏句案例或审稿意见交给创意主笔。
- 更好的戏若需要改变Working事实，在正文外提出迁移，不用解释性台词绕过去。
- 设定不是一次性前置输入。选案、素材、建模、场面、正文和审稿可多次查询，但每次只取当前问题所需知识。
- L4/L4.5/L5以`chapter_layer_source_registry_v3.tsv`查询资格；`ideation`不读旧章纲答案，选案后以带来源哈希的`source_cards`逐项准入。旧同章Reader必须等冷读完成才可揭盲。
- 输入分为已发生事实、未来职责、可选素材、呈现方案。不可静默改事实；不把未来实现方案当已发生事实。新Runtime请求使用`context_policy=author_first_v1`，逐项有来源，不自动装入整份L3邻章和旧详细总纲。

## 模式路由

模式区分职责，不强制每个模式新开一次调用。主笔可以在同一上下文查资料、构思和写作；冷读必须隔离作者答案，不能由同一上下文伪装。执行范围以用户授权的一话/片段/阶段为准。

### `ideation`

读取：

- Runtime v3 `ideation`包的`06-writer-view.md`中所给L1体验、L2总发动机、L3本章位置和上章出口；默认不读同包的调试TSV与完整切片；
- 本章合法人物索引及核心欲望，不读全量档案；
- 合法机体、对手和长期奖励索引；
- 必须保留的未来峰值与少量不可静默改动的硬事实；
- `references/ideation-and-character-sandbox.md`。

方向明确时给一个主案；存在真正分歧时给2-3种结构不同的方案，不机械凑三案。每案先用白话说清谁想做什么、对方怎样行动、什么改变了局势、玩家期待或赢取什么。无需给每一话硬塞战斗、悲剧、Gag和反转。

主笔拥有否决旧章引擎、旧高光和Working场面的权力，但必须列出迁移项。`Creative First`意味着戏剧选择先行，不意味着修辞先出奇。

### `research-admission`

在构思或写作遇到具体问题时读取`research`包，查询IP剧情、名台词/名场面、模玩生态、关系、喜剧和What-if。仅记录实际采用项和重要取舍，不给每条未用素材填写说明。检索不等于准入，主笔可全部不用。

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

主笔先作必要常识预演；在需要独立事实审查且工具与授权允许时另开Agent。读取选定方案、相关实体事实和`references/causality-preflight.md`。需要对照生产板时只查能回答当前问题的部分，不能把整个目录塞进上下文。

只输出会影响故事的矛盾、证据和简单修法；无问题不另造长篇因果交接。不得创造新技术名词或暗中改写人物选择。能用常识机制解决的问题，不得叠加世界规则。

### `game-concept`

与章级梗概同时构思，按需读`references/story-to-game-adaptation.md`的早期部分及当前玩法入口。只确认敌方目标、玩家可改变的局面、固定故事结果、可选方法、既有玩法族和可能推翻故事的制作困难。不预排每台机体的完整动作、最终数值或镜头，不把玩法说明放进纯剧情。

### `chapter-treatment`

用连续故事说明人物选择、情势发展、重要转折和下一章缘由。不是台本、逐话动作清单或第一遍详细Reader。不规定统一字数；够判断故事即可。正文创作若发现无戏的场面可回改Candidate梗概，涉及已封存或重大事实按Pipeline迁移。

### `draft`

由一个主笔负责。读取：

- 选定方案；
- 已解决阻塞问题的精简因果骨架；
- Runtime v3 `draft`包中本场明确活跃人物的当场欲望、关系状态和正面声线；
- 已准入素材；
- `references/drafting-reader.md`；
- 按需读取机战、关系或喜剧参考。

不读取负面案例、旧审稿、候选补丁、关卡变量、UI说明、演出资产表或本场不在场人物的全量档案。先写开场或第一完整场做局部熔断；白话因果、空间或人声失效就停，不带着错误语调写完整话。

本模式只产出纯剧情Reader。正文不得出现玩家、菜单、可操作名单、回合、冷却、胜败条件、制作字段或话末百科。战斗只写故事目标、关键反击、人物/机体转折、大动作和结果。读取`references/drafting-reader.md`，写作及交稿前执行其中“称谓与时间指代”检查；不把来源标签直接当成叙事称呼，不用禁词清零代替语义判断。

通过后，超长单话按完整戏剧场拆分，但仍由同一主笔顺序创作。每场只继承必要前情、上一场已确认出口状态和少量原文尾部。

Episode标题也属于创作，不从主题字段自动生成：

- L4、因果骨架和Brief里的标题默认只是“工作标题”，不得直接晋升为玩家可见标题；
- Reader完成后检查标题是否具体、好懂且值得点开；不确定时再提出候选，不每话机械生成三类标题；
- 标题先提供一个角色、机体、动作、奇观或冲突画面，不负责总结本话价值；
- 第一眼要让玩家想点开，通关以后再由故事赋予第二层含义；
- 优先使用玩家本话亲眼看见的具体名词和动词；同章标题连读应形成升级波形；
- 禁止把“不是……”“能不能……”“可以……”等策划判断句直接当成正篇标题；
- 标题若离开作者解释便不知道指什么，退回主笔重命名。

### `reader-review`

独立Agent只读正文、玩家已知前情、Runtime v3 `review_scope=cold_reader`事实切片、`references/absolute-review.md`普通读者/编剧部分和`references/human-voice-semantic-gate.md`。先白话复述自己读到的事件，再评价。不得读L4/L4.5、旧同章Reader、作者意图或后台答案来替正文补意义。

### `game-adaptation`

本模式负责详细解构，在纯剧情Reader暂定成立后运行；早期玩法可行性由`game-concept`共同构思。读取通过的剧情Reader、选定玩法概念、机体能力、地图/资产现实和`references/story-to-game-adaptation.md`。分别安排实际需要的ADV、探索、SRPG、战中事件、关系事件及结算，不要求每话六类齐全。

本模式可以写目标、条件、变量、UI、触发器、单位和资产，但不得给剧情补动机、补前情或发明一个新冲突。如果某项玩法必须靠额外旁白才能成立，退回故事层或重新选择承载。

解构必须读取本章`story_play_topology`。Episode不是默认关卡边界；一场Operation可跨数话，一话也可包含多个Encounter。`story_unit_ids`用于绑定具体故事单元，`carry_from_state`用于把上一Operation的伤势、装备和地图后果带入下一Operation。除非主要世界冲突已经结束，不得把Episode切点写成Mission Clear、奖励结算、全体复位或地图重开。

### `open-information`

在剧情和游戏解构都成立后按需运行。只总结玩家已经通过故事或操作看见的表层事实。一张卡回答一个问题；不得推进剧情、替角色作决定、揭露后台真相或修补正文因果。没有必要时输出`not_required`。

### `mecha-review`

独立Agent读正文、玩家已知前情、必要机体事实、玩法边界和`references/absolute-review.md`机器人文化/游戏部分。需要核对章级目标和制作承载时使用独立的`review_scope=design`包；不得把该包交给冷读席。检查机体是否真在演戏、IP精神是否可感、战斗是否可玩，不按素材数量打勾。

### `rewrite`

原主笔读取正文与合并后的根因简报，并读取`references/rewrite.md`。最多进行一次完整重写。

- 局部问题做局部修正。
- 动机、因果、高潮、人物选择或战斗目的失效时，重写完整场面。
- 因果根因先回到`causality`；发动机失效则回到`ideation`。
- 不在正文中临场添加技术机制、新人物或便利工具解围。

## 实际工作顺序

1. 核对有效前情、人物模型与未来职责；围绕实际问题多次查询Runtime，不生成全章百科。
2. 决定值得讲的故事，简洁章纲与玩法概念相互校准。重大分歧给用户选择；普通场面取舍由主笔负责。
3. 只在新方法或高风险段先试写最不确定的完整场面；开头不是唯一熔断位置。明确方向后，同一主笔按用户范围顺序完成正文。
4. 冷读先判断读出了什么、是否想继续，再评价人声和情绪。事实席核对依据，不能用设定解释抵消冷读失败。
5. 原主笔修根因；无聊不能靠补更多信息解决。至多一次结构性重写，仍失效就停下改故事方案。
6. 另写详细游戏解构与按需公开情报，检查三层一致性及玩家选择空间。
7. 用户确认后按正式治理回写，未确认内容继续Candidate。新方法效果通过同预算直接主笔对照及后续整话验证，不靠固定多Agent数量证明。

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
- 关系、喜剧、泪点与IP投射应属于人物生活和作品体验，但不必每段都改变主因果。熟悉感、品味、身体距离、共同记忆也有价值；不要把亲近都写成交换权限或付债。

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
- 剧情到游戏的独立解构：`references/story-to-game-adaptation.md`
- 机器人动画、IP与战斗戏剧：`references/mecha-ip-dramaturgy.md`
- 成人关系、生活与GAG喜剧：`references/relationship-comedy.md`
- 绝对读者和机战审稿：`references/absolute-review.md`
- 项目人类声线语义门：`references/human-voice-semantic-gate.md`
- 单轮重写：`references/rewrite.md`

不要一次加载全部参考。只加载当前模式需要的文件。
