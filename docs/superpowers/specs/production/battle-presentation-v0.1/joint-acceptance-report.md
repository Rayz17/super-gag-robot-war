# 馆守 Z 联合总装与 C01 切片验收报告

> 日期：2026-07-13
>
> 结论：运行时与 Canon 验收通过；内容时长与正式美术仍需真人验收。当前建议为“可继续试制，不提升为全项目正式模板”。

## 1. 验收矩阵

| 项目 | 结果 | 证据 |
|---|---|---|
| 只导入运行时批准资产 | PASS | 23 项记录中 17 项 `approved_for_runtime + runtime_allowed=true`；导入检查 0 错误 |
| 合同差异先报告 | PASS | `contract-diff-report-2026-07-13.md` |
| full / short / off 同一结算 | PASS | 三模式只消费同一 `last_resolution` 深拷贝 |
| 视频存在 | PASS | 测试 OGV 正常播放并返回 |
| 视频缺失 | PASS | 自动回退静态 Pose + Godot FX |
| 视频加载失败 | PASS | 现存非视频资源触发明确回退，不锁输入 |
| 任意阶段跳过 | PASS | 逐阶段 skip，无重复伤害、击破、对白或回合推进 |
| 连续播放 20 次 | PASS | 无残留节点、媒体状态或输入锁 |
| C01 Canon 顺序 | PASS | 今晚火灾后 30 秒 → 三小时前；馆守 Z 始终半跪 |
| 七海门控 | PASS | 0 号异响前无通讯热点；之后只走普通通讯 |
| 豪司边界 | PASS | 切片在豪司越权介入前结束 |
| 短战棋闭环 | PASS | 选人、武器、目标、待机、结束阶段、敌方行动、胜负与结算可闭环 |
| Windows 资源路径 | PASS | 13 个必需路径 0 缺失；测试视频未进入包 |
| Windows 可执行文件 | BLOCKED | 本机缺少与当前 Godot 版本匹配的 Windows export templates；PCK 已成功生成和读取 |
| 首玩 10–15 分钟 | NEEDS HUMAN TEST | 内容预算达到目标，尚无真人盲测数据 |

## 2. 内容验收

当前切片包含 5 幅动态漫画、15 句 ADV、2 个探索小场景、4 条主对话、3 种战前准备、3 回合战棋和 3 页战后回收。

探索不是清单门：玩家确认任一真实风险即可进入布置；多调查会增加方案和理解。重访不会重复首访选项。场景返回点保留在出口附近，不重置到初始点。

三条路线均被战棋实际消费：安全锁改变馆守 Z 的一次动作；撤离线改变保护目标容错；意图追踪改变敌方信息公开时机。结算再回写馆守 Z 半跪、低热和右臂仍连接的状态。

## 3. 战斗演出验收

- `full` 目标 7.17 秒，包含地图接近、兜灯 Cut-in、全比例半跪 Pose、掌部低热 FX、命中与回位。
- `short` 约 2.08 秒，保留识别动作与结果反馈。
- `off` 立即完成，只显示结算结果。
- 演出开始前战斗已经完成唯一结算；播放器没有伤害、击破、经验、行动结束或剧情事务写权限。
- 生产包无运行时视频，当前正式路径为静态 Pose + Godot FX；测试 OGV 仅覆盖视频状态机且从导出包排除。

## 4. 性能记录

测试环境：Apple M2 Max，OpenGL 3 Compatibility，1280×720。

| 指标 | 结果 |
|---|---:|
| 场景 ready | 252.990 ms |
| full 实际墙钟 | 7175.004 ms |
| 稳态平均 FPS | 106.384 |
| 稳态最低 FPS | 26 |
| 平均帧时间 | 8.665 ms |
| 最大帧时间 | 55.384 ms |
| 场景静态内存增量 | 80,366,610 bytes |
| 峰值静态内存 | 115,563,704 bytes |
| 场景纹理内存 | 63,499,451 bytes |
| 峰值纹理内存 | 118,418,585 bytes |

最低 FPS 和 55 ms 最大帧时间说明首次大图纹理进入 GPU 时仍有尖峰；正式章节需要预热或缩减 2048×2048 Pose 常驻策略。

## 5. 包体记录

| 项目 | 大小 |
|---|---:|
| 批准 PNG 原文件 | 12,150,459 bytes / 11.588 MiB |
| 同代码、排除 C01 战斗美术的 PCK | 9,638,012 bytes / 9.192 MiB |
| 当前生产 PCK | 18,478,756 bytes / 17.623 MiB |
| C01 战斗美术实际 PCK 增量 | 8,840,744 bytes / 8.431 MiB |
| 生产视频增量 | 0 bytes |

17 项批准资产中，当前切片直接使用 12 项，直接采用率 70.6%。馆守 Z 地图 idle 同时用于探索、战棋和演出；全比例 Pose 同时用于漫画、演出和战后页；无人机状态同时用于漫画、战棋和命中反馈。

## 6. 自动验证

```text
scripts/import_battle_presentation_assets.py --check      PASS
scripts/godot-test.sh                                    PASS
scripts/canon-check-godot.sh --strict                    PASS
scripts/canon-smoke-test.sh                              PASS
Windows PCK required-path validation                     PASS
```

视觉总览：`outputs/c01-slice-visual/contact-sheet.png`。

## 7. 验收结论

技术闭环、状态所有权和 Canon 门控已达到可继续内容试制的程度。当前不能宣称“正式模板完成”，原因是：

1. 还没有 3–5 名新玩家的完整首玩时长、迷路点和理解度数据。
2. 探索场景仍偏制图式，尚未达到万机馆值得停留和观察的美术密度。
3. 只验证了一台馆守 Z；尚未证明第二台体型、武器节奏完全不同的机体能低成本复用。
4. Windows PCK 路径通过，但本机 export templates 缺失，未产出独立 EXE。

推荐状态：`candidate pilot accepted with production conditions`。
