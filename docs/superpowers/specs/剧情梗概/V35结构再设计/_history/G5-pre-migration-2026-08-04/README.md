# G5-02 Working 迁移前回滚锚

> 快照时间：2026-08-04 15:41（Asia/Shanghai）
>
> 状态：`history_quarantined_pre_migration_snapshot`

`working-baseline.tar.gz`保存G5-02正式迁移前的Working L1/L2/L3、相关故事表、Canon源、Runtime生产来源、设计图谱、生产看板与知识底座校验脚本。

本目录仅用于整单回滚和差异追溯，不参与Writer检索，不构成第二份Working。

迁移前机器快照清单：

- `docs/superpowers/specs/data/story/v35_g5_pre_migration_snapshot_v1.tsv`
- 28个文件或文件树指纹已通过`build_v35_g5_pre_migration_snapshot.py --check`。
- Reader文件树和五份`C??-story-chain.tsv`是`NO_EDIT`对照项；同目录的三份生产状态注册表不属于故事链正文，允许随正式迁移同步。

若G5-03校验无法在同一根因三轮内通过，使用本快照整单恢复，不逐文件手工拼回。
