# C01 Current Demo 战斗地图精灵生产矩阵 v1

> 状态：`CURRENT_PRODUCTION_PLAN / FAIL_CLOSED / GZ_CML131_E02_E04_LINEAGE_LOCKED / GZ_V10X_IDLE_EAST_SOUTH_AND_SHIELD_BLOCK_SOUTH_REVIEW_ONLY / BREAKER_A38_IDLE_WEST_REVIEW_ONLY / BREAKER_A36_A37_FAIL_STOP_HISTORY_LOCKED / BRAVE_FIST_A33_SOURCE_SYNCED_A35_AND_OVERLOAD_REVIEW_ONLY`  
> 范围：C01E02、C01E03 地面地图，C01E03/E04 组合演出槽，C01E04 空战双 View  
> 不构成：美术通过、用户实际帧签收、Runtime/Default/Canon 迁移

## 结论

这份矩阵是 C01 Demo 地图美术的唯一生产清单，不另造一套程序 pose 真相：

- 地面消费者继续使用已有 `subject + action + facing` exact 合约。
- BREAKER 的 world facing 与 presentation visual facing 已分层：事件演出可显式请求正确 cardinal，但绝不回写 Resolver/Session world truth。
- E03 五个原 `PLANNED_WIRING_GAP` 已接入事件级 exact request：馆守 Z 的 `south_drill_block/north`、`autonomous_overload_rocket_fist/north`、`right_arm_destroyed/north`，以及 BREAKER 的 `drill_tell/north`、`red_slit_open/north`。精确图不存在时只显示 marker，不绑定 idle 或任何其他姿态。
- 地面地图、E02/E03 控制器与组合演出共同读取当前 `CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE` 合同；生产行统一使用 `map_dimetric_40x24`（tile half `40,24`），旧 40×20 只属被 Task111 取代的预生产历史。
- E04 继续使用已有 `subject + source_event_id + action_id` exact 合约。
- 矩阵只把现有消费者请求、Reader/roster 形态和正向设计源对齐；没有绘图，也没有把缺图伪装成已完成。

`c01-map-sprite-production-matrix-v1.tsv` 是人工可维护权威；`c01-map-sprite-production-matrix-v1.json` 只由检查脚本机械生成，不得单独手改。

## 当前数量

| 状态 | 行数 | 含义 |
|---|---:|---|
| `REUSABLE_CURRENT` | 13 | 精确路径/SHA 真正可被当前消费者读取；BREAKER 保留实际事件合法的 `idle/charge/contact north` exact 行，不将 north 扩到 west 事件 |
| `USER_ACCEPTED_CAMERA_V2_CARDINAL_BASE` | 2 | 未改字节的馆守 Z V10X north/west 中立基础；只登记库存并保持 `texture_load=false` |
| `ALPHA_REPAIRED_CANDIDATE_PENDING_USER_VISUAL_REVIEW` | 2 | east/south 保留已确认的设计和注册，仅修复封闭负空间的 Alpha；当前为 Candidate-only exact binding，新字节待实际帧重新目视签收 |
| `USER_ACCEPTED_DESIGN_ONLY` | 53 | 身份或道具设计已确认，但 exact 镜头/动作/朝向精灵不存在；勇拳真实 R4 入场 `idle/east` 缺图行仍不构成地图精灵批准 |
| `MISSING_ART` | 15 | 连可接入的精确形态母图都还没有，主要是 BREAKER 飞行核心 |
| `CANDIDATE_NOT_APPROVED` | 4 | 含未绑定的 brace east/south Alpha 修复候选与万机馆两个 View；都不得伪报成用户批准 |
| `CANDIDATE_AWAITING_USER` | 7 | 馆守 Z V10X `shield_block/south`、BREAKER A38 `idle/west`、勇拳 A35 四态审核库存，以及勇拳 `return_overload_fist/south` 实机待签收图；全部 `texture_load=false`，不得提前接入 |
| `FORBIDDEN_HISTORY` | 31 | 只作失败追溯；除既有禁用源外，显式锁定 BREAKER A30/A32、Call03、初版反向 north、GF 双头失败、旧 B+X、旧 GUIDE V2、A36 Call01 与 A37 Blender 首渲四张 PNG，路径或 SHA 回到正向链即失败 |

总计 127 行：89 行当前需求，38 行参考清单（含 2 个未伪造消费者的馆守 Z N/W 四向基础、1 个勇拳 A33 正向身份库存、4 个 A35 待用户四态与 31 个 History 禁用源）。当前需求中仍只有 15 行可在 Candidate 边界中精确读取（4 个唯一源）；其余 74 行合并为 43 个待生产或待签收输出。新增的 `E03_BF_IDLE_E` 明确记录真实 R4 入场缺口，防止 north 图被错当成 east。

## 已纠正的旧资产回流

