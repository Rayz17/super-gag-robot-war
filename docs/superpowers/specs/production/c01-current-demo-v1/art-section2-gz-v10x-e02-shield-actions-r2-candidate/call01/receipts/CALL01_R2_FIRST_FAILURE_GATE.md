# Call01 R2｜`shield_take / south` 首个失败门

> Decision: `STOP_AFTER_FIRST_SHIELD_ACTION_FAILURE`
>
> 成功姿势：`0`；ImageGen 调用：`1`；random reroll：`0`
>
> `user=false` · `runtime=false` · `default=false` · `canon=false` · `godot_bound=false`

## 调用前 guide

无身份几何 guide 在 50% 明暗底通过：低位、偏心、上提、轻微画面内滚转、俯身错步均能与 `hold / block / bash` 区分。因此合法触发一次 `shield_take/south` 定向生成。

- guide：`../../guide/GZ_V10X_SHIELD_TAKE_SOUTH_IDENTITY_FREE_GEOMETRY_GUIDE_1024.png`
- guide SHA-256：`5e9025f72f0500c87303d5b13c449e8a6b6f08839bd00b87dd46e1a1dce4bced`
- guide QA：`../../qa/GZ_V10X_SHIELD_TAKE_SOUTH_GEOMETRY_GATE_50_100_QA.png`
- guide QA SHA-256：`c200516738faff27e4b20544a1ace0b391d686f185c7939b2534d9fa9d7cc483`

## 唯一调用与隔离 raw

- 动作：`V353U001 | shield_take | south`
- Built-in ImageGen：`call01 only`
- random reroll：`0`
- raw：`../stage-a-block/generation-raw/GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_TAKE_SOUTH_R2_CALL01_FRONT_HANDS_FAIL_RAW.png`
- raw SHA-256：`13e9a723ba72fcdb9f7ae76921425dbebb274c1bff489d40433727bdf85acfe3`
- raw：`1254×1254 RGB`，棋盘烘入 RGB；只做了失败审阅用的确定性 alpha 读回，不生成 master。

## 50% 先验读回

通过的子门：

- V10X 身份与 south 前向首读基本保住；
- 盾位于低位并偏心，身体俯身、错步，首读更接近刚取起而不是稳定持盾／正挡／横拍；
- 冷盾严格是三道宽浅旧擦压痕，无赤红热痕，也没有白色第四痕；
- 无弹孔／圆形弹坑。

首个硬失败：

- 图像把左右两只机械手都画在盾冠与盾正面／外侧可见面上；
- 合同要求盾正面手数 `0`，两只手必须在背面／内侧双握把，背面接触数 `2`；
- 因此肩—肘—前臂—背面握把的承力链没有成立。

失败 QA：

- `../stage-a-block/qa/GUARDIAN_Z_V10X_SHIELD_TAKE_SOUTH_R2_CALL01_FRONT_HANDS_FAIL_50_100_QA.png`
- SHA-256：`4b6fc425d8392888df6e15aa7e25cc0086139dd6e109e019c7d45340a99828d0`

确定性透明读回只用于明暗底 QA：

- `../stage-a-block/qa/GUARDIAN_Z_V10X_SHIELD_TAKE_SOUTH_R2_CALL01_ALPHA_REVIEW_ONLY.png`
- SHA-256：`c730c4609a09984e6d231a72ffaad10a6f997d6a8e5379b9fcf5b23dcf931b9d`
- RGB 与 raw 完全一致；透明像素 `1,105,838`，不透明像素 `466,678`，partial alpha `0`。

## 停线结果

该 raw 不进入 `masters/`、`map-candidates/`、metadata socket 或任何下游姿势的正向父图。以下均未调用、未生成、未伪造完成：

- `shield_hold / south`
- `shield_block / south`
- `shield_bash / south`

本包没有地图 Candidate，因此 `256×256 RGBA8`、pivot `[128,224]`、2×2、scale 1 与 socket readback 均为 `NOT_EMITTED_AFTER_VISUAL_FAIL`；也没有修改 Godot、binding、Resolver、Default、Runtime 或 Canon。
