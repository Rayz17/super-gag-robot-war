# 剧情、设定与制作索引

> 本页由 `scripts/build_story_workspace_index.py` 根据机器 Registry 与 Story Chain 生成。
> 不要手改状态；修改源表后运行 `python3 scripts/build_story_workspace_index.py --write`。

## 一分钟入口

- **只读故事：** [C01章节Reader](V35.9/rebuild/reader/C01-闭馆以后万机出击.md) -> [C02章节Reader](V35.9/rebuild/reader/C02-章节连续阅读稿.md) -> [C03章节Reader](V35.9/rebuild/reader/C03-章节连续阅读稿.md) -> [C04E01《断冠来袭》](V35.9/rebuild/reader/episodes/C04/C04E01-Reader-v1.md) -> [C04E02《先给七号一副身体》](V35.9/rebuild/reader/episodes/C04/C04E02-Reader-v1.md)。
- **只看当前内部结论：** C04尚未进入Reader审定；先查Story Chain。
- **查当前章结束时谁在哪里：** [C04状态账](V35第四层逐章完整总纲/C04/C04-机体人物分支状态账.tsv)。
- **查下一生产门：** [C04 Story Chain](V35.9/rebuild/manifests/C04-story-chain.tsv)。
- **查机器状态：** [六层生产看板](V35六层创作生产看板.md)。

## 当前创作层

| 层级 | 作用 | 状态 | 主文档 |
| --- | --- | --- | --- |
| `L1` | 主题与体验宪章 | `passed` | [V35主题玩家幻想与作品体验宪章-2026-07-18](V35主题玩家幻想与作品体验宪章-2026-07-18.md) |
| `L2` | 定位与全剧总发动机 | `passed` | [V35故事定位世界冲突与全剧总发动机-2026-07-18](V35故事定位世界冲突与全剧总发动机-2026-07-18.md) |
| `H0` | 世界机制与Canon横向底盘 | `passed_with_open_candidates` | [V35世界机制与创作接口设定基线-2026-07-19](V35世界机制与创作接口设定基线-2026-07-19.md)<br>[authority_manifest](../data/canon/authority_manifest.tsv) |
| `L3` | 全剧结构母盘 | `passed` | [V35全剧结构母盘-候选v1-2026-07-20](V35全剧结构母盘-候选v1-2026-07-20.md)<br>[V35全剧长线交叉校验板-结构母盘v1-2026-07-20](V35全剧长线交叉校验板-结构母盘v1-2026-07-20.md)<br>[V35-G5-02定向融合正式迁移回执-v1](V35结构再设计/V35-G5-02定向融合正式迁移回执-v1.md)<br>[V35-C02融合D案审定与五话容量迁移-2026-08-05](V35结构再设计/V35-C02融合D案审定与五话容量迁移-2026-08-05.md) |

## 当前生产序列

| 章 | 状态 | 故事 | 完整总纲 | 制作入口 |
| --- | --- | --- | --- | --- |
| C01《闭馆以后，万机出击》 | `user_accepted` / Working / 用户审定 | [章节Reader](V35.9/rebuild/reader/C01-闭馆以后万机出击.md) | [剧情总纲](V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md) | [本章索引](V35.9/rebuild/chapters/C01/README.md) |
| C02《木桶街，万机初开》 | `user_accepted` / Working / 用户审定 | [章节Reader](V35.9/rebuild/reader/C02-章节连续阅读稿.md) | [剧情总纲](V35第四层逐章完整总纲/C02/C02-完整剧情总纲.md) | [本章索引](V35.9/rebuild/chapters/C02/README.md) |
| C03《工务城，谁在让城市站着》 | `user_accepted` / Working / 用户审定 | [章节Reader](V35.9/rebuild/reader/C03-章节连续阅读稿.md) | [剧情总纲](V35第四层逐章完整总纲/C03/C03-完整剧情总纲.md) | [本章索引](V35.9/rebuild/chapters/C03/README.md) |
| C04《天空铸环，谁给机魂一副身体》 | `episode_e03` / Candidate / 待用户验收 | 缺失 | [剧情总纲](V35第四层逐章完整总纲/C04/C04-完整剧情总纲.md) | [本章索引](V35.9/rebuild/chapters/C04/README.md) |

## 未来章节

C06-C22只读取第三层结构职责。它们的旧同名稿、旧话卡和旧审稿都不是当前正文。

| 章 | 第三层标题 | 候选话数 | 当前状态 |
| --- | --- | ---: | --- |
| C06 | 星火乐园，全挂完全版出击 | 4 | `not_started` |
| C07 | 错版合体大会，谁来组成头部 | 3 | `not_started` |
| C08 | 白舰战役，活着撤退才是主目标 | 4 | `not_started` |
| C09 | 三重防线，二十七年的守城者 | 4 | `not_started` |
| C10 | 三法城，保护到不许活 | 3 | `not_started` |
| C11 | 百机开馆祭，四战区同日 | 5 | `not_started` |
| C12 | 开馆以后，我们真的住在这里 | 2 | `not_started` |
| C13 | 没有万机馆的一天 | 3 | `not_started` |
| C14 | 万机馆暴走，家被分成三艘 | 5 | `not_started` |
| C15 | 二十七年迟到的火花 | 4 | `not_started` |
| C16 | 欢迎回来，不等于回到原位 | 4 | `not_started` |
| C17 | 失败报告来杀现在 | 4 | `not_started` |
| C18 | 完美假馆，每个人都被爱过 | 4 | `not_started` |
| C19 | 天穹联装，我们共同造过的神 | 4 | `not_started` |
| C20 | 全相环，唯一胜利窗口 | 5 | `not_started` |
| C21 | 最强机体的普通一周 | 3 | `not_started` |
| C22 | 万机殿，直到各自回应 | 5 | `not_started` |

## 目录职责

- [`reader/`](V35.9/rebuild/reader/README.md)：玩家可读故事与单话故事源。
- [`chapters/`](V35.9/rebuild/chapters/README.md)：每章制作材料的简洁入口，不保存第二份正文。
- [`V35第四层逐章完整总纲/`](V35第四层逐章完整总纲/README.md)：完整总纲、预生产、导演、战斗、物理与演出规划。
- [`reviews/`](V35.9/rebuild/reviews/README.md)：最终验收与过程审稿；默认只读最终验收。
- [`manifests/`](V35.9/rebuild/manifests/README.md)：机器状态与哈希，判断当前性的唯一依据。
- `_history/`：退役稿与审稿过程证据，只在追溯或打捞高光时使用。

## 旧版本原则

旧文档不删除，因为它们仍承担素材、决策来源和创作演化证据；但它们不再逐项列在本页。
需要追溯时先查 Design Graph 的 `doc_registry.tsv`，再按 `History` 状态打开具体文件。
