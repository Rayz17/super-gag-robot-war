---
record_type: runtime_context_pack
authority: current_canon_projection
status: generated
chapter: C02
tags:
  - story-runtime/context-pack
  - story-runtime/current-canon
---

# C02 Current Canon 检索包

- 请求：`docs/superpowers/specs/story-runtime/context-packs/C02-runtime-pilot/00-实验协议与上下文需求.md`
- 只含 Hard / Working、active Current Canon 的检索投影。
- C02 场景节点与指向这些节点的关系禁读；实体事实允许使用，但不能把实体说明里的旧动作当成新稿场面。
- 盲测过滤节点：**12**
- 为避免章节时序答案泄漏，已隐藏字段：`first_battle_join, first_foreshadow, first_formal_appearance`

## C01 旧守护者

- 节点：`entity:CH002`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`548.5210`

- **aliases**：Old Guardian;导览人格;馆守Z导览人格
- **canonical_name**：旧守护者
- **entity_id**：CH002
- **implementation_policy**：第一章先以轮式导览终端和馆内广播陪伴观众；终端被压后，同一句话从馆守Z胸前扬声器继续说完。人格根始终固定在馆守Z胸腔保护舱内，E02在兜灯解除物理限位、七海撤回本人停机令后取得巨体运动权。
- **notes**：旧守护者与馆守Z是同一主体的日常称呼和正式机体名；导览终端、广播与胸前扬声器只是远程感官和输出端，不是独立AI或可复制机魂。纪存进入导览席只提供路线与判断，不控制四肢。
- **role**：馆守Z机魂人格;展厅导览人格
- **source_group_id**：R01
- **status**：core
- **type**：character
- **显式关系**：
  - 来源组 -> `wanji_coverage:R01` 铁馆魔神

## C02 馆守Z

- 节点：`entity:V353U001`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`explicit_seed, bm25`
- 分数：`502.3885`

- **aliases**：铁馆魔神;18米旧巨神;馆守巨神
- **canonical_name**：馆守Z
- **entity_id**：V353U001
- **implementation_policy**：与MECHA_GUARDIAN_Z为同一机体的V35生命周期ID；旧守护者是其机魂人格。C01E02完成首次正式战斗，E03以过载火箭右拳和勇拳接力击穿BREAKER地面甲壳，右臂回收机构烧毁、主要残片留在旧址；E04装上非拳击型巡展臂装并以左拳击毁飞行核心。后续必须通过独立剧情获得真正后继右臂，不能无损找回旧臂。
- **notes**：内部锚Mazinger式火箭拳、旧超级系后继强化与博物馆守护者；后继弧读取CONCEPT_GZ_SUCCESSOR_ARM_ARC。
- **role**：18米开局旧巨神主力；C01失去原右拳与完整前臂，此后经历巡展臂装、代用结构和后继右臂成长
- **source_group_id**：PK_CORE_IRON_GUARD
- **status**：working_current
- **type**：mecha

## C03 白鸢

- 节点：`entity:N_BAIYUAN`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`489.7199`

- **aliases**：Evelyn Voss;White Kite;创作者遗民;改写者;分镜本;艾芙琳·沃斯;Aveline Voss
- **canonical_name**：白鸢
- **entity_id**：N_BAIYUAN
- **implementation_policy**：英国公民Evelyn Voss，来自英德创作者家庭；White Kite为英文署名，中文发行与玩家界面保持意译笔名白鸢，Baiyuan不再作为原生国际名。C02E01先以被盗用的作品留下痕迹，C02E03肉身到场并临时随舰，C03完成第一份多人可改的共同作品。她把旧分镜、现场传感、地形与机体数据整理成可讨论的预演草图，真实动作仍由驾驶员、机体与工程链执行；当前没有战斗指令权、未来视、造物或画稿改现实能力。
- **notes**：她是会画成人向擦边同人的成年欧美创作者，日常色气、嘴硬和跨语言创作趣味与正剧控制欲形成反差。与纪存、七海的吸引、误解和独立亲近均需通过具体共同经历推进；后续战术席位、不可逆选择与能力升级只从候选覆盖层读取。
- **role**：作者遗迹、战术预演与纪存/七海关系线核心角色
- **source_group_id**：CREATOR_LINE
- **status**：core
- **type**：character

## C04 万机馆巡展舰体

- 节点：`entity:MECHA_WANJI_MOBILE_CHASSIS`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`explicit_seed, bm25`
- 分数：`466.3608`

- **aliases**：万机馆展舰;旧巡展舰;WBM001
- **canonical_name**：万机馆巡展舰体
- **entity_id**：MECHA_WANJI_MOBILE_CHASSIS
- **implementation_policy**：生产态只保留固定展馆、离地转换和巡展舰三态；E01旧照片预告巡展形态，E03地下轮廓回应，E04恢复舰体并进入空战。首战可调用真实巡展史中的退役重盾、救援锚、推进骨架和有限防卫炮，但不是完整战舰火力、无限格纳库或人形机器人。
- **notes**：与WBM001、LOC_WANJI_MOBILE_CHASSIS和泊位规则共同定义后续主循环；旧引擎只足以可靠抵达邻近一站，且缺现代泊位接口。馆藏不会逐件变形成舰体零件。
- **role**：C01E04恢复的百米级移动基地与母舰身体
- **source_group_id**：LOC_WANJI_MOBILE_CHASSIS
- **status**：working_current
- **type**：mecha
- **显式关系**：
  - 来源组 -> `entity:LOC_WANJI_MOBILE_CHASSIS` 巡展舰体与外泊层

## C05 万机馆主循环磁流散热转子

- 节点：`entity:MECHA_WANJI_MAIN_CIRCULATION_ROTOR`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`455.0631`

- **aliases**：主循环转子;巨型转子;展舰散热转子
- **canonical_name**：万机馆主循环磁流散热转子
- **entity_id**：MECHA_WANJI_MAIN_CIRCULATION_ROTOR
- **implementation_policy**：它是场景巨构和任务载荷，不是人格机体、不计参战；模型批次与维修史只能帮助辨认版本和适配方法，真正安装仍需全尺寸实物与工程复核。安装只恢复有限航行，不解决永久外泊、校正和保险。
- **notes**：正式资产应突出巨大转子、运输架、吊装和万机馆检修窗，不制作密集内部机构动画；精确尺寸、重量和安装动作由C02预生产确定。
- **role**：C02使万机馆恢复有限航行的全尺寸工业总成，必须由重型运输和吊装设备搬运，不能退化成手掌大的密封件
- **source_group_id**：MUSEUM
- **status**：needs_review
- **type**：scene_mecha

