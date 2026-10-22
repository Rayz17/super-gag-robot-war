# M6 多玩法体验合同构建门禁实现状态 v1

> 日期：2026-07-15  
> 状态：`candidate_experience_structure_validated_capacity_pending`  
> 适用：多玩法 Episode 内容包、`EpisodeBundleCompiler`、M6 旧件市运行验证  
> 上游：`2026-07-15-chao-gag-multi-play-experience-production-contract-v1.md`、`multi_play_episode_knot_schema_v0_1.tsv`  
> Canon 边界：不把 M6 提升为正式 C02E03，不解冻 V35.10，不提前实现 `SIGNAL`。

---

## 1. 本轮结论

体验生产合同 P4 已进入实际构建链，不再只是文档要求。

`EpisodeBundleCompiler` 现在能阻断：

1. 缺失或不完整的 `EpisodeKnot`。
2. 主模式切换少于两条连续性，或对象连续性引用未知稳定对象。
3. 戏剧对象没有跨至少三个模式的具名锚点。
4. 玩家承诺没有立即、冲突、人物、结算四个可见消费槽。
5. `InteractionOffer` 没有显式重复策略、结果合同或失败继续路径。
6. 未使用玩法层没有戏剧上的 `skip_reason`。
7. 具名机体没有通过可验证动作表达 `machine_claim`。
8. 容量档缺少完成回执、回执不属于本 Episode，或真实时长落在档位之外。

M6 当前结果为：

```text
experience structure: pass
capacity declaration: standard / 35-60 minutes
capacity receipt: pending_external
formal production gate: not passed
```

这意味着构建器已经能检查容量，但 M6 没有真人 35-60 分钟完成回执，不能宣称达到正式单话容量。

## 2. 新增共享组件

### 2.1 `ExperienceContractValidator`

路径：`game-godot/scripts/core/content/experience_contract_validator.gd`

职责：

- 对正式状态 `working_canon / production` 强制要求体验合同。
- 允许旧候选包暂不迁移；显式设置 `experience_contract_required=true` 的候选包立即受阻断式门禁约束。
- 验证戏剧结、人物主张、机体主张、玩家承诺、不可逆成本、下一债务和验收问题。
- 读取 Graph、活动、战斗、Desk 和稳定对象，而不是只验证 manifest 文本非空。
- 把结构通过与容量回执通过分开报告。

### 2.2 `ConsumptionLedgerValidator`

路径：`game-godot/scripts/core/content/consumption_ledger_validator.gd`

四个槽位必须分别指向真实消费者：

| 槽位 | 允许的主要消费者 | M6 实例 |
| --- | --- | --- |
| `immediate` | StableObject 或当前节点 | 旧拳王右拳身体状态 |
| `conflict` | Tactical 节点或 Battle | 擂台翻仓库战 |
| `character` | Narrative 节点 | 纪存与唐胶战后反应 |
| `settlement` | Desk 节点或承诺组 | 先修右拳 / 先补后仓 |

每个槽还必须提供 `visible_evidence`。仅写一个 flag、分数或内部 ID 不算可见消费。

## 3. M6 EpisodeKnot

M6 manifest 现在声明：

- 戏剧对象：`OBJ_M6_RIGHT_GLOVE`。
- 问题：修好一台机器人，是否也包括保留它不肯完成的动作。
- 唐胶主张：维修先听懂承力，不能为直播磨平旧伤和迟疑。
- 纪存主张：保留原速，使以后的人能分辨故障、旧伤和机器停手。
- 机器主张：旧拳王放弃冠军复活镜头，以没打完的一拳接住工人。
- 玩家承诺：`COMMIT_M6_REPAIR_WITHOUT_ERASING_DELAY`。
- 不可逆成本：右拳与后仓至少一项被推迟，直播原计划无法成立。
- 下一债务：右拳复查或后仓修复积压必须在返场时消费。

两个 Desk 方向共用同一承诺组：

1. 原速入主档，先修右拳，后仓继续封闭。
2. 原速留母带，先补后仓，右拳继续限载。

两项都有具体成本和下一责任，不存在无代价的正确答案。

## 4. 转场连续性

M6 的四次非开场模式切换都登记对象、动作、责任三类证据：

| 进入节点 | 对象证据 | 动作证据 | 责任证据 |
| --- | --- | --- | --- |
| Workshop | 右拳、原速录像 | 开场决定先听身体 | 纪存、唐胶 |
| Tactical | 右拳、仓门、录像 | 维修复合事务 | 纪存、唐胶、旧拳王 |
| Reaction | 右拳、录像 | 战果、停拳动作 Cue | 旧拳王、纪存、唐胶 |
| Desk | 右拳、录像、仓门 | 人物反应、战果 | 纪存、唐胶、下一债务 |

