# A35 勇拳 State03 RELEASE 双拳连接返修硬门

> Date: 2026-08-25  
> Status: `PASS_FOR_USER_REVIEW_CANDIDATE / user=false / runtime=false / canon=false`

## 本轮窄范围

- 只补做一张 `State03 RELEASE`，解决此前失败稿左拳与前臂连接被遮挡的问题。
- A33 用户认可稿是唯一身份正向源；A34 State00 是唯一精确编辑目标；State01 只提供同源吸纳机构语义；State02 R1 只提供压缩锁定语义。
- 失败的 A34 State03 R1 仅在账本列为 `zero_pixel_use_do_not_use`，没有作为 ImageGen 输入，未复用任何失败像素。
- Candidate-only；没有修改 Godot、Runtime、Canon 或正式 Sprite 绑定。

## 几何预门

- 先制作无身份几何 guide，并输出 50% 检查图。
- 在 50% 下，左右两条 `肩—上臂—肘—前臂套筒/导轨—闭合拳体` 均连续可见。
- 两个肘都留在拳后；拳体没有覆盖各自腕圈和整段前臂连接。
- 两拳保持分离，拳面为封闭钝性四区甲，没有孔洞、炮口、枪管或脱离结构。
- 接触层只是一小段扁平薄层，不包围拳体，不延伸为射线、光束、环形冲击波或大面积护盾。

几何 guide 结论：`PASS_50PCT_GEOMETRY_GATE`。

## ImageGen 执行

- 模式：built-in ImageGen targeted identity-preserve edit。
- 调用次数：`1`。
- 随机 reroll：`0`。
- Prompt：`prompts/A35-STATE03-RELEASE-CONTACT-CONNECTION-FIX-BUILTIN-IMAGEGEN-PROMPT.md`。

## 输出硬门

- **双拳连接：PASS**。50% 下左、右拳后方的腕圈、双层套筒、侧向回送导轨和通向肘部的前臂结构都可连续追认；没有一只拳成为浮拳或独立抛射物。
- **肘后可见：PASS**。左右肘与上臂都没有被拳体或接触效果完全遮挡，躯干明确前压并由髋腿支撑。
- **拳面封闭：PASS**。两只拳都是完整闭合重拳，中央无孔，无枪口、炮管、发射器或火箭喷焰。
- **接触层：PASS_WITH_VISUAL_CAUTION**。两块青白薄层分别局限在各自拳面紧邻位置，尺寸不大于拳体、没有包围拳体或跨场延伸；当前首读仍以“双拳短行程接触压缩”成立。它们不构成独立持有物，也没有护盾手柄或覆盖躯干的防护面。用户仍需裁决这种可见薄层是否需要在后续动作特效中进一步缩短。
- **双臂虎语法：PASS**。保持宽阔前肢式甲片节奏、橙黑宽槽和四区钝性拳面，没有兽爪、兽足、虎头肩、尾部、四足或变形暗示。

综合结论：`PASS_FOR_USER_REVIEW_CANDIDATE`。只解决现有 State03 连接硬伤，不替代用户视觉验收，也不批准后续 Sprite 或实机接入。

## 交付件

- `delivery/BRAVE_FIST_A35_STATE03_RELEASE_CONTACT_CONNECTION_USER_REVIEW_CANDIDATE.png`
- `qa/BRAVE_FIST_A35_STATE03_RELEASE_CONTACT_CONNECTION_50PCT_GATE.png`
- `qa/BRAVE_FIST_A35_GEOMETRY_TO_RELEASE_50PCT_HARD_GATE_BOARD.png`
- `guide/BRAVE_FIST_A35_STATE03_RELEASE_GEOMETRY_GUIDE.svg`
- `guide/BRAVE_FIST_A35_STATE03_RELEASE_GEOMETRY_GUIDE.png`
- `prompts/A35-STATE03-RELEASE-CONTACT-CONNECTION-FIX-BUILTIN-IMAGEGEN-PROMPT.md`
- `source-lock/A35-STATE03-SOURCE-LINEAGE.tsv`

## SHA-256

- A35 State03 Candidate: `218eb68b1c48f41697fc51e7828a0c5bc4500699392a035b152ee8a4875d8124`
- A35 geometry guide PNG: `457a5ae119a1db417e2713325575ca37f8c48a1b0112a279554918c13b79c2d1`
- A35 50% output gate: `fbc56fa4404c336d91e554b62a09aa721c68403254b621a81707b65af4f775b9`
- A35 geometry-to-output gate board: `a9be795a29123d3e1228827d36c02407011715c5bc954cd72a0e6c6f939e088d`

## 真实停门

用户未明确验收前，本图不得覆盖 A34 正式交付，不得进入四向/动作 Sprite、Godot、Runtime 或 Canon。
