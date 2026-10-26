# 141 · 公式台当前：Q 连续章节初段与 P 练兵场

2026-10-01 更新；下文保留此前的历史证据。工作区 `/Users/rayz/Documents/超gag机器人大战`；接手时核对实际分支和未提交改动。
**Candidate / not_canon / runtime_allowed=false / user_visual_acceptance=false。目标尚未完成。**

## 1. 从这里接手

**2026-10-01 当前 P 修复：** P 为 v11.4「绕行与抢格预告」，Q v2 不变。玩家 journal 231、290、314 行已确定性重放：等长路线可换，自动靠近/团队就位/修正会检验完整路线；不会用拦路效果掩盖空拳。冲突预告与时间轴注明双方及拍数。重放 33、原生界面按钮 13、宿主输入 29、三段集成 64 项通过，现有规则/决策/交互及 Canon 检查通过。自动输入不代表用户重试玩接受；同拍抢空格双方停步以及逐机/团队时间组织差异仍保留。源码备份、失败基线和实际图在 `qa/stage-routing-20261001`；[本轮说明](../../work-packages/2026-09-21-chao-gag-representative-chapter/formula-stage-v11-4-routing-20261001.md)。当前 12 包目录和整个公式台入口保持。

**2026-09-30 v2 当前停点：** Q 已扩充到 15 组 / 150 条对白或事件，含 16 个事件镜头；补赵梅、胶价王等立绘，货柜领袖运输与白鸢尾声，专用朱红货运环和四区绘制材质。王者改为用户指定的对称无嘴面罩、右手巨钻、肩背轴座前向双炮；旧腿侧钻与错误四联图撤回。v2 存档独立，v1 包备份保留。见[v2 制作与证据](../../work-packages/2026-09-21-chao-gag-representative-chapter/chapter-c02-qualifier-v2-20260930.md)。当前是候选适配，未取得美术验收；本版原生输入仅检查到前场与工房，不能沿用 v1 通关记录声称 v2 人工通关。后续仍按原章节顺序推进。

**同日 v1 历史记录：** 按已批准的[到港—报名—资格赛—回到工房](../../work-packages/2026-09-21-chao-gag-representative-chapter/chapter-production-next-20260929.md)完成 Q 连续章节初段。根入口 `公式台-无牌一号出场.command`，索引为 A–J、P、Q 共 12 包。已用原生键鼠走通一条绕侧资格赛路线，保存回工房；规则 83、恢复 48、流程图形集成 54 项通过。新模型街改为工业折转内街，王者头部重做，主要人类对白立绘按共同面部尺度和视线裁切。详见[本段交付](../../work-packages/2026-09-21-chao-gag-representative-chapter/chapter-c02-qualifier-v1-20260930.md)。当前 P 保持[木桶街 v11.3](../../work-packages/2026-09-21-chao-gag-representative-chapter/formula-stage-v11-3-materials-20260929.md)，练习消失 68 项和三段集成 74 项回归通过。下一段仍按原方案制作师徒训练、旧片和正式交手。整章与七公式目标尚未完成，美术及首玩体验等待实际评价。以下 v2 和 9 月 19 日停点是历史证据，不代表当前画面、工具可用性、入口或下一步。

**2026-09-26 用户最新定位优先：** 当前 demo 融回公式台的整体制作。公式台负责精良打磨全项目各类玩法、机制及呈现标准，作为 Godot 上的游戏专用基础层。当前工作方向见 [140 §0.1](140-formula-lab-integrated-visual-production-goal.md)；完整范围仍为七公式与可复用内容生产。先在公式台内完成可操作前场、战斗、战后变化的连续切片，再将共同能力用于其他玩法。

C02 最新独立对照是[第 13 号 V8](../../work-packages/2026-09-21-chao-gag-representative-chapter/stage-v8-20260926.md)。它已有逐机/团队、接力、人物能力、试演与地图操作。**现已追加 P 接入联调包**：在公式台运行器内连续经历可操作前场、V8 战斗与真实战后回应，三个阶段共享同一世界；默认索引为原 A–J 加 P 共 11 包。原 A–J、V8 源码与独立对照入口保留。入口是项目根 `公式台.command` / `公式台-木桶街.command`，没有另起外部 demo 冒充接入。

**最新制作进展：** 已将旧少帧图集替换成纪存、白鸢三维骨架模型；前场使用 Blender 建筑和道具，人物可实际进门且屋顶自动让开；馆守沿用 V10X 造型并补充刚性动作片段。P 当前标题“模型与动作样板 v2”。旧 `map-cast.png` 继续保持 `rejected_for_production`，新样板仍未获得用户视觉或手感验收；不能把它列为全项目美术标准。源文件、实际证据及不足见[本轮模型动作交付](stage-battle-model-motion-v2-20260926.md)。Meshy 本轮未生成/下载/消费额度，本机 Blender 制作已经独立推进，无需用户确认才能继续。

新接入状态检查 61 项、宿主输入检查 23 项通过；旧浏览器原生图形与 headless 各 69 项通过。旧测试无条件按 A 导致原生模式先被暂停的问题已诊断并修正测试前提，未改游戏播放规则。均不构成美术或玩家体验通过。七公式整体目标尚未完成。

地图美术按 [140 §3](140-formula-lab-integrated-visual-production-goal.md) 的最新用户要求执行：纪存、白鸢 `atlas_v2` 的头身比退出新版地图复用；地图角色与场景配套风格化，正比例用于对白立绘和特殊事件画面。更 Q 是制作侧先试的方向，具体比例未定。旧资产的身份和技术资料可参考，失败比例不继承。

下述 2026-09-19 停点保留为旧公式台实验的证据与缺口；与上述最新要求冲突的制作顺序及边界，以最新要求为准。

**2026-09-19 最新用户反馈优先：** 用户实际看见T7界面后明确表示战斗地图方正、空间浪费、战斗与动作表达差，“真的没法玩”，要求重新开展B站实机视频调研，并考虑《席德·梅尔的文明》的交互。主对话已保存当前原生录制，转做战场空间、选中/指令、场景与动作镜头的专项比较。不能继续仅修姿态或坐标便宣称回应了本次问题。140完整目标与Candidate边界保持；格制、回合规则、3D迁移和全局风格的重大变化须先形成具体可审方案。

