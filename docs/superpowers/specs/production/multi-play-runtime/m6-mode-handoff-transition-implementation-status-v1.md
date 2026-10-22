# 《超GAG机器人大战》多玩法模式交接转场实现状态 v1

> 日期：2026-07-15  
> 状态：`candidate_presentation_runtime_validated`。  
> 上游：`2026-07-14-chao-gag-multi-play-implementation-blueprint-v2.md`。  
> Canon 边界：本实现只证明模式交接可表达、可阻断误输入并可由内容包检查；不证明 M6 剧情已通过真人理解门禁，不提升 C02E03，不解冻 V35.10。

## 1. 为什么需要这一层

四种主模式已经能切换，但“能换场景”不等于玩家理解为什么换。若 Narrative、Spatial、Tactical 与 Desk 只在完成按钮后立刻替换，玩家会记住五个界面，而不是同一件事如何逐步变成身体问题、战场压力、人物后果和责任记录。

因此模式交接必须同时回答：

1. 现在在哪里、是什么时间。
2. 刚发生的事实为什么让旧玩法权能结束。
3. 玩家进入下一段后马上要承担什么。
4. 转场期间旧场景和新场景都不能偷跑输入、计时或全局快捷键。

## 2. EpisodeGraph 合同

需要正式交接的节点声明 `transition`：

```json
{
  "transition_id": "M6-TR-03-RING-FLIPS",
  "kind": "pressure_escalation",
  "eyebrow": "直播灯亮，仓库顶先塌了",
  "title": "擂台翻成救援现场",
  "location": "旧件市 · 临时擂台与后仓",
  "time_label": "开播前四分钟",
  "cause": "维修方案刚落到旧拳王身上，直播吊架便压穿后仓。",
  "handoff": "先救人，再决定那一拳该不该打完。",
  "duration": 1.35,
  "fade_seconds": 0.48
}
```

玩家画面不会显示 `NARRATIVE -> TACTICAL`、Graph 节点名或控制器术语。`cause` 是上一段已经成立的具体事实，`handoff` 是下一段的具体责任，不是玩法教程。

Manifest 可声明 `transition_contract = required`。构建器会检查每个节点的 ID、类型、标题、地点、因果、责任、时长范围与全图唯一性；缺失或重复直接阻断 bundle。

## 3. 运行时生命周期

```text
目标场景与合同预检
  -> ModeTransitionDirector 覆盖旧画面
  -> 旧 Mode suspend / exit / 清除输入 owner
  -> 新 Mode prepare / enter
  -> 新 Mode suspend 在覆盖层后方
  -> blocking transition input context
  -> 转场完成或跳过
  -> 精确恢复新 Mode snapshot 与主输入 context
```

`InputRouter.push_blocking_context()` 在转场期间阻断笔记本、手动存档、确认、移动和其他全局输入，只保留显式 `skip_hold`。进入和退出 blocking context 都会清空按住的方向键与摇杆状态，旧场景的持续移动不会在淡出后泄漏到新场景。保存系统若在稳定边界自动保存，会读取转场前冻结的新模式快照，不会为了取快照提前激活场景。

无头测试将转场即时完成，使逻辑回归不依赖真实秒数；窗口运行仍播放完整覆盖和淡出。演出跳过与完整播放得到相同节点、状态和输入上下文。

## 4. M6 五次交接

| ID | 交接事实 | 下一责任 |
| --- | --- | --- |
| `M6-TR-01-LIVE-COUNTDOWN` | 直播要求零瑕疵复刻，右拳却等影子 | 先听关节，不替它补快 |
| `M6-TR-02-BODY-BEFORE-POSE` | 迟疑藏在身体与旧伤中 | 检查、分配零件、校准时机 |
| `M6-TR-03-RING-FLIPS` | 直播吊架压穿后仓，多目标同时受困 | 把维修后果带入救援战 |
| `M6-TR-04-HELD-PUNCH` | 旧拳王停拳接住工人，没有完成冠军动作 | 让人物判断这是失手还是选择 |
| `M6-TR-05-WHAT-REMAINS` | 警报结束，损伤、分歧和责任仍在 | 写回同一份结算记录 |

这五次不是五段独立旁白，而是 EpisodeGraph 的权能交接边界。它们与节点一起进入 M6 自包含 bundle。

## 5. 自动与像素证据

- `multi_play_mode_transition_smoke_test.gd`：文字投影、一次恢复、输入上下文释放、审计快照。
- `multi_play_input_intent_smoke_test.gd`：转场期间阻断笔记本、手动存档和场景确认，只保留跳过。
- `multi_play_timing_m6_smoke_test.gd`：完整五节点依次消费五个转场 ID，并在每次完成后恢复正确模式输入。
- `multi_play_content_compiler_smoke_test.gd`：M6 五个 ID 唯一；Manifest 要求转场时，缺失节点会构建失败。
- `windows_export_resource_validation.gd`：导出包内必须存在转场运行时，且 bundle 必须包含五个闭合转场。
- 1280×720 实际 GL 渲染：`outputs/multi-play-transition-validation/m6-03-ring-flips-transition.png`，中文、地点时间、因果与责任无溢出或遮挡。

## 6. 尚未证明

本层没有证明玩家会认真阅读转场，也没有证明五次转场的时长、措辞和频率恰当。真人盲测仍需回答：

- 玩家能否用自己的话复述“为什么从维修进入战斗”。
- 玩家首先记住的是停拳与救人，还是一张黑底文字卡。
- 连续五次交接是否打断节奏，哪些应缩成镜头内转场。
- 手柄跳过、Windows 字体与超宽屏布局是否自然。

因此它是可复用的呈现合同，不是正式内容通过回执，也不能替代角色演出、场景动画、音乐和机体动作。
