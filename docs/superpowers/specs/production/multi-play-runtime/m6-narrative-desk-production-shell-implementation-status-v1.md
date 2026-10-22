# 《超GAG机器人大战》M6 Narrative / Desk 共享生产壳实现状态 v1

> 日期：2026-07-15  
> 状态：`candidate_production_shell_validated`。  
> 上游：`2026-07-15-chao-gag-multi-play-experience-production-contract-v1.md` P1。  
> Canon 边界：只把 M6 迁入可复用演出与结算壳；M6 仍为 `runtime_validation_only`，新背景和既有角色设定板只是候选运行资产，不提升 C02E03、不形成正式台本或美术锁、不解冻 V35.10。

## 1. 这次解决什么

M1-M6 已经证明四模式能因果流转，但 M6 的开场、战后反应和 Desk 原先仍接近验证页面：人物、场景和选择缺少共同演出语法，Desk 只是读摘要后确认。体验生产合同 P1 因此要求先完成两个共享壳，再继续扩展玩法名词。

本轮实现：

- `ChaoGagNarrativeDirector`：统一背景、左右人物、说话者高亮、广播来源、舞台动作、对白节拍、选择、进度、跳过和精确恢复。
- `ChaoGagDeskWorkbench`：把战后结果投影为证据卡，允许比较两种处理方向，先预览“现在改变 / 仍然欠着 / 下次处理”，再二次确认一次提交。
- `NarrativeModeScene` 和 M6 战后反应共用同一个导演，不各自复制翻页状态机。
- `DeskModeScene` 成为主动承诺节点；纪存档案终端仍是只读覆盖层，两者不再互相冒充。

## 2. M6 的五段权能链

```text
NARRATIVE
  看见直播怎样把“传奇复活”压到一具旧身体上
SPATIAL + CONSTRAINT + TIMING
  亲手检查并决定有限零件与动作反馈如何分配
TACTICAL
  同一具身体和同一组修理结果进入擂台翻仓库救援
NARRATIVE REACTION
  唐胶先从轴温、急停和工单说话；纪存保留原速，不替停拳制造胜利
DESK
  在右拳修复和后仓通行之间承担一个优先级，并留下另一项未结责任
```

Desk 的两项决定都保留原速记录，但对象、关系状态、机体条件和下一笔债不同。它不是好坏选项，也不是领取结算奖励。

## 3. 数据合同

### 3.1 DialogueBeat

M6 对白行现在可声明：

- `beat_id`
- `actor_id`
- `speaker`
- `source_kind`
- `stage_action`
- `text`
- `choices[]`

运行时按 `actor_id` 找到角色侧位和立绘；广播可以没有人物立绘但保留来源标记。选择第一次确认只提交当前回应，不跳过本节拍；下一次确认才继续。

### 3.2 Desk commitment

每个承诺方向可声明：

- 玩家可读标题、说明、立即结果、代价与下一责任。
- `resolution`。
- `facts`、`entity_changes`、`authority_changes`、`relationship_edges`、`promises_and_debts`、`resource_changes`。
- `player_summary`。

证据卡可从静态事实、`world_fact` 或指定活动的 `score_band` 动态读取状态。内部事务 ID、Patch ID 和 debt ID 不直接显示给玩家。

### 3.3 保存与幂等

Narrative 快照保存当前节拍、选择游标和已提交回应。Desk 快照保存处理方向、是否正在预览和是否已经提交。取消只退出预览，不清空玩家选择；提交后不能再次结算。

## 4. 候选运行资产

M6 现在接入：

- 旧件市维修棚背景。
- 擂台坍塌后的停拳现场背景。
- 临时清点桌背景。
- 纪存既有角色头像。
- 唐胶当前锁定设定板中的青年男性修复师形象，运行时只裁切完整上半身，不再放大低分辨率头像格。

这些资产用于验证构图、可读性和对象连续性。它们没有自动成为正式 C02 美术；正式生产仍需角色/场景资产 brief、分层、表情差分和人工美术验收。

## 5. 内容构建闭包

M6 manifest 现在声明五项 presentation asset。`EpisodeBundleCompiler` 会扫描：

- `presentation.background`
- `presentation.cast[].portrait_path`
- `workbench.background`

未在 manifest 声明、文件不存在或引用未闭合时构建失败。二进制资产字节进入确定性源指纹；M6 bundle 资源索引由三项玩法资源扩为八项：两项活动、一项战斗、三张背景和两张人物图。

## 6. 自动与像素证据

新增 `multi_play_presentation_shell_smoke_test.gd`，验证：

- 选择导航、选择提交不跳节拍、选择状态存取和末尾关闭。
- Desk 动态读取活动结果、方向切换、首次确认预览、取消、恢复、二次确认和一次性提交。

既有 M6 五节点测试继续验证五次事务与完整因果链。Windows 导出资源验收已增加共享壳、两个 ModeScene、三张背景和两张人物图，并要求 bundle 的 presentation 引用合同通过。

像素证据输出在：

- `outputs/multi-play-presentation-validation/01-m6-narrative-intro.png`
- `outputs/multi-play-presentation-validation/02-m6-character-reaction.png`
- `outputs/multi-play-presentation-validation/03-m6-desk-commitment.png`

三张图只证明 1280×720 下没有明显重叠、人物焦点和责任层级可读，不替代真人首玩、角色魅力或正式美术门禁。

## 7. 仍未完成

1. Spatial 稳定对象、`InteractionOffer`、房间切换、返回点、动态唐胶和多轮 NarrativeOverlay 已由后续 P2/P3 与 Spatial 生产层实现；正式地图分层、碰撞和场内步行动画仍未完成。
2. Tactical 已消费活动 Patch并完成同物跨尺度映射；旧拳王候选地图图、标志 Pose、唐胶 Cut-in、两项武器和 controlled rescue 已接入，P3b 也为其余八个实体补了 A 档地图轮廓；正式机体 Sprite、动作与音效资产仍未生产。
3. M6 台词和运行资产没有经过正式 C02 Pressure Board、Reader、台本和美术生产验收。
4. Windows 真机、实体手柄和外部真人盲测仍为空。
5. `SIGNAL` 继续关闭，不能用新活动语法绕开当前生产问题。

## 8. 下一步

P1 在候选 M6 上已经实现；P2 的房间/NPC/Overlay、P3 的同物战术映射与候选机体演出、P3b 的九实体地图识别层、P4 的体验结构门禁也已分别由对应状态文档接续验证。下一步补正式空间与机体 Sprite/动作/音效资产，并取得真人容量/理解回执。正式内容生产仍应选择通过 Pressure Board 与 Reader 审查的 Episode，不能把 M6 验证文本直接加厚后冒充正式剧情。