## C06 钢拳擂台

- 节点：`entity:R22`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`397.1768`

- **aliases**：旧拳王;拳击机器人;非致命擂台
- **canonical_name**：钢拳擂台
- **entity_id**：R22
- **implementation_policy**：C02以完整旧拳王机体和机械擂台建立非致命战斗；右拳护具只能作为模型锚、规则钥匙或改装件，不能冒充参战机体。旧拳王通关后正式加入，完整支线留待后续生命周期展开。
- **notes**：用于把机器人拳击、失败记录和父子式修复情感带入可长期使用的机体，而不是只给一只手套参战。
- **role**：非致命战、失败与修复尊严谱系
- **source_group_id**：R22
- **status**：core
- **type**：roster_package

## C07 纪存

- 节点：`entity:CH_JICUN`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`361.1161`

- **aliases**：Ji Cun;Jicun
- **canonical_name**：纪存
- **entity_id**：CH_JICUN
- **implementation_policy**：主角视角优先承担玩家认知，不替设定朗读百科；他在C01主动组织闭馆、救人、保护机体并决定让万机馆离地。作为逐渐苏醒的机魂实体，他必须主动判断、调查、犯险和解决谜团；过往记忆通过行动与代价苏醒，不以存档、贴标签、行政词汇或被动受难代替成长。具体首战结构由C01 L4决定。
- **notes**：纪存没有生物人类血统，但由中国馆长纪文山和万机馆本地社会语料引导形成中文母语化人格、中国文化认同与中国青年男性外观；他不是纪文山的克隆或年轻复制品。纪姓与名字以后可以被他重新确认。对馆体、馆藏机魂和灾前导览系统的深层联系仍按剧情揭示。
- **role**：临时闭馆负责人;机魂实体主角;记忆苏醒者
- **source_group_id**：PROTAGONIST
- **status**：core
- **type**：character

## C08 机魂本地涌现反馈环

- 节点：`entity:CONCEPT_MACHINE_SOUL_EMERGENCE_LOOP`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35世界机制与创作接口设定基线-2026-07-19.md`
- 命中：`explicit_seed, bm25`
- 分数：`348.2904`

- **aliases**：机魂形成环;本地成魂;具身关系闭环;local soul emergence
- **canonical_name**：机魂本地涌现反馈环
- **entity_id**：CONCEPT_MACHINE_SOUL_EMERGENCE_LOOP
- **implementation_policy**：形成发生在具体机体AI核、整副身体、实时黑匣或有明确根节点的本地系统；承认、命名、玩梗、维修和观看可促进时间连续与社会边界，却不是造魂咒语。相同型号、相同动作包可以形成不同主体；复杂AI和热门机体也可能永远没有机魂。
- **notes**：现阶段C05百相副驾驶是最清楚的当代样例；C01跌跌、C02四台重涂机和C03城梁一号从不同尺度提供辅助证据。
- **role**：本地AI/控制核持续运行，具身感知与动作史形成个体差异，个人记忆不被全部清空，人机关系持续把它当作同一对象回应，G.A.G.文化反馈再进入本地系统，最终使其能区分外部期待与自身选择
- **source_group_id**：WORLD_ROOT
- **status**：working_current
- **type**：concept

## C09 七海

- 节点：`entity:CH_QIHAI`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`334.1024`

- **aliases**：佐伯七海;佐伯 七海;さえき ななみ;Nanami Saeki;Qihai
- **canonical_name**：七海
- **entity_id**：CH_QIHAI
- **implementation_policy**：日本公民，成长于神奈川县横滨港区，成年后派驻代哥中国东部沿海分部与本市封存中心。中文界面与同伴称七海，正式文件使用佐伯七海，国际文件使用Nanami Saeki；Qihai只作旧工程转写。C01可先以无公务UI的私人语音建立她与纪存的既有私交；闭馆接管正式启动后，她才以公务风险频道介入现场。第一章始终远程出场，只能撤销本人签发的命令并为自己的判断承担停权，不能替军方、平台或城市授权；具体切电、撤令和UI顺序由C01 L4裁决。C03经公共交通实体到场并限段入住。
- **notes**：她不是代哥黑点的拟人化，而是知道品牌资产生态腐化、仍试图把流程拉回初心的成熟改革者。她的日本企业/公共安全经验和中国派驻生活都要进入日常与选择；后续具体伤势、旧项目责任、权限迁移和关系选择必须从候选覆盖层另查。
- **role**：代哥安全封存局档案官;内部改革派
- **source_group_id**：ORG_DAIGE
- **status**：core
- **type**：character
- **显式关系**：
  - 来源组 -> `entity:ORG_DAIGE` 代哥品牌资产秩序生态

## C10 玩家模型机“无牌一号”

- 节点：`entity:V353U071`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`327.5752`

- **aliases**：无牌一号;全尺寸改件竞技实机
- **canonical_name**：玩家模型机“无牌一号”
- **entity_id**：V353U071
- **implementation_policy**：木桶街原有全尺寸模块竞赛底盘和低权限竞赛AI；缩尺模型只提供改件同构数据，不会放大成机体。它在C02首控，V359-C03E04-CREATIVE经正常运输取得随舰构筑席；首个作业模块由C03 L4确定。
- **notes**：内部锚Gundam Build与模型竞技；名称可由玩家改，不共享社勇王许可。
- **role**：自由改装、零件兼容和玩家构筑单位
- **source_group_id**：PK_GUEST_BUILD_ARENA
- **status**：needs_review
- **type**：mecha

## C11 影子陪练机

- 节点：`entity:V353U049`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`312.6880`

- **aliases**：旧拳王陪练;影子模式机
- **canonical_name**：影子陪练机
- **entity_id**：V353U049
- **implementation_policy**：与MECHA_SHADOW_SPARRING_MACHINE为同一机体的V35生命周期ID；C02参加擂台，录像与原主体同意决定后续可用性，是否随舰由C02 L4裁决。
- **notes**：内部锚机器人拳击影子模式。
- **role**：动作复制、反击教学和非致命训练路线机
- **source_group_id**：PK_GUEST_IRON_FIST
- **status**：needs_review
- **type**：mecha

## C12 火种货柜领袖

- 节点：`entity:V353U043`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`307.3576`

- **aliases**：货柜领袖;变形货柜生命
- **canonical_name**：火种货柜领袖
- **entity_id**：V353U043
- **implementation_policy**：以已有全尺寸载具身体和独立载具人格参加C02，并完成护送万机馆到工务城的一站承诺；C03E04离舰，承担百机航路邀请的地面转递，后续可沿航路召回。它可以进入作业变形形态，但不等于星火车队、火种源或G.A.G.本体。
- **notes**：内部锚Transformers领袖与车队文化；C04不占舰位，C06不得由它包办星火车队谱系。
- **role**：作业变形、护送和领袖支援主力
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C13 商品回收王牌“归一星”

- 节点：`entity:ENEMY_C02_UNITY_RECLAIMER`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`304.5992`

- **aliases**：归一星;人格回收王牌;SKU追猎机
- **canonical_name**：商品回收王牌“归一星”
- **entity_id**：ENEMY_C02_UNITY_RECLAIMER
- **implementation_policy**：它能调用商品回收设施和复制已取得的工厂动作样本，但不能复制四机后来形成的主体判断。具体武装、场地控制和破局方式由C02 L4决定。
- **notes**：归一星属于商品回收实体执行链，不是胶价王投影或索引人格；内部锚商品回收、量产王牌和统一模板，外观不复刻具体喷气角色。
- **role**：C02重涂人格空战具名敌机，读取四台重涂机的工厂动作库并试图把它们压回同一商品身份
- **source_group_id**：DAIGE_PRODUCT
- **status**：needs_review
- **type**：enemy_unit

## C14 白框具身生产链

- 节点：`entity:CONCEPT_WHITEFRAME_EMBODIMENT_CHAIN`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35世界机制与创作接口设定基线-2026-07-19.md`
- 命中：`explicit_seed, bm25`
- 分数：`294.7165`

