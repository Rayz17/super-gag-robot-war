# C01E02 A9.1-A6 ENV-E0｜Current-Topology精品环境零生图派生目标书

日期：2026-08-20  
任务ID：`A9_1A6_ENV_E0_CURRENT_TOPOLOGY_ENVIRONMENT_DERIVATION`  
执行者：美术资产-2  
状态：`OPEN_ZERO_GENERATION_ENVIRONMENT_DERIVATION / CALL03_FALSE / CALL04_FALSE`

## 1. 唯一任务

不用ImageGen、不画机体、不接Godot，把已签current-topology几何与Call02仅存的六块无语义雨夜环境donor，派生成一套可审、可分层、可按四组current相机0px重组的2400×1350环境Candidate。

本任务不是用Python原语“画一张地图”，也不是把Call02或旧A4整屏贴回来。脚本只允许做：权威几何mask导出、既有高质量像素的裁切／遮罩／翻转／错位重组、受控去重、色阶与CML128色块化、图层包装和机器校验。任何需要重新设计建筑、机体或语义对象的缺口必须停回制作人。

## 2. 冻结输入

必须先逐项核对绝对路径与SHA：

- Task98环境层合同：`art-a9-1a6-s-c2-sprite-first-map-camera-masters/environment-layer-contract.json`，SHA `ed683edc21dfde7b92ea3625e59892667694dd850ef49487a5962a19b818126b`；
- Task98 donor裁片表与sheet，均须由Task98 `delivery-hashes.sha256` SHA `41f5ba27a5b12088e84424c73e4fd6aa6aa93ba2bd7285e4bcb8eb94a94e50be`闭合；
- current topology：`game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/golden_slice_profile.json` SHA `61b49e5328e702cd654d28ff39c5c380ba0ae3e78753330635036d33f689523c`；
- current地图合同：`.../g2_a2_visual_compositor/current_topology_map_contract.json` SHA `74c6bbb3f732a61d3ed5a55d9c209b628152b9411395339d665aeeb0d76ab875`；
- tactical interface与生产看板使用派工时最新制作人SHA；
- P98制作人签收：`100-c01e02-g2-a2-c2-producer-playability-preflight-acceptance.md`。

Call02整屏、所谓cleanplate、所有单位／车辆／盾／东门／设施及其阴影反射只属于History，不得作为current可见像素。旧A4六层只能借投影和遮挡方法，`a4_visible_pixels_allowed=false`。

## 3. 唯一写域与调用边界

只允许新建：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a6-env-e0-current-topology-environment/**`

禁止修改生产看板、interface、Task98、Call02、Godot、Canon或其他任务目录。`ImageGen=0 / libtv generation=0 / Call03=false / Call04=false / real_art_loaded=0`。

## 4. 必交ENV-E0／E1／E2

### 4.1 ENV-E0：current几何与相机责任

- 机械导出32×18、40×20、raw origin `[-880,-170]`、world canvas origin `[-1760,-340]`；
- 分别导出道路、建筑block、选择口袋`[15..20,9..11]`、BREAKER承力大道`x20..22/y11..15`及两侧一格肩带、保护区、对象anchor和不可放置区mask；
- 共同PLAN camera `[-480,420]`、CONTACT A `[-480,450]`、CONTACT B `[-500,440]`和NO_FOCUS／base相机的crop readback；
- 至少三个grid→raw→canvas→screen控制点误差≤0.5px；
- mask本身不可作为可见产品图。

### 4.2 ENV-E1：无语义材质模块

只从Task98登记的六块Call02 donor派生：

- 湿路／积水／路标／裂纹；
- 路缘／工业立面；
- 屋顶／排水／女儿墙／前景遮挡。

交付模块atlas、每块父裁片坐标与SHA、变换日志、重复度热图、50%缩略图。不得继承donor的建筑轮廓、坐标、灯位或任何语义对象；不得出现单位、车辆、盾、门、设施、文字或旧救援线。

### 4.3 ENV-E2：2400×1350可见分层Candidate

共同canvas／origin输出：

1. `BASE_GROUND_OPAQUE_2400x1350.png`，z=-1200；
2. `BUILDINGS_WORLD_BODY_RGBA_2400x1350.png`，z=-900；
3. `ROOF_RGBA_2400x1350.png`，z=900；
4. `FOREGROUND_RGBA_2400x1350.png`，z=1100；
5. `OCCLUSION_CONTROL_RGBA_2400x1350.png`，不可见控制层，R=fade、G=outline、B=fringe、A=coverage；
6. `WETNESS_EMISSIVE_CONTROL_RGBA_2400x1350.png`，只作运行控制，不烘未来天气或状态；
7. PLAN／CONTACT A／CONTACT B／NO_FOCUS的1280×720 cleanplate重组帧及50%版；
8. layer toggle、共同origin、alpha边界、重复度与旧像素污染receipt。

北侧建筑承担纵深；南侧保持低矮，不遮BREAKER冲线。选择口袋和接触区不得放建筑、废墟、灯柱或看似可碰撞陈设。东侧生命线用低位实体灯、路缘和出口方向形成，不把整个保护区刷成UI荧光矩形。

本任务不画current盾、东门、警戒设施、车辆或机体。它们必须保持透明空位并由后续独立stateful对象／actor层承担。

## 5. 制作人视觉门

### 50%／640×360

- 3秒能读出中央承接大道、东侧生命线、南侧冲线与西侧盾钩子所在空间；
- 车辆线、小体扑线与BREAK​ER冲线叠回几何overlay后可同时辨认；
- 选择口袋和接触区无遮挡；
- 不出现明显重复贴图、灰盒网格感、程序原语感或旧A4拓扑；
- 环境不抢机体／交互overlay第一焦点。

### 100%／1280×720

- 路缝、路缘、建筑边、屋顶严格服从2:1 dimetric，无透视跳变；
- 四组crop无空洞、接缝、重复花纹和相机漂移；
- CML128的4–7大色块、最多两级硬阴影成立，不退成高噪点半厚涂照片纹理；
- roof／foreground可由局部mask控制，不能整层50%淡化；
- 无旧盾／旧门／旧设施／旧救援线、无双阴影／双反射、无T3–T5未来状态烘死。

任何50%门失败，先返修空间和材质装配，禁止用额外生成掩盖。若100%只剩current交互物件／车辆缺少产品像素，停在预算门，由制作人决定额外一次非批量生成或人工2D，不得挪用Call03／04。

## 6. 完成态

只能自报：`ENVIRONMENT_LAYER_CANDIDATE_FOR_PRODUCER_50_100_REVIEW / IMAGEGEN_ZERO / NO_STATEFUL_OBJECTS / NOT_RUNTIME / FUN_NOT_PROVEN`。

完成后停回制作人；不得自行接Godot、合成机体、开放Call03／04、UA91、G2-B、Runtime或Canon。
