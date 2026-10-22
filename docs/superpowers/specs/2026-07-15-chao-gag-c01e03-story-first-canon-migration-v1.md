# C01E03 Story-First Canon Migration v1

> Status: `canon_migration_applied_validated`
>
> Scope: `C01E03 -> C01E04 / V357-C01-S03 -> S04`
>
> Reconstruction source: `V35.9/rebuild/episodes/C01/C01E03-断臂成桥-v1.md`

## 1. Reason

旧候选层已经给出“馆守Z断臂成桥、豪司越权、白函具身、B1被封”，但没有形成可供故事、玩法、资产和下游共同读取的唯一事实；同时V31第三话的“审批锤、金章承力印机、责任签名矩阵”仍在Canon和图谱中保持活跃，容易覆盖当前巨物救援。具体问题有六项：

1. E02继承的五名馆内人员与豪司后入场混在一起，旧约束“不得生成第六人”会错误禁止有来源的现场峰值六人。
2. 馆守Z右臂可能在“连接、飞出、仍可修、主动切离、旧址成桥”之间跳态，失败重试也可能把半套断臂写进跨话状态。
3. 勇拳、豪司和白函缺少准确生命周期：勇拳不是社勇王人格，豪司不是远程支援，白函也不是无身体UI。
4. 两项战术选择只有标签，没有后续消费者；旧制作表无法回答玩家究竟操作了什么。
5. E04只收到四个抽象增量，可能自动修复供水、风道、档案冷却、消防机腿伤，或把右臂与人员装进展舰货舱。
6. V31责任签名战仍能从默认图谱查询进入当前第一章，造成两套互斥第三话并存。

## 2. Applied Changes

| Migration | Change | Canon level | Downstream lock |
|---|---|---|---|
| `C01MIG013` / `V358MIG051` | E03只读E02原子快照；继承五人全部在L2，豪司随后从西门进入L1，现场峰值六人但过桥恒为五人。三类失败只回本地检查点；仅`RT035`一次提交27键 | accepted and validated | E04只读E03原子快照；禁止无来源第六名继承人员、第六过桥者、半套持久断臂或人口回刷 |
| `C01MIG014` / `V358MIG052` | 馆守Z首次2x2受限控制并永久失右臂；勇拳由豪司本人实名驾驶，仅承梁/推梁，战后企业回收并剥离数据；白函首次具身、占格、切图、承伤并带右肩/内收索伤撤离 | accepted and validated | 社勇王真机不提前；勇拳不入万机馆；白函伤痕和单一样本必须跨话保留；右臂不可装载或无损恢复 |
| `C01MIG015` / `V358MIG053` | V31第三话“审批锤许可端、金章承力印机、支援封锁框、责任签名矩阵、右肩临时通道”整体降为历史创意来源，不再作为当前C01E03场景、首登、玩法或下游状态 | accepted and validated | 当前第三话默认入口只指向《断臂成桥》Episode、Runtime、Graybox、Asset和验收回执；旧节点只允许显式历史查询 |

## 3. Unique E03 End Snapshot

只有五人和两件设备安全、白函撤离、勇拳企业回收、善后完成、B1六锚物理落锁全部成立时，`RT035`才一次写入以下精确集合：

