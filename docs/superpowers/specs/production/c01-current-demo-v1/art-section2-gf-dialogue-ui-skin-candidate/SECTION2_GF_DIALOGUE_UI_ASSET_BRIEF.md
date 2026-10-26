# C01 当前 Demo｜GF 对话交互皮肤｜Section 2 独立资产 Brief

> Status: `SECTION2_ASSET_BRIEF / ART_NOT_DELIVERED / CANDIDATE_ONLY`
>
> Date: `2026-08-24`
>
> Runtime / Default / Save / Canon: `false`
>
> User visual acceptance: `false`

## 0. 本轮结论与停止门

当前仓库**没有**可合法直接接入 `c01_gf_operation_hud` 的 GF 独立对话 UI 皮肤。

- `GF_PLAN_1280x720_v2.png` 与 `GF_CONTACT_1280x720_v2.png` 是整屏视觉锚；框体、地图、人物和事件层已烘在同一图中，不是九宫格、边框、speaker tab、进度件或提示件的可拆交付。
- A9 后续纠偏又明确将两张整屏降为 `mood_and_finish_reference_only`；它们不得作为 UI 定稿、Godot 资产或 Runtime handoff。当前产品计划只恢复其**完成度、HUD 层级、地图融合与 UI 退让关系**作为表现目标，并未恢复整屏像素消费许可。
- 用户已确认的是 GF 纪存与 GF BREAKER 的具体视觉锚；这不等于确认 A9 整屏中的每一个 UI 像素。
- A9.1 的 `deterministic-overlay-ui-template-1280x720.png` / `UI_ONLY_1280x720.png` 只通过预制作版面用途；其中生产标记必须删除，失败整屏也不得成为当前资产。
- `game-godot/assets/ui/ui_panel_9slice.svg` 与 `ui_srw_hud_frame.svg` 是通用扁平基线件，没有 GF 的材质、雕刻边框、层级和状态语言；接入只会继续产生“程序几何框”的首读。

因此本轮禁止：

1. 从 GF 整屏裁框、修补透明后冒充独立资产；
2. 把 A9.1 全屏 overlay 当成正式 UI 贴图；
3. 用旧 A6 纪存通讯合成图或旧人物稿填充新 Demo；
4. 以现有通用 SVG 换皮后声称达到 GF；
5. 在美术组件未交付、未验收前补一张“完成实机帧”。

本任务书完成后停在美术 Section 2。只有独立组件通过透明、缩放、实际 1280×720 构图和用户目视门，主程序才可在 Candidate HUD 中最小接入。

## 1. 权威与责任源

| 对象 | 路径 / SHA-256 | 本任务允许用途 | 禁止用途 |
| --- | --- | --- | --- |
| GF 规划整屏 | `art-a9-gold-frame/delivery/GF_PLAN_1280x720_v2.png` / `c1d2219354a7c8bd6fcccc326181e4875f4e292d916fb0b7512cafd06fce5f1c` | 规划期 UI 层级、人物切片与地图融合、深海军蓝＋金属金＋克制青光的完成度目标 | 裁框、直接消费、作为 UI 定稿或 Runtime 像素 |
| GF 接触整屏 | `art-a9-gold-frame/delivery/GF_CONTACT_1280x720_v2.png` / `83b713d6f700aa3b0bacc541902d98b92baa3de7730f502a1197a783b71c1633` | 接触期 UI 退让、重量峰值和信息减法目标 | 裁框、直接消费、作为 UI 定稿或 Runtime 像素 |
| A9 源层说明 | `art-a9-gold-frame/source-layer-notes.md` | 证明 UI 外框烘在 ImageGen 整屏母层，只有文字另装配 | 推定存在未交付的独立 UI 层 |
| A9 纠偏 | `59-c01e02-a9-g2-producer-correction-and-map-performance-gate.md` | 当前 A9 像素权限上限 | 以较早 completion report 覆盖纠偏 |
| 当前产品目标 | `128-c01-full-breaker-operation-demo-product-objective-and-execution-plan.md` §5.1–5.4 | GF 式整屏体验、正式九宫格、图标、材质边框、字体层级与动效 | 允许默认细线、纯色矩形、debug 描边成为成品 |
| A9.1 overlay | `art-a9-1a6-s-c1-current-topology-scene-first/deterministic-overlay-ui-template-1280x720.png` | 版面职责与中央玩法区留白参考 | 作为成品 UI、裁片或当前像素母版 |

若本 Brief 与上述权威冲突，以 59 与 128 的较新边界为准。

## 2. 当前消费者逐项差距

当前消费者：`game-godot/scripts/c01_breaker_demo/c01_gf_operation_hud.gd`。其对话区域全部由 `_draw()` 中的 `draw_rect` / `draw_colored_polygon` 与运行时 `Label` 组成；场景中没有对应 `NinePatchRect`、`StyleBoxTexture`、AnimationPlayer 或正式 UI 材质消费者。

