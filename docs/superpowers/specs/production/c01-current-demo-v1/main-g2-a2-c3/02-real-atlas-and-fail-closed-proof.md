# 真实 Atlas 与 fail-closed 证明

## 资源消费

C3 Scene 真实加载 4 张透明中性 PNG，以 `Sprite2D + AtlasTexture.region` 切换，不是 rect metadata 或 Polygon 代理。四资源均为 `RGBA8 + alpha + nearest + mipmap=false`，进入采样前各加载 1 次，后续 `reload_count=0`。

| stable id | slot | 尺寸 | PNG SHA-256 |
|---|---|---:|---|
| `V353U001` | `guardian_z_map_current` | 768×768 | `12196a8b5e66c5b8ebd891ae232361238ce08d3ec56d13a72e216eed4db73988` |
| `ENEMY_C01_BREAKER` | `breaker_map_current` | 1152×768 | `debdafd803f9f5c68420726e3b9abf29ab4a2608eecb6a61833fce4fc3407391` |
| `TARGET_C01_EMERGENCY_VEHICLE_01` | `emergency_vehicle_map_current` | 256×256 | `315db68cdde10d4ac1ba049d393d785c3a401b7e02f4160864aeb39373e342d6` |
| `ENEMY_C01_RIFT_SWARM` | `rift_swarm_map_current` | 384×192 | `ff96a2b0ee1e02d4941684b1953b51072b969b364f185bfc097bd1cc2f8bc65b` |

外部 validator 按锁定 schema／overlay／PNG bytes 重算 stable id、slot、path、SHA、尺寸、格式、alpha、filter 和 mipmap；`resources` 整包缺失也会 fail closed。

## clip 与区域切换

- 24 个精确 phase-matrix clip；21 个 continuity phase，每 phase 6 主体。
- 3 个签名、same-facing、one-hop alias；禁止 cross-facing fallback。
- 4 个 base slot 各用同一 Actor / Sprite / source texture 实例切换两个物理 rect，region 与实际截图 patch 同时变化，资源不 reload。

## 真实 Scene fail-closed

5 类负测均送入真实 Registry → Stage → Actor：缺 clip、错 camera contract、错 pivot、错 PNG SHA、rect 越界。目标 Sprite 与 shadow 实际隐藏，旧 proxy/body/shadow 不回退，其他 5 体保持可见，且每项只有唯一 reason；恢复后实例与 baseline 一致。

权威证据：[real-stage-fixture.json](receipts/real-stage-fixture.json)、[atlas-contract.json](receipts/atlas-contract.json)、[10-atlas-contract.log](logs/10-atlas-contract.log)、[12-real-stage-fixture.log](logs/12-real-stage-fixture.log)。
