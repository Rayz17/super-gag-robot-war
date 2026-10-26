# C01E02 M3-R0.5 M0｜零资产表现壳实现与架构回执

> 日期：2026-08-18
>
> 状态：`Candidate shell implemented / non-default / zero real handoff`
>
> 最高结论：`presentation judgeability only`

## 1. 权威输入

- `40-c01e02-m3-r0-5-frozen-contracts.sha256`：更新后 ledger 全项 `OK`，包含 41、42、43、44。
- 41 SHA：`9b81d931bee499f81353bd56a1ebb6a2f6bf64b9ce250ae63cc8b665822fb485`。
- 42 SHA：`fe75667eac656756e35ddbbb784e250d39c0f8b05c2c14f719234d653b944012`。
- 43 SHA：`921242d3ac31c64593bd9ce2465caadce7eeb2b546e78e092d20405cde2ee8a9`。
- 44 SHA：`6ed27cc2240d01d8205b5c564f116c838ba5304ac250be3ec1f1a20009cd44e2`。
- 冻结 R0 resolver SHA：`09de5610d7896abe4c516f98b91e5c7427e5a54d51dd3039e14588e95a6a8386`。
- 冻结 R0 profile SHA：`f62a8be16d1aec0da3986bdee20d94366190b7ae428c78a1d20ecdc1fc3d4f2e`。

## 2. 节点层级

```text
M3R05Runner
├─ SharedRoundAdapter
├─ TacticalBoardView
│  ├─ BoardViewport
│  ├─ NamedGeometryWorld
│  └─ PresentationCamera40x20
├─ PlayerPlanningHUD
├─ CharacterCommsLayer
├─ RoundPresentationDirector
├─ PresentationAssetResolver
├─ PresentationAudio
└─ DeveloperOverlay
```

`PresentationGridTransform` 是独立 `RefCounted` 投影对象。表现、通讯、资产 fallback、音频和调试层均未堆入 resolver，也未修改 R0 玩法文件。

## 3. 状态流

```text
READY
  -> SITUATION_REVEAL (3.4s, 纪存)
  -> PLAN_EDIT (七海 presence 常驻；兜灯首次提示)
  -> PLAN_SUMMARY (可返回；长按 1.15s 才提交)
  -> RESOLUTION_PLAYBACK (B03-B08)
  -> AFTERMATH
```

`RoundPresentationDirector` 只消费一次 `execute_committed_plan()` 的 resolved result。Full、Skip、fallback 使用相同 semantic result；中间视觉帧只含 `gameplay_write_count=0`，不会反写 `world_result`。

## 4. 40×20 投影

投影固定为 `isometric_tile_half_40x20`、逻辑网格 `32×18`、topology `baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8`。

| 锚点 | Cell | World | Roundtrip |
| --- | --- | --- | --- |
| 馆守 Z | `[15,11]` | `[160,520]` | PASS |
| BREAKER | `[20,13]` | `[280,660]` | PASS |
| 东口 | `[31,7]` | `[960,760]` | PASS |
| 墙挂盾 | `[11,10]` | `[40,420]` | PASS |
| 固定原点 | `[0,0]` | `[0,0]` | PASS |
| 固定接触格 | `[20,10]` | `[400,600]` | PASS |
| 远角 | `[31,17]` | `[560,960]` | PASS |

## 5. 角色与显示文案

- 纪存：路线、人员与危险方向。
- 兜灯：机况与承力。
- 旧守护者：机体意志、接触与看盾余韵。
- 七海：44 号 `presence_cards` 独立消费者；显示“七海 / 远程 / 代哥东区封存中心 / 本人停机令已撤回”，`decision` 几何头像，无按钮、无命令能力、无炮火权、无台词。
- 冻结 R0 的 `最后应急车 [自动]` 仅在表现层映射：规划/结算为“应急车”，余韵为“收尾应急车”；R0 profile 未改。
- 玩家路线明确标为“系统预览路径”，没有把冻结 R0 的唯一 BFS 路径描述成可编辑 waypoint。

## 6. 保护边界

- 非默认场景直接启动；未修改 `project.godot`、startup、Autoload、Save 或当前 Runner。
- 未修改 `m3_r0` resolver/profile/tests，也未修改 A4/A5、Canon、Reader、33-44 或任何美术目录。
- 未读取、探测、复制或接入 A6/A7 输出目录。
- 未执行 `git add` 或 `git commit`。
- 真实资源批准、加载和探测计数均为 0。
