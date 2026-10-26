"""Authored Candidate contracts for the second review. No engine implementation."""
VERSION='GW-SYSTEM-CONTRACT-20261009'
SCOPES=['首关依赖','系统恢复专关','全量／对照']
TASK_COUNTEREXAMPLES={
 'Q01':'旧进程版本与配置hash不一致；复现仍使用旧截图。必须拒收，不能拿本次文档替代运行版本。',
 'F01':'把拘束改名为重击、单位改ID；原结果不变，不能因名字切换到推移或多扣弹药。',
 'F02':'2×2只有三格有支撑、3×3仅中心净空；均不能落位。绕行可达不能因默认直路受阻而禁止。',
 'F03':'推开接触型敌人、旋转相对炮口、移动世界锁定目标；三者按各自绑定，不能全部追踪原对象。',
 'F04':'同快照预演100次、快进一次、回放一次；若最终HP、费用或rng有任一差异，不通过。',
 'F05':'桥HP4承受来袭5：实际损4，首次失效城防减2；不能把5当城防损失，也不能修桥倒赚城防。',
 'F06':'撤下焊具再点修复；原地给缺工具原因、不走过去扣移动，不凭故事需要临时长出焊枪。',
 'F07':'有盾敌被推入深水；盾不能防坠落。多格对象被一个爆心覆盖四格，不能按格重复受伤。',
 'U01':'Ctrl左拖跨过友机、普通左键点格、右键退瞄准、Enter焦点在按钮时各测；Ctrl绝不发移动命令。',
 'U02':'走近途中最后一格被占；整个命令失败且费用不变，不先走半路再报技能不可用。',
 'U03':'同一发会撞墙、伤友军、取消远区炮；三项都须画在实际对象上，不能只剩箭头和文字总数。',
 'U04':'无选择、悬停、选中三态；若普通待机就出现规则长文或全身缩略图当头像，直接退回。',
 'U05':'目的泊位塌落、备用位被占；在途机体显示等待和原因，不能消失或刷回移动/主行动。',
 'U06':'连续撤回、回放、结束回合再重置；不得复制精神、弹药、卡牌或贡献奖励。',
 'U07':'把推荐无牌换成其他合法机体；提示必须跟编队，不能仍要求点不存在的无牌。',
 'U08':'0.5秒划过10格后点另一机；迟到预览不能覆盖新对象，idle和行动结束不得有残影闪烁。',
 'U09':'关闭颜色信息后辨可达/敌意/推落；Ctrl手势只改镜头，触控适配不能把桌面点击又变成拖转。',
 'A01':'关HUD、正常战棋距离；靠全场发白或同色机体才能辨物则失败，不以局部特写代替。',
 'A02':'桥断电、未对齐、结构受损三个独立状态；不能同用一张红色贴图，点击范围须匹配实体。',
 'A03':'旋转机位看全部单位背面/落脚；二维面片翻面、王者视觉四格而规则单格均失败。',
 'A04':'UI125%和灰度下悬停图标、长机名；不得裁掉预算/风险，不能高亮整个棋盘掩盖目标。',
 'V01':'首个Tween启动前暂停，再快进/跳过；无残留子轨、二次伤害或漏结束音。',
 'V02':'连续直路、障碍拐角、斜视踢腿；不能格格停顿、穿墙、支撑脚不转而膝反折。',
 'V03':'盾吸收、推不动、第一格撞墙、油火二次爆；受力与终点正确，不播放不存在的长推。',
 'V04':'墙生成中暂停、桥受损后掉构件、机体失能；模型隐藏不等于规则对象删除。',
 'V05':'录系统声连续同招5次；分辨启动/接触/材质，峰值削波、低频盖住危险提示即失败。',
 'V06':'18招逐个普通、快进、连续播放；拳/掌/手刀混用或各招同一挥臂，不因通关就算通过。',
 'V07':'移走说话者或跳过通讯；离场头像不能冒用，跳过后次数/对象/结果保持相同。',
 'E01':'公开射线后移开目标；敌人不能临时转向重选。下一轮重新发布时才可适应。',
 'E02':'出生点堵一轮、持续堵两轮、地面塌落；延后/取消按公开规则，新生敌不当轮偷打。',
 'E03':'高火力全杀与保全控制都实跑；若只有唯一工程机能过或隐藏损失封顶保人，不通过。',
 'L01':'任一区不作为再结束回合；实际代价可见；换编队仍有公开路线，不靠万能互动按钮补救。',
 'L02':'列车从C向东跨B，切区后仍向东；断敌炮专线不能顺便关闭公共母线。',
 'L03':'第二任务换区名、目标和装置ID；不得改引擎按故事名字判胜，两种代价路线均可完成。',
 'S01':'载荷跨两层、脚印一角失撑；选择正确结构面并派生坠落，不能按中心格假悬浮。',
 'S02':'致命敌意在桥下；不旋转也有定位标记，透明处理仅遮挡物，不把全场都幽灵化。',
 'S03':'吊物终点空但途中撞梁，隧道出口被占；拒绝或等候，不瞬移穿越、不永久软锁。',
 'S04':'临架到期时上面有载人机；预告真实失撑和避险路径，不能到期直接删模型。',
 'S05':'转台转90度而炮锁世界格；方向/目标按绑定区分；远区涨水受影响对象须同时显示。',
 'S06':'燃料不足又无合法落位；预演显示迫降后果，不能到结算才淹死或无成本悬空。',
 'S07':'投送2×2到只有三个空格的泊位；不能压缩脚印，更不能到达后刷一轮免费主行动。',
 'R01':'替换为新ID但保留装备/能力；结果相同。14机中出现无装备依据的通用维修即退回。',
 'R02':'卸装/合体/分离后再合、同回合反复变形；唯一部件和行动不复制，已花移动不回满。',
 'R03':'遮名六机辨识、雷翎连续轮开火、审批错误工具；不可用强制空等或随机变工具冒充梗。',
 'P01':'给预算填虚构驾驶员、把CH048提前当C03到场；身份校验必须拦下，不能由UI补Canon。',
 'P02':'无本人签名/本地回执时用七海撤令；不能解全城锁；无出席人物不得使用其能力口吻。',
 'P03':'头像与目标快捷入口同帧提交同能力；仅扣一次且仅有一份回执，无第二套余额。',
 'P04':'空手牌照样救援；seed4101预演100次仍同牌；若额外点击超过预定门槛不得宣称采纳。',
 'P05':'预览同意后落点被占、有人仓被改为损伤目标；旧token作废，不能执行时再随机说不。',
 'P06':'友伤后维修、反复立拆墙刷气势；同root_event不重复计，台词不能推进未接受的故事事实。',
 'Q02':'任意预演/执行差异、旧存档无规则版本、过期缓存覆盖；必须留下失败输入，不只给pass汇总。',
 'Q03':'无口头提示新人无法指出目标与这一手后果；即使全自动通关、截图漂亮也不得认定可玩。',
}
SPIRITS=[]
def spirit(n,name,owner,target,phase,effect,fields,failure,case,cost=1,scope='系统恢复专关',source='D7 §4.2；本版透明信息改编'):
    SPIRITS.append(dict(id=f'SPIRIT-{n}',name=name,owner=owner,target_filter=target,phase=phase,effect=effect,result_fields=fields,failure=failure,case=case,uses=cost,scope=scope,source=source,
        cost={'main':0,'move':0,'sp':0,'energy':0,'use':cost},consume='atomic_successful_command_commit' if cost else 'never'))
