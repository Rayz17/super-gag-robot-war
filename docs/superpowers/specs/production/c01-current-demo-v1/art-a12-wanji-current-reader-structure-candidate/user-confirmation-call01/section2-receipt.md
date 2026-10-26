# 万机馆 Current Reader 结构轮廓候选板回执

- 制作方：Art Asset Section 2
- 日期：2026-08-23
- 状态：`candidate / user=false / runtime=false / canon_not_promoted / godot_not_bound`
- 任务书：`../../129-c01e04-wanji-history-art-unbind-and-current-concept-brief.md`
- ImageGen：内置工具，单次调用；无 reroll；无图像输入
- History 边界：未引用、未读取、未上传、未裁切 `spr_wanji_mobile_chassis_v01.png`
- 交付边界：只交 A/B/C 结构轮廓用户确认板；不做最终材质、透明单体、Atlas、多状态动画或 Godot 绑定

## 权威输入收敛

- C01E04 Current Reader：主展厅、穹顶/大跨度屋盖、两侧展廊与下方承力舰体一起离地；外围玻璃门厅、市政管线和后加固定件留地。
- C01 预生产模型：长 `130–160m`、高 `35–45m`；南侧外部泊位在离地后成为舰首前甲板；18m 馆守Z作为舰首尺度锚。
- 万机馆空间/泊位 Canon：L1 是展陈与情感心脏，B1 是 2–12m 中型泊位与单机重型维修的机库脊柱，B2 是残响/黑匣层；15–30m 大型机以有限外部锁泊为主，战舰级单位不进馆。
- C02 预生产模型：舰体坐在连续重载托架/船台上，由地面车队沿承重作业道低速牵引；舰侧宽面是一次大型支承面。
- 用户当前裁决：旧舰体未确认且不符合现 Reader/设定；本门从 Current 重建，不修旧图。

## 本次轮廓家族

| 方案 | 主轮廓语言 | 固定馆 → 巡展舰连续性 |
| --- | --- | --- |
| A | 连续大跨拱壳 + 低矮带状展廊 | 拱壳主展厅、两侧展廊与下方承力弧线保持一体 |
| B | 双平行展廊 + 低中庭/中部连桥 | 两条公共展廊与 B1 直向脊柱共同离地 |
| C | 三段错落层叠屋面 + 扇形公共前场 | 层叠展陈平台与宽浅舰腹保持同一非对称旧修补轮廓 |

## 50% 目视停止门

- `PASS_FOR_USER_SELECTION`：A/B/C 在主屋盖、展廊排布、舰首形状与腹部承力几何上均有大轮廓区别，不是同一个壳体换细节。
- 每案的固定馆/巡展舰在同视角、同比例下可一一追踪。
- 公共入口、大跨展馆屋盖、观众窗带的首读强于推进和有限防卫结构。
- 不存在履带、轮式主移动、巨炮、人形四肢、小宫殿粘底盘或无限机库门首读。
- 轮廓层已能交给用户选择；未使用第二次 ImageGen 调用。

## 交付

- 生成 raw：`generation-raw/WANJI_CURRENT_READER_STRUCTURE_IMAGEGEN_CALL01_RAW.png`
  - SHA-256: `4f6537d8aa3009cb783107f2895a2dfeda1d150c8251b755fb9634774966209b`
- raw 50% QA：`qa/WANJI_CURRENT_READER_STRUCTURE_IMAGEGEN_CALL01_RAW_50PCT.png`
- 2400 用户确认板：`delivery/WANJI_CURRENT_READER_STRUCTURE_USER_CONFIRMATION_BOARD_2400x1800.png`
  - SHA-256: `e6607f50416bbdd2f1f2ab41ff017ce85c3d6087dba97129250b278a4936b0de`
- 50% 用户确认板：`delivery/WANJI_CURRENT_READER_STRUCTURE_USER_CONFIRMATION_BOARD_1200x900.png`
  - SHA-256: `9d0c148a65cf496a7f31ed11d8ea5991503c6ae24c3ae50843639f54f39bdf36`

## 用户唯一选择问题

> A / B / C 中哪一个最像“会移动的机器人文化馆”，或三案全部退回？

选定轮廓家族前，不继续材质、色彩、损伤、透明空中单体图或 Godot 实机。

## 最终提示词

`stylized-concept` 游戏车体/建筑结构概念表。单张横向三列，每列用同一个抬高的前右三分之四视角、同一比例配对显示固定机器人文化馆和恢复后的低空巡展母舰；三案分别为连续拱壳、双廊中庭、层叠平台，在外轮廓、屋盖量体、展廊组织、舰首与腹部承力几何上真正不同。共同锁定 130–160m 长、35–45m 高，主展厅、两侧展廊、公共入口、南侧泊位/舰首与 B1 承力脊柱在固定馆/巡展舰间一一对应；公共博物馆首读，旧巡展机械次读。仅少量外泊和小口径近防，禁止履带堡垒、军事战列舰、小宫殿粘通用底盘、人形变形、巨炮、无限机库门和任何文字/标志/水印。
