# 馆守 Z V10X Camera V2 四向中立母版｜来源锁

> 状态：`CML130_SCOPED / CANDIDATE_ONLY / FAIL_CLOSED`
>
> 不构成：动作包、Godot 绑定、Runtime、Default、Canon 或用户实际帧签收

## 唯一正向身份源

- `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`
- SHA-256：`e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade`
- 角色：CML130 在 `C01E02_demo_visual_derivation_only` 范围内的唯一正向身份母图。

## 唯一辅助结构参考

- `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png`
- SHA-256：`3873ed1ac32949f5ba2cdfbc334131b1a7d202124aaab1192d3211c0eb006ee9`
- 角色：只校对同一机体的约 4.2 头身、结构、非对称与色块；它是 `design_orthographic`，不得直接裁成地图朝向。

## 当前正向相机源

- `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json`
- SHA-256：`756f77db883fd060fdd323d2533191ade689c0a1362f92f043fac17dbe28ab4a`
- `camera_contract_id=CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE`
- `view_space=map_dimetric_40x24`
- `P(x,y)=((x-y)*40,(x+y)*24)`

76 号与旧 `map-camera-slot-contract.json` 中的 40×20 是被 Task111 当前运行链取代的 preproduction 历史，只能解释旧回执，不能作为本包的正向相机源。本包不修改全局相机合同。

## 本包明确未消费

- CML008 旧视觉像素；
- 旧 `guardian_z_east_camera_v2_candidate.png`；
- A13、A18、A19、A22；
- A8/A9 旧地图派生；
- GF 裁图；
- 旧 40×20 preproduction 相机合同；
- 任何镜像朝向或跨朝向替代。

任何上述路径或 SHA 进入正向输入、参考或绑定，本包立即失效。
