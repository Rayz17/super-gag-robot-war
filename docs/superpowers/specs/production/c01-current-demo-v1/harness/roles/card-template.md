# 评委卡模板

每席只填自己的面。出卡前不看其他席。长文即协议失败。

```text
# 席：<id>
round:
slice:
model:
verdict: pass | fail | warn
frame_evidence: present | missing
evidence:
- 
- 
- 
must_fix:
- 
preserve:
- 
advance:
```

- `pass`：本席硬问成立，且有证据。按量产战棋／机战专业标准，「盖住字也能指认」才算过；「大概能猜」是 `fail`。
- `fail`：本席硬问有一条不成立。多数票不能压过。
- `warn`：证据不足或无实帧。`warn` 不能当 `jury_consensus` 的盘面 / 体验门通过。
- 无窗口实帧时，盘面 / 机体奇观 / 体验门相关项不得 `pass`。
- 宁可少过，不要用「机器门已绿」或「设计意图如此」放行。
