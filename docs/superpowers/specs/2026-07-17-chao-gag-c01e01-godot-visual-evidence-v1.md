# C01E01 Godot Visual Evidence v1

> Status: `accepted_functional_visual_evidence_10_frames`
>
> Resolution: `1280x720`
>
> Source: `game-godot/scripts/c01e01_story_first_visual_capture.gd`
>
> Durable output: `outputs/c01e01-story-first-p5-validation/`

## 1. 验收帧

| 帧 | 画面 | 必须直接读到的信息 | 结论 |
|---:|---|---|---|
| 00 | `00-narrative-cold-open.png` | 火灾之后约 30 秒；雨夜、馆守Z、纪存沉默；不是七年前录像 | 通过 |
| 01 | `01-spatial-front-hall.png` | 六站闭馆路线、当前前厅、馆内 29 人；主画面与路线栏互不遮挡 | 通过 |
| 02m | `02-spatial-model-hospital-dialogue.png` | 模型病院是可操作闭馆事件；纪存与唐胶左右席位、反装锁扣和安全罩任务同屏 | 通过 |
| 02 | `02-spatial-real-machine-dialogue-narrator.png` | 调查覆盖层、纪存与跌跌左右席位、旁白主导时双方降暗 | 通过 |
| 02b | `02b-spatial-real-machine-dialogue-diedie.png` | 跌跌发言高亮、人物图像与左膝故障信息同屏 | 通过 |
| 03 | `03-tactical-round-one.png` | 斜 45 度 8x10 战场、四个人数徽标、黄线、路线箭头、路径框、侧门与巨型馆守Z尺度 | 通过 |
| 03b | `03b-tactical-round-one-evac-motion.png` | R1正式回执逐边播放、当前组/人数/起终格、运动高亮与可跳过提示；信息条不遮馆守Z或可操作格 | 通过 |
| 04 | `04-tactical-round-three-reflector.png` | R3 只剩跌跌可行动；机器犬与 D5 共用格；三枚反光位以安全/危险覆盖显示 | 通过 |
| 05 | `05-narrative-four-orders-system.png` | 四张白框、半开防火门、观众仍在 L1；接管令而非抽象总结 | 通过 |
| 05b | `05b-narrative-four-orders-qihai.png` | 七海公务风险频道、东侧禁行与西带命令、火场图已收到 | 通过 |

## 2. 人工检查结论

1. Narrative、Spatial 与 Tactical 三种模式具有明确的画面层级，不再全部挤在同一个信息面板里；模型病院也不再只是经过背景。
2. Tactical 地图保留斜 45 度构图，馆守Z以场景级尺寸出现，小机器和人群 Token 仍可辨认。
3. R3 画面中机器犬与 D5 的重合是牵引合同的视觉结果，不是重复单位；右栏行动数也显示机器犬已失去独立行动。
4. 四个人群徽标、路径箭头、路径框、黄线、侧门和三枚反光位均在候选画面中可见。
5. 19条正式移动回执现按 `6 / 9 / 4` 逐边插值播放，回合反馈停留后才交还输入，且可跳过、可随Tactical快照恢复；当前单位Sprite、步态帧、音效、镜头和环境动画仍属功能美术，未达到正式售卖品质。

## 3. 复现命令

```bash
HOME=/private/tmp/chao-gag-e01-visual \
godot --path game-godot --display-driver macos --audio-driver Dummy \
  --resolution 1280x720 \
  --script res://scripts/c01e01_story_first_visual_capture.gd
```

脚本必须输出 `C01E01_STORY_FIRST_VISUAL_CAPTURE_OK`。Parity Checker 额外要求九个文件存在且每张大于 50 KB。