| 项目 | 当前 Candidate HUD | GF 目标语言 | Section 2 必须交付 |
| --- | --- | --- | --- |
| 背景 / 外框 | 大块半透明海军蓝纯色多边形；金／青色直条；无纹理、倒角或材质层 | 深石墨／海军蓝材料体，收敛的金属金外缘，局部青色能量强调；有厚薄、倒角、刻蚀与负形 | 可伸缩九宫格外框＋独立可平铺内衬，不能烘文字和地图 |
| Speaker tab | 一块实心金色矩形，深色文字直接压在上面 | 与对话框同源、轮廓有切角或徽记感的名字牌；主体色只作小面积身份强调 | 独立九宫格名字牌与可着色 accent mask；文字仍由 Godot 实时排版 |
| 文本框 | 约 163px 高的扁平深色长框＋整条青线 | 深色半透明可读内腔、金／青分层边缘；大人物切片或地图仍能呼吸 | 左切片与宽框共用的九宫格主体；须给中文长句安全区 |
| 进度 | 裸露 `01 / 05` 文本 | 离散事件／段落珠或小型格位体现当前位置，数字仅作次级信息 | `idle / completed / current / locked` 四态进度珠 atlas；数字不烘入贴图 |
| 交互提示 | `ENTER / A 推进对话` 纯青字，放在普通矩形条内 | GF 六边／仪表语言的独立确认提示；键鼠和手柄同一语义，按下态明确 | 键盘 Enter、鼠标、手柄 A 的 `idle / focus / pressed` 图标 atlas；不烘中英文 |
| 动效 | 无 Tween、无状态过渡、无呼吸或高光 | 轻量入场、speaker settle、当前进度珠脉冲、确认 glyph 呼吸、快速退场；不得遮住战场 | 组件须支持 modulate／位移／缩放；若需边缘扫光，另交可平铺 mask，不交整屏视频 |

当前实帧诊断：`game-godot/captures/c01_breaker_demo/current/04_BRIDGE_A_GF_DIALOGUE_1280x720.png`。该帧只能用于说明差距，不构成 UI 视觉通过。

## 3. 最小独立资产清单

以下六件是本轮的**最小正式组件集**。文件名可在 Section 2 内调整一次，但交付 manifest 必须稳定绑定 `asset_id`，主程序不得按相似文件名扫描。

### UI-01｜对话框九宫格外缘

- `asset_id`: `C01_GF_DIALOGUE_FRAME_9SLICE`
- 建议文件：`delivery/gf_dialogue_frame_9slice_rgba.png`
- 建议源尺寸：`384×192 RGBA8`
- 初始九宫格 margin：`left=64, top=48, right=64, bottom=48`
- 中央区域透明；只承担金属外缘、内缘、角件、刻蚀和有限青光。
- 必须可无破坏伸展到至少：
  - 左人物切片模式：`679×163`
  - 宽地图／系统模式：`1144×163`
- 角件不得在短高框内互撞；金边不能读成纯黄矩形。

### UI-02｜对话框内衬平铺材质

- `asset_id`: `C01_GF_DIALOGUE_FILL_TILE`
- 建议文件：`delivery/gf_dialogue_fill_tile_rgba.png`
- 建议尺寸：`128×128 RGBA8`，无缝平铺。
- 深海军蓝／石墨微材质，中心 alpha 建议 `0.72–0.88`；不得含明显重复图案、文字、噪点脏污或场景像素。
- 在雨夜地图、浅灰 QA 底和品红 alpha QA 底上均须保持文字可读、但不能变成遮住战场的实心板。

### UI-03｜Speaker 名字牌

- `asset_id`: `C01_GF_SPEAKER_TAB_9SLICE`
- 建议文件：`delivery/gf_speaker_tab_9slice_rgba.png`
- 建议源尺寸：`320×64 RGBA8`
- 初始九宫格 margin：`left=52, top=20, right=52, bottom=20`
- 可伸展宽度：`210–330px`；中文名字安全区至少 `150×34px`。
- 不烘姓名、头像、身份标签或 speaker 类型。若需区分“现场／远程／系统”，另用同一份 `accent mask` 由程序着色，禁止生产三套结构不一致的名字牌。

### UI-04｜进度珠四态 atlas

- `asset_id`: `C01_GF_DIALOGUE_PROGRESS_ATLAS`
- 建议文件：`delivery/gf_dialogue_progress_atlas_rgba.png`
- `4×1` cells，每格 `48×48`，总尺寸 `192×48 RGBA8`
- 固定 state 顺序：`idle, completed, current, locked`
- `current` 在 50% UI 缩放下仍明显，但不得用大面积红光；`completed` 与 `locked` 不能只靠亮度区分。
- 实际 beat 数由程序动态生成；禁止把 `01/05` 或固定五格烘入贴图。

