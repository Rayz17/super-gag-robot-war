# C01E02｜G2-A.1-R2C-C1输入与范围回执

日期：2026-08-20  
执行状态：`R2C_C1_IMPLEMENTED_AND_EVIDENCED / WAITING_PRODUCER_REACCEPTANCE`

## 权威输入

| 输入 | SHA-256 |
|---|---|
| `83-c01e02-r2c-c1-primary-swarm-ground-occupancy-correction-objective.md` | `f6ba405a809969f6013ab2f8c5b5405395866583ad4e405f35cb98af06fe7173` |
| `80-c01e02-r2c-producer-exact-geometry-acceptance-and-parallel-visual-dispatch.md` | `f83cbaac5201a978a9e5f2c7b3922b828e3c1772079e255ddf1ac323fed103f8` |
| `c01e02-tactical-visual-interface-v1.json` | `db83cd116431bdb32ae0ca52b4c6994bd4d3eb233f67e2022d3eb76974606a50` |
| 旧R2C `receipts/contact-staging.json`（只读对照） | `199b098524cb4cd7cfcd637d81ba0a2ee2509332d327867f8399178029af1d8c` |

已按`chao-gag-canon`复核Hard／Working／Candidate／History与V35状态。C01E02继续是隔离Candidate切片；本次不修改Canon、Runtime、默认入口或save语义。

## 唯一实现裁决

```text
strategy                 = A_BODY_INTERCEPT
old History anchor       = [21,9]
sole Candidate anchor    = [22,9]
footprint                = [1,1]
status                   = deflected_alive
effective grounded       = true
effective blocks_route   = false
```

resolver的A路`swarm_positions`是唯一写入点。entity anchor由该字段回写；PerformanceDirector继续只读`world_result.entities`生成T2 track；capture overlay只读实际rendered actor cell。没有display-only偏移或第二套终点。

## 写域

仅写入：

- `golden_slice_resolver.gd`中的单一A路主小体坐标；
- C1专用ground-occupancy test、occupancy overlay、capture driver与runner；
- 新证据目录`main-g2-a1-r2c-c1/**`。

保持只读：正式profile、session、route planner、PerformanceDirector、tactical geometry/view、R1音频消费者、旧`main-g2-a1-r2c/**`、G2-A.2、默认入口、save、Runtime、Canon、Reader与美术目录。

## 隔离基线

- 旧`main-g2-a1-r2c/**`共41文件；排序逐文件SHA流的整树摘要在执行前后均为`e32bcd99674f214a8e63102a069f97b59b1ef338c5df128251635291cad98d1e`。
- 暂停中的G2-A.2 `visual_compositor_profile.json`保持`8efca88861a12686b2072f1b580b1f745c2e5d7b0215a361cc037937680a841c`。
- 未执行旧`test_c01e02_m3_golden_slice_g2_a1_r2c.sh`；所有新日志、回执与截图仅落入C1证据目录。
- 未执行`git add`、`git commit`或`git clean`。
