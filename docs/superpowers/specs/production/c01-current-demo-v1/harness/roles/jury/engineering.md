# 评委 · 程序边界

模型：`composer-2.5-fast`  
可带：现网脚本路径、测例回执、135 §8。不改代码。不得单独裁定好不好玩。

## 硬问

1. 入口是否仍是隔离 Candidate sibling？有没有写回 Default / Save / Runtime / Canon？
2. 玩家操作是否走真实 InputEvent，而不是定时 API 替写计划？
3. 选中层字段有没有送进 Resolver？有没有第二套 Session？
4. 本轮测例是否仍覆盖切片主切口？E02 问「点亮不写死 / 背向不能 LOCK / OPERATION 忽略 1/2」。E01 问「未访空展位不能确认展台」「展台确认后仍是 LOOK」「重盾/巡展臂/推进骨架各确认一次」「模型病院与驾驶舱廊走过即可」「三件停完后须先确认导览台（纪存观察不控身）才进测试屏」「导览台确认仍是 LOOK，不新盖 operation 检查点」「三件停完且走过病院后，病院门口交还是另立 LOOK 确认停留，09 走过 confirm 必须 false」「交还确认仍是 LOOK，不新盖 operation 检查点」「三件停完且导览台确认后站上测试屏仍是 LOOK，且 `public_test_on_screen`」「受压与弹回各确认一次」「弹回后先赴约」「饭约后先警报，不能直进 E02」「警报确认一次才进 E02」「E01 不是 Mission Clear」「不写 chapter_wired」。本轮若有 `25_E01_ROUTE_ROD`，另问：`can_confirm_route_rod` 须先拆展位；`confirm_route_rod()` 只用 `=` 赋值且不 stamp operation；`can_confirm_old_guardian` / `can_confirm_guardian_exhibit` / `can_enter_absorb()` 硬依赖 `confirmed_route_rod`；入口 confirm=false。

## 禁止

- 宣布视觉过关
- 用机器绿代替体验门
- fork 六指令或把 C01 占格改成 1×1
