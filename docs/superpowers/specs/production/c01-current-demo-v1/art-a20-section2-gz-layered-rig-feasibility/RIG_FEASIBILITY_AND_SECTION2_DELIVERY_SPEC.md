# 馆守 Z 持盾分层 2D 可行性与 Section 2 最小交付规格

> Status: `RIG_TECHNICAL_PROOF_NOT_CANDIDATE`
>
> Gate: `INFEASIBLE_FROM_ALLOWED_PIXELS`
>
> Runtime: `false`
>
> Canon migration: `false`
>
> Godot binding: `false`

## 1. 裁决

只用当前允许的两张像素源，**不能**以确定性蒙版、分层旋转和遮挡变换，产出能通过视觉门的 Camera V2 south `BLOCK` / `BASH` 馆守 Z 地图动作。

能做的只有：

- 把 A17 重盾的正面、背面和侧面分别裁出为透明图层；
- 把盾盖在 CML008 待机机体的展示板像素上，或只旋转盾牌。

后者的结果仍然是“待机机体上贴了一面盾”：双手不握把，双肘不屈曲，躯干和重心不随动，也不能建立 south `[-40,+24]` 的统一视轴。因此停止伪 rig，不生产可被误认为美术 Candidate 的图。

视觉证据：

- `qa/RIG_SOURCE_FEASIBILITY_AUDIT_NOT_CANDIDATE_2400x1600.png`
- `qa/RIG_SOURCE_FEASIBILITY_AUDIT_NOT_CANDIDATE_1200x800.png`
- `qa/source-pixel-audit.json`

## 2. 允许源的像素审计

### 2.1 馆守 Z 唯一身份源

- Path: `.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`
- Authority: `CML008 Hard / locked_current`
- SHA-256: `a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521`
- Pixels: `1254x1254 / RGB / no alpha`
- 内容：一张已压平的设定展示板，包含主人形、头像、背面插图、手部插图、展馆背景和信息栏。

不足：

1. 主人形与展馆背景完全烘在 RGB 中，没有主体 alpha 或任何原始分层。
2. 主人形只有垂臂、张手、近正面的待机姿态。
3. 左右上臂、前臂、手、肩关节与躯干在像素上相互遮挡；被挡住的装甲表面不存在。
4. 手部插图仍是张手，没有握住 A17 背面握把的封闭手型。
5. 背面插图可以补充身份识别，但它不是 south 持盾视图，也不能补出屈肘后露出的侧面。

### 2.2 重盾唯一像素源

- Path: `docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`
- Authority: `A17 USER_ACCEPTED_SHIELD_DESIGN_BASE / Candidate`
- SHA-256: `169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305`
- Pixels: `1536x1024 / RGBA`
- Alpha extrema: `(0, 254)`
- Fully transparent: `703274` pixels
- Partial alpha: `869590` pixels
- Fully opaque: `0` pixels

正面、背面和侧面在画布上分开，可以依靠 alpha 和固定裁切框独立提取。这只证明“盾牌可拆”，不证明“馆守 Z 可拆”。

## 3. 精确缺失的人工绘制层

如果要保留“可控分层 2D”路线，Section 2 至少需从 CML008 身份重画以下透明层。它们不能从现有像素确定挖出：

| ID | 必需层 | 作用 | 不能从现图挖出的原因 |
| --- | --- | --- | --- |
| `GZ_S_BODY_BASE` | south 三四分头、胸、腰、髋、双腿与脚 | BLOCK / BASH 共用身体与 pivot | 现图为近正面，且肩臂遮挡躯干侧面 |
| `GZ_S_L_UPPER_ARM` | 左上臂，含肩 / 肘连接面 | 受控屈肘 | 上臂与胸背遮挡交叠 |
| `GZ_S_R_UPPER_ARM` | 右上臂，含肩 / 肘连接面 | 受控屈肘 | 同上 |
| `GZ_S_L_FOREARM_BLOCK` | BLOCK 左前臂 | 从侧后方指向左握把 | 现图前臂垂下，方位和可见面不同 |
| `GZ_S_R_FOREARM_BLOCK` | BLOCK 右前臂 | 从侧后方指向右握把 | 同上 |
| `GZ_S_L_FOREARM_BASH` | BASH 左前臂 | 维持双手承力链 | 需新的屈肘、扭身与透视 |
| `GZ_S_R_FOREARM_BASH` | BASH 右前臂 | 维持双手承力链 | 同上 |
| `GZ_S_L_GRIP_HAND` | 左闭合握手，含指节绕把 | 左手-握把接触 | CML008 只有张手 |
| `GZ_S_R_GRIP_HAND` | 右闭合握手，含指节绕把 | 右手-握把接触 | CML008 只有张手 |
| `GZ_S_BLOCK_OCCLUSION` | BLOCK 盾-身-手遮挡遮罩 | 保证手在背面握把，不漂在盾正面 | 现图没有盾与机体合作的原始层级 |
| `GZ_S_BASH_OCCLUSION` | BASH 盾-臂-身遮挡遮罩 | 保证横拍时双手仍真正连着盾 | 同上 |
| `GZ_S_BLOCK_LEG_WEIGHT` | 前后脚弓步 / 压地重心 | 读出承冲、被推退的起点 | 现图是对称站立 |
| `GZ_S_BASH_TORSO_LEG` | 腰髋扭转和蹬地腿 | 读出双手横拍而不是旋转盾图 | 现图没有动作所需的隐藏面 |

