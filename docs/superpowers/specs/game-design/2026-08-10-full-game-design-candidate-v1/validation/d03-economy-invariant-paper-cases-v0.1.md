# D03 经济守恒纸面案例 v0.1

> Status: `candidate_paper_cases / zero_build / no_balance_claim / human_not_run / user_not_decided`

## 1. 边界

[economy-flows.tsv](../data/economy-flows.tsv) 仍然只是25类资源、压力与非货币状态的定性合同。本件不设正式价格、产出曲线、商店、难度或成长数值，只把最小守恒规则写成可机检纸面案例，防止实现时出现负资源、失败仍扣费、重放重复奖励、唯一部件复制，或把关系／同意／权限兑换成货币。

机器输入见 [economy-invariant-paper-cases.tsv](../data/economy-invariant-paper-cases.tsv)。九行覆盖：

- 战术脉冲：一次合法指挥带宽消费与一次超支拒绝；
- Hub维修：一次材料原子提交与一次Body Owner拒绝后的整组0写入；
- Operation：一次具名弹药消费及同事务幂等重放；
- 唯一部件：转移保管或安装不改变全局实例数；
- 禁止兑换：关系不能补材料、同意不能补带宽。

## 2. 统一验算

对`accepted`：

```text
balance_after = balance_before + source_delta - sink_delta
0 <= balance_after <= cap
reserved <= balance_before + source_delta
```

对`rejected`：算术候选可以越界或Owner准备失败，但持久`balance_after`必须等于`balance_before`，没有accepted receipt，所有预留释放。对`idempotent_replay`：不得再次应用source/sink，必须返回原receipt和原后态。

`RES_KEY_COMPONENT`以全局实例数验算：转移前后都必须为1；owner、custody、installed state由`SOG-BODY`回执改变，不能用“消耗一个、奖励一个”模拟转移。

## 3. 当前能证明与不能证明

静态checker通过后，只能证明九个案例的算术、Owner、回滚、重放和禁止兑换字段相互一致。它不能证明：

- 玩家是否觉得资源取舍有趣；
- 2点带宽、2份材料或3发弹药是正确平衡；
- Hub经济能支撑22章；
- 实际RunState／事务代码遵守这些案例。

正式实现前仍需把这些行编译成StateTransaction v2测试，绑定ruleset/build hash，并用失败故障注入证明持久状态确实0写入。
