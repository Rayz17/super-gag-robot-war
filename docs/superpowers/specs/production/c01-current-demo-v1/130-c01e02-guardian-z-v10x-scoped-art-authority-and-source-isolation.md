# C01E02｜馆守 Z V10X 限域美术权威与旧资产隔离

> 日期：2026-08-24  
> 状态：`CURRENT_SCOPED_ART_AUTHORITY / SOURCE_ISOLATION_ACTIVE / SPRITES_STILL_MISSING`  
> 范围：`C01E02 Demo / 馆守Z双臂裸机 / 美术身份派生`  
> 不构成：全局 CML008 替换、Camera V2 Sprite 批准、用户实际像素验收、Godot/Runtime/Default/Canon 迁移

## 1. 用户裁决与根因

52 号回执已封存用户原话：

> 我看了，馆守找到了最新的设计，问题不大，你继续往后面推吧，我就不去那个session自己回复了

该裁决已经让 V10X 成为 C01E02 Demo 馆守 Z 双臂裸机的可派生母图，但原美术 Candidate manifest 仍保留 `approved=false`。后续任务只读后者，又把全局 CML008 的旧视觉图当成本 Demo 的当前身份母图，因而重复画回旧馆守 Z。

这是 scope 权威没有机器化封死的生产隔离缺口，不是美术资产缺失，也不需要用户重新批准旧稿。

## 2. 本 scope 唯一正向路由

1. 新增 `CML130`，仅在 `C01E02_demo_visual_derivation_only` 中提供 Hard 级的“来源优先级”；它不把图像升为 Runtime，也不替换全局 CML008。
2. 唯一正向设计母图是：  
   `docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`  
   SHA-256 `e1d6b00d743e925d37a8fe4c74a1ef9114e1d7b0f4826fc2285bd6dae1470ade`。
3. 原 manifest 中的 `approved=false` 继续表示“未全局晋级／未 Runtime 批准”，不再能否定 52 号已给出的 C01E02 Demo 限域派生权。
4. V10X Q/SD 透明四向只是 `design_orthographic` 身份、比例、结构、非对称和色块参考；不是 `map_dimetric_40x20` Sprite，不得把正侧背直接改名为南西北东。

## 3. CML008 的两层语义

- **全局不变**：CML008 仍保留 Hard 机体身份与生命周期语义，包括 18 m、C01E02 双臂完整、无翼、无背包、原右臂在 E03 毁损等。
- **本 Demo 视觉 scope**：`.superpowers/.../guardian-z-user-selected-base.png` 仅为 `HISTORY_CROSSCHECK_ONLY`；它不得提供正向像素、头胸外观、配色、地图精灵或新姿态派生。

因此，“保留 CML008 语义”不等于“继续画 CML008 旧图”。

## 4. 其他资产的严格角色

- `GZ_QSD_A1_candidate_C_128.png`：只锁约 4.2 头身、动作空间和 bottom-center；不是像素母图。
- A17 重盾：仅是用户接受的盾牌设计基础。正面／外侧面向敌人且不露手；背面／内侧面向馆守 Z，握把和双手仅在此侧。当前 A17 图不是 Camera V2 持盾姿态。
- A13、A18、A19、A22 馆守 Z 持盾稿、旧 `guardian_z_east_camera_v2_candidate.png`、旧 A2 弹孔装甲板均是 `FORBIDDEN_HISTORY`；不得作身份、姿态、盾牌或像素母图。

精确资产、SHA、view space、可用与禁用范围由 `c01e02-guardian-z-scoped-source-lock-v1.tsv` 机器化封存。

## 5. 后续 Section 2 必须的解析顺序

1. 查询 `CML130`，不得只查 CML008。
2. 读取 `c01e02-guardian-z-scoped-source-lock-v1.tsv`，并验证 SHA。
3. 馆守 Z 身份只能有一条 `SOLE_POSITIVE_DESIGN_PARENT`；数量不是 1 即失败关闭。
4. 先按 Camera V2 绘制与战斗地图角度一致的各朝向／各状态 Sprite Candidate，再交程序绑定；不得以程序镜像、旋转或正侧背裁切伪造缺失角度。
5. 任何 `FORBIDDEN_HISTORY` 路径或 SHA 出现在正向输入、ImageGen 参考、合成母图或绑定清单中，整批立即封停。

## 6. 对旧回执的覆盖关系

- 66 号的 `design_selection=already_done / sprite_adaptation=still_required / redesign=forbidden` 仍有效；其“CML008 视觉为正向组合责任源”表述在本 scope 失效。
- 75 号的 V10X Q 谱系恢复仍有效。
- 76 号的 `design_orthographic != map_dimetric_40x20` 仍有效。
- A18 以 `approved=false` 否定 V10X 限域权限的根因判定失效；但该稿的镜头、BASH 读法和 alpha 仍失败，所以继续是 History。
- A19/A22 回退 CML008 旧视觉的路由在本 scope 明确禁止；它们原有视觉失败结论不变。

## 7. 停点

本迁移只修复“用哪张图生产”。它没有补齐 Camera V2 朝向和动作 Sprite，没有批准任何持盾合成，也没有改动 Godot 绑定。后续仍必须经过：精灵规划 → 美术资产 Section 2 制作 → 实际地图帧 → 用户目视确认 → Candidate 程序绑定。
