# A34 State 02/03 独立视觉门 RETURN 回执

> Date: 2026-08-25  
> Status: `PARTIAL_PASS_THEN_HARD_GATE_STOP / Candidate / user=false / runtime=false / canon=false`

## 返修边界

- State 00 机制常态与 State 01 吸纳冲击态原样保留，本轮没有改动其任何像素。
- 初版 State 02 因“长直青色透明段”容易读成炮筒，已移入 `history-rejected-a34-initial/`。
- 初版 State 03 因拳体周围整圈压力光环容易读成护盾或射击，已移入 `history-rejected-a34-initial/`。
- 按硬门每态只使用一次 targeted edit，随机 reroll 为 `0`；State 03 R1 失败后立即停止，没有用第二张图挽救。

## State 02 R1 — PASS_FOR_USER_REVIEW

当前候选：`delivery/BRAVE_FIST_A34_STATE02_R1_PHYSICAL_COMPRESSION_LOCKED_USER_REVIEW_CANDIDATE.png`  
SHA-256：`51093c5f8bdbac527233a033a829368781efd47f50017d8843ee9b2d6a03399a`

- 双前臂相对 State 01 出现明确的物理缩短；嵌套套筒在肘侧堆叠，双拳靠近肘侧。
- 双侧导轨缩短并被橙金护甲/锁扣閉合，没有一长一短或单臂特化。
- 储压显示改成被不透明甲肋分隔的短青色窗，长直透明管已消失；没有炮口、枪管、发射器或射线。
- 拳面仍是封闭四区钝性承击甲，双拳与双前臂保持连接。
- 双臂虎语法仍只是前肢式甲片起伏、肌肉节奏与少量宽槽，没有直白虎纹、兽爪或变形暗示。

## State 03 R1 — HARD_GATE_FAIL_STOP

失败证据：`return-failures/BRAVE_FIST_A34_STATE03_R1_LEFT_CONNECTION_OCCLUDED_HARD_GATE_FAIL.png`  
SHA-256：`198fb16194bd028239a159794b436040acffc9c270defbe6b49236d3e2cf2b6a`

成立项：

- 两只闭合重拳都实际接触同一块装甲受力板；受力板在两个接触点产生凹陷、短裂纹和局部接触能量。
- 压力效果没有再环绕拳体，也没有光束、护盾球、环状射击或越过目标板的能量。
- 右拳、右前臂、短储压窗与接触点的连续关系清楚。

失败项：

- 目标板完全遮挡了左拳后的左前臂和导轨连接；虽然结构上可推断其仍相连，但画面首读不能证明，仍有“左拳独立悬在板上”的歧义。
- 这违反“双拳都必须在同一帧中可见地连接双前臂”的硬门，因此不得进入 delivery，不得用于新四态总览。

## 当前可用与缺口

- 当前仅 State 00、State 01 与 State 02 R1 位于 `delivery/`。
- State 03 仍缺失；没有重做四态总览，避免让失败图或初版拒绝图混入正向审核。
- 本轮不产出 Sprite，不绑定 Godot / Runtime，不晋级 Canon。

