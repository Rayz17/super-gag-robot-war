# A23 Call03｜Section 2 单次生成硬门失败回执

> Status: `SECTION2_FAIL / USER_VISUAL_GATE_NOT_OPENED / MODERNITY_RECOVERED / PHYSICAL_HEAD_PRESENT / ARMOR_SHUTTER_HARD_GATE_FAILED / TOURING_MUSEUM_ENTRANCE_WEAK / SEALED / CANDIDATE_ONLY`
>
> Date: `2026-08-24`
>
> Runtime: `false`
>
> Godot binding: `false`
>
> Canon promotion: `false`
>
> User approval: `not_requested_due_to_internal_hard_gate_failure`

## 1. 调用事实

- Call03 Built-in ImageGen generate 实际调用：`1`
- Call03 reroll：`0`
- A23 全节点累计正式 ImageGen 调用：`3`（Call01 generate 1 + Call02 edit 1 + Call03 generate 1）
- CLI／API／其他生成 fallback：`0`
- 精确 Prompt：`../../rework02/prompts/CALL03-SINGLE-BUILTIN-IMAGEGEN-GENERATE-PROMPT.md`
- 生成原图：`/Users/rayz/.codex/generated_images/01a0316e-9e95-72b3-932a-ed25cb945e9c/exec-46eb8b95-29f7-42fe-8d1b-38fe9171f670.png`

## 2. 正向输入与负例边界

- A15：只取可进入的机器人博物馆母体、公共尺度和巨大 B1/B2。
- A16：只取低矮三级馆冠、连续收尖构面和现代优雅巡展舰语言。
- A23-R1：只取地上馆冠／地下 B1/B2 的同一部件映射。
- Call02 与用户附图：只作失败诊断，未作为正向像素输入。
- 外部机甲／要塞参考：只取独立头部单元、舰体模块重排、基地可进入和人物尺度原则；没有输入或复制外部 IP 像素。

## 3. 封存图

- Section 2 失败诊断图：`../delivery/WANJI_A23_CALL03_MODERN_MUSEUM_CARRIER_REWORK_SECTION2_FAIL.png`
- 尺寸：`1536 × 1024`
- 色彩：`RGB`
- SHA-256：`2db671243b9dae2e6a32254a663d4e25b0e56e586487b1ac93b29429132b1598`

## 4. 四项硬门目视结论

| 硬门 | 结论 | 目视证据 |
| --- | --- | --- |
| 明确实体头、无写实五官 | `PASS_WITH_IDENTITY_RISK` | 主人形肩间存在独立实体头，近景也有额冠—面罩—下部块层级，无眼鼻嘴；但额冠下方仍出现一条发光玻璃／控制桥式横带，万机馆专属识别尚未经过用户判断 |
| 公共机器人博物馆首读 | `PARTIAL / TOURING_STATE_WEAK` | 固定馆切面清楚呈现公众入口、人物、机器人展厅与巨大地下母体；巡展舰虽保留三级馆冠，却更先读成高级飞船／大型游艇，公众入口与展廊入口不够明确 |
| 战斗／升空态装甲闭窗 | `FAIL — HARD STOP` | 巡展舰馆冠仍有连续透亮展窗，人形头部和胸肩保留多条发光玻璃／室内带；没有可追认的闭合装甲闸门或百叶，不能证明战斗防护 |
| 地上／地下同源映射 | `PASS_AT_MAJOR_MASS_LEVEL` | 固定馆的三级馆冠、深 B1/B2 与巡展舰上层／深舰腹、人形胸肩／骨盆腿足保持一致的白色馆体与深色承力体分工 |

## 5. 其他边界

- 现代感与连续流线相比 Call02 明显恢复；巡展舰有明确舰首、航向和深舰腹，没有退回方盒工业堡垒。
- 未画主炮、导弹墙或手持重武器；底部细节只出现机体出击／装备舱、抓持头与推进／状态结构，仍在 Current 能力边界内。
- 以上优点不能覆盖装甲闭窗硬门；机器生成完成不等于制作人视觉通过。

## 6. 停机边界

- Call03 不开放用户“通过／不通过”确认门，只可作为失败诊断历史图。
- 不 reroll，不做确定性修图，不借主会话或其他生成途径补图。
- 不接 Godot，不写 Runtime，不迁移 Canon，不从本图直接切 Sprite。
- 若之后由制作人开启新的视觉调用，应继承文字结构结论，但不得把 Call03 当已批准正向像素母版。
