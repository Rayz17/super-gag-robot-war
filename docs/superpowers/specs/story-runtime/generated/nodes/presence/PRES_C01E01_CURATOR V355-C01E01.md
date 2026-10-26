---
id: "PRES_C01E01_CURATOR"
title: "V355-C01E01"
record_type: "scene_presence"
authority: "working"
lifecycle: "active"
version_scope: "current_scene_presence"
owner: "story"
source_table: "docs/superpowers/specs/data/canon/scene_entity_presence.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/scene_entity_presence.tsv"
generated: true
aliases:
  - "V355-C01E01"
tags:
  - "story-runtime/current"
  - "story-runtime/scene-presence"
  - "canon/working"
---

# V355-C01E01

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `PRES_C01E01_CURATOR`
- **记录类型：** `scene_presence`
- **权威：** `working` / `active`
- **版本范围：** `current_scene_presence`

## 关系

- **所属场景：** [[docs/superpowers/specs/story-runtime/generated/nodes/scenes/V355-C01E01 最后一场导览|最后一场导览]]
- **在场主体：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/characters/CH_CURATOR 旧策展人馆长|旧策展人馆长]]

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `presence_id` | PRES_C01E01_CURATOR |
| `scene_id` | V355-C01E01 |
| `entity_id` | CH_CURATOR |
| `requirement` | required_trace |
| `presence_mode` | recording |
| `lifecycle_claim` | foreshadow_recording |
| `scene_function` | 缺席馆长录音和生活痕迹 |
| `control_state` | 无实时控制 |
| `knowledge_state` | 录音只包含录制时已知内容 |
| `entry_state` | 馆长本人不在场 |
| `exit_state` | 缺席谜团继续 |
| `source_refs` | docs/superpowers/specs/data/canon/entities.tsv |
| `status` | working |
| `notes` | 不可把录音写成实时对话 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/scene_entity_presence.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/scene_entity_presence.tsv`
- 最近确认：`2026-08-01`
- Owner：`story`
- 权威注记：Authority classified by Canon stabilization v1.
