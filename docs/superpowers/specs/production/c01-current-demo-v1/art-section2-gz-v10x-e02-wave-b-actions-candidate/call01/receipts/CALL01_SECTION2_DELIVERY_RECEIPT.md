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

## Alpha 修复后实际 Godot 帧取证

- macOS GUI、`1280×720`、当前 `Camera V2 40×24`、当前 `GroundMapView`：`game-godot/captures/c01_gz_v10x_brace_actual_frame/run_20260824_10_alpha_fix/`。
- `brace/east` 帧 SHA-256：`e717b2f3f70f604ec359ab98928143b7efc32fc58cdb69d9f3b8bac7d80ecc22`。
- `brace/south` 帧 SHA-256：`0dfa4fc4abc267721f7db109a1d9034ad937d95e832f59fabbf93c35dc526fa6`。
- 有效 manifest SHA-256：`4ef1a64203d1888b73554a31e45aee5915db852bd3d2f35fda34d64a4e252423`；内部目视回执 SHA-256：`0fcf2bf959c7fae19bc963bb2ff64533d28ff3e7630111f632673b7bcaa2b47f`。
- 与修复前 History 直接比较，地图精灵中东向有 `74` 个原不透明孔洞像素改为透明，南向为 `284`个；实际帧中肩臂—躯干负空间能看到地图底色，胸、腰、腕、腿和脚尖的白银装甲仍保留。
- pivot `[128,224]`、`2×2`、scale `1`、脚点 `[400,338]` 均未变；binding SHA、Camera 合同 SHA 与 world SHA 前后一致，旧馆守 Z History 没有被缓存或激活。
- `brace` 仍未写入生产 pose binding；取证使用测试层外部 RGBA overlay。生命周期仍是 `Candidate/user=false/runtime=false/default=false/canon=false`，等待用户视觉判断。
