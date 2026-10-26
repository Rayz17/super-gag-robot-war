# C01E02 A4 × Runtime 联合注册与当前对象空间纠偏

日期：2026-08-20  
任务ID：`P85_A4_RUNTIME_JOINT_REGISTRATION_CORRECTION`  
状态：`PAUSED_AWAITING_USER_MAP_ROUTE_DECISION`  
权限：`Candidate production correction only`  
不构成：Canon迁移、Runtime晋级、真实美术handoff、UA91开放、G2-B开放

## 1. 制作人裁决

80号对R2C的玩法几何、A/B接触、socket、Swarm01 `[22,9]`与第二轮回读仍有效；但其中“A4六层已经与单位共同exact注册”的视觉结论撤回。

81号与82号继续暂停。美术不得发起第2次ImageGen；主程序不得继续Scene、Actual Frame或性能宣称。由于2.4所列问题已从“注册误差”扩大为“旧A4世界拓扑与当前R2C世界拓扑冲突”，本合同不得直接派工；唯一下一步是用户先裁决86号地图路线。

本轮纠偏不改resolver、路线、anchor、footprint、接触几何、T1–T5、音频边界或角色设计。它只修复“同一格点在A4像素、Godot单位和美术导向板中落在不同屏幕位置”的联合注册错误。

## 2. 已证实的错误

### 2.1 80号混抄了两个相机时态

R2C camera receipt里的base camera center是：

```text
base_camera_center_raw = [-720,350]
```

但80号同时冻结的：

```text
crop_rect_px       = [480,428,1280,584]
screen_top_left_px = [-480,-370]
```

不是base camera的派生值，而是R2C第5张动态frame在`focus_cell=[17.5,9.5] / focus_weight=1 / zoom=1 / shake=0`时的旧manifest读回。把base center与动态末帧crop并列为共同常量，形成了两套相机。

### 2.2 A4 canvas origin metadata本身错误

A4最终PNG生成器使用：

```text
source_px(x,y) = [880,170] + [40*(x-y), 20*(x+y)]
```

Runtime使用：

```text
raw_px(x,y) = [-880,-170] + [40*(x-y), 20*(x+y)]
```

所以满足`raw_px = canvas_origin_raw_px + source_px`的唯一共同原点是：

```text
canvas_origin_raw_px = [-1760,-340]
```

80/82及旧R2 manifest里的`[-1680,-350]`会使A4可见像素相对grid恒偏`[+80,-10]`。旧R2C测试只回读manifest自报值，没有用A4真实控制点与grid做外部联合校验，因此机器PASS不能排除此错。

### 2.3 美术导向板把格点误作格角

Runtime与A4生成器都把整数grid coordinate视为菱形cell中心。当前81号导向脚本却先对每格加`[0.5,0.5]`再求footpoint，使单位与footprint整体再向屏幕下方漂移20px。

禁止继续使用该算法。cell中心不得加半格；菱形边界由中心加`[(0,-20),(40,0),(0,20),(-40,0)]`得到。

### 2.4 A4旧对象拓扑不是当前G2对象空间

A4获批的是Demo派生源和六层方法，不是当前R2C对象坐标的最终真值。已确认：

| 对象 | A4旧像素/拓扑 | 当前G2唯一逻辑位置 |
|---|---:|---:|
| 墙挂盾 | `[11,10]` | `[14,10]` |
| 东侧撤离口 | `[31,4]` | `[31,7]` |
| 警戒设施 | `[25,5]` | `[27,8]` |

因此A4继续只作建筑、道路、材质、光色、共同canvas与遮挡控制责任源；不得把其旧state/object像素命名为当前对象。当前盾、撤离口、警戒设施、保护区、炮源必须是独立可定位层/Proxy，并服从当前Session/Resolver。

`MAP_STATE_LIGHTING`混合层在G2-A2可读作fixture registration输入，但默认不可见；它不能再次把旧盾位或旧状态带进当前画面。

## 3. 唯一联合变换

### 3.1 基础投影

```text
grid_size              = [32,18]
tile_half_px            = [40,20]
projection_origin_raw   = [-880,-170]
map_viewport_rect       = [0,58,1280,584]
canvas_size_px          = [2400,1350]
canvas_origin_raw_px    = [-1760,-340]
base_camera_center_raw  = [-720,350]
```

```text
raw(g) = projection_origin_raw
       + [(g.x-g.y)*40, (g.x+g.y)*20]

source_px(g) = raw(g) - canvas_origin_raw

effective_camera = lerp(base_camera_center_raw,
                        raw(frame.camera.focus_cell),
                        frame.camera.focus_weight)

screen(raw) = map_rect.center
            + (raw-effective_camera)*zoom
            + shake

layer_screen_top_left = map_rect.center
                      + (canvas_origin_raw-effective_camera)*zoom
                      + shake

crop_position_px = effective_camera
                 - map_rect.size/(2*zoom)
                 - canvas_origin_raw

crop_size_px = map_rect.size/zoom
```

任何Scene、测试、美术脚本或manifest不得独立硬编码另一套`crop`、`screen_top_left`或`grid_to_screen`公式。

### 3.2 校准Gold Frame

