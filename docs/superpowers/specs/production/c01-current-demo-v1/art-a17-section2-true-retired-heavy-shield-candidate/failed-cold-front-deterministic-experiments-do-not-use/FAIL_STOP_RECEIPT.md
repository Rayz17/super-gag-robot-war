# A17 冷态盾纯确定性修复实验｜FAIL STOP

> Status: `FAIL_STOP_VISUAL_GATE_DO_NOT_USE`
>
> `candidate=false / user=false / runtime=false / canon=false / godot_bound=false`
>
> ImageGen: `0 calls`

## 结论

本轮没有产生可交付的 A17 受击前冷态盾 Candidate。本目录中的图像只是失败试验证据，**禁止作为任何后续美术、精灵、持盾姿态、Godot 或 Runtime 的正向输入**。

唯一正向像素源始终是：

`../derived-front-rear-sprites-v1/masters/A17_SHIELD_FRONT_EXTERIOR_RGBA_MASTER_768x1152.png`

SHA-256：`8c20afbefefd04716e580ae5791338524ebc8c520256cdc047fae6de3ca7de47`

没有读取或使用 R2/R3 失败 cold 输出或任何 ImageGen cold edit 作为输入。

## 已通过的纯技术隔离门

- 输入 SHA 锁定：PASS。
- 输出 Alpha 与用户接受正面 master 逐字节一致：PASS。
- 遮罩外 RGBA 逐字节一致：PASS，变更像素 `0`。
- 三道旧白痕保护遮罩与修复遮罩交集：`0`像素。
- 输出尺寸：`768×1152 RGBA`；Alpha bbox 保持 `[41,68,726,1084]`。
- 确定性脚本：`../build_cold_front_deterministic.py`，SHA-256 `d2c10ad78081b8b339e6014cfeffe6b35d3862b37681995d443eda093f3f2fc0`。

## 硬视觉门失败

100% 深浅底实际查看仍明确失败：

1. 中央承力脊和右侧象牙白边框出现周期性 donor 条纹，可读成水平扫描带。
2. 五个分面在热痕轨迹处的边界不连续，中央脊和外边框结构线断裂。
3. 锁定热痕 ROI 仍有 `20`个鲜红高显著像素，不满足“不留红热”。
4. 上述条纹和断线在 50% 仍可见，无法准确读成同一面 A17 三旧痕冷态盾。

因此不得把机器隔离 PASS 冒充视觉 PASS，也不得把失败图重命名为 Candidate。

## 后续唯一安全路线

必须由美术在已接受正面 master 上做分面手工补画：蓝色主面、象牙白纵甲、中央承力脊、外白边框和厚金属外框分层恢复，再独立延续被遮挡的旧白痕。该步骤需要人工绘制判断，不能继续依靠自动 clone/inpaint 强行过门。

## 失败证据

- `masters/FAILED_DO_NOT_USE_A17_SHIELD_COLD_FRONT_EXPERIMENT_768x1152.png`
  - SHA-256 `cf7b47acfcefdc7c7c8f705fc0d282df01563efe5b7253ad4dcbcdf2d4c52c14`
- `map-candidates/FAILED_DO_NOT_USE_A17_SHIELD_COLD_FRONT_EXPERIMENT_256x256.png`
  - SHA-256 `a85acc9c5d23e067f50a4f52e10a08fd812425b2f095ea9083f6d37e523e568d`
- `masks/A17_SHIELD_FOURTH_HOT_SCAR_AND_HALO_MASK_768x1152.png`
- `masks/A17_SHIELD_THREE_OLD_WHITE_SCARS_PRESERVE_MASK_768x1152.png`
- `qa/A17_SHIELD_COLD_FRONT_DARK_LIGHT_QA_100PCT.png`
- `qa/A17_SHIELD_COLD_FRONT_DARK_LIGHT_QA_50PCT.png`
- `qa/A17_SHIELD_COLD_FRONT_MASK_AND_OLD_SCAR_PRESERVE_OVERLAY.png`
- `A17_SHIELD_COLD_FRONT_DERIVATION_METADATA.json`

本轮未修改 binding、玩法、Canon、Default 或 Runtime。
