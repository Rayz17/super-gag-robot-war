# 《超GAG机器人大战》多玩法体验生产合同 v1

> 状态：候选生产设计；补足 `四种玩家权能模式 + 三类活动语法` 从运行时骨架到正式单话体验之间的缺口。  
> 日期：2026-07-15。  
> 上游：`2026-06-22-chao-gag-hybrid-play-experience-design.md`、`2026-07-13-chao-gag-multi-play-runtime-architecture-v1.md`、`2026-07-14-chao-gag-multi-play-implementation-blueprint-v2.md`。  
> 运行样例：M6 旧件市 / 旧拳王验证图。  
> Canon 边界：本文不把 M6 验证台词、C02E03 节点或几何美术提升为正式剧情；不解冻 V35.10；不提前实现 `SIGNAL`。

---

## 0. 核心结论

当前方案已经回答了两个工程问题：

1. 四种主模式如何切换、暂停、存取和提交结果。
2. `CONSTRAINT` 与 `TIMING` 如何复用，而不为每个梗点重造小游戏引擎。

它还没有完整回答三个产品问题：

1. 为什么玩家愿意从一种玩法进入另一种玩法。
2. 每种模式本身凭什么好玩，而不只是换一套 UI 读下一段数据。
3. 为什么玩家最后记住的是人物、机器人和事件，而不是“五个功能都跑通了”。

因此正式实现还需要一层 **体验生产合同**：

> **一话围绕一个戏剧对象和一个不可回避的问题展开；不同模式不是轮流出现，而是让玩家用不同权能逐层认识、触碰、押注、保护并承担同一件事。**

正式生产单位不是：

```text
一段 ADV + 一个探索地图 + 一个小游戏 + 一场战棋 + 一个结算页
```

而是：

```text
一个戏剧结
  + 三条连续性
  + 若干必要模式
  + 一次玩家承诺
  + 至少三次可见消费
  + 一项带入下一话的未完成责任
```

---

## 1. 当前方案的真实状态

### 1.1 已经成立的部分

- `EpisodeDirector -> ModeRouter -> RunStateStore` 已能编排独立 ModeScene。
- `NARRATIVE / SPATIAL / TACTICAL / DESK` 已有运行入口。
- `CONSTRAINT / TIMING` 已能产生四档软结果，并通过 `ActivityOutcome` 改变战斗与人物状态。
- M6 已证明同一个“旧拳王漏掉一拍”的问题可以从维修棚进入擂台，再回到纪存和唐胶的关系。
- 模式交接转场已能显示地点、时间、上一因果与下一责任，并在切换期间冻结输入。
- 内容 bundle 已能校验 Graph、场景、活动、战斗和 Patch 消费闭包。

### 1.2 尚未成立的部分

#### 模式壳存在，但模式乐趣不足

- 当前 `NarrativeModeScene` 主要是平面底色、标题和文本，没有真正的角色构图、物件动作、镜头节奏和选择张力。
- 当前 M6 战后反应使用几何头像占位，人物场仍像“结算说明的拟人化版本”。
- 当前 `DeskModeScene` 只展示摘要和内部 debt id，玩家没有比较、预览和提交，不构成桌面权能。
- 当前 Workshop 虽有连续行走和两种活动，但空间、机体身体和活动反馈仍主要由单场脚本手绘，不能直接支撑批量正式内容。
- 当前 Tactical 已有行动链和斜 45 度地图，但场景物件、机体形象和战前空间的稳定对应仍不足。

#### 因果被记录了，但还没有被充分表演

M6 Graph 的因果是清楚的：维修选择改变擂台局面，停拳救人改变人物关系。问题是玩家需要从画面、动作和角色反应中自己得出这个结论，不能主要依靠转场卡、侧栏说明和结算文字替它解释。

#### 正式单话内容合同仍缺一层

现有 bundle 能证明“引用存在”，但不能证明：

- 戏剧对象在各模式中仍是同一个对象。
- 玩家选择真的有两个有意义的方向。
- 每个模式提供了足够的可玩密度。
- 重要结果不是只被一个数值或一句台词消费。
- 一话的阅读、走动、决策、战斗和回收形成了节奏波形。