spirit(1,'再听一遍','纪存','通讯连通；目标有自主回应；可核验旧工单；愿在当前条件下安全停工；尚未停工','player / 提交即生效',
 '每战1次。核对目标已公开的工单和意愿，写入自愿停工协议，取消该对象的作业承诺。本关B拆解工机的桥来袭伤害3→0；不改变异形、不返机体行动，不替七海签令。',
 ['consent_agreements[target_id]','status[target_id].safe_stop','cancelled_intents[intent_id]','usage[ability_instance_id]'],
 '“它没有可回应的通讯接口”“旧工单尚未核验”“它不同意停工”“已经停工，无需重复”',
 'GW-R1-COMMS',scope='首关依赖')
spirit(2,'以我的名字','七海','本人旧签名；尚可撤销；有当前持权人的单对象执行回执；通讯畅通；本任务未使用','player 提交请求 → work 持权人执行',
 '每任务1次；范围只限回执内的一道锁。七海撤回本人背书并提交请求，本地持权人按预先公布的回执在本轮work阶段解除该锁。先经过enemy阶段，不能事后抹去攻击。她不获得城市写权；被冒用签名须先记录在案。',
 ['revocation_requests[order_id]','scheduled_events[work_unlock]','usage[ability_instance_id]'],
 '“不是她的签令”“缺少当前持权人的执行回执”“签名真实性未核验”“该令已经撤销”',
 'P02-PERMIT-01')
spirit(3,'记录在案','七海','当前战斗已发生的可核验异常事件；含对象、命令号和真实来源；同事件尚未认证','player / 立即认证；请求执行仍按目标接口阶段',
 '每战1次，将公开日志中的事件生成一份签名EvidenceRef。P02中它满足被冒用旧签名的证据条件，仍需SPIRIT-2及持权人回执才能解锁；它本身不增加伤害、不改变敌我阵营、不直接开门。',
 ['evidence[event_id]','procedure_conditions[evidence_verified]','usage[ability_instance_id]'],
 '“此处只有预测，尚未发生”“事件来源无法核验”“这份证据已经记录”',
 'P02-PERMIT-01')
spirit(4,'预演','白鸢／系统基础可用性','任意可检查状态和合法草案；超出已冻结意图只显示条件或未知','preview / 不提交战斗状态',
 '不限次、免费。保存两份草案及各自snapshot_hash，比较HP、位置、资源、承诺取消和跨区变化。白鸢缺席时仍保留系统基础预演，但移除她的头像、声音和个人解释；不会让基础可用性依赖出席。',
 ['PreviewSession.plan_a','PreviewSession.plan_b','PreviewSession.delta'],
 '“局面已变，请重新预演”；未知远期意图标问号，不能写确定伤害',
 'GW-R1-PREVIEW',cost=0,scope='首关依赖')
spirit(5,'补一页','白鸢','配置中真实存在的备用接口及档案；线路和工具均存在；未认证的施工图','player / 认证方案；连接动作另耗主行动',
 '每战1次，认证一个已列出的备用接线方案，省去一次现场测绘主行动。原接口、承重、风险一直可查；能力只使既有施工图可执行，不生成路、桥、机体或新电源。连接仍由具备线缆工具的机体邻接实施。',
 ['work_plans[plan_id].verified','usage[ability_instance_id]'],
 '“这里没有备用接线图”“线路已断，须先修复”“施工图已完成复核”',
 'P02-ARCHIVE-01')
spirit(6,'先吵一句','豪司与社勇王主体AI','双主体均在；当前命令存在财物保全分歧；无人员伤亡或任务致败；权属人允许承担该损失','player / 与被协商命令原子提交',
 '每战1次。已准备好的终式会损伤空置、非城防计分资产时，可选择承担公开财物代价的原命令，或采用可执行反提案。限次只在经协商的命令成功提交时扣；听取/预览/普通接受反提案免费。实名路线声誉−1/任务一次，物理损伤照算，不奖励败选方气势。',
 ['consent_token[command_fingerprint]','consent_costs[reputation]','usage[ability_instance_id]'],
 '“这不是可协商的财物分歧”“仍会伤到人员，不能强行说服”“资产主人没有授权”“局面变化，需重新评估”',
 'P05-CONSENT-01')
spirit(7,'燃魂','豪司','豪司仍驾驶社勇王；本轮至少一项合法直接攻击可发动；未有同类修饰','player / 先提交修饰，下一次攻击使用',
 '每战1次；下一次主攻击对每个独立目标的直接伤害总计+2，每目标只加一次，多段不重复。环境连爆不继承。成功提交能力即扣次数；取消尚未提交的瞄准不扣。修饰在一次合法攻击提交（包括明确打空）或本轮玩家阶段结束时耗尽；不返主行动。',
 ['modifiers[next_direct_attack_plus2]','usage[ability_instance_id]'],
 '“豪司不在驾驶席”“本轮没有可发动的攻击”“已经有燃魂修饰”',
 'P02-BOOST-01',source='D1 §9.3名称；确定伤害参数为本版原创')
spirit(8,'撤回','当班警备驾驶席','实际出席的警备驾驶者；友方可中止的已提交蓄力；安全控制授权有效；尚未释放','player / 即时取消待释放事件',
 '每战1次，远程撤销一项友军已提交但尚未释放的charge。删除未来释放事件，已付弹药、气势不退，不返主行动。仅适用武器蓄力；持续承重不是本指令目标。普通未提交瞄准的右键取消始终免费。',
 ['cancelled_intents[charge_id]','charge_state[target_id]','usage[ability_instance_id]'],
 '“已经释放，不能撤回伤害”“这项工作不是可中止的武器蓄力”“没有友机的安全控制授权”',
 'P02-CANCEL-01',source='报告§7.4(b)对灰崎的提案；测试驾驶席，不认定CH048提前到场')
