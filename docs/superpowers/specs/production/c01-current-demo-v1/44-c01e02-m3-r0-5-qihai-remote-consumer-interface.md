# C01E02 M3-R0.5｜七海远程状态卡消费者接口

> 日期：2026-08-18
>
> 状态：`active interface correction / option B selected`
>
> 目标：确保 A6 七海三态存在明确程序消费者，同时不新增台词或战场权限

## 1. 选择

采用 **B：规划侧栏明确渲染七海 portrait slot 与远程频道边框**。

不采用 B00/B01 无文字弹窗。理由：常驻状态卡能在玩家首次读地图时建立七海的身份、来源与当下职能，不占用阻断式通讯节拍，也不会暗示七海正在给馆守 Z 或城市炮火下命令。

## 2. 数据消费者

`character_comms.json` 或同等 Candidate 数据文件必须新增独立于对白数组的 `presence_cards`：

```json
{
  "presence_id": "R05_PRESENCE_QIHAI_REMOTE",
  "actor_id": "CH_QIHAI",
  "display_name": "七海",
  "channel": "remote",
  "source_label": "代哥东区封存中心",
  "status_text": "本人停机令已撤回",
  "portrait_slot": "R05_PORTRAIT_QIHAI_REMOTE",
  "expression_state": "decision",
  "visible_states": ["SITUATION_REVEAL", "PLAN_EDIT", "PLAN_SUMMARY"],
  "interactive": false,
  "command_capability": "none",
  "artillery_authority": false,
  "line_text": "",
  "source_kind": "accepted_reader_fact",
  "source_ref": "C01 accepted Reader E02"
}
```

`presence_cards` 是明确的 portrait consumer，不得依赖某条 `character_comms` 对白是否触发。未来 M1 只要加载角色美术，就必须同时解析对白消费者和 presence consumer；不得因七海没有台词而把其三态判为孤儿资产。

## 3. 玩家界面

七海状态卡位于 34 号接口的右侧指令面板内，要求：

- 首次进入 `PLAN_EDIT` 后立即可见，确保试玩前 30 秒建立身份；
- 使用远程频道专属边框、轻微信号噪点和来源标签；
- portrait 使用 `decision` 状态；fallback 使用具名几何远程头像，不读取 A6 目录；
- 状态卡不覆盖地图、不弹出大型阻断对话、不抢夺当前单位焦点；
- 无按钮、无目标线、无行动点、无炮火图标、无“待命/可操作”提示；
- 只表达已验收事实“本人停机令已撤回”，不得扩写成战场命令、炮火调度或主题台词。

纪存、旧守护者、兜灯继续按 34 的本地/机魂/机况信息位置出现；七海状态卡不能替代他们的行动反馈。

## 4. M0 测试

M0 至少增加：

1. `CH_QIHAI` 在 `presence_cards` 中恰好出现一次；
2. `portrait_slot=R05_PORTRAIT_QIHAI_REMOTE`、`channel=remote`、`interactive=false`；
3. `line_text` 为空且没有 trigger→action；
4. `command_capability=none`、`artillery_authority=false`；
5. 零 handoff 时仍渲染具名几何卡且 `resource_probe_count=0`；
6. 1280×720 下状态卡不遮挡棋盘、时间线或确认按钮；
7. 正常截图不显示 Stable ID、内部权限字段或 Candidate 文案。

## 5. A6 评审要求

A6 的七海 1280×720 模拟图必须至少有一张使用上述侧栏状态卡位置，展示：

- `decision` 状态在实际缩放下的脸部可读性；
- 远程边框与人物噪点 mask；
- 来源、姓名和状态文本的程序安全区；
- 无按钮与无战场指挥权的视觉读法。

该模拟图和七海人物母版仍是 `Candidate / runtime_allowed=false / runtime_handoff=none`，只进入 U1 逐项评审。本接口不构成 exact handoff。

## 6. 停点

M0 可以用几何 fallback 实现接口并测试，但不得读取 A6 真图。A6 可以按接口制作模拟图，但不得写 Godot。真实接入仍必须等待 U1 与制作人 P1 exact handoff。
