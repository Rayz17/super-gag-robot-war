# Candidate授权合同与故障注入验证 v0.1

> Status: `PASS / schemas_and_empty_registries_only / no_user_authorization`
>
> Scope: DEC-01、DEC-02、DEC-11的收窄边界；DEC-11分相迁移；方向回执实例、精确执行包络回执、共享预算池、scope化Gate实例与Prototype preflight的机器合同。

## 结论

`check_candidate_authorization_contracts.py` 已通过。当前六类执行实例表都只有Schema表头：方向回执 `0`、精确包络回执 `0`、执行包络 `0`、共享预算池 `0`、Candidate Gate实例 `0`、preflight `0`。因此本报告证明“合同可机检且能拒绝越权输入”，不证明用户已批准任何决策、Build、Session或迁移。

R0与P1实现被拆成两个不可互相代签的包络：`E-R0-IMPLEMENT` 只允许R0且`max_total_builds=1`，`E-P1-ABCD-IMPLEMENT` 只允许A/B/C/D且`max_total_builds=4`。两包必须各自取得绑定精确subject hash的用户包络回执，同时共用`STAGE0_R0_P1`单一累计池，合计上限仍是14日、80内部人时、外部现金0，不得变成28日/160人时。

P1已覆盖A/B/C/D四版implementation与human-run前置；`D04-P1-SHORTLIST` 的analysis-only前置不带执行包络，不得Build、接触参与者或产生单一胜者；新的shortlist真人Session须独立human-run包络。`D04-P2-CROSSOVER` 要求DEC-04-A、P1 shortlist M5、精确`TSN-P1-RESULT=shortlist_two/three/four`和独立实现/真人包络；`no_winner/revise_top_two/retire_all`都停机，且不把DEC-03-M当作原型执行权。

DEC-11的现行链迁移被拆为`M计划 → M1 checker → M2 Registry/schema → M3单一scope story-chain → M4部署后重验/回滚`，每相都需独立回执与精确执行包络，无一相已授权。

## 命令与结果

```text
python3 -B docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/scripts/check_candidate_authorization_contracts.py

Candidate authorization contracts: PASS
- schemas: envelope=63; decision_receipt=29; envelope_receipt=19; budget_pool=26; preflight=29; gate_instance=46
- instances: decision_receipts=0; envelope_receipts=0; envelopes=0; budget_pools=0; gate_instances=0; preflights=0
- preflight contracts=13; fault injections rejected=11/11
```

## 故障注入

checker内嵌的11项独立故障注入均被拒绝：

1. 用户批准subject hash后放大人时上限；
2. 授权后扩大可写目录；
3. 无独立包络回执即把draft自改为authorized；
4. 用另一subject的回执代签当前包络；
5. 以通用Gate定义ID冒充scope化的passed Gate实例；
6. 以decision状态文字冒充accepted回执实例；
7. 对同一program scope同时开启两个共享预算池；
8. 共享池累计人时超cap；
9. 用R0包络执行P1合同；
10. 在analysis-only shortlist前置中夹带执行授权。
11. 把`TSN-P1-RESULT=no_winner`冒充成C2 crossover入口；`revise_top_two`和`retire_all`同样是停机结果，只有`shortlist_two/three/four`可进入。

## 停止线

本授权合同checker通过本身不得改写为`approved_for_candidate_test`或“可开始原型”。首批签署包现已独立解析四项原子选项、非授权项、实际回执实例规则和执行包络模板，并由其自身checker判定为`ready_for_signature`。该状态只允许向用户呈请四项方向裁决；当前仍是`presented_no_decision`、六类执行实例全为0，无Build、Session或迁移授权。
