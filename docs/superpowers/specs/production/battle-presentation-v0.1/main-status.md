# 战斗演出 v0.1 主状态

> Status Authority: `current`
>
> 更新日期：2026-07-14

## 当前目标

验证“低成本 AI 美术 + Godot 实时组合”的战斗演出框架，并用馆守 Z 半跪低热量掌部防卫完成一条 C01 多玩法因果链：动态漫画/ADV → 探索 → 战前布置 → 短战棋 → 战斗演出 → 战后回收。

当前成果是 `candidate production pilot`，不替代冻结的 V35.10 Episode Packet，也未提升为全项目正式模板。

## 2026-07-14 叙事演出验证支线

新增一条不覆盖原切片的独立 ModeScene，用双段黄金样片验证动态漫画式探索演出与正比例机体短演出：

- `0号侧廊异响`：横向轻探索 → 主动调查 → 灯光/反光/摄影机/短句演出 → 普通通讯解锁。
- `馆守 Z 半启动`：维修环尺度镜头 → 兜灯 Cut-in → 手指微动作/灰尘/低热胸牌 → 半启动状态提议。
- 旧切片按 `V` 进入样片；`Esc` 返回。原战斗结算、三回合试玩与主入口均未覆盖。
- 机器可读镜头数据位于 `game-godot/data/cinematics/c01_golden_validation.json`；镜头本位于相邻 `cinematic-golden-slice-v0.1` 目录。
- 当前为 `candidate validation`：证明结构与镜头语法可行，不代表纪存走图占位、0号侧廊复用背景和程序合成音达到正式美术质量。

## 已确认边界

- 不修改 V35.8、V35.9、V35.10。
- 不修改 C01 Canon 动作、馆守 Z 半跪限制、首次登场或正式战斗数值。
- 战斗演出只消费 `BattleSession.last_resolution`，不拥有伤害、击破、行动结束或剧情事务结算权。
- 剧情 `PresentationQueue` 与战斗时间轴分离。
- 主 Session 只读美术 Session 的 `art-status.md` 和 manifest，不代写美术状态。
- 当前不引入新运行时插件、付费视频服务或商业授权。

## 总进度

- [x] 读取 runtime contract、主状态、美术状态与 manifest。
- [x] 在导入前生成合同差异报告。
- [x] 只导入 17 项 `approved_for_runtime + runtime_allowed=true` 资产。
- [x] 扩展馆守 Z 三地图态、三 Pose、兜灯 Cut-in 和封存无人机五态映射。
- [x] 完成 full / short / off、任意阶段安全跳过和视频回退。
- [x] 覆盖视频存在、缺失和加载失败三种路径。
- [x] 完成逐阶段跳过、20 次连续播放和不重复结算测试。
- [x] 完成 5 幅漫画、15 句 ADV、2 场景探索、4 条多轮对话和 3 条准备路线。
- [x] 完成 3 回合短战棋、敌方意图、结束阶段、胜负与战后状态回收。
- [x] 统一火灾口径：今晚火灾后 30 秒 → 三小时前；删除七年前火灾。
- [x] 统一七海门控：0 号异响后普通通讯台才可调查。
- [x] 通过 Godot、Canon、导入和 Windows PCK 资源路径验证。
- [ ] 3–5 名新玩家真人盲测与 10–15 分钟时长确认。
- [ ] 安装匹配 export templates 后生成 Windows 独立 EXE。
- [ ] 用第二台动作节奏不同的机体验证演出复用成本。

## 主要实现

```text
game-godot/scripts/c01_slice/c01_playable_slice_scene.gd
game-godot/scripts/c01_slice/c01_slice_director.gd
game-godot/scripts/c01_slice/c01_slice_state.gd
game-godot/scripts/c01_slice/c01_slice_battle_session.gd
game-godot/scenes/c01_playable_slice.tscn
game-godot/scripts/core/presentation/battle_presentation_director.gd
game-godot/scripts/core/presentation/battle_presentation_player.gd
game-godot/scenes/battle_presentation_player.tscn
```

