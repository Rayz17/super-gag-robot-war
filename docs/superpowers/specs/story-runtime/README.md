# Story Runtime Vault

本目录是《超GAG机器人大战》的知识工程工作区，不是第二套 Canon。

## 权威边界

- `docs/superpowers/specs/data/canon/` 及 `authority_manifest.tsv` 仍是机器权威。
- `generated/nodes/` 是 Hard + Working、`active` Canon 的只读投影，可删除并重建。
- `generated/support/` 是与 Current Canon 隔离的全剧创作支撑投影，包含总纲、机体生命周期、人物弧线、玩法、奖励、关系与长期对手。它能参与合同编译，但不能覆盖 Canon。
- `inbox/` 保存尚未审定的候选节点、关系与写作需求，不自动进入 Canon。
- `context-packs/` 保存按章检索、合同编译和单话写作使用的临时上下文包。
- `templates/` 保存 Obsidian 中可调用的候选记录模板。

不要直接修改 `generated/` 中的内容。需要修订事实时，应回到 Canon 源表完成迁移，再运行生成器。

## 重建

```bash
python3 scripts/build_story_runtime_obsidian_vault.py
python3 scripts/build_story_runtime_obsidian_vault.py --check
```

Vault重建会在Current与Candidate Support投影完成后同步重建
`generated/production/`，避免清空`generated/`时遗失生产隔离语料。

Canon 迁移后仍需运行：

```bash
python3 scripts/build_canon_authority_manifest.py
python3 scripts/check_canon_authority.py
scripts/canon-smoke-test.sh
python3 scripts/build_story_runtime_obsidian_vault.py
```

## 两层图谱

### Current Canon

- `generated/graph_nodes.tsv`
- `generated/graph_edges.tsv`
- `generated/runtime_corpus.jsonl`

这里只允许 Hard / Working、active 事实。写作合同可以引用它，不能反向静默修改它。

### Candidate Support

- `generated/support/support_graph_nodes.tsv`
- `generated/support/support_graph_edges.tsv`
- `generated/support/support_runtime_corpus.jsonl`

这里保存可迁移的全剧设计支撑。每个节点带 `candidate_support` 标记，并通过章节、人物、参战包和 Current 实体关系边与 Canon 对齐。它不是“第二套真相”。

## v3 分阶段知识与人物调用

v3是新创作的默认路线。Runtime不再一次编译一份「完整剧情合同」交给主笔，而是在创意、素材检索、实体建模、场面规划、正文、审稿和回写七个阶段重复查询。每次只提供当前决策所需的事实和素材。

```bash
python3 scripts/build_story_runtime_character_models.py
python3 scripts/check_story_knowledge_base.py

python3 scripts/compile_story_runtime_stage_context.py \
  --request <阶段请求.md> \
  --output-dir <阶段上下文包>
```

请求格式见`templates/Story-Runtime-v3阶段查询请求模板.md`。阶段值为：

每个阶段包会生成`06-writer-view.md`。主笔默认只读这一份决策视图；完整切片、TSV、trace和冲突表只给审计或定向二次查询，不得全量追加到作家Prompt。

- `ideation`：只看L1/L2/L3、上章出口、合法人物索引和机体/对手索引，先做三种故事选择。
- `research`：方案成立后，再查IP、名场面、模玩生态、关系、喜剧与What-if素材。
- `entity_model`：拉取选中人物的稳定模型切片、关系边、当前状态、机体归属与逐场存在方式。
- `scene_plan`：检查地点、尺寸、控制权、信息来源、最简单替代方案和场面出口状态。
- `draft`：只给一个已通过的场面链、明确活跃人物和正面声线，不给生产合同、坏句和设计答案。
- `review`：默认`cold_reader`，只给必要前情、成稿与独立事实切片；`design`和`benchmark`必须另行请求，不能让冷读者偷看作者答案或旧稿。
- `writeback`：只对用户确认的成果生成状态差量与迁移候选。

