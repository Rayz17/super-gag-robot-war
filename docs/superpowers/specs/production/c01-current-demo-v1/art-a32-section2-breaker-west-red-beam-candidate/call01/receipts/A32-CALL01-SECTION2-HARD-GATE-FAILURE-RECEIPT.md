# A32 Call01｜BREAKER red_beam/west Section 2 硬门失败回执

> Status: `FAIL_STOP_HISTORY_ONLY`
>
> Consumer scope: `ENEMY_C01_BREAKER|red_beam/west` only
>
> Candidate / Godot / Runtime / Canon: `false / untouched / false / false`

## 权威与输入边界

- `python3 scripts/report_v35_layered_pipeline.py --check`：`V35 layered pipeline dashboard is current`。
- Current Canon 查询：`CML129`为 Hard active；`ENEMY_C01_BREAKER`为 Working current。
- 唯一正向身份／材质输入：CML129 GF锁定结构母体与当前north 384母版。
- 唯一方向输入：本包先制作的非身份`Camera V2 west [-40,-24]`几何导图。
- GF PLAN只提供用户确认的具体设计读感；全屏环境、人物、UI和其他单位均不属于本资产。
- A30 East fail、B/X、Call03及其他History像素没有传入ImageGen，也不得成为后续正向源。

完整输入、SHA与许可范围见`source-lock/A32-SOURCE-LINEAGE.tsv`。

## 调用计数

- Built-in ImageGen：`1`
- Reroll：`0`
- 后续图像调用：`0`

提示词：`prompts/A32-CALL01-WEST-RED-BEAM-BUILTIN-IMAGEGEN-PROMPT.md`。

## 50% / 100%硬门

| 门 | 结果 | 证据 |
| --- | --- | --- |
| GF身份与表面 | `PASS` | 保留低伏重壳、异质长叶叠甲、黑色石金属与细金缝。 |
| 四肢承力 | `PASS` | 四个承力肢体均完整可读，没有缺肢或重复肢。 |
| 单低嵌红缝 | `PASS` | 仅有一个低嵌红缝，短红束从同一前端发出。 |
| Camera V2 west极性 | `FAIL` | 目标轴为`-149.0362°`；raw主轴朝红缝为`165.6712°`，绝对差`45.2926°`；质心到红缝差`37.5932°`。头虽在左侧，却没有沿`[-40,-24]`落在屏幕左上，整体读成近水平／略向左下。容差`10°`。 |
| Alpha | `FAIL_NOT_PROVEN_RECOVERABLE` | raw为`1254x1254 RGB`，棋盘已烘入RGB，没有alpha。因方向硬门先失败，依照“一项失败即停”没有继续做确定性抠图或384注册，不能把“可能可抠”写成已安全恢复。 |
| 50/100综合 | `FAIL_STOP` | 身份质量较好，但不是精确west资产，不能绑定或复用。 |

机器读回：`call01/receipts/BREAKER_A32_CALL01_WEST_HARD_GATE.json`。

QA板：`call01/qa/BREAKER_A32_CALL01_WEST_HARD_GATE_FAIL_QA_50_100.png`，四格依次为raw半尺寸、头部1:1裁切、west几何导图、当前north正向身份母版。

## 封存结论

- 失败raw：`call01/generation-raw/BREAKER_A32_CALL01_WEST_RAW.png`
- raw SHA-256：`398a8408fff6395ef67577f7e431d8aaa689d35898c8a9cf310395ddfd8d9195`
- QA SHA-256：`0a3487bb15b5293f5d1b285bc94003ab8822f50c5fd720b729d83cee9100ffc3`
- 当前north SHA-256保持不变：`6b20111c80e3dc76adb5a05b55395359b7d1bdc2ec189060859058e53dbffde1`

本次不产生384 RGBA Candidate，不产生shared map master，不声明`hit_recoil/west`可复用，不修改binding、Godot、Runtime、Default或Canon。失败raw只作History／诊断证据，禁止进入任何后续正向设计或精灵输入。
