# C01E02 Godot Visual Evidence v1

> Status: `accepted_functional_visual_evidence_10_frames`
>
> Resolution: `1280x720`
>
> Source: `game-godot/scripts/c01e02_story_first_visual_capture.gd`
>
> Durable output: `outputs/c01e02-story-first-runtime-v1/`

## 1. 验收帧

| 帧 | 画面 | 必须直接读到的合同信息 | 结论 |
|---:|---|---|---|
| 01 | `01-black-water-opening.png` | 29 人仍在建筑内；黑水、低位烟、半开防火门；今晚连续时间线 | 通过 |
| 02 | `02-three-evidence-complete.png` | 三证 3/3；普通物件与关键证据分层；调查目标不遮场景 | 通过 |
| 03 | `03-r1-ordered-bridge-sequence.png` | 斜45度战场、三段桥、四条路线、工具轨道、当前合法段与固定支援 | 通过 |
| 03C | `03c-r1-tool-evac-motion.png` | R1 先播放两台封存工具的实体轨道，再播放当回合群众撤离；当前单位、步数和轨迹不遮地图 | 通过 |
| 04 | `04-r2-choice-preview.png` | 护人 / 护工具后果在提交前可读，敌方意图为短标签 | 通过 |
| 05 | `05-r3-qihai-write-disabled.png` | 七海写权限停用、城市消防仍在线、R3 工具意图和现场位置 | 通过 |
| 06A | `06a-r4-to-r5-f2-entry-motion.png` | 29 人完成离楼后，F2A / F2B 沿两条西门路线进入；回合反馈与移动标记同时可读 | 通过 |
| 06 | `06-r4-29-outside-r5-checkpoint.png` | 29/29 楼外、F2 新成人进场、五人退路与 R5 检查点 | 通过 |
| 07 | `07-r5-reverse-brace.png` | SEG3 反折、侧条、五条退出路线、左前腿过载和次梁意图 | 通过 |
| 08 | `08-baihan-eighteen-meter-frame.png` | 18.0 m 远程预量、78% 合拢、`NO BODY / NO HP`、七海停权频道 | 通过 |

## 2. 人工检查结论

1. 隐藏中的楼外撤离组和 F2 接驳员不会在入场前被通用单位绘制器泄露。
2. 撤离路线、桥段、工具轨道、次梁、侧条和固定消防支援占位均由通用 overlay 协议绘制，不依赖截图专用分支。
3. 右侧意图从不可读的长中文串改为稳定 ASCII 技术短标签，避免候选字体缺字与一行溢出。
4. 白函结尾不再只靠舞台说明；测量框是由 Narrative beat 元数据驱动的真实画面效果。
5. R1-R4 的工具、撤离组和 F2 接驳移动由真实 Session 回执逐边播放；可跳过、可随 Tactical 快照恢复，结果页不能在播放结束前覆盖地图。
6. 当前画面达到“功能证据”标准，但地图单位仍是候选 token，不应被描述为正式美术完成。

## 3. 复现命令

```bash
HOME=/private/tmp/chao-gag-e02-visual \
CHAO_GAG_CAPTURE_DIR=/private/tmp/chao-gag-c01e02-story-first-visual \
godot --path game-godot --display-driver macos --audio-driver Dummy \
  --resolution 1280x720 \
  --script res://scripts/c01e02_story_first_visual_capture.gd
```

捕获脚本必须输出 `C01E02_STORY_FIRST_VISUAL_CAPTURE_OK`。正式留档由 Runtime Parity Checker 检查十个文件存在且每张大于 50 KB。
