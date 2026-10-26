# Generation Log

日期：2026-08-25  
调用预算：`3/3 used`  
reroll：`0`  
后续调用：`false`

## Call A — GZ_V10X_E02_SHIELD_BASH_SOUTH

- 调用次数：1
- 参考：V10X 身份父图、V10X Camera V2 共用二维母图、A17 shield front、A17 shield rear。
- 明确禁止：既有 brace / shield_block 姿态输入、旧馆守 Z、3D/程序几何。
- 提示锁：south `[-40,+24]` 抬高正交；主动横拍；一盾；盾正面可见手数 0；双手只握盾背；三旧痕+第四热痕；E02 双臂、无翼无背包。
- raw：`call01/gz-shield-bash-south/generation-raw/GZ_V10X_E02_SHIELD_BASH_SOUTH_CALL01_RAW_FAIL_RGB_1254x1254.png`
- SHA-256：`22dba406cc2147289cd41b6dcb9874fb6763dd21f0d01b795eaac58f52f82e87`
- 结果：`FAIL_STOP_FRONT_VISIBLE_HANDS_CAMERA_AND_BASH_READ`

## Call B — BREAKER_GROUND_RED_BEAM_WEST

- 调用次数：1
- 参考：GF PLAN、GF CONTACT、当前正向二维透明母图、west 几何导图（geometry only）。
- 提示锁：west 前端左上/尾部右下；GF 长叶异质叠壳；四肢承力；只留短促枪口式红光；无长束/环境。
- raw：`call01/breaker-red-beam-west/generation-raw/BREAKER_GROUND_RED_BEAM_WEST_CALL01_RAW_FAIL_RGB_1402x1122.png`
- SHA-256：`bd58898b39abf59f4f3f2b3a5e9796ff918489c88b1f49162d0afeb1e6f4c253`
- 结果：`FAIL_STOP_CAMERA_V2_WEST_POLARITY`

## Call C — BREAKER_GROUND_HIT_RECOIL_WEST

- 调用次数：1
- 参考：GF PLAN、GF CONTACT、当前正向二维透明母图、west 几何导图（geometry only）。
- 提示锁：仍朝 west；不烘 root south 位移；四肢压缩/失衡/后仰/甲片错动；壳完整；无 beam/震动线。
- raw：`call01/breaker-hit-recoil-west/generation-raw/BREAKER_GROUND_HIT_RECOIL_WEST_CALL01_RAW_FAIL_RGB_1254x1254.png`
- SHA-256：`9692b7d85f41e6715b2da27cd117c06cad4c9cd5ec25efc8d657fce468236a71`
- 结果：`FAIL_STOP_CAMERA_V2_WEST_POLARITY_AND_RECOIL_READ`

## 停止边界

三张都在生成后人工像素硬门失败。没有 Alpha 抢救、没有脚本改轮廓、没有 256/384 注册、没有深浅底候选 QA、没有 Godot/Runtime/Default/Canon 写入。未将任何 raw 标成 Candidate sprite。
