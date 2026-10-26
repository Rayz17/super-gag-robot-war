# C01E02 ENV-A5：Camera V2单栋Structure轮廓丰富化试制任务书

状态：`DISPATCHED_ZERO_IMAGEGEN / NW_BLOCK_ONLY / PURE_GEOMETRY / PRODUCER_VISUAL_GATE`

## 目标

只重做`NW_BLOCK`一栋纯色几何Candidate，用“低主楼 + 偏置设备间 + 一侧短檐”解决ENV-A4在50%仍读作单一程序盒体的问题。禁止材质化，禁止扩六栋。

## 冻结权威

- Camera V2：轴`(40,24)`与`(-40,24)`，斜率`±0.600`、角度`±30.9637565°`，无透视汇聚。
- `grid_rect=[1,0,7,5]`。
- local canvas=`[480,378]`，pivot=`[240,378]`。
- front edge raw=`[80,288]`。
- visual envelope raw=`[-160,-90,480,378]`。
- world height class=`HIGH`，总高度不得超过`90px`。
- Task121 foundation像素、Alpha、canvas与pivot逐字不变；玩法阻挡、reveal cells、排序责任不变。
- 只允许重写occluder Alpha；新非零像素不得越出既有visual envelope。
- reveal仅改变完整occluder：`1.00 -> 0.34 -> 1.00`；foundation始终`1.00`。

## 唯一结构方案

- 低主楼：低于原90px整块盒体，保持明确的Camera V2屋顶与两立面。
- 偏置设备间：作为主楼屋顶上的第二级体块，偏离中心，合计总高仍小于等于90px。
- 一侧短檐：只沿Camera V2 exact轴生成，位于原visual envelope内，不形成新玩法占地。
- 允许主楼与低侧翼形成一次轮廓退让；不得增加文字、招牌、材质纹理、新功能语义、动态光影、shader或SubViewport。

## 必交

- 独立`NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png`与`NW_BLOCK_OCCLUDER_CAMERA_V2_ENRICHED_RGBA.png`。
- 100%与50%新旧结构对照。
- 新旧occluder Alpha差分图与visual-envelope overlay。
- normal 1.00、reveal 0.34、restore 1.00三态板。
- 后方单位／路线Proxy在normal与reveal中的可读性QA；Proxy只用于QA，不写入资产。
- 机器readback、source lineage、asset manifest与全包SHA。

## 制作人停止门

- 50%仍首先读作单一矩形程序盒；
- 必须依靠材质才能解释退台、设备间或短檐；
- 任一主边偏离`±30.9637565°`或竖直；
- grid、pivot、front edge、foundation、玩法占地或reveal责任变化；
- 总高度超过90px或新Alpha越出visual envelope；
- 0.34后单位／路线仍不可读，或restore不等于normal。

任一失败即诚实封存`FAIL_FINAL_QUALITY`并停止。机器PASS只开放制作人实际帧审查，不开放材质、六栋、最终PLAN、Runtime、UA91、G2-B或Canon。
