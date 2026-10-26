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

- 请求：`docs/superpowers/specs/story-runtime/context-packs/C02-runtime-v2/00-C02上下文需求-v2.md`
- 只含 Hard / Working、active Current Canon 的检索投影。
- C02 场景节点与指向这些节点的关系禁读；实体事实允许使用，但不能把实体说明里的旧动作当成新稿场面。
- 盲测过滤节点：**4**
- 为避免章节时序答案泄漏，已隐藏字段：``

## C01 旧守护者

- 节点：`entity:CH002`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`438.2073`

- **aliases**：Old Guardian;导览人格;馆守Z导览人格
- **canonical_name**：旧守护者
- **entity_id**：CH002
- **first_battle_join**：V355-C01E02
- **first_foreshadow**：V355-C01E01
- **first_formal_appearance**：V355-C01E01
- **implementation_policy**：第一章先以轮式导览终端和馆内广播陪伴观众；终端被压后，同一句话从馆守Z胸前扬声器继续说完。人格根始终固定在馆守Z胸腔保护舱内，E02在兜灯解除物理限位、七海撤回本人停机令后取得巨体运动权。
- **notes**：旧守护者与馆守Z是同一主体的日常称呼和正式机体名；导览终端、广播与胸前扬声器只是远程感官和输出端，不是独立AI或可复制机魂。纪存进入导览席只提供路线与判断，不控制四肢。
- **role**：馆守Z机魂人格;展厅导览人格
- **source_group_id**：R01
- **status**：core
- **type**：character
- **显式关系**：
  - 来源组 -> `wanji_coverage:R01` 铁馆魔神
  - 首次伏笔 -> `scene:V355-C01E01` 最后一场导览
  - 正式登场 -> `scene:V355-C01E01` 最后一场导览
  - 首次战斗加入 -> `scene:V355-C01E02` 巨神从展台起身

## C02 馆守Z

- 节点：`entity:V353U001`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`explicit_seed, bm25`
- 分数：`393.7277`

- **aliases**：铁馆魔神;18米旧巨神;馆守巨神
- **canonical_name**：馆守Z
- **entity_id**：V353U001
- **first_battle_join**：V355-C01E02
- **first_foreshadow**：V355-C01E01
- **first_formal_appearance**：V355-C01E02
- **implementation_policy**：与MECHA_GUARDIAN_Z为同一机体的V35生命周期ID；旧守护者是其机魂人格。C01E02完成首次正式战斗，E03以过载火箭右拳和勇拳接力击穿BREAKER地面甲壳，右臂回收机构烧毁、主要残片留在旧址；E04装上非拳击型巡展臂装并以左拳击毁飞行核心。后续必须通过独立剧情获得真正后继右臂，不能无损找回旧臂。
- **notes**：内部锚Mazinger式火箭拳、旧超级系后继强化与博物馆守护者；后继弧读取CONCEPT_GZ_SUCCESSOR_ARM_ARC。
- **role**：18米开局旧巨神主力；C01失去原右拳与完整前臂，此后经历巡展臂装、代用结构和后继右臂成长
- **source_group_id**：PK_CORE_IRON_GUARD
- **status**：working_current
- **type**：mecha
- **显式关系**：
  - 首次伏笔 -> `scene:V355-C01E01` 最后一场导览
  - 正式登场 -> `scene:V355-C01E02` 巨神从展台起身
  - 首次战斗加入 -> `scene:V355-C01E02` 巨神从展台起身

## C03 玩家模型机“无牌一号”

- 节点：`entity:V353U071`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`314.1797`

- **aliases**：无牌一号;全尺寸改件竞技实机
- **canonical_name**：玩家模型机“无牌一号”
- **entity_id**：V353U071
- **first_battle_join**：V359-C02E01-CREATIVE
- **first_foreshadow**：V359-C02E01-CREATIVE
- **first_formal_appearance**：V359-C02E01-CREATIVE
- **implementation_policy**：木桶街原有全尺寸模块竞赛底盘和低权限竞赛AI；缩尺模型只提供改件同构数据，不会放大成机体。它在C02首控，V359-C03E04-CREATIVE经正常运输取得随舰构筑席；首个作业模块由C03 L4确定。
- **notes**：内部锚Gundam Build与模型竞技；名称可由玩家改，不共享社勇王许可。
- **role**：自由改装、零件兼容和玩家构筑单位
- **source_group_id**：PK_GUEST_BUILD_ARENA
- **status**：needs_review
- **type**：mecha

## C04 纪存

- 节点：`entity:CH_JICUN`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`288.2008`

- **aliases**：Ji Cun;Jicun
- **canonical_name**：纪存
- **entity_id**：CH_JICUN
- **first_battle_join**：V355-C01E01
- **first_foreshadow**：C01-COLD-OPEN
- **first_formal_appearance**：C01E01-ADV
- **implementation_policy**：主角视角优先承担玩家认知，不替设定朗读百科；他在C01主动组织闭馆、救人、保护机体并决定让万机馆离地。作为逐渐苏醒的机魂实体，他必须主动判断、调查、犯险和解决谜团；过往记忆通过行动与代价苏醒，不以存档、贴标签、行政词汇或被动受难代替成长。具体首战结构由C01 L4决定。
- **notes**：纪存没有生物人类血统，但由中国馆长纪文山和万机馆本地社会语料引导形成中文母语化人格、中国文化认同与中国青年男性外观；他不是纪文山的克隆或年轻复制品。纪姓与名字以后可以被他重新确认。对馆体、馆藏机魂和灾前导览系统的深层联系仍按剧情揭示。
- **role**：临时闭馆负责人;机魂实体主角;记忆苏醒者
- **source_group_id**：PROTAGONIST
- **status**：core
- **type**：character
- **显式关系**：
  - 首次战斗加入 -> `scene:V355-C01E01` 最后一场导览

## C05 万机馆巡展舰体

- 节点：`entity:MECHA_WANJI_MOBILE_CHASSIS`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`explicit_seed, bm25`
- 分数：`270.6790`

- **aliases**：万机馆展舰;旧巡展舰;WBM001
- **canonical_name**：万机馆巡展舰体
- **entity_id**：MECHA_WANJI_MOBILE_CHASSIS
- **first_battle_join**：V355-C01E04
- **first_foreshadow**：V355-C01E01
- **first_formal_appearance**：V355-C01E04
- **implementation_policy**：生产态只保留固定展馆、离地转换和巡展舰三态；E01旧照片预告巡展形态，E03地下轮廓回应，E04恢复舰体并进入空战。首战可调用真实巡展史中的退役重盾、救援锚、推进骨架和有限防卫炮，但不是完整战舰火力、无限格纳库或人形机器人。
- **notes**：与WBM001、LOC_WANJI_MOBILE_CHASSIS和泊位规则共同定义后续主循环；旧引擎只足以可靠抵达邻近一站，且缺现代泊位接口。馆藏不会逐件变形成舰体零件。
- **role**：C01E04恢复的百米级移动基地与母舰身体
- **source_group_id**：LOC_WANJI_MOBILE_CHASSIS
- **status**：working_current
- **type**：mecha
- **显式关系**：
  - 来源组 -> `entity:LOC_WANJI_MOBILE_CHASSIS` 巡展舰体与外泊层
  - 首次伏笔 -> `scene:V355-C01E01` 最后一场导览
  - 正式登场 -> `scene:V355-C01E04` 博物馆追上天空
  - 首次战斗加入 -> `scene:V355-C01E04` 博物馆追上天空

## C06 七海

- 节点：`entity:CH_QIHAI`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`242.0166`

- **aliases**：佐伯七海;佐伯 七海;さえき ななみ;Nanami Saeki;Qihai
- **canonical_name**：七海
- **entity_id**：CH_QIHAI
- **first_foreshadow**：C01E01-QIHAI-PRIVATE-AUDIO
- **first_formal_appearance**：C01E01-QIHAI-CONSOLE
- **implementation_policy**：日本公民，成长于神奈川县横滨港区，成年后派驻代哥中国东部沿海分部与本市封存中心。中文界面与同伴称七海，正式文件使用佐伯七海，国际文件使用Nanami Saeki；Qihai只作旧工程转写。C01可先以无公务UI的私人语音建立她与纪存的既有私交；闭馆接管正式启动后，她才以公务风险频道介入现场。第一章始终远程出场，只能撤销本人签发的命令并为自己的判断承担停权，不能替军方、平台或城市授权；具体切电、撤令和UI顺序由C01 L4裁决。C03经公共交通实体到场并限段入住。
- **notes**：她不是代哥黑点的拟人化，而是知道品牌资产生态腐化、仍试图把流程拉回初心的成熟改革者。她的日本企业/公共安全经验和中国派驻生活都要进入日常与选择；后续具体伤势、旧项目责任、权限迁移和关系选择必须从候选覆盖层另查。
- **role**：代哥安全封存局档案官;内部改革派
- **source_group_id**：ORG_DAIGE
- **status**：core
- **type**：character
- **显式关系**：
  - 来源组 -> `entity:ORG_DAIGE` 代哥品牌资产秩序生态

## C07 万机馆主循环磁流散热转子

- 节点：`entity:MECHA_WANJI_MAIN_CIRCULATION_ROTOR`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`238.1769`

