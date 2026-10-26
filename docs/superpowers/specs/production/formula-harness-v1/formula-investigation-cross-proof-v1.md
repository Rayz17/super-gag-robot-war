# INV_T1 · 三方互证输入与消费者

2026-09-18，Candidate技术制作合同。对应140与chapter-slices的C02E03首包；不是体验或美术验收。保留既有工程试验消费者，按生成payload的`interaction_profile=cross_proof_v1`选择此调查消费者。

## 生产入口

reading.stages中使用`kind=investigation`、`template=INV_T1`、`cross_proof={"path":"artifacts/formulas/production-lab-v1/inputs/cross-proof-m-c02-v1.json"}`；来源标题/引用、read_facts/write_facts沿原生产合同。defaults={}、lines=[]、actor_aliases=[]，不继承旧运输试验模板的实验/数值/结果。cross_proof仅允许用于INV_T1。

引用文件结构：

```text
schema_version: 1
candidate: true
not_canon: true
runtime_allowed: false
user_visual_acceptance: false
source_documents: [{id, path, sha256}]
case: {
  id, title, question, intro, start_room_id,
  groups: [{id, label}],
  rooms: [{id, title, description, actor_name, spawn:[x,y],
    walkable:[[x,y],...], blockers:[{id,polygon:[[x,y],...]}],
    exits:[{id,label,to,at:[x,y],arrival:[x,y]}],
    background_alias?: string}],
  observations: [{id,group_id,room_id,label,source,time_label,text,
    at:[x,y],walk_to:[x,y],source_document_id,source_quote,
    exhibit?:{image_alias,caption}}],
  interpretations: [{id,label,required_evidence:[observation_id,...],
    conflicting_evidence:[observation_id,...],
    incomplete_text,conflict_text,confirmed_text,scope_note,
    effects:{WORLD_FACT:bool},source_document_id,source_quote}],
  continue_label, incomplete_leave_label
}
```

所有位置是1280×720逻辑画面的场景坐标；工作区域x=32..880、y=130..622。右侧是当前物件的短说明，打开记录后覆盖比较页；用户无需填写这些制作坐标。房间导航使用现有FormulaLabRoomNavigation，不在通路到达前取证，不把远距点击当已看见物证。已有图像通过资产别名绑定；没有图像的制作预览明确保留美术缺口，不算完成章节包。

来源文件须位于仓库内，SHA-256与实际内容一致。每条观察/解释的source_quote必须存在于所引用文件中；只能证明有明确来源绑定，不能用字符串命中替代主对话的剧情审读。三类剧情来源可以由同一有效Reader提供；source_documents也可保留未逐条引用的验收/身份文件，仍进入依赖核验。生产source_map保存输入和每份来源；runtime payload只保留玩家文字及绑定所需字段，制作文件路径与哈希不进正面UI。

生成preset保持formula_id=FML_INVESTIGATION、scene_type_id=INV_T1、fixture_only=true；payload包含interaction_profile、case、world_facts。可选background_alias编译为房间background_path，别名必须声明kind=background，通过资产检查并加入来源。资产清单允许portrait、background、evidence三种kind；portrait与background仍只允许PNG，evidence允许PNG或安全SVG。安全SVG必须是合法XML、根元素为svg，并具有正数有限width/height或有效viewBox；只接受svg/g/path/rect/circle原生元素，禁止DOCTYPE、ENTITY、脚本、事件属性、foreignObject、image及任何外链或外部URL引用。observation.exhibit若存在，必须且只能包含非空image_alias与caption，image_alias必须解析到kind=evidence的已声明资产。caption只说明原件图是什么或供玩家核对什么，不替玩家完成比较或写出结论；这是作者与审读者的内容审查要求，生产与Runtime不使用自然语言关键词黑名单，只机械校验结构和非空。编译后runtime exhibit只保留image_path与caption；image_path必须是res://assets/formula_lab内实存Texture2D。exhibit资产与完整哈希进入flow/source_map重建依赖；无exhibit的既有输入与runtime payload不增加字段。消费者与独立runtime contract都进入重建依赖；不可声称仍执行旧INV_T1机械数值。当前支持将完成现场作为后续Narrative背景；不支持next_investigation_briefing，生产与Runner均拒绝该用法。

## 玩家状态与核对

开始时解释未选、依据未选、观察未记录。现场走到物件才记下观察；重复查看不重复写入。选择解释和勾选依据都是可改的草案，不写世界。依据只能从已实际观察的记录中选取。

点击“核对这个说法”时：

1. 未选解释：提示先选说法，不写事实。
2. 已观察到所选解释的任一conflicting_evidence：指出相关矛盾，保持可修改；不能通过不引用已知矛盾材料来绕过。
3. 所选依据缺少该解释的required_evidence，或没有覆盖全部声明groups：证据不足，说明哪类来源尚未作为依据；系统生成的物件名称只列已记录但未引用的项，不提前暴露未发现物件。作者提供的incomplete_text仍须人工审读，非空校验不保证无剧透。
4. 条件满足：显示解释的confirmed_text和scope_note，写入它声明的effects（这些fact必须属于stage.write_facts）；保留已观察记录与依据供回看。

至少三类不同来源、两种解释；记录/解释/地点/出口ID唯一，引用必须有效。每条可确认解释至少有正向依据；至少一种可达解释须能写入已声明事实，不能接受全部解释冲突或均无效果的死局。错误解释允许空effects。全部房间从起点可达且能回到起点；门两端落点、观察接近点和路径均校验。几何合法仍不能保证图中无木箱/栏杆，绑定美术后必须实际行走核验。

新增材料、改选解释或调整依据会撤下过期反馈并要求重新核对。返回记录恢复刚才条目与可见焦点；确认后的页面仅回看记录，不再提供可编辑的解释选项。

成功后回现场仍可查看，事实不会因返回抹掉。明确“继续”才结束本stage；未确认时另有带着未完成结果离开。没有物理试验、中止窗、运输时间推进、机况损耗或Mission Clear。结果沿包runner原有fact_writes/world_facts/process_state交接，不能伪造已发生事实。

## 必要验证

顺序/重复查看不改证据；三个同类记录不能代替三来源；同材料不同解释的反馈不同；不引用已知矛盾不能绕过；未看记录不能作依据；未完成退出不写成功；重复确认/回看不重复写入；跨房间与记录返回保留选中对象和草案；Skip不自动调查或选答案。用不同ID、来源类别和结论的第二份数据验证复用。工程T0/T3既有行为回归不受影响。

本轮第一阶段只交可运行制作预览与准确的未完成项；正式完成仍要求本章必要美术、角色动作、金标对照与真实试玩，不把状态测试计成体验通过。

当前实施与实际限制见[C02E03原生回执](../../../../../artifacts/formulas/production-lab-v1/qa/cross-proof-m-c02-20260918/root-review.md)。最新隔离build为layout-v6；87项状态检查、生产器6项及Canon strict通过。真实成功交接已录，未完成离场还需原生补测；这不是完整体验验收。
