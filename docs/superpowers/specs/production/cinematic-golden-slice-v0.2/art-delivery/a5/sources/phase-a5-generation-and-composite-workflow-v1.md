# C01 Phase A.5 生成与合成工作流 v1

## 来源

- 风格与光影参考：`KF_C01_RM_2P5D_STYLE_V01`。
- 馆守 Z 姿态参考：`POSE_GZ_C01_KNEEL_PALM_GUARD_V01`。
- 人物锁图：`CML001/002/003` 当前透明立绘。
- 小机与观众只作为 A5 比例桥接剪影，不是 Phase B Sprite。

## AI 生成记录

共 4 次 built-in image generation，2 次定点返修：

1. `C01-A5-CLEAN-PLATE-GEN-v1`：把 1280x720 风格 Keyframe 扩展为连续宽厅；无人、无 UI、馆守 Z 仅作 FAR 半跪参照。
2. `C01-A5-CLEAN-PLATE-REFINE-v1`：抬升中间调，移除中心充电设备与旧门活动门叶，降低地面导光为结构暗纹。
3. `C01-A5-BRIDGE-SUBJECTS-v1`：在纯 `#ff00ff` 背景上生成跌跌、机器犬、成年观众三枚非运行时桥接剪影。
4. `C01-A5-CLEAN-PLATE-FG-REMOVE-v1`：移除底部前景栏杆，补全被遮地面，使栏杆回归独立 FG 职责。

主要约束均包含：现代主机游戏硬表面半厚涂、斜侧视、人尺度 35mm 感、闭馆夜景但中间调可读；禁止人物、文字、乱码、白框、贴片机、活动门叶、充电设备、胸灯和低热光束烘焙进 clean plate；馆守 Z 不站立、不攻击、不变形。

生成母版保存在本目录：

- `plate_c01_rm_hall_clean_trial_source_v00.png`：初次宽场景。
- `plate_c01_rm_hall_clean_trial_source_v01.png`：亮度、门叶与设备返修后。
- `plate_c01_rm_hall_clean_trial_source_v02.png`：移除前景栏杆的最终 clean plate 母版。
- `plate_c01_rm_hall_composition_with_fg_source_v01.png`：保留旧栏杆的构图过程记录，不作 clean plate。
- `bridge_subjects_chroma_source_v01.png` / `bridge_subjects_alpha_v01.png`：桥接剪影色键源与本地去背结果。

## 人工与脚本步骤

`build_a5_artifacts.py` 使用 Pillow 执行可复现的技术适配：

1. 将最终 clean plate 适配为精确 1920x900。
2. 以全局裁切 `[320,90,1280,720]` 生成 v03。
3. 按脚底中心叠加锁定人物与桥接剪影，纪存为 190 px；不抠旧 Keyframe 人物。
4. 以矢量示意叠加低热区、安全区与 FG 栏杆，不写对白或按钮。
5. 从同一 clean plate 生成三相机框、脚点、walkable、层级职责和尺度图。
6. 从同一母版直接裁出 A/B/C 三张 1280x720 clean viewport，作为连续性证据。

透明色键使用内置 imagegen skill 的 `remove_chroma_key.py`，由工作区 bundled Python/Pillow 执行；最终五项 A5 交付均为 opaque review evidence，未生成任何 Phase B 动画或运行时 Sprite。
