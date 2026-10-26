# C01E02 A5 小型突入体四朝向母版 Atlas 美术目标

> Status: `active / approved-direction formalization / individual user decision required`
>
> Subject: `ENEMY_C01_RIFT_SWARM`
>
> Runtime slot: `ENEMY_C01CDV1_RIFT_SWARM_MASTER`
>
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 1. 本轮唯一目标

把 A3 已获用户批准的 A「伏壳钳足型」四张 `idle` 朝向样张，机械整理为符合 R2 `qsd_1x1` 约束的 96px 与 128px 两份单行透明 atlas，并在已获批的 MAP-B 三机位上验证实际比例。

本轮不重新设计小体身份，不制作移动/扑击逐帧动画，也不制作六套独立 atlas。完成后必须停在美术 Session，由用户选择具体哪一份 atlas 可作为下一批 Demo handoff 来源。

## 2. 冻结输入

完整读取并核对：

1. `19-current-demo-inplace-rebase-producer-contract.md`；
2. `20-c01e02-j2-joint-integration-contract.md`，SHA-256 `038bfb0d57aea64c1ca3a91cae7e1623a33d7c8aaeb7e7ae2af4541770ca3f0d`；
3. `21-c01e02-a3-rift-swarm-art-objective.md`；
4. `producer-a3/a3-user-approval-receipt.tsv`，SHA-256 `4698ab86e24483bbaf0bd95c5f72e9f2d9cf694f935a6176ee7862ed9465bab4`；
5. `producer-a3/a3-selected-source-hashes.sha256`，SHA-256 `ff09490e4e0cad1c3f324c98397cd909d936a4d9447e42ff74c5c04783224355`；
6. A3 的 A 候选身份页和 north/east/south/west、96/128px 八张透明样张；
7. `producer-a4/a4-user-approval-receipt.tsv`，SHA-256 `dc402de8ee471953fa1de8b98676aa76a9826a2b219dc6010ba7e762f128781b`；
8. `art-a4-map-b-six-layer/A4_MAP_B_six_layer_composite_full_2400x1350.png`，只作外置评审底图；
9. R2 `asset_slot_manifest_r2.json` 的 `qsd_1x1` 约束、当前 Runner 的 `idle/{facing}` 读取方式，以及六个实例到单一 master slot 的绑定；
10. Current Canon 的 `ENEMY_C01_RIFT_SWARM` 与 `V355-C01E02`。

先运行合同、Canon、A3 选源哈希和 A4 回执检查。任何冻结输入漂移时停止，不自行更新制作人回执。

## 3. 身份硬锁

- 唯一候选：`CAND_C01CDV1_A3_RIFT_SWARM_A_CARAPACE_CRAWLER_V1`。
- 身份：低伏三段覆甲、前端钳足、闭合红缝、短承重足；不得借正式化重画比例、附肢或表面语言。
- 移动语法继续登记为“对角足交替爬行”，但本轮不声称已制作或接入移动动画。
- `1×1`、`bottom_center`、一个母版＋六实例轻差分的决定保持；A5 只输出母版 atlas。
- B/C 方案仅保留历史评审身份，不能混合或回流。

## 4. 两份 Atlas 硬规格

### 96px

- 整图：`384×96` PNG/RGBA；
- 单帧：`96×96`；
- 顺序：north → east → south → west；
- 帧表：
  - `idle/north=[0,0,96,96]`
  - `idle/east=[96,0,96,96]`
  - `idle/south=[192,0,96,96]`
  - `idle/west=[288,0,96,96]`

### 128px

- 整图：`512×128` PNG/RGBA；
- 单帧：`128×128`；
- 顺序：north → east → south → west；
- 帧表：
  - `idle/north=[0,0,128,128]`
  - `idle/east=[128,0,128,128]`
  - `idle/south=[256,0,128,128]`
  - `idle/west=[384,0,128,128]`

共同元数据：

```text
binding_kind=sprite_sheet
pivot=0.5,1.0
footprint=1,1
actions=idle
facings=north;east;south;west
```

各帧之间不得有间隔、说明文字、棋盘格底色或跨帧像素；接地点须落在帧底边，四向身体基线不得跳动。

## 5. 动作与实例边界

R2 当前只消费 `idle/{facing}`，且允许的单行尺寸不能合法容纳 move/impact 多帧。本轮因此：

- 只声明 `actions=[idle]`；
- 不把 A3 动作空间板冒充移动或撞击动画；
- 六个实例继续共用母版；
- 用 `instance-variation-defer.tsv` 登记 01 基准、02 红褐色斑、03 冷绿灰色斑、04 黄褐擦痕、05 末端缺口、06 红缝亮度差，全部标记 `runtime_deferred_not_bound`；
- 不制作六套 atlas，不宣称游戏内已经显示轻差分。

若用户要求本轮六只必须肉眼不同，立即停止并把“扩展 R2 instance variation 接口”作为程序与美术联合决策，不自行实现。

## 6. 输出

只写：

`docs/superpowers/specs/production/c01-current-demo-v1/art-a5-rift-swarm-four-facing-atlas/**`

最低交付：

- 96px 与 128px 两份 atlas；
- `atlas-spec.tsv`；
- `instance-variation-defer.tsv`；
- WEST/CENTRAL/EAST 的 96/128 实际比例对照，单位只作外置 overlay；
- 四朝向基线、接地点、红缝与透明边缘检查板；
- `source-validation-receipt.tsv`；
- `asset-manifest.tsv`；
- `user-decision-card.md`；
- `completion-report.md`；
- `core-delivery-hashes.sha256`；
- 可复现打包源与只读 validator。

所有输出保持 `Candidate / runtime_allowed=false / runtime_handoff=none`。

## 7. 用户停止门

交付后逐项请用户判断：

1. 四朝向是否保持 A 案身份、是否存在朝向混淆；
2. 接地点、闭合红缝和扑击端是否稳定；
3. 96px 或 128px 哪一份批准为具体 Demo handoff 来源；同一 slot 不得同时绑定两份；
4. 是否接受当前 Demo 六实例先共用母版、轻差分延后；
5. 是否明确批准所选 atlas 的具体文件与哈希。

只有用户明确选定一份 atlas 后，制作人才可另签 exact handoff。

## 8. 禁止项

- 不写 Godot、Runner、R2 manifest、实例锚点、数量、玩法、存档、Canon、C04 或 A4 地图。
- 不制作 move/impact/死亡逐帧、六套机设、Cut-in、视频或 LibTV。
- 不自行复制到 `approved_runtime_assets_r2`，不把 `runtime_allowed` 改为 true。
- 不批量/付费生成，不 `git add/commit`。
