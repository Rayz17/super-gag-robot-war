# ENV-A3 Camera V2精确Structure样板完成回执

状态：`COMPLETE_ZERO_GENERATION_PILOT / LOCAL_METHOD_PASS / NOT_FINAL_ART`

## 完成

- 已从Camera V2公式直接构造NW_BLOCK独立foundation与occluder；没有继承旧建筑轮廓、屋顶边或自由透视。
- exact grid rect=`[1,0,7,5]`，pivot=`[240,378]`，高度=`84px <= 90px`，两轴=`±30.96°`。
- 已交normal/reveal/restore三态、50%缩略图、A PLAN世界画布精确位置、A PLAN真实crop与未手移focus、A2/A3角度对照。
- ImageGen调用数：`0`。

## 制作人应看

1. `qa/NW_BLOCK_ANGLE_COMPARISON_1600x900.png`
2. `qa/NW_BLOCK_REVEAL_TRISTATE_BOARD_1680x586.png`
3. `qa/A_PLAN_WORLD_CANVAS_NW_BLOCK_EXACT_POSITION_1280x720.png`
4. `qa/A_PLAN_ACTUAL_CAMERA_CROP_NW_BLOCK_OFFSCREEN_1280x720.png`
5. `qa/NW_BLOCK_EXACT_POSITION_FOCUS_1280x720.png`

## 结论

这条方法解决了“素材角度和地图角度不匹配”的几何根因，局部结构与显隐方法可继续；但NW_BLOCK在A PLAN实际镜头外，不能把本样板冒充整张地图签收。扩六栋后仍需一次50%全图制作人实际帧门。
