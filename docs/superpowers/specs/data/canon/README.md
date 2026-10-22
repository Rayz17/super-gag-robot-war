# Canon Index

本目录是《超GAG机器人大战》的机器可读设定入口。它负责回答“现在什么有资格约束其他会话”，不负责收纳全部创作历史。

## 四层权威

| 层级 | 含义 | 默认查询 |
| --- | --- | --- |
| `hard` | 用户确认且被多会话依赖的身份、空间、物理容量、Runtime或美术锁 | 返回 |
| `working` | 已采用的当前创作与设计方向，可以通过迁移继续改进 | 返回 |
| `candidate` | 试写、未来章节、50问题解法、素材池、未通过场面与资产候选 | 不返回 |
| `history` | 已替代、废弃别名、旧Runtime或仅供追溯的来源 | 不返回 |

权威裁决不再从某个表里的 `status` 字段猜测，而统一读取：

- `authority_manifest.tsv`：全部 Canon 记录的当前权威层、生命周期、版本范围和来源。
- `authority_overrides.tsv`：不能仅凭旧状态自动判断的人工裁决，例如当前 C02/C03、C04候选和 Hook。
- `identity_links.tsv`：同一角色、机体、参战包和生命周期 ID 之间的明确关系。

`authority_manifest.tsv` 由下列命令生成，不能手工只改输出而不改源表或例外表：

```bash
python3 scripts/build_canon_authority_manifest.py
python3 scripts/check_canon_authority.py
```

## 查询规则

默认查询只搜索 Canon 数据层，并且只返回 Hard + Working：

```bash
scripts/canon-query.sh 纪存
scripts/canon-query.sh entity CH_QIHAI
scripts/canon-query.sh scene V359-C03
scripts/canon-query.sh layout B1
```

候选、历史和设计图谱必须显式调用：

```bash
scripts/canon-query.sh candidate C04
scripts/canon-query.sh candidate entity CONCEPT_JICUN_MACHINE_SOUL_LINK
scripts/canon-query.sh history scene V31-C01E03-BATTLE
scripts/canon-query.sh index C04
scripts/canon-query.sh audit C04
```

- `current`：Hard + Working，默认模式。
- `candidate`：只看 Candidate Canon。
- `history`：只看 History/Deprecated；显式指定 `index` 时也可查历史图谱。
- `all`：Hard + Working + Candidate，不含历史，默认不查图谱。
- `audit`：全部 Canon 层加设计图谱，仅用于治理和追溯。

设计图谱中的 `canonical`、`needs_review` 或版本状态只说明索引节点自身状态，不自动等于 Canon 权威层。

## 数据边界

### 根 Canon

- `entities.tsv`：角色、阵营、参战包、机体、地点与世界概念的稳定身份。
- `scenes.tsv`：已采用场景、候选场景与历史场景；具体效力由权威清单裁决。
- `runtime_rules.tsv`：可扫描的实现规则。
- `gag_hooks.tsv`：已采用或候选的关系、喜剧与回收钩子。
- `character_mecha_art_locks.tsv`：角色与机体的美术锁、参考和缺口。

### 万机馆锚点

- `wanji_floors.tsv`、`wanji_locations.tsv`：硬空间骨架。
- `wanji_exhibition_zones.tsv`：展区空间和视觉密度锚点。
- `wanji_carrier_berths.tsv`：展舰容量与泊位物理边界。
- `wanji_roster_zone_coverage.tsv`：谱系与展区映射，属于可迁移的当前设计。
- `wanji_collection_taxonomy.tsv`：模型、玩具、实机、核心与参战机体的关系设计。
- `jicun_archive_terminal_views.tsv`：纪存信息终端的当前视图设计。

空间表内的尺寸、连接与容量是高权重锚点；`later_unlocks`、`scene_use`、`first_major_unlock` 等排期字段仍可随当前大纲迁移，不能仅凭空间表把候选章节写死。

### 不属于根 Canon 的内容

下列资料可以被写作流程选用，但不应出现在默认 Canon 查询里：

- IP、名场面、台词、意难平、模玩生态和研究素材池。
- 50项问题的诊断、解法与场面池。
- Pressure Board、Episode Loop、Pipeline 和制作验收过程。
- 尚未通过用户审读的章节候选、关系桥段和资产探索。
- 已替代版本与历史 Runtime。

这些资料通过 Design Graph、写作 Pipeline 或章节 Current Canon Pack 进入创作，不通过把数百个工作流概念伪装成世界实体进入。

## 当前剧情入口

唯一全局状态页是：

`docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md`

当前创作口径：

- L1体验宪章、L2总发动机与L3二十二章结构母盘为Working上位依据。
- C01-C03保留Creative Working故事事实，但不是内容金标准；十二个Current场景行已收敛为L3确认的最小章级事实，旧支持子场景、Reader、Runtime、Graybox和资产合同只作History复用参考。
- C01是当前唯一活动章，必须按story-chain从L4章级对齐、Canon收敛与预生产重新推进。
- C04-C05现有章包为Candidate；旧V35.9 C04 v4与旧C12 Pressure Board均不得反向决定当前结构。
- 黑展柜皇影、零号捷径三核心/设备化/停止权机制、旧十二章预算表和V35.5开局Pressure Board已于2026-07-24迁入History；0号侧廊空间与未解谜团仍可使用，固定未知声音与开启臂只属Candidate。

进入某一章前，优先读取该章的 Current Canon Pack，而不是全量检索所有版本。

## 迁移规则

任何 Canon 变更至少要记录：

1. 为什么旧条目不再适用。
2. 新条目属于 Hard、Working、Candidate 还是 History。
3. 哪些人物、机体、场景、资产和实现会受影响。
4. 哪些旧条目被替代或只保留为来源。
5. 已运行的校验命令。

每章完成`series_alignment`后、开始预生产前，还必须执行章首Canon收敛：把Current条目与L1-L3、本章对齐卡和上一章真实输出比较。只靠旧Reader、Runtime或资产合同自我引用的角色、装置和未来回收义务，必须先降级再写作。

完成变更后至少运行：

```bash
python3 scripts/build_canon_authority_manifest.py
python3 scripts/check_canon_authority.py
scripts/canon-smoke-test.sh
```

表结构与字段说明见 [schema](./references/schema.md)。
