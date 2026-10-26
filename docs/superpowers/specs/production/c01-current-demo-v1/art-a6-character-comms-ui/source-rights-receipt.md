# C01E02 A6 来源与权利边界回执

> Package: `C01CDV1_A6_CHARACTER_COMMS_UI_R05_CANDIDATE`
>
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 来源分类

| 类别 | 来源 | 本包使用 | 边界 |
| --- | --- | --- | --- |
| 角色身份锚 | `09b` 登记的纪存、唐胶/兜灯/七海、馆守 Z 冻结图 | 只做身份、服装、头胸特征参照 | 读取专用；不将冻结锚声称为 A6 Runtime 资产 |
| 剧情与 Canon | 已验收 C01 Reader E02；`CH_JICUN` / `CH001` / `CH_QIHAI` / `CH002` / `V355-C01E02` 当前查询 | 限定角色信息位置、权限和禁止读法 | 不新增台词、战场权限或 Canon 事实 |
| 新作人物图 | OpenAI 内置 `imagegen`，配合项目身份参考 | 纪存三态、七海三态、旧守护者三态 | 生成候选素材；未做法律权利结论；不使用在世艺术家姓名、现有角色/IP 名称、商标或第三方库素材 |
| 透明处理与 packing | 本地 `ffmpeg` chromakey/despill/scale/pad/overlay/hstack | 去绿幕、安全区、分层、atlas、评审图 | 可复现派生；不改写任何外部源文件 |
| 兜灯既有批准件 | `CUTIN_DOUDENG_C01_OBSERVE_V01` / `TENSE_V01` | 只在适配板和本地通讯模拟图中整幅等比缩放 | 不裁切、不变形、不覆盖原件、不复制成 A6 母版、不冒名 Stable ID |
| A4 地图 | 已批准 A4 `A4_MAP_B_pure_read_no_ui_2400x1350.png` | 三张 720p 模拟图的评审背景 | 模拟图内嵌只作演示；不产生新 A4 母版或 Runtime 权利声称 |

## 生成与编辑回执

- 新作位图使用内置 `imagegen`，不使用 CLI 降级、付费外部批处理或 LibTV。
- 透明图采用平滑 `#00ff00` 色键源图后本地去背；validator 检查 alpha 外缘、安全区和绿边比例。
- 七海 `decision` 在制作人视觉复核后使用内置编辑做局部纠偏：嘴唇闭合、下颌与眼神更坚定，身份、服装、平板、构图不变。张嘴版仅留在 `sources/chroma/qihai-decision-speaking-drift-rejected-source.png` 作拒绝轨迹，没有活动消费者。
- 生成图不烘字、姓名、对话、按键、版权标记或水印。模拟图的空白框仅是程序安全区示意。

## 权利声称限制

本回执记录来源与处理边界，不替代制作人的商用法务审查，也不把 Candidate 状态解释为 Runtime、Canon 或 exact handoff 批准。
