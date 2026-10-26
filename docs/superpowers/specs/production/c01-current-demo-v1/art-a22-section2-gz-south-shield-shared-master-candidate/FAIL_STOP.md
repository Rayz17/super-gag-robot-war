# A22 馆守 Z south 持盾共享母版｜失败封存

> Decision: `A_BLOCK_FAIL_STOP`
>
> Deliverable: `NO_CANDIDATE_SPRITE`
>
> Runtime / Godot / Canon: `false`

> **2026-08-24 scope correction:** A22 从 CML008 旧视觉重新生产馆守 Z 的路由已被 130 号明确禁止。A/B raw 继续是 `FORBIDDEN_HISTORY`，不得作身份、姿态、盾牌或 ImageGen 正向输入。

## 实际调用

- Stage A BLOCK built-in ImageGen：`1` 次。
  - Raw: `stage-a-block/generation-raw/GUARDIAN_Z_SOUTH_SHIELD_BLOCK_SHARED_MASTER_CALL01_RAW.png`
  - Size / alpha: `1254x1254 / RGB / hasAlpha=no`
  - SHA-256: `6b33f7251d28c7f9c5f10af684462bcf3689c6fe6de5a9bfe713513f92502eeb`
- Stage B BASH edit：`1` 次。该调用在 A 目视封停消息到达前已在进行并返回；因 A 门失败，结果无条件失效。
  - Raw: `stage-b-bash/generation-raw/GUARDIAN_Z_SOUTH_SHIELD_BASH_CONTACT_EDIT01_INVALID_RAW.png`
  - Size / alpha: `1254x1254 / RGB / hasAlpha=no`
  - SHA-256: `f7ac6c87961095b054ddb82b676b716eaba4232f3d0ad338aeac5da619446135`
  - Status: `INVALID_DUE_TO_A_GATE_FAIL / not reviewed as Candidate`

## A 阶段阻断

1. 馆守 Z 身份明显漂移：巨大圆肩、头胸比例和整体量感不再命中 CML008 的紧凑四头身旧超级系。
2. A17 一体重盾被误画成中央分开的双门 / 双盾结构。
3. 双手视觉上压在盾面，未证明两条手—背面握把—承力架连续关系。
4. 镜头仍接近正面展示视图，没有命中 Camera V2 south `[-40,+24]`。

因此不进入确定性 alpha 清理、256x256 注册、pivot、socket、50% QA 或 Godot 实际帧。A/B raw 均只作失败追溯，禁止复用为后续像素母版；没有修改 Runtime binding，没有迁移 Canon，也没有向用户提交视觉确认。