这正是本文要补的部分。

> 2026-07-15 P4 回执：上述“合同仍缺一层”是本文立项时的缺口。`ExperienceContractValidator` 与 `ConsumptionLedgerValidator` 现已接入 `EpisodeBundleCompiler`；M6 已通过戏剧结、转场连续性、稳定对象跨模式锚点、四消费槽、Offer 失败继续和容量声明的结构门禁。M6 真人容量回执仍为 `pending_external`，因此只证明结构，不证明正式单话容量或玩家理解。

---

## 2. 一话的最小核心：戏剧结

### 2.1 定义

每个正式 Episode 必须有一个 `EpisodeKnot`：

```text
EpisodeKnot
  dramatic_object      玩家能看见、触碰或指认的具体对象
  dramatic_question    本话不能回避的问题
  human_claims[]       不同人物希望对象成为什么
  machine_claim        机器人自身通过动作表达的倾向
  player_commitment    玩家必须承担的具体决定
  irreversible_cost    无论怎样选择都会失去、损坏或欠下什么
  next_debt            带入下一话的未完成责任
```

戏剧对象不能只是抽象主题。它应是：

- 一台机体的一只拳。
- 一面孩子写过字的留言墙。
- 一条撤离路线。
- 一盒被作者否认的模型。
- 一段被剪快的旧录像。
- 一扇只有某人有权打开的门。

主题由人物和玩家怎样对待这个对象自然生长。

### 2.2 三条连续性

一次主模式切换至少保留以下三条中的两条：

1. **对象连续性**：仍在处理同一个具名物件、人物或机体部位。
2. **动作连续性**：上一模式做出的动作在下一模式变成新的规则或局面。
3. **责任连续性**：同一个人或组织仍要承担结果，没有在转场时凭空换题。

若三条全断，下一节点应被视为新场景或新 Episode，而不是同一条多玩法链。

### 2.3 同物异义链

多玩法的乐趣来自“同一个东西在不同尺度下改变意义”。

以 M6 的旧拳王右拳为例：

| 层 | 玩家看到的意义 | 玩家行为 |
| --- | --- | --- |
| Narrative | 买家要冠军复刻，唐胶认为迟一拍不是故障 | 听懂冲突，不急着选阵营 |
| Spatial | 右拳、膝轴、旧影子和仓门是一个身体系统 | 走近、检查、比较声音与动作 |
| Constraint | 零件不够，必须决定先保承力、动作记忆还是坍塌余量 | 分配并预览代价 |
| Timing | 玩家亲手感到那一拍是身体的迟疑，不是抽象数值 | 按住、等待、松手 |
| Tactical | 停拳窗口成为救人的空间和时机 | 保护、占位、决定是否完成攻击 |
| Reaction | 唐胶与纪存争论它是失误、旧伤还是自主选择 | 回应或保持沉默 |
| Desk | 原速录像和维修否决权成为以后可追责的记录 | 决定如何保存、公开和承诺 |

如果删掉其中一层后，其他层完全不受影响，说明这一层很可能只是附加小游戏。

---

## 3. 四种模式各自必须提供什么乐趣

模式由玩家权能定义，但权能必须产生可感知的乐趣。机器合同见 `data/gameplay/multi_play_mode_experience_contract_v0_1.tsv`。

### 3.1 `NARRATIVE`：读人，而不是读设定

#### 核心乐趣

玩家从停顿、目光、物件动作、说谎方式和权力关系中判断“这个人真正想要什么”。

#### 最小结构

一场具名 Narrative Scene 至少应包含：

1. 一个当前可见欲望。
2. 一个角色不愿直说的东西。
3. 一个物件或身体动作承担潜台词。
4. 一次关系位置改变：允许、拒绝、误解、交付、撤回或承担。
5. 若有选择，选择改变立场、权限或后续说法，而不是知识问答。

#### 实现形态

```text
NarrativeModeScene
  SceneStage                 背景、前景、场内对象和镜头锚点
  CharacterStage             左/右/近景/背影/离场站位
  NarrativeDirector          播放 DialogueBeat
  ChoicePresenter            立场选择、沉默、打断、交付
  CinematicCuePlayer         停顿、推拉、震动、音效、Cut-in
```