- **aliases**：白框生态;标准身体;采样回收制造链
- **canonical_name**：白框具身生产链
- **entity_id**：CONCEPT_WHITEFRAME_EMBODIMENT_CHAIN
- **implementation_policy**：白框没有单一幕后主谋，也不是索引分身；索引可逐步借合作、数据和漏洞调用它。每次物理行动必须说明具体机构、设备、身体和中止链。
- **notes**：白函、归一星、衡令、百相等均是各自操作者/协议的实体，不自动等于索引人格。
- **role**：企业、城市、军方与平台共同使用的采样、兼容、回收和标准身体生产生态，为安全答案和无身意识提供物理执行体
- **source_group_id**：WHITEFRAME
- **status**：working_current
- **type**：concept

## C15 兜灯

- 节点：`entity:CH001`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`260.9444`

- **aliases**：窦晓宁;Dou Xiaoning;Doudeng
- **canonical_name**：兜灯
- **entity_id**：CH001
- **implementation_policy**：可在第一章作为维修与安全操作单位出现；她负责判断馆守Z何时能够行动、何时必须制动，并能在现场真正执行，不由纪存或系统代替。具体战斗动作和回合数由C01 L4决定。
- **notes**：中国公民，本名窦晓宁；兜灯是窦姓与童年头灯习惯形成的维修组昵称。铁馆魔神线入口，和馆守Z的长期关系优先于一次战斗爽点；旧C01E02-BATTLE-START仅为历史实现时序。
- **role**：馆守Z整备员
- **source_group_id**：R01
- **status**：core
- **type**：character
- **显式关系**：
  - 来源组 -> `wanji_coverage:R01` 铁馆魔神

## C16 全装冠军“百刃”

- 节点：`entity:ENEMY_C02_FULL_ARMOR_CHAMPION_BAIREN`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`257.6571`

- **aliases**：百刃;全装擂王;过度配件冠军
- **canonical_name**：全装冠军“百刃”
- **entity_id**：ENEMY_C02_FULL_ARMOR_CHAMPION_BAIREN
- **implementation_policy**：必须是完整拳斗或竞技实机；过量配件既带来正面战力，也形成一眼可懂的体积、转向和场地限制，不得只当笑话靶。具体拳赛阶段和破局动作由C02 L4决定。
- **notes**：与旧拳王形成朴素机体对全装商品奇观；正式造型需避开现实产品的一比一拼贴。
- **role**：C02非致命擂台对手机，以过量尖刺、背包和武器包承载模玩过度设计与全装崇拜
- **source_group_id**：MODEL_STREET
- **status**：needs_review
- **type**：enemy_unit

## C17 喷气叛星

- 节点：`entity:V353U044`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`248.7195`

- **aliases**：叛星;重涂喷气首领
- **canonical_name**：喷气叛星
- **entity_id**：V353U044
- **implementation_policy**：C02完成首次战斗并确认独立主体身份；它承认自己也是重涂角色，不以原版血统洗白。后续加入和回收节点由L3生命周期表决定。
- **notes**：内部锚Starscream式叛星；必须有独立头雕、翼型、武器和性格。
- **role**：高速空战、诱饵分身和品牌背叛路线机
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C18 重涂机“死锁”

- 节点：`entity:V353U045`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`233.1868`

- **aliases**：死锁;旧人格近战重涂
- **canonical_name**：重涂机“死锁”
- **entity_id**：V353U045
- **implementation_policy**：C02完成首次战斗并确认独立主体身份；它拒绝被改写成更好卖的英雄版本。后续加入和回收节点由L3生命周期表决定。
- **notes**：内部锚热门重涂与漂移/死锁式身份记忆；正式公开前做避撞审查。
- **role**：近战突入与旧人格冲突路线机
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C19 重涂机“镜星”

- 节点：`entity:V353U046`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`225.4894`

- **aliases**：镜星;镜像重涂
- **canonical_name**：重涂机“镜星”
- **entity_id**：V353U046
- **implementation_policy**：C02完成首次战斗并确认独立主体身份；镜像涂装必须服务它自己的立场与行动，不只作皮肤。后续加入和回收节点由L3生命周期表决定。
- **notes**：内部锚镜像世界重涂。
- **role**：电子干扰和敌我标识翻转路线机
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C20 旧拳王机

- 节点：`entity:V353U048`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`220.3459`

- **aliases**：钢拳旧王;退役拳击机器人
- **canonical_name**：旧拳王机
- **entity_id**：V353U048
- **implementation_policy**：与MECHA_OLD_BOXER_KING为同一机体的V35生命周期ID；C02作为完整可驾驶机体赢得擂台并正式加入，右拳护具永不计作独立机体。
- **notes**：内部锚Real Steel式机器人拳击；具体影子模式错位和决胜拳由C02 L4决定。
- **role**：拳击、受击蓄势和非致命击倒主力
- **source_group_id**：PK_GUEST_IRON_FIST
- **status**：needs_review
- **type**：mecha

