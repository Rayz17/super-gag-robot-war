# 馆守 Z V10X｜E02 Wave B 动作精灵｜正向源隔离

> Status: `Candidate / Section 2 internal production`
>
> `user=false` · `runtime=false` · `default=false` · `canon=false` · `godot_bound=false`

## 唯一正向馆守 Z 输入

- `call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_EAST_CANDIDATE_256.png`
  - 来源包：`art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate`
  - SHA-256：`1f6907776a382dd9daacdb8854725392c8f8d662b402654250327eb66bb9bdb7`
  - 用途仅限 `brace/east` 身份、朝向、相机、比例与材质。
- `call01/map-candidates/GUARDIAN_Z_V10X_CAMERA_V2_IDLE_SOUTH_CANDIDATE_256.png`
  - 来源包：`art-section2-gz-v10x-camera-v2-cardinal-neutral-candidate`
  - SHA-256：`d1181e1b5d24903ed6f0e54c7e262815ddbed9e22e7a8135992dda188821b796`
  - 用途仅限 south 动作的馆守 Z 身份、朝向、相机、比例与材质。

两张源均保留用户已确认的 V10X 设计/朝向/注册，但字节已做确定性 Alpha 修复，当前为 `CANDIDATE_VISUAL_REVIEW_ONLY`。该方向认可不扩张到本包动作。

## 唯一正向盾输入

- A17 用户已接受退役重盾基底：
  `art-a17-section2-true-retired-heavy-shield-candidate/user-confirmation-call01/generation-raw/TRUE_RETIRED_HEAVY_SHIELD_CALL01_RAW.png`
- SHA-256：`169c162c5b2bd0761d535d7dee8573fc547952090dfa7947c3b9630af1c72305`
- 派生时只允许读取该包的 front exterior / rear interior 确定性切图；正面与机体正面同向，双手只接触背面双握把。

## 全部禁止作为正向像素或派生父图

- CML008 旧馆守 Z 像素与旧 east sprite；
- A8、A13、A18、A19、A22 失败 raw；
- QSD 旧图、旧 SVG、旧 Runtime copy；
- A2、A13、A14 弹孔装甲板；
- 任意 cross-facing、mirror、generic 或 previous-pose fallback。

本包没有读取上述禁止项的像素。History 仅能在文字审计中被列名，不得参与 ImageGen 输入、抠图、合成或回退。