spirit(9,'硬停','兜灯','在场或安全链路在线；馆守Z或明确预授权的友方执行器；制动器可用','player / 安全制动立即结算',
 '每战1次。把指定友方持续动作改为safe_stop；取消其将来的动作事件；不退已耗资源、不恢复主行动。承载中的机构只有holding_brake能保住载荷，否则明确预演坠落并由意愿规则校验。重启由原执行者下轮花主行动1。不能暂停敌人时间。',
 ['mechanism_state[target_id].safe_stop','cancelled_intents[action_id]','derived_events[load_result]','usage[ability_instance_id]'],
 '“没有安全控制接口”“制动器已经失效”“停下会伤及人员，不能提交”',
 'P02-STOP-01')
spirit(10,'载荷判读','陆衡','已有两处固定锚点与可校验支撑图；有具备锁固工具的执行者；存在更换支撑的合法方案','player / 输出施工方案；现场动作另付费',
 '每战1次，认证一份无中断支撑交接方案：先把现有两根容量2的支杆锁到固定锚点，总承重4，再解除机体支撑。工程机仍耗主行动1锁固；原承重和坠落后果免费可查。方案不提高材料上限，也不凭空造支杆。',
 ['work_plans[support_handoff].verified','usage[ability_instance_id]'],
 '“现有锚点无法承受4单位载荷”“缺少实际支杆或锁固工具”“没有可以改善的支撑方案”',
 'P02-LOAD-01')

ATTENDANCE=[
 {'id':'GW-RESCUE-R1','people':['纪存','白鸢','豪司（社勇王驾驶席）'],'abilities':['SPIRIT-1','SPIRIT-4'],'note':'豪司本关0条限次精神；仍作为驾驶主体参与免费意愿检查。警备驾驶席不冒充C11人物CH048。'},
 {'id':'P02-PERMIT-01','people':['七海','纪存','白鸢'],'abilities':['SPIRIT-1','SPIRIT-2','SPIRIT-3','SPIRIT-4'],'note':'七海至多2条；测试关明确提供本地持权人回执，非正式剧情权限升级。'},
 {'id':'P02-ARCHIVE-01','people':['白鸢','纪存'],'abilities':['SPIRIT-1','SPIRIT-4','SPIRIT-5'],'note':'预演属于免费能力，不占有限精神槽。'},
 {'id':'P02-BOOST-01','people':['豪司','白鸢'],'abilities':['SPIRIT-4','SPIRIT-6','SPIRIT-7'],'note':'燃魂与协商分别验证，不允许燃魂越过意愿。'},
 {'id':'P02-CANCEL-01','people':['当班警备驾驶席','白鸢'],'abilities':['SPIRIT-4','SPIRIT-8'],'note':'使用本地驾驶资格ID；不为预算二号编造驾驶员。'},
 {'id':'P02-STOP-01','people':['兜灯','纪存'],'abilities':['SPIRIT-1','SPIRIT-9'],'note':'兜灯只接预授权安全链路。'},
 {'id':'P02-LOAD-01','people':['陆衡','白鸢'],'abilities':['SPIRIT-4','SPIRIT-10'],'note':'物理重量和风险不设付费隐藏项。'},
 {'id':'P05-CONSENT-01','people':['豪司','白鸢','纪存'],'abilities':['SPIRIT-1','SPIRIT-4','SPIRIT-6'],'note':'用于双主体四态与反提案；不宣称新的正式故事事件。'},
]

CONSENTS=[
 dict(id='WILL-BRAVE',unit='社勇王',identity='豪司＋社勇王主体AI；不称金章独立人格',trigger='直接或连锁结果伤及有人设施/乘员；或损害未同意牺牲的公共财物',hard='人员HP损失>0、任务立即失败、未知人员状态：reject',soft='只有空置非城防资产损伤：conditional；资产主人准许且SPIRIT-6具名承担后才可提交',alternative='保留机体ID，改为合法move_then_punch或转向；路径/主行动重新计算，已付蓄力气势不退',spirit='SPIRIT-6只处理财物分歧；SPIRIT-1只能听取已公开意愿，不能代替同意',case='GW-R1-SOUL；P05-CONSENT-01'),
 dict(id='WILL-KING',unit='完全版王者',identity='自主机魂',trigger='卸装将丢失部件或切断唯一撤离能力',hard='造成有人乘员坠亡：reject',soft='有承重落点、唯一部件ID和可回收方案：conditional；其余安全攻击accept；气势满不强制必杀',alternative='保翼卸盾或保留装备，产生真实落物Command；不能虚构放置格',spirit='纪存免费呈现已有回收约定；不借SPIRIT-1授予飞行/落位豁免',case='P05-CONSENT-02'),
 dict(id='WILL-LEILING',unit='雷翎',identity='独立主体',trigger='投送目的位不合载荷/承重或跨区无人接收',hard='有乘员且无安全落位：reject',soft='放置为无人货物且有已公告备用位：conditional；正常连续开火accept',alternative='改投声明的备用接收点，按真实路径费用重算；无地点则hold',spirit='免费通讯呈现已公开的接收意愿，不能解除物理阻挡；不额外扣SPIRIT-1',case='P05-CONSENT-03'),
 dict(id='WILL-CARGO',unit='货柜领袖',identity='独立载具人格，能说完整句',trigger='载人时攻击/卸载/撤撑将致乘员受伤；有人运输约定被直接丢弃',hard='无安全卸客位且要求抛弃乘员：reject',soft='乘员可安全先下车：conditional；无人任务可接受风险但预先列代价',alternative='先在邻接安全格drop_passengers再改形；两个已提交动作各付真实费用，不一键免费连做',spirit='免费查看替代路线，不让机体违反人员底线；SPIRIT-1仅处理工单停工',case='P05-CONSENT-04'),
 dict(id='WILL-POLICE',unit='灰崎警备劳务机',identity='当班驾驶者；不新增独立机魂',trigger='非致死装置被用来让可保全人员/工机坠落，或断开本人的警备约定',hard='明确人员伤亡：reject',soft='无人员的市政机损失：公开保全损失后conditional；不伪造机魂发言',alternative='把墙改到能挡射线且不堵疏散的格；替代格须实际合法',spirit='SPIRIT-8只能撤本就可停的蓄力，不能改已经发生的伤害',case='P05-CONSENT-05'),
 dict(id='WILL-BUDGET',unit='预算二号',identity='原资料未明确驾驶或机魂身份',trigger='本版不编造人格拒绝；只做工具、资源、权限和支撑校验',hard='物理/资源不合法属于validation失败，不属于机魂reject',soft='consent=null、has_consent_subject=false（界面状态not_applicable，不进入四态）；不为了凑七张卡产生角色台词',alternative='合法的顶推、真修、改派工程机；不由虚构驾驶员谈判',spirit='无专属精神；原装备动作可用',case='P05-IDENTITY-06'),
 dict(id='WILL-SONGWING',unit='歌翼可变机',identity='当前已查询实体表没有足够主体归属；配置扩展身份待核',trigger='本次仅定义形态、乘员和安全校验接口；人格规则留空',hard='安全/净空违规按通用validation拒绝',soft='consent=null、has_consent_subject=false（界面状态not_applicable，不进入四态），直到取得身份资料；不能称机魂恢复',alternative='可行降落/保留形态等普通Command，不冠以角色意志',spirit='无未授权的精神来源',case='P05-IDENTITY-07'),
]

