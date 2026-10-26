# 美术资产 Session 目标：C01E02 G1 联合 Previs

## Scope

只制作能回答 D1–D3 的低成本 Previs，不制作正式 Runtime 资产。语义来源固定为 `09-frozen-source-snapshot.tsv`，实际人物/机体母版固定为 `09b-frozen-visual-snapshot.tsv`，并须通过 `13-demo-build-contract.json` 校验；不得读取工作树 latest 或 `.superpowers` 活动路径后静默替换身份。

## Must Preserve

- A `KINETIC_CEL` 为常态；B `ARCHIVE_OFFSET` 只用于同体声源、胸灯与机战峰值；C 本轮不用。
- 人物/机体身份和生命周期服从冻结的 Canon 与 CML 锁。
- 纪存：CML001 冻结图只作 Current 身份锚；PV01/PV02 的最新设计方向必须使用同一清单内的 `CAND_JICUN_STANDARD_V1` 与 `CAND_JICUN_Q_RUNTIME_V1`，二者均保持 `design_direction_only / runtime_allowed=false`，不得回退成旧 Current 图的直接派生。
- 馆守 Z：18 米、E02 原装双前臂完整、右肩旧伤；CML008 冻结母版为 Current 身份锚，V10X 是实际 S05–S07 Previs 使用的 `demo_visual_candidate`，同时必须与 CML008 并排校对身份。V10X 仍不是已批准 Runtime 母版。
- V21、A3 飞翼、背包桥、飞翼根、巡展臂、断臂态和旧低热掌防不得进入 E02。
- S07 使用用户接受的 D0-B：挡击、南向推进、强化盾拍、BREAKER 第一次倒地但未毁。
- 禁止任何 `story_first` 头像、Sprite、地图和 v0.2 正式替代品。

## Deliverables

输出目录仅限：

`docs/superpowers/specs/production/c01-current-demo-v1/art-g1/`

必须交付：

1. `PV01_S01_EVAC_WORLD`：1920×900 clean-plate Previs、1280×720 A/B/C 三相机裁切、浅 X/Y 行走带、前中后景遮挡、出口/地下危险入口/跌跌/机器犬/老余/桥机/小满可读性。
2. `PV02_S03_SAME_BODY`：终端话说一半到馆守 Z 胸前续接的两帧或分屏，A 常态+B 局部峰值。
3. `PV03_S04_QIHAI_SCREEN`：七海最新成年身份的双地 ADV 构图；她只在危机联络室远程出现。
4. `PV04_S05_GUARDIAN_STAND`：按台、崩扣、直身、撞墙、第二步站稳五拍缩略镜头板。
5. `PV05_S06_TACTICAL_READ`：12×9 棋盘、安全线、2×2/3×3 footprint、冲撞意图、预测、重盾热点与候选指令布局。
6. `PV06_S07_SHIELD_IMPACT`：挡击、第四焦痕/推进、强化盾拍倒地三帧；馆守 Z 双前臂仍完整，BREAKER 未破甲。
7. `SPACE_CONTACT_SHEET`：World / Screen / Shot 三空间中人物与机体如何保持同一身份。
8. 30–45 秒低保真 Animatic；允许静态分层、相机移动、程序占位音，不使用 LibTV。
9. `asset-manifest.tsv`、`completion-report.md` 与所有交付的 SHA-256。

## Identity Comparison

- 馆守 Z 单独交一张冻结 CML008 与 `CAND_GUARDIAN_Z_COLLECTOR_E02_V10X_LOCKFRAME` 并排卡；S05–S07 的实际 Previs 使用 V10X，但比例、冠、胸、肩和 18 米身份由 CML008 复核。
- V10X 在所有记录中保持 `approved=false / runtime_allowed=false / demo_visual_candidate`。
- BREAKER、消防架桥机、机器犬和退役重盾若无 Current 美术锁，只能交设计 Previs/轮廓，不得宣称形成身份锁。
- 纪存、七海等人物必须只读取 `09b` 冻结副本中的最新合法身份；若清单未提供可用母版，用具名剪影并登记缺口，绝不回退旧头像，也不得自行追读 `.superpowers` 原路径。

## Generation Boundary

- 优先复用合法母版做缩略构图、分层和轮廓；仅在证明镜头必须时做少量候选生成。
- 不调用 LibTV、不产生付费视频、不批量派生、不升 Runtime、不改 Canon。
- 每个 PV 家族先过静态构图再做 Animatic；不要用更多图片掩盖透视、身份或焦点问题。

## Acceptance Evidence

- 每张图明确标注 1280×720 安全区、焦点、玩家视线、可操作带或意图区。
- 提供一张自检表，逐项回答 `04-e02-previs-v0.1.md` 的五个 G1 用户验收问题。
- 发现会改变人物/机体设计、探索形态或战棋规则的问题时停止并报告，不自行裁决。

## Validation

- `python3 scripts/check_c01_current_demo_contract.py`
- `git diff --check`
- 输出目录内无 `runtime_allowed=true`、无 V21 正向依赖、无旧 Demo 路径。
- 不暂存、不提交；完成后给制作人列出文件、哈希、未决项和可与主程序叠图的精确尺寸。
