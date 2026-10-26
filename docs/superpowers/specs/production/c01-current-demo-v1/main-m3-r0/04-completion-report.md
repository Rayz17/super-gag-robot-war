# C01E02 M3-R0｜完成报告

> 结论：`R0 implementation complete / machine gates pass / awaiting user playtest`
>
> 性质：`Candidate development sandbox`
> 不是：完整 E02、R1、默认 Demo、新 Runtime 或 Canon 晋升

## 已交付

同一 Godot 项目中新增了一个非默认、零存档的单轮共同结算沙盒。玩家可以完整经历：

`公开冻结意图 → 编辑短路线与独立朝向 → 主动作或预备及备用 → 可返回摘要 → 长按提交 → 同前态共同结算 → RoundReceipt`

结算包含应急车辆、小体、馆守 Z、BREAKER、城市炮火和路面。成功出口严格停在首次冲撞偏轴、城市炮命中侧甲、BREAKER 开始聚集红光。

## 证明了什么

- 单机计划数组、路线、朝向、主动作/预备、fallback 和摘要语言可以操作；
- 敌方与环境计划在编辑前冻结，草案不会推进世界；
- 同一 resolver 可以同时服务预览与执行；
- 同时接触不依赖实体容器顺序；
- 预备最多触发一次，fallback 不赠送行动；
- 两种单轮成功计划产生真实可见差异；
- 错误计划能够给出具体、可理解的身体责任失败原因；
- 60 次重放和容器反序得到确定一致回执。

## 没有证明什么

- 没有接完整 E02，也没有证明 R1 两条完整打法；
- 没有证明多机编辑、友军争格、跨机反应链或 3–5 机常规战；
- 没有实现盾牌取得、赤红冲击、撤离线清空、盾拍或 P1；
- 没有接美术、动画、声音、视频或 A4/A5；
- 机器 PASS 不代替用户试玩，也不证明最终商业品质。

## 冻结边界确认

- 默认 Demo 仍为 `C01CDV1-M2-R2`；
- 现有 Runner、`candidate_tactical_session.gd`、graybox profile 未改；
- Candidate 正式存档、schema、namespace 未改，R0 保存禁用；
- A4/A5 active binding、validated receipt 与资源未改；
- P1、Full/Skip、失败重试和旧测试未改；
- `project.godot`、startup selector/router、Canon、Reader 未改；
- 未执行 `materialize_sources.py --write`；
- 未 `git add`、未 `git commit`。

## 试玩与证据

启动：

```bash
./scripts/run_c01e02_m3_r0_sandbox.sh
```

操作说明见`02-playable-controls.md`。摘要、两种成功结果和错误结果的 1280×720 捕获及逐事件状态记录见`03-capture-manifest.tsv`与`captures/**`。

## 已知债

1. 当前为具名几何，信息结构可检验，重量、命中、声音和动作爽感尚未生产；
2. 用户尚未实玩，学习成本、计划可读性与“想再试一次”的程度仍是开放门；
3. Canon 的旧馆守 Z 术语定义有一行时序残留，已登记但按禁止写入边界未修；
4. R0 只有一台直接控制机，不能外推多机共同回合体验。

## R1 条件

技术上，R0 所需的 resolver、操作闭环和机器证据已经齐备。R1 **尚未授权**；必须先由制作人和用户试玩本沙盒，确认共同回合语言、两种起手的可读性与操作负担，再决定是否进入完整 E02。

本任务在此停止，等待用户试玩裁决。