```text
GZ_RIGHT_ARM_LOST=TRUE
GZ_CONTROL_STATE=FIRST_CONTROL_COMPLETE_SINGLE_ARM
GZ_RIGHT_ARM_LOCATION=OLD_SITE_L1_L2_COMPOSITE_BRIDGE
GZ_RIGHT_ARM_CARGO=FORBIDDEN
HAOSI_CORP_PUNISHMENT=ACTIVE
BRAVE_FIST_RECOVERY=CORPORATE_COMPLETE
BRAVE_FIST_DATA=STRIPPED
BRAVE_FIST_PROTOTYPE=RECOVERED_BY_CORPORATE
JICUN_MEMORY_FRAGMENT_00=ACQUIRED_LOW_CONFIDENCE
INDEX_DAMAGE_AS_FUNCTION_SAMPLE=ACQUIRED_BY_BAIHAN_SINGLE_LOCAL_SAMPLE
BAIHAN_RIGHT_SHOULDER=CRACKED
BAIHAN_INNER_RETRACTOR=SEVERED
E03_INHERITED_INSIDE_HUMANS=5
HAOSI_POST_SNAPSHOT_ENTRY=1
PEAK_ONSITE_HUMANS=6
BRIDGE_EVAC_HUMANS=5
FIVE_INSIDE_HUMANS=SAFE
HAOSI_SAFE_EXIT=TRUE
PEOPLE_CARGO=FORBIDDEN
B1_MOVING_SPINE=PHYSICALLY_LOCKED_BY_MILITARY
E03_ATOMIC_COMMIT=COMPLETE_AFTER_SIX_ANCHORS
C01_OUTSIDE_EVACUEES=29
E03_FIRE_HANDOFF_CARGO=2_SAFE
FIRE_SUPPLY_BURNED=TRUE
COMMERCIAL_DUCT_DAMAGE=LOCAL_BURNED_HEAT_LEAK
ARCHIVE_MAIN_VAULT_COOLING=EMERGENCY_LOW_PRESSURE_ACTIVE
FIRE_BRIDGE_LEFT_FRONT_LEG=OVERLOAD_PERSISTENT
```

`RT036`只读该集合。结构、探索或切后失败分别回到`SETUP_LOCAL`、`EXPLORE_ENTRY_LOCAL`、`POSTCUT_LOCAL`，不得写任何上述键。

## 4. Runtime And Production Contract

- 地图采用L1/L2双平面、16x12区域Graybox。白函第一脚废止旧楼梯；复合桥是随后唯一L2到L1的单向边。
- 馆守Z固定2x2、零平移、零转向，只执行抬肩、一次滑轨冲击和桥开放前的左臂锁定；过桥期间左臂只等长承力。
- 次梁足迹为`L1(4..12,9)`；勇拳从`L1(3,9)`一步接触`L1(4,9)`，SEG3固定接触`L1(12,9)`。载荷Owner严格按`SEG3 -> SEG3+勇拳 -> 勇拳 -> 勇拳/SEG3关节自由 -> 勇拳/右臂落槽`交接。
- 五次结构钟固定在肩部、勇拳固定、通道响应、载荷交接、滑轨冲击之后。跌跌/机器犬优先路线必须由另一角色在T5后补位；拖到T6回`SETUP_LOCAL`。
- 上层设备路线让标尺瞄准货物夹具、唐胶拨尺并预置低压泵；下层人员路线让标尺瞄准人员缓冲边缘、跌跌挡尺并提供一次失足恢复。它们分别形成20、21或23 Tick过桥序列。
- 身体记忆只给隐藏隔板位置；短短长敲击、勇拳载荷居中、跌跌垫片绿色三项同时Ready才验证第四筋。缺项预览不耗时，强制错误回探索入口。
- 右臂使用五态资产：连接、托槽、悬置可修、复合桥、旧址永久桥。白函是唯一完整新Boss身体；勇拳、馆守Z、SEG3只做有限动作/状态。

## 5. Character, Mecha And Mystery Boundaries

- 纪存拒绝只认自己声纹的`FULL_SHOULDER_ACTUATION`，用公开测量与分工完成破局；低置信记忆不能证明来源，也不能替他作决定。
- 七海仍被停权，只能通过普通电话确认纪存与五人是否回来；她没有远程解锁、写系统或替现场决策。
- 兜灯在确认右臂仍可修后亲手切断主筋；唐胶托刀而不抢刀，战后两人先处理人的手和机器断口。
- 豪司本人到场、实名承担、驾驶无人格勇拳承梁；本话不把越权自动奖励成入队机体。
- 白函只稳定带走一个局部样本`DAMAGED_BODY_TO_SUPPORT_FUNCTION`，不能提前学会人命优先、统一最优机器规则或索引人格。
- B1六处旧对位痕只暴露巨型位移达到外部阈值；军方据此物理锁死移动脊柱。旧图来源、0号和完整馆体真相仍不解释。

## 6. Data And Source Updates

