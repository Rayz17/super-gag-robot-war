# 纪存与馆守Z候选校样提示词 v1

> 生成路径：Codex 内置 `imagegen`。  
> 状态：`candidate_review`，未迁移 Canon，未做透明底、方向拆分与动画切图。

## 1. 纪存正比例

参考图：`core_jicun_stand.png`，仅用于身份与配色锚定。

```text
Redesign the referenced character Ji Cun as the same recognizable person, but mature him from boyish early twenties into a believable 27-29-year-old adult male protagonist and simplify the costume for repeatable game-art production.

Preserve his Chinese appearance, black hair, blue eyes, navy museum uniform, and left forearm archive terminal. Use a slightly longer midface, firmer jaw, eyes 10-15% smaller, flatter lower eyelids, stronger neck and lean broader shoulders. No glasses or facial hair. Mature through bone structure, gaze and posture, not aging symbols.

Use only a clean white shirt, one dark navy museum field coat, straight dark trousers, practical navy boots, one flat chest ID, and the left forearm terminal as the single complex accessory. Remove lanyards, dangling badges, repeated pockets, straps, decorative zippers, gold-line overload, labels, scratches and weathering.

Modern moderately stylized game character art, clean cel shading, restrained semi-painted materials, thicker outer contour, minimal internal lines, two-level shadows. Single full-body three-quarter standee on a plain light neutral background. No text, logos, inset portraits, Japanese writing or watermark. Avoid teenage face, giant eyes, baby face, middle age and ornate fashion posing.
```

## 2. 纪存Q版

参考图：本轮纪存正比例候选为身份母版；旧Q版只作为反例。

```text
Create a production-simplified Q-version of Ji Cun that faithfully inherits the adult identity, face, clothing, colors and left forearm terminal from the new full-body master. About 3.4 heads tall, adult-coded face, moderately sized eyes, clear jaw, straight shoulders, stable stance and enough leg length. He must not read as a child, mascot or schoolboy.

Keep only three identity anchors: simplified black hair silhouette with five large clumps; clean navy field coat over one white shirt block; left forearm rectangular archive terminal plus subtle white hand glow. Use 4-6 large color groups. Simplify the terminal to one shell, one pale screen and two bands. Remove all lanyards, dangling tags, shoulder emblems, extra straps, pockets, piping, tiny zippers, labels, scratches, textures and micro-folds.

Modern game-production chibi, thick outer contour, sparse internal lines and two-level shadows. Single full body on a light neutral background. No multiple poses, captions, Japanese writing or watermark. Avoid two-head mascot proportions, giant eyes, round baby face and accessory clutter.
```

## 3. 馆守Z正比例

参考图：`guardian-z-user-selected-base.png` 锁定旧机身份；前两次减法试验只用于确认“不能简化成泛用勇者系”。

```text
Refine Guardian Z so it keeps readable heroic proportions and low production complexity, while retaining the approved old museum-guardian identity, material weight and color rhythm. It must not become a generic smooth Brave robot and must not return to tiny engineering noise.

Keep the amber eyes, silver slatted mask, blunt museum-roof gold crown, round deep-navy shoulder shells, pair of red archive-door chest plates, post-C01 missing RIGHT forearm on viewer's LEFT, intact large LEFT fist on viewer's RIGHT, and long-legged seven-head body.

Use a central red archive-key block, two tall blunt gold roof pylons and two short side eaves. Put one broad rotating-plinth joint ring behind each shoulder. Make the red chest doors thick, hinged and stepped around a narrow deep-blue catalog-drawer spine with one hollow gold circular seal. Add only large stepped planes, one cool-gray knee plate per leg and one broad red-ivory-gold band on the squared intact left forearm. The missing forearm ends at a clean gold-ringed recovery socket without cables.

Limit the design to about 12-16 large shapes. No panel grids, rivet fields, labels, tiny vents, serial numbers, scratches, paint chips, grime, repeated pinstripes or all-over gold trim. Modern distinctive mecha game art, medium stylization, cel shading with broad hard-surface highlights, thick outer contour and sparse internal lines. Single full-body three-quarter stance on a light neutral background. No V-fin, direct IP copy, wings, cape, weapons, diagrams, text, logos, Japanese writing or watermark.
```

## 4. 馆守Z Q版

参考图：本轮馆守Z正比例候选为身份母版；旧Q版只作为细节密度反例。

```text
Create a clean Q-version of Guardian Z that faithfully inherits the final adult-proportion design. About four heads tall, compact but not round or toy-stumpy, with enough leg length and a tight waist.

Preserve four anchors: architectural gold crown and silver mask; two red archive-vault chest doors around a narrow blue spine and hollow gold ring; intact large left forearm and fist on viewer's right with one red-ivory-gold band; missing robot-right forearm on viewer's left ending at a clean gold-ringed elbow socket.

Use five dominant color groups and 8-10 large armor blocks. Each shoulder is one navy dome plus one gold edge; each leg is one navy block, one gray knee plate and one gold toe frame. Delete all bolts, rivets, panel lines, labels, scratches, weathering, tiny vents and texture. Modern game-production Q mecha, thick outer contour, sparse interior lines and two shadow levels. Single full body on a light neutral background. Avoid two-head proportions, giant head, very short legs, both fists present, wrong missing arm, photoreal rendering and dense surface noise.
```

## 5. 馆守Z C01E02 收藏母版 A稿

参考图：`guardian_z_standard_candidate_v1.png`，仅保留图三的比例、配色和明亮现代呈现；机设本身重新建立。完整规格见 [收藏母版生成规格](art-delivery/sources/guardian_z_collector_master_gpt_image_2_prompt_v1.md)。本轮在 Codex 内置 `imagegen` 执行，不声明底层模型。

生成约束：

- 单机、前3/4、双臂完整等长、无场景背景和文字。
- 6.8–7头身，经典飞拳超级系联想，但不复刻具体原IP零件。
- 必须显形万机冠、0号展门胸、三层转台肩、目录飞拳前臂、展台足。
- 收藏级高细节只集中在门铰、肩环内圈、飞拳导轨、手指、膝后和踝部；外甲保持大色块。
- 禁止缺臂、伸长臂、枪械、满身铆钉、随机划痕、伪文字、暗黑/异形化。

输出：`art-delivery/review/guardian_z_collector_e02_intact_candidate_v2a.png`。

## 6. 馆守Z C01E02 收藏母版 B稿

