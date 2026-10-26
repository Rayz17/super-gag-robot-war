# C01E02 ENV-A1｜模块化精品环境美术派发回执

日期：2026-08-21  
任务ID：`A9_1A6_ENV_A1_MODULAR_TACTICAL_ENVIRONMENT_KIT_MASTER`  
目标任务：美术资产-2 `01a018f7-b863-7973-9d4e-f11e9982024a`  
状态：`DISPATCH_AUTHORIZED / ONE_ENVIRONMENT_CALL / NO_REROLL / CALL03_CALL04_FALSE`

## 1. 历史包边界

Task111制作人签收前，`main-g2-a2-c4b-camera-v2-freeze/delivery-hashes.sha256`已从仓库根逐项校验全绿，manifest SHA为：

`cf01823c07d904c38ffad076f08fddba6b0d72f0fcb68ab731ab0cdcb3a7d83b`

该历史manifest锁定了签收前的看板SHA `64d1c8c2…680552`和interface SHA `62f8a4ae…5898c`。P111签收后对这两份治理文件的合法前移不回写Task111 manifest；Task111输出字节继续由原manifest封存，后继派发改由本回执锁定。

## 2. 派工输入

| 文件 | SHA-256 |
|---|---|
| `112-c01e02-p111-camera-v2-exact-interface-producer-acceptance.md` | `2eda6f614f46b0ba8ef43adc76ff08152d63d3560a5e4b19989c7612d44a2793` |
| `113-c01e02-a9-1a6-env-a1-modular-tactical-environment-kit-master-objective.md` | `f8148ac350ca30a48e991ac73aaf6de3949b3f85c00a473d643819ab601efdde` |
| `38-c01e02-m3-r0-5-production-board.tsv` | `668ab2e882196f28efd6993af0f0453c588a6e465c28a663699d1b37bc494fbe` |
| `c01e02-tactical-visual-interface-v1.json` | `5dc09a26ff0124edd9bc2c3d05f9a0b180ae544ce9c04477664ac9061a443e2f` |
| Camera V2 exact合同 | `756f77db883fd060fdd323d2533191ade689c0a1362f92f043fac17dbe28ab4a` |
| 六建筑／对象注册表 | `0133cf5c5af7a6dba659221249b9e0bb45c51bebc8cb9b81c50cf9d920d25b7b` |

开工时若上述任一SHA不符，必须先确认是否为本回执后的制作人合法治理更新；不得静默读取漂移输入。

## 3. 调用与停止门

- 环境专用预算：`total=1 / used=0 / remaining=1`；派工后允许执行；
- 原单机母版预算：Call03／Call04保持未使用、未开放；
- 首次环境调用后无论成败，环境预算记为`used=1 / remaining=0`；
- 任何整屏烘死、模块不可分离、角色混入、Camera V2漂移或视觉50%失败，均直接收口，不reroll；
- 完成态只到P102实际帧审查，不接Godot真实资产、不开放Runtime／Canon／UA91／G2-B。
