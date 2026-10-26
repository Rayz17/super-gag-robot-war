# C01E02 G1.5-B2 退役重盾美术目标

> Status: `active / B2_only / individual_user_decision_required`
>
> Parent contract: `15-g1-5-representative-art-pilot.md @ cf49dac4d539d23337999807114676c9d060ec3e`
>
> B1 objective: `16-g1-5-b1-breaker-art-objective.md @ 3c15d33a2af030ce3bcdf8d03ed4c627df5d9d45`
>
> B1 gate: `B forelimb-bearer + X alien/bio armor + current closed three-structure relation approved for derivative design / runtime_allowed=false`
>
> Frozen Demo fingerprint: `944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`

## 1. 本轮唯一目标

为 `PROP_C01CDV1_RETIRED_SHIELD` 制作一组可由用户审定的退役重盾方向候选，并在同一设计判断中证明四个 E02 状态成立：`墙挂冷态 -> 左手持盾冷态 -> 挡下赤红冲击的烧红态 -> 强化盾拍后的 E02 受损态`。

本轮只确定重盾自己的轮廓、旧装备表面语言、馆守 Z 持用关系和四态连续性。它没有独立美术锁或可直接复用的正式母版；所有产物仍是 `Candidate / runtime_allowed=false`。交付后必须停下让用户逐项选择，不能进入 B3 地图、B4 动作/FX、C1 程序接入或 D1 LibTV。

## 2. 开工前权威读取

按顺序读取并核对：

1. `00-demo-source-authorization.md`
2. `02-e02-s01-s07-beat-runtime-map.tsv`
3. `04-e02-previs-v0.1.md`
4. `05-e02-asset-call-matrix.tsv`
5. `06-e02-state-checkpoint-contract.tsv`
6. `07-legacy-denylist.tsv`
7. `09-frozen-source-snapshot.tsv`
8. `09b-frozen-visual-snapshot.tsv`
9. `14-g1-joint-alignment-rework.md`
10. `15-g1-5-representative-art-pilot.md`
11. `producer-g1-5/a1-user-approval-receipt.tsv`
12. `16-g1-5-b1-breaker-art-objective.md`
13. `producer-g1-5/b1-user-approval-receipt.tsv`
14. 本文件
15. Current Canon 的 `V355-C01E02`、`V353U001`、`MECHA_WANJI_MOBILE_CHASSIS`，以及权威来源 `C01-完整剧情总纲.md`

先运行：

```bash
python3 scripts/report_v35_layered_pipeline.py --check
python3 scripts/check_c01_current_demo_contract.py
scripts/canon-query.sh scene V355-C01E02
scripts/canon-query.sh entity V353U001
scripts/canon-query.sh entity MECHA_WANJI_MOBILE_CHASSIS
scripts/canon-query.sh 退役重盾
scripts/canon-query.sh candidate 退役重盾
```

必须在来源回执中明确：退役重盾是 Working C01 场面与万机馆巡展装备中的既有实物，但没有独立美术锁；`PROP_C01CDV1_RETIRED_SHIELD` 是 Demo 槽位而不是新的 Canon 实体；本轮没有 Runtime 授权。A1-C 与 B1-B/X 只用于尺度、持盾和受击关系，不构成 Godot handoff，也不得被顺手重画或继续细化。

## 3. 已锁定的物理与剧情事实

所有候选必须同时满足：

- 重盾来自另一台退役防卫巨机，不是馆守 Z 的原配装备，也不是万机馆临时变形出来的部件。
- 它是长期悬挂在主厅侧墙的全尺寸机械结构展品，接近两层楼高，明显沉重；墙挂态、展架/挂点与被馆守 Z 从破墙处扯下的受力关系必须可信。
- E02 馆守 Z 为 18 米、两条原装前臂完整；它以左手取盾、立盾、顶盾前进和横向盾拍。盾不能替换手臂、锁死成腕部装备，也不能遮掉右臂或让 2×2 单位误读成更大 footprint。
- Demo 战棋中重盾热点固定在西北墙面 `(1,2)`；这是 `c01cdv1_s06_g1_v1` 的 Candidate profile，不得迁移成 Canon 或擅自改坐标。
- 盾面保留三次港口碎片雨留下的旧凹痕/焦痕区；资产矩阵中的“三旧焦痕”不得被画成三个新发光核心、三枚徽章或三段新传奇。
- BREAKER 的头部赤红冲击使盾面由受击区向外烧红，冲击从盾的两侧分开；这是材料承热与结构挡击，不是能量护罩。
- 挡击后出现可辨认的第四道新焦痕。强化盾拍可以使盾缘、盾角和主承力面变形、掉漆或出现未贯穿裂纹，但 E02 结束时盾仍能立住并继续使用。
- E03 的贯穿裂纹与 E04 的彻底碎裂都在本轮范围外；不得提前把 E02 受损态画成穿透、断成两半或报废。
- 轮廓需要同时支持正面完整格挡、顶盾推进、横向盾拍，以及后续可放平承担归舰缓冲；本轮不绘制 E03/E04 状态或动作。
- 重盾应读成旧人类防卫装备，与馆守 Z 的老派超级系身份兼容，但不得复制馆守 Z 自身胸甲、BREAKER 的异质/生体装甲或任何现成 IP 盾牌。

