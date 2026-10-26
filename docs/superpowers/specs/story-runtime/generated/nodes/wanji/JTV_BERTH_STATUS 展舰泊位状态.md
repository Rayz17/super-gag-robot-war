---
id: "JTV_BERTH_STATUS"
title: "展舰泊位状态"
record_type: "terminal_view"
authority: "working"
lifecycle: "active"
version_scope: "V35.9_current_design"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv"
generated: true
aliases:
  - "展舰泊位状态"
tags:
  - "story-runtime/current"
  - "story-runtime/terminal-view"
  - "canon/working"
  - "story-runtime/wanji"
---

# 展舰泊位状态

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `JTV_BERTH_STATUS`
- **记录类型：** `terminal_view`
- **权威：** `working` / `active`
- **版本范围：** `V35.9_current_design`

## 关系

- 当前权威表中没有可安全解析的显式关系。

> [!note] 未解析引用
> 首次场景 `C01E04-CUTSCENE`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `view_id` | JTV_BERTH_STATUS |
| `display_name` | 展舰泊位状态 |
| `ui_mode` | status |
| `first_scene` | C01E04-CUTSCENE |
| `source_tables` | wanji_carrier_berths.tsv;wanji_locations.tsv |
| `player_use` | 第一章末解释万机馆怎样成为母舰，又为什么不是无限格纳库 |
| `map_expression` | B1机库脊柱、重型维修架、外部锁泊、任务地会合和残响待机分区显示 |
| `writing_rule` | 写大型机随舰或出击前必须先查泊位状态，战舰级单位不得硬塞进馆内 |
| `visual_anchor` | 工业平面图;泊位容量条;损伤状态灯 |
| `notes` | 展区保留博物馆价值，机库负责出击逻辑，二者不能互相吞掉。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
