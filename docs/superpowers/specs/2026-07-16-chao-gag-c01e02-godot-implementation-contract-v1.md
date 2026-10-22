# 《超GAG机器人大战》C01E02 Godot实现契约 v1

> 日期：2026-07-16  
> 状态：`logic_and_chapter_runner_verified / visual_production_pending`  
> 适用目标：把已正式验收的《四张封存令》迁入当前Godot Story-First运行时。  
> 本文不重写剧情、不迁移Canon，也不以现有Demo的便利性削弱五回合合同。

## 1. 权威输入与当前证据

实现前必须同时读取：

1. `剧情梗概/V35.9/rebuild/episodes/C01/C01E02-四张封存令-v1.md`
2. `剧情梗概/V35.9/rebuild/episodes/C01/C01E02-runtime-contract-v1.tsv`
3. `剧情梗概/V35.9/rebuild/episodes/C01/C01E02-graybox-constants-v1.tsv`
4. `剧情梗概/V35.9/rebuild/reviews/C01E02/22-final-acceptance.md`
5. `2026-07-15-chao-gag-c01e02-story-first-canon-migration-v1.md`

2026-07-16执行`python3 scripts/check_c01e02_runtime_graybox.py`，以下六组检查全部通过：Token路线、F2入场、五人释放、R2分支、回合点池、RT038唯一原子提交。该结果证明源合同可执行，不证明Godot实现已经存在。

同日首个Godot实现增量已通过：`c01_e02_fire_evacuation_5r.json`、`c01e02_fire_evacuation_battle_session.gd`和Scenario Driver Registry现可无界面跑通两条R2工序路线、R3配对补偿、R4四Token 29/29楼外、R5局部检查点失败重试与本地Battle Clear。该增量本身不包含Episode Graph、ADV、RT038 Episode提交、连续Runner或资产，不能据此宣称第二话可玩完成。

第二个Godot实现增量也已通过：`c01_e02_fireline_investigation.json`和`c01e02_fireline_investigation_mode.gd`支持三证任意顺序、首次多轮对话、重复短回看、普通物件非因果隔离、按住方向键连续移动及保存恢复；三证闭合只提交一次`OLD_LAYER_EVIDENCE_READY`。Graph、开场/共同建图/白函结尾ADV、RT038 Episode提交、连续Runner和P0/P1资产仍未完成。

2026-07-16第三个Godot实现增量已通过：`graph.story_first.json`和`manifest.story_first.json`将黑水开场、火线三证、公共建图、五回合消防撤离与白函远程结尾连成五节点Episode。`EpisodeDirector`新增`local_transition_only`，RT001-RT037均只推进局部态；`NarrativeModeScene`可携带结构化`outcome_payload`，白函台词播放完才以`C01E02:RT038:ATOMIC_SNAPSHOT:V01`一次写入人员、权限、物理、机体、关系和敌方样本。整话集成测试实际验证R5失败局部回滚、Battle Clear不持久化、白函ADV前零E02持久键以及RT038唯一提交。

2026-07-16第四个Godot实现增量已通过：`GameKernel.continue_episode()`在替换EpisodeDirector和ModeRouter时保留`RunStateStore`；新默认入口`c01_story_first_chapter_playable.tscn`由`c01_story_first_chapter_runner.gd`连续运行E01和E02，并保存当前Episode索引。跨话Smoke Test从E01真实RT013S终局节点完成后自动进入E02黑水开场，验证RT013S只有一次、B1泵保持零压接管、馆守Z右臂保持连接，E02局部ADV不新增持久事务。当前未完成项缩减为P0/P1正式资产接入、八帧视觉捕获、外部容量回执、Windows真机和实体控制器验证。

## 2. 实现结论

C01E02不能套用普通“我方移动攻击 -> 敌方移动攻击”的战斗模板。它是一张**事件战棋地图**：玩家编排小机工序、工作人员工序和固定消防支援，四组人员按声明路线自动移动，敌方轨道工具在固定相位施压，环境最后结算。

必须同时成立：

- 12x14斜45度固定战术图，L1前厅、装卸坪和B1入口在同一平面表达。
- 先有约5至8分钟火线勘查，再进入五回合SRPG；三证不得在ADV、探索和SRPG重复提交。
- R1至R4所有战斗状态只在本地内存；R5成功仍不持久化。
- 白函远程结尾完整播放后，才由`C01E02_RT038`一次提交全部期末状态。
- R5失败只回到R5局部检查点；29人保持楼外隐藏，不回刷。
- 馆守Z、勇拳、白函都不是本图可操纵或可攻击单位。