同一 `DialogueBeat` 可用以下 profile：

- `cinematic_panel`
- `standard_adv`
- `spatial_overlay`
- `battle_comms`
- `battle_cut_in`
- `daily_scene`

禁止让每个 ModeScene 自己用 `_draw()` 重写一套角色对话框。

#### 可玩性边界

Narrative 不靠频繁选项假装互动。玩家的互动来自：

- 何时追问。
- 是否沉默。
- 把哪件证据交给谁。
- 是否让某人承担公开责任。
- 是否允许一个角色把话说完。

### 3.2 `SPATIAL`：用身体认识世界

#### 核心乐趣

玩家通过距离、遮挡、路线、声音和物件位置形成自己的理解，而不是在全景平面上逐个点击发光圆点。

#### 最小结构

每个正式空间段至少有：

1. 一个可建立方向感的主景和地标。
2. 两到四个相互关联的小场景或空间区段。
3. 一个会移动、变化或阻挡的动态要素。
4. 至少两条推进路径，不要求搜齐所有热点。
5. 一个身体动作：搬、扶、跟随、绕行、护送、停下听、拉闸或撤退。
6. 一次空间状态改变，并能在 Tactical 或返场时被认出。

#### 三层空间密度

```text
建立层：玩家知道我在哪、出口在哪、危险从哪来
行动层：路线、NPC、障碍和可互动对象形成选择
回响层：可选细节补人物、梗点、世界和隐藏条件
```

主线不能要求全部调查回响层。完成关键动作即可推进；多探索改变理解、可选方案和后续台词。

#### 实现形态

```text
SpatialModeScene
  LocationScene
    NavigationLayer
    CollisionLayer
    StableObjectNodes[]
    NPCActorNodes[]
    HazardLayer
    CameraRig
  InteractionDirector
  ActivityHost
  NarrativeOverlay
```

热点只声明可用条件、交互动作、重复策略和结果，不自行改永久状态。

### 3.3 `TACTICAL`：让准备变成需要承担的战场

#### 核心乐趣

玩家读懂敌方意图，在不能全保的局面中使用具名单位和地形做决定，并看见机器人用身体改变空间。

#### 正式关卡最小结构

1. 一个明确主目标和至少一个可牺牲次目标。
2. 一个在战前可读的敌方意图系统。
3. 至少一次中段地图或规则变化。
4. 一个由前序模式产生的可见差异。
5. 至少一次角色或机体主动改变命令含义。
6. 胜利、有代价胜利、失败或撤离均有尊严且能继续。
7. 战后后果写回空间、身体和关系，不只发经验与钱。

#### 战斗不是前序玩法的领奖页

前序活动只能改变：

- 初始位置。
- 可见意图。
- 路线与阻挡。
- 目标完整度。
- 可用动作、支援或停机权。
- 敌我双方的风险窗口。

它不能直接替玩家完成章节主冲突。

#### 实现形态

战斗逻辑与表现继续分离：

```text
DeclarativeBattleSession       权威状态、行动链、AI、结果
TacticalPresenter              斜45度地图、单位、意图、范围、预测
BattleNarrativeBridge          战中短对白、事件触发、角色违令/支援
BattleCinematicDirector        武器演出、Pose、Cut-in、伤害反馈
```

Workshop 中的仓门、吊架、右拳和出口需要通过相同 `stable_object_id` 映射到 Tactical，不允许只在战斗定义里重新造一批同名格子。

### 3.4 `DESK`：组织责任，而不是看结算报告

#### 核心乐趣

玩家把战后复杂后果整理成下一步可执行承诺，并决定什么公开、什么保留、谁先处理。

#### 最小结构

Desk 节点至少包含一次真正的桌面动作：

- 比较两个记录版本。
- 给一个人临时权限。
- 决定先修哪一处身体或设施。
- 指定公开范围和署名。
- 把有限人手派给不同未结事项。
- 保留原始记录，拒绝一个“更好看”的剪辑。

#### 三层信息

