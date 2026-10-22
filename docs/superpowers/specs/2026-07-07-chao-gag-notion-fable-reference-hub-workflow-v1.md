# Notion-Fable Reference Hub 副编剧工作流 v1

日期：2026-07-07
状态：工作流候选；C01 Reference Hub 测试已完成四话。

## 定位

Notion/Fable 不是新的 canon 源，也不是替代 Codex episode packet 的自动编剧。它在本项目里的定位是“外部副编剧”：只负责把已经准备好的单话资料包写成更顺读、更有场面感的 Reader Synopsis 候选稿。

Codex 仍然负责 canon 查询、pipeline 资料组织、制作拆分、机体和名场面账本、分支变量、图谱索引、最终合并和审稿判断。Fable 写出的内容如果好，只吸收到可读剧情层；不能直接覆盖本地源稿。

## 分工

| 环节 | 负责人 | 产物 | 是否可直接进 canon |
| --- | --- | --- | --- |
| canon / pipeline / 素材抽取 | Codex | 自包含 Episode Capsule | 否，仍需按 canon 流程更新 |
| 可读剧情层初稿 | Notion/Fable 5 | Fable Draft / Reader Synopsis | 否 |
| 审稿与合并 | Codex | Patch 建议、Reader Synopsis 候选、制作拆分保留 | 否 |
| 本地源稿维护 | Codex | episode packet、chapter assembly、ledger、TSV、graph | 是，按本地流程 |

## Notion 结构

推荐在项目父页面下建立：

- `Fable Writer Room Reference Hub v1`：只放短版规则和链接，不放长篇全量 canon。
- `REF01-REF08`：短版参考页，分别承载 canon、pipeline、loop、50问题、机体/IP素材、关系边界、名台词账本、当前章节状态。
- `TEMPLATE Episode Capsule - Fable用`：单话模板。
- `CxxExx Episode Capsule - Reference Hub测试`：每话一页，必须自包含本话必要规则。

Reference Hub 的作用是可追溯，不是让 Fable 每次全量检索。实际运行时，每个 Episode Capsule 必须自己包含足够信息。

## 单话流程

1. Codex 从本地最新 episode packet、canon、pipeline 和素材库抽取本话资料。
2. Codex 在 Notion 新建或更新 `CxxExx Episode Capsule`，写入：
   - 本话目标和上一话状态。
   - 必须保留的 canon / hard gates。
   - 本话机体、非计数锚件、名台词使用状态。
   - 纪存、七海、白鸢等关系和主角动作要求。
   - 燃点、泪点、梗点、PV级演出、下一话债务。
   - 禁止项：不得改 canon、不得改机体名单、不得写 TSV、不得解释系统规则。
3. 在 Notion GUI 的侧边 AI 中选择 Fable 5，用当前页面作为主上下文发起写作。
4. Fable 只写 `## Fable Draft - Reference Hub Test`，并按以下结构输出：
   - 一、剧情流程
   - 二、战斗与玩法
   - 三、机体承载
   - 四、情绪与关系
   - 五、结算债务
   - 六、Fable 自检
5. Codex 用 Notion MCP 抓取页面，确认 Fable Draft 已写入。
6. Codex 按本地门禁审稿，决定吸收、局部改写或退稿。
7. Codex 只把通过的语言和场面吸收到本地 Reader Synopsis 候选；制作拆分、变量、ledger 和 canon 仍以本地 episode packet 为准。

## Fable 提示模板

```text
请只读取当前页面 Capsule 内容，写入当前页末尾。
请只写「## Fable Draft - Reference Hub Test」标题及本话 Reader Synopsis / 可读剧情层。
不要改 canon，不要改机体名单，不要创造变量，不要写 TSV，不要解释系统规则。

请保留输出结构：
一、剧情流程
二、战斗与玩法
三、机体承载
四、情绪与关系
五、结算债务
六、Fable自检

重点检查：
1. 本话真实新增机体和非计数锚件不能混淆。
2. 名台词/名场面不得和前文重复，除非当前页面明确允许。
3. 纪存、七海、白鸢至少有一个可见状态变化或关系动作。
4. 燃点、泪点、梗点、PV级演出必须明确落在剧情里。
5. 结尾必须接下一话债务。
```

## Codex 复核门禁

Fable Draft 通过前必须检查：

- 机体/IP密度：真实首登、复出、非计数锚件分开；盒子、展签、手套、道具不能冒充参战机体。
- 名台词账本：直接短引、错引、原创变奏都要有唯一性和场面必要性。
- 主角熔炉：纪存不能只做记录员；七海不能只给几十秒；白鸢不能只画半格。
- 关系事件：成人关系要有误会、吸引、体谅、牺牲、嫉妒、救场或状态变化；儿童线隔离成人向。
- 燃泪梗与PV演出：不能只在自检里声明，正文必须能看到。
- 制作拆分：Fable 的可读稿不能替代 ADV、探索、SRPG、战斗内事件、舰内日常、结算状态。
- 口径安全：不得让 Fable 新增硬 canon、改机体首次登场、改分支变量或替代图谱更新。

## 可靠性记录

C01 测试表明：

- 自包含 Capsule 可以让 Fable 写出可读性更好的剧情层。
- 不能依赖 Fable 稳定读取大量 `@` 引用。E03 首次尝试因全局搜索 Reference Hub 失败；改成“只读当前页面”后成功。
- 即使提示“不搜索 REF”，Fable 仍可能主动加载 Reference Hub 和 REF 页。E04 成功写入，但消耗明显上升。
- Notion 页面更新是异步的；GUI 显示“正在更新页面”后，需要等待并用 MCP 轮询确认。

因此，后续使用时优先采用“短 Hub + 自包含 Capsule + Codex 抓取审稿”的模式。

## C01 测试结论

| 话数 | Notion 页 | 结果 | 备注 |
| --- | --- | --- | --- |
| C01E01 | `C01E01 Episode Capsule - Reference Hub测试` | PASS | Fable 可读稿写入；闭馆路线和万机馆样本表现更顺读 |
| C01E02 | `C01E02 Episode Capsule - Reference Hub测试` | PASS | 右臂同时作为伤臂、桥梁、武器和证据的表达值得吸收 |
| C01E03 | `C01E03 Episode Capsule - Reference Hub测试` | PASS | 首次全局检索失败；轻量重试成功；“我来组成头部”唯一使用需登记 |
| C01E04 | `C01E04 Episode Capsule - Reference Hub测试` | PASS | Fable 擅长展舰起航巨物感；但会加载 REF，不能直接当生产源稿 |

## 禁止用法

- 不得让 Fable 直接改本地 canon、TSV、graph 或 episode packet。
- 不得把 Fable Draft 当作完整 ELO 运行结果。
- 不得用一个 Fable 页面写完整章节或多话正文。
- 不得让 Reference Hub 变成长篇资料坟场；长资料仍留在本地，Capsule 只抽取本话必需内容。
- 不得因为 Fable 文笔顺就跳过 Codex 门禁。

## 推荐后续用法

后续写单话时，先由 Codex 正常跑 pipeline 生成本地 episode packet，再把“本话可读剧情层所需资料”压缩到 Notion Capsule 交给 Fable。Fable 草稿回来后，Codex 只吸收其中真正增强读感、情绪和场面链的部分，并把所有状态变化回写本地源稿、账本和图谱。