## C21 重涂机“雷翎”

- 节点：`entity:V353U047`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`211.0454`

- **aliases**：雷翎;喷气远射重涂
- **canonical_name**：重涂机“雷翎”
- **entity_id**：V353U047
- **implementation_policy**：C02完成首次战斗并确认独立主体身份；具体收尾动作和轮换冲突由C02 L4决定。后续加入和回收节点由L3生命周期表决定。
- **notes**：内部锚喷气重涂军团。
- **role**：远射、侦察和机动换位路线机
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C22 唐胶

- 节点：`entity:CH_TANGJIAO`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`169.5715`

- **aliases**：唐启明;Tang Qiming;Tangjiao;N_TANGJIAO
- **canonical_name**：唐胶
- **entity_id**：CH_TANGJIAO
- **implementation_policy**：第一章可作为维修、路障和手作价值观角色；Story-First首次战术行动为E01把安全罩改成导光挡板；台词必须来自工艺细节，不说主题金句。
- **notes**：中国公民，本名唐启明；唐胶是模型街工房外号。正式合同和家庭危机场可用本名，日常与玩家界面保持唐胶；旧C01E02-BATTLE-START仅为历史实现时序。
- **role**：模型修复师;嘴毒手作派
- **source_group_id**：MUSEUM
- **status**：core
- **type**：character

## C23 万机馆藏品-机体关联规则

- 节点：`entity:CONCEPT_WANJI_COLLECTION_LINKAGE`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`165.3988`

- **aliases**：藏品谱系;模型关系钥匙;展品锚点;collection taxonomy
- **canonical_name**：万机馆藏品-机体关联规则
- **entity_id**：CONCEPT_WANJI_COLLECTION_LINKAGE
- **implementation_policy**：新增参战机体或展品必须说明馆内锚点、关系类型、激活条件和随舰状态；模型/玩具可作为关系钥匙和结构证物，不直接无代价变真机。
- **notes**：对应wanji_collection_taxonomy.tsv和DOC_WANJI_COLLECTION_CARRIER_DESIGN。
- **role**：定义展品、藏品、模型、黑匣子和参战机体的连接方式
- **source_group_id**：MUSEUM
- **status**：core
- **type**：concept

## C24 裂星潮突入体BREAKER

- 节点：`entity:ENEMY_C01_BREAKER`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`bm25`
- 分数：`523.0012`

- **aliases**：BREAKER;破城者;裂星潮突入体
- **canonical_name**：裂星潮突入体BREAKER
- **entity_id**：ENEMY_C01_BREAKER
- **implementation_policy**：地面阶段为近30米黑甲突入壳，能钻地、冲撞与发射赤红冲击；外壳被双拳击穿后露出十余米核心与近50米薄翼，能高速飞行并以脉冲指挥小型突入体。两阶段共用同一主体，不是两只敌人。它会忽略更近的火力与能源站转向万机馆，但本章不解释原因。
- **notes**：正式编号与裂星潮序列待外敌命名协议后补；BREAKER是城市作战呼号。外观先保证地面重甲与飞行核心一眼可辨。
- **role**：C01突破近海防线并追逐万机馆的两阶段外敌
- **source_group_id**：EXTERNAL_RIFT_SWARM
- **status**：working_current
- **type**：enemy_unit

## C25 无标志白色采样机

- 节点：`entity:ENEMY_C01_UNMARKED_WHITE_SAMPLER`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`bm25`
- 分数：`475.6927`

- **aliases**：白色采样机;无标采样机;右拳残片采样机
- **canonical_name**：无标志白色采样机
- **entity_id**：ENEMY_C01_UNMARKED_WHITE_SAMPLER
- **implementation_policy**：只在战后废墟短暂出现，以腹部收纳舱取走一块右拳残片后离开；不与主角交战、不说话、不揭示所属机构。它证明有人在系统性回收机体身体与战斗样本，但不等于索引人格或代哥命令。
- **notes**：C02以后若追踪该样本，必须说明具体机构、物流和分析身体；C01只保留无名钩子。
- **role**：C01尾声回收馆守Z右拳残片的白框生态前台身体
- **source_group_id**：WHITEFRAME
- **status**：working_current
- **type**：enemy_unit

## C26 馆守Z

- 节点：`art_lock:CML008`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv`
- 命中：`bm25`
- 分数：`397.3933`

- **age_band**：18m级
- **asset_status**：locked_current
- **canon_entity_id**：V353U001
- **canonical_name**：馆守Z
- **current_art_reference**：.superpowers/brainstorm/37837-1782033239/content/guardian-z-user-selected-base.png
- **gender_presentation**：非人机体
- **lock_id**：CML008
- **must_not**：E01不得提前站起;原右拳不得无损回收;巡展臂装不得画成完整拳击手臂;后继右臂必须另建形态锁
- **notes**：美术和地图始终按18m机体处理；巡展臂装只含救援锚、抓握框和固定结构。真正后继右臂按CONCEPT_GZ_SUCCESSOR_ARM_ARC另建。
- **package_id**：R01
- **personality_anchor**：博物馆守护机;老派超级系重量
- **pronouns_or_address**：馆守Z;旧守护者本体
- **role_type**：开局主机体;万机馆守护机
- **source_refs**：docs/superpowers/specs/data/canon/entities.tsv;docs/superpowers/specs/data/canon/wanji_roster_zone_coverage.tsv;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md
- **story_gate**：V355-C01E01_PREVIEW/V355-C01E02_FIRST_CONTROL/V355-C01E03_RIGHT_ARM_LOSS/V355-C01E04_TOURING_ARM
- **subject_id**：V353U001
- **subject_type**：mecha
- **unit_or_mecha_link**：兜灯;旧守护者
- **visual_lock**：18m;E01半跪展台态;E02双臂重盾态;E03火箭拳后缺臂态;E04巡展臂装态
- **voice_rule**：机体通过旧守护者广播、视线和大动作表达;不说花哨人话
- **wound_or_drive**：退役封存;原右臂在C01过载毁损
- **显式关系**：
  - 美术主体 -> `entity:V353U001` 馆守Z
  - Canon 主体 -> `entity:V353U001` 馆守Z
  - 参战包 -> `wanji_coverage:R01` 铁馆魔神

## C27 馆守Z巡展臂装

- 节点：`entity:MECHA_GUARDIAN_TOURING_ARM`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`bm25`
- 分数：`380.5562`

- **aliases**：巡展臂装;救援锚臂;临时右臂
- **canonical_name**：馆守Z巡展臂装
- **entity_id**：MECHA_GUARDIAN_TOURING_ARM
- **implementation_policy**：接在馆守Z右肩残存固定口，只能抓握、放锚、牵引、固定和投放装备；不能握拳、精密操作、发射火箭拳或表现成完整新右臂。E04钉住BREAKER侧翼并帮助馆守Z回舰。
- **notes**：后续可在木桶街换装不同工作手，但真正后继右臂必须另建机体形态和剧情。
- **role**：C01E04由万机馆旧救援锚改成的临时右侧装备
- **source_group_id**：V353U001
- **status**：working_current
- **type**：mecha_component
- **显式关系**：
  - 来源组 -> `entity:V353U001` 馆守Z

## C28 G.A.G.文化行动涌现网络

- 节点：`entity:CONCEPT_GAG_CULTURAL_ACTIVATION`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35世界机制与创作接口设定基线-2026-07-19.md`
- 命中：`bm25`
- 分数：`347.7925`

