# 全玩法比较研究与综合假设

> Status: `candidate_research / phase_complete / user_review_pending / synthesis_evidence_grading_complete / no_recoverable_source_archive`
>
> Rule: 外部案例用于提出可证伪假设，不自动成为本项目设计。
>
> Evidence limit: 35条样本均保存官方页面级 URL 与 `2026-08-10` 的人工核查状态；[source-evidence-ledger.tsv](source-evidence-ledger.tsv) 的15条一手证据覆盖14个 unique sample，记录页面／手册章节定位、支持范围与禁止推论，因此其余21/35仍只有页面级索引。[source-response-fingerprints.tsv](source-response-fingerprints.tsv) 中13条成功响应覆盖12个 unique sample，另2条传输失败不计入本次响应复核。成功项的SHA-256只是当次原始HTTP响应字节指纹；响应正文没有保留，也没有页面快照或逐项摘录，不能据此复原逐段引文。

## 一、研究问题

这轮研究不问“哪款游戏最像《超GAG》”，而问六个可以分别求解的问题：

1. 怎样让复杂战棋本身有趣，而不是靠主角超能力救场？
2. 怎样把不完整战报、预演、导航、授权、机魂同意和工程验证做成可操作的 C2 层？
3. 怎样让巨大机器人、驾驶员、支援角色和作战室同时具有身体感和角色身份？
4. 怎样把重剧情、章节持续后果和低刷级成长接进主战术？
5. 怎样设计轻松、短时、可复用的探索、解谜、Hub、关系、收藏和小游戏？
6. 怎样让这些模式共用状态和资产，而不是成为小游戏合集？

机器可读拆解见 [comparative-mechanic-matrix.tsv](comparative-mechanic-matrix.tsv)，综合取舍见 [mechanic-synthesis-decisions.tsv](mechanic-synthesis-decisions.tsv)，关键一手主张与推论边界见 [source-evidence-ledger.tsv](source-evidence-ledger.tsv)，22条综合取舍到样本、locator和响应状态的逐行分级见 [synthesis-evidence-coverage.tsv](synthesis-evidence-coverage.tsv)。

## 二、样本选择与证据规则

- 只使用开发商、发行商、官方商店说明、官方手册和官方开发日志；
- 每个样本必须记录玩家身份、动词、信息、行动经济、失败、成长和故事连接；
- 只收录能回答本项目某个问题的样本，不为知名度凑数量；
- 每个“可迁移点”同时写“不可照搬点”；
- 研究结论只能进入 Candidate 假设池，仍需纸面原型、灰盒和真人试玩。

## 三、研究簇

| 簇 | 核心问题 | 预期样本 |
| --- | --- | --- |
| TACT 基础战术 | 清晰意图、多解、空间、反应、敌我行动、机体身体 | Into the Breach、Tactical Breach Wizards、Valkyria Chronicles 4、BATTLETECH等 |
| C2 信息与指挥 | 报告来源、延迟、置信度、路线、授权、传感暴露、提交 | Radio Commander、Command: Modern Operations、HighFleet、Phantom Brigade、Frozen Synapse等 |
| NARR 剧情—战斗结构 | Reader、档案、战斗、章节后果怎样分层又互相写回 | 13 Sentinels、The Banner Saga、Pyre、BATTLETECH Flashpoint等 |
| MECHA 机器人大战 | 群机、支援席、名场面动画、编队和偏爱表达 | Super Robot Wars Y/30、Valkyria Chronicles 4、BATTLETECH等 |
| EXPL 探索与解谜 | 轻移动、观察、翻译、知识锁、环境谜题和低惩罚 | Outer Wilds、Chants of Sennaar、Heaven's Vault、TOEM、Carto等 |
| HUB 家园与关系 | 日程、地点、人物位置、关系、照料、事件和任务转换 | Fire Emblem: Three Houses、Pyre、Spiritfarer、Citizen Sleeper、Midnight Suns等 |
| STRAT 战略与结算 | 任务选择、世界节点、伤损、连续部署、未选路线和章节回写 | BATTLETECH、XCOM 2、Invisible, Inc.、Banner Saga等 |

