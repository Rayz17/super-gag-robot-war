# C01E02 A9.1-A3｜彩图绑定结构Rig与BREAKER B＋X恢复

> Owner：美术资产 Session  
> 性质：Candidate final master correction before user review  
> 依赖：59、60、62及A9.1-A2实际交付  
> 完成即停：不得扩Atlas、Gold Frame、Golden Turn、Godot、Runtime或LibTV

## 制作人回收结论

A9.1-A2的机器包、硬色块化、A4地图落点／遮挡、纪存CML001消费均成立；主程序G2-A.1-R1也已通过内部消费者门。但A9.1-A2视觉母版仍为`P0=0 / P1=2 / P2=2`，不得送用户批准，也不得开放A9.1-B。

未关闭的P1：

1. 馆守Z最终彩色四向仍是ImageGen turnaround切片与调色；现有“结构叠合”只测Three.js低模自身，没有证明最终彩图与Rig的关节点、比例和轮廓一致。
2. BREAKER通过改成低伏机械雪橇／装甲车去掉龟猿感，却丢失用户已选定B“前肢承重半直立型”，也弱化X“异质／生体装甲”。

P2：量化后仍有脏边碎噪；generation log的V3与source receipt／实际V4不一致，完成报告残留字符串引号，validator没有验证彩图—Rig关系。

## A. 馆守Z：最终彩图必须真正来自同一Rig

- 保留A9.1-A2已经成立的V10X身份、约4头身、双臂、无翼无背包和KINETIC_CEL色块方向，不重新设计身份。
- 建立一个实际可运行的结构源：Blender、Three.js或等价分层Rig均可，但必须含具名头／冠／胸／肩／上臂／前臂／髋／大腿／小腿／脚组件及统一关节点。
- 正、背、严格左、严格右最终彩色交付必须由该同一结构源的正交相机直接渲染／分层着色派生；ImageGen只可作材质或局部身份参考，禁止再次生成四视图成片后切片。
- 每一张最终彩图须与对应Rig silhouette、骨点和组件mask叠合；关键关节点偏差不超过最终1024图的6px，肩宽／胸宽／四肢长度的成对误差不超过3%。
- validator必须读取最终PNG alpha、Rig导出的mask／keypoint JSON并计算误差；不得只检查TSV行数或重复自报数值。

## B. BREAKER：恢复B＋X，不得用A型雪橇替代

- 重新以用户已批准B“前肢承重半直立型”为轮廓责任源：高背壳、低头单红缝、壳体离地、两条前肢明显承重并呈半直立，短后足只稳定，不得落成贴地装甲车、钻头壳或滑橇。
- X表面必须在第一眼可读：非对称叠片、柔性甲缝、异质受力连续性、非工业标准关节；禁止纯硬直对称机械板、普通爪兽、龟甲、猿肩、哺乳腹腔。
- 保留闭合胸缝与封闭上背出口，不显露核心、飞翼或E03损伤。
- 规划与首撞仍从同一个结构母版派生；同样提交最终彩图与Rig／mask叠合证据。

## C. 清稿与证据修复

- 保留已经成立的硬色块与两级硬阴影，清理量化脏边、游离像素和碎噪；实际地图缩放后轮廓必须干净。
- 修正V3／V4来源矛盾、completion／generation log多余引号及CML128 Working层级记录。
- A2的纪存、A4地图与pivot／footprint／遮挡结论可直接复用，不重复生产；只在新两机最终像素替换后重跑实际地图合成。

## 最低交付与停点

1. 馆守Z同一Rig源、四向正交最终彩色图、彩图↔Rig叠合与机器误差回执；
2. BREAKER B＋X结构Rig／分层源、规划与接触同源图、彩图↔Rig叠合；
3. 清稿后的KINETIC_CEL像素板和更新后的A4实际地图缩放图；
4. 修正后的manifest、source receipt、generation log、completion、validator与核心SHA。

全部保持 `Candidate / runtime_allowed=false / runtime_handoff=none`。完成后停止并回传制作人；只有制作人视觉预审通过，才会把母版集中送用户裁决。
