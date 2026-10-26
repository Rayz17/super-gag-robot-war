# BREAKER GF上位确认与50%/100%复核纠偏回执

状态：`ADDITIVE_CORRECTION / PRIOR_RECORD_PRESERVED / IMAGEGEN_0 / REROLL_0 / GODOT_0`。

本回执不删除、不改写上一轮原始生成日志、自审、完成回执或 `delivery-hashes.sha256`。上一轮在当时口径下的判断保留为History记录；但其中“低伏四足／龟形可单独触发一票否决”的门槛，已被用户更高优先级的后续确认覆盖。

## 当前上位裁决

- GF PLAN / GF CONTACT 中的 BREAKER 具体设计漂亮且正确；巨型叠壳、低伏身体和四足承力关系属于获准身份本身，不是单独拒绝理由。
- 本轮只复核：GF具体轮廓与表面忠实度、Camera V2 north、地图缩放可读性、临时Candidate资格。
- Canon仍只把BREAKER作为Working故事实体；GF与本轮适配均保持Candidate，不迁移Canon或Runtime。

## BREAKER四项复核

1. **GF具体轮廓与表面：部分继承，未充分忠实。** Raw保留黑蓝巨壳、低嵌红缝、少量暖磨损边和压低躯干的总体质量；但GF的长叶状非均匀叠片、明显前后流向与开合缝隙，被压成更宽圆、更左右均衡的连续壳面，肢端关系也被平均化。问题是GF具体设计适配漂移，不是“四足本身错误”。
2. **Camera V2 north：不成立。** 合同要求主体朝屏幕右上 `−30.9637565°`；raw的头与主要前承力端落在左下，壳体后段延向右上，首读近似反向。缩放或pivot不能修复朝向。
3. **地图缩放可读性：成立。** 全画布确定性缩至384与192后，黑壳大质量、红缝和肢端仍能清楚分开。保守测量换算后的可见尺寸约为361×308px（384画布），50%约181×154px；不是“缩小后消失”的问题。
4. **临时Candidate资格：不足，必须重做Camera适配。** 它可以保留为 `GF_TRANSLATION_COMPARISON_EVIDENCE`，但不能命名为Camera V2 north母版、临时地图Candidate或Godot输入。重做原因只限GF忠实度与north失败；GF原设计继续有效且不重开。

## 馆守Z复核

- 256目标画布下身份、E02双臂、无翼无背包和右下east顶面关系可读；128下配色与重量仍在，但脸部栅格与胸核开始粘连。
- 仅记 `GZ_LOOK_CANDIDATE_ONLY`。当前raw为烘焙棋盘格RGB，未做alpha与pivot注册，因此不是地图MASTER、Atlas或Runtime资产。

## 像素操作与停门

- 输入只有两张GF整屏和本轮两张raw；没有消费环境、旧Call03、B/X替代稿或其他机体像素。
- 只执行机械crop、LANCZOS确定性缩放、文字标签、layout及只读测量；没有抠图、despill、重画、生成或局部编辑。
- 输出停在制作人50%/100%实际像素复核门；不接Godot、不制作Atlas/动作/CONTACT新姿势、不自行启动新生成。

## 产物

- `BREAKER_GF_VS_RAW_50_100_COMPARISON_2400x1800.png`
- `GUARDIAN_Z_RAW_50_100_REVIEW_1600x1000.png`
- `correction-machine-readback.json`

裁决：`GF_DESIGN_REMAINS_USER_APPROVED / BREAKER_RAW_NORTH_ADAPTATION_MUST_REDRAW / GZ_LOOK_CANDIDATE_ONLY / NO_MASTER_PROMOTION`。