校准目标帧统一`focus_weight=1 / zoom=1 / shake=[0,0]`。自然播放可使用PerformanceDirector的连续focus weight、zoom与shake，但仍调用同一公式。

| 帧 | focus cell | effective camera | crop `[x,y,w,h]` | layer top-left |
|---|---:|---:|---:|---:|
| Base/无focus | n/a | `[-720,350]` | `[400,398,1280,584]` | `[-400,-340]` |
| A PLAN | `[19,10]` | `[-520,410]` | `[600,458,1280,584]` | `[-600,-400]` |
| A CONTACT | `[20.5,10.5]` | `[-480,450]` | `[640,498,1280,584]` | `[-640,-440]` |
| B PLAN | `[18.5,10]` | `[-540,400]` | `[580,448,1280,584]` | `[-580,-390]` |
| B CONTACT | `[20,10.5]` | `[-500,440]` | `[620,488,1280,584]` | `[-620,-430]` |

旧`[480,428] / [-480,-370]`不得再作为任何共同Gold Frame常量。

### 3.3 cell、footprint与pivot

- 整数grid point是cell中心；不得先加`[0.5,0.5]`。
- `footprint_bottom_center`继续采用：投影所有占用cell中心，`x=(min_x+max_x)/2`，`y=max_y+tile_half_y`。
- 同一对象的Sprite pivot、阴影、outline、遮挡patch与interaction socket必须从这一footpoint派生。
- A4 control mask必须先按同一`effective_camera/crop`取样，再与Actor alpha的局部dirty rect求交；Actor轮廓不能自行创造A4 roof/fade coverage。

## 4. 三个强制联合控制点

G2-A2-C1至少用以下A4真实source像素做外部联合验证；每项必须证明`source→screen`与`grid→raw→screen`逐像素误差为0：

| grid | A4 source pixel | Runtime raw |
|---:|---:|---:|
| `[0,0]` | `[880,170]` | `[-880,-170]` |
| `[15,11]` | `[1040,690]` | `[-720,350]` |
| `[20.5,10.5]` | `[1280,790]` | `[-480,450]` |

另须对馆守Z`[15,11]/2x2`、BREAKER`[20,13]/3x3`和Swarm01`[22,9]/1x1`验证footpoint、pivot与A4控制mask局部patch在同一画面坐标。

## 5. 若用户批准“保留当前R2C、重派生current-topology地图”的G2-A2-C1草案

只有用户批准86号推荐路线后，主程序-2才可继续写：

- `game-godot/content/**/g2_a2_visual_compositor/visual_compositor_profile.json`
- `game-godot/scripts/**/g2_a2_visual_compositor/visual_projection.gd`
- `game-godot/scripts/**/g2_a2_visual_compositor/local_occlusion_mask.gd`
- 专用pre-Scene测试、runner与`main-g2-a2-c1/**`证据

当前已写adapter/CompoundActor/overlay可保留WIP，但不得继续Scene、capture、性能宣称。

必须交：

1. 单一projection helper；测试、mask、未来Scene共同调用。
2. corrected canvas origin与动态camera/crop readback。
3. 上述三个A4控制点0px联合误差。
4. PLAN/CONTACT/B路/无focus五组派生值逐项相等。
5. 不加半格的1x1/2x2/3x3 footpoint测试。
6. A4 control mask真实输入SHA、动态crop、coverage交集、dirty rect与patch外alpha不变证明。
7. A4旧对象拓扑与当前对象Proxy分层；`MAP_STATE_LIGHTING.default_visible=false`。
8. 既有R2C-C1 resolver、Swarm01、A/B第二轮、T1–T5、音频与Canon非回归。

任何测试通过都只证明联合注册preflight，不证明Scene、视觉品质或真实资产。

## 6. 美术Call01裁决

`GF_PLAN_CLEANPLATE_CALL01_RAW_1672x941.png`保留，实际ImageGen预算记为`1/4`，但状态改为：

```text
INVALIDATED_AS_EXACT_TARGET_BY_P85
MATERIAL_LIGHTING_MOOD_DONOR_ONLY
```

原因：旧canvas origin、旧动态crop常量与半格footprint均错误；且实际像素中BREAKER仍读成普通低位四足/龟猿轮廓，并出现多于三只的小体。不得直接裁切、叠UI或当作PLAN target。

Art2在86号重新签收前不得生成Call02。恢复后必须先重做A PLAN/A CONTACT两张corrected guide，并从剩余`3/4`预算继续；不得把Call01计成成功母版。

## 7. 停止门

以下保持Blocked：

- A9.1-A6-S继续ImageGen或CONTACT图
- G2-A2 Scene、Actual Frame、性能完成宣称
- A9.1-A6-D
- A9.1-A7-J
- UA91
- A9.1-B
- signed handoff
- G2-B
- 默认入口、Runtime、Canon、付费批量、LibTV

当前唯一合法节点：

```text
U86_A4_LEGACY_VS_CURRENT_R2C_MAP_ROUTE_DECISION
```

若用户批准推荐路线，后续才是：

```text
U86
→ P85转为可派工
→ G2_A2_C1_JOINT_REGISTRATION_PREFLIGHT
→ 新编号制作人实际证据重新签收
→ A9.1-A6-S-C1 与 G2-A2 Scene并行恢复
```
