# C01 E02 三段演出闭合包｜来源与权限回执

日期：2026-08-25  
状态：`CANDIDATE_ONLY / USER_FALSE / RUNTIME_FALSE / DEFAULT_FALSE / CANON_FALSE`

## Authority 分层

- **Hard**
  - `CML131`：C01 E02–E04 馆守 Z 可见派生只认 V10X `e1d6b00d…` 为正向身份父图；`CML008` 在本范围只提供生命周期语义，旧图不得作为像素或姿态输入。
  - `CML129`：GF PLAN / GF CONTACT 中用户确认的 BREAKER 具体设计是当前可见身份锚。
- **Working**
  - `V353U001` 与 `ENEMY_C01_BREAKER` 当前条目只提供角色/单位连续性，不覆盖以上 Hard 视觉谱系。
- **Candidate**
  - 本包三次调用及其 raw 仅为失败 trace；三张均未生成 Candidate sprite。
  - 两张既有 exact pose 继续保持原字节：
    - `V353U001|brace|south`：`a40e94a3c611367ebdf7d1c8fad708f90971f848e8429b1764ebcfb08707d696`
    - `V353U001|shield_block|south`：`875c0756bdaaf099429c8004189fc5fee2588d9f597e5bc4c66c67095459422e`
- **History / forbidden input**
  - A37 BREAKER shared 3D turntable 全目录。
  - A9.1-A3 Blender / Three.js 可见产物。
  - 旧馆守 Z、旧 BREAKER、previous-pose fallback、镜像/旋转/跨朝向复用。

本轮未读取上述 FORBIDDEN_HISTORY 为美术输入，未使用 Blender、Three.js、bpy、Python 建模或程序绘制。

## Exact 正向来源

### 馆守 Z / A17

- V10X 身份父图  
  `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`  
  SHA-256 `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade`
- V10X Camera V2 共用二维母图  
  `docs/superpowers/specs/production/c01-current-demo-v1/art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/masters/GUARDIAN_Z_V10X_CAMERA_V2_CARDINAL_NEUTRAL_SHARED_MASTER_RGBA_1254.png`  
  SHA-256 `3ea73fac822c7c169d2715ab95a36f549c19f330a5c02bb9c031a0ecacf9cd3a`
- A17 盾正面  
  `docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png`  
  SHA-256 `8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47`
- A17 盾背/握把  
  `docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_REAR_INTERIOR_RGBA_MASTER_768x1152.png`  
  SHA-256 `7e9db3af4e7ccf9c361edbc6ebbadf74a4c61c9281eaa62373814a8cefe6bfe0`

### BREAKER

- GF PLAN 身份/轮廓/表面  
  `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-gold-frame/delivery/GF_PLAN_1280x720_v2.png`  
  SHA-256 `c1d2219354a7c8bd6fcccc326181e4875f4e292d916fb0b7512cafd06fce5f1c`
- GF CONTACT 承力语言  
  `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-gold-frame/delivery/GF_CONTACT_1280x720_v2.png`  
  SHA-256 `83b713d6f700aa3b0bacc541902d98b92baa3de7730f502a1197a783b71c1633`
- 当前正向二维透明母图  
  `docs/superpowers/specs/production/c01-current-demo-v1/art-a11-camera-v2-gz-east-breaker-north-map-master-candidate/breaker-gf-camera-v2-north-transparent-candidate/gf-locked-single-master-20260823/deterministic-alpha/source/BREAKER_GF_LOCKED_SINGLE_MASTER_DETERMINISTIC_RGBA_1254.png`  
  SHA-256 `4f93ae3729cb21da59740010e193a66786e2cde9be038fb980337a6401da6d05`
- west 几何导图（仅方向/极性/pivot）  
  `docs/superpowers/specs/production/c01-current-demo-v1/art-a32-section2-breaker-west-red-beam-candidate/source-guides/BREAKER_CAMERA_V2_WEST_GEOMETRY_GUIDE_384_NOT_FINAL_ART.png`  
  SHA-256 `96c2dddbe47bc9aabc2886a2415e4dc8a86948f994f60b425dfcfaac8e773f5e`

## Camera V2 锁

`P(x,y)=((x-y)*40,(x+y)*24)`；south=`[-40,+24]`；west=`[-40,-24]`。  
GZ 目标为 `256×256 / pivot [128,224] / 2×2`；BREAKER 目标为 `384×384 / pivot [192,320] / 3×3`。三张 raw 均在可见硬门前失败，故未伪造尺寸、pivot 或 footprint 回执。
