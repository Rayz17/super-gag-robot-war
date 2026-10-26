# C01E02 M2.5 回归摘要

## A5 Atlas 专项

- production preflight replay: `6 submitted / 6 validated / 0 rejected / 6 probes / synthetic=false`
- default active art: `validated=6 / loaded=6 / probes=6 / runtime_art_loaded=true`
- remaining first-13 slots: `7` 个精确 fallback
- six stable instances: 共用 `1` 个 texture/master slot，PASS
- atlas frames: `idle/north|east|south|west` 四向 rect 与真实像素读取，PASS
- initial facing: `01 east / 02 east / 03 north / 04 north / 05 west / 06 north`，PASS
- bottom-center pivot: `[0.5,1.0]`，原生 `96x96` 绘制、`1x1` footprint，PASS
- geometry double draw: 真 Atlas 成功时小体几何 token 不绘制，PASS
- isolated south: 显示态覆盖四向，不写正式关卡或 save，PASS
- deterministic enemy phase: 六体仍按原 scattered AI 移动，01/02 `east -> south`，玩法签名与禁用美术对照一致，PASS
- missing/bad A5: 五个 A4 地图槽继续加载，仅 A5 单槽回退，PASS
- single A4 drift: A5 继续加载，仅对应 A4 槽回退，PASS

专项结论标记：`C01_CURRENT_CANDIDATE_M2_5_ATLAS_OK instances=6 texture_masters=1 facings=4 movement_compare=pass loaded=6 fallback=7`。

## M2/M2.2/M2.4 保留回归

- 20 次确定性重放、P1 payload、失败重试: PASS
- Full / Skip / 静态 fallback 语义等价: PASS
- CP0 / CP1 / CP2 / PHASE_PENDING / PHASE_STATE 销毁 Runner A、新建 Runner B 恢复: PASS
- schema 1 / 旧 build / 旧 fingerprint 存档拒载且坏存档原文件不变: PASS
- 32x18 滚动地图、6 小体 scattered 非同步、撤离线、盾拍一次性授权: PASS
- M2.2 resolver/zero-handoff/13 槽合成夹具: PASS
- M2.4 五槽历史 receipt 显式回归: PASS
- M2.4 地图绘制层、遮挡、滚动、盾牌单绘: PASS
- `scripts/godot-test.sh` 全量 Godot 回归: PASS

## 入口与平台

- startup selector: default Current Candidate / explicit M6 / explicit legacy: PASS
- 无参数 `project.godot -> startup_router -> Current Runner`: PASS，使用六槽活动链
- 稳定启动脚本: PASS，使用同一 Current Runner
- Windows resource validation: PASS
- active lane audit: `19 paths / 179 checks`，PASS
- static manifest: `approved_handoffs=[] / runtime_art_loaded=false`，保持不变
- active Candidate receipt: `6 validated / 6 loaded / 6 probes / runtime_art_loaded=true`

## Canon 与仓库门禁

- C01 contract checker: PASS
- layered pipeline dashboard: PASS
- Canon authority: PASS
- Canon smoke: PASS
- Godot Canon report/strict: PASS
- active denylist: 旧 fingerprint、旧 CP3、旧 B3、`story_first`、G1.5、`art-a3`、`art-a5` 源目录均为 0 次引用，PASS
- `git diff --check`: PASS

## 冻结边界

本轮没有改变 gameplay、AI、单位数量、footprint、锚点、地图、存档、build/profile/topology、Canon、C04 或启动架构。没有接入下一项美术，也没有制作 `move`、`impact`、`death` 动画或六实例差分。
