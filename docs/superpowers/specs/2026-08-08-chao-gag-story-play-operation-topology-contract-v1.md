# 《超GAG机器人大战》剧情—游玩协同与跨话战斗拓扑合同 v1

> Status: `working_method_current`
>
> Date: 2026-08-08
>
> Scope: L4导演板、战斗预案、物理板完成后，完整章纲开始前；并约束后续L4.5、Episode游戏流程解构、关卡、演出与状态账。

## 一、解决什么问题

Episode是番剧叙事和玩家阅读的连载单位，不天然等于一张战棋地图、一场完整战斗或一次Mission Clear。把两者强行一一对应，会产生四类假象：

1. Boss只是倒地或换形，系统却已经发奖励、恢复状态；
2. 下一话明明接在上一秒，敌人、伤势、装备和地图破坏却被重置；
3. 一话里本来有两场性质不同的比赛或行动，却被压成一个含糊关卡；
4. 为了让每话都有“完整一局”，剧情被迫添加不必要敌人、设施和结算。

本合同只建立剧情与玩法之间的结构桥，不替剧情决定人物动机，也不替关卡设计决定数值。

## 二、七种对象

| 对象 | 定义 | 可以跨越什么 | 不自动意味着什么 |
| --- | --- | --- | --- |
| Story beat / Scene | 人物欲望、反击、选择或结果发生的一段戏 | 可落入多个载体 | 不等于可玩段 |
| Episode | 叙事切话单位 | 可切在同一危机中间 | 不等于新任务或结算 |
| Battle Incident / Operation | 世界中同一主要危机或有明确终点的行动 | 可跨多话、多地图、多Encounter | 不要求连续实时操作 |
| Encounter / Play Segment | 玩家连续操作的一段 | 一话可有多个；也可跨话续玩 | 不等于主要危机已结束 |
| Battle Phase | 同一Encounter内的目标、增援、Boss形态或地图状态 | 可在同一地图或无缝换区 | 不刷新世界状态 |
| Checkpoint / Save Resume | 可保存、退出、回顾并继续的位置 | 可位于Episode切点或Phase间 | 不治疗、不发永久奖励、不复活敌人 |
| Mission Clear | Operation主要冲突已经在世界中结束 | 可发生在话中或话末 | Boss逃脱不必然否定Clear，但必须已失去本Operation目标与能力 |

Operation允许在两个Encounter之间出现ADV、整备、短暂休息或时间跳跃。只要同一敌方目标、损伤、资源债和未完成目标仍在，IncidentState就必须继续。

## 三、边界类型

拓扑表使用以下边界，可用分号组合：

- `chapter_entry`
- `operation_start`
- `encounter_start`
- `encounter_complete`
- `phase_transition`
- `episode_cut`
- `checkpoint`
- `save_resume`
- `operational_pause`
- `mission_clear`
- `time_skip`
- `location_change`
- `operation_end`
- `none`

`episode_cut;checkpoint`是最常见的跨话边界。它只允许标题、回顾、暂停和继续。若同时存在`time_skip`或`location_change`，仍须说明哪些状态被保留、哪些变化有故事内原因。

## 四、IncidentState

每个拓扑行使用`state_in -> state_delta -> state_out`。状态至少覆盖：

- 敌方：本体形态、位置、可行动小体、已公开能力、撤退或追击意图；
- 我方：可用单位、驾驶员、伤势、弹药/负荷、离队或增援；
- 装备：盾、武器、外挂、关键道具由谁持有，是否损坏、拆下或归还；
- 地图：道路、建筑、桥梁、平台、火势、坠落物和可用通路；
- 人员：平民、工房人员、驾驶组和伤员位置及风险；
- 目标：当前主目标、次目标、失败风险和剩余时间；
- 资源：只能由故事明确允许的补给、修理和整备改变；
- 时间：连续、短暂停顿或明确跳时。

同一Operation相邻行的`state_out`必须与下一行`state_in`使用同一个状态ID。说明文字可以分散到状态账，但ID不能断。

每行还必须提供：

- `story_unit_ids`：绑定到当前Episode的稳定故事单元ID，例如`C02E04-B02`，让同一话中的多场比赛、事故或转场不会因文字标题相近而串台；
- `carry_from_state`：只在新Operation首行使用，指向更早Operation已经产生的`state_out`；没有跨Operation承接时填写`none`。

因此，赛事已经Mission Clear并不代表事故能重置冠军战伤势。C02事故首行必须承接赛事终态，离港首行必须再承接事故终态。校验器会拒绝不存在的来源、同一Operation内部滥用和非首行承接。

