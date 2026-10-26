# C01E02 Task109｜G2-A.2-C4 Camera A0 Pilot 完成回执

## 结论

- 机器状态：CAMERA_A0_COMPARISON_COMPLETE / FOCUS_REVEAL_INTERACTION_SUPPORTED / AWAITING_USER_CAMERA_SELECTION
- 本回执不选择正式 Camera V2，不替代制作人／用户实际帧视觉签收。
- 性能口径仅为 FIXTURE_30FPS_STABILITY_ONLY；FINAL_60FPS_NOT_PROVEN。
- 停止门：P109_CAMERA_A0_AND_FOCUS_REVEAL_PRODUCER_USER_VISUAL_SELECTION。

## 冻结输入

- Task104: 1ad0c1d0d5958f432f81479a119310769eaba3b769637b07ba7bcde127edfe61
- Task105: 6046293f86788b561e8e78f581cc1dcfa4968c206e0c5cadc74943aa9c5ef0b7
- Task106: 10c8df7490f21c2df12c513981867fd0168e86f9e789e46105c192996d2d4bf1
- Task106 C3 delivery manifest: b70fe98a3ca1019b5445cbbabb3862e29c614a52dbf6dee15b692a59bb4bca19（仅核受保护C3 source/content/scene/test/evidence条目）
- Task108: c33bc0ffa4fe6f5ecc553001e640eba18a39a917a0c4691def8c940ca0ad0280
- Task109: f67a86dda43d1a509e92f13a2f1f3e26fb29892c9d56a58fb9c5f7755242fd80
- tactical interface 1.6.6: f3ecc25c78a08cc61db422b832f56131df442f420170f46782b74807c6b9555a
- production board: e3a4ef982668a5bf87543bca88e79cf6eb7dd3735f0fcee453569183033477bd

## 证据摘要

- 三档相机对照帧：12 张；遮挡交互帧：8 张。
- 非headless性能：samples=600，p95=4.262ms，max=5.452ms，over33.3=0。
- 外部validator：valid=true；producer_user_visual_selection_passed=false。
- C4 source fingerprint：60964989e0c55a60a87ed78dc9d393be8426541d012a12bcf063522b54917ef3
- C2/C3/gameplay protected fingerprint：38462d6490d49f0abf807a27338388d9bd9c6adde6159a0130eb030875f1e3e6

## 证据入口

- receipts/01-camera-a0-contract.json
- receipts/02-focus-reveal-contract.json
- receipts/03-capture-manifest.json
- receipts/04-performance.json
- receipts/05-run-context.json
- receipts/06-machine-validation.json
- captures/（12张对照＋8张交互actual frames）
- logs/40-canon-report.log
- logs/41-canon-strict.log
- logs/99-final-regression.log
- delivery-hashes.sha256

## 边界

real_art_loaded=0；approved_handoffs=[]；Camera V2未选；ENV-A1、Call03、Call04、G2-B、Default、Save、Runtime、Canon均未开放或晋级。
