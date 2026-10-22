# 《超GAG机器人大战》多玩法内容 Bundle 构建链状态 v1

> 日期：2026-07-15  
> 状态：`candidate_build_chain_validated`。  
> 上游：`2026-07-14-chao-gag-multi-play-implementation-blueprint-v2.md` 第 8.3 节。  
> Canon 边界：构建链只证明内容引用闭合、schema 合法和运行时装载一致；不提升任何验证 Episode，不裁决 C01 战斗版本，不解冻 V35.10。

## 1. 解决的问题

此前 M1-M6 直接读取分散的 Graph、Activity 和 Battle JSON。单个文件即使合法，也不能证明：

- Episode 图引用的场景已登记。
- 图内活动和战斗都由 manifest 声明。
- 活动产生的 `BattleSetupPatch` 真有战斗消费者。
- 3 回合/6 回合等同战斗不同版本没有被误判为重复内容。
- 测试和导出运行的是当前源文件对应的同一份内容。

这会让剧本、美术、玩法和程序会话各自改动后仍能局部通过，却在运行时拼出另一套结果。

## 2. 当前构建链

```text
Canon strict gate
  -> Episode manifest
  -> EpisodeGraph schema / scene / edge validation
  -> Activity grammar validation
  -> Battle schema / cell / unit / objective / intent validation
  -> Activity Patch -> Battle patch_catalog closure
  -> StableObject / InteractionOffer -> Tactical binding closure
  -> ExperienceContract / continuity / four-consumption closure
  -> capacity receipt comparison
  -> inline resource embedding
  -> deterministic source fingerprint
  -> self-contained Episode bundle JSON
  -> ContentRegistry runtime registration
```

仓库根目录执行：

```bash
GODOT_BIN=/opt/homebrew/bin/godot ./scripts/compile-multi-play-content.sh
```

脚本先运行 `canon-check-godot.sh --strict`，再生成四个稳定包。Godot 运行时不解析 Markdown 或 TSV。

## 3. Bundle 合同

每个 bundle 包含：

- `bundle_schema_version`、Episode ID、状态与 `canon_boundary`。
- 原 manifest 与确定性 `source_fingerprint`。
- 已校验并嵌入资源的 EpisodeGraph。
- 按源路径索引的活动/战斗定义及各自 SHA-256。
- 构建器已经执行的图、场景、活动、战斗和 Patch 闭包合同。
- Manifest 要求时，每个节点的转场 ID、类型、地点、因果、责任与时长范围。
- Manifest 声明的背景与人物图，以及 Graph 中 `presentation` / `workbench` 对这些资产的闭合引用。
- Graph 中的 StableObject/InteractionOffer，以及 Battle 中单位部件、武器、目标、事件、格位和 flag 对同一对象的闭合映射。
- `experience_contract_report`，分别记录结构门禁和真人容量回执是否通过，避免用一个总 PASS 混淆两类证据。
- 经验证的容量回执只以 SHA-256 资源条目进入指纹，不把完整私人输入记录嵌入 bundle。

活动和战斗节点保留原始路径用于追溯，同时增加：

- `activity_definition`
- `timing_definition`
- `battle_definition`

运行时优先读取内嵌定义；源路径只用于旧内容兼容，不再是 M1/M4/M5/M6 验证入口的主要依赖。

## 4. 当前输出

| Episode | 输出 | 内嵌资源 |
| --- | --- | ---: |
| M1 C01 接线 | `content/generated/episodes/c01/e01/m1.bundle.json` | 0 |
| M4 C01 战术 | `content/generated/episodes/c01/e01/m4.bundle.json` | 2 个战斗版本 |
| M5 约束复用 | `content/generated/episodes/runtime_validation/m5.bundle.json` | 3 活动 + 1 战斗 |
| M6 第二 Episode | `content/generated/episodes/runtime_validation/m6.bundle.json` | 2 活动 + 1 战斗 + 5 演出资产 |

同一源文件连续构建的四个输出逐字节一致。M4 以 `battle_id + variant_id` 作为版本唯一键，因此同一战斗的 3 回合和 6 回合版本可以并存，不会被错误合并或误报重复。

## 5. 构建时阻断

当前会直接失败的情况包括：