参考图：A稿，执行同一身份下的受控修正，不重新发明机体。

定向修正：

- 删除前臂外侧容易读成步枪/炮管的长条物，改为贴合肘部的飞拳分离环与短导轨。
- 保留可开启红胸门，但由直白矩形柜门改为斜切档案百叶；减少小铰链和碎分件。
- 头部放大约5%，银面罩略加宽；金冠两侧降低并横向展开，避免普通V字冠读取。
- 大腿、小腿、脚和前臂外甲碎线减少约20%，肩环、胸门、肘环、手指和关节内构继续保留收藏级细节。
- 双臂完整等长，不增加武器、损伤、文字或背景。

输出：`art-delivery/review/guardian_z_collector_e02_intact_candidate_v2b.png`。

## 7. 馆守Z现代化 C稿

参考图：B稿。目标不是减少细节，而是移除复古超合金视觉语法。

- 色彩权重调整为约68%墨蓝、16%象牙白/银、10%红、3%香槟金属、3%微白/琥珀光；取消金边包甲。
- 完整肩环改为带缺口的开放偏置转台弧，利用负形而不是金色描边形成记忆点。
- 柜门胸改为沿斜轨滑开的红色档案闸片；前臂从圆筒改为渐收飞拳壳体。
- 比例提高到约7.2–7.4头身，腰腿形成连续流线，脚掌降低为稳定楔形。
- 保留双臂完整等长、飞拳分离环、馆藏修复材质和收藏母版细节。

输出：`art-delivery/review/guardian_z_collector_e02_modern_candidate_v3c.png`。

## 8. 馆守Z现代经典平衡 D稿

参考图：C稿，同一机体受控回调。

- 开放肩弧缩小约20–25%，靠近肩轴，避免读成翅膀或光环。
- 头部放大约6%，银面罩加宽；冠角保持低平建筑感。
- 胸腔加深加宽约8%，红色闸片形成轻微错位，不回到完美对称柜门。
- 前臂中段增宽约8%，大腿与小腿恢复飞拳主角机的承重感。
- 严格保持C稿的低金色占比、现代负形和等长双臂。

输出：`art-delivery/review/guardian_z_collector_e02_modern_candidate_v3d.png`。

## 9. 馆守Z二维图形画风 E稿

参考图：D稿。只验证绘制风格，不主动重设计零件。

- 用粗细分明的二维硬表面线稿、平面色块、两级赛璐璐阴影替换产品渲染。
- 取消塑料/金属玩具高光、装甲渐变和摄影棚商品图质感。
- 高细节通过线条层级组织，不通过纹理、划痕或面板网格组织。
- 微白/琥珀光只出现在眼与胸核，不做霓虹外描边。

输出：`art-delivery/review/guardian_z_collector_e02_modern_graphic_candidate_v3e.png`。

## 10. 馆守Z C×A融合 F稿

双参考职责：C稿锁现代轮廓、开放肩弧、斜轨胸闸、流线腿与低金色；A稿只提供胸、拳、腿的重量、零件厚度和玩具机构清晰度。

- 目标约6.9–7.1头身，胸腔增宽加深10–12%，前臂增厚12–15%，大腿/小腿增厚8–10%。
- 颜色改为墨蓝主甲、选择性高纯钴蓝转折面、清亮朱红、冷白/银、极少淡香槟机构和微白/暖琥珀光。
- 禁止A稿的完整圆肩环、柜门胸、圆筒前臂、厚方靴、金边和红蓝金均分。
- C01E02双臂完整等长；无青光、文字、武器和损伤。

输出：`art-delivery/review/guardian_z_collector_e02_ca_fusion_candidate_v4f.png`。

## 11. 馆守Z C×A增重融合 G稿

参考图：F稿，只修体量，不再换机设与色板。

- 调整到约6.8–6.9头身，头部放大约4%，胸腔加深，上臂增厚约10%，前臂增厚约12%。
- 大腿增厚约12%，小腿增宽约10%，脚掌仅增宽约5%；降低重心并稍微扩大站距。
- 保留窄腰、开放肩弧、斜轨红闸、渐收飞拳壳、钴蓝转折面和低金色占比。
- 两臂工程长度严格一致，不用伸长、透视错觉或损伤表达体量。

输出：`art-delivery/review/guardian_z_collector_e02_ca_fusion_candidate_v4g.png`。

## 12. 馆守Z A母体现代化 H稿

参考图：A稿。A的体量和头冠改为不可牺牲的主角机锚；现代化只改配色、材料、装甲平面和细节分配。

- 保留约6.5–6.7头身、深宽胸腔、粗肩臂、巨大飞拳前臂、承重腿和宽足。
- 强化五段主角冠：中央红目录钥、两根高主屋脊、两段低侧檐；不得削成细横杆或圆滑头盔。
- 肩部保留完整展台环和巨大体量，但圆顶改为大块斜切面；胸门保留厚度，减少柜门铰链。
- 使用墨蓝主甲、少量钴蓝转折面、清亮朱红、冷白/银，以及集中在冠与真实机构的淡香槟金属。
- 两臂完整等长；禁止纤细化、开放光环肩、金边包甲、武器和损伤。

输出：`art-delivery/review/guardian_z_collector_e02_a_modern_candidate_v5h.png`。

## 13. 馆守Z厚钝屋脊冠 I稿

参考图：H稿，只调整冠形，不改身体与配色。

- 中央红目录钥保持高而厚。
- 两根主屋脊缩短约15%、加宽约20%，尖端改为钝梯形。
- 两段侧檐缩短、增厚、趋于横向，采用阶梯式建筑端头。
- 四块冠件连接到可见深蓝眉架，避免漂浮星芒感。
- 保持黑影识别、头部非圆滑化和双臂等长。

输出：`art-delivery/review/guardian_z_collector_e02_a_modern_candidate_v5i.png`。

## 14. 馆守Z A母版全身识别 J稿

参考图：只使用A稿。H/I被用户否决，禁止继承其五段星芒冠、钴蓝跳色或身体造型。

