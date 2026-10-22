# PATCH

> 席位：独立 Canon / 宏观谜团 / 物理连续性定向复核（r2）  
> 范围：仅核对当前源文件、机器表与独立纸演；未读取或采用其他新席位审稿正文。  
> 裁决：C01E02 本话故事、Runtime/Graybox 与原子快照内部闭合；但当前入口、Canon 查询面、S03/S04 下游输入、V35.8 资产语义及设计图谱仍有活跃旧口径或缺边，不能放行为全链闭合。

## 1. 已核对且成立的硬事实

| 核对项 | 独立证据 | 裁决 |
|---|---|---|
| 原始人口守恒 | `C01E01-runtime-contract-v1.tsv:2,19`锁定20:47馆内总数32=`29名撤离对象+纪存/唐胶/兜灯`；`C01E02-input-carry-v1.md:13-22`逐项承接；`C01E02-graybox-constants-v1.tsv:13-16`把29人固定压成`A11+B10+C3+D5`，其中C3含两个孩子，D5含E01同一名维修员；`C01E02-四张封存令-v1.md:187-213`与`C01E02-runtime-contract-v1.tsv:32-37`锁定R4后29楼外、三名核心仍馆内，R5才有两名不属于原32人的城市消防接驳员进入 | 没有凭空增员，也没有把孩子或维修员重生为第五Token。唯一合法表达是：初始32；R4为29楼外+3核心馆内；R5为3核心+F2馆内侧，F2是新增外援、不计原32 |
| E01原子快照 | `C01E01-runtime-contract-v1.tsv:19`的`RT013S`是唯一提交：29只到前厅而非城市安全区，C3监护完整，馆守Z右臂机械核心连接、仅前臂外甲拆检，展陈灯闭馆熄灭而城市电网/维生在线，半开防火门锁死，旧钥匙冻结，B1泵压零，胸灯断，东侧烟进入且喷淋无压；`2026-07-15-chao-gag-c01e01-story-first-canon-migration-v1.md:23-27`的`C01MIG003-007`一致 | E02输入没有从Reader或旧Godot另取状态 |
| 七海权限与城市支援分域 | `C01E02-四张封存令-v1.md:81-93`锁定七海第一条系统命令仅为“切东侧高压，保留西侧维生和出口标志”；`:167-185`锁定她只撤本人签发的东侧高压锁，保留母线隔离并只放消防低压支路；`C01E02-runtime-contract-v1.tsv:2-3,23-25`分别保存`QH_SYSTEM_WRITE_DISABLED`与`CITY_FIRE_RESCUE_SUPPORT=ACTIVE`，防火门靠跌跌机械旁路，B1泵靠兜灯低压旁路 | 七海不能解除安全端门锁、军方泵锁、平台旧钥匙或代哥胸灯切断；停权不等于城市消防撤回 |
| 灯、电、门、泵、烟与期末物理账 | 输入见`C01E02-input-carry-v1.md:13-22`；结算见`C01E02-四张封存令-v1.md:355-365`：`B1_FIRE_PUMP=MANUAL_OPERABLE_LOW_PRESSURE`、西侧消防供水热变形受限、商业后勤风道局部烧损、档案主库完整但紧急冷却、西出口反向支撑下手动开启、城市电网局部隔离且维生在线、旧数字钥匙仍冻结、完整移动脊柱未暴露 | 物理预算成立；E03不得把泵恢复为整馆供水、把风道/档案伤痕清零或把移动脊柱当作已公开地图 |
| 馆守Z、消防架桥机、勇拳、白函 | `C01E02-四张封存令-v1.md:367-377`锁定馆守Z半跪、右臂连接、仅被动冷却；消防机完整全身首显、SEG3反折承梁、左前腿过载；勇拳仅运输架继电闪断、本体零动作、豪司不在场；白函仅远程中庭框位预布。`v35_8_slot_unit_manifest_v35_8.tsv:7-12`、`v35_8_lifecycle_event_review_v35_8.tsv:9-17`与`v35_8_slot_source_absorption_v35_8.tsv:8-11`支持同一E02/E03分界 | 馆守Z断臂、消防机首次自由控制、豪司越权驾驶和白函具身均留E03；E02未提前消费 |
| 公共消防图边界与敌方收益 | `C01E02-四张封存令-v1.md:125-145,355-377`只公开完整消防/撤离层，`FULL_MOVING_SPINE=NOT_EXPOSED`；代哥取得消防图、消防桥接口、七海撤令模式和“救援可被重标为资产迁移”的样本 | 公共图足以带来明确敌方收益，但不等于B1完整移动脊柱、馆体起航结构或0号深层已暴露 |
| G.A.G./索引/白函边界 | `v35_7_mystery_slot_binding_v35_7.tsv:5`、`v35_7_foreshadow_slot_binding_v35_7.tsv:4`、`v35_7_continuity_thread_backflow_v35_7.tsv:13`均锁定C11前只有索引组件/分类规则、没有连续第一人称人格；`entities.tsv:471`明确白函是远程到具身的封存执行机，不是索引肉身或连续人格；本话`:52`亦不把共享组件写成人格 | 宏观谜团没有被E02提前揭晓；白函可以学习样本，但不是“索引天使早期肉身” |
| E03唯一输入与E04载荷延期 | `C01E02-runtime-contract-v1.tsv:39-42`只允许`RT038`在白函远程ADV完成后提交；`C01E02-四张封存令-v1.md:379-382`明定E03必须且只能读取`C01E02_PHYSICAL_SNAPSHOT`；`2026-07-15-chao-gag-c01e02-story-first-canon-migration-v1.md:24-27,31-42`锁定`C01MIG008/009/011/012`；C01地图`:94`锁定所有人先撤完，E04才从生活维持设备、实体独有馆藏、档案服务器三类中选二 | E02正文未提前做E03断臂/具身战，也未把人命重新塞进E04载荷选择 |

