# C01E02 A5 M2.4 后重冻结与续跑指令

> Status: `producer_refreeze_approved / resume_existing_A5`
>
> Lifecycle boundary: `Candidate / runtime_allowed=false / runtime_handoff=none`
>
> User decision: `not required for refreeze; required after A5 delivery`

## 1. 结论

A5 上次因冻结 Runner 从 `95ef71396de74c8076d61ea5b013a4db4aba672312dd9259e3d576297039b222` 漂移到 `de31ba758bd0490bbfa60e411f090e72a5741be322365db33fbff37e0c6c6f06` 而正确停止。该变化来自已授权并已完成的 M2.4 A4 MAP-B 五槽接入，不是未知漂移。

制作人现以 M2.4 终态重新冻结 A5 输入。除 Runner 这一项外，A5 原目标中的合同、A3 选源、A4 回执与评审底图、R2 slot/binding、Canon 三表均已复核，未发现漂移。A5 可以从现有生成器与校验器继续，不需要新的美术方向裁决。

## 2. 唯一权威回执

- 重冻结回执：`docs/superpowers/specs/production/c01-current-demo-v1/producer-a5/a5-m2-4-refreeze-receipt.tsv`
- 回执 SHA-256：`938e404e5c22728006aa907069a9fb7e663bc536a6b3ce918e0836c599fd8f1e`
- 全量冻结输入：`docs/superpowers/specs/production/c01-current-demo-v1/producer-a5/a5-refrozen-inputs.sha256`
- 输入清单 SHA-256：`7ef2553aff03036f787f692672987e4e2139931996fe68945b99d6f7c85b4702`
- M2.4 完成报告：`docs/superpowers/specs/production/c01-current-demo-v1/main-m2-4/05-completion-report.md`
- M2.4 报告 SHA-256：`b1ee2776b74f2158f8fd32d39db06969b08286e40897e5b2dba5b1b6f54823f7`

## 3. 续跑前强制动作

1. 从仓库根运行 `shasum -a 256 -c docs/superpowers/specs/production/c01-current-demo-v1/producer-a5/a5-refrozen-inputs.sha256`，29 项必须全部为 `OK`。
2. 重新运行 `python3 scripts/check_c01_current_demo_contract.py`，并查询 Current Canon 的 `ENEMY_C01_RIFT_SWARM` 与 `V355-C01E02`。
3. 在 `art-a5-rift-swarm-four-facing-atlas/generate_art_a5_rift_swarm_four_facing_atlas.py` 的 `STATIC_SOURCES` 中，只把旧 Runner SHA 替换为 `de31ba758bd0490bbfa60e411f090e72a5741be322365db33fbff37e0c6c6f06`。
4. 把本重冻结回执与 `a5-refrozen-inputs.sha256` 加入 A5 的 source-validation 记录；不得把 M2.4 的运行时资产复制进美术包。
5. 先编译检查生成器与 validator，再生成完整 A5 候选包并运行只读 validator。

任何一项再次漂移，继续硬停止并报告新的路径、期望哈希与实际哈希；不得自行二次刷新。

## 4. 恢复后的原任务范围

继续执行 `25-c01e02-a5-rift-swarm-four-facing-atlas-objective.md`，只交付：

- A「伏壳钳足型」96px `384×96` 四朝向 idle atlas；
- A「伏壳钳足型」128px `512×128` 四朝向 idle atlas；
- `atlas-spec.tsv`、六实例轻差分延期表、三机位比例对照、检查板、source receipt、asset manifest、decision card、completion report、核心哈希和可复现源；
- 所有输出继续为 `Candidate / runtime_allowed=false / runtime_handoff=none`。

仍禁止制作 move/impact/死亡动画、六套 atlas、Godot 接入、exact handoff、Runtime promotion、Canon/剧情/玩法修改、付费生成以及 `git add/commit`。

## 5. 停止门

交付完成后必须停在美术 Session，请用户逐项判断四向身份、接地点/红缝/扑击端、96px 或 128px 单一选型、六实例共用母版，以及所选文件与 SHA。未获得用户明确选型前，主程序不得接入 A5。
