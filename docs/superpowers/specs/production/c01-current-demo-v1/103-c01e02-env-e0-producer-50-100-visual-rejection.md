# C01E02 ENV-E0｜制作人50%／100%视觉拒收回执

日期：2026-08-21  
责任人：制作人-2  
状态：`ENV_E0_GEOMETRY_AND_LINEAGE_RETAINED / ENV_E1_E2_VISUAL_REJECTED / ZERO_GENERATION_ENVIRONMENT_ROUTE_DISPROVEN / CALL03_FALSE`

## 1. 裁决

Task101 的几何、相机和来源链机械闭合；E1材质模块与E2可见六层未通过产品视觉门，不得作为Current精品地图Candidate、ImageGen整屏参考、Godot可见层或UA91母版输入。

签收状态只能是：

`MECHANICAL_GEOMETRY_PASS / VISUAL_50_PERCENT_FAIL / VISUAL_100_PERCENT_FAIL / OVERALL_FAIL / NOT_CONSUMABLE`。

## 2. 已核输入与实际查看范围

- 完成报告：`art-a9-1a6-env-e0-current-topology-environment/completion-report.md`，SHA `513c1be53ccb9011fe270bfb1884f92c5338e5559c533320f4206290b5634951`；
- delivery manifest：`delivery-hashes.sha256`，SHA `0c045511d85a440573135ba9f060a5bd6d814be6c7b202bbf18611563524d1a9`；85项逐项哈希通过，非缓存文件与manifest集合无差异；
- PLAN cleanplate，SHA `e5c04dc37ff6bbb5a9932e5e1886a65a26b5cade2d5b222cc71a5727fc338f68`；
- PLAN轨迹叠图，SHA `b1f8e4bef56cd6ef5ef74d67d898c65015c8c0564b5e5d7b79b098b76d8a4f50`；
- 四相机50%板，SHA `b081406c6b2a0e7424dfc5a989be8468cf02b02fa4c9eff101dfdfcb67d97393`；
- 四相机100%板，SHA `9b8868c7cc81def9d2896dad67129877facc4ccd54783745850fce64cfa20856`；
- layer-toggle板，SHA `e4343bd6aeb7ad09e5f5baf1558baa5415f72dc081421584a83c9d54ae1bdf51`；
- 24块模块50%板及BASE／BUILDINGS／ROOF／FOREGROUND／OCCLUSION／WETNESS分层均已纳入审查。

## 3. 可保留内容

只保留下列机械／来源证据，供下一条环境路线复用：

1. 32×18、40×20、整数grid为cell center、raw origin `[-880,-170]`、canvas origin `[-1760,-340]`；
2. NO_FOCUS／PLAN／CONTACT A／CONTACT B四相机与1280×584地图窗口；
3. 20条grid→raw→canvas→screen控制点全部0px误差；
4. 道路、building block、selection pocket、BREAKER charge avenue／shoulder、保护区、stateful object reserve等拓扑mask；
5. 六个donor裁片的父图、矩形与SHA来源链；
6. Task102对旧Task98三张+20px综合板的History隔离。

以上不等于可见像素获批。由未获批建筑高度派生的roof／occlusion也不得直接消费。

## 4. 50%门失败

在640×360读法上：

- 中央承接大道、东侧生命线和南侧冲线不能从cleanplate自身在3秒内稳定读出；必须依赖QA彩线与文字才能理解空间；
- 大块donor裁片的亮斜纹、水渍和边缘被放大到街区尺度，第一眼读成抽象拼贴而非城市空间；
- 北侧建筑、道路与开放广场的明度层级塌缩，主玩法口袋被近黑块吞没；
- 环境抢走交互读法，却没有形成可识别的东门／万机馆／承力大道场所结构。

因此`VISUAL_50_PERCENT_FAIL`，禁止进入细节返修或下游合成。

## 5. 100%门失败

在1280×720及分层原图上：

- 出现明显硬拼缝、重复斜纹、裁片相位跳变与放大纹理；
- 建筑呈现为贴纹长方体／程序挤出，缺少可信结构、尺度与局部设计；
- CML128所需的4–7大色块与两级硬阴影没有转化为空间层级，反而保留高频水渍噪声；
- donor只覆盖2400×1350 canvas的6.48%，在安全子裁切前已需至少15.44倍面积复用，容量不足不是“再调色”可修的问题；
- E1模块与E2可见层均不能作为后续角色母版的场景校准背景。

因此`VISUAL_100_PERCENT_FAIL / ENV_E1_E2_NOT_CONSUMABLE`。

## 6. 通用机器PASS不得放行

Task101 `machine-validation-report.json` 顶层的`pass=true`只表示尺寸、alpha、hash、来源与注册机械闭合；同文件已明确`visual_self_review_pass=false`及`candidate_visual_promotion_allowed=false`。

下游必须以本回执为优先裁决：

- `mechanical_pass=true`；
- `visual_pass=false`；
- `overall_pass=false`；
- 禁止任何消费者仅凭通用`pass=true`加载E1/E2可见像素。

## 7. 后续路线与停门

“六块donor＋零生成确定性拼装即可得到精品current地图”的路线已经被实际像素否证，停止在History，不得继续机械返修或扩大裁片冒充精品。

若保留Call03／Call04两次单机母版预算，则环境必须另走一条专用路线：以本回执保留的exact拓扑／相机／mask作控制，以高质量current-topology环境图为视觉源，再确定性拆层；可选实施是一次环境专用、非批量生成，或外部人工2D场景绘制。该预算与生产路线扩张必须单独取得用户确认，制作人不得挪用Call03／Call04自行执行。

当前继续保持：

`Call03=false / Call04=false / real_art_loaded=0 / approved_handoffs=[] / UA91=false / G2-B=false / Runtime=false / Canon=false / FUN_NOT_PROVEN`。