## 四、首批已核实样本

### 4.1 Super Robot Wars Y / 30

官方把系列核心明确放在网格战术、跨作品机体与角色、攻击动画、机体/驾驶员升级；Y又把非驾驶角色纳入 Assist Crew，通过 Assist Commands 和使用经验成长。

对本项目最重要的不是照搬“回血、回EN、攻击力上升”，而是两条产品经验：

- 不驾驶主力机的角色也必须在战斗里拥有可见席位和可反复使用的动作；
- 攻击动画、Cut-in、合体/变形和角色台词不是战棋外装，而是机器人大战的核心回报。

不应照搬的是通用增益按钮、反复刷经验和深数值改造。纪存、七海、白鸢与工程组的动作应改变信息、路线、许可、可执行性与后果，而不是换皮回血/加攻。

### 4.2 13 Sentinels: Aegis Rim

官方将作品分成追忆篇、探明篇和崩坏篇：多主角戏剧冒险、已查明事实的档案回顾、机兵战斗三种独立载体。

可迁移的是“纯剧情、已获得知识、战斗”分开呈现并互相解锁，正好支持本项目保持 Reader、开放资料与 gameflow 分离。风险是战斗若只承载抽象敌群和升级，会让人物身体、地点和故事因果脱节；本项目每场战斗仍必须是故事冲突的可操作版本。

### 4.3 Valkyria Chronicles 4

官方把 BLiTZ 定义为战略与动作融合：大型地图上先以指挥视角选单位，再让角色在敌方炮火和迎击下真实移动、瞄准和行动；同时有兵种、编队、命令、潜能、装备、训练、舰体与图鉴。

可迁移的是“全局命令预算＋局部具身执行”：玩家不是拖动棋子瞬移，而是看见身体穿过火线、受阻、寻找掩体和完成动作。这适合巨大机器人建立重量、路线和截击。风险是动作操作、随机潜能、兵种练级和大量装备会把本项目拖向反应操作与刷取；应保留具身路线和持续威胁，改用可暂停/可读的战术提交。

### 4.4 BATTLETECH

官方把地形、站位、武器选择和特殊能力与机库维护、损坏部件替换、Salvage、星际任务选择和基地升级接成一体；Flashpoint还把连续任务、无法中途维修/治疗、部署吨位限制、对话、关键选择和奖励组成短篇故事链。

可迁移的是“机体伤损和连续部署就是剧情状态”，以及用部署限制、维修窗口和任务链改变战术，而不是只提高敌方血量。风险是佣兵财务压力、海量部件、随机Salvage和长期数值优化会吞掉人物剧；本项目只保留功能损伤、稀缺维修位和章节连续状态。

## 五、首轮综合轴（仍为 Candidate）

目前没有任何单一作品同时解决本项目的五个核心矛盾。可行方向是组合一条原创轴：

```text
清晰但不完整的战场信息
→ 主角团解释、提案和权限/同意检查
→ 玩家在有限注意与时间内提交计划
→ 机体进行短阶段、具身、可截击的执行
→ 伤损、关系、权限、敌人学习和地点状态进入后续剧情
```

这条轴必须建立在有趣的基础战棋之上。第一原型不使用主角权能，只验证移动、站位、遮挡、攻击、保护、截击、撤退、地形、敌方意图和两种可行胜法；第二原型才加入信息、导航、预演和授权；第三原型再验证巨构、多阶段、多个角色与机魂拒绝。

## 六、样本覆盖与研究完成度

当前矩阵共收录35条样本记录，覆盖：

