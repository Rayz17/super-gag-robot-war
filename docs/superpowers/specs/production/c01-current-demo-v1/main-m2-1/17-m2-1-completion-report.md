# C01E02 Revision-2 M2.1 显示层接入准备完成报告

> Status: `candidate asset interface ready / approved_handoffs=0 / runtime_art_loaded=false`

## 本轮完成

在不改 M2 Runner、玩法、状态机、存档、输入、地图或具名几何回退的前提下，建立了 Revision-2 专用资产车道：

- Schema：`game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/asset_slot_schema_r2.json`
- Manifest：`game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/asset_slot_manifest_r2.json`
- 制作人 handoff 预检：`game-godot/scripts/candidate_runtime_demo/c01/e02/asset_integration_r2/candidate_asset_resolver_r2.py`
- Godot 消费壳：`game-godot/scripts/candidate_runtime_demo/c01/e02/asset_integration_r2/candidate_asset_slot_resolver_r2.gd`
- 专项验证入口：`scripts/test_c01_candidate_asset_r2.sh`

Manifest 绑定唯一 M2 build/fingerprint/profile/topology，登记 51 个槽位、14 个 Stable Instance 映射和 6 条仅供方向预登记的 A1/B1/B2 回执。方向批准仍是 `runtime_allowed=false / runtime_handoff=none`，没有读取或导入对应图片。

## 预登记表面

- 地图 6 槽：base、buildings、roofs、foreground、occlusion mask、damage/state layers。
- 战棋 Q/SD 3 槽：馆守Z `V353U001`、BREAKER `ENEMY_C01_BREAKER`、小体母版 `ENEMY_C01_RIFT_SWARM`；明确 2x2、3x3、1x1 footprint、四朝向、96/128 px preview 和可缺省动作。
- 小体 Stable Instance：`ENEMY_C01_RIFT_SWARM_01..06`。
- 重盾 4 态：wall_hung、held_cold、red_blocked、heat_deformed，expected stable ID 均为 `MECHA_WANJI_MOBILE_CHASSIS`。
- 人物 World + Screen 20 槽：纪存 `CH_JICUN`、兜灯 `CH001`、唐胶 `CH_TANGJIAO`、七海远程 `CH_QIHAI`、旧守护者 `CH002`、机器犬 `V353U040`、跌跌 `V353U038/CH057`、老余 Candidate ID、小满 `CH_XIAOMAN`、阿澄 `CH005B`。
- 战场目标 4 个母槽、14 项 instance 映射：两辆应急车辆、东侧撤离口、两处警戒设施和四类可破坏物。
- 演出 14 槽：起身、取盾、挡击、盾拍静态 Cut-in，4 类 FX，5 类 audio，以及 1 个可选盾拍视频与同语义静态 fallback。

逐槽 expected stable ID、usage、binding、constraint、fallback 见 `r2-slot-registration-receipt.tsv`；实例见 `r2-instance-binding-receipt.tsv`。

## 强门禁

Producer handoff 必须逐槽精确匹配 handoff ID、Stable/Subject ID、slot、usage、M2 fingerprint、地图 topology、binding、pivot、actions/facings、atlas/frame regions、资源 SHA 与声明参数。通过元数据授权后才允许触碰文件；路径经过 lexical normalization 与 realpath 检查，拒绝 `..`、编码绕过、字符串前缀伪装和 symlink 逃逸。

实际媒体验证不信任声明值：PNG 读取真实尺寸、色型和 alpha；音频读取真实 codec、采样率、声道与时长；视频读取真实 codec、画幅、宽高比、fps 与时长。任一不符均回到原 M2 具名几何；不会自动搜索目录，也不会回退 G1.5、B3、`story_first`、旧头像、旧 Previs/animatic 或旧美术。

## 三机位结果

WEST `(-160,320)`、CENTRAL `(240,480)`、EAST `(830,620)` 均与 A2 review center、world rect 和 screen rect 精确对齐。三张 1280×720 截图只含当前 M2 程序几何；没有生成美术叠图，也没有为 A2 修改相机、地图或玩法。

证据：`C01E02_M2_1_WEST_PROGRAM_1280x720.png`、`C01E02_M2_1_CENTRAL_PROGRAM_1280x720.png`、`C01E02_M2_1_EAST_PROGRAM_1280x720.png`、`three-camera-program-capture-receipt.tsv`、`a2-camera-alignment-receipt.tsv`。

## 边界与下一门

- 未修改 `project.godot`、默认入口、Autoload、共享 Current、Save/Profile、Canon、剧情、玩法因果、难度、单位数或 footprint。
- 未读取 C04，也未把 C04 作为依赖。
- 未创建第二套 Demo；试玩仍使用 `scripts/run_c01_candidate_demo_g1.sh`。
- 未 stage、commit 或接入任何真实美术/音视频。

下一道门只能由制作人逐槽签发 exact handoff。收到用户批准与制作人 handoff 后，先运行同一 preflight 生成验证回执，再允许 Godot 槽位从具名几何切换；本任务在此停止，不自行开始真实资产接入。