## 4. Section 2 最小交付：两张固定姿势，不做逐帧动画

为控制成本，建议不让美术制作一套通用骨骼动画或逐帧连打。最小可用交付只要两张固定关键姿势：

1. `GZ_SOUTH_SHIELD_BLOCK`
   - Camera V2 south，屏幕前向 `[-40,+24]`。
   - E02 时点两条原始手臂必须完整，不得提前缺右臂。
   - 馆守 Z 在盾后；双手握住盾背面两套握把或可见地绕住两侧承力边，不得把手画在盾正面。
   - 肩-肘-腕-握把形成两条可追踪的承力链；双脚前后压地。
   - 盾面位于 BREAKER 与胸口之间，盾正面对外。

2. `GZ_SOUTH_SHIELD_BASH_CONTACT`
   - 沿用同一 south 视轴、身份比例和脚点系统。
   - 双手全程不离盾；双肘屈曲，躯干扭转，前脚压地，后脚推蹬。
   - 用 A17 的钝厚盾边发生接触，不得读成刀刃、枪口或只旋转了盾的贴图。
   - 输出一张接触姿势即可；程序通过整体位移、`hit-stop`、受击震动、接触闪光和碎屑补成动作，不要求美术逐帧画。

## 5. 技术格式与接触证据

每张姿势需同时交付：

- 制作源：`1024x1024 RGBA`，透明背景，不带地图、棋盘、展馆或栏目。
- Runtime 裁切：`256x256 RGBA`，pivot `[128,224]`，馆守 Z 始终为 `2x2 footprint`。
- 透明门：alpha 必须同时包含 `0` 和 `255`；不接受背景烘入、黑底或棋盘烘入。
- 身份门：头部金色角冠、红蓝胸甲与中央星标、圆肩、老式重装甲、双臂不对称色块必须来自 CML008；不得回退到任何旧稿身份。
- 盾牌门：只读 A17 的盾冠、收尖轮廓、厚边、中央承力脊、背面双握把与蓝白金老装甲。
- 接触放大图：另交左手-左握把、右手-右握把的 `4x` 放大图，要能看见掌面、指节、握把和盾背承力框的物理连续。
- Socket 数据：每姿势给出 `left_grip_socket`、`right_grip_socket`、`shield_center_socket`、`shield_impact_socket`、`foot_pivot`的 256 画布像素坐标。

## 6. 视觉停止门

下列任一项不成立，Section 2 必须停在内审，不得请求 Godot 绑定：

1. 去掉 south 箭头后，头-胸-髋-脚的主轴仍能首读为屏幕左下。
2. BLOCK 时两只手都与两套背面握把真正接触，盾正面对外，机体不是用背拿盾。
3. BASH 时两只手、双肘、腰髋与脚步共同发力，不是只转动盾牌。
4. E02 两条原始手臂完整，没有提前套用 E03 缺右臂状态。
5. 50% 缩放与实际 `256x256` 中仍能读出盾冠、双手接触、承冲 / 横拍两种不同动作。

## 7. 边界

本包没有读取或复用 A18 / A19 失败 raw、V10X `approved=false`、A2 / A13 / A14、east Candidate 或任何其他馆守 Z 像素。没有调用 ImageGen，没有绑定 Godot，没有将技术审计板冒充成美术完成或用户验收。
