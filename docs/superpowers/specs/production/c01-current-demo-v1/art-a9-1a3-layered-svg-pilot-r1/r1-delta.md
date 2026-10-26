# A9.1-A3 分层 SVG Pilot｜唯一局部 R1 差异

日期：2026-08-19  
任务：71-c01e02-a9-1a3-svg-pilot-producer-review-and-local-r1  
权限：Candidate；`runtime_allowed=false`；`redesign=false`；`revision_round=R1_ONLY`

## 冻结基线

- 馆守Z 70号父 SVG：`463ed057c6d7d36415693cb23c279920eaa417f947ae17728fa958ca390d231c`
- BREAKER 70号父 SVG：`3e5a590a9fd44c6c789550581b7780dfbddb4701989620a4bdfdf11899ca717a`
- 两个父目录文件均只读消费；R1 仅写本目录。
- 馆守Z继续锁定 CML008 Hard 身份、V10X E02 双臂裸机限域与用户 C 动作骨架；BREAKER继续锁定用户 B 身体承重拓扑与 X 表面关系。

## 馆守Z：仅局部内部清稿

未改变：256 frame、外轮廓、bbox、pivot、头身比、肩宽、四肢类别及长度、头冠／银栅格脸／红X胸甲／圆金核／宽肩环／等重圆柱前臂、E02双臂、无翼无背包。

本轮只改：

- `r1_internal_negative_space_allowance`：仅在胸下—髋—上腿交界的三个既有内部负形加入白名单；不越过 R1 外轮廓包络。
- `r1_torso_pelvis_interlock`：补入局部胸髋咬合、白色髋关节与中央护裆装甲，使躯干与腿部读作同一承重结构。
- `hard_shadow_1`：只为新增咬合区补一处受控硬阴影。
- `accent_highlight`：只补两段细关节高光，维持外粗内细线压。

机器差异：approved silhouette IoU=`0.980006`；R1 envelope IoU=`1.000000`；内部补合=`689 px`；移除批准像素=`0 px`；中心漂移=`0 px`；包络外 alpha max=`0`。

## BREAKER：仅固定身体内的 X 表面清稿

未改变：384 frame、B 外身体、高背壳、低嵌头单红缝、前肢承重半直立、短后足仅稳定、bbox、pivot、闭合胸缝、封闭上背出口。

本轮只改：

- `x_bio_plate_04`：在原位置把内部甲片节奏改为不规则咬合；未改变身体或外壳。
- `r1_x_flexible_seam_network`：在固定壳体内加入方向不一的暗缝与少量暗红受力缝。
- `r1_forelimb_load_plates`：在固定前肢轮廓内加入不等分承重甲片；未改肢长、接地点或拓扑。
- `r1_head_shell_overlap`：在固定低头位置补壳唇遮叠；单红缝保持。

机器差异：approved silhouette IoU=`1.000000`；R1 envelope IoU=`1.000000`；增删外轮廓像素=`0 px`；中心漂移=`0 px`；包络外 alpha max=`0`。

## 明确未发生

- ImageGen调用：0；Blender调用：0；Pillow机体绘制：0。
- 无新概念、无新身体、无新方向、无新动作、无四向／动作条／Atlas／Godot／LibTV／Runtime接入。
- 制作人冻结可见几何后未再修改任何机体 path；本单不启动 R2/R3。