- **aliases**：主循环转子;巨型转子;展舰散热转子
- **canonical_name**：万机馆主循环磁流散热转子
- **entity_id**：MECHA_WANJI_MAIN_CIRCULATION_ROTOR
- **first_battle_join**：V359-C02E01-CREATIVE
- **first_foreshadow**：V359-C02E01-CREATIVE
- **first_formal_appearance**：V359-C02E01-CREATIVE
- **implementation_policy**：它是场景巨构和任务载荷，不是人格机体、不计参战；模型批次与维修史只能帮助辨认版本和适配方法，真正安装仍需全尺寸实物与工程复核。安装只恢复有限航行，不解决永久外泊、校正和保险。
- **notes**：正式资产应突出巨大转子、运输架、吊装和万机馆检修窗，不制作密集内部机构动画；精确尺寸、重量和安装动作由C02预生产确定。
- **role**：C02使万机馆恢复有限航行的全尺寸工业总成，必须由重型运输和吊装设备搬运，不能退化成手掌大的密封件
- **source_group_id**：MUSEUM
- **status**：needs_review
- **type**：scene_mecha

## C08 商品回收王牌“归一星”

- 节点：`entity:ENEMY_C02_UNITY_RECLAIMER`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`225.7328`

- **aliases**：归一星;人格回收王牌;SKU追猎机
- **canonical_name**：商品回收王牌“归一星”
- **entity_id**：ENEMY_C02_UNITY_RECLAIMER
- **first_battle_join**：V359-C02E02-CREATIVE
- **first_foreshadow**：V359-C02E02-CREATIVE
- **first_formal_appearance**：V359-C02E02-CREATIVE
- **implementation_policy**：它能调用商品回收设施和复制已取得的工厂动作样本，但不能复制四机后来形成的主体判断。具体武装、场地控制和破局方式由C02 L4决定。
- **notes**：归一星属于商品回收实体执行链，不是胶价王投影或索引人格；内部锚商品回收、量产王牌和统一模板，外观不复刻具体喷气角色。
- **role**：C02重涂人格空战具名敌机，读取四台重涂机的工厂动作库并试图把它们压回同一商品身份
- **source_group_id**：DAIGE_PRODUCT
- **status**：needs_review
- **type**：enemy_unit

## C09 白鸢

- 节点：`entity:N_BAIYUAN`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`217.3756`

- **aliases**：Evelyn Voss;White Kite;创作者遗民;改写者;分镜本;艾芙琳·沃斯;Aveline Voss
- **canonical_name**：白鸢
- **entity_id**：N_BAIYUAN
- **first_foreshadow**：V359-C02E01-CREATIVE
- **first_formal_appearance**：V359-C02E03-CREATIVE
- **implementation_policy**：英国公民Evelyn Voss，来自英德创作者家庭；White Kite为英文署名，中文发行与玩家界面保持意译笔名白鸢，Baiyuan不再作为原生国际名。C02E01先以被盗用的作品留下痕迹，C02E03肉身到场并临时随舰，C03完成第一份多人可改的共同作品。她把旧分镜、现场传感、地形与机体数据整理成可讨论的预演草图，真实动作仍由驾驶员、机体与工程链执行；当前没有战斗指令权、未来视、造物或画稿改现实能力。
- **notes**：她是会画成人向擦边同人的成年欧美创作者，日常色气、嘴硬和跨语言创作趣味与正剧控制欲形成反差。与纪存、七海的吸引、误解和独立亲近均需通过具体共同经历推进；后续战术席位、不可逆选择与能力升级只从候选覆盖层读取。
- **role**：作者遗迹、战术预演与纪存/七海关系线核心角色
- **source_group_id**：CREATOR_LINE
- **status**：core
- **type**：character

## C10 白框具身生产链

- 节点：`entity:CONCEPT_WHITEFRAME_EMBODIMENT_CHAIN`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35世界机制与创作接口设定基线-2026-07-19.md`
- 命中：`explicit_seed, bm25`
- 分数：`203.4129`

- **aliases**：白框生态;标准身体;采样回收制造链
- **canonical_name**：白框具身生产链
- **entity_id**：CONCEPT_WHITEFRAME_EMBODIMENT_CHAIN
- **first_foreshadow**：SYSTEM-DESIGN
- **first_formal_appearance**：SYSTEM-DESIGN
- **implementation_policy**：白框没有单一幕后主谋，也不是索引分身；索引可逐步借合作、数据和漏洞调用它。每次物理行动必须说明具体机构、设备、身体和中止链。
- **notes**：白函、归一星、衡令、百相等均是各自操作者/协议的实体，不自动等于索引人格。
- **role**：企业、城市、军方与平台共同使用的采样、兼容、回收和标准身体生产生态，为安全答案和无身意识提供物理执行体
- **source_group_id**：WHITEFRAME
- **status**：working_current
- **type**：concept

## C11 兜灯

- 节点：`entity:CH001`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`193.7368`

- **aliases**：窦晓宁;Dou Xiaoning;Doudeng
- **canonical_name**：兜灯
- **entity_id**：CH001
- **first_battle_join**：V355-C01E01
- **first_foreshadow**：C01E01-REPAIR-BAY
- **first_formal_appearance**：C01E01-REPAIR-BAY
- **implementation_policy**：可在第一章作为维修与安全操作单位出现；她负责判断馆守Z何时能够行动、何时必须制动，并能在现场真正执行，不由纪存或系统代替。具体战斗动作和回合数由C01 L4决定。
- **notes**：中国公民，本名窦晓宁；兜灯是窦姓与童年头灯习惯形成的维修组昵称。铁馆魔神线入口，和馆守Z的长期关系优先于一次战斗爽点；旧C01E02-BATTLE-START仅为历史实现时序。
- **role**：馆守Z整备员
- **source_group_id**：R01
- **status**：core
- **type**：character
- **显式关系**：
  - 来源组 -> `wanji_coverage:R01` 铁馆魔神
  - 首次战斗加入 -> `scene:V355-C01E01` 最后一场导览

## C12 影子陪练机

- 节点：`entity:V353U049`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`192.1188`

- **aliases**：旧拳王陪练;影子模式机
- **canonical_name**：影子陪练机
- **entity_id**：V353U049
- **first_battle_join**：V359-C02E03-CREATIVE
- **first_foreshadow**：V359-C02E03-CREATIVE
- **first_formal_appearance**：V359-C02E03-CREATIVE
- **implementation_policy**：与MECHA_SHADOW_SPARRING_MACHINE为同一机体的V35生命周期ID；C02参加擂台，录像与原主体同意决定后续可用性，是否随舰由C02 L4裁决。
- **notes**：内部锚机器人拳击影子模式。
- **role**：动作复制、反击教学和非致命训练路线机
- **source_group_id**：PK_GUEST_IRON_FIST
- **status**：needs_review
- **type**：mecha

## C13 火种货柜领袖

- 节点：`entity:V353U043`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`177.3413`

- **aliases**：货柜领袖;变形货柜生命
- **canonical_name**：火种货柜领袖
- **entity_id**：V353U043
- **first_battle_join**：V359-C03E04-CREATIVE
- **first_foreshadow**：V359-C02E01-CREATIVE
- **first_formal_appearance**：V359-C02E01-CREATIVE
- **implementation_policy**：以已有全尺寸载具身体和独立载具人格参加C02，并完成护送万机馆到工务城的一站承诺；C03E04离舰，承担百机航路邀请的地面转递，后续可沿航路召回。它可以进入作业变形形态，但不等于星火车队、火种源或G.A.G.本体。
- **notes**：内部锚Transformers领袖与车队文化；C04不占舰位，C06不得由它包办星火车队谱系。
- **role**：作业变形、护送和领袖支援主力
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha
- **显式关系**：
  - 首次战斗加入 -> `scene:V359-C03E04-CREATIVE` 第一座可以回来的城

## C14 旧拳王机

- 节点：`entity:V353U048`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`175.2180`

- **aliases**：钢拳旧王;退役拳击机器人
- **canonical_name**：旧拳王机
- **entity_id**：V353U048
- **first_battle_join**：V359-C02E03-CREATIVE
- **first_foreshadow**：V359-C02E03-CREATIVE
- **first_formal_appearance**：V359-C02E03-CREATIVE
- **implementation_policy**：与MECHA_OLD_BOXER_KING为同一机体的V35生命周期ID；C02作为完整可驾驶机体赢得擂台并正式加入，右拳护具永不计作独立机体。
- **notes**：内部锚Real Steel式机器人拳击；具体影子模式错位和决胜拳由C02 L4决定。
- **role**：拳击、受击蓄势和非致命击倒主力
- **source_group_id**：PK_GUEST_IRON_FIST
- **status**：needs_review
- **type**：mecha

## C15 全装冠军“百刃”

- 节点：`entity:ENEMY_C02_FULL_ARMOR_CHAMPION_BAIREN`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`160.3683`

- **aliases**：百刃;全装擂王;过度配件冠军
- **canonical_name**：全装冠军“百刃”
- **entity_id**：ENEMY_C02_FULL_ARMOR_CHAMPION_BAIREN
- **first_battle_join**：V359-C02E03-CREATIVE
- **first_foreshadow**：V359-C02E03-CREATIVE
- **first_formal_appearance**：V359-C02E03-CREATIVE
- **implementation_policy**：必须是完整拳斗或竞技实机；过量配件既带来正面战力，也形成一眼可懂的体积、转向和场地限制，不得只当笑话靶。具体拳赛阶段和破局动作由C02 L4决定。
- **notes**：与旧拳王形成朴素机体对全装商品奇观；正式造型需避开现实产品的一比一拼贴。
- **role**：C02非致命擂台对手机，以过量尖刺、背包和武器包承载模玩过度设计与全装崇拜
- **source_group_id**：MODEL_STREET
- **status**：needs_review
- **type**：enemy_unit

## C16 喷气叛星

- 节点：`entity:V353U044`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`154.8124`

- **aliases**：叛星;重涂喷气首领
- **canonical_name**：喷气叛星
- **entity_id**：V353U044
- **first_battle_join**：V359-C02E02-CREATIVE
- **first_foreshadow**：V359-C02E02-CREATIVE
- **first_formal_appearance**：V359-C02E02-CREATIVE
- **implementation_policy**：C02完成首次战斗并确认独立主体身份；它承认自己也是重涂角色，不以原版血统洗白。后续加入和回收节点由L3生命周期表决定。
- **notes**：内部锚Starscream式叛星；必须有独立头雕、翼型、武器和性格。
- **role**：高速空战、诱饵分身和品牌背叛路线机
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C17 重涂机“死锁”

- 节点：`entity:V353U045`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`152.0754`

- **aliases**：死锁;旧人格近战重涂
- **canonical_name**：重涂机“死锁”
- **entity_id**：V353U045
- **first_battle_join**：V359-C02E02-CREATIVE
- **first_foreshadow**：V359-C02E02-CREATIVE
- **first_formal_appearance**：V359-C02E02-CREATIVE
- **implementation_policy**：C02完成首次战斗并确认独立主体身份；它拒绝被改写成更好卖的英雄版本。后续加入和回收节点由L3生命周期表决定。
- **notes**：内部锚热门重涂与漂移/死锁式身份记忆；正式公开前做避撞审查。
- **role**：近战突入与旧人格冲突路线机
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C18 机魂本地涌现反馈环

- 节点：`entity:CONCEPT_MACHINE_SOUL_EMERGENCE_LOOP`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35世界机制与创作接口设定基线-2026-07-19.md`
- 命中：`explicit_seed, bm25`
- 分数：`146.4007`

