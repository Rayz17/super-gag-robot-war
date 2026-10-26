# 139 · 公式台轨 A 交接（给后续模型继续做）

> Status: `candidate_lab_handoff / 2026-09-05 / not_canon`
>
> 给下一位模型（含 GPT-6）接着做。**权威是现网磁盘**，不是本篇的记忆。开工前先对照本篇「现网事实」用 grep/读文件核对；对不上就以磁盘为准。
>
> 对照：[137](137-formula-production-harness.md) · [138](138-formula-lab-case-survey.md) · [fusion TSV](formula-lab-fusion.tsv)

**禁止把本刀或任何一档 dest 收完标成总目标完成。** 总目标是七公式对标 138 §2.3 金标成片水准，现网未齐。

---

## 0. 一句话

把公式台**轨 A 实验室**升到可对标 138 调研参考案例的交付水准：七公式禁止再用夹具色块/夹具剧情当产品；改为**可换档临时美术**；互动与绘制必须**严格高于裂湾底盘**（裂湾只当工程下限，不当设计金标）；**形态也要像金标视觉交互语言**，不能只字段/逻辑/操作流像。空间物理按配置演算「哪里需要什么样的图」；sprite 认真生成范例并形成公式；公式台支持运算/放置/编辑（也是轨 B 系统化需求）。

---

## 1. 总目标（不要缩小）

用户原目标，不可改写成「这一刀做完就算 138 齐」：

1. **七公式**仍是 JSON preset 换档、真实按键可玩完、有抽帧验收。
2. **禁项仍守融合表**（138 §2.3「合不进去必须丢掉」）。
3. **不进 CML130/131、不绑成片 Reader、不升 Canon、`user_visual_acceptance` 仍为 false。**
4. 临时美术也必须解决**空间物理关系**：不能随便找张图放到底上；游戏视角、背景、物件脚落地面线、与绘景同一套透视语言。需要**按配置演算**哪里需要什么样的图。
5. 不能只在字段级或逻辑上像金标；**形态**（视觉交互语言）也要复刻。
6. sprite 认真生成范例、形成公式；素材提供维护功能；公式台支持运算、放置、编辑。

### 1.1 138 §2.3 融合壳（金标借哪一层）

| 公式 | 融合成哪一套 |
| --- | --- |
| 叙事 | Y 分层铬 + Dialogue Manager 剧本 |
| 战术 | Y 铬 + ITB 意图 overlay + **00c 全队一次提交**（不跟 ITB 单机结束回合） |
| 调查 | 金偶像两态板 + Obra 确认门 + 请求开始试验 |
| 探索 | Popochiu 房间热点 + Outer Wilds 知识卡 |
| 结算 | 编队卡伤损（XCOM 结构）+ Banner 两行后果 |
| 世界图 | SRW30 三入口 + ITB 并排卡 |
| Hub | 返馆见人 + 3 槽工作卡 |

裂湾机兵 = 工程下限，**不当设计金标、不进备选**。

### 1.2 硬约束（违反即偏航）

- 对用户一律中文。
- 公式台是 **Candidate 实验室**。Canon 入口：`chao-gag-canon`。当前活动章仍是 **C04**。本任务**不改 Canon / 已验收 Reader**。
- 改完可跑 `python3 scripts/report_v35_layered_pipeline.py --check`（最近一次：`V35 layered pipeline dashboard is current`）。
- **T5–T11 不为每档另做小游戏。** 护线/承力/合体记 `capability_gap`。
- 屏上无「夹具」「临时美术」字样。
- 绘景砖走 `resolve_texture`，**不 iso 打孔**。
- `Art.draw_unit_sprite` / 调查 doll 回退仍定义，**不要复活**。
- 官方帧（`artifacts/formulas/*/frames/`）这些 dest 刀**不要重抽**；新抽写到 `tests/tier-*`。
- 省略 `plate=` 必须仍走旧几何体积（可换档门）。
- **tex 单独不是门。** `plate=` 才开绘景 dest。

---

## 2. 现网事实（2026-09-05 磁盘）

核对命令（必须先跑）：

```bash
python3 - << 'PY'
from pathlib import Path
p = Path("game-godot/scripts/formula_lab/formula_lab_space_plate.gd").read_text()
for k in ["TILE_ORDER", "DEST_ORDER"]:
    i = p.find(k)
    print(p[i:i+220].replace("\n"," "))
PY
```

**当时读到的值：**

