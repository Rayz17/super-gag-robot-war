# C01E01 剧情监督/连续性定向复审 r2

> Review Seat: 剧情监督 / Showrunner / Continuity
>
> Scope: 仅复核联合裁定后的 C01E01；不重写、不扩章
>
> Verdict: `PATCH`
>
> Blocker Status: `B01 CLOSED / B02 CLOSED / NO NEW BLOCKER`

证据缩写：`episode` = `docs/superpowers/specs/剧情梗概/V35.9/rebuild/episodes/C01/C01E01-最后一条闭馆路线-v1.md`；`runtime` = `docs/superpowers/specs/剧情梗概/V35.9/rebuild/episodes/C01/C01E01-runtime-contract-v1.tsv`；`map` = `docs/superpowers/specs/剧情梗概/V35.9/rebuild/maps/C01-逐章重构地图-v1.md`；`decision` = `docs/superpowers/specs/剧情梗概/V35.9/rebuild/reviews/C01E01/06-joint-revision-decision-r1.md`。

## 一、裁决

联合裁定要求关闭的两项剧情监督 Blocker 已关闭。开篇钩子、六站节奏、九点失约和“发送消防图 -> 四令取得介入口 -> 火场启动”的主因果均已成立；不需要改 Story Core、可读剧情或章地图。

当前只剩一处运行时连续性错位：合同在 R2 提前把 29 人全部结算到前厅，但可读剧情和 R3 合同仍把“最后一位观众/最后一组越线”留给胸灯高潮。此处是原子状态搬移，判 `PATCH`，不升格为 `BLOCKER`。

## 二、定向证据

| 复核面 | 判定 | 精确证据 |
|---|---|---|
| 开篇钩子 | `PASS` | 冷开场以次日 00:30 的单臂馆守Z、巨构轮廓、断臂通路和发烫钥匙起问，随后准确切回 20:47（episode:61-65）；日常入口立即落到 32 人、凉饭、餐具和旧杯（episode:69-89），再由旧警报、空白回信、0号敲击和风险闸形成递进（episode:105-119）。这保住了联合裁定锁定的故事发动机并修正时间口径（decision:11-13,54）。 |
| 六站节奏 | `PASS` | 唯一有向路线明确为六站且全在 L1，0号门在路线结束后（episode:91-95；runtime:3）；可读层只前景化三组运动：总图/纵向尺度（episode:95）、馆守Z/模型修复（episode:97）、现实机/馆外工务（episode:99-103）。探索拆分再次锁定唯一顺序及 L2/L3/B1/B2 不可进入（episode:192-195），与章地图及联合裁定的三组前景要求一致（map:53-60；decision:55-57）。原 B02 关闭。 |
| 九点损失 | `PASS` | “九点见”的私人约定先由餐具、杯子和未合箱落地（episode:79-89）；R2 钟声响时纪存只能看一眼晚饭提醒，机器犬叼走湿纸袋（episode:143-149）；救援后他取回湿袋，公务频道随即接管（episode:159-167）。闭馆和晚饭是在玩家救援过程中实际失去，不再由结算代述，满足联合裁定的声音拍要求（decision:54）。 |
| 主因果与不可逆动作 | `PASS` | 纪存先拒绝暴露完整搬运脊道，只拆出一段消防回线（episode:119,127-135）；尾声主动发送真实但不完整的回线图（episode:167-171），外部当场捕获路由地址与唤醒声纹（episode:171），四令随即冻结门、胸灯、数字钥匙和泵站（episode:173），烟进入且喷淋失效（episode:175）。`RT012-RT014`逐项固化同一链条（runtime:13-15），满足联合裁定的直接因果条件（decision:66,98）。原 B01 关闭。 |
| E02 必然性 | `PASS` | E01 结束时 29 人只在前厅黄线、尚未离馆（episode:157-159）；四令已造成半开防火门、胸灯切断、数字钥匙冻结、泵压归零，七海只能立即下达西移命令（episode:171-177）。章地图把同一输出直接写成 E02 的火场输入（map:44-45），并对齐联合裁定的 E02 必读状态（decision:89,98）；不存在问询或普通封馆即可收束的替代下一话。 |

## 三、唯一最小修补

### P-R2-01：把 29 人完成态从 R2 移回 R3

**冲突证据**

- `RT008`在 R2 写成 `all_tokens_cross_asset_line / ALL_29_STAGED_FRONT_HALL`（runtime:9）。
- 可读剧情 R2 只明确慢速组过框（episode:149；战中触发 episode:218），R3 才报“最后一位观众已通过”，且跌跌等“最后一组越线”后起身（episode:151-155）。
- `RT010`自身也在 R3 写有 `guide voice confirms last visitor`（runtime:11），因此合同内部与可读层同时冲突。

**最低修法**

1. `RT008`只结算九点钟声、湿晚饭袋和 Token D/慢速组越线；结束态改为慢速组已到前厅、其余撤离 Token 位于最终导引线。
2. 把 `ALL_29_STAGED_FRONT_HALL`及`C01_VISITOR_RESCUE_SEED_ALL_29_STAGED_NOT_CITY_SAFE`移到`RT010`，由安全胸灯角、馆守Z保护动作和最后一组越线共同生成。
3. 不改 episode、章地图、回合数或 E02 输入；不新增合同字段。

完成这一个状态搬移后，本席改判 `PASS`。
