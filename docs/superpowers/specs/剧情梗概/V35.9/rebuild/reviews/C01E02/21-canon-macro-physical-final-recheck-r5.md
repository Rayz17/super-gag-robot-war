# C01E02 Canon / Macro / Physical 最终定向复验 r5

> 席位：原 Canon / 宏观谜团 / 物理连续性独立审稿席  
> 证据基线：2026-07-15 当前磁盘  
> 复验对象：`18-canon-macro-physical-recheck-r4.md` 的 PATCH-1..3  
> 最终裁决：`PASS`

## 1. 裁决摘要

18号报告的三项索引/图谱补丁均已闭合，且未使C01E02正文、Runtime/Graybox、原子物理快照或E03/E04下游发生回归：

- PATCH-1：R07包级formal/battle、coverage、CW045与社勇王援护时序已迁入当前Story-First口径；默认查询不再把旧`C01E03-04`作为R07 formal/battle答案。
- PATCH-2：馆守Z肩部机制已归属`V353U001`；废弃alias精确查询只返回redirect target；馆守Z图节点已有E01/E02/E03现行三阶段边，旧边均为historical。
- PATCH-3：18号报告列出的11条旧标准化流程关系全部historical化；六个目标历史节点不存在非historical入/出边。

本轮未发现阻断或仍需源文件修补的活跃冲突。裁决为`PASS`。

## 2. PATCH-1：R07与社勇王时序闭合

- `docs/superpowers/specs/data/canon/entities.tsv:48`：R07的`first_formal_appearance`与`first_battle_join`均为`V355-C01E03`；policy明确E03只是豪司/勇拳包级首次介入，社勇王真机首控仍锁`V355-C03E03`。
- `docs/superpowers/specs/data/canon/entities.tsv:32-33`：CH036在`V355-C01E03`正式/首战；CH037在该话仅作远程/终端预告，formal/battle仍为`C08-01`。
- `docs/superpowers/specs/data/canon/wanji_roster_zone_coverage.tsv:8`与`docs/superpowers/specs/data/design_graph/consistency_watchlist.tsv:57`同值保存“E01锚件预告 -> E03豪司/勇拳包级介入 -> C03E03社勇王真机首控”。
- `docs/superpowers/specs/data/canon/entities.tsv:144`：`MECHA_SHA_YONG_WANG_SUPPORT`的formal/battle均为当前`C05E20-BRAVERY-COMBO`；E01只保留锚件预告，不再引用旧`C01E03-04`作当前答案。
- 精确执行`./scripts/canon-query.sh entity R07`可读到核心R07的`V355-C01E03` formal/battle，且没有任何当前行以`C01E03-04`充当这两个first字段。`scripts/canon-smoke-test.sh:109-116`已把该条件固化为回归断言。

结论：PATCH-1 `PASS`。

## 3. PATCH-2：馆守Z alias与现行生命周期闭合

- `docs/superpowers/specs/data/canon/entities.tsv:332`：`MECHA_GUARDIAN_Z_SHOULDER_CHANNEL`的父ID为`V353U001`，三项first时序均为`V355-C01E03`；notes明确它只是部位/地图机制，不增加机体计数。
- `docs/superpowers/specs/data/design_graph/graph_nodes.tsv:55`：`N_GUANSHOU_Z`由`DATA_CANON_ENTITIES`拥有，aliases含`V353U001`，现行notes完整覆盖E01低热、E02零身体动作且右臂连接、E03首控并永久断臂。
- `scripts/canon_query.py:246-260`：精确实体ID若为`deprecated_alias`，输出`alias_redirect`和redirect target后立即返回，不再进入全字段子串扫描。实测`entity MECHA_GUARDIAN_Z`只得到`V353U001`一个`entity_id`，不会再命中肩部子机制。
- `docs/superpowers/specs/data/design_graph/graph_edges.tsv:87,89,139`：E113/E115/E135分别为`historical_introduces`、`historical_reenters_body`、`historical_reenters_body`，旧三话时序仅供追溯。
- `docs/superpowers/specs/data/design_graph/graph_edges.tsv:1888-1890`：E1952/E1953/E1954分别建立E01低热预告、E02零动作/右臂连接约束、E03首控/断臂激活的现行三阶段边。
- `scripts/canon-smoke-test.sh:69-86`已断言alias查询仅一个实体、不得泄漏旧首战，并要求`N_GUANSHOU_Z`同时返回E1952/E1953/E1954。

