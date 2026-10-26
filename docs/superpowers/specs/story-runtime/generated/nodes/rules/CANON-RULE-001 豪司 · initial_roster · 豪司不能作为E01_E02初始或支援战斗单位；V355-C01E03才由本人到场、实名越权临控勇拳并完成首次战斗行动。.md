---
id: "CANON-RULE-001"
title: "豪司 · initial_roster · 豪司不能作为E01/E02初始或支援战斗单位；V355-C01E03才由本人到场、实名越权临控勇拳并完成首次战斗行动。"
record_type: "runtime_rule"
authority: "hard"
lifecycle: "active"
version_scope: "runtime_stable"
owner: "runtime"
source_table: "docs/superpowers/specs/data/canon/runtime_rules.tsv"
source_of_truth: "docs/superpowers/specs/data/canon/runtime_rules.tsv"
generated: true
aliases:
  - "豪司 · initial_roster · 豪司不能作为E01/E02初始或支援战斗单位；V355-C01E03才由本人到场、实名越权临控勇拳并完成首次战斗行动。"
tags:
  - "story-runtime/current"
  - "story-runtime/runtime-rule"
  - "canon/hard"
---

# 豪司 · initial_roster · 豪司不能作为E01/E02初始或支援战斗单位；V355-C01E03才由本人到场、实名越权临控勇拳并完成首次战斗行动。

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `CANON-RULE-001`
- **记录类型：** `runtime_rule`
- **权威：** `hard` / `active`
- **版本范围：** `runtime_stable`

## 关系

- **约束主体：** [[docs/superpowers/specs/story-runtime/generated/nodes/entities/characters/CH036 豪司|豪司]]
- **允许起点：** [[docs/superpowers/specs/story-runtime/generated/nodes/scenes/V355-C01E03 双拳打碎外壳|双拳打碎外壳]]

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `rule_id` | CANON-RULE-001 |
| `severity` | P1 |
| `entity_id` | CH036 |
| `entity_name` | 豪司 |
| `implementation_key` | haosi |
| `scope` | C01E01-C01E02 |
| `rule_type` | initial_roster |
| `forbidden_file` | game-godot/scripts/core/battle/battle_session.gd |
| `forbidden_regex` | _player\("haosi" |
| `allowed_from_scene` | V355-C01E03 |
| `message` | 豪司不能作为E01/E02初始或支援战斗单位；V355-C01E03才由本人到场、实名越权临控勇拳并完成首次战斗行动。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/runtime_rules.tsv`
- Source of Truth：`docs/superpowers/specs/data/canon/runtime_rules.tsv`
- 最近确认：`2026-08-01`
- Owner：`runtime`
- 权威注记：Authority classified by Canon stabilization v1.
