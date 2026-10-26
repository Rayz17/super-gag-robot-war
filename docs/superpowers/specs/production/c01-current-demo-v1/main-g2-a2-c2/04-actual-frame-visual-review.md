# G2-A2-C2 actual frame 视觉复核

## 证据范围

专用非默认Scene以macOS非headless OpenGL环境重抓15张1280×720 actual frames，完整manifest见[actual-input-frame-manifest.json](receipts/actual-input-frame-manifest.json)。`required_frame_count=15 / fixture_load_count=0 / approved_handoffs=[] / real_art_loaded=0 / call02_pixels_loaded=false`。

| ID | 帧 | 主要视觉检查 |
|---|---|---|
| 00 | [PUBLIC空草稿](captures/00_PUBLIC_EMPTY.png) | 对象分类、三意图绑定、无预填结果 |
| 01 | [A未闭合](captures/01_INVALID_INCOMPLETE_A.png) | 缺项可理解、可修正 |
| 01B | [A路线族失败草稿](captures/01B_A_INVALID_ROUTE_DRAFT.png) | 已写入草稿但未到承接位置；明确提示撤销重画 |
| 02 | [A动态闭合](captures/02_A_DYNAMIC_CLOSED.png) | 正面卡位收益/代价随路线展开 |
| 02C | [A主动比较B](captures/02C_A_COMPARE_OTHER.png) | C键展开另一路同层级收益/代价，当前草稿不变 |
| 03 | [A提交前摘要](captures/03_A_COMMIT_SUMMARY.png) | 明确可返回修改与长按0.7秒CTA |
| 04 | [A return/undo](captures/04_A_RETURN_UNDO.png) | 生命周期与撤销状态可见 |
| 05 | [A CONTACT](captures/05_A_CONTACT.png) | 当前方案、T3.00、两格前缘承力；未提前炮击 |
| 06 | [A T5后果](captures/06_A_T5_CONSEQUENCE.png) | 路面损伤、设施受损、机体热/蓄能在地图内可见 |
| 07 | [B动态闭合](captures/07_B_DYNAMIC_CLOSED.png) | 护撤离线收益/高热代价随路线展开 |
| 07C | [B主动比较A](captures/07C_B_COMPARE_OTHER.png) | Back展开另一路同层级收益/代价，当前策略不变 |
| 08 | [B提交前摘要](captures/08_B_COMMIT_SUMMARY.png) | 与EDIT态明确区分，可返回/长按可见 |
| 09 | [B return/undo](captures/09_B_RETURN_UNDO.png) | 修改链可见 |
| 10 | [B CONTACT](captures/10_B_CONTACT.png) | 当前方案、T3.25、转身+一格错位+热排出 |
| 11 | [B T5后果](captures/11_B_T5_CONSEQUENCE.png) | 路损较低、设施保全、高热/蓄能在地图内可见 |

## 人工复核结果

最终15张已逐张打开复核；其中新增失败草稿、A比较、B比较及最终A/B CONTACT、A/B T5后果帧再次实际打开确认。PUBLIC中应急车、三只小体、东门、警戒设施、重盾以不同中性轮廓与就地中文标识区分；三条意图与顶部同色/同形图例对应。SUMMARY状态与操作CTA明确；A/B CONTACT均只突出当前方案与对应T3.00/T3.25，已发生的车/小体轨迹降级，BREAKER冲线与承力姿势为主焦点。

失败草稿帧把“已写入但不可提交”的原因和撤销重画动作同时放在产品画面；两张比较帧把current/other的热量、设施、路损、接触时点/前缘、第二轮热量/余量并列到同一层级，同时明确另一路只供比较、不替换当前草稿。所有15帧的C2 copy边界均只有四个公共固定copy键，静态A/B责任结果不可达。

产品帧不再出现“生产”、“回读”、“占位”等内部词；本批仍是无身份Proxy，不代表真实美术或最终Lookdev通过。