**最新独立试制：** [package-o-dock-field-v5](../../../../../artifacts/formulas/production-lab-v1/builds/package-o-dock-field-v5/flow.json)，见[第二轮体验审核及录像](../../../../../artifacts/formulas/production-lab-v1/qa/dock-field-20260919/root-review-v2.md)。现场指令、按需可达边界和共同提交保留；仅对完整回执证明确实无变化的三条原地朝向记录省去独立停留，14个引擎包全保留。相同R3自动采样从13.748秒缩到11.759秒，首工程动作从约4.396秒提前至2.452秒。preview-v7保存142图、11项检查通过、无强制绘制、最大间隔97.780ms；84来源行/81路径SHA及五JSON重建一致。新节奏48项、旧事件536项/72包及Canon检查通过；旧测试首次6项过时断言已按既有HP回执前值/在场快照修正，三条已有图像导出警告仍在。当前包未进current-packages.json。

**独立空间对照：** space-probe-v2使用真实R3拆主锁包和临时3D体块，分析速度0.5倍，冻结包后不改引擎；不是完整回合、物理模拟、Meshy生成或生产渲染器替换。97图、零强制绘制、最大间隔97.816ms；主对话看完两组共239图/13联系板，并核全景/接触原图。首版舰体遮脚的取景已拒用。新取景能同时看脚、架与舰侧，但连接仍突然消失、发力不足、伙伴与场景未齐。**当前生产包仍是规则灰模和离散姿态；空间、重量、原生手感及战斗体验均未通过。**

**Meshy 补充：** 用户提出可用图生3D降低Blender起模工作；[适用性调研](../../../../../artifacts/formulas/experience-foundation-v1/meshy-project-fit-20260919.md)已核多视图、拓扑、机械绑定限制、GLB导出、费用与条款。先以Call04衍生单物体舰态图做小样，再核独臂Z的机械动作；多形态母版不能直接整张输入。没有项目上传、生成、付费或插件安装，本项目模型质量尚未实测。140完整目标保持。

**Meshy 当前条件：** 用户已答只有免费账号；[Lite舰体首样](../../../../../artifacts/formulas/experience-foundation-v1/chapter-art/meshy-wanji-pilot-v1/README.md)锁定现有单图及母源，首轮不升级、不用多视图或API。月赠额度不等于实有余额。CUA能选择浏览器并读空白标签，Meshy创建/导航两次20秒超时；未读到账号或参数，也未上传。不要将此写成“用户未解锁”或“所有窗口均不可控”。CLI/MCP底层仍受API付费权限限制，未安装。准备材料与继续本地体验工作不依赖这个在线小样。

**当前原生通道仍不可用：** 本轮两次直接取Godot窗口均约120秒超时，第二次已重置工具并新开R3。没有成功发出键鼠输入。native-v1只保存自动前两轮设置与启动图，无完整capture.json；自建进程已结束。不要把超时解释为用户未解锁、不要再让用户重复解锁。此前v11成功过的原生证据保留，但不能代替新场景原生试玩。

**v11历史工程停点（下述审查未被作废，当前独立试制见上）：** `package-o-wanji-call04-v11/flow.json` 使用reading/carrier v5，新增Z抱架/拔架两张内置生成Candidate姿态及舰身固定座；Call04母版不变。render-v9的332张自动图已逐项审过（328棋盘图、20张Z局部图、4张完整结果页）；动作仍跳变，前后遮挡、脚点、其他角色/桥梁及整体战场表达不合格。81来源行/78规范化路径当前SHA一致，五JSON重建一致，126结构边界、67真实成功/失败结果、6生产器及Canon检查通过。这些仅是工程与有限画面证据，用户最新整体否决优先。详见 `artifacts/formulas/production-lab-v1/qa/tactical-carrier-t7-20260919/verification-v11.json`。

**v11历史原生输入与部分实录：** 直接通过 `/Applications/Godot.app` 重新取得真实DEBUG窗口后进行了键鼠规划、返回改路、R1正常执行、R2实际Skip、R3正常执行；R4仍在规划目标时按用户新方向F10保存退出。`native-v11-01/capture.json` 与344张PNG已落盘，accepted=written=344、pending=0、写入无错误；未完成R4/R5或最终检查点。344张保存序列尚未完整逐帧审核。分段核实R1执行的182张无强制绘制，最大间隔99.953ms；R3执行的136张全部依赖看门狗，最大间隔278.474ms，不能证明正常原生节奏。Master录音1363.893秒的峰值为0，不能声称有声音或听感通过。自建Godot录制进程已退出。随后B站浏览器控制仍超时，正采用已验证的公开有界取片方式做有序帧研究，不再要求用户重复解锁。

用户要求先从金标实际操作建立本项目统一体验语言，再从有效定稿Reader与机制解构选七个章节验证包；允许基于既定美术新增Candidate验证资源。最新补充：按问题比较多个B站候选，选择最合适的主来源和对照，不凭一条片子定标准；数据与分析核完后删除下载的大视频，只留必要证据。**140§6.1及143已写入这套选材、交叉核查与清理要求，用户已明确要求修订后直接继续。**

**本次专项研究和下一轮方案：** [文明/幻影旅团视频分析](../../../../../artifacts/formulas/experience-foundation-v1/video-study/battle-scene-composition-20260919/README.md)已核地图选择/移动、目标比较和同场规划→执行→再规划；[战场构建方案](../../../../../artifacts/formulas/experience-foundation-v1/battle-scene-direction-20260919.md)优先试连续局部场景、按需格线和现场指令。文明完整普通攻击链、原声与新方案实玩仍未证，不把研究当体验通过。v11详细停点见[审核](../../../../../artifacts/formulas/production-lab-v1/qa/tactical-carrier-t7-20260919/root-review-v11.md)。

