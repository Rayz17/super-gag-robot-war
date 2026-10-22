# Story Runtime 生产源隔离

本目录决定资料能否进入实际写作调用。Canon继续保存完整事实和历史；这里负责生产可见性。

## 四层

1. `current_fact`：Hard / Working 且 active。编译器可检索，作家只读取本场需要的短事实卡。
2. `creative_material`：IP、名场面、关系、喜剧、现实案例与总纲候选。主笔先确定场面方向，再按记录ID点名准入。
3. `history`：旧Reader、旧版本、效果实验和`_history`。只供追溯或定向恢复。
4. `postwrite_lint`：坏句、坏结构和审稿案例。只在正文完成后检查。

`production_source_policy_v1.tsv`是机器可读入口。默认写作上下文只含：

- Creative First最小内核；
- 当前章的一句话发动机和带入状态；
- 当前场涉及的紧凑事实；
- 核心人物当场欲望；
- 用户认可的正向声线样本。

候选素材、旧Reader、坏句示例、审稿报告和原始合同不进入默认作家上下文。

## 人物与对白调用

重要角色的人物小传不是只在建模阶段读取一次，也不能依靠主笔记忆。每个关键ADV、关系场和高风险战中通讯进入正文前，draft pack必须从稳定人物模型按场提取：

- 此刻想得到什么、在怕什么；
- 与当前听众已经熟悉到什么程度；
- 目前知道什么、误解什么、不能知道什么；
- 压力下会先做什么动作，句子通常多长；
- 一小段已经认可的正面声线样本。

这份切片只交给主笔。冷读审稿不得读取人物小传，只能从正文判断人物是否成立；设计审稿才可在冷读完成后对照模型检查漂移。C03对白返修的场景级示例见`C03-dialogue-repair-2026-08-06/01-C03主笔人物与听众切片.md`。

## 构建与检查

```bash
python3 scripts/build_story_runtime_production_corpora.py
python3 scripts/check_story_runtime_production_isolation.py
```

生成物位于`story-runtime/generated/production/`，可以删除并重建。
`build_story_runtime_obsidian_vault.py`会在重建图谱后自动重建这批生成物；
其`--check`也会把生产语料缺失或哈希漂移视为失败。
