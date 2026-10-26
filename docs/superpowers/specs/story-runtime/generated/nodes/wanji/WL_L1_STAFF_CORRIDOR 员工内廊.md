---
id: "WL_L1_STAFF_CORRIDOR"
title: "员工内廊"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "员工内廊"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 员工内廊

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_L1_STAFF_CORRIDOR`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_L1 观众层 _ 主展层|观众层 / 主展层]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/locations/LOC_WANJI_MUSEUM 万机馆|万机馆]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_ARCHIVE_ROOM 档案室|档案室]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_REPAIR_BAY 维修角|维修角]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_ZERO_GATE 0号侧廊门口|0号侧廊门口]]

> [!note] 未解析引用
> 首次场景 `C01E01-ADV`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_L1_STAFF_CORRIDOR |
| `parent_floor_id` | WF_L1 |
| `parent_location_id` | LOC_WANJI_MUSEUM |
| `canonical_name` | 员工内廊 |
| `area_type` | staff_corridor |
| `c01_access_state` | limited_c01 |
| `approx_position` | 档案室与维修后场之间 |
| `connected_locations` | WL_L1_ARCHIVE_ROOM;WL_L1_REPAIR_BAY;WL_L1_ZERO_GATE |
| `first_scene` | C01E01-ADV |
| `gameplay_use` | 引导纪存独自去0号侧廊 |
| `art_scale_anchor` | 窄走廊;员工灯;禁入牌 |
| `notes` | 孩子不能跟到0号侧廊门口。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
