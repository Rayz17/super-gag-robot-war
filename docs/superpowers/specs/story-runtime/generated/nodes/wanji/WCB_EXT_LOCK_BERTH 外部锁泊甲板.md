---
id: "WCB_EXT_LOCK_BERTH"
title: "外部锁泊甲板"
record_type: "wanji_berth"
authority: "hard"
lifecycle: "active"
version_scope: "stable_spatial_or_interface_anchor"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv"
generated: true
aliases:
  - "外部锁泊甲板"
tags:
  - "story-runtime/current"
  - "story-runtime/wanji-berth"
  - "canon/hard"
  - "story-runtime/wanji"
---

# 外部锁泊甲板

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `WCB_EXT_LOCK_BERTH`
- **记录类型：** `wanji_berth`
- **权威：** `hard` / `active`
- **版本范围：** `stable_spatial_or_interface_anchor`

## 关系

- **所属空间：** [[docs/superpowers/specs/story-runtime/generated/nodes/wanji/WL_EXT_LOCK_BERTH 外部锁泊甲板|外部锁泊甲板]]

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `berth_id` | WCB_EXT_LOCK_BERTH |
| `canonical_name` | 外部锁泊甲板 |
| `parent_location_id` | WL_EXT_LOCK_BERTH |
| `capacity_type` | external_berth |
| `size_range` | 15-30m;飞行机;外部随航 |
| `can_host` | 大型超级机器人;飞行机;临时随航单位;大型武装包 |
| `cannot_host` | 需要密闭机库的战舰级单位;无法暴露的高风险核心 |
| `c01_state` | locked_until_c01e04 |
| `story_unlock` | C01E04展舰驶离后可见 |
| `gameplay_use` | 出击演出;补给;随航维修;大型单位待机 |
| `art_scale_anchor` | 展舰外侧/顶部/尾部伸缩锁臂;磁锁;维修无人车 |
| `notes` | 大型机体可以跟着万机馆走，但不必全塞进馆体。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/wanji_carrier_berths.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