结论：PATCH-2 `PASS`。

## 4. PATCH-3：旧标准化流程边闭合

18号报告点名的11条关系现均带historical语义，notes也统一把当前答案导向V35.9四话链：

- `docs/superpowers/specs/data/design_graph/graph_edges.tsv:311-313,315-316`：E357为`historical_constrained_by`，E358/E359为`historical_uses`，E361为`historical_introduces`，E362为`historical_threads_fire_alarm`。
- `docs/superpowers/specs/data/design_graph/graph_edges.tsv:450,455`：E496/E501均为`historical_constrained_by`。
- `docs/superpowers/specs/data/design_graph/graph_edges.tsv:1128,1131,1134,1141`：E1174/E1177/E1180/E1187均为`historical_maps_to`。

本席对`N_EP01_MERGED_V03`、`N_CH01_EP01_MERGED_FLOW`、`N_EP01_ROUTE_TIERS`、`N_EP01_LEGAL_EXECUTION_UNITS`、`N_CH01_STANDARDIZED_SCRIPT`、`N_CH01_STANDARDIZED_FLOW`重跑全部入/出边结构审计，结果为`checked_nodes=6, leaks=0`。`scripts/canon-smoke-test.sh:198-212`已将同一条件固化为持续断言。

结论：PATCH-3 `PASS`。

## 5. C01E02快照与下游无回归

- `docs/superpowers/specs/data/design_graph/graph_nodes.tsv:886`仍把C01E02唯一物理期末快照锁为：29人楼外、3核心+F2馆内、七海写权限关闭而城市消防继续、泵手动低压、供水热损、完整移动脊柱未暴露；E03不得恢复人员、设施双分支或勇拳E02动作。
- `docs/superpowers/specs/data/design_graph/graph_edges.tsv:1877`的E1941只允许S03从29人楼外、3核心+F2馆内、既有设施伤痕、消防机腿伤、勇拳静态、白函预布及移动脊柱未暴露起步。
- 同表`:1878`的E1942要求S04先继承E02伤痕再叠E03增量，且人员不得重新进入载荷选择；`:1879`的E1943继续约束state propagation不得清零E02伤痕。

因此，本轮索引与图谱迁移没有造成29人回刷、馆内5人膨胀、损伤预算复原、勇拳E02动作、馆守ZE02主动化、白函提前具身、完整移动脊柱提前暴露或E03/E04下游重生。

## 6. 独立校验回执

- `python3 scripts/check_c01e02_runtime_graybox.py`：`PASS`，TOKEN_ROUTES、F2_ENTRY、FIVE_PERSON_RELEASE、R2_BRANCH_GUARDS、ROUND_POOLS、ATOMIC_COMMIT全部通过。
- `scripts/canon-smoke-test.sh`：`PASS`，输出`Canon smoke test passed`。
- `scripts/canon-check-godot.sh --strict`：`PASS`，无runtime violation。
- `python3 scripts/check_v35_8_slot_loadout.py`：`PASS`，95槽manifest/action/source/selector/lifecycle/asset/high-density合同闭合。
- 定向TSV结构审计：`PASS`，13张目标表列形一致、主键唯一。
- 六历史节点全边关系审计：`PASS`，`checked_nodes=6, leaks=0`。
- 工作树缓存审计：`PASS`，未发现`__pycache__`、`.pyc`、`.pytest_cache`、`.mypy_cache`或`.ruff_cache`新增物。

## 7. 最终裁决

`PASS`。

18号报告的PATCH-1..3已逐项闭合；当前默认查询、alias重定向、馆守Z现行边、旧流程历史关系及C01E02下游快照互相一致。无需修改C01E02 Episode、Runtime、Graybox、迁移单、S03/S04 PB、state propagation或其他被审源文件。
