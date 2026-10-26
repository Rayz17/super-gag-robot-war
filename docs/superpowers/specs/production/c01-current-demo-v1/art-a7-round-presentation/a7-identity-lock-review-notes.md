# A7 共同身份锁板：父制作人审查说明

## 当前状态

- `review_revision=R2`
- 上一版身份门结论：`not_passed`
- `lifecycle=Candidate`
- `runtime_allowed=false`
- `runtime_handoff=none`
- `review_gate=parent_producer_identity_review_pending`
- `u1_ready=false`
- 本轮只执行 41 第 6-7 节；这不是 Cut-in、Atlas、道路、FX、音频或 animatic 的完成回执。

## 审查对象

父制作人本轮只需复核同路径覆写后的 `A7_IDENTITY_LOCK_GUARDIAN_C_BREAKER_BX_2400x1600.png`。R2 已直接重构图形，不以文字替代两项纠偏：

1. 馆守 Z 三视图和四动作统一改为约 `4.2 头身`：宽方肩、厚红胸甲、短粗腿、紧凑深蓝双前臂/拳、银栅格脸；不再使用长手长腿、窄肩的人形比例。
2. 馆守 Z 的双前臂在每个可见角度均完整，机器人右肩保留旧伤，没有提前画成最终报废。
3. BREAKER 三视图和四动作统一改为 B 结构：巨大高背壳、肩壳下前探的独立低位头块、壳外前肢承重、壳下后腿柱体。
4. BREAKER 的单一红缝只画在独立头块中；闭合胸缝另画在头块下方胸板，避免把红缝读成躯干上的嘴。
5. BREAKER 壳面使用 X 的非对称曲面分片与少量柔性接缝，同时保持 B 的高背轮廓，不变成人形黑机、普通四足兽、光滑蜘蛛或眼罩机器人。
6. `18m / 2x2` 与 `近 30m / 3x3` 的同屏比例、`idle/brace/contact/red_charge_only` 身份连续性是否成立。
7. 停止态是否正确：红光只有蓄能、没有发射；墙挂盾仍在墙上并恰有三处旧焦痕。

## 来源与隔离

- 馆守 Z 只引用 `GZ_QSD_A1_direction_board_1920x1080.png` 的 C 方向证据。
- BREAKER 只引用 B 身份板与 X 表面关系板。
- 四张漂移图已按原字节登记为 `rejected_exploration / identity_drift`，没有被裁切、描摹、重着色、放大或拼入本锁板。
- 锁板图由确定性 Pillow 绘制脚本生成；底部只显示三份批准证据的只读缩略图与已核验 SHA。
- `a7-identity-lock-sha256-receipt.tsv` 是 R2 送审字节的评审候选指纹，不是最终封存 hash 或完成回执。

## 声明边界

本锁板只申请父制作人的身份门审查。未获得明确通过前，不得据此派生 Cut-in、Atlas、道路、FX、音频、animatic 或 U1 媒体，不得宣称 `U1 ready`、`R1 ready`、可交接或 Runtime 可用。
