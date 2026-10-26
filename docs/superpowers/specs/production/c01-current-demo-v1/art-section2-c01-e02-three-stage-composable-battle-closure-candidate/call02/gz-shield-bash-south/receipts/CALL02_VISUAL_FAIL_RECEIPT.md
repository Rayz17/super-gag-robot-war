# GZ_V10X_E02_SHIELD_BASH_SOUTH｜Call02 视觉失败回执

状态：`FAIL_STOP / candidate_created=false`  
晋级：`user=false / texture_load=false / runtime=false / default=false / canon=false`

## 像素硬门

- 单一 A17 盾正面：PASS。厚边、中央脊、三道旧白痕及第四道赤红热痕存在；无第二盾、弹孔或完整盾背。
- 双腿完整、无翼、无背包、四边未裁：PASS。
- 盾正面可见肢体：**FAIL**。至少可见 `hand=1 / wrist=1 / forearm=1 / handle=0`；上缘中央手甲/腕/前臂压在敌方可见盾正面。
- 双臂分别进入两个盾背握把区：**FAIL**。一臂已在正面，另一臂只在右缘含混，无法成立两个独立、非交叉的隐藏握持关系。
- Camera V2 south：**FAIL**。仍读成戏剧化前 3/4 透视，未稳定保持平行高斜正交与左下 `[-40,+24]` 主轴。
- 盾心离开胸中线：PASS；规定的 15–25° 动态倾斜：**FAIL**，目测约 10–12°。
- 横拍第一读法：**FAIL**。仍接近顶盾推进/格挡，宽面横向领击、肩髋反扭与驱动/锚定关系不足。
- V10X 严格身份：**FAIL**。头冠、银栅脸及蓝红金可辨，但胸 X/圆核与双臂接触结构被遮挡或漂移，不能完成严格追认。
- 透明技术门：**FAIL**。实际 `1254×1254 PNG / RGB / hasAlpha=false`，棋盘已烘入。

依据派工硬门，任何一项已经足以停止。本轮没有 Alpha 抢救、没有 256×256、没有 pivot `[128,224]` 或 2×2 注册、没有深浅底 QA，也没有第二次调用或旧姿态补位。

最终裁决：`CALL02_VISUAL_FAIL_FRONT_LIMB_CAMERA_BASH_AND_RGB_CHECKER / NO_CANDIDATE_PROMOTION`