2026-09-18已有按140建立的goal，不重复创建。主对话已核目标卡为active，目标正文就是金标研究、统一语言与七个章节包。三方互证、两房间背景、原件比较、查看/引用分离与既有实玩成功链继续保留。目标未完成，未发生用户暂停。

**最新来源纠错（优先于旧记录）：** 主对话此前只沿用8月23日129，漏读8月24日A23 Call04及A25用户回执。Call04已被用户选为“目前最好”的深化母版；另起A/B/C和其待答前置已撤回。现已按140授权，以Call04为唯一像素参考制作专用舰态Candidate投影并接入T7。A25巡展舰03/04偏通用飞碟，失败人形和旧履带馆体不作正向源。见[来源纠错与当前绑定](../../../../../artifacts/formulas/experience-foundation-v1/chapter-art/wanji-t7-call04-v1/source-correction.md)。

**本轮新增研究：** [Y准备/接触/收势](../../../../../artifacts/formulas/experience-foundation-v1/video-study/srwy-contact-motion-20260919/README.md)比较五个用途不同候选后，采用白河愁ACE连续流程与常盘绿演出对照。ACE旧粗采样接触点按30fps加密，对照核手部准备及两次挥击；187采样点/177唯一源时间，主对话看过15联系板，保留14板与11关键原帧。补入体验语言第8条，搬运/拔锁仍是本项目待验改造。实际音频输入尝试明确返回不支持，原声未听辨。两视频20,037,389字节、连同冗余39,122,313字节已清理，不动原生QA。

**v10历史隔离小样（当前为上方v11，接续方向已改）：** [O Call04整架v10](../../../../../artifacts/formulas/production-lab-v1/builds/package-o-wanji-call04-v10/flow.json)，输入reader-o-wanji-call04-v1与reading/carrier-o-wanji-call04-v4。继续使用Call04及五张Z姿态原图；馆体配准v4留出后方地面，新增独立脚影/手点，完整钢架跟手拔离、放下，再由货柜领袖沿真实路线拖走。未改八格、规则和时长。render-v8对应包v10，333张实际GPU采样全部审过：329棋盘裁片、20张Z放大图及4张完整结果页；运动最大间隔97.402ms。78来源/75个规范化路径SHA匹配，五JSON重建一致，真实成功/失败结果67项、整架边界94项、生产器6项及Canon检查通过。**姿态仍跳，动作像提架而非抱架，钢架与舰身的固定连接、精确地面配准、其他伙伴/桥梁美术、原生与声音均未通过。** 见[第十版审核](../../../../../artifacts/formulas/production-lab-v1/qa/tactical-carrier-t7-20260919/root-review-v10.md)。下一步应处理抱架发力和原固定处，不继续只挪抓握点。3已选主场景、M/N两个功能预览、0完成包不变。

**v10阶段录制稳定性历史：** render-v7在275张后停于post-draw等待，首次留下进程采样；探针显示游戏仍在推进，根因尚未确定。录制器改用持久post-draw回调，每帧立即写JSONL；render-v8完整333张且日志逐条一致，仅证明本轮完整，不称长期卡顿根治。旧中断证据、1.5秒取样/5秒外部看门狗与250ms空窗门槛保留。最新CUA getState仍30秒超时，没有键鼠输入；用户已解锁，不再重复要求解锁。

**v10阶段原生复测历史（已被上方v11覆盖）：** 用户已确认Mac可操作。本轮CUA getState仍在30秒超时并重置；没有发送键鼠，不再把工具超时解释为用户仍锁屏。自动录制均已结束，无残留自建Godot录制进程；声音与原生操作未验证。

**此前研究继续复用：** [ITB实际撤销与双作者返回](../../../../../artifacts/formulas/experience-foundation-v1/video-study/itb-undo-return-20260919/README.md)补到铁板大河08:09.75指向“撤销移动”→08:10同机归位、可达区重开、同一回合保持，区别于关闭武器预览。另核两位作者的任务结束→成果→区域地图→下一任务；主来源有地区比较/任务预览，对照有机甲详情返回。撤销仍为单作者证据，原声未证。五个有界视频142,024,143字节及冗余文件共188,774,949字节已清理，保留10联系板/25关键原帧与来源、采样、结论；不重下已核区间凑数。

**第三个主场景的当前入口：** [C03E01「托住桥，拆掉锁」](../../../../../artifacts/formulas/experience-foundation-v1/chapter-tactical-source-fit-v1.md)，TAC_T7。[O路线试制v2](../../../../../artifacts/formulas/production-lab-v1/builds/package-o-carrier-route-v2/flow.json)已接真实隔挡、两格维修入口、牵住延后、拔主锁后重开与外圈维修路。入口仅在实际轮末合拢，草案/返回不付代价；占位中的身体不会被直接夹入障碍。抢进与牵住后分批进入均第5轮、余量8；绕外圈第6轮、余量7。“牵住”现为补救，不硬凑第三种已验策略。共同承重/全卸载和三锁后另轮留守保持，`mission_clear=false`。新整包路线261项与旧O/E/F、占位、承重及Python定向回归通过；50来源当前匹配、五份JSON重建一致，见[第三轮审核](../../../../../artifacts/formulas/production-lab-v1/qa/tactical-carrier-t7-20260919/root-review-v3.md)。**仍是中性几何开发入口，没有本包原生、连续身体接触或声音验收；3个已选主场景、M/N两个功能预览、0个完成章节包。** 旧O开发v2及其回执保留，旧源码哈希只代表当轮状态。

**此前T7现场演出（历史）：** 当轮入口为 [O现场结构v1](../../../../../artifacts/formulas/production-lab-v1/builds/package-o-carrier-worksite-v1/flow.json)。修复牵引回执未被识别、拔锁片段丢目标、准备阶段提前开放入口及无关敌方HP；补同场锁爪松脱、真实路径拖行、牵引线和承重结构，保留中性角色标记。三轮真实Godot渲染254/251/298帧，按画面返工场地尺度、标签与工作时长；最终逐帧查看91张工作动作，另核原尺寸关键帧。**自动API＋正常时钟渲染，不是原生键鼠、声音或体验验收。** 新演出9项/采样32项/整包路线261项及旧HP、E/F、占位、承重、Python回归通过；52来源当前匹配，五JSON重建一致，见[第四轮审核](../../../../../artifacts/formulas/production-lab-v1/qa/tactical-carrier-t7-20260919/root-review-v4.md)。角色身体动作、轮末接重/入口合拢连续演出、空黑结算卡和工程用语仍未解决；不计第三个功能预览、第二实质输入或完成章节包。上段路线v2为保留历史，其50来源只代表当轮源码。

