# C01E02 M2.4 A4 MAP-B 五槽真实接入完成报告

> Status: `implementation complete / internal gates pass / awaiting joint playtest`
>
> Runtime lane: `candidate_runtime_demo`
>
> Formal Runtime promotion: `not authorized`

## 结果

M2.4 在同一 `C01CDV1-M2-R2` Runner 内完成 A4 MAP-B 五个静态槽的真实接入。无环境变量时，无参数默认入口通过 Candidate-local、SHA 锁定的 active config 消费冻结 receipt：

`validated_handoff_count=5 / loaded_slot_count=5 / resource_probe_count=5 / runtime_art_loaded=true`

其余八个 M2.2 首批槽仍是具名几何 fallback。`STATE_LAYERS` 明确未加载，因此没有墙挂盾与独立重盾状态的双绘。

## 运行行为

- BASE / BUILDINGS: 单位前
- ROOFS / FOREGROUND: 单位后
- OCCLUSION_MASK: 只采样，不可见绘制
- STATE_LAYERS: fallback，可破坏物与状态继续程序化绘制
- HUD / path / cursor: 保持在地图之上，不随战场滚动
- 单个资源漂移: 只降级该 slot
- 配置或 receipt 失效: `0 probes` 全 fallback，仍可玩
- 无效显式 receipt: 不会偷偷落到默认 active receipt

## 冻结哈希

- validated receipt: `e240cd06835de85e2a9801a022ec5a0bef82f17ff49960496a99fd81f6a24e61`
- active config: `ef37e5172d4e97eaf36d92370aaab4747e1fdede1dd56adf7da8bb567bb35ce7`
- Runner: `de31ba758bd0490bbfa60e411f090e72a5741be322365db33fbff37e0c6c6f06`
- static manifest: `2cc85fc524b453b255c4d8aa521236e0845664f1a8721829da7a5befa21b93c9`

## 证据导航

- 槽位台账: `01-runtime-slot-ledger.tsv`
- 三机位、EAST_POST 和滚动录像: `02-capture-manifest.tsv`
- fail-closed 矩阵: `03-fail-closed-test-matrix.tsv`
- 回归结果: `04-regression-summary.md`
- 原始日志: `logs/**`
- 捕获回执: `captures/*-state.json`

## 未执行

- 未接 A5 atlas、馆守 Z、BREAKER、小体或重盾真实资产。
- 未修 A4 `STATE_LAYERS`，未做动态拆包。
- 未修改 Canon、剧情、玩法、存档、build identity、profile、topology 或启动架构。
- 未 `git add/commit`。

本报告是 M2.4 内部实现与自动门禁 PASS，不是最终 Demo 用户验收。按目标书在此停止，等待制作人与用户联合试玩。
