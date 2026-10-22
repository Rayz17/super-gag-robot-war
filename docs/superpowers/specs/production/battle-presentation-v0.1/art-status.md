# 馆守 Z C01 半跪防卫美术交付状态

> Status Authority: `art_session_current`
>
> 更新日期：2026-07-13
>
> 文件边界：本页只维护美术交付状态，不修改 `runtime-contract.md`、`main-status.md`、Godot 代码、V35.8、V35.9 或剧情动作。

## 当前结论

用户已确认馆守 Z 当前方案，并选择封存无人机 **B 悬浮档案盒型**。馆守 Z 地图三态、全比例三 Pose、独立阴影和兜灯四张 Cut-in 已进入 `approved_for_runtime`；B 方案已形成一张透明锁图母体和 `idle / scan / lock / hit / disabled` 五个同母体状态，另有独立阴影。

manifest 现记录 23 项，其中 17 项允许运行时导入。馆守 Z 两张 16:9 母帧只升为 `approved_as_video_reference`：它们可以用于未来短视频试制，但仍不等于视频文件完成。

## 馆守 Z 交付

| Stable ID | 规格 | 状态 |
|---|---|---|
| `SPR_GZ_C01_KNEEL_IDLE_V01` | 512x512，轴点 `(256,432)` | `approved_for_runtime` |
| `SPR_GZ_C01_KNEEL_GUARD_V01` | 512x512，轴点 `(256,432)` | `approved_for_runtime` |
| `SPR_GZ_C01_KNEEL_RECOIL_V01` | 512x512，轴点 `(256,432)` | `approved_for_runtime` |
| `SHADOW_GZ_C01_KNEEL_V01` | 512x512，独立阴影 | `approved_for_runtime` |
| `POSE_GZ_C01_KNEEL_START_V01` | 2048x2048，轴点 `(1024,1856)` | `approved_for_runtime` |
| `POSE_GZ_C01_KNEEL_PALM_GUARD_V01` | 2048x2048，锁图源派生 | `approved_for_runtime` |
| `POSE_GZ_C01_KNEEL_CONTACT_V01` | 2048x2048，轴点 `(1024,1856)` | `approved_for_runtime` |

地图播放顺序为 `idle -> guard -> recoil -> idle`。回位复用同一 idle 文件，不另造近似帧；C01 仍只表现半跪、低热量单掌推挡和受力，不出现完整站立、双拳发光或全功率动作。

## 兜灯 Cut-in

| Stable ID | 用途 | 状态 |
|---|---|---|
| `CUTIN_DOUDENG_C01_COMMAND_V01` | 命令 | `approved_for_runtime` |
| `CUTIN_DOUDENG_C01_OBSERVE_V01` | 观察 | `approved_for_runtime` |
| `CUTIN_DOUDENG_C01_TENSE_V01` | 紧张 | `approved_for_runtime` |
| `CUTIN_DOUDENG_C01_SAFETY_LOCK_V01` | 强制停止/安全提醒 | `approved_for_runtime` |

四张图从既有 `core_doudeng_expressions.png` 拆分，没有重绘兜灯，也不把四宫格整张交给运行时。对白、速度线和伤害数字继续由 Godot 叠加。

## 封存无人机 B

锁图母体：[`design_seal_drone_b_master_v01.png`](./art-delivery/approved/design_seal_drone_b_master_v01.png)

视觉锁为扁平微白档案盒壳体、深海军蓝中脊、黄铜关节、四个对称折叠夹臂、前置水平封条投影槽和三段编号状态灯。它的敌意来自扫描、封存框和流程灯，不使用怪物脸、独眼头、枪炮、刀刃或红色黑客网格。

