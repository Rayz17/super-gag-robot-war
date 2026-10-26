# C01E02｜战棋透视、交互与资产接口制作人纠偏

> 日期：2026-08-19  
> 状态：`CURRENT_PRODUCTION_INTERFACE / ART_STOPPED / UA91_BLOCKED / G2_B_BLOCKED`  
> 适用：C01E02 Candidate Demo、A4地图、A5及后续地图Sprite、Golden Turn第一轮  
> 不构成：Hard/Working Canon修改、UA91视觉批准、Runtime晋级、G2-B派工或付费批量生成

> 2026-08-19下游纠偏：78号已覆盖本文件中“A9.1-A6孤立双Pilot直接送UA91”的顺序及第8节旧DAG。本文件第1–6节与G2-A.1-R2几何接口继续有效；当前以78号Scene-First联合Gold Frame门为准。

## 1. 制作人裁决

用户指出的问题成立，而且是制作人接口失职，不是美术执行者应自行补全的常识题。

34号与59号虽然冻结了32×18网格、`tile_half=(40,20)`、多格占地和部分pivot，但没有把以下内容签成同一个可消费接口：

- 地图Sprite的固定绘制相机；
- 逻辑四向到屏幕四个斜向的映射；
- 设计turnaround与战术相机帧的用途边界；
- 多格单位anchor、footprint、bottom-center、pivot和z-sort；
- 每段路径的运动朝向、终点朝向、接触法线与受力／击退向量；
- 身体、盾、武器、命中点的视觉socket；
- A4六层地图与G2视窗的共同原点、遮挡和裁切规则。

因此，A9.1-A5把眼平正／侧／背turnaround裁成 `south/west/north/east`，以及G2-A.1夹具消费者机器通过，都不能证明资产能进入同一个战棋世界。

自本合同起：

1. A9.1-A5判为 `SOURCE_CORRECT / PURPOSE_WRONG / VIEWPOINT_PRECONDITION_FAILED / HISTORY_WIP_ONLY`；“四向可直接复用为地图Sprite”结论撤销。
2. `V10X → Q/SD四视图`仍是馆守Z当前正确身份、比例、配色和结构Candidate参考；不降级、不丢弃，也不再被当作地图帧直接裁切。
3. G2-A.1只保留resolver、T1–T5事件时序、40×20数学投影和夹具消费者证明；“可直接插真资产”结论撤销。
4. 美术、UA91、A9.1-B、exact handoff与G2-B保持冻结，直到本合同要求的程序校准证据和一对地图相机Pilot通过制作人实际像素预审。

## 2. 三种视觉空间必须分开

| `view_space` | 用途 | 相机规则 | 可否绑定地图单位槽 |
|---|---|---|---|
| `design_orthographic` | 机设、身份、比例、正侧背结构责任源 | 眼平正交turnaround | 否；只能作绘制参考 |
| `map_dimetric_40x20` | 战棋地图、移动、接触、受击、环境交互 | 本合同固定A4相机 | 是 |
| `screen_ui` | 通讯头像、HUD、意图与摘要 | 屏幕空间 | 否 |
| `cinematic` | LibTV、Cut-in、Peak Space | 可有镜头透视 | 否；必须从地图状态进入并回到同一状态 |

Runtime绑定必须显式携带 `view_space` 与 `camera_contract_id`，并拒绝把 `design_orthographic`、`screen_ui` 或 `cinematic` 文件绑定到 `map_dimetric_40x20` 槽位。

V10X Q四视图的正确角色是：锁身份、比例、结构、左右非对称、色块与材质。它不是四张地图相机帧。分开制作地图资产时，相机不动，只让机体在地面上旋转；四帧都必须是同一斜俯相机下的三分之四视图，不能出现纯正面、纯侧面或纯背面。

## 3. `A4_MAP_SPRITE_CAMERA_V1`

### 3.1 逻辑坐标与投影

- 网格：`32 × 18`。
- 世界轴：`+x=east`，`+y=south`，`-y=north`，`-x=west`。
- tile half：`(40,20)`；单格菱形为80×40。
- G2当前raw origin：`(-880,-170)`。
- 正投影：

```text
raw_screen_x = -880 + (grid_x - grid_y) * 40
raw_screen_y = -170 + (grid_x + grid_y) * 20
```

- 相机控制器只能在这个raw结果上做平移、聚焦、统一缩放与震动，不能改变投影轴。
- 视觉相机：固定平行轴测／2:1 dimetric，无消失点、无随地图纵深缩小。绘制等价参考为方位约45°、俯角约30°；上式和校准板是最终权威。
- 视点位于世界东南侧（`+x,+y`）看向西北地面；顶部必须可见。

### 3.2 方向映射

