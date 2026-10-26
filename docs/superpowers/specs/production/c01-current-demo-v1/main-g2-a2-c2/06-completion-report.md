# C01E02 G2-A2-C2 / Task96 完成回执

日期：2026-08-20  
任务：`G2_A2_C2_SCREEN_INPUT_TIMELINE_AND_EMBODIED_CONSEQUENCE`  
最终状态：**Candidate proxy实现、actual frames、回归、性能与交付证据已收口；停在P98制作人预审门，`FUN_NOT_PROVEN`。**

## 已完成

1. 新建专用非默认C2 Scene，A键鼠与B手柄等价`InputEvent`实际进入`Control._input`，再由输入适配调用Session公开API；driver不直调Session。
2. PUBLIC从空草稿开始；A路由InputEvent真实写入一条`route_family_endpoint_mismatch`失败草稿，再经Z/undo和重新输入修复。被入口拒绝的落点仅保留为额外fail-closed证据，没有冒充失败草稿修复。
3. A/B责任结果逐字段从Resolver公开preview与只读R2 Resolver投影动态形成；C/Back真实展开另一路同层级收益/代价，且current/other family与token不同、当前draft signature及selected strategy不变。
4. preview与PerformanceDirector `active_plan`各自独立构造有序`event_sequence`并由外部validator重算同token；相邻事件交换负例必得不同hash。两路自然播放T1–T5，执行分别为13,334.692ms / 13,322.257ms，逻辑timeslice与world result未改。
5. 地图内已呈现应急车通过、馆守Z自主挡小体、A两格前缘承力/路面+设施受损、B护线转身/一格错位/高热，以及T4/T5后果。
6. 城市炮许可已fail-closed：PUBLIC/EDIT/SUMMARY/A:T3.00/B:T3.25均false，首次true只在T4 motion；15张交付actual frames均无提前物理炮击标记。Resolver逻辑真值未篡改。
7. 15张1280×720非headless actual frames已最终重投并逐张复核；新增真实失败草稿、A键盘比较、B控制器比较三帧，主体分类、意图图例、SUMMARY CTA、A/B CONTACT焦点与中文产品copy均成立。
8. C2 Product UI只收到`jicun_line / objective / timeline / top_threats`公共固定copy白名单；`strategy_a / strategy_b`及任何静态责任结果字段不可达，本次copy边界修复没有再修改旧C1 adapter。
9. 非headless 120+600帧性能为p50=6.388ms、p95=8.090ms、max=11.459ms，性能门PASS；采样窗截图/IO/日志写入均为0。
10. B旧R1/R2 exact hash保持`c3b307…` / `f09de0…`，Full/Skip、R2/R3、R2C几何与Canon回归全绿。
11. R1音频语义断言独立PASS；macOS Godot退出阶段的纯清理抖动另以`attempts=2 / consecutive_clean=2 / semantic_errors=0`连续干净退出证据收口，没有把重试冒充语义PASS。
12. Task89/93证据保持只读；Call02失败后的真实像素未接入，Task99/C3仍blocked。

## 关键交付SHA

| 产物 | SHA-256 |
|---|---|
| `99-final-regression.log` | `0a51d5bc29a8de79a698b13649574976189ff259eb9016a98f0e8efcaa522134` |
| `screen-input-contract.json` | `2cb97b025c8c36258229d65c34788935585147d14da7d3058c629da68b77fdd0` |
| `actual-input-frame-manifest.json` | `a1ba2c37b592dfbc983dd6ffa1944098582eabc6edaab2875474e3b30ea08a47` |
| `raw-screen-trace-validation.json` | `be9538cff8e1a1cf0d0fcb712b4869152d997ad6a49d84f59f7b7827dad66bed` |
| `timeline-semantic-nonregression.json` | `936263feb8c5540f19fe86fb2946d0c1527d3a48b1dfbc7c987c571c694cf7f9` |
| `performance-600-frames.json` | `83fde14e30ee5452c19ee1f4f007105c5be0f2d39bb427519dec85894449b2d8` |
| C2专用Scene | `670541b0d1db934eb084554b0af95bb7693a5a1a8b5ef87d99061668408384c8` |
| fail-closed visual adapter | `1351c8a27dd154debb393b64ded873d4c60b999036cb27f6233e5cc8e00e150f` |
| C2输入适配 | `7a1607955935ef18a48823ecbe4bbd60352c18199f376086d330ebde8a05f670` |
| C2 Product UI | `f5a6534e14e5e65c67374478632debf7d6ec9464faafd269bf101d38528ac33e` |
| C2 Scene脚本 | `0c5703885e05a02b469f12f97cf6b3c86c707fae82430a7381999be83a588b0c` |
| 外部trace validator | `fad63a8f2dabfbfd7d1d1af7818428c1d44d5519f7a339da51efb9b72055ed4e` |
| C2 runner | `6c5f894472eb99c91d009fc957951daf94c3be2e8bf56d556e8e9aadfcaf2346` |

全量文件哈希见[delivery-hashes.sha256](delivery-hashes.sha256)。

## 证据入口

- [屏幕输入与动态责任解](02-screen-input-and-live-draft-proof.md)
- [共同时间线与地图内因果](03-shared-timeline-and-map-consequence-proof.md)
- [15张actual frame视觉复核](04-actual-frame-visual-review.md)
- [回归、性能与隔离](05-regression-performance-and-isolation-proof.md)
- [actual-input-frame-manifest.json](receipts/actual-input-frame-manifest.json)
- [raw-screen-trace-validation.json](receipts/raw-screen-trace-validation.json)
- [performance-600-frames.json](receipts/performance-600-frames.json)
- [99-final-regression.log](logs/99-final-regression.log)

## 停止门

本交付只支持：`SCREEN_INPUT_PREFLIGHT_SUPPORTED / LIVE_DRAFT_PREFLIGHT_SUPPORTED / MAP_CONSEQUENCE_PREFLIGHT_SUPPORTED / FUN_NOT_PROVEN`。

已停在P98制作人系统实机帧、屏幕操作与可玩性预审门；不自行开放Task99/C3、Call03、UA91、G2-B、Default Entry、save、Runtime或Canon，也不声称FUN PASS。