## 3. Episode Graph

建议Episode ID：`C01E02-STORY-FIRST-CANDIDATE`。

| 顺序 | node_id | mode | 合同范围 | 玩家可见任务 | 持久事务 |
|---|---|---|---|---|---|
| 1 | `c01e02_black_water` | `NARRATIVE` | RT001-RT003 | 看清29人仍在馆内、四令的物理后果与七海切电的正负结果 | 无；只读E01 RT013S |
| 2 | `c01e02_fireline_evidence` | `SPATIAL` | RT004-RT007 | 完成机器犬烟流、跌跌温度片、双层旧管三证链 | 本话局部态 |
| 3 | `c01e02_public_map_setup` | `NARRATIVE` | RT008-RT010 | 共同建图；消防架桥机四腿落地并接入联合救援端 | 无 |
| 4 | `c01e02_fire_evacuation` | `TACTICAL` | RT011-RT036F | R1-R4送29人离楼，R5反折SEG3保住五人退路 | Battle Clear仍为局部态 |
| 5 | `c01e02_baihan_remote` | `NARRATIVE` | RT037-RT039 | 白函远程改报并预量18米框位 | 台词播放完才提交RT038 |

所有成功边单向连接。探索取消返回当前探索，战斗失败按失败层级重试，不允许跳过白函结尾直接完成Episode。

Episode完成回执必须明确：

- `transaction_id=C01E02:RT038:ATOMIC_SNAPSHOT:V01`
- `C01E02_ATOMIC_TRANSACTION=COMMITTED`
- `C01E02_PHYSICAL_SNAPSHOT`含完整替代性快照，而非增量碎片。

## 4. 火线勘查模式

新建`c01e02_fireline_investigation_mode.gd`，复用空间交互底层，不复用E01六房间自由逛馆外壳。

### 4.1 场景范围

- 一张紧凑前厅/门槽/泵站入口场景。
- 玩家控制纪存在可行走区域连续移动，支持按住方向键和鼠标持续行走。
- 信息面板不得遮挡可交互物；对话时进入单一放大层，底部不重复显示同一句。

### 4.2 必做三证

| offer_id | 参与者 | 演出 | 局部事实 |
|---|---|---|---|
| `inspect_dog_smoke_streamer` | 纪存、机器犬 | 传感器朝出口，飘带反向指馆内 | `OLD_LAYER_EVIDENCE_1_OF_3` |
| `retrieve_diedie_temperature_strip` | 纪存、跌跌 | 跌跌穿低位缝，推回烧焦双色温度片 | `OLD_LAYER_EVIDENCE_2_OF_3` |
| `trace_double_wall_pipe` | 纪存、唐胶、兜灯 | 敲墙回声与低温示踪叠加 | `OLD_LAYER_EVIDENCE_3_OF_3` |

三项首次完成后，自动形成`OLD_LAYER_EVIDENCE_READY`并开放退出。顺序可自由；每项首次为多轮对话，重复调查只给短回看，不重复选项、不重复写状态。

可选物件只承担氛围：门框热变形、总管发黄、湿晚饭袋、无编号螺栓盒。后二者不得变成变量或谜题钥匙。

## 5. 五回合事件战状态机

新建`c01e02_fire_evacuation_battle_session.gd`，继承`DeclarativeBattleSession`，但使用独立`scenario_driver`：`c01e02_fire_evacuation_v1`。

### 5.1 固定相位

R1-R4：

`small_units -> staff_work -> fire_support -> enemy_tools -> evac_auto -> environment -> local_receipt`

R5：

`relation_event -> f2_entry -> local_checkpoint -> brave_preview -> fire_support -> beam_fall -> local_guard`

剧情事件和自动移动不暗扣AP。玩家任何时候可请求结束当前行动层或回合，但缺少必要工序时必须显示将发生的停步、烟值或硬失败结果，不能按钮无效或软锁。

### 5.2 本地状态

Session至少保存：

- `round_number`
- `phase_id`
- `completed_actions`
- `staff_ap_remaining`
- `fire_points_remaining`
- `token_cells`与`token_smoke`
- `diedie_cell`、`dog_harness_state`
- `bridge_state`与`seg3_state`
- `pump_state`、`door_state`
- `needle_state`、`ruler_state`
- `qihai_write_state`、`city_fire_support_state`
- `r2_fire_choice`
- `local_receipts`
- `r5_checkpoint`
- `failure_reason`

