# Writer Room Subagents

Use this reference when the user authorizes subagents or when a full-run thick synopsis needs independent review roles. Subagents are an audit surface, not theatrical role labels.

## Rule

The main orchestrator owns continuity, files, ledgers, and final gate decisions. Subagents provide independent findings on bounded review surfaces. Do not delegate the immediate blocking integration step.

Default to the lightest review tier that honestly fits the claim. A normal episode does not need all strict seats. Use full strict review only for chapter gates, opening arc gates, final run gates, user-requested strict review, key climax/relationship rupture episodes, or episodes that repeatedly fail Standard Review.

If subagent tools are unavailable, mark the packet:

```text
Reviewer Mode: single-context fallback
Fallback reason: subagent tools unavailable / user did not authorize
```

Do not call that packet subagent-reviewed.

## Story-First Reconstruction Five-Seat Baseline

For a prefix that passed contracts but failed as continuous story, use five independent reconstruction seats before rewriting. This is the required baseline for V35.9 C01-C12 and may be reused for later prefix reconstruction. It does not replace the strict per-episode seats when a strict Episode or Chapter Gate is claimed.

| role_id | role | independent evidence surface |
|---|---|---|
| `showrunner_continuity` | 剧情监督/连续性 | single-run causality, chapter handoff, branch assembly, dramatic fingerprints, repeated solution grammar, climax placement |
| `mecha_ip_spectacle` | 机器人文化/IP/奇观 | real unit participation, IP/scene recognizability, positive mecha desire, recurring mecha arcs, process-based PV spectacle, Wanji breadth |
| `gameplay_production` | 游戏制作/玩法叙事 | player action, controlled units, map, fail pressure, midpoint change, branch earned through play, production layer separation |
| `character_relationship` | 人物弧线/关系/生活 | protagonist agency and capacity change, relationship causality, attraction/rupture/sacrifice, daily warmth, comedy, emotional release |
| `canon_macro_physical` | Canon/宏观谜团/物理预算 | canon level, G.A.G./Index/Far Star/Jicun reveal cadence, recurring opponent chain, Wanji damage/energy/space/resource continuity, C13 inheritance |

For a full-prefix baseline, each seat writes evidence by chapter, distinguishes reader-assembly problems from underlying story problems, names locked highlights, and proposes pass evidence. For an episode or chapter replay, the same seats return concise `pass/fail`, evidence, must-fix actions, ledger risks, and an advance decision.

The five seats must not share a jointly authored verdict before returning their independent findings. The orchestrator performs synthesis after all five reports exist. A majority pass does not override one evidenced blocker.

## Standard Episode Review

Use this for normal episodes in a serial run.

- Reviewer mode: `single-context standard` if reviewed locally, or `targeted subagent standard` if 1-3 targeted agents were used.
- Expected savings: a 5-episode chapter should usually need 0-15 targeted episode subagent calls plus one strict chapter gate, instead of 85 strict per-episode calls. Total token use should normally fall by about 50%-75%.
- Local hard gates: mecha/IP density, gameplay clarity, protagonist/relationship event, macro-shadow debt, canon/asset boundary, quote/scene continuity, what-if/regret trigger and failure dignity when relevant, burn/tear/gag/PV payload, next debt.
- Optional targeted seats: choose only the risk surfaces that are uncertain. Typical choices are `mecha_ip`, `gameplay`, `relationship`, `protagonist`, `what_if_regret`, or `canon_asset`.
- Subagent input: short Context Pack plus relevant packet sections only. Do not send the whole repository, full graph, all ledgers, or full orchestration history unless the role specifically needs it.
- Subagent output cap: `pass/fail`, max three evidence bullets, must-fix actions, ledger risks, one advance sentence. Long essays are a failure of the review protocol.
- Validation: do not use `--strict-writer-room`; use structural plus strict creative validation and record the run command.

Standard review can pass an episode, but it cannot certify a chapter or whole run as strict writer-room reviewed.

## Ideal Writer Room

The ideal writer room has two layers:

