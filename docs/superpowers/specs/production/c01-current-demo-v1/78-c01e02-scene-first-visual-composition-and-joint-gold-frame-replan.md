# C01E02｜Scene-First视觉合成与联合Gold Frame重排

> 日期：2026-08-19  
> 状态：`CURRENT_DAG_CORRECTION / R2_CONTINUES / ART_FROZEN / UA91_REDEFINED / G2_B_BLOCKED`  
> 适用：C01E02 Candidate Demo第一轮45–75秒Golden Turn  
> 不构成：Hard／Working Canon修改、用户视觉批准、真实美术接入、Runtime晋级、G2-B派工、付费批量生成

## 1. 制作人即时裁决

用户给出的目标画面不是要逐像素照抄的资产，也不能证明交互已经实现；它是本Demo的**整屏体验水准参考**：统一斜俯雨夜地图、地图内路线与威胁、巨体真实站地与遮挡、大型人物通讯、正式HUD和同一画面中的演出重点。

当前玩法底座与G2-A.1-R2几何校准仍有价值，不推倒、不叫停。需要纠正的是R2之后的施工顺序：

1. “孤立机体Sprite先做完，再直接送UA91”撤销。
2. “整帧概念图好看，就直接切成Runtime资产”禁止。
3. 改为“精确几何上的整屏场景目标 → 可拆视觉系统与资产 → 用可拆资产重新组成整屏 → 用户裁决 → 稀疏动作 → 真实接入”。
4. 新“主程序-2”只收口77号R2；不得扩项做视觉合成、真实美术或G2-B。
5. 新“美术资产-2”继续冻结；没有本文件之后的唯一任务书，不得重画设计、扩Atlas或生成新资产。

本文件只覆盖76号中“A9.1-A6直接双Pilot送UA91”的下游顺序。76号第1–6节的投影、方向、footpoint、pivot、遮挡、接触socket与稀疏状态原则继续有效。

## 2. 为什么必须Scene-First，但不能Full-Frame-Only

当前失败发生在两个相反极端：

- 只做分离资产时，没有共同场景相机、光向、可见尺度、落脚、遮挡、安全区和交互焦点，最后把各自好看的图贴成不同世界。
- 只做整帧生成时，模型能临时统一气氛与透视，但输出不可分层、不可注册、不可遮挡、不可逐状态消费，也不能证明45–75秒真实交互。

正确链路必须闭环：

```text
exact gameplay geometry
→ integrated scene target
→ separable map / unit / UI / portrait / FX assets
→ runtime-like recomposition from those separable assets
→ user visual decision
→ playable Golden Turn
```

整屏场景目标负责回答“这款游戏应该长什么样”；可拆资产与程序消费者负责回答“它是否真的能运行”；最终试玩负责回答“它是否真的好玩、好读、好看”。三者不能互相冒充。

## 3. 第一轮目标画面的视觉系统

| 系统 | 第一轮必须达到 | 责任边界 |
|---|---|---|
| 战术几何 | 32×18、40×20 dimetric、逐段朝向、多格footpoint、接触法线与socket同源 | G2-A.1-R2；只决定空间，不决定美术完成度 |
| 地图合成 | A4共同画布上的成片雨夜街区、建筑层、屋顶／前景遮挡、道路战损、湿地与灯光 | 美术交可拆层；程序按共同origin与mask消费 |
| 地图单位 | 馆守Z／BREAKER服从同一地图相机、共同光向、占地与脚点；由shadow/body/attachment/emissive/fx组成 | 不再用一张眼平透明PNG当完整Actor |
| 路线与威胁 | 路径带、终点框、朝向、危险区、接触与受力向量清晰且不遮住关键单位 | 程序Overlay Renderer；沿R2几何绘制 |
| 人物通讯 | 纪存大型半身／动作立绘、台词、目标与命令HUD形成正式安全区 | `screen_ui`；执行接触前必须退让，不得遮住受力点 |
| Peak Space | 仅在少量高峰使用LibTV／Cut-in，并回到同一地图落点、朝向、损伤与幸存状态 | 不得用播片遮掩地图Sprite或接触错误 |
| 天气与重量 | 远近雨层、湿地反光、水花、hit-stop、闪光、碎屑、反冲、震屏和声音形成合力 | 大部分反射可烘焙；不要求本轮改为3D或实时全反射 |

