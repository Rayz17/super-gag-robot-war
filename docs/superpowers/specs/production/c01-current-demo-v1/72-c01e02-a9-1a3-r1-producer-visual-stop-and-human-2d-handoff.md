# C01E02 A9.1-A3｜R1制作人视觉停止回执与人工2D接力边界

> 日期：2026-08-19  
> 状态：`producer visual reviewed / pair rejected / Codex auto-art stopped`  
> 权限：Candidate；`runtime_allowed=false`；非Canon迁移；非exact handoff

## 1. 纠偏结论

馆守Z与BREAKER的设计选择早已关闭。本轮之前发生的反复，根因是制作合同把“尚未形成最终地图Sprite母版”错误解释成“需要重新创作一套设计”。

正式改为：

```text
design selection = closed
map Sprite adaptation = unfinished
redesign = forbidden
```

- 馆守Z继续服从CML008 Hard身份、V10X E02限域与用户批准C动作骨架型；
- BREAKER继续服从用户批准B前肢承重半直立身体与X异质／生体装甲表面；
- A9、A9.1-A/A2、64号Blender与69号ImageGen失败派生均无权重新定义二者。

## 2. 制作人实际像素审查

已直接查看，而非只读validator：

- `GUARDIAN_Z_C_SOUTH_IDLE_256-R1.png`；
- `BREAKER_BX_NORTH_CHARGE_READY_384-R1.png`；
- `SVG_PILOT_50_100_REVIEW_1920x1080-R1.png`；
- `SVG_PILOT_ON_A4_MAP_1280x720-R1.png`；
- `SVG_SILHOUETTE_OVERLAY_1920x1080-R1.png`；
- 两份分层SVG、来源锁、delta与QA回执。

### 2.1 馆守Z

结论：`PRESERVE_AS_USER_REVIEW_CANDIDATE / NOT YET UA91 APPROVED`。

- 已保持既有身份、4.2头身、冠／银脸／红X胸／金核／宽肩环／双圆柱前臂；
- 胸下—髋—上腿咬合比70号完整，50%和A4地图上仍可辨认；
- 该张可以保留为以后与合格BREAKER并列送UA91的候选；
- 不因配对方失败而重画馆守Z，也不在本回执中擅自替用户批准。

冻结文件：

- SVG SHA-256：`c453f4d51d79612e24d12be92ad778bbeeb6ff622a95ab9be4986acda9eb5a61`；
- PNG SHA-256：`cf5efaf32e4a0ffd00fe2b21024e9e9281e3d01b62c2834f7fdedbbc531a8157`。

### 2.2 BREAKER

结论：`PRODUCER_VISUAL_FAIL / HUMAN_2D_FINISH_REQUIRED`。

- B的高背、低嵌头、单红缝、前肢承重和短后稳定关系仍在；
- X暗缝与非对称分件已有技术实现；
- 但100%、50%及A4实读的第一印象仍是“装甲猿／普通重四足”，没有达到“高背异质突入壳”；
- 因此不能作为UA91母版、不能扩方向／状态、不能进入A9.1-B或Runtime。

冻结失败证据：

- SVG SHA-256：`1af66d4cc8fceeeee57d3b3215b573388a59e33e9e5866dc5e0c94a6966a66ea`；
- PNG SHA-256：`ce8970cc679fd81cca6e2308cdde73276f0eead3466982550d2355ef772bc18e`。

## 3. 机器结果不升级视觉结论

R1来源锁与交付哈希通过；`machine_pass_all=true`。馆守Z approved silhouette IoU=`0.980006`，BREAKER=`1.000000`，bbox、pivot与包络外alpha均通过。

这些只证明文件边界与几何约束。它们不推翻上面的制作人第一读法，也不构成产品或视觉验收。

## 4. 停止门

71号只授权一次局部R1，现已消耗并停止：

- 不开R2/R3；
- 不再用Codex、Python、Blender或整机ImageGen自动清稿；
- 不让失败BREAKER牵连馆守Z重新设计；
- 不扩四向、动作、Atlas、A9.1-B、Godot、LibTV或G2-B；
- 原主程序继续冻结，`real_art_loaded=0`、U2与G2-B均未开放。

## 5. 唯一后续美术接力

下一次可写动作必须是“人工2D美术局部成品化”，不是新概念设计：

1. 只处理一张`BREAKER B+X north charge-ready 384`；
2. B身体、比例、接地点、pivot和外包络不变；X表面关系不变；
3. 允许人工重画壳内甲片节奏、承重前肢装甲语言、头壳遮叠、线压与硬阴影，使第一读法脱离猿／普通四足；
4. 当前R1 SVG只作可编辑分层脚手架与失败对照，不作审美终点；
5. 先交透明单帧、50%／100%板与A4地图板；制作人实际像素通过后，才与本回执冻结的馆守Z候选一起送UA91；
6. UA91前仍不画其他方向或状态。

若没有人工2D美术资源，本DAG保持停门，不用自动重画伪造进度。

## 6. 当前DAG

```text
馆守Z R1候选冻结 ───────────────┐
                                ├─ 制作人配对预审 ─ UA91用户母版裁决
BREAKER人工2D单帧接力 ─ 制作人门 ┘

UA91通过 → exact interface冻结 → A9.1-B → signed handoff → G2-B
```

