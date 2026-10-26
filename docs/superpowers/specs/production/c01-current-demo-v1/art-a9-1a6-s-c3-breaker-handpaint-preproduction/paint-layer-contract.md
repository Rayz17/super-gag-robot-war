# BREAKER Camera V2 人工概念重构分层合同

状态：`STOP_SCRIPT_SCAFFOLD_REQUIRES_HUMAN_CONCEPT_REDRAW / NO_SOLE_SCAFFOLD / NOT_FINAL_ART`

## 1. 当前没有可覆画底稿

REV1—REV4的1536／384图全部是History视觉失败证据，不得作为sole scaffold、清稿底图、描边源或局部覆画起点。

- REV1：圆壳＋四足龟兽读法；
- REV2：承重柱加强，但穹顶壳和四足读法仍占优；
- REV3：192纯黑union仍是驼背猿／熊；
- REV4：平顶楔壳和外张冲击垫有所改善，但纯黑剪影仍像驼背猿／双足熊。

最后脚本尝试保留在：

`qa/BREAKER_NORTH_CAMERA_V2_REV4_REJECTED_SCAFFOLD_RGBA_1536.png`

它只证明精确画布与失败根因，不能交人工画师直接覆画。下一步必须由真人概念美术重新构造剪影，不是在REV4上修表面。

## 2. 仍有效的精确接口

- 工作画布：`1536×1536 RGBA`；
- 最终地图槽基准：`384×384`，工作倍率`4×`；
- footprint：`3×3`；
- pivot：工作图`[768,1280]`，最终图`[192,320]`；
- Camera V2 north：最终`[40,-24]`，工作图`[160,-96]`；
- registration：`footprint_bottom_center`；
- 不允许手填screen offset、移动world anchor或改玩法占地。

这些数值是新真人概念重构的画布约束，不构成当前REV4的视觉通过。

## 3. B与X的责任边界

### B：新剪影和身体结构

真人概念美术必须重新解决：

- 非对称直线攻城楔，不是半圆穹顶、肩峰圆拱或驼背轮廓；
- 平顶偏置高脊和后端斜切形成机械攻城壳；
- 壳底抬高并保留明显胸腹负空间；
- 两条前肢是机械铰接的承重／冲击主柱，末端为外张楔形支脚或爪垫，不是圆脚、腿或熊掌；
- 两条后稳定器为薄短支架，尽量不形成第二对腿；
- 低嵌头必须是壳前侧横向嵌槽，不得形成口鼻、动物头或颈；
- 192纯黑剪影不看内部线仍必须读成半直立攻城／突入体。

### X：B通过后才开放的表面责任

X只负责非对称异质／生体甲片、受力柔性缝、窄红单缝、闭合胸缝、封闭上背出口、有限磨损和硬阴影。X不能拯救或改变失败的B剪影。

## 4. 未来合格概念图的推荐图层

| 顺序 | 图层／组 | 责任 | 进入192黑剪影 |
|---:|---|---|---|
| 00 | `GUIDE_camera_v2_3x3_pivot` | 精确网格、north、pivot、socket | 否 |
| 10 | `B_rear_stabilizer_brackets` | 薄短后支架 | 是 |
| 20 | `B_forelimb_far_hinge_ram` | 远侧机械铰＋冲击主柱 | 是 |
| 30 | `B_flat_offset_siege_wedge` | 平顶偏置高脊攻城楔 | 是 |
| 40 | `B_chest_negative_space_head_slot` | 胸腹负空间与横向嵌槽头 | 是 |
| 50 | `B_forelimb_near_hinge_ram` | 近侧机械铰＋冲击主柱 | 是 |
| 60 | `X_asymmetric_armor_primary` | B通过后才画的表面甲片 | 是 |
| 70 | `X_flexible_seams` | 受力柔性缝 | 是 |
| 80 | `X_red_slit_chest_outlet` | 红缝、闭合胸缝、封闭出口 | 是 |
| 90 | `CML128_A_line_shadow` | 深墨蓝线压、最多两级硬阴影 | 是 |
| 99 | `SOCKET_review_only` | 五socket评审层 | 否 |

## 5. Socket目标

所有local socket以pivot为`[0,0]`，仅作为未来真人概念图的初始目标，真实像素完成后必须复测：

| socket | 最终384 local | 工作1536 local | 工作1536 absolute |
|---|---:|---:|---:|
| `body` | `[0,-98]` | `[0,-392]` | `[768,888]` |
| `shield` | `[-68,-84]` | `[-272,-336]` | `[496,944]` |
| `weapon` | `[68,-96]` | `[272,-384]` | `[1040,896]` |
| `impact` | `[12,-18]` | `[48,-72]` | `[816,1208]` |
| `target` | `[12,-18]` | `[48,-72]` | `[816,1208]` |

## 6. 停止点

当前不授权人工“覆画REV4”，也不授权ImageGen、REV5脚本、其他方向、动作、CONTACT、Atlas、Runtime、UA91或Call04。只有制作人另行批准真人概念重构资源后，才可从空白Camera V2画布重新做B剪影；先过192纯黑门，再画X表面。