```text
现在：必须先处理什么
证据：为什么会变成这样
承诺：提交后谁获得权限、谁承担代价、什么被推迟
```

Desk 不显示内部 `debt_id`、Patch id 或事务 id。内部状态必须投影成人物能理解的普通语言和具体对象。

#### 实现形态

```text
DeskModeScene
  WorkbenchProjection          从统一状态生成可读卡片
  CompareView                  版本、证据、人物请求
  ConstraintActivityHost       安排与承诺
  CommitmentPreview            即时、战术、关系、跨话后果
  CommitReceipt                具体句子，不是资源报表
```

笔记本可作为覆盖层随时阅读；Desk 是剧情节点，玩家必须做一次组织性决定。两者不能继续由同一个静态摘要页冒充。

---

## 4. 三类活动怎样嵌入，而不是弹出

### 4.1 `CONSTRAINT`

玩家体验不是“把卡片放对”，而是在有限资源和互相冲突的责任之间做安排。

每个实例必须有：

- 具体对象和人物。
- 至少两个不能同时满足的要求。
- 可撤销草案。
- 可读后果预览。
- 一次正式提交。
- 提交后有人受益，也有人被推迟、暴露或失望。

### 4.2 `TIMING`

玩家体验不是“追指针拿高分”，而是听懂机器身体并在正确时刻介入或停手。

每个实例必须把抽象曲线绑定到：

- 一个具体机体部位。
- 一种可听见或看见的机械反馈。
- 一个角色对“修好”的不同理解。
- 一个失败也能继续的身体后果。

评分只用于系统归档；玩家首先看到的是“右拳发热”“膝轴让了一步”“影子仍慢半拍”。

### 4.3 `SIGNAL`

`SIGNAL` 只用于玩家确实需要分辨多个版本、信号层或真伪证据的场景。它不是通用解谜皮肤。

当前保持未实现，直到 M6 真人盲测证明玩家能够在一次 Episode 中理解四模式、`CONSTRAINT` 与 `TIMING`，且没有明显认知过载。

未来最小实例应先满足：

- 有两个都说得通但不能同时为真的版本。
- 玩家已在 Narrative 或 Spatial 中见过相关人和物。
- 筛选结果改变后续可见信息或敌方规则。
- 错判产生可恢复的错误行动，而不是重做谜题。

---

## 5. 正式单话的节奏与容量

### 5.1 不固定打卡，但必须形成波形

标准 Episode 可以采用：

```mermaid
flowchart LR
  A["人物欲望先落地"] --> B["玩家进入具体空间"]
  B --> C["第一次小承诺"]
  C --> D["压力升级或误判"]
  D --> E["正式战术冲突"]
  E --> F["人物重新解释结果"]
  F --> G["玩家整理未完成责任"]
```

也可以是：

- `NARRATIVE -> TACTICAL -> NARRATIVE` 的紧急战。
- `SPATIAL -> TIMING -> NARRATIVE` 的舰外抢修。
- `DESK -> NARRATIVE -> DESK` 的听证与公开责任话。
- `SPATIAL -> SIGNAL -> TACTICAL` 的残响侦察话。

未使用层必须有戏剧上的 `skip_reason`，不能以制作未完成代替。

### 5.2 三种正式容量档

| 档位 | 首次游玩目标 | 适用 | 典型构成 |
| --- | ---: | --- | --- |
| `compact` | 22-35 分钟 | 撤退、日常危机、关系短章 | 2-3 个主模式，短 Tactical 或无 Tactical |
| `standard` | 35-60 分钟 | 常规主线 Episode | 3-4 个主模式，15-30 分钟 Tactical |
| `major` | 60-90 分钟 | 章末、路线转折、巨型事件 | 多阶段 Tactical，完整前后场与关系回收 |

这不是强迫玩家把每个热点看完。首玩容量来自场景、人物和战局的有效变化，不来自重复对白、走空路或把同一信息解释三次。

### 5.3 模式内容预算

