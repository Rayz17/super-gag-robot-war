# BREAKER 多朝向审计与精确消费合同

> 状态：`CURRENT_PRODUCTION_PLAN / PRESENTATION_ONLY / FAIL_CLOSED`  
> Camera：`CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE`  
> 边界：不生成美术，不改 World/Resolver/Session，不迁移 Runtime/Default/Canon。

## 已确认的问题

此前只有一张 north PNG，却连 R2/R3 的 west 互动也由 `red_beam/north`、`hit_recoil/north` 承担。这样即使 world state 的 `facing=north` 没写错，实际演出仍会出现“倒着发射、背对接触、受击位移方向被当成朝向”的画面。R1 实际就是 north 的 `charge/contact` 可继续使用显式 north exact 行；这不是跨朝向 fallback。

现在拆为两层：

- `world facing`：Resolver/Session 的战术真值，本次不改。
- `presentation visual facing`：由当前事件的位移、攻击目标或受击来源计算，只用于请求 `subject + action + facing` exact key。

`visual_facing` 请求 E/S/W 而 exact 图不存在时，地图必须显示 marker，并写出 `missing_exact_breaker_facing_pose`；禁止拿 north 图代替，禁止镜像、旋转、跨朝向和上一 pose 继承。

## E02 逐事件审计

| 事件 | BREAKER 位移/力向量 | 攻击或受击来源 | 演出朝向 | exact action | 判定 |
|---|---|---|---|---|---|
| R1 E1 VEHICLE | `[0,0]` | 无 | N（world 北冲预备） | `idle/north` | 本事件不覆盖 |
| R1 E2 SWARM | `[0,0]` | 无 | N（world 北冲预备） | `idle/north` | 本事件不覆盖 |
| R1 E3 CONTACT | 主冲 `[0,-2]`；接触后偏转另算 | 馆守 Z 在北 | N | `charge/north` → `contact/north` | 唯一 |
| R1 E4 CITY-GUN | `[0,0]` | 城市炮从东/东北打侧甲；正面仍与馆守 Z 承力 | N | 后续可补 `side_hit/north` | 不因侧击突然转身 |
| R1 E5 ROAD-RED | `[0,0]` | self/道路；仍在北向接触轴 | N | 后续可补 `red_charge/north` | 明确保留北轴 |
| R2 E1 TAKE-SHIELD | `[0,0]` | 下一发射线由 post anchor 指向西侧挡击位 | W | 后续可补 `red_charge/west` | R2 合同显式预瞄，不读上一 pose |
| R2 E2 RED-BLOCK | A `[-4,-1]`；B `[-4,0]` | BREAKER → 馆守 Z/盾 | **W** | **`red_beam/west`** | 唯一 |
| R2 E3 FINAL-VEHICLE | `[0,0]` | 无新来源 | W | `idle/west` | R2 合同显式保持攻击轴 |
| R2 E4 EAST-GATE | `[0,0]` | 无新来源 | W | `idle/west` | R2 合同显式保持攻击轴 |
| R2 E5 BALANCE | `[0,0]` | self recovery | W | 后续可补 `recover_balance/west` | R2 合同显式保持攻击轴 |
| R3 E1 SIDE-PRESS | 语义 `[0,0]` | 馆守 Z 位于西侧合法侧压位 | W | 后续可补 `brace/west` | 唯一 |
| R3 E2 WINDOW | 语义 `[0,0]` | 西侧受力轴仍锁定 | W | 后续可补 `recover_balance/west` | 依当前玩家 Resolver 合法侧压位锁轴，不受通用轨道提前南移污染 |
| R3 E3 SHIELD-BASH | 接触开始，位移在下一拍结算 | 馆守 Z 从西侧横拍 | **W** | **`hit_recoil/west`** | 唯一 |
| R3 E4 KNOCKDOWN | **位移 `[0,+2]` = S** | 受击来源仍是西侧馆守 Z | **W** | **`hit_recoil/west`** | 面向 W、位移 S，严禁混用 |
| R3 E5 P1-HOOK | `[0,0]` | self recovery | W | 后续可补 `recover_balance/west` | R3 合同显式保持受击轴 |

附带发现：现有 E02 `PerformanceDirector` generic track 会把 R3 最终 `[0,+2]` 位移重复投到多个包含 BREAKER 的事件，并统一携带 final world `north`。这不是事件语义真相；本次只在精灵选择层纠正 facing，没有改动作时序或玩法，generic track 的事件位移拆分应另立表现修复项。

