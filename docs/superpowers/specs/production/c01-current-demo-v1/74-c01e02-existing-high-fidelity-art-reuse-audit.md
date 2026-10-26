# C01E02｜现有高质量美术复用审计

> 日期：2026-08-19  
> 状态：`SUPERSEDED_BY_75 / WRONG_OLD_GZ_BASELINE_SELECTION / HISTORY_ONLY`  
> 上游：73号R1透明PNG用户视觉全退

> **纠错声明（2026-08-19）**：本审计把旧版 `guardian_z_sprite_chibi.png`（SHA `60352b…1038`）误当成当前馆守Z Q版候选。该结论已由75号纠偏回执撤销，禁止继续执行本文件第2.2节与第4节第1—2项。当前唯一正确的馆守Z E02 Candidate Q谱系为 `V10X e1d6… → c701… → 330346… / 3873…`；正文保留仅作错误历史证据。

## 1. 结论

73号退回后，对当前共享工作区做了只读审计。结论不是“两台都缺设计”：

- 馆守Z已有高质量透明Q图，可零重画直接作为地图单帧候选；
- BREAKER已有B身体与X表面用户裁决，也有多张高分探索稿，但没有一张同时满足“高质量＋严格B＋X”的透明成品；
- 因此馆守Z进入现成资产用户确认门，BREAKER保持最终二维执行缺口；不得再把两者打包重画。

## 2. 馆守Z复用清单

### 2.1 Hard身份

`/Users/rayz/Documents/超gag机器人大战/.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`

- SHA-256：`a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521`；
- Authority：CML008 Hard；
- 用途：锁头冠、脸、胸、肩环、圆柱前臂和旧超级系重量；
- 禁止：直接当地图Sprite或被Candidate稿覆盖。

### 2.2 现成高质量透明Q图

`/Users/rayz/Documents/超gag机器人大战/.superpowers/brainstorm/37837-1782033239/content/asset-production/guardian-z-v1/guardian_z_sprite_chibi.png`

- SHA-256：`60352bc2e948e57cb3fa1eef21e93bc3c3ae2923d3d4f6564e32271143e31038`；
- 规格：1254×1254 RGBA；
- Authority：当前美术方向manifest的`locked_reference_baselines`；Candidate、非Runtime、非Hard本体；
- 用途：不重画，只裁切／缩放／pad为south或front-three-quarter idle地图单帧；
- 身份：双臂完整、无翼、无背包，直接继承CML008造型；
- 禁止：虚构成北／侧／背视图，声称Hard／Runtime，或重画机设。

该资产在67号来源冻结中被遗漏；这是此前转去C128放大与SVG重画的关键流程错误。

### 2.3 比例立绘与峰值姿态

- `guardian_z_stand.png`：  
  `/Users/rayz/Documents/超gag机器人大战/.superpowers/brainstorm/37837-1782033239/content/asset-production/guardian-z-v1/guardian_z_stand.png`  
  SHA-256：`73f14133c3f1fe99cb554dd622374fb7061cfc78379a62351465eb304080f9c8`；只用于LibTV／Cut-in／比例身份细节，不作地图Q图。
- `guardian_z_attack_pose.png`：  
  `/Users/rayz/Documents/超gag机器人大战/.superpowers/brainstorm/37837-1782033239/content/asset-production/guardian-z-v1/guardian_z_attack_pose.png`  
  SHA-256：`b524df7343ddaffb47a349095997a90834cf73679fecc8b544fb35e6872ceda9`；只用于峰值Cut-in／LibTV／动作参考，不作routine地图Sprite。

### 2.4 E02限域与C方向

- V10X E02候选：`guardian_z_collector_e02_lockframe_candidate_v10x.png`，SHA `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade`；只校正双臂裸机、无翼无背包的局部边界；
- C128：`GZ_QSD_A1_candidate_C_128.png`，SHA `d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e`；只锁约4.2头身、动作空间、pivot和2×2读法，不是绘画母版。

## 3. BREAKER复用清单与真实缺口

### 3.1 已批准责任源

- B身体板：  
  `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png`  
  SHA-256：`7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868`；锁高背、低头、前肢承重半直立与短后稳定结构。
- B128方向样张：  
  `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png`  
  SHA-256：`e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4`；只锁north轮廓、重心与bottom-center pivot，不是成品。
- X关系板：  
  `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png`  
  SHA-256：`cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85`；锁异质生体甲、单红缝、闭合胸缝与封闭上背出口。

### 3.2 高分稿只可捐局部

- `BREAKER_BX_GROUND_SHELL_MASTER_RGBA_1400.png`，SHA `cbeb1ecb18e9d1ed41dd96d939c56e1f00f0eeab3f1af6bd4ddca048e8e02113`：高分透明但整体偏龟／猿，只可捐甲片、柔性缝与红缝；
- `BREAKER_BX_NONANIMAL_KINETIC_MASTER_RGBA_1400.png`，SHA `b47ebc4a6b8538f23892229f5554ae6c33b066ac37cf7077a71399e6931fb89d`：偏雪橇／车辆，只可参考硬色块与阴影画法。

磁盘上没有可整图复用的高质量严格B＋X透明成品。真实缺口是一次合格的最终二维执行，不是重新做方向选择。

## 4. 生产边界

1. 馆守Z不再画；先由用户确认`guardian_z_sprite_chibi.png`是否作为地图south/front-three-quarter基线；
2. 确认前不裁切、不缩放、不写Runtime；
3. BREAKER只允许未来补一张产品级`north charge-ready`；不得整机ImageGen、Blender Python或程序几何绘制；
4. BREAKER单帧未过制作人实际像素门前，不扩方向／动作；
5. Golden Turn的蓄力、冲撞与受击优先由Godot位移、倾斜、缩放、遮罩红光和冲击FX表达，降低逐帧美术需求；
6. A9.1-A3 Rig／SVG／R1全部隔离为失败证据，不再成为派生源；
7. UA91、A9.1-B、exact handoff与G2-B继续冻结。

本审计未修改任何图片或Runtime文件。
