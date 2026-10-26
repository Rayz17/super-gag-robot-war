# 馆守 Z V10X｜E02 `shield_take/south`｜R3 body-only guide 门

> 状态：`PASS_BODY_ONLY_GEOMETRY_GUIDE / IMAGEGEN_NOT_CALLED`

## 通过项

- guide 不含盾、装甲板、墙架、地面道具或任何盾牌轮廓；
- 双肩—肘—手链完整，双手终止在未来 rear handle 位置；
- 双手允许在未来 `shield_front_exterior` 图层之后被完全遮挡；
- 身体为低位上提的错步过渡，双臂高度不同，不是稳定 `hold`，也不是对称降髋 `block`；
- 50% 明暗底均能读到两条连续手臂链和两个空手终点。

## 文件

- `guide/GZ_V10X_SHIELD_TAKE_SOUTH_BODY_ONLY_FUTURE_HANDLES_GUIDE_1024.png`
  - SHA-256：`6aa0f0e540640e8a1d281ad0f45fe6fcf7b40f5ac425a6c4363af8c7835047d8`
- `guide/GZ_V10X_SHIELD_TAKE_SOUTH_BODY_ONLY_FUTURE_HANDLES_GUIDE_50PCT.png`
  - SHA-256：`8dac97f8239cbf5384401ee4fb6a1332f526c940e3cccf2b00a4bee3e70cb555`

该门只说明 body-only 生成姿势的几何输入成立，不批准任何生成体、盾层、合成图或 Candidate。预算调整后先执行的唯一 A17 冷态盾窄域编辑在 50%/100% 门失败，因此 body-only ImageGen 调用没有触发。
