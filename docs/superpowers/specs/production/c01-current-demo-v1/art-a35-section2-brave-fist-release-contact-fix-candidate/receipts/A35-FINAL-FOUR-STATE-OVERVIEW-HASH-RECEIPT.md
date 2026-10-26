# A35 / A34 勇拳最终四态总览确定性排版回执

> Date: 2026-08-25  
> Status: `PASS_FOR_USER_REVIEW_CANDIDATE / user=false / runtime=false / canon=false`

## 结果

已将以下四张独立状态原图排成单张横向总览：

1. `STATE 00 机制常态 / NEUTRAL`
2. `STATE 01 吸收冲击 / ABSORB`
3. `STATE 02 满载锁压 / FULL-LOAD LOCK`
4. `STATE 03 双拳释放 / DUAL-FIST RELEASE`

## 确定性制作边界

- ImageGen 调用：`0`。
- 四张源文件均未覆盖、未修改。
- 总览内只对四张源图做相同尺寸框内的等比缩放与居中排版；未裁切机体、未局部重绘、未抠图、未调色、未替换像素内容。
- 新增内容仅为深色画板背景、状态标签、标题、分隔色条与 Candidate 状态脚注。
- 排版脚本：`production/A35-FOUR-STATE-OVERVIEW.ffscript`。
- 失败的旧 A34 State03 不在最终四态源列表中。

## 最终源列表与 SHA-256

- State00：`517ebdce81c2ec0858d4ab3bfac6fe9d87a08b4aa1e5f5052d19400ea1a6a24f`
- State01：`3cc73984a067bc0403101bdd3ee2cffb85c677f5fdb7a42a5c78a11054c7ab1c`
- State02 R1：`51093c5f8bdbac527233a033a829368781efd47f50017d8843ee9b2d6a03399a`
- State03 A35：`218eb68b1c48f41697fc51e7828a0c5bc4500699392a035b152ee8a4875d8124`
- 排版脚本：`4d9b20a88aa0d364dc29619452bafc8b2ce1f877160ceca37197cdc20184e31c`
- 最终四态总览：`630f45c00788e5304e81d2e2f3f223c8e1e4cb95c53f38621687ece6aaf9fbd7`

机器可读源表：`source-lock/A35-FINAL-FOUR-STATE-SOURCE-LIST.tsv`。

## 目视检查

- 四个状态按 `00 → 01 → 02 → 03` 从左到右排列，中文和英文状态名均完整可读。
- 四台机体均保持完整全身；状态 03 的双拳、腕圈、套筒、导轨和肘部连接在总览尺度下仍可辨认。
- 状态 01 的吸收火花、状态 02 的压缩锁定、状态 03 的短行程双拳释放能在同一画面直接比较。

## 真实停门

该总览只供用户视觉审定。用户未确认前，四态仍不得进入正式 Sprite、Godot、Runtime 或 Canon。
