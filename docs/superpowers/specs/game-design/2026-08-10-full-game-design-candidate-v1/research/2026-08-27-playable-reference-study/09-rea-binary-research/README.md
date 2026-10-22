# 09 · REA/Ghidra 二进制研究(OGS 主程序)

对《超级机器人大战OGS》(SLPS_257.33,自用光盘镜像)的本地逆向研究基础设施。
研究目标:战斗公式与数值逻辑(配合 公式台 的泛化复刻)。**仅本地研究,不分发任何提取物。**

## 流水线(已打通)

```
超级机器人大战OGS.iso (4.2G, ~/Games/iso/)
  └─ hdiutil attach -readonly → 盘根
       ├─ SLPS_257.33   引导主程序,4.7MB,MIPS32-III 小端 ELF,入口 0x00100008,VER 1.04
       ├─ DATA/BATTLE.BIN   1.5G,"LICE" 魔数容器,熵 6.39(结构+压缩混合)→ 战斗资源/数据
       ├─ DATA/{MAP,GRAPHIC,SQ2,IM,SHARED,WINDOW}.BIN, PSS(视频)/STRM(音频)
       └─ IRX/  PS2 系统驱动
  └─ 证据: evidence/SLPS_257.33 (sha256 前 32 位 205da08f022d008c1b46f315ec84912c)
  └─ Ghidra headless 自动分析:13 秒成功,工程在 ./OGS-project
```

## 已确认事实

1. **函数符号已被剥离**(`file` 的 not-stripped 是误报,.symtab 存在但大小为 0)。
   函数名要靠字符串引用 + 动态对照恢复。
2. **调试字符串幸存**,例:`(a) invalid motion_type(%d)-0`(动作类型校验)、
   `sceGs*`/`libdma` 系统库串、C++ 标准库 wchar_t 流串。说明 release 版保留了
   printf 调试,是定位战斗/动作逻辑的现成锚点。
3. **日文文本不在主 ELF**(抽样为假阳性),在 DATA 包内;BATTLE.BIN 是自定义容器。

## 工具链结论(重要)

- **REA 的 MIPS 通道不收 PS2**:`rea/docs/ghidra-mips.md` 只认证通用 MIPS
  (o32 / 32R2,无机器专属指令);PS2 的 R5900(MMI/LQ/SQ)与 PSP Allegrex 同列为
  "需单独支持的处理器档案"。→ **PS2 走 Ghidra 直连,REA 服务其它目标**(如 itb-lab)。
- **Ghidra 12.1.4 的 release zip 不含 mac_arm_64 反编译器原生库**(只有 linux/win)。
  → 反编译用 **Ghidra 11.4.3**(自带 mac_arm_64 natives,`~/tools/ghidra_11.4.3_PUBLIC`)。
  12.1.4 留给 REA/常规分析;两个版本工程互不兼容,分别建库。
- 剩余难点:EE 自定义指令(LQ/SQ/MMI)在 Ghidra 普通 MIPS 模块下是未定义指令,
  涉及处需社区 R5900 扩展或人工识别;VU1 微码不在本 ELF 内。

## 语言档案根因(2026-10-19,关键修复)

- **Ghidra 自动导入选了 `MIPS:LE:64:64-32R6addr`(R6 档)**:R6 删除了
  branch-likely(BEQL/BNEL/BLEZL/BGTZL/BC1TL/REGIMM),本作 gcc 产物大量使用它们
  → 全二进制约 90% 的代码区被标记为坏数据;`lui` 也被显示成 `_aui`。
- **修复:用 `-processor MIPS:LE:64:default` 重导入**(pre-R6 语义,REL6=0)。
  结果:指令 119,684 → **233,967**,函数 6,673 → **6,890**(+修复管线 +606),
  零未定义。工程:`./OGS-project6432`(114 工程为 R6 旧档,弃用)。
- `MIPS:LE:32:64-32addr`(EE 理想档)在发行版里**没有编译产物 .sla**,不可用。
- 修复管线:坏区逐字 disassemble(0 字=nop 合法)+ 全段裸扫 jal(操作码 0x03)
  目标处 createFunction。脚本在 `scripts/`,输出在 `evidence/decomp|catalogs/`。

## 裸扫描技术要点(踩坑全录)

- MIPS 编码:操作码字段 lui=0x0F/addiu=0x09/daddiu=0x19/ori=0x0D(**注意
  0x3C<<26 会溢出,要写 0x0F<<26**);PS2 ELF 小端,字节序要先翻转;
- Ghidra `getScalar().getUnsignedValue()` 返回**64 位符号扩展值**(0xFFFFFFA0
  = -0x60),lui 的标量**预先左移 16 位**显示(0x530000 实为原始 imm 0x0053);
- `%hi/%lo` 配对:addiu 形式 = hi + signext(lo),编译器会做 hi 进位调整
  (0x53A258 = aui 0x540000 + addiu -0x5DA8);
- Jython 坑汇总:中文路径 PyString 崩(脚本放 ASCII 路径)、文件需 PEP-263
  编码声明、**项目目录里的同名脚本会抢在 scriptPath 之前被解析**、
  `getBytes` 必须用 `jarray.zeros` 预分配缓冲。

## 已恢复的关键情报(2026-10-19)

