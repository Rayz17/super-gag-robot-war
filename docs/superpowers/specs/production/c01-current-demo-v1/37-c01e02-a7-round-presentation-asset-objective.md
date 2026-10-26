# C01E02 A7｜单轮共同结算演出资产目标

> 派发对象：美术资产 Session A7
>
> 状态：`authorized Candidate audiovisual asset pass / user review required / no Runtime handoff`
>
> 写入：`docs/superpowers/specs/production/c01-current-demo-v1/art-a7-round-presentation/**`

## 1. 唯一目标

为 R0.5 的五个共同结算节拍提供一套最小但足以判断重量、命中、速度与悬念的 Candidate 资产：

`T1 车辆通过 → T2 小体截击 → T3/T3.25 巨体接触 → T4 城市炮击 → T5 红光蓄能／望向重盾`

这不是馆守 Z、BREAKER 或 E02 的完整动画生产。只做单回合两个成功草案和一个失败草案共用的代表性资产。

## 2. 开工前置

1. 使用 `chao-gag-canon`；
2. 完整读取 09b、10、31、32、33、34、37；
3. 查询 `V353U001`、`ENEMY_C01_BREAKER`、`ENEMY_C01_RIFT_SWARM`、`V355-C01E02`；
4. 只读已验收 C01 Reader E02 从“馆守 Z，起身”到 BREAKER 首次聚集红光；
5. 核对 A4/A5 用户批准回执和当前 MAP-B 三机位；
6. 读取但不导入 G1.5 A1 馆守 Z C 方向、B1 BREAKER `B + X` 方向和 B2 重盾 `A + F-D70/P30` 回执。
7. 用 `40-c01e02-m3-r0-5-frozen-contracts.sha256` 核验本轮合同。

所有棋盘尺寸、pivot 与 720p 合成使用 34 号锁定的 `isometric_tile_half_40x20`，不使用 R0 原几何的 30×15 投影导出美术母版。

G1.5 文件只授权派生方向，不是 sprite master 或 runtime 资产。不得放大 96/128px 旧样张冒充新交付。

## 3. 视觉核心

- 馆守 Z 是 18m 退役守护者，力量来自体重、站位与承受，不是轻盈格斗机；
- BREAKER 接近 30m，以前肢承重、异质／生体甲面和无眼红缝建立压迫，不是常规人形黑机；
- 小体仍为 A5 同源散乱个体，截击不把它演成爆炸杂兵；
- 城市炮火是远端自主支援，画面必须有“先偏开冲角，后命中侧甲”的因果；
- 红光只蓄能，不释放、不打中重盾；墙挂重盾仍为三道旧焦痕。

## 4. 核心美术交付

### 4.1 战术棋盘母版

| Slot | 最低交付 | 建议规格 |
| --- | --- | --- |
| `R05_GUARDIAN_MAP_ACTION_4DIR` | 四向 `idle/step_a/step_b/brace/recoil` | 单帧 `256×256 RGBA`，20 帧 atlas，pivot `0.5,0.88` |
| `R05_BREAKER_MAP_ACTION_4DIR` | 四向 `idle/charge/contact` | 单帧 `320×320 RGBA`，12 帧 atlas，pivot `0.5,0.9` |
| `R05_VEHICLE_EAST_MOVE` | 向东 2–4 帧通过动画 | 单帧 `128×128 RGBA`，12fps，pivot `0.5,0.82` |
| `R05_SHIELD_WALL_HUNG` | 墙挂冷态、三道旧焦痕 | `256×256 RGBA`，pivot `0.5,1.0` |

四向顺序固定 `north/east/south/west`，不得在 manifest 外另用文件名猜朝向。

### 4.2 关键帧／Cut-in

| Slot | 画面语义 | 规格 |
| --- | --- | --- |
| `R05_CUTIN_SWARM_INTERCEPT` | 馆守 Z 横腿／身体侧顶改开小体，不击毁 | `1600×900 RGBA` 分层静帧 |
| `R05_CUTIN_GIANT_CONTACT` | 两巨体正撞、馆守 Z 被推但冲线开始偏轴 | `1600×900 RGBA` 分层静帧 |
| `R05_CUTIN_ARTILLERY_SIDE_HIT` | 炮击命中 BREAKER 暴露侧甲，黑片剥落 | `1600×900 RGBA` 分层静帧 |
| `R05_CUTIN_RED_CHARGE` | 无眼头部红缝聚光，前景不出现受击盾 | `1600×900 RGBA` 分层静帧 |

