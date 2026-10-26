# BREAKER Red Beam West｜Call01 失败回执

状态：`FAIL_STOP / candidate_created=false`

- GF 身份：大体 PASS。低伏巨壳、非均匀长叶叠甲、四肢承力保留。
- Camera V2 抬高顶面：PASS；未触边/无环境：PASS。
- 红光：PASS。短促、贴近前端；未烘长束或命中。
- Camera V2 west 极性：**FAIL**。红缝/前端落在左下、尾体抬向右上，实际读成 south `[-40,+24]`，不是 west 所需“前端左上、尾部右下”。
- 额外结构风险：侧面另有一处红缝，存在第二眼/额外解剖风险。
- 技术 raw：`1402×1122 RGB / hasAlpha=false / baked checker`。

因此未执行 Alpha、384×384、pivot `[192,320]`、3×3、100%/50% 深浅底 QA。该 raw 不得作为 west pose 或 Runtime FX 基底。
