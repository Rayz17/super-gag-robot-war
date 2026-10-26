# C01E02 ENV-A6：Camera V2单栋Structure材质试制任务书

状态：`DISPATCHED_ZERO_IMAGEGEN / NW_BLOCK_ONLY / A5_ALPHA_LOCKED / PRODUCER_VISUAL_GATE`

## 上游裁决

制作人已实际查看ENV-A5的50%纯几何与0.34 Proxy QA，并裁决：`PASS_STRUCTURE_HIERARCHY / NOT_FINAL_ART`。本任务只放行`NW_BLOCK`一栋材质试制，不放行其余五栋。

## 冻结项

- A5 `grid_rect=[1,0,7,5]`、canvas=`[480,378]`、pivot=`[240,378]`、front edge=`[80,288]`、visual envelope=`[-160,-90,480,378]`逐字不变。
- Camera V2轴`(40,24)`与`(-40,24)`、角度`±30.9637565°`、无透视汇聚。
- 总高度`82px <= 90px`；低主楼、低东翼、偏置设备间、南侧短檐体块不变。
- A5 foundation与occluder Alpha逐像素锁定；A6只改现有Alpha内RGB，不加新轮廓。
- reveal仍为完整occluder `1.00 -> 0.34 -> 1.00`，foundation始终`1.00`。

## 允许的材质与建筑读法

- 4—7个主要色值块，不依靠高频细节制造“精品感”。
- 屋顶：克制的防水层、exact轴拼缝与一条排水带。
- 立面：连续窗带、明确入口；低东翼可有一块大尺度服务面板。
- 设备间：一组宽百叶，不做密集格栅。
- 最多三处小面积暖色边灯，不出现文字、招牌或新功能语义。
- 只允许低频雨蚀，亮度变化不超过`±8`；禁止照片噪声、重复贴片和旧donor几何。
- 所有结构线只允许`±30.9637565°`或竖直。

## 禁止

- 新Alpha、新檐口、新设备、新轮廓或手工screen offset；
- 动态光、shader、SubViewport、ImageGen；
- 旧ENV-A1建筑、屋顶边、道路白线、排水沟或任何旧视角像素；
- 把Proxy、路线、单位或UI写入交付资产；
- 自动扩其余五栋。

## 必交与停止门

必交：独立foundation/occluder、100%/50% A5-A6对照、Alpha锁定readback、normal/reveal 0.34地图Proxy QA、source lineage、machine report、manifest与全包SHA。

若50%仍首先读作程序模型、材质压过体块、结构线产生非Camera V2角度、Alpha/pivot/grid变化，或0.34地图Proxy不可读，即诚实封存`FAIL_FINAL_QUALITY`并停止。机器PASS只开放制作人单栋实际帧审查，不开放六栋、最终PLAN、Runtime、UA91、G2-B或Canon。