| 逻辑facing | grid delta | 屏幕向量 | 屏幕读法 | 固定相机下的主体读法 |
|---|---:|---:|---|---|
| `north` | `(0,-1)` | `(+40,-20)` | 右上 | 后部＋一侧的斜俯三分之四 |
| `east` | `(+1,0)` | `(+40,+20)` | 右下 | 前部＋一侧的斜俯三分之四 |
| `south` | `(0,+1)` | `(-40,+20)` | 左下 | 前部＋另一侧的斜俯三分之四 |
| `west` | `(-1,0)` | `(-40,-20)` | 左上 | 后部＋另一侧的斜俯三分之四 |

禁止：

- `south = 设计正面`、`north = 设计背面`、`east/west = 严格侧面`；
- 把north/east/south/west画成屏幕上／右／下／左；
- 对馆守Z右肩旧伤或BREAKER X非对称叠片做无语义镜像；
- 在地图不同Y位置对单位做探索场景式透视缩放。

A5小体四向是现存正确投影范例；A4本身是地图相机范例。纪存早期走动条证明的是“先锁场景相机，再画稀疏帧，由程序补运动”，不是A4地图角度范例。

### 3.3 光照与画法

- 常态地图Sprite继续服从CML128 `KINETIC_CEL`。
- A4共同光向不随单位朝向改变；顶面中亮，屏幕右向立面较亮，屏幕左向立面较暗。
- 深墨蓝轮廓与有限硬色阶；不把商品渲染软渐变直接缩成地图成品。
- 竖直结构需表现固定俯视缩短与可见顶面；不得靠二维倾斜伪造眼平图中不存在的顶面信息。

## 4. 多格单位注册、尺寸与遮挡

### 4.1 anchor与footpoint

- 逻辑 `anchor` 是占地矩形的最小格／左上逻辑格；占地向 `+x,+y` 生长。
- 逻辑碰撞仍按完整footprint：馆守Z `2×2`，BREAKER `3×3`，小体 `1×1`。
- 可见Sprite唯一注册点为整个footprint投影后的 `footprint_bottom_center`，不是anchor格中心。
- 复用M2已证明算法：遍历占地格中心，取最小／最大screen-x与最大screen-y，返回 `((min_x+max_x)/2, max_y+tile_half_y)`。
- 帧内pivot必须表示同一个接地点；每帧交付normalized pivot与pixel pivot，动作帧不得漂脚。
- 阴影、脚、履带或承重前肢必须与同一地平面接点闭合。

### 4.2 尺寸

- A5小体96px为已批准Demo来源。
- 馆守Z256、BREAKER384仅保留为当前Candidate画布／占位尺度，须在统一相机校准板内复验，不等于旧像素获准复用。
- 应急车128为当前审查尺度；其正式地图视角仍须遵循本合同。
- 禁止以单张PNG的bbox或画布中心代替可见占地、身高和接地点验收。

### 4.3 z-sort与地图层

- 单位与可遮挡物统一按 `footpoint.screen_y + explicit_z_bias` 排序，不能按anchor y或“单位类别”固定层级决定前后。
- A4六层保持共同2400×1350 canvas；每层必须共享origin、pivot、world rect与mask语义。
- G2当前1280×720视窗与A4共同canvas的exact origin／裁切映射尚未证明，状态为 `BLOCKED_UNTIL_A4_LAYER_REGISTRATION_PROOF`。
- 屋顶、前景与巨型机体采用哪一种fade／cutout／occlusion mask，必须由程序校准任务给出同图证据；在此之前不能让美术猜。

## 5. 交互几何必须驱动画面

### 5.1 路径与朝向

- 每一段移动的朝向由相邻waypoint delta计算。
- `final_facing`只在抵达终点后的转身／站定帧生效，不能套在整条route上。
- 路线带、2×2幽灵、朝向扇面、移动Sprite与提交摘要必须使用同一组投影向量。
- 输入继续表达世界cardinal；UI必须把它投影成右上／右下／左下／左上，不能把north伪画成屏幕上。

### 5.2 接触、受力与socket

每个高关注接触姿态必须在exact handoff中同时给出：

- `approach_grid_vector`与其projected screen vector；
- `body_socket_px`、`shield_socket_px`、`weapon_socket_px`、`impact_socket_px`；
- target socket；
- `impulse_grid_vector`、recoil screen vector与post-contact anchor；
- 对应的state、facing、frame rect、hold与fps。

网格矩形相邻只证明逻辑接触，不证明两张Sprite在画面上没有隔空或穿插。FX必须从同一impact socket发射，路裂、碎屑、后滑、倾斜和相机震动必须沿同一受力向量。

### 5.3 当前Golden Turn冲突

