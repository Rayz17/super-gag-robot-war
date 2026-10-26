# C01E02 M3-R0.5｜媒体 Packing 与 A7 身份连续性纠偏令

> 日期：2026-08-18
>
> 状态：`active producer correction / supersedes conflicting media metadata only`
>
> 适用车道：`M0 / A6 / A7`
>
> 不改变：R0 resolver、玩法因果、故事停点、角色权限、默认入口、存档、Canon 或 Runtime 状态

## 1. 触发原因

并行审计确认两个阻断问题：

1. M0 的草稿 `presentation_asset_manifest.json` 把评审画幅、单帧尺寸与 Atlas 总尺寸混用，和 34、36、37 号合同冲突；即使程序和美术各自完成，也无法精确接入。
2. A7 首轮四张 ImageGen 源图中的馆守 Z 与 BREAKER 没有保持同一身份：馆守 Z 的头部、胸甲、比例与旧化程度漂移；BREAKER 在四张图里变成数种不同的黑色巨兽轮廓。

因此，M0/A6/A7 的完成回执、最终 hash、handoff 声明与 U1 提交全部暂缓。现有工作可以保留，但不能作为封存权威。

## 2. 唯一媒体 Packing 权威

唯一结构化规格：

`42-c01e02-m3-r0-5-media-packing-v2.json`

SHA-256：

`fe75667eac656756e35ddbbb784e250d39c0f8b05c2c14f719234d653b944012`

```text
packing_contract_id=C01E02_R05_MEDIA_PACKING_V2
atlas_origin=top_left
frame_order=row_major
safe_rect=x,y,width,height in single-frame pixels
pivot=normalized within a single frame
```

42 号文件仅覆盖 34、36、37 和 M0 草稿 manifest 中互相冲突的媒体尺寸、打包、帧序、pivot、safe rect、alpha 与音频参数。其余玩法、语义、allowlist、用户门和禁止项继续由 33–37 约束。

任何车道不得再从“建议规格”自行推导另一套总图尺寸。若 42 缺少必要槽位，写 `BLOCKED.md` 交制作人补充，不得本地发明。

## 3. 已冻结的关键口径

### 3.1 地图与已批准源

- A4 五层 native size 全部为 `2400×1350`；`BASE` 无 alpha，其余四层有 alpha。`1280×720` 只是评审视口，不是资源 native size。
- A5 小体为 `384×96`，四个 `96×96` 帧横排，顺序 `north/east/south/west`。
- 兜灯 OBSERVE/TENSE 各自为 `1920×640` 独立静帧，safe rect 为 `[160,64,1600,512]`；不得打包成新 Stable ID。

### 3.2 A6 人物

- 纪存：三列一行，`focused/alarm/resolve`，总图 `2304×768`，单帧 `768×768`。
- 七海：三列一行，`controlled/decision/concerned`，总图 `2304×768`，单帧 `768×768`；源文件必须保留人物 RGBA 与远程噪点 mask 分层，运行评审 Atlas 可合成。
- 旧守护者：三列一行，`guide/contact/shield_gaze`，总图 `3072×768`，单帧 `1024×768`；源文件必须保留 `head/chest/waveform` 三层，运行评审 Atlas 可合成。
- 三者都必须先通过透明边缘、单帧安全框、状态身份一致性和 1280×720 缩放检查。

### 3.3 A7 棋盘单位与演出

- 馆守 Z：总图 `1280×1024`，单帧 `256×256`；行是 `north/east/south/west`，列是 `idle/step_a/step_b/brace/recoil`。
- BREAKER：总图 `960×1280`，单帧 `320×320`；行是 `north/east/south/west`，列是 `idle/charge/contact`。
- 应急车：总图 `512×128`，四个 `128×128` 帧横排，`idle/move_a/move_b/move_c`，仅 east，12fps。
- 墙挂重盾：`256×256` 单帧，只允许 `wall_hung_3_scorches`。
- 四张 Cut-in：各自 `1600×900 RGBA` 分层静帧，不允许用 `1280×360` 条幅替代。
- 尘土、炮击、红光：各为八个 `256×256` 帧横排，总图 `2048×256`，18fps。
- 三种路面末态：各自 `2400×1350 RGBA`、与 A4 同原点；每种另有六个 `512×256` 过程帧横排，总图 `3072×256`。
- 音频统一 `48kHz/24-bit WAV`；声道、精确时长和 loop 以 42 为准，不再使用 44.1kHz 临时参数。

## 4. M0 立即修正

M0 可以恢复不依赖媒体尺寸的逻辑实现，但封存前必须：

1. 将草稿 manifest 标记从 `DRAFT_QUARANTINED` 更新为“受 42 约束的零 handoff schema”，登记 `packing_contract_id` 与 42 SHA；
2. 逐槽镜像 42 的 `total_size/frame_size/grid/frame_order/pivot/safe_rect/alpha/audio`，包括三个新增路面过程槽；
3. manifest 的 Stable ID、fallback 形状和零探测策略继续由 34/35 控制；42 不授权真实资产；
4. 增加自动测试，逐槽比较 42 与 manifest；任何漏槽、多槽、错帧、错音频参数均 fail closed；
5. 在 packing validator 通过前，不生成完成报告、最终 hash、正式捕获或“接入壳就绪”声明。

