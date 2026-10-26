# 美术资产 Session 目标：C01 Phase B1 最小运行时总装包

> Goal ID：`GOAL_C01_RM_ART_PHASE_B1_INTEGRATION_V1`
>
> 开放范围：仅六类总装试点资产
>
> 禁止解释为：全量 Phase B、全角色动画或全项目风格锁

## Objective

把已经通过联合方向验收的 A.5 构图转化为一个最小但真实可集成的运行时资产包，验证 AI 美术从 full-frame 概念图进入 clean plate、Alpha、MASK、四方向走图和动作帧后，是否仍能保持质量和一致性。

本轮只解决“真实美术能否装进 Godot 并仍然好看、好走、好操作”。不要补齐所有人物和演出。

## 开工前必读

1. `joint-perspective-acceptance-report-v1.md`
2. `perspective-integration-trial-contract-v1.md`
3. `art-phase-a5-manifest-v1.json`
4. `art-phase-a5-layout-metrics-v1.json`
5. `art-phase-a5-completion-report-v1.md`
6. 主程序最新 Phase B1 状态/坐标回执
7. `character_mecha_art_locks.tsv` 的 `CML001` 与 `CML008`

开工时在美术状态页记录 `phase_b1_integration_pilot`；`phase_b2_bulk_generation_allowed=false`。

## Must deliver

### 1. 运行时基础底板

建议 Stable ID：

```text
BG_C01_RM_HALL_BASE_V01
```

- 1920×900 opaque sRGB。
- 以 `PLATE_C01_RM_HALL_CLEAN_TRIAL_V01` 为唯一构图母版继续技术清理。
- 含 FAR + MID_CLEAN 固定结构；不含人物、小机、白框、可动门叶、前景栏杆、可切换灯态和低热光束。
- 馆守 Z 可保持半跪未点灯远景主体；胸灯和余辉另交 MASK。
- 三个裁切必须对应相机中心 `(640/960/1280,450)`，边缘不得出现空洞、重复柱、断裂地砖或扩图接缝。

本轮允许 FAR/MID 合并为一张底板，不为假视差重做两张大图。

### 2. 前景遮挡

```text
FG_C01_RM_HALL_OCCLUSION_V01
```

- 1920×900 透明 PNG，至少包含前景栏杆与一处展台/结构遮挡。
- 提供 Alpha 边缘检查、遮挡范围和 z/y-sort 交接说明。
- 不把固定黑边或整屏调色烘焙进 FG。

### 3. 旧服务门 PROP

```text
PROP_C01_RM_OLD_SERVICE_DOOR_V01
```

- 至少 `closed / opening / open` 三态；opening 可用 3–5 帧或程序形变，但轮廓不能跳形。
- 透明背景、统一 pivot、状态画布一致。
- 与 Zone C clean plate 门洞精确对齐。

### 4. 灯光与低热 MASK

```text
MASK_C01_RM_HALL_LIGHTS_V01
```

- 至少包含环境灯、低热地面区、馆守 Z 胸灯窄扇和硬停余辉四个可独立控制通道/文件。
- MASK 使用灰度或明确 Alpha，不烘焙对白、白框、攻击爆光或全功率效果。
- 胸灯仍是低热环境动作：窄、短、受控，不得变成必杀技光炮。

### 5. 纪存最小四方向走图

```text
SPR_JICUN_C01_2P5D_V01
```

- 前/后/左/右四方向。
- 每方向 idle 1–2 帧、walk 4 帧；本轮不做 terminal/braced/inspect 和半身。
- `CML001` 锁定：黑发蓝眼、无眼镜、青年而不幼、馆内制服、左臂终端。
- 导出源分辨率必须支持运行时 165–220 px 高度；最终 190 px 时脸、发型、制服和左臂终端可读。
- 所有帧统一脚底中心 pivot；步态循环脚点漂移不超过 2 px。

### 6. 跌跌最小动作

```text
SPR_DIEDIE_C01_RESCUE_V01
```

- 最低包含 idle、四向移动所需方向差分、主动前倾、fall 3–4 帧和 down。
- 运行时 60–100 px 仍能读出朝向与“主动摔倒占格”，不能只剩噪点。
- fall → down 的接触点不跳格，不画成受重伤或搞笑摔残。
- 本轮不做 getup、回充和完整表演扩展。

## Manifest 与运行时权限

- 新建独立 `art-phase-b1-manifest-v1.json`。
- 每项记录路径、尺寸、帧序、FPS、pivot、Alpha/颜色空间、来源母版、hash、批准状态和适用场景。
- 通过美术技术 QA 的项目可标为：

```text
approval_status=approved_for_trial_runtime
runtime_allowed=true
runtime_scope=SCN_C01_RM_RESCUE_2P5D_PHASE_B1_ONLY
```

- `runtime_allowed=true` 只允许进入独立 Phase B1 试制场景，不等于最终美术批准、主线默认资产或跨场景复用。
- A.5 五项候选图保持原状态，不覆盖其 Stable ID。

## AI 生产约束

- 背景继续沿用 A.5 clean plate，不重新抽一张相似但透视不同的大厅。
- 角色先锁四方向 Key，再派生走路帧；禁止每帧独立 Prompt 直接拼接。
- 优先局部重绘、形变、补帧和人工清理，避免服装扣件、终端手臂和脸在帧间漂移。
- 透明边缘、色边、重复肢体、脚下残影和 AI 纹理爬动必须在 manifest 前清理。
- 不生成本轮未授权的兜灯、唐胶、观众、机器犬、贴片机、七海半身、纪存半身或 Cut-in。

## Acceptance

- 三相机裁切无扩图接缝或重要结构跳变。
- 底板、FG、旧门和 MASK 可独立开关，叠合后与 A.5 v03 构图一致。
- 纪存四方向一眼仍是同一人；190 px 下身份信息可读，脚点稳定。
- 跌跌 60–100 px 下动作意图可读，fall/down 落点连续。
- 所有 runtime trial 文件通过尺寸、Alpha、pivot、帧序和 hash 检查。
- Phase B1 之外新资产数量为 0。

## Stop and ask

- clean plate 无法清成可用底板，必须重新设计整个大厅。
- 纪存四方向无法稳定保持 CML001，需要改造型、减方向或换风格。
- 跌跌在 60–100 px 下无法读动作，需要提高全局小机比例。
- 需要把 FAR/MID 强制拆开、追加 3D/视频、改变三相机区或相机 Y=450。
- 需要生产其他角色/动画才能让本轮“看起来完整”。
- 需要覆盖既有 `approved_for_runtime` ID 或把 trial runtime 宣布成正式批准。

## Completion report

完成时报告六类资产、实际文件/帧数、生成与返修次数、AI/人工步骤、hash、manifest、trial runtime 列表、未批准列表、三个相机裁切 contact sheet、纪存四方向/循环预览、跌跌 fall/down 预览，以及是否建议交主程序总装。不得自行开放 Phase B2。