SIGNATURES=[
 dict(id='SIG-1',unit='社勇王',source='entities: V353U024、SOCIAL_BRAVE_AI_REFUSAL：主体AI可拒绝高功率命令；审批章细则为报告§7.4(a)提案',rule='三格扇面各4伤、力量3推1；对象逐一结算。有人设施将受伤时提交前拒绝，给出合法单拳反提案。许可不能改物理伤害。',minimum='首关18招＋GW-R1-SOUL；审批章完整流程放R03-SIGNATURE-01',moves=['MV01','MV02','MV03'],fx=['FX02','FX05','FX13'],tell='从三格共同出手、双主体改案和核心大拳辨认，不靠标题。',later='章是持权人签发的区域/时段/工具许可，不是收集能量。准备2气势、释放1主行动；章不消耗、不加伤。无许可只能选普通拳或按已授权应急条款实名承担声誉−1；盖错章灰态，保留能合法工作的牵引工具建议，不随机变工具。'),
 dict(id='SIG-2',unit='完全版王者',source='entities: MECHA_C02_COMPLETE_KING：外翼、盾组、钻、背炮有真实战术价值',rule='2×2飞行体；双肩各一条首实体止步的炮线各3伤；右钻3伤、力量4推2；不是同一招换特效。',minimum='首关四格身体/飞行/炮钻；R03-SIGNATURE-02验证卸装',moves=['MV04','MV05','MV06'],fx=['FX01','FX03','FX14'],tell='宽体双炮的两处首体终点与右臂钻长位移。',later='卸装主行动1，唯一部件落邻接合法格。卸盾失shield；卸炮失cannon并移动上限+1；卸翼失fly。仅工位、同部件完好、相邻工具单位付主行动1可重装；不恢复本轮已用移动/行动。'),
 dict(id='SIG-3',unit='雷翎',source='entities: V353U047：远射、侦察、机动换位；标定合同为本版原创改编',rule='光束2伤打首体，命中后标定至本轮enemy末；下一个其他友机的直接攻击忽略目标的护群减伤1一次，不忽略自身装甲/盾；爆破五格各2伤无推。',minimum='首关光束/爆破/飞行；R03-SIGNATURE-03展示对护群的标定接力',moves=['MV16','MV17','MV18'],fx=['FX06','FX12'],tell='窄线击中后留下交接标记，下一台接火；与五格爆破分开。',later='不采奇数轮禁火。专关精瞄：准备主行动1＋弹药1，锁定当时的射线起点、方向及6格范围；下一轮原位且未受打断才ready。释放主行动1、首体3伤并标定，不追踪原目标，不重复扣弹。ready后每战1次可改快射：放弃固定射线，重新选一个正交方向，主行动1、首体2伤并标定；已付弹不退、不重复扣。若原目标已离线或友方进入旧射线，改快射可保住一次合法攻击；没有ready仍按普通光束。全程不增加主行动。载荷投送另走真实载荷规则。'),
 dict(id='SIG-4',unit='预算二号',source='entities: V353U032：廉价替代件完成高价值工程；临时支架数值为原创',rule='真修主行动1＋备件1恢复≤3；顶推主行动1、零备件、零直接伤、力量3推1。选择省材料还是永久修好，而非同款加血。',minimum='首关MV11/12真修与无伤控制；R03-SIGNATURE-04临时支架',moves=['MV11','MV12','MV13'],fx=['FX11','FX15'],tell='受损永久HP恢复与零伤受力箭头可分辨；三个独立锚点部署。',later='机载唯一可回收支架：容量4、HP2、质量1；邻格部署主行动1，不耗备件，保持当前及下一运输阶段后折叠。折叠物仍在场，邻接主行动1回收；未收回不可再部署。到期不扣设施HP，失撑触发真实坠落。'),
 dict(id='SIG-5',unit='灰崎警备劳务机',source='entities: V353U033：非致命控制、封路、警戒；不采报告新增伤3枪的建议',rule='拘束射程3，锁一台质量≤3目标的主动移动至本轮enemy末，不推不伤、不取消原地射击；墙射程2、主行动1＋备件1、HP3，按实体真正挡直射。',minimum='首关锁步/墙/有资格的柜操作；R03-SIGNATURE-05一锁一墙改线',moves=['MV14','MV15'],fx=['FX08','FX11'],tell='带张力的索、被划掉的移动与仍保留的炮线；墙挡到哪里就改到哪里。',later='首个真实保全危险工机的任务结果计一次声誉，不以“按了墙按钮”计奖；射界未变的墙不算贡献。'),
 dict(id='SIG-6',unit='货柜领袖',source='entities: V353U043：作业变形、护送、独立人格；能完整开口',rule='护场所选中心格的对象盾2、该格四邻覆盖到的其他对象各盾1，多格对象取最高一次，敌我同效；吊运射程2、载荷≤3、落点距载荷原位≤3。变形1×1→2×1，净空与扫掠都算。',minimum='首关MV07–10护场/吊运/载具脚印；R03-SIGNATURE-06载人',moves=['MV07','MV08','MV09','MV10'],fx=['FX07','FX09','FX10','FX13'],tell='先看到盾覆盖的车队与真实提起/落下，再看到运输形态的长车身。',later='载客上限4，乘员/载荷有ID，质量合计计承重。载人时不能无安全格卸客或缩回不兼容形态；车毁后安全邻格可救，无合法格按公开规则处理。'),
 dict(id='SIG-7',unit='歌翼可变机',source='报告§7.4(a)建议；当前身份材料不足，不作为已恢复名场面',rule='三形态的身体/武器表与广域震荡做全量专关；无新增精神身份。',minimum='不进首关；R03-SIGNATURE-07',moves=[],fx=[],tell='四点覆盖和形态交换火力/机动，不与雷翎同款爆破。',later='人形移动4、半转换移动3、航空移动6，切形主行动1、只保留原剩余移动与新上限较小值；震荡中心2伤、四邻力量2推1无伤。全量专关确认具备对应装备后开放。'),
]

