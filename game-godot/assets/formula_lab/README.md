# 公式实验室临时美术

这些图是**临时资源**，不是成片、不是 Canon、不进 CML130 / CML131。

来源：`scratch/srw-y-mode-recreation/assets/`（裂湾机兵隔离实验自己的立绘、机体、地砖、背景）。只借像素，不借裂湾的菜单、铬、胜负条件。金标仍是 138 调研案例。

缺图时壳会退化成色块，但色块不再是产品面。preset 里的 `res://assets/formula_lab/` 路径才算合法绑定。

世界图 T0/T1/T2 入口把 `temp/tiles/` 的水/岸/林/码头当**地区海图材质**，按 `map.chart.features` 多边形坐底；T0 固定目的地卡用 `entry.fixed_sit_uv`、T1/T2 短卡用 `entry.*_sit_uv`、针点用 `chart_uv` 落在同一 sit 上。废港风景照不再当世界图入口垫底。

探索与 Hub 房间按 `room.features` 多边形坐墙/地/门/道具；热点用 `walk_to_uv` / `polygon_uv` 落在同一 sit。室内默认仍用坐底色、不铺 iso tile grain（避免再读成风景照垫底）；外场院地可留浅草纹。Hub 馆另写 `surfaces`：按 feature 的 AABB 采样局部纹理/道具图（墙=废砖浅纹、地=路砖、门=开口、坞/家具=码头木台、架=废砖），人用 `stand_uv` 站地板，工作卡用 `card_sit_uv` 坐家具。探索房间另写自己的 `surfaces`：室内墙/地采样 `tile-house` 灰墙与石径，外场采样 `tile-grass`，码头地板采样 `tile-dock` 角料（与 Hub 家具木台不同裁切），内腔采样废混凝土与冷却管水色。不整张 `lab.png` / `garden.png` / `ship.png` 当房间垫底。

调查现场同样按 `site.features` 坐墙/地/门/装卸台/道具，并按 `surfaces` 给每块 feature 采样工房纹理：墙/地=`tile-ruin` 废混凝土（与 Hub 废砖浅纹、探索内腔不同裁切），装卸台=`tile-dock` 内侧钢木 + metal 收边（不是 Hub 家具木台，也不是探索码头角料 plank），缓冲尺金属、控制台家具、坞口开口、检查道槽底湿痕（T3 `workshop_lane` / T2 `bay_lane` / T1 `tri_lane` 把水色平行四边形收成坐进台面的检查槽，水色只作槽底湿痕）、校准板纸面。证据点用 `hotspot_uv` / `polygon_uv` 落在尺/台/墙/道上，`walk_to_uv` 落在地面，手册用 `paper_uv` 当盖层。不整张港区/工房/船舱风景照垫底，也不抄 Hub 路砖或探索房瓦灰墙/石径/草地。

战术战场同样按 `board.features` 坐边界/地面/掩体，并按 `surfaces` 给每块 feature 采样战场纹理：远堤=`tile-ruin` 立方体面压实土堤（AABB `[0.58,0.66,0.14,0.10]`，不是 Hub 废砖浅纹、不是调查工房混凝土、不是叙事闸位金属 `[0.40,0.64]`），交战地面=`tile-road` 擦伤沥青（AABB `[0.42,0.52,0.18,0.14]`，不是 Hub 路砖、不是叙事湿沥青密封地），环垫/绳桩=`tile-ruin` 顶面混凝土金属收边（不是 Hub 家具木台），残骸=`tile-ruin` 中腹碎砖，撤离口=开口。等距盘用 `origin_uv` 坐到地面上，grout 坐在配置地面上，单位仍站已有格子。不整张 `battle-day.png` 庭院照垫底，也不铺草绿岛。结算清图留棋复用同一套 board view，但 SET 预设没有 surfaces，仍走色块坐底。

战术演出层按 `execute.features` 坐远堤/交战地面/近景；左右机体用 `left_stand_uv` / `right_stand_uv` 站在演出地面上。不整张 `battle-day.png` 庭院照垫底。

结算清图留棋复用同一套战场坐底；编队卡用 `card_sit_uv` 叠在留棋/坞口上，Banner 用 `banner_uv` 坐在留棋战场上。不整张 `battle-day.png` 庭院照垫底。

叙事 ADV 的场面层同样按 `layers[].stage.features` 坐墙/地/门/道具，并按 `surfaces` 给每块 feature 采样校准棚纹理：墙=`tile-house` 陶土棚壁（不是探索房瓦灰墙），地=`tile-road` 湿沥青密封地（不是 Hub 路砖 AABB、不是探索石径），柜/台=门板木，闸=废砖金属收边，坞口=开口；棋盘走格用同一 `tile-road` 湿沥青巡查道（全砖 iso）。立绘用 `stands[].portrait_uv` 落在同一 sit。黑底层不垫风景照。不用 `garden.png` / `lab.png` 整屏垫底。