- **aliases**：Great Archive Grid;G.A.G.根规则;梗与记忆活化;文化行动语法;GAG涌现现象
- **canonical_name**：G.A.G.文化行动涌现网络
- **entity_id**：CONCEPT_GAG_CULTURAL_ACTIVATION
- **implementation_policy**：G.A.G.没有中央主机、独立母域、统一人格、法律权或万能能源；全球联网机器人生态是物理载体，Great Archive Grid是人类后来建立的观测、编译、路由、监测与断路协议。它能检索、放大、连接、活化、催化、误译和投射，但不能从公共灵魂池分发机魂、自行封存清噪改写或凭空制造身体。
- **notes**：二十七年前统一回应借制度化接口救下地球；灾前人类已因机器偶发个性主动放大该现象。根边界以V35世界机制基线和gag_capability_boundaries.tsv为准。
- **role**：全球机器人训练、生产、维修、城市/军用接口、实机AI、模型玩具、作品与玩家活动联网后，文化行动语法持续串流、误接并反馈到真实机器的分布式涌现现象
- **source_group_id**：GAG
- **status**：working_current
- **type**：concept

## C29 社勇王

- 节点：`entity:V353U024`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`bm25`
- 分数：`346.7324`

- **aliases**：全尺寸社勇王;勇者救援实机
- **canonical_name**：社勇王
- **entity_id**：V353U024
- **implementation_policy**：全尺寸实机；模型盒和说明书只作锚件。C03由豪司与机体主体AI完成首次正式并肩，AI在战局变化后第一次拒绝驾驶员，双方重新协调并赢下战斗；E04由机体、工务城与企业确认三个月公共道路试用，企业保留产权、维护义务与到期复核。玩家可长期操作不等于万机馆永久所有。
- **notes**：当前说话者为社勇王机体主体AI，不提前启用CH037金章独立人格；内部锚Brave/GaoGaiGar式AI伙伴与工具浪漫。
- **role**：C03以后勇者救援主力，承担完整合体、巨大工具、主体选择和AI拒绝
- **source_group_id**：PK_CORE_BRAVE_CO
- **status**：needs_review
- **type**：mecha

## C30 维修角

- 节点：`entity:LOC_WANJI_REPAIR_BAY`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`bm25`
- 分数：`345.6560`

- **aliases**：右臂维修区;维修天桥;兜灯工位
- **canonical_name**：维修角
- **entity_id**：LOC_WANJI_REPAIR_BAY
- **implementation_policy**：作为C01闭馆路线与小机行动的维修锚点；对白必须服务馆守Z旧伤、保留或替换的分歧以及人物关系，不能用琐碎维修术语堆容量。
- **notes**：当前只锁馆守Z右臂处于可见的拆检受损状态，机械核心仍属于本体；右臂如何在E03留在旧址，由C01 L4的物理因果、战斗预案和演出规划共同决定。
- **role**：馆守Z右臂、兜灯整备和唐胶工艺判断空间
- **source_group_id**：MUSEUM
- **status**：core
- **type**：location

## C31 火种变形者

- 节点：`entity:R18`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`bm25`
- 分数：`344.5009`

- **aliases**：货柜领袖;可变机械生命;商品生命
- **canonical_name**：火种变形者
- **entity_id**：R18
- **implementation_policy**：C02由货柜领袖、四台同骨架重涂实机和未发售样件分别展开商品生命、同模不同主体与取消企划议题；具体加入状态按各机条目处理。不得把“火种”解释成G.A.G.本体或火种源。
- **notes**：木桶街与商品化主题的关键谱系，后续大型车队、战队和勇者机不是本包一机包办。
- **role**：商品生命与玩具宇宙谱系
- **source_group_id**：R18
- **status**：core
- **type**：roster_package

## C32 工务城

- 节点：`entity:LOC_PUBLIC_WORKS_CITY`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`bm25`
- 分数：`342.6269`

- **aliases**：环形工务城;公共巨构港;万机馆第一归港
- **canonical_name**：工务城
- **entity_id**：LOC_PUBLIC_WORKS_CITY
- **implementation_policy**：上环为可移动城区，中层为工务环轨，下层为旧巡展舰骨；C03结束后提供安全外泊、低速校正和有限事故支持，但不免费修复全部损伤。具体道路翻转、追击路线和泊位结构由C03预生产确定。
- **notes**：工务城不是代哥分部或单一反派城市；其连续运行系统真实救过人，也会把无主、无保险和难分类身体优先当作可征用部件。
- **role**：建立在灾前巡展舰骨上的三层移动城市，也是万机馆第一座可返回公共泊位
- **source_group_id**：PK_CORE_PUBLIC_WORKS
- **status**：needs_review
- **type**：location

## C33 七海 / 佐伯七海