FIXTURES=[
 dict(id='GW-R1-COMMS',board='首关B原局',setup='拆解工机(3,3)HP5，桥HP4，工机已公开3伤；纪存通讯在线，旧工单可核验，voluntary_stop=true',steps='悬停工机→目标旁通讯→再听一遍→悬停看取消3伤→右键取消→再次点目标提交',expect='取消时usage仍1；成功后usage0，工机停原格，桥来袭工机分量3→0，架设炮分量2保留；不返任何机体行动',negative='换成无通讯异形/删除工单/停机不安全/切断通讯，分别显示原因且次数不变'),
 dict(id='GW-R1-PREVIEW',board='首关C原局',setup='沿07默认六手或换防方案分别保存草案；白鸢在通讯席',steps='保存A导弹清轨→保存B单束清箱＋护车→来回切换10次→取消；再提交一项真实移动',expect='比较中原HP/弹药/行动不变；实际移动后两份旧snapshot过期；未知下轮敌意不伪装确定',negative='白鸢移出出席表，系统预演仍在但无她的头像/台词'),
 dict(id='GW-R1-SOUL',board='首关A的可重放教学快照，不改R1开局',setup='A原设施/敌人保留；社勇王改到(5,3)，王者仍(2,5)；社勇终式ready，准备成本已付，主行动1、剩移4。东向扇面(7,2)(7,3)(7,4)，避难所(7,2)有人HP3',steps='选东向终式→看有人避难所4伤与reject→预览反提案：移(5,2)，单拳打啮线体(6,2)→普通点目标提交',expect='拒绝不扣；反提案移1、主1、啮线体4→2，社勇自盾1；先前准备费用不退；无人随机夺权',negative='在预览和提交间把(5,2)占上，新状态重验失败，不能偷偷穿过去'),
 dict(id='P02-PERMIT-01',board='独立8×6许可测试局，R2玩家阶段',setup='锁柜(4,2)HP3；警备机(3,2)主1；有E17异常事件、七海旧签名Q17、本地持权回执D17(仅Q17)，锁定=true；一台待命工机(6,2)不攻击',steps='先点以我的名字，缺证据灰态→记录E17→请求撤Q17→结束玩家阶段到work→警备机下轮操作柜',expect='两条能力各扣1；work只解Q17的锁；柜的物理开关仍关闭，须机体主1现场开；其他柜不变',negative='把签发者改为别人/移除D17/仅有预测E17/重复提交，都不得解锁或扣次'),
 dict(id='P02-ARCHIVE-01',board='独立8×6接线局',setup='主线断口(3,2)；实际备用接口(2,3)(5,3)，预埋电缆完好；工程机(2,2)move5主1；未复核施工图R9',steps='看现有备用线和风险→补一页R9→工程机到(2,3)接口旁的(1,3)用线缆工具接线',expect='认证耗1次，不改地形；移2、主1才接通；不使用能力则先花一轮主行动测绘，下轮仍能接',negative='删备用线实体或工具，不能靠图纸接电；已认证不重复扣'),
 dict(id='P02-BOOST-01',board='独立8×6伤害局',setup='社勇(1,2)，无甲无盾敌(2,2)HP8；豪司出席；破甲拳基础2伤，主行动1',steps='预览燃魂后取消→再提交燃魂→打拳→重放多段同对象/扇面/盾吸收的独立变体',expect='取消不扣；提交扣1；单拳敌8→4；同对象同招只+2一次，环境爆炸不加；无第二主行动',negative='普通瞄准反复取消不复制修饰；玩家阶段结束不出拳则修饰过期、次数不退'),
 dict(id='P02-CANCEL-01',board='独立9×7蓄力局',setup='王者(1,2)2×2双炮ready，朝东；友机(5,2)，敌(7,3)，准备弹药已扣；警备驾驶席有安全链路',steps='用撤回点王者charge标记→看两炮未来事件消失→提交',expect='usage−1，charge取消，已耗弹不退，友机无伤，王者主行动不增加',negative='指向已释放event或托桥状态，灰态且不耗'),
 dict(id='P02-STOP-01',board='独立8×6制动局',setup='馆守Z(2,3)左臂持续操作绞盘；负载(3,3)质量2、holding_brake=true；转动事件将把负载送入(4,3)断口；兜灯安全链路有效',steps='悬停硬停看负载保留(3,3)→提交→下轮馆守付主1重启',expect='取消转动，载荷不落，不生出右手；usage−1，主行动不返；重启仅下一轮',negative='刹车改false则明确预演坠落；负载改为载人时reject，不把停机变成万能安全'),
 dict(id='P02-LOAD-01',board='独立8×6支撑局',setup='桥(4,2)(5,2)载重4，社勇(3,2)brace；固定锚(4,1)(5,1)各2，支杆已在场；预算机(3,1)有锁固工具',steps='免费查载荷→载荷判读认证方案→预算主1锁两杆→社勇解除支撑并走开',expect='认证usage−1但不直接撑桥；锁固后support总容量4，解除社勇支撑仍安全；预算少主1',negative='任一支杆不存在/锚损坏，不出假方案、不扣次；认证后新伤害使方案过期'),
 dict(id='P05-CONSENT-01',board='独立9×7双主体局',setup='社勇(1,3)终式ready、move4主1；东扇面(3,2)(3,3)(3,4)，两敌HP6和中间空置非城防货仓HP6；资产主人应急书面许可有效',steps='普通无财物版accept→仓入扇面conditional→替案移(2,2)单拳(3,2)免费可选→先吵一句选实名原案→最后换成有人仓重测',expect='协商原案三体各−4，存活可推者推1；货仓固定不推；主1、精神1、声誉−1；有人仓reject不可说服；接受反提案不扣精神',negative='章不在范围/费用不足/目标已换，旧consent_token失效；不会只因已看动画而耗次'),
]

