# C01E02 G1.5-B3 旧会展广场战棋地图美术目标

> Status: `active / B3_only / individual_user_decision_required`
>
> Parent contract: `15-g1-5-representative-art-pilot.md @ cf49dac4d539d23337999807114676c9d060ec3e`
>
> B2 objective: `17-g1-5-b2-retired-shield-art-objective.md @ 8f709de1c40132cf9c6a8b8bc918b1638a310cb0`
>
> B2 gate: `A tower shield + F(D70/P30) + E02 four-state continuity approved for derivative design / runtime_allowed=false`
>
> Frozen Demo fingerprint: `944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`

## 1. 本轮唯一目标

为 `BG_C01CDV1_PLAZA_TACTICAL` 制作 2–3 套严格共用同一投影、坐标和战斗状态的旧会展广场候选层包，让用户判断：

1. 画面是否具有“万机馆外旧会展广场”的场景身份，不再像悬空灰格；
2. 北侧保护方向、中央回旋区、南侧承冲区、两机尺度与西北重盾热点是否一眼可读；
3. 遮挡能否增加纵深，同时不遮住战棋信息和玩家操作；
4. 重盾墙挂与取走后的空挂点能否作为互斥状态独立切换。

本轮只做地图美术方向与分层原型。全部产物仍是 `Candidate / runtime_allowed=false`，不是正式 Runtime 地图；交付后必须停下让用户逐项裁决，不得自行开始 B4、C1、D1 或 LibTV。

## 2. 开工前权威读取

按顺序读取并核对：

1. `00-demo-source-authorization.md`
2. `02-e02-s01-s07-beat-runtime-map.tsv`
3. `04-e02-previs-v0.1.md`
4. `05-e02-asset-call-matrix.tsv`
5. `06-e02-state-checkpoint-contract.tsv`
6. `07-legacy-denylist.tsv`
7. `09-frozen-source-snapshot.tsv`
8. `09b-frozen-visual-snapshot.tsv`
9. `10-cross-session-coordination.md`
10. `13-demo-build-contract.json`
11. `14-g1-joint-alignment-rework.md`
12. `15-g1-5-representative-art-pilot.md`
13. `16-g1-5-b1-breaker-art-objective.md`
14. `17-g1-5-b2-retired-shield-art-objective.md`
15. `producer-g1-5/a1-user-approval-receipt.tsv`
16. `producer-g1-5/b1-user-approval-receipt.tsv`
17. `producer-g1-5/b2-user-approval-receipt.tsv`
18. `producer-g1-5/g15-b1-readonly-review.md`
19. `producer-g1-5/g15-b2-readonly-review.md`
20. 本文件
21. 冻结提交与冻结清单登记的 C01 物理板、战斗预案、E02 Reader、游戏流程和完整剧情总纲相应段落
22. Current Canon 的 `V355-C01E02`、`V353U001`、`ENEMY_C01_BREAKER` 及“旧会展广场”空间事实

先运行：

```bash
python3 scripts/report_v35_layered_pipeline.py --check
python3 scripts/check_c01_current_demo_contract.py
scripts/canon-query.sh scene V355-C01E02
scripts/canon-query.sh entity V353U001
scripts/canon-query.sh entity ENEMY_C01_BREAKER
scripts/canon-query.sh 旧会展广场
```

必须在来源回执中明确：A1-C、B1-B/X 与 B2-A/F 都只是获批派生方向，没有 Sprite Master 或 Runtime handoff；B1-B 样张尚未真正绘入 X 表面语言，B2-A 样张也尚未真正绘入 F(D70/P30)。这些文件只可进入尺度、遮挡与热点的审查合成图，不得烘焙进地图底板，也不得冒充最终机体或盾资产。

## 3. 坐标、状态与玩法硬锁

所有候选必须使用稳定态 `C01CDV1_JOINT_S06_T2_STAGE1_V1`：

| 项 | 锁定值 |
|---|---|
| 画幅 | `1280×720`；顶栏 `y=0..54`；内容区 `y=54..648`；底栏 `y=648..720` |
| profile | `c01cdv1_s06_g1_v1` |
| checkpoint | `CP2 commit_count=1` |
| turn / stage | `2 / 1` |
| 棋盘 | `12×9`，共 108 格；原点西北，`x` 向东，`y` 向南 |
| 北侧安全线 | `y=0..1` |
| 馆守 Z | anchor `(5,3)`；footprint `2×2`；facing `south` |
| BREAKER | anchor `(5,6)`；footprint `3×3`；facing `north` |
| 重盾热点 | `(1,2)`；屏幕中心 `(385,204)` |
| 进度 | 仅 `north_safety_line_held=true`；其余进度、`finisher_ready`、`finisher_triggered` 均为 `false` |
| 敌方意图 | `BREAKER / 冲撞 / 北侧城市安全线` |
| 受影响格 | `x=5..7, y=0..5` |

