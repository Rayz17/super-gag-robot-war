# R2C actual-frame视觉复核

捕获方式：Godot root viewport `get_texture().get_image()`；不是Pillow、SVG或离线合成。五张均为1280×720，加载既有A4六层地图与identity-free代理，`real_art_loaded=0`。

| 帧 | 目视内容 | 本任务复核 |
|---|---|---|
| `01_A_T2_SOUTH_BRACE` | A下侧7步路线、2×2 endpoint footprint、south箭头、BREAKER仍在公开冲线起点 | 路线与T2 south brace可读 |
| `02_A_T3_FRONT_CONTACT` | A `[20,9]`与BREAKER `[20,11]`、两格接触边、`[20.5,10.5]`socket、recoil/post标记、T4炮线 | 全前缘接触与post差异可读；矩形不重叠 |
| `03_B_T2_EAST_TO_SOUTH` | B上侧路线、T2 east箭头与T3.25 south预览箭头同时存在 | “先护线、后转正”没有被单一final facing压平 |
| `04_B_T3_25_OFFSET_CONTACT` | B `[19,9]`、一格接触边、`[20,10.5]`socket、A `[20,9]`灰色参照、B recoil/post与炮线 | 横向一格差、B仍回到离散`[19,9]`可读 |
| `05_R2_DYNAMIC_BREAKER_BLOCK` | post-A BREAKER `[21,11]` 3×3、A第二轮10步路线、`[20,10]`红色拒绝交叠 | 动态阻挡和preview=execute拒绝语义可读 |

PNG及逐帧状态、摄像机、几何与hash位于`04-actual-frame-manifest.json`。接触帧使用半透明代理以露出footprint、contact edge与socket；A4前景仍按既有深度覆盖局部图例，但核心几何线与anchor标记可辨。

视觉复核结论仅为“证据可交付”，不是制作人视觉接受。正式美术、局部遮挡升级、G2-A.2与G2-B均未开放。