**当前布局与舰体：** [布局图v2](../../../../../artifacts/formulas/experience-foundation-v1/chapter-art/t7-dock-layout-v2/dock-layout-v2.png)按当前输入/真实结果生成，已核两格入口、外圈固定隔挡、可触及拖行终点。它是规则图；v1坐标图和[万机馆A/B/C](../../../../../artifacts/formulas/experience-foundation-v1/chapter-art/wanji-structure-options-v1/review.md)只保留历史。A/B/C的待答项已撤回，当前使用Call04衍生舰体，不再等整馆身份选型。

**探索候选核源：** C01东侧撤离的单话、合成章、用户验收三项实际SHA与清单匹配，Reader头`user_review_pending`是未同步元数据；[源审计](../../../../../artifacts/formulas/experience-foundation-v1/chapter-exploration-source-audit-v1.md)已记录。机制稿把撤离/自由探索放在E01、E02转巨机护线，切片边界与可操作主体仍须整合，未计第四主场景。“人类不进后续巨机棋盘”不扩大成禁止探索段人类操作。

**上一轮N制作保留：** C02离港后的「新同伴的第一晚」已制作一个展陈活动：[package-n-first-night-v7](../../../../../artifacts/formulas/production-lab-v1/builds/package-n-first-night-v7/flow.json)。免费走近、两画改选、一次花费2/3、演出后同室换画/闲聊与独立结束，复用现有Hub结果底座。新房间、白鸢四姿势及两幅画均是Candidate；未复用被否决资产。已核完整runner的8张自动阶段图并修复脚踩长凳、图片溢出、过早完成提示、菜单内部编号。**没有本包原生键鼠证据，贴画接触/连续动作和完整三活动取舍未通过。** 详见[审核](../../../../../artifacts/formulas/production-lab-v1/qa/hub-n-first-night-20260919/root-review.md)。


**N的工程与来源证据：** 36项流程检查、19项Python生产器检查通过；旧Hub状态5270项、生产组合265项及choice回执12项通过。上轮v7的26条来源哈希匹配，四份核心产物另目录重建逐字节一致；本轮T7修改生产器和package runner后，这两条与当前源码不同，其余24条仍匹配，旧产物/会话保留，完整runner自动结束保留实际所选rescue及花费2。[资产源](../../../../../artifacts/formulas/experience-foundation-v1/chapter-art/n-first-night-v1/source-v1.md)保留原图、Blender源/.blend与几何注册。v1-v6为迭代历史；默认包索引未变，不能把两个画面选择计为两份实质输入。

**N原生停点：** 用户已再次确认“当前已解锁，可以操作”。本轮恢复CUA文档后重新`getApp(org.godotengine.godot)`，接口仍立即返回Mac locked；上轮重置后getState超时也保留为历史。接口与用户报告不一致，不断言用户未解锁、不重复要求解锁。PID23198的v7 native-v3进程重新核到仍在，目录仍只有首屏`00000.png`；没有新键鼠/F9/F10证据。保持会话，窗口通道有新状态时按[操作计划](../../../../../artifacts/formulas/production-lab-v1/qa/hub-n-first-night-20260919/native-plan.md)接回，不能盲信旧句柄。旧native-v1/v2及被SIGTERM的旧v3不计完成实录。

**调查M保留入口：** `package-m-scale-v18`，见[尺度、步态试验与取消行走复测](../../../../../artifacts/formulas/production-lab-v1/qa/cross-proof-m-c02-20260919/walk-scale-v1/root-review.md)。使用 v7 输入：纪存显示高度230、白鸢235，保留v15基础图集与标签；取消行走后清目的地并显示“选一处，走近查看。”。v17新左向图经实际试验视觉不通过，v18未采用；右向和20格新图也拒用，不复用为正向参考。默认索引、Reader、旧包和输入保留；工房未拿纪存冒充跌跌/机器犬。

v18状态测试218项、0失败，生产器13项及最终Canon严格检查通过。v18录后44项来源/33唯一文件相符；v17录后48项/36文件曾相符，随后消费者提示修复另建v18，不能把历史哈希当当前源码匹配。工程PASS不代表体验通过。

**M既有原生回执：** v17c保存377帧、v18保存136帧，均F10排空后exit 0，writer无错误、pending=0、forced_draw_count=0。全部513个状态、174个选定帧和12张联系板已核，含全部114个移动帧；另核6张全幅。v17c新左向四帧均真实出现，白鸢同场及判断页中断有证据；v18修复取消意图，返回原位，再次选对象才继续，未提前记证/引用/写事实。前后方向运动仍未作原生演示。首次v17启动未被CUA识别，v17b误点空地保存550静止帧，均不计成功运动证据。上述M实录会话已结束，不按M旧句柄续接；本轮N的新控制问题另见下段。原生启动使用实际 `/Applications/Godot.app/Contents/MacOS/Godot` 路径，小写Homebrew symlink进程本轮未被CUA按bundle识别。

**本轮画面仍未通过：** 人物相对桌面、凳子和门框的量级改善，标签仍可读，但这不是统一头身比或Q/SD定案。新左向图虽取消运动中插站姿，换腿仍不清楚、抬腿和停步生硬，故拒用；v18旧步态的大步/站姿跳换仍是缺口。检修、举本仍是离散姿势；完整机体/跌跌/机器犬、王者自主动作、声音与初见推理未完成。**M与N共2个功能预览（N未原生实玩），0个完成的章节验证包。**

