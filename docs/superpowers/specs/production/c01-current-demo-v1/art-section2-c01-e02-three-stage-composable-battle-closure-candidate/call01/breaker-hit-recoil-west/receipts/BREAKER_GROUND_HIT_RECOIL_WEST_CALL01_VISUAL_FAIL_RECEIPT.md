# BREAKER Hit Recoil West｜Call01 失败回执

状态：`FAIL_STOP / candidate_created=false`

- GF 身份：基本 PASS。低伏巨壳、非均匀长叶叠甲、单一低嵌红缝、完整四肢保留；四肢略偏标准机械化。
- Camera V2 抬高顶面：PASS；壳完整/无 beam：PASS；未触边：PASS。
- Camera V2 west 极性：**FAIL**。前端在左下、尾部在右上，更接近 south，不是 west 的左上→右下。
- hit_recoil 第一读法：**FAIL**。更像稳定 idle/brace；四足稳固，缺少明确后仰、失衡、四肢压缩与长叶甲错动。
- 技术 raw：`1254×1254 RGB / hasAlpha=false / baked checker`。

因此未执行 Alpha、384×384、pivot `[192,320]`、3×3、100%/50% 深浅底 QA。未把程序 root south 位移误画入 Sprite，也未用 B 或旧姿态补位。
