# C01E02 ENV-A6/A7制作人资产签收与A8整屏试装放行

状态：`PRODUCER_SIGNED / SIX_MODULAR_STRUCTURE_ASSETS_ACCEPTED_FOR_EXACT_RECOMPOSITION / NOT_FINAL_PLAN`

## 制作人实际帧结论

制作人已查看A6单栋100%／50%和地图0.34显隐：`NW_BLOCK`从纯几何进入清楚的机战地图工业建筑语言，窗带、入口、屋面排水和设备间均服从Camera V2；未使用动态光、逐像素遮挡或复杂渲染。结论为`PASS_ASSET_METHOD_CANDIDATE / NOT_FINAL_PLAN`。

A7先经过隐藏名称、统一灰、50%轮廓门。首轮SE/NM/NW出现三栋近似风险，RGB未放行；REV2只改SE和NM后，六栋分别读作维修厅、安保办公附楼、仓储交通厅、服务廊、设备能源站和断连廊，机器最大高相似团由2降为1。制作人随后查看六栋RGB 50%／100%和整件`1.00→0.34→1.00`，结论为`PASS_SIX_STRUCTURE_ASSET_PACK_CANDIDATE / NOT_FINAL_PLAN`。

机器PASS不替代以上两次人工轮廓门和RGB门。

## 锁定证据

- A6完成回执：`art-a9-1a6-env-a6-camera-v2-one-structure-material-pilot/completion-report.md`，SHA256 `299ef6518b09ff5f8595fa20fbfe2dabcd4a1c8a5e5b3f180ae2fc0e2dd5b609`。
- A6交付清单：`art-a9-1a6-env-a6-camera-v2-one-structure-material-pilot/delivery-hashes.sha256`，SHA256 `8a31eb3556ab6e061b658caecae4b29f248953806036f89200e3020e6f06b29e`，全项通过。
- A7完成回执：`art-a9-1a6-env-a7-camera-v2-six-structure-asset-pack/completion-report.md`，SHA256 `5aab48f8dea0d2b52500b819adbba0c9c3c6f8b829227da134a3bc019166bd50`。
- A7交付清单：`art-a9-1a6-env-a7-camera-v2-six-structure-asset-pack/delivery-hashes.sha256`，SHA256 `ef67ad3be40ecb5f9a26f7bfe9a5149d281d090aef4e9c2be6e619d1673cb36f`，全项通过。
- A7机器报告：`art-a9-1a6-env-a7-camera-v2-six-structure-asset-pack/receipts/A7-machine-validation-report.json`，SHA256 `32b95f120f1d9c2307a8cf816290296543f08669b39f41a0ceff486507723c2b`。
- A7六栋50%板：`art-a9-1a6-env-a7-camera-v2-six-structure-asset-pack/qa/A7_SIX_STRUCTURE_GROUP_BOARD_50_PERCENT_900x560.png`，SHA256 `558662ef7a0630621f3110775af22a04319c31e7586b7f78c02aa98b9b2daa7e`。
- A7显隐板：`art-a9-1a6-env-a7-camera-v2-six-structure-asset-pack/qa/A7_SIX_STRUCTURE_NORMAL_REVEAL_GROUP_1800x1120.png`，SHA256 `07f640c6add9a3d470d01fcc12669360eb95de4092edfffb4e2bf385f7742c5a`。

## A8放行范围

放行一次零ImageGen、QA-only的Camera V2整屏试装：只读取A2被明确保留的`GROUND_BAKE_CURRENT_V2_2400x1350.png`、A7六栋独立foundation/occluder、Task111 Camera V2与structure registration；按原world坐标生成A/B PLAN和A/B CONTACT的actor-free cleanplate，不得手移建筑。

另用QA Proxy检查馆守Z／BREAKER脚点、路线和建筑前后关系，并只把实际相交的建筑occluder降到0.34。不得全图淡化，不得把Proxy写进资产。

A8只允许制作人判断整屏构图、实际遮挡和模块位置；不交状态物件、单位正式像素、最终PLAN、CONTACT演出或Runtime。

## 继续关闭

`STATEFUL_OBJECT_ART / BREAKER_REAL_MASTER / GUARDIAN_Z_MASTER / FINAL_PLAN / CONTACT / SPARSE_CLIPS / FINAL_60FPS / HUMAN_PLAYTEST / UA91 / G2_B / DEFAULT / SAVE / RUNTIME / CANON`继续关闭。
