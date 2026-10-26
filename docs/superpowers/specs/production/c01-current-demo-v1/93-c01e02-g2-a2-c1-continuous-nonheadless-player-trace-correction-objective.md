# C01E02 G2-A2-C1 连续非headless玩家链证据纠偏任务书

日期：2026-08-20  
任务ID：G2_A2_C1_CONTINUOUS_NONHEADLESS_PLAYER_TRACE_CORRECTION  
状态：DISPATCHED / P89_AND_CALL02_REMAIN_BLOCKED

## 1. 纠偏原因

89号交付的路线族、公开Session API、A/B CONTACT、current topology、12张actual frame、性能与隔离证据均已通过制作人和独立复核；视觉代理门可记为FIRST_READ_SUPPORTED_FOR_LOOKDEV。

唯一实质缺口：现有50.8秒capture先同步完成全部公开API编辑，再调用author_plan_time累计45秒；manifest中的trace从COMMIT_SUMMARY开始，没有连续包含PUBLIC_SITUATION、EDITABLE_DRAFT、COMMIT_SUMMARY、JOINT_RESOLUTION、ROUND_RESULT。因此它只能证明无fixture公共API链与约5.8秒Director自然执行，不能证明89号要求的45-75秒连续玩家链。

## 2. 唯一允许修正

对A、B各补一条同一非headless 1280x720 Scene中的连续证据：

1. 从PUBLIC_SITUATION实际开始记录。
2. 在连续process frames中依次调用公开Session API：begin planning、append waypoint、set facing、set action或prepared reaction、open summary、return to edit、undo、redraw、open summary、0.7秒hold commit。
3. 自然进入PerformanceDirector并播放T1-T5，最后到ROUND_RESULT。
4. 每次公开动作、状态变化与关键event必须带同一连续时钟的timestamp、frame index和session state。
5. 总时长45-75秒；玩家阅读／编辑时间必须分布在真实状态段中，不得在完成编辑后用author_plan_time、sleep或单独加钟伪造。
6. fixture_load_count=0、direct_draft_mutation=false、direct_phase_injection=false、authored_by_input=true、preview_execute_same_resolver=true。

自动化可用确定性输入节奏，但必须在连续Scene帧中逐步发生；无需声称真人完成速度、物理手柄回放或FUN PASS。

## 3. 禁止改动

- 不改88/89/92冻结的投影、相机、route family、端点、步数、动作、时序、socket、world result、A/B责任数值。
- 不改已通过的12张视觉内容，除非连续trace重抓机制机械要求更新manifest/hash；不得借机改产品设计。
- 不接真实美术，不开Call02、UA91、G2-B、Default Entry、save、Runtime或Canon。
- 不把旧测试期望改成接受新玩法哈希；B R1/R2继续精确c3b307.../f09de0...。

## 4. 必交补证

- continuous-player-trace-A.json
- continuous-player-trace-B.json
- continuous-player-trace-validation.log
- 更新后的natural-sequence/actual-frame manifest或明确supersession readback
- 最后一轮全回归日志，时间必须晚于最终源码与测试文件；06-completion-report.md证据入口必须指向该最终日志
- 更新后的06-completion-report.md与delivery-hashes.sha256

## 5. 完成状态

仅当上述证据独立复核通过，Task89才可重新进入P89制作人签收。当前保持：

- REGISTRATION_SUPPORTED
- CURRENT_TOPOLOGY_SUPPORTED
- FIRST_READ_SUPPORTED_FOR_LOOKDEV
- COMPLETE_CONTINUOUS_PLAYER_TRACE_NOT_YET_PROVEN
- FUN_NOT_PROVEN
- CALL02_ALLOWED=false