这些字段必须进入`snapshot()/restore()`，否则笔记本覆盖层、保存恢复和R5重试会破坏回合状态。

### 5.3 回合动作

**R1**

- 跌跌：离合准备。
- 机器犬：与C3及软管建立`GUIDE_AND_HOSE_HARNESS`，之后不再单独行动。
- 工作人员共享2 AP：唐胶隔板、兜灯/兜灯线迹锁定合同中的对应工序。
- 消防机3点一次确认固定合法桥序`SEG1 -> SEG2 -> SEG3`；错误预览零消耗返回。
- 回合末必须满足C3挂接、三桥段完成、人口守恒。

**R2**

- 工作人员完成内门手动保持和隔板转位，跌跌复位泵闩。
- 唯一消防点给出带后果预览的二选一：
  - `WATER_CURTAIN`：D5烟值较低，针车进入接触态。
  - `PREEMPTIVE_INTERFACE_FLUSH`：针车提前后退，D5烟值较高。
- 标尺机在敌方相位由预置材料角度实体弹开。

**R3**

- 回合开始演出七海撤销本人东侧高压令；写权限灰掉，城市消防支援保留。
- 跌跌先锁离合，工作人员后接低压旁路；顺序反了不结算成功。
- 消防动作必须补偿R2选择：先护人则冲洗针车，先冲洗则补延迟水幕。
- 两路收束到工具安全、泵手动低压、D5烟值低于3。

**R4**

- 四Token按`C3 > B10 > D5 > A11`逐tick自动推进到四个楼外固定格。
- C3不可拆，D5必须仍是原四名需协助成人加同一维修员。
- 跌跌退到`(9,9)`检修凹位；机器犬随C3到`(1,7)`。
- 形成`FIRE_SUPPLY_BURNED_LOCAL`，但不提交Episode状态。

**R5**

- 纪存报29，七海问32；自动清场取消。
- 两名外部消防接驳员按GB038入场，建立R5局部检查点。
- 勇拳只播放许可继电响一下、机内压力零、本体零位移。
- 城市消防新发1点；玩家反折SEG3，保留检修踏步并承梁。
- 成功后仍需进入白函ADV；失败恢复R5检查点，29人保持隐藏楼外。

## 6. 地图与HUD

地图严格读取Graybox TSV，不在GDScript复制另一套坐标真相。首版可把TSV转译为JSON，但JSON必须可由测试与TSV逐项比对。

### R1-R4侧栏

- 主目标：`R4前 29/29 离楼`
- 必要条件：`C3完整 / B1泵手动低压 / 烟值<3`
- 显示：共享工作人员AP、消防点池、四Token端点和人数、烟值、针车/标尺机下一动作。
- R2预览必须同时画出D5烟值变化和针车结果。

### R5侧栏

- 主目标切换为：`反折SEG3，保住五人退路`
- `29/29已在楼外`固定绿色显示，不作为重新移动的单位。
- 显示：新应急点1、次梁坠落意图、五人出口连通性、消防机左前腿压力。

地图视口不能被菜单覆盖。菜单放右侧栏；地图上的意图线、桥段、烟区、Token路线和固定支援轮廓必须始终可读。

## 7. 代码复用与缺口

### 可直接复用

- `EpisodeBundleCompiler`：NARRATIVE/SPATIAL/TACTICAL图编译。
- `EpisodeDirector`与`RunStateStore`：节点推进和RT038单事务提交。
- `NarrativeModeScene`与`NarrativeDirector`：双侧人物、当前说话者高亮、系统/远程通讯演出。
- `SpatialNarrativeOverlay`、`StableObjectRegistry`、`SpatialNpcRegistry`：三证调查和重复态。
- `DeclarativeBattleSession`：战斗定义、保存恢复、Outcome外壳。
- `TacticalModeScene`：斜45度坐标、光标、侧栏、表现队列和输入。
- E01跌跌、机器犬、撤离Token、馆守Z半跪资源可作为基线复用。

### 逻辑运行时实现状态

1至5已实现并进入自动回归；正式视觉生产仍按第8节执行。

1. `scenario_driver_registry.gd`
   - 用`scenario_driver`映射Session类和可选Presentation Adapter。
   - 替换`TacticalModeScene._new_battle_session()`对E01类的直接硬编码。
2. `c01e02_fire_evacuation_battle_session.gd`
   - 多行动层、自动Token、烟值、工具状态、R2分支、R5检查点和Outcome。