- **aliases**：机魂形成环;本地成魂;具身关系闭环;local soul emergence
- **canonical_name**：机魂本地涌现反馈环
- **entity_id**：CONCEPT_MACHINE_SOUL_EMERGENCE_LOOP
- **first_foreshadow**：SYSTEM-DESIGN
- **first_formal_appearance**：SYSTEM-DESIGN
- **implementation_policy**：形成发生在具体机体AI核、整副身体、实时黑匣或有明确根节点的本地系统；承认、命名、玩梗、维修和观看可促进时间连续与社会边界，却不是造魂咒语。相同型号、相同动作包可以形成不同主体；复杂AI和热门机体也可能永远没有机魂。
- **notes**：现阶段C05百相副驾驶是最清楚的当代样例；C01跌跌、C02四台重涂机和C03城梁一号从不同尺度提供辅助证据。
- **role**：本地AI/控制核持续运行，具身感知与动作史形成个体差异，个人记忆不被全部清空，人机关系持续把它当作同一对象回应，G.A.G.文化反馈再进入本地系统，最终使其能区分外部期待与自身选择
- **source_group_id**：WORLD_ROOT
- **status**：working_current
- **type**：concept

## C19 万机馆藏品-机体关联规则

- 节点：`entity:CONCEPT_WANJI_COLLECTION_LINKAGE`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`134.0533`

- **aliases**：藏品谱系;模型关系钥匙;展品锚点;collection taxonomy
- **canonical_name**：万机馆藏品-机体关联规则
- **entity_id**：CONCEPT_WANJI_COLLECTION_LINKAGE
- **first_foreshadow**：SYSTEM-DESIGN
- **first_formal_appearance**：SYSTEM-DESIGN
- **implementation_policy**：新增参战机体或展品必须说明馆内锚点、关系类型、激活条件和随舰状态；模型/玩具可作为关系钥匙和结构证物，不直接无代价变真机。
- **notes**：对应wanji_collection_taxonomy.tsv和DOC_WANJI_COLLECTION_CARRIER_DESIGN。
- **role**：定义展品、藏品、模型、黑匣子和参战机体的连接方式
- **source_group_id**：MUSEUM
- **status**：core
- **type**：concept

## C20 重涂机“雷翎”

- 节点：`entity:V353U047`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`132.9465`

- **aliases**：雷翎;喷气远射重涂
- **canonical_name**：重涂机“雷翎”
- **entity_id**：V353U047
- **first_battle_join**：V359-C02E02-CREATIVE
- **first_foreshadow**：V359-C02E02-CREATIVE
- **first_formal_appearance**：V359-C02E02-CREATIVE
- **implementation_policy**：C02完成首次战斗并确认独立主体身份；具体收尾动作和轮换冲突由C02 L4决定。后续加入和回收节点由L3生命周期表决定。
- **notes**：内部锚喷气重涂军团。
- **role**：远射、侦察和机动换位路线机
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C21 重涂机“镜星”

- 节点：`entity:V353U046`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`131.5651`

- **aliases**：镜星;镜像重涂
- **canonical_name**：重涂机“镜星”
- **entity_id**：V353U046
- **first_battle_join**：V359-C02E02-CREATIVE
- **first_foreshadow**：V359-C02E02-CREATIVE
- **first_formal_appearance**：V359-C02E02-CREATIVE
- **implementation_policy**：C02完成首次战斗并确认独立主体身份；镜像涂装必须服务它自己的立场与行动，不只作皮肤。后续加入和回收节点由L3生命周期表决定。
- **notes**：内部锚镜像世界重涂。
- **role**：电子干扰和敌我标识翻转路线机
- **source_group_id**：PK_GUEST_FIRESEED
- **status**：needs_review
- **type**：mecha

## C22 唐胶

- 节点：`entity:CH_TANGJIAO`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`124.5943`

- **aliases**：唐启明;Tang Qiming;Tangjiao;N_TANGJIAO
- **canonical_name**：唐胶
- **entity_id**：CH_TANGJIAO
- **first_battle_join**：V355-C01E01
- **first_foreshadow**：C01E01-MAIN-COMBO_TABLE
- **first_formal_appearance**：C01E01-MAIN-COMBO_TABLE
- **implementation_policy**：第一章可作为维修、路障和手作价值观角色；Story-First首次战术行动为E01把安全罩改成导光挡板；台词必须来自工艺细节，不说主题金句。
- **notes**：中国公民，本名唐启明；唐胶是模型街工房外号。正式合同和家庭危机场可用本名，日常与玩家界面保持唐胶；旧C01E02-BATTLE-START仅为历史实现时序。
- **role**：模型修复师;嘴毒手作派
- **source_group_id**：MUSEUM
- **status**：core
- **type**：character
- **显式关系**：
  - 首次战斗加入 -> `scene:V355-C01E01` 最后一场导览

## C23 陆衡

- 节点：`entity:CH_LUHENG`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`explicit_seed, bm25`
- 分数：`110.6538`

- **aliases**：陆衡·姆旺吉;Heng Lu Mwangi;Lu Heng;Luheng;N_LUHENG;现实工程师
- **canonical_name**：陆衡
- **entity_id**：CH_LUHENG
- **first_foreshadow**：V359-C03E01-CREATIVE
- **first_formal_appearance**：V359-C03E01-CREATIVE
- **implementation_policy**：中国与肯尼亚双重家庭及跨港公民背景；母系陆家来自中国沿海工业区，父系Mwangi家来自蒙巴萨港。C01不出场、不随舰；其正式加入时机由C03新L4重编。C03仍可保留他曾为采购删去稳定程序现场语境的责任线，但具体到场、资质后果和随舰状态由该章重新封存。
- **notes**：中文团队称陆衡，国际工程文件使用Heng Lu Mwangi。工程能力来自教育、港口生活和失败经验，不来自族裔刻板；说话要来自参数、工况和失败记录，不能只吐槽不科学。
- **role**：现实工程师;跨港工务顾问
- **source_group_id**：R24
- **status**：core
- **type**：character
- **显式关系**：
  - 来源组 -> `entity:R24` 第0次站立
  - 首次伏笔 -> `scene:V359-C03E01-CREATIVE` 整座城压上来
  - 正式登场 -> `scene:V359-C03E01-CREATIVE` 整座城压上来

## C24 博物馆追上天空

