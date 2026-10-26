# R3｜`shield_take/south`｜A17 冷态盾编辑首个失败门

> Decision：`STOP_AFTER_COLD_SHIELD_EDIT_CALL01_FAIL`
>
> 成功姿势：`0`；shield-edit ImageGen：`1`；body-only ImageGen：`0`；random reroll：`0`
>
> `candidate_emitted=false` · `user=false` · `runtime=false` · `default=false` · `canon=false` · `godot_bound=false`

## 已通过的前置门

- A17 front/rear 确定性派生回执与 SHA 已锁；
- R2 失败 raw、旧馆守 Z 和历史失败资产没有被读取或传入；
- body-only 无身份几何 guide 通过：两条肩—肘—手链完整；两手到未来 rear handle 位置；图中没有盾、板、墙架；50% 首读是低位上提过渡；
- 纯算法去除热痕的插值、镜像与调和扩散诊断均因破坏 A17 面板／旧痕／表面连续性而被拒绝；调和模糊版只保留在 `preflight-fail/`，没有传入 ImageGen。

## 唯一 A17 冷态窄域编辑调用

- 正向输入仅为：
  `../../art-a17-section2-true-retired-heavy-shield-candidate/derived-front-rear-sprites-v1/masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png`
- 输入 SHA-256：`8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47`
- prompt：`../A17_COLD_FRONT_NARROW_EDIT_PROMPT.md`
- prompt SHA-256：`3d3339c51f481a2fd7bf0efa820dc6a9e7465b3e1aa7028151861e03baec2100`
- Built-in ImageGen：`shield-edit call01 only`
- random reroll：`0`
- built-in output：
  `/Users/rayz/.codex/generated_images/01a0329b-f0db-7fc1-a5fe-c8e50061c997/exec-00f5369b-b20b-4194-9b55-0d685e50a6cc.png`
- 隔离失败 raw：
  `../call01-shield-edit/preflight-fail/generation-raw/A17_COLD_FRONT_CALL01_FOURTH_WHITE_SCAR_IDENTITY_DRIFT_FAIL_RAW.png`
- raw SHA-256：`00c2d224227e32fd7fd4bacfc5f925df3e0268ab40a75305023a87267a6b2e8a`
- raw：`1024×1536 RGB`；棋盘背景烘入，没有 Alpha。

## 50%／100% 首个硬失败

1. 第四道赤红热痕没有被恢复为无痕面板，而是变成了额外一道斜向白色擦痕；要求严格三道旧白痕，实际为四道。
2. 要求透明 RGBA 单盾，实际输出是带烘入棋盘的 RGB。
3. 窄域之外的盾冠、面板分割、边框、金色嵌件与磨损细节发生全局重绘，不再是 A17 front master 的保真局部编辑。

因此冷态盾没有通过身份与时点硬门。失败 QA：

- `../call01-shield-edit/preflight-fail/qa/A17_COLD_FRONT_CALL01_FAIL_50_100_QA.png`
- SHA-256：`e5f0d79e77582f50b2fb78b9d1a1f53905181f0bcfd8211ffb92ef8823baa56f`

## 停线结果

- body-only ImageGen：`NOT_CALLED_AFTER_COLD_SHIELD_FAIL`；
- generated body raw：`null`；
- `body/arms/hands(back) -> shield_front_exterior(front)` 最终分层合成：`NOT_EMITTED`；
- `256×256 RGBA8` Candidate：`null`；
- pivot `[128,224]`、2×2、scale 1：`NOT_RUN_WITHOUT_CANDIDATE`；
- layered manifest：`null`；socket：`null`；composite owner：`null`；
- Godot、binding、Resolver、Default、Runtime、Canon：均未修改。

该失败 raw 和所有 `preflight-fail/` 文件只能作为负面证据，禁止进入下一批正向输入。

