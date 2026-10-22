# V35章节生产链机器门禁

这里的TSV不是剧情资料，而是章节生产状态机。它负责证明一章确实按以下顺序通过：

```text
章级对齐
-> 章级预生产
-> 导演板 / 战斗预案 / 必要物理板
-> 剧情—游玩拓扑与状态桥接
-> 完整剧情总纲
-> 独立首读因果盲审
-> 逐话结构表 / 状态账 / 四视角章审 / 累计连续性回执
-> 章级演出承载规划
-> 单话Episode Reader
-> 机械合成章节Reader
-> 人类声线语义审查
-> 章节审定
-> 用户创作验收
-> 下一章
```

## 硬规则

1. `passed`与`generated`是唯一能解锁下游的状态，而且必须保存与当前文件一致的SHA-256。
2. 文件存在不等于通过。`invalidated`表示只可作为重做输入，不能继续生产。
3. 上游改动后哈希失配，所有依赖它的下游自动失去通过资格。
4. Reader合成器必须接收本章manifest；缺少完整总纲、演出承载或任一未通过单话时直接失败。
5. 进入下一章前，`advance`门要求章节Reader、人类声线语义审查、章节审定及用户创作验收全部通过。
6. `V35-upper-layer-registry.tsv`与`V35-chapter-registry.tsv`登记全剧六层和C01-C22；`V35六层创作生产看板.md`只能由报告脚本生成。
7. `production_profile`只允许`light`、`standard`、`heavy`或尚未开章的`unassigned`。重量章必须启用物理板；所有档位都必须经过首读盲审、声线语义审查和用户验收。
8. `user_acceptance`只能由`record_v35_user_acceptance.py`根据用户明确决定封存，通用`--record-stage`命令、批量运行和沉默都不能代替。
9. Episode只是叙事连载切点，不天然等于一场关卡或一次`Mission Clear`。`story_play_topology`必须先把Episode、Operation、Encounter、Phase、Checkpoint和结算边界作多对多映射，并记录跨段`IncidentState`。
10. 户外战棋默认采用可滚动地图，建筑、道路和可破坏物属于棋盘本体；只有封闭室内或明确的局部工具玩法才可使用固定小地图。地图变化不得抹掉同一Operation的伤势、装备、敌群、破坏态与当前目标。
11. `story_play_topology`含`decision_pending`、空Operation/Encounter/Phase/故事单元/状态ID、跨章Episode ID或无来源的`carry_from_state`时不得封存。候选读取参数不具备解锁效力，迁移器也必须先跑语义校验。

## 命令

查看全剧当前层、活动章、缺口和下一门：

```bash
python3 scripts/report_v35_layered_pipeline.py
```

初始化已经被前章`advance`解锁的新章：

```bash
python3 scripts/init_v35_story_chain.py \
  --chapter C02 \
  --episodes 4 \
  --physical-board required \
  --profile heavy \
  --chapter-title '木桶街，万机初开'
```

查询本章下一合法阶段：

```bash
python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C01-story-chain.tsv \
  --next
```

检查章级剧情—游玩拓扑：

```bash
python3 scripts/check_v35_story_play_topology.py \
  docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C04/C04-剧情游玩拓扑与状态桥接.tsv \
  --chapter C04
```

```bash
python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C01-story-chain.tsv
```

只检查某个生产入口：

```bash
python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C01-story-chain.tsv \
  --target write-outline

python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C01-story-chain.tsv \
  --target write-episode

python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C01-story-chain.tsv \
  --target assemble

python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C01-story-chain.tsv \
  --target advance
```

某项经人工与对应审查通过后，才由命令封存当前哈希：

```bash
python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C01-story-chain.tsv \
  --record-stage complete_outline \
  --record-status passed
```

不得先把状态手填为`passed`，再补内容。

上游返修时自动废止其全部下游：

```bash
python3 scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C01-story-chain.tsv \
  --invalidate-stage complete_outline
```

封存或失效操作会自动刷新全剧六层看板。

章内话数不是机械配额。若L4在逐话结构表封存前决定调整，使用：

```bash
python3 scripts/resize_v35_story_chain.py \
  --chapter Cxx \
  --episodes <新话数> \
  --migration-doc docs/superpowers/specs/<已登记迁移文档>.md \
  --reason '<容量变化原因>'
```

它会在一次事务中同步上位registry、章节registry、manifest和看板；当前话数上界从L3 Registry动态读取。突破上界时在同一命令加入`--new-ceiling`。若`first_read_causal_audit`或其下游已封存，先使该阶段失效。

记录用户明确的创作验收：

```bash
python3 scripts/record_v35_user_acceptance.py \
  --chapter Cxx \
  --evidence '<用户明确决定>' \
  --scope '<被认可的文件与边界>'
```