### UI-05｜下一步提示 atlas

- `asset_id`: `C01_GF_DIALOGUE_NEXT_PROMPT_ATLAS`
- 建议文件：`delivery/gf_dialogue_next_prompt_atlas_rgba.png`
- `3×3` cells，每格 `64×64`，总尺寸 `192×192 RGBA8`
- 行：`keyboard_enter, mouse_primary, gamepad_south`
- 列：`idle, focus, pressed`
- 只画设备 glyph 与 GF 式承载壳；不烘 `ENTER`、`A` 以外的说明句，不烘“推进对话”。本地化说明仍由 Godot Label 提供。

### UI-06｜边缘扫光／身份强调 mask

- `asset_id`: `C01_GF_DIALOGUE_ACCENT_MASK`
- 建议文件：`delivery/gf_dialogue_accent_mask_rgba.png`
- 建议尺寸：`256×64 RGBA8`；灰度或白色 alpha mask，可平铺／拉伸。
- 只用于名字牌入场、当前进度珠或框缘一次性微光；不得含固定颜色、文字或整屏 vignette。
- 若 UI-01 与 UI-03 已能在纯 modulate 动效下达到目标，本项可以在首门被制作人明确豁免；不能以豁免为由把动效删成静态纯色框。

## 4. 共同技术合同

每件资产必须在 `asset-manifest.tsv` 逐行提供：

```text
asset_id
path
media
width
height
alpha
color_space
filter_mode
repeat_mode
nine_slice_left
nine_slice_top
nine_slice_right
nine_slice_bottom
safe_rect
atlas_layout
state_ids
lifecycle
runtime_allowed
runtime_handoff
user_visual_acceptance
source_rights_receipt
sha256
```

共同硬门：

- PNG 必须为 `RGBA8`，不得只把 RGB 白底改名为透明图；所有外轮廓之外 alpha 必须为 0。
- 透明边缘在深蓝、白、50%灰与品红底检查，无白边、黑边、色键残留或半透明矩形画布。
- 资产中禁止烘入人物、头像、地图、机体、故事台词、beat 数、内部 ID、Candidate/debug 标记。
- `filter_mode` 与 `repeat_mode` 必须明确；九宫格角件不得被线性采样污染，平铺内衬不得出现接缝。
- `lifecycle=production_quality_candidate`；首次交付必须保持 `runtime_allowed=false`、`runtime_handoff=none`、`user_visual_acceptance=false`。
- 不声明 pivot 的 UI 组件填 `pivot=n/a`；atlas 必须声明 cell rect 与 state 顺序，禁止让消费者猜帧。
- 另交 `source-rights-receipt.md`、`delivery-hashes.sha256` 与可编辑源层说明。GF 整屏只能作为视觉参考，不可直接成为像素 source layer。

### 4.1 B06 与 E07 的画面类型不同，禁止共用 alpha 硬门

本节约束与 UI 组件同屏出现的 action slice；它**不改变** UI-01 至 UI-06 自身必须为 RGBA8 独立组件的要求。

| Beat / slot | `asset_type` | 正确像素合同 | 禁止误判 |
| --- | --- | --- | --- |
| `B06_JICUN_IS_STILL_INSIDE` / `JICUN_EXITS_GUARDIAN_CHEST` | `local_scene_insert` | 纪存与馆守 Z 胸前导览席／局部舱内环境共同构成一个矩形场景插片；允许不透明，或仅在外轮廓／安全裁切边缘带 alpha。必须声明 `safe_crop_rect`、字幕／UI 避让区和插片自身的内容边界；**不强制清除场景内部负空间**。 | 不得按“人物抠图”要求把座席、舱内结构和局部环境扣掉；不得因为 alpha 不透明而自动失败。 |
| `E07_NEXT_TIME_I_BOOK` / `JICUN_POST_BATTLE_CALL` | `character_cutout` | 人物通讯切片为 `RGBA8` 真透明；人物外轮廓之外及手臂、头发、衣物形成的内部负空间必须清空。必须通过深色、浅色、品红底与 alpha histogram 检查。 | 不得保留白底、棋盘底、半透明矩形画布或内部白洞；不得把整块通讯截图当 cutout。 |

后续 action-slice binding manifest 至少要分开声明：

```text
asset_type = local_scene_insert | character_cutout
alpha_policy = opaque_or_edge_alpha | full_cutout_alpha
safe_crop_rect
internal_negative_space_required
```

