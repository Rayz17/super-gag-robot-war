# LibTV 馆守 Z 低热掌防验证回执 v1

> 日期：2026-07-15  
> 状态：`review_ready_not_runtime_approved`  
> 适用演出：`BP_C01_GZ_PALM_GUARD_V01` / `VID_GZ_C01_PALM_GUARD_V01`

## 1. 结论

LibTV 首尾帧视频验证完成。生成结果保持馆守 Z 半跪、固定机位和单掌防卫动作，未出现站立、迈步、全功率攻击、双拳发光、敌机、爆炸或字幕。4 秒母片与 1.625 秒运行时候选均保留在 `art-delivery/review/`。

本回执只证明素材达到人工复看候选，不修改 Canon、战斗结算、正式资产 Manifest 或 Godot 运行时批准状态。用户复看通过后，仍需执行 Godot 导入、20 次连续播放、跳过/回退和 Windows 导出验证，才能提升为 `approved_for_runtime`。

## 2. LibTV 任务

- CLI：LibTV CLI `1.1.1`
- Skill 包 SHA-256：`8169fb0a24922da519e9d669aed6675b700a93c9aba9404198e3905554ea51e2`
- 模型：`Seedance 2.0 VIP`（`star-video2`）
- 模式：`frames2video`
- 参数：`count=1`、`ratio=16:9`、`resolution=1080p`、`duration=4`、`enableSound=off`、`search_enabled=0`
- 任务 ID：`20260715215103048137259`
- LibTV workspace ID：`2902190`
- LibTV project UUID：`fc035e21db0c4f73b9985c27ed4de6ff`
- 画布：[C01｜馆守Z低热掌防｜首尾帧验证](https://www.liblib.tv/canvas?spaceId=2902190&projectId=fc035e21db0c4f73b9985c27ed4de6ff)

## 3. 输入锁

| 用途 | 文件 | SHA-256 |
|---|---|---|
| 首帧 | `art-delivery/staging/video_gz_c01_palm_guard_start_frame_v01.png` | `140cf573a314cc0f51bec4da8f93c2d1778278158b6fb0be295f641182839361` |
| 尾帧 | `art-delivery/staging/video_gz_c01_palm_guard_end_frame_v01.png` | `8456a5bc6e75d57d0ef6ad8f54886fdce7d59489fc6fb07af3ee4fdb35755fb8` |

## 4. 生成指令

> 严格把第一张参考图作为第一帧，第二张参考图作为最后一帧。固定机位、固定焦距、固定灰色背景和地平线。馆守Z是同一台18米旧式守护机，全程保持半跪，膝部和脚部不得位移。唯一主要动作：画面右侧的巨掌从较低防卫位缓慢抬起至正面防卫位，肩部与肘部做沉重的机械伺服联动，躯干只有极轻微受力后坐。胸牌始终保持低亮暖黄色，不增加新灯光。装甲形状、红蓝金配色、表面划痕、头冠、手指数量、左右臂和腿部结构必须保持一致。禁止站立、迈步、攻击、挥拳、光束、爆炸、烟雾、火花、敌机、镜头运动、景别变化、文字和字幕。动作缓慢、有重量，结尾稳稳停在第二张图的单掌防卫姿态并短暂停留。保持原参考图的硬表面机械插画质感。

## 5. 保留产物

| 产物 | 规格 | SHA-256 | 状态 |
|---|---|---|---|
| `art-delivery/review/vid_gz_c01_palm_guard_libtv_seedance2_master_v01.mp4` | H.264；1920x1080；24 fps；4.041667 s；97 帧；无声 | `209183ded5c9fe22866e365cd1c895a2d251f9b8c94f69b7f0491ff1497439f1` | 母片保留 |
| `art-delivery/review/vid_gz_c01_palm_guard_libtv_seedance2_runtime_candidate_v01.mp4` | H.264；1920x1080；24 fps；1.625 s；39 帧；无声 | `d06237efc9a8bd357f9956d3f1c43c997c704506ad2abe3bbeea8490b2fa1d2c` | 运行时候选母版 |
| `art-delivery/review/vid_gz_c01_palm_guard_libtv_seedance2_runtime_candidate_v01.ogv` | Theora；1920x1080；24 fps；1.625 s；无声 | `4e24223a686ab0308918e38640ed44c563d9c9104ba2f5836fbd55913e17f17e` | Godot 候选；已通过 FFmpeg 全流解码 |
| `art-delivery/review/vid_gz_c01_palm_guard_libtv_seedance2_contact_sheet_v01.jpg` | 2 fps 八帧接触表 | `45cb3e37150a07349e78d23df011dfa71e7f461caf159416e56afdbaf4ee8c6b` | 人工复看证据 |

## 6. 当前 QA

- 通过：首尾帧顺序与动作方向。
- 通过：全程半跪，膝部和脚部没有大幅位移。
- 通过：固定镜头、固定背景、无敌机、无字幕、无烘焙爆炸或光束。
- 通过：掌部由低位抬至正面防卫位，动作轮廓在缩略接触表中可读。
- 通过：MP4 和 OGV 均为 1920x1080、24 fps、无声；OGV 可完整解码。
- 待用户：主观判断 1.625 秒加速版的重量感是否足够。
- 待运行时：导入 Godot，比较 `full` 模式视频与静态 Pose + Godot FX 回退。
- 待运行时：连续播放 20 次、跳过、缺视频回退和 Windows 导出资源验证。

## 7. 提升门槛

用户确认镜头观感后，才允许：

1. 把 OGV 复制为 `res://assets/battle_presentation/c01/guardian_z/vid_gz_c01_palm_guard_v01.ogv`；
2. 把 MP4 复制为对应母版路径；
3. 在正式 Manifest 中新增 `VID_GZ_C01_PALM_GUARD_V01`，先标 `runtime_validation_candidate`；
4. 通过运行时检查后再标 `approved_for_runtime`。
