# B06 胸前导览席局部场景插片 — Call 01 Candidate Receipt

## 结论

`PASS_FOR_CANDIDATE_REVIEW`。本轮执行了 1 次 OpenAI built-in ImageGen 定向编辑，`0 reroll`。生成件保留了现有 B06 纪存的成人脸、黑发、深藏青博物馆外套、白衬衫、撑框回稳动作和左前臂档案终端；同时将原先的纯人物透明立绘返修为包含胸前导览席、束带、舱门框、踏步、扶手与 V10X 局部胸舱结构的叙事插片。

这只是美术 `Candidate`，不等于用户视觉接受，也不等于 Runtime/Canon/Default 通过。

## Story lock

| field | exact value |
| --- | --- |
| bridge | `BRIDGE_B_CORE_REVEAL_TO_CARRIER` |
| beat_id | `B06_JICUN_IS_STILL_INSIDE` |
| slot | `JICUN_EXITS_GUARDIAN_CHEST` |
| line | `有点响，别的没事。` |
| stage direction | `纪存从馆守Z胸前导览席进入主厅；右臂残片留在封锁广场。` |

## Pixel contract

| field | value |
| --- | --- |
| asset_type | `local_scene_insert` |
| alpha_policy | `opaque_or_edge_alpha` |
| actual file | `1024×1536`, PNG, RGB8, opaque |
| content_rect | `[40,40,984,1496]` |
| safe_crop_rect | `[72,72,952,1464]` |
| internal_negative_space_required | `false` |
| intended placement | 左侧局部场景插片；非 `1280×720` 全屏背景 |
| filter/repeat | 未绑定；Candidate 评审阶段 `n/a` |

RGB 不透明不是失败：Section 2 合同对 B06 允许不透明的矩形局部场景插片，且明确禁止为满足“人物抠图”而删掉导览席与舱内结构。

## Source isolation

| role | source | sha256 | result |
| --- | --- | --- | --- |
| sole identity/action edit target | old B06 RGBA Candidate | `5cfa39e2d5c0723f972ea758a3c85e90f27ad90b73a8020d1c05d87136a9a569` | only Jicun identity/action preserved |
| supporting current environment material reference | CML130 V10X scoped sole positive parent | `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade` | only red/deep-navy/white/amber/gold chest-interior language used |
| forbidden | CML008 and old Guardian Z visual history | `n/a` | not supplied to ImageGen; not used |

## Visual gate

| gate | review result |
| --- | --- |
| Jicun identity | pass: same adult face/age/hair, no glasses, same coat/shirt/trousers/shoes |
| arm terminal | pass: cyan left-forearm archive terminal remains prominent; no readable map UI/text |
| action semantics | pass: braced hand, shifted center of gravity and stepping exit read as post-impact steadying; no pointing/piloting |
| guide-seat semantics | pass: seat back, short frame, loose harness and adjacent hatch/step read as a compact guide seat; no yoke/joystick/fire-control panel |
| local cabin identity | pass: deep-navy ribs, red chest lining, narrow white load-bearing frame and amber lights follow V10X material language |
| forbidden content | pass: no whole Guardian Z, enemy, exterior battle, extra person, caption, dialogue UI, logo or watermark |
| 50% composition | pass: person + seat + hatch remain a single readable relationship; head, hands and feet stay inside crop |
| 100% crop | pass: face, bracing hand, terminal, seat, harness and threshold retain clean anatomy/structure |

## Delivery

- Raw call result: `../raw/JICUN_B06_CHEST_GUIDE_SEAT_LOCAL_SCENE_RAW_CALL01.png`
- Candidate delivery: `../delivery/JICUN_B06_CHEST_GUIDE_SEAT_LOCAL_SCENE_CANDIDATE_V1.png`
- 50% full QA: `../qa/JICUN_B06_LOCAL_SCENE_50PCT_FULL_QA.png`
- 100% identity/action QA: `../qa/JICUN_B06_LOCAL_SCENE_100PCT_IDENTITY_ACTION_CROP_QA.png`
- 100% seat/threshold QA: `../qa/JICUN_B06_LOCAL_SCENE_100PCT_SEAT_THRESHOLD_CROP_QA.png`
- Combined 50/100 QA: `../qa/JICUN_B06_LOCAL_SCENE_50_100_CROP_QA_BOARD.png`
- Reproducible QA builder: `../../build_b06_local_scene_qa.py`

## Lifecycle boundary

- `candidate=true`
- `user_visual_acceptance=false`
- `runtime_allowed=false`
- `runtime_handoff=none`
- `runtime_bound=false`
- `canon=false`
- `default=false`
- No Godot, HUD, story, binding, resolver or Runtime file was changed by this delivery.
