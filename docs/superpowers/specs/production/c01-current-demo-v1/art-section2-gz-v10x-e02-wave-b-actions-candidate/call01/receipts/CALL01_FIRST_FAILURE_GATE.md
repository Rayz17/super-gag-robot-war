# Call01｜首个失败门与停线回执

> Decision: `STOP_AFTER_FIRST_SHIELD_ACTION_FAILURE`
>
> `user=false` · `runtime=false` · `canon=false` · `godot_bound=false`

## 首个失败姿势

- 请求：`V353U001 | shield_take | south`
- Built-in ImageGen call：`1`；random reroll：`0`
- 隔离 raw：`stage-a-block/generation-raw/GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_TAKE_SOUTH_CALL01_BLOCK_RAW.png`
- SHA-256：`fb61c5bdf53ec50753bd54a737f2148e04804622a5d4ac1078dafcbef496c55f`

## 首个失败硬门

1. A17 的冷态连续性要求是 **三道** 宽浅旧擦痕；结果把移除赤红热痕后的盾面画成 **四道** 冷白擦痕。
2. 关键姿态首读更接近已经完成的 `shield_hold / shield_block`，没有明确证明“从低位扯起、进入持盾位”的 `shield_take` 过渡。

因此该 raw 没有进入 `masters/`、`map-candidates/`、QA 或 metadata 的可交 Candidate 列表，也不得作为任何后续姿势的派生父图。

## 停线范围

按“一姿势最多一次调用、零随机重抽、前一姿势失败即停”执行，以下没有调用、没有文件、没有伪造完成：

- `shield_hold/south`
- `shield_block/south`
- `shield_bash/south`

