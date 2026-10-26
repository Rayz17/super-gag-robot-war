# C01E02 J2 联合整合合同

> Status: `active / C01E02-only / in-place M2 continuation`
>
> Demo scope: `C01E02 S01–S07`
>
> C04 dependency: `none`

## 1. 当前结论

当前同一 Godot 入口已经具备可玩的 Revision-2 灰盒：S01–S07、32×18 户外滚动战棋、馆守 Z、BREAKER、6 个 `scattered` 小型突入体、撤离线、取盾—挡击—清空撤离线—盾拍和 E02 Phase Checkpoint 均可运行。

M2.1 已登记 51 个显示槽和 14 个实例映射，但目前仍为：

```text
build_id=C01CDV1-M2-R2
content_fingerprint=00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4
profile_id=c01cdv1_e02_scroll_m2_r2
topology_sha256=baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8
approved_handoffs=0
runtime_art_loaded=false
```

活动 Runner 尚未消费 R2 resolver；现有美术也没有一项达到精确 Runtime handoff 条件。因此 J2 的目标不是假装“已经合入美术”，而是建立可逐槽接入、可回退、可对照的真实显示链，同时继续完成首批美术设计门。

## 2. 已锁定、不再重复询问的 A2 决定

权威回执：`producer-a2/a2-user-approval-receipt.tsv`。

- 地图方向：`MAP-B 馆墙防灾环廊型`；
- 战术读法：通过；
- 遮挡：`淡出＋轮廓`；
- 压力密度：`MID / 6 个 scattered M2 锚点`。

该决定只批准继续派生，仍为 `Candidate / runtime_allowed=false / runtime_handoff=none`。它没有批准正式地图分层、Godot 导入、小体造型、最终数值或 Runtime promotion。

## 3. 本轮并行执行

### 3.1 主程序 M2.2：真实接线预备

执行 `22-c01e02-m2-2-runner-asset-lane-objective.md`。

主程序把 R2 从隔离测试壳接到同一活动 Runner，先以合成测试夹具验证首批 13 个战棋视觉槽。零 handoff 时必须保持现有几何画面、玩法状态、存档和 Phase P1 完全不变；不得读取美术目录或自行授权任何真实资产。

### 3.2 美术 A3：小型突入体 Q/SD 身份方向

执行 `21-c01e02-a3-rift-swarm-art-objective.md`。

只制作 2–3 个受控方向和 96/128px、1×1、四朝向可读性验证；完成后必须停在美术 Session，让用户逐项选择和修改。不得顺带制作正式 atlas、地图分层、馆守 Z/BREAKER/盾母版、人物或 Cut-in。

两条工作互不写同一目录，可以并行；都不依赖 C04。

## 4. 后续依赖，不在本轮提前执行

1. 用户完成 A3 小体方向裁决；
2. 美术另接 A4，把获批 MAP-B 派生为 base/buildings/roofs/foreground/occlusion/state 六层 Candidate，并停给用户审；
3. 用户明确批准具体资产“作为 Demo 派生来源”；
4. 制作人按 slot、Stable ID、路径、SHA、尺寸、pivot、atlas/frame、build/fingerprint/profile/topology 逐项签发 exact handoff；
5. 主程序只消费签收项目，做 WEST/CENTRAL/EAST 同状态真实接入捕获；
6. 用户联合试玩后，再决定是否继续投资馆守 Z、BREAKER、重盾、人物和 Cut-in。

任何一步失败都只回退对应槽，不回滚已可玩的 M2，也不建立第二套 Demo。

## 5. 用户停止门

以下事项必须停给用户：

1. 小型突入体身份、表面同源程度、移动动作语法和实例差分；
2. MAP-B 正式六层拆分与遮挡效果；
3. 每批真实资产的 Demo handoff；
4. 联合试玩是否明显更好看、仍好操作并值得继续投资；
5. 玩法因果、Canon、正式 Runtime、批量/付费生成或 LibTV。

## 6. C04 边界

C04 纯剧情 Story Chain 独立继续。其 Episode、演出投资档和未来关卡合同不得成为 C01E02 J2 输入；J2 也不得修改、等待或代签 C04。
