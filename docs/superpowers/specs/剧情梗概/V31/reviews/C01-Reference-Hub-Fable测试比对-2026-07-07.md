# C01 Reference Hub-Fable 测试与 Codex V31 比对

日期：2026-07-07
范围：C01E01-C01E04，测试 Notion Reference Hub + Fable 5 作为外部 Reader Synopsis 副编剧的可行性。

## 测试对象

Notion 父页面：

- `超GAG机器人大战企划`：`https://app.notion.com/p/396701074b6880c9acf6c308e54db0af`
- `Fable Writer Room Reference Hub v1`：`https://app.notion.com/p/396701074b688107b898d55316c96901`

本地 Codex 源稿：

- `docs/superpowers/specs/剧情梗概/V31/episodes/C01E01-今日闭馆后馆名被冻结.md`
- `docs/superpowers/specs/剧情梗概/V31/episodes/C01E02-馆守Z手臂成为地图.md`
- `docs/superpowers/specs/剧情梗概/V31/episodes/C01E03-勇气审批角临时许可.md`
- `docs/superpowers/specs/剧情梗概/V31/episodes/C01E04-万机馆临时展舰起航.md`

## 总结论

Reference Hub + 自包含 Episode Capsule 的方案可用，但只能作为“可读剧情层副编剧”。

Fable 的优势是顺读、连续场面、人物情绪动作和高潮气氛；Codex V31 的优势是制作拆分、机体/变量/ledger、canon 边界和可交付给玩法/美术/程序的结构。后续不应二选一，而应让 Fable 提供 Reader Synopsis 候选，Codex 负责审稿和合并。

## 运行状态

| 话数 | Notion 页 | 结果 | 关键观察 |
| --- | --- | --- | --- |
| C01E01 | `39670107-4b68-8169-84b8-e8d6457de2d9` | PASS | Fable 写入 `## Fable Draft - Reference Hub Test`；15个万机馆样本、馆守Z半跪、封存改名贴片机、冷却针车均能读出开局承诺 |
| C01E02 | `39670107-4b68-81ba-a5e6-c09c028fb3b7` | PASS | 右臂作为伤臂、桥梁、武器和证据的四重身份写得清楚；七海条款例外和兜灯硬停机权更有戏 |
| C01E03 | `39670107-4b68-8116-8842-e14ff499c946` | PASS | 首次全局搜索 REF 失败；改为只读当前页后成功；`我来组成头部`作为唯一直接短引出现，需要进入名台词账本 |
| C01E04 | `39670107-4b68-81b0-82eb-c40f18777456` | PASS | Fable 仍主动加载 Reference Hub 和 REF 页，消耗较高但成功写入；展舰起航的巨物感、B1泊位/外部锁泊逻辑和纪存放弃全保存捷径值得吸收 |

## 与旧比对报告的差异

旧报告 `C01-Notion-Fable-vs-Codex-原稿比对-2026-07-07.md` 记录过 E03/E04 当时未能由 Fable 生成，局部采用 Codex fallback。本次 Reference Hub 测试已经补齐：E03 和 E04 均由 Notion GUI / Fable 生成并经 MCP 抓取确认。

旧报告中“Fable 适合 Reader Synopsis，Codex 适合生产源稿”的判断仍成立，但 E03/E04 的状态需要以本报告为准。

## 每话比对

### C01E01

Fable 版本更像第一眼能抓住玩家的开场：闭馆路线不只是信息展示，而是把“万机馆真的很多机器人文化”做成可阅读的移动镜头。七海实名冻结、纪存公开清单、馆守Z仍在服役的冲突也更容易读懂。

Codex V31 源稿仍更完整：样本表、制作拆分、机体首登和变量边界更清楚。合并时建议吸收 Fable 的闭馆路线顺读段和纪存/七海责任交锋，但保留 V31 的样本表、Production Split 和 ledger。

注意事项：场景小物件不要引入旧台本中“茶杯位置”等已被指出的矛盾；闭馆路线要继续保持大馆感，而不是只剩几件展示样品。

### C01E02

Fable 版本最大的增量是把馆守Z右臂写成四重身份：伤臂、桥梁、武器、证据。这个处理能同时服务剧情、战斗、美术和后续责任线，比单纯“手臂成为地图”更有记忆点。

Codex V31 源稿仍保留更多分支变量、敌方单位、战斗目标和制作拆分。合并时建议吸收右臂四重身份、七海“流程内例外”的危险感、兜灯硬停机权的戏剧表达；不要丢掉原稿里的 branch variables 和生产层字段。

### C01E03

Fable 版本能把勇气审批角写成可读的关系场面：小满喊出 `我来组成头部`，但责任不落到孩子身上；社勇王盒子仍然只是非计数锚件；责任签名矩阵、七海待审许可和豪司远程越权都保留了戏。

Codex V31 源稿本身已经较强，Fable 更像一次语言和顺读整理。合并时建议作为 Reader Synopsis 候选吸收，但必须记录名台词唯一使用，不允许后续普通话数重复消费。

### C01E04

Fable 版本补强了移动展舰的母舰起航感：陆衡第一句追问右肩许可、万机馆多层身体、七海把它定义为移动风险源但留下消防锁复核窗口、纪存拒绝 0号/B2 全保存捷径、B1泊位和外部锁泊解释机体存储逻辑。这些都比单纯“战舰化”更有巨物感和取舍感。

Codex V31 源稿仍更适合制作：回合触发、SRPG胜败条件、结算变量、后续 C02 状态和 graph/canon 对齐更完整。合并时建议吸收 Fable 的起航镜头和情绪余味，但保留本地制作拆分。

## 工作流问题

1. Fable 不能稳定遵守“不搜索 REF”。E04 明确出现主动加载 Reference Hub 的情况。
2. 长 REF 会造成高消耗和失败风险。E03 首次失败正是因为全局搜索结果过多。
3. Fable 输出标题不一定完全按要求。E03 使用了 `# Fable Draft - C01E03...`，仍需 Codex 抓取判断内容是否可用。
4. Fable 不负责生产账本。它会压缩变量、战斗、机体层级和制作拆分，所以不能替代本地 episode packet。

## 结论与下一步

后续可采用以下稳定流程：

1. Codex 按本地 pipeline 写或修单话 episode packet。
2. Codex 把本话必要资料压成自包含 Notion Capsule。
3. Fable 只写 Reader Synopsis 候选。
4. Codex 抓取 Fable Draft，按机体、名台词、主角熔炉、关系、燃泪梗、PV演出、制作拆分、canon 边界审稿。
5. 只吸收通过的语言和场面，不直接覆盖本地源稿。

本次 C01 四话测试通过，说明 Notion/Fable 可以成为“读感增强器”。但正式全剧 ELO 仍必须以本地逐话 packet、chapter assembly、reviews、ledgers 和 validator 为准。
