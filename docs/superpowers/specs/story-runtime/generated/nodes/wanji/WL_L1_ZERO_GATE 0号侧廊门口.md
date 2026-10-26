---
id: "WL_L1_ZERO_GATE"
title: "0号侧廊门口"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "0号侧廊门口"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 0号侧廊门口

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_L1_ZERO_GATE`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_L1 观众层 _ 主展层|观众层 / 主展层]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/locations/LOC_ZERO_CORRIDOR 0号侧廊|0号侧廊]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_MAIN_HALL 主展厅|主展厅]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_STAFF_CORRIDOR 员工内廊|员工内廊]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B2_ZERO_DEEP 0号侧廊深处|0号侧廊深处]]

> [!note] 未解析引用
> 首次场景 `C01`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_L1_ZERO_GATE |
| `parent_floor_id` | WF_L1 |
| `parent_location_id` | LOC_ZERO_CORRIDOR |
| `canonical_name` | 0号侧廊门口 |
| `area_type` | sealed_gate |
| `c01_access_state` | door_only_c01 |
| `approx_position` | 主展厅后侧无声区域 |
| `connected_locations` | WL_L1_MAIN_HALL;WL_L1_STAFF_CORRIDOR;WL_B2_ZERO_DEEP |
| `first_scene` | C01 |
| `gameplay_use` | 旧地图矛盾;纪存异常感;深潜未来入口 |
| `art_scale_anchor` | 窄门;旧封条;不反光材质;可辨认的普通物理痕迹 |
| `notes` | C01只到门口，不解释封闭原因；是否出现声音、终端缺页或其他异常由当前L4决定。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
