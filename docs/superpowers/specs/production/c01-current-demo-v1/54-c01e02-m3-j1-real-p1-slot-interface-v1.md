# C01E02 M3-J1｜真实 P1 槽位接口 v1

> 状态：`interface_frozen / exact_handoff_unsigned / Candidate only`
>
> 本合同替代 M1a fixture 的媒体规格作为未来真资产车道接口，但不覆盖或改写 M1a fixture 证据。
>
> 本合同不批准任何新美术、不开放 Godot 真资产接入、不晋升 Canon 或正式 Runtime。

## 1. 包级身份

```text
contract_id=C01E02M3P1REALV1
build_id=C01CDV1-M3-J1-M1-REAL-V1
rules_profile_id=c01cdv1_e02_shared_round_m3_j1
asset_profile_id=c01cdv1_e02_m3_p1_real_v1
topology_sha256=baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8
handoff_scope=candidate_demo_exact_copy_only
runtime_lane=candidate_non_default
resource_root=res://assets/candidate_runtime_demo/c01/e02/m3_j1/p1_v1
save_mode=disabled
story_checkpoint_write=false
operation_commit=false
formal_runtime_allowed=false
canon_promotion=none
directory_scan_forbidden=true
implicit_asset_search_forbidden=true
source_overwrite_forbidden=true
```

M1a 的 `fixture_validation_only` manifest、receipt、资源根和测试全部保留原字节。M1 不得把真实 P1 配置伪装成 fixture，也不得放宽 fixture denylist。

## 2. 每槽强制字段

每槽必须分开记录：

```text
slot_id
subject_id
asset_stable_id
usage
consumer_kind
source_path
source_sha256
authorized_copy_path
copied_sha256
dimensions
pixel_format
alpha_policy
color_space
frame_size
grid
frame_order
source_pivot_norm
render_registration
safe_rect
footprint
source_lifecycle
u1_receipt_id
u1_receipt_sha256
producer_p1_receipt_id
candidate_demo_load_allowed
formal_runtime_allowed
identity_critical
u2_required
fallback_policy
forbidden_states
```

- `subject_id` 只表示 Canon 主体；旧守护者必须用 `CH002` 并同时绑定馆守 Z `V353U001`，兜灯必须用 `CH001`。
- `asset_stable_id` 使用获批资产自己的 Stable ID，不得由主程序另造人物或机体身份。
- `source_pivot_norm` 是美术锚点；`render_registration` 是 Godot 摆放方式。全画布地图使用 `full_canvas_origin=(-880,-170)`，不得把画布原点冒充美术 pivot。
- `alpha_policy` 只允许 `opaque_rgb / straight_rgba_transparent / rgba_opaque_alpha / semantic_rgba_control`。
- `candidate_demo_load_allowed=true` 只能由最终 P1 receipt 赋予；美术源 manifest 的 `runtime_allowed=false` 保持不变。

## 3. P1a：已有批准来源的真实槽

| slot_id | subject / asset | 精确来源与 SHA | 接口 |
|---|---|---|---|
| `R05_MAP_BASE` | `MAP_C01CDV1_SCROLLING_STREET_R2_BASE` | `art-a4-map-b-six-layer/A4_MAP_B_BASE_2400x1350.png` / `6fd40a256afee225457594558edf274823de5d1e771d1f570d0263c5df217789` | 2400×1350 RGB；`opaque_rgb`；`full_canvas_origin` |
| `R05_MAP_BUILDINGS` | `MAP_C01CDV1_SCROLLING_STREET_R2_BUILDINGS` | `A4_MAP_B_BUILDINGS_2400x1350.png` / `db3f83eeb3ed5e583d0a831a203ab0d5446a594f9ed9e34f25f175f290f62237` | 2400×1350 RGBA |
| `R05_MAP_ROOFS` | `MAP_C01CDV1_SCROLLING_STREET_R2_ROOFS` | `A4_MAP_B_ROOFS_2400x1350.png` / `7fea3c7918ff85bb1d5df1f4bcc5856afac1d8fa7f174d59b862f985962f11a9` | 2400×1350 RGBA |
| `R05_MAP_FOREGROUND` | `MAP_C01CDV1_SCROLLING_STREET_R2_FOREGROUND` | `A4_MAP_B_FOREGROUND_2400x1350.png` / `454b3cf845ba91d7d7f13e201874bbbe79f871297a36930a24348823df1525a3` | 2400×1350 RGBA |
| `R05_MAP_OCCLUSION_MASK` | `MAP_C01CDV1_SCROLLING_STREET_R2_OCCLUSION_MASK` | `A4_MAP_B_OCCLUSION_MASK_2400x1350.png` / `b5f68f4749f6bff2025409622888d8e8faa17d977aca372caa43121eec18e899` | 2400×1350；`semantic_rgba_control`；sample-only |
| `R05_RIFT_SWARM_IDLE_4DIR` | subject `ENEMY_C01_RIFT_SWARM`; asset `CAND_C01CDV1_A5_RIFT_SWARM_A_IDLE_ATLAS_96_V1` | `art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png` / `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b` | 96×96×4；`idle/north,east,south,west`；pivot `[0.5,1]` |
| `R05_CUTIN_DOUDENG_OBSERVE` | subject `CH001`; asset `CUTIN_DOUDENG_C01_OBSERVE_V01` | `battle-presentation-v0.1/art-delivery/approved/cutin_doudeng_c01_observe_v01.png` / `b8530e98b9d76edb9275680488558167ad368697fe6f55a3af00ac5492196d3a` | 1920×640 RGBA；静态；pivot `[0.5,0.5]` |
| `R05_CUTIN_DOUDENG_TENSE` | subject `CH001`; asset `CUTIN_DOUDENG_C01_TENSE_V01` | `battle-presentation-v0.1/art-delivery/approved/cutin_doudeng_c01_tense_v01.png` / `c846e48b04b7d8671fd4853330487d0f39d1df98a70550d1f03d49770a26f159` | 同上 |

