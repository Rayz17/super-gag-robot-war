# A23-R1｜Call02 前结构准入回执

> Status: `STRUCTURE_GATE_PASS_FOR_SINGLE_TARGETED_IMAGEGEN_EDIT / CANDIDATE_ONLY`
>
> Date: `2026-08-24`
>
> ImageGen calls in rework01 before this gate: `0`
>
> Runtime: `false`
>
> Canon promotion: `false`

## 输入

- 用户裁决后的返修 Brief：`../00-USER-DIRECTED-STRUCTURE-CORRECTION-BRIEF.md`
- 可目视结构板：`../source-guides/WANJI_A23_R1_GROUND_UNDERGROUND_TRANSFORMATION_PROOF.png`
- 可编辑源：`../source-guides/WANJI_A23_R1_GROUND_UNDERGROUND_TRANSFORMATION_PROOF.svg`

## 四项准入结论

| 用户根因 | 结构板结论 | 图上证明 |
| --- | --- | --- |
| `ABOVE_GROUND_MUSEUM_IDENTITY_MISSING` | `PASS_FOR_ONE_EDIT` | 固定馆明确有南入口／门楣、L1 主展厅、大屋面、L2 展廊和 L3 档案脊；同色馆冠整体进入巡展舰上层，并分入人形胸、肩内侧和上背 |
| `GROUND_UNDERGROUND_MAPPING_UNPROVEN` | `PASS_FOR_ONE_EDIT` | 固定馆切面显示更大的 B1/B2；B1 成为舰腹龙骨、人形背脊／骨盆／腿内整备舱；B2 核心三态保持中央连续，外围承力壳才进入腿足 |
| `MILITARY_OVERREAD` | `PASS_FOR_ONE_EDIT` | 服务梁改为绿色吊装／展陈作业架；金色卷扬鼓、缆线出口与锚头在舰态和人形前臂都可见；炮塔轮廓删除，近防只剩檐下小开口 |
| `HEAD_GENERIC` | `PASS_FOR_ONE_EDIT` | H1/H2/H3 小轮廓并列筛选；内部选择 H2 偏心未闭合检索环＋H1 厚馆门楣，具备独立头壳和短颈，无双眼、鼻、嘴，也不再是通用横向 visor 头 |

## 结构不漂移项

- 只保留 A23 Call01 已被用户接受的低矮巡展体→巨型人形方向、装甲闭窗和同源部件原则；
- A23 Call01 的军用装甲车外观、炮塔、通用头部与“红窗带等于博物馆”的解释全部退回；
- 地上馆冠是身份层，不承担大多数质量；B1/B2 是巡展舰与未来人形的主身体；
- B2 封闭核心不拆分、不展示内部；
- 馆藏与展品不变形成装甲；
- C01 仍不出现人形。

## 一次 edit 边界

允许一次 built-in ImageGen 定向 edit，`0 reroll`：

- Image 1：A23 Call01，角色为 `edit target`，只保留两形态总体方向与画面工艺基线；
- Image 2：A23-R1 结构板，角色为 `supporting structure reference`，只约束构件身份、比例、映射和无脸头；
- 输出若仍先读成军事载具、馆冠缺失、地下去向不清或头部通用，则直接 `SECTION2_FAIL_STOP`；
- 无论成功失败都不接 Godot、Runtime 或 Canon。
