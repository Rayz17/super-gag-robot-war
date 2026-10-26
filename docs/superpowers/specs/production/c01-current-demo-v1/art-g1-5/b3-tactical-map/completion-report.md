# C01E02 G1.5-B3 完成报告

## 结果

- 交付 `MAP-A / MAP-B / MAP-C` 三组严格同坐标、同 T2/S1 状态的地图分层候选。
- 每组包含不烘入程序信息的环境底板、独立天气旧损、前景遮挡/软淡出、墙挂重盾/空挂点互斥态与 T2/S1 可读性合成。
- 共享几何为 `12x9 / 108 cells`，签名 `3a898cacdd1d2020a403aaa087140f5eb9990bffc983b037142fc1a8afa034c4`。
- 当前 profile 不包含 blocked-cell 拓扑；108 格均登记为 `uniform_ground / collision_semantic=none`。

## 证据边界

- 馆守 Z A1-C、BREAKER B1-B/X、退役重盾 B2-A/F 都只是获批派生方向，没有 Sprite Master 或 Runtime handoff。
- B1-B 比例样张尚未真正绘入 X 异质/生体装甲；B2-A 样张也尚未真正绘入 F(D70/P30)。
- 上述样张仅出现在可读性审查合成图，未烘入底板、遮挡或天气层。

## 生命周期

- 全部产物：`Candidate`
- `runtime_allowed=false`
- `runtime_handoff=none`
- 未写入 Godot，未改 Canon/Runtime/玩法/坐标/footprint/CP2，未开始 B4/C1/D1/LibTV/Cut-in/视频。

## 生成侧自检

- 冻结来源：34 项 git blob + SHA-256 逐项精确匹配。
- 合同提交：`a851398347806850c8b0e0ce6a4d83a14e0677bb`。
- Demo fingerprint：`944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`。
- 交付后仍需由用户完成三项独立裁决；未获批前不解锁 B4。