1. manifest、graph 或资源缺失/JSON 损坏。
2. manifest 与 graph 的 Episode ID 不一致。
3. 起始节点、出口、失败/取消边或目标节点非法。
4. 未知主模式或未登记 `scene_id`。
5. 图引用了 manifest 未声明的活动/战斗。
6. Activity grammar、槽位、卡片、Timing 阶段或结果合同非法。
7. 战斗格子越界、单位/目标重复、意图目标不存在或 Patch 操作引用不存在对象。
8. 活动结果产生 Patch，但该 Episode 没有战斗 `patch_catalog` 消费它。
9. bundle schema 或 `canon_boundary` 在运行时注册时不匹配。
10. 必需转场缺失、ID 重复、类型非法，或把同一句话同时写成因果和下一责任。
11. Graph 引用了 manifest 未声明的背景/人物图，或演出资产文件不存在。
12. StableObject/Offer ID 或前置非法，战术 binding 指向不存在对象，或重要稳定对象没有 Tactical 映射且未声明跳过理由。
13. 正式 Episode 缺失 `EpisodeKnot`，或人物/机体主张、不可逆成本、下一债务不完整。
14. 非开场模式切换少于两条连续性，或对象连续性引用未知稳定对象。
15. 戏剧对象没有跨至少三个模式的真实 beat、Offer、Battle binding 或 Desk anchor。
16. 玩家承诺缺少立即、冲突、人物、结算任一消费槽，或槽位没有玩家可见证据。
17. InteractionOffer 没有显式重复策略、结果合同或失败继续路径。
18. 具名机体的 `machine_claim` 没有引用真实单位/武器动作 Cue。
19. 未使用玩法层没有戏剧上的 `skip_reason`。
20. 正式 Episode 的容量回执 pending、缺失、未完成、Episode 不匹配或时长落在声明档位之外。

## 6. 运行时接入

- `ContentRegistry.load_episode_bundle()` 校验并登记稳定包。
- M1、M4、M5、M6 可视入口均从 bundle 取得 Graph。
- `ConstraintActivityHostMode`、旧拳王维修棚和 `BattleSetupResolver` 优先读取节点内嵌定义。
- M6 完整五节点测试使用编译 Graph，仍通过探索、复合活动、战棋、人物关系和 Desk 五次事务闭环。
- Windows 导出包验证要求包含编译器与 M6 bundle，并检查三项内嵌内容和 `runtime_validation_only` 边界。

## 7. 自动证据

`multi_play_content_compiler_smoke_test.gd` 覆盖：

- 四个 manifest 均可编译、重复编译结构一致。
- 仓库中的生成包与当前编译结果逐字节一致。
- bundle 可由 `ContentRegistry` 注册并取得 Graph。
- M6 的 `CONSTRAINT`、`TIMING` 和 Battle 可以脱离源路径用内嵌定义配置。
- 未知场景、未声明活动和无消费者 Patch 的负例被拒绝。
- M6 Canon 边界保持 `runtime_validation_only`。
- M6 三张背景与两张人物图进入资源索引和确定性指纹；未声明演出资产负例被拒绝。
- M6 六个稳定对象与六个 Tactical binding 闭合；删除零件盘 binding 的负例会以具名对象 ID 拒绝构建。
- M6 P4 结构合同通过，但 bundle 明确记录 `structure_pass_capacity_pending`，不伪造外部时长证据。
- 删除模式连续性、人物消费槽或 Offer 失败继续路径的负例均被具名拒绝。
- 40 分钟完成回执通过 `standard` 容量档；3 分钟回执被拒绝；正式状态不能使用 pending 容量证据。

上述测试已经并入 `scripts/godot-test.sh`，并与 M1-M6 运行时测试、模式交接转场、Narrative/Desk 生产壳、Spatial/Tactical 同物连续性、三房间 Spatial 生产层及 strict Canon 检查一同通过。P3b Tactical 地图视觉更新后的 M6 bundle 含 11 项资源索引，指纹为 `b838cddf609cc4b1eaf7d70677d9415c83906378a6682d8f027d6889409aa34c`；编译器同时记录 `battle_presentation_manifest_validated=true`。Windows EXE/PCK 已同步重导出，包内 58 个必需路径、九个地图视觉、八个程序化 profile、旧拳王表现清单/地图图/Pose、P2-P4 共享运行时、Spatial/体验结构状态和容量 pending 状态通过独立 PCK 验证，嵌入 PCK 与独立 PCK 逐字节一致。

## 8. 尚未替代的门禁

构建通过不等于内容通过。它不能替代：

- 真人对剧情因果、玩法动机和角色反应的理解。
- Windows 真机、实体手柄、字体和布局验收。
- 正式 Episode Packet、Pressure Board、台本、资产与演出验收。
- `SIGNAL` 活动控制器；编译器目前会明确拒绝尚未实现的 grammar。
- C01 正式采用 3 回合或 6 回合版本的剧情裁决。

因此它是生产一致性基础设施，不是新的玩法，也不是 Canon 晋级捷径。