当前R1 fixture中，馆守Z `[18,10]` 的2×2与BREAKER `[20,11]` 的3×3沿东西侧形成接触，但表现标签却是馆守Z`south`、BREAKER`north`；它与57号“馆守Z正面承接、BREAKER南向北冲”的第一读法不闭合。

本合同不擅自选择新舞台调度。主程序窄纠偏必须先提交：

1. A/B实际route的逐段facing；
2. 双方footprint接触边与法线；
3. approach、impact、impulse/recoil和post-contact anchor；
4. 一张使用校准proxy的同地图动画／逐帧证据；
5. Reader语义与网格几何一致性断言。

在该证据签字前，馆守Z／BREAKER的正式move、brace、contact、recoil、side-hit帧全部阻断。

## 6. 第一轮稀疏生产范围

第一轮不制作 `state × facing × frame` 的完整笛卡尔积。具体组合见 `c01e02-golden-turn-r1-map-visual-state-matrix-v1.tsv`。

程序／FX承担：选择轮廓、脚底环、幽灵、路线带、正确投影的朝向扇面、位置补间、短bob、hit-stop、闪白、相机震动、碎屑、雨水、独立红缝发光与炮线。它们不能替代高关注接触姿态，但也不应被重复画进每张Sprite。

美术只在几何关闭后制作Golden Turn真正出现的方向／状态：

- 馆守Z：先做一个 `map_dimetric_40x20` idle相机Pilot；通过后才扩规划所需四向idle与实际路径的最小步态。
- BREAKER：先做同一相机下、由B＋X责任源派生的一个方向Pilot；接触状态等程序法线签字后再做。
- A5小体：既有四向idle可继续作正确相机范例；只补实际路径使用的稀疏动作。
- 应急车：只做第一轮实际east方向；不能把纯侧视车辆贴回A4。
- 路损、警戒设施、炮线与红缝：按地图层／独立FX处理。
- 第一轮巨体接触留在滚动战棋地图；LibTV不能用来遮掉错误的地图入口／出口姿态。

## 7. 下一道校准门

### G2-A.1-R2：几何消费者纠偏（仍非G2-B）

必须证明：

- facing fan经过40×20投影；
- route逐段朝向正确，终点朝向独立；
- 2×2／3×3按footprint bottom-center注册；
- manifest pivot被实际消费；
- z-sort以footpoint为准；
- A4六层exact origin／裁切／遮挡映射成立；
- 接触法线、socket、FX与击退向量同源；
- binding拒绝错误 `view_space`／`camera_contract_id`。

该任务只可使用校准proxy，不接入真实馆守Z／BREAKER资产，不开放G2-B。

### A9.1-A6：统一相机双Pilot（由78号改为内部派生门）

在G2-A.1-R2证据通过后，美术只交：

1. 馆守Z一个地图idle方向；
2. BREAKER一个地图idle／charge-ready方向；
3. 同一A4位置、相同光向、footpoint、阴影和遮挡的100%／50%对照板；
4. 设计责任源并排板，证明身份未漂移；
5. `view_space`、`camera_contract_id`、pivot、footprint与来源SHA。

任一主体出现眼平纸片、不同相机、比例／身份漂移或程序图标感，即停，不扩四向或动作。

上述双Pilot不再是UA91的直接送审物。它只能在78号整屏场景目标通过制作人预审后，作为可拆资产内部Pilot生产，并必须重新组成`GF_PLAN_RECOMPOSED`／`GF_CONTACT_RECOMPOSED`整屏实际帧后再进入UA91。

## 8. 联合DAG与停止门

```text
76接口冻结
→ G2-A.1-R2校准proxy证明
→ 制作人签几何消费者回执＋接触舞台裁决
→ A9.1-A6-S整屏场景目标Lookdev
  ↘ G2-A.2视觉合成系统proxy（可并行）
→ A9.1-A6-D最小可拆资产Pilot
→ A9.1-A7-J GF-PLAN／GF-CONTACT联合重组
→ 制作人整屏实际像素预审
→ UA91用户联合画面裁决
→ exact interface冻结
→ A9.1-B可组合实物
→ 制作人signed handoff
→ G2-B只整合45–75秒第一轮Golden Turn
→ UGT用户试玩
```

当前禁止：继续A9.1-A5裁图、完整四向全状态Atlas、真实接入、G2-B、付费LibTV、默认入口替换、Hard/Working Canon修改。

## 9. 权威与证据

- 当前Canon继续负责馆守Z／纪存等身份、比例、物理尺度和剧情承诺；本文件只补Candidate生产接口，不篡改Canon。
- A4地图与A5小体的用户批准继续有效；它们是统一地图相机的正例。
- V10X Q谱系恢复继续有效；75号只有“直接裁成地图四向”的用途结论被本文件覆盖。
- G2-A.1-R1 `real_art_loaded=0`与夹具PASS继续是内部工程证据，不是产品视觉验收。
