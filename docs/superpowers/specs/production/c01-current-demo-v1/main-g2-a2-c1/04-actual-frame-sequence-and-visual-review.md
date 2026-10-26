# G2-A2-C1 Actual Frame、自然序列与目视复核

## 最终重抓帧

全部为 Godot 非 headless 1280×720 actual frame，`fixture_load_count=0`、`real_art_loaded=0`。

| ID | SHA-256 |
|---|---|
| `00_JOINT_REGISTRATION_CONTROL` | `bb89340b0deaa435178c1b172ed3c3ff902b45b722df6a22da91e7ddafa31dd9` |
| `01_PUBLIC_SITUATION` | `4d62d7876458991eb124dac1bfa64dcea08edcde685019e1d6ded7802020cc3e` |
| `02_EDITABLE_DRAFT_A` | `2bd9fa53a575ddafcc0c63a7557924d1fc5bb509a2b42966ae08bc0da5708fe1` |
| `03_EDITABLE_DRAFT_B` | `14d116e50535774defd76e2642f0a575fdaa1a86c557eebe0cf857ffb6611b41` |
| `04_COMMIT_SUMMARY_A` | `664ded8b6297fed5a89e99223eeab13e3860ccb75233a497ddc9a02b66ec6e59` |
| `05_COMMIT_SUMMARY_B` | `47f039ae23e5243273e6fd1c3f10719935614a28b7395415c941475bdc0d4fa8` |
| `06_T1_VEHICLE` | `c470e2c8f9c4e3476f35f84da3d79dfdb89f0c104970759dfbaf057edacfcdf0` |
| `07_T2_SWARM` | `415b7212ff096bfa5d3eb439a7a72ef9639c12a7853575f8bc7d3e6f7024dc08` |
| `08_T3_CONTACT_HITSTOP` | `6003d3c63550a95b5210403b6009b56a880001648177c524833999137c8e5ac2` |
| `08B_T3_CONTACT_HITSTOP_B` | `70c25f5409d3698eb61b7cd30e336e1d70960244cabd2e15a26c893af8574fd7` |
| `09_T5_A_B_CONSEQUENCE_COMPARE` | `916ff4904f537e61ade045b83bbe316c23609852d59a4ca737bc59d19317be5e` |
| `10_LOCAL_OCCLUSION_METHOD` | `a22314d7893f073e90dface7f736f030ba004cfeb317105d646aa50e8b14acc0` |

图片目录：[captures/](captures/)；逐帧机器 readback：[actual-frame-manifest.json](receipts/actual-frame-manifest.json)。

## 最终目视复核

- PUBLIC：应急车、三只小体、东门、警戒设施、墙挂重盾的类别轮廓与就地短标可区分；三威胁图例与地图轨迹一一对应。
- DRAFT/SUMMARY：显示“路线可行｜7/6步｜可查看预计后果”；SUMMARY 有“提交前摘要／返回修改／长按确认提交”的独立状态与 CTA。
- CONTACT：A/B 当前方案与 T3.00/T3.25 明示；未选卡片降级。已发生的 T1 车/T2 小体轨迹保留但降级，impact 区中段意图标签隐去，BREAKER 冲线/接触姿势为第一焦点。
- 产品帧未出现“中性构图占位”、“回读”、“生产”等内部词；通讯标识为“纪存｜战术通讯”。
- `00` 与 `10` 是联合注册/遮挡方法证据帧，不作为产品文案帧。

本次目视复核只是制作侧 preflight，不替代制作人 3/10/30 秒签收。

## 45–75 秒非静态自然序列

| 方案 | duration | samples | presenter exit | contact boundary | 结果 |
|---|---:|---:|---:|---:|---|
| A | 50.8s | 1031 | 1.745s | 2.585s | `exit < contact` |
| B | 50.8s | 1031 | 1.745s | 2.585s | `exit < contact` |

序列由 `GoldenSliceSession + Resolver + PerformanceDirector` 自然驱动，`direct_phase_injection=false`、`fixture_load_count=0`；非 headless capture 进程共渲染 1499 process frames。

证据：[actual-frame-manifest.json](receipts/actual-frame-manifest.json)、[natural-sequence.json](receipts/natural-sequence.json)、[40-actual-frame-capture.log](logs/40-actual-frame-capture.log)。
