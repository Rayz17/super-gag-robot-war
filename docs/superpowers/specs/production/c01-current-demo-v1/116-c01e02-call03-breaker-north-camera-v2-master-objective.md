# C01E02 Call03：BREAKER 北向 Camera V2 单主体母版任务书

状态：`DISPATCHED_ONE_CALL / NO_REROLL / ENVIRONMENT_INDEPENDENT / CALL04=false`

## 1. 制作决定

ENV-A1 的模块原图可保留，但当前整屏环境没有通过P102的50%读法。该问题不得继续串行阻塞与环境像素无关的单主体机体母版。

Call03因此改为与环境整合修正并行：只生产一张BREAKER北向地图相机母版；不读取、不引用、不消费任何ENV-A1像素。此调度变化不修改玩法、锚点、身份或Camera V2，只解除无必要的美术工种串行依赖。

## 2. 权威输入

- P102环境分层裁决与并行放行：
  - `115-c01e02-p102-env-a1-producer-visual-review-and-parallel-release.md`
  - SHA-256 `ec545f37d766a248e4c0a5b9dff5e9056a703bb0b53d30fd3a767175bd06140c`
  - 只授权BREAKER单主体母版与ENV-A2并行；不代表ENV-A1整屏视觉通过。
- P99真实Atlas中性消费者制作人签收：
  - `106-c01e02-p99-sprite-first-preproduction-and-c3-producer-acceptance.md`
  - SHA-256 `10c8df7490f21c2df12c513981867fd0168e86f9e789e46105c192996d2d4bf1`
- Route A2用户批准：
  - `108-c01e02-route-a2-modular-environment-and-interaction-user-approval.md`
  - SHA-256 `c33bc0ffa4fe6f5ecc553001e640eba18a39a917a0c4691def8c940ca0ad0280`
- Camera V2制作人签收：
  - `112-c01e02-p111-camera-v2-exact-interface-producer-acceptance.md`
  - SHA-256 `2eda6f614f46b0ba8ef43adc76ff08152d63d3560a5e4b19989c7612d44a2793`
- Camera V2 exact合同：
  - `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json`
  - SHA-256 `756f77db883fd060fdd323d2533191ade689c0a1362f92f043fac17dbe28ab4a`

当前Canon只确认BREAKER是近30米黑甲突入壳，地面阶段能钻地、冲撞与发射赤红冲击；B身体与X表面仍是本次Candidate美术责任源，不得反向晋升Canon。

## 3. ImageGen唯一输入

只允许两张图，顺序固定：

1. Camera V2 40×24 text-free geometry guide：
   - `art-a9-1a6-s-c2-call03-breaker-north-v2/source-guides/BREAKER_NORTH_CAMERA_V2_40X24_GEOMETRY_GUIDE_384.png`
   - SHA-256 `fedfd4e3150b4856f4120fb832b2b3a8f1ba00f9a0b6b90f2c2c4701497d7131`
   - 只约束384×384安全框、3×3 footprint、pivot `[192,320]`、north屏幕向量`[40,-24]`、半直立承力外包络。
2. BREAKER B+X唯一安全身份板：
   - `art-a9-1a6-s-c2-sprite-first-map-camera-masters/BREAKER_BX_ISOLATED_SAFE_REFERENCE_BOARD_2400x1800.png`
   - SHA-256 `e36bd3c9d186806d88614bd9f9df1eb97b56228889cc96b2cad1fda992170ee3`
   - B负责高背壳、低嵌头、前肢承重半直立、短后足；X负责异质生体甲、非对称曲面、柔性缝、闭合胸缝和封闭上背出口；底部CML128区只负责画法。

严禁引用：ENV-A1、Call02整屏、旧A4地图、馆守Z、任何其他机体、CONTACT、UI或角色像素。

## 4. 唯一生成目标

- ImageGen恰好1次；无自动reroll、无编辑调用。
- 单主体、纯色易抠背景；无地面、投影、环境、文字、标记、武器FX或第二对象。
- 输出视觉方向为地图`north`：屏幕右上`[40,-24]`，能看见壳体与肩背顶面；不是眼平正面或自由透视。
- 第一读法必须是：巨背壳压住躯干、低头嵌在壳缘、两条承重前肢形成半直立冲撞姿态、短后足只负责稳定。
- 一票失败：龟、猿、普通四足兽、车辆、雪橇、甲壳虫或趴地坦克。
- X表面必须覆盖B身体：非对称异质板片、柔性接缝、窄红单缝、闭合胸缝、封闭上背出口；不得变成工业对称方盒。
- KINETIC_CEL：4—7个大色值块、干净线压、最多两级硬阴影、有限磨损；禁止照片厚涂和高频噪点。

## 5. 确定性后处理

仅允许：原字节入库、背景去除/despill、等比缩放、固定384×384透明画布、pivot `[192,320]`、透明像素RGB清零、SHA与alpha bbox记录。

禁止：重画身体、搬肢体、补第二套结构、改朝向、形变、用环境遮住缺陷或手移pivot。

输出目录唯一为：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-s-c2-call03-breaker-north-v2/**`

## 6. 必交QA和证据

- ImageGen raw原图与生成日志，明确Call03=`1`、Call04=`0`、reroll=`0`。
- `BREAKER_NORTH_CAMERA_V2_MASTER_RGBA_384.png`。
- 100%透明底图、50%缩略图、geometry-guide注册叠图、alpha/pivot/bbox板。
- 简单Camera V2 grid上的3×3 footprint／pivot重组图；不得使用ENV-A1环境像素。
- `source-lineage.tsv`、`asset-manifest.tsv`、`machine-validation-report.json`、`50-100-visual-self-review.md`、`completion-report.md`、`delivery-hashes.sha256`。

## 7. 50%／100%门

50%先看轮廓：必须读成B的半直立承力突入体；任何龟／猿／普通四足／车辆读法即失败且停止，不消耗Call04。

100%再看身份：B身体与X表面共同成立；北向顶面、窄红缝、闭合胸缝、封闭上背出口、短后足、透明边和pivot都正确。

机器PASS不等于制作人视觉PASS。完成后停在P100，不得自行开放Call04、CONTACT、Atlas、Runtime、UA91、G2-B或Canon。