```
TILE_ORDER := house, grass, road, ruin, forest, dock, water, sky, horizon, vista,
              interior, workshop, chart, leftover, hall, yard, quay, patrol
DEST_ORDER := cabinet, gate, opening, leftover_pad, leftover_dock, board_pad
SPACE_ORDER := wall_face, floor_plane, prop_body, sky_loft, cabinet, gate, opening,
               leftover_pad, leftover_dock, board_pad
```

- **没有** `tile-chrome.png`，**没有** `execute_pad` dest API。
- 演出层 `execute_pad` **仍是几何锈铁脚台**（`_draw_execute_pad_volume` / `_draw_execute_pad_foot`）。
- 地图层 `board_pad` 已收：`plate=road` → dest contain-sit `tile-road` 湿沥青菱。
- 结算 `leftover_pad` / `leftover_dock` 已收：`plate=leftover` → dest contain-sit `tile-leftover`（`draw_horizon_strip`，低机位，不是 iso 菱）。
- stamp 最近一次记录：`SPACE_STAMP_OK written=45`。

### 2.1 坐井台 F 循环（新 dest **只能往后追加**）

`sit_desk_space_shot` 是 **F×13 → `wall_face`**。**不要把 dest 井插到 loft 之前**，否则打坏 `cabinet` 的 F×4。

| dest 井 | 从 wall_face 再按 F | 抽帧脚本里的循环 |
| --- | --- | --- |
| leftover_pad | F×7 | leftover dest 脚本：F×13 + F×7。**不要改这个循环。** |
| leftover_dock | F×8 | leftover dest `02` |
| board_pad | F×9 | `sit_desk_board_dest_shot.gd`：F×13 + F×9 |
| **下一 dest（execute_pad）** | **F×10** | 只能追加在 `board_pad` 之后 |

坐井台 F 循环会刷 `mecha-wreck.png` 缺 ctex，是既有噪音，**不挡 dest 测**。

---

## 3. 已收（近期 dest / 绘景刀，供对照，勿重做）

细节与 RGB 数以 137 §14、138 §12 为准。下面只记「做了什么、别碰什么」。

| 刀 | 金标形态 | 现网做法 | 勿改 |
| --- | --- | --- | --- |
| 叙事巡查柜/闸/坞口 | Y 等距绘景物件 | cabinet contain-sit `shed_far`；闸警戒带；坞口绘景拥有坞喉 | `origin_uv` / `map_sit` / 立绘 vista |
| 结算 leftover 垫/坞 | XCOM AAR 卡坐在清图战场上 | leftover dest 外扩岛 + `draw_horizon_strip` | `card_sit_uv` / `banner_uv` / `origin_uv` |
| 战术地图层 `board_pad` | Y/ITB 机体站在等距沥青上 | `board_pad_along_dest` + `draw_space_polygon(..., "prop_body")` iso 菱 | `origin_uv` / 格子 / `stand_uv` / ITB / Y 铬 |

抽帧路径（已有，可当对照，**不要当「只改一物」的全屏基线**除非同日同脚本）：

- `artifacts/formulas/FML_TACTICAL/tests/tier-board-prop/`
- `artifacts/formulas/lab-desk/tests/tier-sit-board-dest/`
- `artifacts/formulas/FML_SETTLEMENT/tests/tier-leftover-prop/`
- `artifacts/formulas/lab-desk/tests/tier-sit-leftover-dest/`
- 演出层旧对照：`FML_TACTICAL/tests/tier-execute-plate/`（T0/T1）、`tier-execute/`、官方 `frames/13_COMMITTED_AND_EXECUTING` / `14_EXECUTION_SEGMENT`

范例已盖：`leftover__leftover_pad.png`、`leftover__leftover_dock.png`、`road__board_pad.png`（在 `game-godot/assets/formula_lab/temp/plates/examples/`）。

---

## 4. 当前正要开的下一刀（未实现）

**只打演出层 `execute_pad`。** 不要并进 `execute_rope` / `execute_berm` / `board_rope`。

### 4.1 差口

金标（机战 Y 演出层）：机体站在**近景湿铬沥青**上，不是左右两块锈铁岛。

现网：`_draw_execute_pad_volume`（`formula_lab_placeholder_art.gd` ~6867）在宽 footprint 且非 `stance=single` 时画 sit 洗 + 地填 + 中心 streak + grit + **左右两块构造脚台**；`stance=single` 或窄盒只画一块脚台。脚台是几何 deck/lip/streak/chrome/螺栓。

| 档 | 演出层 surface | 现状 |
| --- | --- | --- |
| TAC_T0 | `ring_pad` `finish=execute_pad` `volume=execute_pad` | 铁暖双脚 |
| TAC_T1 | `pad_west` / `pad_east` `stance=single` | 冷荧光单脚 |
| TAC_T3 | `ring_pad` 省略 palette | 锈铁双脚 `(35,41,56)/(40,42,54)`；中心 streak `(640,520)=(20,30,51)` |
| TAC_T2 | **没有** execute_pad | 不要硬加 |

