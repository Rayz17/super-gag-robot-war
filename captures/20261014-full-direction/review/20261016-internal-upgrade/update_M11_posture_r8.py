"""Continue the existing M11 batch with one user-directed posture correction."""
from pathlib import Path
from PIL import Image
import csv, hashlib, html, json

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parents[3]
BASE = OUT.relative_to(PROJECT).as_posix() + '/'
DATE = '2026-10-21'
def read(name): return json.loads((OUT / name).read_text())
def write(name, data): (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

preferred = 'samples/M11-side-r7-angle-attempt.png'
selected = 'samples/M11-selected-head-r6.png'
current = 'samples/M11-posture-r8.png'
generated = Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470/exec-f415d834-8d6c-408a-a1ef-4234fda981f8.png')
assert sha(OUT/current) == sha(generated)
assert sha(OUT/selected) == read('M11-head-selected-and-turnaround-r6.json')['sha256']
with Image.open(OUT/current) as im: size, mode = list(im.size), im.mode
item = dict(id='POSTURE', file=current, sha256=sha(OUT/current), pixel_size=size, mode=mode,
            generated_source=str(generated), prompts=['M11-posture-prompt-r8.txt'],
            role='沿用户肯定的斜侧稿修正缩脖子、肩线与胸颈过渡',
            user_accepted=False, runtime_integrated=False, handoff_sent=False)
direction_name = 'M11-posture-direction-r8.json'
production_name = 'M11-posture-production-r8.json'
reader = 'M11-turnaround-structure-r7.html#posture-r8'
refurl = 'https://www.hasbropulse.com/product/transformers-studio-series-commander-class-the-transformers-the-movie-8631-optimus-prime/F85145L00'
direction = dict(
    date=DATE, revision='M11-posture-direction-r8', authority='direct_user_feedback',
    existing_batch='design-followthrough-r1.json',
    preferred_source_feedback=dict(verbatim='这一稿的状态还不错', file=preferred,
        generated_source='/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470/exec-f27ddb78-5a5c-4794-86d4-f4df8b1a91e0.png',
        sha256=sha(OUT/preferred), scope='用户肯定此稿整体状态，作为本次体态修正基底；不是全批或工程验收。'),
    latest_correction='但是货柜领袖有点缩脖子，你参考擎天柱的体态来修正吧',
    selected_head_receipt='M11-head-selected-and-turnaround-r6.json',
    supersedes_author_preference='作者此前因斜角和背架厚度未选该图；用户最新肯定优先，保留其体量，不沿减薄背架稿替换本次基底。',
    scope=['协调颈部露出、肩线和胸甲上沿，参考擎天柱挺拔领袖体态',
           '保留原头纵向比例、双侧天线、勇者颏甲与长腿身形',
           '保留白蓝橙、单片胸窗、四轮位和用户肯定稿的背架体量',
           '本轮先修同一斜侧看稿；此前三视须后续按体态同步，不能称已经全组同步'],
    posture_reference=dict(url=refurl, role='体态参考；非头脸或涂装复制',
        inspection='作者通过官方产品图浏览器截图观察正面站姿与肩胸关系'),
    previous_direction='M11-head-aspect-chin-direction-r7.json',
    new_image_user_accepted=False, runtime_changed=False, handoff_sent=False)
write(direction_name, direction)
review = dict(
    reviewer='author', independent_review=False,
    actual_media=[preferred, selected, current],
    observed=['新稿下颌下方露出连续深色装甲颈部，原图头部几乎贴在胸窗上沿。',
              '近侧肩壳顶线降低并后移，下颌和下半脸不再陷入肩甲；肩壳仍厚重。',
              '头盔高宽比与原稿近似，头部整体略缩小，未横向拉宽或纵向压扁。',
              '两根钝头侧天线、前凸颏甲、单片风挡、橙色灯与轮毂、四个近侧轮位、长腿和原背架体量保留。',
              '远侧手臂可见范围略增，属于重绘/体态造成的投影差异。'],
    limits=['本轮是斜侧体态源稿；正侧背旧稿未同步，不是同模型正交。',
            'R7头仓草模仍是上一轮局部包络，未验证新增颈部展开行程、肩架与胸甲活动净空。',
            '新稿待用户看图，未改模型、动作或游戏运行。'])
production = dict(date=DATE, revision='M11-posture-production-r8', asset='货柜领袖肩颈体态局部修正',
    canon_entity='V353U043', existing_batch='design-followthrough-r1.json',
    previous_production='M11-turnaround-structure-production-r7.json', reader=reader,
    direction_record=direction_name, generation_mode='built-in image_gen',
    items=[item], preferred_visual_basis=direction['preferred_source_feedback'],
    selected_head_reference=read('M11-turnaround-structure-production-r7.json')['selected_head_reference'],
    prompt_index='M11-posture-prompts-r8.json', author_review=review,
    current_turnaround_alignment='requires_r8_posture_alignment',
    previous_layout_applicability=review['limits'][1],
    new_images_user_accepted=False, runtime_changed=False, handoff_sent=False)
write(production_name, production)
write('M11-posture-prompts-r8.json', dict(generation_mode='built_in_image_gen',
    inputs=[dict(role='edit_target',file=preferred,sha256=sha(OUT/preferred)),
            dict(role='head_design_reference',file=selected,sha256=sha(OUT/selected))],
    selected_outputs=[dict(id='POSTURE',file=current,prompts=item['prompts'])],
    reference_urls=[refurl]))

ledger = read('design-followthrough-r1.json')
ledger['latest_m11_cargo'] = production_name
ledger['latest_m11_user_feedback'] = direction_name
ledger['production_focus'].update(
    current_step='接续R7：用户肯定f27斜侧稿状态后指出缩脖子；R8已修肩颈、胸颈过渡，当前只完成斜侧源稿。',
    next='沿R8体态对齐正侧背及颈部展开/肩架/胸甲收纳；继续原三视与可变结构范围。')
if direction_name not in ledger['production_focus']['source_basis']:
    ledger['production_focus']['source_basis'].append(direction_name)
ledger['experience_record_m11_posture_r8'] = dict(
    classification='experience', parent_focus='ART-M11-TURNAROUND-STRUCTURE-R7',
    original_request=direction_name, production_record=production_name,
    start='用户肯定f27斜侧整体，但指出头颈陷入肩胸、体态缩脖子。',
    actual_input='沿同一图编辑，协调头颈高度、肩线和胸甲上沿，保持轮组/背架/长腿。',
    visible_consequence='颈部可见，下颌与胸肩分离，肩胸仍有重量。',
    next_decision='看修正后的领袖体态是否达到预期，再将同一关系同步原三视与活动结构。',
    runtime='源设计工序，未接入主工程；正常游戏镜头/HUD/动作/实听/性能本轮未测。',
    author_observation=production_name+'#author_review', independent_review=False,
    user_acceptance=False, defect_id='ART-M11-NECK-POSTURE-07')
defect = next((x for x in ledger['defect_ledger'] if x.get('id')=='ART-M11-NECK-POSTURE-07'), None)
if defect is None:
    defect=dict(id='ART-M11-NECK-POSTURE-07', defect='头颈被高肩甲与胸甲挤住，呈缩脖子体态。', attempts=[])
    ledger['defect_ledger'].append(defect)
if not any(current in x.get('files',[]) for x in defect['attempts']):
    defect['attempts'].append(dict(files=[current], observed=True,
        outcome='author_observed_improvement',
        method='从用户肯定f27整机出发，协调抬头颈、降肩/后展和胸甲上沿；保留厚重体量。',
        evidence=production_name, result='下颌下方装甲颈部可读、肩线降低；新图尚未用户确认。'))
defect.update(latest_user_evidence=direction_name,current_source=current,closed=False,
    remaining='新图待看；正侧背与颈部/肩架活动结构尚未按新体态同步。')
side = next(x for x in ledger['defect_ledger'] if x.get('id')=='ART-M11-SIDE-CAMERA-01')
side['latest_user_preference'] = dict(record=direction_name,file=preferred,
    note='作者旧未选意见保留为历史；用户肯定此图整体状态，R8以此继续。斜侧看稿不冒充正交侧视。')
write('design-followthrough-r1.json', ledger)
decisions = read('user-art-decisions-20261016.json')
decisions['latest_M11_direction'].update(date=DATE,record=direction_name,current_reader=reader,
    preferred_whole_body_source=preferred,current_posture_source=current,
    posture_correction_authorized=True,specific_new_images_user_accepted=False)
write('user-art-decisions-20261016.json', decisions)
author = read('sample-author-review.json')
author['latest_M11_source_record']=production_name
author['latest_M11_posture_review']=review
write('sample-author-review.json',author)

# Add this correction to the existing reader; do not maintain a second progress reader.
page=OUT/'M11-turnaround-structure-r7.html'
s=page.read_text()
if 'id="posture-r8"' not in s:
    section=f'''<section id="posture-r8"><h2>当前：抬出头颈，打开肩胸</h2><p>沿用户肯定的斜侧稿保留厚重体量，露出短实装甲颈部，降低肩线并调整胸甲上沿。保留原头型、双侧天线、勇者颏甲、长腿和原背架。</p><figure><a href="{current}"><img src="{current}" alt="货柜领袖R8肩颈体态修正，保留高头壳与长腿"></a><figcaption>R8 当前斜侧体态看稿</figcaption></figure><details><summary>对照用户肯定的原稿</summary><figure><img src="{preferred}" alt="用户表示状态不错的f27原稿"><figcaption>本次编辑基底；用户肯定整体状态后指出缩脖子。</figcaption></figure></details><p>以下保留上一轮三视与结构；肩颈尚未同步R8。<a href="{production_name}">本次源稿与观察</a> · <a href="M11-posture-prompt-r8.txt">内置生图实际提示词</a> · <a href="{refurl}">体态参考：Hasbro官方擎天柱</a></p></section>'''
    s=s.replace('<h2 id="robot">',section+'<h2 id="robot">',1)
    s=s.replace('人形正、侧、背</h2>','上一轮人形正、侧、背（体态待同步）</h2>',1)
    s=s.replace('<a href="#robot">','<a href="#posture-r8">当前肩颈修正</a><a href="#robot">',1)
    page.write_text(s)

# Migrate only the existing Working design-direction row, preserving exact head lock CML138.
def load_tsv(f):
    with f.open() as h:
        r=csv.DictReader(h,delimiter='\t')
        return r.fieldnames,list(r)
def save_tsv(f,fields,rows):
    with f.open('w') as h:
        w=csv.DictWriter(h,fieldnames=fields,delimiter='\t',lineterminator='\n')
        w.writeheader();w.writerows(rows)
f=PROJECT/'docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv'
fields,rows=load_tsv(f)
r=next(x for x in rows if x['lock_id']=='CML137')
r.update(
    visual_lock='未来电驱货车/摄像头后视与可见双侧天线方向保持。原eac75eab头型和高宽比由CML138固定，R2长腿尺度与勇者颏甲保持。用户肯定f27斜侧稿整体状态，以此保留体量；最新参考擎天柱挺拔体态修缩脖子，协调短实颈部、肩线和胸甲上沿。具体R8新稿未自动采用。',
    current_art_reference=BASE+direction_name,
    asset_status='preferred_whole_body_state_posture_correction_authorized_new_drawing_candidate',
    source_refs=';'.join([BASE+'M11-head-selected-and-turnaround-r6.json',BASE+'M11-head-aspect-chin-direction-r7.json',BASE+direction_name,BASE+production_name]),
    notes='用户正面反馈优先于作者旧斜角/背架偏好；参考体态不复刻具体头脸。R7旧三视与头仓未按R8肩颈同步，整机装配/受力仍待校核。')
save_tsv(f,fields,rows)
f=PROJECT/'docs/superpowers/specs/data/canon/authority_overrides.tsv'
fields,rows=load_tsv(f)
r=next(x for x in rows if x['record_type']=='art_lock' and x['record_id']=='CML137')
r.update(version_scope='M11_preferred_whole_body_state_neck_posture_direction_20261021',
    source_of_truth=BASE+direction_name,last_confirmed=DATE,
    notes='用户肯定f27整体状态后要求参考擎天柱体态修缩脖子；保留CML138头型、R2长腿及勇者颏甲。R8新绘制稿未自动采用；旧三视与收纳结构待同步。')
save_tsv(f,fields,rows)
f=PROJECT/'docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md'
s=f.read_text()
entry='- 2026-10-21用户肯定货柜领袖f27斜侧稿整体状态，随后要求参考擎天柱体态修正缩脖子。CML137按'+BASE+direction_name+'更新：保留原头、颏甲、长腿与原稿体量，协调颈部露出、肩线及胸甲上沿。R8斜侧源稿已绘，旧三视与头仓活动结构尚未同步；新图未自动采用，不推进剧情或运行。\n\n'
if entry not in s: s=s.replace('## 一、当前结论\n\n','## 一、当前结论\n\n'+entry,1)
f.write_text(s)
print('M11 R8 posture correction recorded in existing batch.')

