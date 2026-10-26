# C01E02 P109｜Camera A0与焦点显隐制作人签收

日期：2026-08-21  
责任人：制作人-2  
状态：`PRODUCER_SELECTED_40X24 / FOCUS_REVEAL_ACCEPTED_FOR_C4B / REAL_ART_ZERO / ENV_A1_STILL_HELD`

## 1. 签收结论

Task109机器与交付闭合，制作人已逐张查看12张相机对照和8张显隐交互帧。正式选择：

`CAM_A0_V2A_40X24`

40×24作为Camera V2的唯一精确重注册输入；40×20保留为低俯角History基线，40×26保留为高俯角对照，不进入后续美术。

本签收只选择Candidate视角并接受“独立建筑上部整件alpha显隐”交互方法，不直接把Pilot camera晋级为正式接口。ENV-A1仍须等待C4B完成投影、crop、canvas、pivot、socket、建筑注册与A5兼容性冻结。

## 2. 选择理由

### 40×20不选

- 仍是用户指出的低俯角基线；
- A PLAN焦点读回需要淡化2栋，建筑遮挡压力最高；
- CONTACT时大体proxy与近景建筑叠压最明显。

### 40×24入选

- A PLAN焦点淡化目标由2栋降为1栋；
- CONTACT仍保留巨体立面与方向感，没有明显变成俯拍棋子；
- 东门、警戒设施、撤离方向和底部UI仍有足够安全边；
- 与40×26相比已取得主要遮挡收益，构图更稳健。

### 40×26不选

- 遮挡收益相对40×24很小，同样主要淡化1栋；
- 地图纵向展开继续增大，东门／南缘对象更接近底部UI与裁切边；
- 对最终机体地图画法的顶面要求更高，当前Demo没有足够收益承担额外返工。

## 3. 焦点显隐签收

接受以下产品方法：

- Ground与foundation不淡；
- 只改变真正遮挡焦点的独立occluder alpha；
- 鼠标与手柄同格结果一致；
- 建筑自身focus保持不透明；
- T3 CONTACT可自动显隐；
- 无SubViewport、逐像素mask、动态光、第二Owner或Actor alpha修改。

冻结的第一轮路线没有穿过六栋建筑遮挡范围，因此route-trigger按fail-closed不透明是正确结果，不要求为演示伪造路线或移动建筑。

## 4. 已核证据

- 完成回执：`main-g2-a2-c4-camera-a0-pilot/06-completion-report.md`，SHA `0d33c774c47620789d31a3131408f2137a98e890b2e68064b7890d24bbe5a773`
- 机器验证：`main-g2-a2-c4-camera-a0-pilot/receipts/06-machine-validation.json`，SHA `95a57a0cf69f2e57968d37385f2ff05e7be115954abdf81d312cd519cfad77a5`
- 交付清单：`main-g2-a2-c4-camera-a0-pilot/delivery-hashes.sha256`，SHA `185e3fc55de904cb096e6073236a2e51bc8acd7bb1cb2489101cae0b7efb798f`；独立`shasum -c`全PASS。
- 12张相机对照＋8张显隐帧；注册误差0px。
- 非headless 600帧：p95 `4.262ms`、max `5.452ms`、超过33.3ms为0。
- 外部validator 12／12分区PASS、0 error；Canon report／strict PASS。

关键目视帧：

- 40×20 A PLAN：`captures/01_V1_40X20_A_PLAN.png`，SHA `477ad6fc819694df281d449463e9cf451ccae443684334b5db6ed2146adcc282`
- 40×24 A PLAN：`captures/05_V2A_40X24_A_PLAN.png`，SHA `34af047a344f5cce8e8b46737e668a74becc31b2578a3325d928577b3c670954`
- 40×26 A PLAN：`captures/09_V2B_40X26_A_PLAN.png`，SHA `6b314c400ce3bf8532dba8b5daa472a6c87fee11b68e05b00a983b48fb8ca349`
- 40×24鼠标显隐：`captures/14_V2A_MOUSE_HOVER_REVEAL.png`，SHA `a2677ecb61ebd262c8ef6866508aec1902417e237d4f1945cf6a09e7833c1511`
- 40×24 T3自动显隐：`captures/17_V2A_T3_CONTACT_AUTO_REVEAL.png`，SHA `496b668712e436cfe435a076d6f308a35632b9948fc2a8cc083c366be540452f`

## 5. 立即开放与继续关闭

开放：

- `G2_A2_C4B_CAMERA_V2_EXACT_INTERFACE_FREEZE`

继续关闭：

`ENV_A1 ImageGen / Call03 / Call04 / real_art / final_60fps / FUN / UA91 / G2-B / Default / Save / Runtime / Canon`

