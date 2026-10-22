# 战斗演出运行时合同 v0.1（Candidate）

> 状态：`candidate_runtime_contract`
>
> 日期：2026-07-13
>
> 适用范围：Godot 战斗演出框架与 C01 馆守 Z 半跪掌部防卫垂直切片。
>
> 非 Canon 声明：本合同不修改 V35.8、V35.9、V35.10、剧情动作、首次登场、战斗数值或现有美术锁。所有演出只读取已经完成的战斗结算。

## 1. 运行时边界

战斗内核是唯一结算权威：

```text
BattleSession.confirm_attack()
  -> CombatResolver.resolve()
  -> BattleSession.last_resolution
  -> BattlePresentationDirector.select_sequence()
  -> BattlePresentationPlayer.play_sequence()
  -> 返回地图
```

- `BattlePresentationDirector` 只把 `last_resolution` 映射为演出序列，不计算命中、伤害、击破、EN、行动结束或回合推进。
- `BattlePresentationPlayer` 只播放序列。跳过、缺图、缺视频、载入失败都不得回调战斗结算。
- 现有 `PresentationQueue` 保留给剧情台词和地图剧情；战斗时间轴使用独立的 `steps` 数组。
- 每个演出序列保存一份深拷贝的 `source_resolution`，用于画伤害数字与击破反馈；播放器不得持有或修改 `BattleSession`。
- C01 首条映射只识别既有结算 `attacker_id=old_guardian`、`weapon_id=safety_line`。这是候选表现映射，不改变旧守护者/馆守 Z 的身份关系或战斗数据。

## 2. 稳定 ID

| 类型 | 稳定 ID | 用途 |
|---|---|---|
| `presentation_id` | `BP_C01_GZ_PALM_GUARD_V01` | C01 馆守 Z 半跪低热量掌部防卫/推挡 |
| `pose_id` | `POSE_GZ_C01_KNEEL_PALM_GUARD_V01` | 半跪、单掌前推的正比例全身 Pose |
| `sprite_state_id` | `SPR_GZ_C01_KNEEL_GUARD_V01` | 地图态半跪防卫状态 |
| `cutin_id` | `CUTIN_DOUDENG_C01_SAFETY_LOCK_V01` | 兜灯/控制界面安全锁 Cut-in |
| `video_id` | `VID_GZ_C01_PALM_GUARD_V01` | 1–3 秒无声机械动作短片 |
| `target_placeholder_id` | `SPR_ENEMY_SEAL_DRONE_PLACEHOLDER_V01` | 封印无人机占位目标 |

ID 一经进入 `approved_for_runtime` 不改名。画面修订通过文件版本后缀和清单版本推进，不复用旧 ID 表示不同动作。

## 3. 文件命名和路径

运行时目标路径（由美术 Session 交付；当前允许不存在）：

```text
res://assets/battle_presentation/c01/guardian_z/
  pose_gz_c01_kneel_palm_guard_v01.png
  sprite_gz_c01_kneel_guard_v01.png
  cutin_doudeng_c01_safety_lock_v01.png
  vid_gz_c01_palm_guard_v01.ogv
  vid_gz_c01_palm_guard_v01.mp4
  manifest.json
```

- 小写 ASCII、下划线分词、版本后缀固定为 `_vNN`。
- MP4 是母版，OGV 是 Godot 运行时资源；不得只交 MP4。
- `manifest.json` 记录稳定 ID、像素尺寸、轴点、Alpha、状态和源文件哈希。
- 未经 `approved_for_runtime` 的文件即使存在，正式构建也视为不可用；开发构建可显式预览 `review_ready`。

最小 manifest 结构：

```json
{
  "schema_version": "1.0",
  "assets": [
    {
      "asset_id": "POSE_GZ_C01_KNEEL_PALM_GUARD_V01",
      "path": "res://assets/battle_presentation/c01/guardian_z/pose_gz_c01_kneel_palm_guard_v01.png",
      "status": "approved_for_runtime",
      "width": 2048,
      "height": 2048,
      "pivot": [1024, 1856],
      "alpha": "straight",
      "sha256": "..."
    }
  ]
}
```

