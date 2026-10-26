# A29｜万机馆未来人形比例／B1-B2 下身一致性窄返修

> Status: `SECTION2_FAIL_STOP_AFTER_CALL01 / NO_USER_DELIVERY`
>
> User approval: `false`
>
> Runtime: `false`
>
> Godot binding: `false`
>
> Canon: `false`

## 已完成

- A25 最新用户裁决已先写回 A25 回执。
- 以 0 次 ImageGen 建立前后共享比例、关节点、摄影包络和 B1/B2 部件映射 guide：`00-SHARED-HUMANOID-PROPORTION-AND-MODULE-GUIDE.md`。
- 正向源和诊断源已隔离并锁 SHA：`source-lock/A29-SOURCE-LINEAGE.tsv`。
- Call01 精确提示词：`prompts/A29-CALL01-FRONT-BUILTIN-IMAGEGEN-PROMPT.md`。

## 停止原因

Call01 没有产出一张独立前侧 3Q，而产出多视图、文字、箭头设计板；主体仍保留整块白色护胫和鞋型足，并自行标出约 40m。因此同时违反独立画布、摄影、B1/B2 下身映射、无文字和巨物尺度门。

失败图仅在 `failed/WANJI_A29_CALL01_FRONT_SECTION2_FAIL.png` 留证。依据“front 未通过则 rear 不得独立设计”和“每资产一次、0 随机 reroll”，Call02 未调用；`delivery/` 保持为空。

详见 `receipts/A29-CALL01-SECTION2-HARD-GATE-FAILURE-RECEIPT.md`。
