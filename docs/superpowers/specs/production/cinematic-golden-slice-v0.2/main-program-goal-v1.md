# 主程序 Session 目标：C01 2.5D 低热救援验证

> 当前状态：本目标的技术基线已完成并通过候选验收。后续“电影化斜侧视 + X/Y 浅纵深 + 分区相机”试验改读 `main-program-perspective-trial-goal-v1.md`；不得用后续返修覆盖本目标的可回退基线。

## Objective

在不覆盖现有 C01 可玩切片和双段黄金样片的前提下，实现独立场景 `SCN_C01_RM_RESCUE_2P5D_V01`，完成 8–12 分钟的“2.5D 巡检 → 白框事故 → 三步战术 → 馆守 Z 低热演出 → 七海审计”闭环。

开工前必须完整读取：

- `producer-brief-and-shotbook-v1.md`
- `2026-07-13-chao-gag-multi-play-runtime-architecture-v1.md`
- `battle-presentation-v0.1/runtime-contract.md`
- `battle-presentation-v0.1/art-status.md`
- 美术 Session 最新 manifest/状态页

## Must deliver

1. 独立 `ModeScene`，不得继续扩张旧 `c01_playable_slice_scene.gd` 的单体 `_draw`；旧场景最多增加一个开发入口。
2. 真正 X/Y 可移动的浅纵深房间：`CharacterBody2D`、walkable polygon、碰撞、Y-sort、前景遮挡、摄影机区域 rail、热点距离判断。
3. 三种对白 Profile：`scene_caption`、`halfbody_focus`、`cinematic_cutin`。普通对白不得默认弹大头像框。
4. 同房间三步战术层：R1标准救援失败、R2跌跌主动摔倒占格、R3机器犬诱导＋安全审查＋低热胸灯。
5. 兜灯安全拒绝：照射扇区内仍有人或小机时不能放行，提示具体原因；这不是“按钮灰掉但不解释”。
6. 馆守 Z 演出复用当前批准的正比例半跪 Pose，但必须只亮低热胸灯，不站起、不攻击、不改变正式战斗状态。
7. 七海审计必须表现为四个可见操作：时间线比对、恢复延迟记录、关闭自动结案/删档、实名锁定镜像。
8. 完整播放和任意跳过落到同一 preview outcome；重复进入不得重复提交事务。
9. 提供自动截图：探索全景、白框误分类、失败占格、馆守 Z 胸灯、回充余韵、七海审计六张。
10. 提供 smoke tests、Canon strict、全项目回归结果和试玩说明。

## Architecture constraints

- 复用/演进 `CinematicDirector`，但把对白 Beat、空间活动和三步战术结果拆成数据，不把剧情逐句硬编码在场景脚本。
- 表现层不拥有正式剧情、战斗或 Canon 结算，只发出 `preview outcome`。
- 不引入新插件、付费 SDK、网络服务或商业运行时依赖。
- 不把三步战术层直接推广为全游戏新战斗内核；本轮只测“同房间轻战术”是否好懂、好玩、好看。
- 正式视觉验收不得使用旧 `portrait_jicun.png`、`portrait_doudeng.png`、`portrait_qihai.png`。新资产未到时用明确几何占位，不得把旧图截图冒充完成。
- 主程序不得修改美术 `art-status.md` 的批准结论，只读取 manifest。

## Suggested implementation order

1. 建 `c01_real_machine_rescue_validation.tscn` 和独立生命周期。
2. 几何占位完成 2.5D 移动、遮挡、镜头区和六个热点。
3. 接入剧情 Beat 与三种对白 Profile。
4. 完成 R1/R2/R3 数据和可撤回预览。
5. 接入馆守 Z 低热序列与七海审计。
6. 等美术 manifest 后按 Stable ID 换图，不按文件名猜资产。
7. 做截图、性能、跳过、重复进入与回归验证。

## Acceptance

- 玩家在 20 秒内能证明不是单线横移：至少完成一次前后绕行和前景遮挡。
- 四个探索条件必须通过实际走动/调查得到，不由开场自动赠送。
- R1 失败原因可读为“标准动作被预测”，不能像数值不足或脚本强制失败。
- R2 必须由玩家确认跌跌摔倒位置；R3 必须由玩家完成诱导、安全检查和照射确认。
- 普通对白中至少 70% 不使用头像框；大特写只用于承担、拒绝、审计和机战高潮。
- 馆守 Z 胸灯段保持半跪、低热、一次输出、命中后硬停机。
- 退出/跳过/重播无脏状态；预览事务幂等。
- 1280×720 目标设备稳态 60 FPS；首次大图尖峰需记录。
- `godot-test.sh`、新增 smoke、`canon-check-godot.sh --strict`、`canon-smoke-test.sh` 全部通过。

## Stop and ask

- 需要改变剧情动作或对白结论。
- 需要把浅纵深改成纯横版、俯视或八方向大地图。
- 需要新增正式战斗内核或替换现有 SRPG。
- 美术 Stable ID、轴点、方向数或画面视角与共享合同冲突。
- 需要使用旧头像作为最终资产，或需要绕过美术批准状态。
- 发现当前镜头本在可玩性上根本不成立，需要改变 R1/R2/R3 因果。

## Completion report

完成时必须给出：运行入口、实现文件、数据文件、六张截图、全量测试结果、实测时长、已知占位、与美术 manifest 的差异、是否建议升级为正式模板。不要自行宣布升级。
