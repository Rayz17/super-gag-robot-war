# C01E02 G2-A2-C3｜Current-Topology真实Atlas中性消费者目标书

日期：2026-08-20  
任务ID：`G2_A2_C3_CURRENT_TOPOLOGY_REAL_ATLAS_NEUTRAL_CONSUMER`  
执行者：主程序-2  
状态：`OPEN_BY_P98_AND_TASK98_PRODUCER_RELEASE / FIXTURE_ONLY / REAL_ART_ZERO`

## 1. 唯一任务

在Call03任何单机母版生成以前，证明current-topology专用Scene不是只读clip metadata并画`Polygon2D`，而是能真实加载、校验和消费透明PNG Atlas：显式`sparse state×facing×frame→rect`、统一pivot、footprint-bottom-center、z-sort、局部遮挡和五socket全部闭合。

本任务只使用身份中性的彩色几何测试Atlas，`fixture_validation_only=true / real_art_loaded=0`。不接Call02，不接V10X／B＋X／A5真实像素，不证明美术、FUN、UA91或Runtime。

## 2. 前置门

以下两项已经完成并由制作人关闭前置门；执行时必须锁定下列字节：

1. `G2_A2_C2_SCREEN_INPUT_TIMELINE_AND_EMBODIED_CONSEQUENCE`完成，P98签收文件`100-c01e02-g2-a2-c2-producer-playability-preflight-acceptance.md` SHA `cd4d128a023136be7197190382b9724b002ad9f093247ce25160838e9d1ffdcc`；Task96 manifest SHA `b8bcb8c0f94f56ba60a48ad7b2c756108ebee16a1e712facece8946c30877d60`。P98没有要求改R2C几何，仍`FUN_NOT_PROVEN / real_art_loaded=0`。
2. `A9_1A6_S_C2_SPRITE_FIRST_MAP_CAMERA_MASTER_PREPRODUCTION`完成并经制作人逐图／逐hash预检：
   - `delivery-hashes.sha256` SHA `41f5ba27a5b12088e84424c73e4fd6aa6aa93ba2bd7285e4bcb8eb94a94e50be`；
   - `atlas-schema-current.json` SHA `159c0af021c99a8c778692f5b02794e5ec55a476514da55ff55958baa19e8e5d`；
   - `map-camera-slot-contract.json` SHA `17e195dcac011be803bd69d893a918830dd838a5aa7a4aedd3e76bab45fb1a24`；
   - `socket-contact-contract.json` SHA `c954af9b0ac7e5a1ef0e55f95b613367af9ab5ddbaec3fc55f5f4a258e5b8ea5`；
   - `first-round-state-facing-phase-matrix.tsv` SHA `992ff3e6c35eb5cf6aa69ae928190f5c8ac3bb11927474569e1211ebb655bb2e`；
   - `first-round-phase-continuity-readback.tsv` SHA `e03f74e3e81ce888554b7ec0ba7e8e5c8e81600a1bc1f1974b755d73b7d64199`。

前置文件SHA不符或schema仍开放即停，不得自行发明第二套字段。

## 3. 实现边界

优先在`g2_a2_visual_compositor/**`内增加隔离的真实Atlas consumer／resource binding；不得改Resolver、Session、R2C route family、T1–T5逻辑、world result、相机、对象anchor、Default、save或Canon。

允许新建：

- 96／128／256／384身份中性透明测试Atlas与fixture manifest；
- `Sprite2D`／`AtlasTexture`消费组件及CompoundActor的fixture-only切换；
- 专用C3测试、capture driver、runner；
- `docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c3/**`。

禁止把中性测试图做成角色／机体造型；只用带frame编号、朝向箭头、socket十字与不对称角标的简单色块，便于机器与人同时辨认rect、方向和pivot。

## 4. 唯一current schema

必须直接消费预生产`atlas-schema-current.json`，关键字段至少包括：

