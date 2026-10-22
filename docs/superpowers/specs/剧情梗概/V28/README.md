# V28 ELO 运行目录

状态：V28 逐话循环编剧运行目录。C01-C03 已按 packet-first 流程完成 12 个 episode packet、3 个章节组装稿、3 个 prefix review 和对应 ledgers，当前整体为 warn-through，可供用户连读审稿后决定是否从 C04 继续。

V28 以后不再把多章合并稿当作真正 ELO 产物。真实运行必须按以下结构推进：

- `episodes/`：一话一个 episode packet，源稿。
- `chapters/`：章节组装稿，只能由已通过 packet 生成。
- `reviews/`：每章 prefix regression review 和 regression replay log。
- `ledgers/`：机器可读 TSV 账本。

当前已完成：

- `episodes/C01E01-今日闭馆后馆名被冻结.md`
- `episodes/C01E02-馆守Z手臂成为地图.md`
- `episodes/C01E03-勇气审批第3回合.md`
- `episodes/C01E04-流亡展舰起航.md`
- `episodes/C02E01-木桶街入夜.md`
- `episodes/C02E02-限定版暴乱.md`
- `episodes/C02E03-胶价王拍卖台.md`
- `episodes/C03E08-灰模没有签名.md`
- `episodes/C03E09-母版夜潜.md`
- `episodes/C03E10-站不住的英雄.md`
- `episodes/C03E11-预展听证.md`
- `episodes/C03E12-三联展柜.md`
- `chapters/C01-闭馆夺名与展舰起航.md`
- `chapters/C02-模型街临时开馆.md`
- `chapters/C03-原型工房与灰模母版.md`
- `reviews/C01-prefix-review.md`
- `reviews/C02-prefix-review.md`
- `reviews/C03-prefix-review.md`

最终校验：

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py \
  docs/superpowers/specs/剧情梗概/V28 \
  --require-subagents \
  --require-chapter-reviews \
  --require-run-validation-log \
  --min-story-chars 1200
```

结果：`PASS: docs/superpowers/specs/剧情梗概/V28 has 12 episode packet(s), 3 chapter file(s), 3 prefix review(s).`

当前连读 watchpoints：

- C04 必须从 C03 的 `failure_note_to_c04`、`failure_record_integrity` 和现实机器小舞台灰显入口自然进入，不可突然换题。
- 七海在 C01-C03 已有流程刺痛和安全表轻触，C04-C08 需要继续升级为更大职业代价和更有情绪的关系事件。
- 机体密度必须继续维持，不能回到只写证词/展签/功能模块的状态。
- G.A.G./索引/远星宏观线目前只是打底，后续章要逐步抬升到宇宙尺度和文化共同语言。

运行前优先读取：

- `docs/superpowers/specs/2026-07-02-chao-gag-episode-loop-writing-workflow.md`
- `docs/superpowers/specs/data/story/episode_loop_episode_packet_template_v0_2.md`
- `/Users/rayz/.codex/skills/chao-gag-writing-pipeline/references/writer-room-subagents.md`

完成任何一批后，必须运行：

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py \
  docs/superpowers/specs/剧情梗概/V28 \
  --require-subagents \
  --require-chapter-reviews \
  --require-run-validation-log \
  --min-story-chars 1200
```

如果没有实际启用子agent，只能去掉 `--require-subagents` 并在每个 packet 标记 `Reviewer Mode: single-context fallback`，不能声称为子agent编剧室产物。

首次检查时先去掉 `--require-run-validation-log`。通过后将实际 validator 命令和 `pass` 结果写入 `ledgers/run_validation.tsv`，再带该参数复跑作为完成态证明。
