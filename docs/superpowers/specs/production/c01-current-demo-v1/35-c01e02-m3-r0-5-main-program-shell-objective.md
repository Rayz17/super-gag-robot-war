# C01E02 M3-R0.5｜主程序 M0 零资产表现壳目标

> 派发对象：主程序 Session
>
> 状态：`authorized Candidate implementation / shell only / zero real handoff`
>
> 停点：零真实资产可玩壳、接口回执和捕获完成后停止

## 1. 开工顺序

1. 使用 `chao-gag-canon`；
2. 完整读取 10、31、32、33、34 号合同；
3. 读取 `main-m3-r0/00–04`、R0 代码、profile 和测试；
4. 运行 `python3 scripts/report_v35_layered_pipeline.py --check`、`python3 scripts/check_c01_current_demo_contract.py` 与 `./scripts/test_c01e02_m3_r0.sh --skip-capture`；
5. 用 `40-c01e02-m3-r0-5-frozen-contracts.sha256` 核验 33–39、R0 resolver/profile 与冻结输入，并记录当前 Git 边界。

任一冻结输入不符时停止，不自行更新制作人合同。

## 2. 唯一目标

在同一 Godot 项目中新增一个非默认 `m3_r05` 表现沙盒，完整复用 R0 resolver/profile 与三个草案，用**具名几何、程序 UI 和合法合成音**实现 34 号的交互和演出壳。

本轮必须证明：

- 玩家界面与调试层已分离；
- 角色通讯、意图显示、摘要和执行围绕同一个回合数据运行；
- 结算不是单帧跳转，B03–B08 有可验证的时间轴、相机、对象移动、命中停顿和回退点；
- 真实美术为 0 时仍可玩且不探测 A6/A7 目录；
- 等未来 exact handoff 后，可逐槽替换资产，不改玩法和布局。

## 3. 实现分层

建议结构，等价命名可以：

```text
M3R05Runner
  ├─ SharedRoundAdapter          # 只读调用 R0 resolver
  ├─ PresentationGridTransform  # 整数格 → A4 40x20 显示投影
  ├─ TacticalBoardView          # 等距地图、单位、路线、意图
  ├─ PlayerPlanningHUD          # 玩家指令和作战摘要
  ├─ CharacterCommsLayer        # 角色头像、通讯和 trigger_once
  ├─ RoundPresentationDirector  # 不反写 gameplay 的 beat player
  ├─ PresentationAssetResolver  # 零 handoff fail-closed
  └─ DeveloperOverlay           # F3 调试层
```

不得把新界面、通讯、演出、资产加载和 resolver 再次堆进一个 `_draw()` 大函数。使用 Godot `Control`、`CanvasLayer`、`Camera2D`、`AnimationPlayer`、`TextureRect`、`AudioStreamPlayer` 等引擎节点表达明确层级。

`PresentationGridTransform` 锁定 `isometric_tile_half_40x20` 与 topology `baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8`，但不修改 R0 profile 文件。至少用馆守 Z、BREAKER、东口、墙挂盾和三个固定格位证明 40×20 映射与 A4/M2 对齐；镜头缩放不得破坏 pivot 和 footprint。

## 4. 表现约束

- `RoundPresentationDirector` 只消费已确定的 resolved event list，不再调 resolver，不修改 `world_result`；
- 事件播放顺序只来自 B03–B08 与回执，不以动画节点完成顺序推断玩法；
- Full、Skip、退出重进和缺资产必须从同一 committed plan 得到同一语义结果；
- 每个 beat 有 `beat_started`、`beat_finished`、`asset_slots_used`、`fallback_slots_used` 和 `elapsed_ms` 回执；
- 对话只能由 `character_comms.json` 或等价数据源驱动，有一次性触发 ledger；
- 玩家输入在阻断对话期只负责翻页，不同时穿透到棋盘；
- 规划期的角色信息位于右侧指令面板，不在玩家点选地图时弹出大头像遮挡。

