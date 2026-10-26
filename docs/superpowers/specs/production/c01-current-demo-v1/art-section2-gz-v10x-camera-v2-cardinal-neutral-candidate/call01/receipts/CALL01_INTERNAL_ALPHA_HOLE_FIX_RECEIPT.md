# Call01｜馆守 Z V10X 封闭负空间 Alpha 修复回执

> 状态：`DETERMINISTIC_ALPHA_REPAIR_COMPLETE / ACTUAL_GUI_FRAMES_CAPTURED / USER_VISUAL_REVIEW_PENDING`
>
> `imagegen_calls=0`、`rgb_subject_bytes_changed=false`、`runtime_default_canon_promotion=false`

## 用户问题与根因

用户指出“抠图还有很多白色区域没有镂空”。原脚本只删除与画布边界连通的高亮中性背景；手臂、躯干和腿部轮廓封闭的负空间不与边界连通，因而棋盘/白底被错留为不透明。

## 确定性修复

仅对精确连通组件改 Alpha，不做全局 white-key，不改主体 RGB、画布、pivot、脚点或可见 bbox：

- `idle/east`：严格组件 bbox `[958,215,986,352]`、`1305 px`；包括中性边缘后删除 bbox `[958,214,986,364]`、`1420 px`。
- `idle/south`：严格组件 bbox `[244,819,273,970]`、`1582 px`；包括中性边缘后删除 bbox `[243,819,274,971]`、`1681 px`。
- `idle/north|west`：未发现同类封闭背景组件，字节不变。
- `brace/east`：删除 bbox `[761,457,834,535]`、`2952 px`。
- `brace/south`：删除 bbox `[448,429,512,576]`、`3751 px`，以及 `[714,427,842,615]`、`7071 px`。

白色/银色真装甲通过胸部中脊、大腿、腕环与脚尖哨兵点保留；四角 Alpha 均为 `0`，主连通域、可见 bbox、`pivot=[128,224]`、`canvas=256x256` 均不变。

## 字节与生命周期

- `idle/east` 新 SHA：`1f6907776a382dd9daacdb8854725392c8f8d662b402654250327eb66bb9bdb7`；旧 SHA `c6dd358980e19045626e0ed17de0614b543a971d7275cde76816e3f1d1f3b0de` 为 `REJECTED_ALPHA_HISTORY`。
- `idle/south` 新 SHA：`d1181e1b5d24903ed6f0e54c7e262815ddbed9e22e7a8135992dda188821b796`；旧 SHA `0b3d2f437558216b8d3a94a1ea5255f7b9310a94447ba530a1d89b210ccfc12d` 为 `REJECTED_ALPHA_HISTORY`。
- `brace/east` 新 SHA：`af2e6cc0d8bde79c756c175027f71d339549235fc737926a34adc890d706eebe`。
- `brace/south` 新 SHA：`a40e94a3c611367ebdf7d1c8fad708f90971f848e8429b1764ebcfb08707d696`。
- idle E/S 仅在 Candidate Demo 精确绑定中加载，`user_visual_acceptance=false`；brace E/S 仍 `texture_load=false`。

## QA 与实际帧

- 四向黑/深灰/高饱和洋红/高饱和绿、100%/50% QA：`call01/qa/GUARDIAN_Z_V10X_CAMERA_V2_CARDINALS_MULTIBACKGROUND_ALPHA_QA_100_50.png`。
- brace 同等 QA：`art-section2-gz-v10x-e02-wave-b-actions-candidate/call01/qa/GUARDIAN_Z_V10X_CAMERA_V2_BRACE_MULTIBACKGROUND_ALPHA_QA_100_50.png`。
- 实际 macOS GUI East：`game-godot/captures/c01_gz_v10x_bound_idle_actual_frame/run_20260824_07_alpha_fix/01_GZ_V10X_BOUND_IDLE_EAST_CAMERA_V2_1280x720.png`，SHA `9f0a9175108acb80a663fd75c9e52f93c61e7e58294b58e776adafe15c527f2f`。
- 实际 macOS GUI South：`game-godot/captures/c01_gz_v10x_bound_idle_actual_frame/run_20260824_07_alpha_fix/02_GZ_V10X_BOUND_IDLE_SOUTH_CAMERA_V2_1280x720.png`，SHA `773ceeb778a26e836381d4ab8347e28a941a168c0f9ab103d7f2d538a3cfd2f6`。
- 实际帧 manifest：`game-godot/captures/c01_gz_v10x_bound_idle_actual_frame/run_20260824_07_alpha_fix/actual-frame-manifest.json`，SHA `bbdddc618dcbcb9e4966692d1f45fc365dbb5ac64488dac02ebe280259c01b12`。

目视确认：用户箭头所指的手臂/躯干封闭孔已显示地图背景，没有白块或棋盘残留；白/银胸甲、腰甲、大腿和脚尖仍保留。