`stable_id / slot_id / revision / resource_path / sha256 / view_space=map_dimetric_40x20 / camera_contract_id=CURRENT_TOPOLOGY_CAMERA_V1 / native_size / atlas_size / display_scale / footprint / pivot_normalized / pivot_px / z_bias / sparse_clips / state_aliases_with_signature / fps_or_hold / loop / filter / mipmap / interaction_sockets / shadow_owner / fixture_validation_only`。

禁止：

- `A4_MAP_SPRITE_CAMERA_V1`别名回退；
- 旧M2四向横条／统一frame_count矩形假设；
- state或animation模糊兜底；
- 跨facing fallback；
- 缺clip时显示上一张或第一张图。

## 5. 四类中性Atlas

至少真实绑定：

1. 馆守Z槽：256×256 frame、2×2、pivot`[128,224]`；
2. BREAKER槽：384×384 frame、3×3、pivot`[192,320]`；
3. 小体槽：96×96 frame、1×1、pivot`[48,72]`；
4. 应急车槽：128×128 frame、1×1、pivot`[64,96]`。

clip覆盖必须来自完整连续phase矩阵，而不是只覆盖离散截图。馆守Z至少含`idle/east`、`move/east,north`、`brace/east,north,south`、`contact/south`、`recoil/east,south`；BREAKER含north的`charge/contact/recoil/side_hit/red_charge`；车辆含east的`waiting/drive/recoil/passed`；小体01含west的`idle/move/recoil/deflected`，其余小体保持各自idle facing。允许带签名的同facing alias或engine tween，禁止跨facing借帧。

## 6. 注册、socket与遮挡

- Sprite必须`centered=false`，位置=`footpoint_screen - pivot_px×display_scale`；
- 可见脚点与projection helper计算的`footprint_bottom_center`误差≤0.5px；
- z-sort取footpoint screen y＋显式z_bias；
- shadow由引擎独立层唯一持有，测试PNG不得烘影；
- socket坐标基准统一为相对footpoint local offset；receipt必须同时给local与screen值；
- PLAN／CONTACT实际帧中，sprite与roof／foreground局部mask作用，patch外alpha不变；
- 1×1／2×2／3×3前后穿插必须随脚点改变，不能按单位类型固定层级。

## 7. 强制证据

1. resource SHA、尺寸、alpha、atlas size、filter／mipmap与schema逐项fail-closed；
2. 每种slot至少两张不同rect实机截图与readback，证明`AtlasTexture.region`真的改变；
3. A／B自然InputEvent执行链中逐帧记录`subject/state/facing/frame/rect/pivot/footpoint/z/socket/missing_reason`；
4. 连续T1–T5覆盖所有中间phase，`missing_clip_subjects=[]`，不得只抽离散门帧；
5. 故意缺clip、错camera id、错pivot、错SHA、越界rect五组负测均隐藏目标并给出唯一原因；
6. GZ PLAN脚点`(400,340)`、BREAKER PLAN脚点`(520,520)`及A／B CONTACT控制点≤0.5px；
7. 局部屋顶遮挡、shadow单一owner、socket坐标基准与A／B impact world point回读；
8. 120＋600帧非headless性能、重复加载次数／显存／p95帧时；采样窗口禁止截图IO；
9. C2屏幕输入、12–15秒演出、R1 route family、R2／R3／Full／Skip与B旧hash非回归；
10. `approved_handoffs=[] / real_art_loaded=0 / default unchanged / save=false / Canon=false / FUN_NOT_PROVEN`；
11. delivery hashes与唯一最终回归日志。

## 8. 验收状态与停止门

机器与制作人只能签：`REAL_ATLAS_NEUTRAL_CONSUMER_PREFLIGHT_SUPPORTED / FIXTURE_ONLY / REAL_ART_ZERO`。

出现以下任一项即停：需要改玩法几何／结果、需要使用真实身份像素才能证明consumer、current camera无法直接消费、连续phase仍缺clip、socket／shadow／遮挡有双真相、共享文件与C2验收态冲突。

通过后仍不得自行开放Call03。必须由制作人联合签收Art预生产＋C3中性消费者，再逐字授权一次`BREAKER_PLAN_MAP_CAMERA_MASTER_NORTH_RGBA_384`。
