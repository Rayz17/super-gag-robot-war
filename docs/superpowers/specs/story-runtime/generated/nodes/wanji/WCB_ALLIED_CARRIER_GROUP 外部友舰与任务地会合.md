---
id: "WCB_ALLIED_CARRIER_GROUP"
title: "外部友舰与任务地会合"
record_type: "wanji_berth"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv"
generated: true
aliases:
  - "外部友舰与任务地会合"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-berth"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 外部友舰与任务地会合

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WCB_ALLIED_CARRIER_GROUP`
- **记录类型：** `wanji_berth`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_EXT_LOCK_BERTH 外部锁泊甲板|外部锁泊甲板]]

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `berth_id` | WCB_ALLIED_CARRIER_GROUP |
| `canonical_name` | 外部友舰与任务地会合 |
| `parent_location_id` | WL_EXT_LOCK_BERTH |
| `capacity_type` | allied_carrier |
| `size_range` | 50m以上 |
| `can_host` | 白舰;舞台战舰;逃亡舰;远征舰;城市级巨构 |
| `cannot_host` | 馆内常驻;L1展陈;B1泊位 |
| `c01_state` | locked_until_story_join |
| `story_unlock` | C05后按章节会合 |
| `gameplay_use` | 母舰支援;地图兵器;撤退路线;舰队调度 |
| `art_scale_anchor` | 远景编队;通讯舰桥;地图边缘支援光标 |
| `notes` | 万机馆是主基地，不是唯一母舰；战舰级单位应保留自身空间感。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
