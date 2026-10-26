# C01E02 M3-R0.5 M0｜Packing 冲突审计与纠偏闭环

> 日期：2026-08-18
>
> 状态：`RESOLVED_BY_41_AND_42 / schema validation only / no handoff`

## 1. 历史暂停点

制作人审计指出旧草稿把评审画幅、单帧尺寸、atlas 总尺寸和 Runtime packing 混在一起。主程序车道当时停止捕获与完成回执，逐项记录了 34↔36/37↔旧 manifest 的冲突，未修改 33-37，也未读取 A6/A7 输出目录。

主要冲突包括：A4 被误写成 1280×720、A6 三态母版/atlas 模型不一致、A7 atlas/pivot/frame rect 未冻结、道路末态与过程帧混用、音频被误写为 44.1k/mono/错误时长。

## 2. 制作人纠偏

- 41 冻结 42 为唯一 packing 权威，并明确 A7 Stable ID 身份。
- 42 冻结 28 个视觉槽与 16 个音频槽的 exact schema。
- 43 冻结 R1 hard gates 与 claim boundary。
- 44 选择选项 B，冻结七海独立 `presence_cards` 消费者。

## 3. 逐族解决结果

| 家族 | 42 后 manifest/schema |
| --- | --- |
| A4 | 五槽均 `2400×1350`；base 无 alpha，其余有 alpha |
| A5 | `384×96`，4× `96×96`，N/E/S/W |
| 兜灯 | `1920×640` 静帧与冻结安全区 |
| 纪存 | `2304×768`，3×1，单帧 `768×768`，focused/alarm/resolve |
| 七海 | `2304×768`，3×1，controlled/decision/concerned，character + remote noise mask |
| 旧守护者 | `3072×768`，3×1，单帧 `1024×768`，head/chest/waveform layers |
| 馆守 Z | `1280×1024`，5×4，20 帧，pivot `[0.5,0.88]` |
| BREAKER | `960×1280`，3×4，12 帧，pivot `[0.5,0.9]` |
| 应急车 | `512×128`，4×1，12fps，pivot `[0.5,0.82]` |
| Cut-ins | 每槽 `1600×900` layered static |
| FX | dust/artillery/red 均 `2048×256`，8×1，单帧 `256×256`，18fps |
| Road final | 三槽均 `2400×1350` |
| Road process | 三槽均 `3072×256`，6×1，单帧 `512×256`，18fps |
| Audio | 16 槽全部 `wav_pcm_s24le / 48000 Hz`，channels/duration/loop 逐槽精确 |

## 4. 机器闭环

`media_packing_validator.gd` 对 42 SHA、合同身份、坐标约定、完整槽集合和每个权威字段做 exact compare；额外拒绝缺 Stable ID/fallback、非零 handoff/runtime 状态。负向夹具覆盖 A4 尺寸、road process 帧数和音频 codec 漂移。

结果：`C01E02_M3_R05_MEDIA_PACKING_OK visual=28 audio=16 probes=0`。

## 5. 边界

冲突已在 M0 schema 层解决，因此允许生成零资产捕获与报告。该结果不表示 A6/A7 真实资源已制作、评审、批准、探测、加载或 exact handoff；这些计数仍全部为 0。