- 节点：`scene:V355-C01E04`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md`
- 命中：`bm25`
- 分数：`635.6234`

- **allowed_new_entities**：MECHA_GUARDIAN_TOURING_ARM;MECHA_WANJI_MOBILE_CHASSIS;ENEMY_C01_UNMARKED_WHITE_SAMPLER
- **chapter**：C01
- **episode**：1-4
- **kind**：carrier_air_battle
- **location**：万机馆巡展舰/舰首/城市外海空域
- **next_scene**：V359-C02E01-CREATIVE
- **notes**：万机馆恢复巡展舰身体，以有限防卫炮和真实巡展装备参加空战；馆守Z装上非拳击型巡展臂装，从舰首出击并以左拳击毁飞行核心；第七次巡展启动。纪存、唐胶、兜灯、跌跌和机器犬随舰，陆衡未登场，豪司与勇拳被企业回收，七海留城受调查；木桶街因旧泊位和全尺寸改件成为下一站。
- **optional_entities**：CH_QIHAI;V353U038;V353U040;ENEMY_C01_UNMARKED_WHITE_SAMPLER
- **required_entities**：CH_JICUN;CH001;CH002;CH_TANGJIAO;CH036;MECHA_BRAVE_FIST_PROTOTYPE;V353U001;MECHA_GUARDIAN_TOURING_ARM;MECHA_WANJI_MOBILE_CHASSIS;ENEMY_C01_BREAKER
- **scene_id**：V355-C01E04
- **source_refs**：docs/superpowers/specs/剧情梗概/V35全剧结构母盘-候选v1-2026-07-20.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-章级对齐卡.md
- **title**：博物馆追上天空
- **unlocks**：BREAKER_DESTROYED;WANJI_SEVENTH_TOUR_ACTIVE;GZ_TOURING_ARM_STATE;ROUTE_MODEL_STREET_FIRST_STOP;WHITE_SAMPLER_GAINS_RIGHT_FIST_FRAGMENT
- **显式关系**：
  - 必须在场 -> `entity:CH_JICUN` 纪存
  - 必须在场 -> `entity:CH001` 兜灯
  - 必须在场 -> `entity:CH002` 旧守护者
  - 必须在场 -> `entity:CH_TANGJIAO` 唐胶
  - 必须在场 -> `entity:CH036` 豪司
  - 必须在场 -> `entity:MECHA_BRAVE_FIST_PROTOTYPE` 勇拳试作机
  - 必须在场 -> `entity:V353U001` 馆守Z
  - 必须在场 -> `entity:MECHA_GUARDIAN_TOURING_ARM` 馆守Z巡展臂装
  - 必须在场 -> `entity:MECHA_WANJI_MOBILE_CHASSIS` 万机馆巡展舰体
  - 必须在场 -> `entity:ENEMY_C01_BREAKER` 裂星潮突入体BREAKER
  - 可选在场 -> `entity:CH_QIHAI` 七海
  - 可选在场 -> `entity:V353U038` 跌跌
  - 可选在场 -> `entity:V353U040` 机器犬
  - 可选在场 -> `entity:ENEMY_C01_UNMARKED_WHITE_SAMPLER` 无标志白色采样机
  - 允许新增 -> `entity:MECHA_GUARDIAN_TOURING_ARM` 馆守Z巡展臂装
  - 允许新增 -> `entity:MECHA_WANJI_MOBILE_CHASSIS` 万机馆巡展舰体
  - 允许新增 -> `entity:ENEMY_C01_UNMARKED_WHITE_SAMPLER` 无标志白色采样机

## C25 最后一场导览

- 节点：`scene:V355-C01E01`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md`
- 命中：`bm25`
- 分数：`457.1344`

- **allowed_new_entities**：ENEMY_C01_BREAKER
- **chapter**：C01
- **episode**：1-1
- **kind**：adv_exploration_hook
- **location**：万机馆开放层短导览路线/模型病院/中庭
- **next_scene**：V355-C01E02
- **notes**：当前只锁故事事实：三十多名观众参加最后导览；旧照片预告第六次巡展；馆守Z、模型病院、巡展装备与未开放展区建立万机馆厚度；豪司通过公开测试正式登场；纪存与七海的晚饭被BREAKER警报打断。
- **optional_entities**：ENEMY_C01_BREAKER
- **required_entities**：CH_JICUN;CH002;CH_TANGJIAO;CH001;CH_QIHAI;CH036;MECHA_BRAVE_FIST_PROTOTYPE;V353U001;V353U038;V353U040;CH_XIAOMAN;CH_ACHENG
- **scene_id**：V355-C01E01
- **source_refs**：docs/superpowers/specs/剧情梗概/V35全剧结构母盘-候选v1-2026-07-20.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-章级对齐卡.md
- **title**：最后一场导览
- **unlocks**：C01_LAST_TOUR_COMPLETE;C01_DINNER_INTERRUPTED;BREAKER_APPROACHES
- **显式关系**：
  - 必须在场 -> `entity:CH_JICUN` 纪存
  - 必须在场 -> `entity:CH002` 旧守护者
  - 必须在场 -> `entity:CH_TANGJIAO` 唐胶
  - 必须在场 -> `entity:CH001` 兜灯
  - 必须在场 -> `entity:CH_QIHAI` 七海
  - 必须在场 -> `entity:CH036` 豪司
  - 必须在场 -> `entity:MECHA_BRAVE_FIST_PROTOTYPE` 勇拳试作机
  - 必须在场 -> `entity:V353U001` 馆守Z
  - 必须在场 -> `entity:V353U038` 跌跌
  - 必须在场 -> `entity:V353U040` 机器犬
  - 必须在场 -> `entity:CH_XIAOMAN` 小满
  - 可选在场 -> `entity:ENEMY_C01_BREAKER` 裂星潮突入体BREAKER
  - 允许新增 -> `entity:ENEMY_C01_BREAKER` 裂星潮突入体BREAKER
  - 后续场景 -> `scene:V355-C01E02` 巨神从展台起身

## C26 巨神从展台起身

- 节点：`scene:V355-C01E02`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md`
- 命中：`bm25`
- 分数：`451.5621`

- **allowed_new_entities**：V353U034
- **chapter**：C01
- **episode**：1-2
- **kind**：evacuation_giant_battle
- **location**：万机馆开放层/东侧货运坡道/旧会展广场
- **next_scene**：V355-C01E03
- **notes**：三十多名观众全部撤出；旧守护者从轮式导览终端转由馆守Z胸前扬声器继续发言，玩家确认同一主体；七海只撤回本人停机令并进入调查；纪存进入导览席提供路线判断；馆守Z扯下退役重盾，首次正面挡住BREAKER。
- **optional_entities**：CH_XIAOMAN;CH_ACHENG
- **required_entities**：CH_JICUN;CH_QIHAI;CH_TANGJIAO;CH001;CH002;V353U038;V353U040;V353U034;V353U001;ENEMY_C01_BREAKER
- **scene_id**：V355-C01E02
- **source_refs**：docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-章级对齐卡.md
- **title**：巨神从展台起身
- **unlocks**：C01_VISITORS_EVACUATED;QH_WITHDRAWS_OWN_STOP_ORDER;GUARDIAN_Z_FIRST_CONTROL
- **显式关系**：
  - 必须在场 -> `entity:CH_JICUN` 纪存
  - 必须在场 -> `entity:CH_QIHAI` 七海
  - 必须在场 -> `entity:CH_TANGJIAO` 唐胶
  - 必须在场 -> `entity:CH001` 兜灯
  - 必须在场 -> `entity:CH002` 旧守护者
  - 必须在场 -> `entity:V353U038` 跌跌
  - 必须在场 -> `entity:V353U040` 机器犬
  - 必须在场 -> `entity:V353U034` 消防架桥机
  - 必须在场 -> `entity:V353U001` 馆守Z
  - 必须在场 -> `entity:ENEMY_C01_BREAKER` 裂星潮突入体BREAKER
  - 可选在场 -> `entity:CH_XIAOMAN` 小满
  - 允许新增 -> `entity:V353U034` 消防架桥机
  - 后续场景 -> `scene:V355-C01E03` 双拳打碎外壳

## C27 裂星潮突入体BREAKER

- 节点：`entity:ENEMY_C01_BREAKER`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`bm25`
- 分数：`435.6039`

- **aliases**：BREAKER;破城者;裂星潮突入体
- **canonical_name**：裂星潮突入体BREAKER
- **entity_id**：ENEMY_C01_BREAKER
- **first_battle_join**：V355-C01E02
- **first_foreshadow**：V355-C01E01
- **first_formal_appearance**：V355-C01E01
- **implementation_policy**：地面阶段为近30米黑甲突入壳，能钻地、冲撞与发射赤红冲击；外壳被双拳击穿后露出十余米核心与近50米薄翼，能高速飞行并以脉冲指挥小型突入体。两阶段共用同一主体，不是两只敌人。它会忽略更近的火力与能源站转向万机馆，但本章不解释原因。
- **notes**：正式编号与裂星潮序列待外敌命名协议后补；BREAKER是城市作战呼号。外观先保证地面重甲与飞行核心一眼可辨。
- **role**：C01突破近海防线并追逐万机馆的两阶段外敌
- **source_group_id**：EXTERNAL_RIFT_SWARM
- **status**：working_current
- **type**：enemy_unit
- **显式关系**：
  - 首次伏笔 -> `scene:V355-C01E01` 最后一场导览
  - 正式登场 -> `scene:V355-C01E01` 最后一场导览
  - 首次战斗加入 -> `scene:V355-C01E02` 巨神从展台起身

## C28 双拳打碎外壳

- 节点：`scene:V355-C01E03`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md`
- 命中：`bm25`
- 分数：`413.4297`