| 模式 | 标准 Episode 建议 | 不合格信号 |
| --- | --- | --- |
| Narrative | 2-4 场，每场有关系转折或行动结果 | 只讲设定、所有人同一种口吻 |
| Spatial | 2-4 个关联小场景，1 个动态事件，2 条推进路径 | 搜齐发光点才开门 |
| Activity | 1 个主要活动，必要时与第二语法复合 | 评分与剧情对象无关 |
| Tactical | 1 场有中段变化的主冲突 | 只清怪，前序选择仅显示 buff |
| Desk | 1 次比较/安排/承诺 | 静态摘要后按确认 |

---

## 6. 典型 Episode 的端到端例子

以下继续使用 M6 的“旧拳王漏掉一拍”，但只作为体验结构例，不把验证内容升格为 C02 正式剧情。

### 6.1 Narrative：先让人和欲望成立

直播买家不是一条系统提示，而是通过画面要求“复刻冠军右摆拳”。唐胶嘴上答应看机器，手却先关掉自动补帧；纪存发现影子录像比现实拳慢一拍。

玩家可追问买家、问唐胶为什么不校正，或先听机器。三种选择不决定正确答案，而是决定接下来谁愿意先给纪存哪一部分权限。

### 6.2 Spatial：让玩家亲自形成判断

维修棚拆成前台、维修架、旧影像角和后仓四个关联小场景。玩家可先：

- 听右拳轴承。
- 跟着电缆找到膝轴负载。
- 对照原速影子。
- 发现后仓吊架已超载。

调查任意两个能推进，但所得维修方案不同。玩家不需要搜齐全部圆点。

### 6.3 Constraint + Timing：做出第一次承诺

玩家把有限零件分给承力链、动作记忆或仓顶余量。随后不是跳到抽象网页，而是镜头推近机体右拳，唐胶在旁边报声音，玩家通过按住和松手确认身体反馈。

结果立即在场景里出现：站姿、灯色、声音、唐胶的手和纪存能否靠近都发生变化。

### 6.4 Tactical：前面的事变成战场

直播开始，吊架压穿后仓。玩家认得刚才走过的门、仓架和出口。第二回合地图翻转时：

- 保承力链，旧拳王能撑住上层，但转身慢。
- 保动作记忆，能更早看见停拳窗口，但仓门更脆。
- 保后仓余量，救援路线更宽，但右拳输出受限。

主目标从“完成直播动作”变成“让工人和出口活下来”。机器人不是被玩家替它做决定；玩家创造条件，旧拳王可在关键时刻拒绝完成那一拳。

### 6.5 Reaction：人物重新解释同一动作

战后先看被拳面接住的人，再切到唐胶的手仍放在急停上。纪存是否保留原速录像、是否公开把停拳写成机器选择，会改变唐胶给他的权限。角色根据自己的欲望和损失说话，不朗读活动档位。

### 6.6 Desk：把余波变成下一步

玩家比较直播剪辑、原速录像和维修记录，必须决定：

- 公开哪一版。
- 谁拥有下次维修否决权。
- 先修拳还是先补后仓。

无论怎样提交，都留下一个具体未完成责任进入下一话。

---

## 7. 数据合同

### 7.1 `experience_contract`

每个正式 Episode manifest 必须增加：

```json
{
  "experience_contract": {
    "episode_knot_id": "KNOT_C02_OLD_BOXER_MISSED_BEAT",
    "dramatic_object_id": "ANCHOR_OLD_BOXER_RIGHT_FIST",
    "dramatic_question": "修好一台机器人，是否包括保留它不肯完成的动作？",
    "player_commitment_id": "COMMIT_C02_REPAIR_PRIORITY",
    "irreversible_cost": "至少一项身体、空间或公开责任被推迟",
    "next_debt_id": "DEBT_C02_ORIGINAL_SPEED_RECORD",
    "capacity_band": "standard",
    "required_continuity": ["object", "action", "responsibility"],
    "required_consumption_slots": ["immediate", "conflict", "character", "settlement"]
  }
}
```

字段定义见 `data/gameplay/multi_play_episode_knot_schema_v0_1.tsv`。

### 7.2 `stable_object_binding`

同一地点或物件跨模式绑定：

