# C01E02 M3-R0.5｜主程序与美术联合接口合同

> 状态：`active shared interface / presentation only`
>
> 上游：`33-c01e02-m3-r0-5-presentation-validation-producer-contract.md`
>
> 目标画幅：`1280×720 / 16:9 / Godot 4.7`

## 0. 投影与拓扑锁

```text
visual_layout_profile_id=c01cdv1_e02_m3_r05_layout_40x20_v1
logical_grid=32x18
visual_projection=isometric_tile_half_40x20
topology_sha256=baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8
```

R0.5 使用独立显示投影配置，不读 R0 `sandbox_profile.json` 的 30×15 画面缩放作为美术对齐基准。同一 resolver 格位通过纯显示 `PresentationGridTransform` 投影到 40×20；寻路、footprint、接触和回执仍使用原整数格。地图缩放只通过相机完成，不对 A4 贴图和单位 pivot 分别施加不同缩放。

## 1. 界面状态与空间合同

### 1.1 玩家状态

```text
SITUATION_REVEAL
→ PLAN_EDIT
→ PLAN_SUMMARY
→ HOLD_TO_COMMIT
→ RESOLUTION_PLAYBACK
→ AFTERMATH
```

这是表现层状态，不取代 R0 的玩法 lifecycle。`PLAN_SUMMARY` 与执行继续调用同一 `SharedRoundResolver`。

### 1.2 1280×720 布局

| 状态 | 区域 | 坐标 | 规则 |
| --- | --- | --- | --- |
| 所有状态 | 顶部任务条 | `x0 y0 w1280 h48` | 只显示深层目标、当前阶段和最大 3 个危险图标 |
| `PLAN_EDIT` | 战术地图 | `x0 y48 w900 h552` | 全部可交互格、路线、朝向和意图箭头必须在此区内可见 |
| `PLAN_EDIT` | 指令面板 | `x900 y48 w380 h552` | 角色头像、机体、主动作／预备／备用／风险；不在地图上叠大面板 |
| `PLAN_EDIT` | 共同时间线 | `x0 y600 w1280 h120` | T1–T5 给出主体、目标和预计接触，不显示 stable ID |
| 大型通讯 | 对话带 | `x0 y548 w1280 h172` | 出现时暂停规划输入；不允许在玩家仍需点地图时遮挡地图 |
| `RESOLUTION_PLAYBACK` | 演出地图 | `x0 y48 w1280 h672` | 指令面板收起，镜头与对象动画使用完整宽度 |
| `RESOLUTION_PLAYBACK` | 角色短通讯 | 左下／右下各 `w360 h132` | 只在对应节拍出现；说话者高亮，对方降暗，不同时堆叠三人 |
| 调试 | Debug overlay | `F3` 切换 | hash、receipt、build、slot/fallback 只能出现在此层 |

任何动画、头像、提示或文字不得改变布局容器尺寸。地图、按钮、时间线和角色占位使用稳定约束，不因文字长度、表情或资产缺失抖动。

## 2. 玩家语言与调试语言分离

| 调试／内部语言 | 玩家界面 |
| --- | --- |
| `PUBLIC_SITUATION` | `敌方行动已确认` |
| `main_action=BODY_REDIRECT` | `迎击改线` |
| `prepared_reaction` | `预备：截住漏网小体` |
| `fallback` | `路线受阻时：守住东口` |
| `COMMIT_SUMMARY` | `作战确认` |
| `RoundReceipt` | `本轮结果` |
| `success=true` | 由事件结果表达，不显示布尔值 |
| `M3_R0_PROTOTYPE_STOP` | `BREAKER 开始聚集红光` |

正常界面禁止显示 `hash`、`stable_id`、`Candidate`、`prototype_stop`、`mission_clear=false` 或任何开发回执字段。

## 3. 共同结算演出时间线

