# C01E02 G2-A.1-R2 战棋几何消费者校准完成报告

> 状态：`PROXY_IMPLEMENTATION_AND_EVIDENCE_COMPLETE / PRODUCER_GEOMETRY_ACCEPTANCE_GATE / BLOCKED_BY_CONTACT_STAGING_DECISION`
> 范围：仅 G2-A.1-R2 Candidate 校准；不是 G2-B，不是 Runtime 晋级，不是 Canon 变更。

## 结论

77号任务书要求的消费者纠偏和可审证据已完成：四向、route、ghost、facing fan、contact normal 和 force arrow 共用 `A4_ISOMETRIC_40X20` 投影；route 动画改为逐段 facing；1×1、2×2、3×3使用完整 footprint bottom-center、binding pivot/display scale 和 footpoint screen-y z；view-space、camera、pivot 与稀疏 clip 均 fail closed；A4 现有六层以共同 2400×1350 canvas/origin/crop 在 Godot 实际帧中注册。

但当前正式 A 方案仍是东西接触边，与“馆守Z正面承接、BREAKER南向北冲”不闭合。本任务没有覆盖 `golden_slice_profile.json`，而是提交候选影响表并依约停在制作人签字门。

## 逐项验收

| 任务 | 结果 | 证据 | 边界 |
|---|---|---|---|
| R2.1 投影向量统一 | `PASS_MACHINE + ACTUAL_FRAME` | `02-projection-direction-proof.tsv`；`01_DIRECTION_FAN` | 制作人视觉签字待完成 |
| R2.2 路径逐段朝向 | `PASS_MACHINE + ACTUAL_FRAME` | `03-route-segment-facing-proof.tsv`；A 的 east/north 帧；B 的 north/east 帧；failure 机器断言 | `final_facing` 仅 endpoint settle |
| R2.3 多格注册、pivot、z | `PASS_MACHINE + ACTUAL_FRAME` | `04-registration-pivot-z-proof.tsv`；`04_REGISTRATION_OCCLUSION` | 遮挡是 50% fade + outline Candidate，尚待制作人视觉签字 |
| R2.4 view-space 与稀疏 clip | `PASS_MACHINE + ACTUAL_CONSUMER` | `07-view-space-and-sparse-clip-proof.tsv` | 旧 R1 笛卡尔 fixture 只允许显式测试适配 |
| R2.5 A4 六层注册 | `PASS_MACHINE + ACTUAL_FRAME` | `05-a4-layer-registration.json` | 六层仅在测试捕获中只读加载；未写入 m3 runtime 引用 |
| R2.6 接触几何 | `BLOCKED_BY_CONTACT_STAGING_DECISION` | `06-contact-geometry-candidates.tsv`；`05_CONTACT_SOCKET_FORCE` | 候选未进入正式 profile |

## 关键机器回执

- 四向 screen delta：north `[40,-20]`，east `[40,20]`，south `[-40,20]`，west `[-40,-20]`。
- A route segment facings：`east,east,east,north`；endpoint settle `south`。
- B route segment facings：`north,east,east,east,east,north`；endpoint settle `east`。
- failure route segment facings：`east,east,south`；endpoint settle `west`。
- A 当前：`guardian_east_to_breaker_west`，`narrative_front_contact_closed=false`。
- A 候选 `[19,9] + south`：`guardian_south_to_breaker_north`，几何闭合，但增加两段路线并与 B 终点重合。
- B 当前：接触边和 approach 闭合，但馆守Z `east` 为侧身；T3-only `south` 转身可几何闭合，但需制作人决定 interaction-facing 是否可以覆盖 endpoint settle。
- 候选接触实际帧中：馆守Z impact socket = BREAKER target socket = contact flash = road debris = screen `[640,350]`。

## Actual-frame 证据

`08-capture-manifest.json` 记录 7 张 1280×720 Godot root viewport 实际帧，不是 Pillow、SVG 或离线合成：

1. `01_DIRECTION_FAN`：共用 40×20 basis 的四向扇面。
2. `02_ROUTE_EAST_SEGMENT`、`03_ROUTE_NORTH_SEGMENT`：A 方案逐段转向。
3. `04_REGISTRATION_OCCLUSION`：1×1、2×2、3×3 footpoint、z 和屋顶/前景遮挡 Candidate。
4. `05_CONTACT_SOCKET_FORCE`：候选接触 socket、flash、debris、impulse/recoil 同源。
5. `06_ROUTE_B_NORTH_SEGMENT`、`07_ROUTE_B_EAST_SEGMENT`：B 方案逐段转向。

这些帧已完成生成和本任务内的可读性目检，但不代表制作人/用户验收。

## 回归与隔离

- 专用 suite：`PASS`。
- 既有 Golden Slice/R1 直接回归：`11/11 PASS`。
- 全仓 `scripts/godot-test.sh`：`PASS`。
- Canon report/strict、authority check、canon smoke、V35 layered dashboard：全部 `PASS`。
- 正式 profile SHA256 仍为 `28ba689ea08d08201e2c9dbce0de65c7ba085f54181d7b0034bcd298d8d2af28`。
- 默认入口仍为 `res://scenes/startup_router.tscn`。
- 馆守Z/BREAKER 真实美术加载 `0`；`approved_handoffs=[]`；G2-B/Runtime/Canon 均未开放。
- 未执行 `git add`、commit、clean、reset 或 checkout；共享工作树的其他改动保持原状。

## 制作人必须决定的事

1. 在 `06-contact-geometry-candidates.tsv` 中选择或否决 A/B 接触舞台调度；程序不会擅自写入正式 profile。
2. 查看 7 张 actual frame，确认方向、A/B 逐段转向、多格脚点、遮挡、接触和受力是否在同一斜俯战棋世界中可接受。
3. 是否接受“屋顶/前景 50% fade + footpoint outline”作为本轮 G2-A.1-R2 的 Candidate 遮挡策略。

本轮交付到 `producer geometry acceptance gate` 为止。签字前后都不由本任务推定或启动任何下游施工顺序；不派 A9.1-A6 正式像素，不提交 UA91，不做 A9.1-B，不签 exact handoff，不派 G2-B，并等待制作人新的下游任务书。
