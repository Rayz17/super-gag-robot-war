# C01E02 M2.4 冻结输入与预检回执

## 身份

- Demo: `C01CDV1-M2-R2`
- contract revision: `2`
- save schema: `2`
- content fingerprint: `00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4`
- profile: `c01cdv1_e02_scroll_m2_r2`
- topology: `baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8`
- objective SHA-256: `fdc09239f5d7d35c930834ea1a53eb37a8f8346a1a8c6834423f676d1a7be2af`

## 制作人输入

| 输入 | SHA-256 | 结果 |
| --- | --- | --- |
| `a4-user-approval-receipt.tsv` | `dc402de8ee471953fa1de8b98676aa76a9826a2b219dc6010ba7e762f128781b` | PASS |
| `a4-map-static-5-copy-plan.tsv` | `21bed025aa4efff116003b952b4e9450071d96b4f18021e52f82f7b9d845181d` | PASS |
| `a4-map-static-5-exact-handoff.json` | `494defbd783f478b8c51458457b514295e5e8e026f59a3e48c024451fb10e429` | PASS |

## 生产预检

- submitted: `5`
- validated: `5`
- rejected: `0`
- resource probes: `5`
- synthetic fixture: `false`
- runtime art loaded: `true`
- receipt payload SHA-256: `65643b3d71829da05f5c1232fa55d7d0f1720e0d8145ef60f7e0200b9e7b4d68`
- frozen receipt file SHA-256: `e240cd06835de85e2a9801a022ec5a0bef82f17ff49960496a99fd81f6a24e61`
- rejection log SHA-256: `f3dbb55bfcf80790917e03383fbce30fbdb23d9626eea069a1ba743bc55513cb`

预检重放产生的 receipt/rejection 与 Candidate-local 冻结副本字节一致。

## Active Binding

- config: `game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/active_asset_binding_r2.json`
- config SHA-256: `ef37e5172d4e97eaf36d92370aaab4747e1fdede1dd56adf7da8bb567bb35ce7`
- receipt: `res://content/candidate_runtime_demo/c01/e02/asset_integration_r2/validated_receipts/a4_map_b_static_5.validated.json`
- 优先级: `disable active art > explicit environment receipt > default active config`
- 无目录扫描、无通配符、无最近文件猜测。

`asset_slot_manifest_r2.json` 仍保持 `approved_handoffs=[]` 且静态 `runtime_art_loaded=false`。五槽加载只是 Candidate Runtime 活动回执，不是 Canon 或正式 Runtime promotion。
