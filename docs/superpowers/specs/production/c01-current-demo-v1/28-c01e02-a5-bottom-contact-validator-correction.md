# C01E02 A5 双足接地校验修正

> Status: `producer_technical_correction / additive_to_27`
>
> Creative impact: `none`
>
> Lifecycle boundary: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 1. 问题与证据

已获批准的源图：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a3-rift-swarm-qsd/samples/A3_A_east_96_review.png`

SHA-256：`66ab008651b84f799d3c9cf7e1df7c8d9c9a0e21a5b248fca83d3f5fa37dc03a`

其底边存在 29 个非透明接触像素，接触包络为 `x=32..64`，跨过 `bottom_center x=48`；但 `x=48` 本身是双足之间的一像素透明缝。造型符合 A5 目标“接地点落在帧底边、pivot 为 bottom_center”，现有生成器与 validator 却错误要求底边正中心像素必须非透明，因此把合法双足造型误判为失败。

## 2. 获准修正

只允许修改：

- `art-a5-rift-swarm-four-facing-atlas/generate_art_a5_rift_swarm_four_facing_atlas.py`
- `art-a5-rift-swarm-four-facing-atlas/validate_art_a5_rift_swarm_four_facing_atlas.py`

把两处旧条件：

```text
底边正中心像素必须非透明
```

统一替换为：

```text
底边必须存在至少一个非透明接触像素；
底边非透明接触包络必须跨过 bottom_center；
不要求双足之间的 bottom_center 像素本身着色。
```

推荐实现为先取得底边一行的 alpha bounding box，并同时检查：

```text
bottom_contact_bbox is not None
bottom_contact_bbox.left <= size // 2 < bottom_contact_bbox.right
```

仍须保留 `alpha bbox bottom == frame size`、左右边缘透明、顶部透明、红缝检查及逐帧像素直贴验证。

## 3. 边界

- 不重画、裁切、平移或修补 A3 已批准源图。
- 不改变 `pivot=0.5,1.0`、`footprint=1,1`、四朝向顺序或 96/128px atlas 规格。
- 不放宽为悬空造型；底边无接触或接触包络完全偏在中心一侧仍必须失败。
- 不修改 Godot、Runner、R2 manifest、Canon、A4 或 Runtime。
- 将本修正文件及其 SHA 纳入 A5 `source-validation-receipt.tsv`。

本修正不新增用户创作决策。完成 A5 包后仍按 25号目标停在用户选择 96px/128px 的原裁决门。