`execute_ground` 已是几何湿铬（远/中/近/过道反光/透视缝），注释写明**不整块 blit `tile-road`**（`(20,29,51)` 是禁色）。**本刀不要改 `execute_ground`。**

### 4.2 砖：禁止复用地图层 iso `tile-road`

这是用户点名的空间物理错误：「不能随便找张图放到底上」。

| 层 | 相机 | 已收砖 | 绘制原语 |
| --- | --- | --- | --- |
| 地图层 `board_pad` | 等距俯视 | `tile-road` 湿沥青**菱** | `draw_space_polygon(..., "prop_body")` |
| 结算 leftover | 清图低机位暮空 | `tile-leftover` 砖尘褐 | `draw_horizon_strip` |
| 演出层 `execute_pad` | **近景 / 四分之三侧视**、combat_haze **钢青湿铬** | **尚无**。需要**另一套近景湿铬砖** | 应对齐 leftover：低机位 `draw_horizon_strip`，**不要** iso `prop_body` |

**禁止：**

- 把 `plate=road` 抄进演出层。
- 把 `tile-road` iso 菱 contain-sit 到近景脚台上。
- 用 leftover 暮空褐当 combat 钢青。
- 把 `plate=chrome` 抄进气氛 / berm / `execute_ground` / 地图层。

**应对齐：**

1. 认真生成一枚近景湿铬板（建议 `tile-chrome.png` + catalog 分带 `execute_pad`），透视必须是**地面向远堤退行的低机位沥青**，不是等距菱，不是庭院照整张垫底。
2. `SpacePlate`：`execute_pad_owns_prop` / `execute_pad_along_source_uv` / `execute_pad_along_dest`（pair=整环 footprint 或左右脚 dest；`stance=single` 紧凑单脚）。dest 是已收脚点岛，**不改 `stand_uv`**。
3. 坐井台 `DEST_ORDER` / `SPACE_ORDER` **追加在 `board_pad` 之后**：`execute_pad`。
4. `plate=chrome`（或选定名）**只点** execute 的 `ring_pad` / `pad_west` / `pad_east`。
5. 省略 plate 仍走旧锈铁体积。
6. 金标形态倾向：**共享湿铬战场**（整环 dest contain-sit），而不是两块锈铁岛 1:1 换成两块贴纸。T1 `stance=single` 保持紧凑单脚 dest。

### 4.3 验收（本刀）

抽帧目录建议：`artifacts/formulas/FML_TACTICAL/tests/tier-execute-pad/` + `lab-desk/tests/tier-sit-execute-dest/`。

对照：`tier-execute-plate/` + 官方 13/14。T0 可 J 提交进 execute；T1/T3 要走摘要/长按通道（抄 `tactical_execute_plate_shot.gd` / `tactical_board_pad_shot.gd`）。

必须证明：

- Y 铬 / 底栏胸像 / 机体井 / `stand_uv` **未动**。
- 旧脚台色 `(35,41,56)` / `(36,52,68)` / `(60,42,36)` **应降**（exact 计数跌）。
- 旧 `tile-road` dither `(20,29,51)` **不要复活**。
- 地图层赭环 **不要回潮**（board_pad 已收不要打坏）。
- 屏上无「夹具」「临时美术」。

### 4.4 本刀收完后要改的文档

137 §14 新条目；138 §2.3 战术演出层那一行 + §12；fusion TSV；asset-specs TSV；七份 `lab.json` 的 `next_agent_notes`。`user_visual_acceptance` 仍为 false。

---

## 5. 复制哪套公式（dest 刀标准工序）

对照最近收成的 `board_pad` / `leftover_*`，**不要发明第三套闸门。**

1. `SpacePlate`：`surface_uses_*_plate`（**只有 `plate=` / `join=`，tex 不是门**）→ `*_owns_prop` → `*_along_source_uv`（catalog bands）→ `*_along_dest`（`leftover_contact_quad` 顶点序：远左、远右、近右、近左；外扩偏移锁已收 sit）。
2. `Art`：`_draw_*_plate`：有 plate 则阴影 + 按相机选 `draw_horizon_strip` **或** `draw_space_polygon`；失败则旧体积。体积入口开头 `if _draw_*_plate(...): return`。
3. preset surfaces **只点该 volume** 的 `tex` + `plate` + `source_uv` + 白 modulate。
4. catalog `bands.<kind>`、`wells.json` 井尺寸、`space_needs.json` sit/uv/examples 对。
5. `TILE_ORDER` 若新砖必须登记。`DEST_ORDER` / `SPACE_ORDER` **只追加，不插入**。
6. 坐井台 dest_template：相机语言必须对（board_pad = iso 菱；leftover/execute = 低宽地面岛）。
7. 抽帧：`scripts/godot-run.sh --script res://tests/formula_lab/<shot>.gd -- <绝对 out_dir>`  
   **不要** `--path game-godot`（相对路径会写到 `game-godot/artifacts/`）。
