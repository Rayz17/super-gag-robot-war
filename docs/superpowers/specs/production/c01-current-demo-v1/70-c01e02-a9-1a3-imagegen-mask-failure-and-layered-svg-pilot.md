# C01E02 A9.1-A3｜整机ImageGen结构约束失败与分层SVG清稿Pilot

> 日期：2026-08-19  
> 状态：`producer correction active / ImageGen whole-body edit frozen / layered SVG pilot assigned`  
> 上游：69号两张忠实清稿Pilot  
> 边界：Candidate only；不开放Atlas、Godot、Runtime、G2-B或UA91。

## 1. 69号实际结果与制作人裁决

实际证据：

- `art-a9-1a3-faithful-cleanup-pilot/GUARDIAN_Z_IMAGEGEN_EDIT_ATTEMPT_RAW_RGB_1254.png`；
- `art-a9-1a3-faithful-cleanup-pilot/SILHOUETTE_MASK_OVERLAY_1920x1080.png`；
- `art-a9-1a3-faithful-cleanup-pilot/completion-report.md`。

机器与实际像素共同显示：

- 返回`1254×1254 RGB`，无alpha，棋盘格烘进像素；
- 批准C mask归一化宽／高约`0.797／0.945`，生成主体约`0.568／0.891`；
- 直接轮廓IoU约`0.556`，批准mask内保守内容覆盖仅`59%`；
- 肩、前臂、髋、脚和内部装甲均重新布局；后裁mask只能令外部alpha为0，不能补回错位内容。

裁决：

```text
ImageGen visual finish = promising donor only
exact body fidelity = FAIL
faithful cleanup pilot = FAIL
Guardian calls = 1
Guardian rerolls = 0
BREAKER calls = 0
whole-body ImageGen production route = frozen
```

不得把这张“更精致但更窄的新身体”当馆守Z新设计；它只保留为失败证据，不参与当前SVG身体构建。

## 2. 纪存旧走动案例的正确复用边界

旧纪存走动由一次ImageGen生成右向四帧条带，Python只去绿幕，Godot切四帧并水平镜像左向。它证明：

- Sprite条带、切帧、镜像、pivot和移动状态机是可行工程方法；
- 小地图尺寸下少量帧即可形成基础运动感。

它没有证明：

- 四方向、攻击／受击／蓄力／接触等多状态；
- 机体跨帧身份、拓扑和比例严格一致；
- 旧像素符合当前CML001／CML008／CML128或可进入Runtime。

因此本轮只复用“Sprite消费架构”，不复用旧纪存像素，也不复用“一次生成整条”的美术方法。

## 3. 新路线：零ImageGen、零Blender的手工分层SVG

馆守ZC和BREAKER B的原始生产脚本已经把主体拆成显式2D几何组件：

- `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/generate_g15_a1.py`；
- `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/generate_breaker_b1.py`。

新Pilot不运行这些脚本去“画新机体”，而是把其中已经获批C／B的组件关系人工转写为分层SVG path，在同一轮廓内手修贝塞尔、遮挡、线压和硬阴影。Python只允许做SVG渲染、尺寸、alpha、bbox、pivot、hash和排板QA。

## 4. 唯一任务：两张分层SVG单帧Pilot

### 4.1 写入范围

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-layered-svg-pilot/**`

### 4.2 必交主文件

1. `GUARDIAN_Z_C_SOUTH_IDLE_MASTER.svg`；
2. `GUARDIAN_Z_C_SOUTH_IDLE_256.png`；
3. `BREAKER_BX_NORTH_CHARGE_READY_MASTER.svg`；
4. `BREAKER_BX_NORTH_CHARGE_READY_384.png`。

只做这两张，不做其他方向、动作条或Atlas。

## 5. 组件与责任源

### 5.1 馆守Z SVG命名层

- `silhouette_guard`；
- `helmet_crown_face`；
- `shoulder_ring_left/right`；
- `chest_left/right`、`center_spine_core`；
- `upper_arm_left/right`；
- `cyl_forearm_left/right`、`wrist_hand_left/right`；
- `pelvis`、`thigh_left/right`、`shin_left/right`、`foot_left/right`；
- `e02_right_shoulder_old_damage`；
- `hard_shadow_1`、`hard_shadow_2`、`accent_highlight`。

责任：C128锁约4.2头身与大轮廓；CML008锁身份；V10X锁E02双臂裸机细节；A9.1-A/A2只捐不改变身体的色块、侧背局部和线压。

### 5.2 BREAKER SVG命名层

- `silhouette_guard`；
- `high_back_shell`；
- `x_bio_plate_01..07`；
- `low_head_single_red_slit`；
- `closed_chest_seam`；
- `sealed_upper_back_exit`；
- `forelimb_left/right`、`wrist_claw_left/right`；
- `short_rear_stabilizer_left/right`；
- `hard_shadow_1`、`hard_shadow_2`、`accent_red`。

责任：B身份板/B128锁身体与承重拓扑；X关系板锁表面及三处封闭关系；A9.1-A只捐壳片、暗材质、红缝局部；A9.1-A2只捐KINETIC_CEL画法，不捐雪橇身体。

## 6. 固定画布、bbox与pivot

| 主体 | frame | 目标alpha bbox | pivot | footprint |
| --- | ---: | ---: | ---: | ---: |
| 馆守Z | 256×256 | 204×242 | 128,254 | 2×2 |
| BREAKER | 384×384 | 318×330 | 192,348 | 3×3 |

- mask外像素必须为0；
- 相对批准C/B轮廓IoU目标`≥0.96`；
- bbox中心与pivot漂移`≤1px`；
- E/W镜像、后视和动作均不在本轮。

## 7. KINETIC_CEL完成度门

- 深墨蓝主线；轮廓／承重边粗，内部分件线细；
- 每主体4–7个主色块，最多两级硬阴影；
- 用独立shadow path形成体积，不使用PBR软渐变或噪声贴图；
- 保留有限手工不对称、装甲咬合与遮挡，不得继续堆圆角矩形／基础原语；
- 馆守Z在50%显示仍读出冠、银脸栅、红X胸、金核、双圆柱前臂；
- BREAKER在50%显示仍读出高背、单红缝、前肢承重、短后稳定、异质叠片。

SVG技术通过但第一眼仍像程序图标、剪贴画或低模，则视觉失败。

## 8. 必交证据

1. `SVG_LAYER_AND_SOURCE_BOARD_1920x1080.png`：命名层与责任源；
2. `SVG_SILHOUETTE_OVERLAY_1920x1080.png`：批准mask／SVG alpha叠合；
3. `SVG_PILOT_ON_A4_MAP_1280x720.png`：256／384实际显示；
4. `SVG_PILOT_50_100_REVIEW_1920x1080.png`：50%／100%身份与画法；
5. `layer-spec.tsv`、`source-lock.tsv`、`visual-self-review.md`、`delivery-hashes.sha256`、`completion-report.md`。

## 9. 停止门与DAG

任一主体身份、比例、KINETIC_CEL或地图第一读法失败，立即停；不得扩方向、动作或Runtime。

两张均过制作人实际像素预审后，才按稀疏矩阵扩：

- 馆守Z先补N/E/W idle，再只为Golden Turn实用方向扩`step_a/step_b/brace/recoil`；
- BREAKER先保持north的`idle/charge/contact`，其他方向先只做idle；
- 右肩旧伤与X非对称叠片不可盲目镜像。

A9.1-B、UA91、exact handoff、G2-B与LibTV继续冻结。
