# Task93 连续非headless玩家链证据纠偏回执

日期：2026-08-20  
任务：`G2_A2_C1_CONTINUOUS_NONHEADLESS_PLAYER_TRACE_CORRECTION`  
状态：Candidate PASS / producer P89 reacceptance pending / `CALL02_ALLOWED=false`

## 输入锁

- 93号：`e16bbe51ff8d078e69cee159ba216d5b4f334b7db31ee0f8298fc948132cf06c`
- 生产看板：`0679b21649a5c2403acdcaa6f267d2cbd11c818d3ad35b1200aca9773001ba7c`
- 接口 1.6.1 动态 gate 同步版：`9bfcbc827c0c65a347d75a76a0e07dcb07382efb299021d75fed80c3969b6534`

接口更新只改变 Task89 returned / Task93 dispatched / P89 blocked 动态 gate，不改变 schema、几何或 copy。

## 新增与改动

- 新增 `g2_a2_c1_continuous_player_trace_driver.gd`：A/B 分别在单一非 headless Scene 中跨 process frames 调用公开 Session API。
- 新增 `validate_g2_a2_c1_continuous_player_trace.py`：从原始数组独立重算，不读取驱动 PASS 布尔值。
- 更新 `g2_a2_c1_scene_sequence_test.gd`：旧 receipt 降级为 Director/视觉回归，不再伪装完整玩家链。
- 更新专用 runner：三项当前输入联锁、A/B 非 headless trace、外部验证、12帧只读、源码前后 fingerprint 与最终 log mtime 门。
- 新增 A/B trace、validation log 与 supersession readback；更新06及交付哈希。

resolver、session、director、compositor adapter/Scene、玩法 profile、地图 contract、actual capture driver、12帧及 manifest 均未修改。

## 原始数组重算结论

| 项 | A | B |
|---|---:|---:|
| 总时长 | 46514.334ms | 46536.997ms |
| hold时长 | 702.700ms | 705.814ms |
| hold process frames | 111 | 113 |
| commit count | 1 | 1 |
| 最大相邻动作间隔 | 4003.252ms | 4005.263ms |

状态序列均为：

`PUBLIC_SITUATION → EDITABLE_DRAFT → COMMIT_SUMMARY → EDITABLE_DRAFT → COMMIT_SUMMARY → JOINT_RESOLUTION → ROUND_RESULT`

事件序列均为：

`GS-R1-E1-VEHICLE → GS-R1-E2-SWARM → GS-R1-E3-CONTACT → GS-R1-E4-CITY-GUN → GS-R1-E5-ROAD-RED`

外部 validator 证明五事件全部晚于唯一 commit；公开动作分布在不同 frame，最大间隔小于6秒；hold 位于650–900ms且不少于10帧；主钟/帧源分别为 `Time.get_ticks_usec` / `Engine.get_process_frames`；Scene/Session/Director instance 全程稳定。

## 非回归与隔离

- B R1=`c3b307b9698d645598594cb6674c86779a13420b9934cf562f379d112d1f41fa`
- B R2=`f09de07bb6b0b32c1a44e7ca1d5e24a6cbc3bac498010cb92490b781bd6480a6`
- 两者各20次唯一。
- actual-frame manifest SHA=`0b7ef06c11bdf59642bdd9c81364eca0f72963d064b9f1a6ae35c104ac2f06ab`，未重抓、未改图。
- `fixture_load_count=0 / direct_draft_mutation=false / direct_phase_injection=false / preview_execute_same_resolver=true`。
- `approved_handoffs=[] / real_art_loaded=0 / default=false / save=false / Runtime=false / Canon=false / G2-B=false`。

## 最终门

唯一全回归入口为 [99-final-regression.log](logs/99-final-regression.log)。其 mtime 严格晚于最终源码、测试与 runner；运行前后源码 fingerprint 均为 `3655df85c99219594292cccafaf670ae6e69ba91471f6ec9a274f7215af170e3`。

Task93 仅支持将 Task89 重新送入 producer P89 reacceptance。它不证明真人节奏、物理手柄回放、FUN 或制作人签收；`CALL02_ALLOWED=false`。
