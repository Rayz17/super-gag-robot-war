# 馆守 Z V10X｜E02 盾动作 R2｜正向源隔离

> `Candidate / Section 2 internal / user=false / runtime=false / canon=false`

## 唯一馆守 Z 正向像素源

- `../art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_SOUTH_CANDIDATE_256.png`
- SHA-256：`d1181e1b5d24903ed6f0e54c7e262815ddbed9e22e7a8135992dda188821b796`
- 角色：用户已确认的 V10X 身份、`south=[-40,+24]`、Camera V2 40×24、比例与材质；字节已做 Alpha 修复，当前待新实际帧目视签收。

共享 RGBA master 只用于哈希交叉核验，不作为另一个设计来源：

- `../art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate/call01/masters/GUARDIAN_Z_V10X_CAMERA_V2_CARDINAL_NEUTRAL_SHARED_MASTER_RGBA_1254.png`
- SHA-256：`3ea73fac822c7c169d2715ab95a36f549c19f330a5c02bb9c031a0ecacf9cd3a`

## 唯一盾牌正向设计源

- `../art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`
- SHA-256：`169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305`
- 角色：用户接受的盾冠、厚边、中央承力脊、蓝白旧装甲、背面双握把与前臂轨。
- 本姿势发生在受击前；只保留三道宽浅旧擦压痕。A17 图中的赤红第四痕是未来受击状态，必须完全不存在，也不得改成白色第四痕。

## 无身份几何 guide

- `guide/GZ_V10X_SHIELD_TAKE_SOUTH_IDENTITY_FREE_GEOMETRY_GUIDE_1024.png`
- SHA-256：`5e9025f72f0500c87303d5b13c449e8a6b6f08839bd00b87dd46e1a1dce4bced`
- 角色：只锁 `shield_take` 的低位、偏心、上提、滚转、遮挡和双手在背面；它不提供馆守 Z 身份或盾牌造型。

## 禁止项

- CML008 旧馆守 Z 像素、旧 east、旧 Runtime copy；
- A2/A13/A14 弹孔装甲板；
- A18/A19/A22 失败 raw；
- 上一批 `shield_take` 失败 raw；
- 任意 cross-facing、mirror、generic、previous-pose fallback。

以上禁止图像的像素不会被打开、传入 ImageGen、合成、抠图或当作回退父图。
