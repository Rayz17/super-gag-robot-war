# C02 Creative First 隔离烟测

本请求只验证生产源隔离、精简作家上下文与正向声线装配，不代表C02新稿或新的故事裁决。

```json
{
  "schema_version": 2,
  "chapter": "C02",
  "previous_chapter": "C01",
  "next_chapter": "C03",
  "experiment_mode": "creative_first_production_isolation_smoke",
  "creative_material_mode": "off",
  "writer_material_mode": "none",
  "prior_state_file": "docs/superpowers/specs/story-runtime/production/smoke/C01-exit-state-smoke.md",
  "writer_context_max_chars": 18000,
  "writer_carry_in": [
    "闭馆夜接近天亮时，万机馆以百余米巡展舰形态离开原城，旧航行系统只能抵达邻近站点。",
    "纪存、唐胶、兜灯、跌跌、机器犬与馆守Z随舰，七海留在原城接受内部调查。",
    "馆守Z在C01失去原装右前臂，临时巡展臂可抓握、放锚和搬运。",
    "万机馆需要安全泊位、补给、完整检修与能长期工作的主循环部件。",
    "一台无标志白色采样机带走馆守Z右臂残片，玩家只知道有人正在收集战斗样本。",
    "唐胶认得木桶街来电者，熟悉当地生态，也在躲避一段旧关系。"
  ],
  "minimum_foundation_selected": 4,
  "minimum_canon_selected": 8,
  "minimum_material_selected": 0,
  "query_terms": [
    "C02 木桶街 万机馆主循环转子 纪存 唐胶 兜灯",
    "货柜领袖 旧拳王 馆守Z 机器人大战"
  ],
  "canon_seed_keys": [
    "entity:CH_JICUN",
    "entity:CH_TANGJIAO",
    "entity:CH001",
    "entity:MECHA_WANJI_MOBILE_CHASSIS",
    "entity:MECHA_WANJI_MAIN_CIRCULATION_ROTOR",
    "entity:V353U001",
    "entity:V353U043",
    "entity:V353U048"
  ],
  "contract_entity_keys": [
    "entity:CH_JICUN",
    "entity:CH_TANGJIAO",
    "entity:CH001",
    "entity:MECHA_WANJI_MOBILE_CHASSIS",
    "entity:MECHA_WANJI_MAIN_CIRCULATION_ROTOR",
    "entity:V353U001",
    "entity:V353U043",
    "entity:V353U048"
  ],
  "entity_state_contracts": [
    {
      "entity_id": "CH_JICUN",
      "incoming_state": "第一次作为巡展负责人面对外部共同体。",
      "allowed_changes": "主动争取部件、识别伙伴并带队完成逆转。",
      "required_outgoing_state": "以领队身份决定前往工务城。"
    },
    {
      "entity_id": "CH_TANGJIAO",
      "incoming_state": "回到熟悉的木桶街，带着旧人脉、手艺和未解决的过去。",
      "allowed_changes": "公开一部分维修史，并让别人学会复做关键工艺。",
      "required_outgoing_state": "带着更新后的街区关系继续随舰。"
    },
    {
      "entity_id": "CH001",
      "incoming_state": "负责馆守Z与万机馆的现场整备。",
      "allowed_changes": "主导一项改变运输或战斗结果的机械方案。",
      "required_outgoing_state": "带着可在工务城落地的止动方案上舰。"
    },
    {
      "entity_id": "MECHA_WANJI_MOBILE_CHASSIS",
      "incoming_state": "百米级巡展舰刚离开旧址，旧主循环系统只能支撑短程航行。",
      "allowed_changes": "取得并安装全尺寸主循环转子，恢复前往工务城的有限航行能力。",
      "required_outgoing_state": "装入主转子并取得木桶街回访泊位，校正工作留给C03。",
      "control_or_identity": "万机馆的移动舰体，由岗位组协同操作。"
    },
    {
      "entity_id": "V353U001",
      "incoming_state": "18米馆守Z带着C01失去原右臂的战损随舰抵达。",
      "allowed_changes": "以单臂、重盾和巡展臂完成搬运与主力战斗动作。",
      "required_outgoing_state": "保持单臂状态继续随舰。",
      "control_or_identity": "旧守护者是馆守Z唯一机魂人格。"
    },
    {
      "entity_id": "V353U043",
      "chapter_aliases": "货柜领袖",
      "first_use_name_rule": "首次写明火种货柜领袖，随后使用货柜领袖。",
      "incoming_state": "全尺寸载具生命在木桶街活动，拥有独立人格与作业变形能力。",
      "allowed_changes": "完成首控、护送与独立选择。",
      "required_outgoing_state": "与万机馆同行前往工务城。"
    },
    {
      "entity_id": "V353U048",
      "incoming_state": "完整退役拳击机器人仍在木桶街地下擂台。",
      "allowed_changes": "用身体、经验和战术打完一场作品级非致命决胜。",
      "required_outgoing_state": "正式加入万机馆主力。"
    }
  ],
  "core_character_contracts": [
    {
      "entity_id": "CH_JICUN",
      "chapter_role": "离馆后的实际领队",
      "chapter_desire": "让万机馆拥有继续旅行的身体，也赢得第一批愿意同行的机器人。",
      "must_active_function": "主动选择争夺方式，并组织不同机体完成一次局势逆转。",
      "must_change_or_reveal": "承认自己想拥有一支能并肩战斗的队伍。",
      "relationship_obligation": "面对同伴对风险和去向的不同判断。",
      "next_chapter_handoff": "亲自决定前往工务城。",
      "cannot_reduce_to": "审批员或被动受难者"
    },
    {
      "entity_id": "CH_TANGJIAO",
      "chapter_role": "木桶街本地关系发动机",
      "chapter_desire": "拿到救命件，也保住维修痕迹背后的真实经历。",
      "must_active_function": "用手艺和旧人脉分别解决一个别人解决不了的问题。",
      "must_change_or_reveal": "把个人手艺交给更多人复做。",
      "relationship_obligation": "与兜灯发生具体的手艺分歧和互相补位。",
      "next_chapter_handoff": "把全尺寸工程问题交给陆衡。",
      "cannot_reduce_to": "模型百科或吐槽机"
    },
    {
      "entity_id": "CH001",
      "chapter_role": "舰体安全与馆守Z整备负责人",
      "chapter_desire": "拿到部件，同时让馆守Z和万机馆以完整身体继续旅行。",
      "must_active_function": "提出并执行一项改变巨件运输或战斗结果的机械方案。",
      "must_change_or_reveal": "允许唐胶和街区工匠参与复核。",
      "relationship_obligation": "与唐胶在动手解决问题时产生火花。",
      "next_chapter_handoff": "带着可在工务城落地的止动方案上舰。",
      "cannot_reduce_to": "检查员或唐胶助手"
    }
  ],
  "new_entity_admissions": [],
  "exclude_node_patterns": [
    "^scene:.*C02",
    "^scene:V359-C02"
  ],
  "foundation_exclude_heading_patterns": [
    "旧二十章结构实验"
  ],
  "foundation_seed_headings": [
    "3.1 第一幻想",
    "6.1 投射的是共同记忆",
    "1.2 总发动机句",
    "5.1 机魂的稳定定义"
  ],
  "canon_top_k": 8,
  "graph_seed_top_k": 8,
  "graph_hops": 1,
  "foundation_top_k": 4,
  "material_top_k": 0
}
```
