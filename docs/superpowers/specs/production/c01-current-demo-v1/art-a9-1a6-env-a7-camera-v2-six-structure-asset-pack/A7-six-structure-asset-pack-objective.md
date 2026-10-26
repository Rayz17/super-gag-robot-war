# C01E02 ENV-A7：Camera V2六栋独立Structure资产包任务书

状态：`DISPATCHED_ZERO_IMAGEGEN / SIX_INDEPENDENT_STRUCTURES / NOT_PLAN`

## 上游放行

- A5制作人裁决：`PASS_STRUCTURE_HIERARCHY / NOT_FINAL_ART`。
- A6制作人裁决：`PASS_ASSET_METHOD_CANDIDATE / NOT_FINAL_PLAN`。
- 本任务只扩六栋独立Structure资产，不开放地图PLAN整合。

## 权威冻结

六栋逐字继承Task121各自`grid_rect / local canvas / pivot / front edge / visual envelope / world-height limit`；Camera V2只允许`(40,24)`、`(-40,24)`与竖直结构边，无透视汇聚、无手工screen offset。

| ID | 用途 | 高度上限 |
| --- | --- | ---: |
| `NW_BLOCK` | 展馆维修厅；逐字继承A6 foundation与occluder | 90px |
| `NM_BLOCK` | 中型办公／安保附楼 | 72px |
| `NE_BLOCK` | 仓储／交通厅 | 90px |
| `SW_BLOCK` | 服务廊 | 72px |
| `SE_BLOCK` | 设备／能源站 | 90px |
| `BROKEN_SKYWALK` | 低矮断连廊 | 54px |

所有foundation逐字继承Task121（NW的A6 foundation与Task121字节一致）；每栋occluder允许在自己的固定envelope与高度上限内独立重做Alpha和RGB。玩法占地、pivot、front edge、reveal cells与排序责任不得改变。

## 差异化硬约束

- `NM_BLOCK`：紧凑办公主楼、偏角安保观察体与短入口檐；50%识别点是高低错位的角部观察体。
- `NE_BLOCK`：横向低仓储大厅、长条屋顶采光／交通脊与宽装卸檐；50%识别点是长脊和宽入口。
- `SW_BLOCK`：狭长分段服务廊、两个不同高度端部与连续侧廊；50%识别点是横向分节节奏。
- `SE_BLOCK`：低设备基座、两级主设备体与偏置高能源块；50%识别点是紧凑多级设备群。
- `BROKEN_SKYWALK`：左右桥头、两段断裂桥舌和明确空隙；50%识别点是无法误读为完整建筑的断口。
- 禁止把同一盒体缩放、换色、增减一个小设备后冒充另一栋。

## 共享美术语法

每栋4—7个主要色值块；共享克制的防水屋面、连续窗／服务面、明确入口、设备层、最多三处暖色边灯与低频雨蚀。建筑用途决定这些元素的比例和位置，不共享同一面板排布。禁止旧donor几何、照片噪声、动态光、shader、SubViewport、ImageGen、文字或招牌。

## 必交与停止门

- 六栋各自独立foundation/occluder；完整`1.00 -> 0.34 -> 1.00`。
- 六栋100%与50% group board、normal/reveal group board。
- `camera-pivot-angle-audit.tsv`、`role-distinction.tsv`与标准化Alpha重复度审计。
- machine report、source lineage、manifest与全包SHA。

若50%有三栋以上第一读近似，或重复度审计出现三栋高相似团，立即封存`FAIL_REPETITION`，不得进入PLAN。任一角度、pivot、grid、front edge、height、envelope或foundation失败同样停止。机器PASS和内部目视只允许制作人审六栋资产板，不开放最终PLAN、Runtime、UA91、G2-B或Canon。
