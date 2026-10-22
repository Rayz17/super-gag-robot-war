# V34 Episode Loop / Pipeline Flow Repair Design

日期：2026-07-09

## 1. 问题判断

V31/V32 的主要失败不是“规则不够多”，而是规则没有形成稳定的数据流。许多设定、素材、分支、牺牲、机体、名场面和关系要求已经写进 canon、pipeline、episode loop、TSV 和账本，但写稿时它们经常停留在字段、候选池或审稿口号里，没有真正进入玩家能读到、玩到、记住的剧情场面。

因此旧 validator 能显示 pass，但只能证明目录、packet、ledger 和部分强字段存在，不能证明：

- 选中的素材真的被读了。
- 读到的素材真的进入本话构思。
- 构思真的变成可读剧情和可制作玩法。
- 分支、牺牲、what-if、机体/IP、名台词、关系爆点等没有被字段化后遗失。

V34 的修复目标不是继续堆 KPI，而是把每个“应该使用的素材”拉成一条可审计链路：

```text
Source selected -> Scene bound -> Reader visible -> Production visible -> Ledgered -> Next read carried
```

缺任何一环，都不能声称本话已经按 pipeline 和 episode loop 完成。

## 2. 新增三道硬门

### 2.1 Episode Input Manifest

每话写作前必须列出本话实际读取和选用的来源，不再只写“Canon/setting: 已查”或“Mecha candidates: 若干”。

必填信息：

- `source_class`：来源类型。
- `source_id`：表行、文档段落、母稿场面、补丁条目或前话债务编号。
- `selected_or_skipped`：selected / skipped。
- `selection_reason`：为什么本话需要它，或为什么跳过。
- `must_preserve_payload`：必须保留的情节、机体动作、名场面、关系动作、分支条件或制作要求。
- `read_scope`：实际读取的文件、行范围、章节或 packet。

建议 source class：

- `canon`
- `mother_draft`
- `accepted_patch`
- `50_issue`
- `mecha_ip`
- `quote_scene`
- `what_if_regret`
- `branch_variable`
- `finale_sacrifice`
- `relationship_sacrifice`
- `daily_life`
- `real_world_resonance`
- `value_axis`
- `wanji_body_mode`
- `production_split`
- `enemy_gain`
- `protagonist_memory`

规则：如果本话涉及分支、隐藏、say得、saved-death、名场面IF、牺牲、万机馆暴走、七海/白鸢/纪存关系爆点、真实证词、远星/索引/G.A.G.主线或新参战机体，必须至少有对应 source class 的 selected 行。没有就视为没有用上该层。

### 2.2 Scene Binding Matrix

写 Draft Synopsis 前，必须把每个 selected source 绑定到具体场面，不允许“素材已查，但后面自由发挥”。

每条绑定至少包含：

- `bound_readable_scene`：可读剧情里哪一段会出现。
- `player_action`：玩家做什么，没有玩法则写 skip reason。
- `character_action`：谁做了不可替代的动作。
- `mecha_or_map_action`：哪台机体、地图或展舰身体发生可见动作。
- `enemy_gain_or_misuse`：敌人如何偷学、误读、商品化、军用、清噪或封存。
- `state_delta`：本话之后改变什么。
- `next_required_read`：下一话或章节复审必须继续读什么。

规则：selected source 不能只绑定到字段、摘要、账本或“主题表达”。它必须至少进入一个可读场面，并且至少有一个角色动作、玩家动作、机体/地图动作或敌方收益。

### 2.3 Source Absorption Review

Writer Room Review 之后新增吸收审查。它只问一个很笨但很重要的问题：

> 玩家连读本话时，能不能感到这些素材真的变成了故事？

审查结果分三类：

- `pass`：素材已经进入可读剧情和制作拆分。
- `partial_warn`：素材进入了字段或制作拆分，但读感还弱；必须写 patch 或 watchpoint。
- `fail`：素材只存在于 Context Pack、Pressure Board、ledger、候选池或名词列表，剧情里看不到。

强制 fail 情况：

- 新机体只在字段列表里有名字，剧情和战斗里不行动。
- 名场面只写“映射某IP”，没有原创化桥段或玩家触发。
- 分支变量只写 ledger，没有改变路线、奖励、失败尊严或后续汇合差异。
- 牺牲语法只写“eligibility”，没有保护全队/世界或成全另一人的场面。
- 七海、白鸢、纪存只产生权限/水印/半格/若干秒之类小安排，没有情绪事件、关系后果或状态变化。
- 万机馆暴走、展舰变形、G.A.G.异常只写 UI 或系统红光，没有巨物动作、收益和可见代价。

## 3. 工程改动

### 3.1 Packet Template

`episode_loop_episode_packet_template_v0_2.md` 增加：

- `### Episode Input Manifest`
- `### Scene Binding Matrix`
- `## 7.1 Source Absorption Review`
- Gate Result 中的 `Source absorption gate`
- State Deltas 中的 `Source absorption delta`
- Auto Next Brief 中的 `Source absorption next reads`

### 3.2 Gate Checklist

`episode_loop_gate_checklist_v0_2.tsv` 增加 V34 门禁：

- 每话必须有 Input Manifest。
- selected source 必须绑定到场面。
- selected source 必须在 Reader Synopsis / Draft Synopsis 可见。
- selected source 必须在 Production Split 或 State Delta 可见。
- 分支、what-if、牺牲、机体/IP、名台词、价值轴和主角记忆不得只存在于字段。
- 章节 prefix review 必须检查 source absorption 是否在连读中成立。

