# V35.10 正式逐话 Episode Pipeline 运行

> 状态：`frozen_candidate_pending_full_pressure_board_gate`  
> Canon Mode：`living_plus_v357_v358_candidate`  
> 本目录保存一次提前发生的逐话试跑。五份Packet保留其历史审稿证据，但当前不计正式完成；V35.9全剧95槽Pressure Board通过前禁止续写。

## 当前冻结裁决（2026-07-12）

- 冻结原因：旧V35.8虽曾结构通过，但当时尚未完成敌我、素材精确绑定、选择器、生命周期、唯一资产与高密度语义门禁；V35.9也只生成到C07。
- 冻结对象：C01E01-C01E04与C02E01共5份Episode Packet，以及C01章节合订稿和相关运行账本。
- 历史结论：文件内`pass`表示当时的单话/章审结果，允许未来回收，不表示当前基线下正式验收。
- 当前正式Episode进度：`0`。
- 解冻条件：V35.9的18章95槽Pressure Board全部通过章审、C01至C18前缀回归和全剧回收审计。
- 解冻动作：从C01E01逐份复核，保留未受新基线影响的主体，定点修订发生结构变化的Packet；之后从C02E02顺序续写。
- 唯一状态入口：`../V35-PRODUCTION-STATUS.md`。

## 运行顺序

1. 从`C01E01`开始，一次Pipeline只写一话；
2. 每话读取对应V35.9 Pressure Board、V35.8 Loadout、前序状态和必要素材；
3. 每话保存一份独立Episode Packet，包含可读剧情、Production Split、Writer Room Review、Patch Log、Gate和State Deltas；
4. 每章完成后执行章审；C03完成后执行C01-C03开局前缀审；
5. C01-C03未通过前，不把C04标记为正式逐话开始；
6. V35.9中已存在的C04-C07压力板保留为候选施工输入，不代表对应章节已经写成。

## 进度口径

- `board_ready`：只有压力板。
- `packet_draft`：已有单话文件，尚未通过审稿。
- `episode_pass`：单话Pipeline全部通过。
- `chapter_pass`：本章所有单话通过且章审通过。
- `prefix_pass`：C01到当前章连读审通过。

正式逐话完成数只统计`episode_pass`，不得统计Pressure Board数量。

## 历史试跑记录（不计当前正式进度）

- `episodes/`下已有C01E01-E04四份独立厚版Episode Packet；它们在旧门禁下通过，当前冻结待新基线复核。
- `chapters/C01-最后一夜万机馆站起来.md`为四话连续装配稿，包含跨话玩法闭环；它不是单话源文件。
- `reviews/C01-prefix-review.md`记录全部严格席、三轮根因回放和最大轮次裁决。Canon/资产与主要创作席均通过；厚度席第三轮仍发现Reader设计语残留，终审后已执行最小修法并按规则取最优版封章，没有伪造第四轮PASS。
- C01旧章级状态为`chapter_pass_max_attempt_policy`，只作历史审稿证据，不再授权继续推进。
- C02E01也已生成并冻结；C02E02及以后不得开始。C03、C04均未进入当前正式逐话生产。

## C01E01 Canon迁移

- **原因**：旧`R07`资产锁只允许第一话出现社勇王模型/取件屏，但V35.5、V35.8和V35.9已把“全尺寸社勇王在馆外送修直播中受限首显”作为开局机器人世界宽度的一部分，旧锁与候选施工层互相冲突。
- **变更**：模型锚仍严格是模型，不会参战；社勇王真机只允许头颈/目光和吊具确认动作，不进入棋盘、没有HUD、豪司不出场，C03E03才首次控制。
- **影响面**：只调整`character_mecha_art_locks.tsv`的豪司说明和R07参战包首显边界；不改变豪司登场、社勇王首控、勇者许可高潮或模型到实机Linking规则。
- **回滚**：若后续美术审认定第一话无法承担真机首显，可把送修直播替换成全尺寸维修诊断影像；C01E01战斗、状态与人物逻辑不受影响。
