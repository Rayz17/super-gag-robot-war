# C01E02 G2-A2-C1 Current-Topology与无夹具Golden Turn目标书

日期：2026-08-20  
任务ID：`G2_A2_C1_CURRENT_TOPOLOGY_FIXTURE_FREE_GOLDEN_TURN`  
执行者：主程序-2  
状态：`DISPATCHED / PROXY_ONLY / REAL_ART_ZERO`  
上游：U86、87、88、85、84  
下游：制作人actual-frame签收 → Art Call02 → G2-A2真实scene-first收敛

## 1. 唯一任务

在保留R2C已签接触与三轮因果的前提下，完成第一轮“玩家从空草稿亲手编排”的Candidate闭环，并给current-topology精品地图生产一套唯一的投影、注册、公开态和无身份Proxy责任源。

本任务不是G2-B，不接真实美术，不改默认入口，不宣称已好玩或已完成Demo。

## 2. 必读与supersede

用绝对路径完整读取：

1. `88-c01e02-r2c-fun-first-current-topology-map-and-interaction-contract.md`
2. `87-c01e02-u86-route-a-user-approval-and-gameplay-alignment-reopen-receipt.md`
3. `85-c01e02-a4-runtime-joint-registration-and-current-object-space-correction.md`
4. `84-c01e02-r2c-c1-producer-reacceptance-and-parallel-resume-receipt.md`
5. `82-c01e02-g2-a2-visual-compositor-proxy-objective.md`
6. `00c-core-game-design-master-review.md`
7. 当前`golden_slice_profile.json`、Session、Resolver、PerformanceDirector、G2-A2 WIP与专测

88/89在本任务范围内显式supersede 81/82的旧相机、旧canvas origin、固定crop、旧A4 exact-world和fixture-only交互假设。82中独立子树、CompoundActor、局部遮挡、全屏安全区、雨湿、性能和`real_art=0`要求仍保留。

## 3. 允许写域

只允许：

