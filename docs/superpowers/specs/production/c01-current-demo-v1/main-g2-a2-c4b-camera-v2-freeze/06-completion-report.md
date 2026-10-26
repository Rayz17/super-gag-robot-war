# C01E02 Task111｜G2-A.2-C4B Camera V2精确接口冻结完成回执

## 结论

- CAMERA_V2_40X24_EXACT_INTERFACE_CANDIDATE / A5_COMPATIBILITY_RECORDED / GAMEPLAY_UNCHANGED / REAL_ART_ZERO / AWAITING_PRODUCER_RELEASE_TO_ENV_A1
- A5裁决：V2_COMPATIBLE_FOR_PLAN。
- 本机器回执不开放ENV-A1、Call03或Runtime；不替代制作人实际帧签收。
- FINAL_60FPS_NOT_PROVEN。

## 输入锁

- Task110: 66e5cf7ac2b7e0ea06c33b26698124fd0918c7ab173104be8a2a6733e4f4d78e
- Task111: 7302a78a104533e1f97591cdfe78084ecaecfb181764939ded5c5d262e1f12bb
- tactical interface: 62f8a4aea770cc45c98ef48c827b67bf61c1712d769b0aeb15fdeb2a7855898c
- production board: 64d1c8c243dfd722dac50ca6627cc65d28b3533e2142d0529c8dfaa216680552
- Task109 report/manifest: 0d33c774c47620789d31a3131408f2137a98e890b2e68064b7890d24bbe5a773 / 185e3fc55de904cb096e6073236a2e51bc8acd7bb1cb2489101cae0b7efb798f
- A5 atlas bytes: 1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b

## 证据

- actual frame rows: 8。
- performance samples: 600；p95=2.862ms；max=6.273ms。
- external validator valid=true。
- C4B source fingerprint: 5e8bd55ed248914243ffa2e4e80fabd418a698a4be6ee8c67814fc979c7df639
- protected gameplay/C2/C3/C4 fingerprint: db1be3445ef90d7bef7046aaf38575060d5c2da39844bcc1cb499fef3aaa1ffe

## 入口

- receipts/05-A5-camera-v2-compatibility-receipt.json
- receipts/06-camera-v2-capture-manifest.json
- receipts/07-camera-v2-performance.json
- receipts/08-run-context.json
- receipts/09-machine-validation.json
- captures/（4 full + 3 A5 100% crops + 1 A5 50% map）
- logs/40-canon-report.log
- logs/41-canon-strict.log
- logs/99-final-regression.log
- delivery-hashes.sha256
