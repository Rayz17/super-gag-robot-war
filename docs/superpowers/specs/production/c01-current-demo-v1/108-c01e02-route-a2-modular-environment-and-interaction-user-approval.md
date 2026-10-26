# C01E02 U108｜路线A2：模块化精品环境与交互式遮挡用户批准

日期：2026-08-21  
责任人：用户／制作人-2  
状态：`USER_APPROVED_ROUTE_A2 / MODULAR_ENVIRONMENT / CAMERA_A0_REQUIRED / NO_GENERATION_YET / CALL03_FALSE / CALL04_FALSE`

## 1. 用户裁决与本次修正

用户同意继续路线A，但明确补充：

> 地图视角不应把“45度”当成精确参数；建筑和自然元素要有机战地图的存在感与玩法比例，但不应烘死在环境图中。建筑／物件应作为独立资源放置，遮挡单位或路线时再由光标／焦点触发半透明。

制作结论：该要求属于游戏交互合同，不是美术后处理。107号原路线A的“整张环境母图生成后再拆建筑／roof”方法被本文件取代；107号所批准的**一份额外环境专用预算**保留，但在相机A0与独立对象交互Pilot通过前不得执行。

本路线完整包含：

1. 精品模块化环境；
2. BREAKER北向地图母版；
3. 馆守Z东向地图母版；
4. 复用现有小体正例与确定性对象层，完成PLAN重组；
5. PLAN通过后再做CONTACT、稀疏动作、最终性能与真人试玩。

## 2. 调研后的产品判断

### 2.1 相机不是“精确45度”，而是可读性参数

等距／二测地图的格子纵横比本身就在模拟俯角。Unity官方文档明确区分2:1 dimetric与更接近真等距的比例，并允许通过格子Y比例改变投影视感。由此推断：当前`40×20`只是一个候选视角，不是不可变的美术定律。

本项目先做三档同拓扑对照：

| 候选 | tile half | 产品含义 |
|---|---:|---|
| V1 | 40×20 | 当前约30°低俯视基线 |
| V2-A | 40×24 | 中等抬高，保留机体侧面体量 |
| V2-B | 40×26 | 更高俯视，降低建筑遮挡 |

表中的角度只作视觉标签，最终权威仍是投影公式与实机截图，不把近似角度反写为玩法真值。

### 2.2 战术物件必须与地面分责

Fire Emblem、Triangle Strategy、Tactics Ogre等战棋产品都把地形、位置和高低／阻挡关系作为战术读法的一部分；Godot也支持把可交互场景对象独立实例化，而不是只能烘进TileMap。由此确定本项目的最小分层：

```text
GroundBake（道路／排水／场地纹理／轻微预烘光影）
  ├─ StructureInstance × 6（独立建筑／断桥）
  ├─ TacticalObject（盾／东门／警戒设施／炮源提示）
  ├─ Actor（馆守Z／BREAKER／车／小体）
  ├─ FX（雨、湿地反光、接触水花）
  └─ UI／路线／ghost／通讯
```

任何会参与阻挡、选中、状态变化、遮挡或“借题打法”的物件，都不得烘进GroundBake。有体积的树、巨石等自然物同样按StructureInstance／MapObject处理；只有不产生体积遮挡的平面植被可以进入GroundBake。

### 2.3 机战式遮挡优先简单、明确、可预测

最终方案不建设逐像素轮廓、SubViewport、实时法线或通用动态灯光。每个独立建筑／物件仅有两部分：

- `foundation/body`：保持可见，告诉玩家它占了哪些格、能否通过；
- `occluder`：屋面／高立面，必要时整件淡化。

单位与建筑按同一地面脚点Y排序；真正遮住当前关注内容时，唯一`OcclusionRevealController`只改变该件`occluder`的alpha。Godot的CanvasItem/Y-sort/Z顺序足以承担这个目标，不再把战棋棋盘做成渲染技术项目。

## 3. Route A2冻结的环境资产结构

### 3.1 GroundBake

只含：