```json
{
  "stable_object_id": "ANCHOR_OLD_BOXER_RIGHT_FIST",
  "narrative_anchor": "right_fist_closeup",
  "spatial_node": "workshop/right_fist",
  "activity_target": "timing/right_fist_load",
  "tactical_prop_or_unit": "unit_old_boxer/right_fist_state",
  "desk_projection": "record/original_speed_punch"
}
```

Bundle 编译器应阻断必需模式缺少绑定、同一 ID 指向互相矛盾实体、以及 Tactical 重新命名导致的断链。

### 7.3 `interaction_offer`

所有调查、对话和局部动作使用统一合同：

```text
offer_id
actor_id
target_id
verb
availability_conditions[]
presentation_profile
first_use_beat
repeat_policy: disabled | short_repeat | stateful_repeat
outcome_contract
failure_continuation
```

这可以解决旧 Demo 中 NPC 无限重复首轮对话、通讯台过早可调查、所有热点一句话结束等问题。

### 7.4 消费账本

每个重要结果必须在构建时登记：

```text
result_id
immediate_consumer
conflict_consumer
character_consumer
settlement_consumer
optional_cross_episode_consumer
```

编译器目前只验证 Patch 有 Tactical consumer；下一步应扩展为体验消费账本检查，但不能用“存在一句文本”冒充人物回收。

> 2026-07-15 实现回执：消费账本检查已实现。四槽必须分别指向真实 StableObject、Tactical/Battle、Narrative、Desk/承诺组，并提供玩家可见证据；删除人物槽会阻断构建。结构闭包仍不能替代人物质量与真人回收验收。

---

## 8. Godot 实现边界

### 8.1 保留现有核心

以下部分继续保留，不重写：

- `GameKernel`
- `EpisodeDirector`
- `ModeRouter`
- `RunStateStore`
- `StateTransaction`
- `OutcomeValidator`
- `InputRouter`
- `SaveService`
- `ConstraintActivityController`
- `TimingActivityController`
- `DeclarativeBattleSession`
- `EpisodeBundleCompiler`
- `ModeTransitionDirector`

### 8.2 共享生产壳与验证组件

```text
scripts/core/presentation/
  narrative_director.gd
  scene_stage.gd
  character_stage.gd
  dialogue_beat_player.gd
  cinematic_cue_player.gd

scripts/core/spatial/
  spatial_scene_runtime.gd
  stable_object_node.gd
  interaction_director.gd
  actor_controller.gd
  location_transition.gd

scripts/core/desk/
  desk_projection_builder.gd
  commitment_preview.gd
  settlement_presenter.gd

scripts/core/battle/presentation/
  tactical_presenter.gd
  battle_narrative_bridge.gd
  battle_cinematic_director.gd

scripts/core/content/
  experience_contract_validator.gd
  stable_object_binding_registry.gd
  consumption_ledger_validator.gd
```

### 8.3 ModeScene 变薄

正式 ModeScene 只负责组合共享组件和本场资源，不再自己手写全部输入、绘制和台词。

```text
Episode-specific ModeScene
  = location/presentation assets
  + authored beats/offers
  + shared runtime components
  + small scene-specific rule adapter
```

若一个 Episode-specific 脚本继续同时绘制场景、角色、卡片、时机条、侧栏和结算，它应被视为尚未完成平台化，而不是“复用成功”。

### 8.4 转场的呈现层级

现有因果转场保留为安全底座，但正式演出按以下优先级：

1. **匹配剪辑**：同一物件从人尺度切到战术尺度。
2. **动作接力**：上一场动作直接造成下一场变化。
3. **声音先行**：警报、关节声、广播或角色一句话带入下一场。
4. **地点时间卡**：需要明确时空跳跃时使用。
5. **完整因果说明卡**：仅在测试、复杂跳转或无资产降级时使用。

不能让每次模式切换都停下来阅读一张解释卡；那会把连续戏剧重新切成章节菜单。

---

## 9. 生产工作流

### 9.1 先写故事，再拆玩法

```text
Reader Synopsis
  -> EpisodeKnot
  -> Scene Beats
  -> 玩家承诺与失败尊严
  -> 选择必要 Mode
  -> 稳定对象绑定
  -> Activity/Battle/Reaction/Desk 合同
  -> Bundle 编译
  -> 像素与真人验收
```

