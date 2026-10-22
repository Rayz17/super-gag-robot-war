# 馆守 Z 战斗演出联合总装合同差异报告

> 日期：2026-07-13  
> 审计对象：`runtime-contract.md`、`main-status.md`、`art-status.md`、`art-delivery-manifest.json` 与当前 Godot 播放器。  
> 处理原则：本报告落盘前不导入任何美术文件；后续只处理 `approval_status=approved_for_runtime` 且 `runtime_allowed=true` 的资产。

## 结论

核心构图资产的稳定 ID、尺寸和轴点一致，可以联合总装；清单字段协议、扩展动作集合、无人机命名和视频完成状态不一致，不能把原美术 manifest 原样交给当前播放器。

解决方式限定为“机械适配”：从美术 manifest 逐项验证源文件、SHA-256、尺寸、轴点和批准状态，再生成仅含批准资产的 Godot 运行时 manifest。不得为缺失视频、旧占位无人机 ID 或未列明动作猜测文件。

## 一致项

| 资产 | Runtime 合同 | 美术 manifest | 结果 |
|---|---|---|---|
| 掌部防卫 Pose | `POSE_GZ_C01_KNEEL_PALM_GUARD_V01`；2048x2048；轴点 `(1024,1856)` | 完全一致；`approved_for_runtime` | 可导入 |
| 半跪防卫地图态 | `SPR_GZ_C01_KNEEL_GUARD_V01`；512x512；轴点 `(256,432)` | 完全一致；`approved_for_runtime` | 可导入 |
| 兜灯安全锁 Cut-in | `CUTIN_DOUDENG_C01_SAFETY_LOCK_V01`；1920x640；轴点 `(960,320)` | 完全一致；`approved_for_runtime` | 可导入 |
| 演出主 ID | `BP_C01_GZ_PALM_GUARD_V01` | 美术资产均指向同一 C01 半跪防卫交付，但根节点未填写 `presentation_id` | 资产可用；根元数据需由运行时集成清单显式补齐 |
| 半跪限制 | 半跪、低热量、单掌；禁止站立/全功率/双拳发光 | `art-status.md` 与交付备注一致 | 通过 |

## 差异项

| 编号 | 严重度 | 差异 | 证据 | 联合总装处理 |
|---|---|---|---|---|
| D01 | blocker | 播放器按 `asset_id/status` 查询；美术清单提供 `stable_id/approval_status/runtime_allowed` | `battle_presentation_player.gd::_manifest_asset_status()` 与 schema 1.2 manifest | 生成运行时适配 manifest，同时保留 `stable_id` 与规范化 `asset_id/status`；播放器也兼容读取两种字段，但必须同时检查 `runtime_allowed` |
| D02 | major | Runtime 合同示例 schema 为 1.0；美术 manifest 为 1.2，且 `manifest_version`、根 `presentation_id` 为空 | `runtime-contract.md` 第3节；美术 manifest 根节点 | 运行时 manifest 写入 `schema_version=1.2-runtime-adapter`、`source_schema_version=1.2`、`contract_version=0.1`、`presentation_id=BP_C01_GZ_PALM_GUARD_V01` |
| D03 | major | Runtime 合同只列一张地图态、一张 Pose；美术交付为三地图态、三 Pose 和三条动画序列 | `art-status.md` 合同反馈1；manifest `animation_sequences` | 仅按 manifest 已批准序列扩展 Director；不自行发明帧或时长 |
| D04 | major | Runtime 使用旧占位 ID `SPR_ENEMY_SEAL_DRONE_PLACEHOLDER_V01`；美术正式 ID 为 `SPR_SEAL_DRONE_C01_*_V01` | `runtime-contract.md` 第2/4.4节；`art-status.md` 合同反馈2-3 | 正式显示与资源只使用 `SPR_SEAL_DRONE_C01_*_V01`；旧 ID 只保留为无资源回退别名，不映射为某个具体状态 |
| D05 | major | 文案中“封印无人机”与 Canon/美术“封存无人机”不一致 | `art-status.md` 合同反馈2；Canon `ENEMY_SEAL_DRONE` | UI 与新代码统一显示“封存无人机”；不改历史文档中的兼容说明 |
| D06 | major | Runtime 引用 `VID_GZ_C01_PALM_GUARD_V01` OGV；美术清单没有该视频，只批准两张 `approved_as_video_reference` 母帧且 `runtime_allowed=false` | manifest `video_gate` 与两张母帧 | 不导入母帧为视频，不伪造 OGV；正式验证以视频缺失回退为当前真实状态；存在/加载失败场景使用测试夹具验证 |
| D07 | major | `main-status.md` 仍写“art-status 未发现”和全部资产欠缺 | 当前主状态页 vs 当前美术交付 | 联合总装完成后更新主状态页，保留视频仍欠缺的事实 |
| D08 | minor | 美术清单包含独立阴影、兜灯四表情、无人机五态；Runtime 合同未逐项列出 | manifest 17项运行时批准资产 | 资产可按 exact ID 导入；只有被 Director/场景显式引用的项才加载，其余作为同版本批准储备 |

## 不得自动处理的项目

- 两张 `approved_as_video_reference` 母帧不得改写为 `approved_for_runtime`。
- `CAND_*`、`DESIGN_SEAL_DRONE_B_MASTER_V01`、`sources/`、`staging/` 不得导入。
- 不把旧占位无人机 ID 静默别名到 `idle/scan/lock/hit/disabled` 中任一状态。
- 不新增馆守 Z 站立、全功率、双拳发光或右臂无损复原动作。
- 不把本次运行时适配视为 V35.10 解冻、正式 Episode 完成或全项目演出标准升级。

## 执行门槛

只有以下检查全部通过后才允许复制资产到 `game-godot/assets/battle_presentation/`：

1. 批准状态与 `runtime_allowed` 双重通过。
2. `delivery_path` 存在且位于 `art-delivery/approved/`。
3. 文件 SHA-256、PNG 宽高与 manifest 一致。
4. `runtime_path` 位于 `res://assets/battle_presentation/c01/`，没有路径穿越。
5. 核心三项稳定 ID、尺寸、轴点继续与 runtime contract 一致。
6. 动画序列只引用同一 manifest 内 `approved_for_runtime` 资产。