| Beat ID | 目标时长 | 回执事件 | 画面 | 角色／声音 | 不可改的语义 |
| --- | ---: | --- | --- | --- | --- |
| `R05-B00` | 3–4s | 公开意图 | 镜头依次指向应急车、小体、BREAKER 冲线 | 纪存：“人都在后面。把它引到南边去。” | 敌人与车辆计划已冻结 |
| `R05-B01` | 交互 | 草案编辑 | 路线、朝向、冲线、车辆线和保护区一屏可读 | 兜灯首次进入指令面板时显示 Reader 原句：“它管身体，你管路。别抢方向，也别让它一脚踩进楼里。” | 台词只触发一次，不自动填草案 |
| `R05-B02` | 交互 | 作战确认 | 五个事件卡与未覆盖风险；可返回 | 纪存／兜灯仅对当前草案的路线或承力给一条反应 | 摘要与执行同 resolver |
| `R05-B03` | 2.5–3.5s | T1 车辆 | 车辆从馆守 Z 落脚区前通过，相机短跟随 | 警报、轮胎／履带、近距离通过声 | 车辆不可控，且先于馆守 Z |
| `R05-B04` | 2.5–3.5s | T2 小体 | 小体扑向保护线；主动作与预备方案使用不同动作和镜位 | 纪存或旧守护者的无文字确认反应 | 小体侧推／改线，不被消灭，仍 `scattered` |
| `R05-B05` | 4–6s | T3/T3.25 巨体接触 | 馆守 Z 与 BREAKER 移动、碰撞、命中停顿、被推移，路面翻起 | 重低频碰撞、机械承力；兜灯显示当前承力反应 | 同前态接触组；不按实体顺序抢占 |
| `R05-B06` | 2–3s | T4 城市炮击 | 侧甲暴露后炮击落点、白闪、黑色碎片 | 先远处炮口声，后命中声 | 只在冲角偏开时命中；七海不指挥炮火 |
| `R05-B07` | 3–4s | T5 路面／红光 | 动态降低环境亮度，BREAKER 红缝聚光，旧守护者的视线越过巨机望向墙挂盾 | 环境音压低，红光蓄能 sting；旧守护者不说主题金句 | 只是表现视线；不生成取盾动作／路线，不释放冲击，盾状态仍为 `wall_hung_3_scorches` |
| `R05-B08` | 2–3s | 余韵 | 玩家可读的三条结果，然后“重玩另一解／退出” | 不播胜利音，不显示 Mission Clear | 不写 P1 或存档 |

`Skip` 只跳过 B03–B08 的可见表现，不跳过提交、不改变 resolver 输入、不触发额外行动。

## 4. 角色通讯数据合同

每条通讯至少包含：

```text
beat_id
speaker_stable_id
speaker_display_name
channel = local / cockpit / machine_voice / remote
portrait_slot
expression_state
screen_side
line_text
source_kind = accepted_reader_exact / approved_short_line / nonverbal
source_ref
trigger_once_key
blocking
minimum_display_seconds
skippable
```

规则：

- 主程序不根据状态拼接“临时台词”；
- 通讯有 `trigger_once_key`，返回摘要、重选动作和移动光标不得重复播放同一句；
- 只有说话者使用高亮表情，对方保持降暗或不出现；
- 七海必须有远程频道边框，不得像现场队友；
- 旧守护者使用馆守 Z 头部／胸前扬声器／导览席波形的组合身份，不使用人脸。

## 5. 资产槽位

### 5.1 可在 P1 重绑的已批准源

| Slot | Stable ID | 来源状态 |
| --- | --- | --- |
| `R05_MAP_BASE` | `MAP_C01CDV1_SCROLLING_STREET_R2_BASE` | A4 已批准，需新 build/fingerprint exact rebind |
| `R05_MAP_BUILDINGS` | `MAP_C01CDV1_SCROLLING_STREET_R2_BUILDINGS` | 同上 |
| `R05_MAP_ROOFS` | `MAP_C01CDV1_SCROLLING_STREET_R2_ROOFS` | 同上 |
| `R05_MAP_FOREGROUND` | `MAP_C01CDV1_SCROLLING_STREET_R2_FOREGROUND` | 同上 |
| `R05_MAP_OCCLUSION_MASK` | `MAP_C01CDV1_SCROLLING_STREET_R2_OCCLUSION_MASK` | 同上 |
| `R05_RIFT_SWARM_IDLE_4DIR` | `ENEMY_C01_RIFT_SWARM` | A5 已批准，需新 build/fingerprint exact rebind |
| `R05_CUTIN_DOUDENG_OBSERVE` | `CUTIN_DOUDENG_C01_OBSERVE_V01` | 既有 `approved_for_runtime`，1920×640，需精确跨车道重绑 |
| `R05_CUTIN_DOUDENG_TENSE` | `CUTIN_DOUDENG_C01_TENSE_V01` | 既有 `approved_for_runtime`，1920×640，需精确跨车道重绑 |

### 5.2 A6 新角色槽与兜灯使用规则

| Slot | Expected Stable ID | 最低状态 |
| --- | --- | --- |
| `R05_PORTRAIT_JICUN` | `CH_JICUN` | `focused / alarm / resolve` |
| `R05_PORTRAIT_QIHAI_REMOTE` | `CH_QIHAI` | `controlled / decision / concerned` |
| `R05_COMMS_OLD_GUARDIAN` | `CH002` | `guide / contact / shield_gaze` |

兜灯在 R0.5 使用 5.1 的 `OBSERVE/TENSE` 两张既有批准件：`OBSERVE` 对应规划／机况读取，`TENSE` 对应承力警告／碰撞。A6 可以把原件放进 720p 模拟图验证构图，但不得输出新的 `R05_PORTRAIT_DOUDENG` 运行母版。若两张既有件无法满足布局，必须在 U1 明确提出“新作兜灯”选项，不得静默裁切或变形。

