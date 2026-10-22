# C01E01 游戏制作 / 玩法叙事席定向复检 r2

> Review seat: gameplay / production
>
> Evidence boundary: `C01E01-最后一条闭馆路线-v1.md`、`C01E01-runtime-contract-v1.tsv`、`C01-逐章重构地图-v1.md`、`06-joint-revision-decision-r1.md`
>
> Ruling: `BLOCKER_TO_PRODUCTION_LOCK / TARGETED_CONTRACT_PATCH_ONLY`
>
> Scope: 不改 Story Core，不扩展 E02，不重写 Episode。

Evidence aliases: `Episode=C01E01-最后一条闭馆路线-v1.md`；`Runtime=C01E01-runtime-contract-v1.tsv`；`Map=C01-逐章重构地图-v1.md`；`Decision=06-joint-revision-decision-r1.md`。

## 一、总裁定

联合裁定的大部分玩法阻断已关闭：探索/战棋控制对象已分开，跌跌翻面归还玩家，馆守Z仅为场景支援，29人的算术与儿童看护关系成立，误照不再制造 Game Over，活动敌方也已收束到一个路径框家族和两台贴片机。

但当前 TSV 仍是“成功演出时序”，不是可纸面跑通的 `8x10 / 3回合` 关卡合同：缺少格位与移动常量，R2/R3的过线时点互相冲突，且没有可执行的失败/回滚分支。因此本席仍为 **BLOCKER**，但只需定向补合同，不动故事核心。

## 二、分项复检

| 项目 | 分类 | 精确证据 | 复检结论 |
|---|---|---|---|
| `8x10 / 3回合可执行性` | **BLOCKER** | Decision `:71-78`要求固定地图、回合和相位；Episode `:199-209`只复述规则；Runtime `:5-12`只列成功事件。 | 无跌跌/机器犬/A-D起点、闭馆线/侧门/传感格/回充格坐标，无小机移动力、Token每回合自动格数与固定路径，不能验算三回合可达。 |
| `R2/R3状态守恒` | **BLOCKER** | Runtime `:9` 在 `ROUND_2_EVENT`强制 `all_tokens_cross_asset_line` 并进入 `ALL_29_STAGED_FRONT_HALL`；Episode `:151-155`却在R3触发“最后一位观众已通过”和“最后一组越线”。 | 同一批Token同时在R2全部过线、R3再有最后一组；`JAMMED_ONE_ROUND`也未说清覆盖哪个自动移动相位。 |
| `控制权` | **PATCH** | Episode `:192`锁探索纪存，`:199-204`锁战棋只控跌跌/机器犬，`:217-219`将主动侧倒和胸灯确认交给玩家；Runtime `:10-11`保留兜灯硬停与馆守Z自主保护。 | 主权已关闭。仅R3的“玩家移动挡板”（Episode `:151`）未说明是独立场景支援，也未指定唐胶是实际执行者。 |
| `29人 / 4 Token` | **PATCH** | Episode `:69`为 `21+4+1+1+2=29`，`:202`为 `11+10+3+5=29`，与Map `:25`、Runtime `:2-4`一致。但Episode `:139`已把维修员算入D5，`:141`又把他写成工具柜后的独立救援对象、再与慢速组会合。 | 算术 **PASS**，物理Token状态未唯一。按当前字面制作会得到D4+维修员独立标记，与“始终4 Token”冲突。 |
| `失败条件` | **BLOCKER** | Episode `:205-208`规定R3后仍有Token在资产区才失败，非法胸灯角度只阻断并重瞄；Decision `:78`同样锁“超时或Token未过线”。Runtime `:5-12`没有任何失败行，反而把R2全员过线写成 `mandatory_outcome`。 | 可读规则已正确，运行时合同无法产生失败、重试或成功原子提交。 |
| `资产上限` | **PASS** | Episode `:291-293`锁一张L1连续景、1个活动路径框家族、2台贴片机和一次馆守Z胸灯，并排除馆守Z/社勇王/白函完整战斗集；与Decision `:71-78`一致。 | 战棋核心资产量已可控，不需加机体或敌AI。只需在合同补记四枚Token角标、传感格/闭馆线/光路预览等低成本地图UI，不改资产等级。 |

## 三、最小修复

1. **给TSV补唯一的灰盒常量表。** 只增加 `8x10`坐标、两小机与A-D起点、闭馆线/侧门/传感格/回充格、移动力、Token自动格数和固定路径。R3胸灯标为不吞小机行动的独立支援：玩家选挡板格/光路，唐胶执行，兜灯否决非法角，馆守Z只做自主收灯。
2. **把唯一过线时点锁在R3。** 将TSV `RT008`改为D5到达闭馆线前 staging 格，不输出 `ALL_29_STAGED_FRONT_HALL`；在R3安全光路确认后增加Token自动移动与 `29/29、4/4`统一结算。同时写死 `JAMMED_ONE_ROUND` 覆盖至该次R3过线相位。
3. **把D唯一化为一枚 `D5_LOCKED` Token。** 维修员是D5内的锚定成员，开局不再生成第五枚人员标记；机器犬自主锁定D5，玩家只承担开侧门放入一台贴片机的路线代价。
4. **给TSV补一对结算分支。** `R3_STATUS: 4/4过线 -> SUCCESS_COMMIT`；否则 `MISSION_FAIL_TIMEOUT -> RETRY_NO_STATE_COMMIT`。`BLOCKED_BY_DOUDENG -> AIM_PREVIEW` 只重瞄，不进失败分支。
5. **在资产表补一行低成本战棋UI清单。** 仅列四枚Token人数角标、安全箭头、传感格、闭馆线、有限离散挡板格和胸灯 `READY/BLOCKED/SPENT`；不新增战斗单位、HP、攻击或完整敌AI。

## 四、重验门槛

不改可读故事的前提下，用补后合同纸面跑一次R1-R3：任何成功路径都必须在R3唯一地交 `29/29、4/4`；任何失败都只能是R3结束仍有Token未过线；失败重试不留结算状态。达成后本席可转 `PASS`。