- 主路、撤离线、广场铺装、排水、积水与克制的预烘反光；
- 不改变passability的低矮地面装饰；
- 统一的雨夜冷蓝灰值域与东门方向青色引导。

禁止含：建筑、断桥、盾、东门、警戒设施、炮、小体、车辆、巨体、路线、UI、文字、未来时态FX。

### 3.2 独立StructureInstance

首包固定为Current topology的六项：

| object_id | footprint source | 首轮职责 |
|---|---|---|
| NW_BLOCK | `[1,0,7,5]` | 西北街区边界／远景框景 |
| NM_BLOCK | `[10,0,5,4]` | 中北建筑，控制上缘空间 |
| NE_BLOCK | `[22,0,7,4]` | 东门前场背景与炮源方向 |
| SW_BLOCK | `[0,15,8,3]` | 近景遮挡测试／广场边界 |
| SE_BLOCK | `[26,14,6,4]` | 东南街区与撤离方向收边 |
| BROKEN_SKYWALK | `[8,5,7,2]` | 万机馆破损叙事与局部遮挡 |

每项至少包含：

`object_id / anchor / footprint / pivot / front_edge_footpoint / z_bias / foundation_sprite / occluder_sprite / visual_bounds / reveal_cells / gameplay_tag / state`

首轮只冻结“硬阻挡、路径塑形、场景地标、局部显隐”四项语义，不暗加建筑HP、掩体命中率、LOS、高低差伤害、破坏链、推动或室内楼层系统。

### 3.3 Stateful TacticalObject

墙挂盾`[14,10]`、东门`[31,7]`、警戒设施`[27,8]`、保护区`[20,5,12,7]`与炮源`[29,2]`继续读取Session／Resolver公开态，独立于地面和建筑资源。A路设施受损／路损42与B路设施保全／路损24必须在地图上兑现，不能只留在数字卡。

ENV-A1同一次模块Kit调用必须把墙挂盾、东门、警戒设施及道路损伤overlay做成**隔离面板／独立资源关系**，不得烘入GroundBake或六栋建筑；炮源在首轮继续只交确定性edge cue，不要求画面内炮塔。若一次Kit无法让这些对象达到产品级，P102应诚实停门并单列对象资产缺口，不得拿程序图冒充正式像素。

## 4. 焦点驱动显隐合同

### 4.1 视觉状态

- `OPAQUE`：alpha 1.00；
- `REVEALED`：目标alpha 0.34，允许验收区间0.30—0.40；
- `RELEASE_HOLD`：原因消失后短暂保持，再恢复。

建议节奏：90ms淡入透明、100ms保持、160ms恢复。相同格／相同签名不重启Tween。

### 4.2 触发原因与优先级

```text
执行主体被挡
  > 已选单位被挡
  > 当前路线／终点ghost被挡
  > 正在查看建筑自身（保持不透明并高亮）
  > 光标所指内容被挡
```

- 鼠标悬停只在跨越grid cell时更新presentation focus，不写Session；
- 手柄复用现有战术光标；鼠标与手柄指向同一格时必须得到同一组淡化对象。现有键盘没有格光标移动，本Pilot只做输入不退化，不额外发明键盘光标；
- 如果玩家正在查看建筑自身，建筑保持不透明；若建筑后同时有已选单位或执行主体，则后者可读性优先；
- CONTACT／hit-stop期间，挡住双方的建筑保持透明到动作读清后再恢复；
- 同屏目标是通常只淡真正相交的1—2件，不允许全图“呼吸”；若确有第3件同时遮挡，不得为满足数字而漏掉。

### 4.3 排序和遮挡边界

- 建筑、物件、1×1／2×2／3×3单位统一按`front_edge_footpoint.screen_y + z_bias`排序；
- foundation始终可见，不能因淡化让阻挡范围消失；
- Controller只改occluder alpha，不改Actor alpha、Atlas region、阴影、材质或Session状态；
- 禁止第二套遮挡owner、逐像素mask、SubViewport、轮廓shader、实时动态光照。

## 5. 相机A0先行门

