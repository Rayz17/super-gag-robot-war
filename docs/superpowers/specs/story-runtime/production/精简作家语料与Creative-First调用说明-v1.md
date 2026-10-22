# 精简作家语料与Creative First调用说明 v1

> 状态：`RETIRED_METHOD_REFERENCE`  
> 退役日期：2026-08-01  
> 当前入口：`story-runtime/README.md`、`2026-08-01-chao-gag-story-runtime-v3-knowledge-character-rebuild.md`与`templates/Story-Runtime-v3阶段查询请求模板.md`。  
> 本文只用于追溯v2的静态最小内核和两次素材门，不得再组装新作家Prompt。

## 一、作家实际读取什么

```text
Creative First最小内核
+ 本章一句话戏眼
+ 6至12条前章正向状态
+ 本场相关人物欲望
+ 本场相关机体/地点短事实
+ 已明确准入的素材
+ 4条用户认可声线
```

默认没有“已明确准入的素材”这一段。主笔先提出并选择场面方案，随后才把具体IP、名场面、关系或文化记录ID加入。

## 二、后台保留什么

后台仍可读取：

- 全量Current Canon；
- L1至L3；
- 生命周期、阵营、玩法和关系合同；
- 848条Candidate Support与创作素材；
- 完整前章状态和精确Reader接缝；
- 12条坏句回归案例；
- History与旧稿高光。

后台负责找错、补事实和提供候选，不负责替初稿决定全部内容。

## 三、两次素材门

### 第一次：创意研究

主笔已经提出三种场面方向后，检索器可以从素材目录找候选。此时素材仍在后台。

```json
{
  "creative_material_mode": "explicit_only",
  "material_seed_ids": ["<候选记录ID>"]
}
```

### 第二次：作家准入

主笔选定真正会改变当前场面的记录后，才允许摘要进入作家上下文。

```json
{
  "writer_material_mode": "admitted",
  "writer_material_seed_ids": ["<已选记录ID>"]
}
```

第二组ID必须已经出现在第一组检索结果中。

## 四、旧兼容模式

```json
{
  "creative_material_mode": "legacy_bm25"
}
```

这个模式只用于重放旧实验或比较检索召回，不作为新写作默认值。即使使用它，`writer_material_mode`仍默认为`none`。

## 五、正向状态继承

新请求优先提供`writer_carry_in`：

```json
{
  "writer_carry_in": [
    "人物、机体、地点和伤势的正向事实",
    "上一话造成的可见变化",
    "自然发动本话的未完愿望"
  ]
}
```

编译器仍保存完整前章状态用于审稿与哈希，但作家只读这组短增量。缺少显式增量时，编译器会从前章状态中提取最多12条正向事实作为兼容回退。

## 六、检查

```bash
python3 scripts/build_story_runtime_production_corpora.py
python3 scripts/compile_story_runtime_context_pack.py
python3 scripts/compile_story_runtime_context_pack.py --check
python3 scripts/check_story_runtime_production_isolation.py
```

`check_story_runtime_production_isolation.py`会阻止：

- v1内核重新成为默认；
- Candidate素材提前进入作家上下文；
- `_history`、旧上下文包和效果实验进入生产包；
- 已知坏句进入默认内核或烟测作家上下文；
- 正向声线与负面回归案例混库；
- 精简事实语料出现Candidate或History。