- 节点：`art_lock:CML004`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv`
- 命中：`bm25`
- 分数：`341.5341`

- **age_band**：成年
- **asset_status**：locked_current
- **canon_entity_id**：CH_QIHAI
- **canonical_name**：七海 / 佐伯七海
- **current_art_reference**：.superpowers/brainstorm/37837-1782033239/content/char_tangjiao_doudeng_qihai_v3.png
- **gender_presentation**：日本成年女性
- **lock_id**：CML004
- **must_not**：第一章不得本人到场;不得纯反派威胁;不得少女化;不得把她写成代哥黑点拟人化或恋爱脑;不得抹掉日本派驻身份
- **notes**：法定名佐伯七海 / Nanami Saeki。她的魅力来自成熟权力感、公开承担、制度创造力和被万机馆生活拖进真实共同体；与白人欧洲创作者白鸢明确区分。
- **package_id**：ORG_DAIGE
- **personality_anchor**：成熟优雅的档案官;礼貌克制但有手腕;知道代哥生态腐化仍借流程改流程;生活中规整到近乎笨拙
- **pronouns_or_address**：她;七海;佐伯七海;Nanami
- **role_type**：代哥安全封存局档案官;内部改革派;远程秩序压力;临舰共同监督
- **source_refs**：docs/superpowers/specs/data/character_voice/character_dossiers_core.tsv;docs/superpowers/specs/data/canon/entities.tsv;docs/superpowers/specs/data/story/v35_core_cast_nationality_name_baseline_v1.tsv;docs/superpowers/specs/data/story/v35_core_cast_cultural_visual_diversity_v35_0.tsv;docs/superpowers/specs/剧情梗概/V35全剧结构母盘-候选v1-2026-07-20.md;docs/superpowers/specs/剧情梗概/V35-L1-L3到Current-Canon收敛迁移-2026-07-24.md;docs/superpowers/specs/剧情梗概/V35-C03四话结构复原与Current-Canon迁移-2026-07-26.md
- **story_gate**：C01E01-QIHAI-CONSOLE/V359-C03E04-CREATIVE
- **subject_id**：CH_QIHAI
- **subject_type**：character
- **unit_or_mecha_link**：封存流程;白名单;法务投影;公共信托开馆;临舰审查终端
- **visual_lock**：日本成年女性锁：深色直发、精致克制的日本/东亚五官、冷白法务服装、成熟秩序与危险吸引力；第一章只远程投影，C03实体到场并在E04登舰；不得再用模糊“东方系”替代国籍与生活来源
- **voice_rule**：公事口吻里留例外;危险感来自实际决定、现场承担和克制欲望;日常可以出现派驻生活与日本家庭习惯;不要撒娇或少女化
- **wound_or_drive**：见过失控机魂灾难;相信封存能保护世界;也知道限定、配额、商品化和运营指标正在磨损玩家热爱;害怕自己一旦进入生活就无法继续只做流程
- **显式关系**：
  - 美术主体 -> `entity:CH_QIHAI` 七海
  - Canon 主体 -> `entity:CH_QIHAI` 七海
  - 参战包 -> `entity:ORG_DAIGE` 代哥品牌资产秩序生态

## C34 铁馆魔神

- 节点：`wanji_coverage:R01`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/wanji_roster_zone_coverage.tsv`
- 命中：`graph_1hop_from:entity:CH002:来源组`
- 分数：`0.0000`

- **art_asset_hint**：馆守Z主展位;胸牌灯;右臂拆件;封闭层深处只画空间缺口与警示灯
- **c01_map_signal**：C01中庭可见并互动;前厅总图最大锚点
- **display_anchor**：馆守Z18米半跪实机;右臂旧件;B2封闭层状态灯
- **first_major_unlock**：C01
- **notes**：开局主轴，必须给最大视觉权重，但不能吞掉其他展区；不得预画指定的暗面机体。
- **package_id**：R01
- **package_name**：铁馆魔神
- **physical_scale**：18m实机;重型维修架
- **primary_zone_id**：WEZ_L1_01_GUARDIAN_ATRIUM
- **secondary_zone_ids**：WEZ_B1_01_HANGAR_VIEW;WEZ_B2_01_ZERO_BLACK_BOX_DEPTH
- **terminal_filter**：giant;guardian;sealed_core
- **显式关系**：
  - 主展区 -> `wanji_exhibition:WEZ_L1_01_GUARDIAN_ATRIUM` 万机中庭 / 巨神守护厅
  - 次展区 -> `wanji_exhibition:WEZ_B1_01_HANGAR_VIEW` 展舰机库参观窗
  - 次展区 -> `wanji_exhibition:WEZ_B2_01_ZERO_BLACK_BOX_DEPTH` 0号侧廊与黑匣子封存层

## C35 战前对话

- 节点：`gag_hook:IN003`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/gag_hooks.tsv`
- 命中：`graph_1hop_from:entity:V353U001:被相关主体`
- 分数：`0.0000`

- **category**：战前对话
- **entity_id**：CH036
- **first_allowed_scene**：V355-C01E03
- **hook_id**：IN003
- **implementation_note**：V355-C01E03豪司本人到场事件使用；不得恢复旧远程支援或展品借用单笑话。
- **payoff**：勇气不是审批通过，而是有人把失败、处罚和测试壳损伤实名背下。
- **related_entities**：CH001;V353U001
- **setup**：豪司现场报姓名、岗位和运输责任，申请在许可冻结状态下越权临控勇拳。
- **显式关系**：
  - 主梗主体 -> `entity:CH036` 豪司
  - 相关主体 -> `entity:CH001` 兜灯
  - 相关主体 -> `entity:V353U001` 馆守Z

## C36 deprecated_alias_of · MECHA_GUARDIAN_Z · V353U001

- 节点：`identity_link:IDL005`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/identity_links.tsv`
- 命中：`graph_1hop_from:entity:V353U001:被右侧主体`
- 分数：`0.0000`

- **left_entity_id**：MECHA_GUARDIAN_Z
- **link_id**：IDL005
- **notes**：馆守Z旧ID只作兼容跳转，制作和生命周期读取V353U001。
- **relation**：deprecated_alias_of
- **right_entity_id**：V353U001
- **scope**：V35.9
- **status**：active
- **显式关系**：
  - 右侧主体 -> `entity:V353U001` 馆守Z

## C37 生活温度

