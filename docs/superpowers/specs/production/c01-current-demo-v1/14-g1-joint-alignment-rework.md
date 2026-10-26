# C01E02 Candidate Demo G1.1 联合返工合同

> Status: `active / narrow_joint_rework / user_D1_D3_not_decided`
>
> Frozen source snapshot: `fe7a0764d11f5ac5f9d11accb7398df664132b0b`
>
> Build contract: `C01CDV1-G1 / 1.0.0`
>
> Content fingerprint: `944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`

## 1. 本轮到底返修什么

本轮不是重做 Demo，也不批准 D1–D3。它只关闭两类已经由制作人复核确认的交付缺口：

1. 主程序存档合同虽能在单实例内跑通，但 CP0 缺三个冻结源哈希，CP3 不能从磁盘合法恢复，坏指纹会静默重开；这些问题会使试玩证据不可复现。
2. 美术和主程序虽然各自完成，但 S01 不是同一坐标/相机/状态，S06 不是同一投影/回合状态，不能生成有意义的 50% 联合叠图。

本文件是 `13-demo-build-contract.json` 之外的制作人返工指令，不加入其 `semantic_files`，不改变既有冻结源、D0-B 结果或 `content_fingerprint`。若实现发现必须改变探索形态、S06 胜法、人物/机体身份、共享内核、Canon 或 Runtime 生命周期，立即停止并交用户确认。

## 2. 执行顺序与所有权

```text
美术 G1.1 对齐 ─┐
                 ├─> 制作人逐像素叠图与联合只读复核 ─> D1–D3 用户决策包
主程序 G1.1 修复 ┘
```

- 美术与主程序可以并行；双方完成后才允许制作人生成正式叠图。
- 继续服从 `10-cross-session-coordination.md` 的写入 allowlist、冻结源、denylist 和停止条件。
- 两个 Session 不修改本文件，不执行 `git add`、`git commit`、Canon migration 或 Runtime promotion；制作人统一审计和提交。
- 其他 Session 的工作树变化不得吸收、覆盖或回滚。设定/剧情/台本可继续推进 C03+，但不自动回灌本 Demo。

## 3. 共同的 S01 对齐态

Stable state：`C01CDV1_JOINT_S01_CAMB_V1`

| 项 | 锁定值 |
|---|---|
| Episode / checkpoint | `S01 / CP0` |
| 事件状态 | `spatial_completed=[] / no_failure` |
| 世界 / viewport | `1920×900 / 1280×720` |
| 映射 | `screen = world - camera_center + (640,360)` |
| 相机 | B，`camera_center=(960,450)`；裁切 `Rect(320,90,1280,720)` |
| 纪存脚点 | world `(845,716)`；screen `(525,626)` |
| 相机稳定性 | 捕获前直接锁定 B，不保留 lerp 中间值 |

共享注册锚如下。程序交互点、具名几何与美术 overlay source 必须使用同一行；不得再用门代替跌跌、用机器犬代替老余。

| 对象 | World | Camera B Screen |
|---|---:|---:|
| 跌跌 / 防火门交互点 | `(475,680)` | `(155,590)` |
| 机器犬 | `(850,655)` | `(530,565)` |
| 老余 / 轮椅 | `(980,676)` | `(660,586)` |
| 架桥机脚点 | `(1170,573)` | `(850,483)` |
| 小满 | `(1492,676)` | `(1172,586)` |
| 东侧出口 | `(1792,650)` | `(1472,560)`，本机位外 |
| 地下危险入口 | `(260,675)` | `(-60,585)`，本机位外 |
| 前景遮挡中心 | `(1080,640)` | `(760,550)` |

共同背景几何：

- 主行走面四点：`(80,700) (1680,570) (1880,760) (260,875)`。
- 地下区：`Rect(170,480,180,195)`。
- 东侧出口：`Rect(1700,290,185,360)`。
- 美术保留现有带报告标注的 PV01；另导出无双重标题/页脚的 Camera B overlay source。
- 主程序把 S01 热点、可视具名几何和捕获输入收敛到上述锚；这只是构图坐标对齐，不改变四项撤离因果、两项失败或 CP0/CP1。

## 4. 共同的 S06 对齐态

Stable state：`C01CDV1_JOINT_S06_T2_STAGE1_V1`

选择第一次基础回合结束后的首个可读冲撞意图态，而不是没有宽冲撞带的 CP2 初帧，也不是已经开放终结的完成态：

