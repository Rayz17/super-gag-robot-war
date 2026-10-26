# C01 2.5D 低热救援主程序联合验收报告 v1

> 场景：`SCN_C01_RM_RESCUE_2P5D_V01`  
> 日期：2026-07-14  
> 验收对象：`main-program-goal-v1.md`  
> 结论：**主程序候选验证通过；正式美术、真人盲测和第二场景复用未通过，因此不建议升级为全项目正式模板。**

## 1. 边界

本轮交付是独立的 C01 现实机器区 2.5D 低热救援验证，不覆盖：

- 旧 `c01_playable_slice.tscn`。
- 旧 `c01_cinematic_validation.tscn`。
- 正式 C01E01、六回合 SRPG 或 V35.10 Episode。
- V35.8、V35.9、V35.10 与 Canon TSV 进度。
- 美术 Session 的 `art-status.md` 批准结论。

所有结算均为 `candidate_preview_only`。表现层只提出一个幂等 preview outcome，不写正式剧情、战斗或存档状态。

## 2. 运行入口

```bash
cd /Users/rayz/Documents/超gag机器人大战
./scripts/godot-run.sh
```

直接指定场景：

```bash
/opt/homebrew/bin/godot \
  --path /Users/rayz/Documents/超gag机器人大战/game-godot \
  res://scenes/c01_real_machine_rescue_validation.tscn \
  --resolution 1280x720
```

默认主场景已设为：

```text
res://scenes/c01_real_machine_rescue_validation.tscn
```

### 操作

- `方向键 / WASD`：连续 X/Y 行走。
- 鼠标左键按住地面：持续朝指针移动。
- `E / Enter`：调查最近热点。
- `Enter / 左键`：推进对白。
- 战术阶段：点击右侧行动；R2 点击倒地点；R3 点击照射扇区。
- `Esc / Space`：只跳过当前演出，不跳过结算。
- 完成后 `Enter / R`：重播，preview 事务不会重复提交。

## 3. Must Deliver 验收

| # | 要求 | 结果 | 证据 |
|---:|---|---|---|
| 1 | 独立 `ModeScene`，不扩旧单体场景 | PASS | `c01_real_machine_rescue_validation.tscn` 继承 `ModeScene`；旧切片仍独立存在并通过回归 |
| 2 | 真 X/Y 浅纵深房间 | PASS | `CharacterBody2D`、walkable polygon、StaticBody 碰撞、Y-sort、前景栏杆、camera rail、距离热点；smoke 验证 X/Y 位移与遮挡层 |
| 3 | 三种对白 Profile | PASS | `scene_caption=72`、`halfbody_focus=6`、`cinematic_cutin=2`；大视觉占比 10%，普通场内对白占 90% |
| 4 | 同房间 R1/R2/R3 | PASS | R1 两个标准动作后被预测；R2 错误预览可撤回且正确位置由玩家确认；R3 诱导、拆罩、安全审查、低热输出完整 |
| 5 | 兜灯具名安全拒绝 | PASS | 扇区 A 明确指出机器犬；扇区 B 明确指出跌跌；不是无解释禁用按钮 |
| 6 | 馆守 Z 半跪低热一次输出 | PASS | 复用批准 Pose；outcome 固定为 `half_kneel_low_heat_support_used_once_hard_stopped`；无站起、攻击或伤害结算 |
| 7 | 七海四个可见审计操作 | PASS | 比对三线、恢复延迟、关闭自动结案/删档、实名锁镜像，必须按序执行 |
| 8 | 完整/任意跳过同结果，重入幂等 | PASS | 新 smoke 分别跑完整与全跳过路线，语义 outcome 精确相等；第二次进入 `commit` 被 ledger 去重；重播无脏状态 |
| 9 | 六张自动截图 | PASS | 见第 6 节；自动抓图已修正为 P1、P2、R2、R3、P3、P4 六个真实阶段 |
| 10 | smoke、Canon strict、回归、说明 | PASS | 22 个 Godot smoke、Canon strict、Canon smoke、PCK 资源验证全部通过；本报告与 README 提供入口 |

## 4. Acceptance 验收