- **allowed_new_entities**：MECHA_BRAVE_FIST_PROTOTYPE
- **chapter**：C01
- **episode**：1-3
- **kind**：giant_boss_phase_change
- **location**：旧会展广场/勇气测试场/断裂高架
- **next_scene**：V355-C01E04
- **notes**：豪司越过企业撤离令驾驶勇拳参战；勇拳储存冲击并补在馆守Z火箭右拳尾部，两机击穿BREAKER地面甲壳；馆守Z右臂回收机构过载毁损；飞行核心与增援显形，万机馆地下巡展舰体开始回应。
- **optional_entities**：CH_QIHAI;CH001
- **required_entities**：CH_JICUN;CH002;CH036;MECHA_BRAVE_FIST_PROTOTYPE;V353U001;ENEMY_C01_BREAKER
- **scene_id**：V355-C01E03
- **source_refs**：docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-完整剧情总纲.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C01/C01-章级对齐卡.md
- **title**：双拳打碎外壳
- **unlocks**：GZ_RIGHT_ARM_DESTROYED;HAOSI_CORP_CONSEQUENCE;BREAKER_CORE_REVEALED;WANJI_CARRIER_RESPONDS
- **显式关系**：
  - 必须在场 -> `entity:CH_JICUN` 纪存
  - 必须在场 -> `entity:CH002` 旧守护者
  - 必须在场 -> `entity:CH036` 豪司
  - 必须在场 -> `entity:MECHA_BRAVE_FIST_PROTOTYPE` 勇拳试作机
  - 必须在场 -> `entity:V353U001` 馆守Z
  - 必须在场 -> `entity:ENEMY_C01_BREAKER` 裂星潮突入体BREAKER
  - 可选在场 -> `entity:CH_QIHAI` 七海
  - 可选在场 -> `entity:CH001` 兜灯
  - 允许新增 -> `entity:MECHA_BRAVE_FIST_PROTOTYPE` 勇拳试作机
  - 后续场景 -> `scene:V355-C01E04` 博物馆追上天空

## C29 无标志白色采样机

- 节点：`entity:ENEMY_C01_UNMARKED_WHITE_SAMPLER`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`bm25`
- 分数：`314.1194`

- **aliases**：白色采样机;无标采样机;右拳残片采样机
- **canonical_name**：无标志白色采样机
- **entity_id**：ENEMY_C01_UNMARKED_WHITE_SAMPLER
- **first_foreshadow**：V355-C01E04
- **first_formal_appearance**：V355-C01E04
- **implementation_policy**：只在战后废墟短暂出现，以腹部收纳舱取走一块右拳残片后离开；不与主角交战、不说话、不揭示所属机构。它证明有人在系统性回收机体身体与战斗样本，但不等于索引人格或代哥命令。
- **notes**：C02以后若追踪该样本，必须说明具体机构、物流和分析身体；C01只保留无名钩子。
- **role**：C01尾声回收馆守Z右拳残片的白框生态前台身体
- **source_group_id**：WHITEFRAME
- **status**：working_current
- **type**：enemy_unit
- **显式关系**：
  - 首次伏笔 -> `scene:V355-C01E04` 博物馆追上天空
  - 正式登场 -> `scene:V355-C01E04` 博物馆追上天空

## C30 第一座可以回来的城

- 节点：`scene:V359-C03E04-CREATIVE`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C03四话结构复原与Current-Canon迁移-2026-07-26.md`
- 命中：`bm25`
- 分数：`269.9084`

- **allowed_new_entities**：V353U050;HUNDRED_MECHA_ROUTE_INVITATION
- **chapter**：C03
- **episode**：3-4
- **kind**：creative_working_calibration_life_and_route_launch
- **location**：工务城公共泊位/车站/万机馆厨房与B1通信席
- **next_scene**：V359-C04E01-CREATIVE
- **notes**：转子完成低速校正，工务城成为可回访公共泊位；社勇王、工务城与企业确认三个月公共道路试用，企业保留产权、维护与到期复核；七海放弃本轮复职审查并以天空铸环航段共同监督身份登舰；白鸢继续留舰；纪存发出百机航路邀请。方舟探测器只转发同一白舰的当前求援和二十七年前旧包，不等于方舟T完整人格。
- **optional_entities**：V353U031;V353U032;V353U033;V353U034;V353U039;V353U041;V353U049
- **required_entities**：CH_JICUN;CH_QIHAI;N_BAIYUAN;CH_LUHENG;CH036;CH_TANGJIAO;CH001;V353U001;V353U024;V353U043;V353U048;V353U071;V353U038;V353U040;V353U050;HUNDRED_MECHA_ROUTE_INVITATION;LOC_PUBLIC_WORKS_CITY
- **scene_id**：V359-C03E04-CREATIVE
- **source_refs**：docs/superpowers/specs/剧情梗概/V35全剧结构母盘-候选v1-2026-07-20.md;docs/superpowers/specs/剧情梗概/V35-C03四话结构复原与Current-Canon迁移-2026-07-26.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C03/C03-完整剧情总纲.md
- **title**：第一座可以回来的城
- **unlocks**：SOCIAL_BRAVE_THREE_MONTH_TRIAL;SOCIAL_BRAVE_LONG_TERM_PLAYABLE;WANJI_LOW_SPEED_CALIBRATED;PUBLIC_WORKS_CITY_HOME_PORT;PUBLIC_WORKS_CROSS_CITY_SUPPORT;QH_ONBOARD_AS_JOINT_SUPERVISOR;BAYUAN_TEMPORARY_PASSENGER_EXTENDED;HUNDRED_MECHA_ROUTE_INVITATION_SENT;ROUTE_SKY_FOUNDRY
- **显式关系**：
  - 必须在场 -> `entity:CH_JICUN` 纪存
  - 必须在场 -> `entity:CH_QIHAI` 七海
  - 必须在场 -> `entity:N_BAIYUAN` 白鸢
  - 必须在场 -> `entity:CH_LUHENG` 陆衡
  - 必须在场 -> `entity:CH036` 豪司
  - 必须在场 -> `entity:CH_TANGJIAO` 唐胶
  - 必须在场 -> `entity:CH001` 兜灯
  - 必须在场 -> `entity:V353U001` 馆守Z
  - 必须在场 -> `entity:V353U024` 社勇王
  - 必须在场 -> `entity:V353U043` 火种货柜领袖
  - 必须在场 -> `entity:V353U048` 旧拳王机
  - 必须在场 -> `entity:V353U071` 玩家模型机“无牌一号”
  - 必须在场 -> `entity:V353U038` 跌跌
  - 必须在场 -> `entity:V353U040` 机器犬
  - 必须在场 -> `entity:V353U050` 方舟折叠探测器
  - 必须在场 -> `entity:HUNDRED_MECHA_ROUTE_INVITATION` 百机航路邀请
  - 必须在场 -> `entity:LOC_PUBLIC_WORKS_CITY` 工务城
  - 可选在场 -> `entity:V353U031` 市政吊装机
  - 可选在场 -> `entity:V353U032` 预算二号救援机
  - 可选在场 -> `entity:V353U033` 灰崎警备劳务机
  - 可选在场 -> `entity:V353U034` 消防架桥机
  - 可选在场 -> `entity:V353U039` 乐森偶
  - 可选在场 -> `entity:V353U041` 积木智者
  - 可选在场 -> `entity:V353U049` 影子陪练机
  - 允许新增 -> `entity:V353U050` 方舟折叠探测器
  - 允许新增 -> `entity:HUNDRED_MECHA_ROUTE_INVITATION` 百机航路邀请

## C31 社勇王，现场合体

- 节点：`scene:V359-C03E03-CREATIVE`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C03四话结构复原与Current-Canon迁移-2026-07-26.md`
- 命中：`bm25`
- 分数：`248.3505`

- **allowed_new_entities**：V353U024;SOCIAL_BRAVE_AI_REFUSAL
- **chapter**：C03
- **episode**：3-3
- **kind**：creative_working_brave_boss_battle
- **location**：工务城中央坞环与西环承重区
- **next_scene**：V359-C03E04-CREATIVE
- **notes**：当前只锁战斗事实：社勇王选择豪司并完成完整合体，首锤正面击裂衡令工具冠；住宅承载条件改变后，机体拒绝第二锤，豪司撤回命令并继续并肩；城梁一号横移到新承点；衡令失去工具冠、外甲和城市接口，只带原有受损旧核与战场观测撤离，没有取得新实体样本。
- **optional_entities**：V353U038;V353U040;V353U071;V353U039;V353U041
- **required_entities**：CH_JICUN;CH_QIHAI;N_BAIYUAN;CH_LUHENG;CH036;CH_TANGJIAO;CH001;V353U001;V353U024;V353U031;V353U032;V353U033;V353U034;MECHA_C03_CITY_BEAM_GIANT;ENEMY_C03_REQUISITION_RIG_HENGLING;SOCIAL_BRAVE_AI_REFUSAL;LOC_PUBLIC_WORKS_CITY
- **scene_id**：V359-C03E03-CREATIVE
- **source_refs**：docs/superpowers/specs/剧情梗概/V35全剧结构母盘-候选v1-2026-07-20.md;docs/superpowers/specs/剧情梗概/V35-C03四话结构复原与Current-Canon迁移-2026-07-26.md;docs/superpowers/specs/剧情梗概/V35第四层逐章完整总纲/C03/C03-完整剧情总纲.md
- **title**：社勇王，现场合体
- **unlocks**：SOCIAL_BRAVE_FIRST_FULL_COMBINE;HAOSI_PRIMARY_PILOT_WITH_AI_REFUSAL;CITY_BEAM_GIANT_RELOCATED;HENGLING_WITHDRAWS_DAMAGED
- **显式关系**：
  - 必须在场 -> `entity:CH_JICUN` 纪存
  - 必须在场 -> `entity:CH_QIHAI` 七海
  - 必须在场 -> `entity:N_BAIYUAN` 白鸢
  - 必须在场 -> `entity:CH_LUHENG` 陆衡
  - 必须在场 -> `entity:CH036` 豪司
  - 必须在场 -> `entity:CH_TANGJIAO` 唐胶
  - 必须在场 -> `entity:CH001` 兜灯
  - 必须在场 -> `entity:V353U001` 馆守Z
  - 必须在场 -> `entity:V353U024` 社勇王
  - 必须在场 -> `entity:V353U031` 市政吊装机
  - 必须在场 -> `entity:V353U032` 预算二号救援机
  - 必须在场 -> `entity:V353U033` 灰崎警备劳务机
  - 必须在场 -> `entity:V353U034` 消防架桥机
  - 必须在场 -> `entity:MECHA_C03_CITY_BEAM_GIANT` 市政承梁机“城梁一号”
  - 必须在场 -> `entity:ENEMY_C03_REQUISITION_RIG_HENGLING` 征用裁装机“衡令”
  - 必须在场 -> `entity:SOCIAL_BRAVE_AI_REFUSAL` 社勇王AI拒绝关系
  - 必须在场 -> `entity:LOC_PUBLIC_WORKS_CITY` 工务城
  - 可选在场 -> `entity:V353U038` 跌跌
  - 可选在场 -> `entity:V353U040` 机器犬
  - 可选在场 -> `entity:V353U071` 玩家模型机“无牌一号”
  - 可选在场 -> `entity:V353U039` 乐森偶
  - 可选在场 -> `entity:V353U041` 积木智者
  - 允许新增 -> `entity:V353U024` 社勇王
  - 允许新增 -> `entity:SOCIAL_BRAVE_AI_REFUSAL` 社勇王AI拒绝关系
  - 后续场景 -> `scene:V359-C03E04-CREATIVE` 第一座可以回来的城

