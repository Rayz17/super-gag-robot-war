---
id: "CONCEPT_INFORMATION_ARRIVAL_ORDER_DRIFT"
title: "非穿越式信息到达错序"
record_type: "entity"
entity_type: "concept"
authority: "working"
lifecycle: "active"
version_scope: "V35_expedition_front_v1"
owner: "canon"
source_table: "docs/superpowers/specs/data/canon/entities.tsv"
source_of_truth: "docs/superpowers/specs/data/story/far_star_lightslot_communication_rules.tsv"
generated: true
aliases:
  - "非穿越式信息到达错序"
  - "到达逆序"
  - "包序漂移"
  - "回复先于原包"
  - "四时间戳"
tags:
  - "story-runtime/current"
  - "story-runtime/entity"
  - "canon/working"
  - "story-runtime/concepts"
---

# 非穿越式信息到达错序

> [!warning] Current Canon 自动投影
> 本页由 Canon 源表生成。请勿直接编辑；应修改权威源并重建。

## 身份

- **ID：** `CONCEPT_INFORMATION_ARRIVAL_ORDER_DRIFT`
- **记录类型：** `entity`
- **权威：** `working` / `active`
- **版本范围：** `V35_expedition_front_v1`
- **实体类型：** `concept`

## 关系

- 当前权威表中没有可安全解析的显式关系。

> [!note] 未解析引用
> 来源组 `DEEP_SPACE_SIGNAL`、首次伏笔 `SYSTEM-DESIGN`、正式登场 `SYSTEM-DESIGN`
> 这些值没有匹配到 Current Canon 节点，因此只保留为提示，不建立图谱边。

## Canon 字段

| 字段 | 当前值 |
| --- | --- |
| `entity_id` | CONCEPT_INFORMATION_ARRIVAL_ORDER_DRIFT |
| `type` | concept |
| `canonical_name` | 非穿越式信息到达错序 |
| `aliases` | 到达逆序;包序漂移;回复先于原包;四时间戳 |
| `source_group_id` | DEEP_SPACE_SIGNAL |
| `status` | working_current |
| `role` | 后发消息走更快的新信道先到、早发消息沿旧光路或实体投递后到，导致抵达与译码确认顺序不同于生成顺序 |
| `first_foreshadow` | SYSTEM-DESIGN |
| `first_formal_appearance` | SYSTEM-DESIGN |
| `first_battle_join` | — |
| `implementation_policy` | 每包必须记录发信者本征时、地球基准时、抵达时和译码确认时；所有确定内容都在接收前生成，不提供未来信息。 |
| `notes` | 可写讣告先于家书、答复先于求援原包；不得真预言、向过去发令、改写历史或用通信复活人物。 |

## 权威来源

- 注册表：`docs/superpowers/specs/data/canon/entities.tsv`
- Source of Truth：`docs/superpowers/specs/data/story/far_star_lightslot_communication_rules.tsv`
- 最近确认：`2026-07-20`
- Owner：`canon`
- 权威注记：到达与确认可以错序，但所有消息在接收前已生成，不构成时间旅行或未来信息。
