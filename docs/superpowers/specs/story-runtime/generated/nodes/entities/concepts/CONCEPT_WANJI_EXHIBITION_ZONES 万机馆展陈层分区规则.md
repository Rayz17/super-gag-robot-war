---
id: "CONCEPT_WANJI_EXHIBITION_ZONES"
title: "万机馆展陈层分区规则"
record_type: "entity"
entity_type: "concept"
authority: "working"
lifecycle: "active"
version_scope: "V35.9_current"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/entities.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/entities.tsv"
generated: true
aliases:
  - "万机馆展陈层分区规则"
  - "展区总图"
  - "万机感"
  - "exhibition zones"
  - "展陈层地图"
tags:
  - "story-runtime/current"
  - "story-runtime/entity"
  - "canon/working"
  - "story-runtime/concepts"
---

# 万机馆展陈层分区规则

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `CONCEPT_WANJI_EXHIBITION_ZONES`
- **记录类型：** `entity`
- **权威：** `working` / `active`
- **版本范围：** `V35.9_current`
- **实体类型：** `concept`

## 关系

- 当前权威表中没有可安全解析的显式关系。

> [!note] 未解析引用
> 来源组 `MUSEUM`、首次伏笔 `SYSTEM-DESIGN`、正式登场 `SYSTEM-DESIGN`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `entity_id` | CONCEPT_WANJI_EXHIBITION_ZONES |
| `type` | concept |
| `canonical_name` | 万机馆展陈层分区规则 |
| `aliases` | 展区总图;万机感;exhibition zones;展陈层地图 |
| `source_group_id` | MUSEUM |
| `status` | core |
| `role` | 定义万机馆展陈层的大分区、视觉密度、尺度、开放状态和美术锚点 |
| `first_foreshadow` | SYSTEM-DESIGN |
| `first_formal_appearance` | SYSTEM-DESIGN |
| `first_battle_join` | — |
| `implementation_policy` | 新增地图、展区台本、场景图或美术资产前必须先查wanji_exhibition_zones.tsv；第一章闭馆路线只是样本，不代表万机馆总容量。 |
| `notes` | 对应wanji_exhibition_zones.tsv和DOC_WANJI_COLLECTION_CARRIER_DESIGN。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/entities.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/entities.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
