---
id: "WL_L1_FAR_STAR_REPLY_CASE"
title: "延迟回信副柜"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "延迟回信副柜"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 延迟回信副柜

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_L1_FAR_STAR_REPLY_CASE`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_L1 观众层 _ 主展层|观众层 / 主展层]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_OLD_VIDEO 旧影像厅|旧影像厅]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_OLD_VIDEO 旧影像厅|旧影像厅]]

> [!note] 未解析引用
> 首次场景 `C01E01-FARSTAR-REPLY-CACHE`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_L1_FAR_STAR_REPLY_CASE |
| `parent_floor_id` | WF_L1 |
| `parent_location_id` | WL_L1_OLD_VIDEO |
| `canonical_name` | 延迟回信副柜 |
| `area_type` | read_only_signal_case |
| `c01_access_state` | open_c01 |
| `approx_position` | 旧影像厅出口 |
| `connected_locations` | WL_L1_OLD_VIDEO |
| `first_scene` | C01E01-FARSTAR-REPLY-CACHE |
| `gameplay_use` | 读取L3离线缓存;吐出空白回信;纪存编号错闪 |
| `art_scale_anchor` | 窄型旧终端柜;纸张出口;只读灯;无回复键 |
| `notes` | 第一章只读取L3远星观测廊离线缓存元数据；无实时通信、导航或当前远星政治信息。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
