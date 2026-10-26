# 万机馆巡展舰 → 未来人形巨机关系候选板回执

- 制作方：Art Asset Section 2
- 日期：2026-08-23
- 状态：`candidate / user=false / runtime=false / canon_not_migrated / godot_not_bound`
- 停止点：`PASS_FOR_USER_SILHOUETTE_AND_RELATION_DECISION`；不是变形工程定型、Current Art 或 Runtime Art。

## 这次纠正的命题

用户已明确：万机馆的未来第二形态应可变形为人形巨型机。

本轮因此不再把“侧舱张开”或“展馆挂在竖向圆筒上”当作可变设计，而是要同时设计：

1. 具有明确舰首、航向、舰尾和低矮横向体态的巡展舰/移动堡垒。
2. 舰态中已经存在的左右主承力体、中央龙骨、肩/髋大轴环、头部密封舱和舰尾推进块。
3. 具有完整头、颈、胸、肩臂、手、骨盆、双腿、膝与脚的人形巨机第二形态。
4. 每一个舰态大块在人形中都有去向，不消失、不复制、不漂浮脱离。

## Canon / Reader 边界

### 当前必须保留

- `MECHA_WANJI_MOBILE_CHASSIS` 在 C01E04 只是 `130–160m` 级低矮巡展舰/移动基地。
- C01 的生产态只有固定展馆、离地转换和巡展舰三态；本章不显示人形。
- 舰首前甲板是 18m 馆守Z的出击与守备位；自动航行负责推力、转向与配平。
- 万机馆是公共博物馆与生活共同体；不是完整战列舰火力、无限格纳库或馆藏拼装变形。

### 本板新增的只是 Candidate

- “后续某章解锁人形巨机”是用户刚确认的方向，但解锁章节、尺度、能力、武装、变形代价和剧情因果均没有迁移到 Current Canon。
- 本轮不修改 `authority_manifest.tsv`、`entities.tsv`、Reader、Godot 或 Runtime。

## ImageGen 回执

- 模式：内置 ImageGen，`stylized-concept`
- 调用：`1`
- reroll：`0`
- 图像输入：`none`
- A13 RETURN 稿：未上传、未作为正向像素参考、未编辑。
- 最终提示词：[`IMAGEGEN_FINAL_PROMPT.md`](../IMAGEGEN_FINAL_PROMPT.md)

## 50% 首读

### 已成立

- `PASS`：舰态是低矮横向整体，楔形舰首朝右，舰尾推进块在左，航向首读明确。
- `PASS`：馆守Z尺度小人站在舰首前甲板，可以直接判断巨型下层主体与 18m 机体的比例。
- `PASS`：公共展窗、层叠屋盖与舰首前甲板已整合进舰壳，不是展馆粘在薄底盘上。
- `PASS`：第二形态为完整人形，具备头、胸、肩臂、手、骨盆、腿、膝和脚，不是展馆挂竖筒或侧舱张开。
- `PASS`：舰首/前甲板到胸甲、展窗到胸肩结构、锈色大轴环到肩髋关节的造型连续性清楚。

### 仍开放

- `OPEN`：人形头部和胸甲已经完整，但它们是否足够“万机馆独有”，还是只读成一台完整的通用工业机器人，必须由用户决定。
- `OPEN`：中间帧能读出肩臂展开、龙骨立起和人形骨架锁定，但“后部左右舰体如何前后分段收成大腿/小腿/脚”只到概念级，未达工程正投影证据。

因此本板可进入用户的轮廓/关系裁决，但不得直接制作变形动画、Atlas 或人形 Runtime。

## 用户精确裁决问题

1. **舰态轮廓：** 舰首/航向、低矮移动堡垒、巨大下层主体是否成立？回复 `通过 / 退回`。
2. **人形身份：** 头胸与全身比例是否足够像万机馆独有的未来第二形态？回复 `通过 / 退回`。
3. **同体映射：** 舰首→胸、前舰体→臂、后舰体→腿、龙骨→躯干是否可信？回复 `通过 / 需补拆分`。

## 交付

| 文件 | SHA-256 |
| --- | --- |
| `generation-raw/WANJI_CARRIER_TO_HUMANOID_IMAGEGEN_CALL01_RAW.png` | `4f82a2b96db35b6e8c8f2984a8584729fdf8ead6406b1e298acab2f379cfc93f` |
| `qa/WANJI_CARRIER_TO_HUMANOID_IMAGEGEN_CALL01_RAW_50PCT.png` | `cfb423112e078b63c20dad163278859d8a0fc9eb035284e82d47131d1093a5a4` |
| `delivery/WANJI_CARRIER_TO_HUMANOID_USER_CONFIRMATION_BOARD_2400x1800.png` | `6f3660e4216586ecedc0d6b43277f2a4b25aa3881c3282cf3f50904fd649f52d` |
| `delivery/WANJI_CARRIER_TO_HUMANOID_USER_CONFIRMATION_BOARD_1200x900.png` | `3470c8823d74838e70e94cc01e2b23735fc334ee9005b796afac16034ad5c764` |
