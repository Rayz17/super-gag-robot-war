# C01E02 G1.5-B1 BREAKER 地面壳美术目标

> Status: `active / B1_only / individual_user_decision_required`
>
> Parent contract: `15-g1-5-representative-art-pilot.md @ cf49dac4d539d23337999807114676c9d060ec3e`
>
> A1 gate: `C action-frame direction approved for derivative design / runtime_allowed=false`
>
> Frozen Demo fingerprint: `944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`

## 1. 本轮唯一目标

为 `ENEMY_C01CDV1_BREAKER_GROUND` 制作“正比例轮廓身份方向 + Q/SD 地图转译”判断板，提供 2–3 个受控候选，然后停下让用户逐项选择和修改。

BREAKER 与馆守 Z 不同：它只有 Working Canon 文字身份，没有现成美术锁或可直接缩小的正比例母版。因此 B1 是一次需要用户裁决的敌方主体设计，不得把程序占位轮廓、旧 Demo 图或任一自动生成结果冒充正式机设。

## 2. 开工前权威读取

按顺序读取并核对：

1. `00-demo-source-authorization.md`
2. `02-e02-s01-s07-beat-runtime-map.tsv`
3. `04-e02-previs-v0.1.md`
4. `05-e02-asset-call-matrix.tsv`
5. `07-legacy-denylist.tsv`
6. `09-frozen-source-snapshot.tsv`
7. `09b-frozen-visual-snapshot.tsv`
8. `14-g1-joint-alignment-rework.md`
9. `15-g1-5-representative-art-pilot.md`
10. `producer-g1-5/a1-user-approval-receipt.tsv`
11. 本文件
12. Current Canon 的 `ENEMY_C01_BREAKER` 与其权威来源 `C01-完整剧情总纲.md`

先运行：

```bash
python3 scripts/report_v35_layered_pipeline.py --check
python3 scripts/check_c01_current_demo_contract.py
scripts/canon-query.sh entity ENEMY_C01_BREAKER
scripts/canon-query.sh candidate entity ENEMY_C01_BREAKER
```

必须在来源回执中明确：`ENEMY_C01_BREAKER` 是 `Working / active` 文字身份；当前没有 BREAKER 美术锁；本轮所有设计都是 `Candidate / runtime_allowed=false`。

## 3. 已锁定的设计事实

所有候选必须同时满足：

- 地面阶段站立后接近 30 米；馆守 Z 为 18 米，战场上应明显更高大并占据 3×3 footprint。
- 主体是层层黑甲包覆的城市突入重壳，能收紧四肢变成巨大钻头，在地下移动，并以低头冲撞作为主要威胁。
- 头部常态只有一道发红裂缝；它既是最明确的视觉焦点，也是 E02 赤红冲击的发射方向。
- 四肢压低时必须读成重新蓄势的攻城重物；侧面转向后要留下清楚的可受击侧甲。
- 双爪需要能够在 E03 夹住馆守 Z 的飞拳，但本轮不画 E03 动作帧。
- 胸甲中央要有保持闭合的结构缝；E03 才张开同色红裂。E02 常态不得提前把它画成亮弱点。
- 地面壳内部与上背结构要能容纳同一主体的十余米核心；E03 外壳破开后核心才从上背升起并展开近 50 米薄翼。
- E02 的强化盾拍只造成第一次侧翻/倒地与表层裂痕，地面壳没有被击毁，仍能翻身并重新压低身体。
- 美术语言必须原创，不复制现成机甲、怪兽或具体 IP 轮廓。

## 4. 受控候选与交付画面

提供 2–3 条真正可区分、但不改变上述能力和因果的轮廓方向。可围绕下列母题探索，不得替用户选定：

- A：低伏攻城楔型——冲撞、钻地和 3×3 占地最直观；需要证明站立、侧翻与双爪仍可读。
- B：前肢承重半直立型——双爪、抬头和侧推反馈最清楚；需要避免过度类人。
- C：装甲舱壳兽型——最容易解释“地面壳包住飞行核心”；需要避免变成普通坦克或泛用怪兽。

每个候选必须展示：

1. 正面黑白轮廓；
2. 严格侧面轮廓；
3. 默认朝北的三分之四主视图；
4. 收肢钻地与低伏冲撞的缩略轮廓验证；
5. 96×96 与 128×128 透明原生样张；
6. 放入锁定等距 3×3 footprint 的实读效果；
7. `north_west_cell` footprint anchor、`bottom_center` Sprite pivot 与接地中心；
8. 与已批准馆守 Z C 方向的 2×2 尺度对照。只能读取签收回执登记的 C 文件和哈希；其用途仅为美术尺度比较，不构成 Godot handoff；
9. 对 `idle / move / brace / impact` 后续动作空间的简短说明；本轮不制作动作帧。

输出只写：

`docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b1-breaker-ground/**`

最低交付：方向板、A/B/C 的 96/128 px 样张、`source-validation-receipt.tsv`、`asset-manifest.tsv`、`completion-report.md`、`delivery-hashes.sha256` 和可复现生成源。不得覆盖 A1 根目录文件。

## 5. 禁止项

- 不在 E02 展开薄翼、露出飞行核心、打开胸部红裂或画出 E03 破甲/贯穿状态。
- 不把头部红缝、胸部红裂和飞行核心的中央红孔画成同一个外露结构。
- 不让盾拍击毁 Boss，不画 E04 飞行终结或小型突入体群。
- 不加入驾驶舱、驾驶员、阵营编号、文字徽章，也不解释 BREAKER 为何追逐万机馆。
- 不恢复白函或任何 History 敌机设计，不读取旧 story_first 资产作为美术母版。
- 不制作最终 Sprite Sheet、动画、Cut-in 或视频；不写 Godot；不改 3×3 footprint、玩法、Canon 或 Runtime。
- 不调用 LibTV。任何付费生成或批量 AI 派生先停下交用户确认。

## 6. 用户停止门

交付方向板后必须在美术任务中停止，并请用户分别裁决：

1. 主轮廓选低伏攻城楔、前肢承重半直立，还是装甲舱壳兽；
2. 表面语言偏机械攻城壳还是异质/生体装甲；该选择会影响裂星潮后续敌群，不能由 Session 静默确定；
3. 头部红缝、闭合胸裂和上背核心出口的关系是否清楚，同时没有提前泄露 E03。

用户可以选择：`选定某路线，允许继续细化`、`选定路线但按意见修改`、`全部重做`、`仅参考` 或 `批准作为 Demo 派生来源`。未获得明确回复前不得继续 B2 重盾，也不得把任一候选交给主程序。
