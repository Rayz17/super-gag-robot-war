# C01E02 U86路线A用户批准与玩法对齐重开回执

日期：2026-08-20  
任务ID：`P87_U86_ROUTE_A_USER_APPROVAL_AND_GAMEPLAY_ALIGNMENT_REOPEN`  
状态：`USER_APPROVAL_RECORDED / GAMEPLAY_ALIGNMENT_COMPLETE / P88_P89_P90_SIGNED / ART_CALL02_STILL_BLOCKED`  
权限：`Candidate production only`  
不构成：Canon迁移、Runtime晋级、真实美术handoff、UA91开放、G2-B开放

## 1. 用户原文与正式裁决

用户原文：

> 保留R2C互动骨架，按当前玩法空间重做精品地图。不过请认真核对主策划session已经给出的玩法设计，尽可能做得好玩一些

正式裁决：

1. 86号路线A获批：保留当前R2C互动骨架与current R2C对象空间；旧A4不得恢复为current exact world。
2. A4只保留为视觉语言、材质、建筑分层与遮挡方法donor；current-topology地图须重新派生。
3. 本批准附带新的制作要求：恢复美术与Scene施工前，制作人必须读取并吸收主策划任务已经封存的玩法总案，不能只做几何对格或漂亮静帧。
4. 本轮仍是Candidate Demo；用户尚未批准任何新地图像素、真实单位Sprite、完整Golden Turn、Runtime或Canon晋级。

## 2. 当前权威与明确排除

### 2.1 当前故事／机体责任源

- Current Working场景：`V355-C01E02`《巨神从展台起身》。馆守Z在E02首控参战，站到BREAK​ER与东侧撤离线之间，护到最后车辆通过，取得退役重盾并首次击倒BREAK​ER。
- Current Working机体：`V353U001`馆守Z；C01E02为首次正式战斗。
- `V359-C01E02`“馆守Z身体零动作／消防五回合”链已经在Design Graph登记为History，不得回流本Demo。

### 2.2 玩法方向责任源

- 主策划任务：`019fe60f-8afd-7781-ac0e-d5f89d09617a`，标题《主策划》。
- 当前总案：`docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/00c-core-game-design-master-review.md`，状态为用户方向批准的Candidate设计，不自带Build权限。
- Demo迁移合同：`19-current-demo-inplace-rebase-producer-contract.md`。
- 当前R2C逻辑基线：79、80、83、84号及`main-g2-a1-r2c*`证据。

冲突顺序：Canon Hard/Working → 已验收Reader／回执 → 19号Demo合同 → 本回执对00c的Demo限域转译 → R2C已签逻辑几何 → A4视觉donor → History。

## 3. 00c在C01E02中的限域转译

C01只承担“基础身体责任”的早期教学，不提前塞入完整人物牌、气势条、名场面作业、Meta或多机编队。第一轮Golden Turn必须把以下公共语言做实：

1. **公开意图：**BREAK​ER冲线、小体扑向东门／车辆、车辆通过时点与环境变化在提交前可读；信息来源与时效可见。
2. **可反悔规划：**路线、终点朝向、主要动作／预备反应在提交前自由修改，不写世界状态。
3. **提交摘要：**同一屏预览争格、接触、承力、预备触发顺序、A／B代价与第二轮余量。
4. **共同结算：**馆守Z、BREAK​ER、小体、应急车、城市炮和环境按冻结意图进入同一Session／Resolver结果；敌人不得读取玩家未提交草稿。
5. **身体与朝向：**多格身体、转身、正面承力、错位接触、反冲、footpoint、socket与遮挡必须既能算也能看懂。
6. **非歼灭目标：**最后车辆通过和撤离线保护是主要责任；小体不要求全灭，至少一组幸存。
7. **两种真实打法：**主动迎撞与先护撤离线必须改变执行时序、热量、接触位置／后果和第二轮余量，不得只改路线颜色或战报文字。
8. **规则精通奖励：**若玩家利用公开冲线、朝向、道路宽度或预备条件做出强解，系统要在预览与结果中承认，不以隐藏免疫收回。

## 4. “尽可能好玩”的制作人门

在恢复可见像素前，必须回答并证明：

- 玩家第一眼能否说出“我要让车通过，同时挡开小体，并站到BREAK​ER冲线前”。
- 玩家是否在30秒内看懂主动迎撞与先护线的区别，以及为什么后者更热、第二轮更紧。
- 玩家是否真的选择了路线、朝向和预备，而不是按唯一高亮答案。
- 执行是否形成清楚的因果兑现：车先过、小体被挡、馆守Z转正、巨体接触、城市炮取得侧甲窗口。
- 接触是否有重量：接触前静默、hit-stop、局部碎地／水花、反冲、声音和镜头同源；不能靠白闪或独立满屏插画冒充。
- PLAN与CONTACT画面能否在正确地图透视下同时读出主要目标、威胁、路线、身体、撤离口和下一时点，而不是先看装饰。

如果现有R2C字段不足以支持上述读法，允许在Candidate范围内补UI、公开态、预备语义、反馈与视觉层；若要改变已签anchor、route、contact normal、R1→R2后果、故事顺序或胜负条件，必须先由制作人重新签几何／玩法合同。重大玩法迁移仍停给用户。

## 5. 本回执后的唯一合法DAG

```text
P87 主策划玩法对齐审计
→ current-topology地图／交互目标合同
→ G2-A2-C1联合注册与无身份Proxy连续Session preflight
→ 制作人核验actual frames与玩法第一读法
→ A9.1-A6-S-C1按同一地图、镜头和公开态制作PLAN／CONTACT整屏目标
→ G2-A2 Scene与美术scene-first并行收敛
→ 制作人联合Gold Frame预审
→ 用户UA91
```

截至本回执首次落盘时继续禁止：Art Call02、CONTACT生成、G2-A2 Scene／Actual Frame、真实资产、UA91、A9.1-B、signed handoff、G2-B、Default Entry、Runtime、Canon、批量付费生成与LibTV。下节仅按88／89限域解除proxy-only Scene／Actual Frame；其余停止门不变。

## 6. 对齐完成与执行入口

主策划总案、当前R2C代码与current topology的交叉审计已完成。后续唯一入口：

- 制作人玩法／地图合同：`88-c01e02-r2c-fun-first-current-topology-map-and-interaction-contract.md`
- 主程序-2目标书：`89-c01e02-g2-a2-c1-current-topology-fixture-free-golden-turn-objective.md`
- 美术资产-2预生产目标书：`90-c01e02-a9-1a6-s-c1-current-topology-scene-first-preproduction-objective.md`

主程序-2现可做proxy-only actual frame与无fixture输入证明；美术资产-2只可做pre-generation准备。新的可见像素仍须等待89完成后由制作人实际签收并另发`CALL02_ALLOWED`。