| 验收项 | 结果 | 证据/说明 |
|---|---|---|
| 20 秒内可证明非单线横移 | PASS | smoke 使用真实 `CharacterBody2D` 前后与左右位移；walkable polygon 深度带约 360 px，前景栏杆参与 Y-sort 遮挡 |
| 四个巡检条件不自动赠送 | PASS | 开场只有交权；四项事实必须分别调查跌跌、机器犬/旧门、成年观众、低热扇区 |
| R1 原因为标准动作被预测 | PASS | 数据与演出文本均为“标准动作全部命中预测”，不读取数值门槛 |
| R2 玩家确认；R3 玩家执行 | PASS | smoke 与 paced route 均覆盖错误预览、撤回、正确占格、诱导、拆罩、两类拒绝和最终放行 |
| 至少 70% 普通对白无头像框 | PASS | 72/80 为 `scene_caption`，即 90%；大视觉 8/80，即 10% |
| 胸灯段半跪、低热、一次、硬停机 | PASS | 数据 outcome、状态和演出 Cue 三处一致 |
| 退出/跳过/重播无脏状态 | PASS | `request_skip` 只跳表现；重播清理 overlay、贴片机、灯光、审计和 tween；事务幂等 |
| 1280x720 稳态 60 FPS | PASS | 本机 M2 Max/OpenGL：探索 119.856 FPS，P95 13.403 ms；馆守 Z 119.868 FPS，P95 13.107 ms；0 帧超过 20 ms |
| 首次大图尖峰记录 | PASS WITH DEBT | 同步 `show_guardian` 调用 56.866 ms；正式资产总装前建议异步预热 |
| 全量门禁 | PASS | `godot-test.sh`、新增 smoke、Canon strict、Canon smoke 全绿 |

## 5. 实测时长

自动化完整路线使用真实场景、真实 CharacterBody2D 行走、完整演出和明确首读停留模型：

| 指标 | 实测 |
|---|---:|
| 墙钟 | `535.545s` |
| 分钟 | `8.926min` |
| 实际路线对白 | 79 行 / 1746 字 |
| 阅读停留 | `442.823s` |
| 决策停留 | `47.8s` |
| X/Y 移动 | 1195.164 世界单位 / `5.835s` |
| 完整演出 | 是，`skip_count=0` |
| 最终状态 | `COMPLETE` |
| preview 提交 | 一次，accepted |
| 移动/流程失败 | 0 |

证据：[paced-playthrough.json](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/paced-playthrough.json)。

这是一条 `scripted_first_read_pace_not_human_blind_test`：阅读速度为 4.7 中文字/秒，每行加 0.9 秒反应，最低 2.4 秒；它证明现有内容在透明首读模型下落入 8–12 分钟，不冒充 3–5 名新玩家盲测。真人迷路点、理解度和自然操作时长仍需另测。

## 6. 六张截图

1. [探索全景](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/01-explore-panorama.png)
2. [白框误分类](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/02-white-frame-misclassification.png)
3. [失败占格](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/03-failure-block.png)
4. [馆守 Z 低热胸灯](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/04-guardian-low-heat.png)
5. [回充余韵](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/05-recharge-afterglow.png)
6. [七海审计](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/06-qihai-audit.png)

联系表：[contact-sheet.png](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/contact-sheet.png)。

## 7. 性能与打包

性能原始数据：[runtime-performance.json](/Users/rayz/Documents/超gag机器人大战/outputs/c01-real-machine-rescue-v01/runtime-performance.json)。

测试主机：Apple M2 Max，Godot 4.7 stable，OpenGL 4.1 over Metal，1280x720。

- 场景 ready：154.985 ms。
- 探索稳态：平均帧 8.343 ms，P95 13.403 ms。
- 馆守 Z 稳态：平均帧 8.342 ms，P95 13.107 ms。
- 首次大图同步加载：56.866 ms。
- 大图显示后纹理内存：32,261,747 bytes。

PCK：

- [chao-gag-c01-real-machine-rescue.pck](/Users/rayz/Documents/超gag机器人大战/outputs/windows/chao-gag-c01-real-machine-rescue.pck)
- 大小：约 18 MiB。
- SHA-256：`d834eaffecf3f2e80a8529fa73eeee28c6817dbd5cd620b246ab5bfd612ef401`
- 包内资源验证：16/16 路径存在，主场景正确，测试视频夹具已排除，静态 Pose/FX fallback 可用。

本机没有 Windows 导出模板，因此本轮交付可复核 PCK，不伪报 Windows EXE。

## 8. 测试结果

2026-07-14 当前工作区执行：

```text
GODOT_BIN=/opt/homebrew/bin/godot ./scripts/godot-test.sh
PASS: 22/22 Godot smoke scripts

scripts/canon-check-godot.sh --strict
PASS: no runtime violations

scripts/canon-smoke-test.sh
PASS

Windows/PCK resource validation
PASS: 16/16 required paths; test fixture excluded

git diff --check
PASS
```

