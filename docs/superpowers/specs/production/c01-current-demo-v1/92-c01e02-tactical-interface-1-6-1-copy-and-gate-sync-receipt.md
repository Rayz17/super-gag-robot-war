# C01E02 Tactical Visual Interface 1.6.1 制作人同步回执

日期：2026-08-20  
状态：NON_GEOMETRIC_POST_DISPATCH_CLARIFICATION  
权限：Candidate production interface only

## 变更哈希

- 旧接口1.6.0：607724af9bc6cf21619cc8411e17f02ec337154a4d28320bec536edd21178135
- 新接口1.6.1：870f405ddbba5705db278f5f6c4da1e8d2a7e9fcded935b25b792d2d77b51a7c

## 唯一变更范围

1. 同步Task90预生产已由91号制作人签收、Call02仍阻塞的门状态。
2. 把A/B策略第一读法改为全中文且对称展示收益与代价；不再只显示热量／余量，也不在产品copy中出现east、south、damaged、active或R2等工程写法。
3. 将原contact_t3_entity_state明确标记为A路；另登记B路已冻结的核心状态，并继续等待Task89完整actual readback。
4. 将旧81/82标为分别被90/89取代，补登记89、91、P89 review与Call02当前状态。

## 未改变项

- 32x18、40x20投影、runtime raw origin、canvas origin、共同PLAN相机与A/B CONTACT相机未改变。
- A/B route family、端点、步数、朝向、动作／预备、T3/T3.25、socket、post结果、热量、设施、道路与第二轮结果未改变。
- 89号写域、11帧、45-75秒自然trace、real_art_loaded=0与fixture-free验收要求未改变。
- 90号预生产输入历史仍按当时607724...哈希有效；未来Call02必须消费当前1.6.1与P89签收帧，不得沿用旧copy或未分路CONTACT状态。

Task89可在不重开几何与任务范围的前提下，将本回执作为post-dispatch产品copy／gate clarification，并在完成报告同时记录89原始输入锁与本回执SHA。
