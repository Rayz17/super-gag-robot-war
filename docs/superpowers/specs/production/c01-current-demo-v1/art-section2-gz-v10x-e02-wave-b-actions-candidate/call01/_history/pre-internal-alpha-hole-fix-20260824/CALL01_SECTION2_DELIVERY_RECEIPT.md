# Call01｜馆守 Z V10X E02 Wave B 动作精灵｜Section 2 内部交付

> Status: `2 INTERNAL_PASS / 1 BLOCKED / 3 NOT_CALLED`
>
> 全部为 `Candidate`；`user=false`、`runtime=false`、`default=false`、`canon=false`、`godot_bound=false`

## 内部通过的独立资产

| 动作 | 文件 | 内部视觉门 | 技术门 |
| --- | --- | --- | --- |
| `brace/east` | `map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_BRACE_EAST_CANDIDATE_256.png` | V10X 身份、east 朝向、降重心、双脚撑地在 50% 可读 | 256×256 RGBA8；pivot `[128,224]`；2×2；scale 1；透明底 |
| `brace/south` | `map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_BRACE_SOUTH_CANDIDATE_256.png` | V10X 身份、south/屏幕左下朝向、降重心、双脚撑地在 50% 可读 | 256×256 RGBA8；pivot `[128,224]`；2×2；scale 1；透明底 |

每张均有独立 `DARK_LIGHT_50_100_QA.png`、`SOCKET_READBACK.png` 与单张 metadata JSON。ImageGen raw 的浅色连通棋盘底只通过确定性 alpha 清理移除；该步骤保持 raw 的 RGB 字节不变，再统一缩放并登记脚点，没有重绘、镜像、旋转或合成旧图。

## 阻断与未生产

- `shield_take/south` 首次结果在“三道旧痕”和取盾动作首读失败，隔离在 `stage-a-block/`。
- `shield_hold/south`、`shield_block/south`、`shield_bash/south` 按停线规则未调用。

本回执只证明 Section 2 内部选择，不替代用户视觉批准、实际地图帧批准或 Runtime 资产验收；本包没有修改 Godot、binding、Resolver、Default 或 Canon。