独立按Runtime/Graybox相位重放的终点为：`32_initial(29+3)`；R4=`29_outside+3_core_inside`；R5新增`F2_external`；烟表终值`A0/B1/C0/D2`；只有`BAIHAN_REMOTE_PRESET_COMPLETE`后提交`RT038`。因此本轮问题不是E02五回合本体不可执行，而是活跃查询与下游承接尚未迁净。

## 2. 必须修的活跃冲突

### 2.1 当前C01地图仍保留错误四令与越权撤令

1. `docs/superpowers/specs/剧情梗概/V35.9/rebuild/maps/C01-逐章重构地图-v1.md:68`
   
   活跃冲突：把四方动作写成“消防切电、代哥锁接口、平台冻钥匙、军方把馆守Z和B1划军资”，既漏掉安全端防火门锁，又把七海后发的东侧高压命令混进E01四令，还把代哥/军方的物理对象写错。
   
   最小修法：改为“安全端锁半开防火门；代哥端切馆守Z胸灯；平台冻结旧路由数字钥匙；军方端令B1泵压归零。七海切东侧高压是随后独立的第一条系统命令。”

2. 同文件`:71`
   
   活跃冲突：“服务器别再派人回去”赋予七海未建立的服务器调度权，并把E04服务器载荷词提前带入撤令。
   
   最小修法：逐字采用本话权限句：“撤销我签发的东侧高压锁。保留母线隔离，只放消防低压支路。现场继续往外带人。”随后保留写权限熄灭与城市消防继续两个分离状态。

### 2.2 当前PB的E03/E04入口没有完整读取唯一快照

