# 100% 首读自审

## 馆守Z raw

- 身份：可识别为当前V10X/Q/SD馆守Z；金冠、红冠、蓝额盔、银栅格脸、红X胸、圆金核、肩环和圆柱前臂均保留。
- 边界：E02双臂、无翼、无背包、无武器成立。
- 视角：明显见头肩、胸、前臂和足部顶面；主体朝屏幕右下，east读法基本成立。
- 风险：输出没有alpha；约4头身与地图256缩放后的细节/线压仍未经过实际像素门。因此仅记 `GZ_RAW_VISUALLY_VIABLE_PENDING_SEPARATE_PRODUCER_REVIEW`，不是MASTER。

## BREAKER raw

- 有继承GF的暗色叠片壳、低红缝与重量，但孤立后第一读法变成高壳龟状普通四足。
- 四条清楚分立的动物式肢端抢过了“前部连续承力＋短后稳定”的关系；壳形也过于完整封闭，GF场景里的异质压迫转为普通生物壳。
- 主体纵轴从左下指向右上不够明确，头与前肢更像朝屏幕左下，未可信满足Camera V2 north。
- 裁切、despill、pivot或缩放都不能修复上述身份/朝向；按用户条件判 `BREAKER_RAW_VISUAL_FAIL_TURTLE_QUADRUPED_AND_NORTH_READ`。

## 总裁决

`PAIR_GATE_FAIL`。不制作同屏比例门，因为用失败BREAKER做比例板会把错误身份包装成候选。机器输入与调用次数正确，不等于视觉通过。
