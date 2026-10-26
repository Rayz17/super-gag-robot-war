# A30｜BREAKER Wave A 四向中立 Candidate

> 状态：`STOPPED_AFTER_EAST_HARD_GATE_FAIL / NO_DERIVED_CANDIDATE / USER_FALSE / RUNTIME_FALSE / CANON_FALSE`

本包回应用户对 BREAKER 多朝向的明确追问，补齐 `east / south / west` 三个缺失中立方向；现有 `north` 原位保留，不覆盖、不重画。

本轮只建立四向视觉审查资产与精灵 metadata。不得写入 Godot 绑定、Runtime、Default 或 Canon；只有四向用户门通过后，才允许生产 `red_beam/west` 与 `hit_recoil/west`。

## 固定合同

- 相机：`CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE`
- 方向：`north=[40,-24] / east=[40,24] / south=[-40,24] / west=[-40,-24]`
- 画布：`384×384 RGBA8`
- pivot：`[192,320]`
- footprint：`3×3`
- scale：`[1,1]`
- registration：`footprint_bottom_center`
- 镜像：禁止
- 随机重抽：`0`

## 正向来源

见 `source-lock/A30-SOURCE-LINEAGE.tsv`。所有其他 BREAKER 稿件一律不是本包正向输入。

## 原定输出范围

- `call01/map-candidates/BREAKER_GF_LOCKED_CAMERA_V2_IDLE_EAST_CANDIDATE_384.png`
- `call01/map-candidates/BREAKER_GF_LOCKED_CAMERA_V2_IDLE_SOUTH_CANDIDATE_384.png`
- `call01/map-candidates/BREAKER_GF_LOCKED_CAMERA_V2_IDLE_WEST_CANDIDATE_384.png`
- 四向 100% QA 板与 alpha/pivot/方向读回
- Candidate 回执

## Call01 实际结果

EAST 首次且唯一一次内置 ImageGen 调用同时触发方向极性与 alpha 硬门；因此没有生成任何 384×384 map Candidate，SOUTH/WEST 未调用。详见 `call01/receipts/A30-CALL01-SECTION2-HARD-GATE-FAILURE-RECEIPT.md`。