L1至L3不是每轮全量重复塞入；编译器只抽取本章需要的体验承诺、全剧发动机与结构职责。H0/Canon在建模与因果阶段加深；L4只作为可迁移的章引擎和出口；L4.5定义玩家如何看见；L5只提取已确认连续性或在冷读后揭盲；L6当前显式为空，不能反向假定。阶段政策见`production/layer_usage_policy_v3.tsv`，逐章来源和状态见`production/chapter_layer_source_registry_v3.tsv`。章级源默认只显示索引，必须以`admitted_layer_source_ids`逐项准入。

人物不在每次写作前临时重建。`data/character_runtime/character_model_registry.tsv`将人物的形成史、欲望、恐惧、行为、声线、关系、能力、机体、知识和当前弧线分别保留来源与权威层。`data/canon/scene_entity_presence.tsv`只记非默认的远程、作品痕迹、机魂联系、限定出场与禁止出场，防止人物被提前召唤或忽然拥有不属于他的机体。

新具名实体必须说明「现有人物为什么不能承担」、本章功能、离场/复用方式和资产成本。但Working事实与旧章引擎不是牢笼；主笔可否决并提交迁移，Runtime只禁止静默改写。

## v2.2 的现在定位

`compile_story_runtime_context_pack.py`及交互级事务工具保留为已定稿长单话的分段生产、缓存和回执工具，不再是从零构思章节的默认入口。未经选案和实体建模门的内容，不得直接进入v2.2的交互级拆分。

生产隔离的完整入口：

- `production/当前可用源清单-v1.md`
- `production/退役与隔离清单-v1.md`
- `production/文风污染报告-v1.md`
- `production/layer_usage_policy_v3.tsv`
- `production/chapter_layer_source_registry_v3.tsv`

`production/精简作家语料与Creative-First调用说明-v1.md`与静态Creative First内核已经退役，只供历史回归。

构建或修改生产源后必须运行：

```bash
python3 scripts/build_story_runtime_production_corpora.py
python3 scripts/build_story_runtime_production_corpora.py --check
python3 scripts/check_story_runtime_production_isolation.py
```

长单话和高密度单话不能再默认一次生成完。只有选案、人物/实体建模和场面规划通过后，才能进入以下交互级生产：

1. 用`单话场面事务计划-v1.tsv`规划完整场面或战斗阶段；
2. 编译单话稳定前缀；
3. 每次只组装一个场面事务上下文；
4. 场面正文通过局部审查后提交出口状态；
5. 后续场面只继承状态、必要旧场回执和上一场少量原文尾段；
6. 全部场面提交后机械合成整话，并通过接缝审查；
7. 封存期末状态供下一话使用。

交互级入口：

```bash
python3 scripts/compile_story_runtime_episode_run.py --help
python3 scripts/assemble_story_runtime_interaction_context.py --help
python3 scripts/prepare_story_runtime_interaction_review.py --help
python3 scripts/commit_story_runtime_interaction.py --help
python3 scripts/assemble_story_runtime_episode_draft.py --help
python3 scripts/seal_story_runtime_episode.py --help
python3 scripts/check_story_runtime_episode_run.py --help
python3 scripts/prune_story_runtime_interaction_cache.py --help
```

缓存采用章级、单话级、场面静态和交互差量四层结构，并以内容哈希寻址。编译器版本、共享schema和本地检索语料哈希也进入失效判断。较早场面改写会使后续场面及整话合成失效，但保留已提交正文、状态与审查证据供追溯。

`contexts/` 是可重建缓存；正文、回执、审查、期末状态与 `history/` 不是缓存。清理器默认 dry-run，只有追加 `--apply` 才删除不再引用的旧上下文：

```bash
python3 scripts/prune_story_runtime_interaction_cache.py \
  --run-dir <单话Runtime目录> \
  --apply
```
