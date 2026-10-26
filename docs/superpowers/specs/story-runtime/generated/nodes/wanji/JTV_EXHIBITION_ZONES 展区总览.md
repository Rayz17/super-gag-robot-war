---
id: "JTV_EXHIBITION_ZONES"
title: "展区总览"
record_type: "terminal_view"
authority: "working"
lifecycle: "active"
version_scope: "V35.9_current_design"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv"
generated: true
aliases:
  - "展区总览"
tags:
  - "story-runtime/current"
  - "story-runtime/terminal-view"
  - "canon/working"
  - "story-runtime/wanji"
---

# 展区总览

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `JTV_EXHIBITION_ZONES`
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
| `view_id` | JTV_EXHIBITION_ZONES |
| `display_name` | 展区总览 |
| `ui_mode` | map_overlay |
| `first_scene` | C01E01-ADV |
| `source_tables` | wanji_exhibition_zones.tsv |
| `player_use` | 给美术、台本和玩家一个“万机感”目录，避免只记得馆守Z和几个展岛 |
| `map_expression` | 按L1/L2/L3/B1/B2分层显示19个展区;当前路线为亮色;未开放区保留名称与轮廓 |
| `writing_rule` | 新增展区、展柜、场景图或角色移动前必须先查本视图与展区表 |
| `visual_anchor` | 展区色块;密集图标;可折叠筛选栏 |
| `notes` | “第一章走过的展岛”只是样本，不是万机馆容量上限。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