- 节点：`gag_hook:GH059`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/gag_hooks.tsv`
- 命中：`graph_1hop_from:entity:N_BAIYUAN:被相关主体`
- 分数：`0.0000`

- **category**：生活温度
- **entity_id**：CH_QIHAI
- **first_allowed_scene**：V359-C03E03-CREATIVE
- **hook_id**：GH059
- **implementation_note**：第一章仍禁止本人到场；C03实体到场与登舰读取合并后的当前E03，旧四话槽及旧章点只作History来源。
- **payoff**：她不是倒戈，而是从C01停权、C03事故责任一路被自己的公开追责拖进共同体。
- **related_entities**：CH_JICUN;N_BAIYUAN
- **setup**：七海以公开共同监督身份登舰，发现万机馆临时舱位比违规清单还乱。
- **显式关系**：
  - 主梗主体 -> `entity:CH_QIHAI` 七海
  - 相关主体 -> `entity:CH_JICUN` 纪存
  - 相关主体 -> `entity:N_BAIYUAN` 白鸢

## C38 巡展舰体与外泊层

- 节点：`entity:LOC_WANJI_MOBILE_CHASSIS`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`graph_1hop_from:entity:MECHA_WANJI_MOBILE_CHASSIS:来源组`
- 分数：`0.0000`

- **aliases**：地下旧舰体;巡展舰体;舰底;外部锁泊
- **canonical_name**：巡展舰体与外泊层
- **entity_id**：LOC_WANJI_MOBILE_CHASSIS
- **implementation_policy**：E03只以地下旧舰轮廓、应急灯和回应预显影；E04整体离地并进入外海战场。首章只需舰桥、主展厅、舰首装备位、外部锁泊与整体轮廓，不建立四岗位闯关、载荷二选一或复杂内部变形。
- **notes**：属于万机馆原有巡展舰身体，不是临时长出的新底盘；容量边界继续读取wanji_carrier_berths.tsv，后续现代泊位兼容由C02处理。
- **role**：万机馆由固定展馆恢复巡展舰身体的空间
- **source_group_id**：MUSEUM
- **status**：core
- **type**：location

## C39 模型病院与手作病历

- 节点：`wanji_collection:WCT_C02_MODEL_HOSPITAL`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/wanji_collection_taxonomy.tsv`
- 命中：`graph_1hop_from:entity:R22:被关联参战包`
- 分数：`0.0000`

- **activation_rule**：投入修复件;唐胶判断;孩子托付记录
- **c01_visibility**：open_c01
- **canonical_name**：模型病院与手作病历
- **collection_id**：WCT_C02_MODEL_HOSPITAL
- **display_form**：断件盒;姓名贴;补土;旧说明书;修复灯
- **gameplay_use**：微修复;改装提示;说得证物;战后展陈
- **linked_roster_packages**：C02;R18;R22;H07;H11
- **linked_unit_examples**：未发售样件;旧拳王;拼装诸侯会;五兽王冠
- **notes**：模型不是材料堆;每件重要模型都应有人名或旧使用痕迹。
- **relation_type**：hobby_artifact
- **size_class**：DESK_TO_SMALL
- **storage_or_berth_rule**：常驻L1/工坊;关联真机通过外部样件仓、角色支线或残响投射
- **story_function**：把收藏、修复、玩具商品化和童年托付连起来
- **显式关系**：
  - 关联参战包 -> `entity:R18` 火种变形者
  - 关联参战包 -> `entity:R22` 钢拳擂台
  - 关联参战包 -> `wanji_coverage:H07` 拼装诸侯会
  - 关联参战包 -> `wanji_coverage:H11` 五兽王冠

## C40 钢拳擂台

- 节点：`wanji_coverage:R22`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/wanji_roster_zone_coverage.tsv`
- 命中：`graph_1hop_from:entity:R22:被参战包`
- 分数：`0.0000`

- **art_asset_hint**：小擂台;旧手套;欢呼灯条
- **c01_map_signal**：C01模型街有拳套小件
- **display_anchor**：旧拳王模型;影子陪练机;观众欢呼计
- **first_major_unlock**：C02;C03
- **notes**：失败父亲修复线要和模型修复、非致命战连起来。
- **package_id**：R22
- **package_name**：钢拳擂台
- **physical_scale**：擂台道具;中小型机
- **primary_zone_id**：WEZ_L2_05_DUEL_SPORTS_CORNER
- **secondary_zone_ids**：WEZ_L1_03_MODEL_TOY_STREET;WEZ_L1_04_REAL_CIVIC_LAB
- **terminal_filter**：boxing;father;nonlethal
- **显式关系**：
  - 参战包 -> `entity:R22` 钢拳擂台
  - 主展区 -> `wanji_exhibition:WEZ_L2_05_DUEL_SPORTS_CORNER` 擂台与运动机器人角
  - 次展区 -> `wanji_exhibition:WEZ_L1_03_MODEL_TOY_STREET` 模型玩具街 / 手作圣堂
  - 次展区 -> `wanji_exhibition:WEZ_L1_04_REAL_CIVIC_LAB` 现实机器与市政实验场

## C41 模型玩具街 / 手作圣堂

- 节点：`wanji_exhibition:WEZ_L1_03_MODEL_TOY_STREET`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/wanji_exhibition_zones.tsv`
- 命中：`graph_1hop_from:entity:R22:被覆盖参战包`
- 分数：`0.0000`

- **approx_scale**：约30x10m;多排柜台
- **art_brief**：像玩家自己的收藏柜被放大成街;盒绘、透明盒、补件盘和姓名贴要密
- **c01_access_state**：public_open
- **canonical_name**：模型玩具街 / 手作圣堂
- **floor_band**：L1
- **map_code**：L1-W03
- **map_position**：主厅西侧暖灯长廊
- **notes**：模型不是低级展品，而是万机馆最有目标玩家情感的展区。
- **roster_coverage**：R18;R22;H07;H09;H10;H11;H12
- **scene_use**：唐胶登场;C02模型线;战后展陈;收藏情感
- **signature_displays**：模型病院;旧盒绘墙;重涂柜;断件病历;孩子寄存格
- **terminal_map_layer**：model_layer;collection_layer
- **visual_density**：very_high
- **zone_id**：WEZ_L1_03_MODEL_TOY_STREET
- **显式关系**：
  - 覆盖参战包 -> `entity:R18` 火种变形者
  - 覆盖参战包 -> `entity:R22` 钢拳擂台
  - 覆盖参战包 -> `wanji_coverage:H07` 拼装诸侯会
  - 覆盖参战包 -> `wanji_coverage:H09` 彩队巨神
  - 覆盖参战包 -> `wanji_coverage:H10` 电磁五虎机
  - 覆盖参战包 -> `wanji_coverage:H11` 五兽王冠
  - 覆盖参战包 -> `wanji_coverage:H12` 铁巨人朋友

## C42 现实机器与市政实验场

