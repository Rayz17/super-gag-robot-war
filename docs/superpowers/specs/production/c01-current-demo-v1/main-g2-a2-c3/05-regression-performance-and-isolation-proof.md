# 回归、性能与隔离证明

## 唯一 formal runner

`scripts/test_c01e02_m3_golden_slice_g2_a2_c3.sh` 在最终源码冻结后运行一次，exit 0。runner 先生成 preflight regression bundle，通过第一次外部机器重算与 Canon report/strict，再从 outer full log 封存 [99-final-regression.log](logs/99-final-regression.log)，更新 summary 的 path/SHA/mtime，最后第二次验证封存产物。

- 最终机器验证：11 sections，0 errors，`PASS`。
- 新鲜度：60 个 validator 消费的 receipt / PNG / regression log 全部晚于 run start 且晚于最终 source mtime。
- 源码指纹：before / after / final 均为 `851cf33659d301fbe605bcf713fe88ffcf1e90111619653748635fb7a7cc7e55`。
- Canon：report 与 strict 均通过，无 runtime violation。

## 非 headless 动态性能

macOS / Apple M2 Max / Godot 4.7 / Compatibility OpenGL3 / VSync 0；120 帧 warmup + 600 帧采样，真实 InputEvent 提交后自然经过 T1–T5、CONTACT、动态 camera/anchor/rect/panel，并回到 PLAN。

- average `11.894 ms`
- p50 `8.402 ms`
- p95 `26.053 ms`
- max `30.066 ms`
- `frames_over_33.3ms=0`
- 4 PNG load-once，reload 0，region cache 22→22，texture VRAM 6,455,296→6,455,296 bytes

结论只能写：`FIXTURE_30FPS_STABILITY_ONLY / FINAL_60FPS_NOT_PROVEN`。本夹具 strict 60fps p95 门为 FAIL；真实静态 current-topology 地图与真实单位组合后、任何 G2-B signed handoff / UGT 以前，必须重开 `p95<=16.7ms / max<=33.3ms` 正式门。

## 玩法非回归

- C2 屏幕输入、12–15s 时线与 Full/Skip 语义：PASS；Full `13320ms`、Skip `0ms`。
- R1 route family：A=21 / B=15，直达 BFS、alternate、20 次确定性：PASS。
- R2 / R3 / contact / ground occupancy / projection / audio / asset fail-closed：PASS。
- B R1 exact：`c3b307b9698d645598594cb6674c86779a13420b9934cf562f379d112d1f41fa`。
- B R2 exact：`f09de07bb6b0b32c1a44e7ca1d5e24a6cbc3bac498010cb92490b781bd6480a6`。
- audio runtime 退出清理：连续两次干净退出，semantic errors=0；未把退出清理重试冒充语义 PASS。

权威入口：[performance-600-frames.json](receipts/performance-600-frames.json)、[regression-summary.json](receipts/regression-summary.json)、[machine-validation.json](receipts/machine-validation.json)、[100-final-runner.log](logs/100-final-runner.log)。
