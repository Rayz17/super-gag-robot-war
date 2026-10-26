# Call01 R2｜Section 2 内部交付回执

> Status: `0 INTERNAL_PASS / 1 FAILED / 3 NOT_CALLED`

## 交付结论

本批没有成功盾动作 Candidate。唯一先导动作 `shield_take/south` 在调用前几何门通过，生成后也保住 V10X、低位取盾、冷盾三道旧痕；但两手错误出现在盾正面／外侧，违反 `front=0 / rear=2` 的正反与承力硬合同，因此整批按首错停线。

| 姿势 | ImageGen | 结果 | Candidate / socket |
| --- | ---: | --- | --- |
| `shield_take/south` | 1 | `FAIL_FRONT_HANDS` | 未生成 |
| `shield_hold/south` | 0 | `NOT_CALLED_AFTER_STOP` | 未生成 |
| `shield_block/south` | 0 | `NOT_CALLED_AFTER_STOP` | 未生成 |
| `shield_bash/south` | 0 | `NOT_CALLED_AFTER_STOP` | 未生成 |

## 证据入口

- 50%/100% 失败 QA：`../stage-a-block/qa/GUARDIAN_Z_V10X_SHIELD_TAKE_SOUTH_R2_CALL01_FRONT_HANDS_FAIL_50_100_QA.png`
- 失败 metadata：`CALL01_R2_METADATA.json`
- 首错说明：`CALL01_R2_FIRST_FAILURE_GATE.md`

所有文件都只在本新包内；没有接入 Godot，没有修改 binding、Resolver、Default、Runtime、Canon 或生产矩阵。失败 raw 明确禁止作为下一批正向输入。
