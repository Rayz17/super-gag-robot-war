# 超GAG角色-机体-美术锁定审计 v02

日期：2026-06-27

更新：2026-06-28，锁定表已扩展为覆盖 `pilot_cast.tsv` 全 76 条参战角色/群体/机体人格。

## 结论

项目里已经有三类基础资料，但之前没有一张“制作锁定表”把它们合并：

- `pilot_cast.tsv`：有 76 条参战角色/驾驶员/单位对应，是参战规模和机体关系的底表。
- `character_dossiers_core.tsv`：有 16 个核心角色的小传、欲望、恐惧、语气禁区，是写对白和人物弧线的底表。
- 美术资产 session：已经产出多个角色/机体方向，但有旧稿、新纠错稿、待拆分稿并存，不能直接无脑引用。

本轮新增并扩展 `data/canon/character_mecha_art_locks.tsv`，作为当前的角色、机体、驾驶员、美术参考和冲突缺口根表。以后写台本、画角色、画机体、做地图、补 canon 实体，优先查这张表。

## 新增文件

- 机器可读锁定表：`docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv`
- schema：`docs/superpowers/specs/data/canon/references/schema.md`
- canon 查询入口：`scripts/canon-query.sh art <关键词>` 或 `scripts/canon-query.sh lock <关键词>`
- 烟测：`scripts/canon-smoke-test.sh`
- 图谱登记：`doc_registry.tsv`、`graph_nodes.tsv`、`graph_edges.tsv`、`canonical_terms.tsv`、`consistency_watchlist.tsv`

## 校验来源

本轮对齐了以下资料：

- `docs/superpowers/specs/data/character_layer/pilot_cast.tsv`
- `docs/superpowers/specs/data/character_voice/character_dossiers_core.tsv`
- `docs/superpowers/specs/data/canon/entities.tsv`
- `docs/superpowers/specs/data/canon/wanji_roster_zone_coverage.tsv`
- `.superpowers/brainstorm/37837-1782033239/content/c-route-character-production-lock-29.html`
- `.superpowers/brainstorm/37837-1782033239/content/c-route-character-mecha-correction-31.html`
- `.superpowers/brainstorm/37837-1782033239/content/c-route-mecha-face-modes-asset-ledger-34.html`
- `.superpowers/brainstorm/37837-1782033239/content/wanji_c01_mecha_scene_asset_contract_v1.json`

## 已解决的关键冲突

1. 唐胶性别和美术方向  
   旧美术页 29 曾写成“女性/中性偏女性”。31 页纠错明确唐胶必须是男孩/青年模型修复师，`character_dossiers_core.tsv` 也使用“他”。锁定表已以 31 页纠错和 34 页台账为准，标记为 `conflict_resolved`。

2. 馆守Z尺寸和第一话状态  
   馆守Z锁定为 18m 级巨型机器人，第一话是半跪展示态和胸牌接入，不能完全站起、不能救世主式满功率出击，也不能吞掉其他展区。

3. 七海第一话出现方式  
   七海第一话不本人到场，只通过档案终端、通讯柱或封存框体投影出现。现场压力来自封存无人机、0号开启臂和采样贴片。

4. 方舟T定位  
   方舟T是远星 AI 陪伴线的小型 AI 模块/参数屏/探测器，不是巨大机体，不占万机馆格纳库的巨型机体池。C01 只能轻触，C10 正式展开。

5. R18“火种变形者”边界  
   R18 的“火种”是商品生命、玩具宇宙和变形谱系的包名/主题，不等同于 G.A.G. 本体，也不能直接写成变形金刚火种源机制。

## 当前覆盖

锁定表 v02 覆盖了五类对象：

- 第一章和 Demo 核心：纪存、兜灯、唐胶、七海、小满、阿澄、旧守护者、馆守Z、豪司、陆衡、跌跌、法务执行单位。
- 后续核心人物线：白鸢、槐、赤罡、方舟T、索引天使、勒修、雾生、葵司等。
- 参战谱系代表：R02、R03、R04、R07、R18、R23、H12 等。
- `pilot_cast.tsv` 全 76 条：包括R01到R24、S05和H09-H12隐藏包中的驾驶员、NPC、群像、Boss人格、机魂角色和生活锚点。
- 美术资产已给出当前参考的对象：唐胶/兜灯/七海、馆守Z、R02、R03、R04、R18、豪司/陆衡、小满/阿澄。

## 仍需补齐

1. 全 76 条 pilot_cast 已全部进入锁定表，但锁定强度不同。  
   已有美术参考或第一章硬规则的条目标为 `locked_current`、`current_reference`、`contract_locked` 或 `conflict_resolved`；只有文字设定的角色标为 `no_art_yet`；需要重新分离视觉方向的角色标为 `needs_redesign`。

2. canon entity 缺口仍存在。  
   白鸢、槐、赤罡、方舟T、索引天使、红面具、莉歌、跌跌，以及大部分后续章节参战角色尚未全部进入 `entities.tsv`。锁定表已先用 `subject_id` 对齐 `pilot_cast`，后续需按章节补 canon entity。

3. 美术定稿层级需要继续区分。  
   `locked_current` 是当前可依赖锁定；`current_reference` 是可参考但未最终拆分；`needs_redesign` 是方向已发现问题；`no_art_yet` 是只有文字设定。

4. 万机馆地图资产需要引用锁定表。  
   中庭、合体环廊、模型街、现实机器实验场、法务封存单位、B1机库和B2残响接口后续出图时，应同时查展区覆盖表和锁定表，避免尺寸和参战谱系漂移。

## 使用规则

写角色对白前：

```bash
scripts/canon-query.sh art 唐胶
scripts/canon-query.sh art 七海
scripts/canon-query.sh art 白鸢
```

写机体或展区前：

```bash
scripts/canon-query.sh lock 馆守Z
scripts/canon-query.sh art R02
scripts/canon-query.sh art R18
scripts/canon-query.sh coverage R18
```

写第一话战斗或法务接管前：

```bash
scripts/canon-query.sh art 封存无人机
scripts/canon-query.sh lock 0号开启臂
scripts/canon-query.sh rules 七海
```

## 下一步建议

下一步不要立刻重写大段台本。更稳的顺序是：

1. 补 `entities.tsv`：先补白鸢、槐、赤罡、方舟T、索引天使、红面具、莉歌、跌跌这些剧情和美术都会用到的对象。
2. 将美术资产 session 的后续定稿回填到 `current_art_reference` 和 `asset_status`，尤其是白鸢、槐、R03、R04、R05/S05、R06、R09、R10、R15和隐藏包。
3. 再回到逐话梗概和台本：用锁定表约束角色声音、机体尺寸、登场方式和参战关系。
