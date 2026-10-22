# V30 C01-C03 严格ELO试跑

本目录是一次按V30严格创作门禁执行的前三章 episode loop 试跑。

## 目录结构
- `episodes/`：12个单话packet，作为生产源事实。
- `chapters/`：C01-C03三章可读组装稿，供连读审稿。
- `reviews/`：C01/C02/C03 prefix review，以及C01-C03 opening arc review。
- `ledgers/`：首登机体、名台词、关系、主角弧线、纪存记忆、敌方收益、严格体验门禁、校验记录。

## 本轮关键取舍
- C01保留闭馆夺名、馆守Z、勇者审批、展舰起航，但补足万机馆厚度、真实机体首登和展舰巨物感。
- C02保留模型街、火种货柜、重涂、旧拳王，但把采购/价格生态写成真实战斗、隐私保护和外部开馆节点。
- C03采用V26候选迁移，把第0次站立、工务城、小查和三法城前移，灰模母版/白鸢正式线后移C04，仅以未署名分镜尾钩建立引力。

## 审查口径
本轮使用三位真实subagent作为批量侧写顾问：
- canon/素材与运行约束：`019f2e76-6414-7780-bfd8-cc3f2968d1c0`
- 机体/IP/名台词挂载：`019f2e76-8977-7260-be13-9358845f3fc5`
- 主角/关系/燃泪梗建议：`019f2e76-adf0-7aa1-b00c-9298b2c5f0c8`

因为本轮是三章试跑，不是108个独立新agent逐话审稿，校验命令显式使用 `--allow-reused-subagent-ids`，并在 `ledgers/run_validation.tsv` 中记录。

## 验证命令
```bash
python3 /Users/rayz/.codex/skills/chao-gag-writing-pipeline/scripts/check_episode_loop_run.py docs/superpowers/specs/剧情梗概/V30 --require-subagents --allow-reused-subagent-ids --require-chapter-reviews --require-run-validation-log --strict-prefix-warn-policy --strict-creative-gates --min-story-chars 1200 --min-new-ip-units 2 --min-wanji-c01-samples 8
```

当前结果：`pass`。
