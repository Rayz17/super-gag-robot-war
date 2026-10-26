# C01E02 A4 MAP-B 六层地图美术目标

> Status: `active / first reviewable art pass / individual user decision required`
>
> Subject: `MAP_C01CDV1_SCROLLING_STREET`
>
> Runtime slots: `MAP_C01CDV1_R2_BASE / BUILDINGS / ROOFS / FOREGROUND / OCCLUSION_MASK / STATE_LAYERS`
>
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 1. 本轮唯一目标

把用户已批准的 `MAP-B 馆墙防灾环廊型` 从布局方向板派生为一套可实际分层、可在 WEST/CENTRAL/EAST 三段滚动视口中审查的首轮地图美术候选。

本轮要交付真正可叠合的六层图，不再制作 A/B/C 地图方向比较，也不把单位烘进地图。完成后必须在美术 Session 展示关键图并停给用户逐项修改；不得自行交 Godot 或签发 Runtime handoff。

## 2. 冻结输入与开工检查

完整读取并核对：

1. `19-current-demo-inplace-rebase-producer-contract.md`，SHA-256 `6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94`；
2. `20-c01e02-j2-joint-integration-contract.md`，SHA-256 `038bfb0d57aea64c1ca3a91cae7e1623a33d7c8aaeb7e7ae2af4541770ca3f0d`；
3. `producer-a2/a2-user-approval-receipt.tsv`，SHA-256 `5eae8ce88217e1ab7185ef3fbf42dd234574ab8b016c068c441f8424c41a5e76`；
4. `producer-a3/a3-user-approval-receipt.tsv`，SHA-256 `4698ab86e24483bbaf0bd95c5f72e9f2d9cf694f935a6176ee7862ed9465bab4`；
5. `producer-a3/a3-selected-source-hashes.sha256`，SHA-256 `ff09490e4e0cad1c3f324c98397cd909d936a4d9447e42ff74c5c04783224355`；
6. `art-a2-rolling-district/candidate-spec.tsv`、`topology-receipt.tsv`、`camera-continuity.tsv`、`occlusion-rule.tsv` 及全部 MAP-B 三机位材料；
7. `main-m2-2/01-13-slot-test-matrix.tsv`、`main-m2-2/05-completion-report.md` 与 R2 manifest 的六个地图槽约束；
8. Current Canon 的 `V355-C01E02`，只作场景事实边界，不反向新增设定。

开工前运行：

```bash
python3 scripts/check_c01_current_demo_contract.py
scripts/canon-query.sh scene V355-C01E02
shasum -a 256 -c docs/superpowers/specs/production/c01-current-demo-v1/producer-a3/a3-selected-source-hashes.sha256
```

任一冻结文件或哈希漂移时停止并回报，不自行更新制作人回执。

## 3. 场景与拓扑硬锁

- 唯一方向为 `MAP-B 馆墙防灾环廊型`：北侧万机馆旧展墙与居民建筑形成保护面，中央空场供两台巨体回旋，东侧防灾环廊通往撤离口。
- 固定 `32×18`、拓扑 SHA-256 `baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8`；不得移动道路、可通行区、馆守 Z/重盾/BREAKER/撤离线与 6 个 scattered 小体的既定锚点。
- 建筑、街区、道路、连廊和警戒设施全部位于棋盘世界层；不得退回“固定小棋盘＋屏幕外前后景”。
- 视觉身份必须是旧会展区与万机馆南侧防灾设施，不得画成普通现代商业街、纯工业测试场或室内棋盘。
- 使用冷白馆墙、墨蓝铺装、朱红应急结构、低饱和绿灰修补面的既定材料关系；细节密度服从格位、移动范围、目标提示和 96px 小体可读性。

## 4. 六层核心交付

全部核心层以同一 `2400×1350` 画布、同一原点和同一像素配准输出：