- A稿约6.7–6.9头身、巨胸宽肩、粗前臂、承重腿、宽足与原三段冠基本不动；不得瘦身、增高或增加任何冠角。
- “馆藏转轴”统一肩、飞拳分离环和膝外轴：深色分度转台配三段淡香槟锁扣，不画成整圈金轮胎。
- “展门折线”统一红胸门、前臂外壳和小腿前甲：每处只用一条大折线，不铺高达式密集分甲。
- “目录脊柱”连接红色头顶目录钥、象牙白胸中轴、腰扣和脚背短脊。
- 删除枪状前臂外挂；双前臂改为等长、同源、带完整环形分离缝和两段锁扣的飞拳舱体。
- 配色约58%墨蓝、15%朱红、17%象牙白/银、5%深枪灰、3%淡香槟、2%暖琥珀/微白；取消独立钴蓝色块，金色面积比A至少减少三分之一。
- 高细节只在胸门铰链、肩环内圈、肘部接口、手指、膝后与踝部；无文字、编号、日文、伪文字、随机磨损、武器和背景。

输出：`art-delivery/review/guardian_z_collector_e02_a_fullbody_identity_candidate_v6j.png`。

## 15. 馆守Z重冠展架 K稿

参考A稿体量和J稿已成立的银色脸谱、粗飞拳，不继承J的小圆帽、整圈金属环和对称柜门胸。

- 建立由前额眉架、中央红色目录钥、中央冠壳、左右侧后盔壳和颈部接口组成的完整头盔。
- 以“断环 + 目录钥”贯穿全身：肩部为向前开口的厚C形承力弧，胸部为红色断环括号夹住象牙白目录脊柱，膝与脚背只做克制回声。
- 双前臂为等长同构旋封飞拳：三片外壳围绕分离环，发射前可旋转闭锁；不得成为炮管或伸长臂。
- 保留A稿深宽胸腔、粗肩臂、承重腿和宽足，降低金属金面积，采用墨蓝、冷白、清亮朱红和少量香槟金属。

输出：`art-delivery/review/guardian_z_collector_e02_heavy_crown_frame_candidate_v7k.png`。

## 16. 馆守Z断环飞拳 L稿

参考K稿，收紧而不削弱整机符号。

- 肩部C形承力弧缩小并贴近肩轴，不得形成外挂光环或翅膀。
- 红色断环胸框保持厚而简洁，中央象牙白目录脊柱贯穿头、胸、腰和脚背。
- 左右旋封飞拳必须工程等长、严格镜像，红色楔形外壳、三片旋封甲和深色分离环完全同构。
- 头盔保留完整冠壳和后脑体量，但不增加星芒式长角；整机保持6.6–6.8头身的厚重主角比例。

输出：`art-delivery/review/guardian_z_collector_e02_compact_broken_frame_candidate_v7l.png`。

## 17. L稿头雕三角度诊断

只展开L稿头雕的正面、前3/4和严格侧面，不重新设计脸谱。

- 检查中央红钥是否嵌入盔壳，而非贴在圆帽上。
- 检查金属眉冠是否由深色眉架承托。
- 检查侧后盔壳、耳部圆形接口和颈部装甲是否形成一个完整头盔体积。
- 无文字、无场景、无胸部以下机体；用于识别叠片数量、负形和侧面轮廓问题。

输出：`art-delivery/review/guardian_z_head_sculpt_l_three_view_candidate_v7l.png`。

## 18. 馆守Z圆帽简化 M稿

作为内部失败对照，沿用L稿身体，只把头部简化到接近下限。

- 删除连续侧后盔片，只保留圆滑主帽、短中央红钥和低平金属眉条。
- 不得改动肩胸断环、旋封飞拳、体量或色板。
- 目的不是提供生产候选，而是验证“少零件”何时会退化为无主角感的圆帽。

输出：`art-delivery/review/guardian_z_collector_e02_plain_helmet_control_v7m.png`。

## 19. 馆守Z三块盔壳 N稿

以L稿身体为唯一父级，在L的过度分层和M的圆帽朴素之间重做头部。

- 头盔只保留三块主质量：一块带屋脊折面的中央冠壳、两块从太阳穴连续包覆到后脑的左右侧壳。
- 中央红色目录钥完整嵌入中央冠壳；香槟金眉冠短、厚、有深色眉架支撑，不形成星芒或普通V字天线。
- 银色脸谱、琥珀眼、耳部圆形接口和颈部装甲保持清楚，但不得以细碎叠片填满侧面。
- 身体、断环肩胸、双臂等长和旋封飞拳完全沿用L，不用更换身体掩盖头雕判断。

输出：`art-delivery/review/guardian_z_collector_e02_balanced_vault_helmet_candidate_v7n.png`。

## 20. 馆守Z高断拱冠 O稿

沿用N稿全部身体，只验证更强的头盔黑影上限。

- 中央红色目录钥保持嵌入式厚冠；左右深蓝断拱侧壳从太阳穴向后上方展开，与中央冠保留清楚负形。
- 侧壳必须是完整承力盔壳，不使用金色长角、细天线、星芒冠或鬃甲叠片。
- 金色只在眼线上方形成短承托边；脸谱、耳部接口、后脑体量和身体完全不动。
- 本稿用于测试主角剪影强度，不直接视为生产候选。

输出：`art-delivery/review/guardian_z_collector_e02_high_vault_crown_control_v7o.png`。

## 21. 馆守Z低断拱冠 P稿

参考O稿，只收敛其兽角/虫颚风险，不改动N/L身体。

- 左右深蓝侧冠高度降低约30–35%，以向后展开为主，只轻微上扬；末端为宽而钝的建筑切面，不是尖角。
- 中央红色目录钥必须成为头部唯一最高点，并与左右侧冠保留清楚负形。
- 头盔仍只有中央、左、右三块主冠质量；后脑完整，耳部接口清楚，适合实体玩具拆件。
- 金色眉架只作短承托，不进入主要黑影；禁止普通V字天线、星芒、兽角、虫形、头发式小鳍和圆帽。
- 银色纵栅脸谱、琥珀眼、断环肩胸、旋封飞拳、双臂等长和全身配色完全沿用。

输出：`art-delivery/review/guardian_z_collector_e02_low_vault_crown_candidate_v7p.png`。

## 22. P稿头雕三角度验证

只使用P稿作为设计参考，展开同一头雕的正面、前3/4和严格侧面，不再改机设。

- 锁定宽银色纵栅面罩、短而有重量的下颌、琥珀眼、中央红钥、低矮深蓝侧冠、短香槟金眉架、圆形耳部接口和完整颈甲。
- 三个角度保持相同比例与零件数量；中央红钥始终为唯一最高点。
- 侧面必须证明侧冠并入后脑，而非独立兽角；全头仍只有中央、左、右三块主冠质量。
- 禁止身体、文字、标注、场景、普通V角、星芒、虫形、鬃甲叠片和随机划痕。