1. **Standing consultants**: canon/material, mecha/IP, and protagonist/relationship consultants may provide shared advice for a chapter or arc. They are useful for context extraction and side review, but they do not count as per-episode writer-room review.
2. **Per-episode seats**: every formal thick episode packet must receive independent role findings for the current episode. These role findings decide whether the episode may advance.

For a strict writer-room run or Strict Chapter Gate, the per-episode seats are:

| role_id | role | blocker surface |
|---|---|---|
| showrunner | 剧情监督 | 戏剧无转折、因果断线、高潮不成立 |
| 50_issue | 50问题审计 | 旧问题只贴标签、没有场面化解决 |
| mecha_ip | 机器人文化专家 | 参战机体少、IP投射弱、名场面不可识别 |
| gameplay | 游戏制作人 | 玩家不知道玩什么、地图/胜败条件/中段变化不清 |
| character_dialogue | 人物与对白编辑 | 人物同声、金句化、台词没有听众和动作 |
| relationship | 感情戏/成人卖相顾问 | 纪存/七海/白鸢等关系无吸引、误会、牺牲、狗血事件 |
| protagonist | 主角熔炉编辑 | 主角只有小指标动作，没有打击、代价、升级或新限制 |
| jicun_memory | 纪存机魂记忆编辑 | 机魂记忆只讲设定，不破局、不保护、不付代价 |
| quote_scene | 名台词/名场面连续性编辑 | 直接引用复用、错用，或梗点没有进入剧情动作 |
| spectacle_emotion | 燃泪梗编辑 | 无燃点、泪点、梗点，或都是小口径设计 |
| robot_anime_pv | 机器人动画/PV导演 | 没有可剪预告的巨大机器画面和动画时机 |
| commercial_opening | 商业开局制作人 | 玩家没有继续动机、奖励期待或试玩吸引力 |
| macro_mystery | 宏观谜团监督 | G.A.G./索引/远星/旧灾变没有事件化阴影 |
| player_interest | 玩家兴趣代表 | 读完无法复述“发生了什么值得说” |
| wanji_culture | 万机馆文化容量编辑 | 万机馆/开馆/馆藏规模和谱系不够“万机” |
| thickness | 厚度编辑 | 退化成话卡、设计备忘录或两段摘要 |
| canon_asset | Canon/资产监督 | canon冲突、资产层级不清、图谱/索引遗漏；真实证词无来源/边界/授权状态 |

Strict writer-room runs must use fresh reviewer ids per role and per episode. Reusing three standing consultants across many packets is allowed only as advisory context and must be labeled as shared advisory review, not as `Reviewer Mode: subagent` for the packet.

The validator flag for this mode is:

```bash
--strict-writer-room
```

This flag implies `--require-subagents`, requires all strict seats above, and ignores `--allow-reused-subagent-ids`.

## Required Review Roles

For non-strict thick synopsis episode packets, use these baseline roles only when a targeted or baseline subagent pass is needed. For strict chapter gates, opening arc gates, final run gates, explicitly user-requested strict review, or any run that claims an ideal writer room, use the full strict seats above instead of this baseline table.

| role_id | role | scope | required output |
|---|---|---|---|
| showrunner | 剧情监督 | 戏剧推进、反转、高潮、连续因果 | findings; must-fix; nice-to-have; pass/fail |
| mecha_ip | 机器人文化专家 | 参战机体、IP投射、名场面、模玩生态、机战爽点 | missing units; weak homages; concrete patch actions |
| gameplay | 游戏制作人 | 战斗形式、地图、胜败条件、回合触发、玩法变体 | playable clarity; mid-battle twist; fail states |
| relationship | 感情戏顾问 | 纪存/七海/白鸢、成人张力、误会、积累、狗血事件 | emotional event; accumulation; attraction risk; patch |
| protagonist | 主角熔炉编辑 | 纪存机魂、主角成长、代价、升级/新限制 | desire; blow; choice; cost; state delta |
| canon_asset | Canon/资产监督 | canon漂移、资产层级、图谱索引、制作可用性 | hard conflicts; candidate rows; asset-tier fixes |
| quote_scene | 名台词/名场面连续性编辑 | 直接引用、名场面投射、复用纪律、中文玩家识别度 | reuse audit; payload gaps; replacement or refrain policy |
| spectacle_emotion | 燃泪梗/PV编辑 | 燃点、泪点、梗点、PV级机器人演出、文化吐槽 | missing gates; stronger set-piece actions |
| wanji_culture | 万机馆文化容量编辑 | 万机馆厚度、馆藏密度、展区谱系、馆藏到参战关系 | breadth gaps; exhibit-to-roster fixes |
| what_if_regret | 机战IF/原作遗憾编辑 | 分支、隐藏、说得、救人、名场面反转、失败尊严 | selected what_if_id; originalization risk; trigger/failure dignity patch |

