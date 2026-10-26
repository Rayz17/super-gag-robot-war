# C01 勇拳 Camera V2 east 地图母版 Call01｜Section 2 回执

> Date: `2026-08-23`  
> Verdict: `FAIL_SEALED / NO_REROLL / NO_256_CANDIDATE`  
> Lifecycle: `Candidate evidence only`  
> `user_approved=false / runtime_allowed=false / canon_promotion=none`

## 本轮范围

只尝试一张 C01 地面勇拳 Camera V2 east 中性地图母版；不做空战、多向、动作包、社勇王组件或 Godot 接入。

## 输入与责任

| 输入 | 责任 | SHA-256 |
| --- | --- | --- |
| `BRAVE_FIST_USER_APPROVED_PIXEL_IDENTITY_REFERENCE.png` | 唯一身份、配色、完整身体、英雄脸、中央胸板、同一双大拳与拳后套筒 | `9159384683a1d43c5d5e3fe6d0eebf28707eedd25a076f03d88269035773ccff` |
| `source-guides/BRAVE_FIST_CAMERA_V2_EAST_GEOMETRY_GUIDE_1024_NOT_FINAL_ART.png` | 无身份 Camera V2 east、抬高正交 dimetric、2×2、pivot `[128,224]`、脚点与中性站姿 | `a68ff7d2c13546c85b92f057676962a37c8c4bd11211e7ce667af893f6b68361` |

几何源 SVG：`source-guides/BRAVE_FIST_CAMERA_V2_EAST_GEOMETRY_GUIDE_256_LOGICAL.svg`，SHA-256 `221f2404ec71003b6756bdbd3b9749f0a1bcb7931f30ccd1f7753849a34935c0`。导向图没有勇拳、馆守Z或任何其他机体身份像素。

## 唯一生成结果

- built-in ImageGen：`1` 次；reroll：`0` 次。
- raw：`generation-raw/BRAVE_FIST_CAMERA_V2_EAST_CALL01_RAW.png`
- raw SHA-256：`e97ac2e49c2008fc1d12afdcbddcdd7943c8d6feda910734ccc32860f38f86a7`
- raw readback：`1254×1254 / PNG / RGB / hasAlpha=no`

## 三道硬门

| 门 | 结果 | 首读证据 |
| --- | --- | --- |
| 勇拳身份 | `PASS_FOR_FAILURE_EVIDENCE_ONLY` | 橙金轻快完整机器人、英雄脸、中央胸板、双大拳和拳后套筒均可追认；没有社勇王组件。 |
| Camera V2 east | `FAIL` | 虽大致朝屏幕右侧／右下，但镜头仍偏近正面英雄立绘；近侧拳和远侧拳出现明显透视大小差，胸面近正视，未成立为抬高正交 dimetric east 地图母版。 |
| 真透明 Alpha | `FAIL` | PNG 是 RGB，无 Alpha；灰白棋盘格已烘入 RGB，不能冒充透明底。 |

## 停止与不存在项

按本任务硬门，任一项失败即停止。本轮不做第二次 ImageGen、不做去背景补救、不把 raw 确定性注册到 256、不生成名为 `BRAVE_FIST_CAMERA_V2_EAST_GROUND_MASTER_CANDIDATE_256` 的候选、不接 Godot。身份保住不抵消相机和 Alpha 失败。