M0 不得修改 33–42，也不得读取 A6/A7 真实输出。

## 5. A6 恢复条件

A6 可以继续同一目录中的人物状态一致性和透明边缘工作。完成前必须：

1. 保留每状态无损母版，同时按 42 输出一张明确的评审 Atlas；
2. `portrait-spec.tsv` 同时登记单帧和总图尺寸、列序、pivot、safe rect；
3. 七海保留远程噪点 mask，旧守护者保留 head/chest/waveform 源层；
4. 兜灯继续使用原批准文件，只进入布局模拟图；
5. validator 读取真实 PNG 尺寸、alpha bbox、透明边缘和 Atlas 分格，不信任 manifest 声明；
6. 在 42 对齐通过前不生成最终 hash 或完成回执。

不得另起重复美术目录，不得写 Godot。

## 6. A7 首轮源图隔离

以下四张源图必须保留原字节并登记为 `rejected_exploration / identity_drift / runtime_allowed=false / runtime_handoff=none`：

| 文件 | SHA-256 |
| --- | --- |
| `rejected-exploration/source/R05_CUTIN_SWARM_INTERCEPT_imagegen_source.png` | `14da360aafc93e55507659a015afb87f1f24a8b23472ad9c01c2040ed0e5879c` |
| `rejected-exploration/source/R05_CUTIN_GIANT_CONTACT_imagegen_source.png` | `a01e55edf1d14ed3601dd2dac6b8c9c98f72f37eafe54a930978b4e5f9976bf1` |
| `rejected-exploration/source/R05_CUTIN_ARTILLERY_SIDE_HIT_imagegen_source.png` | `be01ab84be1ba19bf55975040a1b29254e759c9cfa53695e737660861b31b0d5` |
| `rejected-exploration/source/R05_CUTIN_RED_CHARGE_imagegen_source.png` | `8a1093377704ca6f9ba7345900cb6a0f65ecb2bca62d97a95363daaed63edcbd` |

它们不得被裁切、描摹、变色或二次放大成最终 Cut-in、Atlas、FX、animatic 或 U1 展示。A7 应新增 `rejected-exploration-receipt.tsv`，不要删除或覆盖原文件。

## 7. A7 身份锁板门

A7 下一步只授权制作一张共同身份锁板，不授权立即重做四张 Cut-in：

`A7_IDENTITY_LOCK_GUARDIAN_C_BREAKER_BX_2400x1600.png`

身份锁板必须同时引用并登记以下只读方向证据：

- 馆守 Z：`GZ_QSD_A1_direction_board_1920x1080.png`，选择 C 动作骨架方向；
- BREAKER 轮廓：`BREAKER_B1_candidate_B_identity_sheet_1800x1200.png`；
- BREAKER 表面：`BREAKER_B1_surface_relation_board_1800x1100.png`，选择 X 异质／生体装甲语言。

锁板至少包含：

1. 馆守 Z 正面、三分之四与侧面轮廓；金色横向头冠、红色中脊、银白格栅脸谱、红胸甲、圆形金色胸口、双圆柱前臂、右肩旧伤必须固定。R0.5 发生在右前臂最终报废前，不得提前画成断臂。
2. BREAKER 正面、三分之四与侧面轮廓；近 30m、3×3、前肢承重半直立、低头钻地轮廓、无眼单一红缝、闭合胸缝和 X 异质／生体曲面必须固定。
3. 馆守 Z 18m/2×2 与 BREAKER 近30m/3×3 在 40×20 棋盘上的同屏比例。
4. 两者的固定色板、不可漂移识别点和禁止形态：馆守 Z 不得变成新式尖角英雄机；BREAKER 不得变成人形黑机、普通四足兽、光滑蜘蛛或眼部面罩机器人。
5. `idle/brace/contact/red_charge_only` 四个关键动作缩略图，用同一身份而非重新设计机体。

身份锁板必须先交制作人视觉审查。未收到“identity lock pass”前，A7 不得继续四张 Cut-in、机体 Atlas 或 animatic。FX、路面和音频也不得封存，可保留尚未绑定身份的程序性草稿。

## 8. 重做 Cut-in 后的连续性门

制作人通过身份锁板后，四张 Cut-in 才可逐张重做。每张 manifest 条目必须登记同一个 `identity_lock_id` 和锁板 SHA。四张图必须满足：

- 馆守 Z 与 BREAKER 的头部、胸甲、肢体数量、比例、旧化和色板逐图一致；
- 小体截击只改线、不击毁；
- 巨体接触必须看见馆守 Z 被推移和路面承力；
- 炮击只在冲角偏开后命中 BREAKER 侧甲；
- 红光只蓄能、不释放；若画到重盾，重盾仍固定在墙上且只有三道旧焦痕，不得像已取得或正在受击。

## 9. 恢复与停点

本纠偏令生效后：

- M0 可按 42 恢复程序实现；
- A6 可按 42 恢复人物生产；
- A7 只恢复到身份锁板门；
- 三车道仍不得 stage/commit、真实接入或宣称 U1 已就绪。

重大缺口继续写各自 `BLOCKED.md`，交制作人裁决。