1. **类目录(17 个,注册函数 FUN_00150080 的调用方)**:
   CFade/CMenu/CMessage/CSetValue/CDrawMap/CWndCommon/CSequence/
   **CMapCamera**/CScreenEffectTest/**CMapBattleDisp**/**CMapBattleUnit**/
   CMoviePlay/CChangeEffect/CSetFlag/CWallPaper/CDispCompass →
   `evidence/catalogs/ogs_classes.txt`。类名注册助手 = FUN_00150080。
2. **vtable**:CMapBattleUnit = `0x0057cda0`(首 2 槽空,实体方法 30+);
   CMapBattle(构造于 FUN_00231854)= `0x0057a740`。
3. **事件命令注册表**(FUN_00157810,注册对象在 ctx+0x6ae0):
   Unit Move=0x3f, Unit OnceMore=0x40, Unit Kill=0x42, …,
   Change Pilot=0x46+, Spirit On Hicchuu(必中)/Hirameki(觉醒),
   以及调试输入菜单(Input Unit HP/EN/Parts, Input Main Pilot Lv/SP/Guts/
   Point/Shootdown)——**Unit/Pilot 字段名直接来自官方调试菜单**。
4. **战斗上下文大结构**(FUN_0036d7a0/00371d70 的 param_1,≥0x3c70 字节):
   +0x6f0/+0x760 攻/守消息窗对象、+0x2ab0 特效对象(虚调用 +0x58)、
   +0x3118 子状态、+0x311c 状态机游标、+0x3128 32 位标志字、
   +0x3bf4/0x3bf8/0x3bfc 插值(上限 0x30)、+0x3c40/0x3c44(上限 0x80/0x20)、
   +0x3970/0x3ac0 三元素步进 100/4 数组。
5. **战斗演出状态机对**:FUN_0036d7a0(攻方,454 行)/ FUN_00371d70(守方,
   344 行)——演出层而非公式层;公式层在 **CMapBattle 地图侧结算族**
   (vtable 方法聚集于 0x34a-0x35c 区,下一轮目标)。
6. **助手函数**:FUN_00150ee0 统计打印、FUN_00114908 断言打印
   (`slice_start_code` 样证函数即经它)、FUN_00150080 类名注册、
   FUN_00157810 事件命令注册。
7. motion_type 调度:FUN_00107988(b 型)/ FUN_001085f0(c 型)/
   FUN_0010acc0(Invalid modion ignored)。
8. 资源线索:`baku2.pig`(FUN_0013be70 区)、`\DATA\BATTLE.BIN;1` 装载锚、
   `m%04d.mpd` 模型四件套(ModelData/ObjectData/EffectData/SequenceData)、
   NGY 系中间件(ngycdvd/ngysnd.irx,Anita 动画内存池)。

## 下一步锚点

- CMapBattle 族 vtable 方法(0x0034a-0x0035c)反编译 → 地图侧伤害公式;
- CDispSpirit::CDrawExecute(00556caf)→ 精神命令效果结算;
- `\DATA\BATTLE.BIN;1` 装载函数(常量对 00532bf0)→ 1.5G 容器解析;
- 动态侧:PCSX2 调试器断点对照(已在 07/08 号研究覆盖设置方法)。

## 反编译样证(2026-10-15,Ghidra 11.4.3 + Jython)

- 全量统计:**6673 个函数 / 119,684 条指令 / 零未定义** —— EE 的 R5900 自定义指令
  在这份编译产物里没有造成任何反汇编障碍(gcc 产物基本走标准 MIPS-III)。
- 405 个字符串引用被分析器解析;直接选中的样证函数 `FUN_0010de78`
  (引用断言串 `slice_start_code(0x%08x) out of range`,属纹理切片系统)
  反编译成功:26 行可读 C 伪代码,含边界校验、断言路由与调用链。
- 部分函数会有 `pcode error / bad instruction data` 警告(EE 特殊指令残留),
  是局部噪声不是全局障碍;遇到时换函数或人工看反汇编。
- 复现:脚本 `ogc_stats.py`(统计)/ ogc_demo3.py(样证)在本目录;
  注意 **Jython 两个坑**:中文路径会炸(脚本放 ASCII 路径)、文件需 PEP-263 编码声明。

## 复现命令

```bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
G14=~/tools/ghidra_11.4.3_PUBLIC/support/analyzeHeadless
DIR="$(pwd)"
# 建库(必须指定 pre-R6 语言!)+ 自动分析
$G "$DIR" OGS-project6432 -import evidence/SLPS_257.33 -processor MIPS:LE:64:default
# 统计
$G "$DIR" OGS-project6432 -process SLPS_257.33 -noanalysis -scriptPath scripts -postScript ogc_stats2.py
# 字符串/常量对/类目录/函数修复管线(输出到 /tmp/ogs_*.txt)
for S in ogs_strings ogs_rawscan ogs_class ogs_mkfunc_all; do
  $G "$DIR" OGS-project6432 -process SLPS_257.33 -noanalysis -scriptPath scripts -postScript $S.py
done
# 指定函数反编译
$G "$DIR" OGS-project6432 -process SLPS_257.33 -noanalysis -scriptPath scripts \
  -postScript ogc_decomp.py 0036d7a0 00371d70
# 动态侧:PCSX2 v2.7.524(/Applications)设置 → 调试器,断点对照静态地址
```
