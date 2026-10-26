# C01E02 Current Demo M2 改造前基线

- 记录日期：2026-08-08
- Git HEAD：`a851398347806850c8b0e0ce6a4d83a14e0677bb`
- Git branch：`codex/srw-kernel-sandbox`
- 制作人合同：`19-current-demo-inplace-rebase-producer-contract.md`
- 合同 SHA-256：`6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94`
- 性质：同一 `candidate_runtime_demo` 的原位重基审计；本文件不是可运行旧版入口。

## 冻结故事截面

| 输入 | SHA-256 |
|---|---|
| C01 已验收 Reader | `c9a9aa490badea3d2de937e0003b80547974fed27103b31ec9181cd3583cfc8b` |
| C01 用户验收回执 | `3d11387d92120cfdeeb0069a2a7cdfbe677ed0ea2ac5ae6649038de7b0cd532b` |
| C01 剧情游玩拓扑 | `5d640ed3e70854a178194ceeeffe7d444a928547a414af3407674b9d4f4be5aa` |
| C01 游戏流程解构 | `68ac0efa2d8316f33eb41ca745568684dd180021931355e8ff1d0798196b5296` |
| 全局拓扑合同 | `550da9196bb9029aa0ceb7d75cd1bfdb73c852dd806fb4b609f1765c652eee76` |

## Revision 1 运行身份

- `contract_id=C01CDV1-G1`
- `contract_version=1.0.0`
- `content_fingerprint=944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`
- `save_schema_version=1`
- `save_namespace=c01_candidate_demo_v1/c01e02`
- `terminal_state=c01cdv1_e02_complete`
- 战棋轮廓：固定 `12x9`、单 BREAKER、CP3 Episode 终局。

## 活跃入口与实现哈希

| 文件 | SHA-256 |
|---|---|
| `game-godot/scenes/candidate_runtime_demo/c01/e02/c01e02_g1_runner.tscn` | `a2bbe3d6d7bea7db79da88a6e575a10303af0dd9a2527b2d3470ba057323150b` |
| `game-godot/scripts/candidate_runtime_demo/c01/e02/c01e02_g1_runner.gd` | `649861ef83f3ff970976be2197202df1bb441faf8c6bf02d1778cec90181a96a` |
| `game-godot/scripts/candidate_runtime_demo/c01/e02/candidate_input_router.gd` | `6a5186a4d1ba5731c9d06df196258af5d2c42c565bfae4b8f4f905591e30e734` |
| `game-godot/scripts/candidate_runtime_demo/c01/e02/candidate_isolation_guard.gd` | `89abe54505a79e53ce2b2430af1a83438e8b6e22c603dcf59d53fe1446f89c71` |
| `game-godot/scripts/candidate_runtime_demo/c01/e02/candidate_local_state.gd` | `1f86e932abc7d0bfac201807e2baa4b14f21ff302aaf1dd3235c01b57833c868` |
| `game-godot/scripts/candidate_runtime_demo/c01/e02/candidate_save_store.gd` | `359d8b86e61c6ce42b22e31fa3c238edfb4df561f113c4361682c0fc44144d05` |
| `game-godot/scripts/candidate_runtime_demo/c01/e02/candidate_tactical_session.gd` | `c2763274150a793a969ff6cbc93c70fae57055ce928f64de747d915e2ea9e980` |
| `game-godot/content/candidate_runtime_demo/c01/e02/episode_g1.json` | `26426e22d2f60d8e48aed1079906efe7e59491bdbe1d5fed90b4c870f6f1` |
| `game-godot/content/candidate_runtime_demo/c01/e02/graybox_profiles.json` | `08b66594e4ae63d094ba519559cf7878b7931209a31dfb8a33e6bd7b2612dfb8` |
| `game-godot/content/candidate_runtime_demo/c01/e02/named_geometry_fallbacks.json` | `6c788ec14a5e36ee76403f8f57cc10a54938ebe6d9d051f33714c7ab70fbb5b1` |
| `game-godot/content/candidate_runtime_demo/c01/e02/generated/build_identity.json` | `e166e76342242e49490f0c7cb9b381dfc58679150b1581c56db9f6d0f59f2e4e` |
| `game-godot/content/candidate_runtime_demo/c01/e02/generated/materialized_snapshot.json` | `a7c1fc3c7bb7d5cc0f7dfef86bf250c914cc053deb744fc0259e7a3bdf1e0dec` |
| `game-godot/tests/candidate_runtime_demo/c01e02_g1_bad_fingerprint_test.gd` | `95bc480dc01d48fec23b543709f6c321571c04a40353f5bcac00574878a3ef9b` |
| `game-godot/tests/candidate_runtime_demo/c01e02_g1_capture_driver.gd` | `df51505a4f693738549910997bb54ceec927c41375a5a82375ec571e813afe2f` |
| `game-godot/tests/candidate_runtime_demo/c01e02_g1_contract_test.gd` | `9dfa8a83c733beec48a3ef9011a45eacef2f6b12f5900f433f7f8acb1f997787` |
| `game-godot/tests/candidate_runtime_demo/c01e02_g1_persistence_test.gd` | `0b1c69fa5489e5813b116c412253c85ef92c734e9af893bf7014af891ddaa942` |
| `scripts/check_c01_current_demo_contract.py` | `e60af1f6fcd3b8d8b6c922ff5f08d2be41f64be0302eec55b51812e33be7a5a5` |

## 回滚边界

Git 提供旧实现恢复证据；M2 不创建旧入口、旧存档加载器或第二套 build。需要回看时只从上述 HEAD/哈希审计，不允许 revision 1 内容重新进入活跃 Candidate Runtime。
