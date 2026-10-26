# 馆守 Z south 持盾三姿势｜生成前几何硬门

> Status: `PASS_FOR_ONE_BUILTIN_CALL_ONLY`
>
> Lifecycle: `internal geometry control / not art Candidate`
>
> Runtime / Godot / Canon: `false`

## 输入边界

- 馆守 Z 身份只取 CML008 Hard：`.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png`。
- 盾只取 A17 用户接受的 Candidate 设计基底：`art-a17-section2-true-retired-heavy-shield-candidate/.../TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`。
- 未读取或复用 A18 / A19 失败 raw、A2 旧弹孔板、V10X `approved=false` 或 east Sprite 像素。

## Guide 门

Guide：`guide/GZ_SOUTH_SHIELD_THREE_POSE_GEOMETRY_GUIDE_1536x1024.png`

1. 三格共用同一约 4.2 头身、腿长、肩宽和脚点系统。
2. 每格的 foot pivot 为本地 512 宽画布 `(256,896)`；转成 256 方形 Runtime 裁切时目标 pivot 固定为 `[128,224]`。
3. 青色虚线统一表示 Camera V2 south 屏幕方向：左下；不得改成正面、east 或镜像 south。
4. HOLD：站姿稳定、盾正面对外、两条手臂接到背面双握把。
5. BLOCK：弓步承冲、盾位于敌人与胸口之间；两条肩—肘—腕—握把承力链必须可追踪。
6. BASH_CONTACT：盾钝厚边朝左下接触，腰髋与双腿同时扭转；双手全程不脱盾。
7. Guide 上青色圆点只表示背面握把接触 socket，不是要画在盾正面的装饰或手。
8. 红色箭头、青色虚线、红色 pivot 十字与三格边框都不得进入生成图。

## 生成后停损门

以下任一项出现即封存本次输出，不重抽：

- 馆守 Z 身份、头冠、胸甲、比例或配色重新设计；
- E02 提前缺失右臂，或多臂、断手、手指数量明显异常；
- 盾不是 A17 的盾冠、收尖厚边、中央承力脊和蓝白金旧装甲；
- 任一姿势读成背持盾、单手盾、手贴在盾正面或手与握把断开；
- HOLD / BLOCK / BASH 三格动作不可区分，或 BASH 只是旋转盾牌；
- south 主轴错误，或使用 east 图镜像冒充；
- 背景、地板、格线、投影、文字、箭头或非透明底烘入；
- 三个角色身份、盾牌或身体比例不一致；
- 无法切成三张各自完整的 256x256 RGBA Sprite。

