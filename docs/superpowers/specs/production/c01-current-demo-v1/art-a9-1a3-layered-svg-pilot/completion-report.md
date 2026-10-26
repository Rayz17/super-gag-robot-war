# Task 70 分层SVG Pilot交付回执

状态：`READY_FOR_PRODUCER_PIXEL_REVIEW / MACHINE_PASS / VISUAL_ACCEPTANCE_PENDING`

权威：`Candidate only`  
`runtime_allowed=false`  
ImageGen调用：`0`  
Blender调用：`0`

## 两张主文件

1. `GUARDIAN_Z_C_SOUTH_IDLE_MASTER.svg`：手写分层path母版；外轮廓只受批准C128 Alpha护栏约束。
2. `GUARDIAN_Z_C_SOUTH_IDLE_256.png`：256×256透明实际渲染。
3. `BREAKER_BX_NORTH_CHARGE_READY_MASTER.svg`：手写分层path母版；外轮廓只受批准B128 Alpha护栏约束。
4. `BREAKER_BX_NORTH_CHARGE_READY_384.png`：384×384透明实际渲染。

Alpha护栏文件`GUARDIAN_Z_C_APPROVED_ALPHA_256.png`与`BREAKER_B_APPROVED_ALPHA_384.png`只携带批准源Alpha，不含可见彩色机体像素；它们是两份SVG可复验的依赖文件。

## 四张审查板

- `SVG_LAYER_AND_SOURCE_BOARD_1920x1080.png`
- `SVG_SILHOUETTE_OVERLAY_1920x1080.png`
- `SVG_PILOT_ON_A4_MAP_1280x720.png`
- `SVG_PILOT_50_100_REVIEW_1920x1080.png`

## 机器检查

| 主体 | frame | alpha bbox | pivot | silhouette IoU | bbox/pivot漂移 | mask外Alpha |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 馆守Z | 256×256 | 26,12,230,254（204×242） | 128,254 | 1.000000 | 0 px | 0 |
| BREAKER | 384×384 | 33,18,351,348（318×330） | 192,348 | 1.000000 | 0 px | 0 |

两份SVG必需命名层齐全，未出现可见`rect/circle/ellipse/polygon/line`基础几何、渐变或滤镜；责任源SHA在`qa-report.json`中逐项复验。`delivery-hashes.sha256`覆盖本目录全部交付核心。

## 停止门

机器PASS不等于视觉PASS。本轮已经停在制作人实际像素预审门；未扩四向、动作、Atlas、Godot或Runtime。若任一主体被制作人判为程序图标/剪贴画、身份失败或B+X第一读法失败，则本Pilot视觉失败，不得以机器证据升级。
