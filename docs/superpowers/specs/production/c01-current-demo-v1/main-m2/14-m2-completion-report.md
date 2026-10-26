# C01E02 Current Candidate Demo M2 完成报告

> Status: `candidate_runtime_demo / internal M2 PASS / awaiting producer and user playtest`

## 原位重基结果

- 保留同一 Godot 项目、同一 `c01e02_g1_runner` 入口和同一 `candidate_runtime_demo/c01/e02` 内容路径，未建第二套可运行 Demo。
- `project.godot` 未修改；入口 `.tscn` 保持改造前 SHA-256 `a2bbe3d6d7bea7db79da88a6e575a10303af0dd9a2527b2d3470ba057323150b`。
- Revision 1 的 `12x9`、单 Boss、旧 CP3/Episode 终局、旧 fingerprint 和旧存档命名空间已从活跃运行链移除。
- 只读取制作人合同和 5 个冻结故事输入；没有修改 Canon、剧情正文、美术目录或共享 Autoload/Runtime。

## 已实现

1. S01–S07 单一连续入口，CP2 失败重试不重播同体揭示、撤令和起身。
2. 32x18 斩97四十五度户外棋盘，道路、楼房、街区、破损连廊、警戒设施和可破坏物均为实际世界层。
3. 边缘阈值平滑滚动，键盘、手柄、鼠标都保留馆守 Z 选中态和寻路反馈；HUD 与棋盘分栏。
4. 数据驱动的 2x2 馆守 Z、3x3 BREAKER、6 个 1 格小体、应急车辆、撤离口和警戒目标。
5. `ENEMY_C01_RIFT_SWARM` 逐体选择附近目标的确定性散乱 AI；不编队、不共享目标，全灭不构成胜利。
6. 固定因果顺序：取盾 → 挡下赤红冲击 → 最后车辆通过 → `rescue_lane=cleared` → 玩家亲手确认一次性盾拍。
7. 盾拍结果先原子提交，表现层只读播放；Full、Skip、静态 fallback 和退出重入逐字段等价。
8. 演出后回到同一连续战场，进入只读 `E02 Phase Checkpoint P1`，明确不是 Mission Clear。
9. Save schema 2 使用独立唯一槽；旧 schema/build/fingerprint 显式 fail-closed，不迁移、不覆写旧文件。

## 试玩

```bash
scripts/run_c01_candidate_demo_g1.sh
```

默认为无持久化验证。需要测试新存档槽时：

```bash
C01_M2_PERSIST_SAVE=1 scripts/run_c01_candidate_demo_g1.sh
C01_M2_PERSIST_SAVE=1 C01_M2_CONTINUE=1 scripts/run_c01_candidate_demo_g1.sh
```

战棋操作：方向键/WASD 移动光标，`M` 移动，`H` 取盾，`P` 拦截，`B` 立盾，`E` 结束回合，`F` 确认盾拍；鼠标和手柄也可用。

## 证据

- 左到右连续滚动：`C01E02_M2_SCROLL_LEFT_TO_RIGHT_1280x720.mp4`
- 多小体与撤离线战局：`C01E02_M2_SWARM_RESCUE_1280x720.mp4`
- 盾拍 Full / Skip：`C01E02_M2_SHIELD_BASH_FULL_1280x720.mp4` / `C01E02_M2_SHIELD_BASH_SKIP_1280x720.mp4`
- 边界、战局、静态 Cut-in 和 Phase 截图：见 `capture-manifest.tsv`
- 结果 payload、重放、存档和回归证据：见 `13-m2-test-summary.md`

## 仍缺资产

当前仅为具名几何灰盒，未装载任何未批准美术或旧资产。后续仍缺：馆守 Z/BREAKER/小体 Q/SD 与轻量动作，旧会展街区正式地图与遮挡规则，人物头像/立绘，取盾、挡击、盾拍 Pose/Cut-in，FX、音频和可选短视频。这些都需制作人/用户选择后再接入，本轮未自行冒充 Runtime 资产。

## 交接结论

M2 已达到制作人合同的内部工程门，但不宣称最终 Demo 用户验收。下一停止门是制作人/用户实际试玩，判断滚动战棋的可读性、操作手感和压力是否足以进入正式美术、小体设计与 LibTV 镜头阶段。