新增 `c01_real_machine_rescue_smoke_test.gd` 覆盖：

- 数据包与三 Profile。
- X/Y 移动、walkable polygon、Y-sort。
- 四项巡检不自动赠送。
- R1 两动作、R2 撤回、R3 两种具名拒绝。
- 馆守 Z 语义硬停机。
- 七海四步顺序。
- full/skip outcome 精确相等。
- 二次进入事务不重复。
- 重播清理脏状态。

## 9. 实现与数据

主入口：

- `game-godot/scenes/c01_real_machine_rescue_validation.tscn`
- `game-godot/scripts/c01_real_machine_rescue/c01_real_machine_rescue_validation.gd`

组合组件：

- `c01_rm_rescue_state.gd`
- `c01_rm_room.gd`
- `c01_rm_actor.gd`
- `c01_rm_prop.gd`
- `c01_rm_dialogue_presenter.gd`
- `c01_rm_tactical_overlay.gd`
- `c01_rm_hud.gd`
- `c01_rm_cinematic_canvas.gd`
- `c01_rm_cinematic_fx.gd`

共享演进：

- `scripts/core/modes/mode_scene.gd`
- `scripts/core/state/preview_transaction_ledger.gd`
- `scripts/core/cinematic/cinematic_director.gd`

数据：

- `game-godot/data/cinematics/c01_real_machine_rescue_validation.json`

验证工具：

- `c01_real_machine_rescue_smoke_test.gd`
- `c01_real_machine_rescue_capture.gd`
- `c01_real_machine_rescue_performance_probe.gd`
- `c01_real_machine_rescue_paced_playthrough.gd`

## 10. 美术 Manifest 差异

### 当前可用于运行时

本样片只读取既有 `battle-presentation-v0.1` manifest 中两项 `approved_for_runtime` 资产：

- `POSE_GZ_C01_KNEEL_PALM_GUARD_V01`
- `CUTIN_DOUDENG_C01_SAFETY_LOCK_V01`

旧 `portrait_jicun.png`、`portrait_doudeng.png`、`portrait_qihai.png` 只作为 JSON 中的禁止清单字符串出现，未被任何对白或序列加载。

### Phase A Keyframe

美术 Session 已交：

- `KF_C01_RM_2P5D_STYLE_V01`
- 状态：`pending_user_approval`
- `runtime_allowed=false`
- Phase B generated assets：0

因此程序未加载 Keyframe，也未把它截图冒充运行时。状态权威仍是：

- `cinematic-golden-slice-v0.2/art-status.md`
- `cinematic-golden-slice-v0.2/art-keyframe-manifest-v1.json`

### 仍为几何占位

- `BG_C01_RM_HALL_FAR/MID`
- `FG_C01_RM_HALL_OCCLUSION`
- `MASK_C01_RM_HALL_LIGHTS`
- 纪存、兜灯、唐胶、成年观众四方向 Sprite
- 跌跌、机器犬单体母版和动作帧
- 白框 FX 与裂罩贴图
- 纪存/七海审计半身

## 11. 已知问题

1. 人物、房间、白框和审计半身仍是明确几何占位，不能进行正式美术验收。
2. 馆守 Z 首次大图同步加载产生 56.866 ms 尖峰；Phase B 总装时应预载或线程加载。
3. 当前时长证据是 paced automation，不是 3–5 名新玩家盲测。
4. PCK 已验证，Windows EXE 尚未生成。
5. 四令音频 Cue 有数据但没有正式音效资产；流程不依赖音频。
6. 这是同房间轻战术验证，不是正式 SRPG 内核，也不证明完整 Episode 多模式切换。

## 12. 是否升级为正式模板

**不建议当前升级。**

可以确认：

- `ModeScene + 数据驱动 CinematicDirector + preview transaction` 方向可继续试制。
- 同房间 2.5D 探索与三步轻战术能够形成 8–12 分钟完整小弧。
- 小型机器承担解法、馆守 Z 承担受限高潮的结构成立。

升级前仍需：

1. 用户确认 Phase A Keyframe 后，完成 Phase B 分层背景、四方向 Sprite、动作帧与审计半身。
2. 3–5 名新玩家盲测，记录自然首玩时长、迷路点、错误理解和取消次数。
3. 处理首次大图预热。
4. 用第二地点或第二机体复用，证明不是 C01 专用控制器。
5. 接入上层 `EpisodeDirector / ModeRouter` 后验证正式探索到 SRPG 再到结算的跨模式闭环。

当前推荐状态：`validated_candidate_with_placeholders`。
