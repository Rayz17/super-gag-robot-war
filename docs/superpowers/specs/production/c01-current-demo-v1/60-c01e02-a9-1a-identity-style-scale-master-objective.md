# C01E02 A9.1-A｜身份、画风与比例唯一母版目标

> Owner：美术资产 Session  
> 依赖：55、56、59  
> 状态：`Candidate / user master review required`  
> 本阶段完成即停，不制作整帧Gold Frame、Atlas、Golden Turn或Runtime资产

## 1. 任务目标

把“漂亮但每帧重画”的A9流程改成可连续生产的唯一母版流程。只回答四个问题：

1. 馆守Z在地图Q/SD规格中是否仍是唯一的V10X馆守Z；
2. BREAKER是否稳定保持用户批准的B＋X身份；
3. 18m／近30m与2×2／3×3的体量关系是否固定；
4. 常态画面是否真正服从A档`KINETIC_CEL`，而不是暗色半厚涂AI概念图。

## 2. 必读与唯一身份源

开始前完整读取并核验：

- `docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv` 中 `CML001`、`CML008`、`CML128`；
- `.superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_jicun_stand.png`；
- `.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`；
- `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/series_style_storyframe_v23a_kinetic_cel.png`；
- `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png`；
- `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png`；
- A4获批的`40×20`投影、馆守Z2×2、BREAKER3×3、小体1×1；
- A9 v2只作雨夜、灯光、色温、碎地和重量参考，不作机体／人物／UI身份来源。

如上述来源互相冲突，写精确阻断并停；不得自行挑一张“更好看”的替换Hard Lock。

## 3. 交付物

### A. 馆守Z唯一Q/SD母版

- 一张透明背景、约4头身、E02双臂、无翼无背包的主母版；
- 正／背／左／右四向轮廓校验图，允许先以同一母版的Rig／确定性变换建立，不要求本阶段输出完整运行Atlas；
- 保留金色层叠头冠、中央红冠、蓝色额盔、银色栅格脸、红色X胸甲、圆形金核、宽方肩环、等重圆柱前臂和V10X配色；
- 用轮廓叠合或关键点表证明头身、肩宽、胸宽、前臂长度、腿长在各向一致。

### B. BREAKER唯一地面壳母版

- 一张透明背景的B＋X主母版；
- 规划待机与首撞承压只允许从同一母版的分层／Rig派生，不得分别重新生成新身体；
- 三秒可辨：低头块单红缝、前肢承重半直立、巨背壳、闭合胸缝、封闭上背出口；
- 与小体A并排，证明不是放大版小体；与馆守Z并排，证明近30m／3×3压过18m／2×2。

### C. 纪存通讯母版使用裁决

- 本阶段不得重新创造第三张纪存脸；
- 默认直接使用CML001当前脸、制服和左臂终端，制作一个不遮挡战场的22–25%屏占比通讯构图代理；
- 若认为需要采用A6或其他27–29岁候选，必须先交`CML001 current vs candidate`身份迁移板并停止，等待用户明确选择，不得在本任务内自行替换Hard Lock。

### D. 风格与比例联合板

- `KINETIC_CEL`合规板：外轮廓、内线密度、大色块、两级硬阴影、材质高光和磨损预算逐项对照；
- `18m 2×2 / near-30m 3×3 / 1×1 swarm`同一`40×20`等距地面量尺板；
- 50%与25%缩放可读性板；去掉标签后仍能分辨馆守Z、BREAKER和小体。

### E. 来源与可复现证据

- `asset-manifest.tsv`、`source-receipt.tsv`、`identity-keypoints.tsv`、`scale-contract.tsv`、`style-compliance.tsv`、`completion-report.md`与核心SHA；
- 记录每项`source_tool`、参考图角色、编辑链和禁止用途。

## 4. ImageGen与制作方法

- 默认使用内置ImageGen；项目资产必须保存回工作区。
- 身份敏感对象优先采用`identity-preserve`或对既有母版的定点编辑；每次迭代只修改一个目标，并重复写明不变量。
- 不允许用五张参考混合后整帧重生的方法建立身份母版。
- ImageGen只产出独立源资产；Krita／Blender／分层合成用于轮廓清理、视角代理、Rig、遮罩和一致性校验。
- Pillow、ImageDraw、Canvas或程序多边形不得绘制用户可见机体、人物和地图；可用于拼板、标签、切片、遮罩和校验。

## 5. 用户门与禁止项

完成后停在制作人回收点，由制作人统一展示以下三项：

1. 馆守Z唯一Q/SD母版与四向一致性；
2. BREAKER B＋X母版、与小体区分及两机体量关系；
3. `KINETIC_CEL`合规与纪存当前身份消费方式。

不得制作或启动：`GF-PLAN v3`、`GF-CONTACT v3`、完整Atlas、地图重绘、FX序列、音频、LibTV、Godot、exact handoff、Runtime或Canon迁移。

