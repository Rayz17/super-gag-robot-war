# 馆守Z收藏母版 gpt-image-2 生成规格 v1

## 生成目标

Create one premium Japanese super-robot character-design illustration for **Guardian Z**, an original 18-meter lead mecha awakened from the central display of a futuristic robot museum. This is the intact C01E02 base body with two complete arms of exactly equal total length. The reference image is only a starting point for the navy/red/gold palette, approximate heroic proportion, silver face mask, and broad shoulder mass. Redesign the mecha substantially so it has a unique silhouette, clear toy mechanisms, and premium collectible appeal.

## 必须保留的经典联想

- A bold heroic super-robot face: deep navy helmet, warm-gold three-part crown, glowing amber eyes, brushed-silver lower face mask.
- A powerful red chest focal area, heavy rocket-punch forearms, broad upper body, compact waist, stable display-plinth feet.
- The first read should evoke the lineage of classic Japanese rocket-punch super robots without copying any exact existing head crest, face grille, chest plate, weapon, proportion, or logo.

## 必须新增的馆守Z独有结构

- **Archive Crown**: one short thick red vertical catalog-key crest in the center, with two low outward gold eaves. It must not be a conventional V-fin or a spiky crown.
- **Exhibit-0 Chest Doors**: two thick red door panels with visible outer hinges and a narrow vertical ivory-and-amber archive core between them. The doors must look genuinely openable, not painted-on chest plates.
- **Display-Turntable Shoulders**: each shoulder has three readable layers: a navy curved outer shell, a warm-gold rotating ring, and a dark inner axle. Make this a strong silhouette and a believable articulation/play feature.
- **Catalog Rocket Forearms**: large but elegant navy forearm shells, a clean launch socket/rail behind each elbow, articulated dark hands, and one bold red/ivory/gold archival color band near each wrist. The two arms must be symmetrical in length and basic structure.
- **Museum-Plinth Feet**: wide stable feet with a subtle stepped display-base geometry, able to support a forward rocket-punch pose.
- Three to five intentional restoration plates may appear at structural service points, but no random full-body weathering.

## 比例与造型

- Approximately 6.8 to 7 heads tall, sturdy heroic super-robot anatomy, broad chest, compact waist, powerful forearms, clear thighs and shins, not lanky and not squat.
- Strong black-silhouette readability. Make the crown, openable chest doors, rotating shoulder rings, rocket forearms, and plinth feet identifiable without internal detail.
- Mix clean straight structural lines, broad soft arcs, and a few 45-degree cuts. Avoid excessive spikes, insectoid/alien shapes, military realism, Gundam-like dense panel segmentation, or generic Brave-series proportions.
- The design should feel both classic and newly ownable, suitable for a premium die-cast action figure and a long-running SRPG protagonist.

## 高细节分配

- This is a high-detail collector master for art books, posters, cards, and toy development.
- Keep the large armor surfaces clean. Concentrate fine mechanical detail only inside shoulder rings, chest-door hinges, elbow launch rails, fingers, knee backs, ankle gaps, and foot undersides.
- Use 2–3 meaningful major panel lines per limb. Every bolt or seam must imply assembly or movement.
- Materials: semi-matte deep navy armor, saturated vermilion-red chest doors, warm gold structural frames, brushed silver mask, charcoal joints, ivory ceramic inner panels, warm amber plus faint white machine-soul light.
- Clean contemporary anime mecha line art with selective premium model rendering, two-level cel shading plus restrained material highlights. Bright neutral studio lighting, no dark gothic mood.

## 构图与交付

- One single mecha only, full body, standing neutral heroic pose, front three-quarter view, both feet visible, both equal-length arms clearly visible, hands relaxed but powerful.
- Plain warm-white to very-light-gray studio background with a soft grounding shadow. No museum scene, no pedestal blocking the feet, no border, no collage, no inset views.
- No typography, no labels, no Japanese, no Chinese, no English, no logos, no watermark, no decorative symbols that resemble text.
- Portrait 2:3 composition with comfortable whitespace around crown, fists, and feet.

## 负面约束

Do not preserve the reference's generic smooth round shoulders without mechanisms. Do not make the robot simply more detailed. Do not use tiny random armor tiles, full-body rivets, dense scratches, camouflage, military decals, caution markings, barcode-like text, asymmetrical arm lengths, missing limbs, battle damage, hunched posture, tiny head, oversized feet, chibi proportions, photoreal movie robot aesthetics, grotesque biomechanical shapes, or a dark background.

## API/CLI参数

```text
operation: edit
model: gpt-image-2
quality: high
size: 2048x3072
input_fidelity: implicit high (gpt-image-2 fixed behavior; do not pass the CLI flag)
background: opaque
output_format: png
reference: ../review/guardian_z_standard_candidate_v1.png
output: ../review/guardian_z_collector_e02_intact_candidate_v2.png
```

说明：当前 Codex 内置 `imagegen` 接口不暴露模型选择；要保证使用 `gpt-image-2`，需通过本地 CLI/API 执行此规格，并在本机环境配置 `OPENAI_API_KEY`。不要把密钥写入文档、提交到仓库或粘贴进对话。

## 已验证命令

以下命令已于2026-08-02通过 `--dry-run` 参数校验；`gpt-image-2` 的图像输入固定为高保真，因此不要追加 `--input-fidelity`：

```bash
python3 /Users/rayz/.codex/skills/.system/imagegen/scripts/image_gen.py edit \
  --model gpt-image-2 \
  --prompt-file docs/superpowers/specs/production/art-direction-v0.3/art-delivery/sources/guardian_z_collector_master_gpt_image_2_prompt_v1.txt \
  --image docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_standard_candidate_v1.png \
  --quality high \
  --size 2048x3072 \
  --background opaque \
  --output-format png \
  --out docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/guardian_z_collector_e02_intact_candidate_v2.png
```

当前执行状态：`payload_validated / generation_blocked_by_missing_local_api_key`。
