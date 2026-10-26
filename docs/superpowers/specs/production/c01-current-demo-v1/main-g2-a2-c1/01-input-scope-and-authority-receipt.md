# G2-A2-C1 输入、权威与写域回执

日期：2026-08-20（Asia/Shanghai）  
任务：`89 / G2-A2-C1` + `93 / 连续非headless玩家链证据纠偏`  
状态：Task89 已退回补证；Task93 Candidate 证据已收口，停在制作人 P89 reacceptance gate。

## 权威分层

- Hard：已接受 Canon 与默认 Runtime 只读，本任务未修改。
- Working：89、88、85、92、93、当前动态 gate 看板及接口 1.6.1 作为当前制作合同读取。
- Candidate：仅在 89 写域中实现 current-topology、无夹具玩家链、路线族、无身份 Proxy 合成器与证据。
- History：81/82 旧相机、旧 origin/crop、A4 exact-world 及 R2C/R2C-C1 旧证据只读；A4 只作 `fixture_validation_only/material_donor`。

## 锁定输入

| 输入 | SHA-256 | 处理 |
|---|---|---|
| `93-c01e02-g2-a2-c1-continuous-nonheadless-player-trace-correction-objective.md` | `e16bbe51ff8d078e69cee159ba216d5b4f334b7db31ee0f8298fc948132cf06c` | 当前唯一纠偏任务锁 |
| `89-c01e02-g2-a2-c1-current-topology-fixture-free-golden-turn-objective.md` | `ecd331d25e14c14e152ffc80303509e7e5c231f3fbfa4d34dc91cd7ff96d7321` | 原始任务锁 |
| `88-c01e02-r2c-fun-first-current-topology-map-and-interaction-contract.md` | `6a26aad909719cb01e9c2f411dae251eb2bfa278d163121f9a3d68ddc0cf06af` | 现行版；派工时 `5c3dbcd7…cab2ed9` 已 supersede |
| `87-c01e02-u86-route-a-user-approval-and-gameplay-alignment-reopen-receipt.md` | `79ab8d7837e1402a63fc9a3fa0f78ffe2a96941bcfb040dd45a87d6aef3ee4fc` | 只读 |
| `85-c01e02-a4-runtime-joint-registration-and-current-object-space-correction.md` | `488153a6d35583763bb7594bd890505a6cc68834fda187180f5ae12d1aa48abe` | 只读投影公式 |
| `84-c01e02-r2c-c1-producer-reacceptance-and-parallel-resume-receipt.md` | `ed3c2ce39c653e714d6ab679abbf5f19c9cd3cd2aab6c17a00cb3e5c98976dea` | R2C-C1 上游签收 |
| `92-c01e02-tactical-interface-1-6-1-copy-and-gate-sync-receipt.md` | `16b4f087c52cab9dd9d52457d3bca931399abe756895d20884853ce94c2d747e` | NON_GEOMETRIC 现行澄清 |
| `c01e02-tactical-visual-interface-v1.json` | `9bfcbc827c0c65a347d75a76a0e07dcb07382efb299021d75fed80c3969b6534` | 接口 1.6.1；仅动态 gate 同步，无 schema/几何/copy 变化 |
| `38-c01e02-m3-r0-5-production-board.tsv` | `0679b21649a5c2403acdcaa6f267d2cbd11c818d3ad35b1200aca9773001ba7c` | Task89 returned、93 dispatched、P89 blocked |
| `00c-core-game-design-master-review.md` | `eadd8add793eced85bdd1fa7b2a56566bc17ba8bb586069b96e9644e9345899a` | 玩法责任只读 |

## 唯一写域

- `golden_slice_profile.json`
- `golden_slice_resolver.gd`
- `g2_a2_visual_compositor/**` 下的 content/scripts/scenes
- 专用 `g2_a2_c1_*` 测试、capture/performance driver
- Task93 连续 trace driver、外部 validator 与证据回执
- `scripts/test_c01e02_m3_golden_slice_g2_a2_c1.sh`
- `main-g2-a2-c1/**`

未执行 `git add/commit/clean`，未回滚或覆盖共享工作树其他改动。

## 只读不变对象

| 对象 | 最终 SHA-256 |
|---|---|
| `golden_slice_session.gd` | `c32c43146bad16385c013cc682aea98b2ee7b376e34b8af22e5f606573e0a5ce` |
| `performance_director.gd` | `ee132eb1f29cceae0c389e78e9a1a1f8d9e4fb4e984bac143c93760a0b6db5b4` |
| `tactical_world_view.gd` | `5e6fd6f22fc5c05b99bedb2c887c2881907b43a62f21da6b3ff3acc34cb43084` |
| `startup_router.tscn` | `5c19e60028b16128919e7422c5f0e5ce428183dcfad5d93306440134caae612d` |
| `project.godot` | `482437d3830366dc00c97a0e7dd1a5a6806e39e3203df09d1b79d3fd653eac29` |

隔离标志最终为：`approved_handoffs=[]`、`real_art_loaded=0`、非默认、save disabled、Runtime/Canon/G2-B 均未开放。
