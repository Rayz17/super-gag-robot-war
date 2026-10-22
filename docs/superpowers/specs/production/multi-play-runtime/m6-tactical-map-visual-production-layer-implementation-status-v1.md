# M6 Tactical A 档地图视觉生产层实现状态 v1

> 日期：2026-07-15  
> 状态：`candidate_map_visual_layer_validated`  
> 上游：`2026-07-15-chao-gag-multi-play-state-weave-implementation-blueprint-v1.md`、`m6-tactical-presentation-production-layer-implementation-status-v1.md`。  
> Canon 边界：本层只解决 M6 斜 45 度战场的单位识别与资产分档；全部新增轮廓保持 `runtime_validation_candidate`，不提升 C02E03、V35、正式机体造型或资产锁。

## 1. 为什么增加这一层

旧拳王已有透明地图图和标志 Pose，但其余实体仍是圆点或带字方框。玩家能读规则，却不能凭轮廓认出“过装冠军、陪练影子、作业货柜、拍卖锤、镜头无人机、伤员、仓门、证据箱”，战场仍像调试器。

正式生产又不能要求每个规则模块都拥有主角机同等数量的位图、动作帧和 Cut-in。因此 P3b 增加两档并存合同：

- 叙事主机体：透明位图地图资产、标志 Pose、必要 Cut-in 和招式演出。
- 次要机体、规则单位与目标：数据驱动的 A 档地图轮廓，必须有独立体态、功能部件、阵营色和状态降饱和。

程序化轮廓不是最终美术替代品，而是正式资产到位前仍能保证玩法可读、Canon 身份和屏幕构图的生产底座。

## 2. 共享运行时

新增 `TacticalUnitVisualRenderer`：

- 只在 Tactical `_draw()` 中绘制，不接管战斗规则、占格或目标判定。
- 从表现清单读取 `visual_kind=procedural`、`profile`、调色板、比例、偏移和 DONE 降饱和策略。
- 与现有 Texture2D 单位走同一个 `BattlePresentationCatalog.unit_visual()` 入口。
- 未知 profile 会被表现清单校验拒绝，不会静默退回错误轮廓。
- 没有表现清单的旧 M4 关卡继续使用原有规则图形，不会借用 M6 资产。

当前共享 profile：

| Profile | 用途 | 画面识别点 |
| --- | --- | --- |
| `echo_fighter` | 影子陪练机 | 双重残影、拳手身体、冷色视线 |
| `cargo_lifter` | 货柜领袖 | 货柜躯干、驾驶窗、顶撑臂 |
| `bairen_overarmored` | 全装冠军百刃 | 过量肩甲、尖刺背包、红色胸楔 |
| `auction_hammer` | 拍卖锤机械臂 | 固定底座、两段关节、落槌头 |
| `camera_drone` | 直播镜头无人机 | 四旋翼、中央镜头、追拍吊架 |
| `rescue_stretcher` | 坍塌区伤员 | 担架、人体轮廓、救援标记 |
| `warehouse_gate` | 仓门与撤离口 | 卷闸肋条、报警面板、门槛 |
| `evidence_cache` | 失败录像与回收日志 | 立体证据箱、卷盘镜头 |

## 3. M6 全图视觉闭包

M6 表现清单现在声明九个地图实体：

1. `old_boxer_king`：候选透明位图，仍是最高视觉层级。
2. `shadow_sparring`：A 档陪练机轮廓；Canon ID 为 `MECHA_SHADOW_SPARRING_MACHINE`。
3. `cargo_leader`：A 档作业变形轮廓；Canon ID 为 `V353U043`。
4. `bairen_champion`：A 档过装冠军轮廓；Canon ID 为 `ENEMY_C02_FULL_ARMOR_CHAMPION_BAIREN`。
5. `auction_hammer_arm`：A 档规则模块轮廓；Canon ID 为 `ENEMY_AUCTION_HAMMER_ARM`。
6. `live_camera_drone`：A 档规则模块轮廓；Canon ID 为 `ENEMY_LIVE_CAMERA_DRONE`。
7. `injured_worker`：A 档保护目标轮廓。
8. `warehouse_gate`：A 档空间目标轮廓。
9. `evidence_cache`：A 档可牺牲证据目标轮廓。

旧拳王右拳护具仍只通过 `OBJ_M6_RIGHT_GLOVE -> right_fist/body_jab` 绑定进入规则和演出，不成为第十个棋盘单位。

## 4. 自动与像素证据

`multi_play_timing_m6_smoke_test.gd` 现额外验证：

- 旧拳王仍解析为 Texture2D 完整机身。
- 八个其余实体全部解析为指定程序化 profile。
- 五个具名机体/敌方模块的运行 ID 保留 Canon 实体 ID。
- 表现清单、状态变体、右拳非单位规则和既有 M6 因果链继续通过。

1280x720 GPU 截图：

- `outputs/multi-play-presentation-validation/06-m6-tactical-object-continuity.png`

截图证明斜 45 度地图不再依靠圆点和单字区分实体，敌方意图线、行动环、HP、来源金点和侧栏仍无遮挡。它不证明正式造型、动画质量或真人首读速度。

## 5. 编译与 Windows 证据

- M6 bundle 仍含 11 项内容资源，源指纹更新为 `b838cddf609cc4b1eaf7d70677d9415c83906378a6682d8f027d6889409aa34c`。
- 内容编译器会通过 `BattlePresentationCatalog` 校验程序化 profile；未知 profile 无法进入 bundle。
- Windows 包要求 `tactical_unit_visual_renderer.gd` 存在，并在包内重读表现清单验证九个视觉 ID 与八个程序化 profile。
- 独立 PCK 验证通过 58 个必需路径，`tactical_map_visual_contract_pass=true`。
- EXE 为 137,283,648 bytes，SHA-256 `0eca9ef3e740b3140e0a339edcddedcd50727414becaed427fe8a3216cc82f7a`。
- PCK 为 28,233,776 bytes，SHA-256 `1a5af21211a290abce7cd328fe0e6b833b1e23bbd13d7ab0dc5ff5af8fd1ccb5`；EXE 偏移 109,049,856 的嵌入包与独立 PCK 逐字节一致。

## 6. 仍未完成

1. 八个 A 档轮廓不是正式机体美术；百刃、影子陪练和货柜领袖后续仍需正式地图 Sprite。
2. 旧拳王尚无移动、受击、顶门、回位与方向帧。
3. 敌方胶价王五部件 Boss 的主持投影、价格核心与清算采样箱尚未进入这张 M6 验证图；不得把当前三敌机误报为正式 C02E03 完整 Boss。
4. 正式音效、配音、碰撞闪白、相机轨迹、性能档和真人首读验收仍未完成。
5. Windows 真机与实体手柄仍未执行。
6. M6 继续是 `runtime_validation_only`；P5 正式 Episode 仍需独立 Pressure Board、Reader、资产和盲测验收。
