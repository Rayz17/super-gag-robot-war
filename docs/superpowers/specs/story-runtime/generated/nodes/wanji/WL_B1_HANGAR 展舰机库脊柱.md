---
id: "WL_B1_HANGAR"
title: "展舰机库脊柱"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "展舰机库脊柱"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 展舰机库脊柱

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_B1_HANGAR`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_B1 移动底盘 _ 展舰机库脊柱|移动底盘 / 展舰机库脊柱]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/locations/LOC_WANJI_MOBILE_CHASSIS 巡展舰体与外泊层|巡展舰体与外泊层]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_MOBILE_CHASSIS 移动底盘|移动底盘]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_MEDIUM_BERTHS 中型泊位列|中型泊位列]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_HEAVY_SERVICE_RACK 重型维修架|重型维修架]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_L1_REPAIR_BAY 维修角|维修角]]

> [!note] 未解析引用
> 首次场景 `C01E04-01`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_B1_HANGAR |
| `parent_floor_id` | WF_B1 |
| `parent_location_id` | LOC_WANJI_MOBILE_CHASSIS |
| `canonical_name` | 展舰机库脊柱 |
| `area_type` | hangar |
| `c01_access_state` | locked_until_c01e04 |
| `approx_position` | 主展厅地下 |
| `connected_locations` | WL_B1_MOBILE_CHASSIS;WL_B1_MEDIUM_BERTHS;WL_B1_HEAVY_SERVICE_RACK;WL_L1_REPAIR_BAY |
| `first_scene` | C01E04-01 |
| `gameplay_use` | 馆守Z维修;中型机体常驻;出击准备;资源取舍 |
| `art_scale_anchor` | 半躺维修架;机库灯;大型工具车;吊轨;货运升降台 |
| `notes` | C01E04后成为基地整备层；B1可支撑机战母舰功能，但不能无限容纳战舰级单位。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