8. RGB：`/tmp/chao-gag-rgb-venv/bin/python3` + Pillow。对照旧色 exact 计数跌 + 金标铬/底栏未动。
9. stamp：`scripts/godot-run.sh --script res://tests/formula_lab/space_plate_stamp.gd`

关键文件：

| 角色 | 路径 |
| --- | --- |
| dest / catalog / 绘制原语 | `game-godot/scripts/formula_lab/formula_lab_space_plate.gd` |
| 体积绘制 | `game-godot/scripts/formula_lab/formula_lab_placeholder_art.gd` |
| 坐井台 | `game-godot/scripts/formula_lab/formula_lab_sit_desk.gd` |
| 砖与井 | `game-godot/assets/formula_lab/temp/plates/{space_catalog,space_needs,wells}.json` |
| 砖图 | `game-godot/assets/formula_lab/temp/tiles/tile-*.png` |
| 战术档 | `artifacts/formulas/FML_TACTICAL/presets/TAC_T{0,1,3}.json` |
| 对照抽帧脚本 | `game-godot/tests/formula_lab/tactical_board_pad_shot.gd`、`sit_desk_board_dest_shot.gd`、`tactical_execute_plate_shot.gd` |

`leftover_along_dest` 外扩（已锁，勿改）：垫 `(-118,-78)…`；坞 `(-28,-56)…`。  
`board_pad_along_dest` 外扩（已锁，勿改）：T0/T3 `(-40,-30),(36,-34),(32,40),(-44,44)`；T1 `stance=single` **不外扩**。

---

## 6. 总目标下仍未齐（本刀之外）

即使 `execute_pad` 收完，下列仍在，**禁止标 complete**：

**战术**

- T5–T11 未做（不为每档另做小游戏）。
- `execute_rope` / `execute_berm` 体积仍是几何（本刀之后的下一候选，仍要相机语言对，不要 iso 砖乱贴）。
- 承力 / 拦截 / 合体 = `capability_gap`。

**结算**

- T3 章末 `SET_CAP_CHAPTER` 不假实现。

**调查**

- 主工程 Desk 仍是勾选列表（实验室已有两态板，主工程未换）。

**探索**

- `EXPL_CAP_CROWD_STATE` 跨尺交接未做。

**世界图**

- 下一轮未验证。

**Hub**

- 主工程无万机馆 Hub。

**叙事**

- T3 无 preset；T4 同意事件；T5 探索叠层。

**形态债（贯穿）**

- 官方帧未因这些刀重抽。
- 多处仍是「可换档临时美术」，未冻结。
- 金标视觉交互语言：铬已收较多，场面物件仍在从几何体积迁到绘景 dest；迁完仍要核对「看上去像不像」，不能只 RGB 计数。

---

## 7. 抽帧与运行备忘

- 设计分辨率 **1280×720**，窗口短抽。
- 进公式台真实按键，不要伪造 readback。
- RGB 脚本惯例：exact 计数旧夹具色 → 0 或大跌；金标铬/键/机体井像素相等。
- `tier-iso-plate/`（2026-09-04）对 T0/T3 是**偏旧**全场对照，全屏 Δ 大会混进其它已收刀，不能单独证明「只改了环垫」。新刀尽量对照**同层最近一次** `tier-*`。

---

## 8. 给后续模型的开工清单

1. 读本篇 §1–§4，再读 138 §2.3 战术段 + 137 §14 最近三条。
2. grep 确认 `DEST_ORDER` 仍以 `board_pad` 结尾、`execute_pad` dest API 仍缺失。
3. **只实现 §4 的 `execute_pad` 绘景 dest。** 砖必须是近景湿铬，禁止 `tile-road`。
4. 抽帧 + RGB + 范例 + 文档（§4.4）。
5. 不要改 Canon / Reader / `stand_uv` / 地图层已收 `board_pad` / leftover dest 的 F 循环。
6. 收完后**不要**把总目标标 complete；下一刀再锁 `execute_rope` 或其它公式的形态债。

会话记录（非权威）：Cursor agent transcript `8c86c47f-c689-4d38-b049-8b0a90a824e5`。
