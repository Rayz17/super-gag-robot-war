# GF Dialogue UI 现代方向｜用户接受回执

> Date: `2026-08-25`
>
> Decision: `USER_ACCEPTED_DIRECTION`
>
> User statement: `这套可以采用了`

## 批准范围

用户批准的是 Call01 现代方向板所确立的整体调性：

- 万机馆现代舰桥航电＋高科技展馆导览系统；
- 薄型石墨／深海军蓝复合材质；
- 冷白信息、克制青色信号和极少量安全橙；
- 非对称、开放、薄层、精密工业仪表感的组件语言；
- 明确非 D&D、非魔法、非宝石徽章、非厚重奇幻九宫格的现代方向。

批准视觉基底：

- `call01/raw/GF_DIALOGUE_UI_MODERN_DIRECTION_BOARD_CALL01.png`
- SHA-256: `54c2fd074699dccc363e4eeca2ea0a2021823b96b2c765f3d32859848c0fa446`

## 未自动批准的范围

本回执不等于：

- 方向板 RGB 像素可直接裁切成生产件；
- 任何真透明组件已通过技术门；
- Godot 绑定、Candidate HUD 消费、Runtime、Default、Save 或 Canon 批准；
- B06、E07 或 wide fallback 实际 1280×720 画面通过；
- 最终用户实帧签收。

## 生产授权

允许 Section 2 以该方向板为唯一正向视觉基底，进入独立 RGBA 组件生产与技术 QA。原 D&D 风格 Call01 仍为 `USER_REJECTED / HISTORY_ONLY / DO_NOT_USE`，不得作为新稿输入或像素来源。

生产阶段固定门：

```text
user_accepted_direction = true
component_visual_acceptance = false
actual_frame_user_acceptance = false
runtime_allowed = false
runtime_handoff = none
godot_binding_allowed = false
canon_modified = false
```

## Candidate HUD 采用记录

用户后续对当前现代 UI 套件明确表示：`这套可以采用了`。因此 C01 可将六个经独立技术验证的 RGBA 组件接入正式 Candidate HUD 消费链，而不再只由实帧测试子类临时读取。

该采用权限严格限定为：

```text
candidate_hud_adoption_authorized = true
component_visual_acceptance = false
actual_frame_user_acceptance = false
b06_e07_action_slice_acceptance = false
runtime_promotion = false
default_promotion = false
canon_promotion = false
```

这不改变 B06 / E07 人物动作图的独立验收门，也不将三张 1280×720 实帧记为用户通过。
