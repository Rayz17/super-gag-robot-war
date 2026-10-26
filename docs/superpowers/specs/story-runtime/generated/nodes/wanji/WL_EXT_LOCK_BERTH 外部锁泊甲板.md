---
id: "WL_EXT_LOCK_BERTH"
title: "外部锁泊甲板"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "外部锁泊甲板"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 外部锁泊甲板

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_EXT_LOCK_BERTH`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_EXT 旧会展区外部|旧会展区外部]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/locations/LOC_WANJI_MOBILE_CHASSIS 巡展舰体与外泊层|巡展舰体与外泊层]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_MOBILE_CHASSIS 移动底盘|移动底盘]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_EXT_FRONT 旧会展区入口|旧会展区入口]]

> [!note] 未解析引用
> 首次场景 `C01E04-05`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_EXT_LOCK_BERTH |
| `parent_floor_id` | WF_EXT |
| `parent_location_id` | LOC_WANJI_MOBILE_CHASSIS |
| `canonical_name` | 外部锁泊甲板 |
| `area_type` | external_berth |
| `c01_access_state` | locked_until_c01e04 |
| `approx_position` | 展舰外侧/顶部/尾部伸缩泊位 |
| `connected_locations` | WL_B1_MOBILE_CHASSIS;WL_EXT_FRONT |
| `first_scene` | C01E04-05 |
| `gameplay_use` | 大型机锁泊;飞行机随航;外部补给;出击演出 |
| `art_scale_anchor` | 伸缩锁臂;磁锁;外部维修无人车;远景随航灯 |
| `notes` | 15米以上大型机可跟随万机馆，但不必全部进入馆体；战舰级单位仍以外部友舰或任务地会合存在。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
