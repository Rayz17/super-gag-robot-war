# C01E02｜R2C-C1 Actual Frame视觉复核

复核结论：两张图均为1280×720 Godot root viewport在同一次自然Session／Resolver／PerformanceDirector连续序列中的实际帧；主小体、馆守Z与BREAKER的占地轮廓及footpoint可以独立辨认，`[22,9]`没有通过视觉offset伪造。

| 帧 | 时点／phase | SHA-256 | 视觉读回 |
|---|---|---|---|
| `C01E02_G2A1_R2C_C1_A_T2_SWARM_DEFLECT_ACTUAL_1280x720.png` | `GS-R1-E2-SWARM / environment_aftermath / 1920ms` | `7a04670b113e0db25be2eb91582013ac34ab5ddffa8d9803b3b7ef0da522287c` | 青色1×1主小体在`[22,9]`；黄色2×2馆守Z在`[20,9]`；红色3×3 BREAKER仍在公开路线起点`[20,13]`。三者有独立footpoint标记。 |
| `C01E02_G2A1_R2C_C1_A_T3_CONTACT_ACTUAL_1280x720.png` | `GS-R1-E3-CONTACT / contact_hit_stop / 2585ms` | `8b504ee85752dfdd55c1ea6c654df2e870ef10b0aa4689e2102ae9221164b563` | 主小体继续保持`[22,9]`；馆守Z为`[20,9] / 2×2 / south`；BREAKER为`[20,11] / 3×3 / north`，前缘相接而不重叠。 |

## 视觉检查要点

- 顶部读回条明确显示`resolver world = entity anchor = T2 final_cell = overlay = [22,9]`。
- 青／黄／红三组菱形占地使用不同颜色，footpoint使用独立圆环与横线；小体不再落入馆守Z的右上占格。
- T3可直接读到半开矩形：Swarm`[22,23)×[9,10)`、馆守Z`[20,22)×[9,11)`、BREAKER`[20,23)×[11,14)`；交集为空。
- Manifest回读的rendered actor cell与屏幕footpoint来自运行中`tactical_world_view.performance_receipt()`，不是capture driver手填显示坐标。
- 两帧像素采样分别得到76／78种颜色，均有1032个采样点为不透明；不是空帧或离线合成。

## 证据边界

这些帧证明本次地面占位纠偏、消费者单一真值与实际viewport呈现。它们仍是`real_art_loaded=0`的工程Proxy，不证明真实美术、成片遮挡、完整45–75秒演出、打击感、用户体验或G2-A.2完成。机器PASS与本次程序侧视觉复核都不能替代制作人复签。

当前停止门：`WAITING_PRODUCER_REACCEPTANCE`。
