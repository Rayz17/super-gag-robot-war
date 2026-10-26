# InputEvent、连续 phase、CONTACT 与 socket 证明

## A / B 屏幕输入链

两条分支均从专用非默认 Scene 进入 `Control._input`，再由公开 Session API 作者化；driver 没有直调 Session。

- A：mouse 1 / keyboard 5 / screen 6，策略 A，`commit_count=1`。
- B：joy 14 / screen 14，策略 B，`commit_count=1`。
- B 证据从 B 选策后的公开 trace 起点独立收集，不携带默认 A 启动帧。

外部 validator 不信任 `valid/PASS`，直接将 raw trace 按“相邻 phase 发生变化”压缩：A / B 分别精确等于各18相权威序列，并在 T5 后回到 `PLAN`。每相 6 主体的 state / facing / frame / logical clip / physical clip / alias signature / fps-or-hold / loop 均与锁定 matrix + continuity 重算相等。

## CONTACT 几何

| 分支 | T3 | 共享 impact world | impact screen | BREAKER post | T4 side world | T4 canonical screen |
|---|---:|---:|---:|---:|---:|---:|
| A | 3.00 | `[20.5,10.5]` | `[640,350]` | `[21,11]` | `[24,12.5]` | `[700,460]` |
| B | 3.25 | `[20,10.5]` | `[640,350]` | `[21,10]` | `[24,11.5]` | `[760,450]` |

两分支的 impact 投影误差均小于 0.001 px；T4 side 按 Task98 canonical zoom=1 独立计算，不套动态 zoom。Task98 socket 仍为 provisional，没有为过测强行把 GZ impact / BREAKER target 重合到共享点。

## socket

4 个 base / 6 个 actor 每体恰好 5 个 socket：`body / impact / shield / target / weapon`。local offset 逐项等于 Task98 contract，screen 位置由 `footpoint + local * display_scale` 重算，误差门为 0.5 px。

权威证据：[actual-input-frame-manifest.json](receipts/actual-input-frame-manifest.json)、[machine-validation.json](receipts/machine-validation.json)、[13-task105-actual-input-capture.log](logs/13-task105-actual-input-capture.log)。
