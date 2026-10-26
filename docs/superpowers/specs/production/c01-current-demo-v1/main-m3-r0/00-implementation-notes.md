# C01E02 M3-R0｜实现说明

> 状态：`Candidate development sandbox / R0 only`
>
> 默认入口：未改变，仍为 `C01CDV1-M2-R2`
> 正式 Runtime / Canon：未授权

## 冻结身份

- `sandbox_contract_id=C01E02M3R0`
- `sandbox_contract_revision=1`
- `build_id=C01CDV1-M3-R0-SANDBOX`
- `rules_profile_id=c01cdv1_e02_shared_round_m3_r0`
- `entry_role=non_default`
- `save_mode=disabled`
- `operation_commit=false`
- `story_checkpoint_write=false`
- `asset_mode=named_geometry_only`

31 号迁移合同 SHA-256 为 `06d17169f8002a09617a8acb2a92886495ad8dbe524cfca237f9079159050860`；32 号 R0 任务书 SHA-256 为 `c7f4cd589d04d4bcc398a02a4e8c113a12d4227ca9cedac9efda7bd64157a350`。开工及最终测试均重新核验。

## 分层

### 数据

`sandbox_profile.json`定义 32×18 棋盘、2×2 馆守 Z、3×3 BREAKER、三只散乱小体、不可控应急车、撤离口、警戒设施、挂墙重盾、城市炮火、路面以及五条 `confirmed` 公开意图。

它还包含四个仅供测试的验收草案；试玩界面不会读取草案模板来替玩家填计划。

### 纯逻辑

`shared_round_resolver.gd`实现：

1. `RoundStartSnapshot`与编辑前冻结的`FrozenIntentSet`；
2. 以数组承载的`UnitPlanDraft[]`；
3. 短路线、独立终点朝向、主动作 XOR 预备反应；
4. 预先声明的 fallback，与预备反应严格分离；
5. 同一前态的时间片和接触组结算；
6. `PreviewSummary`与`execute_round`共用唯一 resolver；
7. 确定性`RoundReceipt`和容器顺序无关的规范哈希。

### 可玩壳

`m3_r0_sandbox.gd`是隔离的 1280×720 Node2D 场景。它提供：

- 公开局势；
- 可按住连续移动的光标和鼠标落点；
- 路线、朝向、动作/预备和备用的独立编辑；
- 可返回修改的摘要；
- 有可见进度的长按提交；
- T1–T5 共同结算；
- 成功或失败的轮回执及一键重置。

R0 只使用程序几何、色块与文字。没有读取 A4/A5、旧头像、旧地图、旧视频或任何真实美术目录。

## 复用与新建

复用的是同一个 Godot 项目、32×18 战术尺度、等距投影概念、2×2/3×3 footprint、道路/建筑/撤离线数据语义与 BFS 通行思路。

新建的是共同回合 resolver、冻结公开意图、草案数组、独立朝向、预备/fallback、共同接触组、RoundReceipt 与 R0 UI。R0 没有加载或实例化旧 `candidate_tactical_session.gd`，也没有经过旧 Runner。

## 文件指纹

| 文件 | SHA-256 |
| --- | --- |
| `sandbox_profile.json` | `f62a8be16d1aec0da3986bdee20d94366190b7ae428c78a1d20ecdc1fc3d4f2e` |
| `shared_round_resolver.gd` | `09de5610d7896abe4c516f98b91e5c7427e5a54d51dd3039e14588e95a6a8386` |
| `m3_r0_sandbox.gd` | `42be3c42fd76d1f6f5d4ac4efe01467229d4aa47da9f6e0d1a56a02fae9c375f` |
| `c01e02_m3_r0_sandbox.tscn` | `820110d8386821967f7bf057e39c54ba656c43681549e2718d7116e2715e6937` |
| `m3_r0_shared_round_contract_test.gd` | `c88c850b152e4ce6d73e4f2a1bcc1cf34aa350932b73c97176c0b5e69b78c779` |
| `m3_r0_playable_flow_test.gd` | `4af886dd3a36c3c1d7adf64d48ecf7b9e78a2c824fc9608d79fa5599cb173c79` |
| `m3_r0_capture_driver.gd` | `411bfa14659335b2fa106fa0bfcd7ebf967fd719cda31aa6ccee7654b950c033` |
| `run_c01e02_m3_r0_sandbox.sh` | `2b765596ea59e61efcd62cb65035c840e06044743bab618121e5af41d81303d8` |
| `test_c01e02_m3_r0.sh` | `ddf7976ad6ff17dbafac04e38c9bebb8259bf11b33414b419334513483ccfe1a` |

## 边界债

Canon 当前实体行、C01 story-chain、已验收 Reader 与本合同一致，均规定馆守 Z 在 E02 首次正式战斗；但旧 `canonical_terms.tsv` 的 `TERM_GUANSHOU_Z`定义仍残留“E02身体零动作、E03首控”。本任务禁止修改 Canon，因此只登记，不在 R0 内修复。该残留没有进入 resolver、场景或测试。
