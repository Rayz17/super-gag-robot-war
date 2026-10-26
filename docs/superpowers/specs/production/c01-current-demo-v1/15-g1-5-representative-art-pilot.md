# C01E02 G1.5 代表性真实资产 Pilot 联合合同

> Status: `active / production_grammar_user_confirmed / individual_asset_approval_required / no_runtime_art_yet`
>
> Parent production baseline: `4347597e7f7960dc605a8ec1b53d26b7d8df91cb`
>
> Frozen story/visual contract: `C01CDV1-G1-v1.0.0`
>
> Existing G1 content fingerprint: `944febc74eecb05f7b7c163728910befb2dc9a210a971c3d71526841e3d5af94`

## 1. 本轮到底在做什么

G1.5 不是批量补齐 E02，也不是把已有 Previs 升格为正式美术。它只验证一条可重复的真实资产接入链：

1. 美术为一个确定会使用的对象提出可审查的设计候选；
2. 用户在美术 Session 逐项确认或要求修改；
3. 制作人只对用户明确批准的具体文件签发精确交接；
4. 主程序把该资产装入隔离的 Candidate Demo 槽位，并保留占位/静态回退；
5. 联合比较“原灰盒”和“批准资产接入版”，再决定是否进入下一项。

本轮第一个对象固定为 `MECHA_C01CDV1_GUARDIAN_Z` 的 E02 完整双前臂 Q/SD 战棋地图造型。美术只执行 A1，主程序只执行 M1。A1、M1 完成不等于资产获批，也不自动开放 BREAKER、动作帧、正式 Cut-in 或 LibTV。

## 2. 用户已经确认的制作语法

以下是 Demo 的表现分工，不再要求两个 Session 自行猜测：

| 空间/用途 | 应用形态 | 禁止误用 |
|---|---|---|
| World 探索 | 专门重绘的 Q 版人物/小型机器，配合分层场景与镜头移动 | 不把正比例人物整张图缩小当地图角色 |
| Tactical 战棋 | 专门重绘的 Q/SD 机体 Sprite，明确 footprint、朝向和动作读法 | 不把正比例机体 Pose 直接缩放塞进格子 |
| Screen 对话 | 最新场景底图、正比例人物半身/表情、Godot 分层调度 | 不复用旧头像，不把满屏 Keyframe 当常驻立绘 |
| Shot 高潮 | 正比例人物/机体 Keyframe、Pose、Cut-in；必要时再做 2–5 秒 LibTV 短片 | 不让长视频替代可玩状态，不在母帧未通过时烧视频额度 |
| 返回可玩 | 回到同一 World/Tactical 状态，因果与输入连续 | 不用换场掩盖状态断裂 |

现有 36 秒 Animatic 只是一份内部节奏和镜头顺序板，不是剧情动画成片，不是正式美术验收件，也不是 LibTV 产物。它保持冻结，不作为 G1.5 A1 的交付物。

## 3. 权威、生命周期与逐项用户门

- 本文件记录 Demo 的制作方向，不迁移 Canon、身份锁或正式 Runtime。
- 所有新产物初始均为 `Candidate / runtime_allowed=false`。
- “Session 已完成”“文件存在”“自动检查 PASS”均不代表用户批准。
- 每个美术对象必须单独在美术 Session 展示。用户只能逐项给出下列结论之一：
  - `方向通过，可继续细化`
  - `需要修改`
  - `仅参考，不进入 Demo`
  - `批准作为 Demo 派生来源，等待制作人交接`
- 用户确认前，美术不得自行开始下一个对象；主程序不得读取或复制该候选图。
- 用户确认后，仍须由制作人登记精确 Stable ID、文件路径、SHA-256、用途和允许接入的 Candidate 槽位，才能进入程序总装。
- 付费生成、批量 AI 派生、LibTV、Canon 迁移、正式 Runtime promotion、玩法因果或共享架构修改，均须停下交用户确认。

## 4. G1.5-A：现在并行派发的两个目标

### A1 — 美术资产：馆守 Z Q/SD 地图造型方向板

只完成下列工作，然后停止并等待用户在美术 Session 审定：

1. 依次读取 `00`、`04`、`05`、`07`、`09b`、`10`、`14` 和本合同；运行 `python3 scripts/check_c01_current_demo_contract.py`。
2. 核对 `VIS_CML008_CURRENT_BASE` 与 `VIS_GUARDIAN_Z_V10X` 的身份关系，明确哪些是 Hard/Current 身份锚，哪些只是 E02 Candidate Previs；不得读取 V21/A3 飞翼或 E03 以后破损状态作为设计输入。
3. 提交一张设计判断板，包含 2–3 个受控的 Q/SD 比例方向候选；这不是最终 Sprite 表，也不制作动画。
4. 每个候选必须同时展示：
   - 正面或三分之四主视图；
   - 96 px 与 128 px 原生显示尺寸；
   - 放入 2×2 footprint 的战棋读法；
   - 与身份锚并排的识别点标注。
