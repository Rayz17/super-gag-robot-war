# C01E02 Task98 runtime grid registration 制作人签收

Date: 2026-08-21  
Authority: `102-c01e02-task98-runtime-grid-registration-producer-correction.md`  
Status: `ACCEPTED_REGISTRATION_GUIDE_CORRECTION / CALL03_FALSE / CALL04_FALSE / REAL_ART_ZERO`

## 签收结论

制作人已逐张查看纠偏后的三张综合导向板，并独立复核回执与交付哈希。Task98 中曾整体下偏 20px 的 integrated guide 证据已被正确替换；当前地形格心、selection pocket、BREAKER charge avenue 与六个主体脚点处于同一 runtime 投影坐标系，可恢复为 C3 与后续单机地图视角母版的注册导向证据。

本签收只恢复几何／注册证据，不批准任何角色像素、环境成品、Runtime 接入或 ImageGen 调用。

## 已验事实

- `cell_diamond(x,y)` 以整数 `(x,y)` 为格心；矩形边界使用 `x/y - 0.5` 到 `x+w/y+h - 0.5`。
- 五个投影控制点最大误差 `0.0px`。
- 馆守Z、BREAKER、应急车、三只小体的 PLAN 脚点最大误差 `0.0px`。
- selection pocket 与 BREAKER charge avenue 顶点最大误差 `0.0px`。
- 100% 与 50% 板目视均未再出现“脚点正确、地形整体下偏”的双坐标问题。
- 两张局部机体 geometry guide 与五份 C3 冻结合同前后逐字节一致。
- 三张旧错图以原字节保存在 `_history/task102-pre-runtime-grid-correction/`，不得重新路由为当前证据。

## 锁定交付

- `delivery-hashes.sha256`: `1e0aa9666398fa3149a48c64e404fcc67b181c18dbabe67b64d9690d11952741`
- `runtime-grid-registration-correction-receipt.json`: `502a03ddd7620f4d80b263a3b9a96da09d3a9be6971e99c7ba2ea4ee416b899a`
- `runtime-grid-registration-completion-correction.md`: `973081ef9542141b899b5cd7c998e32bfcb7ee5a7ca0359f29fe17a9fc805653`
- actor-free guide: `948aa1acfdf7b27cd8a18085c228684f0b80b744048b54dee961bc6c9378f2df`
- PLAN 100% QA: `8daed6efaf7c170a207f6b106e3035eef6af043d84a6bf9eefc00d0ef2785ec2`
- PLAN 50% QA: `cd75c0ca4b64a5de439df07fa8abea77e4b081fd6db002de6fe1d9f1e944a906`

独立执行 `shasum -a 256 -c delivery-hashes.sha256`：26/26 PASS；排除 manifest 本身与 Python cache 后，实际文件集合与 manifest 完全相等。

## 仍关闭的门

- `Call03=false / Call04=false`；不得由本注册签收推导出付费生成授权。
- `approved_handoffs=[] / real_art_loaded=0`。
- C3 仍须独立通过真实 Atlas、roof／foreground 单一遮挡责任、动态性能、A／B 连续链与联合制作人签收。
- 环境 ENV-E0 可见像素已被 103 号视觉拒收，本签收不恢复其 E1/E2 消费资格。
- `FUN_NOT_PROVEN / UGT_NOT_OPEN / G2_B_NOT_OPEN / DEFAULT_UNCHANGED / SAVE_FALSE / CANON_UNCHANGED`。
