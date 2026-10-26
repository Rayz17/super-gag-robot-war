# C01E02 M2.2 实现说明

> Status: `synthetic fixture verified / zero real handoff`
>
> Active entry: `res://scenes/candidate_runtime_demo/c01/e02/c01e02_g1_runner.tscn`

权威合同 SHA-256：`19=6a2a05c4a4627106e716b45202aafcf10a3466f94d53211617feaaed5398bf94`、`20=038bfb0d57aea64c1ca3a91cae7e1623a33d7c8aaeb7e7ae2af4541770ca3f0d`、`22=5898e70d394f1b36386bd28c7feae8cf1af3fc2e505349ff73412e664db98e33`。

## 冻结身份

```text
contract_revision=2
build_id=C01CDV1-M2-R2
save_schema=2
content_fingerprint=00f20b087b384f40f2a3602c25d41220dbda7504562533e811b6986522963fd4
profile_id=c01cdv1_e02_scroll_m2_r2
topology_sha256=baefc17f22f1a7d8956133e73be3a4d0e1a62a369441d782701975fa6230f8d8
approved_handoffs=[]
runtime_art_loaded=false
```

## 接线链

```text
producer exact handoff batch
  -> Python metadata authorization
  -> authorized resource probe
  -> frozen validated receipt + rejection report
  -> whole-file SHA-256 supplied to Godot
  -> Godot independently verifies receipt and entry hashes
  -> same active Runner prepares each requested slot
  -> verified texture or that slot's named-geometry fallback
```

Python 批量入口位于 `candidate_asset_resolver_r2.py`，支持 `--handoff-batch`、`--output-receipt`、`--output-rejections`、`--allow-partial` 和受限的 `--fixture-mode`。Godot 消费端位于 `candidate_asset_slot_resolver_r2.gd`，活动 Runner 在启动时显式调用它，但默认不提供 receipt，因而零探测、全槽回退。

## 强门禁

- 先验授权范围、生命周期、build/fingerprint/profile/topology、Stable/Subject/slot/usage/binding，通过后才读取资源。
- 拒绝 `..`、反斜杠、NUL/编码绕过、字符串前缀伪装、realpath 越界与 symlink 逃逸。
- Python 读取真实 SHA、PNG 尺寸/alpha、音视频编码/时长/帧率；Godot 消费前再校验 receipt 与资源 SHA、图像尺寸。
- receipt 文件 SHA 不符时，活动 Runner 整包拒载、零资源探测；坏 receipt 本身不被改写。
- 坏槽不进入 validated receipt；`--allow-partial` 仅允许其他已验槽继续，坏槽精确回退。
- 合成夹具只允许 `res://tests/fixtures/candidate_asset_r2/m2_2/`，不会探测美术 Session 目录。测试结束只删除该 M2.2 子目录及对应导入缓存，不清理其他会话夹具。

## Runner 显示层

- MAP 固定顺序：base -> buildings -> state layers -> units/shield -> roofs -> foreground；occlusion mask 仅驱动已定的“淡出＋轮廓”。
- Q/SD 从 atlas 实际取四朝向 frame，bottom-center pivot 只影响显示，2x2/3x3/1x1 footprint 与 anchor 仍由冻结战棋状态拥有。
- 重盾四槽只读 `wall_hung / held_cold / red_blocked / heat_deformed`，没有增加取盾、挡击或盾拍状态。
- 几何/夹具对照开关仅在 fixture mode 可用，不写存档，不改战棋签名或 Phase payload。

## Schema

- 批量 handoff：`game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/producer_handoff_batch_schema_r2.json`
- 冻结 receipt：`game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/validated_asset_receipt_schema_r2.json`
- 单槽 handoff：`game-godot/content/candidate_runtime_demo/c01/e02/asset_integration_r2/asset_slot_schema_r2.json`

本轮未写入 `approved_runtime_assets_r2`，未接入 A1/B1/B2/A2/A3 或任何真实图像。