不能先决定“这话来一个音游”，再找剧情理由。

### 9.2 四席联合走查

每个正式 Episode 在进 Godot 前由四个视角检查：

| 视角 | 必答问题 |
| --- | --- |
| 编剧 | 角色不靠系统说明也会这样行动吗？ |
| 游戏 | 玩家做了什么不可替代的决定？ |
| 机器人文化 | 机体是否有正向欲望、身体性和标志动作？ |
| 制作 | 同一资产和规则是否能跨模式复用，而不是暗中造五套内容？ |

### 9.3 真人验收不只看通关

测试者结束后应能用普通语言回答：

1. 这一话到底发生了什么。
2. 为什么要从上一个场景进入下一个场景。
3. 自己哪次选择真正改变了战场。
4. 哪个人或机器人因此改变了对谁的态度或权限。
5. 下一话仍欠着什么。

只要测试者主要回答“先探索、再小游戏、再战棋”，本轮体验合同就没有通过。

---

## 10. 实施优先级

### P0：冻结 M6 为架构回归样例

- 保留现有五节点、两活动、Patch、事务、存档、输入和导出测试。
- 不继续把验证文字和几何 UI 当正式内容堆厚。
- 建立五节点像素基线和真人首玩基线。

### P1：先完成 Narrative 与 Desk 的共享生产壳

原因：这两层当前最像验证界面，也最直接影响人物真实感、剧情理解与结算余韵。

- `NarrativeDirector v1`：背景、左右人物、说话者高亮、动作、停顿、选择和空间/战斗 overlay profile。
- `DeskWorkbench v1`：比较、预览、承诺、一次提交；笔记本只读覆盖层与 Desk 剧情节点分开。
- 将 M6 intro、reaction、desk 迁入共享壳，验证不复制台词状态机。

> 2026-07-15 实现回执：M6 已迁入 `ChaoGagNarrativeDirector` 与 `ChaoGagDeskWorkbench`。背景、左右人物、说话者焦点、广播、舞台动作、选择、动态证据卡、处理方向、后果预览、取消、二次确认、精确存取和一次提交均已通过自动与 1280×720 像素验证；M6 bundle 同时闭合五项演出资产引用。该结果只完成候选样例上的 P1，不提升 M6 或新资产为正式内容，详见 `production/multi-play-runtime/m6-narrative-desk-production-shell-implementation-status-v1.md`。

### P2：建立 Spatial 稳定对象和互动合同

- 用场景节点替代手绘热点坐标。
- 统一 `InteractionOffer`、重复策略、条件解锁和多轮 NarrativeOverlay。
- 支持房间/小场景切换、返回点和动态 NPC。
- 把 Workshop 的右拳、膝轴、影子、仓门登记为稳定对象。

> 2026-07-15 实现回执：M6 已把右拳护具、膝轴、原速录像、仓门报警器、直播终端和零件盘登记为 Graph 声明的稳定对象，并生成 `Area2D` 场景节点；Workshop 已拆为直播前台、维修内场和零件后仓三个 Graph 房间，支持 Portal、精确返回点、唐胶动态位置、非清单分组推进和多轮 `SpatialNarrativeOverlay`。`InteractionOffer` 覆盖首轮/重复序列、条件解锁、选择分支、显式活动入口和精确存取，`SpatialInteractionDirector` 统一物件、人物与门口交互；Bundle Compiler 阻断房间、出生点、Portal、对象和 NPC placement 断链。候选 P2 生产层已完成，但正式地图分层、碰撞、行走 Sprite、真人容量和正式 Episode 验收仍未完成，详见 `production/multi-play-runtime/m6-spatial-production-layer-implementation-status-v1.md`。

### P3：让 Tactical 继承同一空间

- 同一对象映射到战术格、单位部件或地图事件。
- 中段地图变化由具名对象状态触发。
- 战中人物反应读取 ActivityOutcome 和关系边，不朗读 score band。
- 增加机体地图 Sprite、标志 Pose、Cut-in 和武器/救援短演出。

