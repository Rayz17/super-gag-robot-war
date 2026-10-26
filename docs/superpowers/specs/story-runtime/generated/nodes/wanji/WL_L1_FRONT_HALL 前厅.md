---
id: "WL_L1_FRONT_HALL"
title: "前厅"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "前厅"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 前厅

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_L1_FRONT_HALL`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_L1 观众层 _ 主展层|观众层 / 主展层]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/locations/LOC_WANJI_MUSEUM 万机馆|万机馆]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_EXT_FRONT 旧会展区入口|旧会展区入口]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_MAIN_HALL 主展厅|主展厅]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_ARCHIVE_ROOM 档案室|档案室]]

> [!note] 未解析引用
> 首次场景 `C01E01-ADV`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_L1_FRONT_HALL |
| `parent_floor_id` | WF_L1 |
| `parent_location_id` | LOC_WANJI_MUSEUM |
| `canonical_name` | 前厅 |
| `area_type` | public_hub |
| `c01_access_state` | open_c01 |
| `approx_position` | L1南侧入口 |
| `connected_locations` | WL_EXT_FRONT;WL_L1_MAIN_HALL;WL_L1_ARCHIVE_ROOM |
| `first_scene` | C01E01-ADV |
| `gameplay_use` | 移动教程;闭馆清单;观众滞留;卷帘门锁死 |
| `art_scale_anchor` | 服务台;纪念章台;等待黄线;卷帘门 |
| `notes` | 小满和阿澄在这里等待离馆，不是默认跟随主角队列。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
