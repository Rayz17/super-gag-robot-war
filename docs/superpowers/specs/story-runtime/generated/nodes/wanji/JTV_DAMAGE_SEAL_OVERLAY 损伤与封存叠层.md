---
id: "JTV_DAMAGE_SEAL_OVERLAY"
title: "损伤与封存叠层"
record_type: "terminal_view"
authority: "working"
lifecycle: "active"
version_scope: "V35.9_current_design"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv"
generated: true
aliases:
  - "损伤与封存叠层"
tags:
  - "story-runtime/current"
  - "story-runtime/terminal-view"
  - "canon/working"
  - "story-runtime/wanji"
---

# 损伤与封存叠层

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `JTV_DAMAGE_SEAL_OVERLAY`
- **记录类型：** `terminal_view`
- **权威：** `working` / `active`
- **版本范围：** `V35.9_current_design`

## 关系

- 当前权威表中没有可安全解析的显式关系。

> [!note] 未解析引用
> 首次场景 `C01E02-BATTLE`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `view_id` | JTV_DAMAGE_SEAL_OVERLAY |
| `display_name` | 损伤与封存叠层 |
| `ui_mode` | damage_overlay |
| `first_scene` | C01E02-BATTLE |
| `source_tables` | wanji_exhibition_zones.tsv;wanji_carrier_berths.tsv;runtime_rules.tsv |
| `player_use` | 战斗后显示哪些展品受损、哪些门被封、哪些区域仍不可进入 |
| `map_expression` | 火警、法务封条、卷帘门、B1供能、B2封存和展品损伤作为叠层显示 |
| `writing_rule` | 写战后检查、清算压力或封锁路线时，用终端叠层承载信息，不让角色站着念说明 |
| `visual_anchor` | 红色封条;黄黑警示线;损伤百分比 |
| `notes` | 损伤叠层也是剧情压力，不只是UI提示。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