| 项 | 锁定值 |
|---|---|
| profile | `c01cdv1_s06_g1_v1` |
| checkpoint | `CP2 commit_count=1` |
| turn / stage | `2 / 1` |
| 馆守 Z | anchor `(5,3)`；footprint `2×2`；facing `south` |
| BREAKER | anchor `(5,6)`；footprint `3×3`；facing `north` |
| 重盾热点 | `(1,2)` |
| 进度 | `north_safety_line_held=true`；其余进度、`finisher_ready`、`finisher_triggered` 均为 `false` |
| 敌方意图 | `BREAKER / 冲撞 / 北侧城市安全线` |
| 受影响格 | `x=5..7, y=0..5` |

唯一投影：

```text
center_x = 420 + (x - y) * 35
center_y = 150 + (x + y) * 18
cell vertices = (0,-18), (35,0), (0,18), (-35,0)
```

像素锁：

- 棋盘包围盒 `x=105..840, y=132..510`；棋盘与 UI 留 `x=852..884` 空隙。
- 重盾中心 `(385,204)`。
- 馆守 Z anchor 中心 `(490,294)`；2×2 包围盒 `420..560 × 276..348`。
- BREAKER anchor 中心 `(385,348)`；3×3 包围盒 `280..490 × 330..438`。
- 冲撞带包围盒 `385..700 × 222..384`。
- 顶栏 `y=0..54`，内容区 `y=54..648`，底栏 `y=648..720`。
- 意图面板 `Rect(885,78,355,118)`；状态/指令面板 `Rect(885,210,355,414)`。
- 六按钮维持程序现有两列布局；强化盾拍在此状态可见但禁用。

本轮不改变 profile、坐标规则、胜负条件、4–6 回合目标或 D3 因果链。现有程序 `BASELINE_S06_1280x720.png` 保留为 `finisher_ready` 因果证据，但不得再与美术初态或 T2/S1 图叠合。

## 5. 主程序 G1.1 必做

### 5.1 存档与恢复 P1

1. CP0 三个 hash 必须由 `materialize_sources.py` 读取 `09-frozen-source-snapshot.tsv` 后写入 `build_identity/source_hashes`，再由 Candidate LocalState 复制；禁止另写常量或读取 worktree latest：
   - `story_source_hash ← C01CDV1_STORY_E02 = dd07412d84e8b21918a8369a312b0125fdd452b74d229602c8dde1922b8237b1`
   - `gameflow_source_hash ← C01CDV1_GAMEFLOW_C01 = 284771d905e0283b32e33c436e9a9c47a5578b1a7bbed6927ffb4fea7b14312b`
   - `canon_authority_hash ← CANON_AUTHORITY_MANIFEST = d5203da48a7634c1ed977e5a638403d03cc3797980342747c83cfbb39c24969a`
2. 将 `c01cdv1_e02_complete` 定义为合法 `TERMINAL_STATE_ID`，但不冒充第八个 Episode node。磁盘恢复后进入只读完成视图；不得重播 S07、重发结果或二次提交 CP3。
3. 用 Candidate 专用临时 save 目录完成 CP0–CP3 的“落盘 → 销毁 Runner A → 新建 Runner B → continue”测试。最低断言：CP0 回 S01 且三 hash 完整；CP1 回 S03 且只提交一次；CP2 回 S06 且初态签名一致、不重播 S03–S05；CP3 回合法终态且只提交一次。
4. 结构合法但 `content_fingerprint` 错误的 Candidate save 必须明确返回 `candidate_save_fingerprint_mismatch`，不创建 CP0、不进入 S01、不覆盖或删除坏存档，前后文件 SHA-256 相同，也不回落 Current/`story_first`。

### 5.2 联合画面与捕获

- 按第 3 节实现 S01 共享锚，补出跌跌和老余的具名几何；更新受影响的 PV01 与载体切换捕获，不加载 `art-g1`。
- 新增 `BASELINE_S01_CAM_B_X845_Y716_1280x720.png`。
- 按第 4 节新增 `BASELINE_S06_T2_STAGE1_1280x720.png`。
- 建议新增 `BASELINE_CP3_RESTORE_1280x720.png`，证明完成态来自磁盘恢复且没有重播 S07。
- 原 S06 `finisher_ready` 截图保留，manifest 明确其状态；不得覆盖成 T2/S1。

### 5.3 机器证据与测试

