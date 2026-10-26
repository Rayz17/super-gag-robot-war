# C01E02 A9.1-A3｜已有批准母版优先与零重设计纠偏

> 日期：2026-08-19  
> 状态：`active correction / Candidate only`  
> 用户纠偏：馆守 Z 已有通过设计稿；不得把制作地图 Sprite 误解为重新设计馆守 Z 或反复重抽 BREAKER。  
> 覆盖范围：本单覆盖 65 号 P0 中立即重新生成两张身份源图的安排；65 号 Sprite-first、稀疏 Clip、Godot／LibTV 分工继续有效。

> **2026-08-24 scope 纠偏：** `design_selection=already_done / sprite_adaptation=still_required / redesign=forbidden` 继续有效；但本文第2.1节把 CML008 旧视觉图当作 C01E02 Demo 正向组合责任源的表述已被 130 号覆盖。本 scope 中只能从用户确认的 V10X（SHA `e1d6b00d…`）派生身份；CML008 图仅 History/crosscheck。Q/SD正侧背仍不是 Camera V2 地图 Sprite。

## 1. 根因与新口径

此前多轮把以下三个不同层次混为一件事：

1. 已批准的身份／轮廓／表面关系；
2. 地图 Q/SD 规格转译；
3. 最终逐帧位图生产。

结果是每到第3步又重新发明第1步，造成馆守 Z 身份漂移和 BREAKER 在龟、猿、车、雪橇之间来回变化。

本单冻结：

```text
design_selection = already_done
sprite_adaptation = still_required
redesign = forbidden
```

“需要新画 Sprite”只表示需要按地图方向、动作、pivot和目标像素重新绘制／清稿，不表示可以改变机设、轮廓、身体拓扑或表面关系。

## 2. 馆守 Z 的唯一组合责任源

### 2.1 Hard 身份

- `CML008`：馆守 Z Hard Art Lock；
- 文件：`.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`；
- 责任：身份、头冠、脸、胸、肩环、圆柱前臂、旧超级系重量、18m生命周期。

### 2.2 E02 限域机设

- V10X：`guardian_z_collector_e02_lockframe_candidate_v10x.png`；
- 文件：`docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`；
- 权限：只用于 C01E02 Candidate 双臂裸机派生；不得升 Canon／Runtime。

### 2.3 用户已选地图 Q/SD 轮廓

- 用户选择：`C可以`；
- 选择项：C「动作骨架型」，约4.2头身；
- 父板：`docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_direction_board_1920x1080.png`；
- 128样张：`docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/GZ_QSD_A1_candidate_C_128.png`；
- 正式回执：`docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/a1-user-approval-receipt.tsv`。

这三者合起来已经决定“馆守 Z 是谁、E02长什么样、地图Q版采用什么身体比例和动作空间”。后续不得再提案 A/B/C，不得改变头身、肩宽、胸甲布局、前臂圆柱关系或脚部大形。

A9.1-A/A2 四向图只能用于回收已完成朝向、清稿和缩放工作；若与上述三层冲突，冲突部分作失败派生，不得反向覆盖批准源。

## 3. BREAKER 的唯一组合责任源

### 3.1 Working 故事实体

- `ENEMY_C01_BREAKER`：Working／active；近30m地面突入壳，3×3；当前没有 Hard Art Lock。

### 3.2 用户已选轮廓

- 用户选择：`B可以`；
- B「前肢承重半直立型」；
- 身份板：`docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_identity_sheet_1800x1200.png`；
- 128样张：`docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_candidate_B_128.png`。

### 3.3 用户已选表面与结构关系

- 用户选择：`X 异质/生体装甲`；
- 用户对红缝—胸缝—封闭上背出口三处关系的决定：`保持`；
- 关系板：`docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/BREAKER_B1_surface_relation_board_1800x1100.png`；
- 正式回执：`docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-5/b1-user-approval-receipt.tsv`。

后续任务不是从文字重新想象 B＋X，而是把已选 B 的外轮廓／承重拓扑与 X 的表面语言合成同一张产品级地图 Sprite。

不得：

- 增删主要肢体、把前肢改成四条同构兽腿；
- 把短后稳定结构改成长后腿、足垫、爪兽或轮履；
- 改成贴地雪橇、装甲车、钻头壳、龟、猿或普通四足兽；
- 改动红缝、闭合胸缝和封闭上背出口的三处关系；
- 让 A9.1-A/A2/A3 失败派生成为新的责任源。

## 4. 新 P0｜只读已有稿复用审计

立即停止65号两张新图生成。P0改为只读审计，不使用 ImageGen，不修改既有美术文件。

必须回传：

1. 馆守 Z 现有稿清单：Hard／V10X／用户批准C／A8／A9.1-A／A9.1-A2，逐项标注“责任源／可直接复用／只可回收局部／失败派生”；
2. BREAKER 现有稿清单：用户批准B、X关系板、A8、A9.1-A、A9.1-A2、A9.1-A3，同样分级；
3. 明确推荐的零重设计生产链：哪一张负责外轮廓，哪一张负责身份细节，哪一张只负责画法或朝向；
4. 报告当前尚未落盘的临时 ImageGen 结果并确认不会继续消费。

完成即停，由制作人签来源冻结，不送用户重复选择已经批准的馆守 Z C 或 BREAKER B＋X。

## 5. 来源冻结后的正确 Pilot

制作人另行书面开放后，只能做“忠实转译 Pilot”：

- 馆守 Z：以用户批准 C 的轮廓／比例为不可变 mask，以 CML008＋V10X补身份细节，以 KINETIC_CEL完成线压和两级硬阴影；不得改变设计。
- BREAKER：以用户批准 B 的外轮廓和承重拓扑为不可变 mask，把批准 X 表面语言覆盖进去；不得重新解释身体。
- ImageGen若不能稳定保持不可变 mask，立即停止；不得靠继续重抽寻找“另一台更好看的机体”。
- 任何变化只允许：线条质量、色块归并、硬阴影、有限磨损、透明边、动作关节角和朝向投影。
- 任何变化不得涉及：头身比、主轮廓、肢体数量／类型、胸肩布局、主体比例、身份标志或B＋X三处结构关系。

Pilot先做批准源与输出的轮廓叠合；身份关键外轮廓和主关节偏差超过目标图3%即失败。机器误差通过仍不代替制作人实际像素审查。

## 6. 治理边界

本单不修改 Canon，不把批准方向样张升为 Runtime，不开放 A9.1-B、Atlas、Godot、exact handoff、G2-B或LibTV。

主程序继续冻结；美术先复用既有资产，不得以“最终资产还没做”为理由重开设计阶段。
