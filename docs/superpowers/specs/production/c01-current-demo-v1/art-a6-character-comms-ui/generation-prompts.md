# C01E02 A6 ImageGen 最终提示词集

> Mode: OpenAI built-in `imagegen`
>
> Use case: `stylized-concept` + `background-extraction`; Qihai correction uses `identity-preserve`
>
> 说明：下列为最终保留输出的规范化语义提示词，合并了重复技术约束；不声称是工具调用序列化的逐字节日志。

## 公共约束

```text
Asset type: C01E02 R0.5 tactical UI character communication portrait source.
Style/medium: clean restrained anime-game character illustration with crisp readable facial features and materials at dense 720p UI scale; original project design, not an imitation of a named artist, franchise, or existing game character.
Composition: one subject only, upper-body communication portrait, generous padding, full silhouette inside frame, no crop through the head or key props.
Scene/backdrop: perfectly flat solid #00ff00 chroma-key background; uniform color with no shadow, gradient, floor, texture, reflection, or lighting variation.
Constraints: no text, logo, watermark, UI, dialogue bubble, weapon command icon, extra character, cast shadow, or contact shadow. Do not use #00ff00 on the subject.
```

## 纪存

```text
Input image: frozen CML001 Jicun identity anchor, identity reference only.
Subject: young Chinese male museum guide and temporary closure lead; dark tousled hair, blue-gray eyes, navy technical field jacket over white shirt, staff lanyard, rugged route-reading wrist tablet. He reads people, routes, and danger in a sinking city; he is not a military commander or omniscient hero.
focused: eyes and finger actively reading the route tablet, closed mouth, measured breathing, clear practical concentration.
alarm: same identity, clothing, tablet, scale, and composition; eyes snap toward a newly revealed danger, jaw slightly tense, controlled warning rather than panic.
resolve: same identity, clothing, tablet, scale, and composition; tablet lowered slightly, closed mouth and steadier shoulders, looking toward a chosen safe route with grounded resolve, not a command pose.
```

## 七海

```text
Input image: frozen CML002/003/004 Qihai identity crop, identity reference only.
Subject: mature Japanese female archival safety officer stationed at the Daige East District sealing center; short asymmetric black bob, amber-brown eyes, white formal technical coat with restrained navy/red/gold panels over a black high-neck uniform, translucent work slate. Professional remote official carrying the consequence of withdrawing only her own shutdown order; never an onsite teammate, artillery commander, or battlefield superior.
controlled: composed remote status, lips closed, eyes checking the slate, restrained posture.
decision: same identity, clothing, slate, scale, and composition; firm eyes and jaw, lips fully closed, accepting the consequence of the withdrawn order; no speaking, issuing-command, pointing, or broadcast pose.
concerned: same identity, clothing, slate, scale, and composition; concern visible in eyes, brow, neck, and shoulders while remaining professional and controlled; lips closed.
```

### `decision` 局部纠偏

```text
Edit target: the retained Qihai decision source.
Change only the mouth, jaw, and eye resolve: close the lips completely, make the jaw and gaze firmer, and preserve restrained accountability after withdrawing her own shutdown order. Do not add a speaking posture.
Keep unchanged: identity, face proportions, hair, earrings, clothing, translucent slate, hands, body pose, camera, lighting, scale, and composition. No text, UI, command gesture, weapon or artillery cue.
```

## 旧守护者

```text
Input image: frozen CML008 Guardian Z head/chest identity crop, identity reference only.
Subject: the Old Guardian is the same subject as the 18 m Guardian Z, expressed only through the worn navy/charcoal armored head, gold crown fins, silver grille, amber eye light, red chest armor, blue star chest plate, and chest speaker bars. No human face, avatar, virtual girl, independent AI body, assistant hologram, shield, or extra limb.
guide: calm frontal guide attention, steady amber eyes and readable chest speaker area.
contact: same machine identity and materials, braced contact tension through head angle and chest load, no punching pose.
shield_gaze: same machine identity and materials, gaze turned toward the offscreen retired shield while body remains the Guardian itself; do not draw the shield.
```

## 本地后处理

```text
Convert the flat green source to RGBA with chromakey plus green despill. Scale uniformly with Lanczos, pad into the frozen safe rectangle, keep frame edges transparent, preserve separate Qihai noise and Old Guardian head/chest/waveform source layers, then pack row-major according to media packing v2.
```
