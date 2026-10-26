# C01E02 M2.5 冻结输入与预检回执

## 身份

- Demo: `C01CDV1-M2-R2`
- contract revision: `2`
- save schema: `2`
- content fingerprint: `00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4`
- profile: `c01cdv1_e02_scroll_m2_r2`
- topology: `baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8`
- objective SHA-256: `24ec8a724aa5b00731f4628054c5675aaefa11c77979845d84a643e085b00689`
- M2.4 prechange Runner SHA-256: `de31ba758bd0490bbfa60e411f090e72a5741be322365db33fbff37e0c6c6f06`

## 制作人输入

| 输入 | SHA-256 | 结果 |
| --- | --- | --- |
| `main-m2-4/05-completion-report.md` | `b1ee2776b74f2158f8fd32d39db06969b08286e40897e5b2dba5b1b6f54823f7` | PASS |
| `producer-a5/a5-user-approval-receipt.tsv` | `45c1687c3fdbdd87d7f9e872933b48925871f680eeaa0095d360623ad1a34f75` | PASS |
| `producer-a5/a5-rift-swarm-96-copy-plan.tsv` | `1467bf0e8dae7de0969761cd06c36ad7c8ff7259e424a457e694827d1da2b6ca` | PASS |
| `producer-a5/a4-static-5-plus-a5-rift-swarm-96-exact-handoff.json` | `abd97837d9abe811862b3a0e5878e6263fd46379eb6f4336fb6af18bb5bd1e36` | PASS |
| `art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png` | `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b` | PASS |
| `art-a5-rift-swarm-four-facing-atlas/atlas-spec.tsv` | `3d52d578c1e189a4cb57d2b2691c41e29c17d6f76dde29dafc9c7269b763a6dd` | PASS |
| `asset_slot_manifest_r2.json` | `2cc85fc524b453b255c4d8aa521236e0845664f1a8721829da7a5befa21b93c9` | PASS / unchanged |

## 修改前门禁

- A5 validator: PASS，使用工作区 bundled Python/Pillow；系统 Python 缺少 Pillow 的首次诊断不作为产品失败。
- A5 core hash: PASS，包含冻结的 M2.4 Runner `de31...f06`。
- Current Demo contract: PASS。
- M2.4 default baseline: `5 validated / 5 loaded / 5 probes`，PASS。
- M2.2 zero-handoff baseline: `0 / 0 / 0`，PASS。
- Godot Canon strict、Canon authority、Canon smoke: PASS。

原始证据位于 `preflight/logs/**`。M2.5 后 Runner 改动是目标书授权的下游消费变更；A5 源包及其冻结哈希未回写。

## 字节复制与生产预检

- Candidate-local copy: `game-godot/content/candidate_runtime_demo/c01/e02/approved_runtime_assets_r2/a5_rift_swarm/rift-swarm-idle-96.png`
- copied SHA-256: `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b`
- submitted: `6`
- validated: `6`
- rejected: `0`
- resource probes: `6`
- synthetic fixture: `false`
- receipt payload SHA-256: `74388c294b05eef5a922cc51fcf63e11ffd514b2eef0e6e3bde96e4bf560b386`
- frozen receipt file SHA-256: `c284fe2b04f04526cd22280e47e89f879f2d3d5e3d5c8a82528e27b71b7e2e5e`
- rejection log SHA-256: `4f008659b215c141b77f5d7233e462cc34a4a8b33c7e5c5f4ccd2e03735a53a0`

严格预检重放产生的 receipt/rejection 与 Candidate-local 冻结副本一致。旧 A4 五槽 receipt/rejection 仍分别为 `e240cd06835de85e2a9801a022ec5a0bef82f17ff49960496a99fd81f6a24e61` 与 `f3dbb55bfcf80790917e03383fbce30fbdb23d9626eea069a1ba743bc55513cb`，原字节未变。

## Active Binding

- config: `game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/active_asset_binding_r2.json`
- config SHA-256: `7a6e993a4452b9e6888c936341bfe614d0cf18dfe9a913d68a84d7a7ddd48b49`
- receipt: `res://content/candidate_runtime_demo/c01/e02/asset_integration_r2/validated_receipts/a4_static_5_plus_a5_rift_swarm_96.validated.json`
- priority: `disable active art > explicit environment receipt > default active config`
- default result: `6 validated / 6 loaded / 6 probes / 7 fallback`

`asset_slot_manifest_r2.json` 仍保持 `approved_handoffs=[]`、静态 `runtime_art_loaded=false`。六槽加载只由本 Candidate Demo 的 exact validated receipt 授权，不是 Canon 或正式 Runtime promotion。