## Delegation Timing

1. Main orchestrator writes or receives the single-episode draft packet.
2. In Standard Review, spawn only targeted review subagents when useful. In Strict Review, spawn independent review subagents with only the episode packet, relevant brief, and role instructions.
3. While agents run, the main orchestrator checks structure, ledgers, and canon locally.
4. Merge returned findings into the packet's `Writer Room Review`.
5. If any role marks `fail`, patch locally only if the failure is local. If structural, rebuild the pressure board/card and rerun the episode.

## Prompt Skeleton

```text
You are the <role> for 超GAG机器人大战. Review exactly one episode packet.

Do not rewrite the episode. Do not summarize generally. Return:
1. pass/fail
2. top findings with concrete evidence
3. must-fix patch actions
4. risks to ledgers
5. one sentence on whether this packet may advance

Check only your role surface. Treat missing playable mecha, weak relationship events,
thin protagonist growth, absent enemy gain, unclear asset tier, accidental direct quote
reuse, missing burn/tear/gag payloads, weak PV spectacle, or thin Wanji collection breadth
as blockers when they belong to your role. If the episode uses real-world testimony,
check source, usage mode, concrete object, sensitivity boundary, authorization status,
and whether it avoids cheap grief consumption.
If the episode uses top-level theme, Far Star, Index, opening rights, real-world
testimony, or finale material, check `robot_culture_value_axes_v0_1.tsv` usage:
axis id, scene payload, gameplay payload, character choice, mecha payload,
enemy misuse, future debt, and whether the value is drama rather than slogan.
If the episode uses branch, hidden unit/support, say得, saved-death, original
tragedy reversal, famous-scene IF, or terminal all-support material, check
`roster_what_if_regret_pool_v0_1.tsv` usage: selected what_if_id, source anchor,
regret axis, IF repair question, originalization payload, playable trigger,
failure dignity, route/hidden use, and avoid boundary. Reject direct IP copying,
cheap revival, and abstract route menus.
```

## Packet Recording

Every packet that used subagents must record:

```text
Reviewer Mode: subagent
Subagent Review IDs: showrunner=<id>; 50_issue=<id>; mecha_ip=<id>; gameplay=<id>; character_dialogue=<id>; relationship=<id>; protagonist=<id>; jicun_memory=<id>; quote_scene=<id>; spectacle_emotion=<id>; robot_anime_pv=<id>; commercial_opening=<id>; macro_mystery=<id>; player_interest=<id>; wanji_culture=<id>; thickness=<id>; canon_asset=<id>
Optional Targeted IDs: what_if_regret=<id>
Subagent Blocking Findings:
Subagent Patch Actions Applied:
Subagent Findings Not Applied:
Reason:
```

If the main orchestrator overrules a subagent blocker, the packet gate status must be `warn` or `failed`, not `pass`, unless the packet includes a concrete patch addressing it.

## Anti-Patterns

- Do not invent subagent findings after local self-review.
- Do not ask all subagents to review everything; role scopes must stay bounded.
- Do not use subagents to write six alternative episodes for the same slot unless the task is explicitly exploratory.
- Do not proceed to chapter assembly while a blocking role finding is unpatched.
- Do not let subagent review replace prefix regression. Episode review and chapter prefix review are different gates.
