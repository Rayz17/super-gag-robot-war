# C01E02 A6 角色通讯 UI 用户裁决卡

> Package: `C01CDV1_A6_CHARACTER_COMMS_UI_R05_CANDIDATE`
>
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`
>
> 当前状态：待 U1 用户逐项批准，未产生 exact handoff。

## 先看什么

1. `boards/jicun-state-board-1280x720.png`
2. `boards/doudeng-approved-layout-board-1280x720.png`
3. `boards/qihai-state-board-1280x720.png` 与 `simulations/jicun-qihai-remote-presence-1280x720.png`
4. `boards/old-guardian-state-board-1280x720.png`
5. 三张 `simulations/*.png` 与 `boards/layout-safe-area-review-board-1280x720.png`

## 七海消费者定性

七海是规划侧栏 `presence_cards` 的远程状态卡消费者，**不是通讯台词或对话弹窗**。模拟图使用闭口的 `decision`，程序安全区对应姓名“七海”、来源“代哥东区封存中心”和状态“本人停机令已撤回”；`line_text` 为空，卡片无按钮、无目标线、无行动点、无命令或炮火权。

## 核心候选与 SHA-256

| 内容 | 文件 | SHA-256 |
| --- | --- | --- |
| 纪存三态 atlas | `assets/atlases/r05-portrait-jicun-states-2304x768.png` | `d6ec72d6976f532cfde707902231de3df5633d17aca66116710e4fa72b67622e` |
| 七海远程三态 atlas | `assets/atlases/r05-portrait-qihai-remote-states-2304x768.png` | `477f0873c6bdda04dde1312c49d57aaf53b1f2f6337023269290c5f87edbf67f` |
| 旧守护者三态 atlas | `assets/atlases/r05-comms-old-guardian-states-3072x768.png` | `41dd29862ed0a2be873dbaac580c4269c4ad3161156834021812c5a0b1a7e4be` |
| 纪存–兜灯模拟 | `simulations/jicun-doudeng-local-1280x720.png` | `43b75fb10ac8fc49bf961f3bd19d2e7d5cbf74c6986c49b61b4f03fc8f3b1f35` |
| 纪存–七海 presence 模拟 | `simulations/jicun-qihai-remote-presence-1280x720.png` | `7bf09d221790e07c94b5f475f738db49519d4779d3897df8eac49efd05b3df9d` |
| 纪存–旧守护者模拟 | `simulations/jicun-old-guardian-machine-1280x720.png` | `90d2ad3054830bcf9f4b44e513f40c8f3e34d6aaed1c85f47f3cec2e26875ec2` |
| 兜灯适配板 | `boards/doudeng-approved-layout-board-1280x720.png` | `9eb780435ac52d2d2c3f99d57001e757222f1a7403ab5efdaf006c523174a0a6` |

## 请逐项回答

1. 纪存是否像在读城市、人员和路线，而不是统帅或全知主角？
2. 既有兜灯 OBSERVE/TENSE 在新布局中是否一眼能读出工艺与机况责任？若不适配，是否另开“新作兜灯”任务？
3. 七海是否保持远程、克制和承担撤令后果？`decision` 的闭口、坚定眼神是否消除“正在发布战场指令”的误读，并且状态卡而非通讯台词的消费方式是否清楚？
4. 旧守护者是否清楚是馆守 Z 同一主体，而不是独立 AI、人类头像或虚拟助手？
5. 四个信息位置在 1280×720 实际占位中是否可读、有个性，且不遮挡战术地图与长文安全区？
6. 请指定批准作为 R0.5 Demo 派生来源的**具体文件与 SHA-256**；未点名的文件继续保持 Candidate。

建议回复格式：

```text
纪存：通过/修改……；
兜灯：适配通过/另开新作任务；
七海：闭口 decision 通过/修改……，确认为 presence card 而非通讯台词；
旧守护者：通过/修改……；
720p 布局：通过/修改……；
批准派生来源：<文件> / <SHA-256>……
```

本卡不自动授权 Godot 导入、Runtime promotion、Canon promotion 或 exact handoff。
