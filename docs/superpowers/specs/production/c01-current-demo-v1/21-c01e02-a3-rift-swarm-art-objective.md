# C01E02 A3 小型突入体 Q/SD 美术目标

> Status: `active / direction design only / individual user decision required`
>
> Subject: `ENEMY_C01_RIFT_SWARM`
>
> Runtime slot: `ENEMY_C01CDV1_RIFT_SWARM_MASTER`
>
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 1. 本轮唯一目标

为 E02 同场的弱小突入体制作 2–3 个可明确区分的 Q/SD 身份方向，证明它们在 32×18 滚动战棋的 1×1 格、96/128px 和四朝向中可读，并为后续 `idle / move / impact` 动作保留空间。

本轮只让用户决定“这种小体应该长什么样、怎么动”。不得制作最终 atlas，不得交 Godot，不得顺带推进其他美术资产。

## 2. 开工前权威读取

完整读取并核对：

1. `19-current-demo-inplace-rebase-producer-contract.md`，SHA-256 `6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94`；
2. `20-c01e02-j2-joint-integration-contract.md`；
3. `producer-a2/a2-user-approval-receipt.tsv`；
4. `art-a2-rolling-district/candidate-spec.tsv` 与 MAP-B 三机位材料；
5. `producer-g1-5/b1-user-approval-receipt.tsv`，只读取 BREAKER 已批准的 B＋X 方向关系；
6. `main-m2-1/r2-slot-registration-receipt.tsv` 与 `r2-instance-binding-receipt.tsv`；
7. Current Canon 的 `ENEMY_C01_RIFT_SWARM` 与 `V355-C01E02`。

先运行：

```bash
python3 scripts/check_c01_current_demo_contract.py
scripts/canon-query.sh entity ENEMY_C01_RIFT_SWARM
scripts/canon-query.sh scene V355-C01E02
```

必须在来源回执中写清：该群体当前是 Working 的中性技术锚，不锁物种名、造型、能力、动机或最终棋盘数量；A3 是 Candidate 设计，不能反向改 Canon。

## 3. 设计硬边界

所有候选同时满足：

- E02 是少量小体借 BREAKER 破口漏入，分别扑击、游荡、围堵附近目标；不配合 Boss，不同步转向，不组成箭头或队形。
- 地图上使用一个 1×1 母版身份，实例为 `ENEMY_C01_RIFT_SWARM_01..06`；六只可有轻微色斑、甲片缺口或附肢差分，但不制作六套独立机设。
- 与 BREAKER B＋X 有同一异质/生体装甲生态的亲缘感，但不能像“缩小版 BREAKER”，也不能提前显露 E03 的统一脉冲指挥能力。
- 在 96px 和建筑遮挡的 `淡出＋轮廓` 下仍能分清朝向、接地点和扑击端；不得靠文字、发光血条或巨大特效维持身份。
- 原创，不复制具体机甲、怪兽、虫族或现成 IP 轮廓。
- 不新增飞行、远程炮击、钻地、合体、召唤、治疗等玩法能力；造型若暗示新能力，须在候选说明中明确“视觉语汇，不构成机制”。

## 4. 候选与交付

提供 2–3 条真正不同的母版方向。差异应来自主体重心、附肢组织和移动语法，而不是只换颜色。

每个候选至少展示：

1. 黑白主轮廓、严格侧面和三分之四身份图；
2. north/east/south/west 四朝向静态验证；
3. 96×96 与 128×128 透明原生样张；
4. 1×1 等距 footprint、`bottom_center` pivot、接地点和遮挡轮廓测试；
5. WEST/CENTRAL/EAST 中至少 CENTRAL 的 MAP-B 评审合成，不把小体烘进地图；
6. `idle / move / impact` 的动作空间草图，每项只需关键姿态，不做完整帧；
7. 与 3×3 BREAKER B＋X 方向的同源/差异说明；
8. “一个母版＋六实例轻差分”的规则样例。

只写：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a3-rift-swarm-qsd/**`

最低交付：方向板、各候选 96/128px 透明样张、四朝向/动作空间板、MAP-B 上图测试、`candidate-spec.tsv`、`source-validation-receipt.tsv`、`asset-manifest.tsv`、`user-decision-card.md`、`completion-report.md`、`delivery-hashes.sha256` 和可复现生成源/只读 validator。

## 5. 禁止项

- 不写 Godot，不改 Runner、R2 manifest、玩法、数值、footprint、Canon 或 Runtime。
- 不制作最终 sprite sheet、完整逐帧动画、死亡演出、Cut-in、视频或 LibTV。
- 不覆盖 A1/B1/B2/A2，不读取旧 `story_first`、旧 Demo 小体或外部 IP 作为母版。
- 不制作正式 MAP-B 六层，不重画馆守 Z、BREAKER、重盾或人物。
- 不批量或付费生成；若确需扩大生成额度，先停给用户确认。
- 不 `git add/commit`。

## 6. 用户停止门

交付后在美术 Session 停止，请用户逐项裁决：

1. 主轮廓选哪一案，或按哪些意见修改；
2. 与 BREAKER B＋X 的同源程度是否合适；
3. 移动语法偏爬行、跃扑或其他候选中的哪一种；
4. “一个母版＋六实例轻差分”是否足够；
5. 96/128px 与遮挡轮廓是否通过。

只有用户明确批准“作为 Demo 派生来源”，才允许另派正式四向 atlas；本任务不得自行继续。