输出：`art-delivery/review/guardian_z_head_sculpt_p_three_view_candidate_v7p.png`。

## 23. 馆守Z九头身铰接X Q稿

多参考职责：截图锁L头盔基础；P提供紧凑断环、等长旋封飞拳和色彩层级；K提供胸肩重量；J只提供胸肩三轴铰与小点缀色。

- 鞋底至头冠约九头身，主要拉长大腿和小腿；小头、深胸、宽肩、粗拳、长腿、宽足同时成立。
- 胸前四块短红楔围绕象牙白中轴组成X，全部收在躯干；肩甲红白短斜片隔着铰链续写X，不做连续飞翼胸板。
- 每侧肩甲最多三块大甲，胸肩之间露出石墨三轴铰、单枚香槟锁和小状态片。
- 三处标识：左肩断环/目录钥馆章、右肩精确`MMM`、小腿精确`GZ-01`及三条刻度；禁止其他伪字和贴纸。
- 双臂完整等长；无武器、损伤、青光和场景。

输出：`art-delivery/review/guardian_z_collector_e02_ninehead_hinged_x_candidate_v8q.png`。

## 24. Q稿档案夹天线 R对照

只改Q天线：每侧内眉片、圆铰和外夹片；外夹片末端短促上折，验证折页机构的显性上限。身体、贴花和双臂完全不动。

输出：`art-delivery/review/guardian_z_collector_e02_ninehead_archive_clamp_control_v8r.png`。

## 25. Q稿剪式X天线 S稿

只改Q天线：每侧两块短厚金属片围绕太阳穴圆铰轻微交叠，形成一个小菱形负形；总体保持低位横向，中央红脊最高。禁止普通V角、长角、星芒和额外小刺。

输出：`art-delivery/review/guardian_z_collector_e02_ninehead_scissor_antenna_candidate_v8s.png`。

## 26. 枢轴横冠 T头雕三角度

参考S全身和用户选择的L头盔基础，展开正面、前3/4和严格侧面。生成收敛项：每侧一块内金眉片、一枚可见圆铰、一块宽钝外片；完整深蓝盔体、红额脊、银脸、耳轴和三组后掠盔片不变。

输出：`art-delivery/review/guardian_z_head_sculpt_pivot_antenna_three_view_candidate_v8t.png`。

## 27. 九头身枢轴横冠 T稿

以Q为完整身体父级，以T头雕三视为唯一头部修正：每侧内眉片—圆铰—宽钝外片，四块金色件总计，主要横向、轻微后掠；不改任何身体结构、比例、贴花或双臂长度。

输出：`art-delivery/review/guardian_z_collector_e02_ninehead_pivot_antenna_candidate_v8t.png`。

## 28. T稿目录缺口 U对照

只在T外天线片下缘增加一个浅目录标签缺口并缩短端头，验证单一负形能否强化万机馆身份；不增加零件，不改身体。

输出：`art-delivery/review/guardian_z_collector_e02_ninehead_catalog_notch_antenna_candidate_v8u.png`。

## 29. K上半身回归 V结构稿

多参考责任：K为腰带以上的硬母体，用户截图/L头雕为头部硬母体，v8只贡献腰以下的九头身增量，J只贡献胸肩铰链。

- 完整恢复K的深厚胸腔、巨大红色双片胸口卡扣、象牙白中轴、巨大深蓝C形真正肩甲和粗壮等长双飞拳。
- 胸口红甲不得拆成四块X楔，深蓝主肩甲不得改成红白斜片。
- 另外增加一对红色肩前甲，安装在肩关节正前方，从胸甲外上角向真正肩甲内前缘延伸，必须能看到独立铰链缝。
- 腰带以上完全不缩小；只拉长大腿、小腿和踝段，以厚上身叠长承重腿读取8.8至9头身。
- 宽金色主眉冠保留，中央冠后方只增加两根短辅助天线；不复制Z高达具体V角。

输出：`art-delivery/review/guardian_z_collector_e02_k_upper_ninehead_shoulderfront_candidate_v9v.png`。

## 30. 横向红肩前甲 W稿

以V为唯一整机父级，只修正红肩前甲：

- 将V中偏竖直、偏小盾的红肩前甲压低、加宽，主要向左右水平延伸。
- 内端从K红色胸口卡扣的外上角起势，外端到达深蓝C形真正肩甲的内前缘；正面远看形成宽阔红色上身色带。
- 保留狭石墨铰链缝，让胸甲、肩前甲和深蓝主肩甲仍是三个结构层。
- 禁止修改K胸甲、主肩甲、上身体积、腿长、双臂长度、头雕或贴花密度。

输出：`art-delivery/review/guardian_z_collector_e02_k_upper_lateral_shoulderfront_candidate_v9w.png`。

## 31. W头雕双辅助天线三角度

以用户选定的完整深蓝头盔和W全身头部为唯一父级，展开正面、前三分之四和严格侧面。

- 保留中央红额脊、宽金色主眉冠、琥珀眼、银色纵栅脸谱、圆形耳轴与完整后头盔。
- 只增加左右两根短辅助天线，位于中央冠后上方，向外上约20至25度，长度显著短于主眉冠半边。
- 三个角度保持相同零件数量和根部位置；禁止额外小刺、星芒冠、兽角或Z高达头雕复制。

输出：`art-delivery/review/guardian_z_head_sculpt_dual_aux_antenna_three_view_candidate_v9w.png`。

## 32. W母体三刀结构升级 X稿

参考W稿完整机体与W头雕，把它们视为硬父级，不重做头、胸、比例或飞拳身份。

- 只改三处：巨大深蓝C形真肩甲改为有唯一内前下缺口的厚折面断框；每只前臂上端增加正好三块大型银白旋封环片；只在脚背再回声一次断框缺口。
- 红肩前甲仍由红胸卡扣外上角向左右延伸，外端在视觉上扣入深蓝断框的唯一缺口。
- 保留九头身长腿、厚上身、两只完整工程等长飞拳和W头部的宽主眉冠 + 两根短辅助天线。
- 禁止大翼膀、巨大背包、变形、新武器、青光、细碎贴花、随机划痕、文字、伪字和场景。

