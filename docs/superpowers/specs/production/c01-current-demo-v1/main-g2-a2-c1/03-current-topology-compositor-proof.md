# G2-A2-C1 Current-Topology 与无身份 Proxy 合成器证明

## 唯一投影与五组相机

Scene、overlay、mask、测试和 capture 共用 `visual_projection.gd`；`canvas_origin_raw=[-1760,-340]`。

| 组 | profile | crop | layer top-left |
|---|---|---|---|
| PUBLIC | PUBLIC_PLAN_SUMMARY | `[640,468,1280,584]` | `[-640,-410]` |
| PLAN | PUBLIC_PLAN_SUMMARY | `[640,468,1280,584]` | `[-640,-410]` |
| SUMMARY | PUBLIC_PLAN_SUMMARY | `[640,468,1280,584]` | `[-640,-410]` |
| CONTACT A | CONTACT_A | `[640,498,1280,584]` | `[-640,-440]` |
| CONTACT B | CONTACT_B | `[620,488,1280,584]` | `[-620,-430]` |

`[0,0]`、`[15,11]`、`[20.5,10.5]` 三控制点均 0px 闭合；1×1、2×2、3×3 均使用 `footprint_bottom_center`。

机器证据：[current-topology-projection.json](receipts/current-topology-projection.json)。

## 六层与全屏公开态

六层顺序为 GROUND、STRUCTURES、ROOFS、OCCLUSION CONTROL、LIGHT/WEATHER、DYNAMIC OBJECTS。专用非默认 Scene 使用 `CompoundMapActor`、footpoint y-sort、rain/wet/reflection proxy 与局部 roof fade。

PLAN 必显公开态完整绑定：馆守Z、BREAKER、应急车、三只小体、东门、警戒设施；另有墙挂重盾、保护区、炮源与三条 intent trajectory。所有必显 subject 的 subject→proxy、state/facing alias 与 sparse clip 均 fail-closed 解析成功。

车、小体、东门、警戒设施、重盾采用分类中性轮廓与就地中文短标；顶部三威胁与地图轨迹共用颜色+形状标记。

机器证据：[current-topology-pre-scene.json](receipts/current-topology-pre-scene.json)；责任源文件为 `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/current_topology_map_contract.json`。

## 局部遮挡与 A4 donor 边界

- A4 `MAP_OCCLUSION_CONTROL` source SHA=`b5f68f4749f6bff2025409622888d8e8faa17d977aca372caa43121eec18e899`。
- RGBA 语义为 R=fade fill、G=roof outline、B=safety fringe、A=coverage。
- A4 coverage 与 Actor alpha 局部 patch 交集为 7472 px；无 control coverage 输出为 0。
- patch 外 740075 px 逐像素校验，alpha 改变为 0。
- 更新为 dirty-rect only，不在每帧扫 1280×584。
- A4 旧像素不可见，不是 current topology 产品控制源；`approved_handoffs=[] / real_art_loaded=0`。

机器证据：[a4-donor-mask-method.json](receipts/a4-donor-mask-method.json)。

## CONTACT 分路与时态

| 方案 | timeslice | 馆守Z | BREAKER | Swarm01 |
|---|---|---|---|---|
| A | T3.00 | `[20,9] / south` | `[20,11] / north` | `[22,9] / 1×1 / deflected_alive / grounded / non-blocking` |
| B | T3.25 | `[19,9] / south` | `[20,11] / north` | `[22,8] / 1×1 / deflected_alive / grounded / non-blocking` |

T3 只允许微裂、少量碎屑、水花与接触 FX；炮击逻辑真值保留为 `fired_hit_side_armor`，但 presentation 为 `tracking/forecast_only`、`physical_shot_allowed=false`。T5 赤红蓄能与完整路面翻起同样不提前实体发生。

机器证据：[actual-frame-manifest.json](receipts/actual-frame-manifest.json)、[natural-sequence.json](receipts/natural-sequence.json)。
