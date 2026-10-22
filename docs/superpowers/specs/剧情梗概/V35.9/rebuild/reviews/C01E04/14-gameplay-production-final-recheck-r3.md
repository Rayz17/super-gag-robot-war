# C01E04 游戏制作 / 玩法最终针对性复核 r3

> Reviewer Mode: `targeted subagent standard`
>
> Subagent Review ID: `gameplay_production=019f692d-ce33-75f1-9a54-8422047382a3`
>
> Scope: 只复核r2所留城区入口锁臂、Bundle预算、转体、回滚与误败阻断。

## 终判

**`PASS`。** r2所列唯一玩法阻断已经闭合；本席允许C01E04进入整话最终验收。该结论不外推为正式美术、真人容量、Windows或平台Production验收。

## 独立证据

1. P4双臂展开承重后，`RT039`用一次可见`CORRIDOR_FOLD`同步收臂，结算热量与条件档案冷却，再建立`arms=BOTH_RETRACTED`的`CITY_LOCAL`；正文、Runtime、Graybox和资产态一致。
2. 三步黄金路线手算结果为：`LIFE_PHYSICAL heat3`、`LIFE_ARCHIVE heat3/archive1`、`PHYSICAL_ARCHIVE heat7/archive1`，均满足`heat<8 / cooling>0 / structure>0`。
3. 五步转体路线在`LIFE_PHYSICAL`与`LIFE_ARCHIVE`均可完成，终值分别为`heat5`与`heat5/archive1`，不再是假按钮。
4. 收臂本身导致`heat8`或活动档案冷却归零时，`CITY_LOCAL`尚未创建，回`HALF_RISE_LOCAL`；城区内失败则恢复已含收臂成本的`CITY_LOCAL`，不会重复付费或复制七海回执。
5. `PHYSICAL_ARCHIVE`无法承担五步路线，`RT040`会按Bundle资源预演在确认前禁用并显示具体原因，不允许玩家走入确定性误败。

## 验证

`PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_c01e04_runtime_graybox.py`通过：57 Runtime行、40 Graybox行、56资产状态、三精确Bundle与四检查点全部闭合。