## E03 逐事件审计

E03 当前 controller 只发 semantic placeholder；BREAKER 没有 plan，world anchor 不动。下面的方向来自 Reader/profile 的攻击关系，不从 `[0,0]` world 位移伪造。

| 事件 | BREAKER world Δ | 叙事力向量/来源 | 演出朝向 | action | 结论 |
|---|---|---|---|---|---|
| R4 E1 BRAVE-FIST-ENTRY | `[0,0]` | 勇拳入场并先承受冲击，但未给 BREAKER 接触点/轨迹 | — | `attack_windup` | semantic gap，不猜 |
| R4 E2 SHIELD-CRACK | `[0,0]` | BREAKER 明确继续向北挤压馆守 Z，叙事力向量 `[0,-1]` | N | `contact/north` | 唯一 |
| R4 E3 FIRST-MISALIGNMENT | `[0,0]` | 勇拳擦身，未给接触边/轨迹 | — | `brace` | semantic gap，不猜 |
| R4 E4 FIRST-PINCER | `[0,0]` | 馆守 Z north、勇拳 south 同时夹击 | — | 专用 `pincer_recoil` | 对向双源，不得硬塞 N/S |
| R5 E1 DRILL-TELL | `[0,0]` | 向地层下钻 | — | `drill_tell` | 垂直轴不属于 N/E/S/W |
| R5 E2 DRILL-BLOCK | `[0,0]` | 馆守 Z south、勇拳 north 对向挤压 | — | 专用 `drill_blocked` | 对向双源 |
| R5 E3 RED-SLIT | `[0,0]` | self 弱点开合 | — | `red_slit_open` | 无方向状态 |
| R5 E4 FOCUSED-FIRE | `[0,0]` | 两机南北 + 城市炮第三源 | — | 专用 `focused_hit` | 多源 |
| R6 E1 AUTONOMOUS-OVERLOAD | `[0,0]` | 馆守 Z 延续南侧位置发射 | toward 当前 GZ（预期 S） | catch anticipation | 运行时按实际 source 求向 |
| R6 E2 FIST-CAUGHT | `[0,0]` | 飞拳来自当前 GZ 位置 | toward 当前 GZ（预期 **S**） | `fist_caught/south` | 唯一 |
| R6 E3 BRAVE-FIST-RELAY | `[0,0]` | 手里是南侧 GZ 的拳，但直接冲击源是北侧勇拳 | — | `fist_caught` | 未指定 pose owner/socket，semantic gap |
| R6 E4 SHELL-BREAK | `[0,0]` | 南北双源贯穿破壳 | — | `ground_shell_broken` | 交给专用破壳投影 |
| R6 E5 CORE-PULSE | `[0,0]` | 飞行核心离地显形 | N/A | `flight_core` | 切换形态合同，不是地面 cardinal |

## 折叠后的唯一美术输出计划

### Wave A：四向中立母版

- `idle/north`：现有唯一可加载行，继续锁路径与 SHA。
- `idle/east`
- `idle/south`
- `idle/west`

后三张必须从同一已接受 BREAKER 设计与 Camera V2 注册规范独立绘制；不得由 north 镜像或旋转。它们是 E02/E03 共享母版，不因事件重复出图。

### Wave B：实际事件动作

- `charge/north`（现有 north 地图体的显式 exact 行已可消费）
- `contact/north`（现有 north 地图体的显式 exact 行已可消费）
- `red_beam/west`
- `hit_recoil/west`
- `fist_caught/south`（E03 R6；按 source-facing 合同）

后续只有在 presentation 语义补齐后才生产 `side_hit`、`red_charge`、`recover_balance`、`pincer_recoil`、`drill_blocked`、`focused_hit` 等，不把“多源/垂直/无向”的缺口膨胀成假四向清单。

## 当前停点

当前唯一 BREAKER 图源仍是 north 地图体，只对实际 north 请求的 `idle/charge/contact` 显式 exact 行合法加载。R2 `red_beam/west`、R3 `hit_recoil/west`、R6 `fist_caught/south` 会 fail closed 到 marker；receipt 明确记录缺失 exact pose。等美术资产 session 交回相应 PNG 后，只需新增 exact binding 并跑实际地图帧签收，不需要改 world truth 或玩法 Resolver。
