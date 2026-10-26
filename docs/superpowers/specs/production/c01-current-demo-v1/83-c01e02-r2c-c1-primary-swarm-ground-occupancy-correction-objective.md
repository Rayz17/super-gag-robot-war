# C01E02｜G2-A.1-R2C-C1主小体地面占位纠偏唯一任务书

日期：2026-08-20  
状态：`DISPATCHED_TO_MAIN_PROGRAM_2 / ART_AND_G2_A2_PAUSED_AT_ENTRY_GATE`  
权威范围：Candidate exact geometry纠偏；不改Canon、正式Runtime、默认入口或真实美术权限

## 1. 纠偏原因与制作人裁决

R2C当前A路把第一只突入小体回写到`[21,9]`，同时馆守Z在`[20,9]`、footprint为`2×2`，实际占用`x=20..21 / y=9..10`。两者发生真实地面占位重叠。现有测试只把BREAKER标记为动态阻挡，没有检查非阻挡小体与可见巨体的占位互斥，因此机器PASS没有发现这个产品错误。

制作人裁决：

```text
strategy                    = A_BODY_INTERCEPT
primary_swarm_old_anchor    = [21,9]       # invalid / History only
primary_swarm_new_anchor    = [22,9]       # sole Candidate ground truth
primary_swarm_footprint     = [1,1]
primary_swarm_status        = deflected_alive
primary_swarm_grounded      = true
primary_swarm_blocks_route  = false        # preserve existing gameplay property
guardian_anchor             = [20,9]
guardian_footprint          = [2,2]
ground_rectangles_overlap   = false
```

禁止以airborne/display-only offset、隐藏小体、缩小透明度或画面错位制造“逻辑`[21,9]`、显示`[22,9]`”双真相。resolver、entity anchor、performance track终点、Overlay、Actual Frame与下游美术统一读取`[22,9]`。

## 2. 保持不变的R2C真值

除A路第一只小体外，80号签收的全部值保持不变：

- A/B规划路线、settle facing、contact facing与T3.00/T3.25时点；
- 馆守Z/BREAKER contact anchor、impact socket、normal、recoil、post anchor；
- T1应急车、T3巨体接触、T4城市炮、T5路面／赤红蓄能的事件顺序；
- A路`heat=24 / margin=4`及第二轮`heat=68 / margin=1`；
- B路所有world result及第二轮`heat=88 / margin=0`；
- post-BREAKER 3×3动态阻挡、A/B第二轮exact路线和非法穿越点；
- `real_art_loaded=0`、`approved_handoffs=[]`、非默认入口、save disabled、G2-B关闭。

不得借本纠偏改玩法收益、路线成本、接触构图、其他小体位置、UI文案、相机或画面风格。

## 3. 实现范围

先审计再做最小修改。允许写：

- `game-godot/scripts/candidate_runtime_demo/c01/e02/m3_golden_slice/shared_round_domain/golden_slice_resolver.gd`
- 直接验证本纠偏所需的`game-godot/tests/candidate_runtime_demo/m3_golden_slice/g2_a1_r2c_*`
- 必要的专用测试／capture driver及`script/test`入口；禁止修改旧证据来伪装历史
- 新证据目录：`docs/superpowers/specs/production/c01-current-demo-v1/main-g2-a1-r2c-c1/**`

以下只读：正式profile、session、route planner、performance director、tactical geometry/view、R1音频消费者、80号之前的`main-g2-a1-r2c/**`证据、82号G2-A.2目录、默认入口、save、Canon、Reader与全部美术目录。

若performance director已经从`world_result`读取终点，则不得为本纠偏复制一套手写终点；用测试证明它自然得到`[22,9]`。

## 4. 必须新增的验证

1. A路`world_result.swarm_positions.ENEMY_C01_RIFT_SWARM_01 == [22,9]`。
2. 同一实体的`entities[].anchor == [22,9]`且`status == deflected_alive`。
3. T2 Swarm performance track的`final_cell == [22,9]`；T3继续显示同一地面anchor，不回退`[21,9]`。
4. 1×1小体矩形与馆守Z2×2、BREAKER3×3均`no overlap`；同时小体保持`blocks_route=false`。
5. A/B preview与execute仍逐字段一致；连续20次A/B执行hash分别稳定。
6. A路第一轮其余world字段不变；A路第二轮exact路线仍为10步、`68/1`，非法`[20,10]`仍因post-BREAKER拒绝。
7. B路结果逐字段不变，第二轮仍为9步、`88/0`。
8. T1→T5顺序、T3 contact socket、T4 side socket、R1 contact audio边界全部回归通过。
9. 真实美术加载仍为0，默认入口／save／Canon／Runtime隔离继续通过。

## 5. 必交证据

全部写入`main-g2-a1-r2c-c1/**`：

1. `01-input-and-scope-receipt.md`
2. `02-ground-occupancy-proof.json`：同时给出三个footprint矩形、交集、grounded与blocks_route字段
3. `03-r1-r2-nonregression-proof.md`
4. `04-determinism-receipt.json`
5. `05-actual-frame-manifest.json`
6. `captures/C01E02_G2A1_R2C_C1_A_T2_SWARM_DEFLECT_ACTUAL_1280x720.png`
7. `captures/C01E02_G2A1_R2C_C1_A_T3_CONTACT_ACTUAL_1280x720.png`
8. `06-actual-frame-visual-review.md`
9. `07-test-report.md`及完整日志
10. `08-completion-report.md`
11. `delivery-hashes.sha256`

两张Actual Frame必须来自Godot root viewport，并清楚显示小体、馆守Z与BREAKER的独立footpoint／占位。静态注入帧只能证明空间纠偏，不能冒充连续演出完成。

## 6. 完成与停止门

完成状态只能是：

`R2C_C1_IMPLEMENTED_AND_EVIDENCED / WAITING_PRODUCER_REACCEPTANCE`

完成后停下。制作人必须重新核验代码、回归、哈希和两张Actual Frame，随后才可：

- 恢复80号Candidate exact geometry签收；
- 给81号Scene-First美术发新SHA并解除pre-generation gate；
- 允许82号G2-A.2继续实现。

在制作人重新签收前，A9.1-A6-S、G2-A.2、UA91、A9.1-B、G2-B与Runtime晋级全部Blocked。
