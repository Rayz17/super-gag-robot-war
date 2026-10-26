# C01E02 A9.1-A3｜R0既有稿复用制作人审查与R0.1显示尺度对照

> 日期：2026-08-19  
> 状态：`producer reviewed / source reuse PASS / scale FAIL-DEFERRED / no master approval`  
> 上游：67号来源冻结及`art-a9-1a3-existing-source-reuse-r0/**`  
> 边界：Candidate only；不开放新设计、ImageGen、最终Sprite、Atlas、Godot、Runtime或G2-B。

## 1. 制作人实际像素审查

已直接查看：

- `art-a9-1a3-existing-source-reuse-r0/R0_EXISTING_APPROVED_SOURCES_ON_A4_MAP_1280x720.png`；
- `art-a9-1a3-existing-source-reuse-r0/R0_SOURCE_ROLE_BOARD_1920x1080.png`；
- 两张exact批准样张及`completion-report.md`。

审查结论：

| 门 | 结论 | 制作人判断 |
| --- | --- | --- |
| 既有设计来源复用 | `PASS` | 馆守Z清楚回到`CML008 + V10X + 用户C`；BREAKER清楚回到`用户B + X + 三处关系保持`，无需再设计 |
| exact副本 | `PASS` | C128与B128均保持源SHA，不存在暗改轮廓 |
| 设计身份 | `PASS_FOR_NEXT_MECHANICAL_STEP` | 两者第一读法与已选方向一致；此结论不是最终美术完成度通过 |
| 18m／近30m显示尺度 | `FAIL_DEFERRED` | 两张源均为128画布；BREAKER alpha为106×110，馆守Z为102×121，原生1:1无法证明巨体压迫感 |
| KINETIC_CEL最终清稿 | `NOT_REVIEWED` | R0被要求零重画，本轮没有也不应产生最终清稿 |
| Runtime／UA91 | `BLOCKED` | 没有最终单帧、四向、动作或exact handoff |

制作人裁决：

```text
existing_designs_are_sufficient = true
redesign_needed = false
display_scale_calibration_needed = true
final_sprite_cleanup_needed = true
```

## 2. 立即派工：R0.1 deterministic display-scale sweep

### 2.1 目的

只回答“同一获批轮廓在地图上应显示多大”，不回答“重新长什么样”。不得借尺度校准改造身体。

### 2.2 唯一写入范围

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-existing-source-reuse-r0-1-scale/**`

### 2.3 固定输入

- 馆守Z：67号exact `GUARDIAN_Z_C128_APPROVED_EXACT.png`，SHA `d72cfc1873da2d89bc22d867536b3d73547fc17d4ed154c40fec26a5fd71214e`；
- BREAKER：67号exact `BREAKER_B128_APPROVED_EXACT.png`，SHA `e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4`；
- 地图：A4 central viewport，SHA `b8ccc9b6eefb802b929a6d674e668611c6d9a88e123e24a2991710ae7e5f4ea9`。

### 2.4 唯一比较档

- 馆守Z固定：源128 → frame 256，整数2.0× nearest-neighbor，只作尺度代理；
- BREAKER A：源128 → frame 320，整数／分数确定性nearest-neighbor；
- BREAKER B：源128 → frame 384；
- BREAKER C：源128 → frame 448。

这里的`frame`是比较画布，不是最终Atlas合同。不得裁掉alpha bbox，不得改变宽高比，不得单独移动头、壳、肢体或重心。

### 2.5 必交物

1. `R0_1_SCALE_SWEEP_A4_3840x720.png`：三段相同A4地图，馆守Z固定256，BREAKER分别320／384／448；bottom-center注册一致；
2. `R0_1_SCALE_DECISION_BOARD_1920x1080.png`：并排展示三档alpha bbox、2×2／3×3占位、遮挡与第一读法；
3. `scale-sweep.tsv`：源尺寸、源bbox、目标frame、实际缩放倍数、目标bbox、pivot、footprint、lane occlusion notes；
4. `delivery-hashes.sha256`与`completion-report.md`。

### 2.6 硬禁区

- ImageGen、Blender、重画、paint-over、补细节、描边、锐化、去噪、色彩修改均为0；
- 不读取或消费此前临时generated_images；
- 不把nearest-neighbor放大图称为最终美术；
- 不写Atlas、Godot、Runtime、LibTV、Canon，不git add／commit。

### 2.7 制作人选择标准

- BREAKER第一眼显著大于馆守Z并能承担近30m／3×3压迫感；
- 不因过大遮死道路、保护对象、炮线或关键格；
- 低头单红缝、前肢承重、高背壳仍可读；
- 两者bottom-center与footprint相容；
- 选择只冻结显示尺寸，不改变设计与Canon。

完成即停。制作人查看三档实际PNG后选择一个显示尺寸，再单独开放馆守Z`south idle`与BREAKER`north charge-ready`两张忠实清稿Pilot。

## 3. DAG边界

```text
R0 source reuse PASS
→ R0.1 display scale selection
→ two single-frame faithful-cleanup pilots
→ producer visual preflight
→ UA91
```

A9.1-B、exact handoff、G2-B与LibTV继续冻结。
