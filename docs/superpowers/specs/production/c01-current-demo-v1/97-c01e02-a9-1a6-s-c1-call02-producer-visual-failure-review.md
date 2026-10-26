# C01E02 A9.1-A6-S-C1 Call02 制作人视觉失败回执

日期：2026-08-20  
任务ID：`P97_CALL02_A_PLAN_PRODUCER_VISUAL_REVIEW`  
状态：`CALL02_VISUAL_FAIL_IDENTITY_AND_REGISTRATION / ENVIRONMENT_METHOD_DONOR_ONLY / CALL03_FALSE / CALL04_FALSE`

## 1. 制作人结论

Call02没有通过整屏、50%或100%视觉门，不能作为current-topology共享PLAN母版，不能作为A CONTACT的Call03基础，也不能进入UA91、真实资产接入或Runtime。

雨夜工业城市的暗值、湿地反光、建筑分面、屋顶遮挡、边灯与青／红光色方法可以保留为环境方法参考；生成图中的馆守Z、BREAKER、三只小体、应急车、墙挂盾、东门、警戒设施及其阴影／反射／位置一律不得作为当前像素或注册责任源。

这不是“机器完成但等待润色”，而是身份与空间注册两项产品前提同时失败。禁止在整屏图上局部补脸、挪机体或继续生成CONTACT来掩盖根因。

## 2. 锁定交付与独立复验

| 对象 | SHA-256 | 制作人用途 |
|---|---|---|
| Call02 raw `CALL02_A_PLAN_RAW.png` | `98f30a9797591204f702ad1b36aaad1042c2cece1fd35a088b44d828f9e156d5` | History／环境方法参考 |
| `PLAN_SHARED_CURRENT_PHYSICAL_CLEANPLATE_1280x720.png` | `fe584aa232441962d54b3b3f168baa6a96c110503ee8b6891eafe7e9dee625d8` | 失败诊断；不得当cleanplate责任源 |
| `GF_PLAN_A_INTEGRATED_LOOK_TARGET_1280x720.png` | `710dd89c481c73a56a63ff6e80930d91d334b3bff68897112264f2cee0b2d6f2` | 失败整屏诊断 |
| `generation-log.md` | `1d884397d082cf736a49be159761c1a92429d6d7106a958963ac88c07a65b144` | 调用、参考图与prompt审计 |
| `completion-report.md` | `bb142acfdae6964159ea2694ddd0cacdaf9b5db9e892694dde9578ab0fac45d9` | 美术线程自报失败边界 |
| `delivery-hashes.sha256` | `06f7c142605188bf25e04dc0d14b8db741cb4e533ccd7c290f7cb5d45687995f` | 19项交付闭环 |

制作人从Call02目录独立执行交付manifest复验，19项全部一致；raw为`1672×941 RGB`，确定性后处理只有16:9中心裁切与一次缩放，UI／路线／ghost／edge cue可独立关闭。Call02实际消耗一次，Call01历史一次，剩余两次未消耗。

文件闭环只证明“交付物是所声明的文件”，不证明画面身份、注册或产品可用。

## 3. 整屏与3／10／30秒门

### 3秒

依靠确定性UI、路线与红／青色方向，能粗略读出“撤离、威胁、拦截”的战棋场景；但两台巨体与小体类别身份错误，画面本身不能可靠说明是谁在以什么身体承担责任。结论：`FAIL`。

### 10秒

环境层次、东缘青光与中央威胁区可读，但生成器重排了实体。冻结预期脚点为：馆守Z`(400,340)`、BREAKER`(520,520)`、应急车`(520,320)`、三只小体`(840,360)/(800,540)/(1200,460)`；实际画面中车辆、馆守Z与小体均明显漂移。确定性路线／ghost因此与生成角色脱节，无法把路线、占地和承力关系当成current-topology真相。结论：`FAIL`。

### 30秒

A／B责任差异仍可由外加UI解释，但底图中的身体、位置和接触前关系不可信，不能证明“城市空间替机体承伤”或“机体高热换城市保全”。结论：`FAIL`。

## 4. 50%整屏门

通过项仅限：

- 蓝灰雨夜的中低明度层级；
- 湿路、混凝土、建筑立面与屋顶的材质分离；
- 东缘青色安全方向与红色威胁方向的色彩对位；
- 局部屋顶／前景遮挡与边灯的氛围方法。

失败项：

- 馆守Z第一读法是通用高比例英雄机，不是约四头身、旧超级系重量的V10X；
- BREAKER第一读法是高壳龟兽／普通四足，不是B前肢承重半直立身体＋X异质闭合生体甲；
- 三只小体被同质化成缩小甲壳兽，A5身份没有保住；
- 实体漂移后，路线、车辆、巨体冲线与选择口袋不再共享一套空间真相。

结论：`FAIL_50_PERCENT`。环境强不构成整屏可修基础。

## 5. 100%身份门

馆守Z虽然没有生成翼／背包，但V10X金冠、银栅格脸、红X胸甲／金核、方肩环、等重圆柱前臂和四头身重量均不足，肢体变成长细的通用机。

BREAKER缺失B方向的半直立承重前肢、短后足稳定、低嵌头和X方向的连续应力缝／异质甲闭合关系，正中任务书的一票禁止“龟／猿／普通四足／装甲车”。

结论：`FAIL_100_PERCENT_IDENTITY`。整屏ImageGen不能继续承担两机地图母版与exact registration的双重责任。

## 6. 可复用与永久排除

### 只可作方法donor

- 局部无语义建筑面、湿路、雨线、反光、屋顶层次与低位前景；
- 青安全／红威胁的光色关系；
- 局部环境材质和暗值区间。

使用时必须重新服从current-topology block mask、唯一投影与对象坐标，不得整屏回贴。

### 不得复用

- Call02中的全部单位、车辆、对象像素及其影子／反射；
- raw整屏的坐标、建筑占地、相机注册与遮挡关系；
- 任何“把错误机体挪回脚点”或“局部补成正确身份”的伪修复；
- 以Call02为父图继续生成A／B CONTACT。

## 7. 制作路线纠偏

后续视觉生产改为分离式门控：

1. 以Task89／96的current-topology、block mask、相机与注册公式制作**无动态actor／object的环境cleanplate**；Call02只捐局部环境方法。
2. 先单独建立风险最高的`BREAKER_PLAN_MAP_CAMERA_MASTER`，只解决3×3、north地图相机、B＋X身份、footprint-bottom-center与地面阴影；50%／100%不过立即停。
3. BREAKER通过后，再单独建立`GUARDIAN_Z_PLAN_MAP_CAMERA_MASTER`，只解决2×2、east地图相机、V10X约四头身身份与统一pivot；失败不reroll。
4. 使用A5已通过的小体、current对象层、环境cleanplate与两台独立母版做确定性合成，禁止为了“看着顺”手移anchor。
5. 重跑整屏、50%／100%与3／10／30秒门；通过后才允许制作CONTACT与稀疏clip。

这一路线不是重画馆守Z或BREAKER设计，而是把“设计身份”“地图相机资产”“环境世界”“交互overlay”四类责任拆开，避免整屏生成器同时猜身份、透视和坐标。

## 8. 当前门禁

- `Call03=false / Call04=false`，剩余两次调用保留，不自动改作reroll；
- 下一步只允许零生成的分离式预生产与exact guide／source lineage／注册板；
- `real_art_loaded=0`；
- `P98 / UA91 / A9.1-B / signed exact handoff / G2-B / Default / Save / Runtime / Canon / FUN PASS / UGT READY`继续Blocked。
