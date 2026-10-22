# V35.9 Story-First工作区

> 本页由 `scripts/build_story_workspace_index.py` 根据机器 Registry 与 Story Chain 生成。
> 不要手改状态；修改源表后运行 `python3 scripts/build_story_workspace_index.py --write`。

当前批次：`L4-C01-C05-20260724` / `active`；停止门：`C04_user_acceptance_then_C05_rebuild`。

## 当前入口

1. 当前故事：[C01章节Reader](reader/C01-闭馆以后万机出击.md) -> [C02章节Reader](reader/C02-章节连续阅读稿.md) -> [C03章节Reader](reader/C03-章节连续阅读稿.md) -> [C04E01《断冠来袭》](reader/episodes/C04/C04E01-Reader-v1.md) -> [C04E02《先给七号一副身体》](reader/episodes/C04/C04E02-Reader-v1.md)。
2. [章节制作索引](chapters/README.md)。
3. [机器状态说明](manifests/README.md)。
4. [最终内部验收](reviews/C01-C05连续阅读与Reader表演验收-v2.md)。
5. [C06冻结继承包](handoff/C05期末状态与C06继承包-v1.md)。

## 规则

- 当前故事只从 `reader/episodes/Cxx/`生成，章节Reader与跨章合订稿禁止手改。
- 每章是否有效只看对应 `manifests/Cxx-story-chain.tsv`。
- `reviews/`里的逐轮意见是过程证据，不是另一版正文。
- `maps/`、`migrations/`、`diagnostics/`和旧 `episodes/`是历史生产资料，不参与当前阅读。
- C06尚未初始化，不得从旧A5或旧C06稿直接继续。
