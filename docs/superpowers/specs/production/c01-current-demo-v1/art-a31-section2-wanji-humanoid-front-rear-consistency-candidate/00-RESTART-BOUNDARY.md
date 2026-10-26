# A31｜万机馆未来人形前后视一致性新一轮

> Status: `FRONT_FIRST / CANDIDATE_ONLY`
>
> User approval: `false`
>
> Runtime / Godot / Canon: `false / false / false`

- A25／Call04 的现代馆体、展舰与上半身调性不推倒。
- A24 已成立的小型双眼指挥头、非对称天线和双层馆门胸部由 A25 前视现有像素保留。
- A29 Call01 多面板失败图永久禁止成为正向参考。
- 本轮先只调用一次 built-in ImageGen 生成一张独立前 3Q。只有前视通过单画布、宽度、B1/B2 下身和非鞋型足硬门，才调用一次独立后 3Q。
- 每张最多一次调用，随机 reroll 为 0；任一图失败即停止。

共享比例与部件映射继续读取 A29 的 `00-SHARED-HUMANOID-PROPORTION-AND-MODULE-GUIDE.md`；A31 不改变其定量包络。
