# C01E02 M2.5 A5 小型突入体四向 Atlas 接入完成报告

> Status: `implementation complete / internal gates pass / awaiting joint playtest`
>
> Runtime lane: `candidate_runtime_demo`
>
> Formal Runtime promotion: `not authorized`

## 结果

M2.5 在同一个 `C01CDV1-M2-R2` Runner 内完成 A5 小型突入体 96px `idle` 四向 Atlas 接入。默认 Current 现在只消费一份合并活动回执：A4 MAP-B 五个静态槽加 A5 小体母版槽。

`validated_handoff_count=6 / loaded_slot_count=6 / resource_probe_count=6 / runtime_art_loaded=true / fallback_count=7`

六只 `ENEMY_C01_RIFT_SWARM_01..06` 没有复制成六套资源，继续共用 `ENEMY_C01CDV1_RIFT_SWARM_MASTER` 的同一纹理。Runner 按每只实例的实时 `facing` 读取 `idle/north|east|south|west`；真实 Atlas 绘制成功时不再叠画旧几何 token。

## 视觉与行为证据

- 四 frame 均完成 source rect 与像素审计，含正式初始阵列没有的 south 隔离显示态。
- Atlas 保持原生 `96x96`、bottom-center `pivot=[0.5,1.0]`、`footprint=[1,1]`。
- WEST / CENTRAL / EAST 三机位均同时显示真实 A4 地图与真实 A5 小体。
- MOVE_BEFORE / MOVE_AFTER 证明真实敌方回合后，六体按既有 scattered AI 移动并切换朝向；禁用美术对照的玩法结果一致。
- 地图滚动、遮挡、重盾单绘、救援线、P1 payload 与 M2.4 行为保持不变。

中央机位：`captures/C01E02_M2_5_CENTRAL_A4_MAP_B_A5_SWARM_1280x720.png`

## 冻结哈希

- A5 Candidate-local PNG: `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b`
- combined validated receipt: `c284fe2b04f04526cd22280e47e89f879f2d3d5e3d5c8a82528e27b71b7e2e5e`
- combined rejection log: `4f008659b215c141b77f5d7233e462cc34a4a8b33c7e5c5f4ccd2e03735a53a0`
- receipt payload: `74388c294b05eef5a922cc51fcf63e11ffd514b2eef0e6e3bde96e4bf560b386`
- active config: `7a6e993a4452b9e6888c936341bfe614d0cf18dfe9a913d68a84d7a7ddd48b49`
- post-integration Runner: `7a3aa518fa63e239b6cc48a618c5bf77c1989eabc5a5989361521e707e439824`
- static manifest: `2cc85fc524b453b255c4d8aa521236e0845664f1a8721829da7a5befa21b93c9`，未改
- historical A4 five-slot receipt: `e240cd06835de85e2a9801a022ec5a0bef82f17ff49960496a99fd81f6a24e61`，原字节保留

## 证据导航

- 冻结输入与预检: `00-frozen-input-and-preflight-receipt.md`
- 13 槽运行台账: `01-runtime-slot-ledger.tsv`
- 三机位、四朝向与移动前后: `02-capture-manifest.tsv`
- fail-closed 矩阵: `03-fail-closed-test-matrix.tsv`
- 回归结果: `04-regression-summary.md`
- 原始日志: `logs/**`
- 捕获状态: `captures/*-state.json`

## 未执行

- 未制作 `move`、`impact`、`death` 动画，当前只有 `idle` 四向。
- 未制作六实例差分，六体仍共用一份母版。
- 未接馆守 Z、BREAKER、重盾或 A4 `STATE_LAYERS` 真实资产。
- 未修改 Canon、剧情、玩法、AI、地图、锚点、存档、build identity、profile、topology、C04 或启动架构。
- 未提升为正式 Runtime，未 `git add/commit`。

本报告是 M2.5 内部实现与自动门禁 PASS，不是最终 Demo 用户验收。按目标书在此停止，等待制作人与用户联合试玩，不自行接入下一资产。
