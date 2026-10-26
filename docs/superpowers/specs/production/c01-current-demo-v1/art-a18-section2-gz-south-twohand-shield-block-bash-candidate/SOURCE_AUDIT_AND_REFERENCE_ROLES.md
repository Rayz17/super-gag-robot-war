# A18 馆守 Z Camera V2 south 双手持盾动作：来源审计与参考角色

> **SUPERSEDED SOURCE ROUTE / HISTORY ONLY（2026-08-24）：** 130 号已锁定 V10X 为 C01E02 Demo 唯一正向身份派生母图；本包的最终 raw 仍因 Camera V2 south、BASH 首读和 alpha 失败而禁止复用。本文不得作新 Section 2 的来源锁；新任务必须读取 `c01e02-guardian-z-scoped-source-lock-v1.tsv`。

Date: 2026-08-23  
Lane: `Candidate / user=false / runtime=false / canon=false`  
Scope: 仅生成一张含 `R2 BLOCK` 与 `R3 BASH` 的两姿态透明候选；不接 Godot，不迁移 Canon。

## Canon / Reader 入门核对

- 已运行 `python3 scripts/report_v35_layered_pipeline.py --check`，并查询 `MECHA_GUARDIAN_Z`、`V353U001` 与 C01 story chain。
- Current C01E02 Reader：馆守 Z 为 18m；此段发生在原右前臂于 E03 损失之前，因此两个姿态都必须保留两条完整原装手臂。Reader 明示退役重盾被从展位取下、立在身前承受赤红冲击并留下第四道焦痕、随后以盾角推进撞击。动作事实见：
  - `docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/story/C01E02-纯剧情Reader-v2.md:121-149`
  - 合章对应 `docs/superpowers/specs/story-runtime/effect-tests/C01-story-gameplay-separation-2026-08-07/C01-纯剧情章节Reader-v2.md:301-329`
- Reader 的取盾句写的是左手先扯出，之后写左手仍握盾柄；本 A18 的“两手同时承力”是已确认的 Demo 地图动作表达约束，不反写为 Reader/Canon 新事实。故本包保持 Candidate。

## 允许输入与唯一角色

| Ref | 路径 / SHA-256 | 允许角色 | 禁止外推 |
|---|---|---|---|
| GZ-PRIMARY | `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`  
`e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade` | 馆守 Z 的用户认可 C01E02 身份父稿；头部、胸甲、海军蓝/红/白/金配色、两条完整等构圆柱前臂 | 原图近眼平视，不提供 map south 透视；白底不得继承 |
| GZ-STRUCTURE | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png`  
`3873ed1ac32949f5ba2cdfbc334131b1a7d202124aaab1192d3211c0eb006ee9` | 当前 V10X/Q-SD 身份、约 4.2 头身地图可读比例、正侧背结构一致性 | 四视图是设计正投影，不等于 Camera V2 cardinal；不直接裁作 Sprite |
| SHIELD-ONLY | `docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`  
`169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305` | **唯一盾视觉源**：盾冠、中央承力脊、厚金属边、背面双竖握把与前臂承力轨、蓝白金配色、三条旧宽浅擦压痕、第四条赤红热痕 | 不得改成装甲板、三孔板、枪炮、背盾或漂浮道具；输入图背景不继承 |
| GZ-CALIBRATION-ONLY | `.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`  
`a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521` | Hard 身份校准锚，仅用于审计“仍是馆守 Z” | 不作为本次像素输入；不覆盖用户后续认可的 V10X/Q-SD 父稿 |

## 明确禁用源

- 旧 A13 持盾姿态稿及其任何裁切、重绘或像素继承。
- 旧 A2 三孔板、弹坑板、带弹孔装甲板。
- 当前近正面 east runtime 候选；它不是 south 动作源。
- `guardian_z_sprite_chibi.png`、A9.1-A3 SVG R1、Blender/rig 分支，以及任何被退回的旧/错误馆守 Z。
- 墙架、展位、地面、城市、枪炮、BREAKER、其他机体、文字与 UI。

## Camera V2 与构图合同

- 固定平行 dimetric：约 45° azimuth、30° elevation，从 southeast 看向 northwest；可见头顶、肩甲、前臂与盾顶厚度。
- 角色逻辑朝 south；本任务的屏幕前向向量为 `[-40,+24]`，即从躯干朝屏幕左下。
- south 必须是抬高的 3/4：读到正面胸甲与一侧体块，不得退回 design front / eye-level / 纯侧视。
- 单张横向透明板，两栏等尺度、同一机体、同一面盾；完整脚底与 bottom-center footpoint 均不裁切。

## 两个姿态与硬门

| Pose | 必须读到 | 硬失败 |
|---|---|---|
| `R2 BLOCK` | 两脚扎地、身体在盾后；盾竖直位于胸腹正前；两条完整手臂分别通向盾背左右握把，双手都真实包住握把/盾缘；盾面带三条旧擦压痕与第四条新热痕 | 背盾、单手、手未接触、手臂消失、盾漂浮、盾在侧后、近正面 eye-level |
| `R3 BASH` | 与 R2 同一 south 朝向；两手仍牢握背面双把，髋肩扭转、盾体横向扫向屏幕左下，强化厚边成为接触侧；动作由全身重心推动 | 改成拳击、单手挥盾、盾脱手、用背扛盾、纯推盾、额外武器、改变机体/盾设计 |

任何一项硬门失败：`VISUAL_FAIL_STOP`，封存本次原图，0 reroll；不以修图、抠图或版式包装掩盖失败。

## ImageGen 输入顺序

1. `GZ-PRIMARY`：馆守 Z 身份主参考。
2. `GZ-STRUCTURE`：Q/SD 比例与四向结构辅助。
3. `SHIELD-ONLY`：唯一盾视觉参考。

本文件在 ImageGen 调用前建立，作为本次唯一 reference-role 清单。

## 调用后权威纠正（2026-08-23）

后续 Current authority 复核确认：本次实际输入的 `GZ-PRIMARY`（`guardian_z_collector_e02_lockframe_candidate_v10x.png`）自身仍为 `approved=false`，不能替代 CML008 `Hard / locked_current` 的馆守 Z 身份锚。因此上表把它称为“用户认可身份父稿”是不正确的，本次调用另增一项 `SOURCE_AUTHORITY_FAIL`，整批永久封存。

今后唯一允许作为馆守 Z Current 身份像素输入的是：

`/Users/rayz/Documents/超gag机器人大战/.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`

SHA-256：`a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521`。

旧 `GZ-PRIMARY` 与 `GZ-STRUCTURE` 只能留作本次失败沿革，不得再用于后续持盾生成；A17 raw 仍是唯一获用户批准的盾牌设计基底。
