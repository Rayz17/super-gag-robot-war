# C01E03 Godot Runtime Parity Audit v1

> Status: `candidate_runtime_parity_47_verified_0_partial_0_missing`
>
> Audit target: `C01E03_RT001..C01E03_RT047`
>
> Boundary: 本报告证明当前 Godot 候选逻辑与 47 条 Runtime 合同逐行可追溯；不证明正式美术、音效、真人节奏、平台导出或商业版本完成。

## 1. 审计口径

本轮不再以“四节点能通关”或“桥战主路可结算”代替逐条实现。每个 Runtime 行必须同时绑定：

1. 权威合同 `C01E03-runtime-contract-v1.tsv`；
2. 当前 Graph、Battle JSON、Session、P6 Spatial 或 Episode 状态实现；
3. 能直接触发对应行为的 Session、Spatial、Integration 或 Chapter Runner 测试；
4. `c01e03_godot_runtime_parity_v1.tsv` 中可被检查器定位的证据令牌。
5. 十张 Tactical 与四张右臂内部 Spatial 的 1280x720 视觉硬证据。

`scripts/check_c01e03_godot_runtime_parity.py` 要求合同与矩阵恰好一一对应。任何 `PARTIAL_CURRENT`、`NOT_IMPLEMENTED`、失效证据路径或缺失令牌都会令当前候选 Parity 门失败。

## 2. 当前结论

| 状态 | 行数 | 含义 |
|---|---:|---|
| `VERIFIED_CURRENT` | 47 | 当前实现与直接测试共同覆盖合同要求 |
| `PARTIAL_CURRENT` | 0 | 没有以高层映射冒充完整实现的行 |
| `NOT_IMPLEMENTED` | 0 | 没有整条 Runtime 缺失 |

这证明 C01E03 当前候选逻辑达到 `47/47` Runtime Parity。结论仅覆盖可执行逻辑和现有候选表现层。

## 3. 本轮补齐的关键行为

### 3.1 开场物理回执

Session 现在直接保存五个 L2 岗位、两件非人员货物、低压交接、白函第一只脚错开旧楼梯、主框旋转和 `SETUP_LOCAL`。七海只留下普通电话回执；豪司从西侧 L1 带失败记录后入场，峰值人数为六，且永不进入 L2 或桥面。

### 3.2 十二度抬肩、标尺目标与公共 Owner

馆守Z的首个动作记录固定 2x2、十二度肩角、L2 下沉与 B1 六处淡痕。上层设备路和下层人员路分别改写标尺目标、泵的位置、首组人货成本和一次恢复规则。私有整肩预览必须在地图目标上实体取消；六项公共 Owner 检查和五段无悬空换载回执共同阻断 P4 提前结算。

### 3.3 飞拳中点与主动断臂

飞拳只击中白函右主框一次。回收轨锁死、双索受力和 `ARM_SUSPENDED_RECOVERABLE` 是切断前的独立中点。P5 结算后，画面不再硬切到另一个模式：尺度定位从 18 米馆守Z收进 5 米右前臂，再落到人能行走的检修步道；P6 验证结束时按反方向回到同一条断臂桥面。

P7 刀口保留正确点和不消耗行动的错误探点；真正切断后先锁馆守Z左臂零位移承力，再开放三段桥。

### 3.4 真实 20 / 21 / 23 Tick 路线

唐胶不再由一个计数命令直接抵达安全区：

- `TANGJIAO_ENTER_ARM_MID` 依次确认 L2 搭接和臂中；
- 正常路线由 `CROSS_TANGJIAO` 确认 L1 滑架搭接和清桥；
- 下层人员路线可选一次 `TANGJIAO_LOWER_MISSTEP_RECOVER`，退回 L2 搭接；
- `TANGJIAO_REENTER_ARM_MID` 明确重新进入臂中，恢复不可重复；
- 两组人货、兜灯和纪存分别保存四态占用回执，下一组只能在上一组清桥后进入。

所有地图目标确认都驱动 0.42 秒候选运动插值：人物与随行货物从旧占位移动到新占位，地图同时显示起点、终点、当前单位和轨迹；播放期间不接受下一步误点，可跳过，Tactical 快照保存当前轨迹与时间。

上层路线为 `20/23`，下层直行为 `21/23`，下层失足恢复为精确 `23/23`。阶段结算还检查五人、两货、唐胶安全、桥面无占用、左臂封锁和三段桥开放。

### 3.5 P8 与唯一持久化边界

P8 在允许 Battle Clear 前核对五人、两货、豪司、白函和勇拳的本地处置。白函取得一次“损伤转功能”样本，勇拳由企业完整拖走并剥离数据，豪司留在 L1 安全侧。Tactical 和善后仍不能持久写入；六锚 Narrative 才以 `C01E03:RT035:ATOMIC_SNAPSHOT:V01` 一次提交精确 27 键。

## 4. 失败恢复与交互回执

- `RT037`：结构钟或 Owner 链失败回 `SETUP_LOCAL`，右臂重新接回，豪司和全部预演本地态重置；
- `RT038`：搜索耗尽或强行误判回 `EXPLORE_ENTRY_LOCAL`，保留悬臂外部姿态并清零四格搜索；
- `RT039`：桥面超载回 `POSTCUT_LOCAL`，保留主动断臂和左臂封锁，清空桥面并把五人两货放回 L2；
- 地图目标选择支持取消；中途存档恢复精确占用步；错误刀口探测不耗行动；唐胶入桥中途取消会删除临时回执并恢复原格。

## 5. 当前机器回执

```text
C01E03_GODOT_RUNTIME_PARITY_CHECK PASS
contract_rows=47 matrix_rows=47
verified_current=47
partial_current=0
not_implemented=0
visual_evidence=14
```

同时通过：

- Runtime / Graybox Checker；
- Bridge Session smoke；
- P6 Embedded Spatial smoke；
- Story-first Episode Integration smoke；
- C01 E01-E04 Chapter Runner；
- Multi-play 内容编译与 Content Compiler smoke。

当前 E03 Bundle 指纹：

```text
c88501d940d59766b84052275489f4b8fc54a673dd55f1c8206774bfa1b23581
```

## 6. 证明边界

本审计不证明：

- 白函标尺、内收索、飞拳、断臂和桥荷的正式 Sprite、逐帧角色动画与 SFX；当前尺度梯和过桥插值仍是候选表现层；
- E03 专用正式 ADV 背景、角色表情、机体 Sprite、Cut-in 和镜头节奏；
- 目标 25 至 35 分钟容量、首次理解率、手柄人体工学和真人失败恢复；
- Windows/Steam 导出、GPU 兼容、跨版本存档和平台成就。

后续可以深化 P1/P3/P4 的物理预览和演出，但不得再把这些生产质量边界写成 Runtime 行缺失，也不得让深化回退 47 行状态机、20/21/23 路线或 RT035 唯一事务。
