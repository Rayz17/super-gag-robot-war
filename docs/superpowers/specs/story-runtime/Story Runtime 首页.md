---
id: STORY_RUNTIME_HOME
record_type: runtime_home
authority: interface
generated: false
tags:
  - story-runtime/home
---

# Story Runtime 首页

这里是《超GAG机器人大战》的 Obsidian 知识工程入口。

> [!important] 一条真相，两层支撑
> Canon 源表负责裁决事实；Story Runtime 同时生成 Current Canon 投影和与其隔离的 Candidate Support 图。后者能编译写作合同，但不能覆盖前者。

## 立即查看

- [[docs/superpowers/specs/story-runtime/generated/图谱总览|Current Canon 图谱总览]]
- [[docs/superpowers/specs/story-runtime/generated/support/支撑图谱总览|全剧创作支撑图谱]]
- [[docs/superpowers/specs/story-runtime/generated/构建报告|最近一次构建报告]]
- [[docs/superpowers/specs/story-runtime/inbox/README|候选收件箱]]
- [[docs/superpowers/specs/story-runtime/context-packs/README|章节与单话上下文包]]
- [[docs/superpowers/specs/story-runtime/production/README|生产源隔离入口]]
- [[docs/superpowers/specs/story-runtime/production/当前可用源清单-v1|当前可用源清单]]
- [[docs/superpowers/specs/story-runtime/production/退役与隔离清单-v1|退役与隔离清单]]
- [[docs/superpowers/specs/story-runtime/production/文风污染报告-v1|文风污染报告]]
- [[docs/superpowers/specs/story-runtime/production/精简作家语料与Creative-First调用说明-v1|精简作家语料与Creative First调用]]
- [[docs/superpowers/specs/2026-07-29-chao-gag-story-runtime-harness-v2|Story Runtime Harness v2.2方法]]

## 三层工作区

| 层 | 用途 | 是否可直接编辑 |
| --- | --- | --- |
| Canon 源 | Hard / Working / Candidate / History 的正式裁决 | 只能走 Canon 迁移 |
| `generated/nodes/` | Current Canon 的 Obsidian、图谱与检索投影 | 否，运行脚本重建 |
| `generated/support/` | 总纲、生命周期、人物、玩法与对手的 Candidate 支撑图 | 否，运行脚本重建 |
| `inbox/` 与 `context-packs/` | 候选创作、需求分析、检索结果和本轮写作包 | 是 |

## 推荐用法

1. 在 Obsidian 的“关系图谱”中查看当前人物、机体、场景和万机馆空间关系。
2. 从一个章引擎创建“章节上下文需求”，明确本章需要检索的实体、机制、IP、关系和制作限制。
3. 用 v2.2生产策略编译四类合同和紧凑作家上下文；Current事实按需压缩，候选素材只在场面方向确定后点名准入，原始检索包留在后台。
4. 章节导演板和单话卡通过后，先规划场面依赖图；一次模型交互只创作一个完整场面或战斗阶段。
5. 每场通过局部因果审查后提交出口状态；较早场面改写会自动使后续失效。
6. 整话机械合成并通过接缝审查后，才生成下一话状态。
7. 用户确认剧情后，把状态回执走 Canon 迁移；重建两层投影，下一章重新编译。

## 重建命令

```bash
python3 scripts/build_story_runtime_obsidian_vault.py
python3 scripts/build_story_runtime_obsidian_vault.py --check
```

当前实现已包含四区生产隔离、精简Current事实语料、Creative First最小内核、多路检索、全剧支撑投影、章节合同编译、四层交互缓存、工具与语料哈希失效、交互级场面事务、顺序状态继承、局部审查、后代失效、整话接缝审查与写后回执。`contexts/`可按保留策略清理，正文、回执、审查与历史不可当缓存删除。旧Reader和坏句只可用于定向追溯或写后检查，不再作为初稿语料；语义好坏仍由主笔、独立审稿和用户判断。