EXPERIMENT={
 'id':'P04-DECK-01','version':'GW-DECK-P04-v1','depends':['GW-RESCUE-R1首关实际通过','P02精神专关','P03确定指令','P05意愿专关'],
 'seeds':[4101,4102,4103,4104,4105,4106],
 'opening_vectors':[
  {'seed':4101,'hand':['L1','W1','W2'],'rng_after_shuffle':2684478695},
  {'seed':4102,'hand':['B2','E2','L2'],'rng_after_shuffle':2786132524},
  {'seed':4103,'hand':['L1','J1','B2'],'rng_after_shuffle':2737286617},
  {'seed':4104,'hand':['C1','B2','J1'],'rng_after_shuffle':977515097},
  {'seed':4105,'hand':['E2','C2','E1'],'rng_after_shuffle':1064639916},
  {'seed':4106,'hand':['P2','J2','C1'],'rng_after_shuffle':962984807},
 ],
 'unit_ids':['brave','king','engineer','cargo','police','leiling'],'formation':'07默认六机，全部stock；局面由首关配置克隆，敌方选择已冻结；不混入成长模块',
 'rounds':3,'participants':12,'new_players':6,'experienced_players':6,
 'stage_goal':{'at_end_of_round':3,'minimum_head_index':13,'city_hp_min':1,'train_hp_min':1,'bridge_passable':True},
 'assignment':'参与者p=0…11，种子序号p%6及(p+1)%6；六种模式排列各分2人，第二种子反向。',
 'modes':{'A':'主版确定人物指令，无随机牌；基础精神两组相同','A_plus':'与B相同16张修饰池公开，回合择用；只用于分辨随机性是否真有价值','B':'16张固定实例，抽3/能量3/手牌5/回合末全弃未用/每招附1'},
 'rng':'xorshift32，0种子拒绝；Fisher-Yates降序，用32位拒绝采样消除取模偏差；牌堆、弃牌、消耗和rng_state随快照存取',
 'thresholds':{'basic_action_dependency_failures':0,'prediction_mismatches':0,'mean_extra_clicks_max':4,'p90_extra_clicks_max':6,'mean_turn_duration_ratio_max':1.20,'invalid_card_rate_max':0.20,'meaningful_choices_ratio_min':1.20,'seed_completion_gap_max':0.15,'prefer_B_vs_A_plus_min':8},
 'decision':'所有硬门均过，且B较A有效决策≥20%、12人中至少8人更愿重玩B而非A_plus才采纳B进入下一压力关；安全门过但只有A_plus收益则保留确定构筑；否则搁置B。不得据12人小样本宣称总体优势。',
}
# Six units x two, two named support people x two = 16 instances; no invented pilot cards.
DECK=[
 ('B1','brave','盾缘延伸',1,'punch','本招自盾1改为相邻一个友方对象盾1，不能两者都得'),
 ('B2','brave','窄幅终式',1,'finisher','只影响中心格，伤害/推距不变；不允许跨越人员底线'),
 ('K1','king','分炮保险',1,'cannon','关闭选定的一条炮线，另一条原数值，弹药成本不退'),
 ('K2','king','短程钻进',1,'drill','推距2改为1，直接3伤与力量4不变'),
 ('E1','engineer','节省备件',2,'repair','本次备件消耗1→0，恢复仍≤3；本场消耗'),
 ('E2','engineer','侧向顶推',1,'jack','从正前推改为选定横侧推1，仍须力3/相邻/合法落点'),
 ('C1','cargo','集中护场',1,'guard','移除四邻盾，中心2→3，敌我仍同效'),
 ('C2','cargo','轻载延伸',1,'lift','质量≤1时落点距载荷原位上限3→4，抓距仍2'),
 ('P1','police','折叠留口',1,'wall','墙保留实体阻射，但为友方地面移动留一条公开通行边，仍检脚印/敌人不能过'),
 ('P2','police','延时解索',1,'pin','当前锁步到期后续至下轮玩家阶段结束，仍不封原地射击'),
 ('L1','leiling','缩束瞄准',1,'beam','射程6→7，仍打首体，不加伤'),
 ('L2','leiling','定点爆破',1,'missile','五格爆破改中心2伤，移除四邻伤害，不加伤'),
 ('J1','纪存','交接复核',1,'transfer','目标泊位失败时使用提交时指定的第二合法备用位；不加速或返行动'),
 ('J2','纪存','载荷协调',1,'lift','载荷和吊者同时有合规吊点时可转向后落地，路径/距离/承重照算'),
 ('W1','白鸢','补记接头',1,'connect','已测绘双接口动作可改另一条配置中存在的备用连接，不创造连接'),
 ('W2','白鸢','保留方案',1,'draw_control','抽1后从手牌选1弃；不弃基础精神；本场消耗'),
]
CARD_CASES=[
 ('CARD-01','装载清点','加载固定B1…W2共16实例→移除雷翎来源→显示L1/L2不兼容→另选两张兼容实例才可开始','牌表不是16、缺席者仍供牌、自动补入隐藏卡'),
 ('CARD-02','回合抽弃','种子4101开局抽3且能量3→另载入满5手牌的边界快照测试W2（不称本牌表常规可达）→抽1并公开弃1→结束回合','普通移动扣能量、静默随机丢牌、手牌超过5不处理'),
 ('CARD-03','附着与取消','社勇拳附B1→换B2因不兼容拒绝且保留B1预约→右键退出释放B1预约→重新附B1并提交','旧牌不退/扣两次；牌在确认前永久消失'),
 ('CARD-04','断线','纪存J1瞄跨区泊位→复制快照断开通讯→重新预演','失联仍可跨区修改；未在场人物发言'),
 ('CARD-05','消耗','打出E1→进入exhaust→切三区→洗弃牌→回合重置','E1经切区/洗牌再出现；整轮回溯未还原先前消耗状态'),
 ('CARD-06','种子','相同初态4101洗牌抽3→预演100次→重置10次→存读档','任一次首手/rng状态不同；预演推进真实rng'),
 ('CARD-07','空牌','手牌强制为空，在无牌模式走07默认六手到运输','维修/移动/接口基础动作消失，或必须抽到某牌才救援'),
 ('CARD-08','行动守恒','对移动后主行动0者附牌、切形、转区、击破试图再出手','任何牌隐式把main从0变1；本版不装载再行动牌'),
 ('CARD-09','关间三选一','关间给E1、C2、K1三张兼容候选→已满16→选择入收藏或替换已装实例→也可放弃领1credit','满额卡死；直接变17张；为不存在来源给牌'),
 ('CARD-10','交易','初始credits4，升级C2花2（轻载最大落距4→5），移除K2花1；重复点击同transaction_id','现金不为1、重复扣款；删除K2使基础钻消失'),
 ('CARD-11','成长','三关固定贡献：4/6/4XP；到6和14阈值各解锁一个可选项；重复回放同结算','仅击殺可成长；同一救援反复领；回放累计XP'),
 ('CARD-12','操作测量','三模式交叉顺序录像；逐次标记开牌栏、选牌、选目标、取消、切区、确认及思考时长','把选牌+选目标算1次；只报成功玩家；未记录无效牌回合'),
]
GROWTH={
 'version':'GW-GROWTH-P04-v1','first_level_enabled':False,'starting_credits':4,'starting_reputation':0,'xp_thresholds':[6,14],
 'reward_rules':[
  {'id':'mission_complete','condition':'达成主目标','credits':3,'reputation':0,'xp':2,'scope':'每任务一次；XP给实际出席且未弃战者'},
  {'id':'rescue_all','condition':'24人全部到撤离口','credits':2,'reputation':1,'xp':2,'scope':'任务一次；XP给有救援因果贡献的操作者'},
  {'id':'infrastructure','condition':'城防损失≤1且桥/母线未失效','credits':1,'reputation':0,'xp':2,'scope':'任务一次；XP给实际防止设施伤害或恢复关键连接的操作者'},
  {'id':'preserve','condition':'有危险市政机且全部保全并停止其破坏','credits':1,'reputation':1,'xp':2,'scope':'任务一次；XP给实际解除威胁者，不计只放墙'},
  {'id':'combat','condition':'击毁本轮公开威胁，或安全控制使其伤害取消','credits':0,'reputation':0,'xp':2,'scope':'同一威胁root_event一次；可归因多人各≤2XP，总计不超过对象2XP'},
  {'id':'municipal_loss','condition':'每台市政机被毁','credits':0,'reputation':-1,'xp':0,'scope':'按asset_id首次；不因此禁止通关'},
  {'id':'signed_override','condition':'明确承担非人员财物代价','credits':0,'reputation':-1,'xp':0,'scope':'每任务一次；不得与同一损失再重复处罚'},
 ],
 'xp_cap_per_participant_per_mission':8,'dedupe':'campaign_id/mission_id/root_event_id/reward_rule_id；正反重复构造、我方造伤后修复不计贡献',
 'attribution':'一个combat事件2XP平分给至多两位有事件依赖边的操作者；1人得2、2人各1；无归因则不虚构。团队奖励单独一次，个人XP按上限截断。',
 'unlocks':{'6':'选一个当前装备兼容的协作模块使用资格，不自动装备；预算未定主体记机组熟练度','14':'再选一个不同战术方向的资格或一张兼容候选牌（仅B）；无自动主行动/气势加成'},
 'shop':{'remove_card':1,'upgrade_card':2,'skip_reward_credit':1,'max_deck':16,'upgrade':'每实例最多一级；交易前后版本、现金、收藏和装载均入快照'},
 'three_missions':[{'mission':'P04-GROW-01','xp':4},{'mission':'P04-GROW-02','xp':6},{'mission':'P04-GROW-03','xp':4}],
}

