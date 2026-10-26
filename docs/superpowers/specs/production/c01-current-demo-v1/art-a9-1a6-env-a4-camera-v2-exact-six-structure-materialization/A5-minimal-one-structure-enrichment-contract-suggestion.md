# ENV-A5最小单栋Structure轮廓丰富化合同建议

建议状态：`PROPOSAL_ONLY / ONE_STRUCTURE / ZERO_IMAGEGEN / NO_A5_PIXELS_AUTHORED`

## 目标

只重做`NW_BLOCK`一栋纯色几何样板，先解决50%“单一长方盒”体块问题，再谈材质。A5不恢复六栋批量。

## 继续冻结

- `grid_rect=[1,0,7,5]`、Camera V2轴`(40,24)/(-40,24)`、pivot=`[240,378]`、front edge=`[80,288]`不变。
- foundation占地、排序责任、reveal cell和玩法阻挡不变。
- `visual_bounds_raw=[-160,-90,480,378]`与HIGH高度上限`90px`不变。
- 所有主边只允许`±30.96°`或竖直；无透视汇聚、无手工screen offset。
- foundation始终Alpha 1.00；整个新occluder仍统一`1.00 -> 0.34 -> 1.00`。

## A5唯一新增权限

允许在既有visual envelope和高度上限内重写**occluder Alpha轮廓**，但不得扩大玩法占地：

1. 主体拆成两级退台，避免一整块矩形屋顶；
2. 一侧加入沿exact轴的短檐口，长度受原envelope约束；
3. 屋顶加入偏置设备间，作为第二体块而非贴图方框；
4. 正立面保留一处断开／内凹，使外轮廓在50%产生明确节奏；
5. 不加文字、招牌、动态光影、自由曲线或新玩法语义。

建议NW样板采用“低主楼 + 偏置设备间 + 一侧短檐”的三体块组合，总高不超过90px；foundation继续显示完整7×5阻挡范围。新Alpha可以与Task121不同，但所有新增非零像素必须位于原`visual_bounds_raw`内。

## 先几何、后材质

A5第一门只交纯色轮廓，不读取ENV-A1 donor：

- normal 100%、50%纯色样板；
- 新旧Alpha差分图与visual-envelope overlay；
- exact角度、pivot、front edge、高度和占地readback；
- occluder 1.00/0.34/restore三态；
- 后方单位／路线Proxy可读性QA，Proxy不得写入资产。

只有制作人确认50%不再首先读作单一程序盒，才允许在同一新Alpha内进入A4式克制材质化；该批准仍只覆盖NW_BLOCK。

## 停止门

- 50%仍为单一矩形板房，或必须靠纹理才能解释退台；
- 任何轴偏离`±30.96°`、高度超过90px、pivot/front edge/grid rect变化；
- 新Alpha越出visual envelope，foundation或reveal cells变化；
- 0.34后仍看不清后方关注点，restore不等于normal；
- 用过量檐口、设备、线条把低楼做成高噪模型，而非清楚的机战地图体块。

任一失败即停止NW样板；不得自动扩六栋。
