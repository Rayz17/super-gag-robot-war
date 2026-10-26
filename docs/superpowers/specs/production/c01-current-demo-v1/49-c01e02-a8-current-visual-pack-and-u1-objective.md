# C01E02 A8｜当前视觉资产收敛与 U1 任务书

> Owner：美术资产 Session
>
> 依赖：48 号联合计划
>
> 生命周期：全部输出 `Candidate / runtime_allowed=false / runtime_handoff=none`

## 目标

以美术资产 Session 的最新用户确认设计为唯一身份来源，交付一个能被主程序精确消费的 C01E02 最小视觉包。不得让主程序自行搜索旧图，也不得把方向样张冒充 Sprite Master。

## 必读与冻结输入

- `09b-frozen-visual-snapshot.tsv`
- `producer-g1-5/a1-user-approval-receipt.tsv`
- `producer-g1-5/b1-user-approval-receipt.tsv`
- `producer-g1-5/b2-user-approval-receipt.tsv`
- `art-a6-character-comms-ui/**`
- `45-c01e02-m3-r0-5-a7-identity-lock-producer-review.md`
- `42-c01e02-m3-r0-5-media-packing-v2.json`
- A4／A5 用户回执，只作同屏比例和场景身份依据

若美术 Session 中存在晚于 09b、且用户已明确批准的设计，先报告制作人并给出原回复证据、具体文件和 SHA；不得静默用旧快照覆盖，也不得仅凭文件时间宣称“latest”。

## Phase A：资产真值与 A6 复核

先交一张并排真值板和 TSV，逐项列出：`Stable ID → Current 身份锚 → 既有用户决定 → 当前候选 → 一致／漂移 → Demo 用途 → 下一动作`。

随后在本美术任务向用户展示并逐项确认：

1. 纪存三态 Atlas：必须延续 Current 的黑发、蓝眼、深蓝馆务外套和腕部终端；不能换成旧 Demo 头像。
2. 七海远程三态 Atlas：必须延续 Current 设计；`decision` 闭口；只作远程权限状态卡，不得读成下达战场命令。
3. 旧守护者三态 Atlas：必须明确为馆守 Z 同一主体的头胸、胸灯与扬声波形，不能画成人类、独立 AI 或副驾驶。
4. 兜灯只展示既有 OBSERVE／TENSE 在新布局中的适配，不重画、不裁切原件。

用户要求修改时在本任务逐项迭代；未获明确批准的文件不得进入 handoff。

## Phase B：最小战棋单位包

先做“单向关键帧＋A4 MAP-B 实际尺寸合成板”，停给用户确认身份与比例；通过后才扩完整 Atlas。

### 馆守 Z

- 槽：`R05_GUARDIAN_MAP_ACTION_4DIR`
- `256×256` 单帧，5列动作 × 4行朝向，总图 `1280×1024 RGBA`
- 动作：`idle / step_a / step_b / brace / recoil`
- 朝向：`north / east / south / west`
- 必须保留 Current 母版的金色多层横冠、中央红冠饰、蓝色额面、银色格栅面、红蓝胸甲、圆形金色胸核、宽厚肩、双圆柱前臂、右肩旧伤；E02本时点双前臂完整。
- 可吸收用户批准的 C 动作骨架，但不能把 C 的极简样张当作最终身份。

### BREAKER

- 槽：`R05_BREAKER_MAP_ACTION_4DIR`
- `320×320` 单帧，3列动作 × 4行朝向，总图 `960×1280 RGBA`
- 动作：`idle / charge / contact`
- 必须保留 B 的前肢承重半直立、巨型背壳、肩下低位头块、头块单红缝，以及 X 的异质／生体装甲；不得人形化、普通四足化或露出飞行核心。

### 重盾与车辆

- `R05_SHIELD_WALL_HUNG`：`256×256 RGBA`，A塔盾＋F-D70/P30，墙挂、三道旧焦痕、尚未取得。
- `R05_VEHICLE_EAST_MOVE`：`128×128`×4帧，仅 east，外观为中性应急车辆；不得医疗十字、救护车专属标志或“最后一辆车”文字。

四项均需在 A4 MAP-B、40×20投影、1280×720界面中检查体量、落点、朝向与遮挡。角色、机体和盾不得烘入地图层。

## Phase C：A7 有限表现包

- 当前 `GIANT_CONTACT` 因馆守 Z 头冠、胸甲与肩部身份明显弱于 Current 母版，继续视为待返修 Candidate；以现有动作构图为基础做窄返修，不恢复被拒的四张探索图。
- 只保留一张 `GIANT_CONTACT`、三套可复用 FX（接触尘土／炮击命中／红光蓄能）和当前原创音频。
- 红光只蓄能，不发射；重盾仍墙挂三旧焦痕；不得出现取盾、挡击、盾拍、倒地或 P1。
- 补齐 `asset-manifest.tsv`、规格、媒体 probe、完成报告、核心哈希和用户决策卡。

## 交付与停止门

- 每个获批候选必须给出具体路径、SHA-256、尺寸、alpha、帧序、pivot、状态、来源与禁止状态。
- 用户逐项批准后立即停止，回传制作人；不得写 Godot、不得复制到 Runtime 根、不得自行签 exact handoff。
- 不制作三套路面精修、其余三张 Cut-in、长 animatic、LibTV 视频或付费批量资产。
- 发现重大身份冲突时写明方案与决策点并停下，不自行折中。

