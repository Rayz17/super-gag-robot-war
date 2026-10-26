# 超GAG机器人大战：故事、玩法、设定与美术评审资料

2026-10-26外部评审资料补齐版。供外部模型结合故事、设定、IP与玩法审查设计。**美术只提供设计类原图，不提供UI/UE、运行截图或三维资产。**

**请先读[总目录](review/00-总目录.md)。** 故事阅读顺序见[01号指南](review/01-阅读指南与当前资料.md)，完整美术和源文件见[资料库](review/library/README.md)。原文里的“当前”“通过”可能只指当时版本，不能按文件名或出现次数判断权威。

| 想做什么 | 入口 |
| --- | --- |
| 了解评审范围、先读哪些故事 | [阅读指南与当前资料](review/01-阅读指南与当前资料.md) |
| 直接交给外部模型开始评审 | [外部评审提示词](review/02-外部评审提示词.md) |
| 避开版本混用、旧稿回流和状态误读 | [版本分歧与待核问题](review/03-版本分歧与待核问题.md) |
| 实际查看当前画风、人物与机体设计 | [美术评审入口](review/04-美术风格与已定资产.md)、[分主体图册](review/art/README.md) |
| 查看134项设计对象、相关候选/历史修订与补充设计稿 | [设计美术资料库](review/library/README.md)、[实际覆盖与排除说明](review/05-全量资产与设定覆盖说明.md) |
| 按领域查完整设定 | [设定分类入口](review/library/SETTINGS.md) |
| 查三维与其他未传项 | [范围及具体排除说明](review/05-全量资产与设定覆盖说明.md) |
| 查某份原文是否完整同步 | [源文件清单与SHA-256](review/SOURCE-MANIFEST.tsv) |
| 查同步范围、排除项与验证 | [快照说明](review/SNAPSHOT.md)、[排除清单](review/EXCLUDED-FILES.tsv) |
| 查角色、机体和世界规则 | [Canon数据入口](docs/superpowers/specs/data/canon/README.md)；有终端时可用`bash scripts/canon-query.sh entity CH_SOULIN` |
| 查看本项目写作Skill | [Canon](review/workflow-skills/chao-gag-canon/SKILL.md)、[创意编剧](review/workflow-skills/chao-gag-story-writer/SKILL.md)、[写作生产](review/workflow-skills/chao-gag-writing-pipeline/SKILL.md) |

核心阅读材料包括C01-C04的现有纯剧情稿、27号全剧概要v5.1、28号玩法与真实分支构思，以及31/32号分章和C05展开提案。全剧概要仍是Candidate；新的25章安排也不是正式冻结的章数。

玩法请同时看8月整合总案和9月至10月的后续候选设计。后续试验中的具体任务、招式与数值，并不会自动成为正篇发生过的事件。

原文和原图按原字节保留。[全量文件清单](review/library/FILE-MANIFEST.tsv)登记仓库内文件、原路径和SHA。已定源设计、授权派生、候选、历史与反例不因同步而变成同一采用状态。`review/`是新增导航和审阅说明，不修改原作设定。

本仓库不是完整可运行工程。未整体同步巨量QA录屏/中间帧、机器缓存、测试矩阵、个人配置、其他Vault和原始第三方工具。具体边界见覆盖说明，不能用这些排除项掩盖真正的设定或源资产漏传。

仓库用于定向评审，素材中的现实IP参照不代表获得发行授权。评审发现的好方案应明确列出改动及影响，再由项目采用；原始版本和验收记录继续保留。