1. `docs/superpowers/specs/剧情梗概/V35.9/chapters/C01/PB-V357-C01-S03.md:14,18,23,28,32`
   
   活跃冲突：`:14`仍以“内部地图外泄、三目标撤离损失”概括输入；`:18,28`写未定量“撤离人群/人群”，会让实现从已出楼29人中凭空回填观众；`:23,32`虽有两条撤离线，却未锁定桥上只有三名核心、两名F2接驳员和必要设备。
   
   最小修法：`:14`改为“唯一读取`C01E02_PHYSICAL_SNAPSHOT`”，逐项列出29楼外、3核心+F2馆内、供水热损、商业风道局部烧损、档案主库紧急冷却、消防机左前腿过载、馆守Z右臂连接、勇拳冻结、白函远程预布、完整移动脊柱未暴露；`:18,23,28,32`把泛称人群改为“纪存、唐胶、兜灯、两名城市消防接驳员及必要设备”，不得生成第六人或把29人召回。

2. `docs/superpowers/specs/剧情梗概/V35.9/chapters/C01/PB-V357-C01-S04.md:14,22,27,34`
   
   活跃冲突：`:14`只列E03人物/机体结果，漏读E02供水、风道、档案伤痕；`:22`仍用不定量“有人未出”；`:27`把选择写成“馆藏/人员模块”，重新把人命做成载荷；`:34`只说“两组模块”。
   
   最小修法：入口增加`C01E02_PHYSICAL_SNAPSHOT;S02_EVAC_SCAR`并声明E03只追加断臂/豪司/纪存记忆结果、不清除E02物理伤痕；`:22`明确仅指S03已知五人和必要设备；`:27,34`改为“全员安全后，从生活维持设备、实体独有馆藏、档案服务器三类选二”，失败与未选损失不得再含人员模块。

3. `docs/superpowers/specs/data/story/v35_5_c01_c03_state_propagation_v35_5.tsv:5`
   
   活跃冲突：E04 incoming仅有`GZ_RIGHT_ARM_LOST;QH_SUSPENDED_INTERNAL_REVIEW`，且值域仍是`collection_core|living_area|public_archive`，无法约束供水/风道/档案伤痕，也容易把`living_area`误读成人员。
   
   最小修法：incoming增加`C01E02_PHYSICAL_SNAPSHOT;S02_EVAC_SCAR`及E03增量；把三选二值域改成明确的`life_support_equipment|unique_physical_collection|archive_server`；`must_not_reset`增加“不得恢复消防供水、商业风道、档案冷却状态，不得把人员列为载荷”。

4. `scripts/build_v35_8_slot_loadout.py:1294-1296`
   
   活跃冲突：`SLOT_CONTINUITY_INPUT_PATCHES`只补S02，没有S03/S04；所以当前生成的`v35_8_slot_gameplay_contract_v35_8.tsv:4-5`无法证明E03唯一输入与E04伤痕/载荷承接。
   
   最小修法：增加`V357-C01-S03`和`V357-C01-S04`两条补丁，内容采用上两项的精确快照与载荷边界；重生成V35.8表并重跑strict。

### 2.3 `entities.tsv`旧场景字段会让canon-query优先返回过期答案

以下裁决按“当前Story-First确实出场”与“只剩历史实现来源”分开，不允许把所有旧ID机械替换成新ID。

#### 必须迁到V355 Story-First时序

