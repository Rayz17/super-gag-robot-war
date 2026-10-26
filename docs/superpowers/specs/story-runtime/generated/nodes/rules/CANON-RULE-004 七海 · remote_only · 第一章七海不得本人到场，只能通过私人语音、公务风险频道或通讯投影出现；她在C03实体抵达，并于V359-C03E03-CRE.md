---
id: "CANON-RULE-004"
title: "七海 · remote_only · 第一章七海不得本人到场，只能通过私人语音、公务风险频道或通讯投影出现；她在C03实体抵达，并于V359-C03E03-CREATIVE以共同监督身份登舰。"
record_type: "runtime_rule"
authority: "hard"
lifecycle: "active"
version_scope: "runtime_stable"
owner: "runtime"
source_table: "docs/superpowers/specs/data/canon/runtime_rules.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/runtime_rules.tsv"
generated: true
aliases:
  - "七海 · remote_only · 第一章七海不得本人到场，只能通过私人语音、公务风险频道或通讯投影出现；她在C03实体抵达，并于V359-C03E03-CREATIVE以共同监督身份登舰。"
tags:
  - "story-runtime/current"
  - "story-runtime/runtime-rule"
  - "canon/hard"
---

# 七海 · remote_only · 第一章七海不得本人到场，只能通过私人语音、公务风险频道或通讯投影出现；她在C03实体抵达，并于V359-C03E03-CREATIVE以共同监督身份登舰。

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `CANON-RULE-004`
- **记录类型：** `runtime_rule`
- **权威：** `hard` / `active`
- **版本范围：** `runtime_stable`

## 关系

- **约束主体：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/characters/CH_QIHAI 七海|七海]]
- **允许起点：** [[docs/superpowers/specs/story-runtime/generated/nodes/scenes/V359-C03E01-CREATIVE 整座城压上来|整座城压上来]]

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `rule_id` | CANON-RULE-004 |
| `severity` | P1 |
| `entity_id` | CH_QIHAI |
| `entity_name` | 七海 |
| `implementation_key` | qihai_remote_presence |
| `scope` | V355-C01E01_TO_C01E04 |
| `rule_type` | remote_only |
| `forbidden_file` | game-godot/scripts |
| `forbidden_regex` | 七海.*现场\|spawn.*qihai |
| `allowed_from_scene` | V359-C03E01-CREATIVE |
| `message` | 第一章七海不得本人到场，只能通过私人语音、公务风险频道或通讯投影出现；她在C03实体抵达，并于V359-C03E03-CREATIVE以共同监督身份登舰。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/runtime_rules.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/runtime_rules.tsv`
- 最近确认：`2026-08-01`
- Owner：`runtime`
- 权威注记：Authority classified by Canon stabilization v1.