## C32 整座城压上来

- 节点：`scene:V359-C03E01-CREATIVE`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/scenes.tsv`
- 命中：`bm25`
- 分数：`241.0685`

- **allowed_new_entities**：V353U039;V353U041;MECHA_C03_CITY_BEAM_GIANT;ENEMY_C03_REQUISITION_RIG_HENGLING;LOC_PUBLIC_WORKS_CITY
- **chapter**：C03
- **episode**：3-1
- **kind**：creative_working_city_conflict
- **location**：工务城外环与万机馆泊位区
- **next_scene**：V359-C03E02-CREATIVE
- **notes**：当前只锁故事事实：市政最初把万机馆视为风险源；衡令同时夺取城市工务机后，本地工班与万机馆建立临时共同战线；七海实体到场担任风险调查方。承重槽、索缆和初战动作由C03 L4重建。
- **optional_entities**：V353U038;V353U040;V353U031;V353U032;V353U033
- **required_entities**：CH_JICUN;CH_QIHAI;N_BAIYUAN;CH_LUHENG;CH_TANGJIAO;CH001;MECHA_WANJI_MOBILE_CHASSIS;MECHA_C03_CITY_BEAM_GIANT;ENEMY_C03_REQUISITION_RIG_HENGLING;LOC_PUBLIC_WORKS_CITY
- **scene_id**：V359-C03E01-CREATIVE
- **source_refs**：docs/superpowers/specs/剧情梗概/V35全剧结构母盘-候选v1-2026-07-20.md;docs/superpowers/specs/剧情梗概/V35-L1-L3到Current-Canon收敛迁移-2026-07-24.md
- **title**：整座城压上来
- **unlocks**：QH_ONSITE_WITNESS;CITY_AND_WANJI_TEMP_ALLIANCE;HENGLING_REQUISITION_EXPOSED
- **显式关系**：
  - 必须在场 -> `entity:CH_JICUN` 纪存
  - 必须在场 -> `entity:CH_QIHAI` 七海
  - 必须在场 -> `entity:N_BAIYUAN` 白鸢
  - 必须在场 -> `entity:CH_LUHENG` 陆衡
  - 必须在场 -> `entity:CH_TANGJIAO` 唐胶
  - 必须在场 -> `entity:CH001` 兜灯
  - 必须在场 -> `entity:MECHA_WANJI_MOBILE_CHASSIS` 万机馆巡展舰体
  - 必须在场 -> `entity:MECHA_C03_CITY_BEAM_GIANT` 市政承梁机“城梁一号”
  - 必须在场 -> `entity:ENEMY_C03_REQUISITION_RIG_HENGLING` 征用裁装机“衡令”
  - 必须在场 -> `entity:LOC_PUBLIC_WORKS_CITY` 工务城
  - 可选在场 -> `entity:V353U038` 跌跌
  - 可选在场 -> `entity:V353U040` 机器犬
  - 可选在场 -> `entity:V353U031` 市政吊装机
  - 可选在场 -> `entity:V353U032` 预算二号救援机
  - 可选在场 -> `entity:V353U033` 灰崎警备劳务机
  - 允许新增 -> `entity:V353U039` 乐森偶
  - 允许新增 -> `entity:V353U041` 积木智者
  - 允许新增 -> `entity:MECHA_C03_CITY_BEAM_GIANT` 市政承梁机“城梁一号”
  - 允许新增 -> `entity:ENEMY_C03_REQUISITION_RIG_HENGLING` 征用裁装机“衡令”
  - 允许新增 -> `entity:LOC_PUBLIC_WORKS_CITY` 工务城
  - 后续场景 -> `scene:V359-C03E02-CREATIVE` 城市的手不是零件

## C33 勇拳试作机

- 节点：`entity:MECHA_BRAVE_FIST_PROTOTYPE`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`bm25`
- 分数：`237.1675`

- **aliases**：勇拳测试壳;豪司试作救援机
- **canonical_name**：勇拳试作机
- **entity_id**：MECHA_BRAVE_FIST_PROTOTYPE
- **first_battle_join**：V355-C01E03
- **first_foreshadow**：V355-C01E01
- **first_formal_appearance**：V355-C01E01
- **implementation_policy**：E01公开直播展示拳甲承受冲击后整量回送的核心能力；E02不参战；E03豪司越过企业撤离令驾驶它加入战斗，以高机动连续打击限制BREAKER，并把已储存冲击补在馆守Z飞拳尾部。E04协助空战后由企业回收。C03社勇王不是本机升级或换皮。
- **notes**：用于让豪司从操纵无机魂试作机升级为与会拒绝自己的勇者AI结伴；不得作为长期常驻机重复计数。
- **role**：C01豪司驾驶的有人试验机，使用社勇王同系列工程骨架但没有独立机魂
- **source_group_id**：PK_CORE_BRAVE_CO
- **status**：working_current
- **type**：mecha
- **显式关系**：
  - 首次伏笔 -> `scene:V355-C01E01` 最后一场导览
  - 正式登场 -> `scene:V355-C01E01` 最后一场导览
  - 首次战斗加入 -> `scene:V355-C01E03` 双拳打碎外壳

## C34 馆守Z

- 节点：`art_lock:CML008`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv`
- 命中：`bm25`
- 分数：`234.6677`

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

## C35 馆守Z巡展臂装

- 节点：`entity:MECHA_GUARDIAN_TOURING_ARM`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35-C01用户审定故事回迁与Canon收敛-2026-07-26.md`
- 命中：`bm25`
- 分数：`232.4801`

- **aliases**：巡展臂装;救援锚臂;临时右臂
- **canonical_name**：馆守Z巡展臂装
- **entity_id**：MECHA_GUARDIAN_TOURING_ARM
- **first_battle_join**：V355-C01E04
- **first_foreshadow**：V355-C01E01
- **first_formal_appearance**：V355-C01E04
- **implementation_policy**：接在馆守Z右肩残存固定口，只能抓握、放锚、牵引、固定和投放装备；不能握拳、精密操作、发射火箭拳或表现成完整新右臂。E04钉住BREAKER侧翼并帮助馆守Z回舰。
- **notes**：后续可在木桶街换装不同工作手，但真正后继右臂必须另建机体形态和剧情。
- **role**：C01E04由万机馆旧救援锚改成的临时右侧装备
- **source_group_id**：V353U001
- **status**：working_current
- **type**：mecha_component
- **显式关系**：
  - 来源组 -> `entity:V353U001` 馆守Z
  - 首次伏笔 -> `scene:V355-C01E01` 最后一场导览
  - 正式登场 -> `scene:V355-C01E04` 博物馆追上天空
  - 首次战斗加入 -> `scene:V355-C01E04` 博物馆追上天空

## C36 城市的手不是零件

- 节点：`scene:V359-C03E02-CREATIVE`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/scenes.tsv`
- 命中：`bm25`
- 分数：`212.1092`

