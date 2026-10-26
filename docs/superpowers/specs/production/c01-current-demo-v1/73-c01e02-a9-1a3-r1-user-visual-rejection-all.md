# C01E02 A9.1-A3｜R1透明PNG用户视觉全退回执

> 日期：2026-08-19  
> 用户裁决：透明PNG“太丑了，跟设计稿相去甚远”  
> 状态：`USER_VISUAL_REJECTED_ALL / NO UA91 CANDIDATE / DOWNSTREAM FROZEN`

## 1. 裁决对象

用户已直接查看71号R1透明PNG，包括：

- `GUARDIAN_Z_C_SOUTH_IDLE_256-R1.png`；
- `BREAKER_BX_NORTH_CHARGE_READY_384-R1.png`。

用户裁决覆盖此前制作人对馆守Z“可能保留为用户候选”的预判。两张均不得进入UA91。

## 2. 正式结论

| 主体 | 用户视觉结论 | 当前权限 |
| --- | --- | --- |
| 馆守Z | 太丑，与已通过设计稿相去甚远 | 技术试验像素；不是母版，不是用户候选 |
| BREAKER | 太丑，与设计方向相去甚远 | 技术试验像素；不是母版，不是用户候选 |

71号R1的SVG、透明PNG、地图板与QA只保留为“程序化／矢量清稿路线失败证据”。`machine_pass_all=true`、IoU、bbox、pivot和hash不构成任何视觉价值或产品验收。

这不是Canon History迁移，也不是可回流的旧美术库；任何后续任务不得加载其可见像素作为最终或fallback Sprite。

## 3. 根因纠正

失败不是因为设计稿不足，而是生产方法偏离了设计稿：

1. 把用于方向／比例判断的低分C128与B128程序样张当成了可放大的美术母版；
2. 用手写SVG path继续复制程序几何，只能保住轮廓统计，无法保住高质量设计稿的体积、结构咬合、材质、线压与气质；
3. 机器门奖励了“像素边界相同”，却没有证明“画得像批准设计”；
4. 因而产物即使技术完整，视觉上仍是扁平、僵硬的程序拼装图。

正式冻结：

```text
approved design art != low-resolution direction schematic
silhouette IoU != design fidelity
editable SVG != production-quality Sprite master
```

## 4. 立即停止

- 馆守Z与BREAKER两张R1全部视觉退回；
- 不开R2/R3，不继续修这两份SVG；
- 不再用Python、Blender、SVG程序几何或整机ImageGen重画；
- 不送UA91，不扩方向／状态／Atlas；
- 不启动A9.1-B、exact handoff、Godot、LibTV或G2-B；
- 原主程序继续冻结。

## 5. 下一步仅做只读复用审计

在任何新美术写入前，制作人先从当前工作区核对已有高质量设计稿、透明图、三视／多视图与姿态稿：

1. 区分Hard／Working／Candidate与失败派生；
2. 找出可直接抠图、裁切、缩放或作局部像素编辑的已有高质量像素；
3. 明确真正缺少的方向和状态，不因缺一张图而重画整个设计；
4. 形成带绝对路径、SHA、用途和禁止项的最小复用清单；
5. 清单经制作人核验后，再决定是直接复用、局部人工2D编辑，还是确实需要补画。

该审计为只读，不构成新生成授权、人工外包授权或付费工具授权。

