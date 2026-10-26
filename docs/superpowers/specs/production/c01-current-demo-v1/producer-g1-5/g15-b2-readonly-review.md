# C01E02 G1.5-B2 制作人只读回收

> Result: `PASS / B3_unlocked`
>
> Lifecycle boundary: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 1. 用户裁决证据

原始裁决来自美术任务 `019ee96f-3179-7643-a8a5-6ec833a8c7e6`：

| 时间（UTC） | 消息 ID | 原文 | 精确裁决 |
|---|---|---|---|
| `2026-08-07T17:36:43.610Z` | `msg_019fdd4c-765a-7533-be2e-ee0fc122dffa` | `1 A；2 F-D70/P30；3 通过` | A「高窄塔盾型」；F「制式重装 70% / 港防修补 30%」；四态连续性按当前呈现通过 |

制作人任务 `019f55ea-799e-7e71-a5f2-f91e74bdae32` 于 `2026-08-07T17:56:32.292Z` 收到正式签收与派发 B3 的请求。精确消息、资产 ID、路径与哈希登记在 `b2-user-approval-receipt.tsv`。

## 2. 实物、来源与哈希核验

- B2 交付共 26 个文件，全部位于 `art-g1-5/b2-retired-shield/**`。
- `delivery-hashes.sha256` 的全部登记项通过。
- `asset-manifest.tsv` 共 23 条，文件与哈希匹配，且全部 `runtime_allowed=false`。
- `source-validation-receipt.tsv` 的 33 项冻结输入与当前文件一致。
- 12 张 96/128 px 样张尺寸与透明通道通过；7 张板图尺寸通过。
- 没有 `BLOCKED.md`，没有 Godot、Canon、Runtime、B3、B4、C1 或 LibTV 产物混入。

获批方向及证据：

| 用途 | Stable ID | SHA-256 |
|---|---|---|
| A 四态身份页 | `CAND_RETIRED_SHIELD_B2_TOWER_V1_FOUR_STATE_SHEET` | `e3d3cb2f736d3fd6bfd972553d8336773530412d695db6153b2a8d3b45015fc5` |
| A 墙挂 96 px | `CAND_RETIRED_SHIELD_B2_TOWER_V1_WALL_HUNG_96` | `fa4bdf49e1914c187c5065b7c1c336a5c7b0041313fb1832eea38120f16b40c2` |
| A 墙挂 128 px | `CAND_RETIRED_SHIELD_B2_TOWER_V1_WALL_HUNG_128` | `17e8821b773ad53302ea2358d34c76465f7b01cc01347b6e8c53c78f66860923` |
| A 持盾 96 px | `CAND_RETIRED_SHIELD_B2_TOWER_V1_HELD_COLD_96` | `619beb0552a2143e2815a26c2179645d5e3eb99f7a9f8637da378b5bad0f3809` |
| A 持盾 128 px | `CAND_RETIRED_SHIELD_B2_TOWER_V1_HELD_COLD_128` | `898516cb583221c891b216d84a686889b4ca9c58cdd0f2bf9188dbef7bdcf232` |
| F 表面语言裁决板 | `G15_B2_RETIRED_SHIELD_SURFACE_BOARD` | `097002a8b4fd7efd2e4713f4263bb47e99b91bc090da21d72238c9add8af8151` |
| 四态连续性裁决板 | `G15_B2_RETIRED_SHIELD_CONTINUITY_BOARD` | `f6f0ac6f8098365971bc1956406da91a2c6233694418bfde71341ae476dca8b1` |

父方向板 `G15_B2_RETIRED_SHIELD_DIRECTION_BOARD` 的 SHA-256 为 `b264d240fea54a4b380774dd333fc88c50f86dd4486ea1514c7d751088197680`；技术规格 `G15_B2_RETIRED_SHIELD_CANDIDATE_SPEC` 的 SHA-256 为 `00782ad70da3a5bcddddec4c86e2549f03e1ca8fbad184a42eaa2a33e11ecdf3`。S07 尺度板 `G15_B2_RETIRED_SHIELD_S07_SCALE_BOARD` 的 SHA-256 为 `9a1d6f43514d7041cffc2362c23256974e75c1c7017fe9de0c0ad3331f9ddd82`，只作为尺度/遮挡相容性证据，不冒充独立获批资产。

## 3. 权威与生命周期判断

- 退役重盾是 Working C01 场面及万机馆巡展装备中的既有实物，但没有独立美术锁；`PROP_C01CDV1_RETIRED_SHIELD` 只是 Demo 槽位，不是新增 Canon 实体。
- A 获批的是高窄塔盾的轮廓、挂点/握持关系及 E02 四态语法。现有 A 图没有完成最终 `A + F(D70/P30)` 精修；F 是以后派生时必须采用的表面参数。
- 四态通过只覆盖三处旧痕、赤红冲击后的第四道新焦痕、局部左右热分流及 E02 非贯穿损伤；E03 贯穿和 E04 完全碎裂仍然排除。
- 96/128 px 文件仍是方向样张，不是 Sprite Master；没有 Godot import、Runtime handoff、Cut-in 或视频授权。
- B/C 只保留为未选审计参考。未选 B 的独立四态页存在左侧可见裁切，但总方向板和连续性板中的 B 完整；该问题不阻断已选 A，也不得让 B/C 成为 B3 派生来源。

## 4. 验证结果

以下检查通过：

- `python3 scripts/report_v35_layered_pipeline.py --check`
- `python3 scripts/check_c01_current_demo_contract.py`
- `python3 scripts/check_canon_authority.py`
- `scripts/canon-smoke-test.sh`
- `scripts/canon-query.sh scene V355-C01E02`
- `scripts/canon-query.sh entity MECHA_WANJI_MOBILE_CHASSIS`
- `scripts/canon-query.sh 退役重盾`
- B2 `shasum -a 256 -c delivery-hashes.sha256`

可复现生成源随 B2 保留；签收依据是冻结交付、来源回执、像素属性与哈希，不在回收时重生或改写用户已经审过的文件。

## 5. 解锁结论

B2 的三项用户门均已关闭，允许派发 `18-g1-5-b3-tactical-map-art-objective.md`。B3 只开放旧会展广场的地图底板、遮挡、重盾挂点/热点状态层与同坐标读法；B4、C1、Runtime promotion、Canon 迁移及 LibTV D1 继续锁定。