- `TACT` 12条；
- `C2` 8条；
- `MECHA` 5条；
- `EXPL` 10条；
- `PUZZLE` 8条；
- `HUB` 11条；
- `REL` 9条；
- `STRAT` 11条；
- `NARR` 11条；
- `COLLECT` 4条。

一个样本可以同时回答多个问题，因此数量不是相加后的作品数。当前研究已经足够进入产品骨架设计；后续只在具体机制出现证据缺口时定向补样本，不再为了“更多游戏名”扩大列表。

当前证据可复核性按“样本是否有 locator”和“本次响应是否成功捕获指纹”分层：

- 35条矩阵记录都有官方URL；15条关键证据覆盖14个 unique sample，所以21/35仍只有页面级索引；
- 13条成功HTTP响应覆盖12个 unique sample；2条失败响应只保留失败原因，没有响应体或hash，不计作本次复核；
- 成功响应的raw SHA-256只能检查当次字节是否漂移。所有响应正文均未保留，也没有可恢复页面快照或逐项摘录，因此hash不是引文档案；
- [synthesis-evidence-coverage.tsv](synthesis-evidence-coverage.tsv) 对22条RDEC逐行重算：4条为`response_fingerprint_full`、13条为`response_fingerprint_partial`、2条为`locator_only_partial`、3条为`hypothesis_only`。这里的`full`只表示该RDEC列出的全部样本都有成功响应指纹，不表示外部作品证明了本项目的取舍。

所以D01可以支持“为什么值得做某个原型”，不能支持“竞品已经证明本项目规则正确”，也不能替代P1/P2/P3与辅助玩法真人测试。

## 七、主战棋综合裁决

### 7.1 保留：清晰意图，但拒绝完美答案

从 Into the Breach 保留“意图必须一眼可读、攻击顺序和保护对象进入主UI”；从 Radio Commander、HighFleet、NEBULOUS 保留“信息有来源、时间、精度和通信链”。综合后：

- 已确认事实、传感接触、角色解释、白鸢预演和七海许可态必须视觉分层；
- 敌方行动只在传感/情报足够时显示目标、范围或动作家族，不默认给精确落点和结果；
- 玩家可以付出暴露、带宽、时间或政治责任换取更高精度；
- 敌人可伪装、变招、干扰、切断通信或利用玩家对旧模式的误判。

### 7.2 保留：短时间窗 WEGO，拒绝脚本编程

从 Phantom Brigade 保留动作时长和冲突点；从 Frozen Synapse 保留“我方计划＋敌方假设”；从 Valkyria 保留路线具身和执行途中受威胁；从 Door Kickers 2 保留同步提交节点。

候选综合是：

1. 规划窗读取不完整Intent；
2. 给3-6个前线单位排一个短阶段动作；
3. 主角团只在有限注意槽内修改信息、路线、许可或可行性；
4. 权限/机魂同意不完整时不能提交高风险动作；
5. 提交后全体进行5-12秒具身执行；
6. 重大新情报只允许触发一次有限中止/改令窗口；
7. 结果进入伤损、关系、权限、敌人学习和地点状态。

不采用逐帧路径、无限等待条件和几十个姿态参数。复杂度应来自相互作用、信息不完备和持续后果，不来自像程序员一样写脚本。

### 7.3 保留：角色化 C2，拒绝通用支援Buff

从 SRW Y 的 Assist Crew 只保留“非驾驶角色要有正式战场席位”；实际动词按本项目角色重做：

- 纪存：整合愿意共享的局部视野、提出路线/接驳，不接管身体；
- 白鸢：基于当前证据预演少量条件方案，结果可被新信息推翻；
- 七海：在本人或已转授范围内授权、限制、叫停，并承担问责；
- 工程组：验证结构/载荷/接口，把候选方案变成可执行或明确不可执行；
- 驾驶员与机魂：接受、修改、拖延或拒绝高风险动作；
- 作战室共享层：传感、通信、来源和过期状态，不归任何角色万能拥有。

