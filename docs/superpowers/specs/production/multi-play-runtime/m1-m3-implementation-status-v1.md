# 《超GAG机器人大战》多玩法运行时 M1-M3 实现状态 v1

> 日期：2026-07-14  
> 状态：候选运行时实现回执  
> 上游蓝图：`2026-07-14-chao-gag-multi-play-implementation-blueprint-v2.md`  
> 边界：记录已经运行和测试的工程事实；不改变 V35 正式进度，不批准美术资产，不裁决第一话正式战斗版本。
> 后续状态：M4、M5 已实现，当前状态请续读 `m5-constraint-implementation-status-v1.md`；本文件保留 M1-M3 的首轮证据。

---

## 1. 本轮结论

当前工程已经跑通第一条真正跨独立模式、共享同一因果状态的纵向链：

```text
Narrative
  -> EpisodeDirector / ModeRouter
  -> C01 Spatial Incident
  -> ActivityOutcome / StateTransaction
  -> RunStateStore
  -> Desk / Notebook overlay
```

这证明多玩法可以表现为同一话中的不同玩家权能，而不是几个互不相干的小游戏。M1-M3 本身没有证明正式 SRPG、活动模板复用、第二地点或第二机体；前两项后来由 M4/M5 扩展验证，但蓝图仍是候选方案。

## 2. 已实现组件

| 层 | 已实现 | 当前责任 |
| --- | --- | --- |
| 共享内核 | `GameKernel` | 启动/关闭 Episode，协调路由、状态、输入与存档服务 |
| Episode 编排 | `EpisodeGraph`、`EpisodeDirector` | 读取声明式节点图，执行进入、完成、转移与稳定边界存档 |
| 模式路由 | `ModeRouter`、`ModeContext`、`ModeScene` | 实例化独立场景，执行 prepare/enter/activate/suspend/resume/exit 生命周期 |
| 因果状态 | `RunStateStore`、`StateTransaction`、`OutcomeValidator` | 验证并幂等提交事实、关系、实体变化、债、战斗设置与反应 |
| 输入与覆盖层 | `InputRouter` | 在 Narrative/Spatial/Tactical/Desk 与 notebook overlay 间切换输入权限 |
| 保存恢复 | `SaveService` | 保存当前节点、模式快照、未完成草稿和已提交事务；恢复到同一稳定边界 |
| 内容注册 | `ContentRegistry` | 将 Episode 清单中的模式 ID 解析为场景路径 |
| 模式壳 | Narrative、Spatial、Tactical、Desk | 四类玩家权能都有独立入口；M1 时 Tactical 仅为合同验证壳，后续 M4 已升级 |

## 3. C01 纵切接入

内容包：

- `game-godot/content/episodes/c01/e01/manifest.m1.json`
- `game-godot/content/episodes/c01/e01/graph.m1.json`
- `game-godot/scenes/c01_multi_play_m1_validation.tscn`

当前图只用于 M1-M3 工程验证：

1. Narrative 建立当前戏剧问题。
2. 进入既有现实机器区 2.5D 样片，作为 `SPATIAL Incident`。
3. 完成后不再写入样片私有 preview ledger，而是提出统一 `ActivityOutcome`。
4. `RunStateStore` 一次性提交馆守 Z 状态、爹爹关系边、膝部检查债、后续战斗设置和人物反应。
5. Episode 路由进入 Desk；笔记本作为覆盖层暂停/恢复当前模式，而不是销毁重建现场。

该图明确不宣称：正式 C01 Episode、正式战斗回合数、正式美术晋级或 V35.10 解冻。

## 4. 已验证的行为

`multi_play_runtime_m1_smoke_test.gd` 已验证：

- 模式切换后旧场景停用并脱离运行树。
- Spatial、notebook overlay、Tactical 输入上下文正确切换。
- 打开笔记本再返回时，玩家位置不重置。
- 保存/读取恢复精确模式、位置和未完成 Tactical 草稿。
- 同一事务 ID 重复提交不会重复产生世界结果。
- 提交前的存档恢复后仍只允许该时间线提交一次。

`c01_multi_play_incident_integration_smoke_test.gd` 已验证：

- 现实机器区样片可由 `ModeRouter` 托管。
- 保存/恢复返回精确位置，不重播入口对白。
- 样片完成后进入 Desk，旧 preview ledger 保持为空。
- 统一状态收到实体变化、关系边、具名债和 `BattleSetupPatch`。
- Desk/Notebook 往返和复盘事务均能正确提交。

2026-07-14 全量 `scripts/godot-test.sh` 通过 25 个测试脚本；新增标志为：

```text
MULTI_PLAY_RUNTIME_M1_SMOKE_OK
C01_MULTI_PLAY_INCIDENT_INTEGRATION_OK
```

## 5. 尚未完成

1. **M4 后续边界**：声明式 Tactical 适配和结果回流已在后续回执验证，但第一话正式采用3回合还是6回合仍未裁决，正式 Episode 仍为 0。
2. **M5 后续边界**：`CONSTRAINT` 已在后续回执形成可复用控制器与内容 schema；`TIMING`、`SIGNAL` 仍未实现。
3. **M6 复用证明**：第二地点、第二机体、第二 Episode 还没有用同一框架生产。
4. **内容编译器（后续已补）**：M1 当轮仍由手写 JSON 直接加载；2026-07-15 后续已实现确定性 Episode bundle、schema lint、场景/资源/Patch 引用闭包与负例测试，见 `m6-content-bundle-build-chain-status-v1.md`。
5. **生产体验**：异步预载、正式转场、音乐总线、Windows EXE、长时游玩和真人盲测仍未通过。
6. **美术边界**：本轮不触碰 B1/Y=450 等既有 2.5D 美术坐标与资产晋级问题。

## 6. 第一话版本冲突

| 来源 | 当前口径 | 权威状态 |
| --- | --- | --- |
| 旧合并版/现设计索引旧条目 | 闭馆探索后进入 6 回合保护战 | 既有制作标准，待新版本正式覆盖 |
| V35.10 冻结候选 `V3510-C01E01` | 3 回合现实机器救援 | 冻结候选，未通过全剧 Pressure Board 门禁，正式 Episode 仍为 0 |
| 当前 2.5D 样片 | 同房间 Spatial Incident 与轻战术 | 工程验证样片，不是正式 SRPG |

在剧情部门正式裁决前，程序不得把三者混写成同一个既定事实。M4 应通过数据驱动 `BattleSetupPatch` 接入战术场景，使正式口径可以替换内容而不重写共享内核。

## 7. 下一实施顺序

1. M4 已建立数据驱动 Tactical adapter 与四类 `BattleOutcome` 回流。
2. M5 已建立首个 `CONSTRAINT` 活动控制器，并验证路线、法务和调度复用。
3. 下一步用第二地点和第二机体做一次无复制的 Episode 接入，并实现首个 `TIMING`。
4. 再做真人时长、平台导出与美术联调，决定是否升级为 Working Canon。