- 新增 `checkpoint-restore-receipt.tsv`：CP0–CP3 每行记录 save SHA、恢复状态、commit count 与结果。
- 新增持久化、坏指纹 fail-closed 日志；更新合同测试、完整回归日志、`capture-manifest.tsv` 与 `completion-report.md`。
- 现有 S01/PV01 与 transition 捕获因世界锚变化而重录；不受影响的 PV05/S06 流程视频可保留并复核原 hash。
- 用真实 `InputEvent` press/release 路径做一次 Candidate 输入隔离测试；若暴露 checkpoint fatal，则升级为本轮 P1，否则作为 G2 前 P2 记录。
- 重跑 materializer self-test、Candidate 专用测试、完整 `scripts/godot-test.sh`、producer contract、Canon strict、denylist/allowlist audit 与 `git diff --check`。

主程序完成条件：上述四项 P1 全通过，S01/S06 两个联合基准可复现，现有隔离与全量回归仍通过。只在同一 Runner 内重复调用不算真实恢复。

## 6. 美术 G1.1 必做

### 6.1 S01

- 保留现有 PV01 clean plate 与带报告标注的 Camera A/B/C 图。
- 新增 `PV01_S01_EVAC_WORLD_coordinate-lock.tsv`，记录第 3 节 stable state、相机、共享锚、脚点和背景几何。
- 新增 `PV01_S01_EVAC_WORLD_overlay_source_cam_B_1280x720.png`：相机 B、纪存 `(845,716)`、共享具名对象与无事件初态；去除会造成双重标题/页脚的报告 chrome，不缩放、不另行裁切。
- overlay source 仍是 `candidate_previs / runtime_allowed=false`，不能进入 Godot Runtime。

### 6.2 S06

- 将 `PV05_S06_TACTICAL_READ_1280x720.png` 从矩形俯视格重排为第 4 节的等距投影和同一 T2/S1 状态；Stable ID 不变。
- 新增无报告 chrome 的 `PV05_S06_TACTICAL_READ_overlay_source_t2s1_1280x720.png`，供严格逐像素叠图。
- V10X 只作馆守 Z 2×2 footprint 内的识别图；BREAKER 继续使用具名 Previs 轮廓。不得改变 D3 链、按钮集合、profile 或终结条件。
- 重新生成 36 秒 Animatic，只替换原 PV05 时段；镜头顺序和总时长不变。

### 6.3 清单

更新 `generate_art_g1.py`、`asset-manifest.tsv`、`g1-user-question-self-check.tsv`、`completion-report.md` 与 `delivery-hashes.sha256`。不重做 PV02、PV03、PV04、PV06、`SPACE_CONTACT_SHEET`、`GZ_IDENTITY_COMPARISON`、占位音或冻结来源回执。

美术完成条件：S01 overlay source 与共享锚一致；PV05 共 108 格、双方 footprint、热点、冲撞带和两个 UI 框与程序像素锁一致；所有输出保持 `runtime_allowed=false`。

## 7. 制作人联合验收输出

双方完成后，制作人只写：

`docs/superpowers/specs/production/c01-current-demo-v1/producer-g1-joint/`

必须交付：

- `S01_CAM_B_X845_Y716_overlay50_1280x720.png`
- `S01_CAM_B_X845_Y716_side_by_side_2560x720.png`
- `S06_T2_STAGE1_overlay50_1280x720.png`
- `S06_T2_STAGE1_side_by_side_2560x720.png`
- `joint-manifest.tsv`
- `joint-readonly-review.md`
- `delivery-hashes.sha256`

叠图必须是同尺寸源图的逐像素 `50% art + 50% program`，不缩放、不裁切、不重采样。通过阈值：

- 画幅、相机框、安全区误差 `0 px`。
- S01 共享脚点/热点偏差 `≤4 px`，前景遮挡轮廓偏差 `≤8 px`。
- S06 格心、菱形边、footprint、冲撞带和面板边界偏差 `≤2 px`。
- 两图状态完全相同；无双重标题、双重页脚或互相覆盖的注释层。
- 所有联合输出标记 `candidate_evidence / runtime_allowed=false`。

联合 PASS 只代表证据足以交用户判断，不代表 D1、D2、D3 已批准，更不开放 G2、付费视频、批量美术或 Runtime promotion。

## 8. 停止并请示

出现以下任一情况，相关 Session 写自己的 `BLOCKED.md` 并停止该分支：

1. 必须修改 `00`–`13`、`13` 指纹、冻结 snapshot 或 D0-B 才能完成。
2. 必须改共享 Autoload、默认入口、Current/`story_first`、正式战棋内核或超出既有 allowlist。
3. 对齐迫使改变斜侧视浅 X/Y、S06 核心胜法、人物/机体设计或馆守 Z V10X 生命周期。
4. 需要 Canon/Working/Candidate/Runtime promotion、付费 LibTV、批量 AI 生成或新的用户创作裁决。
