# ImageGen generation log

治理状态：Candidate；`runtime_allowed=false`；`real_art_loaded=0`；零 reroll；没有调用 Call03/Call04 旧分支。

## 调用 1：馆守Z east

- 调用次数：1/1；reroll：0。
- 时间：2026-08-23（Asia/Shanghai，本任务 turn）。
- 引用恰好三张：
  1. `source-guides/GZ_EAST_CAMERA_V2_EXACT_GUIDE_256.png`，SHA `3d47d9a1022102f9409d14c0798c284c2f82844ebfb274432b283e1ffc3ce9dd`；只管 Camera V2 east、2×2、pivot。
  2. V10X E02，SHA `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade`；只管 E02 结构与身份。
  3. Q/SD 单主体 front，SHA `3303465975ccc726dc3ee4088c57e71cf6e1dfa0fd64a1241f57e48ea4d8da24`；只管约4头身重量与配色。
- Prompt 核心：仅一个馆守Z；抬高正交轴测；east=屏幕右下 `+30.9637565°`；V10X/E02双臂裸机；约4头身；指定冠、脸、红X胸、圆金核、肩环、等重圆柱前臂；无翼、背包、盾、武器、场景、地影、文字。
- 工具原始路径：`/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-053488b4-e77f-40cb-968a-12f34893fcf0.png`。
- 工作区 exact copy：`generation-raw/GZ_EAST_CALL01_RAW.png`，SHA `8a5907c0c2cc071e5f4900d977fbbc6bc3348f983e38f56ed45cb310dfbfe0a5`。
- 工具实际输出：1254×1254 RGB；棋盘格被烘进 RGB，非 genuine alpha。
- 内部首读：身份、双臂、无翼背包、east 右下与顶面关系可继续人工评审；未升级为透明母版。

## 调用 2：BREAKER north

- 调用次数：1/1；reroll：0。
- 引用恰好三张：
  1. `source-guides/BREAKER_NORTH_CAMERA_V2_EXACT_GUIDE_384.png`，SHA `cdcc9b4dd7bdc9224252e883d0263fd359a70dd198209b77348e566e18ed5160`；只管 Camera V2 north、3×3、pivot。
  2. GF PLAN v2，SHA `c1d2219354a7c8bd6fcccc326181e4875f4e292d916fb0b7512cafd06fce5f1c`；具体身份、表面、轮廓锚。
  3. GF CONTACT v2，SHA `83b713d6f700aa3b0bacc541902d98b92baa3de7730f502a1197a783b71c1633`；承力关系辅助锚。
- Prompt 核心：仅提取GF黑壳BREAKER；抬高正交轴测；north=屏幕右上 `-30.9637565°`；巨大异质叠壳、低嵌头单红缝、前部连续承力、短后稳定；禁止龟、猿、普通四足、车辆、场景、地影、文字或其他演员。
- 工具原始路径：`/Users/rayz/.codex/generated_images/01a018f7-b863-7973-9d4e-f11e9982024a/exec-2387c394-1498-45a9-82f0-96a4c0c2b289.png`。
- 工作区 exact copy：`generation-raw/BREAKER_NORTH_CALL01_RAW.png`，SHA `3fced17cdc4099c733429a66c202e851b674df27650f317ead2c157b32347118`。
- 工具实际输出：1254×1254 RGB；棋盘格被烘进 RGB，非 genuine alpha。
- 一票失败：孤立首读仍为高壳龟状普通四足，四条标准肢端过强；主体朝向也未可信锁到 north 右上。命中用户明定立即停止条件。

## 预算与停点

- 馆守Z：1/1；BREAKER：1/1；总计2次；reroll=0。
- 失败发生后没有抠图、补画、局部编辑、追加生成或母版包装。
- 未生成256/384透明母版、50%板、剪影板、A PLAN同屏合成或比例脚点readback；这些只能在两个主体都通过首读后制作。
