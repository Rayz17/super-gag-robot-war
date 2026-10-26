---
id: "CONCEPT_ENCOUNTER_TEMPLATES"
title: "关卡目标模板表"
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
  - "关卡目标模板表"
  - "encounter_templates.tsv"
  - "守"
  - "撤"
  - "截"
  - "诱"
  - "护"
  - "拆"
  - "说得"
  - "同步"
  - "封锁"
  - "传递"
tags:
  - "story-runtime/current"
  - "story-runtime/entity"
  - "canon/working"
  - "story-runtime/concepts"
---

# 关卡目标模板表

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `CONCEPT_ENCOUNTER_TEMPLATES`
- **记录类型：** `entity`
- **权威：** `working` / `active`
- **版本范围：** `V35.9_current`
- **实体类型：** `concept`

## 关系

- 当前权威表中没有可安全解析的显式关系。

> [!note] 未解析引用
> 来源组 `GAMEPLAY`、首次伏笔 `SYSTEM-DESIGN`、正式登场 `SYSTEM-DESIGN`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `entity_id` | CONCEPT_ENCOUNTER_TEMPLATES |
| `type` | concept |
| `canonical_name` | 关卡目标模板表 |
| `aliases` | encounter_templates.tsv;守;撤;截;诱;护;拆;说得;同步;封锁;传递 |
| `source_group_id` | GAMEPLAY |
| `status` | core |
| `role` | 关卡动词、地图压力、敌方意图和软失败模板 |
| `first_foreshadow` | SYSTEM-DESIGN |
| `first_formal_appearance` | SYSTEM-DESIGN |
| `first_battle_join` | — |
| `implementation_policy` | 拆关卡先选任务动词，再设敌方预算；Boss不靠单纯堆HP。 |
| `notes` | 对应DATA_ENCOUNTER_TEMPLATES，当前14类模板。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/entities.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/entities.tsv`
- 最近确认：`2026-08-01`
- Owner：`canon`
- 权威注记：Authority classified by Canon stabilization v1.
