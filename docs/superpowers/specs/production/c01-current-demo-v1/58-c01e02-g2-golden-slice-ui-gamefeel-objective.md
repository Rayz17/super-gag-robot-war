# C01E02 G2｜Golden Slice UI、交互、共同回合与打击感目标

> Owner：主程序 Session  
> 依赖：55、56；与57的 Gold Frame 并行  
> 状态：`Candidate / non-default / internal until real handoff`  
> 本轮不得自行搜索、选择或加载任何真实美术

## 1. 保留与重做

### 保留

- M3-J1 纯 resolver、草案零写入、冻结敌方意图、preview／execute同源；
- waypoint路线、终点朝向、主动作／预备反应／备用方案；
- 32×18地图逻辑、单位footprint、滚屏、重试、确定性、Full／Skip结果等价；
- M1a 的精确 allowlist、逐槽 fail-closed、Sprite／Atlas／Texture／Audio consumer 技术经验。

### 不继续堆叠

- 不在约1100行即时绘制式 `m3_j1_sandbox.gd` 上换皮做成品 UI；
- 不把硬编码720p矩形、文字表格、调试时间线、程序剪影或单音效播放升级为“视觉Demo”；
- 不读取 A8 B1.1、旧portrait／unit、`story_first/**`、旧 M2 receipt 或美术工作目录。

## 2. 新车道

在全新 `m3_golden_slice` 命名空间建立非默认构建；默认M2、现有M3-J1证据与旧测试保持只读。

建议结构：

```text
shared_round_domain/        纯数据、三轮状态与resolver适配
tactical_world_view/        地图、单位、意图、路线、环境状态
planning_hud/               正式Control/Theme与渐进教程
commit_summary/             地图内摘要与长按执行
performance_director/       镜头、hit-stop、FX、角色通讯、Cut-in
audio_director/             多层并发、ducking与总线
asset_consumers/            等待制作人exact handoff的语义槽
```

不得把所有显示、输入、玩法和演出重新塞进一个脚本。

## 3. G2-A｜内部玩法与表现骨架

本阶段可以使用专用测试 fixture，但所有捕获只作内部工程证据，不得给用户判断画面。

### 三轮共同回合

1. 第一轮：让车、挡小体、占线、第一次巨体接触、炮击、红光蓄能。
2. 第二轮：从真实第一轮状态取盾并挡赤红；最后车辆随后通过，东门关闭。
3. 第三轮：玩家以位置、朝向、持盾、已挡击、撤离清空与 BREAKER 重心共同形成盾拍机会；执行后到 P1。

必须实现 A／B 两种第一轮方案，并让差异实际影响第二轮：

```text
guardian_position
guardian_heat
breaker_depth
road_damage
warning_facility_state
swarm_positions
remaining_timing_margin
```

若两路只改变字符串、评分或不可见字段，视为失败。

### 盾拍语义

`shield_bash_opportunity` 不是技能进度清单。只有以下条件同时投影到普通规划语法时才出现一次性情境动作：已取得且挡过赤红的盾、撤离线已清空、BREAKER处于未收回重心／偏轴窗口、馆守 Z可在本轮结束于合法侧向接触区、终点朝向与推力矢量把敌人压回南侧。错过窗口必须重新制造偏轴。

### 自动主体

车辆、小体、BREAKER、城市炮与环境按提交前冻结意图共同结算；敌人不得读取玩家未提交草案。小体仍各自行动，不接受 BREAKER 指挥。

## 4. 正式 UI 与交互

