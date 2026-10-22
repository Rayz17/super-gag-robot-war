# Story Runtime显式来源查询请求

新写作默认使用author_first_v1；下面是结构示例，路径、SHA与引文必须替换为真实核对的来源。不得直接编译占位示例。

```json
{
  "schema_version": 4,
  "context_policy": "author_first_v1",
  "request_id": "C04-IDEATION-001",
  "runtime_phase": "ideation",
  "chapter": "C04",
  "active_character_ids": [],
  "active_entity_ids": [],
  "source_cards": [
    {
      "id": "PREVIOUS-EXIT-01",
      "kind": "fact",
      "authority": "working",
      "source": "已核实的项目内来源相对路径",
      "sha256": "真实来源SHA256",
      "quote": "包含必要因果与否定条件的完整原文摘录",
      "audience": "author"
    }
  ],
  "writer_view_budget_chars": 24000
}
```

## 阶段

- `ideation`：决定值得讲的故事，按真实分歧给方案，不机械凑三案。
- `research`：按需求查Current、Candidate Support和素材库，不替主笔选案。
- `entity_model`：选案后锁活动人物、机体、敌人、地点及其知识/控制/存在状态。
- `scene_plan`：人物选择与情势构成简洁场面链，不预写全套动作。
- `play_concept`：与梗概共同构思玩家可改变的局面、固定结果与可选方法，不写详细数值和镜头。
- `draft`：只装入已选场面链、活动人物切片和必要事实。
- `review`：默认`review_scope=cold_reader`，不读取作者答案；逻辑/制作复核显式使用`design`，揭盲旧稿比较使用`benchmark`，三者不得混用。
- `writeback`：用户确认后记录状态差量，不自动迁移Canon。

同一个章节可以按需要多次查询任意阶段，不要求每层只调用一次。
source_cards的kind分别为fact、future_obligation、creative_material、presentation_option；来源身份与输入用途分别记录。必需事实/未来限制与活动人物不截断，可选卡只能整条省略，超预算先缩小问题。

冷读使用runtime_phase=review、review_scope=cold_reader。只传audience=known_prefix的已知fact与audience=reader_text的待审正文，不传人物模型、作者计划或后台答案。引文必须原样存在于来源，不能把作者解释伪装成原文。

旧请求需要历史复现时显式写context_policy=legacy_inspection。其输出不得用于新写作或证明本轮已使用新方法；不要批量重建旧包。