- **allowed_new_entities**：V353U031;V353U032;V353U033;V353U034
- **chapter**：C03
- **episode**：3-2
- **kind**：creative_working_public_works_chase
- **location**：工务城道路、环轨与旧舰骨
- **next_scene**：V359-C03E03-CREATIVE
- **notes**：当前只锁故事事实：预算二号、市政吊装机、灰崎警备机与带旧伤的消防架桥机夺回工作能力；陆衡承认旧程序责任并失去跨城资质；白鸢的路线由地方驾驶员修改后共同署名。关节算法、地形动作和追击层数由C03 L4重建。
- **optional_entities**：V353U039;V353U041;V353U043;V353U048
- **required_entities**：CH_JICUN;CH_QIHAI;N_BAIYUAN;CH_LUHENG;CH_TANGJIAO;CH001;V353U031;V353U032;V353U033;V353U034;V353U038;V353U040;MECHA_C03_CITY_BEAM_GIANT;ENEMY_C03_REQUISITION_RIG_HENGLING
- **scene_id**：V359-C03E02-CREATIVE
- **source_refs**：docs/superpowers/specs/剧情梗概/V35全剧结构母盘-候选v1-2026-07-20.md;docs/superpowers/specs/剧情梗概/V35-L1-L3到Current-Canon收敛迁移-2026-07-24.md
- **title**：城市的手不是零件
- **unlocks**：PUBLIC_WORKS_FOUR_FIRST_CONTROL;LUHENG_OLD_CERT_SUSPENDED;BAYUAN_COAUTHORED_PREVIS
- **显式关系**：
  - 必须在场 -> `entity:CH_JICUN` 纪存
  - 必须在场 -> `entity:CH_QIHAI` 七海
  - 必须在场 -> `entity:N_BAIYUAN` 白鸢
  - 必须在场 -> `entity:CH_LUHENG` 陆衡
  - 必须在场 -> `entity:CH_TANGJIAO` 唐胶
  - 必须在场 -> `entity:CH001` 兜灯
  - 必须在场 -> `entity:V353U031` 市政吊装机
  - 必须在场 -> `entity:V353U032` 预算二号救援机
  - 必须在场 -> `entity:V353U033` 灰崎警备劳务机
  - 必须在场 -> `entity:V353U034` 消防架桥机
  - 必须在场 -> `entity:V353U038` 跌跌
  - 必须在场 -> `entity:V353U040` 机器犬
  - 必须在场 -> `entity:MECHA_C03_CITY_BEAM_GIANT` 市政承梁机“城梁一号”
  - 必须在场 -> `entity:ENEMY_C03_REQUISITION_RIG_HENGLING` 征用裁装机“衡令”
  - 可选在场 -> `entity:V353U039` 乐森偶
  - 可选在场 -> `entity:V353U041` 积木智者
  - 可选在场 -> `entity:V353U043` 火种货柜领袖
  - 可选在场 -> `entity:V353U048` 旧拳王机
  - 允许新增 -> `entity:V353U031` 市政吊装机
  - 允许新增 -> `entity:V353U032` 预算二号救援机
  - 允许新增 -> `entity:V353U033` 灰崎警备劳务机
  - 允许新增 -> `entity:V353U034` 消防架桥机
  - 后续场景 -> `scene:V359-C03E03-CREATIVE` 社勇王，现场合体

## C37 钢拳擂台

- 节点：`entity:R22`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`bm25`
- 分数：`209.9108`

- **aliases**：旧拳王;拳击机器人;非致命擂台
- **canonical_name**：钢拳擂台
- **entity_id**：R22
- **first_battle_join**：V359-C02E03-CREATIVE
- **first_foreshadow**：C01E01-MAIN-COMBO_TABLE
- **first_formal_appearance**：V359-C02E03-CREATIVE
- **implementation_policy**：C02以完整旧拳王机体和机械擂台建立非致命战斗；右拳护具只能作为模型锚、规则钥匙或改装件，不能冒充参战机体。旧拳王通关后正式加入，完整支线留待后续生命周期展开。
- **notes**：用于把机器人拳击、失败记录和父子式修复情感带入可长期使用的机体，而不是只给一只手套参战。
- **role**：非致命战、失败与修复尊严谱系
- **source_group_id**：R22
- **status**：core
- **type**：roster_package

## C38 工务城

- 节点：`entity:LOC_PUBLIC_WORKS_CITY`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`bm25`
- 分数：`208.8567`

- **aliases**：环形工务城;公共巨构港;万机馆第一归港
- **canonical_name**：工务城
- **entity_id**：LOC_PUBLIC_WORKS_CITY
- **first_battle_join**：V359-C03E01-CREATIVE
- **first_foreshadow**：V359-C02E03-CREATIVE
- **first_formal_appearance**：V359-C03E01-CREATIVE
- **implementation_policy**：上环为可移动城区，中层为工务环轨，下层为旧巡展舰骨；C03结束后提供安全外泊、低速校正和有限事故支持，但不免费修复全部损伤。具体道路翻转、追击路线和泊位结构由C03预生产确定。
- **notes**：工务城不是代哥分部或单一反派城市；其连续运行系统真实救过人，也会把无主、无保险和难分类身体优先当作可征用部件。
- **role**：建立在灾前巡展舰骨上的三层移动城市，也是万机馆第一座可返回公共泊位
- **source_group_id**：PK_CORE_PUBLIC_WORKS
- **status**：needs_review
- **type**：location
- **显式关系**：
  - 正式登场 -> `scene:V359-C03E01-CREATIVE` 整座城压上来
  - 首次战斗加入 -> `scene:V359-C03E01-CREATIVE` 整座城压上来

## C39 社勇王

- 节点：`entity:V353U024`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`bm25`
- 分数：`208.0950`

- **aliases**：全尺寸社勇王;勇者救援实机
- **canonical_name**：社勇王
- **entity_id**：V353U024
- **first_battle_join**：V359-C03E03-CREATIVE
- **first_foreshadow**：V355-C01E01
- **first_formal_appearance**：V359-C03E03-CREATIVE
- **implementation_policy**：全尺寸实机；模型盒和说明书只作锚件。C03由豪司与机体主体AI完成首次正式并肩，AI在战局变化后第一次拒绝驾驶员，双方重新协调并赢下战斗；E04由机体、工务城与企业确认三个月公共道路试用，企业保留产权、维护义务与到期复核。玩家可长期操作不等于万机馆永久所有。
- **notes**：当前说话者为社勇王机体主体AI，不提前启用CH037金章独立人格；内部锚Brave/GaoGaiGar式AI伙伴与工具浪漫。
- **role**：C03以后勇者救援主力，承担完整合体、巨大工具、主体选择和AI拒绝
- **source_group_id**：PK_CORE_BRAVE_CO
- **status**：needs_review
- **type**：mecha
- **显式关系**：
  - 首次伏笔 -> `scene:V355-C01E01` 最后一场导览
  - 正式登场 -> `scene:V359-C03E03-CREATIVE` 社勇王，现场合体
  - 首次战斗加入 -> `scene:V359-C03E03-CREATIVE` 社勇王，现场合体

## C40 第一章闭馆路线

- 节点：`terminal_view:JTV_C01_CLOSING_ROUTE`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/jicun_archive_terminal_views.tsv`
- 命中：`bm25`
- 分数：`198.7110`

- **display_name**：第一章闭馆路线
- **first_scene**：V355-C01E01
- **map_expression**：唯一六站路线依次显示前厅总图、馆守Z基座、合体台与模型病院、现实机器舞台、旧影像厅、档案室;跨层视点与馆外工务屏为两个连续观察点;前厅用社勇王取件屏、跌跌演示屏和外部锁泊灰显建立万机感
- **notes**：这个视图替代“纪存拿笔记本记路线”的低科技表达；Current只锁信息结构和六站样本，不锁旧Runtime。
- **player_use**：给玩家明确“现在只是在闭馆巡检”，并把小满、阿澄移动原因、六站顺序和火灾后的行动转折压实
- **source_tables**：wanji_locations.tsv;wanji_exhibition_zones.tsv;V35-L1-L3到Current-Canon收敛迁移-2026-07-24.md
- **ui_mode**：route
- **view_id**：JTV_C01_CLOSING_ROUTE
- **visual_anchor**：六站路线灯点;巡检勾选;闭馆广播时间戳;两个连续视点;事故状态叠层
- **writing_rule**：第一章探索不得写成孩子默认跟队游览，也不得恢复A/B/C并排路线；六站只是一座十九区大馆的闭馆样本，火灾后切入的小机行动形式、回合数和敌军由C01 L4决定
- **显式关系**：
  - 首次场景 -> `scene:V355-C01E01` 最后一场导览

## C41 七海 / 佐伯七海

- 节点：`art_lock:CML004`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv`
- 命中：`bm25`
- 分数：`194.6291`

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

## C42 铁馆魔神

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

## C43 战前对话

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
  - 首次允许场景 -> `scene:V355-C01E03` 双拳打碎外壳

## C44 deprecated_alias_of · MECHA_GUARDIAN_Z · V353U001

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

## C45 纪存 / 玩家名

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

## C46 纪存的被弃回应起源

- 节点：`entity:CONCEPT_JICUN_DISCARDED_RESPONSE_ORIGIN`
- 权威：`working`
- 来源：`docs/superpowers/specs/剧情梗概/V35世界机制与创作接口设定基线-2026-07-19.md`
- 命中：`graph_1hop_from:entity:CH_JICUN:被来源组`
- 分数：`0.0000`

- **aliases**：被删回应;空白展柜回应;未归类机魂汇聚
- **canonical_name**：纪存的被弃回应起源
- **entity_id**：CONCEPT_JICUN_DISCARDED_RESPONSE_ORIGIN
- **first_foreshadow**：C01-COLD-OPEN
- **first_formal_appearance**：SYSTEM-DESIGN
- **implementation_policy**：纪存不是死者拼盘、统一蜂群或索引善良半身；他拥有新的主体连续性。具体参与片段、旧馆长作用和人形载体来历保持OPEN。
- **notes**：他的主角成长是从被丢弃的答案中醒来，学会用智慧与力量保护差异，同时主动限制自己替所有人解释的能力。
- **role**：万机馆离线保全层锚住二十七年前被统一回应拒绝、被清噪、互相矛盾或无法归类的主体响应，这些响应在长期路由中诞生了纪存这个新的人
- **source_group_id**：CH_JICUN
- **status**：working_current
- **type**：concept
- **显式关系**：
  - 来源组 -> `entity:CH_JICUN` 纪存

