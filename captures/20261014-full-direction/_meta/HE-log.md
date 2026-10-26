# H/E direction draft log — 20261014-full-direction

## Status: PROMPTS READY (parent will GenerateImage)

- Time: 2026-10-14 02:39 CST(+8)
- Agent: Grok Bot executor subagent
- Goal: ONE KINETIC_CEL direction JPG each for remaining H04–H13 and E02–E11

## What this executor did

1. Confirmed `cursor` / GenerateImage unavailable to executors (GetDynamicTools + CallDynamicTool failed; parent steered STOP).
2. Wrote ready GenerateImage payloads matching `M-todo-GenerateImage-pack.json` schema:
   - **`_meta/prompts/HE-todo-GenerateImage-pack.json`** — 20 items (H04–H13, E02–E11)
   - Fields: `id`, `slug`, `filename`, `aspect_ratio`, `reference_image_paths`, `description`
3. Did **NOT** invent placeholder JPGs; did **NOT** mark inventory `draft-v1`.
4. Earlier draft `_meta/HE-generate-prompts.json` is superseded by the pack above (may delete).

## Parent next steps

For each entry in `HE-todo-GenerateImage-pack.json`, call cursor `GenerateImage` with that payload, save/copy result to:
`incoming/{filename}`
Then set inventory item `status` → `draft-v1` and `file` → that path in `_meta/inventory.json`.

## Pack contents

### Humans (3:4 except H12/H13 = 16:9)
- H04 兜灯 → dir-H04-doudeng-v1.jpg (3:4)
- H05 陆衡 → dir-H05-luheng-v1.jpg (3:4)
- H06 豪司 → dir-H06-haosi-v1.jpg (3:4)
- H07 唐胶 → dir-H07-tangjiao-v1.jpg (3:4)
- H08 赵梅 → dir-H08-zhaomei-v1.jpg (3:4)
- H09 胶价王 → dir-H09-jiaojia-v1.jpg (3:4)
- H10 警备驾驶席 → dir-H10-police-seat-v1.jpg (3:4)
- H11 工房工程员 → dir-H11-workshop-staff-v1.jpg (3:4)
- H12 检修员与撤离人群 → dir-H12-civilians-v1.jpg (16:9)
- H13 机器犬及人物地图小单位 → dir-H13-tiny-units-v1.jpg (16:9)

### Enemies (all 16:9)
- E02 群生啮线幼体 → dir-E02-mite-v1.jpg
- E03 喷酸体 → dir-E03-acid-v1.jpg
- E04 远程架设体 → dir-E04-gun-v1.jpg
- E05 重型楔入体 → dir-E05-wedge-v1.jpg
- E06 掠渠体 → dir-E06-hover-v1.jpg
- E07 共振护群体 → dir-E07-screen-v1.jpg
- E08 自动拆锁工机 → dir-E08-worker-v1.jpg
- E09 无人牵引工机 → dir-E09-tug-v1.jpg
- E10 断冠 → dir-E10-rival-v1.jpg
- E11 架设体对空装备变体 → dir-E11-antiair-v1.jpg

## Style refs baked into pack

- Always: `style-lock/01-kinetic-cel-storyframe-v23a.png`
- Humans: + H01/H02/H03 locked peers
- Enemies: + `incoming/dir-E01-niexian-v4.jpg`, `style-lock/11-tactics-user-accepted.png`, `style-lock/02-mech-hero.jpg`