A4 旧 `STATE_LAYERS` 不进入本接口：其中烘有墙挂盾，会与独立盾槽重复。撤离线继续由游戏状态／UI表达，或以后另交不含盾的独立状态层。

## 4. P1b：已有候选但仍需 U1 的槽

| slot_id | subject_id | 当前候选接口 |
|---|---|---|
| `R05_PORTRAIT_JICUN` | `CH_JICUN` | 2304×768；768×768×3；`focused,alarm,resolve`；pivot `[0.5,1]`；当前 SHA `d6ec72d6976f532cfde707902231de3df5633d17aca66116710e4fa72b67622e` |
| `R05_PORTRAIT_QIHAI_REMOTE` | `CH_QIHAI` | 2304×768；`controlled,decision,concerned`；pivot `[0.5,1]`；当前 SHA `477f0873c6bdda04dde1312c49d57aaf53b1f2f6337023269290c5f87edbf67f` |
| `R05_COMMS_OLD_GUARDIAN` | `CH002;V353U001` | A8 B1.1 最终三态；1024×768×3；`guide,contact,shield_gaze`；pivot `[0.5,0.5]` |
| `R05_SHIELD_WALL_HUNG` | `PROP_C01CDV1_RETIRED_SHIELD_WALL_HUNG` | A8 B1.1 最终文件；256×256；pivot `[0.5,1]` |

禁止使用 `CH_OLD_GUARDIAN`、`CH_DOUDENG` 或任何旧 Demo 人物／机体 ID。

## 5. 必须完成扩图并逐文件 U1 的槽

| slot_id | subject_id | 最终接口 |
|---|---|---|
| `R05_GUARDIAN_MAP_ACTION_4DIR` | `V353U001` | 1280×1024 RGBA；256×256；5列×4行；行序 `north,east,south,west`；列序 `idle,step_a,step_b,brace,recoil`；pivot `[0.5,0.88]`；2×2 |
| `R05_BREAKER_MAP_ACTION_4DIR` | `ENEMY_C01_BREAKER` | 960×1280 RGBA；320×320；3列×4行；行序 `north,east,south,west`；列序 `idle,charge,contact`；pivot `[0.5,0.9]`；3×3 |
| `R05_VEHICLE_EAST_MOVE` | `TARGET_C01_EMERGENCY_VEHICLE` | 512×128 RGBA；128×128×4；`east_move_0..3`；pivot `[0.5,0.82]` |
| `R05_CUTIN_GIANT_CONTACT` | `PRES_C01E02_GIANT_CONTACT` | 1600×900 RGBA；静态；pivot `[0.5,0.5]`；必须是 Phase C 的 V10X 身份返修版 |

不得把 B0/B1/B1.1 单向证明条直接填入完整 Atlas 槽。

## 6. Phase C 非身份关键槽

- 三套 FX 继续保持三张独立 Atlas：`R05_FX_CONTACT_DUST / R05_FX_ARTILLERY_HIT / R05_FX_RED_CHARGE`；不得合成 fixture 的虚构单图。
- 音频使用已交候选的真实 `48kHz PCM24` 参数；消费者必须支持真实参数，不得为迎合 fixture 强制降为 `22.05kHz PCM16`。
- FX／音频仍需最终 manifest、哈希、probe、U1和 P1；其 fallback 必须逐槽披露，不能据此声称视听完成。

## 7. 生命周期与 U2 门

```text
interface_frozen
→ U1B_combined_review
→ final_asset_bytes_generated
→ final_file_U1_receipts
→ P1a_existing_source_rebind + P1b_new_identity_handoff
→ P1_REAL_V1_signed
→ M1_real_integration
→ producer_U2_identity_gate
→ user_U2_playtest
```

U2 前必须无 fallback：A4 五个静态层及遮挡采样、A5小体、馆守Z、BREAKER、应急车、墙挂盾、纪存、七海、旧守护者、兜灯两态与 `GIANT_CONTACT`。任一身份关键槽失败，全局 `U2_visual_playtest_ready=false`。

## 8. M1 边界

M1 可以新建 real profile、real receipt loader 与精确 Candidate 资源根；校验源 SHA 后复制并复算；验证媒体参数、帧序、pivot、safe rect、Stable ID、U1/P1回执与 topology；复用 M1a 消费者逻辑但按本接口替换真实槽位；输出真实加载与 fallback 台账、Full/Skip结果等价和确定性证据。

M1 不得修改 M1a fixture 文件或测试结论，不得扫描目录、猜相似文件、直接读取美术工作目录或复用旧 Demo 图，不得导入 A4 `STATE_LAYERS`、V21、旧馆守Z、旧 BREAKER 或旧人物头像，不得修改玩法 resolver、Reader、Canon、默认 M2、正式存档或剧情检查点，也不得在 P1 未签前复制／加载真实资产。
