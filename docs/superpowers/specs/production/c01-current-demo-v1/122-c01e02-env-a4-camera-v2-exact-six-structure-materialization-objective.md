# C01E02 ENV-A4：Camera V2六栋独立Structure锁几何材质化任务书

状态：`DISPATCHED_ZERO_IMAGEGEN / ALPHA_LOCKED / ASSET_ONLY / NOT_FINAL_PLAN`

## 目标

把Task121六栋Camera V2精确几何骨架材质化为可供制作人审看的精品Candidate。不得再画轮廓、改角度或改变玩法占地。

## 冻结项

- Camera V2轴为`(40,24)`与`(-40,24)`，斜率`±0.600`、角度`±30.96°`。
- 六栋`grid_rect / local canvas / pivot / front edge / 90-72-54px高度`逐字继承Task121 readback。
- 每张输出Alpha必须与对应Task121骨架逐像素一致；不得让管线、雨棚、阴影或装饰越出原Alpha。
- 每栋只交同canvas、同pivot的`foundation + occluder`两张RGBA。
- reveal只改变occluder：`1.00 -> 0.34 -> 1.00`；foundation始终`1.00`。

## 材质方法

1. 从Task121骨架重建顶面、两立面与foundation的独立plane masks；并集等于原Alpha。
2. ENV-A1 donor只允许提取基础色统计、去方向低频污渍、去轮廓微颗粒；禁止继承旧建筑边、道路白线、排水沟、路缘、接缝或自由透视。
3. 材质只在exact plane mask内部生成：顶面基值1.00，两立面约0.80/0.62；低频污渍亮度不超过±10，微颗粒不超过±6且混合8%—12%。
4. 轮廓2px、结构缝1px，只沿`±30.96°`或竖直方向。
5. 每栋最多一个小面积琥珀识别点；禁止文字、招牌、新功能语义、动态光照、shader或SubViewport。

## 必交

- 六栋各一张`FOUNDATION_CAMERA_V2_MATERIALIZED_RGBA.png`与`OCCLUDER_CAMERA_V2_MATERIALIZED_RGBA.png`。
- `plane-mask-readback.tsv`、`donor-usage.tsv`、`asset-manifest.tsv`、`source-lineage.tsv`、machine report与全包SHA。
- 六栋100%/50%材质板、normal/reveal/restore三态板、world overview与共享A/B PLAN帧。
- 材质方向审计板，证明主长边仍为`±30.96°`或竖直。

## 停止门

任一Alpha、canvas、pivot、front edge、占地或高度变化；出现20°—25°旧边；donor语义泄漏；需要手移/拉伸/复杂渲染；0.34后仍遮挡关注点；restore不等于normal；50%仍像程序挤出盒或纹理压过玩法读法——均立即停止。

机器PASS只允许进入制作人50%/100%实帧审查，不等于最终PLAN、Runtime、UA91、G2-B或Canon。
