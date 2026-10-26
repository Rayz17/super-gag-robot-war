# 公式台试玩签收引导（一页纸 · 2026-09-16）

> 用途：手感门（feel-signoff.md）签收前的亲手试玩指引。规格门对照表见文末。
> 全程约 30–40 分钟（每公式 3–6 分钟，可分多次）。

## 启动任一公式

```sh
cd /Users/rayz/Documents/超gag机器人大战
python3 scripts/formula_production_lab.py produce --reader <输入包 reader> --reading <reading.json> --assets <assets.json> --candidate-lab --out <新目录>
# 或直接启动已生成的包（十选一，见下）：
/Applications/Godot.app/Contents/MacOS/Godot --path game-godot res://scenes/formula_lab/formula_lab_package.tscn -- --package "<包目录>/flow.json"
```

当前包清单：`artifacts/formulas/production-lab-v1/builds/current-packages.json`（A–J 十包）。

## 通用键位（全实验室一致）

J/Enter/空格=推进·确认（提交类需按满 3 次或长按）　K=跳过场面（结果不变）　
←→↑↓=选目标/画路线　Esc=收起当前层（不产生假结果）　Z=记录　F=百科

## 每公式的试玩路径与验收点

| 公式 | 建议包 | 玩什么 | 手感验收点 |
| --- | --- | --- | --- |
| 调查 | A（手册版） | 现场观察→手册填槽→配置→低载试验→结果对白 | 试验结算是否与你的配置/操作因果一致；手册三栏是否一眼可读 |
| 战术 | E 擂台 / F 穿越 | 看敌方公开意图→编排→按满 3 次提交→执行→判定 | 意图是否一眼可读；失败/代价是否真实；场地变化是否可感 |
| 探索 | C 或 D | 走近观察→记录→线索合成→路线报告 | 知识是否真的改变可选路线；「能证明/不能证明」是否清楚 |
| 世界图 | G 或 H | 地图选点→派遣确认→到场探索→报告 | 未选路线的后果展示是否清楚；派遣确认是否郑重 |
| Hub | I | 走近人与物→工作卡草案→提交→同室后果 | 草案/提交分离是否清楚；后果对白是否读你的真实安排 |

## 签收

试玩后在 `artifacts/formulas/<FORMULA_ID>/` 放入：
- `feel-signoff.md`（按 `feel-signoff.template.md` 填写——判据：不看文档能玩完、因果对得上、没有"按了没反应"）
- `spec-signoff.md`（按 `spec-signoff.template.md` 填写——判据：每类素材的张数/规格/命名可排期）

放入后运行 `scripts/formula-desk freeze --formula <ID>`，测例/换档/手感/规格四门全过即冻结放行。
（当前：测例门 7/7 ✅、换档门 7/7 ✅、冻结门对全部公式正确拒绝中——差的就是这两个签名。）
