---
id: STORY_RUNTIME_CONTEXT_PACKS
record_type: runtime_context_pack_index
authority: compiled_ephemeral
generated: false
tags:
  - story-runtime/context-pack
---

# 章节与单话上下文包

本目录用于存放按具体章引擎或单话需求编译出的写作上下文，而不是继续堆积全量 Canon 摘要。

每个上下文包至少应区分：

- 全量必带：顶层主题、根机制、当前生产门、写作禁区。
- 精确检索：本章角色、机体、敌人、地点、事件、能力与物理约束。
- 邻接扩展：一至二跳关系、前章输出、后章不可提前消费项。
- 创作素材：IP 投射、名场面、What-if、机甲文化生态、生活与关系场面。
- 冲突证据：相互矛盾的来源、尚未裁决的候选和历史高光。
- 预算信息：玩家可见证据、演出载体、资产复用和战斗表达能力。

上下文包是一次写作任务的“可解释编译结果”。确认稿产生后，新增事实必须回流 Canon 或候选收件箱，不能只留在包内。

## v2.1 编译与交互级运行

`scripts/compile_story_runtime_context_pack.py`先在后台生成三层证据：

- `上层与机制检索包`：L1、L2、世界机制基线与 L3 章级职责。
- `Current Canon检索包`：Hard / Working、active Canon 与有界图谱邻接。
- `创作素材检索包`：Candidate 参战包、IP、名场面、模玩生态、关系与现实共鸣材料。

随后生成作家与审稿真正使用的接口：

- `05`：全剧对齐与章间交接合同；
- `06`：实体身份与机体生命周期合同；
- `07`：核心人物行动合同；
- `08`：新实体准入合同；
- `09`：稳定写作内核加本章差量；
- `review-contexts/`：连续性、机器人文化、人物关系和游戏制作四份窄上下文；
- `10` 至 `12`：实体使用、章末状态和人物兑现回执。

作家不读取 `02` 至 `04`。每项结果都在 `retrieval_trace.tsv` 中保存命中分数、选取原因和来源，输入输出哈希和上下文缓存键写入 `runtime_manifest.json`。

可用以下命令编译并检查 C02 v2 包：

```bash
python3 scripts/compile_story_runtime_context_pack.py \
  --request docs/superpowers/specs/story-runtime/context-packs/C02-runtime-v2/00-C02上下文需求-v2.md \
  --output-dir docs/superpowers/specs/story-runtime/context-packs/C02-runtime-v2

python3 scripts/check_story_runtime_harness.py \
  --request docs/superpowers/specs/story-runtime/context-packs/C02-runtime-v2/00-C02上下文需求-v2.md \
  --pack-dir docs/superpowers/specs/story-runtime/context-packs/C02-runtime-v2
```

`assemble_story_runtime_episode_context.py`保留为短单话兼容入口。正式长单话或高密度单话使用场面事务链：

```bash
python3 scripts/compile_story_runtime_episode_run.py \
  --request <章需求.md> \
  --pack-dir <上下文包目录> \
  --director-board <章节导演板.md> \
  --episode-card <当前单话卡.md> \
  --prior-episode-state <上一话状态增量.md> \
  --plan <单话场面事务计划.tsv> \
  --episode <CxxExx> \
  --output-dir <单话Runtime目录>

python3 scripts/assemble_story_runtime_interaction_context.py \
  --run-dir <单话Runtime目录> \
  --fragment-id <CxxExx-Fxx>

python3 scripts/prepare_story_runtime_interaction_review.py \
  --run-dir <单话Runtime目录> \
  --fragment-id <CxxExx-Fxx> \
  --draft <本场正文.md> \
  --state-receipt <本场出口回执.json>

python3 scripts/commit_story_runtime_interaction.py \
  --run-dir <单话Runtime目录> \
  --fragment-id <CxxExx-Fxx>

python3 scripts/assemble_story_runtime_episode_draft.py \
  --run-dir <单话Runtime目录>

python3 scripts/seal_story_runtime_episode.py \
  --run-dir <单话Runtime目录>

python3 scripts/check_story_runtime_episode_run.py \
  --run-dir <单话Runtime目录> \
  --strict

python3 scripts/prune_story_runtime_interaction_cache.py \
  --run-dir <单话Runtime目录>
```

场面只有在局部语义审查七项全部通过后才能提交。上游场面正文或出口状态改变时，后续场面自动失效并从最早根因顺推。整话接缝审查通过后才生成下一话期末状态。章末仍使用`check_story_runtime_harness.py --strict-receipts`验证章级回执；语义审稿不能被脚本替代。

最后一条缓存命令默认只预览。`contexts/` 可以重建；正文、状态回执、审查回执、整话封存与`history/`不能按缓存删除。确需清理时追加`--apply`，当前引用和每场最近一个未引用版本会继续保留。
