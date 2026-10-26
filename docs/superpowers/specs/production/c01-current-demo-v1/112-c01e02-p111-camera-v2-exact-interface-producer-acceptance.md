# C01E02 P111｜Camera V2 40×24精确接口制作人签收

日期：2026-08-21  
任务ID：`P111_CAMERA_V2_EXACT_INTERFACE_PRODUCER_REVIEW`  
状态：`COMPLETE_PRODUCER_ACCEPTED_CAMERA_V2_40X24_EXACT / A5_PLAN_COMPATIBLE / ENV_A1_RELEASED`

## 1. 制作人结论

制作人已逐张查看Task111的4张1280×720 A/B PLAN／CONTACT实际帧、3张A5 100%方向裁片和1张A5 50%地图帧，并独立核验Task111 delivery manifest。

现签收：

- `CURRENT_TOPOLOGY_CAMERA_V2_40X24_CANDIDATE`作为C01E02精品Demo当前正式Candidate地图相机；
- 32×18、正交dimetric、`tile_half=[40,24]`、四组PLAN／CONTACT相机、2400×1350 world canvas、六建筑和独立战术物件注册接口进入ENV-A1唯一责任源；
- 40×24相较旧40×20降低低视角遮挡压力，又没有40×26的额外纵向展开与裁切压力；
- A／B PLAN共同构图、A T3.00／B T3.25 CONTACT均保持原玩法位置、接触与路线语义；
- A5现有96px小体四向图在40×24 PLAN中脚点、朝向与体量可读，裁决为`V2_COMPATIBLE_FOR_PLAN`，无需重画；该结论只覆盖PLAN／idle，不外推T1—T5动作完整性。

Task111画面中的纯色建筑和中性巨体仍是接口Proxy，不是视觉资产或最终Demo效果。本签收批准美术按该接口生产模块化精品环境，不把Proxy视觉质量误报为已完成环境。

## 2. 已核输入与证据

| 责任 | 路径 | SHA-256 |
|---|---|---|
| Task111目标书 | `111-c01e02-g2-a2-c4b-camera-v2-exact-interface-freeze-objective.md` | `7302a78a104533e1f97591cdfe78084ecaecfb181764939ded5c5d262e1f12bb` |
| Task111完成回执 | `main-g2-a2-c4b-camera-v2-freeze/06-completion-report.md` | `b82b07a35bd4dabc60bc3dd909c84554787f6857a15d1026cff92bc0f06f0c45` |
| 机器总回执 | `main-g2-a2-c4b-camera-v2-freeze/receipts/09-machine-validation.json` | `42c7fef811b259fba674f875aec5271f2c8b878fcf81348b86726a6a227f508d` |
| 实际帧manifest | `main-g2-a2-c4b-camera-v2-freeze/receipts/06-camera-v2-capture-manifest.json` | `4275e63d9b748ce512995fa7cc316186d48dcb9fb4b1ab71c20507d639233242` |
| A5兼容回执 | `main-g2-a2-c4b-camera-v2-freeze/receipts/05-A5-camera-v2-compatibility-receipt.json` | `63cb547dff5c2672883451fb942181b835a30c301ea6030b656d9874e4bc1f20` |
| Task111交付manifest | `main-g2-a2-c4b-camera-v2-freeze/delivery-hashes.sha256` | `cf01823c07d904c38ffad076f08fddba6b0d72f0fcb68ab731ab0cdcb3a7d83b` |
| Camera V2 exact合同 | `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/current-topology-camera-v2-40x24-contract.json` | `756f77db883fd060fdd323d2533191ade689c0a1362f92f043fac17dbe28ab4a` |
| 建筑／对象注册表 | `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-structure-object-registration.tsv` | `0133cf5c5af7a6dba659221249b9e0bb45c51bebc8cb9b81c50cf9d920d25b7b` |
| Sprite／socket合同 | `game-godot/content/candidate_runtime_demo/c01/e02/m3_golden_slice/g2_a2_visual_compositor/camera_v2_freeze/camera-v2-sprite-slot-and-socket-contract.json` | `a6874f033554c71af2e3c1d634cd2671d4a3efd1494ba0bccb491579c0117cce` |

`delivery-hashes.sha256`已逐项`shasum -a 256 -c`全绿。Task111机器回执只能证明精确接口、注册和fixture性能；制作人的实际帧签收才完成本P111门。

## 3. ENV-A1现在开放

立即开放`A9_1A6_ENV_A1_MODULAR_TACTICAL_ENVIRONMENT_KIT_MASTER`：

- 允许使用用户在Route A2中单独批准的**1次环境专用ImageGen调用**；
- 该调用与原Call03／Call04两次单机母版预算完全隔离，不得挪用或互相冲销；
- 目标必须是`GroundBake + 6个独立Structure + 独立盾／东门／警戒设施／A/B道路结果`的模块化套件；
- 禁止整屏含建筑烘死、禁止角色、禁止自动reroll、禁止旧A4语义像素和ENV-E0失败像素回流；
- ENV-A1交付后进入P102制作人50%／100%实际帧审查，再决定是否开放Call03 BREAKER。

## 4. 仍保持关闭

本签收不开放：

- Call03 BREAKER、Call04馆守Z；
- CONTACT母版、稀疏动作Atlas、真实Runtime接入；
- UA91、G2-B、Default入口、Save、Canon晋级；
- `FINAL_60FPS_PROVEN`、`FUN_PROVEN`或真人试玩结论。

ENV-A1一旦出现整屏合成、结构不可分离、40×24视角漂移、建筑遮住选择口袋或身份对象错位，立即按单次调用失败收口，不自动再生图。