编译器要求每次至少两类，并检查对象 ID 必须来自 Graph 稳定对象。开场节点没有上一模式，因此不伪造连续性。

## 5. 同物跨模式锚点

戏剧对象不能只在清单里出现。M6 已登记：

### 右拳护具

- Narrative：纪存把影子录像调回原速的开场 beat。
- Spatial：`inspect_right_glove`。
- Tactical：`BIND_M6_RIGHT_GLOVE_TO_FIST`。
- Reaction：停拳后的具名人物场。
- Desk：`EV_M6_RIGHT_FIST_BODY`。

### 原速录像

- Narrative：原速观察 beat。
- Spatial：`inspect_shadow_tape`。
- Tactical：影子陪练与证据目标 binding。
- Desk：`EV_M6_ORIGINAL_SPEED`。

每项必须覆盖至少三个模式，且 anchor 必须在相应节点、Offer、Battle binding 或 Desk 卡片中真实存在。

## 6. InteractionOffer 失败继续

六个 M6 Offer 均新增：

- 显式 `repeat_policy`。
- 指向同一 StableObject 的 `outcome_contract`。
- `failure_continuation.policy`。
- 玩家可读的 `player_feedback`。

典型规则：

- 直播终端未解锁时引导回原速录像，不重置已调查状态。
- 零件盘未解锁时明确缺的是身体证据还是现场证据，可任选对象继续，不要求搜齐热点。
- 录像允许短回看，但不重复提交事实。
- 失败或锁定状态都留在 Spatial 中，不形成重考墙。

## 7. 机体主张动作

战斗定义新增 `machine_claim_cues`。M6 的 `CUE_M6_OLD_BOXER_HOLD_PUNCH` 必须引用真实单位和武器：

```text
old_boxer_king / missed_beat_guard
```

其玩家可见动作是旧拳王停拳接住工人。编译器会阻断未知单位、未知武器、重复 Cue 或没有可见动作的机体主张，避免 `machine_claim` 退化成主题标语。

## 8. 容量回执门禁

容量档：

- `compact`：22-35 分钟。
- `standard`：35-60 分钟。
- `major`：60-90 分钟。

当 `capacity_evidence.status=validated`：

1. 至少一个回执文件必须存在。
2. `episode_id` 必须一致。
3. 回执状态必须为 `completed`。
4. `duration_ms` 必须落入声明档位。
5. 回执哈希进入 deterministic bundle 的资源索引与源指纹，但完整私人输入数据不嵌入 bundle。

候选验证包可使用 `pending_external` 并得到显式 warning；正式状态使用 pending 会构建失败。

## 9. 自动验证

专项内容编译测试覆盖：

- M6 结构合同通过但容量待验。
- 删除 Tactical 转场连续性后拒绝。
- 删除人物消费槽后拒绝。
- 删除 Offer 失败继续路径后拒绝。
- 40 分钟完成回执通过 `standard`。
- 3 分钟回执不能冒充 `standard`。
- `production` 状态使用 pending 容量证据时拒绝。
- 容量回执进入 bundle 资源指纹。

本轮完整 `scripts/godot-test.sh` 34 项全部通过，覆盖旧 Demo、章节流程、探索、对话、战斗、存档、M1-M6、输入、内容编译、转场和共享演出壳。

## 10. 仍未完成

1. M6 没有外部真人容量回执，`capacity_receipt_validated=false`。
2. 验收问题尚未由真人回答，结构通过不能证明故事清楚、人物真实或情感成立。
3. P2 候选生产层已经补齐三房间、Portal、返回点、动态唐胶和多轮 NarrativeOverlay；正式地图分层、碰撞、行走 Sprite 与真人理解仍未完成。
4. P3 已完成旧拳王候选地图图、Pose、Cut-in、两项武器和状态驱动救援演出；P3b 已补齐九实体 A 档地图识别，正式 Sprite、动作资产、音效和真人可读性仍未完成。
5. 尚未选择一话通过 Pressure Board 与 Reader 审查的正式 Episode 做 P5 生产验收。
6. Windows 真机和实体手柄外部回执仍为空。

## 11. 下一步

P4 代码与候选正例已经完成。下一轮不再增加玩法语法，按以下顺序推进：

1. 补 Tactical 正式机体演出，使同物连续性通过画面而不是标签成立。
2. 为 Spatial LocationScene 补正式地图分层、碰撞和场内角色步行动画。
3. 让真人完整游玩 M6，取得时长和五个普通语言问题的回答。
4. 选一话正式 Episode 进入 P5，从可读故事、Pressure Board 和资产计划开始生产。

在 P5 和真人门禁通过前，M6、体验合同与 P1-P4 实现均保持 Candidate，不升级为全项目 Working Canon。