首次生成的折面肩与三段环成立，但肩缺口出现不必要的白色L形支架，左右脚背也不一致；该图只作中间诊断，未交付到项目目录。

## 33. X稿受控纠正

沿用第32节已成立的整机，严格仅纠正两个生成偏差：

- 删除肩断框缺口里的白色L形括号，让红肩前甲的宽钝外端成为唯一扣入件。
- 左右脚背使用完全镜像的象牙白断框缺口，膝甲与小腿不再增加回声。
- 其余头雕、胸卡扣、上身厚度、肩框尺寸、三段环、九头身和双臂等长不动。

输出：`art-delivery/review/guardian_z_collector_e02_lockframe_candidate_v10x.png`。

## 34. 万机锁架四状态首次同图尝试

使用X稿身份，横向四格、相同比例与光线，从左到右绘制封存、启动、机体自身右火箭拳解锁、原右前臂毁损。机体自身右侧必须位于观者左侧。

生成结果中前两格成立，已确定性裁切为：

- `art-delivery/review/guardian_z_lockframe_state_a_sealed_candidate_v10x.png`
- `art-delivery/review/guardian_z_lockframe_state_b_activation_candidate_v10x.png`

后两格废弃：第三格把原右前臂改成灰色钻头，第四格在腰胯添加了虚假损伤。原始四格图不进项目台账。

## 35. C01E03右火箭拳解锁单图

- 机体自身右前臂必须位于观者左侧，必须仍是X稿墨蓝主甲、红色大楼形面和完整拳头的原飞拳。
- 右前臂上端的正好三块银白旋封环径向张开，与肘端出现小而明确的分离缝。
- 右前臂仍完整，无损伤、无灰钻、无炮管、无爆炸；左拳同时保持完整可见。

输出：`art-delivery/review/guardian_z_c01e03_rocket_punch_unlock_candidate_v10x.png`。

## 36. C01E03原右前臂丧失单图

- 观者左侧的机体右拳与右前臂完全缺失，但右肩、右上臂与正常上臂长度必须保留。
- 右肘端只显示紧凑圆形石墨回收接口、少量断裂旋封环和极少暖橙余热。
- 观者右侧的左飞拳完整；腰、胯、腿、胸、头无损伤；不安装巡展臂、救援架或后继臂。

输出：`art-delivery/review/guardian_z_c01e03_right_forearm_loss_candidate_v10x.png`。

## 37. 四状态确定性合成

不再让生成模型于同一大图内同时保持四个复杂状态。使用 `ffmpeg` 将通过的A/B裁切和独立重绘的C/D统一缩放、留白分隔后水平拼合，不修改像素内的机设内容。

输出：`art-delivery/review/guardian_z_lockframe_four_state_validation_candidate_v10x.png`。

## 38. 馆守Z X稿侧背同图 Y稿

参考职责：X稿锁定当前整机、色彩与断框机构；W稿锁定厚上身、红胸卡扣和横向红肩前甲；W头雕三视锁定严格侧面头型。

- 横向同图正好两个完整正投影：左为90度左侧面，右为180度背面；同一中性站姿、同一尺度和零件数。
- 侧面显示厚折面C形断框围绕三轴肩座，内前下方保留唯一缺口；红肩前甲只占前半部并在石墨铰链处停止，红胸只向前突出，不绕到背部。
- 背面没有背包：后脑至腰带之间是贴身深蓝归档脊，由梯形后颈锁盖、三块大纵向服务盖、一条窄银色中轨和一个小暖琥珀状态窗组成。
- 两块平贴肩胛承力盖将归档脊连到左右大同心肩轴；肩断框从后方仍是开口的对称折面拱，不合成光环。
- 双臂完整镜像等长，前臂上端正好三块宽银白旋封环片；无损伤、无换臂、无枪管、无钻头。
- 背面不新增红色图案、贴花、文字、编号、翼膀、推进器、变形件或新武器。

输出：`art-delivery/review/guardian_z_collector_e02_side_rear_turnaround_candidate_v11y.png`。

## 39. Y稿独立左侧面

以第38节同图的左侧机体为直接结构父级，X稿与W头雕只用于身份对照。高分辨率竖图中只画一台朝左的90度严格侧面馆守Z：

- 保留九头身、厚胸、紧腰、巨型飞拳、长承重腿与宽楔足。
- 保留W头侧面、折面断框肩、红肩前甲只占前半部、红胸向后收入石墨肋甲、肘轴与三段旋封环。
- 严格侧面中远侧手臂允许与近侧手臂自然重叠，但机体设定仍是完整等长双臂。
- 纯微暖白背景，无投影、无文字、无三分之四透视、无额外部件。

输出：`art-delivery/review/guardian_z_collector_e02_left_side_candidate_v11y.png`。

## 40. Y稿独立背面

以第38节同图的背面机体为直接结构父级，X稿与第39节侧面只用于比例和部件一致性。高分辨率竖图中只画一台180度严格背面馆守Z：

- 双肩、上臂、飞拳前臂、拳头、腿和足跟必须完整镜像等长。
- 对称折面肩断框各自包围一枚大同心肩轴，下内侧保持开口，左右不合成背后光环。
- 不设背包，只使用贴身归档脊、狭银色中轨、小暖琥珀窗和两块肩胛承力盖。
- 背面以70%墨蓝、15%石墨、10%冷白/银为主；红色只能来自现有前臂侧甲的自然厚度，禁止新红背甲和后背徽章。
- 无翼膀、无推进器树、无排气喷口群、无新功能、无文字与伪字。

输出：`art-delivery/review/guardian_z_collector_e02_rear_candidate_v11y.png`。

## 41. Y侧面保留后的窄背体与模块接口 YR稿

以X稿完整机设、Y稿已获正向反馈的严格侧面比例和Y稿旧背面的零件位置为父级，只纠正180度严格背面：

- 背部实体宽度缩减约12至15%，外轮廓宽度仍由左右独立断框肩承担；不得把厚上身改成纤细机。
- 两枚同心肩轴缩小约20%并向肩内沉入，删除向外鼓起的宽肩胛盖，改为肋部轮廓以内的短石墨承力梁。
- 中央封闭归档脊改为贴身窄H形四点挂架：肩胛内缘下方两个上锁点、后腰两个下锁点、一条象牙白/银色中轨和一个内沉圆形能源控制耦合口。
- 正好四枚小型姿态喷口：两枚在肩根下，两枚在后腰；深石墨与淡香槟内圈，无点火、无辉光。它们只说明跳跃、落地、反作用和舰面站立配平，不能暗示常态飞行。
- 保持九头身、双臂完整镜像等长、巨型飞拳、长腿与宽楔足；纯微暖白背景，无背包、翼膀、武器、文字、伪字和新增红背甲。