唯一投影：

```text
center_x = 420 + (x - y) * 35
center_y = 150 + (x + y) * 18
cell vertices = (0,-18), (35,0), (0,18), (-35,0)
```

像素锁：

- 棋盘包围盒 `x=105..840, y=132..510`；棋盘与 UI 保留 `x=852..884` 空隙。
- 馆守 Z 2×2 包围盒 `420..560 × 276..348`。
- BREAKER 3×3 包围盒 `280..490 × 330..438`。
- 冲撞带包围盒 `385..700 × 222..384`。
- 意图面板预留 `Rect(885,78,355,118)`；状态/指令面板预留 `Rect(885,210,355,414)`。

当前 profile 没有 blocked-cell 或地形阻挡拓扑；除单位占位和越界外，108 格都按同一地面通行语义处理。因此不得用墙、废墟、车辆、深坑或高差暗示某些格不可走，也不得擅自添加掩体、地形代价、高低差或碰撞。重盾热点是交互锚，不是阻挡格。

## 4. 场景事实、功能区与信息层级

- 锁定雨夜的旧会展广场；西北/北侧连接万机馆与出馆方向，东北指向居民区，中央是主战区，南侧是空旷承冲区。
- 西北墙面保留可理解的破墙、展墙或挂架关系，让 `(1,2)` 的重盾热点有物理来源；重盾取走后必须留下同位置的空挂点状态。
- 北侧安全线与冲撞红区属于程序战术 UI。地图可用铺装、立面和空间朝向暗示“北侧需要保护”，但不得把安全线或红区画成世界内发光道路、实体红墙或永久警戒带。
- 网格、可选格、意图、预测、行动菜单和交互图标均由程序拥有，不得烘焙进底板。
- 单位、状态 UI 与敌方意图的明度/饱和度必须高于环境底板；底板避免大面积高饱和红色、密集碎裂线或与可选格相同的高亮颜色。
- 战场不出现人群、小机、消防架桥机、城市炮火单位、杂兵或车辆障碍；S02 后的人类尺度单位已离场。
- 不提前暴露巡展舰前甲板、活动锁泊臂、舰体机关或 E04 起航事实。若使用旧轨槽，只能读成失活的会展遗构，不能成为新玩法或舰体伏笔。

## 5. 三条受控候选方向

只改变材质、明暗、环境密度和遮挡组织，不改变几何、路径、单位位置、胜法或故事因果：

- `MAP-A 旧会展轨道开阔型`：宽阔混凝土地面、失活轨槽与服务线，战术读法最强；需要避免过空、像测试场或提前暗示舰体机关。
- `MAP-B 馆墙防灾广场型`：突出西北万机馆破墙/展墙、东北居民方向和防灾广场身份，场景叙事最强；需要避免墙体、展台或防灾设施看起来会阻挡棋盘。
- `MAP-C 雨夜混合型`：结合轨道骨架与馆墙，用克制的雨面反射、旧损与远处火光增强电影感；需要严格控制噪声、反光和假障碍。

不得由美术任务替用户预选。若三案只换颜色而没有空间组织差异，视为未完成。

## 6. 分层规则与精确交付

仅写入：

`docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b3-tactical-map/**`

最低交付：

1. `TACTICAL_MAP_B3_direction_board_2400x1600.png`：并列解释三案的场景身份、战棋读法、遮挡收益和风险。
2. 每个 `MAP-A / MAP-B / MAP-C` 各交一组 `1280×720` 同坐标文件：
   - `base_opaque`：不含单位、网格、UI、天气、重盾或热点图标的环境底板；
   - `foreground_occlusion_rgba`：前景遮挡层；
   - `occlusion_fade_mask`：与遮挡层同尺寸的淡出 mask；
   - `shield_wall_hung_rgba`：墙挂重盾审查状态；
   - `shield_acquired_empty_mount_rgba`：取盾后的空挂点状态；两者互斥；
   - `weather_damage_rgba`：雨面、烟尘、远处火光与旧损的独立氛围层；
   - `T2S1_readability_composite`：使用锁定 T2/S1 几何和获批方向样张做尺度/遮挡审查，明确标记 `candidate_evidence / not_runtime`。
