# C01E02 A8 B1.1｜动作重量与接触可读性窄返修目标

> Owner：美术资产 Session
>
> Lifecycle：`Candidate`
>
> `runtime_allowed=false / runtime_handoff=none / exact_handoff=false`
>
> Parent dispatch：`52-c01e02-a8-v10x-scoped-user-decision-and-phase-b-dispatch.md`

本轮只修制作人对 A8 B0/B1 综合包识别出的视觉执行缺陷；不重选身份、不改变玩法／剧情／footprint，也不扩制作范围。

## 0. 输入与制作人结论

- 52 号 SHA-256：`d65c85e4a9778e84cb4356dcd6ced40269d474ec064c7562e8b0deb414c9ad38`
- B0/B1 manifest SHA-256：`9d8b32a32352d46be55e9ac19b518034038b15927f942045cafbbb861e57da69`
- B0/B1 completion report SHA-256：`93af1728f9fb51bb9ab0e2bf70bdc120ca52bc0f78c727bfb415bf019fa49c1d`
- B0/B1 core hash list SHA-256：`09cb64f2964382ba7a7eee31850776c8d44cf653056896c478027d33fb666ca8`

技术包、来源链、尺寸／alpha／pivot登记与生命周期检查通过；但制作人视觉门结论为 `REVISION_REQUIRED_BEFORE_U1B`。当前包只能保留为方向证明，不能据此扩完整 Atlas、进入 Phase C、签 P1 或接入 Godot。

## 1. 冻结不变

- 馆守 Z：V10X 裸机身份、红色肩前甲独立锁块、A1-C 动作骨架；无 V21 飞翼。
- BREAKER：B“前肢承重半直立型”＋X“异质／生体装甲”；头部红缝、闭合胸缝、封闭上背核心出口。
- 重盾：A 高窄塔盾＋F-D70/P30、墙挂、尚未取得、恰好三处旧焦痕。
- 应急车辆沿用 B0/B1 原文件与 SHA，不返修。
- A4 地图、A5 小体、既有逻辑格、footprint、朝向与剧情状态全部保持。
- 仍只制作馆守 Z `south` 与 BREAKER `north`，不得扩完整四向 Atlas。

若返修需要改变上述身份、比例合同、动作种类或剧情状态，写 `BLOCKED.md` 并停止。

## 2. 馆守 Z south 五动作

保持 `idle / step_a / step_b / brace / recoil`，单格 `256×256 RGBA`，pivot `[0.5,0.88]`。

- `step_a/step_b` 必须有可读的左右交替迈步、骨盆重心偏移和对侧肩臂补偿，不能只是整体平移、缩放或肩宽变化。
- `brace` 必须读出降重心、双脚撑地、肩臂迎击和躯干压缩。
- `recoil` 必须读出受力后的上身回仰／侧退与惯性余量，同时双脚仍能解释支撑。
- 五帧底部基线不得漂移；V10X 头冠、面栅、红肩、圆核和粗圆柱前臂不得丢失。
- 无文字标签、原生 1:1 与 50% 显示时，至少能仅凭轮廓区分 `idle / 行走 / brace / recoil`；`step_a/step_b` 能看出相反支撑脚。

禁止增加盾、飞翼、火箭拳、缺臂、武器或新动作。

## 3. BREAKER north 三动作与 X 表面

保持 `idle / charge / contact`，单格 `320×320 RGBA`，pivot `[0.5,0.9]`，3×3 footprint。

- 保留 B 型前肢承重半直立轮廓。
- 把当前过度对称、硬直线机械分板收束为受控的 X 表面：轻微非对称覆甲、柔性闭合缝与生长层叠感；这些特征必须在原生地图尺寸可见。
- `charge` 必须出现低头、前移、压低重心、前肢抓地和后体蓄势。
- `contact` 必须出现明确的冲击压缩、前肢承载和回弹准备，不能只是待机帧放大或下移。
- 三帧保持红缝、闭合胸缝和封闭上背出口；不得打开核心、展开飞翼或制作 E03 破甲状态。
- `contact` 的 alpha 左、右、上边缘至少保留 8px 安全区，不得触边；三帧接地点基线一致。

## 4. T3 接触可读性

重做 A4 初态比例板与 `1280×720` T3 接触／界面裁切，但不得改变逻辑格、朝向、救援线和剧情状态。

- 调整姿势、镜头裁切与绘制顺序，让馆守 Z 的 `brace` 和 BREAKER 的 `contact` 同时可读。
- 双方头部／视觉焦点、主要躯干及至少两个支撑点必须可见；任一单位不得遮挡另一单位超过约 50% 的关键身份轮廓。
- BREAKER 必须明确读成更大、更重的 3×3 威胁，但不得擅改 footprint 或物理身高合同。
- 建筑淡出、轮廓与 UI 不得吞掉红缝、馆守 Z 头冠或双方接地点。
- 墙挂盾仍是场景物，状态保持 `wall_hung`；赤红冲击仍为 `not released`。

## 5. 旧守护者三态稳定性

保持 `guide / contact / shield_gaze`、单帧 `1024×768`、三联 Atlas `3072×768`、pivot `[0.5,0.5]`。

- 三态共用同一头胸主体锚点；头胸主体中心误差不超过 2px。
- 肩、头冠和胸甲外轮廓逐帧叠加不得可见横跳。
- 只通过胸灯、扬声波形和轻微视线／光强调区分状态；`shield_gaze` 不得靠整幅水平位移表达。
- 继续明确为馆守 Z 同一主体，不加入人类头像、独立 AI、副驾驶或 V21 飞翼。

## 6. 重盾旧焦痕

- 保持现有盾形、尺寸、颜色比例、墙挂横杆、pivot与未取得状态。
- 将规则同心圆／接口状痕迹改为三处略不规则的烧蚀边、暗色热蚀中心与有限旧损晕染。
- 禁止增加第四道焦痕、贯穿、裂解或后续章节损伤。

## 7. 最低交付与停止点

只交：

1. 馆守 Z south 五动作修正版与动作条。
2. BREAKER north 三动作修正版与动作条。
3. 旧守护者 V10X 三态修正版与三联 Atlas。
4. 墙挂盾焦痕修正版。
5. A4 初态比例板与 T3 `1280×720` 裁切修正版。
6. 一张 B1.1 前后对比板。
7. 更新后的 manifest、SHA-256、尺寸／alpha／pivot 审计、validator 与完成报告。

应急车辆登记为“沿用 B0/B1 原字节未改”。完成后停止并回传制作人集中评审。

本轮禁止：完整四向 Atlas、新动作类型、车辆动画、Phase C、GIANT_CONTACT、Cut-in、FX、音频、LibTV、Godot、Runtime copy、exact handoff、Canon／Current 晋升，以及纪存／七海／兜灯／720p 总体布局返修。
