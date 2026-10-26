# C01E02 A9.1-A6-S-C1 Call02｜Current-Topology共享PLAN Look Target任务书

日期：2026-08-20  
任务ID：`A9_1A6_S_C1_CURRENT_TOPOLOGY_SCENE_LOOKDEV / CALL02`  
状态：`DISPATCHED / CALL02_A_PLAN_ONLY / CALL03_FALSE`

## 1. 唯一任务

使用剩余ImageGen预算中的一次Call02，制作 **A/B共享物理世界** 的current-topology PLAN整屏视觉目标。先交无UI cleanplate，再用确定性UI／路线／ghost合成产品帧，停在制作人视觉预审。

本任务不生成A CONTACT，不重画设计，不拆Sprite／Atlas，不接Godot，不进入UA91或Runtime。A/B PLAN的物理世界相同，不能浪费一次生图去生成B PLAN。

## 2. 解门输入锁

- 94号制作人回执必须存在且逐字包含`CALL02_ALLOWED=A_PLAN_ONLY`；
- Tactical interface `1.6.2`：`8fdad825167723a0b6180d4cd86dfbb02262865e11483db3334af1a50ccadd99`；
- 当前看板：`a87862e59b226cf398e72a6fabcfd9e4ae2452de0a05b1421319ecd279e7aebb`；
- 90号预生产目标：`67332c6d9644ca0fbcf42aac1a850717201496d34ec0808e4c3013eae9fe4898`；
- 91号预生产验收：`470b7180ee4dccee2f25dca7653b290f8e363399db3ed1cba4b0d6a4f7bb8e6d`；
- 预生产11项哈希：`e2710ce24214cdb96ca647c3ffe1fa8e0db0867fa918a7531b34962e04ed07a9`。

任何输入不符即停，不得自行换参考。

## 3. ImageGen唯一四图输入

顺序即职责优先级；不增加第五张：

1. **Exact current-topology PLAN raster guide**  
   `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a2-c1/captures/02_EDITABLE_DRAFT_A.png`  
   SHA `2bd9fa53a575ddafcc0c63a7557924d1fc5bb509a2b42966ae08bc0da5708fe1`  
   只继承camera、crop、2:1投影、道路／block、实体与对象脚点、占地、前后关系及安全区；忽略所有Proxy造型、文字、UI、路线、ghost和颜色。
2. **唯一安全身份／画法板**  
   `art-a9-1a6-s-c1-current-topology-scene-first/identity-style-safe-board.png`  
   SHA `dc473235883669165e0eef58ce8c9d390e719e946e133648893b7d0ca83f3276`  
   馆守Z只取V10X区；BREAKER只取B body＋X surface；CML128区`STYLE ONLY / IGNORE ANATOMY`。
3. **A4 donor-only地图语言板**  
   `art-a9-1a6-s-c1-current-topology-scene-first/map-language-board.png`  
   SHA `4776660f7ab282f1434286e6670f080256b56a3208f2f5a0d13b754b78797819`  
   只取暗值、雨湿、建筑分面、屋顶边灯与局部遮挡方法；严禁旧坐标、旧盾、旧出口、旧设施和旧救援线。
4. **唯一小体地图相机身份**  
   `art-a5-rift-swarm-four-facing-atlas/A5_RIFT_SWARM_A_IDLE_96_384x96.png`  
   SHA `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b`  
   只约束当前三只小体，不得增加。

`00_JOINT_REGISTRATION_CONTROL`与`10_LOCAL_OCCLUSION_METHOD`只作QA，不作ImageGen参考；Call01、旧unsafe identity board与任何A9/A3/SVG/Blender机体永久禁用。

## 4. Call02 cleanplate exact合同

只生成一张`PLAN_SHARED_CURRENT_PHYSICAL_CLEANPLATE`，最终交付为1280×720：