## 4. 受控候选与四态判断

提供 2–3 条真正可区分、但不新增故事事实的轮廓路线。可围绕以下功能母题探索，不得替用户选定：

- A：高窄塔盾型——墙挂与正面覆盖最清楚；需要避免骑士盾、人物比例盾或过度制式军徽感。
- B：宽体防爆板型——挡击分流、顶盾推进和重物感最清楚；需要避免完全遮住馆守 Z 或读成建筑墙板。
- C：偏心撞角型——横向盾拍、旧损伤和新增第四焦痕最容易形成视觉焦点；需要避免变成带刃武器或馆守 Z 的专属原配装备。

每个候选必须展示：

1. 正面、背面握持结构与严格侧面轮廓；
2. 主厅侧墙的墙挂冷态，标出展架/挂点、盾体重心与可被左手扯下的受力位置；
3. 馆守 Z A1-C 方向的左手持盾冷态，展示 18 米机体、2×2 footprint 和盾体覆盖关系；
4. `墙挂冷态 / 持盾冷态 / 赤红冲击烧红态 / E02 盾拍后受损态` 四态连续条；
5. 三处旧凹痕/焦痕区与第四道新焦痕的前后对照；新焦痕必须一眼可辨，但不能抹掉旧史；
6. 烧红态的受击中心、热扩散和两侧分流方向；不得用整面均匀发光代替材质与结构；
7. E02 受损态的变形边、未贯穿表裂与继续立盾的结构余量；
8. `wall_hung` 与 `held_cold` 两种战棋用途各自的 96×96、128×128 透明原生样张；它们只是方向样张，不是 Sprite Master；
9. `wall_mount_center`、`grip_center`、`bottom_center` Sprite pivot 与接地/挂墙基准；不得改变 G1 已锁定的热点或单位坐标；
10. 一张 S07 尺度/遮挡验证：馆守 Z 立盾、BREAKER B 方向发射轴和北侧安全线仍能辨认。B1 的 X 表面选择只可用文字/色块提示，不能把尚未派生的 B+X 当成正式敌机图。

输出只写：

`docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b2-retired-shield/**`

最低交付：方向判断板、各候选四态板、各候选 `wall_hung`/`held_cold` 的 96/128 px 透明样张、S07 尺度/遮挡验证板、`candidate-spec.tsv`、`source-validation-receipt.tsv`、`asset-manifest.tsv`、`user-decision-card.md`、`completion-report.md`、`delivery-hashes.sha256` 和可复现生成源。不得覆盖 A1 或 B1 文件。

## 5. 禁止项

- 不制作最终 Sprite Sheet、完整动作帧、正式 Cut-in、视频或 LibTV；不写 Godot；不签发 Runtime handoff。
- 不开始 B3 地图、B4 两机动作/FX、C1 接入或 D1 试片。
- 不修改馆守 Z、BREAKER、重盾热点、2×2/3×3 footprint、胜负条件、`confirm_shield_bash` 或 CP0–CP3。
- 不把重盾画成能量盾、变形机、手臂替换件、飞行翼、驾驶舱、拥有独立机魂的新机器人，或 BREAKER 的生体甲片。
- 不添加未经确认的驾驶员、阵营编号、文字徽章、武器名、制造商、传奇战役或三段新战绩。
- 不提前绘制 E03 贯穿裂纹、E04 完全碎裂、馆守 Z 右臂毁损、巡展臂装或推进骨架。
- 不读取旧 `story_first`、History 盾图或现成 IP 作为美术母版。
- 不调用 LibTV。任何付费生成或批量 AI 派生先停下交用户确认。

## 6. 用户停止门

交付后必须在美术任务中停止，并请用户分别裁决：

1. 主轮廓采用高窄塔盾、宽体防爆板、偏心撞角，或指定窄修改；
2. 旧装备表面语言更偏“退役防卫巨机的制式重装”、“港防工业修补感”，还是明确比例融合；不得自行新增所属组织或型号史；
3. 四态连续性是否通过：三处旧痕、第四道新焦痕、烧红分流与 E02 非贯穿受损是否清楚，同时没有提前泄露 E03/E04。

用户可以选择：`选定某路线，允许继续细化`、`选定路线但按意见修改`、`全部重做`、`仅参考` 或 `批准作为 Demo 派生来源，等待制作人交接`。未获得三项明确回复前不得开始 B3，也不得把任一候选交给主程序。
