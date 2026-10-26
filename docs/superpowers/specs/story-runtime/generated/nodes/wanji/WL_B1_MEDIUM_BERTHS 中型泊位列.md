---
id: "WL_B1_MEDIUM_BERTHS"
title: "中型泊位列"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "中型泊位列"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 中型泊位列

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_B1_MEDIUM_BERTHS`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_B1 移动底盘 _ 展舰机库脊柱|移动底盘 / 展舰机库脊柱]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/locations/LOC_WANJI_MOBILE_CHASSIS 巡展舰体与外泊层|巡展舰体与外泊层]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_HANGAR 展舰机库脊柱|展舰机库脊柱]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_MOBILE_CHASSIS 移动底盘|移动底盘]]

> [!note] 未解析引用
> 首次场景 `C01E04-01`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_B1_MEDIUM_BERTHS |
| `parent_floor_id` | WF_B1 |
| `parent_location_id` | LOC_WANJI_MOBILE_CHASSIS |
| `canonical_name` | 中型泊位列 |
| `area_type` | hangar_berth |
| `c01_access_state` | locked_until_c01e04 |
| `approx_position` | B1机库脊柱两侧 |
| `connected_locations` | WL_B1_HANGAR;WL_B1_MOBILE_CHASSIS |
| `first_scene` | C01E04-01 |
| `gameplay_use` | 2-12米机体常驻整备;改装;补给;支援派遣 |
| `art_scale_anchor` | 4-6个折叠泊位;地面锁具;侧向吊轨;维修臂 |
| `notes` | 用于解释工务机、现实机器和支援型机体随舰；不塞15米以上巨型机长期常驻。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
