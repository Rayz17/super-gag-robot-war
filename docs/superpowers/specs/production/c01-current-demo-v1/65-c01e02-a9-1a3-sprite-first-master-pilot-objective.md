# C01E02 A9.1-A3｜Sprite-first 四向母版与动作 Pilot 纠偏任务书

> 日期：2026-08-19  
> Owner：美术资产-2 Session  
> 制作人：制作人-2 Session  
> 生命周期：`Candidate / non-default / runtime_allowed=false / no Canon promotion`  
> 状态：`active P0 microgate`  
> 用户授权：用户在审阅“Sprite-first 双母版＋稀疏 Clip＋Godot 因果演出＋LibTV 峰值”方案后明确要求制作人直接安排工作。

## 1. 本单覆盖什么，不覆盖什么

本单是 64 号任务书的生产方法纠偏覆盖单，不改写 59 号身份、风格、比例、地图连续性和用户视觉门。

被本单覆盖并停止执行：

- 64 号 A 节中“最终彩图必须由 Blender／Three.js Rig 正交直出”的强制方法；
- 64 号最低交付中以 Rig 直出四向彩图、彩图↔Rig 叠合作为产品视觉成立前提的部分；
- 继续用 Python、Pillow、Three.js、Blender `bpy` 原语或鼠标自动化制造身份关键可见美术；
- 把脚本低模、Raw Rig、mask、keypoint、尺寸误差或机器 PASS 当作最终母版。

继续有效：

- 59 号全部身份、比例、KINETIC_CEL、World Space、A4 投影和同一主体连续性要求；
- 64 号 B 节 BREAKER B「前肢承重半直立」＋X「异质／生体装甲」全部第一读法；
- 64 号 C 节清稿、来源回执与 Candidate 边界；
- 馆守 Z `CML008` Hard、纪存 `CML001` Hard、`CML128 KINETIC_CEL` Working；
- V10X 只作为 C01E02 Candidate 限域派生来源，不升 Canon 或 Runtime。

原目录 `art-a9-1a3-rig-bound-bx-restoration/**` 全部保留原字节，降为：

```text
history_and_measurement_evidence_only
visual_master_allowed=false
runtime_handoff_allowed=false
```

不得删除、覆盖、改名或继续扩出四向、接触态、A4回填与完成包。

## 2. 新生产模式

```text
Hard／限域身份来源
→ BASE_CLEAN 正比例身份标准
→ Q_RUNTIME N/E/S/W 四方向 Key
→ 单方向动作 Pilot
→ 制作人视觉预审
→ UA91 用户母版裁决
→ 稀疏 GT Clip 扩产
→ exact handoff
→ G2-B
```

“Codex 制作 Sprite”在本单中只指：

1. 使用 `imagegen` skill 和图像生成／局部编辑能力制作可见位图；
2. 每次以获批身份源或上一张获批同主体图作为参考，只改变一个方向、姿态或局部；
3. 使用确定性脚本做 chroma、despill、透明边清理、裁切、pad、一次缩放、拼板和校验；
4. 脚本不得绘制、补造、重构或重新配色主体的头、胸、肩、肢体、甲片和动作轮廓。

禁止一次 Prompt 生成整张四视／动作表；禁止每帧仅凭文字独立生图；禁止生成整张可玩截图作为最终证据。

## 3. 双母版锁

### 3.1 BASE_CLEAN

负责正比例身份和非对称结构，不直接当地图 Sprite。至少记录：

- 正、背、严格左、严格右；
- 身份不可漂移锚；
- 左右是否允许镜像；
- 当前生命周期／损伤态；
- 来源路径、SHA-256 和权限层级。

### 3.2 Q_RUNTIME

负责战棋地图真实读法，必须另做 `north,east,south,west` 四方向 Key；正比例三视图不能代替地图四方向。

- 馆守 Z：约4头身、18m、E02双臂、无翼、无背包、2×2 footprint；保留金色层叠头冠、中央红冠、蓝额盔、银栅格脸、红X胸甲、圆形金核、宽方肩环和等重纵向圆柱前臂。
- BREAKER：近30m、3×3；高背壳、低嵌头单红缝、壳体离地、两条前肢明显承重且半直立、短后足只稳定；必须第一眼读出非对称叠片、柔性甲缝和异质受力连续性，胸缝和上背出口保持封闭。
- 不得以镜像替代 BREAKER 左右方向；馆守 Z 也默认分别制作左右，只有制作人确认完全对称的局部才可机械镜像。

## 4. P0 内部微型视觉门｜现在只做这些