### 5.3 A7 新演出槽

| Slot | Expected Stable ID | 用途 |
| --- | --- | --- |
| `R05_GUARDIAN_MAP_ACTION_4DIR` | `V353U001` | 四向 `idle/step_a/step_b/brace/recoil` |
| `R05_BREAKER_MAP_ACTION_4DIR` | `ENEMY_C01_BREAKER` | 四向 `idle/charge/contact` |
| `R05_VEHICLE_EAST_MOVE` | `TARGET_C01_EMERGENCY_AMBULANCE` | 应急车自动通过 |
| `R05_SHIELD_WALL_HUNG` | `PROP_C01CDV1_RETIRED_SHIELD_WALL_HUNG` | 三道旧焦痕的墙挂重盾 |
| `R05_CUTIN_SWARM_INTERCEPT` | `V353U001` | 小体截击关键帧 |
| `R05_CUTIN_GIANT_CONTACT` | `V353U001;ENEMY_C01_BREAKER` | 首次巨体接触关键帧 |
| `R05_CUTIN_ARTILLERY_SIDE_HIT` | `ENEMY_C01_BREAKER` | 侧甲命中关键帧 |
| `R05_CUTIN_RED_CHARGE` | `ENEMY_C01_BREAKER` | 红缝聚光，不含释放 |
| `R05_FX_CONTACT_DUST` | `PRES_C01E02_R05_CONTACT_DUST` | 碰撞尘土／碎屑 |
| `R05_ROAD_STATE_LONG_BROKEN_ARC` | `PRES_C01E02_R05_ROAD_LONG_BROKEN_ARC` | 成功草案 A：长弧裂痕／强度 72 |
| `R05_ROAD_STATE_TWIN_BUCKLES` | `PRES_C01E02_R05_ROAD_TWIN_BUCKLES` | 成功草案 B：双隆起／强度 80 |
| `R05_ROAD_STATE_BREAKER_STRAIGHT_GOUGE` | `PRES_C01E02_R05_ROAD_BREAKER_STRAIGHT_GOUGE` | 失败草案：直线犁沟／强度 62 |
| `R05_FX_ARTILLERY_HIT` | `PRES_C01E02_R05_ARTILLERY_HIT` | 白闪、火花、黑色碎片 |
| `R05_FX_RED_CHARGE` | `PRES_C01E02_R05_RED_CHARGE` | 红光蓄能循环 |

音频槽位为 `R05_SFX_COMMS_OPEN/CLOSE`、`CURSOR`、`CONFIRM`、`ILLEGAL`、`SUMMARY_OPEN`、`HOLD_LOOP`、`FOOTSTEP`、`ROAD_BREAK`、`VEHICLE_PASS`、`SWARM_RUSH`、`GIANT_CONTACT`、`ARTILLERY_HIT`、`RED_CHARGE_LOOP`、`RED_CHARGE_STING` 与 `RAIN_ALERT_AMBIENCE`。不含配音或 BGM。

## 6. 资产交接字段

每个真实槽必须精确验证：

```text
producer_handoff_id
slot_id
expected_stable_id
subject_id
usage
build_id
presentation_profile_id
rules_profile_id
topology_sha256
resource_path
sha256
binding_kind
native_width / native_height
has_alpha
pivot
safe_area
atlas_frames / animation_frames
facings
duration / fps / sample_rate / channels
source_approval_receipt
```

路径正规化后必须位于 R0.5 Candidate 资产根内，拒绝 `..`、符号链接逸出和字符串前缀伪装。未批准、坏 hash、错 stable ID、错尺寸、错帧、错绑定的单个槽只回退该槽，不得让玩法变化或全局 fatal。

## 7. Full、Skip 与 fallback

- `Full`：播放地图移动、角色短通讯、关键帧、FX 和音频；
- `Skip`：在锁定同一已提交计划后快速应用同一表现事件列表的末态；
- `Fallback`：不存在真实资产时，使用同 pivot、同 footprint、同时长边界的具名几何，不回退旧图；
- 三者不得重算 gameplay，不得二次提交 resolver，不得修改世界结果。

## 8. 联合证据

最终真实接入车道至少交付：

- `PLAN_EDIT`、`PLAN_SUMMARY`、两个成功结果、一个失败结果的 1280×720 PNG；
- 完整 Full 和 Skip 视频；
- Full 播放首帧与最终世界状态不得相同；B03–B08 至少各有一个可核验的中间视觉状态；
- 角色通讯触发回执；
- 每个表现 beat 的开始／结束时间与资产槽回执；
- Full/Skip/fallback 结果等价证据；
- UI 遮挡、文字溢出、重复台词、非法旧资产探测和非默认入口的自动测试。
