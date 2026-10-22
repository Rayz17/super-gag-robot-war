# C12 Codex Merge Plan（V31.2 本地合并完成）

状态：v31_2_local_reader_layer_merged。

说明：本章未声称已通过 Notion GUI/Fable 5 实机生成。当前执行的是 Fable Writer Room Hub 方法的本地化版本：

1. Codex读取V31 episode packet、章节稿、canon/pipeline规则与V31.1覆盖层。
2. Codex按Episode Capsule口径为每话整理剧情事实、机体、玩法、关系与下一话债务。
3. 以Fable三轴（剧情可读性、台词自然度、关系张力）重写 `Reader Synopsis / 可读剧情层`。
4. Codex将该层合并回本地 C08-C15 episode packet，并保留旧制作源稿、玩法字段、ledger和验证链。

采纳原则：
- 已采纳：更像剧情的连续流程、身体化动作、关系刺点、燃泪梗落点、下一话债务。
- 未改变：canon、机体名单、玩法主规则、状态变量和章节主线方向。
- 后续：若之后实际运行Notion/Fable GUI，应以本V31.2层作为输入，而不是回到旧迁移稿。
