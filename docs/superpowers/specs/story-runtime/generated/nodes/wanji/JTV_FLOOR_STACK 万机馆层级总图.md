---
id: "JTV_FLOOR_STACK"
title: "万机馆层级总图"
record_type: "terminal_view"
authority: "working"
lifecycle: "active"
version_scope: "V35.9_current_design"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv"
generated: true
aliases:
  - "万机馆层级总图"
tags:
  - "story-runtime/current"
  - "story-runtime/terminal-view"
  - "canon/working"
  - "story-runtime/wanji"
---

# 万机馆层级总图

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `JTV_FLOOR_STACK`
- **记录类型：** `terminal_view`
- **权威：** `working` / `active`
- **版本范围：** `V35.9_current_design`

## 关系

- 当前权威表中没有可安全解析的显式关系。

> [!note] 未解析引用
> 首次场景 `C01E01-ADV`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `view_id` | JTV_FLOOR_STACK |
| `display_name` | 万机馆层级总图 |
| `ui_mode` | map |
| `first_scene` | C01E01-ADV |
| `source_tables` | wanji_floors.tsv;wanji_locations.tsv;wanji_exhibition_zones.tsv |
| `player_use` | 让玩家理解万机馆不是一间展厅，而是外部、L1、L2、L3、B1、B2构成的多层旧会展馆 |
| `map_expression` | L1主展层高亮;L2和L3灰色可见;B1显示低频供能;B2只显示0号门轮廓 |
| `writing_rule` | 台本中需要说明空间、移动路线或封锁状态时，优先让纪存看终端，不写成纸笔记 |
| `visual_anchor` | 腕持式折叠终端;旧馆内网UI;低亮蓝白线框 |
| `notes` | 第一章只开放闭馆路线，但终端总图必须让玩家看见大量未开放区域。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
