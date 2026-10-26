# Task105 简化遮挡、z 与实际帧回执

## 唯一遮挡 owner

C3 运行时隐藏但不改字节的旧 C2 `ROOFS_FOREGROUND_CURRENT`，启用唯一 C3 等价 owner：6 个小型固定 building-zone CanvasItem panel，z=900。可见单位的确定性 display bounds 与 panel 相交时，仅该 panel 从 alpha 0.94 切到 0.38，离开后恢复 0.94。

同一实际 BREAKER / Swarm02 被移出触发区后再恢复：

- 同一 panel id，alpha 精确 `.38 → .94 → .38`；
- 目标 panel bounds 不变，其他 5 panel 整行不变；
- Actor / Sprite 三态均可见，恢复位置等于 before；
- Actor / Sprite instance、AtlasTexture region、material、modulate、self_modulate 和主体 alpha 不变；
- triggered / normal 实际 PNG SHA 不同。

有效 Scene 调用图中没有 SubViewport、ViewportTexture、实时 alpha 轮廓、CPU 像素 mask、dirty-patch GPU toggle 或 split topology；旧复杂 WIP 仅留存 History，未被 Scene／runner 引用。独立椭圆影仍由 `engine_independent_ground_shadow_layer` 持有。

## z 与三尺寸

单张非 headless 实际帧同时显示 1×1 / 2×2 / 3×3 真实 Sprite。外部重算锁定：

- BREAKER `[18,8] → [640,380]`
- GZ `[20,9] → [680,400]`
- vehicle `[21,11] → [640,420]`

由 `sprite_top_left + pivot * display_scale = footpoint`与 `z=round(footpoint_y+bias)` 独立计算 rect／z 及 back-to-front 顺序；`z_as_relative=false`，有效 z 位于 building -900 与 roof 900 之间。三体是 fixture-only 可见重叠，不改 Session / Resolver 玩法 anchor。

## 制作人目视入口

- [A PLAN](captures/task105/A_PLAN.png) / [A CONTACT](captures/task105/A_CONTACT.png)
- [B PLAN](captures/task105/B_PLAN.png) / [B CONTACT](captures/task105/B_CONTACT.png)
- [panel triggered](captures/task105/ROOF_PANEL_TRIGGERED.png) / [panel normal](captures/task105/ROOF_PANEL_NORMAL.png)
- [1×1 / 2×2 / 3×3 overlap](captures/z-overlap/C3_Z_OVERLAP_1X1_2X2_3X3.png)

机器 PASS 不替代制作人对这些实际帧的 P99 目视签收。