> 2026-07-15 实现回执：M6 已将六个稳定对象映射到旧拳王部件/武器、影子陪练、仓门与证据目标、敌方镜头、坍塌事件和地图格；解析结果在战棋中显示玩家可读来源，并由 Bundle Compiler 校验映射闭包。后续 P3 表现层已加入声明式 `BattlePresentationCatalog`、完整旧拳王地图图、标志 Pose、唐胶候选 Cut-in、两项武器演出和仓门/维修草案驱动的第二回合事件版本；原速录像也会切换漏拍停拳演出。该结果仍是候选运行时证明，其他单位地图图、正式动作帧、正式 Cut-in、音效、真人和平台验收未完成。详见 `production/multi-play-runtime/m6-spatial-tactical-object-continuity-implementation-status-v1.md` 与 `m6-tactical-presentation-production-layer-implementation-status-v1.md`。

### P4：扩展 Bundle 体验门禁

- `experience_contract` 完整性。
- 三条连续性至少保留两条。
- 稳定对象绑定闭包。
- 重要结果四消费槽。
- 每个 InteractionOffer 有重复策略与失败继续路径。
- 容量档与实际首玩回执对比。

> 2026-07-15 实现回执：P4 已接入构建器。M6 manifest 已声明完整 `experience_contract`，四次非开场切换均提供至少两类连续性证据，两个稳定对象跨四种模式绑定，六个 Offer 有显式重复/结果/失败继续合同，玩家承诺有四槽消费账本。容量门禁会读取完成回执并校验 `compact / standard / major` 时长；M6 当前只有 `standard` 声明、没有外部完成回执，因此 bundle 诚实记录 `structure_pass_capacity_pending`。详见 `production/multi-play-runtime/m6-experience-contract-build-gate-implementation-status-v1.md`。

### P5：用一话正式内容做生产验收

选择一话已通过 Pressure Board 与 Reader 审查的正式 Episode，从可读故事开始生产，不直接升级 M6 验证台词。通过后，才考虑把本合同与 v2 蓝图提升为 Working Canon。

### P6：最后决定是否实现 `SIGNAL`

只有真人证明当前四模式、两活动和单话容量可理解、可记忆、可重复生产，才新增第三语法。

---

## 11. 验收门禁

### 11.1 模式本体

- Narrative 有人物欲望、潜台词、物件动作和关系位移。
- Spatial 有方向感、动态要素、非清单推进和身体动作。
- Tactical 有意图、取舍、中段变化和机器人身体性。
- Desk 有比较、预览、承诺和不可重复提交。

### 11.2 跨模式连续性

- 每次主模式切换保留三条连续性中的至少两条。
- 至少一个稳定对象跨三个以上模式可被玩家认出。
- 玩家承诺有立即、冲突、人物和结算四个消费槽。
- 软失败改变局面、人物或责任，不形成小游戏重考墙。

### 11.3 内容与情感

- 玩家先说出人物和事件，再说出系统。
- 机器人用动作表达欲望，不只以故障、拒绝和损坏证明人格。
- 角色反应来自欲望、恐惧、当下物件和关系历史。
- 多玩法选择为角色创造条件，不替角色做完灵魂决定。
- 结算留下一个玩家愿意继续追问的未完成责任。

### 11.4 制作与工程

- ModeScene 不复制输入、存档、台词和永久状态逻辑。
- 正式资产通过稳定 ID 在 establishing / spatial / tactical / desk 之间绑定。
- Bundle 编译、Canon strict、存取、跳过、输入和视觉回归全部通过。
- 验证内容、候选 Canon 和正式 Episode 状态保持分离。

---

## 12. 最终建议

保留现有 `四模式 + 三语法 + SRPG + 事务状态`。它是正确的工程收敛，不应推翻。

下一阶段不要再横向增加玩法名词，也不要继续只补底层状态机。应把生产重点转到：

> **戏剧结、同物异义、模式本体乐趣、稳定对象、玩家承诺、四次消费和人物回收。**

一句最简判断：

> 多玩法不是玩家一话里做了很多不同的事；而是同一件重要的事，逼玩家从不同身体、尺度和责任位置重新理解，并最终为自己的理解付出代价。
