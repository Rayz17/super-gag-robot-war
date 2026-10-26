# C01E02 A9.1-A3｜显示尺度冻结与两张忠实清稿 Pilot

> 日期：2026-08-19  
> 状态：`producer Candidate scale selected / two-frame cleanup pilot assigned / no Runtime`  
> 上游：68号R0.1三档实际PNG  
> 核心原则：这不是重新设计；是在已批准轮廓mask内部完成正式位图清稿。

## 1. 制作人尺度选择

制作人已直接查看：

- `art-a9-1a3-existing-source-reuse-r0-1-scale/R0_1_SCALE_SWEEP_A4_3840x720.png`；
- `art-a9-1a3-existing-source-reuse-r0-1-scale/R0_1_SCALE_DECISION_BOARD_1920x1080.png`。

三档判断：

- 320：道路与UI净空最好，但近30m巨体压力偏弱；
- 384：BREAKER bbox `318×330`，相对馆守Z `204×242`，宽度1.56×、高度1.36×；道路、红缝、前肢承重和右侧UI仍可读；
- 448：巨体感最强，但bbox `371×385`，UI净空仅27px、topbar净空54px，常态地图遮挡过高。

冻结：

```text
GUARDIAN_Z display frame = 256
BREAKER display frame = 384
selection lifecycle = Candidate producer scale lock
design change = none
```

该选择只冻结本Demo地图显示量尺；不修改18m／近30m Canon，不授权Runtime。

## 2. 唯一任务：two-frame faithful cleanup pilot

### 2.1 输出

只制作两张：

1. 馆守Z `south idle`，最终透明frame `256×256`；
2. BREAKER `north charge-ready`，最终透明frame `384×384`。

不做其他方向、动作条、Atlas或完整包。

### 2.2 唯一写入范围

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-faithful-cleanup-pilot/**`

## 3. 不可变身体mask

### 3.1 馆守Z

- mask源：67号exact `GUARDIAN_Z_C128_APPROVED_EXACT.png`；
- 外轮廓、约4.2头身、胸肩大形、四肢长度／宽度、脚底、south idle姿态不可变；
- CML008与V10X只补身份细节，不得把身体改回高身比展示稿。

### 3.2 BREAKER

- mask源：67号exact `BREAKER_B128_APPROVED_EXACT.png`；
- B高背壳、低嵌头、前肢承重半直立、短后稳定结构、north charge-ready姿态不可变；
- X关系板只把异质／生体装甲、单红缝、闭合胸缝、封闭上背出口烘入同一身体；不得产生另一具身体。

允许在高分辨率工作层把批准alpha mask确定性放大；最终任何非透明像素不得越出mask。不得用“更好看”为由改外轮廓。

## 4. 位图工作流

本Pilot必须使用`imagegen` skill做“编辑既有Sprite”，不能从文字生成新机体：

1. 每主体把exact 128源作为第一参考与不可变构图；
2. 馆守Z附加CML008、V10X、CML128 A常态参考；
3. BREAKER附加B身份板、X关系板、CML128 A常态参考；
4. ImageGen每主体最多`1`次编辑调用，禁止reroll寻找新造型；
5. 输出后以批准alpha mask裁切，mask外alpha必须为0；
6. 只允许透明边、despill、一次缩放、pad、颜色量化、alpha mask与机械排板；脚本不得绘制机体结构；
7. 若一次编辑无法在批准mask内形成可信清稿，标记失败并停止，不得继续抽卡。

### 馆守Z清稿目标

- CML008头冠／脸／胸／肩环／圆柱前臂识别点完整；
- E02双臂、无翼无背包；
- 深墨蓝压力线、4–7大色块、最多两级硬阴影；
- 256px地图尺寸下不糊成红蓝方块，脸、圆金核与双前臂仍可读。

### BREAKER清稿目标

- 第一眼是B＋X，不是龟、猿、雪橇、车或普通四足；
- 单红缝、闭合胸缝、封闭上背出口、异质叠片明确；
- 前肢确实承重，短后结构只稳定；
- 384px下保持巨大黑壳质量，但轮廓不吞道路信息。

## 5. 必交证据

1. 两张透明源工作图与最终`256／384`frame；
2. `SILHOUETTE_MASK_OVERLAY_1920x1080.png`：批准mask与最终alpha叠合；mask外像素数必须为0；
3. `PILOT_ON_A4_MAP_1280x720.png`：按69号量尺和bottom-center放回A4，只作视觉预审；
4. `PILOT_IDENTITY_STYLE_REVIEW_1920x1080.png`：责任源、最终单帧、50%／100%读法；
5. `source-lock.tsv`、`generation-log.md`、`pilot-self-review.md`、`delivery-hashes.sha256`、`completion-report.md`。

## 6. 制作人视觉门

机器必须检查alpha、尺寸、hash、mask外像素；制作人另看：

- 身份是否仍是馆守ZC与BREAKER B＋X；
- 比例与重心是否保持；
- KINETIC_CEL是否达到可用而非程序草图；
- 384档BREAKER压迫感是否成立且地图仍可读。

任一主体失败，只返该主体的局部编辑方案；不得重开设计，不扩四向／动作。

## 7. 冻结边界

本单不开放UA91、A9.1-B、Atlas、Godot、exact handoff、G2-B、LibTV、Canon迁移或git add／commit。两张Pilot通过制作人视觉门后，才决定是否扩四向关键帧。
