# C01E02 A9.1-A3｜分层SVG Pilot制作人像素审查与局部R1

> 日期：2026-08-19  
> 状态：`machine PASS / producer visual revision required / one local SVG revision assigned`  
> 上游：70号分层SVG Pilot  
> 边界：不重开设计；只改同一分层SVG内部path，不做新概念或新身体。

## 1. 制作人实际像素结论

已直接查看两张透明PNG、A4地图板、50%／100%板与轮廓叠合板。

### 1.1 已证明

- Codex可以不靠ImageGen／Blender，直接用分层SVG产出可消费的地图Sprite；
- 馆守Z回到CML008＋V10X＋用户C，未再设计新机体；
- BREAKER回到B身体与384量尺，未再变成雪橇／车辆；
- 两者frame、bbox、pivot、mask外alpha和来源锁均通过；
- SVG是可编辑分层母版，适合后续方向／状态派生。

### 1.2 尚未通过

| 主体 | 制作人视觉结论 | 根因 |
| --- | --- | --- |
| 馆守Z | `REVISION_REQUIRED` | 身份识别已回归，但C128方向样张被当成逐像素最终mask，腿胯／胸下负形过硬，整体仍有程序图标感；KINETIC_CEL线压和装甲咬合不足 |
| BREAKER | `REVISION_REQUIRED` | 量尺、高背和前肢承重成立，但X异质甲片与柔性缝第一读法仍弱，正面体块偏普通猿／重壳四足 |

机器IoU=1不等于视觉通过。本轮不送UA91，不扩四向或动作。

## 2. 纠正“批准方向”与“最终像素mask”的关系

用户批准C／B锁的是设计、比例、承重拓扑和大轮廓，不是要求永久保留低分128样张的每一个锯齿、内孔和负形。

R1冻结：

```text
outer silhouette envelope = unchanged
body topology and proportion = unchanged
local contour smoothing and internal negative-space cleanup = allowed
overall silhouette IoU >= 0.96
bbox center / pivot drift <= 1px
redesign = forbidden
```

允许修清低分样张的内孔、连接、装甲交叠和线压；不得改变头身、肩宽、四肢类别／长度、高背壳、承重前肢或短后稳定结构。

## 3. 唯一写入范围

`docs/superpowers/specs/production/c01-current-demo-v1/art-a9-1a3-layered-svg-pilot-r1/**`

初版目录保持原字节。R1从以下母版复制后局部修改：

- 馆守Z初版SVG SHA：`463ed057c6d7d36415693cb23c279920eaa417f947ae17728fa958ca390d231c`；
- BREAKER初版SVG SHA：`3e5a590a9fd44c6c789550581b7780dfbddb4701989620a4bdfdf11899ca717a`。

## 4. 馆守Z唯一局部返修

- 外轮廓、256 frame、约4.2头身、头冠／银脸／红X胸／金核／宽肩环／双圆柱臂不变；
- 补齐胸下到髋、髋到上腿的装甲咬合，缩小“躯干悬空＋两条腿分离”的程序感；
- 内部负形可以填合，但不得扩大外轮廓；
- 腿／脚保持C动作空间，加入清楚的白色结构关节和两级硬阴影；
- 轮廓与承重边线粗、内部分件线细；减少零碎短线与机械对称噪声；
- 50%尺寸必须像完整机体，不像拼接图标。

## 5. BREAKER唯一局部返修

- 384 frame、B高背、低嵌头单红缝、两条承重前肢、短后稳定结构不变；
- 不改变外身体，仅重做内部X表面节奏：5–7块非对称异质叠片、不同方向硬缝／柔性缝和少量暗红受力缝；
- 胸缝闭合、上背出口封闭；不得画核心；
- 弱化左右肢体的普通猿类对称，靠甲片与线压而不是改肢体拓扑；
- 前肢关节要读作攻城承重结构，不是动物肩臂；
- 50%尺寸第一眼应是“高背异质突入壳”，不是龟、猿或普通四足。

## 6. 必交物与停止门

沿用70号四主文件与四张审查板命名，加`-R1`稳定后缀；补`r1-delta.md`逐条说明只改了哪些path。

机器门：

- outer bbox、pivot目标不变；
- silhouette IoU`≥0.96`；
- mask envelope外alpha=0；
- 无ImageGen、Blender、Pillow机体绘制、渐变、滤镜或PBR；
- source lock与hash全部通过。

制作人门：

- 馆守Z完整机体感、装甲咬合、KINETIC_CEL完成度通过；
- BREAKER B＋X第一读法通过且不再普通猿／四足；
- 两者放回A4后仍清晰、量尺成立。

本单只允许这一次局部R1。若仍失败，停止Codex自动美术清稿并向用户报告需人工2D美术接力；不得继续R2/R3循环，不得重画设计。

## 7. DAG边界

R1过制作人实际像素门后，才可送UA91判断两张母版；UA91前仍不扩四向、动作、Atlas、A9.1-B、Godot、exact handoff、G2-B或LibTV。
