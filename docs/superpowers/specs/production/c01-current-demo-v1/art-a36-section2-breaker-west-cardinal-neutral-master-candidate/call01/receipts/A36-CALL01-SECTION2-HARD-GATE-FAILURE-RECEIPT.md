# A36 Call01 — BREAKER west 中立母版硬门失败回执

## 结论

`FAIL_STOP / DIAGNOSTIC_HISTORY_ONLY / NO_DELIVERY / NO_GODOT / NO_RUNTIME / NO_CANON`

本轮 built-in ImageGen 实际调用 `1` 次，随机 reroll `0` 次。调用只使用：

- 当前 BREAKER north Candidate，作为唯一身份／材质像素源；
- 由 Camera V2 40×24 数值机械生成的匿名 west 几何 guide，作为唯一构图源。

A30、A32、B+X、Call03 与旧 GUIDE 系像素均未传入调用。

## 硬失败

1. Camera V2 west 目标角为 `-149.0362°`；生成结果朝红缝 PCA 主轴为 `-175.8097°`，误差 `26.7735°`，超过 `10°` 硬门。结果仍是近水平向左侧视，而不是头端明显上升到左上的固定 dimetric west。
2. 主体质心到红缝方向为 `-179.2591°`，相对目标误差 `30.2228°`。红缝虽然位于形态头端，但整台机体没有跟随 west 轴。
3. 输出为 `1254×1254 RGB24`，`hasAlpha=false`；浅色棋盘烘进 RGB，不是真透明精灵。

因此没有进行去背景、缩放、384 注册、pivot/socket 生产，也没有生成 Candidate delivery。

## 证据

- Raw：`call01/generation-raw/BREAKER_A36_CALL01_WEST_CARDINAL_NEUTRAL_HARD_GATE_FAIL_RAW.png`
  - SHA256 `622d59bc9c770148e75d3c78171728a907510ba42497854e8d5fdbd37977581e`
- QA：`call01/qa/BREAKER_A36_CALL01_WEST_HARD_GATE_FAIL_QA.png`
  - SHA256 `0acf60be9c78ee6df868f6174d35e89b2e5778d63240eb2e3d106329789ec5f3`
- 数值回执：`call01/receipts/BREAKER_A36_CALL01_WEST_HARD_GATE.json`
- 几何 guide：`call01/source-guides/BREAKER_WEST_CAMERA_V2_GEOMETRY_GUIDE_1536.png`
  - SHA256 `aeb27a36735c56be51a79ded893cb5eadebd74bddc53618ba64da2a0155eaaad`

## 生产边界

- 当前 north SHA `6b20111c80e3dc76adb5a05b55395359b7d1bdc2ec189060859058e53dbffde1` 未修改。
- `idle/west`、`red_beam/west`、`hit_recoil/west` 仍全部缺图；运行时继续 fail-closed marker，禁止 north／镜像／上一姿态回退。
- 下一轮不能把本次 raw 当正向输入；如再做，应由美术资产 session 采用人工三维转面／结构建模或可控分层重绘，不再重复同型单张 ImageGen 纠偏。
