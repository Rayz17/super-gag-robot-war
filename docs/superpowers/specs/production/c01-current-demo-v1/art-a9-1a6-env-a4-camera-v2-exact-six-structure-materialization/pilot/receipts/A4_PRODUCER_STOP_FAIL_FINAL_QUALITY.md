# ENV-A4 NW_BLOCK制作人失败回执

状态：`COMPLETE_STOPPED / MECHANICAL_PASS / FAIL_FINAL_QUALITY / SIX_STRUCTURE_BATCH_FORBIDDEN`

日期：`2026-08-22`

## 裁决

- Camera V2、注册、pivot与Alpha逐像素锁定通过。
- NW_BLOCK在50%仍首先读作单一长方程序盒体，未达到精品地图Structure质量。
- 根因是Task122同时锁死旧单体occluder Alpha轮廓；材质只能改变表面，不能改变50%体块读法。
- 因此停止ENV-A4，不扩其余五栋，不以更多纹理、噪声或线框细节伪装修复。

## 已封证据

- `../qa/NW_BLOCK_MATERIAL_PILOT_50_PERCENT_560x310.png`
- `../qa/NW_BLOCK_MATERIAL_PILOT_100_PERCENT_1120x620.png`
- `NW_BLOCK-material-pilot-readback.json`
- `../delivery/NW_BLOCK_FOUNDATION_CAMERA_V2_MATERIALIZED_RGBA.png`
- `../delivery/NW_BLOCK_OCCLUDER_CAMERA_V2_MATERIALIZED_RGBA.png`

本包只证明失败原因、锁注册方法和donor去语义方法；不得进入最终PLAN、CONTACT、Runtime、UA91、G2-B、Canon或对外视觉验收。
