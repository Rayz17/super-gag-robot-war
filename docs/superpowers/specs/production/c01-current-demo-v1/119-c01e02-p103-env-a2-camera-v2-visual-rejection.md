# C01E02 P103：ENV-A2 Camera V2制作人视觉拒收

状态：`COMPLETE_VISUAL_FAIL / GROUND_GEOMETRY_RETAINED / STRUCTURE_AND_OBJECT_PIXELS_NOT_PROMOTED`

## 裁决

ENV-A2的确定性重组、字节继承、pivot注册与Camera V2底板公式均成立；但制作人与用户目视均确认，六栋继承建筑的像素视角没有服从Camera V2，不能进入最终PLAN。

## 证据

- ENV-A2 completion SHA-256：`e661aeb295b65bd620affb00634d2f75120ff523fc52feb823fe387a0ca1e25f`
- machine report SHA-256：`2b416030f60f7626706a273193817fe1cdda61b0bc64a8c9bbc564163c9d0091`
- delivery manifest SHA-256：`4d6a9305c2b6a9984b990b3d784187d32514ea5639e837f23c69fbe4cd800b7d`
- A PLAN 100% SHA-256：`f6aa829dcc360fc62325d0e8460d8531652670dd6c31c41e03ee3a983b4789c0`
- A PLAN 50% SHA-256：`cfcc6fce0a6ca89d6ec9f1645b65751b84944e3cc24a0c8d834ae28bd6b119c2`

Camera V2地面轴为`(40,24)`与`(-40,24)`，斜率应为`±0.600`、角度`±30.96°`。ENV-A2底板车道线符合该数值；六栋结构的主屋顶/基础边实测大多仅约`±20°～25°`，斜率约`0.36～0.45`，比目标平约`7°～11°`，部分基础边近水平并带自由透视。

因此`0px registration`只证明摆位和pivot，不证明像素属于同一相机。

## 保留与隔离

- 可保留：40×24 GroundBake几何方法、Camera V2四机位crop、模块ID/anchor/footprint/pivot、独立foundation/occluder接口、0.34显隐交互方法。
- 不可晋级：六栋Structure可见像素、盾/东门/警戒设施当前可见像素、四张环境cleanplate、ENV-A2自报视觉PASS。
- 禁止：对旧像素做简单缩放、手移或遮挡来冒充Camera V2；禁止进入最终PLAN、CONTACT、Runtime、UA91、G2-B或Canon。

下一版环境与战术物件必须直接在同一Camera V2模板中制作，并以屋顶两轴`±30.96°`与无透视汇聚作为50%前置门。
