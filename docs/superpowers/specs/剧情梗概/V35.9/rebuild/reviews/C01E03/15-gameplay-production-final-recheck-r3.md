# C01E03 Gameplay / Production 最终独立复验 r3

> Review seat: original SRPG gameplay director / production designer
>
> Review object: C01E03 r2 Episode / Runtime / Graybox / Asset生产包
>
> Prior finding set: `GPR2-01..07`
>
> Checker run: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_c01e03_runtime_graybox.py` -> exit `0`
>
> Independent ruling: `PASS`
>
> Write boundary: 本文只写本席复验结论，不修改Episode、Runtime、Graybox、Asset、Checker、Canon或其他审稿文件。

## 一、发现（按严重度排序）

**未发现需要`PATCH`或`BLOCK`的P0/P1/P2 Gameplay / Production问题。**

本席没有把检查器绿灯或`14-runtime-graybox-paper-run-r2.md`的主控结论当作验收依据。除运行指定检查器外，另行逐行核对了状态前后继、分支守卫、27键集合、Runtime动作成本、桥段回执、失败重入和资产表示。检查器存在三处不能单独充当证明的边界：其状态BFS不验证失败谓词的来源，桥面总数含硬编码算式，完整新身体检查依赖资产标记；以下结论均有独立补证。

## 二、`GPR2-01`：三类回滚与唯一成功重入

**结论：`PASS`。**

1. `RT003`在白函第一脚关闭旧楼梯后真实结束于`SETUP_LOCAL`（Runtime L4），不是无实体的文字检查点。
2. `RT037 / RT038 / RT039`分别结束于`SETUP_LOCAL / EXPLORE_ENTRY_LOCAL / POSTCUT_LOCAL`，下游回执分别为`REENTER_RT004 / RT020 / RT026`（Runtime L38-L40）。三个终点都与真实后继的`start_state`逐字相等。
3. 独立逐行重入结果：
   - `RT037 -> SETUP_LOCAL -> RT004 ... RT035`成立；选`DIEDIE_PAD_ROUTE + UPPER_EQUIPMENT_ROUTE`时，全链每一行的`end_state`均等于下一行`start_state`。
   - `RT038 -> EXPLORE_ENTRY_LOCAL -> RT020 -> RT021 -> RT022(valid) -> RT023 ... RT035`成立。
   - `RT039 -> POSTCUT_LOCAL -> RT026 -> RT044 -> RT027 ... RT035`成立。
4. 切后锁定没有在检查点或回滚中降级：`RT024.end_state=ARM_CUT_COMPOSITE_BRIDGE_ACTIVE_LEFT_BLOCK_LOCKED`与`RT025.start_state`一致（Runtime L25-L26）；`RT039`又明确恢复`GZ_left_arm_block_locked`、先闭后开桥、五人/两货回L2和桥面清空（L40）。
5. 三个失败行的`start_state`是全局失败谓词入口，不是正常成功链节点：T6由`GB018`触发，探索强制错误由`RT022/GB021`直送`RT038`，桥超载/截断/失撑由`GB015/GB025`触发。正常成功链中不存在误入这些谓词的分支；触发后也不存在零行动终点。
6. 三个失败行均声明`no_persistent_write`或更强的禁止写入范围（Runtime L38-L40），回滚只恢复本局状态。

## 三、`GPR2-02`：精确27键与单一原子提交

**结论：`PASS`。**

1. Episode结算区从`GZ_RIGHT_ARM_LOST=TRUE`到`FIRE_BRIDGE_LEFT_FRONT_LEG=OVERLOAD_PERSISTENT`共有27项（Episode L382-L410）。独立解析结果为：27条、27个唯一完整键值、27个唯一键。
2. `RT035.mandatory_outcome`同样为27条（Runtime L36）。逐项集合差为`Episode - RT035 = 0`、`RT035 - Episode = 0`，顺序也完全一致；无缺项、无额外项、无同键异值。
3. `RT035.end_state`与`RT036.start_state`均为`C01E03_ATOMIC_TRANSACTION_COMMITTED`（Runtime L36-L37）；`RT036`只读且不变更状态。
4. Runtime唯一`phase=ATOMIC_SNAPSHOT`的行是`RT035`。`RT037-039`不含27个持久键中的任何`KEY=`写入，也没有`COMMIT`动作。
5. 成功守卫不是只写在说明中：五人/两货安全经`RT030`进入`FIVE_AND_CARGO_SAFE_LOCAL`，随后依次完成白函撤离、勇拳企业回收、善后和六锚锁定，才由`RT034 -> RT035`提交（Runtime L31-L36）。

## 四、`GPR2-03`：八阶段、结构钟与T6

**结论：`PASS`。**

1. Runtime顺序已与Episode阶段表一致：P1=`RT005`、P2=`RT008`、P3=`RT009`、P4=`RT010-016`、P5=`RT017-018/040-041`、P6=`RT019-023`、P7=`RT024-030/044-047`、P8=`RT031-034`（Episode L320-L330；Runtime L6-L35、L41-L48）。不存在上一轮的`P1 -> P3 -> P2`倒序。
2. 五次结构结算按Runtime实际顺序为：
   - T1 `RT005`: `(heat+2, displacement+1)`；
   - T2 `RT008`: `(+1,+1)`；
   - T3 `RT009`: `(+1,+0)`；
   - T4 `RT016`: `(+1,+1)`；
   - T5 `RT017`: `(+2,+2)`。
3. 基础和为`heat=7 / displacement=5`。跌跌垫片路在T2、T4各减1位移，得到`7/3`，再由`RT040`泄放冷却液到`6/3`；机器犬软管路在T1、T5各减2热量，得到`3/5`，再由`RT041`压实底垫到`3/4`（Runtime L6、L9-L10、L17-L18、L41-L42；Graybox L17、L19、L33）。
4. 两条补位动作都必须先把状态从`SUPPORT_ROUTE_RESPONSE_REQUIRED`推进到`SUPPORT_ROUTE_STABILIZED`，`RT019`才可建立探索检查点；不能跳过补位偷进P6。
5. 结构钟只在上述五个带`THEN_STRUCTURE_TICK`的出口推进。拖延到T6或强制破坏Owner链进入`RT037`，并回到`SETUP_LOCAL`（Graybox L19、L26；Runtime L38）；对白、Cut-in和检查点不暗扣Tick（Graybox L2）。

## 五、`GPR2-04`：两项选择的真实消费者

**结论：`PASS`。**

1. 支援选择不是UI标签：`RT004`锁定路线键（Runtime L5）；该键在T1/T2/T4/T5分别改变热量或位移结算，并在T5后只开放对应的`RT040`或`RT041`角色动作（L6、L9、L17-L18、L41-L42）。两路改变遥测、执行Owner、动作Clip与语音回报，之后才允许进入探索。
2. 通道选择有两组可见消费者：
   - 上层设备路进入`RT042`：标尺目标为`CARGO_ENTRY_CLAMP`，唐胶拨尺，泵预置，`RT027`成本5，人员失足恢复关闭（Runtime L43、L28）。
   - 下层人员路进入`RT043`：标尺目标为`PERSON_BUFFER_EDGE`，跌跌拨尺，泵不预置，`RT027`成本6，并开放一次`RT045-047`失足恢复（Runtime L44、L28、L46-L48）。
3. 两路虽在`LANE_BRANCH_RESOLVED`汇合，但汇合发生在目标、响应角色、设备起位和恢复权限均已消费之后。`RT042/043`及`RT045`均带明确`IF_ROUTE`守卫，不能把上层折扣与下层恢复拼成非法最优路。
4. 上层是更快但无失足保险，下层多1 Tick换一次可操作恢复；这是速度/容错差异，不是同结果的两句对白。

## 六、`GPR2-05`：次梁几何、一步接触与Owner链

**结论：`PASS`。**

1. 次梁连续足迹为`L1(4..12,9)`；勇拳入口参考格`L1(3,9)`、接触格`L1(4,9)`，曼哈顿距离为1；SEG3接触格`L1(12,9)`。两接触格都在同一连续足迹内（Graybox L32）。
2. 勇拳接触前最多移动1格、接触后平移0；SEG3四足固定、左前腿过载不参与移动（Graybox L10-L11、L32）。因此接触不要求勇拳跨图瞬移，也不要求消防Rig换格。
3. Runtime载荷Owner逐行闭合：
   - `RT012`: SEG3；
   - `RT013`: SEG3 + Brave；
   - `RT014`: Brave并写入`BRAVE_FIST_BEAM_CLAIMED=TRUE`；
   - `RT015`: Brave继续托梁，SEG3只绕固定关节转托槽；
   - `RT016`: 右臂落槽。
   前后状态逐字相接，任何时点都没有`Owner=None`（Runtime L13-L17；Graybox L12）。
4. 馆守Z继续是固定2x2、零平移、零转向单位（Graybox L7）；其动作区与梁Owner分离，不会把整机移动偷换成肢体动作。

## 七、`GPR2-06`：探索三类输入与重入

**结论：`PASS`。**

1. `RT020`固定消耗3个搜索Tick排除三条假筋，`RT021`记忆提示耗时0；第四Tick只在敲击`SHORT_SHORT_LONG`、勇拳`LOAD_CENTER`、垫片`GREEN`三项同时`READY`时由`RT022`写入`FOURTH_RIB_VERIFIED=TRUE`（Runtime L21-L24；Graybox L20、L22）。
2. 任一项`NOT_READY`只显示缺项且成本0，仍停留在验证输入，不会因查看错误原因耗掉最后一格；玩家可修正离散输入后再次确认。
3. 测试强制以`NOT_READY`结算时，明确消耗第4 Tick并直送`RT038`；`RT038`恢复`ARM_SUSPENDED_RECOVERABLE`、外部姿态和`search_tick=0`，结束于`EXPLORE_ENTRY_LOCAL`（Runtime L23、L39）。
4. 独立反例纸演为：三次检查 -> 任一`NOT_READY`强制确认 -> `RT038` -> `RT020`三次检查 -> 三项`READY` -> `RT022`成功 -> `RT023`。全程有下一合法动作，无隐藏耗时、无零行动软锁。

## 八、`GPR2-07`：三段桥、资产覆盖与预算

**结论：`PASS`。**

1. 标尺Hazard两种目标态均已列入资产矩阵（Asset L30-L31）；低压泵和消防设备各有weight2桥面Token与回执图标（L32-L33）。
2. 五名过桥者复用现有角色Token/脚步Clip，并只新增一次失足Clip；桥面HUD覆盖三段占用、整桥货物预留和一次性恢复（Asset L34-L35）。
3. 右臂五种碰撞/地图状态逐项存在（Asset L7-L11），足以支持连接、托槽、悬置、复合桥和旧址永久桥，不靠一张贴图跨状态。
4. 唯一完整新身体仍为白函（Asset L12-L16）。馆守Z、勇拳、SEG3均为复用身体、有限Clip或程序骨骼变体；标尺、货物、人类与HUD均为复用/Token/UI，不新增第二个完整主体。

## 九、独立20 / 21 / 23 Tick纸演

共同前段按守卫选择后逐行成立：

`RT004 -> RT005 -> RT006 -> RT007 -> RT008 -> RT009 -> (RT042|RT043) -> RT010 -> RT011 -> RT012 -> RT013 -> RT014 -> RT015 -> RT016 -> RT017 -> RT018 -> (RT040|RT041) -> RT019 -> RT020 -> RT021 -> RT022 -> RT023 -> RT024 -> RT025`

桥面成本直接取Runtime动作字段，不引用纸演表的预填总数：

| 路线 | Runtime动作链 | 独立求和 | 结果 |
|---|---|---:|---|
| 上层设备正常 | `RT026(2) -> RT044(1) -> RT027(5) -> RT028(6) -> RT029(3) -> RT030(3)` | `20/23` | 五人、两货安全 |
| 下层人员正常 | `RT026(2) -> RT044(1) -> RT027(6) -> RT028(6) -> RT029(3) -> RT030(3)` | `21/23` | 五人、两货安全 |
| 下层一次失足 | `RT026(2) -> RT045(1) -> RT046(1) -> RT047(1) -> RT027(6) -> RT028(6) -> RT029(3) -> RT030(3)` | `23/23` | 恢复恰用一次，五人、两货安全 |

三路中，唐胶、两件货物/两名接驳员、兜灯、纪存都留下`L2_OVERLAP -> ARM_MID -> L1_SLIDER_OVERLAP -> CLEAR`回执；货物占桥时由全桥预留规则禁止第二货物或人员并入（Graybox L15-L16、L21；Runtime L27-L31、L45-L48）。`RT030`之后三路共用`RT031 -> RT032 -> RT033 -> RT034 -> RT035`，没有超限后的伪成功汇流。

## 十、状态图与生产反例审计

1. 从正常输入构建状态图时，除只读成功终点外，没有“有入边、无后继”的普通状态；`RT037-039`是失败中断入口，不能误判为应由正常成功行产生的剧情节点。
2. 三个多出口状态均有守卫：`SUPPORT_ROUTE_RESPONSE_REQUIRED`按支援键选`RT040/041`，`LANE_BRANCH_PENDING`按通道键选`RT042/043`，`TANG_AT_ARM_MID`只在下层路线允许`RT045`。独立按守卫走三条成功路，未借用错误分支。
3. 双层区域复算：L2危险唇口25个格均可四邻接到`BRIDGE_ENTRY L2(9,6)`；桥出口`L1(8,6)`可沿`y=6`到`WEST_EXIT L1(1,6)`，避开白函、馆守Z、SEG3和勇拳足迹。旧楼梯关闭后，没有第二条L2到L1边，也没有反向会车入口（Graybox L2-L5）。
4. 未发现“脚本通过但生产不可实现”的额外完整身体、单位瞬移、无Owner帧、桥面会车、恢复循环、失败后半提交或计数软锁。

## 十一、检查器复核

指定命令实际运行exit `0`，输出依次通过Runtime schema、人口、拓扑、回滚图、结构钟、选择消费者、换载几何、右臂状态、探索输入、三条桥模拟、27键原子载荷、资产范围与纸演标记。

本席没有沿用其结论文本：另行确认了失败中断的真实来源、逐分支状态连续性、Runtime `COSTn`的20/21/23求和、27键顺序/集合、三条失败重入和所有必显资产表示。检查器当前覆盖与独立纸演相互印证，没有发现可由字符串占位掩盖的反例。

## 十二、席位结论

**独立结论：`PASS`。** `GPR2-01..07`全部关闭。三类回滚可重入且不污染持久态，27键只在`RT035`一次提交，五次结构钟与T6失败闭合，两项选择有真实消费者，梁几何与Owner链可实现，探索三类输入无软锁，20/21/23三条桥路线均在上限内完成，资产范围保持白函为唯一完整新身体。Gameplay / Production gate可解除并进入Runtime Graybox实现。
