# C01E02 Current Candidate M2 验证摘要

> 结论：`internal M2 PASS / candidate evidence`。这不等于最终 Demo 用户验收或 Runtime promotion。

## 构建身份

- Producer contract SHA-256: `6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94`
- `contract_id=C01CDV1`
- `contract_revision=2`
- `build_id=C01CDV1-M2-R2`
- `content_fingerprint=00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4`
- `save_schema=2`
- `save_namespace=c01_current_candidate/c01/e02/r2`

## 自动验证

| 门禁 | 结果 | 证据 |
|---|---|---|
| Revision-2 合同检查 | PASS | `logs/02-revision-2-contract-check.log` |
| S01–S07 连续流程、滚动、动态单位、操作输入 | PASS | `logs/03-candidate-contract-test.log` |
| 20 次确定性重放 | PASS | `deterministic-replay-receipt.tsv` |
| CP0/CP1/CP2/演出待完成/Phase P1 销毁后重建 | PASS | `checkpoint-disk-restore-receipt.tsv` |
| Revision-1 旧存档 fail-closed，字节不变 | PASS | `old-save-rejection-receipt.tsv` |
| Full/Skip 逐字段等价，盾拍只提交一次 | PASS | `full-skip-equivalence.json` |
| E02 Phase Checkpoint payload | PASS | `phase-checkpoint-payload.json` |
| 现有 Godot 全仓 smoke suite | PASS | `logs/06-existing-godot-regression.log` |
| Canon report + strict | PASS / 0 violation | `logs/09-canon-report.log`, `logs/10-canon-strict.log` |
| V35 layered pipeline | PASS / current | `logs/11-v35-layered-pipeline.log` |
| 1280x720 非空白、左右边界差异、无临时 AVI | PASS | `logs/12-capture-visual-qa.log` |

## 锁定出口

`OP-C01-BREAKER / ENC-C01-GROUND / P1 / mission_clear=false`。BREAKER 存活且首次倒地，馆守 Z 双前臂完整，重盾第四焦痕、热变形、未贯穿，撤离线已清空，5 个小体以 `scattered` 状态带 Stable ID 和位置存活。

## 重现命令

```bash
scripts/test_c01_candidate_demo_g1.sh
scripts/test_c01_candidate_demo_g1.sh --capture --skip-existing-regression
```

