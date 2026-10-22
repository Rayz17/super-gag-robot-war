# C01E01 r3语义传播补丁关闭记录

> Status: `patched_pending_independent_targeted_r4`
>
> Scope: 关闭`13-gameplay-final-pass-r3.md`与`14-canon-final-pass-r3.md`的全部定向项；不新增剧情，不把本记录当作独立PASS。

## 1. 游戏制作席四项补丁

| ID | 修复 | 唯一口径 | 证据 |
|---|---|---|---|
| `GPR3-01` | S01失败合同 | R3结束仍未集结4枚Token即`MISSION_FAIL_TIMEOUT`，回到`BATTLE_SETUP`，零持久状态；四令只在成功后的消防路由与声纹捕获后发生 | 生成器`SLOT_FAILURE_PRESSURE_OVERRIDES`；生成表`V358GAME001` |
| `GPR3-02` | 机器犬挂接行动经济 | R1挂接D5后，R2-R3与D5共享撤离自动路径，不再拥有独立移动/情境动作，直到D5完成集结 | `RT004`；`GB009` |
| `GPR3-03` | 反射座解析 | `(4,8)`是唯一安全位；`(3,8)/(5,8)`由兜灯否决并无损返回`AIM_PREVIEW` | `GB022`；`RT009/RT011B` |
| `GPR3-04` | 原子物理快照 | `RT011`只作局部战斗Clear，不写Episode handoff；`RT013S`是唯一持久提交，键为`C01_PHYSICAL_SNAPSHOT=COMMITTED`，并包含东侧烟入与喷淋干管无压 | `RT011/RT013S`；正文结算 |

## 2. Canon席七项传播补丁

| ID | 修复 | 唯一口径 | 证据 |
|---|---|---|---|
| `CPR3-01` | 活跃场景链 | 新增Story-First救援、七海公务台与四令接管链；旧合并版六回合链标记`historical_runtime_reference`，旧V31右臂桥标记`historical_story_source` | `data/canon/scenes.tsv` |
| `CPR3-02` | 人命与载荷 | E01固定人命优先；E04仅在全员离楼后选择生活维持设备、实体独有馆藏、档案服务器三类载荷二保一 | `entities.tsv`；`scenes.tsv`；V35.5/V35.7/V35.8上游 |
| `CPR3-03` | 右臂生命周期 | E01-E02馆守Z右臂核心保持连接；E02切割标尺机只切消防/路线设备与检修外甲；E03才飞拳、主动切筋、成桥 | `entities.tsv`；`scenes.tsv`；`V355A03` |
| `CPR3-04` | 深层空间拆分 | B1只作机库远景；远星副柜位于L1旧影像区并只读L3离线缓存；B2零号门只由远端监视窗可见 | `V355A18A/A18B/A18C`；V35.5母板 |
| `CPR3-05` | S01胜败 | 唯一失败为R3结束仍有Token未越黄线；小机回充是post-clear；危险胸灯角只重瞄；展件不进入人命同层Game Over | PB S01；V35.5母板；Runtime/Graybox |
| `CPR3-06` | S02机器犬 | 读取29人已在前厅，改为侦察出口烟流、牵引C3照看组与稳定消防软管，不重复救维修员 | 生成器动作/签名覆盖；`V358U002-05`与`V358ACT002-05` |
| `CPR3-07` | 灯光语义 | 展陈灯由闭馆程序熄灭；城市电网和维生在线；四令另行切断馆守Z胸灯并锁门、冻钥匙、停泵 | V35.7 S01 next logic；V35.5母板；`RT013S` |

## 3. 保持不变的升级边界

- 白函仍是E02远程非实体归责，E03完整身体首战。
- 索引在C11前仍没有连续第一人称。
- E01只把29人送到L1前厅黄线，真正离开建筑属于E02。
- 七海在零号前只使用私人语音，零号后才接入只读公务风险频道；第一条改变系统状态的命令留E02。
- 馆守Z的微偏头与灯瓣收暗仍属自主场景动作，不计玩家首控。

## 4. 自动与定向验证

- `python3 -m py_compile scripts/build_v35_8_slot_loadout.py`：PASS。
- `python3 scripts/build_v35_8_slot_loadout.py`：生成95槽、609单位/动作/资产行。
- `python3 scripts/check_v35_8_slot_loadout.py --max-errors 80`：PASS。
- `scripts/canon-smoke-test.sh`：PASS。
- 涉及的Canon、V35.5/V35.7/V35.8、Runtime、Graybox与图谱TSV：列数全一致。
- 活跃`scenes.tsv`定向筛查：无`C01_COLLECTION_PRIORITY`、人/展品/服务器伪选择、六回合旧战或E02右臂桥。
- V35.5定向筛查：无`real_mecha_fragment`、真机残肢、远星柜绑定B1、关键展件坠落或胸灯误烧Game Over。
- V35.8定向筛查：`V358GAME001`为零提交重试；`V358U002-05/V358ACT002-05`不再重复维修员；S02/S03白函阶段未回退。

## 5. 独立放行条件

原游戏制作/关卡合同席与原Canon/宏观/物理席必须分别以本轮实际文件为证，给出`PASS`或新的精确`PATCH`。只有两席均PASS，才允许：

1. 将C01E01状态改为`accepted_story_audience_production_canon`；
2. 将Canon migration状态改为`applied_and_validated`；
3. 生成C01E02继承包并开始第二话Story Core。
