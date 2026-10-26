# A22 馆守 Z south 持盾共享母版｜输入锁

> **RETIRED / DO NOT CONSUME（2026-08-24）：** 本锁使用 CML008 旧视觉并排除 V10X，与 52 号用户限域裁决和 CML130 直接冲突。后续 Section 2 不得读它作正向来源；改读 `c01e02-guardian-z-scoped-source-lock-v1.tsv`。

> Lifecycle: `Section 2 Candidate production only`
>
> Runtime / Godot / Canon: `false`

只允许三项输入：

1. `CML008 Hard locked_current`
   - `.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`
   - SHA-256 `a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521`
   - 只提供馆守 Z 身份、比例、结构、配色与磨损语言。
2. `A17 USER_ACCEPTED_SHIELD_DESIGN_BASE`
   - `docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`
   - SHA-256 `169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305`
   - 提供同一盾的正面、背面、侧缘和握把结构。
3. `A22 BLOCK pose-only guide`
   - `guide/GZ_SOUTH_BLOCK_SINGLE_SUBJECT_GEOMETRY_GUIDE_1024.png`
   - 只提供 Camera V2 south、盾前置、两臂握把链、弓步与 foot pivot 的几何约束。

禁用：A13、A18、A19 失败 raw；A2 旧装甲板；A8 旧身份；V10X `approved=false`；east 运行候选；上一轮三姿势 RGB 失败 raw。禁止镜像 east 伪造 south。

固定输出规格：Camera V2 south `[-40,+24]`；Runtime `256x256 RGBA`；pivot `[128,224]`；footprint `2x2`。生成图只可成为 Candidate 源，不自动获得 Runtime 或 Canon 权威。