[v12检修与白鸢实录](../../../../../artifacts/formulas/production-lab-v1/qa/cross-proof-m-c02-20260919/figures-v1/root-review.md)保留提前退出不记证、继续露印、完成重看与原件返回的证明；[v8回执](../../../../../artifacts/formulas/production-lab-v1/qa/cross-proof-m-c02-20260918/record-view-v1/root-review.md)保留查看/引用分离，v7留六图与路径，v5留成功链。不混用版本、来源哈希和会话。工房两版栏杆图仍未采用。

已完成的金标研究（各有范围与限制）：

- [Y双来源研究](../../../../../artifacts/formulas/experience-foundation-v1/video-study/srwy-source-screening-20260918/README.md)：比较五个候选后，实际分析两位作者的局部片段。第一来源观察地图信息、详情、地图对白、战斗HUD分层。第二来源用23:20–23:42半秒序列及23:42–24:40逐秒序列，补到武器/目标→摘要→返回换目标→新摘要→演出→地图局部结果→下一单位操作，见[实际操作链](../../../../../artifacts/formulas/experience-foundation-v1/video-study/srwy-source-screening-20260918/ace-command-chain.md)。未拿直播音乐设置/存档停顿测系统节奏。两源战斗HP栏可见性有差异、原因未证；第一来源加速控件高亮，不按标题判原速。
- [ITB前轮目的地与预览返回](../../../../../artifacts/formulas/experience-foundation-v1/video-study/itb-route-undo-20260918/README.md)：Wil P2的00:00–00:25半秒序列显示三处任务详情比较、任务预览和部署；另一作者04:25–04:40半秒序列显示武器预览关闭再进入，黄色教学框核为奖励目标。[本轮增量](../../../../../artifacts/formulas/experience-foundation-v1/video-study/itb-undo-return-20260919/README.md)已补实际移动撤销及两作者成功战后返回，不再沿用“全部未证”旧停点；攻击后撤销、失败撤退和不同路线长期后果仍未证。
- [金偶像双来源序章](../../../../../artifacts/formulas/experience-foundation-v1/video-study/golden-idol-prologue-20260918/README.md)：四个候选中选两作者，实际查看现场/思考往返、局部填写与完成过程。两源都区分收齐词语、分区正确和整案完成，主来源另看到回案例画廊。已撤回小联系板上“已完成分区退回未完成”的误读，原帧显示仍保持绿色，不能用于事实撤回规则。
- [Obra Dinn双来源确认](../../../../../artifacts/formulas/experience-foundation-v1/video-study/obra-dinn-confirmation-20260918/README.md)：四候选中一条初见不可下载，不计观看；主来源17:10–18:20每2秒、对照19:00–19:50每秒序列补到填写→三人查证提示→对应书页由手写变排字→回到回忆场景，对照另见子菜单返回改选。不可编辑权限、全部错误规则、原声仍未证。
- [Outer Wilds同题双来源](../../../../../artifacts/formulas/experience-foundation-v1/video-study/outer-wilds-quantum-20260918/README.md)：四候选中选SmaltSoda与Shrikezw。主来源06:00–07:35逐秒、对照09:00–11:20每2秒，看到读规则、保留照片、改变位置/观察、穿过拱门并进入下一条件；主来源10:15–10:44逐秒另见回飞船日志。跨地点量子卫星应用、对照日志返回、原声仍未证。301采样点中104只作概览定位，197为上述较密序列；保留必要21原帧，不以帧数作为完成指标。
- 截至Outer Wilds一轮，累计十九份研究视频1,017,932,406字节及冗余帧/临时文件已删除，总清理1,177,322,799字节；保留来源、区间、采样数据、必要图证和结论。r2/r3/r4临时目录均已不存在，没有动原生QA或游戏资产。后续XCOM与Banner清单单列如下。
- [OG既有实玩复核](../../../../../artifacts/formulas/experience-foundation-v1/og-existing-play-review.md)保留原结论：两张已查原图含约200%速度及静音，旧笔记含焦点/输入混杂。菜单与状态证据可用，正常节奏、原声和时延未证。
- [XCOM 2战后两来源](../../../../../artifacts/formulas/experience-foundation-v1/video-study/xcom2-aar-20260918/README.md)：六候选筛选后，实际查看关辉志P3的37:10–40:40每2秒序列及82年份可口可乐当前P44的14:50–17:40每2秒序列。任务结束→返航→逐人状态/详情返回→基地/世界的链已补；主来源同一伤情在基地个人页仍可见，对照接到后续编队。对照明显有外观模组，只辅助比较层次；未证失败撤退、原声、恢复过程或所有受伤者的出场资格。体验语言第4条已补对象和后果的连续表达；两段临时视频及冗余帧按[清理回执](../../../../../artifacts/formulas/experience-foundation-v1/video-study/xcom2-aar-20260918/cleanup.json)清除，未动原生QA。
- [Banner Saga代价延续](../../../../../artifacts/formulas/experience-foundation-v1/video-study/banner-saga-continuation-20260918/README.md)：四候选中选两作者，实际分析主来源06:40–11:58与对照07:38–11:50的1秒/2秒序列。战后回人/营地、明确休息、行军事件及后果到下一地点已取得有界证据；最终选项、补给减号和个人页“杀戮”由主对话原帧核正。两源第一个事件同选赠物资，不能当不同分支实验。保留27联系板/19必要原帧；两份视频105,318,913字节及其他临时文件的清理见[回执](../../../../../artifacts/formulas/experience-foundation-v1/video-study/banner-saga-continuation-20260918/cleanup.json)。多目的地选择、完整Hub生活与原声仍未证。
- [Citizen Sleeper行动与周期](../../../../../artifacts/formulas/experience-foundation-v1/video-study/citizen-sleeper-hub-cycle-20260918/README.md)：四候选中选两作者，主来源补预览取回/改放、执行反馈、结束循环及回到旧工作进度；已有进度的对照补喂猫后具体对象回应、自我修理和独立的结束周期。主对话原图确认08:28结束按钮→08:38新骰子，纠正把它仅当转场的初读。293个较密采样点含7点重叠细查；保留26联系板、2环境联系板、16关键原图。两份视频239,602,004字节及临时文件已按[回执](../../../../../artifacts/formulas/experience-foundation-v1/video-study/citizen-sleeper-hub-cycle-20260918/cleanup.json)清理。新工作规则第7条接入00c的免费查看与至多3次高价值安排，未移入骰子/生存衰减；该轮未覆盖的Hades增量见下一项，风花雪月和声音仍待研究。
- [Hades返家与生活动作](../../../../../artifacts/formulas/experience-foundation-v1/video-study/hades-house-20260919/README.md)：主对话复筛四条B站实况后，采用追风却九尾P1及红蔷薇与猫ii第二集。实际有序帧补到返家、接近、抚摸接触回应、肖像交谈与返回、工单购买保留；0.25秒细查确认杜莎结束交谈后飞离，不是永久站在原处。411采样点含25个重叠点，28正文联系板、4定位概览板及23必要原图已审。三份视频149,411,664字节及临时文件已按[回执](../../../../../artifacts/formulas/experience-foundation-v1/video-study/hades-house-20260919/cleanup.json)清理。第7条补空间、身体、情境动作和后续行为的联系；480p视频无音轨，不提供本作步态帧数/速度/头身比，也未通过当前美术。风花雪月仍只在筛选阶段。
- [风花雪月活动与离开](../../../../../artifacts/formulas/experience-foundation-v1/video-study/fe3h-monastery-20260919/README.md)：上述Hades轮次后，主对话取片纠正A/B初选，以D等离子Natural与新增G星尘研完成366采样点（350唯一）、28正文联系板与21关键原帧的查看。确认合唱后先扣次数再演出；烹饪预览退出不扣；G三次用餐后归零仍可走动交谈，另行结束才推进日期。G标题6月22日，实际主区间为6月29日，已纠正。四份视频371,441,316字节及冗余帧按[回执](../../../../../artifacts/formulas/experience-foundation-v1/video-study/fe3h-monastery-20260919/cleanup.json)清理；源码静查确认现有Hub有post_cycle同室结果查看，后续复用，不能假报缺失。完整讲习/休养/出击形态、长期关系回呼、原声和亲手体验未证。

