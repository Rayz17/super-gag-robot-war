# C01E02 Revision-2 M2.1 显示层接入准备验证摘要

> 结论：`candidate interface PASS / no runtime art / awaiting exact producer handoff`。本结论不构成真实美术接入、Runtime promotion 或最终 Demo 用户验收。

## 构建与空间身份

- `build_id=C01CDV1-M2-R2`
- `contract_revision=2`
- `save_schema=2`
- `content_fingerprint=00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4`
- `profile_id=c01cdv1_e02_scroll_m2_r2`
- `topology_sha256=baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8`
- `approved_handoffs=[]`
- `runtime_art_loaded=false`

## 自动验证

| 门禁 | 结果 | 证据 |
|---|---|---|
| Revision-2 contract checker | PASS | `logs/01-revision-2-contract-check.log` |
| R2 schema/manifest，51 槽、14 instance、6 direction registration | PASS | `logs/02-r2-asset-manifest.log`、`logs/02b-r2-interface-receipts.log` |
| 零 handoff / 零 probe | PASS | `logs/02-r2-asset-manifest.log`、`logs/04-r2-godot-shell-test.log` |
| 实际 PNG 尺寸/alpha/hash/atlas | PASS | `logs/03-r2-resolver-tests.log` |
| 实际 WAV codec/采样率/声道/时长 | PASS | `logs/03-r2-resolver-tests.log` |
| 实际 MP4 codec/画幅/fps/时长 | PASS | `logs/03-r2-resolver-tests.log` |
| 错 stable ID、路径穿越、前缀伪装、symlink 逃逸、坏 hash、错尺寸/atlas/topology/fingerprint | PASS / fail closed | `logs/03-r2-resolver-tests.log` |
| Full / Skip / 缺视频同 semantic result，零 gameplay mutation | PASS | `logs/03-r2-resolver-tests.log`、`logs/04-r2-godot-shell-test.log` |
| M2 20 次确定性重放、Phase P1 | PASS | `logs/05-m2-contract-regression.log` |
| CP0/CP1/CP2/PENDING/PHASE 跨 Runner 恢复 | PASS | `logs/06-m2-persistence-regression.log` |
| schema 1 / 旧 build / 旧 fingerprint 存档拒载且字节不变 | PASS | `logs/07-m2-old-save-rejection.log` |
| 全仓 `scripts/godot-test.sh` | PASS | `logs/08-full-godot-regression.log` |
| Canon report + strict | PASS / 0 violation | `logs/09-canon-report.log`、`logs/10-canon-strict.log` |
| Canon authority + smoke | PASS | `logs/11-canon-authority.log`、`logs/12-canon-smoke.log` |
| V35 layered dashboard | PASS / current | `logs/13-layered-dashboard.log` |
| 16 个 active path × 7 个旧来源 token | PASS / 112 个零命中 | `active-lane-denylist-audit.tsv`、`logs/14-active-lane-denylist.log` |

## 三机位联合捕获

| 机位 | 程序状态 | A2 对齐 | PNG SHA-256 |
|---|---|---|---|
| WEST | turn 1；馆守Z + wall_hung 重盾 | exact aligned | `0598b4bbdc86e27d63cd23d1f18bb528e6dbc96d41fb7f78900c87c580b6356a` |
| CENTRAL | turn 1；BREAKER + 6 个 scattered 小体 | exact aligned | `a40f2a6a9347e8f9748abf6065cac482e9bef52601888ebf39e69f01adc681a1` |
| EAST | turn 6；rescue_lane=cleared；5 survivors；finisher_ready | exact aligned | `ffda6531b0798582e98e102e692ee5d7a661782a52bcdf107291fe5aaa1719d5` |

三机位的 camera center、world rect、screen rect、profile 与 topology 均和 A2 `camera-continuity.tsv` 一致；`runtime_camera_changed=false`、`runtime_map_changed=false`。详见 `a2-camera-alignment-receipt.tsv` 与 `three-camera-coordinate-contract.json`。

## 不变性证据

M2 五个内容核心哈希保持不变：build identity `3ceadfee…`、materialized snapshot `3b7470d4…`、episode `59041794…`、profile `07f611fa…`、named fallback `cfcabcdf…`。Runner 脚本为 `4429345d…`，入口场景仍为 `a2bbe3d6…`；完整回执见 `logs/15-hash-receipt.log`。

试玩入口仍是：

```bash
scripts/run_c01_candidate_demo_g1.sh
```
