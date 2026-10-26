# C01E02 M2.2 测试摘要

## 专项链路

- Revision-2 合同检查：PASS，冻结 build/fingerprint/save schema 无变化。
- Manifest 默认态：51 槽、`approved_handoffs=0`、`resource_probes=0`、`runtime_art_loaded=false`。
- Python resolver：14/14 PASS；包括真实 PNG/音频/视频媒体探测，以及坏 Stable ID/hash/topology/dimension/alpha/frame/pivot/path/symlink 拒绝。
- Handoff batch：全量 13/13，单槽 1/1，坏屋顶 12/13，缺三层 10/10；坏屋顶唯一拒绝原因为 `asset_sha256_mismatch`。
- 活动 Runner：默认 0/13、全量 13/13、单槽 1/13、坏屋顶 12/13、缺三层 10/13 均 PASS。每个合法槽只有一次 Godot SHA/资源探测。
- Frozen receipt 文件 SHA 被篡改：整包 fail-closed，加载 0 槽、探测 0 项。
- 显示状态：Q/SD 四朝向 atlas 映射、重盾四态、地图五层绘制与 mask 取样均有实际绘制回执。
- 对照开关：存档 payload 不变，战棋 deterministic signature 不变，新增存档字段为 0。

## 零 Handoff 不变性

- WEST/CENTRAL/EAST 三张 1280x720 PNG 与 M2.1 基线通过 `cmp` 字节级相等。
- M2 合同回归：20 次确定性重放 PASS，出口 Phase P1。
- 落盘恢复：CP0、CP1、CP2、PHASE_PENDING、PHASE_STATE 五例均经 Runner A 销毁、Runner B 恢复 PASS。
- 旧存档：schema/build/fingerprint 错误 fail-closed，坏存档前后 SHA 不变。
- 活动资产车道 denylist：16 路径、112 项检查 PASS。
- 全量 `scripts/godot-test.sh`：PASS。
- 测试后 Revision-2 合同复查：PASS。
- Canon 边界：六层看板 current、authority check PASS、Canon smoke PASS、Godot strict PASS，无 Runtime 越界。
- 真实美术根：`approved_runtime_assets_r2` 不存在；测试后 M2.2 合成夹具目录已移除。

## 可复现命令

```bash
scripts/test_c01_candidate_asset_r2_m2_2.sh
```

完整输出位于 `main-m2-2/logs/`。脚本在成功、失败或中断时都会删除合成 PNG 夹具与对应导入缓存。