| 文件/行 | 实体 | 最小迁移 |
|---|---|---|
| `docs/superpowers/specs/data/canon/entities.tsv:27` | `CH001`兜灯 | `first_battle_join`由`C01E02-BATTLE-START`改为`V355-C01E01`；她在E01三回合战已承担胸灯安全锁动作 |
| 同文件`:28` | `CH002`旧守护者 | `first_battle_join`改为`V355-C01E01`；限定为广播/导览人格与馆守Z低热支援，不得解释为本体首控 |
| 同文件`:31` | `CH_TANGJIAO` | `first_battle_join`改为`V355-C01E01`；E01已用安全罩改导光挡板 |
| 同文件`:35` | `CH_JICUN` | `first_battle_join`改为`V355-C01E01`；当前首次战术行动就是E01三回合救援 |
| 同文件`:53` | `ORG_DAIGE` | `formal_appearance`由`C01E02-MAP-STORY`改为`C01E01-QIHAI-CONSOLE`；E01零号异响后公务频道和四令接管已构成正式制度出场 |
| 同文件`:56` | `ENEMY_SAMPLE_PATCH` | 三个first字段改为`V355-C01E01`；规则改为E01 R2改写地箭、R3两台回收膜压力。旧“第4回合删除镜像”及V28/V31变体移入historical notes，不再作为active policy |
| 同文件`:57` | `ENEMY_SEAL_PATH_FRAME` | 三个first字段改为`V355-C01E01`；规则改为E01三回合活动路径框家族的复闭、卡轨、脱锚，不再指向旧E02/E03链 |
| 同文件`:62,66` | `LOC_WANJI_MAIN_HALL`、`LOC_WANJI_REPAIR_BAY` | 清除`C01E02-BATTLE-START`；主展厅战术首用改`V355-C01E01`。维修角若schema要求battle字段则同样指E01，否则留空并以E01探索/救援锚为准 |
| `docs/superpowers/specs/data/canon/scenes.tsv:98` | `V355-C01E01` | 把`ENEMY_SAMPLE_PATCH;ENEMY_SEAL_PATH_FRAME`加入required/allowed实体，闭合故事、生产表与实体首战三方引用 |

#### 必须标为historical/deprecated，不得伪造V355当前首战

| 文件/行 | 实体 | 最小迁移 |
|---|---|---|
| `docs/superpowers/specs/data/canon/entities.tsv:45` | `MECHA_GUARDIAN_Z` | 这是`V353U001`的旧重复ID。标`deprecated_alias_of=V353U001`并让canon-query重定向；旧`C01E01-GUARDIAN-CASE/C01E02-BATTLE-START`移入历史注。权威时序只取`:474`：E01可见低热支援，E03正式/首控/战斗加入 |
| 同文件`:54` | `ENEMY_SEAL_DRONE` | 当前E01/E02 Story-First均未使用该独立单位；把旧first字段和“第一话轨道进入”规则标`historical_runtime_reference`或`current_story_first_unscheduled`。保留已锁美术资产，但不得因资产存在推导当前出场 |
| 同文件`:55` | `ENEMY_ZERO_OPEN_ARM` | 旧6回合“连续2回合开门”仅保留historical/deprecated；当前E01/E02不排入。未来若使用`:333`的`ENEMY_ZERO_OPEN_ARM_RESIDUAL`，必须另走E03当前迁移，不能反向恢复旧首战 |

`scenes.tsv:19-21`已正确标成`historical_runtime_reference`，无需删除；问题在于上述活跃实体字段仍把它们当first答案。迁移必须让query默认命中`V355-C01E01/02/03`，只有显式查询historical时才返回旧场景。

同时修正以下同源查询面，否则只改`entities.tsv`仍会反污染：

- `docs/superpowers/specs/data/canon/runtime_rules.tsv:5`：七海远程规则scope从`C01E02-MAP-STORY`迁到当前V355 C01远程链；保留“第一章远程、无本人到场”的权限边界。
- 同文件`:6`：封存无人机语气规则可保留为通用美术/表演约束，但旧scene/allowed_from必须标historical或unscheduled，不能继续声称当前E01/E02参战。
- `docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv:5,9,32-34`：七海story gate改`C01E01-QIHAI-CONSOLE`；馆守Z锁转向`V353U001`当前生命周期；封存无人机/0号开启臂保留锁图但标Story-First未排期；采样贴片gate迁`V355-C01E01`。
- `scripts/canon-smoke-test.sh:22-37,106-108`：旧场景可作为“历史可检索”测试保留，但必须新增当前V355正向断言与负向断言：活跃first/formal/policy不得再返回`C01E02-BATTLE-START`、`C01E02-MAP-STORY`或6回合规则。

