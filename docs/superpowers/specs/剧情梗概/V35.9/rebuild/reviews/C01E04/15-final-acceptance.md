# C01E04 最终放行记录

> Final status: `accepted_story_audience_production_canon`
>
> Accepted source: `episodes/C01/C01E04-万机馆站起来-v1.md`
>
> Accepted end-state source: `C01E04-runtime-contract-v1.tsv / C01E04_RT054`

## 放行依据

- 剧情监督与机体/IP/奇观席分别在`08-showrunner-targeted-recheck-r2.md`、`09-mecha-ip-targeted-recheck-r2.md`判定`PASS`；人物/关系席既有PASS未被本轮局部玩法补丁改写。
- Canon/宏观谜团/物理席在`12-canon-macro-physical-final-recheck-r3.md`确认六锚、四操作员、零疏散载荷、B1双值及旧伤连续无阻断。
- Gameplay/Production席在发现城区双臂态反例后，于`14-gameplay-production-final-recheck-r3.md`独立手算三Bundle、五步转体和失败回滚并最终判定`PASS`。
- `13-runtime-graybox-paper-run-r2.md`与机器checker共享同一入口口径：P4展开承重，P5前可见同步收臂并结算一次成本，`CITY_LOCAL`从双臂已收状态开始。
- 当前实跑全部通过：E02、E03、E04 Runtime/Graybox，V35.8 95槽strict，Canon smoke与Godot strict。

这里的Production放行指**故事与玩法生产契约可交接**，不代表57行Runtime已经逐项实现，也不代表正式美术、真人容量、Windows或平台验收完成。候选Godot纵切及其剩余边界继续以实现证据文档为准。

## C02唯一可继承事实

1. 万机馆旧址永久失去，WBM001以`CRUISE_CARRIER_WITH_DAMAGE`受损巡航态离开；它是移动基地/地图边缘支援，不是完整战舰火力或无限格纳库。
2. 四名随舰操作员精确为纪存、兜灯、唐胶、陆衡；二十九名撤离者、豪司和消防人员留在城市安全区，疏散人员载荷恒为零。
3. 馆守Z永久单臂，以胸前承重位成为常驻支援；右臂留在旧址成桥，禁止无来源修复、回收或装船。
4. 勇拳试作机及数据已由企业回收；白函带右肩裂和断索撤离；E02-E03供水、风道、档案冷却和消防机伤痕均未被E04清零。
5. 三类载荷只允许精确Bundle：`LIFE_PHYSICAL`、`LIFE_ARCHIVE`、`PHYSICAL_ARCHIVE`。代表路线为`LIFE_PHYSICAL`；C02必须逐类读取携带/旧址状态及档案冷备值，不能抽象成“缺一类资源”。
6. B1当前态为`RELEASED_LOW_SPEED_CRUISE_AFTER_SIX_ANCHORS`，历史态另存`PHYSICALLY_LOCKED_BY_MILITARY`；六锚留旧址，不得在C02重新演一次解锁。
7. 七海仍远程停权，已留下公开四十秒东锁延迟、停职延长和内审记录；她没有登舰，也没有恢复系统写权限。
8. 纪存取得右腕至胸口反灼与低置信旧供电记忆；它能提示身体顺序但不能自动给答案。黑展柜皇影只完成无光睁眼、卡右锁臂、拘束止扩张三拍，不可控、无完整身体。
9. 旧馆导航名熄灭，移动风险编号生效；生活循环、旧制转接和馆守Z承重垫形成36小时硬时钟，唯一现实可达节点锁定木桶旧件市。
10. 远星只留下`OPEN -> CLOSE -> OPEN`错序半帧，不构成实时通信、导航或真相揭示。

## 禁止回流

- 不得生成隐藏维修班、人员/消防货物/右臂载荷、三类全保或重新选择目的地。
- 不得把零号写回抽象诱惑、让皇影免费纠错、让七海到场控制，或把万机馆起航压回一句Cutscene。
- 不得把P4双臂展开与P5道路姿态混成同一状态；城区入口同步收臂有可见成本，城市失败回滚不重复付费。
- 不得用候选Godot纵切冒充57行完整Parity、正式美术或平台验收。