本迁移更新或登记：

- `data/canon/entities.tsv`
- `data/canon/scenes.tsv`
- `data/story/v35_5_c01_c03_state_propagation_v35_5.tsv`
- `data/story/v35_5_c01_c03_slot_episode_mapping_v35_5.tsv`
- `data/story/v35_5_c01_c03_mecha_exposure_v35_5.tsv`
- `data/story/v35_5_c01_c03_enemy_asset_budget_v35_5.tsv`
- `scripts/build_v35_8_slot_loadout.py`及V35.8生成表
- `V35.9/rebuild/maps/C01-逐章重构地图-v1.md`
- `V35.9/rebuild/README.md`及三张重构账本
- `data/design_graph/doc_registry.tsv / graph_nodes.tsv / graph_edges.tsv / consistency_watchlist.tsv`

历史Reader、旧V31稿、旧Pressure Board和早期审稿回执不回写；它们保留为创意与问题证据，不得覆盖当前Episode。

## 7. Validation Requirements

放行C01E03前必须同时满足：

1. `check_c01e03_runtime_graybox.py`验证47行状态图、五次结构钟、两组选择消费者、梁几何、探索离散输入、20/21/23桥面预算、三类失败重入和精确27键。
2. 原Gameplay/Production席不依赖检查器结论，独立纸演并给出PASS。
3. V35.8生成器和strict检查采用有来源峰值六人/桥上五人语义，并写入馆守Z、勇拳、消防机、小机、白函的真实动作与资产边界。
4. Canon查询默认返回当前Episode；V31审批锤/签名链只作历史来源；E04唯一继承E03原子快照。
5. Canon smoke、Godot strict、目标TSV结构、图谱引用和缓存审计通过。
6. 原Canon/宏观谜团/物理席独立复核并给出PASS；随后才能写最终放行回执。

## 8. Current Validation State

- Story / Audience：总编、机体/IP、人物/关系三席已在`11`、`12`、`09`号回执给出PASS。
- Runtime / Graybox：`14-runtime-graybox-paper-run-r2.md`与`check_c01e03_runtime_graybox.py`本地主控通过。
- Gameplay / Production：`15-gameplay-production-final-recheck-r3.md`独立判定PASS，`GPR2-01..07`全部关闭。
- Canon / 宏观谜团 / 物理连续性：独立席`17-canon-macro-physical-final-recheck-r4.md`确认迁移本体、人口、生命周期、桥体和谜团边界均已闭合，唯一阻断为smoke脚本仍匹配旧措辞；该断言已改为现行Canon稳定字段。随后四项实跑全部通过：V35.8 strict 95槽、E03 Runtime/Graybox、Canon smoke、Godot strict。
- 最终放行：见`V35.9/rebuild/reviews/C01E03/18-final-acceptance.md`。

## 9. Godot Candidate Mapping Update (2026-07-16)

现行候选运行包已将四节点Episode、八阶段断臂桥战、RT035唯一提交和C01连续Runner接入Godot。P6不再由八个战棋菜单命令替代探索：P5在`EXPLORE_ENTRY_LOCAL`暂停外层Session，推入馆守Z右前臂的人尺度Spatial；玩家排除三条假筋，记忆只定位门，再读取唐胶、勇拳、跌跌三项独立外部输入。成功后八项合同回执原子写回同一Session并进入P7；误判只重置P6，存档同时恢复外层战局与内层位置/证据。

该映射已经过自动回归和四帧视觉检查，详见`2026-07-16-chao-gag-c01e03-godot-embedded-spatial-evidence-v1.md`。它仍是`candidate_runtime_mapping`：不得据此宣称47行Runtime逐项Parity、正式美术、真人容量或平台验收完成。

同日第二轮地图交互把P4勇拳预接触一格移动、P5白函主框目标选择、P7正确/错误切筋点、五组人货四段清桥和八阶段白函结构意图接入同一Session；目标选择、桥中占用、取消和存档恢复均有自动与视觉证据。P1/P3及部分P4仍保留紧凑的专业动作命令，正式敌方Hazard动画、真人容量和平台验收仍未完成。