### 2.4 V35.8对馆守Z的动画预算仍允许身体动作

1. `docs/superpowers/specs/data/story/v35_8_slot_asset_manifest_v35_8.tsv:12`
   
   活跃冲突：馆守Z E02动画范围仍为泛化的`map_body_motion_and_one_readable_state_change`，与本话“半跪、右臂连接、仅被动冷却/低压继电、零身体动作”冲突。
   
   最小修法：改为`passive_temperature_sensor_and_low_voltage_relay_fx_no_body_motion`。

2. `scripts/build_v35_8_slot_loadout.py:1526-1542`
   
   根因：S02已有勇拳、白函、消防机override，却没有`(V357-C01-S02,V353U001)`。
   
   最小修法：补上述精确override，重生成资产表后运行`python3 scripts/check_v35_8_slot_loadout.py`。

### 2.5 设计图谱有新行，但语义引用未闭合且旧推荐节点仍活跃

1. 新链存在：`doc_registry.tsv:628-631`、`graph_nodes.tsv:885-889`、`graph_edges.tsv:1868-1876`已登记E02故事、迁移、Runtime/Graybox、唯一快照、权限分域、消防机包和白函两阶段。

2. 缺边：`graph_edges.tsv:1872`的E1936只让快照约束C01重构地图，没有直接约束当前`PB-V357-C01-S03.md`、`PB-V357-C01-S04.md`与`v35_5_c01_c03_state_propagation_v35_5.tsv`；`doc_registry.tsv:628-631`依赖也未列这三项。
   
   最小修法：为当前S03、S04和state propagation补节点/文档登记，并从`N_C01E02_ATOMIC_PHYSICAL_SNAPSHOT`增加三条`constrains/feeds`边；修完2.2后再把状态从pending提升。

3. 旧推荐污染：`graph_nodes.tsv:157,160`仍把合并版和旧法务单位列为`canonical/current recommended`；`graph_edges.tsv:218,288-301`中的E264、E334、E339、E340、E344、E347仍声称第一章是6回合保护战、旧场景归当前第一话且七海远控旧单位；`consistency_watchlist.tsv:17,30,53`的CW005/CW018/CW041仍把旧合并结构写成fixed current。
   
   最小修法：不删除历史图谱；统一把这些节点、边和watch项标`historical_superseded_by_v359_story_first`，取消“当前推荐/fixed current”优先级，并让V359节点成为默认入口。旧Godot实现仍可从historical边检索。

## 3. 校验器结论边界

- `scripts/canon-smoke-test.sh`当前返回`Canon smoke test passed`，但`:22-37,106-108`本身把旧场景、旧两回合开启臂/6回合实现和旧合并节点当预期答案；它只能证明历史数据仍可查询，不能证明活跃first/formal字段已迁净。
- `python3 scripts/check_v35_8_slot_loadout.py`当前返回`V35.8 strict semantic validation passed: 95 slots`，但生成器没有S03/S04连续性补丁，也没有馆守Z S02动画override；strict只能证明当前生成表相互一致，不能证明其语义符合E02原子快照。
- 两项通过均是必要回归信号，但不足以推导本席放行。完成2.1至2.5的最小迁移、重生成V35.8、补当前canon负向断言，并再次运行两项校验后，才具备改判条件。

## 4. 最终裁决

**PATCH**：不改C01E02故事正文、Runtime或Graybox；修当前地图两处权限口径、S03/S04与E04载荷承接、Canon活跃first/formal查询面、馆守Z V35.8动画预算及图谱优先级/缺边。旧封存无人机、0号开启臂和6回合实现只留historical/deprecated；兜灯、旧守护者人格、唐胶、纪存、代哥、采样贴片与路径框迁到V355 Story-First真实时序；馆守Z旧ID改为`V353U001`的deprecated alias。
