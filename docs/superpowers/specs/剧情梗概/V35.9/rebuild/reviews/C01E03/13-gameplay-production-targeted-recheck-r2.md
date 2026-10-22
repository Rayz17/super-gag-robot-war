# C01E03 Gameplay / Production 定向独立复验 r2

> Review seat: original SRPG gameplay director / production designer
>
> Review object: 当前`C01E03-断臂成桥-v1.md`及E03 Runtime / Graybox / Asset生产包
>
> Prior finding set: `GPR1-01..08`
>
> Checker run: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_c01e03_runtime_graybox.py` -> exit `0`
>
> Independent ruling: `PATCH`
>
> Production gate: `REMAINS_BLOCKED_BEFORE_RUNTIME_GRAYBOX`
>
> Write boundary: 本文只做原Gameplay/Production席复验，不修改Episode、TSV、检查器、Canon或其他审稿文件。

## 一、发现（按严重度排序）

### [P0] `GPR2-01_ROLLBACK_DEAD_ENDS`：三类回滚有文字目标，却都落在没有后继的死状态；切后重试还未保证恢复左臂锁定

**证据**

- Runtime的三条失败行分别结束于`RETRY_LOCAL_NO_PERSISTENCE`、`EXPLORE_RETRY_LOCAL`、`POSTCUT_RETRY_LOCAL`（`C01E03-runtime-contract-v1.tsv` L38-L40）；39条Runtime中没有任何一行以这三个状态为`start_state`。
- Graybox声明四个检查点为`SETUP_LOCAL / EXPLORE_ENTRY_LOCAL / PRECUT_LOCAL / POSTCUT_LOCAL`（`C01E03-graybox-constants-v1.tsv` L24），但Runtime没有创建`SETUP_LOCAL`的行；`RT037`所谓“回到最近Setup”因此没有可到达的目标节点。
- `RT024`结束态为`ARM_CUT_COMPOSITE_BRIDGE_ACTIVE_LEFT_BLOCK_LOCKED`，`RT025`却从较弱的`ARM_CUT_COMPOSITE_BRIDGE_ACTIVE`开始（Runtime L25-L26）；`RT039`回滚内容只写右臂已切、五人/货物归位和桥面清空，没有恢复`GZ_left_arm_block_locked`（L40）。若按合同字段实现，切后失败后`RT030`要求的`PRELOCKED_LEFT_ARM`可能不再成立。
- Episode明说三类本地点只保存战斗内态并回最近本地点（正文L357-L359）；纸演也声称失败后可立即继续（`10-runtime-graybox-paper-run-r1.md` L62-L74），但这些继续边在TSV中不存在。
- 检查器的回滚验证只查三行含`no_persistent`且动作名不含`COMMIT`（检查器L200-L213），没有验证失败`end_state`是否等于某个真实检查点、是否存在后继，或左臂锁定位是否恢复。

**独立反例**

强制两件设备同时上桥触发`RT039`后，状态成为`POSTCUT_RETRY_LOCAL`。因为`RT026`只接受`POSTCUT_LOCAL`，且没有`POSTCUT_RETRY_LOCAL -> POSTCUT_LOCAL`转换，玩家无法重新开始唐胶过桥，也没有新的失败或退出动作，形成零行动软锁。探索失败和切前失败同理。

**最小可执行修法**

1. 在Runtime中建立一次真实的`SETUP_LOCAL`，并让`RT037`结束于一个确定检查点；若切前失败需要两个目标，按失败发生段拆成确定映射，不能用“nearest”隐藏分支。
2. 令`RT038.end_state=EXPLORE_ENTRY_LOCAL`、`RT039.end_state=POSTCUT_LOCAL`，并在`RT039.mandatory_outcome`显式恢复`LEFT_BLOCK_LOCKED / bridge_closed_then_reopen_allowed / five_L2 / cargo2_L2`。
3. 统一`RT024 -> RT025`的复合状态，保证左臂锁定不因创建检查点被降级。
4. 检查器建立Runtime状态图，断言三条失败边的终点都有合法后继，并实际从每个回滚点跑到`RT035`。

### [P0] `GPR2-02_ATOMIC_PAYLOAD_UNBOUND`：唯一提交行存在，但没有绑定Episode的精确21个状态键，且提交后的只读断言状态名不连续

**证据**

- Episode结算明确列出21个键，从`GZ_RIGHT_ARM_LOST`到`E03_ATOMIC_COMMIT`（正文L381-L404）。
- 唯一提交`RT035`只用`GZ_single_arm / right_arm_old_site_bridge / Haosi_safe`等自然语言近义词概括结果，没有写入上述任何一个精确`KEY=VALUE`（Runtime L36）。独立逐键比对结果为21/21均未在`RT035`出现。
- `RT035.end_state`写成`C01E03_ATOMIC_TRANSACTION=COMMITTED`，`RT036.start_state`却是`C01E03_ATOMIC_TRANSACTION_COMMITTED`（Runtime L36-L37）；按精确状态机，两行不相接。
- 检查器只确认`ATOMIC_SNAPSHOT`相位恰有一行、Graybox五个Guard字符串存在，以及`RT036`含`NO_WRITE`（检查器L200-L213）；后面的Episode对齐只检查七个词出现在Markdown正文，不检查它们由`RT035`提交（L242-L252）。

**风险**

实现方可以让检查器全绿，却漏写豪司处罚、勇拳数据剥离、右臂禁止装载、白函两处精确伤痕、纪存记忆或人口键。E04随后只能重新拼读Episode prose，违背单一原子输入，也可能因`RT035/036`状态别名无法执行成功断言。

**最小可执行修法**

1. 在`RT035.mandatory_outcome`或独立快照表中逐项写出正文L383-L403的精确键值；保留伤痕继承项的精确枚举，不用近义短语替代。
2. 统一`RT035.end_state`与`RT036.start_state`为同一个字面状态。
3. 检查器从Episode结算段读取预期键集，与原子提交键集做`exactly once + no missing + no extra conflicting value`比较，并确认失败行不可写这些键。

### [P1] `GPR2-03_PHASE_AND_STRUCTURE_CLOCK`：P6/P7压力钟可求和，P1-P5结构钟仍未进入Runtime，八阶段编号也与Episode顺序错位

**证据**

- Episode阶段顺序是`P1占岗 -> P2切区选择 -> P3勇拳介入 -> P4换载`（正文L320-L325）。Runtime却在`RT007-008`先执行`P3_ENTRY/P3_BRAVE`，到`RT009`才执行`P2_CHOICE`（Runtime L8-L10）。
- Graybox定义`STRUCTURE_TICK_LIMIT=6`、热风道、档案抽水和白函敌方相位（Graybox L19），但39条Runtime中`STRUCTURE_TICK`出现次数为0；没有哪一个玩家动作或敌方相位实际推进这只钟。
- Runtime只明确给馆守Z两次动作各`heat_plus1/displacement_plus1`（L6、L18）。纸演据此直接判定总量2/2安全（纸演L21-L31），完全没有结算Graybox所称热风道、档案抽水和白函内收。
- 检查器没有验证Runtime相位单调顺序、结构Tick消费、敌方相位次数或阈值；它只通过常量/字符串存在性间接宣布Agency与其他子项PASS。

**风险**

程序若按Runtime实现，P1-P5没有时限，白函不会按结构钟行动；若按Graybox自行补每行动一Tick，则P4四项Owner确认加五步换载会远超6 Tick。两种实现都与纸演不同，无法证明两条支援路线可通关。

**最小可执行修法**

1. 统一八阶段顺序。最低改动是把`RT009`移到豪司介入前，或将Episode/Runtime的阶段号统一成同一条顺序；不能保留`P1 -> P3 -> P2`。
2. 指定`STRUCTURE_TICK`只在哪些原子节点增加，例如每个完整玩家回合或指定的P1-P5阶段出口，并列出对应白函动作、热/位移变化和失败阈值。
3. 将两种支援选择的资源修正写入这些Tick行；检查器对两路逐Tick求和，而不是只比较馆守Z的2/2动作量与静态余量。

### [P1] `GPR2-04_CHOICES_NOT_CONSUMED`：两项选择有枚举，没有下游消费者；桥面成功路线固定为7动作，人员容错、设备折扣和标尺机意图均不可执行

**证据**

- `RT004`写出跌跌/机器犬两路余量（Runtime L5），但从`RT005`起不再出现`DIEDIE_PAD / DOG_HOSE / heat_margin / displacement_margin`任何一个分支标记；两路执行完全相同的后续动作。
- `RT009`声明设备路减1个货运动作、人员路获得一次错位恢复并增加1 Tick，标尺机目标也改变（L10）；从`RT010`起没有任何Runtime行读取`UPPER_EQUIPMENT / LOWER_PERSON / person_misstep / cargo_action_discount`。
- 撤离`RT026-030`的固定成本恒为`1+2+2+1+1=7`，五行均无通道分支（Runtime L27-L31）。Graybox则只在常量里额外写`LOWER_PERSON_extra1=8`（L21），没有“人员错位”动作、恢复边、设备折扣应用点或两种标尺机目标。
- 单个人员动作直接以`CROSS_L2_TO_L1_THREE_SEGMENTS_COST1`跨完整三段（Runtime L27）；因此玩家没有停在某一桥段的合法状态，正文所谓“错误格”和`person_misstep1`也无从发生。
- 纸演四组合表只是把上层路线记为7/8、下层路线记为8/8并宣称意图不同（纸演L51-L60），没有执行任一条分支专属动作。检查器的Agency验证也只查两个枚举和`both routes`字符串（检查器L180-L191）。

**风险**

支援选择目前只改变UI标签；通道选择对无失误玩家而言是“7 Tick”严格优于“8 Tick”，人员路承诺的容错无法使用。玩家agency仍是假选择，三段桥也可能退化为五次剧情按钮。

**最小可执行修法**

1. 为支援选择增加真实消费者：指定哪些结构Tick由垫片减少位移、哪些由软管减少热量，并让两路触发不同但可恢复的预警/动作窗口。
2. 为通道选择增加分支动作：设备路明确把哪一枚`cargo+worker`从2降为1；人员路增加一次可确认的`MISSTEP_RECOVER_COST1`，并定义其前后桥段、占格和恢复状态；两种标尺机意图必须有目标与结算差异。
3. 若要保留三段桥作为玩法，人员移动需产生至少入口/中段/出口占格回执；若坚持一键整桥，就删除错误格、人员错位和逐段调度的玩法承诺，并另补第二项真实选择。
4. 检查器实际遍历四个选择组合，并至少强制一次设备折扣、一次人员错位恢复和两种标尺机意图，不得以`both routes`字符串代替可达性。

### [P1] `GPR2-05_HANDOFF_GEOMETRY_UNPROVED`：换载时序已经无`Owner=None`，但Graybox没有次梁足迹或两个接触点，无法证明勇拳在受限移动内真的能接到SEG3所托的同一根梁

**证据**

- FireBridge Rig固定在L1 `(12..13,9..10)`，四足不能移动（Graybox L10）；勇拳锚位在L1 `(3..4,9..10)`，接触前最多平移1、接触后平移0（L11）。
- `GB011`只用状态串声明`SEG3 -> both -> Brave`，没有`SECONDARY_BEAM`的格位/跨度、`SEG3_CONTACT_CELL`或`BRAVE_CONTACT_CELL`（L12）。Runtime同样只有Owner文字，没有几何接触回执（L13-L17）。
- 检查器的换载验证只检查五行顺序、标记字符串和“zero/never owner NONE”（检查器L127-L143），不读取任何坐标或可达距离。

**风险**

当前坐标允许一种合法读法：勇拳距SEG3八格以上且只能移动一格，但次梁未定义为跨到勇拳锚位；Owner可在文本中转移，画面上却没有接触。程序或关卡师必须自行发明梁长度与接触位置，物理软锁仍未被生产合同排除。

**最小可执行修法**

在Graybox补`SECONDARY_BEAM`足迹及两个具名接触格/接触区，断言勇拳从入场格在`translation_before_contact<=1`内可达其接触点，SEG3初始托点属于同一梁，且SEG3关节转位不改变四足。检查器应计算这两个接触关系，再验证Owner链。

### [P1] `GPR2-06_HYBRID_FAILURE_NOT_DEFINED`：探索成功路线可求和，但“第四Tick校验失配”没有可选择的对齐状态；失败只存在于结论句

**证据**

- `RT020-022`锁定三次可见检查、零Tick记忆和一次公开验证，4/4成功路线本身清楚（Runtime L21-L23；Graybox L20、L22）。
- `RT022`又声明`INVALID_ALIGNMENT_CONSUMES_FINAL_TICK`，但没有列出节拍/姿态候选、合法对齐值、预览反馈或玩家如何产生invalid alignment（Runtime L23）。Graybox只重复“invalid final echo alignment”并直接转`RT038`（L22）。
- 检查器只查4 Tick、3检查、1验证和`FOURTH_RIB_VERIFIED=TRUE`字符串（检查器L193-L198）；纸演也只手选一次有效对齐，再另写一个无数据来源的失败案例（纸演L35-L39、L68-L70）。

**风险**

实现时要么验证永远成功，探索失败条件是假的；要么程序自行发明节拍窗口，玩家在没有合同化反馈的情况下被最后一Tick强制重来。

**最小可执行修法**

用最小离散规则锁定验证：例如三项外部输入各有`READY/NOT_READY`，只有三项同一验证Tick为`READY`才成功；未齐时按钮显示缺项且可取消，若玩家确认不齐才消费第4 Tick。纸演和检查器各跑一次有效组合与一次明确无效组合，并在修复`RT038`回滚边后重进成功路线。

### [P2] `GPR2-07_ASSET_MATRIX_OMISSIONS`：主机体范围已收住，但资产矩阵仍未申报本关必显的标尺Hazard、两件货物与五人桥上表现

**证据**

- Graybox要求两台切割标尺Hazard（L9），Runtime要求`CARGO_PUMP / CARGO_FIRE_GEAR`和五人逐次过桥（Runtime L3、L27-L31），Episode也把这些作为胜利载荷与可见动作（正文L203-L205）。
- 资产矩阵只有馆守Z、右臂、白函、勇拳、SEG3、小机、UI、环境与六锚（`C01E03-asset-state-matrix-v1.tsv` L2-L29），没有标尺机复用行、货物Token、五人通行动作/Token或桥载荷HUD的范围声明。
- 检查器必需资产集合也不含这些对象（检查器L215-L240）；`len(asset_rows)>=25`只能证明行数，不能证明本话所有可见/可碰撞对象已预算。

**风险**

总体仍可控制在“白函唯一完整新Boss”，但关卡、美术与UI会分别临时补Hazard、货物和护送表现，导致碰撞、可读性或排期漏项。

**最小可执行修法**

矩阵补四类显式复用/轻资产行：两台标尺机=`reuse E02 hazard + two intent states`；两件货物=`map prop/token`；五人=`reuse actor/token + bridge traversal/handoff`；桥载荷=`UI/collision state`。全部可标为复用或UI-only，不新增完整主体。检查器把这些类别加入必需集合。

## 二、逐项关闭表

| 原项 | 复验 | 独立结论 |
|---|---|---|
| `GPR1-01` 唯一提交/回滚 | 唯一写入行存在；三失败终点无后继、Setup未创建、原子载荷未绑定精确键 | `PATCH` |
| `GPR1-02` 区域拓扑/人口 | L2五人、L1豪司、峰值6/过桥5、远程操作员、单向桥均闭合；独立BFS确认桥出口可绕开占格到西门 | `PASS` |
| `GPR1-03` SEG3/勇拳换载 | 时序Owner链与四足零位移闭合；次梁/接触格缺失，几何可达未证 | `PATCH` |
| `GPR1-04` 八阶段/压力钟 | Search/Bridge钟可求和；Structure钟零Runtime消费者，P2/P3顺序不一致 | `PATCH` |
| `GPR1-05` 真实选择/危险预览 | 私有整肩与危险动作已正确降为不可确认预览；两项选择没有下游分支动作 | `PATCH` |
| `GPR1-06` Owner/2x2馆守Z | 固定2x2、零平移/转向、肢体作用区、动作Owner和白函组件/Hazard分层已明确 | `PASS` |
| `GPR1-07` 探索/桥三段 | 4-Tick成功链与单向7/8预算存在；失败输入、回滚重入、逐段占格/容错未闭合 | `PATCH` |
| `GPR1-08` 资产范围 | 白函唯一完整新主体、右臂五态和三台巨物范围成立；Hazard/货物/护送/UI漏项 | `PATCH` |

## 三、已通过的独立证据

1. **检查器真实执行成功。** 指定命令exit `0`，RT001-039、三份TSV表宽、现有字符串门与Episode关键标记均通过；本席不否认这部分schema证据。
2. **人口和区域链可达。** 按Graybox L2/L1区域重建四邻接图，25个L2危险唇口格均可达桥入口；桥出口`L1(8,6)`可避开白函、馆守Z、消防Rig和勇拳占格，到达`WEST_EXIT L1(1,6)`。29人和远程操作员均无战场格，豪司不污染桥上5人。
3. **右臂物理尺寸成立。** 5m前臂、1.4m滑架、4.2m净距、0.9m高差、双索和两端0.8m搭接继续一致；不需要重写Story Core或索要新大地图。
4. **2x2巨型单位与主资产层级可实现。** 馆守Z固定足迹和有限肢体动作、勇拳锚定承梁、SEG3固定Rig、白函唯一完整新Boss均符合原席范围控制。

## 四、最低复验条件

无需重写Episode主峰；只需生产包完成以下最小闭环后回本席复验：

1. 修正四个死状态、创建Setup检查点、恢复切后左臂锁定，并让三类失败各自真正重进成功链。
2. `RT035`提交正文全部精确键，`RT035 -> RT036`字面连续；检查器比较原子键集而非Markdown存在性。
3. 对齐P2/P3顺序，把Structure Tick写入具体Runtime节点并逐Tick演算两种支援选择。
4. 给两项选择加入分支专属消费者，定义人员错位恢复、设备折扣与两种标尺机意图；检查器遍历四组合及分支动作。
5. 增加次梁/接触区几何，定义探索有效/无效对齐输入；桥若保留三段玩法则提交逐段占格回执。
6. 资产矩阵补Hazard、两货物、五人护送和桥载荷UI的复用/轻资产行。
7. 独立运行更新后的检查器，并提供三条“失败 -> 精确检查点 -> 再成功 -> 唯一提交”的机器路径；编剧纸演结论仍不替代本席。

## 五、席位结论

**独立结论：`PATCH`。** Story/Audience通过项与Episode主峰保持锁定；`GPR1-02`和`GPR1-06`已关闭，换载时序、桥尺寸和主资产上限也有实质进展。但当前检查器的exit `0`主要证明字段与标记存在，尚未证明失败可重入、原子键完整、结构钟可运行或两项选择真实改变动作。`GPR2-01`与`GPR2-02`是Runtime阻断项；其余为小范围生产合同补丁。完成前不得解除Gameplay/Production gate。
