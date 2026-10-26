# C01E02 A2 滚动旧会展街区完成报告

## 交付边界

- 包 ID：`C01CDV1_A2_ROLLING_DISTRICT_V1`
- 只写入 `art-a2-rolling-district/**`。
- 全部为 `Candidate / runtime_allowed=false / runtime_handoff=none`。
- 未写 Godot，未改 Canon/剧情/玩法，未生产小体机设、正式 tile/sprite、动作帧、Cut-in、视频或 LibTV。

## 共享拓扑

- 源 profile：`c01cdv1_e02_scroll_m2_r2`
- 拓扑签名：`baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8`
- 棋盘：`32x18`，大于 `900x594` 战术视口。
- 三案完整复用地形区、单位锚点/footprint、非可控救援对象、可破坏物、取盾点和 `scattered` 组织态。

## 旧 B3 处置

- `18-g1-5-b3-tactical-map-art-objective.md`、旧 `12x9` profile、`BG_C01CDV1_PLAZA_TACTICAL` 和旧 B3 交付只在 `superseded-history-ledger.tsv` 登记为 `superseded_history_only`。
- 它们没有进入新判断板、没有进入 active source receipt，也没有被修改。

## 已知来源残留

- Current Canon 场景备注仍保留旧的“撤离后取盾”句子；已验收 Reader 和 revision-2 制作人合同明确实现顺序为“取盾挡下赤红冲击 -> 最后车辆通过 -> 盾拍”。
- A2 只表达空间关系，不把时序烘进地图，未修改 Canon。
- A2 开工时 `check_canon_authority.py` 通过；交付复核期间，并行 C04 写入使全局检查暂时报告 `ANT_BROKEN_CROWN` authority coverage 缺项，并在其 `authority_manifest.tsv` 差异中留下尾随空白。A2 未修改这些文件；C01 的 `ENEMY_C01_RIFT_SWARM` Working 行仍可正常查询，且明确不锁造型和棋盘数量。

## 用户停止门

等待用户分别决定：A/B/C 场景身份、战术读法、遮挡原则、小体布局密度。