输出：`art-delivery/review/guardian_z_collector_e02_rear_modular_candidate_v12yr.png`。

## 42. C01退役推进骨架挂载验证

横向工程对照图中绘制两台完全相同尺度的馆守Z严格背面：左为第41节YR裸机，右为同一裸机安装C01退役推进骨架。

- 右侧装具由窄幅外露桁架、与四点挂架对应的四枚粗锁爪、覆盖中央耦合口的圆形耦合盖和两台靠近中轴的大型直喷筒组成。
- 两台喷筒竖向放置、喷口到达后腰下方，整副骨架不超过内肩轴宽度，不形成翅膀，不挡住双臂与髋关节。
- 退役感使用补强带、略不均匀的喷口内圈和一台喷筒略短表达；不堆满划痕、小管线或军用武器细节。
- 左右机体都保留完整等长双臂，只用于验证同一裸机的挂载前后关系；无点火、无烟火、无青光、无文字和伪字。

输出：`art-delivery/review/guardian_z_c01_propulsion_frame_mount_validation_candidate_v12yr.png`。

## 43. W母体短厚背面 Z稿

以W稿正面、X稿断框完整态和已获肯定的Y稿严格侧面为三项硬父级，单独生成一台180度严格背面馆守Z：

- 机体必须和W/X共用同一骨架。后颈至腰带是短、厚、宽的紧凑上背；九头身只由长腿承担，不拉长胸腹和背脊。
- 背躯呈宽倒梯形，两块大墨蓝肩胛甲用短倒V/断X甲缝组织上背，然后经过两级大甲片迅速收进高腰。
- 取消纵贯后颈至后腰的银色H轨。四锁座横向嵌入肩胛下缘与后腰上缘；肩胛之间只保留一个短厚八角耦合盘。
- 本体四枚姿态喷口改为扁平楔形：肩胛下两枚、后裙上两枚。无火焰、无常亮光，不暗示常态飞行。
- 双肩、双臂、飞拳前臂、腿和足镜像等长；纯微暖白背景，无背包、翼膀、文字和新红背甲。

输出：`art-delivery/review/guardian_z_collector_e02_rear_wbody_candidate_v13z.png`。

## 44. “整机飞拳”推进骨架 Z稿

以前一节Z稿裸机背面为不可修改的底体，只增加C01退役推进骨架，单独生成同尺度严格背面挂载态：

- 核心命题是“一次点火把整台馆守Z发射成第三枚飞拳”，不是给机器人安装两台航空发动机。
- 使用从肩胛到后裙的短粗石墨X承力架、四枚锁爪和中央八角耦合盖。耦合盖由短红锁块、象牙白分段框和暖琥珀状态核构成。
- 左右推进胴均为前臂体量的短粗多边形装甲块：墨蓝断框外甲、红色斜向锁甲、石墨内构；下端正好三块宽银白旋封环片与一个巨大六边形/梯形喷口。
- 推进胴靠近中轴并保持在肩框外宽以内，最低不超过后裙；一侧约短8至10%，增加一枚宽补强箍和不同热变色。
- 禁止圆柱火箭筒、航空发动机、油箱、进气道、机翼、长管、枪炮、导弹、青光、火焰、文字和场景。

输出：`art-delivery/review/guardian_z_c01_wholebody_punch_frame_mount_candidate_v13z.png`。

## 45. 裸机八喷口严格背面 v14

以V13Z短厚背面为不可拉长的结构父级，保持W/X厚上身、九头身长腿、等长双飞拳和短八角耦合盘。只把本体姿态推进整理为八枚深腔喷口：上背2、后腰2、小腿后外侧每腿2；统一石墨内腔、银白分段内圈与极少香槟热障层，不点火。四个象牙白实心锁座与喷口严格分形，浅金槽只作被动散热。无背包、翼膀、文字与场景。

输出：`art-delivery/review/guardian_z_collector_e02_rear_integral_verniers_candidate_v14.png`。

## 46. 魔神系谱大型飞翼推进骨架单体 v14

参考现代魔神系大型红翼的商品轮廓与背部合体逻辑，但不复制具体Jet Scrander：

- 两片宽厚红色主翼，外端各有一个馆守Z式矩形断框缺口；两片明显更短的上稳定翼构成不完整断X。
- 中央为短厚墨蓝/石墨挂体，大型红色倒梯形锁甲、象牙白断框、暖琥珀状态核、四枚粗锁爪与短八角耦合口。
- 翼根下方两台短粗多边形推力盒，各含一个梯形主喷口和两个小矢量喷口；一侧略短并有一条宽补强箍。
- 禁止飞机机首、座舱、长圆筒、火箭筒、油箱、导弹、枪炮、四片等长镰翼、日文与伪字。

输出：`art-delivery/review/guardian_z_c01_flight_wing_frame_standalone_candidate_v14.png`。

## 47. 大型飞翼挂载严格背面 v14

以第45节裸机和第46节飞翼单体为双硬父级，在宽幅白底中只画一台九头身馆守Z严格背面。中央挂体贴合短厚上背，不能拉长躯干或垂过后腰；双宽主翼翼展约肩宽2.2倍，双短稳定翼构成断X。双臂保持完整镜像等长；至少四枚小腿喷口继续可见。无点火、动作、武器、文字与额外喷口。

输出：`art-delivery/review/guardian_z_c01_flight_wing_frame_mount_rear_candidate_v14.png`。

## 48. 大型飞翼挂载后侧工程视 v14

沿用第47节挂载轮廓，改为完整后左三分之四视图，只用于展示装具深度。两台短粗多边形主推力盒必须在翼根下方清楚可见，终止于后裙以上；每台显示梯形主喷口与两个小矢量喷口，一侧略短并带宽补强箍。中央四爪、八角耦合盘和可见腿部小喷口同时成立；禁止把推力盒画成长筒、航空发动机或火箭筒。

输出：`art-delivery/review/guardian_z_c01_flight_wing_frame_mount_rear_threequarter_candidate_v14.png`。

## 49. A红弓宽翼正面 v15