| Stable ID | 识别动作 | 状态 |
|---|---|---|
| `SPR_SEAL_DRONE_C01_IDLE_V01` | 低噪悬停、夹臂收束 | `approved_for_runtime` |
| `SPR_SEAL_DRONE_C01_SCAN_V01` | 柔和梯形扫描区 | `approved_for_runtime` |
| `SPR_SEAL_DRONE_C01_LOCK_V01` | 四角封存框和投影线 | `approved_for_runtime` |
| `SPR_SEAL_DRONE_C01_HIT_V01` | 同轴短促倾斜和受力线 | `approved_for_runtime` |
| `SPR_SEAL_DRONE_C01_DISABLED_V01` | 降亮、失衡、投影槽熄灭 | `approved_for_runtime` |
| `SHADOW_SEAL_DRONE_C01_V01` | 512x512 独立悬浮阴影 | `approved_for_runtime` |

五态均由同一张透明母体确定性派生，机壳、夹臂数量、透视和比例不会在状态切换时漂移。A 轨道吊挂型和 C 环框巡检型保留为 `not_selected` 历史方案，禁止运行时导入。

## 视频母帧

`VID_GZ_C01_PALM_GUARD_START_FRAME_V01` 与 `VID_GZ_C01_PALM_GUARD_END_FRAME_V01` 已批准为构图参考，仍保持 `runtime_allowed=false`。视频平台、模型和商业使用条件未确认，因此本轮没有生成 MP4、OGV，也没有开始批量视频。

## 合同反馈

1. `runtime-contract.md` 仍只列馆守 Z 单个占位状态。美术侧已在 manifest 给出三地图态、三 Pose、动画顺序和稳定 ID，主程序 Session 需要扩展映射。
2. 合同使用“封印无人机”，Canon 和本交付统一使用“封存无人机” (`ENEMY_SEAL_DRONE`)。可以保留旧占位 ID 作为兼容别名，但界面显示和正式文件名应使用“封存”。
3. 无人机正式稳定 ID 为 `SPR_SEAL_DRONE_C01_*_V01`，旧 `SPR_ENEMY_SEAL_DRONE_PLACEHOLDER_V01` 只应作迁移别名。
4. 美术侧不修改合同与 Godot 代码；导入时以 manifest 的 `runtime_path` 为准。

## 禁止使用

- 不导入 `art-delivery/sources/`、`art-delivery/staging/` 或 `CAND_*` 项。
- 不把 `DESIGN_SEAL_DRONE_B_MASTER_V01` 当地图单位；它只作锁图参考。
- 不把两张视频母帧记作视频已完成。
- 不把现有站立 Q 版 `guardian_z_sprite_chibi.png` 当半跪动画帧。
- 不把兜灯四宫格整张交给运行时。
- 不为 C01 临时补全站立、全功率或常规武器化表现。

## 主程序可导入清单

只导入 `art-delivery-manifest.json` 中同时满足 `approval_status=approved_for_runtime` 与 `runtime_allowed=true` 的 17 项。它们位于 `art-delivery/approved/`，包含馆守 Z 7 项、兜灯 4 项、封存无人机 6 项。尺寸、轴点、安全区、Alpha 和 SHA-256 均以 manifest 为准。

## 验证

```text
build_art_delivery.py                  PASS
finalize_art_delivery_manifest.py      PASS
validate_art_delivery.py               PASS (23 assets, 0 warnings, 0 errors)
PNG dimensions / alpha corners         PASS
Safe-area visible bounds               PASS
Visible chroma-fringe heuristic        PASS
Manifest path / size / SHA-256          PASS
25% map readability review              PASS
Checkerboard alpha edge review          PASS
scripts/canon-smoke-test.sh             PASS
scripts/canon-check-godot.sh --report   PASS (no runtime violations)
```

总览：[`guardian_z_c01_art_delivery_contact_sheet_v02.jpg`](./art-delivery/review/guardian_z_c01_art_delivery_contact_sheet_v02.jpg)

无人机五态：[`seal_drone_b_state_contact_sheet_v01.png`](./art-delivery/review/seal_drone_b_state_contact_sheet_v01.png)

缩放检查：[`map_scale_readability_check_v02.png`](./art-delivery/review/map_scale_readability_check_v02.png)

透明边缘检查：[`alpha_edge_check_v02.png`](./art-delivery/review/alpha_edge_check_v02.png)
