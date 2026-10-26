# C01E02｜R2C-C1制作人重新签收与精品视觉并行恢复回执

日期：2026-08-20  
状态：`R2C_C1_CANDIDATE_EXACT_REACCEPTED / A9_1A6_S_AND_G2_A2_RESUMED / REAL_ART_UA91_G2B_BLOCKED`  
制作人：新“制作人-2”  
权威范围：C01E02隔离Candidate；不构成Canon、正式Runtime、默认入口、真实美术或用户视觉批准

## 1. 制作人复验

制作人已从仓库根目录执行63项交付哈希复算，全部`OK`；另以不写证据的独立Godot headless调用重跑C1核心测试，得到：

```text
C01E02_G2A1_R2C_C1_GROUND_OCCUPANCY_OK
anchor=22,9 overlap=false T2=T3=22,9 A20=true B20=true R2=68/1,88/0
```

关键输入指纹：

| 输入／证据 | SHA-256 |
|---|---|
| 83号唯一纠偏任务书 | `f6ba405a809969f6013ab2f8c5b5405395866583ad4e405f35cb98af06fe7173` |
| C1 `delivery-hashes.sha256`文件自身 | `c7bb45901a3f8129f80b28fffb21004036510aba3e3202e6ca438fb3c9f6f9bf` |
| `02-ground-occupancy-proof.json` | `bb832b70416c8f1ccfb6b62781111e3ddb534bfdbae0d7ceff9035036d6917f4` |
| `04-determinism-receipt.json` | `2beda567a039aab60077c395ea28dbb1cbe12f3b5999b46022d58b84e4c5ac8d` |
| `05-actual-frame-manifest.json` | `f5bf90a096c2c04c46971c9b29e879d52a0247069d39114b49ba7ca5197ee5e5` |
| `08-completion-report.md` | `775c266e838fa43efb93138971aef5400ae60262e81069c8f00f54a599438db9` |
| T2 Actual Frame | `7a04670b113e0db25be2eb91582013ac34ab5ddffa8d9803b3b7ef0da522287c` |
| T3 Actual Frame | `8b504ee85752dfdd55c1ea6c654df2e870ef10b0aa4689e2102ae9221164b563` |
| 改后resolver | `c74f070ad88ec81f94222e84ff635bd8cf1be0741107428c78ddf5470cc16b29` |
| C1专用runner | `cebc574e7ca9f23218d67f39b9893815f45f2d274154a4366741bbde8ee06ccf` |

旧`main-g2-a1-r2c/**`41文件整树摘要执行前后均为`e32bcd99674f214a8e63102a069f97b59b1ef338c5df128251635291cad98d1e`，旧证据没有被覆盖。

## 2. 制作人Actual Frame复签

制作人已实际查看T2与T3两张1280×720 Godot root viewport帧：

- T2：青色1×1主小体在`[22,9]`，黄色2×2馆守Z在`[20,9]`，BREAKER仍在公开冲锋起点；三者footpoint可独立辨认。
- T3：小体继续在`[22,9]`，馆守Z`[20,9] / 2×2`与BREAKER`[20,11] / 3×3`合法前缘接触；小体不与任一巨体占位重叠。
- 两帧均来自同一自然`Session → Resolver → PerformanceDirector`连续序列；capture driver没有静态注入第二套坐标。

这只签收空间纠偏与消费者单一真值。工程Proxy、标注层与动态相机zoom不构成成片视觉、目标构图、真实遮挡或打击感批准。

## 3. 重新冻结的唯一真值

```text
A_BODY_INTERCEPT Swarm01 ground anchor = [22,9]
status                                  = deflected_alive
grounded                                = true
blocks_route                            = false
display_anchor alias                    = forbidden
```

半开矩形：

- Swarm：`[22,23)×[9,10)`
- 馆守Z：`[20,22)×[9,11)`
- BREAKER接触态：`[20,23)×[11,14)`
- BREAKER post态：`[21,24)×[11,14)`

交集为空；`[22,9]`在32×18网格内且road／rescue_lane均passable。A路old/new冻结mutation字段唯一差异为`swarm_positions.ENEMY_C01_RIFT_SWARM_01`；B路无差异。

80号其余投影、相机、A/B路线、facing、contact socket、recoil、post anchor、T1–T5顺序、T4 side socket、R2 exact读取全部恢复为已签Candidate真值。A/B R1、R2各20次单一hash；B旧签hash精确保持；A第二轮仍为`10步 / heat 68 / margin 1`，B仍为`9步 / heat 88 / margin 0`。

## 4. 恢复的两项并行施工

### A9.1-A6-S｜整屏Scene-First Lookdev

- 恢复81号任务；允许按81号最多4次全屏ImageGen调用开始两张整屏目标制作。
- 必须使用本回执的`Swarm01=[22,9]`，并服从81号冻结的全部演员、对象、轨迹、文案、A/B第一读法及T3/T4/T5边界。
- 交付仍停在制作人内部整屏、50%与100%像素预审，不得直送UA91。

### G2-A.2｜无身份视觉合成器Proxy

- 恢复82号新增实现；83阶段保留的既有G2-A.2文件继续原地施工，不回滚或重建。
- resolver／session／performance director继续只读；消费者必须自然读取`[22,9]`。
- 全程`approved_handoffs=[] / real_art_loaded=0`，不得接81号或任何人物／单位真实像素。

两项并行，但必须分别停在制作人内部视觉门与系统实机帧／序列门；通过后才可派A9.1-A6-D及联合重组。

## 5. 继续Blocked

本回执不开放：

- UA91用户母版裁决；
- A9.1-A6-D可拆资产、A9.1-B运行时组合资产；
- signed exact real-art handoff；
- G2-B 45–75秒真实资产Golden Turn；
- UGT、第二／三轮、完整约4.5分钟Golden Slice；
- 默认入口、save、正式Runtime、Canon或付费批量生成。

后续仍按“整屏目标 → 制作人视觉预审 → 最小可拆资产 → 同消费者重组 → UA91”的Scene-First门推进，不能因机器PASS或文件齐全跳级。
