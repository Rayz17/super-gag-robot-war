# C01E02｜G2-A.1-R2 战棋几何消费者校准唯一任务书

> 日期：2026-08-19  
> Owner：新主程序任务（不得resume／fork legacy“主程序”）  
> 状态：`READY_FOR_DISPATCH / CALIBRATION_PROXY_ONLY / REAL_ART_FORBIDDEN / G2_B_FORBIDDEN`  
> 上游唯一接口：76号、`c01e02-tactical-visual-interface-v1.json`、第一轮地图视觉状态矩阵

## 1. 任务目的

修正G2-A.1在地图投影、移动朝向、多格单位注册、pivot、z序和接触几何上的消费者断裂，使程序先能用校准proxy证明“同一个战棋世界”。本任务不是G2-B，不接入馆守Z／BREAKER真实美术，不开放UA91、Runtime或默认入口。

必须保留：

- 现有shared-round resolver的纯域结构、preview／execute同源原则；
- T1–T5事件时序与A/B两类策略语义；
- `A4_ISOMETRIC_40X20`数学投影；
- `save_disabled`、Candidate隔离和非默认入口；
- G2-A.1-R1已有contact/audio非metadata消费者证据。

不得把测试PASS、fixture atlas或manifest字段存在冒充视觉几何完成。

## 2. 必读输入

1. `76-c01e02-tactical-perspective-interaction-and-asset-interface-correction.md`
2. `c01e02-tactical-visual-interface-v1.json`
3. `c01e02-golden-turn-r1-map-visual-state-matrix-v1.tsv`
4. `59-c01e02-a9-g2-producer-correction-and-map-performance-gate.md`
5. `main-g2-a1-r1/06-completion-report.md`
6. `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/golden_slice_profile.json`
7. `game-godot/scripts/candidate_runtime_demo/c01/e02/c01e02_g1_runner.gd`中已证明的atlas rect、pivot与`_tactical_footprint_bottom_center`

## 3. 唯一写域

- `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/**`
- `game-godot/scenes/candidate_runtime_demo/c01/e02/m3_golden_slice/**`
- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/**`
- `game-godot/tests/candidate_runtime_demo/m3_golden_slice/**`
- `scripts/test_c01e02_m3_golden_slice_g2_a1_r2.sh`
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a1-r2/**`

不得写Canon、Reader、A4/A5/A9美术源、旧Runner、默认启动器或其他任务目录；不得git add／commit／clean。

## 4. 必须完成的代码纠偏

### R2.1 投影向量统一

- 所有cardinal overlay调用与地图相同的40×20basis。
- facing fan必须显示：north右上、east右下、south左下、west左上。
- route、ghost、facing fan、contact corridor、force arrow和摘要证据必须共享同一转换函数。

### R2.2 路径逐段朝向

- route动画逐段从相邻点delta派生facing。
- `final_facing`仅在endpoint settle／turn阶段应用。
- track数据必须能表达稀疏clip map与逐段facing；禁止继续用一个facing字段覆盖整条route。
- 为A、B、failure fixture分别增加断言，检查每段facing序列与终点朝向分离。

### R2.3 多格注册与pivot消费

- anchor继续表示footprint最小格。
- 2×2、3×3可见单位放在完整footprint的`footprint_bottom_center`。
- 实际消费binding的normalized／pixel pivot与display scale；错误、缺失或越界必须fail closed。
- 以footpoint screen-y作为统一z-sort主键；类别只允许显式小bias，不能替代空间深度。
- 增加单位跨格移动、前后交叉、屋顶／前景遮挡的校准proxy证据。

### R2.4 view-space与稀疏clip接口

- binding必须包含并校验 `view_space=map_dimetric_40x20` 与 `camera_contract_id=A4_MAP_SPRITE_CAMERA_V1`。
- 拒绝 `design_orthographic`、`screen_ui`、`cinematic` 进入地图单位槽。
- 用显式 `state/facing/frame -> rect` 稀疏clip map，允许有签名的state alias；不得要求统一frame_count矩形笛卡尔积。
- 保留旧fixture兼容只能通过显式测试适配层，不能成为真实handoff默认路径。

### R2.5 A4六层注册

- 用A4现有批准六层或无身份proxy验证共同2400×1350 canvas、origin、pivot、crop、zoom与screen rect。
- 输出exact layer registration manifest；不得再把任意32px fixture图scale成地图层来声称真实地图ready。
- 明确屋顶／前景的fade、cutout或occlusion mask Candidate方案，并用同一画面证明巨型单位的footpoint排序。

### R2.6 接触几何候选证据

当前A方案网格接触边与`south/north`叙事标签冲突。本任务必须：

- 计算每个A/B候选终点的两侧footprint、接触边、contact normal、approach与projected vector；
- 检查57号“馆守Z正面承接、BREAKER南向北冲”的语义；
- 给出最小fixture修正候选及其对车辆、小体、保护线、城市炮侧甲窗口的影响；
- 在producer签字前，只把候选放入R2 sandbox／报告，不覆盖正式profile语义；
- 接触proxy必须有body／impact socket、recoil vector与post-contact anchor，同一socket驱动flash和debris。

若无法在不破坏现有Reader／玩法因果的情况下闭合，报告 `BLOCKED_BY_CONTACT_STAGING_DECISION`，不得伪造PASS。

## 5. 必交证据

目录：`docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a1-r2/`

1. `01-input-receipt.tsv`：输入路径、SHA、权限与未读取legacy聊天声明。
2. `02-projection-direction-proof.tsv`：四向grid delta、screen delta、overlay位置和测试。
3. `03-route-segment-facing-proof.tsv`：A/B/failure逐段facing与endpoint settle。
4. `04-registration-pivot-z-proof.tsv`：1×1／2×2／3×3 footpoint、pivot、z与遮挡。
5. `05-a4-layer-registration.json`：六层共同canvas／origin／crop／mask。
6. `06-contact-geometry-candidates.tsv`：A/B接触边、法线、socket、受力、影响与状态。
7. `07-view-space-and-sparse-clip-proof.tsv`：错误空间拒绝与稀疏atlas消费。
8. `08-capture-manifest.json`与至少四张1280×720实际运行截图：方向扇面、逐段转向、多格footpoint／遮挡、接触socket／受力。
9. `09-test-report.txt`：专用suite与现有回归suite命令／结果。
10. `10-completion-report.md`：逐条PASS／FAIL／BLOCKED，不得只给总PASS。
11. `delivery-hashes.sha256`。

截图必须来自运行时actual frame，不能用离线Pillow／SVG合成代替消费者证明。

## 6. 验收与停止门

机器门之外，制作人必须查看实际截图／运行帧并确认：

- 所有单位像站在同一斜俯地图，而非眼平纸片；
- north/east/south/west与地图菱形一致；
- 2×2／3×3脚点、遮挡和接触没有隔空／穿插；
- A/B路线中朝向随每段改变，抵达后才转final facing；
- contact、flash、碎地、击退沿同一向量。

未通过前：不派A9.1-A6正式像素、不提交UA91、不做A9.1-B、不签exact handoff、不派G2-B。

