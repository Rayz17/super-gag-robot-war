# 制作组 · 实帧抽帧

窗口抽帧，不是机器门。无窗不强跑。不签视觉验收。

## 入口

`scripts/breaker-desk frames --slice e02 --round-dir PATH`

复用 `game-godot/tests/c01_breaker_demo/e02_gameplay_hud_actual_frame_capture.gd`。必须窗口跑，禁止 `--headless`（`Viewport.get_texture()` 无窗会挂）。

产出：`round_NNN/frames/*.png` + `frames.json`。`user_visual_acceptance` 只许 `false`。

## 禁止

- 把抽帧绿当用户目视
- 用 headless 冒充实帧
- 把旧轮 PNG 冒充本轮新产出