- `32×18 / tile_half=[40,20] / 2:1 orthographic dimetric`，约45°方位、30°俯视；禁止透视汇聚、按y缩放与眼平纸片；
- `canvas_origin=[-1760,-340]`；共同PLAN camera=`[-480,420]`；map viewport=`[0,58,1280,584]`；
- 馆守Z`[15,11]/2×2/east`，BREAKER`[20,13]/3×3/north`，应急车`[17,10]/east`；
- 小体01`[22,7]/west`、02`[26,12]/north`、03`[29,5]/south`；
- 墙挂重盾`[14,10]`、东门`[31,7]`、警戒设施`[27,8]`、保护区`[20,5,12,7]`；炮源`[29,2]`保持画外；
- 所有单位以`footprint_bottom_center`接地，共地面阴影、按footpoint y排序；屋顶只做局部fade／cutout；
- `[15..20,9..11]`选择口袋与BREAK​ER五格承力大道无遮挡；东门为主地标，西侧破墙／墙挂盾为次地标；
- 地图采用中低明度蓝灰雨夜；东门青色安全反光与BREAKER红缝危险方向分离；馆守Z胸炉与大色块必须从湿地中读出。

cleanplate绝对禁止：文字／伪字、UI、路线、ghost、footprint框、朝向扇面、edge cue、T3接触、T4炮击、T5赤红／完整翻路、额外单位、机体重设计。

馆守Z必须是V10X双臂、无翼、无背包；BREAKER必须是B前肢承重半直立身体＋X异质闭合生体甲，禁止龟／猿／普通四足／装甲车轮廓。

## 5. 确定性整屏合成

ImageGen只交物理cleanplate。美术任务必须另交一张`GF_PLAN_A_INTEGRATED_LOOK_TARGET_1280x720.png`，使用现有确定性overlay/UI模板合成：

- 顶部`y=0..57`：唯一目标＋三威胁；地图`y=58..641`；底部`y=642..719`：五时点；
- 纪存通讯位于左下安全区、宽度不超过320px，不挡馆守Z、路线或选择口袋；
- 一次只显示当前A草稿路线与`[20,9]/south`终点ghost；BREAKER`[20,11]`只作敌方意图ghost；
- A：正面承接、热24、第二轮68／余量1；设施受损、路损42；
- B对照：设施保全、路损24；热46、第二轮88／余量0；
- 产品图不得出现`ROUTE FAMILY / east / south / damaged / active / R2 / HUD FORECAST ONLY`等制作或英文术语；
- UI、路线、文字、ghost与edge cue必须可独立开关，不得烘回cleanplate。

## 6. 必交与预算

1. `CALL02_A_PLAN_RAW.*`与原始工具回执；
2. `PLAN_SHARED_CURRENT_PHYSICAL_CLEANPLATE_1280x720.png`；
3. `GF_PLAN_A_INTEGRATED_LOOK_TARGET_1280x720.png`；
4. 无UI／仅UI／仅路线／仅ghost的确定性分层或重组回执；
5. generation log：逐项登记实际四图路径／SHA、prompt、调用次数、输出SHA与失败项；
6. `call-budget-receipt.json`：Call01历史1次、Call02本次1次、剩余2次、`Call03=false`；
7. delivery hashes与完成报告。

所有输出标记：`NON_SEPARABLE_CANDIDATE_LOOK_TARGET / NOT_SPRITE / NOT_ATLAS / NOT_RUNTIME / real_art_loaded=0`。

## 7. 制作人视觉门

- **3秒：**能读出车先过、三小体扑东门、BREAKER北冲、馆守Z去挡；
- **10秒：**能分清车／三小体／东门／设施／墙挂盾／两巨体，并追出当前路线、终点ghost与PLAN→摘要关系；
- **30秒：**能复述A保机体余量但城市／路受损，B保城市但高热零余量，且T3／T4／T5仍是forecast；
- **50%：**先看整屏关系、身份、地标、路线和UI层级；
- **100%：**再查V10X无翼背、B＋X结构、四肢、脚点、遮挡、材质、无伪字与无身份拼接。

## 8. 一票停止门

出现任一项即判Call02失败并停，不得自动消耗Call03／04：旧A4拓扑回流、错相机／自由透视、馆守Z或BREAKER身份拼接、对象移位、额外小体、选择口袋被堵、UI／路线／未来时态烘入、50%第一读法不成立。

只有Call02成为可修基础并经制作人签收，同时96号交互预审通过，才另发Call03。Call04最多一次，只修单一局部缺陷；若前两张均通过且无需纠偏，才优先考虑B CONTACT。