新建独立目录：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-sprite-first-master-pilot/`

只交：

1. `P0_GUARDIAN_Z_Q_SOUTH_IDLE_SOURCE_1024.png`：透明背景，馆守 Z south idle 高分辨率源；
2. `P0_BREAKER_BX_Q_NORTH_CHARGE_READY_SOURCE_1024.png`：透明背景，BREAKER north charge-ready 高分辨率源；
3. `P0_NATIVE_SCALE_SWEEP_A4_1280x720.png`：将馆守 Z 按 256×256、BREAKER 分别按 320／384／448 安全格方案放入 A4 正式 `tile_half=(40,20)` 地图，保持2×2／3×3实际占位，供制作人冻结 BREAKER 帧格；
4. `P0_IDENTITY_SOURCE_AND_ANCHOR_BOARD_2400x1350.png`：身份源、生成结果、不可漂移锚和禁止项并排；文字只能由确定性排版加在图外；
5. `source-lock.tsv`、`generation-log.md`、`p0-self-review.md` 和两张源图 SHA-256。

P0 完成后必须停止并回传制作人。不得自行进入四向、动作 Pilot、Atlas、UA91 或完成报告。

### P0 制作人视觉门

制作人必须看实际像素，不以 validator 代签。五项同时通过才派 P1：

1. 馆守 Z 去标签仍可识别为 CML008／V10X 限域形态；
2. 馆守 Z 约4头身、旧超级系重量和 KINETIC_CEL 大形成立，不是幼体玩具或高细节缩略糊团；
3. BREAKER 第一眼是 B＋X，而非雪橇、装甲车、龟、猿、哺乳兽或普通四足机甲；
4. 两机同屏比例、脚点、遮挡和战术 UI 安全区成立；
5. 深墨蓝线压、4–7个主色块、最多两级硬阴影和受控磨损成立。

任一项失败，只返修这两张，不扩产。

## 5. P1 四向 Key＋动作 Pilot｜仅由制作人书面放行

P1 不在本轮自动开放。收到制作人精确放行后才交：

### 馆守 Z

- N/E/S/W 四方向 idle Key；
- south Pilot：`idle, step_a, step_b, brace, contact, recoil_a, recoil_hold`；
- 256×256 native 帧，初始 pivot 候选 `[0.5,0.88]`，2×2；最终 pivot 由 alpha bbox 和 A4底边中心实测冻结。

### BREAKER

- N/E/S/W 四方向重心 Key；
- north Pilot：`charge_ready, charge_a, charge_b, contact, redirect, side_hit, red_charge_hold`；
- 帧格使用 P0 冻结尺寸，pivot 由 alpha bbox 和 A4承重点实测，3×3。

### 联合证明

- 真实 A4 1280×720 中央／左右相机区合成；
- 路线、朝向、冲撞走廊、意图和前景／屋顶遮挡同时开启；
- 单帧原尺寸、50%和25%三档读法板；
- 不打 Atlas，只交逐帧透明 PNG、frame ledger、pivot／bbox／safe rect 与来源链。

P1 完成后停止在制作人视觉预审。制作人通过后才集中送 UA91；机器 PASS 不得直接开放 UA91。

## 6. 后续稀疏 GT 预算｜本单不生产

UA91 通过后，A9.1-B 预计只扩：

| 主体 | 首轮预算 |
|---|---:|
| 馆守 Z | 四方向共32帧 |
| BREAKER | north约9–11帧 |
| 小体 | 既有四向idle＋west move／deflected，共9帧 |
| 应急车 | east waiting／drive／passed，共6帧 |
| 墙挂盾 | GT静态1帧 |

单位合计约57–59帧，不得按 G2-A.1 fixture 的 `states × facings × 3` 生产约210帧笛卡尔积。

## 7. G2 与 LibTV 边界

- G2-A.1-R1 的 `real_art_loaded=0` 内部消费者证明保持原结论；本单不触碰主程序。
- G2-B 继续冻结，直到 UA91、A9.1-B实物、制作人冻结稀疏接口并签 exact handoff。
- Golden Turn 45–75秒内 LibTV 预算为0；首次巨体接触、城市炮和红光均留在Godot地图。
- 完整 Golden Slice 通过 UGT 后才可另行申请赤红挡击、盾拍各1.5–3秒 LibTV；LibTV不能写结算。

## 8. 禁止项与停点

```text
CANON_MIGRATION
DEFAULT_ENTRY
FORMAL_RUNTIME
GODOT_REAL_BINDING
ATLAS
EXACT_HANDOFF
A9_1B_BULK
LIBTV
PAID_BULK_WITHOUT_NEW_APPROVAL
GIT_ADD_OR_COMMIT
OLD_STORY_FIRST_OR_OLD_UNIT_TEXTURE_LOAD
```

本单只开放 P0 两张身份关键源图及其实际地图比例证据。完成即停；制作人负责审图、返修或放行 P1，不让用户在任务间搬运。