金标研究方法是本地有序视频帧分析，未听辨原声，不冒称整段实时影音观看或亲手测试。第一批[体验语言工作规则](../../../../../artifacts/formulas/experience-foundation-v1/experience-language.md)已有七条；新增C02样例已开始局部实际验证，完整语言仍未完成。七条规则不是七包完成。来源比较、实际观察与后续问题统一见[gold-research.md](../../../../../artifacts/formulas/experience-foundation-v1/gold-research.md)；不回退到Wiki和经验代填。

**首包来源：** [C02E03「工号在漆下面」](../../../../../artifacts/formulas/experience-foundation-v1/chapter-slices.md)。E03/章Reader/验收回执实算哈希与C02故事链一致；当前原剧情、独立Candidate解构与INV_T1原类型相符。已明确玩家查看/提出解释、角色专业判断、三类证据、S2局部退出和必要Candidate美术，当前实现范围以上述实际回执为准。无牌一号为V353U071，完全版王者为MECHA_C02_COMPLETE_KING；V353U048是旧拳王。白鸢CML011候选原图已实际查看，两机在已查登记表中未找到当前图像锁，不冒称全库无图。

**下一项实质工作：** 按战场构建方案与dock-field首轮审核，先验证同一现场中的可达路面、机体脚点、舰体体积、桥跨、锁架连接及准备→接触→受力→脱开→落定；环境、身体和镜头共同处理，不回退到只挪坐标/换姿态。逐帧发现原地朝向、等待等引擎记录被当作独立演出空拍：先核哪些记录没有可见变化，保留真实转向、关键起手和预警，再做显示层节奏修正。若分层2D无法做到需要的遮挡与身体连续性，做独立局部接触技术对照并列出3D资源代价，正式迁移仍需具体样片后的用户确认。原生工具恢复后实际点选、改路、取消、共同执行与同场结果；本轮自动按键/坐标分发测试不等于亲手操作。N同室生活、M工房、其他四主场景、每公式两份输入/组合、剩余金标和声音继续按140；3已选主场景、M/N两个功能预览、0完成包不变。

接手完整读本文件与[140唯一目标](140-formula-lab-integrated-visual-production-goal.md)。[142 GLM交接](142-formula-lab-astra-handoff.md)只查增量；137查生产合同，138/视频账查找片线索，00c查本项目气质与规则。旧融合表不是已证标准；不沿用“只差签字和六项裁决”，不让用户先填表，不重载旧对话。

待答Google外部服务方案仍未批准、未登录、未调用，不因用户提供下载网站而扩为外发授权。此前SnapAny成功解析但直链403/客户端入口的尝试已结束，现用本机现有yt-dlp与FFmpeg。历史141保存在[_history/研究修订前](_history/141-formula-lab-fresh-session-handoff-before-gold-research-correction-2026-09-18.md)及[_history/更早停点](_history/141-before-experience-goal-2026-09-18.md)，按需查，不叠加旧全文。

## 2. 已核到的新进展及证据范围

以下为 09-18 主对话对磁盘代码、JSON、报告与部分原PNG的核查；不是对全部新增帧的逐帧审查，也不是用户验收。

