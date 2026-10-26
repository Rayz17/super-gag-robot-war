# C01E02 P99｜Sprite-first预生产与C3中性消费者制作人签收

日期：2026-08-21  
责任人：制作人-2  
状态：`P99_ACCEPTED / REAL_ATLAS_NEUTRAL_CONSUMER_PREFLIGHT_SUPPORTED / SIMPLE_2D_OCCLUSION / FIXTURE_ONLY / REAL_ART_ZERO / FINAL_60FPS_NOT_PROVEN`

## 1. 制作人裁决

P98的current map-camera槽位／Atlas／socket／phase合同，与Task99／Task105的C3真实Atlas中性消费者已经联合闭合。后续真实单机地图Sprite不再需要美术猜相机、脚点、占地、pivot、clip或遮挡接口。

本签收只关闭“是否具备接入真实透明Sprite的确定性消费者”这一前置门，不批准中性色块为美术资产，不证明FUN、UA91、G2-B、Runtime、save、Default Entry、Canon晋级或最终60fps。

可签状态只有：

`REAL_ATLAS_NEUTRAL_CONSUMER_PREFLIGHT_SUPPORTED / SIMPLE_2D_OCCLUSION / FIXTURE_ONLY / REAL_ART_ZERO`

## 2. 已核封包

- 完成回执：`main-g2-a2-c3/06-completion-report.md`；
- delivery manifest：`main-g2-a2-c3/delivery-hashes.sha256`，SHA-256 `b70fe98a3ca1019b5445cbbabb3862e29c614a52dbf6dee15b692a59bb4bca19`；147项独立`shasum -a 256 -c`全部通过，C3封包内除manifest自身外无遗漏，manifest晚于完成报告与正式证据；
- 最终机器验证：`receipts/machine-validation.json`，SHA-256 `5e70b9b3d106994ebf3817e14c3ff25dd2f6533f3e256556d8d1d51b97d36abf`；11 sections、0 errors、PASS；
- `logs/99-final-regression.log`是封存回归权威，SHA-256 `e957a8df9b0531fee73fd442e31c395324400e74e66ca39c04b7bc054e8881ad`；
- `logs/100-final-runner.log`是runner退出后的完整外层执行转录，SHA-256 `8f64916cb14ea1e313e034634a9e8da4d2a75f06f5819cc686fee1efe5cb58ce`；两者职责不同，不互相冒充。

## 3. 产品帧目视签收

制作人已逐张查看正式封包中的A／B PLAN、A／B CONTACT、同一屋顶片normal／trigger与1×1／2×2／3×3重叠帧：

- `A_PLAN.png`：`f270a47758ad2c5d9b1cdf28ebfff060caddcc3d17ad52286ce22524e1b5c172`；
- `A_CONTACT.png`：`123ff912be6e8e30584bab177a9de985d0eac614024c35dca05c2366f64502da`；
- `B_PLAN.png`：`1596a4fc3ce3cb71bae2ba3e193e14b8ab6b4ec817b6e2c1b947996c52eb3119`；
- `B_CONTACT.png`：`1237911ba2251896b85041d6945ad3de63daf8713da139a706b4c01e816f49fa`；
- `ROOF_PANEL_TRIGGERED.png`：`f270a47758ad2c5d9b1cdf28ebfff060caddcc3d17ad52286ce22524e1b5c172`；
- `ROOF_PANEL_NORMAL.png`：`2728a52036f6b233b6933e11e325fb9799d1ff09ee042c8448d7724a05ae8404`；
- `C3_Z_OVERLAP_1X1_2X2_3X3.png`：`663d235a1871746436828e5c2841adf167e2f4515d10f2854a12d163cc82642c`。

目视结论：

1. A／B规划与接触镜头中的主体脚点、占地、方向切片和共同接触焦点没有出现第二套坐标；
2. 简化遮挡只改变相交屋顶片，未出现整层淡化；主体Sprite、Atlas region与主体alpha保持不变；
3. 1×1、2×2、3×3主体在同一画面内可见，前后关系随脚点Y成立；
4. 中性色块只证明消费者、注册与时序，视觉质量明显不是产品资产，严禁进入PLAN母版、UA91或真实handoff。

## 4. 性能边界

正式非headless 120帧预热＋600帧动态采样：average `11.894ms`、p50 `8.402ms`、p95 `26.053ms`、max `30.066ms`、`frames_over_33.3ms=0`；资源load-once、reload 0、显存无增长。

因此只能签：

`FIXTURE_30FPS_STABILITY_ONLY / FINAL_60FPS_NOT_PROVEN`

正式current-topology静态地图与真实馆守Z／BREAKER／小体／车辆组合后，必须在G2-B或UGT以前重开`p95<=16.7ms / max<=33.3ms`门。本回执不得替代最终性能验收。

## 5. 后续唯一合法动作

P99前置门关闭后，只允许另立一张带exact路径、SHA、相机、画布、pivot、身份门和停止门的Call03单主体任务书，生成一次`BREAKER_PLAN_MAP_CAMERA_MASTER_NORTH_RGBA_384`，完成后立即停在P100制作人50%／100%视觉审查。

本文件自身不等于ImageGen调用，也不开放自动reroll、Call04、CONTACT、全Atlas、真实Runtime接入或G2-B。若Call03出现龟／猿／普通四足第一读法、B身体关系或X表面关系漂移、方向／脚点／占地错误，即整轮失败并停止，不得自动消耗Call04。

环境ENV-E0的几何／相机／mask可保留，但可见像素已由103号回执拒收。环境新生成或外部人工2D属于独立预算／路线门，不得挪用Call03／Call04。

继续保持：

`real_art_loaded=0 / Call04=false / UA91=false / G2-B=false / Runtime=false / save=false / Default unchanged / Canon unchanged / FUN_NOT_PROVEN`