- 节点：`wanji_exhibition:WEZ_L1_04_REAL_CIVIC_LAB`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/wanji_exhibition_zones.tsv`
- 命中：`graph_1hop_from:entity:R22:被覆盖参战包`
- 分数：`0.0000`

- **approx_scale**：约26x12m;软垫舞台
- **art_brief**：冷白工程灯加生活化标识;软垫、充电线、维修车和失败记录都要可见
- **c01_access_state**：public_open
- **canonical_name**：现实机器与市政实验场
- **floor_band**：L1
- **map_code**：L1-E04
- **map_position**：主厅东侧靠充电桩
- **notes**：这一带要和超级系形成强烈反差：小、笨、真实，但一样值得保护。
- **roster_coverage**：R24;R10;R20;R21;R22
- **scene_use**：现实机器尊严;第3章伏笔;非致命护送
- **signature_displays**：跌跌小舞台;市政作业臂;看护机器人标本;涂鸦训练板;摔倒次数白板
- **terminal_map_layer**：real_machine_layer;objective_layer
- **visual_density**：high
- **zone_id**：WEZ_L1_04_REAL_CIVIC_LAB
- **显式关系**：
  - 覆盖参战包 -> `entity:R24` 第0次站立
  - 覆盖参战包 -> `wanji_coverage:R10` 工务机动队
  - 覆盖参战包 -> `wanji_coverage:R20` 三法城
  - 覆盖参战包 -> `wanji_coverage:R21` 废城小查
  - 覆盖参战包 -> `entity:R22` 钢拳擂台

## C43 擂台与运动机器人角

- 节点：`wanji_exhibition:WEZ_L2_05_DUEL_SPORTS_CORNER`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/wanji_exhibition_zones.tsv`
- 命中：`graph_1hop_from:entity:R22:被覆盖参战包`
- 分数：`0.0000`

- **approx_scale**：约18x10m
- **art_brief**：小擂台、护栏、旧海报、维修胶布;生活气强
- **c01_access_state**：locked_after_c01
- **canonical_name**：擂台与运动机器人角
- **floor_band**：L2
- **map_code**：L2-SW05
- **map_position**：二楼西南小展场
- **notes**：给“机器人也可以是运动、失败父亲和小镇生活”一个空间。
- **roster_coverage**：R22;R10;R24;R08
- **scene_use**：第2/3章擂台线;非致命决斗;热血训练
- **signature_displays**：旧拳王手套;影子陪练机;观众欢呼计;钻头训练靶
- **terminal_map_layer**：duel_layer;crowd_layer
- **visual_density**：medium
- **zone_id**：WEZ_L2_05_DUEL_SPORTS_CORNER
- **显式关系**：
  - 覆盖参战包 -> `entity:R22` 钢拳擂台
  - 覆盖参战包 -> `wanji_coverage:R10` 工务机动队
  - 覆盖参战包 -> `entity:R24` 第0次站立
  - 覆盖参战包 -> `wanji_coverage:R08` 钻破天盖

## C44 纪存 / 玩家名

- 节点：`art_lock:CML001`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv`
- 命中：`graph_1hop_from:entity:CH_JICUN:被Canon 主体`
- 分数：`0.0000`

- **age_band**：青年
- **asset_status**：locked_current
- **canon_entity_id**：CH_JICUN
- **canonical_name**：纪存 / 玩家名
- **current_art_reference**：.superpowers/brainstorm/37837-1782033239/content/asset-production/core-cast-v1/core_jicun_stand.png
- **gender_presentation**：中国青年男性呈现;机魂主体;玩家名可变
- **lock_id**：CML001
- **must_not**：不得写成无情记录机器;不得万能谜语主角;不得回到眼镜成熟版或幼相版;不得画成旧馆长克隆体
- **notes**：中国身份来自纪文山和万机馆社会语境的引导、长期生活与纪存主动认领，不代表生物人类血统。人物魅力来自判断、照顾、行动和记住具体的人，不用责任结算句式代替成长。
- **personality_anchor**：冷静档案员;用吐槽和归档动作遮住不安
- **pronouns_or_address**：他;纪存;玩家名
- **role_type**：第一主角;档案员
- **source_refs**：docs/superpowers/specs/data/character_voice/character_dossiers_core.tsv;docs/superpowers/specs/data/canon/entities.tsv;docs/superpowers/specs/data/story/v35_core_cast_nationality_name_baseline_v1.tsv;.superpowers/brainstorm/37837-1782033239/content/c-route-next-production-assets-36.html
- **story_gate**：C01-COLD-OPEN
- **subject_id**：CH_JICUN
- **subject_type**：character
- **unit_or_mecha_link**：纪存档案终端
- **visual_lock**：36页按用户贴图锁定：黑发蓝眼、无眼镜、中国青年男性外观、青年而不幼、馆内制服、左臂档案终端、微白机魂光；五官来自本地服务体和馆员/观众记忆的综合生成，不得画成纪文山的年轻复制品；后续补机魂异常状态差分
- **voice_rule**：说人话;先照顾听众和场面;不要替主题做总结
- **wound_or_drive**：怕遗漏;怕把人先变成记录再理解
- **显式关系**：
  - 美术主体 -> `entity:CH_JICUN` 纪存
  - Canon 主体 -> `entity:CH_JICUN` 纪存

## C45 纪存的被弃回应起源

- 节点：`entity:CONCEPT_JICUN_DISCARDED_RESPONSE_ORIGIN`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35世界机制与创作接口设定基线-2026-07-19.md`
- 命中：`graph_1hop_from:entity:CH_JICUN:被来源组`
- 分数：`0.0000`

- **aliases**：被删回应;空白展柜回应;未归类机魂汇聚
- **canonical_name**：纪存的被弃回应起源
- **entity_id**：CONCEPT_JICUN_DISCARDED_RESPONSE_ORIGIN
- **implementation_policy**：纪存不是死者拼盘、统一蜂群或索引善良半身；他拥有新的主体连续性。具体参与片段、旧馆长作用和人形载体来历保持OPEN。
- **notes**：他的主角成长是从被丢弃的答案中醒来，学会用智慧与力量保护差异，同时主动限制自己替所有人解释的能力。
- **role**：万机馆离线保全层锚住二十七年前被统一回应拒绝、被清噪、互相矛盾或无法归类的主体响应，这些响应在长期路由中诞生了纪存这个新的人
- **source_group_id**：CH_JICUN
- **status**：working_current
- **type**：concept
- **显式关系**：
  - 来源组 -> `entity:CH_JICUN` 纪存