回血、回EN、加攻击等普通支援仍可由机体/装备系统提供，但不应成为主角团身份的主要表达。

### 7.4 保留：功能伤损和连续部署，拒绝佣兵磨损

从 BATTLETECH、XCOM和Pyre保留：

- 部件/舰区功能伤损改变下一阶段的可用动作；
- 伤员、机体、支援岗位不能在Episode切话时自动恢复；
- 失败、撤退和部分成功也进入故事；
- 维修位、角色岗位和关系状态制造编队选择。

不采用随机永久死亡、刷合同、随机Salvage、庞大币种和数值装甲墙。

## 八、轻探索与解谜综合裁决

不为11个案例各造一种小游戏，只保留三个可复用原型家族。

### 8.1 P-EX1 微型自由探索

来源组合：A Short Hike × TOEM × Alba。

```text
远处可见的地点目标
→ 两到三条地标路线
→ 观察/拍摄/帮助具名人物
→ 得到可验证证据或公共支持
→ 改变后续维修、关系、设施开放或战场条件
```

每次20-40分钟；不铺满图标，不做同质跑腿。

### 8.2 P-EX2 调查与工程实证

来源组合：Botany Manor × Strange Horticulture × Obra Dinn。

```text
分散的物件/损伤/日志证据
→ candidate/likely/confirmed判断
→ 配置真实负载、温度、信号或接口
→ 实体试验
→ 修复、拒绝、保存或交付
→ 结果写回机体、关系和权限
```

每案5-15分钟；不能只搜三张纸再输配方。

### 8.3 P-EX3 知识门控遗迹

来源组合：Outer Wilds × Chants of Sennaar；Heaven's Vault只补“错误解释的前向小后果”。

```text
第一次看见但不理解
→ 在另一地点/时段获得语义或因果证据
→ 重访并验证
→ 知识本身打开路线
→ 旧判断可能被修正
```

用于B2、黑匣子、迟到回信和机魂动作语法，不把所有资料变文字替换题，也不复制全游戏时间循环。

### 8.4 统一失败与回写

辅助玩法只用三种失败语法：

- `local_retry`：当前空间/操作可立即重试；
- `hypothesis_unconfirmed`：证据不足，结论保持候选；
- `forward_consequence`：错误或放弃产生小而可读、以后可修正的后果。

每次辅助玩法强制输出：

```text
evidence_created
world_or_relation_writeback
future_consumer
```

缺任一字段，就只是拖延下一段Reader。

## 九、Hub、关系、收藏与任务转换综合裁决

### 9.1 万机馆是移动之家，不是菜单皮肤

从 Pyre、Spiritfarer 和 Hades 保留：任务成败后回到同一个会变化的家；角色上舰、离舰、受伤、留下物件和改变工作习惯，都在空间中可见。

### 9.2 一章一个有限整备周期

从 Three Houses、Citizen Sleeper、Chimera Squad 保留有限时段/岗位，但压缩为每次返馆显示2-5个事项组、标准3格内最多提交3张高价值工作卡：

- 修复/整备；
- 调查/档案；
- 关系/照料；
- 开馆/公共沟通；
- 外勤/工程试作。

同一角色同一时段只能在一个岗位。玩家不是为了清光全员对白，而是在可见的未来后果中选择。

### 9.3 任务牌与战后关系回流

从 Midnight Suns 保留任务开始前显示目标、风险、奖励和要求；战后只触发1-2个由刚才结果产生的高价值关系/生活事件。关系成长优先解锁：

- 新的援护或组合动作；
- 更可靠的信息共享；
- 可提出但仍可拒绝的高风险方案；
- 支线/隐藏路线；
- 舰内岗位与设施使用许可。

不采用每日送礼答案表和好感刷取。

### 9.4 收藏是共同生活史

收藏不只解锁百科百分比。每项重要藏品至少关联：

