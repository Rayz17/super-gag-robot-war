# C01E02 G1.5-A 制作人只读回收

> Status: `A1_C_direction_user_approved / M1_shell_producer_accepted / B1_unlocked / C1_locked`
>
> Review date: `2026-08-07`

## 结论

- 用户在美术任务中以“C可以”选定馆守 Z 的 C“动作骨架型”，并在制作人任务中再次确认 A1。批准范围只是后续 Q/SD 派生方向。
- A1 的 96/128 px C 样张仍是 `direction_sample_not_sprite_master / runtime_allowed=false`；A/B 只留作未选参考。
- 本轮没有向主程序签发真实资产 handoff，也不授权把两张 C 样张当作 Sprite Sheet 直接加载。
- M1 接入壳通过制作人只读复核：六个槽位、零 approved handoff、零真实资源探测，G1.1 与共享入口未改变。
- 因此只开放 B1 的 BREAKER 设计探索；C1 真实总装、B2 及其后资产仍未开放。

精确 A1 文件、哈希、用户证据与生命周期见 `a1-user-approval-receipt.tsv`。

## 验证

- A1 `delivery-hashes.sha256`：全部通过。
- G1.5 M1 Godot asset-shell test：`C01_CANDIDATE_G1_5_ASSET_SHELL_OK`。
- `scripts/canon-check-godot.sh --strict`：通过。
- `python3 scripts/check_c01_current_demo_contract.py`：通过；预批准 Runtime 资产仍为 `0`。
- M1 的 27 个文件均在合同 allowlist 内；未修改 `project.godot`、启动路由、Autoload、共享 Current、Save/Profile 或 G1.1。

## C1 前必须补齐的程序门

M1 的任务是证明接口可以 fail-closed，不是开放真实接入。进入 C1 前，主程序还必须另行解决：

1. 将“M1 必须零 handoff”的验证器迁移为可校验制作人批准态的正式 Candidate handoff 流程；
2. 规范化资源路径并拒绝 `..` 等越界路径，而不是只做字符串前缀比较；
3. 将 handoff 的 `stable_id` 与制作人指定 ID 精确绑定；
4. 为 Sprite Sheet 增加 atlas/frame-region 映射，并在 D1 前实际探测视频尺寸。

这些是未来 C1/B4/D1 的阻断项，不阻碍当前 B1 美术方向探索。
