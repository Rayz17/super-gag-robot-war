# 禁止源与非污染边界

状态：`ACTIVE_FOR_HANDPAINT_PREPRODUCTION`

## 绝对禁止作为像素、mask、轮廓或材质donor

- Call03失败raw：`art-a9-1a6-s-c2-call03-breaker-north-v2/generation-raw/CALL03_BREAKER_NORTH_RAW.png`；
- Call03目录内任何由失败raw派生的抠图、缩放、拼板或master候选；
- R1失败的BREAKER SVG／PNG及其自动清稿派生；
- ENV-A1／ENV-A2／旧A4整屏、建筑、道路、UI、角色和馆守Z像素；
- 任何龟、猿、普通四足、车辆、雪橇、甲壳虫或趴地坦克轮廓；
- 任何旧Runtime fixture或neutral proxy作为真实身份图；
- 任何ImageGen新调用、自动reroll或局部编辑调用。

## B方向源的允许范围

用户批准的B身份板和B128只允许人工目视理解“高背、低嵌头、前肢承重半直立、短后稳定足”的责任关系。禁止：

- 复制、裁切、拼贴、描边采样、alpha合并或颜色采样；
- 把128像素直接放大成1536底稿；
- 把旧角度、旧pivot或旧相机视作Camera V2 exact；
- 以“来源已批准”代替本包192黑剪影与50／100实际帧门。

本包可见底稿由`build_breaker_handpaint_preproduction.py`从新坐标和新多边形确定性绘制；`geometry-readback.json`记录`historical_breaker_pixels_consumed=false`和`call03_raw_read_or_consumed=false`。

## 生命周期

REV1—REV4全部只作History失败对照；当前没有可用覆画底稿。尤其禁止把REV4交给人工画师做表面覆画或清稿。未来若获得真人概念资源授权，必须从空白Camera V2画布重构B黑剪影，再经过192纯黑实际目视门；不得产出其他方向、动作、Runtime资产或Call04。
