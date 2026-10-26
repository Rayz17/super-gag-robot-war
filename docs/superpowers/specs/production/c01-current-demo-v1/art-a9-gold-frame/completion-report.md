# C01E02 A9 Phase GF｜完成报告

## 完成项

- `GF-PLAN 1280×720`：正式雨夜地图局部、Q/SD馆守Z/BREAKER/小体/应急车、纪存路线判断、规划UI、路线/朝向/保护/威胁与五时点。
- `GF-CONTACT 1280×720`：同场景首次巨体接触、体量差、承力支点、后滑、道路翻起、雨水飞散、侧甲炮击、红缝聚光、小体被挡开与执行态UI退让。
- 同一墙挂重盾源层：三道旧痕，冷态，未取得。
- 50%可读性并排板与馆守Z/纪存/BREAKER身份叠图。
- 源层说明、来源回执、技术检查、提示词和SHA清单。

## 方法

- 用户可见角色、机体、地图、FX和道具均来自内置 ImageGen 正式生成/编辑流程。
- FFmpeg只用于尺寸统一、参考拼板、alpha提取、UI图素复用和精确中文装配。
- 未调用 Pillow、ImageDraw、Canvas、LibTV、CLI API 或付费批量生成。

## 状态

- 全部为 `production_quality_candidate`。
- `runtime_allowed=false`。
- `runtime_handoff=none`。
- 不构成 Canon 晋升、Godot 资产、exact handoff 或 Golden Turn 开工授权。

## 真实限制

- 双帧是视觉目标帧，不是可拆分的最终地图、Sprite、Atlas或FX序列。
- A4拓扑已作为构图来源，但当前画面不声明像素级格位/投影一致性；用户 Gold Frame 通过后才应建立正式地图母版和单位资产。
- 机体在接触态有剧情性遮挡；身份叠图用于确认头冠、胸甲、前臂、红缝与体量关系，最终动画仍需分层Rig/姿态母版。
- 最终质量结论由制作人统一展示并回收用户判断，本任务不自行签署通过。

Phase GF 完成，立即停止。未进入 Golden Turn、完整 Atlas、Cut-in、声音、LibTV、Godot 或 Runtime。