- 馆守 Z 旧 `guardian_z_east_camera_v2_candidate.png` 已从 `bindings` 和 `pose_bindings.idle/east` 活动表中解绑。文件未删除，只在 `history_unbound_sources` 中以 `FORBIDDEN_HISTORY + texture_load=false` 留追溯。
- 馆守 Z 当前唯一正向身份母图是 V10X：E02 查询 CML130，整个 C01 Current Demo 的 E02–E04 必须同时查询 CML131。CML131 只扩展视觉血统与阶段连续性，不批准任何具体 Sprite；V10X 原图仍是 `design_orthographic` 派生父项，不是 Camera V2 地图精灵。
- 用户于 2026-08-24 对 Call01 的 V10X 设计方向、Camera V2 40×24、pivot/2×2/scale 与实际地图尺寸脚点回复“这个通过”。后续又明确指出 E/S 封闭负空间仍有白底未透明，因此 E/S 仅保留方向认可，新 Alpha 字节降回 `CANDIDATE_VISUAL_REVIEW_ONLY`，待新实际帧签收；N/W 字节未变且只登记库存。没有建立 base binding，也没有打开 Runtime、Default 或 Canon。
- A17 只是用户确认的重盾设计基底；盾正面/外侧朝敌，双手和握把在背面/内侧。它不能单独冒充馆守 Z 持盾复合 pose。
- 馆守 Z V10X `shield_block/south` 的 Alpha 修复 Candidate 与一张 test-only Godot 实际地图帧已经存在：正面盾面与机体面向同向、正面可见手为 0，旧馆守 Z 资源未被缓存或接入；但握把接触被盾体遮挡，仍需用户目视判断，故只登记为 `CANDIDATE_AWAITING_USER + texture_load=false`。
- 勇拳当前唯一正向身份源仍是用户认可的 A33 重拳／虎鬓冠基底。`return_overload_fist/south` 已有一张从 A33 独立派生、经 Alpha/尺寸机检和内存态 Godot 实机验证的 Candidate，但实机中主拳与目标尾部仍有空间分离、副拳读法偏弱，因此仍是 `texture_load=false / user=false`。R4 字面入场是 `idle/east`，R5/R6 的 `idle/south` 只属于非动作快照；R4 回送、R5 连打、R6 接力分别请求 `rear_impact_return/north`、`north_return_strikes/south`、`return_overload_fist/south`，不可用 idle 或 north 图代替。
- A35 最终四态中的 00、01、02R1、03 只登记为 `CANDIDATE_AWAITING_USER`。A13 旧指针、A26 单侧长粗臂拒绝稿、A34 初版长筒 State02、护盾环 State03 以及左拳连接遮挡的 State03 R1 均为 `FORBIDDEN_HISTORY`，不得作为正向像素、结构或姿态来源。
- 失败的 A16 east Camera V2 稿继续保持 `FORBIDDEN_HISTORY`，不得回用。
- BREAKER 当前只有 north 母图可加载；A38 已有一张真实 Runner 的 R3 E1 test-only 实机帧，能证明 `idle/west`、3×3、pivot、零旋转／零翻转以及 A37／旧稿零加载，但中央背甲连续性和地图观感仍待用户实际像素裁决，因此矩阵继续登记为 `CANDIDATE_AWAITING_USER + texture_load=false`。`idle/charge/contact north` 作为实际 R1 方向的显式 exact 行继续加载；`red_beam/hit_recoil north` 已解绑，R2/R3 缺图时只显示 marker 并回执 `missing_exact_breaker_facing_pose`。
- BREAKER A30 east raw、A32 west raw、旧 Call03、初版反向 north、GF 双头对称失败、旧 B+X 板、旧 GUIDE V2 384、A36 Call01 raw 与 A37 Blender 首渲四张 PNG 均只登记为 `FORBIDDEN_HISTORY + texture_load=false`。A37 是被用户中止的误路，同时 north 朝向约偏 15.98°且低模身份失败；不构成 Candidate，不填补任何 BREAKER 多朝向需求。
- 多朝向生产只允许“同一已确认 2D 身份母版下逐向、逐状态独立绘制”；不得再把方向一致性转换成 Blender／Three.js／Python 建模或共享 3D 转台。Python 只允许 Alpha、尺寸、pivot／footprint、QA 与 hash。
- 万机馆仍是两个待图槽：战略全景是 130–160m 真实比例世界主体；局部空战是裁切背景。两个 View 共享同一世界快照，但绝不复活旧舰体图。

## P0 美术生产队列