- 使用 Godot `Control/Container/Theme` 和世界空间 Overlay；支持1280×720基准与向上缩放。
- 地图占主画面；顶部一个目标＋最多三个威胁；右侧命令抽屉可收起；底部五图标时间线。
- 意图／时点／目标箭头贴在单位和地格上；无选择时不铺满网格。
- 路线为可增删 waypoint 的粗亮路径带；终点显示2×2幽灵、朝向扇面、保护区和争格提示。
- 摘要保持地图可见，只回答五个玩家问题；按返回可继续修改，世界状态与随机种不变。
- “执行本轮”需约0.7秒长按，具备进度环、蓄能声与中途取消；提交后不接受后见之明弹窗。
- 摄像机中央约60%安全区；光标过阈值才滚动，带平滑减速和地图边界；执行时由director接管，结算后恢复玩家上下文。
- 教程分步开放，不提供唯一答案；帮助只能解释规则与风险。
- 用户可见画面禁止坐标、内部ID、hash、Candidate、debug英文与“REAL ART”技术标记。

## 5. 表现导演与打击感

建立数据驱动的表现 cue，不把视觉时长写回玩法 resolver。至少支持：

- `anticipation_ms`、`hit_stop_ms`、`shake_vector/amp/decay`、`flash_frames`、`recoil_ms`、`aftermath_ms`；
- world／UI／character／cutin分层；
- camera pan／zoom／lead／return；
- 同一事件的Full／Skip／fallback；
- 多路音效并发与BGM／ambient ducking；
- Cut-in结束后精确恢复地图位置、朝向、环境状态与当前焦点。

首次巨体接触目标：250–400ms蓄势、67–100ms hit-stop、120–180ms定向震屏、250–400ms反冲、500–800ms道路与碎屑余波。实际值允许微调，但不得退化为sprite平移＋一次白闪。

音频系统必须能在同一事件叠加至少四层并控制总线；不能像当前原型一样只播放第一个槽。正式音频缺失时该事件标记 `presentation_not_ready`，不得用程序噪声冒充用户版。

## 6. 资产接口

G2-A 只定义语义槽，不冻结最终尺寸／帧数；57 Gold Frame 与美术实物通过后，由制作人签新的 exact handoff。最低语义槽：

```text
VS_MAP_BASE / BUILDINGS / ROOFS / FOREGROUND / OCCLUSION / LIGHTING
VS_GUARDIAN_QSD
VS_BREAKER_QSD
VS_SWARM_QSD
VS_VEHICLE_EAST
VS_SHIELD_STATES
VS_JICUN_PERFORMANCE
VS_QIHAI_REMOTE
VS_DOUDENG_PERFORMANCE
VS_OLD_GUARDIAN_GUIDE / CONTACT / SHIELD_GAZE
VS_CUTIN_RISE / SHIELD_BLOCK / SHIELD_BASH
VS_FX_* / VS_SFX_* / VS_BGM_* / VS_AMBIENT_*
```

主程序不得根据相似文件名、时间戳或目录扫描自行绑定。身份关键槽任一缺失、错SHA或fallback时，`integrated_visual_playtest_ready=false`。

## 7. G2-A 验收与停止点

机器与内部人工必须证明：

- 三轮共享前态结算，第一轮两解实际改变第二轮；
- 摘要可返回且与执行同一 resolver；
- 盾拍由身体／时序条件生成；
- 摄像机阈值滚动、UI焦点与输入链可用；
- 多层音频与表现 cue 能被真实消费者调用；
- Full／Skip、20次重放、容器重排、失败重试结果一致；
- 无Reader／Canon／默认M2／正式存档写入；
- 真实资产加载数仍为0，且没有旧资产探测。

完成后停止在制作人门；不展示夹具画面，不声称 UI、打击感或联合 Demo 已完成。等待57 Gold Frame通过和制作人 exact handoff，再进入 G2-B 真资产联合实机。

## 8. G2-B 预告（本轮不提前执行）

在制作人签发真资产与Gold Frame布局后：

- 将正式地图、单位、人物、FX与音频接入同一非默认构建；
- 先完成45–75秒 Golden Turn；
- 录制Full／Skip与A／B两路捕获，制作人视觉门通过后才交用户；
- 用户认为值得继续后，再扩完整约4.5分钟 Golden Slice。

禁止自行开始 G2-B、P1、Runtime copy、LibTV、完整E02或默认入口替换。