- `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/golden_slice_profile.json`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/shared_round_domain/golden_slice_resolver.gd`
- `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/**`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/**`
- `game-godot/scenes/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/**`
- 专用`g2_a2_c1_*`测试、capture driver与runner
- `scripts/test_c01e02_m3_golden_slice_g2_a2_c1.sh`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c1/**`

禁止修改R2C/R2C-C1旧证据目录、默认Scene、startup、save、真实资产、Canon、角色／机体设计。现有共享工作树有大量用户与并行任务改动，全部保留；不git add/commit/clean。

## 4. 必做实现

### 4.1 第一轮路线族

- 在profile增加机器可读A/B `route_family_contract`；保留现有`planning_route`并改名义为`hero_route`或明确标记`hero_route_only`。
- 第一轮Resolver按88号端点、步数、动作／预备、朝向、连续性、2×2可放、时序与接触几何判定，不再以逐格`_route_equals`作为成功必要条件。
- 回执增加`route_family_id / route_family_valid / hero_route_exact / route_steps`。
- R2、R3判定和全部已签world result不改。
- 旧A/B fixture继续成功且world result／事件／几何不变；新增非hero但同族合法路线也成功。

### 4.2 无fixture玩家链

新增专测与实际运行链，禁止调用`load_fixture()`、`acceptance_fixture()`或直接覆写draft：

```text
PUBLIC
→ begin_planning
→ append_waypoint（含直接终点与另一条waypoint路线）
→ set_final_facing
→ set_main_action 或 set_prepared_reaction
→ open_summary
→ return_to_edit
→ undo / 重画 / 再开summary
→ 0.7s hold commit
→ PerformanceDirector自然播放
→ ROUND_RESULT
```

至少覆盖A键鼠路径、B手柄等价公共API路径、一个提交前明确非法且可修正的计划。输入设备细节可由现有root适配，但Session证据必须来自上述公开API。

### 4.3 责任预演与确定性copy

动态预演只能消费同一Resolver输出，不另写结果表。当前草稿至少显示：

- 当前形成A、B或尚未闭合；
- 保护对象、接触时点／边、责任收益、城市代价、机体热量、第二轮余量；
- A：设施damaged、路损42、热24、R2 68/1；
- B：设施active、路损24、热46、R2 88/0；
- T4/T5仍是forecast而非T3实体结果。

执行表现必须从既有结果补齐责任因果：A的完整正面冲量经旧路面传递，T5显示路损42与警戒设施受损；B的错位承接把代价留在馆守Z热量，T5显示路损24与设施保持active。不得新增外围小体的隐藏攻击意图。

逐字copy继续服从82既有合同；UI不得出现内部ID、`settle facing`英文或调试术语。目标锚点、保护区、当前身体与ghost必须在地图上真实可见。

### 4.4 current-topology与唯一投影

- 单一projection helper同时供Scene、overlay、mask、测试和capture使用；
- `canvas_origin_raw=[-1760,-340]`；动态camera/crop按85公式派生；PUBLIC/PLAN/SUMMARY共同相机按88冻结为`[-480,420]`、crop`[640,468,1280,584]`、layer top-left`[-640,-410]`，CONTACT仍使用A`[-480,450]`／B`[-500,440]`；
- `[0,0]`、`[15,11]`、`[20.5,10.5]`三个A4/source控制点0px闭合；
- 不加半格，1×1／2×2／3×3均用`footprint_bottom_center`；
- 生成机器可读`current_topology_map_contract.json`，逐项绑定current terrain zone、盾、出口、设施、保护区、炮源和所有PLAN对象；
- A4六层只作`fixture_validation_only/material_donor`，`MAP_STATE_LIGHTING.default_visible=false`，不得把旧对象带进Scene。

### 4.5 无身份Proxy Scene

建立专用非默认Scene，至少可运行：

- GF_PLAN A、GF_SUMMARY A、GF_CONTACT A；
- GF_PLAN B、GF_SUMMARY B、GF_CONTACT B；
- 公开态→编辑→摘要→执行的45–75秒第一轮连续序列；
- 当前topology地面／建筑／遮挡proxy、三条意图轨迹、路线、footprint、facing、timeline、纪存安全区、A/B责任预演；
- T3只出现微裂／少量碎屑／水花／contact FX，T4与T5只HUD forecast；
- rain/wet/reflection proxy、局部roof fade、footpoint y-sort；
- A/B结果帧能分别读出设施／路损／热量／余量差异。

几何proxy可程序绘制，但不得冒充美术或进入UA91。

## 5. 强制测试与证据

至少交：

1. JSON/profile/schema与所有source SHA校验；
2. route-family正／负例：hero A/B、直接点终点A/B、另一条合法同族A/B、错误步数／终点／朝向／动作；
3. 无fixture A/B全链与返回／撤销／重画；
4. preview与execute同Resolver token、一次提交、Full/Skip世界结果一致；
5. 20次A/B确定性；
6. R2C-C1 Swarm01、A/B post、R2动态占位、R3、音频边界非回归；
7. current topology、五组camera/crop、三控制点、1×1／2×2／3×3、pivot／socket／z／局部mask测试；
8. `00_JOINT_REGISTRATION_CONTROL`、`01_PUBLIC_SITUATION`、`02_EDITABLE_DRAFT_A`、`03_EDITABLE_DRAFT_B`、`04_COMMIT_SUMMARY_A`、`05_COMMIT_SUMMARY_B`、`06_T1_VEHICLE`、`07_T2_SWARM`、`08_T3_CONTACT_HITSTOP`、`09_T5_A_B_CONSEQUENCE_COMPARE`、`10_LOCAL_OCCLUSION_METHOD`实际1280×720 PNG及机器readback；
9. 45–75秒非headless连续序列trace，明确未调用fixture；
10. 非headless 120帧warmup＋600帧采样，记录设备、Godot、renderer、vsync、p50/p95/max、内存、纹理重复加载；
11. `approved_handoffs=[] / real_art_loaded=0 / default_entry_unchanged / save_disabled`回执；
12. `delivery-hashes.sha256`与`06-completion-report.md`。

实际截图IO不得进入性能采样窗。机器PASS只证明Candidate preflight，不证明视觉品质或好玩。

## 6. 停止条件

完成后必须停在制作人预审，不能自行恢复Art Call02、接入真实像素、改默认入口、开放UA91／G2-B或扩第二／三轮视觉。若发现必须改变A/B anchor、contact normal、socket、T1–T5、R1→R2后果或故事顺序，停止并回制作人；不得顺手迁移。