关键帧只作 0.4–1.0 秒的动态变焦／屏幕切入，不制作长视频，不把棋盘的位移和状态变化外包成一段不可交互的 MP4。

### 4.3 FX

- `CONTACT_DUST`：8 帧、256×256、18fps，有 alpha；
- 三个互斥路面末态：`LONG_BROKEN_ARC/72`、`TWIN_BUCKLES/80`、`BREAKER_STRAIGHT_GOUGE/62`；各交 before/after + 6 帧翻起过程。末态层按 A4 相同原点输出 `2400×1350 RGBA`，过程帧可为局部 `512×256`；
- `ARTILLERY_HIT`：白闪、火花、黑色碎片分层，8 帧、256×256；
- `RED_CHARGE`：8 帧可循环红光，256×256，提供 additive/normal 预览；
- 评审板必须展示黑底、A4 MAP-B 合成底与 1280×720 实际尺寸三种条件。

## 5. 声音交付

只制作原创／可证明来源的非语音 Candidate，不复用 SRW、动画、电影或商业素材库中未获授权的声音。

| 类型 | 槽位 | 规格 |
| --- | --- | --- |
| UI | `COMMS_OPEN/CLOSE`、`CURSOR`、`CONFIRM`、`ILLEGAL`、`SUMMARY_OPEN`、`HOLD_LOOP` | WAV 48kHz/24-bit，峰值 ≤ -3dBFS；`HOLD_LOOP` 无爆点 |
| 世界 | `FOOTSTEP`、`ROAD_BREAK`、`VEHICLE_PASS`、`SWARM_RUSH`、`GIANT_CONTACT`、`ARTILLERY_HIT` | WAV 48kHz/24-bit，立体声可通过 Godot 定位 |
| 悬念 | `RED_CHARGE_LOOP`、`RED_CHARGE_STING` | loop 1–2s 无爆点；sting 2–4s |
| 环境 | `RAIN_ALERT_AMBIENCE` | 30–45s 无缝循环，不含旋律性 IP 引用 |

每个 WAV 登记来源、时长、sample rate、channels、peak、loop points、rights note 和 SHA-256。本轮不做人声配音或 BGM。

## 6. 评审交付

- 战术四向最小动作 Atlas 和车辆／重盾透明资产；
- 四张 Cut-in 分层静帧；
- 接触尘土、三种互斥路面末态与过程、炮击、红光 FX；
- 声音母件；
- 两种成功草案和一种失败草案的 1280×720 分镜接触表；
- 一条 15–25 秒 animatic 只作时序评审，不得当作 Runtime 回退视频；
- `asset-manifest.tsv`、`atlas-spec.tsv`、`fx-spec.tsv`、`audio-spec.tsv`、`source-validation-receipt.tsv`、`user-decision-card.md`、`completion-report.md`、`core-delivery-hashes.sha256`；manifest 逐项登记 `source_tool`、`rights_note`、`forbidden_states`；
- 可复现生成／合成源和只读 validator。

所有资产标记 `Candidate / runtime_allowed=false / runtime_handoff=none`。

## 7. 用户停止门

美术 Session 完成后必须展示并请用户判断：

1. 馆守 Z 和 BREAKER 在棋盘上是否有 18m 对近 30m 的体量差；
2. 小体截击是否读作“改线保护”而不是杂兵击杀；
3. 巨体碰撞是否有重量、被推移和路面受力；
4. 两个成功草案与失败草案的路面末态是否能在无文字时被区分；
5. 炮击是否清楚由冲角偏开才命中侧甲；
6. 红光是否足以形成悬念，又没有提前演出释放或挡击；
7. 声音是否明显改善节奏和反馈，但不依赖 IP 熟悉感；
8. 哪些具体文件批准作为 R0.5 Demo 派生来源。

未批准前不写 Godot，不复制到 runtime assets，不自签 handoff，不改 A4/A5，不用长视频替代引擎演出，不 `git add/commit`。
