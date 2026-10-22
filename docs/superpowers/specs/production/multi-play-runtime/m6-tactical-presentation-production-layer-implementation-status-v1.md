# M6 Tactical 表现生产层实现状态 v1

> 日期：2026-07-15  
> 状态：Candidate runtime proof passed  
> Canon 边界：`runtime_validation_only`

## 1. 本轮解决的问题

旧版 M6 Tactical 虽然已有斜 45 度地图、武器预测、敌方意图和六个稳定对象映射，但机体仍主要是圆点，探索差异只显示为侧栏文字，攻击和第二回合坍塌没有消费战斗表现运行时。

本轮将 P3 从“规则映射成立”推进到“地图、招式和战中事件可见地承认此前状态”。

## 2. 新增共享运行时

- `scripts/core/presentation/battle_presentation_catalog.gd`
  - 加载并校验数据化表现清单。
  - 解析单位地图图、攻击 Profile、事件 Profile、Full/Short/Off 步骤。
  - 按已知稳定对象与事件 Variant 选择演出版本。
  - 校验资源路径、Profile 引用和单位状态图。
- `battle_presentation_director.gd`
  - 优先读取声明式清单；未声明时保留 C01 馆守 Z 和通用攻击回退。
- `battle_presentation_player.gd`
  - 标题、副标题、页脚、人物、台词和裁切区域数据化。
  - 支持 `boxing` FX，不再把所有机体画成馆守 Z 掌部防卫。
  - 只在 `runtime_validation_only` 中允许 `runtime_validation_candidate` 候选图。
- `tactical_mode_scene.gd`
  - 地图单位从清单读取 Texture2D。
  - 攻击与战中事件结算后播放可跳过演出。
  - 演出播放期间锁定战棋输入，结束后继续胜败检查。
  - 阶段菜单可切换 Full、Short、Off，选择随存档恢复。

## 3. M6 数据与资产

表现清单：

- `assets/battle_presentation/m6/old_boxer/manifest.json`

候选运行时资产：

- `sprite_old_boxer_map_idle_v01.png`
- `pose_old_boxer_missed_beat_v01.png`
- 唐胶 Cut-in 暂复用候选人物图并声明裁切区域。

新图由 OpenAI built-in imagegen 参考 M6 维修棚中的完整旧拳王机生成，再用 `remove_chroma_key.py` 去除纯色背景。身份锚点保持：约 3 米完整机身、米白头甲、窄红眼、磨损青灰躯干、红色维修右臂、暴露关节、左膝缠带与重脚。右拳护具没有被制作成独立单位。

所有新图均为 `runtime_validation_candidate`，不是正式锁定美术。

## 4. 状态驱动事件

`M6-C02-RING-COLLAPSE` 现有三种状态：

1. `default`：敌方阶段后，坍塌再对仓门造成 1 点损伤。
2. `exit_warning_known`：调查过仓门报警器，货柜领袖提前抢位，不再追加坍塌损伤。
3. `controlled_rescue`：调查仓门且打开维修草案，旧拳王左膝落地、右拳顶门；不追加坍塌损伤，并播放专属人物 Cut-in、标志 Pose 和事件页脚。

敌方拍卖锤原本造成的攻击损伤不会被探索状态抹掉。测试比较同回合默认与 controlled 分支，后者仓门完整度恰好多 1，证明变化来自坍塌事件，不是删掉敌方行动。

## 5. 状态驱动招式

旧拳王两项武器进入声明式表现：

- `body_jab`：唐胶提示先让旧膝接住重量，标志 Pose、拳击 FX、停顿、震动和伤害反馈。
- `missed_beat_guard`：默认是救援优先的停拳；若 Spatial 已看过原速录像，改为 `original_timing_restored`，唐胶明确说“别补那一拍”，标题与页脚显示原速空拍。

## 6. 编译门禁

`EpisodeBundleCompiler` 新增：

- 战斗定义声明的表现清单必须出现在 Episode `presentation_assets`。
- 清单内每个运行时图片必须被 Episode 显式声明。
- 清单 JSON、资源路径、单位图、Profile 和 asset ref 必须通过校验。
- Bundle 写入 `battle_presentation_manifest_validated=true`。

M6 Bundle 当前：

- `resource_count=11`
- `source_fingerprint=b838cddf609cc4b1eaf7d70677d9415c83906378a6682d8f027d6889409aa34c`
- `experience_production_gate_status=structure_pass_capacity_pending`

负向测试会从 Episode 声明中删掉旧拳王地图图，编译必须以 `undeclared_battle_presentation_asset` 拒绝。

## 7. 自动化与像素证据

专项自动化覆盖：

- M4 Tactical 旧流程仍可实例化、存取与结算。
- M6 表现清单、单位地图图和 Profile 校验。
- 仓门 + 维修草案选择 `controlled_rescue`。
- controlled 分支仅免除额外坍塌损伤。
- 原速录像切换 `漏拍停拳` 演出 Variant。
- 右拳护具不出现在战斗单位列表。
- 编译器拒绝未声明的 Tactical 表现资产。

GPU 截图：

- `outputs/multi-play-presentation-validation/06-m6-tactical-object-continuity.png`
- `outputs/multi-play-presentation-validation/07-m6-tactical-held-punch-presentation.png`
- `outputs/multi-play-presentation-validation/08-m6-tactical-collapse-presentation.png`

截图证明完整旧拳王机已进入斜 45 度地图，原速漏拍和 controlled rescue 都有独立标题、Pose 和来源说明。它们不证明正式美术、真人理解或平台兼容。

## 8. 尚未完成

1. 其余八个地图实体已由 P3b 补成独立 A 档程序化轮廓，不再使用圆点；百刃、影子陪练和货柜领袖仍需升级为正式地图 Sprite。
2. 旧拳王只有一张地图待机图和一张 Pose，尚无独立移动、受击、顶门与回位帧。
3. 唐胶 Cut-in 仍来自候选人物合图，需正式横幅构图。
4. 正式音效、配音、碰撞闪白、相机轨迹和性能档尚未验收。
5. standard 真人容量、Windows 真机和实体手柄仍未执行。
6. M6 不因此成为正式 C02E03，也不提升 V35 状态。