5. 必须保留头冠/面部、胸部、肩部与右肩旧伤等馆守 Z 识别点；E02 保持两条原装前臂完整。不得出现飞翼/背包、巡展替换臂、火箭拳或 C01E03 以后的右臂毁损。
6. 只写入 `docs/superpowers/specs/production/c01-current-demo-v1/art-g1-5/**`；登记来源、父级、状态、SHA-256 和 `runtime_allowed=false`。不得覆盖 `art-g1/**`，不得写 Godot，不得迁移资产。
7. 交付时在美术 Session 直接向用户说明各候选在“像馆守 Z、格上可读、动作可扩展”三方面的取舍，并停在用户门；不得继续 BREAKER、盾、动作帧、Cut-in 或 LibTV。

若现有身份资料不足以做受控候选，应写 `art-g1-5/BLOCKED.md`，列出缺的决定并停止，不得自行补 Canon。

### M1 — 主程序：真实资产接入壳与回退验证

主程序可与 A1 并行，但只能使用几何测试夹具：

1. 冻结 G1.1 已通过的玩法、状态机、CP0–CP3、现有捕获和 `main-g1/**` 证据，不覆盖原结果。
2. 在 Candidate 专用命名空间内建立数据驱动的 G1.5 接入壳，至少支持：
   - `MECHA_C01CDV1_GUARDIAN_Z` 与 `ENEMY_C01CDV1_BREAKER_GROUND` 的 Q/SD Sprite 槽；
   - 2×2/3×3 footprint、统一 anchor/pivot、朝向和 96/128 px 预览；
   - `idle / move / brace / impact` 等命名动作的可缺省映射；
   - `CUTIN_C01CDV1_GUARDIAN_STAND` 与 `CUTIN_C01CDV1_SHIELD_VICTORY` 的静态 Pose/Cut-in 槽；
   - 可选短视频层及同镜头静态回退，Full/Skip 结果一致。
3. 只用明确标记的几何/色块测试夹具验证接口。不得加载 `art-g1/**`、`art-g1-5/**`、旧 portrait、旧 story_first 资产或任何视频。
4. 对缺文件、错误尺寸、未知动作、`runtime_allowed=false` 或缺少制作人交接记录的资产实行 fail-closed；运行时退回具名占位或静态 Pose，不得静默加载。
5. 输出一份槽位 schema/manifest、自动检查，以及 1280×720 的接入壳证据图；证据图只证明尺寸、anchor、遮挡与回退接口，不承担美术判断。
6. 只写入：
   - `game-godot/content/candidate_runtime_demo/c01/e02/**`
   - `game-godot/scripts/candidate_runtime_demo/**`
   - `game-godot/scenes/candidate_runtime_demo/**`
   - `game-godot/tests/candidate_runtime_demo/**`
   - `docs/superpowers/specs/production/c01-current-demo-v1/main-g1-5/**`
   - 必要时扩展现有 `scripts/run_c01_candidate_demo_g1.sh` 与 `scripts/test_c01_candidate_demo_g1.sh`，但不得改变默认 G1.1 行为。
7. 禁止修改 `project.godot`、启动路由、Autoload、共享 Current、默认入口、Save/Profile 边界和玩法规则。若接口必须依赖这些修改，写 `main-g1-5/BLOCKED.md` 并停止。

M1 完成后只报告“接入壳就绪”，不得声称真实美术已接入或 Demo 已更好看。

## 5. 后续依赖队列（现在不派发）

| 顺序 | 解锁条件 | 下一项 | 用户门 |
|---|---|---|---|
| B1 | A1 的馆守 Z Q/SD 方向获批 | BREAKER 身份方向板与 Q/SD 候选 | 单独审定 BREAKER |
| B2 | B1 获批 | 退役重盾墙挂/持盾/烧红/受损四态 | 单独审定重盾 |
| B3 | 两机一盾方向获批 | 战棋地图底板、遮挡与热点层 | 单独审定地图 |
| B4 | B1–B3 获批 | 两机最小动作帧与战斗 FX | 逐组审定，不批量放行 |
| C1 | 用户批准具体文件且制作人签发交接 | 主程序只接入获批资产，制作 A/B 对照 | 用户试玩/联合验收 |
| D1 | 正比例起止母帧另行获批 | 从 S05 或 S07 选择一个必用高潮做 2–5 秒 LibTV 试片 | 付费生成前再次确认 |

默认优先候选是 S07 的挡击/强化盾拍，因为 `D0_S07_OUTCOME=gameplay_finisher` 已锁定；但这不构成本轮 LibTV 授权。

## 6. 制作人回收与继续派发规则

- 制作人负责读取两个 Session 的完成报告、核对实际文件与 hash、检查越界，并维护下一步交接；用户不需要自己重写或转发目标。
- 用户只需在美术 Session 对当前展示项给出审美/设计判断；若主程序遇到共享架构、玩法或 Canon 决策，也必须停下交用户。
- 两边完成 G1.5-A 后，制作人先做联合只读验收；只有 A1 获批，才向美术派发 B1。M1 可先完成并等待，不得以程序空槽催促用户接受美术。
- 设定/剧情/台本 Session 继续独立推进；其工作树 latest 不自动回灌本 Demo 冻结截面。