## 五、Story到Play映射

| 模式 | 使用方式 |
| --- | --- |
| `direct_play` | 玩家直接操作故事中的决定性行动 |
| `supported_play` | 人物作出决定，玩家执行路线、站位或代价管理 |
| `observe` | 必须由角色完成、玩家只观看的短动画或ADV |
| `expanded` | 剧情中的一个大动作拆为数个可玩Phase |
| `compressed` | 多个重复或低价值动作压为短战、蒙太奇或一次交互 |
| `optional_echo` | 可选任务回响主题，不改变主线既定结果 |

## 六、玩家代理权限

| 权限 | 玩家能决定 | 玩家不能决定 |
| --- | --- | --- |
| `execution_only` | 如何执行角色已经作出的选择 | 替角色改变动机、关系和不可逆决定 |
| `cost_or_route` | 路线、顺序、损伤、资源和局部救援优先级 | 改写主线胜负和人物核心选择 |
| `authorized_branch` | 剧情已授权的分支结果 | 越过未开放的关系、身份或Canon边界 |

游戏设计若需要更多代理权，必须向剧情层提交问题，不能在关卡脚本中静默替人物决定。

## 七、地图与镜头承载

- 户外战棋默认是可滚动棋盘。镜头或光标接近阈值后滚动，街区、道路、楼房、桥梁和可破坏建筑是地图本体，不是固定小屏外的背景。
- 室内、驾驶舱、狭窄维修通道或封闭竞技场可使用固定图。
- Operation跨地图时使用`location_change`，不因此清除敌我状态。
- 同一地点的破坏态、火灾态、竖直态或坍塌态优先复用一张地图及状态差分，不为每话新建无关地图。

## 八、问题分级与责任

| 类别 | 典型问题 | 首要责任 |
| --- | --- | --- |
| `carrier` | 故事动作没有合适ADV、动画或玩法载体 | 制作人桥接层 |
| `agency` | 玩家替人物作出未授权选择 | 剧情与游戏设计共同退回 |
| `playability` | 目标不清、阶段无操作价值 | 游戏设计 |
| `asset_budget` | 地图、形态或单位需求不可承受 | 制作、演出、美术提出降本案 |
| `story_causality` | 战斗为何发生或为何胜利只能靠玩法文档解释 | 剧情层 |
| `canon_conflict` | 首登、身份、能力、伤亡或Hard Lock冲突 | Canon裁决 |
| `state_parity` | 跨话伤势、敌人、装备、地图和目标不连续 | 制作人桥接层先定位，回到责任层修正 |

剧情/Canon拥有动机、因果、知识、身份与不可逆结果。制作人桥接层拥有Operation边界、多对多映射和IncidentState。游戏设计拥有地图、规则、失败、重试、存档和数值。演出与美术拥有呈现载体与降本回退。后三级都可以报告故事问题，不能偷偷改故事答案。

## 九、生产门

```text
章级对齐与预生产
-> 导演板、战斗预案、物理板
-> story_play_topology
-> 完整章纲
-> 纯剧情Reader
-> 独立游戏流程解构
-> 三层一致性与state parity
```

`story_play_topology`只锁结构，不写回合数、敌军数值、逐格路线或完整台词。其表头由`scripts/check_v35_story_play_topology.py`校验。

正式封存还必须满足：

- `operation_id`、`episode_id`、`story_unit`、`story_unit_ids`、`encounter_id`、`phase_id`、`state_in`、`state_out`和`carry_from_state`均非空；
- `episode_id`属于当前章，例如C04只能填写`C04E*`；
- 每个`story_unit_id`属于本行Episode；跨Operation的`carry_from_state`必须能找到更早、不同Operation的`state_out`；
- 任一行若为`authority=decision_pending`，默认生产校验必须失败，不能解锁完整章纲；
- `--allow-decision-pending`只用于阅读候选表，绝不用于迁移器、`record-stage`或正式封存；
- 既存拓扑文件迁移进story-chain前也必须重新通过相同语义校验，不能仅凭文件存在和哈希盖章。

## 十、迁移规则

已验收Reader若故事连续性成立，只是旧L4.5误把Episode切点写成结算，不重写Reader。新增拓扑表作为制作层裁决，并在后续游戏流程中以它为准。

若修正会改变敌人首次出现、人物动机、伤亡、机体永久损坏、路线分支或已验收故事事实，必须形成用户决策包；用户裁决后从最早受影响故事层失效并重新验收。不能以“仅游戏层增加单位”绕过明确相冲突的Reader事实。
