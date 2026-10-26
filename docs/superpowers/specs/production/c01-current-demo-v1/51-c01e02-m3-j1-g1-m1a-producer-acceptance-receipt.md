# C01E02 M3-J1｜G1＋M1a 制作人签收回执

> 签收时间：2026-08-18T11:17:58Z
>
> 生命周期：`Candidate engineering evidence`

## 冻结依据

- 联合计划：`48-c01e02-m3-j1-current-art-and-gameplay-joint-producer-plan.md`
  - SHA-256：`06592d45483496247f915313fd22b6f28a4b392b1a073e2960f271d0af16eb35`
- 主程序任务书：`50-c01e02-m3-j1-common-turn-core-and-real-consumer-objective.md`
  - SHA-256：`6690773d4f3cf9182769336b72e84c87d1df4f3cf0017b2e86cc184ffd2f8deb`
- 完成报告：`main-m3-j1/06-completion-report.md`
  - SHA-256：`e002abf45baab7bde956b256d6bfc7217cab86af84d031455a65f86bdc43e776`
- 实现哈希清单：`main-m3-j1/07-implementation-hashes.sha256`
  - SHA-256：`9f215c4aa3e9bd0084c0ca62d7710152f46862e716e7b9625cc7b48c0559a2a2`

## 制作人结论

- `G1_COMMON_TURN_CORE = complete_candidate_engineering_evidence_only`。
  - waypoint 可编辑；终点朝向独立；冻结意图实际驱动结算；提交摘要可返回；Preview／Execute 共用纯 resolver；路线哈希与事件计数来自真实数据；两种成功方案和一种失败方案成立。
- `M1A_REAL_CONSUMER_FIXTURE = complete_fixture_only`。
  - 19 个合成 fixture 槽通过精确路径、SHA、尺寸、帧序、pivot 与 fail-closed；Godot 的 Sprite2D、AtlasTexture、TextureRect 和三路音频消费者实际工作。
- 制作人独立复跑 `C01E02_M3_J1_SKIP_CAPTURES=1 scripts/test_c01e02_m3_j1.sh`：PASS。
- 当前默认入口仍是 `C01CDV1-M2-R2`；本车道非默认、禁存档、未写故事检查点。

## 不能据此声称

- `real_art=0`；`U2_visual_playtest_ready=false`。
- `exact_handoff=none`；没有加载 A4/A5/A6/A7/A8、身份锚或旧 Demo 美术作为 Runtime 图。
- M1a 消费者仍是 fixture 验证车道，尚未与共同回合沙盒合为真实美术试玩。
- 未完成完整 E02、取盾、挡赤红冲击、最后车辆通过、盾拍或 P1。
- 未晋升正式 Runtime、Canon 或默认 Demo。

## 下一门

等待 A8 交付具体获批文件后，由制作人统一签署 P1 exact handoff；随后另派 M1，把真实资产消费者与 G1 共同回合内核合进同一个非默认构建。主程序在 P1 前继续停止，不扩功能。