第一轮目标是一个可控的高完成度切片，不承诺全游戏任意单位、任意方向、任意动作的资产全集。

## 4. 新增验收门

### P78-R2｜制作人几何签收

主程序-2完成77号后，制作人必须：

- 核对专用suite、既有回归、五张actual frame与delivery hash；
- 实看方向扇面、逐段转向、1×1／2×2／3×3脚点、遮挡、socket与受力向量；
- 对`east-west`现状与57号`south/north`叙事目标作接触舞台选择；
- 签定第一轮GF-PLAN与GF-CONTACT的exact anchor、facing、camera focus和contact normal。

在制作人签字前，后续美术与视觉合成任务均不派发。机器全绿但`contact_decision=pending`时，R2只能报“代码／证据完成，产品门未关闭”。

79号实际验收已签收R2的通用几何消费者，但否决现有A/B正式接触站位，并签发`STAGGERED_FRONT_CONTACT_V1`的R2C窄任务。故本门当前必须等待R2C把A/B正面接触、接触后位置差和第二轮读取闭合后，才可最终关闭。

### A9.1-A6-S｜整屏场景目标Lookdev

以P78-R2签定的精确几何为底，只制作两张1280×720整屏视觉目标：

1. `GF_PLAN_TARGET`：可读路线、终点／威胁、目标HUD、纪存通讯、馆守Z和场景关系；
2. `GF_CONTACT_TARGET`：UI退让、馆守Z与BREAKER接触、impact socket、受力方向、路裂／碎屑／雨夜光效和接触后的空间读法。

硬要求：

- 地图、单位、阴影、建筑遮挡和FX共用`A4_MAP_SPRITE_CAMERA_V1`；
- 馆守Z身份责任源继续为V10X最新版链；BREAKER继续服从已批准B＋X；禁止重做设计；
- 常态服从CML128 `KINETIC_CEL`，不把商品渲染软渐变缩小冒充地图成品；
- 两张图必须沿R2 exact坐标构图，不能自由移动单位来迁就画面；
- 该阶段是Candidate视觉意图，不是可拆资产、Runtime或UA91批准。

制作人先做整屏内部预审。若身份、透视、比例、地图完成度、交互第一读法或安全区任一不成立，停在本门，不向下拆资产。

### G2-A.2｜视觉合成系统Proxy门

在P78-R2签收后，程序用无身份proxy实现并证明：

- 六层大地图共同canvas／origin／crop／filter与occlusion；
- `shadow/body/attachment/emissive/fx`复合地图Actor；
- 正式路线、终点、威胁与接触Overlay Renderer；
- 远近雨层、湿地mask／低成本倒影、水花与道路状态层挂点；
- 大型通讯Presenter、目标区、命令区、事件条与关键接触安全区；
- 1280×720目标机器性能、贴图过滤、显存与帧率证据。

本门仍为`real_art_loaded=0`。不得用proxy通过宣称目标视觉完成，也不得转入G2-B。

### A9.1-A6-D｜可拆资产内部Pilot

只有整屏场景目标通过制作人内部预审后，才从同一目标和责任源制作最小可拆件：

- 目标画面实际可见的地图局部层与mask Pilot；
- 馆守Z一个实际规划方向、BREAKER一个实际接触方向的地图Sprite Pilot；
- 纪存一张实际通讯构图Pilot；
- 一组路线／威胁／接触UI和一组雨夜／接触FX Pilot。

孤立透明图只作内部资产检查，不单独进入UA91。必须同时验证100%／50%显示、footpoint、阴影、遮挡、共同光向、身份责任源与`view_space`。

### A9.1-A7-J｜联合Gold Frame重组门

使用上述**可拆资产**和G2-A.2消费者重新组成：