- 一台具体机体/一个主体；
- 一段已在故事或探索中赢得的知识；
- 一个展陈位置或空间痕迹；
- 一项可见的关系、工程、战术或公共支持回写；
- 一个未来再次被读取的窗口。

## 十、明确不采用

- 完美信息＋唯一最优解；
- 无限回退；
- 玩家万能控制所有机体和机魂；
- 随机永久死亡与程序生成主线地图；
- PP/Credits/刷合同/随机Salvage主导成长；
- 大量装备词条和随机Mod；
- 巨型Hub跑腿、全员日更对白和送礼答案；
- 每章一种独立小游戏；
- 纯节点Hub取代万机馆实体空间；
- 抽象谜题不回写角色、机体或世界；
- 为了“战略感”叠多资源、多倒计时和数据库级菜单。

## 十一、进入D02/D04/D05的已登记原型队列

下表只使用 [prototype-test-registry.tsv](../data/prototype-test-registry.tsv) 中的正式 `prototype_id`。旧研究占位名 `P-TAC1`、`P-TAC2`、`P-TAC3` 已废止，不得作为依赖、证据或回执引用。

| 已登记原型 | 研究来源 | 先回答的问题 |
| --- | --- | --- |
| `D04-P1-A`、`D04-P1-B`、`D04-P1-C` 三单位同图基础战术 | Into the Breach、Valkyria、BATTLETECH | 没有主角权能时，移动/站位/反应/保护/撤退是否已有两种胜法？ |
| `D04-P1-A/B/C/D`、`D04-P1-SHORTLIST` 与 `D04-P2-CROSSOVER` 的时制中立比较 | Phantom Brigade、Frozen Synapse、Radio Commander | 共享身体语义下哪些Scheduler应淘汰/shortlist；装入同一最小核心C2后，最终应select、revise、no_selection或retire_all？ |
| `D04-P2` 角色C2权能 | CMO、HighFleet、NEBULOUS、SRW Y | 信息、路线、许可、工程和同意能否产生不同选择而非Buff菜单？ |
| P-EX1 微型自由探索 | A Short Hike、TOEM、Alba | 地标、证据和具名人物能否在20-40分钟内产生后续回写？ |
| P-EX2 调查/工程实证 | Botany Manor、Strange Horticulture、Obra Dinn | 玩家能否从证据提出假设，并由实体试验确认而非文本判分？ |
| P-EX3 知识门控遗迹 | Outer Wilds、Chants、Heaven's Vault | 失败/误判能否留下知识并允许后续纠偏？ |
| P-HUB1 一次回馆周期 | Pyre、Midnight Suns、Chimera Squad、Spiritfarer | 2–5个事项组能否被压进固定3格、最多3张工作卡，并通过角色岗位和战后变化形成轻松但真实的取舍？ |

## 十二、研究后的下一步

G1研究在Candidate层完成。下一步把上述裁决写成D02产品体验宪章和D03系统/状态图；同时只先验证 `D04-P1-A`、`D04-P1-B`、`D04-P1-C` 的共同基础战术问题，避免在基础战棋未成立前先堆 `D04-P2` 主角权能。

## 十三、首批官方来源

- [Super Robot Wars Y official launch/system description](https://www.bandainamcoent.com/news/super-robot-wars-y-now-available-for-consoles-and-pc)
- [Super Robot Wars 30 official site](https://www.bandainamcoent.com/games/super-robot-wars-30)
- [13 Sentinels: Aegis Rim official site](https://asia.sega.com/13sar/)
- [Valkyria Chronicles 4 official system page](https://asia.sega.com/val/cht/system/inner.html?page=strategy)
- [BATTLETECH official overview](https://www.paradoxinteractive.com/zh-CN/games/battletech/about)
- [BATTLETECH Flashpoint official announcement](https://www.paradoxinteractive.com/media/press-releases/press-release/battletech-flashpoint-launches-today)