## C47 生活温度

- 节点：`gag_hook:GH059`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/gag_hooks.tsv`
- 命中：`graph_1hop_from:entity:CH_JICUN:被相关主体`
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
  - 首次允许场景 -> `scene:V359-C03E03-CREATIVE` 社勇王，现场合体

## C48 巡展舰体与外泊层

- 节点：`entity:LOC_WANJI_MOBILE_CHASSIS`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`graph_1hop_from:entity:MECHA_WANJI_MOBILE_CHASSIS:来源组`
- 分数：`0.0000`

- **aliases**：地下旧舰体;巡展舰体;舰底;外部锁泊
- **canonical_name**：巡展舰体与外泊层
- **entity_id**：LOC_WANJI_MOBILE_CHASSIS
- **first_foreshadow**：V355-C01E03
- **first_formal_appearance**：V355-C01E04
- **implementation_policy**：E03只以地下旧舰轮廓、应急灯和回应预显影；E04整体离地并进入外海战场。首章只需舰桥、主展厅、舰首装备位、外部锁泊与整体轮廓，不建立四岗位闯关、载荷二选一或复杂内部变形。
- **notes**：属于万机馆原有巡展舰身体，不是临时长出的新底盘；容量边界继续读取wanji_carrier_berths.tsv，后续现代泊位兼容由C02处理。
- **role**：万机馆由固定展馆恢复巡展舰身体的空间
- **source_group_id**：MUSEUM
- **status**：core
- **type**：location
- **显式关系**：
  - 首次伏笔 -> `scene:V355-C01E03` 双拳打碎外壳
  - 正式登场 -> `scene:V355-C01E04` 博物馆追上天空

## C49 代哥品牌资产秩序生态

- 节点：`entity:ORG_DAIGE`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/entities.tsv`
- 命中：`graph_1hop_from:entity:CH_QIHAI:来源组`
- 分数：`0.0000`

- **aliases**：代哥法务部;代哥清算部;第七档案室;安全封存局;限定流通局;商品化谱系局;数字运营局;IP价值战略室
- **canonical_name**：代哥品牌资产秩序生态
- **entity_id**：ORG_DAIGE
- **first_foreshadow**：C01E01-QIHAI-CONSOLE
- **first_formal_appearance**：C01E01-QIHAI-CONSOLE
- **implementation_policy**：C01由闭馆期限届满、四方接管和公务风险频道构成正式制度出场，不依赖零号侧廊异常触发。浅层动机是降低G.A.G.活化、混装馆藏和未登记移动设施的公共风险，同时保护品牌资产与流通秩序；后续必须区分安全封存、限定流通、商品化谱系、数字运营和IP价值战略等不同部门，不能写成一股纯恶意意志。
- **notes**：旧C01E02-MAP-STORY正式出场口径已由V355-C01E01取代；具体执行单位、UI和接管顺序由当前C01 L4裁决。
- **role**：品牌资产秩序生态;安全封存与商品化/运营/流通压力
- **status**：core
- **type**：faction

## C50 七海 · remote_only · 第一章七海不得本人到场，只能通过私人语音、公务风险频道或通讯投影出现；她在C03实体抵达，并于V359-C03E03-CREATIVE以共同监督身份登舰。

- 节点：`runtime_rule:CANON-RULE-004`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/runtime_rules.tsv`
- 命中：`graph_1hop_from:entity:CH_QIHAI:被约束主体`
- 分数：`0.0000`

- **allowed_from_scene**：V359-C03E01-CREATIVE
- **entity_id**：CH_QIHAI
- **entity_name**：七海
- **forbidden_file**：game-godot/scripts
- **forbidden_regex**：七海.*现场|spawn.*qihai
- **implementation_key**：qihai_remote_presence
- **message**：第一章七海不得本人到场，只能通过私人语音、公务风险频道或通讯投影出现；她在C03实体抵达，并于V359-C03E03-CREATIVE以共同监督身份登舰。
- **rule_id**：CANON-RULE-004
- **rule_type**：remote_only
- **scope**：V355-C01E01_TO_C01E04
- **severity**：P1
- **显式关系**：
  - 约束主体 -> `entity:CH_QIHAI` 七海
  - 允许起点 -> `scene:V359-C03E01-CREATIVE` 整座城压上来

## C51 兜灯 / 窦晓宁

- 节点：`art_lock:CML002`
- 权威：`hard`
- 来源：`docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv`
- 命中：`graph_1hop_from:entity:CH001:被Canon 主体`
- 分数：`0.0000`

- **age_band**：青年
- **asset_status**：locked_current
- **canon_entity_id**：CH001
- **canonical_name**：兜灯 / 窦晓宁
- **current_art_reference**：.superpowers/brainstorm/37837-1782033239/content/char_tangjiao_doudeng_qihai_v3.png
- **gender_presentation**：中国青年女性
- **lock_id**：CML002
- **must_not**：不得只讲抽象守护论;不得变成普通热血驾驶员;不得把昵称画成儿童化装饰
- **notes**：本名窦晓宁；兜灯来自窦姓与童年戴头灯钻进馆守Z检修口的习惯。和馆守Z的关系优先于战斗爽点。
- **package_id**：R01
- **personality_anchor**：嘴硬手巧;把照顾说成维修流程
- **pronouns_or_address**：她;兜灯;窦晓宁
- **role_type**：馆守Z整备员;继承者
- **source_refs**：docs/superpowers/specs/data/character_voice/character_dossiers_core.tsv;docs/superpowers/specs/data/story/v35_core_cast_nationality_name_baseline_v1.tsv;.superpowers/brainstorm/37837-1782033239/content/c-route-character-mecha-correction-31.html;.superpowers/brainstorm/37837-1782033239/content/c-route-mecha-face-modes-asset-ledger-34.html
- **story_gate**：C01E01-REPAIR-BAY
- **subject_id**：CH001
- **subject_type**：character
- **unit_or_mecha_link**：馆守Z
- **visual_lock**：中国青年女性；维修服、头灯、安全绳、工具磨损和手上旧伤优先，昵称不靠可爱化表达
- **voice_rule**：维修动作先行;骂人要带工具、工序和旧件日期
- **wound_or_drive**：怕祖辈留下的是暴力神话
- **显式关系**：
  - 美术主体 -> `entity:CH001` 兜灯
  - Canon 主体 -> `entity:CH001` 兜灯
  - 参战包 -> `wanji_coverage:R01` 铁馆魔神

## C52 SRW系统梗

- 节点：`gag_hook:GH026`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/gag_hooks.tsv`
- 命中：`graph_1hop_from:entity:CH001:被相关主体`
- 分数：`0.0000`

- **category**：SRW系统梗
- **entity_id**：CH036
- **first_allowed_scene**：V355-C01E03
- **hook_id**：GH026
- **implementation_note**：不要让梗抢走断臂成桥主轴；勇拳是有人测试壳，金章只作终端预告。
- **payoff**：豪司只来得及答应一声，便实名越权驾驶勇拳先去顶梁。
- **related_entities**：CH001;R07
- **setup**：豪司想喊启动口号，金章终端先提示口号额度冻结。
- **显式关系**：
  - 主梗主体 -> `entity:CH036` 豪司
  - 相关主体 -> `entity:CH001` 兜灯
  - 相关主体 -> `entity:R07` 勇气株式会社
  - 首次允许场景 -> `scene:V355-C01E03` 双拳打碎外壳

## C53 低俗机战日常

- 节点：`gag_hook:GH062`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/gag_hooks.tsv`
- 命中：`graph_1hop_from:entity:CH001:被相关主体`
- 分数：`0.0000`

- **category**：低俗机战日常
- **entity_id**：main_cast
- **first_allowed_scene**：C01
- **hook_id**：GH062
- **implementation_note**：不能让正剧人物持续降智；不得替代机体/IP密度。
- **payoff**：缓冲阴郁气质，让主角团像真的住在展舰上。
- **related_entities**：CH001;CH_TANGJIAO;CH036;CH037
- **setup**：泡面、换灯管、尖刺背包撞门、合体Pose堵走廊也要被勇气许可或安全规程处理。
- **显式关系**：
  - 相关主体 -> `entity:CH001` 兜灯
  - 相关主体 -> `entity:CH_TANGJIAO` 唐胶
  - 相关主体 -> `entity:CH036` 豪司
  - 相关主体 -> `entity:CH037` 金章

## C54 same_unit_as · MECHA_SHADOW_SPARRING_MACHINE · V353U049

- 节点：`identity_link:IDL003`
- 权威：`working`
- 来源：`docs/superpowers/specs/data/canon/identity_links.tsv`
- 命中：`graph_1hop_from:entity:V353U049:被右侧主体`
- 分数：`0.0000`

- **left_entity_id**：MECHA_SHADOW_SPARRING_MACHINE
- **link_id**：IDL003
- **notes**：影子陪练机通用候选条目与V35生命周期条目指向同一单位。
- **relation**：same_unit_as
- **right_entity_id**：V353U049
- **scope**：V35.9
- **status**：active
- **显式关系**：
  - 右侧主体 -> `entity:V353U049` 影子陪练机