## 5. 资产壳

新 manifest 预登记 34 号全部槽位，但必须保持：

```text
approved_handoffs=[]
validated_handoff_count=0
loaded_slot_count=0
resource_probe_count=0
runtime_art_loaded=false
```

零 handoff 时每个槽使用同 native rect、pivot、safe area 和时长边界的具名几何 fallback。不读 A6/A7 输出目录，不读 G1/G1.5、story_first 或旧头像。

资产 resolver 必须先有单测夹具能验证正确、坏 hash、错 stable ID、路径逸出、错尺寸、错帧、错音频参数、错 build/profile 和单槽回退。这些夹具不是真实美术授权。

## 6. 可玩要求

1. 无帮助模式下先显示 3–4 秒局势揭示，然后进入规划；
2. 方向键／WASD 持续移动光标，鼠标点击路线，Q/E 转朝向，动作可鼠标和手柄操作；
3. 敌方冲线、车辆路线、小体目标、城市炮火条件与 T1–T5 在一屏内有明确对应；
4. 角色 UI 不只显示姓名：纪存给路线，兜灯给承力，七海显示远程撤令状态，旧守护者显示机体意志；
5. 作战确认可返回，长按执行有进度，长按完成后才锁计划；
6. 执行时指令面板收起，地图宽度扩展，相机按事件跟随而不丢失空间连续性；
7. 正常结果页只显示“冲线已偏开／撤离仍进行／红光正在聚集”等玩家事实，开发回执留在 F3。

## 7. 测试

至少覆盖：

- R0 resolver/profile 哈希和三个验收草案的结果冻结；
- 三个草案的 Full/Skip/fallback 逐字段语义等价；
- B03–B08 事件顺序、每个主体结算一次和视觉末态匹配；
- Full 播放首帧不是 resolver 最终世界快照，B03–B08 的中间视觉状态不反写 gameplay；
- 两个成功草案具有不同镜位／角色反应／视觉状态；
- 失败草案的摘要警告与执行失败原因一致；
- 对话 `trigger_once_key`、摘要返回、重置后的触发重置规则；
- 调试层默认隐藏，正常截图不包含 hash/receipt/Candidate 文字；
- 32×18 全域和关键锚点在 40×20 投影下与 A4/M2 坐标对齐，30×15 仅存在原 R0 对照场景；
- 1280×720 地图可交互点不被大型对话遮挡，文字不溢出；
- 零 handoff 时 0 探测；测试夹具不足以让任何真实美术被加载；
- 默认 M2、R0、A4/A5、Canon 和全量 Godot 回归。

## 8. 排他 allowlist

只允许新增：

- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_r05/**`
- `game-godot/scenes/candidate_runtime_demo/c01/e02/m3_r05/**`
- `game-godot/content/candidate_runtime_demo/c01/e02/m3_r05/**`
- `game-godot/tests/candidate_runtime_demo/m3_r05/**`
- `scripts/run_c01e02_m3_r05_presentation.sh`
- `scripts/test_c01e02_m3_r05.sh`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-m3-r05-shell/**`

只允许与上述新资源对应的 `.uid`。

禁止修改 R0 代码／profile／测试，当前 Runner、tactical session、A4/A5 binding/receipt/assets，`project.godot`、startup、Autoload、存档、Canon、Reader、33–37 制作人合同和任何美术输出目录。

## 9. 交付与停点

交付 `main-m3-r05-shell/**`：

- 实现笔记与架构回执；
- 零 handoff manifest/resolver 回执；
- `PLAN_EDIT`、`PLAN_SUMMARY`、Full 结果和 F3 调试层的 1280×720 捕获；
- 一段具名几何完整回合捕获；
- 测试、哈希和完成报告。

完成后停止。不读、不接、不复制 A6/A7 真实资产，不自行签 handoff，不进入 M1 或 R1。
