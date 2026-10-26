# C01E02 A6｜角色通讯 UI 美术目标

> 派发对象：美术资产 Session A6
>
> 状态：`authorized Candidate art / user review required / no Runtime handoff`
>
> 写入：`docs/superpowers/specs/production/c01-current-demo-v1/art-a6-character-comms-ui/**`

## 1. 唯一目标

为 R0.5 交付一组能在 1280×720 战术界面中立即建立“谁在说话、他／她知道什么、此刻担心什么”的角色通讯资产。

只新作纪存、七海、旧守护者三个通讯主体；兜灯复用两张既有 `approved_for_runtime` Cut-in 并验证新布局。不扩到唐胶、小满、阿澄、豪司或全章头像，不制作立绘收集系统。

## 2. 开工前置

1. 使用 `chao-gag-canon`；
2. 完整读取 09b、10、31、32、33、34、36；
3. 查询 `CH_JICUN`、`CH001`、`CH_QIHAI`、`CH002`、`V355-C01E02`；
4. 只读取已验收 C01 Reader E02；
5. 核对 `frozen-assets/cml001-jicun-current-base.png` 和 `cml002-003-004-tangjiao-doudeng-qihai-current-base.png` 哈希；
6. 核对 `battle-presentation-v0.1/art-delivery-manifest.json` 中 `CUTIN_DOUDENG_C01_OBSERVE_V01`／`TENSE_V01` 的批准状态、1920×640 尺寸与合同登记 SHA；
7. 用 `40-c01e02-m3-r0-5-frozen-contracts.sha256` 核验本轮合同；
8. 旧守护者的身份从馆守 Z 头部、胸前扬声器和导览席信号表达，不为其创造人类脸或独立 AI 身体。

冻结输入漂移、角色身份冲突或需要重设计服装／种族／机体时，写 `BLOCKED.md` 并停止。

## 3. 角色设计意图

| Stable ID | 战斗中的信息位置 | 画面重点 | 禁止读法 |
| --- | --- | --- | --- |
| `CH_JICUN` | 导览席，标记人员、路线和危险方向 | 年轻、专注、在沉降的城市视野中努力保持清醒 | 军事指挥官、超然全知主角 |
| `CH001` 兜灯 | 机况台，看承力、关节和冷却 | 复用既有 OBSERVE/TENSE 批准件，在布局中保持人物位于画面右侧及透明背景 | 重画同一用途、拉伸变形、用新文件覆盖既有 Stable ID |
| `CH_QIHAI` 七海 | 代哥东区封存中心远程通讯 | 克制、职业，但撤令后风险已落在她本人身上；远程频道有可见延迟／噪点 | 现场队友、可命令城市炮火的上司 |
| `CH002` 旧守护者 | 馆守 Z 机魂人格和巨体身体的意志 | 头部目光、胸前扬声器、导览 UI 波形三者建立同一主体 | 虚拟女孩、可复制助理、纪存的机体皮肤 |

## 4. 核心交付

三个新作主体各交付一张透明上半身／通讯母版和三个状态；兜灯只作既有资产布局验证：

| Slot | 状态 | 建议母版 |
| --- | --- | --- |
| `R05_PORTRAIT_JICUN` | `focused / alarm / resolve` | 每状态 `768×768 RGBA`，人体安全框 `x96–672 y48–744` |
| `R05_PORTRAIT_QIHAI_REMOTE` | `controlled / decision / concerned` | 同上，人物本体与远程噪点 mask 分层 |
| `R05_COMMS_OLD_GUARDIAN` | `guide / contact / shield_gaze` | `1024×768 RGBA`，提供 head/chest/waveform 独立层 |
| `R05_CUTIN_DOUDENG_OBSERVE/TENSE` | `existing approved source / no new master` | 原件 1920×640；只进入评审模拟图，不复制为 A6 Runtime 资产 |

同时交付：

- 三组新作角色状态板 + 兜灯两张既有批准件适配板；
- 纪存–兜灯本地通讯、纪存–七海远程通讯、纪存–旧守护者机魂通讯三张 1280×720 模拟图；
- 左／右占位、说话者高亮、对方降暗、长文本安全区和 720p 缩放验证板；
- `asset-manifest.tsv`、`portrait-spec.tsv`、`source-validation-receipt.tsv`、`user-decision-card.md`、`completion-report.md`、`core-delivery-hashes.sha256`；manifest 逐项登记 `source_tool`、`rights_note`、`forbidden_states`；
- 可复现的源文件和只读 validator。

图中不烘字、姓名、对话、按键、边框或版权标记。UI 框、文字和高亮由 Godot 程序层制作。

## 5. 生成与风格边界

- 允许在本任务范围内用可用的图像生成／编辑能力制作受控 Candidate；不使用付费外部批处理或 LibTV。
- 以冻结身份锚为外观来源，不将其当作可直接运行资产。
- 兜灯原件保持只读、原尺寸、原 SHA 和原 Stable ID；模拟图可以缩放摆放，但不得写回、裁切覆盖或输出冒名母版。
- 风格为清晰、克制、可在高密度战术 UI 中快速识别的动画游戏立绘；不用过度色气，不用每人都同样的“严肃美型脸”。
- 三个表情必须通过眼神、嘴角、颈肩和呼吸紧张度建立差异，不只换颜色或特效。
- 不模仿具体在世艺术家、动画 IP 或已有游戏角色。

## 6. 用户停止门

美术 Session 完成后必须展示并请用户逐项回答：

1. 纪存是否像在读城市与人员，而不是统帅；
2. 既有兜灯 OBSERVE/TENSE 在新布局中是否一眼能看出工艺与机况责任；若不适配，是否批准另开新作任务；
3. 七海是否保持远程、克制和承担撤令后果的状态；
4. 旧守护者是否清楚是馆守 Z 同一主体；
5. 四人在 720p 实际占位是否可读、有个性且不遮挡战术信息；
6. 哪些具体文件批准作为 R0.5 Demo 派生来源。

未批准前全部保持 `Candidate / runtime_allowed=false / runtime_handoff=none`，不写 Godot，不复制到 runtime assets，不自签 handoff，不 `git add/commit`。
