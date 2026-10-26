# A23 Call02｜Section 2 定点结构返修用户目视回执

> Status: `USER_REVIEWED / OVERALL_NOT_ACCEPTED / TRANSFORMATION_MAPPING_DIRECTION_RETAINED / MODERN_MUSEUM_CARRIER_ELEGANCE_LOST / BOXY_INDUSTRIAL_FORTRESS_OVERREAD / HEAD_DIRECTION_NOT_ACCEPTED / REWORK_REQUIRED / CANDIDATE_ONLY`
>
> Date: `2026-08-24`
>
> Runtime: `false`
>
> Godot binding: `false`
>
> Canon promotion: `false`
>
> User approval: `rejected_for_call02`

## 0. 用户最新裁决（覆盖生成时首读）

- Call02 整稿不接受；不得作为后续正向像素母版。
- 只保留“固定展馆→低矮巡展舰→未来巨型人形”的形态方向，以及地上馆冠／地下 B1/B2 的同源映射证明。
- 本稿丢失了此前较好的现代展馆与巡展舰流线，整体重新读成方盒、工业堡垒和纯军事工程体；不能作为“现代高科技展馆＋战舰＋大型游艇＋飞船”的综合方向。
- 头部虽有实体且无五官，但“巨型偏心环＋竖槽”不获接受；Call03 必须改为万机馆专属的简洁装甲面块＋天线群／馆冠式头雕，不得成为无头、写实人脸或通用杂兵头。
- 巨型传统链锚与龙门架过度抢占首读，后续只允许以收纳式救援锚／绞盘、服务梁和装备投放结构存在，不得压过公共馆身份。

## 1. 用户裁决继承

- A23 Call01 整稿继续保持：`OVERALL_NOT_ACCEPTED / REWORK_REQUIRED`。
- 只继承用户接受的低矮巡展体→巨型人形方向。
- 本次不是复活 Call01 外观，而是对 `MILITARY_OVERREAD / HEAD_GENERIC / ABOVE_GROUND_MUSEUM_IDENTITY_MISSING / GROUND_UNDERGROUND_MAPPING_UNPROVEN` 四项做定点结构返修。

## 2. 调用事实

- rework01 Built-in ImageGen edit 实际调用：`1`
- rework01 reroll：`0`
- A23 全节点累计正式 ImageGen 调用：`2`（Call01 generate 1 + Call02 edit 1）
- CLI／API fallback：`0`
- Image 1：A23 Call01，角色仅为 `edit target`；不把用户退回外观当正向答案
- Image 2：A23-R1 结构板，角色为 `supporting structure reference`
- 精确 Prompt：`../../rework01/prompts/CALL02-TARGETED-BUILTIN-IMAGEGEN-EDIT-PROMPT.md`

## 3. 交付物

- 用户目视候选：`../delivery/WANJI_A23_CALL02_MUSEUM_MOTHERBODY_TARGETED_REWORK_CANDIDATE.png`
- 尺寸：`1586 × 992`
- 色彩：`RGB`
- SHA-256：`b12089837330ab4d75b3753100caf27bd4979796b7500c94599ff2bebc04edc9`

## 4. 生成当时制作人首读（已被第 0 节用户裁决覆盖）

| 用户根因／硬门 | 当前结论 | 图上证据与边界 |
| --- | --- | --- |
| 形态方向不得推倒 | `PRESERVED` | 左侧仍为低、宽、深的巡展舰，右侧仍为同源巨型人形；没有退回外骨骼或普通馆楼站起 |
| `ABOVE_GROUND_MUSEUM_IDENTITY_MISSING` | `RECOVERED_FOR_USER_REVIEW` | 左上固定馆切面有完整开放主展厅、连续公共展层、机器人展陈与大屋面；同一屋面、展廊和中央入口进入巡展舰上层，并成为人形胸肩背 |
| `GROUND_UNDERGROUND_MAPPING_UNPROVEN` | `VISIBLE_AT_MAJOR_MASS_LEVEL` | 固定切面明确显示地上馆冠只占上层，地下机库／封闭母体明显更大；舰态深色巨舰腹、人形深色骨盆与腿足保持同一主质量语言。B2 单一核心在人形内部的精确落位仍被外甲遮蔽，后续结构定稿不得把腿部梅红面板误写成拆分核心 |
| `MILITARY_OVERREAD` | `SUBSTANTIALLY_REDUCED` | Call01 的枪管、肩炮和炮塔群全部消失；两侧为有滑车／工具端的展陈作业龙门架；舰腹与前臂明确出现卷扬、链缆和锚头；战斗依靠盾甲、作业手、锚与质量 |
| `HEAD_GENERIC` | `REWORKED_FOR_USER_REVIEW` | 头部为独立实体头壳＋短颈；厚馆门楣冠与偏心未闭合机械检索环形成缩略图识别；前面只有竖向技术槽，无横向眼罩、双眼、鼻或嘴 |
| 战斗态玻璃防护 | `PASS_WITH_LOCAL_DETAIL_RISK` | 固定馆 inset 可开放玻璃；巡展舰／人形的大展窗均转为暗红百叶。人形下胸入口仍露出少量纵向内构，需用户认可母方向后明确为闭合双层馆门，而不是开放玻璃入口 |
| 双形态作业／救援优先 | `PASS_FOR_USER_REVIEW` | 舰态龙门架、人形肩背作业架，舰腹锚具和人形前臂锚具均可追认；仅保留小型状态缝与推进口，没有重炮 |
| 既有 IP 复制 | `NO_POSITIVE_IP_PIXEL_INPUT` | 只编辑本项目 Call01 和原创结构板；无外部 IP 图片输入。检索环、馆门楣、馆冠／地下母体映射保持原创 Candidate |

## 5. 真实残余风险

1. `B2_INTERNAL_MAPPING_DETAIL_GATE`：主质量映射已成立，但外观板没有剖开人形骨盆；B2 连续核心的精确内部位置仍需后续确定性结构图证明，不能靠两块腿部色板推断。
2. `CIVIC_GATE_COMBAT_CLOSURE`：人形下胸馆门内部仍可见少量纵向结构；若母方向通过，应把它锁成装甲双门＋深层防爆百叶。
3. `ANCHOR_LITERALNESS`：链锚很清楚，但可能过于接近传统船锚；需要用户判断万机馆是否应保留这种直接、老巡展设备感，还是改成更现代的可展开救援地锚／抓持头。
4. `UNAPPROVED_GLYPH`：中央馆门出现了模型自动生成的装饰符号；它不是已批准馆徽，不得直接进入后续资产。
5. `INDEX_RING_READ`：偏心检索环已摆脱通用杂兵头，但仍需用户判断其是否真正帅、是否过于像光环／问号式附件。

## 6. 停止边界

本稿只到用户视觉确认：

- 不接 Godot；
- 不写 Runtime；
- 不迁移 Canon；
- 不把本回执的 `PASS_FOR_USER_VISUAL_REVIEW` 当作用户批准；
- 用户若接受母方向，下一步应先做可确定的正侧背／内部映射结构定稿，再派生游戏资产；不得立刻用本张概念图切 Sprite。
