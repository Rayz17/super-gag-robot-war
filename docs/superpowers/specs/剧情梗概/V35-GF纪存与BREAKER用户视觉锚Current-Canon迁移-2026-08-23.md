# V35 GF纪存与BREAKER用户视觉锚 Current Canon迁移（2026-08-23）

> Status: `user_confirmed_visual_anchor_migration / hard_art_lock_scope_only`

## 用户裁决

用户明确确认：`GF_PLAN_1280x720_v2.png`中的纪存形象正确，BREAKER设计漂亮且应作为后续制作目标；A6纪存三态形象不正确。该裁决覆盖旧任务中“GF只借氛围、不得借人物或BREAKER身份”的限制，但不把GF整帧升为可拆Runtime资产。

## Current锁定

1. **纪存**：GF PLAN局部成为当前用户认可的具体外观与动作语言锚。保留成年中国青年男性、黑发、无眼镜、深蓝馆务外套、左臂档案终端和主动指路线的行动感。旧`core_jicun_stand.png`只保留身份语义沿革；A6三态人物图进入用户拒绝History，不得进入Demo、Runtime或继续派生。
2. **BREAKER**：GF PLAN负责地面形态的身份、轮廓与表面基准，GF CONTACT负责承力与首次接触动作基准。低伏巨型叠壳、非均匀长叶甲片、低嵌单红缝头部与四肢承力关系属于获准设计；不得再由B/X简图、Call03失败稿或文字重设计覆盖。
3. GF双帧仍是不可拆的全屏RGB/RGBA合成图。它们只提供用户认可的视觉责任源；正式人物切片、地图Sprite、可组合战斗姿态仍须由美术资产任务重新生成或补全遮挡，并经过用户实际像素确认后才能进入Candidate程序。
4. 这次迁移不批准GF整帧地图几何、相机注册、Runtime、Atlas、默认入口或最终性能，也不改变C01剧情和玩法结果。

## 生产约束

- 纪存后续透明动作切片必须保持GF脸、年龄感、发型、服装、左臂终端与主动行动语言；不得回退A6幼相三态。
- BREAKER后续Camera V2 north地图母版与战斗姿态必须从GF具体设计派生；相机适配失败应重做视角，不得重开身份或把“低伏四足”本身当失败理由。
- GF局部设计获批不等于当前像素可以抠出、补画或直接绑定；每个实际资产仍按自身alpha、pivot、角度、尺度和动作门验收。

## 权威变更

- `CML001`继续为Hard，但当前具体视觉锚迁至GF PLAN纪存局部；旧具体立绘降为语义沿革参考。
- 新增Hard `CML129`，锁定GF BREAKER地面设计与CONTACT承力动作基准。
- `authority_manifest.tsv`由生成器重建，不手工编辑。

## 不变项

- 纪存故事身份、人物职责与中国文化认同不变。
- BREAKER仍是同一主体的地面重甲与飞行核心两阶段；本迁移只锁当前已获准的地面可见设计。
- 全部新派生资产在用户确认前保持Candidate、`runtime_allowed=false`。
