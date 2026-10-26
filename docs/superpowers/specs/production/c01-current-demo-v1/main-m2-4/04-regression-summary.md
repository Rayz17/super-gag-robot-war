# C01E02 M2.4 回归摘要

## M2.4 专项

- production preflight 重放: `5 submitted / 5 validated / 0 rejected / 5 probes`
- default active art: `validated=5 / loaded=5 / probes=5 / runtime_art_loaded=true`
- remaining first-13 slots: `8` 个精确 fallback
- disable mode: `0 / 0 / 0 / false`
- bad config, missing config, bad receipt SHA: 非 fatal，`0 probes`
- single-resource missing/drift: 只降级对应 slot，其他四层继续加载
- occlusion: 馆守 Z 在 mask 内时 overhead alpha `0.28` 且绘制轮廓；离开 mask 后 alpha `1.0` 且轮廓取消
- shield: `STATE_LAYERS` 未加载，逐帧 `shield_draw_count=1`
- scroll: 36 帧 WEST→EAST，战棋和存档签名前后一致

## M2/M2.2 保留回归

- 20 次确定性重放: PASS
- CP0 / CP1 / CP2 / PHASE_PENDING / PHASE_STATE 五类销毁 Runner A、新建 Runner B 恢复: PASS
- schema 1 / 旧 build / 旧 fingerprint 存档拒载且原文件不变: PASS
- Full / Skip / 静态 fallback 语义等价: PASS
- 零 handoff 三机位与 M2.1 像素基线 `cmp`: PASS
- M2.2 13 槽合成夹具、partial receipt、缺层 fallback: PASS
- `scripts/godot-test.sh` 全量 Godot 回归: PASS

## 入口与边界

- startup selector: default Current Candidate / explicit M6 / explicit legacy: PASS
- 无参数 `project.godot -> startup_router -> Current Runner`: PASS
- Windows resource validation: `status=pass`
- static manifest: `approved_handoffs=[] / runtime_art_loaded=false`
- active denylist and exact five-file inventory: PASS
- `project.godot`, startup selector/router, stable launcher, tactical rules, save schema, build/fingerprint/profile/topology: 未改

## Canon 与仓库门禁

- C01 contract checker: PASS
- layered pipeline dashboard: PASS
- Canon authority: PASS
- Canon smoke: PASS
- Godot Canon report/strict: PASS
- `git diff --check`: PASS

## 已知视觉债

A4 五个静态地图槽已接入，但本轮没有完成撤离灯、空盾架、战损建筑和重盾四态的动态美术拆包。这些仍由程序化状态表现，不得把 M2.4 称为“动态地图美术完成”。