3. `c01e02_fireline_investigation_mode.gd`
   - 紧凑火线勘查，不复制E01房间路线逻辑。
4. 场景无关战术绘制接口
   - Session提供`map_overlays()`、`intent_overlays()`、`scenario_status()`和`presentation_events()`。
   - `TacticalModeScene`不再增加`_draw_c01e02_*`硬编码岛。
5. Chapter Runner
   - 默认入口已改为`c01_story_first_chapter_playable.tscn`，保留E01 RT013S后无重置启动E02。
   - 话间手动存档携带Episode索引与Director快照；单话E01入口仍保留作调试用途。

## 8. 资产分级

### P0：功能验证不可缺

- 12x14三翼火场地形与烟/热覆盖层。
- 消防架桥机固定全身俯视/斜45度图、四腿状态、三段桥独立图层。
- 针车与标尺机共享轨道底盘及两种工具臂。
- 四类撤离Token、D5低速托盘、F2双人标记。
- 勇拳封闭运输架静态图；许可灯必须能保持黑色。
- 反折SEG3、次梁、开放检修踏步、左前腿过载状态。

### P1：首轮视觉评审

- 黑水喷头/前厅烟压ADV背景。
- 共同建图与消防机四腿落地背景或分层大图。
- 七海便装通讯肖像、权限灰条状态。
- 白函远程折叠线与18米框位合拢演出。
- 跌跌温度片、机器犬飘带、唐胶/兜灯双层管取证小演出。

### P2：爽感增强

- 三段桥逐段落下的短Sprite动画。
- 针车冲洗反冲、标尺机熔痕偏转。
- SEG3反折承梁、火星、悬挂压缩和涂层发黑的Cut-in。
- 消防驾驶员压力播报与角色短反应镜头。

已有`unit_brave_fist.svg`只能作为占位参考，不能证明静态运输架资产完成；现有馆守Z资源不得播放站起、攻击或断臂动画。

## 9. 文件交付清单

```text
game-godot/content/episodes/c01/e02/
  manifest.story_first.json
  graph.story_first.json
  battle/c01_e02_fire_evacuation_5r.json
game-godot/scripts/core/battle/
  scenario_driver_registry.gd
  c01e02_fire_evacuation_battle_session.gd
game-godot/scripts/modes/multi_play/
  c01e02_fireline_investigation_mode.gd
game-godot/assets/battle_presentation/c01/e02/
  manifest.json
  ...P0/P1 assets
game-godot/scripts/
  c01e02_story_first_smoke_test.gd
  c01e02_story_first_episode_integration_smoke_test.gd
  c01e02_story_first_visual_capture.gd
```

## 10. 验收门槛

实现不能只凭“能打完”判定完成。

1. **源合同**：`python3 scripts/check_c01e02_runtime_graybox.py`通过。
2. **编译**：E02 manifest/graph/battle资源全部由`EpisodeBundleCompiler`编译，无未知场景、坐标或实体引用。
3. **两条R2路径**：护人和抢先冲洗都能在R3补偿后进入同一安全状态。
4. **硬失败**：烟值3、C3拆分、缺桥、泵永久锁、R4非29、R5退路压死均有可恢复路径，无软锁。
5. **R5回滚**：失败后29人不回刷、R5新点恢复为1、未写RT038；重试成功可继续。
6. **原子提交**：白函ADV前世界状态无E02持久键；ADV后所有RT038键一次出现，RT039只读。
7. **连续流程**：E01完成后直接进入E02，E01 RT013S原样可见；不能靠重新启动场景伪造输入。
8. **视觉捕获**：至少保存黑水开场、三证完成、R1桥序、R2选择预览、R3七海停权、R4 29/29、R5反折桥、白函18米框位八帧。
9. **Canon**：`scripts/canon-smoke-test.sh`和`scripts/canon-check-godot.sh --strict`通过。

## 11. 实现顺序

1. 建scenario driver registry，回归E01无变化。
2. 建E02 JSON、Session纯状态机和无渲染Smoke Test。
3. 接战术HUD、意图、自动Token和R5检查点。
4. 实现三证探索及Graph/Manifest。
5. 接ADV、RT038原子提交和E01到E02连续Runner。
6. 补P0资产并做视觉捕获。
7. 两条R2路线、全部失败门和完整Episode集成回归。

在第2步以前不生成大批美术；在第5步以前不宣称第二话能走通；在第7步以前不宣称C01E02实现完成。