1. **P0-A｜BREAKER Wave A 四向中立**：`idle/north` 已有并可加载；A38 `idle/west` 已完成 test-only 实机帧但仍等待用户实际像素签收，不可加载；`idle/east|south` 尚缺。各方向共享同一设计母版与注册规范，但必须独立 2D 绘制，禁止镜像／旋转／3D 转台。
2. **P0-B｜BREAKER Wave B 实际事件动作**：五个键是 `charge/north`、`contact/north`、`red_beam/west`、`hit_recoil/west`、`fist_caught/south`。前两个使用当前 north 地图体的显式 exact 行已可消费；本轮真正缺失的新输出是 west red beam、west recoil 和 south fist-caught。R3 面向 west，但位移 `[0,+2]` 仍按 south 投影。
3. **P0-C｜C01E02 馆守 Z，2 个 brace + 1 个 block 待签收，3 个持盾输出缺失**：`idle E/S` 已以 Alpha 修复 Candidate exact 接入并待新实际帧签收；`brace E/S` 已有同样修复的未绑定候选；`shield_block/south` 已有 V10X + A17 独立 Candidate 与 test-only 实机帧，但用户未签收；仍缺 `shield_take/hold/bash S`。只用 CML130／CML131 的 V10X 身份父图；持盾行叠加 A17 正反面结构。
4. **P0-D｜C01E03 地面延展**：馆守 Z 必须遵守 CML131：过载前保持 V10X 双臂身份，过载后独立制作原右拳与完整前臂毁损态，不能回流 CML008 旧图或用完整态改标签。`idle/south` 只用于 R5/R6 非动作快照，不再冒充连打或接力；R4 字面入场另列 `idle/east`，不得拿 north 冒充。馆守 Z 三个事件态与 BREAKER 两个 R5 状态已是 active exact request，但仍全部缺图并 fail-closed；勇拳另有三个独立缺图门：`rear_impact_return/north`、`north_return_strikes/south`、`return_overload_fist/south`。勇拳只允许从 A33 身份基底重新制图；A35 四态在用户批准前不能直接派生 Camera V2 或动作 Sprite。馆守 Z、勇拳与 BREAKER 其余已列行保持 fail-closed。
5. **P0-E｜组合演出，6 个 hero-cut pose**：E03 的 `OVERLOAD_FIST / RELAY_PUNCH / FIST_CAUGHT`，E04 的 `RETURN_DIVE / CORE_APERTURE_OPEN / LEFT_CORE_PUNCH`。不得把 256/384 地图精灵放大冒充。
6. **P0-F｜E04 空战，9 个 round/action master + 39 个 exact binding key**：馆守 Z、勇拳、BREAKER 飞行核心各 3 个 round/action master。同一 `planned_output_id` 可在同回合事件中显式复用，但 39 个 event/action 键必须逐行绑定，不得依赖上一 pose、镜像或事件 fallback。
7. **P0-STOP｜万机馆 2 个 View 暂不生产最终精灵**：先等当前“现代机器人博物馆 + 战舰/大型游艇/飞船 + 非五官头冠天线群 + 可见武装”设计稿获用户确认，再做战略主体和战术背景。

每个包的停点都是：Section 2 出图 → 程序 exact 绑定 → 实际地图帧 → 用户目视确认。机器 PASS 不代替最后一步。

## 检查

```bash
python3 scripts/check_c01_map_sprite_production_matrix.py --self-test --write-json
```

检查会：

- 验证 TSV 行唯一性、状态、来源文件和 SHA；
- 验证 CML131 在 Canon authority 中保持 `hard/active`，并核对馆守 Z E02 完整双臂、E03 过载前／后、E04 巡展臂装四个阶段都锁定 V10X 2D 血统与 `NO_BLENDER / NO_THREEJS / NO_PYTHON_MODELING`；
- 从 E03/E04 profile、E04 dual-view contract 和现有 exact binding 中复核消费者请求全集；
- 直接读取当前 40×24 Camera V2 合同，并确认 GroundMap、E02、E03、Composed 四个运行时消费者及所有相关矩阵行与其一致；
- 拒绝任何 `FORBIDDEN_HISTORY` 路径/SHA 重回 active binding；
- 强制上述 12 个 BREAKER 禁用源按真实 path/SHA 各登记一次，并以负向自测分别验证 A36/A37 path 与 A30 SHA 无法进入 active binding；
- 强制勇拳所有当前需求只引用 A33 正向身份基底，并保证 A35 00/01/02R1/03 只以 `CANDIDATE_AWAITING_USER + texture_load=false` 登记；
- 拒绝缺行、旧 pose 继承、镜像/跨朝向/通用主体 fallback；
- 验证 E02/E03 共28个 BREAKER 事件的 presentation-facing 审计，固定 R2 `red_beam/west`、R3 `hit_recoil/west` 与 R6 `fist_caught/toward GZ source`，并强制多源/垂直事件保留 semantic gap；
- 拒绝把 `USER_ACCEPTED_DESIGN_ONLY`、`CANDIDATE_NOT_APPROVED`、`CANDIDATE_AWAITING_USER` 或“有矩阵行”伪报成已签收美术；只有 `V353U001|idle|east` 与 `V353U001|idle|south` 两个 Alpha 修复 exact consumer 可在 Candidate 边界内设 `texture_load=true`，但 `user_visual_acceptance=false`；north/west、brace、盾态、勇拳四态与 E03 其余输出均继续 fail-closed。
