# A19 根因修正版：来源审计与输入角色

> **SUPERSEDED SOURCE ROUTE / HISTORY ONLY（2026-08-24）：** 本包把 CML008 旧图当正向馆守 Z 像素源的路由已被 130 号禁止。新 Section 2 只能从 CML130/V10X 限域母图制作，并必须重新绘制 Camera V2 各朝向／状态 Sprite；本包只作失败追溯。

Date: 2026-08-23  
Lane: `Candidate / user=false / runtime=false / canon=false`

## Authority result

- `python3 scripts/report_v35_layered_pipeline.py --check`：dashboard current。
- `scripts/canon-query.sh CML008`：馆守 Z 的当前 Hard Art Lock 为 `CML008`，状态 `locked_current`；E02 是双臂重盾态。
- 馆守 Z 当前生命周期实体为 `V353U001`；R2/R3 均在原右前臂毁损前，因此两条原装手臂必须完整。
- 本包不迁移任何故事、Canon、Runtime 或 Godot 绑定。

## ImageGen 三个且仅三个像素输入

1. **Image 1 / 唯一身份像素源 — CML008 Hard**
   - `/Users/rayz/Documents/超gag机器人大战/.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`
   - SHA-256 `a9688f07d923d79680e1ba13a1cc51135b72dd29b38cf25242e2239107b86521`
   - 只提供馆守 Z 身份、色彩、头胸、四肢与老派超级系重量。
2. **Image 2 / 唯一盾像素源 — A17 user accepted shield base**
   - `/Users/rayz/Documents/超gag机器人大战/docs/superpowers/specs/production/c01-current-demo-v1/art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`
   - SHA-256 `169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305`
   - 只提供盾冠、主承力脊、厚边、背面双把/承力轨、三旧擦压痕与第四热痕。
3. **Image 3 / 无身份几何导图**
   - `guide/GZ_SOUTH_R2_R3_GEOMETRY_GUIDE_1536x1024.png`
   - SHA-256 `6182ffbe53ab3c64190ffd211b3e6705fe9c3892dc958ad59ade9b8f469ce439`
   - 只提供 Camera V2 south `[-40,+24]`、BLOCK/BASH 两种轮廓、`body_back -> shield -> forearms/hands_front` 层级与两手握把接触。
   - 导图颜色、文字、箭头、机器人几何均禁止成为成品身份或画面元素。

## 全量禁用

- A18 的原图、裁切、Prompt 或任何像素。
- V10X（本任务定义 `approved=false`）、QSD 四视图与其衍生图。
- 旧 east、A13 持盾稿、A2/A14 三孔板/弹孔装甲板。
- 任何其他馆守 Z 像素源；任何其他盾像素源。

## Stop rule

- 几何导图须先在 100% 与 50% 目视：三秒首读唯一为“左：双手正面格挡；右：双手横向盾拍；二者都朝屏幕左下 south”。若不唯一，不调用 ImageGen。
- guide 通过后仅允许 built-in ImageGen 一次、0 reroll。
- 身份、双臂/双手接触、动作差异、south 方向或真实 alpha 任一失败，立即封存；不做用户确认板、不接 Godot/Runtime/Canon。