| 项目 | 核到什么 | 仍不能据此宣布什么 |
| --- | --- | --- |
| A 新录制 | `qa/investigation-onsite-20260910/gui-a-manual-v3/` 329 PNG与索引一致；00328为真实成功结果对白，状态为A_RESULT、2/3段、LOW_GAIN_PASS=true；v4另有5帧回源过程 | v3 final字段已回A_INTRO，不能拿它作3/3终态截图；需要某一终态时定向补证，不因此重录全部A |
| B 成功与中止后离开 | success-v1 201帧；activestop-v4 4帧。final均为2/2、result；前者BRACE_PASS/TOOL_LEFT=true，后者仅ABORTED_SAFE=true。已看成功回执与中止结果对白原图 | 成功片末PNG是结果卡，完成状态另来自final；不能混称每一步均有原图。v1/v2各1200帧封顶，不能当完整离开过程；v3仅1帧失败录制 |
| B 未开始 | neverstarted-v1 3帧，00002已到B_RESULT对白，未写成功/中止事实 | final又处B_TEST，不能宣称有最终汇总原帧 |
| 写盘状态 | 上述capture的帧数与PNG数相符，writer pending=0、errors=[] | 只证明记录落盘。GLM所报138源零漂移还须定位对应录后证据；主对话本轮只找到明确的录前文件和较早baseline录后文件，不把会话文字当新核验 |
| 键盘回到来源 | `investigation_lab_shell.gd`已有ROW_SOURCE导航与J回跳；`investigation_config_input_flow_test.gd`已有回源检查 | 事实Widget当前未为SRC焦点实现高亮和自动滚动。代码级缺口已观察，实际玩家影响仍要在新评估中核验 |
| 采集器 | `production_manual_package_capture.gd`已有检查点完整readback与`--max-frames` | 不补造修改前录像中缺失的状态/画面 |
| 测例与换输入 | 七公式现存test/swap报告gate_pass均true，共24档案例；战术报告实际覆盖T0–T3且仍报18项能力缺口 | 不是七公式体验完成、不是T4–T11实现完成。本轮未重新执行这些测试 |
| 引导与生产增量 | A onboarding-v2有四句前言；package browser有“怎么玩”面板；K rebuild-proof有输入、产物和重建说明 | 四句说明未证明解决首玩困惑；改一句台词不计第二实质输入；编辑后完整实玩来自GLM记录，未在本轮重做 |

上述调查QA目录前缀：`artifacts/formulas/production-lab-v1/`。
GLM会话细节在 `qa/investigation-onsite-20260910/gui-a-manual-v3-session-note.md`、`gui-b-routes-session-note.md`。
十包实玩、D/H补全等已有记录应复用；需要更强结论时查所需帧和状态，不把“勿重做”解释成禁止核实或禁止针对缺口复测。

**09-10 的锁屏停点已被后续新增录制越过。** 不再按旧PID70997/session51887续接，不预设今日仍锁屏或仍有同一进程；实际操作时重新确认当前进程、包、窗口及用户占用情况。

## 3. 当前入口：默认列表与隔离变体分开

唯一默认Candidate索引为 [current-packages.json](../../../../../artifacts/formulas/production-lab-v1/current-packages.json)，本轮未改。目录均相对 `artifacts/formulas/production-lab-v1/builds/`：

| 包 | 默认目录 | 承担体验 |
| --- | --- | --- |
| A | package-a-briefing-v1 | 同场前言→调查试验→结果对白 |
| B | package-b-onsite-v2 | 承力/交割试验，成功/中止/未开始各自承接 |
| C | package-c-exploration-actors-v1 | 器材棚走近、观察、问人、路线计划 |
| D | package-d-exploration-actors-v1 | 三空间线索、归档与知识开路 |
| E | package-e-registered-map-v1 | 固定擂台与真实战损结算 |
| F | package-f-registered-map-v1 | 限时穿越、动态阻挡、撤出与失败 |
| G | package-g-environment-v2 | 派遣→器材棚巡访→真实报告 |
| H | package-h-environment-v1 | 派遣→三室观察归档→路线报告 |
| I | package-i-hub-in-room-v1 | 自然返馆、闲聊、安排、同室后果 |
| J | package-j-hub-review-v1 | 试验约束复核、书页标记与现场查看 |

较新隔离入口：

- A `package-a-manual-v1`、`package-a-onboarding-v2`；B `package-b-manual-v1`。
- F `package-f-lookdev-v1`；K战术对抗已审入口 `package-k-tactical-duel-v1`，见原T3主审，不与下条K混名。磁盘另有K战术v2，启用前核它自己的来源与验证范围。
- K编辑重建证明 `package-k-rebuild-proof-v1`，是C内容变体，不是新的战术输入。
- L/T1 `package-l-camera-v1`。
- O/T7 当前隔离入口 `package-o-wanji-call04-v10`：Call04配准v4、Z独立手脚点与整架拔离，现场结果页沿用。`wanji-call04-render-v8`有333张本版采样，全审见第十版审核；中间v9包/render-v7中断275PNG及采栈保留。v8包及更早各录制只证明其当轮源码，不混称新包实录。dev-v1为被拒包；A/B/C不绑定、不作正向源。
- M/C02E03最新制作变体 `package-m-scale-v18`：v7输入保留基础图集并校准显示尺度，取消行走提示已原生复测。v17四格新步态试验不通过、不得复用；v16仅静态尺度校准。v14/v15同场与标签、v12检修/白鸢、v8查看/引用分离、v7六图与路径和v5成功链按各自范围保留，不混用版本与会话。

A v2没有进入默认索引。体验评估应核对“用户真正打开的入口”与待测变体，不能看着v2说明去验旧A，也不为追最新直接覆盖默认。隔离变体不计新增实质输入。

统一浏览场景：`game-godot/scenes/formula_lab/formula_lab_package_browser.tscn`；单包场景：`game-godot/scenes/formula_lab/formula_lab_package.tscn`。单包可按各自REBUILD.txt启动/重建；先验证文件存在，再选当前入口，不按名称猜“latest”。

## 4. 新目标起点与尚未交付的内容

