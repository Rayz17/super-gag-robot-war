# C01E02｜馆守Z V10X Q版谱系恢复与资产治理纠偏

> 日期：2026-08-19  
> 状态：`SOURCE_ROUTE_CURRENT / DIRECT_MAP_REUSE_SUPERSEDED_BY_76 / VISUAL_APPROVAL_NOT_GRANTED`  
> 触发：用户指出74号所呈现Q版为旧设计，并确认早前任务已生成最新设计的Q版  
> 覆盖：74号馆守Z结论及看板 `UGZ_EXISTING_CHIBI_BASELINE_REVIEW`

> **2026-08-19用途纠偏：** 本文件恢复的V10X Q谱系继续有效；第5.1节“直接裁成地图四向”的安排已被76号纠偏覆盖。该四视图是 `design_orthographic` 身份／结构参考，不是 `map_dimetric_40x20` Sprite。A9.1-A5裁切产物按视角前提失败保留为History WIP。

## 1. 制作人结论

用户判断正确。最新版馆守Z Q版没有丢失，也不是“尚未制作”；它已经落盘并有父图、用户限域回执、生成记录、透明派生和SHA清单闭环。

错误发生在生产路由：74号把美术方向manifest中的旧 `locked_reference_baselines` 误读为“当前最新版”，没有沿E02设计父图和SHA继续追溯。67号第36行其实已经登记最新版Q四向，74号仍抓回旧图，属于制作人审计失误，不是用户需要重新批准旧设计。

自本回执起：

- 撤销旧 `guardian_z_sprite_chibi.png` 的当前候选资格；
- 馆守Z不重画设计，不再以Blender、SVG、Python原语或C128可见像素替代最新版Q版；
- 恢复 `V10X → 同纸Q源 → 透明前向／四向` 为唯一当前Candidate Q生产链；
- 该链仍未获得UA91或Runtime批准，不能把“找回正确资产”冒充“最终Sprite已通过”。

## 2. 唯一正确谱系

| 层级 | 文件 | SHA-256 | 权威与用途 |
|---|---|---|---|
| Hard身份校准锚 | `.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png` | `a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521` | CML008 Hard；校准身份，不是最新版地图图 |
| E02最新设计父图 | `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png` | `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade` | 52号用户限域批准的C01E02裸机Demo Candidate派生母体；不晋级Hard/Runtime |
| V10X Q/SD同纸源 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/sources/guardian_z_v10x_qsd_turnaround_imagegen_v2.png` | `c701f3efa72301720117bae08b1479d704315c5a4de62034bf385263ea57f412` | 最新设计约4头身、同纸四向生成源；Candidate |
| 透明中间源 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/sources/guardian_z_v10x_qsd_turnaround_rgba.png` | `2afe2ff0ed254096cf6820cdfbc97e7e3cea5eace85e24187fc58f79168726c4` | 只做外部白底转Alpha；Candidate中间层 |
| 透明前向Q图 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_MASTER_FRONT_RGBA_1024.png` | `3303465975ccc726dc3ee4088c57e71cf6e1dfa0fd64a1241f57e48ea4d8da24` | 当前前向视觉审查母图；Candidate、非Runtime |
| 透明四向Q图 | `docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a-identity-style-scale-masters/delivery/GUARDIAN_Z_V10X_QSD_FOUR_DIRECTION_RGBA_2560x960.png` | `3873ed1ac32949f5ba2cdfbc334131b1a7d202124aaab1192d3211c0eb006ee9` | 当前四向继承与一致性审查源；Candidate、非Runtime |

正式闭环证据：52号限域用户回执、A9.1-A `generation-log.md`、`source-receipt.tsv`、`asset-manifest.tsv`，以及67号来源冻结第36行。旧任务聊天只作导航，不作为本纠偏权威。

## 3. 角色边界与明确排除

### 3.1 C方向的正确角色

`GZ_QSD_A1_candidate_C_128.png`（SHA `d72cfc…214e`）的用户原话为“C可以”，正式回执同时写明 `runtime_allowed=false`、`not_sprite_master`。它只约束约4.2头身、动作空间、地图占位与bottom-center注册点；不得再把其程序可见像素或exact mask当作最终绘画母版。

### 3.2 排除项

- 旧版 `guardian_z_sprite_chibi.png`，SHA `60352b…1038`：旧CML008时期高质量Q图，无V10X父链；History/reference only。
- A8 Python Sprite、A9.1-A2量化稿、A9.1-A3 Blender、分层SVG与R1透明PNG：仅保留失败工程证据、关节点或尺寸信息；不得覆盖V10X Q像素链。
- `series_style_guardian_z_q_candidate_v22.png` 等早于V10X且被用户否决的探索稿：History，不得回流。

## 4. 为什么会表现为“失忆”

1. 新美术任务按交接要求没有继承legacy聊天历史，这是有意隔离，不是文件丢失。
2. 本应替代聊天记忆的正式信息分散在Hard Art Lock、52号限域回执、A9.1-A manifest、67号冻结单和后续失败合同中。
3. 现有流程没有一个以“主体＋父SHA＋用户权限＋当前派生＋视觉状态”为键的单一入口。
4. 74号又把“locked reference baseline”误等同“latest identity master”；而该manifest第11行明确说这些review基线不替换人物／机体identity master。

因此：资产数量多、目录层级乱是真实治理缺陷；但本次正确链在磁盘上足够清楚，漏检仍是制作人责任。

## 5. 即刻生产安排

### 5.1 馆守Z：只做零重画继承预演

**本节已被76号覆盖，不再是当前派工。** 眼平正／侧／背turnaround缺少A4斜俯相机所需的顶面和缩短信息，裁切、缩放、bottom-center或二维倾斜都不能把它变成地图四向。下列步骤只保留为已执行过程记录，不得继续或进入UA91。

美术资产-2下一步只允许：

1. 校验本回执及资产谱系表的exact SHA；
2. 从 `330346…` / `3873…` 裁出既有方向，不新增可见像素，不做ImageGen、Blender、SVG或Python机体绘制；
3. 按既定map display scale与bottom-center注册点，制作50%／100%和A4实际地图放置审查板；
4. 列出可直接继承的方向、确实缺失的动作，以及软渐变／结构一致性问题；
5. 停在制作人实际像素预审，不生成Atlas、不写Runtime。

62号“保留A9.1-A当前V10X正面身份，不重新抽一台馆守Z”继续有效。若地图缩放后现有高质量像素已足够读，优先用Godot位移、倾斜、缩放、受击闪白、遮罩与FX表达动作；只有被Golden Turn镜头实际证明缺失的关键帧才进入局部二维清稿。

### 5.2 BREAKER：冻结，另走B＋X责任源

本纠偏不把馆守Z结论外推给BREAKER。BREAKER目前仍缺一张同时满足产品级质量与用户批准B＋X的可用母图；在独立来源谱系和单帧视觉门完成前，不得与馆守Z一起重画、批量扩方向或接Runtime。

## 6. 门禁

- UA91仍未开放；先过制作人对正确V10X Q资产的地图内视觉预审。
- A9.1-B、exact interface、signed handoff、G2-B继续冻结。
- 本回执不改Hard/Working Canon，不构成付费批量生成或Runtime晋级。
- 任何后续任务必须先读取 `c01e02-current-production-asset-lineage.tsv`，不得仅按文件名、最近任务号或聊天摘要选源。
