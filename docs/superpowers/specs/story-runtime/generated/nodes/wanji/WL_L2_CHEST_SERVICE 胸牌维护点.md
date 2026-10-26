---
id: "WL_L2_CHEST_SERVICE"
title: "胸牌维护点"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "胸牌维护点"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 胸牌维护点

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_L2_CHEST_SERVICE`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_L2 环形天桥 _ 胸牌维修层|环形天桥 / 胸牌维修层]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_GUARDIAN_Z_PLINTH 馆守Z主展位|馆守Z主展位]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L2_RING_BRIDGE 二楼环形天桥|二楼环形天桥]]

> [!note] 未解析引用
> 首次场景 `C01E01-REPAIR-BAY`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_L2_CHEST_SERVICE |
| `parent_floor_id` | WF_L2 |
| `parent_location_id` | WL_L1_GUARDIAN_Z_PLINTH |
| `canonical_name` | 胸牌维护点 |
| `area_type` | maintenance_point |
| `c01_access_state` | visible_limited_c01 |
| `approx_position` | 馆守Z胸牌附近 |
| `connected_locations` | WL_L2_RING_BRIDGE |
| `first_scene` | C01E01-REPAIR-BAY |
| `gameplay_use` | 胸牌亮起;旧守护者回本体前置 |
| `art_scale_anchor` | 巨大胸牌灯;维修吊篮;安全锁面板 |
| `notes` | 胸牌亮不等于馆守Z完全站起。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
