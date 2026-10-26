# C01E02 Candidate Demo G1.1 联合只读验收

> 结论：`JOINT ALIGNMENT PASS / D1-D3 USER DECISION PENDING`
>
> Frozen snapshot：`fe7a0764d11f5ac5f9d11accb7398df664132b0b`
>
> Content fingerprint：`944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`
>
> Lifecycle：`candidate_evidence / runtime_allowed=false`

## 1. 本结论代表什么

本轮只确认美术 Previs 与程序灰盒已经在同一画幅、相机、坐标和游戏状态下可比较。它不表示画面已经达到正式美术品质，不表示试玩已经好玩，也不替用户批准 D1–D3、G2、付费视频、批量生成或 Runtime promotion。

验收使用两张原生 `1280×720` 输入，由 `generate_joint_review.py` 直接执行逐像素 `Image.blend(art, program, 0.5)`；没有缩放、裁切、变换、重采样或二次标注。Side-by-side 只是把两张原图原尺寸并排。

## 2. S01 联合态

State：`C01CDV1_JOINT_S01_CAMB_V1`

- 双方均为 `S01 / CP0 / spatial_completed=[] / no_failure`，Camera B 直接锁定 `center=(960,450)`，纪存 world `(845,716)` / screen `(525,626)`。
- 跌跌、防火门交互点、机器犬、老余、架桥机、小满等共享脚点由同一 coordinate lock/profile 驱动；叠图中注册点保持在合同 `≤4 px` 阈值内。
- 前景遮挡经第三轮单点返修后，双方均为 Camera B screen `Rect(705,310,110,270)`；轮廓边界误差 `0 px`，满足 `≤8 px`。
- 美术源在 `y=0..54` 与 `y=648..720` 使用无文字安全带；叠图只保留程序 HUD，不再出现双重标题或页脚。
- 结论：S01 技术对齐 PASS。它只让 D1 的斜侧视浅 X/Y 探索证据变得可比较，不判断该探索形态是否值得采用。

## 3. S06 联合态

State：`C01CDV1_JOINT_S06_T2_STAGE1_V1`

- 双方均为 `CP2 commit_count=1 / turn=2 / stage=1`；馆守 Z `(5,3)` 2×2 朝南，BREAKER `(5,6)` 3×3 朝北，重盾 `(1,2)`，只有 `north_safety_line_held=true`，终结技仍禁用。
- 双方使用同一等距投影 `center=(420+35*(x-y), 150+18*(x+y))` 与 108 格棋盘；棋盘、双方 footprint、重盾、冲撞带 `x=5..7,y=0..5` 的边界满足合同 `≤2 px`。
- 意图框 `Rect(885,78,355,118)`、状态/指令框 `Rect(885,210,355,414)` 与六个按钮矩形同位；美术叠图源只保留几何，不含板面、单位、按钮或报告文字，因此没有双重注释。
- 结论：S06 技术对齐 PASS。它只让 D3 的可读性证据可信，不判断姿态谜题本身是否好懂或好玩。

## 4. 上游完整性

- 美术 `asset-manifest.tsv` 共 20 条，全部 `runtime_allowed=false`；S01/S06 两张叠图源分别为 `candidate_previs`，馆守 Z V10X 仍是 Demo visual candidate，没有升格。
- 主程序 `capture-manifest.tsv` 共 7 条：5 条 `candidate_evidence`、1 条 `retained_pre_joint_evidence`、1 条 `candidate_causal_evidence`，全部 `runtime_allowed=false`；本轮直接参与叠图的两张 G1.1 program source 均为 `candidate_evidence / runtime_allowed=false`。真实 Runner A 落盘、销毁、Runner B 恢复的 CP0–CP3 测试与坏 fingerprint fail-closed 均已通过。
- 主程序独立复核为 P0=0、P1=0。仅保留两个不阻断的 G2 前 P2：可补 CP3 terminal 截图；可补“持续按 D 同时在 checkpoint 按 E”的重叠输入测试。
- 本轮未改 `00`–`13`、冻结 snapshot、D0-B、Canon、Current/`story_first`、共享内核或正式 Runtime 生命周期。

## 5. 交给用户的三个决定

联合对齐 PASS 后，仍只开放以下三个用户判断，不自动开放 G2：

1. **D1 探索形态**：S01/S03 是否采用斜侧视浅 X/Y 探索，而不是横版或俯视小人。
2. **D2 机体派生基准**：馆守 Z V10X 是否可作为本 Demo 的继续派生基准。
3. **D3 战棋可读性**：S06 的“守北线 → 改向 → 取盾 → 格挡 → 强化盾拍”姿态谜题是否一眼能懂、值得继续。

建议用户同时查看四张联合图、36 秒美术 Animatic 和程序试玩，再分别作 D1、D2、D3 判断；三项可以独立批准、驳回或要求窄返修。
