# C01E02 M3-R0.5 M0｜启动与控制

## 启动

```bash
cd /Users/rayz/Documents/超gag机器人大战
./scripts/run_c01e02_m3_r05_presentation.sh
```

该命令直接启动非默认场景 `res://scenes/candidate_runtime_demo/c01/e02/m3_r05/c01e02_m3_r05_presentation.tscn`。默认 startup 不变。

## 控制

| 状态 | 键鼠 / 手柄 |
| --- | --- |
| 局势揭示 / 阻断通讯 | `Enter`、`Space`、鼠标左键或手柄 A 在最短显示时间后翻页 |
| 移动光标 | 方向键或 `WASD`；持续按住会重复移动；左摇杆可移动 |
| 选择落点 | 地图左键；键盘 `Enter` 使用当前光标落点 |
| 转向 | `Q` / `E`；右栏左右转向按钮 |
| 行动 / 预备 / fallback | 右栏按钮 |
| 进入摘要 | `Space` 或“查看作战确认” |
| 返回修改 | 摘要页“返回修改”或 `Esc` / `Backspace` |
| 执行 | 长按摘要页“长按执行本轮”；键盘可长按 `Enter` / `Space` |
| 跳过演出 | 共同结算时“跳过演出”或确认键 |
| 调试层 | `F3` 切换；默认隐藏 |
| 结果页重玩 | “重玩另一解”或 `R` |

## 测试

```bash
./scripts/test_c01e02_m3_r05.sh
```

可选参数：`--skip-capture`、`--skip-full-regression`。完整证据批次未使用 `--skip-capture`，全量 Godot 回归另以最终代码运行并通过。
