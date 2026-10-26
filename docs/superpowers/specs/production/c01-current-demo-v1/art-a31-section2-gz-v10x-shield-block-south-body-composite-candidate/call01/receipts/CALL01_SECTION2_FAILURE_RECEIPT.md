# A31 Call01｜`V353U001|shield_block|south`｜Section 2 失败停线回执

> 结论：`HARD_GATE_FAILED_NO_COMPOSITE`
>
> ImageGen 调用 `1` 次，随机 reroll `0` 次，最终 Candidate `0` 个。

## 本次做了什么

- 按 `identity-preserve` 模式，把当前 CML130/V10X Camera V2 south 资产作为编辑目标，把 CML130 V10X lockframe 作为唯一高分辨率身份参考。
- 只要求生成 BODY-ONLY：双臂前伸、双肘弯曲、双拳对准两个不可见的盾背握把目标；提示词明确禁止盾、背景、FX、文字与第二视图。
- 没有把 A17 盾像素送入 ImageGen；A17 热态／受击后正面外壳始终保留为确定性合成源。

## 硬门结果

| 门 | 结果 | 证据 |
|---|---|---|
| CML130/V10X 身份 | `NOT_PROMOTABLE` | 蓝红白金主色块与若干身份特征仍可认，但比例变成偏高挑的正面 hero body；在错误镜头下不能证明锁定的紧凑 south 地图身份。 |
| Camera V2 south | **`FAIL`** | 画面接近正面平视；头、胸、骨盆与双足没有共同指向 lower-left `[-40,+24]`，也没有 40×24 高俯视所需的 top/side planes。 |
| 双臂／双手 | `PASS` | 两条等长完整手臂；双肘弯曲；双前臂内收；两个拳头分离且分别连接。 |
| BODY-ONLY / 无盾 | `PASS` | 没有生成盾牌或盾牌碎片。 |
| 真 Alpha | **`FAIL`** | Raw 为 `1024×1536 RGB`，仅有 `R/G/B` 三通道；浅色棋盘已烘进 RGB，不是透明预览。 |
| 无文字／无 FX | `PASS` | 未发现文本、标注、光效或敌人。 |

Camera 与 Alpha 任一失败即触发来源锁中的停线规则。本次两项同时失败，因此没有尝试抠图、阈值去背、matting、旋转、镜像、跨朝向回退或第二次生成。

## 停止后的资产状态

- Raw 只保留为失败证据：
  - `call01/generation-raw/GUARDIAN_Z_V10X_CAMERA_V2_SHIELD_BLOCK_SOUTH_BODY_ONLY_CALL01_RAW.png`
  - SHA-256 `77fd478233d4bdd1d0a81b807be4e5e0217d256e79097a4a4c22f8db3d272f7b`
- Camera QA：
  - `call01/qa/CALL01_CAMERA_V2_SOUTH_FAIL_COMPARISON.png`
  - SHA-256 `567310bdebe0860f1c0ab67cb464f96c8121991b89e9766083454bfc49b57f9b`
- Alpha QA：
  - `call01/qa/CALL01_ALPHA_FAIL_DIAGNOSTIC.png`
  - SHA-256 `e32b3ac2e4a6c105b1df89b0bc0528b16822c2b24c7cfa4530c2c8c1c82abe8a`
- 未生成：`256×256 RGBA`、pivot `[128,224]`、footprint `[2,2]` 的地图 Candidate。
- 未生成：front-edge socket 登记。它只有在 BODY-ONLY 合格、A17 确定性合成实际发生后才合法。
- 未修改：任何 Godot binding、production matrix、Runtime、Default 或 Canon。

## 后续门

这不是请求重抽的授权。若未来另开生产批次，必须重新取得调用授权，并继续以 CML130 V10X south 为唯一姿态／身份正向输入，以真正透明的 BODY-ONLY、明确 lower-left south 高俯视和双后握把手位作为同一批次的前置硬门；A17 合成仍只能在这些门全部通过后执行。
