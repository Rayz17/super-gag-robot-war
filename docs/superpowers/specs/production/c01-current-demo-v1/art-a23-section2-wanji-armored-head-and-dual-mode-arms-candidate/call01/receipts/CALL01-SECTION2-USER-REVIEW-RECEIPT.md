# A23 Call01｜Section 2 用户目视候选回执

> Status: `USER_REVIEWED / TRANSFORMATION_FORM_DIRECTION_ACCEPTED / OVERALL_NOT_ACCEPTED / MILITARY_OVERREAD / HEAD_GENERIC / ABOVE_GROUND_MUSEUM_IDENTITY_MISSING / GROUND_UNDERGROUND_MAPPING_UNPROVEN / REWORK_REQUIRED`
>
> Date: `2026-08-24`
>
> Runtime: `false`
>
> Godot binding: `false`
>
> Canon promotion: `false`
>
> User approval: `partial_direction_only / overall_not_accepted`

## 0. 用户裁决（覆盖 Section 2 内部首读）

- 接受项：低矮巡展体变为巨型人形的**形态方向**。
- 不接受项：A23 Call01 **整稿不接受**，不能作为后续正向视觉定稿或 Runtime 资产。
- 根因 1 `MILITARY_OVERREAD`：巡展态先读成重装甲军事载具，炮塔／武器感压过公共机器人博物馆。
- 根因 2 `HEAD_GENERIC`：虽有头且没有具体五官，但仍是通用无脸机甲头，缺少万机馆自己的文化与档案识别。
- 根因 3 `ABOVE_GROUND_MUSEUM_IDENTITY_MISSING`：地上公共展馆的入口、门厅、展厅屋面与展陈空间没有形成可追认的主体。
- 根因 4 `GROUND_UNDERGROUND_MAPPING_UNPROVEN`：没有证明较小的地上馆体与更大的 B1/B2 地下母体怎样分别进入巡展舰和人形的胸肩背、舰腹、骨盆、腿足与承力骨架。
- 后续边界：只做定点结构返修；保留低矮巡展体→巨型人形拓扑、装甲闭窗与双形态同源部件，不以换皮、加细节或加炮掩盖映射缺口。

## 1. 唯一调用事实

- Built-in ImageGen 实际调用：`1`
- Reroll：`0`
- CLI／API fallback：`0`
- 正式出图前两次 Section 2 的 Codex `403`：均发生在 ImageGen 前，不计调用
- 像素输入：只有 A23 无身份几何／拓扑 Guide
- A21 用户退回整稿：`0` 像素输入
- 现有 IP 参考图：`0` 像素输入

## 2. 交付物

- 用户目视候选：`../delivery/WANJI_A23_CALL01_DUAL_MODE_USER_REVIEW_CANDIDATE.png`
- 尺寸：`1586 × 992`
- 色彩：`RGB`
- SHA-256：`153ac2993639e00ffc047ff4a98ca5210d52f64afb74a6423798248d006d6e77`
- 精确 Prompt：`../prompts/CALL01-BUILTIN-IMAGEGEN-PROMPT.md`

## 3. Section 2 交用户前的内部首读（History，已被用户裁决覆盖）

下表只记录为什么该稿当时被送审，不再代表当前判断。凡与第 0 节用户裁决冲突者，一律以用户裁决为准。

| 硬门 | 结论 | 图上证据 |
| --- | --- | --- |
| 有明确头部、绝无人脸五官 | `PASS_FOR_USER_REVIEW` | 头部与短颈、肩胸分层清楚；前面只有深嵌黑色传感带与偏置琥珀孔，没有双眼、鼻、嘴或人脸 |
| 战斗／巡展警戒态不裸露大玻璃 | `PASS_FOR_USER_REVIEW` | 舰体主展窗节奏和人形胸口均转为暗红装甲百叶；头、胸、腿正面没有游客或透明舱 |
| 两形态能追认同源防护、近防、服务梁与推进 | `PASS_FOR_USER_REVIEW` | 舰首厚甲进入双前臂盾；两侧重型服务梁进入肩背；舰腹青色推进进入足底；近防口在两态延续 |
| 救援锚／绞盘与作业手不被普通枪炮吞掉 | `PASS_WITH_VISIBLE_FOLLOWUP_RISK` | 巡展态左侧可见下探作业／锚具，顶端 inset 证明盾甲后方作业臂与五指手展开；但绞盘鼓、缆线出口在人形远景仍不够显眼，后续定稿必须结构化补清，不能靠文字解释 |
| 机器人博物馆母体而非游艇／方盒 | `INTERNAL_MISREAD / USER_OVERRULED` | 内部把百叶节奏和人车尺度误判成足够的馆体身份；用户已明确指出它首先读成军事载具，且地上展馆主体缺失 |
| 可战斗但不冒充 C01 重战舰 Canon | `PASS_WITH_BOUNDARY_NOTE` | 输出主要使用盾甲、作业手、支援梁、近防与推进，没有主炮、胸炮、剑或导弹墙；梁端炮口必须继续解释为有限近防／未来 Candidate 挂点，不能倒写成 C01 已有重炮 |
| 不复制现有 IP | `PASS_FOR_USER_REVIEW` | 未使用 IP 像素输入；轮廓、头部、色分、武装与变形部件均按 A23 原创约束生成 |

## 4. 用户已证实的问题

1. 头部不是“是否足够无脸”的小风险，而是已经被用户判定为缺乏万机馆独有识别的通用无脸机甲头。
2. 服务梁和炮口不是轻微抢眼，而是已经形成 `MILITARY_OVERREAD`，掩盖救援、展陈与作业职责。
3. 和平展馆态未显示不只是少一张 inset；地上公共馆体与更大地下母体的部件身份、相对尺寸和去向本身没有被证明。

## 5. 停止边界

该图已完成用户视觉裁决并被整体退回。返修稿再次获得用户明确批准前：

- 不接 Godot；
- 不写 Runtime；
- 不迁移 Canon；
- 不派生精灵图或模型；
- 不把内部 `PASS_FOR_USER_VISUAL_REVIEW` 写成用户认可。
