# 项目级 P1 迁移交接单 v0.1

> Status: `candidate_read_only_handoff / no_canon_write / no_story_chain_write`
>
> Evidence date: `2026-08-10`
>
> Scope: 记录本主策划包之外、会阻断后续生产的两个现行项目故障；本文件不是修复授权，也不是门实例或验收回执。

## 1. `P1-KB-PRESENCE-MODE`

### 当前失败证据

```text
python3 -B scripts/check_story_knowledge_base.py
exit=1
AssertionError: Invalid presence mode: PRES_C01E01_RIFT_SWARM
```

来源行为：

- `docs/superpowers/specs/data/canon/scene_entity_presence.tsv` 将 `PRES_C01E01_RIFT_SWARM` 的 `presence_mode` 写为 `remote_contact`；
- `scripts/check_story_knowledge_base.py` 当前只接受 `physical / remote_live / recording / work_trace / mentioned / system_effect / not_present`；
- 该记录在 `authority_manifest.tsv` 中仍是 active Working 记录，不能靠跳过校验处理。

### 需要的迁移决策

Canon owner 必须先判断 `remote_contact` 是需要正式加入模式词表的新语义，还是应迁移到既有模式。不得只为让脚本 PASS 把值随意改成 `remote_live`：敌方接触点、远程在场角色和纯系统效果不是同一概念。

### 消费者影响

- 场景实体在场投影；
- C01E01/E02 的敌方接触与揭示；
- knowledge-base 全库校验及任何依赖它的迁移门；
- Reader/gameflow 的 writer-safe presence context。

### 修复后的最低反向测试

1. 新值必须在唯一模式定义中有明确语义和允许字段；
2. `PRES_C01E01_RIFT_SWARM`、远程人物、记录回放和系统效果各有区分用例；
3. 删除模式注册或恢复非法值时，校验必须稳定失败；
4. 全库 knowledge-base 检查通过后仍须单独核对 C01 Accepted Story hash；PASS 不授权改写 Reader。

## 2. `P1-C04-PREPRODUCTION-BYPASS`

### 当前冲突证据

现行 story-chain 把 Stage20/21 及其下游板件登记为 `passed`：

```text
docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C04-story-chain.tsv
Stage20 preproduction_model = passed
Stage21 preproduction_table = passed
```

但专用校验实际失败：

```text
python3 -B scripts/check_chapter_preproduction_model.py \
  docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C04/C04-预生产实体动作表.tsv
exit=1
```

失败包括全表 `status=candidate` 不在专用Schema允许值中，以及 `character_group / mecha_group` 等非法 `item_type`。与此同时：

```text
python3 -B scripts/check_v35_story_chain.py \
  --manifest docs/superpowers/specs/剧情梗概/V35.9/rebuild/manifests/C04-story-chain.tsv \
  --next
```

仍返回 `NEXT: episode_e03`、`STATUS: invalidated`、`READY: yes`。这证明通用链检查没有消费专用 Stage21 结果，新门禁也尚未部署到 Current 链。

### 需要的修复提案

1. 在任何 `director_board` 或 Writer 前置检查中，把 Stage20 Markdown 与 Stage21 机器表分成两个真实门实例；
2. Stage21 必须绑定专用 checker 路径/版本、实际输入路径/hash、profile、结果回执和失效消费者；
3. C04 heavy profile 还必须引用真实低保真地点/尺度/双态/控制链材料，不能用“可以画”替代文件存在；
4. 先重建合法 Stage20/21，再重建受其影响的导演、战斗、物理、L4/L4.5 与 E03；E01/E02只做兼容审计，不自动废弃；
5. 若新地点/机体事实改变 E01/E02 已成立因果，再按范围化失效规则处理，禁止暗补 sidecar。

### 消费者影响

- C04 `director_board / battle_preplan / physical_board / chapter_outline / L4.5`；
- E03/E04、章Reader与后续审查；
- Runtime writer-safe context、gameflow、Previs 与资产BOM；
- C05+ 的章级预生产模板和门实例。

### 修复后的最低反向测试

1. 只要 Stage21 专用 checker 失败，`--before-stage episode_e03` 必须非零退出，`--next` 不得显示 `READY: yes`；
2. 删除任一 heavy-profile 必需图、改变其hash、引入非法 status/type，必须使 Stage21 及全部消费者失效；
3. 通用 packet checker PASS 不能覆盖专用 checker FAIL；
4. 修复后必须保存 scope、input/checker version、完整hash、receipt path/hash 与 invalidation targets；
5. E03 重新进入写作前，由用户另行裁决地点/C2方向；本交接单不构成批准。

## 3. 当前停止条件

- 本包内部可继续做只读检查、Candidate 修复提案和隔离故障注入规格；
- 未取得对应 authority owner 和用户范围回执前，不改 `scene_entity_presence.tsv`、`authority_manifest.tsv`、C04 story-chain、Reader 或 Runtime；
- 任何“全包 PASS”都必须同时报告这两个项目级 P1，直到各自有可恢复的修复提交、通过证据和范围化回执。