运行时按 `asset_id` 读取 `status`，不会因为目标路径碰巧存在就自动批准。低帧率、环境策略禁用、manifest 未批准或载入失败都会走程序回退。

## 4. 静态资产规格

### 4.1 馆守 Z 正比例 Pose

- 文件：`pose_gz_c01_kneel_palm_guard_v01.png`
- 尺寸：`2048 x 2048 px`，透明 PNG。
- Alpha：普通/直通 Alpha（straight alpha），sRGB；禁止预乘 Alpha。
- 透明安全区：四边至少 `128 px`；掌部光效方向额外保留画面右侧 `320 px` 透明区。
- 轴点：`(1024, 1856)`，定义为半跪状态与地面主要接触面的中心，不是画布中心。
- 构图：馆守 Z 必须保持半跪；躯干最多局部抬起；一只手掌作为防卫面，另一臂不出现双拳同时发光。
- 禁止：完整站立、全功率出击、无损英雄 Pose、双拳发光、烘焙伤害数字/对白/光束/爆炸。

### 4.2 地图态 Sprite State

- 文件：`sprite_gz_c01_kneel_guard_v01.png`
- 尺寸：`512 x 512 px`，透明 PNG，单状态图；后续帧动画另立 sheet 合同。
- Alpha：普通/直通 Alpha（straight alpha），sRGB。
- 透明安全区：四边至少 `32 px`。
- 轴点：`(256, 432)`，对应 2x2 地图单位占格底面中心。
- 轮廓：在 25% 缩放下仍能读出“半跪、巨掌前挡、胸牌低亮”。

### 4.3 兜灯/控制界面 Cut-in

- 文件：`cutin_doudeng_c01_safety_lock_v01.png`
- 尺寸：`1920 x 640 px`，透明 PNG。
- Alpha：普通/直通 Alpha（straight alpha），sRGB。
- 画面安全区：左右各 `160 px`、上下各 `64 px` 不放眼睛、手、关键文字或仪表读数。
- 轴点：`(960, 320)`；运行时以屏幕中心对齐。
- 内容：兜灯或安全锁控制界面二选一；不得加入未在 Canon 中出现的新驾驶舱、完整启动口号或剧情字幕。

### 4.4 封印无人机占位目标

- 文件：由运行时程序图形提供默认占位，不要求美术 Session 首轮交付。
- 如交付静态图：`512 x 512 px`，轴点 `(256, 416)`，普通 Alpha，四边至少 `32 px`。

## 5. 视频规格

- `video_id`：`VID_GZ_C01_PALM_GUARD_V01`
- 母版：`1920 x 1080`、H.264 MP4、24 或 30 fps、无声、时长 `1.0–3.0 s`。
- 运行时：同尺寸 OGV/Theora、无声、固定帧率；Godot 内置视频能力是 v0.1 唯一运行时路线。
- 首帧：必须能从静态半跪 Pose 自然切入，馆守 Z 仍处于半跪低热状态。
- 尾帧：手掌停在可由 Godot 叠加掌部光效和冲击波的位置；不得在视频里完成伤害数字、对白、整段光束或爆炸。
- 安全区：中心 `1600 x 900 px` 放关键动作；四边允许运行时裁切。
- 音频：不嵌入。音效、语音、BGM 由 Godot 分轨播放。
- 回退：文件不存在、载入失败、设备不支持或性能策略禁用时，保持静态 Pose，并由 Godot 绘制掌部光、冲击线、冻结帧与震屏。

## 6. 通用演出步骤协议

每个步骤至少含：

```gdscript
{
  "type": "mecha_pose",
  "duration": 0.8,
  "asset_id": "POSE_GZ_C01_KNEEL_PALM_GUARD_V01",
  "asset_path": "res://...png",
  "optional": true,
  "payload": {}
}
```

播放器必须识别：