- `GF_PLAN_RECOMPOSED`；
- `GF_CONTACT_RECOMPOSED`。

这两张必须来自actual runtime frame，或来自与Runtime使用同一origin、pivot、crop、z、mask和slot manifest的确定性合成器。禁止用另一张整帧生成图补洞，禁止把Lookdev目标冒充重组结果。

制作人视觉预审同时查看：整屏、关键单位100%裁切、50%游戏尺度、遮挡前后与目标图差异说明。通过后才提交UA91。

## 5. UA91重新定义

UA91不再让用户裁决两张孤立透明机体。用户必须看到同一包中的：

1. `GF_PLAN_RECOMPOSED`整屏；
2. `GF_CONTACT_RECOMPOSED`整屏；
3. 馆守Z／BREAKER在50%游戏尺度和100%裁切的身份对照；
4. Lookdev目标与可拆重组结果的差异说明；
5. 明确选择：`批准 / 定向返修 / 路线重想`。

UA91只批准第一轮所需的视觉母版与共同世界，不证明动作全集完成，也不证明交互手感。用户批准后，制作人才冻结exact interface；之后A9.1-B只扩第一轮稀疏状态，G2-B只整合45–75秒第一轮Golden Turn，最后由UGT真实试玩判断。

## 6. 纠偏后的联合DAG

```text
G2-A.1-R2收口（当前继续）
→ P79制作人部分签收＋接触舞台裁决
→ G2-A.1-R2C实现并回放STAGGERED_FRONT_CONTACT_V1
→ P78-R2制作人签exact PLAN／CONTACT几何
→ A9.1-A6-S整屏场景目标Lookdev ──────────┐
   G2-A.2视觉合成系统Proxy ───────────────┤
→ A9.1-A6-D最小可拆资产Pilot ─────────────┤
→ A9.1-A7-J GF-PLAN／GF-CONTACT联合重组 ──┘
→ 制作人整屏视觉预审
→ UA91用户联合画面裁决
→ 制作人冻结exact interface
→ A9.1-B第一轮稀疏可组合实物资产
→ 制作人signed handoff
→ G2-B只整合45–75秒第一轮Golden Turn
→ UGT用户试玩
→ 通过后才扩第二／三轮与约4.5分钟Golden Slice
```

Lookdev与G2-A.2可在P78-R2签收后并行，但二者都不能越过联合重组门。美术不能靠漂亮整帧绕过分层，程序不能靠proxy绕过美术。

## 7. 当前任务状态与下一步

| 任务 | 当前状态 | 当前唯一动作 |
|---|---|---|
| 新主程序-2／G2-A.1-R2 | `PARTIAL_ACCEPTED` | 通用几何已签；按79号只做R2C接触舞台闭环 |
| 新美术资产-2 | `FROZEN_BY_P78` | 不生成、不重画、不扩Atlas，等待整屏场景目标唯一任务书 |
| G2-A.2 | `NOT_DISPATCHED` | 等P78-R2签收 |
| UA91 | `BLOCKED_BY_JOINT_GOLD_FRAME` | 不看孤立机体，不提前裁决 |
| A9.1-B | `BLOCKED_BY_UA91_AND_EXACT` | 不生产 |
| G2-B | `BLOCKED_BY_SIGNED_HANDOFF` | 不派工 |

当前制作人已按79号完成R2部分签收并派R2C；下一次动作是查看R2C的A/B实际帧、第二轮回读与侧甲炮线。只有签字后，才给程序和美术各一份共享同一整屏目标、但写域分离的唯一任务书。

## 8. 权威边界

- 本文件是Candidate生产DAG与视觉合成接口纠偏，不修改Current Canon。
- V10X、B＋X、CML128及已有用户回执的权限不变；任何Candidate图仍不能冒充Hard身份母版或Runtime资产。
- 目标参考画面只约束体验水准和系统关系，不自动取得项目资产身份，也不授权照抄其具体角色、场景或UI设计。
- 测试、hash、文件齐全、actual frame与用户视觉批准分别记账；任一项不得替代另一项。
