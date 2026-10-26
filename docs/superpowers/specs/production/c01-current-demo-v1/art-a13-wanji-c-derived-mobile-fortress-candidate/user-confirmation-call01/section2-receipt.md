# 万机馆 C 路线深化：移动堡垒 / 可变结构候选板回执

- 制作方：Art Asset Section 2
- 日期：2026-08-23
- 状态：`candidate / user=false / runtime=false / canon_not_promoted / godot_not_bound`
- 目标：只提交一套 C-derived 新主体的用户确认板；不提交最终侧视比例、透明单体、Atlas、Godot 绑定或 Canon 迁移。

## 本轮用户裁决的直接修正

1. 不再把万机馆画成“展馆从地下拔出，底下只藏一块薄底盘”。
2. 地表公共馆体只占总垂直体积约 `1/3`；地下以中央深龙骨、左右巨型机库/收藏承力舱、航行炉和旧推进环构成约 `2/3+` 的真正巡展身体。
3. 巡展舰态不是展馆粘飞行板；展馆成为有人生活和观众尺度的上层城市/展馆冠部，全部隐藏舰腹展开后形成完整移动堡垒。
4. 可变潜力只由大分缝、侧舱转轴、中央脊和锁止环提示；本轮不画人形、不命名终局形态、不把未定变形升为 Canon。

## 权威输入

- Current Reader：`C01E04-博物馆追上天空-v1.md`；公共前厅恢复航行台，主展厅、穹顶、两侧展廊与下方承力舰体一起离地，玻璃门厅、市政管网与后加支撑留地。
- Working Canon：万机馆是从固定展馆恢复的百米级低空巡展舰体；不是临时新长底盘、军用战列舰或人形机器人。
- Hard 空间边界：L1 是展陈心脏；B1 是中型泊位与单机重修的机库脊柱；15–30m 大型机以有限外部锁泊为主；战舰级单位不入馆。
- 现行尺度：长 `130–160m`、高 `35–45m`；用户已明确指出这一上限可能压缩了移动堡垒所需的隐藏体积。

## 单次 ImageGen 回执

- 模式：内置 ImageGen，`stylized-concept`
- 调用：`1`
- reroll：`0`
- 图像输入：无；不是修改 History 旧舰图。
- 最终提示词：[`IMAGEGEN_FINAL_PROMPT.md`](../IMAGEGEN_FINAL_PROMPT.md)

## 50% 首读结论

### 成立的部分

- `PASS`：固定馆剖面能直接读出地表展馆与巨大地下旧身体，隐藏体积明显大于地表馆体。
- `PASS`：巡展态上层仍有公共入口、层叠屋盖和暖色展窗，下层由中央龙骨、左右舱体与推进环构成完整移动堡垒，不再是薄底盘。
- `PASS`：未来可变只有结构语法，没有越界画成人形或声称某种最终形态。

### 必须由用户裁决的缺口

- `OPEN`：生成的 3/4 透视为了强调地下体积，把中央龙骨和侧舱表现得偏深、偏竖。它不能同时冒充现行 `35–45m` 高的低矮侧视比例。
- 因此确认板将同一构型分成两个尺度门：
  - `S`：保留现行约 `160m` 上限，后续必须收敛舰腹和容量。
  - `L`：约 `230m` 移动堡垒，只是 `non-Canon scale-migration candidate`，需用户先选中才能开始受影响的高度、泊位、地图和 Canon 迁移。

本轮停止结论为 `PASS_FOR_USER_STRUCTURE_AND_SCALE_DECISION`，不是最终外形 PASS。

## 交付

| 文件 | SHA-256 |
| --- | --- |
| `generation-raw/WANJI_C_DERIVED_MOBILE_FORTRESS_IMAGEGEN_CALL01_RAW.png` | `97e73bea46369518af841a10181fac18eac318aff90683c04063a423340dd518` |
| `qa/WANJI_C_DERIVED_MOBILE_FORTRESS_IMAGEGEN_CALL01_RAW_50PCT.png` | `ecea3df660ecafedd093efd592ab43bd84db4e1876bf0515bd0103330714c8e6` |
| `delivery/WANJI_C_DERIVED_MOBILE_FORTRESS_USER_CONFIRMATION_BOARD_2400x1800.png` | `938a31e6ba7610bd4f79b80c2df34d9e3f2ae4203293d24edf8de5963688f08f` |
| `delivery/WANJI_C_DERIVED_MOBILE_FORTRESS_USER_CONFIRMATION_BOARD_1200x900.png` | `4202a0f2c4ea3e105581916f29831e829a379615b103193254907471296f61fa` |

## 用户回复门

请只裁决三项：

1. `构型成立 / 退回`：层叠公共馆 + 中央深龙骨 + 左右巨型舱体的主体关系是否成立。
2. `S / L`：保留约 160m 并收敛舰腹，还是将约 230m 作为尺度迁移候选。
3. `保留可变语法 / 退回`：是否保留侧舱转轴、中央脊与锁止环的未来可变提示。

用户选择前，不继续材质、色彩定稿、正投影定型、透明单体或 Godot 接入。
