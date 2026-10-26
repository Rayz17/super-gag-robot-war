# Call01 GF Dialogue UI 用户否决隔离声明

> Lifecycle: `USER_REJECTED / HISTORY_ONLY / DO_NOT_USE`
>
> Date: `2026-08-24`
>
> Runtime / Candidate consumer / test-only consumer / Canon: `false`

## 用户结论

Call01 对话 UI 被明确否决：

> “有点老气，不要像是魔法和 D&D 游戏那种老式的 UI。”

否决范围包含 Call01 的全部像素与派生物：

- `raw/GF_DIALOGUE_UI_SKIN_ATLAS_CALL01_RAW.png`
- `deterministic-salvage-candidate/delivery/` 内的 RGBA atlas 与全部组件
- `deterministic-salvage-candidate/qa/` 内的目视板
- 所有白边清理、棋盘去除、九宫格裁切和机器指标

## 强制边界

- 不得载入 Godot，不得用于任何 test-only 或实际帧。
- 不得进入 Candidate consumer、Runtime、Default、Save 或 Canon。
- 不得作为新稿的 ImageGen 图像输入，不得裁图、贴图、变形、采样或复用任何像素。
- 可保留为生产历史和技术诊断证据；其白边清理结果不具备美术或消费资产资格。

新的现代 GF 对话 UI 必须从独立调用重新生成，仅可参考已确认 `GF_PLAN` / `GF_CONTACT` 的信息层级与色彩关系，不得引用本 Call01 的图像。
