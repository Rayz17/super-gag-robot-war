# C01E02 M3-R0.5｜M0 工程壳证据纠偏回执

> 日期：2026-08-18
>
> 状态：`active correction / supersedes visual-judgeability claims only`
>
> 旧证据保留：`main-m3-r05-shell/**` 原字节、原报告和原哈希不覆写

## 1. 纠偏结论

M0 的青色矩形馆守 Z、黑红多边形 BREAKER、字母／汉字／加号头像属于通用程序占位，不是 Current 身份设计的简化表达。因此：

```text
M0 evidence class = engineering_shell_evidence_only
character identity judgeability = NOT PROVEN
mecha identity judgeability = NOT PROVEN
overall visual judgeability = NOT PROVEN
U2 visual playtest eligibility = false
```

旧截图、AVI 与完成报告继续证明：场景可启动、槽位和布局存在、节拍可播放、fallback 可运行、Full/Skip/fallback 不改变冻结玩法结果、零 handoff 时没有探测真实美术。它们不得再被用于判断人物是否在场、机体是否像既定设计、画面是否好看或演出是否达到用户视觉验收。

## 2. 真实资产接入能力审计

当前 `presentation_asset_resolver.gd` 永久返回 `named_geometry_fallback` 或 `synth_audio_fallback`；场景没有真正消费美术的 `Sprite2D/AnimatedSprite2D/TextureRect/AtlasTexture` 绑定链。修改 manifest 开关不能形成真实接入。

未来 M1 必须另行实现：

1. 逐槽 exact handoff loader：校验 producer handoff、Stable ID、build/profile/topology、正规化路径、SHA-256、真实图片／atlas／音频参数、alpha、pivot、safe area、frame rect 和 facing；单槽错误 fail closed。
2. 世界消费者：地图层、馆守 Z、BREAKER、小体、车辆、重盾和 FX 的真实 `Sprite2D/AnimatedSprite2D` 或等价节点。
3. Screen 消费者：纪存、七海、旧守护者、兜灯和代表性 `GIANT_CONTACT` 的真实 `TextureRect/AtlasTexture` 或等价节点。
4. 音频消费者：真实 `AudioStreamPlayer` 及 loop／channel／duration 校验；不把 synth fallback 算作真实加载。
5. 身份关键槽门：任一关键槽仍 fallback 时，整轮自动降回 `engineering_shell_evidence_only`，禁止标记为 U2 有效视觉试玩。

身份关键槽至少包括：

- `R05_PORTRAIT_JICUN`
- `R05_PORTRAIT_QIHAI_REMOTE`
- `R05_COMMS_OLD_GUARDIAN`
- `R05_GUARDIAN_MAP_ACTION_4DIR`
- `R05_BREAKER_MAP_ACTION_4DIR`
- `R05_SHIELD_WALL_HUNG`
- `R05_CUTIN_GIANT_CONTACT`
- `R05_CUTIN_DOUDENG_OBSERVE`
- `R05_CUTIN_DOUDENG_TENSE`

非身份 FX／音频可以在 U2 以逐槽披露的 fallback 存在，但不得掩盖关键槽缺失。

## 3. M0.1 身份感知 fallback 规则

M0.1 仍不加载真实资产，只修技术占位的身份误导：

- 馆守 Z schematic：`18m / 2x2`、金色横向冠、中央红冠饰、银色格栅面、红胸、圆形金色胸核、双圆柱前臂、右肩旧伤；本时点双前臂完整。
- BREAKER schematic：`近30m / 3x3`、前肢承重半直立、低伏冲撞、肩壳下低位头块、头块单一红缝、闭合胸缝、封闭上背核心出口、X 异质／生体装甲语言；不得画成人形黑机或普通四足兽。
- 纪存／七海：不发明脸；只用技术剪影／身份框和正确姓名、来源、职能，并在调试回执标记 `portrait_unavailable=true`。
- 旧守护者：只用馆守 Z 机头、胸灯和扬声波形，显示“馆守 Z 本体”；不画成人类第四队员。
- 兜灯：P1a 重绑前不假画脸；技术框显示“维修角 / 机况·承力”。
- 所有 schematic 沿用正式槽 rect、safe area、pivot、时长和镜头位置，不改玩法或布局接口。

## 4. 玩家语义修正

- 顶栏：`本轮操作：馆守Z`，明确只有一台直接操作机。
- 纪存：`导览席 / 路线·人员·危险`，不显示“现场频道”，不暗示驾驶或控制四肢。
- 兜灯：在玩家获得规划输入前保留已验收原句“它管身体，你管路。别抢方向，也别让它一脚踩进楼里。”
- 旧守护者：`馆守Z本体 / 身体自行负责`，不是副驾驶。
- 七海：`远程权限状态 / 本人停机令已撤回`，无行动图标、待命、支援、按钮、战场指令或炮火权。
- 应急车：去掉没有 Reader 依据的医疗十字；内部旧 `ambulance` ID 不得视觉化为设定事实。

## 5. 新生产顺序

```text
M0.1 = 内部布局、节拍、身份感知回退与接入门验证
P1a = A4/A5/兜灯既有批准件的 R0.5 exact rebind（可选并行准备）
U1  = A6/A7 具体文件逐项用户批准
P1b = 新人物／机体／Cut-in exact handoff
M1  = 真实 loader、消费者和联合接入
U2  = 身份关键槽全真实加载后的有效用户视觉试玩
R1  = 继续受既有玩法因果硬门限制
```

本回执不替用户批准任何 A6/A7 文件，不改 Canon、Reader、默认 M2 Demo 或旧批准资产字节。