### 3.3 Ledger Schema

新增 `source_absorption.tsv` 账本，字段：

```text
episode_id
source_class
source_id
selected_or_skipped
bound_scene
player_action
character_action
mecha_or_map_action
enemy_gain_or_misuse
state_delta
reader_visible
production_visible
absorption_status
next_required_read
```

### 3.4 Validator

`check_episode_loop_run.py` 新增可选开关：

```bash
--require-source-absorption
```

开启后要求：

- 每个 episode packet 有 `### Episode Input Manifest`。
- 每个 episode packet 有 `### Scene Binding Matrix`。
- 每个 episode packet 有 `Source Absorption Review`。
- `ledgers/source_absorption.tsv` 存在且字段完整。
- 每话至少有一条 selected source absorption 行。
- selected 行必须有 `bound_scene`，必须有至少一个动作/后果字段，必须 `reader_visible=yes` 且 `production_visible=yes`，`absorption_status=pass`。

该开关不影响旧 V31/V32 默认结构校验；旧稿可以继续作为历史稿通过默认 validator，但不能再声称通过 V34 素材吸收审计。

## 4. 对 Episode Loop 的影响

### 单话循环

每话顺序改为：

1. Previous Episode Audit。
2. Episode Input Manifest。
3. Context Pack。
4. Scene Binding Matrix。
5. Pressure Board。
6. Episode Card。
7. Draft Synopsis / Reader Synopsis。
8. Production Split。
9. Writer Room Review。
10. Source Absorption Review。
11. Patch Merge。
12. Gate Result。
13. State Deltas。
14. Auto Next Brief。

如果某个 source 在第 10 步 fail，不允许靠“下一话会补”直接推进，除非写入 `next_required_read` 和 unresolved/watchpoint，并明确这是非阻塞延后，而不是漏写。

### 章节复审

章节完成后，prefix review 除了连读戏剧性，还要检查：

- 每章重要 source 是否在读感中存在，而不是只在账本中存在。
- 分支经历是否让汇合点有差异。
- 机体/IP首登是否真的变成参战、支援、Boss、场景巨机、地图机制或可回收解锁。
- 七海、白鸢、纪存是否出现大动作、误会、牺牲、成长、破裂或状态改变。
- G.A.G./索引/远星/万机馆的宏观线是否被事件化。

发现问题时，仍按旧规则找最早根因章节 K，回到 K 重跑，并重放 K+1..N。若同一根因三轮未解决，写 unresolved issue，不继续死循环。

## 5. 这次修复针对的旧失败模式

### V31/V32 字段齐但读感弱

旧稿可以通过 `creative_experience_gates.tsv`，但读者仍然觉得小打小闹。V34 要求燃点、泪点、梗点、PV、机体、关系、主角动作都必须从 source 绑定到场面。

### 分支和牺牲在写稿中消失

旧 loop 里分支变量很多，但主线读起来没有不同经历。V34 要求 `branch_variable`、`what_if_regret`、`finale_sacrifice`、`relationship_sacrifice` selected 后必须绑定到玩家触发、失败尊严、汇合差异或后续必读。

### 参战机体被原创小机关稀释

旧稿经常把功能模块、盒子、手套、展签、规则机当成机体密度。V34 要求 `mecha_ip` selected source 必须在剧情和制作层说明它是 full unit / support unit / enemy unit / Boss module / scene mecha / new form 之一，否则只能是 non-count anchor。

### 名场面与名台词没有进入桥段

旧稿有时只说“投射某类名场面”，但读者 get 不到。V34 要求 `quote_scene` source 绑定到具体场面、台词 tier、触发方式和复用策略。

### 主角团只做小安排

旧稿中纪存、七海、白鸢常停留在记录、延迟、半格、留白。V34 要求这些动作必须绑定到更大后果：公开责任、权限变化、支援状态、路线变化、关系误解/救场/伤害、机魂记忆、敌方收益或公共代价。

## 6. 后续使用方式

新一轮 V34/V35 全剧重跑时，建议命令：

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py \
  docs/superpowers/specs/剧情梗概/V34 \
  --strict-prefix-warn-policy \
  --strict-creative-gates \
  --require-source-absorption \
  --min-story-chars 1200 \
  --min-new-ip-units 2 \
  --min-wanji-c01-samples 8
```

章节完成态再加：

```bash
--require-chapter-reviews
```

最终完成态再加：

```bash
--require-run-validation-log
```

## 7. 结论

V34 修复的是工程中的“吸收断链”。以后不是问“canon 有没有”“pipeline 有没有”“TSV 有没有”，而是问：

> 这些东西有没有变成玩家能读到、能操作、能记住、能在后续剧情里付账的场面？

如果没有，它就是没有被使用。

## 8. V35.4后继适配

V34解决`Source selected -> Scene bound -> Reader visible`吸收断链，但不负责判断来源是否来自正确作者槽、路线、舰群和生命周期。V35正式运行在V34吸收门之前增加 [V35.4槽位适配层](../2026-07-11-chao-gag-v35-slot-pipeline-adapter-v1.md)：

```text
Slot/Route/Fleet/Decision resolved
-> V34 Source Absorption
-> Single-Episode Pipeline
-> V35 Contract Gate
```

两层缺一不可。只开`--require-source-absorption`仍可能写出“素材都进入场面，但进入了错误路线、错误舰群或错误人生状态”的稿件；只开`--require-v35-slot-contract`则可能结构正确但读感里看不到素材。
