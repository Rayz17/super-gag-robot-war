---
id: "WL_B1_MOBILE_CHASSIS"
title: "移动底盘"
record_type: "wanji_location"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_locations.tsv"
generated: true
aliases:
  - "移动底盘"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-location"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 移动底盘

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WL_B1_MOBILE_CHASSIS`
- **记录类型：** `wanji_location`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属楼层：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WF_B1 移动底盘 _ 展舰机库脊柱|移动底盘 / 展舰机库脊柱]]
- **上级空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/locations/LOC_WANJI_MOBILE_CHASSIS 巡展舰体与外泊层|巡展舰体与外泊层]]
- **相连空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_HANGAR 展舰机库脊柱|展舰机库脊柱]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_MEDIUM_BERTHS 中型泊位列|中型泊位列]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_B1_HEAVY_SERVICE_RACK 重型维修架|重型维修架]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_EXT_LOCK_BERTH 外部锁泊甲板|外部锁泊甲板]]、[[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_EXT_FRONT 旧会展区入口|旧会展区入口]]

> [!note] 未解析引用
> 首次场景 `C01E04-05`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `location_id` | WL_B1_MOBILE_CHASSIS |
| `parent_floor_id` | WF_B1 |
| `parent_location_id` | LOC_WANJI_MOBILE_CHASSIS |
| `canonical_name` | 移动底盘 |
| `area_type` | chassis |
| `c01_access_state` | locked_until_c01e04 |
| `approx_position` | 万机馆底部 |
| `connected_locations` | WL_B1_HANGAR;WL_B1_MEDIUM_BERTHS;WL_B1_HEAVY_SERVICE_RACK;WL_EXT_LOCK_BERTH;WL_EXT_FRONT |
| `first_scene` | C01E04-05 |
| `gameplay_use` | 展舰启动;撤离;后续移动基地;外部锁泊供能 |
| `art_scale_anchor` | 液压支架;旧履带/悬浮底盘;启动钥匙;外部锁臂供能线 |
| `notes` | 万机馆转为流亡展舰的物理锚点；大型机随舰主要走外部锁泊或任务地会合。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_locations.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