3. `TACTICAL_MAP_B3_layer_contact_sheet_2200x1400.png`：展示各层开关及墙挂/空挂点互斥关系。
4. 一张无报告文字的 geometry-only alignment overlay，严格显示 108 格格心、双方 footprint、热点、冲撞带、HUD 安全区和 UI 空隙，用于与程序 `BASELINE_S06_T2_STAGE1_1280x720.png` 做逐像素核对。
5. `candidate-spec.tsv`。
6. `map-layer-spec.tsv`：登记 z-order、alpha、anchor/pivot、状态互斥、碰撞语义和程序/美术所有权。
7. `cell-visual-audit.tsv`：登记 108 格心、热点、受影响带及遮挡覆盖检查。
8. `source-validation-receipt.tsv`、`asset-manifest.tsv`、`user-decision-card.md`、`completion-report.md`、`delivery-hashes.sha256`、可复现生成源和只读 validator。

遮挡约束：

- 棋盘外可使用硬遮挡；进入 108 格投影区的任何遮挡必须在独立 RGBA 层中，并配套 soft fade mask，`collision_semantic=none`。
- T2/S1 合成图里，馆守 Z、BREAKER、重盾热点、北侧安全线与冲撞带不得被遮住。
- 硬遮挡不得侵入意图面板、指令面板、顶部/底部 HUD 安全带或 `x=852..884` 空隙。
- A1-C、B1-B、B2-A 方向样张只能出现在审查合成图中，不能进入 `base_opaque`、遮挡或天气层。

## 7. 禁止项

- 不写 Godot，不修改 `graybox_profiles.json`、战斗脚本、UI、M1 接入壳、默认入口、Save/Profile 或共享架构。
- 不修改 Canon、Runtime 生命周期、12×9 投影、坐标、footprint、热点、路径、胜负条件、回合目标、CP2 或 D3 因果链。
- 不制作 B4 动作帧/FX、C1 接入、D1/LibTV、Cut-in、视频或正比例高潮母帧。
- 不把 B1/B2 方向样张继续精修成最终机体/盾资产；不覆盖 A1/B1/B2 交付。
- 不读取旧 `story_first`、History 战术地图或现成 IP 作为母版。
- 不新增组织、型号史、驾驶员、传奇战役、文字徽章、可交互机关或故事事实。
- 不批量或付费生成，不 stage/commit。

若地图成立必须依赖新增 blocked cell、掩体、高低差、镜头角度、动态遮挡代码、玩法规则、Canon 事实或 Runtime 改动，写 `b3-tactical-map/BLOCKED.md`，列明冲突并停止。

## 8. 验证与停止门

最低验证：

```bash
python3 scripts/report_v35_layered_pipeline.py --check
python3 scripts/check_c01_current_demo_contract.py
python3 scripts/check_canon_authority.py
scripts/canon-smoke-test.sh
python3 docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b3-tactical-map/validate_tactical_map_b3.py
(cd docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/b3-tactical-map && shasum -a 256 -c delivery-hashes.sha256)
git diff --check
```

只读 validator 至少断言：尺寸/透明通道正确、108 格投影与全部像素锁一致、三案几何完全相同、热点中心和 UI 空隙正确、墙挂/空挂点互斥、遮挡层与 mask 配对、格内遮挡 `collision_semantic=none`、manifest 全部 `runtime_allowed=false`。

交付后必须在美术任务中停止，并请用户分别裁决：

1. 地图主方向采用 `MAP-A / MAP-B / MAP-C`，或指定窄修改；
2. 遮挡采用“棋盘外硬遮挡”还是“棋盘外硬遮挡 + 格内软淡出”，并确认纵深不挡操作；
3. 隐去说明文字后，是否仍能指出北侧保护方向、南侧承冲区、西北重盾热点和取盾后的空挂点，且两机、冲撞带与 108 格操作清楚。

未获得三项明确裁决前，不得开始 B4，也不得将任何地图层交给主程序。B3 获批只解锁 B4 的单独派发；C1、Runtime promotion、Canon 迁移和 LibTV 仍继续锁定。