| `type` | 运行时职责 | 缺资源时 |
|---|---|---|
| `map_anim` | 地图单位接近、起势、目标标记 | 程序图形占位 |
| `camera` | 推近、平移、构图切换 | 保持当前构图 |
| `pilot_cutin` | 角色/控制界面 Cut-in | 程序色块与名字牌 |
| `mecha_pose` | 正比例机体 Pose | 程序绘制半跪轮廓 |
| `video` | 无声短片 | 静态 Pose + Godot FX |
| `fx` | 掌光、冲击线、爆闪、碎片 | 程序粒子/Canvas 绘制 |
| `audio` | SFX/Voice/BGM cue | 静默继续 |
| `freeze` | 命中冻结 | 保持最后画面 |
| `shake` | 屏幕震动 | 可降级为轻微偏移或关闭 |
| `damage_popup` | 使用 `source_resolution` 显示伤害/击破 | 始终可用字体绘制 |
| `return_to_map` | 清理覆盖层并解锁输入 | 强制清理全部临时状态 |

未知步骤类型必须安全跳过并记录诊断，不得卡住时间轴。

## 7. 播放模式

### `full`

目标总时长约 `6–8 s`：地图接近/镜头 → 兜灯或控制界面 Cut-in → 半跪全比例 Pose → 可选短视频 → Godot 掌部光效/冲击 → 冻结/震屏 → 伤害与击破 → 返回地图。

### `short`

目标不超过约 `2.5 s`：地图动作 → 关键 Pose → Godot FX → 冻结/震屏 → 伤害反馈 → 返回地图。使用同一 `source_resolution`。

### `off`

不创建可见演出，立即完成并返回地图。使用同一结算结果，不补算、不重放。

### 安全跳过

- 任意可见阶段按确认、取消或点击可跳到 `return_to_map`。
- 跳过只清理演出节点、音视频和输入锁；不得调用 `confirm_attack()`、`end_player_phase()` 或改写单位字典。
- 多次跳过调用必须幂等。

## 8. 资产状态规则

`manifest.json` 的 `approved_for_runtime` 采用以下状态：

| 状态 | 含义 | 正式运行时 |
|---|---|---|
| `placeholder` | 程序占位或临时图 | 使用回退 |
| `draft` | 未完成构图 | 不载入 |
| `review_ready` | 可供视觉审查 | 开发预览可载入 |
| `approved_for_runtime` | 尺寸、轴点、构图、Canon 锁和技术检查均通过 | 可载入 |
| `rejected` | 不得继续使用 | 不载入 |

批准必须同时满足：稳定 ID 匹配、像素规格匹配、轴点可复现、禁止项检查通过、PNG 边缘无黑边、OGV 可解码、首尾帧匹配、20 次播放无残留。

## 9. 美术 Session 首轮交付清单

1. `POSE_GZ_C01_KNEEL_PALM_GUARD_V01`：2048 方图透明 PNG。
2. `SPR_GZ_C01_KNEEL_GUARD_V01`：512 方图透明 PNG。
3. `CUTIN_DOUDENG_C01_SAFETY_LOCK_V01`：1920x640 透明 PNG。
4. `VID_GZ_C01_PALM_GUARD_V01`：1–3 秒无声 MP4 母版；确认构图后转 OGV。
5. `manifest.json`：逐文件填写尺寸、轴点、Alpha、状态、哈希、审查备注。

Godot 负责掌部光、冲击波、命中闪白、震屏、伤害数字、击破文字、对白框、SFX/Voice/BGM。美术不得把这些元素永久烘焙进 Pose 或视频。

## 10. 验收证据

- 视频路径为空或文件不存在，`full` 仍从地图动作播放到伤害反馈并返回地图。
- `full`、`short`、`off` 与中途跳过前后，目标 HP、攻击者行动状态和回合数不发生第二次变化。
- 同一播放器连续运行至少 20 次，子节点数不增长，无输入锁、旧画面、旧音频或旧视频残留。
- `full` 含全部必要阶段，`short <= 2.5 s`，`off` 无可见延迟。
- 全部 Godot smoke test、严格 Canon check 和 Canon smoke test 通过。
