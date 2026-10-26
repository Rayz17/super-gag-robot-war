# A31 Call01｜单画布前 3Q 硬门失败回执

> Date: `2026-08-24`
>
> Status: `SECTION2_FAIL_STOP / NO_USER_DELIVERY`
>
> Runtime / Godot / Canon: `false / false / false`

## 调用事实

- Built-in ImageGen front calls：`1`。
- Built-in ImageGen rear calls：`0`；前视未过门，后视不得独立设计。
- Random reroll：`0`。
- 编辑目标：`../source-lock/WANJI_A25_05_FRONT_EDIT_TARGET.png`。
- 下身结构参考：`../source-lock/WANJI_A25_02_B1_B2_STRUCTURE_REFERENCE.png`。
- 精确提示词：`../prompts/A31-CALL01-FRONT-SINGLE-CANVAS-BUILTIN-IMAGEGEN-PROMPT.md`。
- 默认生成：`/Users/rayz/.codex/generated_images/01a0331a-00ea-7f73-abf8-df6507f356e5/exec-47bd2367-6358-4e88-980b-833da4cea149.png`。
- Workspace 失败留证：`../failed/WANJI_A31_CALL01_FRONT_SINGLE_CANVAS_SECTION2_FAIL.png`。
- 尺寸／格式：`1536 × 1024 PNG`。
- SHA-256：`c624a3a7339437a8090119837e3a694a4e92c73d495ee47e463a1a83907b935f`。

## 硬门结果

| 门 | 结果 | 可见证据 |
| --- | --- | --- |
| 一张独立前 3Q | `FAIL` | 输出同时包含前视、后视和固定馆地下剖面三个大区块 |
| 一个机体／一个角度 | `FAIL` | 前后两台完整人形同时出现 |
| 无设计板／无文字 | `FAIL` | 标题、规格、身高重量、功能列表与层级说明大量出现 |
| 上身调性保留 | `PARTIAL_PASS` | 小头、双青眼、天线、馆门胸部和肩臂大体可追认 |
| 前视收窄 | `FAIL` | 仍保持横向宽厚重装机器人包络，没有达到 A29 guide 的胸肩髋关系 |
| B1/B2 分段小腿 | `FAIL` | 小腿仍由大块连续白色护胫主导，竖向交通核、设备层与桁架未成为首读 |
| 非鞋型基座足 | `FAIL` | 足部仍有鞋尖、脚背和靴型外轮廓 |
| 可作为后视几何母版 | `FAIL` | 前视未建立合格几何，禁止继续调用后视 |

## 停止边界

- 不裁切设计板中的人形冒充独立交付，因为裁切不能修复宽体、白护胫和鞋型足。
- 失败图不得成为后视、后续 Wanji、Godot、Runtime 或 Canon 的正向输入。
- `delivery/` 为空；不存在待用户确认的 A31 正式候选图。
