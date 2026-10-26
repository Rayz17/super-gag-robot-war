# 馆守 Z south 持盾三姿势 Sprite 母版｜Call01 失败封存

> Decision: `VISUAL_FAIL_STOP`
>
> Deliverable result: `NO_REGISTERABLE_SPRITE_EXPORTED`
>
> Retry: `0 / forbidden in this task`
>
> Runtime / Godot / Canon: `false`

## 调用边界

- Mode: `built-in ImageGen / one call only / 0 reroll`
- Built-in output ID: `01a0305c-4159-7012-8dbd-24f6bcdb5e0b`
- Prompt: `../../IMAGEGEN_FINAL_PROMPT.md`
- Geometry hard gate: `../../GUIDE_HARD_GATE.md`
- Raw: `../generation-raw/GUARDIAN_Z_SOUTH_SHIELD_HOLD_BLOCK_BASH_CALL01_RAW.png`
- Raw size: `1536x1024`
- Raw format: `PNG / RGB / hasAlpha=no`
- Raw SHA-256: `a446371cea9ac09e14d36ad66d68032323d6470b275f3dc34920e970e2d75f62`

## 唯一允许输入

| Role | Path | SHA-256 |
| --- | --- | --- |
| CML008 Hard 馆守 Z 身份 | `.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png` | `a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521` |
| A17 用户接受的盾设计基底 | `art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png` | `169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305` |
| 本轮姿势几何 Guide | `guide/GZ_SOUTH_SHIELD_THREE_POSE_GEOMETRY_GUIDE_1536x1024.png` | `32535ddf5a3350830867abb046ea0dd25f63be564e2869f008f384b383c76df7` |

本轮没有读取或复用 A18 / A19 失败 raw、旧 A2 弹孔板、V10X `approved=false` 或 east Sprite；没有镜像 east 伪造 south。

## 通过项

1. 三格大体保持同一个馆守 Z 身份，头冠、胸甲、圆肩与老式重装甲可追认 CML008。
2. 三面盾大体保住 A17 的收尖轮廓、厚边、中脊、蓝白金配色、三道旧痕与红色新热痕。
3. 三个身体均保留 E02 双臂状态，没有提前套用 E03 缺右臂。
4. HOLD、BLOCK、BASH 的腿部重心存在一定差异。

这些通过项不足以晋升为 Sprite。

## 阻断项

1. **透明通道硬失败**：输出是 RGB，`hasAlpha=no`；画面中的灰白棋盘已经烘进像素。不能交付要求的 256x256 RGBA，也不能通过确定性裁切得到干净边缘。
2. **双手握把证据失败**：每格盾牌都遮蔽了至少一只手与大部分握把；可见前臂没有同时证明两条“肩—肘—腕—闭合手—背面握把”连续承力链。不能排除单臂承盾或手漂在盾侧。
3. **BASH 接触姿势失败**：第三格仍以大面积盾正面朝镜头，钝厚盾边没有成为明确的接触先导；动作更像低姿顶盾，不能独立读成双手横拍接触帧。
4. **south 视轴不足**：头胸仍接近正面英雄展示视图，三格没有稳定命中 Camera V2 south 的左下三四分主轴。
5. **256 像素可读性未成立**：缩到地图规格后，被盾遮住的双手与握把只会进一步消失，因此不得用原图切片冒充动作 Sprite。

## 封存动作

- 不做棋盘格去背、补画手、镜像、液化、拼贴或二次生成；这些操作无法同时修复接触关系、BASH 透视和 south 视轴。
- 不输出 `GZ_SOUTH_SHIELD_HOLD_256.png`、`GZ_SOUTH_SHIELD_BLOCK_256.png` 或 `GZ_SOUTH_SHIELD_BASH_CONTACT_256.png`。
- 不输出 pose manifest / sockets，因为不存在可注册的 Sprite 像素。
- 不修改 `candidate_ground_mecha_bindings.json`，不接 Godot，不迁移 Canon，不请求用户实际帧验收。

## 结论

本轮唯一 ImageGen 调用未达到“实际 Sprite 源”门槛，按任务约束在 Section 2 内部封存。下一次有效生产必须由美术在同一锁定母版上直接绘制两手、握把、隐藏面与 BASH 侧缘透视；不能再依赖一次多姿势生成图自动解决物理接触。

