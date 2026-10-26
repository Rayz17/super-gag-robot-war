# ENV-A3 NW_BLOCK 50% / 100%目视自审

状态：`LOCAL_STRUCTURE_METHOD_PASS / A_PLAN_FULL_FRAME_INTEGRATION_NOT_PROVEN / NOT_FINAL_ART`

## 目视结论

- 角度：新屋顶和地基两轴由同一`40×24`投影直接生成，实测斜率`±0.600`、角度`±30.96°`，不存在自由透视或汇聚；旧A2像素仅作为拒收对照。
- 50%：外轮廓、屋顶平面、两面墙体、地基和门位仍可区分；材质密度克制，没有用渲染噪声掩盖几何。
- 100%：foundation与occluder共享`[240,378]` pivot；normal/reveal/restore只改变occluder alpha `1.00 -> 0.34 -> 1.00`，foundation保持`1.00`。
- 排序：front edge仍为raw`[80,288]`，A PLAN readback`[320,-70]`，未加任何手工screen offset。
- A PLAN限制：NW_BLOCK按当前玩法位置本来就在A PLAN镜头上缘之外。因此A PLAN实际crop只能证明“没有被手移”，局部视觉门由exact-position focus与world-canvas overview承担；这栋样板本身不能单独证明六栋全图50%整合。

## 放行边界

可放行同模板扩建的只是：`foundation/occluder分层 + exact-40×24结构几何 + 整件0.34显隐`方法。不可据此宣称环境全图、六栋风格统一、最终PLAN、CONTACT、Runtime或60fps已通过。
