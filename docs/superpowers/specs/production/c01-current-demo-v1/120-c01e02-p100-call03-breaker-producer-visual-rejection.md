# C01E02 P100：Call03 BREAKER北向母版制作人视觉拒收

状态：`COMPLETE_VISUAL_FAIL / CALL03_CONSUMED / NO_REROLL / CALL04_FALSE`

## 裁决

Call03唯一原图已由制作人按50%／100%两级门目视。第一读法明确是龟形／普通四足兽，且朝向不符合Camera V2 north；因此不能制作384母版，不能开放Call04。

## 证据

- raw：`art-a9-1a6-s-c2-call03-breaker-north-v2/generation-raw/CALL03_BREAKER_NORTH_RAW.png`
- raw SHA-256：`0aef14923503f0c132343cb0223306580470911bfe32b9e57a5fe33e0664c592`
- 50/100自审 SHA-256：`1303af4bffbcd9967e15463268a2f2ee0abe1af1321f14c631815bfebba02a17`
- 失败封包manifest SHA-256：`cc99940c750949f6093bcfa6b76a787828c3db3c62768d0c3735a57a2af60632`

50%失败：四肢等权落地、后足不短、壳体横卧，整体读成龟／普通四足，而不是B的前肢承重半直立突入体。

100%失败：虽然保留黑甲与窄红缝，但表面偏工业对称板甲，缺少X的异质非对称生体甲、柔性缝和B的短后足承力关系；身体朝向也不是north屏幕向量`[40,-24]`。

该raw仅保留History失败证据，不得用作地图Sprite、identity donor、CONTACT、Atlas或环境遮挡输入。不得自动reroll或挪用Call04。
