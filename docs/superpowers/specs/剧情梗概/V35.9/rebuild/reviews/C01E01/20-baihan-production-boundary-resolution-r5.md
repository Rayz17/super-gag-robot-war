# C01E01 白函生产边界补丁关闭记录 r5

> Status: `patched_pending_independent_targeted_r6`
>
> Scope: 只关闭`19-canon-targeted-recheck-r5.md`的`R5-P01`。

## 修复

1. `v35_5_c01_c03_enemy_asset_budget_v35_5.tsv`
   - 白函资产明确拆成E02远程非实体子资产和E03完整旗舰Boss。
   - E02仅包含远程语音、重框投影、区域改报和从机调度。
   - 折叠封存臂、占格承伤、飞拳改图、Boss阶段和带伤撤离全部锁到E03。
2. `v35_5_c01_c03_mecha_exposure_v35_5.tsv`
   - E02的具名敌机栏只保留冷却针车和切割标尺机。
   - 白函远程语音/重框投影移入`remote_projection_non_count`锚点。
   - E02可计机体暴露从7改为6；E03完整白函计数保持不变。

## 实际验证

- 两张V35.5表TSV列宽：PASS。
- 白函定向`rg`：E02远程非实体、E03完整身体边界一致。
- `python3 scripts/check_v35_8_slot_loadout.py --max-errors 80`：PASS。
- `scripts/canon-check-godot.sh --strict`：PASS。
- `scripts/canon-smoke-test.sh`：PASS。

原Canon审稿席须重新读取两张当前表并给出独立r6结论；本记录不代替PASS。
