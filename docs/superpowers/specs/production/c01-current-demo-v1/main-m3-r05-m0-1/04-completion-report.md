# C01E02 M3-R0.5 M0.1 完成报告

## 结论

47 号目标书 allowlist 内的 M0.1 身份感知回退已实现并通过机器门。当前仍是非默认、禁存档、零真实资产工程壳：`evidence_class=engineering_shell_evidence_only`、`real_asset_loader_implemented=false`、`user_visual_playtest_eligible=false`、`u2_eligible=false`。

本报告不声称视觉可判断、可用户视觉试玩、可交接或 R1 ready。

## 实现

- Resolver 逐项报告九个身份关键槽为 `portrait_or_identity_unavailable`，固定输出 fallback count 与全部 U2 blockers；manifest 的 `runtime_allowed` 开关不能产生加载、probe 或 U2 资格。
- 馆守Z技术 schematic 锁定 18m/2x2、0.5/0.88 pivot、金横冠/中央红饰/银格栅/红胸/圆金胸核、双完整圆柱前臂和右肩旧伤。
- BREAKER 技术 schematic 锁定近30m/3x3、0.5/0.9 pivot、前肢承重半直立/低伏冲撞、肩壳下低位头块、单红缝、闭胸缝、封背出口与 B+X 异质生体装甲语言。
- 重盾保持墙挂三旧焦痕；应急车移除医疗十字，只保留中性应急技术轮廓与“自动”语义。
- 纪存、七海、兜灯使用无脸技术剪影；旧守护者使用馆守Z机头、胸灯和扬声波形。七海卡显示“远程权限状态 / 本人停机令已撤回”，无按钮、行动图标、命令或炮火权。
- 顶栏显示“本轮操作：馆守Z”；纪存、兜灯、馆守Z本体职责文案按 46 冻结。兜灯原句仍只触发一次，且显示期间规划输入被阻断。
- F3 回执直接显示工程壳证据级别、loader=false、U2=false、九槽 fallback 与阻断原因。

## 超时事故

PID 16942 的首次 UI smoke 不计 PASS。其首次脚本编译失败导致 `_run()` 在到达 `SceneTree.quit()` 前中断，进程随后空转；TERM 清理成功。显式 float 修复后，UI flow 在 15 秒外部硬门下 0.64 秒退出，M0.1 专测 0.45 秒退出，均无残留。最终总门已默认给每个 Godot 子进程施加 60 秒 alarm，超时直接非零失败。详见 `00-ui-flow-hang-incident-receipt.json`。

## 测试与捕获

最终 `scripts/test_c01e02_m3_r05_m0_1.sh` exit 0：updated 40 ledger、packing、M0.1 专测、M0 原专项、五张新捕获、R0、默认 startup、M2、M2.5、V35/current-demo、全量 Godot 与 Canon 全部通过。旧 `main-m3-r05-shell/**` 前后摘要均为 `c9c4578d54d12b1ec86f1707f2ae767257975d99d53556fbd332ac857672991f`。

五张新图及逐图 state receipt 只位于 `main-m3-r05-m0-1/captures/`，全部 1280x720、非空，并标记 `engineering_shell_evidence_only`。详见 `03-capture-manifest.tsv`。

## 全部 U2 Blockers

1. `exact_handoff_loader_not_implemented`
2. `world_real_asset_consumers_not_implemented`
3. `screen_real_asset_consumers_not_implemented`
4. `audio_real_asset_consumer_not_implemented`
5. `identity_critical_slot_fallback:R05_PORTRAIT_JICUN`
6. `identity_critical_slot_fallback:R05_PORTRAIT_QIHAI_REMOTE`
7. `identity_critical_slot_fallback:R05_COMMS_OLD_GUARDIAN`
8. `identity_critical_slot_fallback:R05_GUARDIAN_MAP_ACTION_4DIR`
9. `identity_critical_slot_fallback:R05_BREAKER_MAP_ACTION_4DIR`
10. `identity_critical_slot_fallback:R05_SHIELD_WALL_HUNG`
11. `identity_critical_slot_fallback:R05_CUTIN_GIANT_CONTACT`
12. `identity_critical_slot_fallback:R05_CUTIN_DOUDENG_OBSERVE`
13. `identity_critical_slot_fallback:R05_CUTIN_DOUDENG_TENSE`

未来 M1 仍需 producer exact handoff、逐槽 fail-closed loader、世界 Sprite/AnimatedSprite 消费者、屏幕 Texture/Atlas 消费者、真实 AudioStreamPlayer 消费者及九个关键槽全部真实加载。M0.1 未开始 P1a/P1b/M1，也未读取 A6/A7 文件。

## 43 第 6 节强制段落

以下是 43 号合同规定的声称上限：

```text
Claim level: presentation judgeability only
General common-turn causality: NOT PROVEN
Editable route/waypoints: NOT IMPLEMENTED
Commit summary completeness: INCOMPLETE IN FROZEN R0
Derived mutation/settlement evidence: NOT PROVEN
Actual route hash: NOT IMPLEMENTED
R1 readiness: BLOCKED BY PRODUCTION BOARD HARD GATES
```

46 号纠偏继续降低本次实际声称：`character identity judgeability = NOT PROVEN`、`mecha identity judgeability = NOT PROVEN`、`overall visual judgeability = NOT PROVEN`。因此 M0.1 的实际证据级别仅为 `engineering_shell_evidence_only`。

## 停点

M0.1 到此停止。默认入口、冻结 R0 resolver/profile、玩法结果、project/startup/Autoload/Save、A4/A5、Canon/Reader、33-47、A6/A7 和旧 M0 证据均未修改；未执行 git add/commit。
