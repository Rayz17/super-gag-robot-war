# Camera V2 双主体地图母版输入预审

状态：`INPUT_PREFLIGHT_CANDIDATE`；`runtime_allowed=false`；不改 Canon、Godot、Atlas 或现行环境。

## 当前权威分层

- Hard：CML008 只锁馆守Z 18m 身份、E02 双臂与无翼无背包边界；Hard 图仅人工交叉检查，不喂生成器。
- Working：CML128 `KINETIC_CEL` 只以文字约束线压、4–7 大色块、最多两级硬阴影；含冲突翼背机体的风格图不喂生成器。
- Candidate：V10X E02 与最新 Q/SD 是馆守Z本轮身份、结构、比例责任源；GF PLAN/CONTACT v2 是用户最新确认的 BREAKER 具体设计责任源；Camera V2 合同只负责投影、方向、画布、footprint 与 pivot。
- History：Call03 龟形、B+X替代造型、眼平 east、旧Q、A8程序图、A9.1-A3 Blender/SVG/R1及其他失败派生均不得成为生成参考。

## 调用输入角色

- 馆守Z：`GZ_EAST_CAMERA_V2_EXACT_GUIDE_256.png` 决定 elevated dimetric east 与 pivot；V10X 决定 E02 结构；单主体 Q/SD front 决定约4头身重量与配色。三者不互相替代。
- BREAKER：`BREAKER_NORTH_CAMERA_V2_EXACT_GUIDE_384.png` 决定 elevated dimetric north 与 pivot；GF PLAN v2 决定巨大异质黑壳、低嵌头与整体轮廓；GF CONTACT v2 只补充前部承力关系。
- A8/A9整屏只在生成后做 Camera V2 同屏 QA，绝不喂生成器。

每主体最多一次定向调用，零 reroll；任一首读身份失败即停止，不靠后处理改变身体或掩盖失败。
