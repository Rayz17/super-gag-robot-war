# G2-A2-C2 屏幕输入与动态责任解证明

## 真实屏幕事件链

A通过`InputEventMouseButton + InputEventKey`，B通过`InputEventJoypadButton`，事件实际进入专用Scene的`Control._input`，再由`c2_screen_input_adapter.gd`调用Session公开API。capture/performance driver源码扫描证明没有Session、fixture或direct draft mutation调用。

外部validator从manifest原始数组重算后，A/B生命周期均为：

`PUBLIC_SITUATION → EDITABLE_DRAFT → COMMIT_SUMMARY → EDITABLE_DRAFT → COMMIT_SUMMARY → JOINT_RESOLUTION → ROUND_RESULT`

| 策略 | 实际输入 | 原始InputEvent数 | 外部重算hold | hold帧数 | 执行时长 | commit |
|---|---|---:|---:|---:|---:|---:|
| A | 鼠标+键盘 | 23 | 670.657ms | 59 | 13,334.692ms | 1 |
| B | 手柄等价InputEvent | 29 | 681.415ms | 60 | 13,322.257ms | 1 |

两路均完整包含summary、return to edit、undo、redraw、再次summary、0.7s hold与自然T1–T5；单一Scene/Control/Session/Director instance id可回读。这仅证明确定性屏幕输入接线，不声称真人或物理手柄回放。

## 空草稿、真实失败草稿与修复

- PUBLIC首帧路线只有起点，没有预填A/B结果卡；
- 未闭合时显示`还差：终点／步数／朝向／动作或预备`；
- A路InputEvent先成功写入一条`route_family_endpoint_mismatch`失败草稿，草稿hash变为`1dc7700d407e7193be7cb4b9cb8f460e6cc68fed6411c89ef06009c5cebec96f`，preview明确`success=false`；
- 随后Z/undo令草稿hash再次变为`e5c6c808308cce3cbb1c26ce8d6c4d9a4ac26a9653e65c5a2c6737e42b819e4d`，再由下一次输入重画为合法路线并得到preview success；
- 外部validator从raw trace重算顺序为输入序号7失败草稿、序号10撤销、序号11合法重画，且三阶段hash变化成立；
- 被入口拒绝的`[20,13]`另记为一条fail-closed证据，不作为“失败草稿→撤销修复”的代理证据；
- 路线、终点、朝向、动作/预备齐全后，才从同一Resolver preview生成当前方案责任结果；
- A/B直点终点与alternate同族路线均成功，路线族仍为A=21、B=15，20次确定性通过；
- preview/execute使用同一Resolver token；时间线token由两侧独立公开态投影后比较，详见03号证明。

## 动态责任结果与只读另一路比较

当前卡与主动展开的另一路卡都由Resolver公开preview字段动态格式化：本轮热量、设施状态、路损来自`world_result`，接触时点来自E3 event log，承接前缘来自`plan_summary.contact_geometry`；第二轮热量/余量由只读adapter用同一已解析结果构造R2输入后调用Resolver，未复制A/B常量。逐字段缺失均fail closed，`static_copy_used=false`。

| 动态责任 | A | B |
|---|---|---|
| 本轮热量 | 24 | 46 |
| 警戒设施 | 受损 | 保全 |
| 道路损伤 | 42 | 24 |
| 接触 | T3.00 / 2格前缘 | T3.25 / 1格错位 |
| 第二轮 | 热量68，余量1 | 热量88，余量0 |

C/Back实际InputEvent进入两路nonheadless trace并展开同层级收益/代价：A当前卡比较B，B当前卡比较A。外部validator证明：

- current与other的`route_family_id`均非空且彼此不同；
- current与other的Resolver token均非空且彼此不同；
- 比较开关前后current `draft_signature`完全不变；
- `selected_strategy`完全不变；
- A/B compare actual frame均存在，收起后仍回到当前方案。

## C2产品copy边界

C2 Scene只向Product UI传入`jicun_line / objective / timeline / top_threats`四个固定公共copy键。manifest逐帧记录`strategy_result_keys_present=[]`、`static_responsibility_copy_reachable=false`、`configured_copy_exact_public_whitelist=true`；责任结果只能来自上述动态preview路径，不能从profile的`deterministic_copy_contract.expected_text`或静态strategy表进入产品UI。

证据：[screen-input-contract.json](receipts/screen-input-contract.json)、[raw-screen-trace-validation.json](receipts/raw-screen-trace-validation.json)、[route-family-nonregression.json](receipts/route-family-nonregression.json)。
