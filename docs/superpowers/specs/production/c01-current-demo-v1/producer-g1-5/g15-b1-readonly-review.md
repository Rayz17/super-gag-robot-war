# C01E02 G1.5-B1 制作人只读回收

> Result: `PASS / B2_unlocked`
>
> Lifecycle boundary: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 1. 用户裁决证据

原始裁决均来自美术任务 `019ee96f-3179-7643-a8a5-6ec833a8c7e6`：

| 时间（UTC） | 原文 | 裁决 |
|---|---|---|
| `2026-08-07T16:05:57.380Z` | `B可以` | 主轮廓采用 B「前肢承重半直立型」 |
| `2026-08-07T16:09:13.705Z` | `X 异质/生体装甲` | 后续表面语言采用 X |
| `2026-08-07T16:13:21.250Z` | `保持` | 头部红缝、闭合胸缝、封闭上背核心出口保持当前关系 |

制作人任务 `019f55ea-799e-7e71-a5f2-f91e74bdae32` 于 `2026-08-07T16:18:39.202Z` 收到三项合并确认和正式回收请求。精确消息 ID、资产 ID、路径与哈希登记在 `b1-user-approval-receipt.tsv`。

## 2. 实物与哈希核验

- B1 交付共 18 个文件，全部位于 `art-g1-5/b1-breaker-ground/**`。
- `delivery-hashes.sha256` 登记的 17 项全部通过。
- `asset-manifest.tsv` 共 15 条，全部 `runtime_allowed=false`。
- 13 项冻结来源与来源回执登记值一致。
- 96/128 px 样张尺寸及透明通道通过；三张身份页、总方向板和表面/结构关系板尺寸通过。
- 没有 `BLOCKED.md`，没有 Godot、Canon、Runtime 或 A1 文件被 B1 改写。

获批方向证据：

| 用途 | Stable ID | SHA-256 |
|---|---|---|
| B 身份页 | `CAND_BREAKER_B1_FORELIMB_BEARER_V1_IDENTITY_SHEET` | `7035ba01896844d0e74a0e7989f26177fe4010b0458f742e200da5d0f900f868` |
| B 96 px | `CAND_BREAKER_B1_FORELIMB_BEARER_V1_96` | `699f2f45ecc3371a87dd88e200851c20b5f0b750cfb1cb8ca6446d85ac872876` |
| B 128 px | `CAND_BREAKER_B1_FORELIMB_BEARER_V1_128` | `e8000411704e9da6408eb746080545850e23d5eb3e63afd33f251a9ab33c7ac4` |
| X 与三结构关系证据板 | `G15_B1_BREAKER_SURFACE_RELATION_BOARD` | `cdedf6b1c59b953395decc3a94221903a25ec3ba631b9727382177fe05a40d85` |

父方向板 `G15_B1_BREAKER_DIRECTION_BOARD` 的 SHA-256 为 `075322ec14fb356e7339f7902aca858707ef5a02298bb984360cf5a1c54512cf`；技术元数据 `G15_B1_BREAKER_CANDIDATE_SPEC` 的 SHA-256 为 `fb15c3fb39f5d51d9eba1f5248c136b2f7f85d005983e8f43f35e020793b8b8c`。

## 3. 权威与生命周期判断

- `ENEMY_C01_BREAKER` 仍是 `Working / active` 文字身份；没有 BREAKER 美术锁，也没有 Candidate Canon 同名行。
- 现有 B 图只批准轮廓、尺度和动作扩展空间。它们的表面仍是中性方向样张，不能声称已经完成 B+X 精修。
- X 与三处结构裁决只授权后续美术派生，不建立整个裂星潮敌群的 Canon 美术锁。
- B1 没有 Sprite Master、正式机设、Godot import 或 Runtime handoff；A/C 保留为未选审计参考。

## 4. 验证结果

以下检查通过：

- `python3 scripts/report_v35_layered_pipeline.py --check`
- `python3 scripts/check_c01_current_demo_contract.py`
- `python3 scripts/check_canon_authority.py`
- `scripts/canon-smoke-test.sh`
- `scripts/canon-query.sh entity ENEMY_C01_BREAKER`
- `scripts/canon-query.sh candidate entity ENEMY_C01_BREAKER`（预期无 Candidate 行）
- B1 `shasum -a 256 -c delivery-hashes.sha256`

本轮没有用默认系统 Python 重写冻结交付；可复现生成源随 B1 保留，但签收依据是冻结文件、来源回执、像素属性和哈希核验。

## 5. 解锁结论

B1 的三项用户门均已关闭，允许派发 `17-g1-5-b2-retired-shield-art-objective.md`。B2 只开放退役重盾的独立方向与四态判断；B3、B4、C1、Runtime promotion 和 LibTV D1 仍然锁定。
