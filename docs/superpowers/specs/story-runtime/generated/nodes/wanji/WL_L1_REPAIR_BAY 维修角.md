---
id: "WL_L1_REPAIR_BAY"
title: "维修角"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "维修角"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 维修角

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_L1_REPAIR_BAY`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_L1 观众层 _ 主展层|观众层 / 主展层]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/locations/LOC_WANJI_REPAIR_BAY 维修角|维修角]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_MAIN_HALL 主展厅|主展厅]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_STAFF_CORRIDOR 员工内廊|员工内廊]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L2_RING_BRIDGE 二楼环形天桥|二楼环形天桥]]

> [!note] 未解析引用
> 首次场景 `C01E01-REPAIR-BAY`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_L1_REPAIR_BAY |
| `parent_floor_id` | WF_L1 |
| `parent_location_id` | LOC_WANJI_REPAIR_BAY |
| `canonical_name` | 维修角 |
| `area_type` | maintenance_zone |
| `c01_access_state` | limited_c01 |
| `approx_position` | 主展厅右后侧 |
| `connected_locations` | WL_L1_MAIN_HALL;WL_L1_STAFF_CORRIDOR;WL_L2_RING_BRIDGE |
| `first_scene` | C01E01-REPAIR-BAY |
| `gameplay_use` | 右臂选择;兜灯整备;战斗支援 |
| `art_scale_anchor` | 5m右前臂外装甲;维修台;工具灯 |
| `notes` | 删减胶带闲聊，集中右臂旧伤、保留/替换、安全锁。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