以W/X馆守Z正面为不可修改本体，取消v14所有上举小翼。每侧只设一片厚实长翼，组合成浅上弧红弓：宽内根、长外掠、略抬钝折翼尖；翼体用大型后缘负空间消除红色实心板感，外端只重复一次矩形断框缺口。翼根完全位于肩后，不能遮挡头冠、胸口、肩前甲和双飞拳。

输出：`art-delivery/review/guardian_z_c01_flight_wing_front_candidate_v15a_red_bow.png`。

## 50. B折刃双段翼正面 v15

每侧正好两段大型承力翼：短厚内段向外上方抬起，通过一枚大银色圆环铰链连接更长、略向下折的外段。铰链后设置一个大三角负空间，外段为红色长折刃和墨蓝承力边。不得增加小翼、飞机部件或武器。

输出：`art-delivery/review/guardian_z_c01_flight_wing_front_candidate_v15b_hinged_blade.png`。

## 51. C下掠披风翼正面 v15

每侧一片巨大机械翼，由肩后略抬形成宽折角，再沿长线下掠至小腿高度；中部切出巨大梯形开口，仅保留红色外甲轨与墨蓝内承力框。整体像主角机背后的两道红色披风斜线，但禁止蝙蝠膜、恶魔翼和奇幻生物感。

输出：`art-delivery/review/guardian_z_c01_flight_wing_front_candidate_v15c_downswept_mantle.png`。

## 52. D分叉矢翼正面 v15

每侧一片完整长矢翼，略向上展开。翼体中段切出一个覆盖约55%长度的长菱形负空间，形成红色上承力边与墨蓝下承力边，并只用一枚大型象牙白桥锁跨接。两道边在钝折箭头翼端前重新汇合，外端删除一个矩形角形成断框身份。

输出：`art-delivery/review/guardian_z_c01_flight_wing_front_candidate_v15d_split_arrow.png`。

## 53. E平衡四刃X翼正面 v15

使用四片都有完整体量的机械翼：上主翼长而宽，向上约24度；下副翼约主翼长度68%、宽度75%，向下约16度。上下翼明显不同长，组成开放X而非四等长镰翼；每片均为红色大面、墨蓝承力边、单一后缘切口和钝折翼尖，不得出现细杆稳定翼。

输出：`art-delivery/review/guardian_z_c01_flight_wing_front_candidate_v15e_balanced_x.png`。

## 54. E2矢量喷翼一体背包正面 v16

以W/X馆守Z为不可修改本体，以v15E开放X为概念父级，将总翼展收小约15至18%。左右各设一台短粗多边形矢量喷射盒；每侧上翼与下翼必须是同一喷射盒展开后的上下导流外甲，由一枚大型象牙白/银色断C矢量领共同承载。翼片由宽根、细腰和紧凑风筝形外甲组成，墨蓝凹槽与暖琥珀热流窗从盒体贯入翼根，禁止四块直板、细杆小翼和第二胸标。

输出：`art-delivery/review/guardian_z_c01_vector_jet_wing_mount_front_candidate_v16e2.png`。

## 55. E2矢量喷翼一体背包单体 v16

以后侧三分之四白底单体展示同一装具：短厚中央载体、四粗锁爪、小八角耦合盘、左右双矢量喷射盒、每盒一个大型梯形主喷口与两个小矢量喷口。每侧上下翼围绕同一喷射盒和同一断C矢量领展开，热流槽从盒体连续进入翼根。一侧盒体略短并有宽补强箍；禁止飞机机首、座舱和第三主发动机。

输出：`art-delivery/review/guardian_z_c01_vector_jet_wing_standalone_candidate_v16e2.png`。

## 56. E2矢量喷翼一体背包严格背面 v16

以v14八喷口裸机背面、E2正面和E2单体为三项硬父级。严格180度背面中，中央载体通过四爪和小八角耦合盘贴合短厚W背躯，不延长至后腰以下；双喷射盒、双主喷口、四翼断环与热流槽全部可读。中央八角件必须明显小于左右主喷口；至少后腰2与小腿4枚本体姿态喷口继续可见，并明显小于背包主喷口。

输出：`art-delivery/review/guardian_z_c01_vector_jet_wing_mount_rear_candidate_v16e2.png`。

## 57. A2霸弓双翼正面 v17

以v15A红弓宽翼为飞翼硬父级、W/X为本体硬父级。全机恰好两翼，每侧一片连续主翼；从肩后短厚喷射根部大幅拱起约16度，再沿外凸巨弓曲线向外展开，外三分之一回压为钝凿翼端，总翼展约肩宽2.2倍。每翼只用厚根断C弧、宽红弓壳、墨蓝翼端三个大体块；暖琥珀通道从根部贯入内半翼。禁止四翼X、小稳定翼、直板、巨孔、飞机尾翼和身体改造。

输出：`art-delivery/review/guardian_z_c01_twin_wing_front_candidate_v17a2_overlord_bow.png`。

## 58. A3流线矢弓正面 v17

以v15A红弓宽翼为飞翼硬父级、W/X为本体硬父级。全机恰好两翼；每翼从贴身扁椭圆喷射根部生长，红色外壳、墨蓝承力脊和单条琥珀通道连续成S曲线，根部厚、外端薄，内侧深凹让出双臂，外三分之一后掠收成仍有厚度的钝矢尖，总翼展约肩宽1.95倍。只用三条大型流动面带与受控斜接缝；禁止矩形板、独立下翼、巨大圆环、蝠翼膜、羽毛和航空机身。

输出：`art-delivery/review/guardian_z_c01_twin_wing_front_candidate_v17a3_streamline_vector_bow.png`。

## 59. A3X副翼X延伸正面 v18

以A3流线矢弓与W/X本体为硬父级，主翼数量、S曲线、翼展和本体均不变。每侧只增加一片主翼32至35%长度、约28%根厚的短矢量副翼，由同一翼根下层小转轴向下外侧约24度展开；红色上缘沿胸口X和红肩前甲的方向继续，墨蓝楔体与单条琥珀槽保持从属。视觉层级必须是两片巨大主翼、馆守Z本体、两片短副翼；禁止四翼等权和E2开放X。

输出：`art-delivery/review/guardian_z_c01_twin_wing_front_candidate_v18a3x_vector_vanes.png`。

## 60. A3X严格背面喷口与转轴 v18

