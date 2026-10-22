# C01E01 定向补丁关闭记录 r2

> Status: `all_r2_findings_patched_pending_independent_r3_receipts`
>
> Scope: 仅关闭07-11五席复审列出的局部问题，不以本记录替代独立终检。

## 1. 关闭矩阵

| 来源 | 遗留项 | 关闭证据 | 状态 |
|---|---|---|---|
| 剧情监督07 | R2过早结算29人 | Runtime把R2锁为`A_STAGE_BC_FINAL_LINE_D5_GATE`，R3新增独立撤离相位，只有`RT010A`提交`29/29, 4/4` | `CLOSED` |
| 机甲/IP 08 | 无遗留 | 馆守Z仅场景支援；社勇王/市政吊装机仅真实首显；模型不计机体 | `PASS_PRESERVED` |
| 玩法制作09 | 缺8x10坐标和移动常量 | `C01E01-graybox-constants-v1.tsv`固定网格、起点、路线、移动、闭馆线、侧门、传感格、反射座与三回合回执 | `CLOSED` |
| 玩法制作09 | D5维修员可能生成第五Token | Runtime与graybox均锁`D5=4需协助成人+维修员`；机器犬只附着既有D5，不生成人员标记 | `CLOSED` |
| 玩法制作09 | 胸灯执行权与重瞄不闭合 | 玩家选离散反射座，唐胶执行，兜灯在确认前否决；`BLOCKED_BY_DOUDENG -> AIM_PREVIEW`不耗行动、不提交状态 | `CLOSED` |
| 玩法制作09 | 无失败/回滚分支 | `RT011F`规定R3末未完成即`RETRY_NO_STATE_COMMIT`；成功只在`RT011/RT013S`原子提交 | `CLOSED` |
| 关系10 | 唐胶材料否决权未传播 | Runtime、正文结算与下一话输入同时提交`TANGJIAO_MATERIAL_VETO_AUTHORITY=PERSISTS_TO_E02_E03` | `CLOSED` |
| 关系10 | 作者辩护残留 | 已删除主题答辩段；戏剧指纹只以正面动作句说明解法 | `CLOSED` |
| Canon 11 | 白函E02/E03生命周期冲突 | 生成器锁E02远程无格/无HP，E03完整身体首战；V35.8重新生成并通过严格语义校验 | `CLOSED` |
| Canon 11 | 七海私人/公务时序 | Canon scene与Runtime锁零号前私人语音、零号后只读公务频道、E01无系统改变命令 | `CLOSED` |
| Canon 11 | 馆守Z右臂状态 | Canon地点、正文与快照统一为臂核连接、仅前臂外甲拆检 | `CLOSED` |
| Canon 11 | L1远星副柜缺失 | Canon新增L1只读副柜；只读L3离线缓存，不开L3、不实时通信 | `CLOSED` |
| Canon 11 | 闭馆灯与四令物理动作混写 | 唯一快照分开记录：展陈灯由闭馆熄灭；四令锁门、断胸灯、冻数字钥匙、停泵；城市电网与维生在线 | `CLOSED` |
| Canon 11 | 人命/藏品旧枚举仍活跃 | 生成器、V35.5/V35.7上游、S01/S02压力板迁为`C01_EVAC_PRIORITY=PEOPLE_FIRST_FIXED`；载荷只留E04 | `CLOSED` |

## 2. 纸面三回合复演

### R1

- A11由`(2,6)`移动2格至`(2,4)`。
- B10由`(3,7)`至`(3,5)`；C3由`(4,7)`至`(4,5)`。
- 机器犬在`(7,7)`打开`(7,6)`侧门并附着已含维修员的D5；D5不移动、不拆分。
- 跌跌复位路径框，环境相位将其重闭。

### R2

- 玩家确认跌跌主动侧倒，路径框只在本回合撤离相位处于`JAMMED`。
- A11至黄线`(2,2)`；B10/C3至各自最终导引格`(3,3)/(4,3)`；D5沿固定路线三格至`(5,4)`。
- 九点钟声与湿晚饭袋发生；此时只有A完成停驻，不能提交29人完成态。

### R3

- 玩家选反射座，唐胶执行，兜灯否决危险角并允许无损重瞄。
- 安全角使控制膜卷起、路径框`UNANCHORED`；馆守Z只做自主收暗灯瓣与微偏头，不取得首控。
- B10、C3和D5分别抵达`(3,2)/(4,2)/(5,2)`；与A11共同形成`29/29, 4/4`唯一成功回执。
- 若任一Token未到黄线，则只进入失败重试，不写故事状态。

## 3. 自动验证

- `build_v35_8_slot_loadout.py`：生成95槽、609单位/动作/资产行。
- `check_v35_8_slot_loadout.py`：严格语义校验通过。
- `canon-smoke-test.sh`：通过。
- 两张E01 TSV：runtime全21行均9列，graybox全22行均4列。
- `git diff --check`：通过。

## 4. 放行边界

本记录证明补丁已实施，但不自行宣布Episode通过。最终状态必须读取：

- `13-gameplay-final-pass-r3.md`
- `14-canon-final-pass-r3.md`

两席均为PASS后，才可把C01E01改为`accepted_story_audience_production_canon`并生成C01E02继承包。

