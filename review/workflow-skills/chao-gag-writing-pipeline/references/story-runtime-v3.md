# Story Runtime：按问题组装资料

## 当前入口

新写作使用 `compile_story_runtime_stage_context.py` 的默认 `author_first_v1`。旧自动L1-L3/场景表装载只在显式 `legacy_inspection` 下复现，writer_ready永远false，不是新主笔入口。

模板：`docs/superpowers/specs/story-runtime/templates/Story-Runtime-v3阶段查询请求模板.md`。

## 请求与选择

先按Canon入口裁清本次需要的来源，再用source_cards记录完整原文：
`id / kind / authority / source / sha256 / quote`。

kind是fact、future_obligation、creative_material或presentation_option。authority另标hard/working/candidate/history。二者不等价：Working母盘中的未来实现不是已经发生的事实。编译器验证字节与类型，不替作者裁定语义权威。

提案、研究、人物核对、场面规划、play_concept、正文和复核都可以查询，不强制七次调用。没有必要资料就不查全量库。

- 已发生前情、当前关系、知识、在场与能力限制用fact卡。
- 未来职责与保留项用future_obligation卡。
- 可选IP、日常与梗用creative_material卡，可以不用。
- 空间/战斗/演出候选用presentation_option卡，不是标准答案。
- 选中的人物通过active_character_ids复用现有模型的戏剧核心与正面声线；实体通过active_entity_ids读取当前Canon，不自动加载全章角色。模型不代替本场关系事实。
- 不自动读取旧同章Reader、L3邻章全文或完整工程板。选中资料有冲突先停，不靠压缩掩盖。

## 预算与缓存

主笔默认只读06-writer-view.md。必需事实、未来限制、选中人物与实体整条保留，超预算则BLOCKED，不能使用截断版继续写。可选资料按请求顺序整条加入；被省略的ID列在视图与manifest，按需微查。

manifest绑定源字节、请求配置和编译器版本。角色小传/声线与生成模型不一致时阻断；不得重用旧缓存假装新方法。未知token与费用记UNKNOWN，本地缓存不是计费证明。

完整引用不代表要读全文件。选取能独立保留因果和否定条件的原文段，不能只摘有利半句。机器不能自动证明摘录充分。

## 冷读隔离

review_scope=cold_reader只收：
- audience=known_prefix且kind=fact：玩家已知前情；
- audience=reader_text：本轮待审正文。

不得传active cast/entity、作者卡、旧current_state_sources或selected_scene_chain。冷读先复述事件与喜好，不读取设计答案。design和benchmark是独立范围，不能反改首读结论。

## 正式回写

用户确认前只有Candidate状态。writeback生成差分提案，不自动提升Canon或接受回执。正式封存、invalidation和机械合章由Pipeline处理。

## 命令

```bash
python3 scripts/compile_story_runtime_stage_context.py \
  --request <阶段请求.md> --output-dir <独立Candidate资料包目录>
python3 scripts/test_story_author_context.py
```

不要自动重建全部历史上下文，不删除Reader、回执或他人缓存。当前方法和写作停止点见项目2026-09-05方法合同及C04写作计划。