READABILITY=[
 dict(id='READ-A',question='哪里要供电，哪里会被啮断？',cells='A电柜(4,3)；避难所(7,2)；深槽(6,0)(6,1)',shape='电柜偏置绝缘瓷柱和粗母排穿出方形底座；避难所有退入式门廊/人行灯；深槽真实切断楼板侧壁，能看见内侧与水面',height='A为H2；槽底比平台低1档，水面低0.8格高。啮线体北侧无护栏，邻接推落语义真实',overlay='闲置不铺全城电线。悬停电柜时金色插头＋沿实际母排的细流线指向B桥；悬停啮线体用珊瑚红箭头锁到避难所边缘和闪动HP段',test='首次看默认镜头5秒，指出要接的柜、被攻击的屋和可推落方向；不靠看说明书'),
 dict(id='READ-B',question='桥究竟没对齐、在坏，还是没被撑住？',cells='B桥(4,3)(5,3)(4,4)(5,4)，接口(3,4)，水道x4/5',shape='岸轨到断口止住；桥面低置0.35格高且锁销缩回、轨头横向错开0.25格；升齐后轨头接缝闭合和两侧锁销插入',height='岸台H1，渠底H0；桥低位不可行车，修齐/托到位才匹配H1；侧桁架不能遮接口',overlay='悬停桥出现两枚不同图标：断开的插头、错开的轨扣；预演支撑以金色受力线连真实支点。HP损伤用裂口/垂下梁，不用“没电变红”混淆',test='隐藏HUD与文字先辨断桥；再只开图标，指出缺供电/缺对齐/缺承重中的实际项'),
 dict(id='READ-C',question='车向哪开，哪只柜在给远处敌炮供电？',cells='C轨x2…9,y3；箱(4,3)；馈线柜(6,4)→A炮(7,4)',shape='轨道与道床高于地坪0.08格高；货箱有实底/角件/吊点，断开轨路；馈线柜细高电容＋专线隔离刀，外形区别公共母线',height='C为H0，经可见坡道升到B H1；远景同一柱环编号连续，不把C/B画成左右颠倒的孤岛',overlay='选车仅亮C向东到B的金色轨箭；指向馈线柜时两区边缘出现同一电缆符号，A缩略图闪炮口，被取消2伤单独划掉。常驻不拉全屏线',test='无口头提示能指认车向右跨区、断柜只停A炮而非全部城市供电'),
]

def layer_data():
 return dict(version=VERSION,status='design_contract_only_not_implemented',spirits=SPIRITS,attendance=ATTENDANCE,consents=CONSENTS,signatures=SIGNATURES,fixtures=FIXTURES,experiment=EXPERIMENT,deck=[dict(id=i,source=s,name=n,energy=e,tags=t,effect=f,exhaust=i in ['E1','W2']) for i,s,n,e,t,f in DECK],card_cases=[dict(id=i,name=n,steps=s,fail=f) for i,n,s,f in CARD_CASES],growth=GROWTH,readability=READABILITY)

