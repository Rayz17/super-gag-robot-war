# C01E02 ENV-A3：Camera V2精确独立Structure样板任务书

状态：`DISPATCHED_ZERO_GENERATION / ONE_STRUCTURE_ONLY / NOT_FINAL_ART`

## 目标

用一栋NW_BLOCK证明新的环境制作方法：不再把旧角度建筑贴进新地图，也不做整屏生成。直接依据Camera V2 `40×24`正交网格构造独立foundation与occluder，验证同一视角、排序和整件半透明。

## 精确约束

- Camera V2地面轴严格为`(40,24)`与`(-40,24)`，斜率`±0.600`、角度`±30.96°`，无透视汇聚。
- NW_BLOCK沿用既有anchor、footprint与HIGH高度上限`90px`；不可改玩法占地。
- `foundation`常显、`occluder`独立；仅occluder在reveal时从`1.00`变`0.34`。
- 只做平面分块、两级硬阴影和少量材质贴片；不做SubViewport、动态光照、逐像素mask、全图重绘或复杂shader。
- 允许从ENV-A1无语义局部裁片取颜色/材质，不允许继承任何旧建筑轮廓、屋顶边或自由透视。

## 必交

- `NW_BLOCK_FOUNDATION_CAMERA_V2_RGBA.png`
- `NW_BLOCK_OCCLUDER_CAMERA_V2_RGBA.png`
- 100% normal、34% reveal、restore三态板。
- A PLAN精确位置单栋重组图，以及新旧视角对照图；标出目标`±30.96°`和实测边。
- 简短readback：anchor、footprint、pivot、height、两轴斜率、alpha、source lineage。

## 门

只有单栋在50%仍像同一张地图、100%无透视漂移、显隐后地基/阻挡仍可读，才允许按同一模板扩六栋。失败即停止该方法；不得用手移、拉伸旧建筑或遮挡掩盖。