正式环境和两台机体母版开工前，主程序-2先在同一Current topology、同一演员状态、同一UI和同一玩法结果下制作`40×20 / 40×24 / 40×26`三档对照。

每档至少提供：A PLAN、B PLAN、A CONTACT、B CONTACT。验收只回答四个问题：

1. 巨体仍有足够侧面体量和重量，未变成俯拍棋子；
2. 选择口袋、撤离线、东门和BREAKER北冲轴在3秒内可读；
3. 建筑正常态有存在感，透明态能完整读出单位／路线／接触；
4. UI安全区与CONTACT镜头不因视角抬高而破坏。

相机A0只产出对照和用户选择，不自动把任一数值晋级为Camera V2。用户／制作人签选后，才更新正式投影、方向屏幕向量、crop、sprite画法、socket屏幕位置和环境导向。

## 6. 后续唯一合法生产链

```text
U108 路线A2批准
  → C4 相机A0＋独立建筑＋焦点显隐Pilot
  → P109 用户／制作人选择Camera V2
  → C4B Camera V2精确接口重注册（投影／crop／pivot／socket／A5兼容性）
  → ENV-A1 一次环境专用调用：模块化环境＋独立战术物件Kit，不是整屏场景
  → P102 环境50%／100%审查
  → Call03 BREAKER north
  → Call04 馆守Z east
  → 确定性PLAN重组（复用现有小体）
  → PLAN 3／10／30秒＋50%／100%审查
  → CONTACT与稀疏动作
  → 真实资产60fps与真人试玩
```

ENV-A1只允许一次额外环境专用调用，不挪用Call03／Call04；无自动reroll。目标是**模块化环境Kit母板**：地面材质／道路语言、六项建筑资源、少量低矮装饰，以及盾／东门／警戒设施／道路损伤overlay的隔离资源关系，不生成任何角色。exact摆放、排序、对象状态选择、路线和UI仍由Godot确定性完成。

## 7. 不随路线A2改变的玩法真值

以下全部保留：32×18逻辑网格、Current anchors与passability、A/B最短路线族、T1—T5时序、A/B接触边／socket世界点、热量／余量／设施／路损结果、第二轮写回、R2C Resolver／Session／PerformanceDirector。

需要重新冻结的是视觉接口，而不是玩法几何：tile_half_y、screen vector、相机crop、建筑资源pivot、单位地图画法、局部遮挡与UI安全区。

任何新增建筑玩法效果、移动物件坐标、改路、改接触或改A/B结果，必须另开玩法门。

## 8. 当前授权边界

本文件现在授权：

- 路线A2方法；
- 一份额外环境专用预算继续保留；
- 主程序-2执行零美术的相机／独立对象／焦点显隐Pilot。

本文件现在不授权：

`environment_ImageGen_execution / Call03 / Call04 / real_art / UA91 / G2-B / Default / Save / Runtime / Canon`

## 9. 外部调研来源

- Unity官方等距Tilemap说明：<https://docs.unity3d.com/es/current/Manual/Tilemap-Isometric-CreateIso.html>
- Godot CanvasItem排序／透明属性：<https://docs.godotengine.org/en/stable/classes/class_canvasitem.html>
- Godot TileSet与scene tile：<https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html>
- Nintendo《Triangle Strategy》战术与地形提示：<https://www.nintendo.com/us/whatsnew/tips-for-getting-started-with-triangle-strategy/>
- Nintendo《Fire Emblem Engage》：<https://www.nintendo.com/en-gb/Games/Nintendo-Switch-games/Fire-Emblem-Engage-2267157.html>
- Square Enix《Tactics Ogre: Reborn》：<https://tactics-ogre.square-enix-games.com/en-us/>
- Bandai Namco《Super Robot Wars 30》：<https://en.bandainamcoent.eu/super-robot/super-robot-wars-30>

以上产品用于验证“战术地图可读性、地形与定位、地图战术层和攻击演出分责”的方向；本文件中的具体相机档位、alpha和任务拆分是制作人基于本项目约束作出的推导，并非这些产品的公开参数。