以A3X正面和v14裸机八喷口背面为双硬父级。左右翼根各一枚扁八角深腔主喷口，全背包恰好两枚大型主喷口；中央短载体只有四粗锁块与小八角耦合。每侧显示断C后掠领、厚俯仰叉和短扭转套三个大轴件，副翼用同根体下层小转轴。后腰2与小腿4姿态喷口继续可见并明显更小；禁止第三发动机、长脊、航空涡扇和圆筒。

输出：`art-delivery/review/guardian_z_c01_twin_wing_mount_rear_candidate_v18a3x.png`。

## 61. A3X双翼拳刃模式 v18

两片A3主翼均从背部释放，根部喷射座与两片短副翼留在背上。每片主翼只在中段折叠一次，长度缩至约60%，红壳和墨蓝脊保持可辨；折叠后露出象牙白实体刃缘。断C翼根领打开并同心扣入各自前臂顶部三段旋封环，拳头完整露出，刃体沿前臂外侧并向拳前伸出约一条前臂长度。使用完整双臂三分之四攻击姿态，一臂前刺、一臂护斩；禁止手持剑柄、光剑、背上残留主翼和额外武器。

输出：`art-delivery/review/guardian_z_twin_wing_fist_blade_mode_candidate_v18a3x.png`。

## 62. A3R双层翼刃纠错组 v19（用户否决历史）

使用内置imagegen，把v18的双圆喷口改成四枚矩形喷口，把小副翼改成有分量的墨蓝留守翼，并尝试让红翼刃原尺寸套拳。生成机构母板、装着正面、装着背面、双拳手刀、完整背包单体和留守飞翼单体六张图。

该组因象牙白翼缘、金框喷口、红背盒和直板化分层造成复古玩具感，同时丢失A3原有S弧，被用户否决。六张输出仅作为History保留：

- `art-delivery/review/guardian_z_a3r_layered_wingblade_mechanism_board_candidate_v19.png`
- `art-delivery/review/guardian_z_a3r_complete_flight_front_candidate_v19.png`
- `art-delivery/review/guardian_z_a3r_complete_flight_rear_candidate_v19.png`
- `art-delivery/review/guardian_z_a3r_twin_fist_handblade_mode_candidate_v19.png`
- `art-delivery/review/guardian_z_a3r_backpack_complete_standalone_candidate_v19.png`
- `art-delivery/review/guardian_z_a3r_backpack_residual_flight_standalone_candidate_v19.png`

## 63. A3S原弧隐轨装着正面 v20

以A3正面为编辑目标、W为本体比例参考。A3红色连续S形上弧、墨蓝下凹弧、总翼展、厚根、上扬翼尖与双臂负空间全部视为不可修改；只允许在红壳内部增加顺弧齐平装卸缝，并在肩后露出极短石墨月牙铰链。禁止象牙/白/金翼缘、直板翼、四翼、小副翼、方盒喷口、圆涡扇与航空发动机舱。

输出：`art-delivery/review/guardian_z_a3s_original_arc_hidden_rail_front_candidate_v20.png`。

## 64. A3S原弧隐轨装着背面 v20

以第63节正面、v14裸机八喷口背面和A3为三项参考，绘制同一物体的180度背面。中央挂架必须收在肩胛之间；每侧翼根下方正好两条宽扁石墨暗缝喷口，全背包四条，不设金框、圆口、圆筒或红色背盒。保留裸机后腰与小腿小喷口的层级，背面翼壳仍保持A3红上弧与墨蓝大凹弧。

输出：`art-delivery/review/guardian_z_a3s_original_arc_hidden_rail_rear_candidate_v20.png`。

## 65. A3S双拳翼刃招牌动作 v20

两片手刀必须是第63节完整飞行态的整片红色S形上壳，原尺寸、原厚根、原曲线与原翼尖，不折叠、不缩短、不重画成剑。下缘只藏一条烟黑切削嵌条。翼根内的D形石墨托架只包住拳背与掌根，必须露出拳头进入托架以及拳套和圆筒前臂之间的手腕间隙；禁止圆形腕环、前臂扣具和小臂刃。背上只留下原墨蓝下凹弧翼。

输出：`art-delivery/review/guardian_z_a3s_twin_fist_handblade_mode_candidate_v20.png`。

## 66. A3S完整背包单体 v20

以第63、64节为同件正背父级，绘制脱离机体的三分之四背视产品图。保持A3双S翼原曲线；中央只有小型石墨锁架、十字耦合与两枚短月牙铰链；每侧根部两条暗缝喷口嵌在翼根下方，不外挂发动机。红壳顺弧装卸缝和墨蓝留守翼关系必须清楚，禁止机器人本体、支架与文字。

输出：`art-delivery/review/guardian_z_a3s_backpack_complete_standalone_candidate_v20.png`。

## 67. A3S留守飞翼单体 v20

使用第66节相同相机和尺度，只拆除两片红色S壳。原本位于红壳下方的墨蓝大凹弧翼留在中央挂架上，根部向上转约12度并略伸隐藏轨；保留原翼展、长尖与大负空间，不重新设计成直三角翼或小副翼。空出的顺弧黑色导轨与四条暗缝喷口可见；禁止红色小翼、额外翼对和文字。

输出：`art-delivery/review/guardian_z_a3s_backpack_residual_standalone_candidate_v20.png`。

## 68. A结构 × A3翅膀肩甲保留融合正面 v21

以内置imagegen精确编辑A稿正面，A稿是本体、真肩甲、肩前甲、肩轴、比例与姿态的绝对父级；A3只提供翅膀外段几何。

- 完整保留A稿左右两件深蓝C形断框真肩甲的尺寸、厚度、开口与分段；它们位于最前层，不能被银色圆环、红翼根或裸露肩轴替换。
- 红肩前甲与黑色肩轴位于中层，继续连接胸口X并保留双臂转动空间。
- 背包短桥和A3翼根退到肩后，绝大部分被真肩甲遮住；红色厚翼根从肩甲外后侧开始。
- 翅膀外段采用A3的一对连续S翼：厚红根、长红色缓降再上扬曲线、略抬翼尖、墨蓝大凹弧与双臂外侧负空间。
- 禁止恢复A稿矩形翼板和镂空方翼尖；禁止取消、缩小或遮挡真肩甲；禁止银色翼根圆环、额外小翼、四翼、浅色翼缘和航空发动机。

输出：`art-delivery/review/guardian_z_a_a3_shoulder_preserved_hybrid_front_candidate_v21.png`。
