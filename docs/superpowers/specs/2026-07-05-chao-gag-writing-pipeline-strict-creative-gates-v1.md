# 超GAG写作 Episode Loop 严格创作门禁 v1

日期：2026-07-05

## 背景

V29 第一章试跑证明，旧 episode loop 可以保证文档结构齐全，却不能稳定保证“好看”。它会出现一种危险假阳性：每话都有 packet、章节文件和 prefix review，但读起来仍然小、重复、缺机体、缺名场面、缺主角大动作。

这次升级的目标不是让写作变得机械，而是让 loop 在进入下一话前拦住明显不满足机器人大战体验的稿件。

## V29 暴露的七类失败

1. 名台词/名场面重复：例如第一话和第三话都使用“我来组成头部”相关桥段，没有形成有意的 refrain。
2. 参战机体不足：开篇没有足够真实IP映射机体，盒子、展签、锚件、模块被误当成机体；进入V35长篇后又容易反过来机械要求每话塞陌生新机，导致旧机没有生命周期。
3. IP 名场面没有进入剧情：只有关键词或轻微梗点，缺少对应的场面结构、台词气势、玩法触发。
4. 主角动作太小：纪存、七海仍停在“四十秒”“签名”“水印”这类微动作，没有公共代价、权力变化、觉醒、牺牲或关系破裂。
5. 燃点、泪点、梗点缺门禁：存在“写了字段但没有场面”的问题。
6. 展舰化缺巨物演出：万机馆战舰化作为第一章高潮，必须有空间展开、巨物运动、玩家压力、见证者反应和后果。
7. 万机馆厚度不足：第一话闭馆路线没有把“万机”的馆藏规模、IP 谱系代表性和未来参战承诺展示出来。

## 2026-07-22前置门升级

严格单话Pipeline不能再直接从章级梗概启动。进入某章第一话前，Context Pack必须同时包含：

- 已通过的第四层完整章纲。
- 本章《章节导演板》《物理因果与人物站位板》《战斗与玩法预案》。三板已经逐场回答玩家可见证据、暂定演出载体、信息边界、最低资产和旁白删除判据。
- 已通过的`Cxx-章级演出承载规划.md`，其中按一次实际游玩的顺序排定舰内自由活动、ADV、探索、地图事件、SRPG、战中通讯、短动画、Cut-in、结算和可选事件。

若章级演出承载规划缺失，Pipeline必须返回`blocked_upstream_presentation_plan_missing`，不得把梗概旁白拆成角色说明、战中百科或连续ADV来补洞。单话可以细化场面，但不能临时改变本章地图轮廓、信息来源、关键资产和载体分配；确需改变时，先提交上游章纲/演出规划迁移。

统一载体语法与成本边界读取`剧情梗概/V35游戏叙事演出语法基线-2026-07-22.md`。

## 新增硬门禁

V30 及之后的厚梗概/开篇重写默认启用 `--strict-creative-gates`。

每个单话 packet 必须补充以下字段：

- `Real New IP-Mapped Units:`：真实新增 IP 映射机体。
- `Roster-Package-Class Unit:`：可作为主力、敌方、支援、隐藏、后继、Boss 或代表性参战包的机体。
- `Non-Count Anchors:`：不计入机体数量的盒子、展签、终端、维修单、锚件等。
- `IP Scene Projection:`：本话投射的名场面或经典叙事结构。
- `Burn Point:`：燃点场面。
- `Tear Point:`：泪点物件或关系回收。
- `Gag Point:`：梗点、吐槽或模玩/机器人文化槽点。
- `PV-Scale Spectacle:`：PV 级机器人演出。
- `Wanji Collection Density:`：万机馆或开馆场景的馆藏密度。
- `Wanji Collection Sample Count:`：C01E01 必填，默认至少 8 个代表性馆藏样本。
- `Protagonist Big Move:`：主角级不可逆动作。
- `Qihai/Jicun Big Move:`：七海/纪存核心动作，不能只靠“四十秒”等小安排。

V35.4正式运行还必须补充：

- `New Unit Gate Mode:`：`first_appearance` / `lifecycle_delta` / `bridge_exception`。
- `Roster Lifecycle Payload:`：无新机话中，旧机发生的可见生命周期变化。
- `Available Fleet:`：本话合法可部署机体和舰群。
- `Author Slot ID:`：本话来源作者槽。

`lifecycle_delta`只有新形态、新武器、新驾驶/机魂关系、新合体位置、新政治归属、跨舰转移、敌转友、路线锁或终局回收可以通过。普通复出、换色、数值强化、背景Cut-in和“终于又出场”不算。

## 新增 Ledger

`creative_experience_gates.tsv`

记录每话是否真正拥有燃点、泪点、梗点、PV 演出、IP 场面投射、主角大动作、七海/纪存大动作、万机馆馆藏样本数量，以及门禁结果。

`mecha_ip_first_appearances.tsv`

记录每话真实新增机体、参战包级机体、功能模块、非计数锚件，以及门禁结果。它的作用是防止把“社勇王盒子”“旧拳王手套”“留言墙”等道具误算成参战机体。

V35运行时与`unit_availability.tsv`合读：若`New Unit Gate Mode=lifecycle_delta`，首次出现数量可以为0，但必须至少有一条合格且进入场面/玩法的生命周期事件。`bridge_exception`必须给出原因和下一补偿窗口，且不得连续两话。

`quote_scene_usage.tsv`

扩展为必须记录 `episode_id`、`quote_text_or_phrase`、`quote_family`、`usage_type`、`scene_payload`、`reuse_policy`。直接名台词重复使用时，必须注明是有意反复，否则视为失败。

## 新增审稿角色

- 名台词/名场面连续性编辑：审查直接引用、名场面复用、中文玩家识别度、场面承载。
- 燃泪梗/PV 编辑：审查燃点、泪点、梗点和 PV 级机器人演出是否为真实场面。
- 万机馆文化容量编辑：审查万机馆厚度、展区谱系、馆藏到参战关系和开篇吸引力。

## 运行命令

严格模式示例：

```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py \
  docs/superpowers/specs/剧情梗概/V30 \
  --require-subagents \
  --require-chapter-reviews \
  --require-run-validation-log \
  --strict-prefix-warn-policy \
  --strict-creative-gates
```

V35正式运行追加：

```bash
--require-source-absorption --require-v35-slot-contract
```

旧稿可以用非严格模式做结构验收，但不能再据此声称“创作质量通过”。

## 对下一轮 C01 重写的影响

第一话需要重新卖出三件事：

1. 万机馆真的是“万机”：闭馆路线必须看到多层、多谱系、多尺寸、多时代的代表性馆藏。
2. 这是机器人大战：每话都有真实可识别的机体、名场面投射和战斗/玩法压力。
3. 主角团不是终端操作员：纪存、七海、白鸢必须在开篇就出现会改变权力、关系和战场的选择。

如果 C01E01 仍然只是小样例、小台词、小支援、小延迟，即使字段齐全，也必须被 strict creative gate 拦下。