主场景已切换到：

```text
res://scenes/c01_playable_slice.tscn
```

## 多玩法状态链

三个探索来源可解锁三项不同准备：

| 探索来源 | 关系/事实提交 | 战棋消费 |
|---|---|---|
| 兜灯胸牌安全锁 | 纪存接受兜灯停机权 | 馆守 Z 一次低热掌防可打断重型机 |
| 阿澄、小满撤离线 | 撤离队不等纪存回来 | 撤离灯获得额外完整度 |
| 0 号异响 → 七海普通通讯 | 获得执行顺序，不获得背书 | 第一回合公开敌方意图 |

玩家只需确认一条风险线，不要求清空所有对话。重访使用不同短对白，不重复选项或事务。

## 战斗演出状态

稳定演出 ID：

```text
presentation_id = BP_C01_GZ_PALM_GUARD_V01
pose_id = POSE_GZ_C01_KNEEL_PALM_GUARD_V01
sprite_state_id = SPR_GZ_C01_KNEEL_GUARD_V01
cutin_id = CUTIN_DOUDENG_C01_SAFETY_LOCK_V01
video_id = VID_GZ_C01_PALM_GUARD_V01
```

- `full`：约 7.17 秒。
- `short`：约 2.08 秒。
- `off`：立即完成。
- 三者使用同一战斗结算。
- 当前生产路径没有视频，使用批准静态 Pose + Godot FX。
- 测试 OGV 只验证视频状态机，导出包中明确排除。

## 运行方式

```bash
godot --path game-godot
```

- 方向键或按住鼠标：探索连续移动。
- `Enter` / 点击：调查、推进、确认。
- `Esc` / 右键：取消当前战棋命令或返回。
- `E`：随时结束我方阶段。
- `P`：切换 `full → short → off`。
- `V`：进入双段黄金镜头样片。
- `R`：重开切片。
- 演出中确认、取消或点击：安全跳过。

视觉总览：`outputs/c01-slice-visual/contact-sheet.png`。

双段样片关键帧：`outputs/c01-cinematic-validation/01-exploration.png` 至 `05-validation-complete.png`。

Windows PCK：`outputs/windows/chao-gag-c01-slice.pck`。

## 实测摘要

- 场景 ready：252.990 ms。
- full 演出：7175.004 ms。
- 稳态平均 FPS：106.384；最低 26。
- 峰值静态内存：115,563,704 bytes。
- 峰值纹理内存：118,418,585 bytes。
- 当前生产 PCK：17.623 MiB。
- 同代码无 C01 战斗美术基线：9.192 MiB。
- 该批演出美术实际包体增量：8.431 MiB。
- 生产视频增量：0 MiB。

## 验证

```text
python3 scripts/import_battle_presentation_assets.py --check  PASS
GODOT_BIN=/opt/homebrew/bin/godot ./scripts/godot-test.sh   PASS
res://scripts/c01_cinematic_validation_smoke_test.gd        PASS
./scripts/canon-check-godot.sh --strict                    PASS
./scripts/canon-smoke-test.sh                              PASS
Windows PCK required-path validation                       PASS
```

## 当前问题与决策门

- 探索画面仍偏功能示意，需要主展厅、0 号侧廊和角色走图资产。
- 首次大 Pose 进入 GPU 有帧时间尖峰，需要预热或运行时降采样。
- 本机缺少匹配版本的 Windows export templates，尚未产出 EXE。
- 还没有真人首玩时长、理解度和迷路点数据。

详细材料：

- `c01-playable-slice-production-brief.md`
- `joint-acceptance-report.md`
- `art-rework-issues.md`
- `technical-issues.md`
- `abc-presentation-tier-recommendation.md`
- `production-cost-package-model.md`

推荐：继续作为候选样板打磨；在真人盲测、Windows EXE 与第二机体复用通过前，不提升为正式生产标准，也不决定全游戏 A/B/C 数量和比例。