- **金标研究尚不足**：先区分已操作、原生视频分析、本地有序帧分析、只有离散抽帧、只有文字。复用机战OG实机记录，补齐140§4实际借用的各层。每段要记录来源、实际观看区间、操作与结果、画面/声音/节奏、返回和误操作；链接、字幕或联系板不代替观看，视频观察不冒充亲手手感。
- **统一语言尚未完整建立**：已有七条有来源的工作规则，首个切片已开始局部实测并反向修正规则。动作、声画及其他未研究层尚未定案。原融合表和问题清单仍不能作为已证标准。
- **七个新增章节包尚未选满**：C02E03三方互证与C02航程展位已有功能预览（N未原生实玩）；T7 C03E01托桥拆锁已有可重建且完整消费者通过的中性几何开发入口，但未成有美术、连续动作与原生证据的章节场景；其余四个主包继续核有效Reader、机制解构和身份来源。允许同章不同场景和必要公式衔接，与旧假设包并存，不把旧包改名充数。完成的章节验证包仍为0。
- 其余六类已有[具体来源池](../../../../../artifacts/formulas/experience-foundation-v1/chapter-source-candidates-v1.md)：导览照片、托桥拆锁、东侧撤离、归港后果、紧急离港及生活候选。原7项核源保留；Hub本轮另核C02E05/C03E01/两章验收及C02拓扑5项哈希，收束到离港后的第一晚，明确固定事实与新增适配。Hub已进入单活动制作，仍不计完整；其他候选不计选满或完成，路线保留C01馆体视觉门槛。
- **新增美术只完成局部试制**：两房间背景、六份原件图、近端检修和白鸢三姿势已绑定并局部实录；整体人物尺度未统一，工房两版未采用，完整角色/机体与连续动作未完成。Candidate 制作授权继续有效，失败资产不复用。
- **整体体验评估尚未完成**：首份评估已对照实际金标与C02原生操作并修正具体问题；不是初见玩家评估，也未覆盖七公式。每公式两实质输入、至少两套组合及编辑重建范围继续保留。

产物位于`artifacts/formulas/experience-foundation-v1/`：`gold-research.md`已有多来源筛选、实际序列、纠错和媒体清理；`experience-language.md`为第一批有来源的工作规则；`chapter-slices.md`记录首包方案与当前实现；`experience-review.md`记录首轮实际体验缺陷、修正与后续。研究、完整语言与七包均未完成；文件创建不计研究/体验通过。

已有疑问保留供研究和后续验证：A的情境与动机薄弱、菜单工程化，事实卡键盘回源缺少可见焦点/自动滚动，F成功路线尚缺本轮证明，人物生活动作与机体接触不足，结果是否真正交给下一段。它们不限定全部研究结论；E成功不证明F可解，多写四句引导不证明首玩已改善。

## 5. 自主工作与待答边界

- 主对话自行负责金标研究、统一语言综合、七包选材、验证资源规划、普通制作适配、缺陷修复、实际试玩及生产回写。新目标按140顺序执行，不先让用户完成技术问卷；旧重大待答事项未自动获准。
- 万机馆A/B/C待答项已撤回：漏读了用户已选Call04的后续回执。按既有140授权使用该母源制作Candidate专用投影；不用重新选身份，不升正式Runtime/Canon。
- T4新对抗核心、T1教练人类段、T5后段取盾来源冲突、WR第二周期具体文本/后果保留裁决边界；只阻塞依赖它们的工作。T5首段护线/导流不依赖取盾顺序，不把所有工作等在问卷前。
- 三图紫机/白青机/靶机的RGB保留透明修复已获准且完成。第四灰炮机`mecha-si.png`与金机`mecha-ye.png`不在这三图许可内；前者实际用于E及F拦机甲，后者用于F拦机乙，不能按旧payload的doll字样换身份。
- 白青Blender母型、分件R1/R2、双人共骨架身份试验均未通过并保持停止；不续做这些失败资产的姿态/动画或默认替换。此限制不扩大为禁止所有新增章节验证美术。
- 本次新增章节选材与基于既定设计的Candidate验证美术按140§2、§5.4、§6.3直接执行，可补必要动作、表情和演出画面。保留原环境/空间制作、单人临时Lab试验与T3音效的适用授权；改变既定身份、核心规则或全局风格，以及新增付费、外发、正式晋升仍需具体方案和确认。
- 保留共享工作树，不add/commit/reset/清理，不改正式Reader、Canon、默认Demo或正式Runtime。模型按140§8.1实际能力/接口及总成本选择；主对话负责判断，不为派工而拆任务。

## 6. 既有成果入口：按问题查，不重做

以下相对 `artifacts/formulas/production-lab-v1/qa/`：

| 成果 | 证据入口及限制 |
| --- | --- |
| HP/E/F第二轮与三张alpha | `tactical-package-capture-v1/review-20260908-hp-motion/ROUND-REVIEW.md`；Full/Skip状态一致，不等于动作/声画/视觉通过 |
| A/B手册显示/鼠标/生产依赖 | `investigation-onsite-20260910/root-review.md`及新增两份session-note；旧Root报告锁屏段为历史，新证据以具体会话为准 |
| T3/K实际对抗与音效 | `tactical-t3-production-20260910/root-review.md`、`tactical-t3-production-20260910/native-audit/skip-fixed-v1-review.md`；原生Full/早K与真实PCM已取证，用户视听未验收 |
| T1/L相机、点选与交接 | `tactical-t1-camera-20260910/root-review.md`；79帧，R1运动已审，R2/R3未采到中间execute；未实现人类控制段 |
| F同源空间与视觉变体 | `tactical-lookdev-20260910/root-review.md`；250帧三轮真实运动及遮挡，最终失败；静态机体姿态/接触/整体美术未过 |
| G/H世界派遣与探索 | `world-route-production-20260909/manual-g-review.md`、`manual-h-and-branches.md`、`g-shed-depth-v2-root-review.md`、`h-environment-root-review.md`；场地行走/知识门已有证据，不是完整队伍和世界多周期 |
| J返馆复核 | `hub-review-production-20260909/j-review-root-review.md`；试验约束与书页变化已证，人物生活动作与声画未过 |
| 金标研究线索 | `investigation-onsite-20260910/obradinn-confirmation-source-note.md`；Obra Dinn作者文字不等于确认动画。Y指令菜单、XCOM编队AAR、Banner行军等按140§4.1、§6.1研究完整操作与反馈，不只补几张专帧 |

工具以当前安装为准，历史可用路径：Godot `/Applications/Godot.app/Contents/MacOS/Godot`；Blender `/Applications/Blender.app/Contents/MacOS/Blender`。原生采集使用fresh目录与当前拥有的进程；F8检查点、F9实录、F10排空。旧浮动宿主/keypost位于临时目录，仅在核实存在、代码、用途及窗口归属后选用，不根据142重建脚本的指令盲执行。

下一轮交接只写新增可见改善、实际证据、未通过和下一问题；不要继续把完整历史叠加到本文件。