当前未完成的 `candidate_story_action_slice_bindings.json` / resolver 草案仍把 B06 与 E07 统一为 `alpha_required=true`，并把 `RGBA8 + alpha_required` 写成共同合法性条件；该假设与本节用户合同冲突。它必须保持 `texture_load=false / user_visual_acceptance=false` 的 fail-closed 状态，并在任何激活、测试签收或 UI 实帧消费前**回滚该统一假设或改为按 `asset_type` 分派校验器**。本 Brief 不授权继续修改那组代码。

## 5. 三张评审构图，不得作为消费件

Section 2 只在六件独立组件完成后，使用**同一批组件**装配三张 1280×720 评审图；评审图不进入 active manifest，不允许被 Godot 当作全屏 UI TextureRect：

1. `review/GF_DIALOGUE_B06_LEFT_ACTION_REVIEW_1280x720.png`
   - 左侧使用 `local_scene_insert`：纪存、馆守 Z 胸前导览席与局部舱内环境共同保留；不得为了“透明”删除座席和环境。
   - 对话框从 `x≈338` 开始，不盖住人物面部、动作手势或导览席叙事关系；地图保留主要路线与威胁阅读区。
2. `review/GF_DIALOGUE_E07_REMOTE_REVIEW_1280x720.png`
   - 左侧使用 `character_cutout`：人物外轮廓和内部负空间是真透明，不得残留白底；远程通讯身份清楚，但不能复制旧 A6 小头像框。
   - 名字牌、远程 accent 与确认提示仍使用同一 UI 语法。
3. `review/GF_DIALOGUE_WIDE_SYSTEM_REVIEW_1280x720.png`
   - 无人物切片；宽框约 `x=70..1214, y=400..563`；不得擅自生成当前 speaker 的人物头像。

三图必须使用主程序同一实际地图帧作为只读底图，并另交 50% 缩略并排板。它们只回答“组件放进真实画面是否达到 GF 层级”，不能替代组件 alpha／九宫格检查，也不能作为 Runtime 像素。

## 6. Candidate HUD 接入与动效验收合同

美术通过前，现行程序几何框继续作为**不变的 fail-closed fallback**；不得因为有一半组件就混搭成新的默认视觉。美术通过后，主程序仅在 `c01_gf_operation_hud` Candidate 车道中增加正式消费者：

- UI-01 / UI-03：`NinePatchRect` 或 `StyleBoxTexture`；
- UI-02：可平铺 `TextureRect` / shader-safe tile；
- UI-04 / UI-05：按显式 atlas state 取 `AtlasTexture`；
- UI-06：透明 mask 上做受控 modulate，不修改故事或玩法时序。

最低动效节奏：

| 状态 | 建议时长 | 行为 |
| --- | --- | --- |
| 对话框入场 | `140–180ms` | alpha 0→1，垂直位移不超过 10px，`CUBIC_OUT`；不得覆盖地图中央 |
| Speaker settle | 入场后延迟 `30–50ms`，持续 `100–130ms` | 名字牌轻微横移／缩放回稳；不做弹跳 |
| 当前进度珠 | `800–1000ms` 循环 | 亮度／alpha 小幅呼吸；不得闪烁成警报 |
| 下一步提示 | 文本可读后 `900–1200ms` 循环 | glyph 呼吸；按下时立即切 `pressed`，推进后隐藏 |
| 对话框退场 | `90–130ms` | 快速淡出／下移；玩法控制恢复前完成 |

程序不得把视觉 tween 时长写回 resolver，不得改变 beat ID、台词、推进次数、存档或输入语义。键盘、鼠标、手柄推进仍必须共享同一行为。

## 7. 用户实际帧停门

接入后至少捕获：

- B06 左动作切片实际帧；
- E07 远程通讯实际帧；
- 一个无人物 wide fallback 实际帧；
- 同一 beat 的入场中帧／稳定帧／退出中帧；
- 深色、浅色与品红 QA 底的组件 alpha 板；
- 1280×720 100% 与 50% 缩略并排板。

机器门只检查路径、SHA、RGBA、alpha、九宫格 margin、atlas state、beat 消费和 fallback；**不签视觉通过**。制作人必须先看真实帧，再回主对话让用户判断是否达到此前要求的 GF 交互完成度。未通过前：

```text
formal_gf_dialogue_skin_loaded = false
integrated_visual_playtest_ready = false
runtime_allowed = false
runtime_handoff = none
user_visual_acceptance = false
```

## 8. 明确不改动

- 不修改 `story_bridges.json`、Current Reader、Canon、Default、Save 或正式 Runtime；
- 不激活 B06／E07 action-slice Candidate binding；
- 不覆盖现有六个 story action-slice 兼容 beat；
- 不把机器 PASS、review composite 或单张 PNG 写成用户视觉批准；
- 不在主程序会话重新生成第二套平行美术。