1. `BASE`：不透明底层，包含道路、防灾铺装、地表分区与必要的大尺度导向；不含单位、屋顶、UI 或文字说明。
2. `BUILDINGS`：透明建筑体、馆墙、街区立面及固定设施；不得把可淡出的屋顶烘入本层。
3. `ROOFS`：透明屋顶、雨棚与上层连廊遮挡组；边界必须与遮挡 mask 一一对应。
4. `FOREGROUND`：透明近景世界物件，仅用于确有空间关系的前缘设施；不得用大块装饰遮住棋盘来制造景深。
5. `OCCLUSION_MASK`：透明遮挡控制图，明确可淡出区域、轮廓保留区与安全边界；不得靠美术人员口头说明才能使用。
6. `STATE_LAYERS`：透明状态覆盖候选，至少清楚表达撤离线 `active → cleared`、取盾后墙挂位置变空，以及道路/建筑受损的可见差分。状态层不得改变可通行拓扑或暗示 E03/E04 结果。

六层核心图必须相互独立，关闭任何一层时其他层不得留下该层的重复像素。允许另交状态变体评审图，但不能借此修改 R2 接口或把多个不兼容画布冒充一个已批准 Runtime sheet。

## 5. 评审合成与可读性验证

最低评审证据：

- 一张六层总合成全域图；
- WEST/CENTRAL/EAST 三张 `1280×720` 同状态连续视口；
- 一张六层逐层开关与透明通道检查板；
- 一张遮挡验证板：使用 A3 已批准的 A「伏壳钳足型」透明样张作评审 overlay，并用具名 2×2 馆守 Z、3×3 BREAKER 几何夹具证明不同 footprint 均能正确淡出并保留轮廓；
- 一张状态差分板：撤离线、空墙挂位、道路/建筑损伤分别前后对照；
- 一张纯读图：不显示坐标、箭头、标签或 UI，证明画面本身能读出旧会展区、中央交战空场和东侧撤离方向。

A3 小体只作外置评审 overlay，不得烘入六层，不得在 A4 内重画或制作其正式 atlas。馆守 Z、BREAKER、重盾及人物也只能用合同允许的具名几何夹具；禁止旧资产 fallback。

## 6. 输出与最低文件

只写：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a4-map-b-six-layer/**`

最低交付包括：

- 六层核心 PNG 与必要的状态变体 PNG；
- 六层全域合成、三机位、逐层检查、遮挡检查、状态差分和纯读评审图；
- `layer-spec.tsv`：slot、Stable ID、尺寸、alpha、原点、层序、用途和状态语义；
- `topology-lock-receipt.tsv`；
- `source-validation-receipt.tsv`；
- `asset-manifest.tsv`；
- `user-decision-card.md`；
- `completion-report.md`；
- `core-delivery-hashes.sha256`，只覆盖冻结合同/回执、六层核心图、关键评审图和上述机器可读文件，不把缓存或无关中间图纳入权威清单；
- 可复现生成源与只读 validator。

所有文件继续标记 `Candidate / runtime_allowed=false / runtime_handoff=none`。

## 7. 用户停止门

交付后必须在美术 Session 逐项请用户判断：

1. 画面是否仍明确是 MAP-B 的万机馆南侧旧会展区，而非泛化城市；
2. 场景质感、色彩和细节密度是否通过；
3. 六层拆分、滚动连续性和建筑入格是否通过；
4. A 小体及 2×2/3×3 夹具的 `淡出＋轮廓` 是否自然、是否妨碍操作；
5. 撤离线、空墙挂位、道路/建筑损伤的状态差分是否清楚；
6. 是否批准这六层中的具体文件作为 Demo 派生来源。

未获用户逐项批准前不得返工成 exact handoff，也不得继续下一项。

## 8. 禁止项与后续边界

- 不写 Godot、Runner、R2 manifest、玩法、存档、Canon、C04、正式 Runtime 或 LibTV。
- 不制作小体正式四向 atlas、馆守 Z/BREAKER/重盾正式母版、人物、Cut-in、FX、音频或视频。
- 不重开 MAP-A/MAP-C，不覆盖 A2/A3，不读取旧 `story_first`、旧 B3 或旧头像/机体资产。
- 不批量或付费生成；确需新增付费额度时先停给用户。
- 不 `git add/commit`。

用户批准 A4 的具体六层文件后，由制作人签发首批六槽 exact handoff，再派主程序做 WEST/CENTRAL/EAST 的真实接入与 fallback 捕获。A3 的 A「伏壳钳足型」虽已获准继续派生，但正式四向 atlas 必须另立后续美术目标并再次停给用户，不与本 A4 混做。