def update_details(details):
 """Replace concrete source fields, preserving shared-record identities and analyses."""
 def patch(id,**kw):
  old=details[id];new={**old,**kw}
  for k in old['shared_with']:details[k]=new
 for s in SPIRITS:
  patch(s['id'],adoption='固定为'+s['scope']+'的可执行合同；并非已实现。',design=s['effect']+' 目标：'+s['target_filter']+'；作用阶段：'+s['phase']+'。结果字段：'+', '.join(s['result_fields'])+'。',player_expression='人物头像下的确定指令卡与通讯面板引用同一个ability_instance_id及次数；目标旁快捷入口只筛选同一条能力。悬停先算，点合法目标提交，右键退出。失败句：'+s['failure']+'。',example=next(f['setup']+'；'+f['expect'] for f in FIXTURES if f['id']==s['case']),verification=s['case']+'：'+next(f['steps']+'；反例：'+f['negative'] for f in FIXTURES if f['id']==s['case']))
 for s in SIGNATURES:
  patch(s['id'],adoption='招牌有明确合同和测试局；首关最小集与完整身份功能分别验收。',design=s['rule']+'；范围：'+s['minimum']+'；后续定稿：'+s['later'],player_expression=s['tell']+' 引用'+','.join(s['moves']+s['fx'])+'对应的实际形状与时点，不另造效果。',verification='六机名/色遮蔽的因果识别≥90%，机体识别≥80%，单机≥7/10；记录原始回答与误认。'+s['minimum']+'；'+s['source'],example=s['tell']+'不能把后续合同存在说成首关已实现。')
 for i,n,steps,fail in CARD_CASES:
  patch(i,adoption='P04独立对照规格；配置B不作为角色卡恢复条件。',design=details[i]['design'].replace('首测','P04固定对照').replace('首测平均','P04平均')+' 对照版本GW-DECK-P04-v1，固定16实例与6种子；详见10册。',example=n+'：'+steps,verification=steps+'；失败样子：'+fail+'。所有结果须来自实跑，当前无实测值。')
 patch('CARD-01',design='GW-DECK-P04-v1装载固定16实例：六机各2张共12，纪存和白鸢各2张共4。牌表见10册，不再额外叠“每驾驶员1张”。来源缺席则该牌不兼容，须公开换成合法实例；同名最多2。')
 patch('CARD-03',design='每招最多附1张，AttachedModifier绑定待提交command_id。合法换牌原子释放旧预约并预约新牌；非法换牌保留旧预约和世界状态，给出不兼容原因。右键退出全部释放未提交预约，成功命令才一起扣能量/牌/主行动；同command_id不重复扣。')
 patch('CARD-05',design='E1/W2成功打出进exhaust，其余进discard；预览/取消不移动实牌。exhaust仅新战初始化恢复，切区/洗弃牌不能恢复；完整回合重置还原该回合开始时全部牌区。')
 patch('CARD-09',design='关间三选一先入收藏，不自动超过16装载上限；装入新牌需选择替换实例。候选过滤来源、装备和同名≤2，至少两类战术方向；无适配则只给放弃奖励1credit。CARD-09固定验证E1/C2/K1，不生成无来源驾驶牌。')
 patch('CARD-10',design='GW-GROWTH-P04-v1初始4credits，删实例1、升一级2；C2唯一级将轻载落距4→5，抓距仍2。一次transaction_id仅扣一次；已确认交易不局部回滚，只随完整整备快照恢复。声誉当前只影响公开结算和剧情评价，不暗改价格或屏蔽基础工具。')
 patch('CARD-08',design='GW-DECK-P04-v1禁止所有再行动牌；附牌、换形、击破和转区均不得刷新main。它们只改已声明的形状、资源或条件。再行动不作为本次实验变量。')
 patch('CARD-11',design='GW-GROWTH-P04-v1：每任务完成2XP，救援/保全/设施实际贡献各按表计，个人每任务上限8；阈值6/14，三场4/6/4XP可重算。credits主目标3、全救2、设施1、保全1；reputation全救+1、保全+1、市政毁损−1；按任务/事件去重。首关不启用该成长配置，详细归因和交易见10册。')
 patch('DG-SYS01',design='十条精神采用09册字段表：在场、目标过滤、次数、阶段、结果字段和逐条失败句全部固定。基础检查/预演免费；有限能力成功原子提交才扣；协商修饰与攻击同时提交扣。R1仅SPIRIT-1/4，其余都有P02/P05专关。')
 patch('DG-SYS02',design='配置A卡面字段为card_id/source_person_id/ability_instance_id/target_filter/cost/uses/phase/effect_ref/disabled_reason。人物头像、通讯双页签、目标旁快捷入口都引用同实例；不能三处重复扣次。P03复用GW-R1-COMMS及P02-PERMIT-01；配置B不参与恢复判定。')
 patch('DG-SYS04',design='ConsentResult含state、reason、public_predicates、counterproposal Commands、cost_delta、snapshot_hash和command_fingerprint。四态优先级：硬拒绝→条件→有合法替案时counterproposal→接受。至少社勇WILL-BRAVE在GW-R1-SOUL实跑；同状态提交不得反悔，状态变化先废弃旧token。预算/歌翼身份未明用not_applicable，不能捏造机魂。')
 patch('MV07',design='主行动1，选2格内有对象的中心格，中心对象盾2，中心格四个正交邻格覆盖到的其他对象盾1；按对象ID取最高一次，不能用大脚印多叠盾，持续到本轮运输后。敌我同效；先算护甲/护群，再扣盾与HP，盾不阻推。发射锚点→扫描→逐对象展开薄面。')
 patch('MV16',design='主行动1＋弹药1，6格直线首实体2伤；本束结算后留下标定。至本轮enemy末，下一个其他友机的直接攻击可忽略该目标护群减伤1一次，不忽略自身装甲或盾；按本次攻击根事件消费，多段不重复。瞄准→亮核和色晕→首体刻痕→短散热；不靠大爆炸掩盖端点。')
 patch('SPIRIT-7',verification=details['SPIRIT-7']['verification']+' 多段同对象加伤总额只+2，禁止每独立伤害效果各+2。')
 patch('DG-SYS08',design='首关气势上限3。击破公开威胁、实际保护成功、完成救援/关键协作各提供1；同对象同root_event本轮只计一次，单次多杀至多+1。新获得气势不在同一动作递归再消费；终式准备耗2，主行动规则见07/08。')
 patch('PERSON-07',design='不采用奇数轮禁火与强制空等。雷翎普通光束/爆破每轮在行动资源足够时均合法。标定在命中后产生，下一个其他友机直接攻击消耗；具体数值见SIG-3。瞄准准备后的有限改快射放R03-SIGNATURE-03，不能声称轮换梗原样恢复。')
 patch('PERSON-06',design='王者气势满只显示必杀机会，不自动发动、不因玩家保留行动而暗扣移动。意愿仅检查真实部件回收/人员安全；卸装反提案遵守WILL-KING。')
 patch('ART06',design='设施HP处于0<HP≤max_hp/2时进入受损外观，HP=0按对象合同进入可修失效或摧毁。断件、裂口、灯光与功能入口成表；除非正式移除结构面，装饰缺损不能悄悄改变碰撞。首关READ-A/B/C同时分清没电、未对齐和受损。')
 patch('ART10',design='1080p基准字体：标题22px、关键数值18px、补充说明14px，用户缩放等比放大；底部只当前队伍/主行动，顶部回合/保护值/各区紧急项，I详情按需展开。文字不压住目标；READ-A/B/C以图形和物件为首层。')
 patch('G2',design='按08的18招60Hz时钟逐招落pre/contact/result/input标记，废弃轻重招统一0.10/0.12/0.25等旧区间；工程、拳、炮各自沿实物接触点播放。跨轮蓄力准备27帧另存状态，不把整招时长当接触帧。')
 patch('G6',design='相机仅渲染偏移，不改逻辑相机与拾取射线。1080p轻/中/重分别3/5/8px，12帧回中；同帧多击合成并限8px，不叠到无限震。关震屏/减少动态时偏移0，规则反馈仍保留。')
 patch('SP-BASE4',design='首关非深水/无底坑的落差每档1伤、上限3；深水对无浮航能力者按溺毁，无底坑按坠毁。完整脚印求稳定着陆面；同一大机只计一次基础坠伤。落到实体还生成一次明确碰撞，不以动画帧数重复扣伤。')
 patch('AIR-18',design='首关飞行转区耗主行动1、余移清零，当下抵达且不再出手；地面出发经过本轮enemy/environment/work，在arrival阶段到达，下一轮刷新才可行动。出发前检整脚印泊位与备用位；泊位失效则备用或等待，不丢单位。')
 patch('MV08',design='抓取范围2、载荷≤3、落点距载荷原位≤3，主行动1；检查吊点、完整脚印、承重与全过程净空。近场吊运按MV08时钟18帧抓住、60帧基准落地、78帧接下令；跨区另走07运输合同，不把旧拍数翻译为回合。')
 return details
