"""Register the user's source-design freeze; no runtime or other-chat writes."""
from pathlib import Path
import csv
import hashlib
import html
import json
import shutil

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
DATE = '2026-10-18'
RECEIPT = 'source-design-freeze-20261018.json'
READER = 'source-design-freeze-20261018.html'
QUOTE = '那么目前社勇王素材资产、角色的相关资产，这一批的设计可以先固定了'
SCOPE = '本批具体图稿的形象、造型、配色、画法及所列装配/状态设计固定；模型、裁切透明边、动作、声音和游戏运行仍按制作结果分别验证。'

def read(name):
    return json.loads((P / name).read_text())

def save(name, obj):
    (P / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def backup(name):
    target = P / 'history/design-freeze-20261018' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(P / name, target)

if (P / RECEIPT).exists():
    raise SystemExit('Design freeze already registered. Preserve its exact files and dated snapshots; later handoff belongs in the existing dispatch log.')

names = ['brave-components-production-r12.json', 'design-followthrough-r1.json',
         'user-art-decisions-20261016.json', 'dialogue-production-r2.json',
         'supporting-character-production-r3.json', 'people-expression-production-r1.json',
         'sample-author-review.json', 'brave-components-verification-r12.json',
         'brave-components-r8.html', 'index.html', 'design-followthrough-section.html',
         'direction-revision-content.md']
for name in names:
    backup(name)

art = read('brave-components-production-r12.json')
dialogue = read('dialogue-production-r2.json')
supporting = read('supporting-character-production-r3.json')
expressions = read('people-expression-production-r1.json')
entries = {}

def add(item, group, role, identity=None):
    path = P / item['file']
    digest = sha(path)
    assert digest == item.get('sha256', digest), 'Source changed: ' + item['file']
    entry = {'file': item['file'], 'sha256': digest, 'bytes': path.stat().st_size,
             'group': group, 'role': role, 'source_design_fixed': True}
    if item.get('pixel_size'):
        entry['pixel_size'] = item['pixel_size']
    if identity:
        entry['identity'] = identity
    entries.setdefault(item['file'], entry)

for item in art['current_set']:
    add(item, 'mecha', item['title'] + '；' + item['role'])
for item in art['supplements']:
    add(item, 'mecha_supplement', item['observed'])
    if item.get('editable_source'):
        add({'file': item['editable_source']}, 'editable_diagram', item['observed'])
for record, kind in [(dialogue, '人物立绘母稿'), (supporting, '人物配色母稿'),
                     (expressions, '本批单张表情设计')]:
    for item in record['items']:
        add(item, 'characters', item['name'] + ' · ' + item.get('label', kind), item['id'])

excluded = [
    {'file': 'samples/H02-baiyuan-dialogue-r1.png', 'reason': '旧三手母稿；采用R2双手修正版。'},
    {'file': 'samples/H02-baiyuan-concentrating-r1-rejected-three-hands.png', 'reason': '继承三手错误的表情稿；采用R2。'},
    {'file': 'samples/F11-drill-assembly-r8.png', 'reason': '腿部履带与整机不一致；采用既定整机及R12部件归属。'},
    {'file': 'samples/F11-leg-kit-source-locked-r9.png', 'reason': '错误长腿比例，不作正向制作来源。'},
    {'file': 'samples/F11-leg-proportion-redraw-r10.png', 'reason': '未进入最终选择，仅保留历史补充。'},
    {'file': 'samples/F12-train-two-states-r12a-rejected.png', 'reason': '错误封闭长车厢和粘附拳头。'},
    {'file': 'samples/F12-train-two-states-r12b-rejected.png', 'reason': '重复车头、封闭车厢，停止采用。'},
]
for item in excluded:
    item['sha256'] = sha(P / item['file'])
    item['production_allowed'] = False

receipt = {
    'revision': 'source-design-freeze-20261018', 'date': DATE,
    'status': 'user_confirmed_current_batch_design_fixed',
    'authority_level': 'working', 'authority': 'direct_user_message_in_this_chat',
    'authority_registration': {'art_lock': 'CML132', 'scope': 'internal_art_upgrade_20261018_source_design_only'},
    'verbatim': QUOTE, 'acceptance_scope': SCOPE,
    'existing_batch': 'design-followthrough-r1.json', 'reader': READER,
    'scope': ['M04社勇王整机', 'F09勇拳完整核心', '轰炸机', '海底列车', '钻探机',
              'H01纪存', 'H02白鸢', 'H03七海', 'H04兜灯', 'H07唐胶', 'H09胶价王',
              '上述人物本批默认立绘及各一张表情稿'],
    'source_precedence': {
        'combined_silhouette_and_proportion': 'samples/M04-front-backpack-fins-r7.png',
        'side': 'samples/M04-side-body-reviewed-r6d.png',
        'rear': 'samples/M04-rear-exhaust-corrected-r6b.png',
        'core': 'samples/F09-brave-core-master-r2.png',
        'process_and_local_fixes': 'brave-components-production-r12.json',
        'rule': '整机规定比例/轮廓，所列当前局部修正版规定修正部位；过程图说明归属与状态，不反向改写整机。未列入当前清单的原选变体/旧图只作历史追溯。',
        'identity_boundary': '本批源图取代本批旧派生输入；不改现有身份、国籍、登场阶段、同一物理核心与其他生命周期约束。旧GF画面可留动作语言参考，不与本批新形象竞争正向制图母稿。'
    },
    'fixed_features': [
        '完整勇拳是同一物理核心，保留长发和原头；社勇王头冠/面罩来自轰炸机内舱加载，不更换主体或凭空长冠。',
        '保留已选壮实躯干、巨拳重量、整机头身与腿足比例，不再生成细长小腿。',
        '轰炸机为钝机鼻胸甲、分离肩翼/发动机和双竖翼双格栅背包；进气朝前、排气朝后。',
        '列车中缝拆成两节，一节一臂，车头朝肘后、联接端朝拳，壳体收近/展开但巨拳始终独立。',
        '钻探机两半分别附到两腿，膝钻、前后带面、侧轮、分段胫甲、独立踝足与宽靴依当前整机；R12图说明部件去向。',
        '统一当前画法与材质语言，保留轰炸机石墨、列车象牙白、钻机橙白的分工；不统一洗色。',
        '六名角色依当前母稿保留脸、发型、服装、道具、体型与各自配色；白鸢只用双手修正版。'
    ],
    'production_policy': {
        'allowed': ['沿固定源图做低模、分件、UV、贴图、材质、绑定、共享动作适配和同源裁切',
                    '修复透明边、图层、导出与技术性穿插，并保留设计识别点',
                    '按已定部件与状态做合理近似演出，无需逐对精密碰撞或真实机械折变'],
        'changes_requiring_new_design_decision': ['明显改变头冠/面罩、胸框、肩翼、巨拳、腿足比例或部件朝向/归属',
                                                '换角色脸/发型/服装/体型或重新定义英雄色'],
        'source_design_pending': False,
        'model_generation_dispatched': False, 'runtime_replacement_dispatched': False,
        'other_chat_ledger_written': False,
        'handoff': '本批设计已确认，可集中交接本清单；本次未发消息或向其他会话分派工作。'
    },
    'files': list(entries.values()), 'excluded_history': excluded,
    'remaining_production_checks': ['模型隐藏面、分件/关节净空和正常战棋镜头辨识',
                                    '连续动作、声音与运行性能',
                                    '人物透明边/裁切眼线与实际表情切换；H02/H07表情角像素1/255仍需导出边缘检查'],
    'runtime_assets_replaced': False, 'runtime_user_accepted': False,
    'whole_project_completed': False, 'handoff_sent': False
}

art.update(user_accepted=True, acceptance_scope=SCOPE, source_user_review_pending=False,
           source_design_fixed=True, design_freeze_record=RECEIPT,
           model_hold='source_design_confirmed_downstream_production_not_dispatched',
           model_handoff_ready=True)
art['user_acceptance'] = {'date': DATE, 'verbatim': QUOTE, 'scope': 'current_batch_source_design', 'record': RECEIPT}
art['remaining'] = receipt['remaining_production_checks']
for item in art['consistency_review']:
    item.update(status='source_design_fix_accepted_in_batch_freeze', new_user_accepted=True,
                acceptance_record=RECEIPT)
save('brave-components-production-r12.json', art)

for record, name in [(dialogue, 'dialogue-production-r2.json'),
                     (supporting, 'supporting-character-production-r3.json'),
                     (expressions, 'people-expression-production-r1.json')]:
    record.update(source_design_fixed=True, design_freeze_record=RECEIPT,
                  acceptance_scope=SCOPE,
                  handoff_status='source_design_confirmed_ready_for_grouped_transfer_not_sent')
    for item in record['items']:
        item.update(source_design_fixed=True, source_design_user_accepted=True,
                    design_freeze_record=RECEIPT, acceptance_scope='本批具体二维设计；运行及导出技术质量另验')
        for flag in ['export_user_accepted', 'exact_new_drawing_accepted',
                     'identity_and_drawing_direction_accepted', 'expression_user_accepted']:
            if flag in item:
                item[flag] = True
        item['current_status'] = 'source_design_fixed_runtime_separate'
        if 'identity_acceptance_scope' in item:
            item['identity_acceptance_scope'] = 'R2身份/画法及R3本批配色设计现已固定；技术导出与运行分别验证。'
        if 'dispatch_status' in item:
            item['dispatch_status'] = 'source_design_confirmed_ready_not_sent'
    if 'final_color_user_accepted' in record.get('checks', {}):
        record['checks']['final_color_user_accepted'] = True
    if 'user_export_acceptance' in record.get('checks', {}):
        record['checks']['source_design_user_accepted'] = True
        record['checks']['user_export_acceptance_scope'] = 'source design only; crop/alpha/runtime technical QA remains separate'
    if name == 'people-expression-production-r1.json':
        record['remaining'] = ['实际表情状态选择/回退、切换连续性与裁切眼线由运行接入验证。',
                               '当前每人一张替代表情不扩大为全表情家族；保留透明边检查。']
    save(name, record)

decisions = read('user-art-decisions-20261016.json')
for item in decisions['accepted_character_identities']:
    master = next(q for q in dialogue['items'] + supporting['items'] if q['id'] == item['id'])
    item.setdefault('previous_reference_before_design_freeze', {
        'file': item['current_reference_from_reader'], 'sha256': item['reference_sha256'], 'scope': item['scope']})
    item.update(current_reference_from_reader=master['file'], reference_sha256=master['sha256'],
                scope='本批当前立绘母稿及所列同源表情的设计固定；技术派生和运行另验。',
                design_freeze_record=RECEIPT)
decisions['current_design_freeze'] = {'date': DATE, 'record': RECEIPT, 'reader': READER,
                                     'verbatim': QUOTE, 'scope': SCOPE}
if not any(x.get('verbatim') == QUOTE for x in decisions['followup_decisions']):
    decisions['followup_decisions'].append({'date': DATE, 'authority': 'direct_user_message_in_this_chat',
                                          'verbatim': QUOTE, 'record': RECEIPT, 'scope': SCOPE})
save('user-art-decisions-20261016.json', decisions)

batch = read('design-followthrough-r1.json')
batch.update(source_design_fixed=True, design_freeze_record=RECEIPT,
             canon_changed=True, canon_change_scope='仅登记Working美术源范围CML132；身份、故事、运行未变',
             handoff_status='source_design_confirmed_ready_for_grouped_transfer_not_sent')
batch['model_hold'].update(state='source_design_confirmed_downstream_not_dispatched',
                           resume='本批设计等待条件已由用户确认解除；后续制作仍走主线既有接入安排，不在本次自动启动。',
                           resolved_by=RECEIPT)
batch['not_done'] = receipt['remaining_production_checks'] + ['本次未发送交接，未修改主工程或主会话台账。']
batch['experience_record_r12'].update(new_user_accepted=True, source_design_fixed=True,
                                     user_acceptance_record=RECEIPT)
for finding in batch['experience_record_r12']['author_review']['findings']:
    finding.update(status='source_design_fix_accepted_in_batch_freeze', new_user_accepted=True,
                   acceptance_record=RECEIPT)
batch['source_design_freeze'] = {'date': DATE, 'verbatim': QUOTE, 'record': RECEIPT,
                                'current_source_record': 'brave-components-production-r12.json',
                                'file_count': len(entries), 'runtime_accepted': False}
save('design-followthrough-r1.json', batch)

review = read('sample-author-review.json')
review['current_design_freeze'] = {'date': DATE, 'record': RECEIPT, 'scope': SCOPE, 'user_confirmed': True}
review['baiyuan_hand_defect_20261017']['user_repair_acceptance'] = True
review['brave_components_r12'].update(new_user_accepted=True, design_freeze_record=RECEIPT)
for finding in review['brave_components_r12']['findings']:
    finding.update(status='source_design_fix_accepted_in_batch_freeze', new_user_accepted=True,
                   acceptance_record=RECEIPT)
for item in review['defect_ledger']:
    item['source_design_resolution'] = {'date': DATE, 'record': RECEIPT,
                                        'status': 'current_source_design_accepted',
                                        'excludes': 'technical model/projection/runtime validation'}
    if 'current_author_result' in item:
        item['current_author_result'] = '本批当前源图已由用户固定；模型、隐藏面/活动及运行验证仍分开。'
    if 'remaining' in item:
        item['remaining'] = '源图设计等待已解除；严格同模型视图、隐藏面与运行活动仍待制作验证。'
save('sample-author-review.json', review)

receipt['source_records'] = [{'file': name, 'sha256': sha(P / name)} for name in names[:7]]
save(RECEIPT, receipt)

E = lambda s: html.escape(str(s), quote=True)
portraits = ''.join(f'<figure><a href="{E(x["file"])}"><img src="{E(x["file"])}" alt="{E(x["name"])}本批固定母稿"></a><figcaption>{E(x["id"])} · {E(x["name"])}</figcaption></figure>' for x in dialogue['items'] + supporting['items'])
file_rows = ''.join(f'<tr><td>{E(x["role"])}</td><td><a href="{E(x["file"])}">{E(Path(x["file"]).name)}</a></td><td><code>{x["sha256"][:16]}</code></td></tr>' for x in receipt['files'])
features = ''.join(f'<li>{E(x)}</li>' for x in receipt['fixed_features'])
excluded_rows = ''.join(f'<li><a href="{E(x["file"])}">{E(Path(x["file"]).name)}</a>：{E(x["reason"])}</li>' for x in excluded)
page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>本批设计固定｜社勇王与六名角色</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f4f1e8;color:#22323b;font:17px/1.7 system-ui,-apple-system,sans-serif}}main{{max-width:1150px;margin:auto;padding:48px 28px}}h1{{font-size:38px;line-height:1.3}}h2{{margin-top:50px;font-size:25px}}a{{color:#236768}}.tag{{color:#236768;font-weight:700}}.notice{{border-left:5px solid #d56d30;padding:14px 24px;background:#fffdf7}}.hero{{display:block;max-width:650px;width:100%;margin:24px auto}}.people{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}figure{{margin:0;background:#e2e8e2;padding:12px;border-radius:8px}}figure img{{width:100%;height:350px;object-fit:contain}}figcaption{{text-align:center;font-weight:650}}table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{text-align:left;padding:12px;border-bottom:1px solid #cbd1cb;vertical-align:top}}.scroll{{overflow:auto}}code{{font-size:12px}}li{{margin:12px 0}}@media(max-width:700px){{.people{{grid-template-columns:repeat(2,1fr)}}figure img{{height:280px}}h1{{font-size:29px}}main{{padding:25px 18px}}}}
</style></head><body><main><p class="tag">2026.10.18 · 用户确认 · 当前批次设计基准</p><h1>社勇王、四机组件与六名角色<br>本批设计先固定</h1><div class="notice"><p>用户原话：“{E(QUOTE)}”</p><p>当前源图已固定，后续从这套设计制作模型、材质、动作和同源人物资源。明显改变造型或部件关系时另作设计决定；不再沿失败稿反复重画。</p></div><p><a href="brave-components-r8.html#redraw-r12">查看四机全部当前图与部件设计</a> · <a href="index.html#design-followthrough-20261017">返回升级总页</a> · <a href="{RECEIPT}">完整文件与校验清单</a></p>
<img class="hero" src="samples/M04-front-backpack-fins-r7.png" alt="固定的社勇王整机比例与轮廓母稿"><h2>这套设计继续保留什么</h2><ul>{features}</ul><h2>六名角色的当前母稿</h2><p>纪存、白鸢、七海，以及兜灯、唐胶、胶价王的最新配色稿；每人本批一张替代表情也登记在下表。固定的是本批设计，裁切、透明边和游戏内切换仍检查实际结果。</p><div class="people">{portraits}</div>
<h2>唯一当前制作输入：{len(entries)}个文件</h2><p>正侧背、四机单体、局部修正、装配/状态图与人物派生均逐个绑定文件校验。整机主稿规定比例；局部修正规定对应部位，过程图不反向重造整机。</p><div class="scroll"><table><thead><tr><th>负责内容</th><th>当前文件</th><th>SHA-256前16位</th></tr></thead><tbody>{file_rows}</tbody></table></div>
<h2>明确排除的旧稿</h2><ul>{excluded_rows}</ul><h2>接下来按固定设计制作</h2><p>可做低模、分件、UV、贴图、材质、绑定、共享动作适配和同源裁切。技术性修边或净空调整不能演变成重新设计头胸、肩翼、拳体、腿长或角色形象。</p><p>本次解除本批源图的“等待设计确认”。未在此启动三维任务、发送交接或修改其他会话台账。模型、连续音画、正常战棋镜头与运行接入按真实制作结果分别验证；整项工务城整改状态不因设计固定而改为完成。</p></main></body></html>'''
(P / READER).write_text(page)
print(f'Design fixed: {len(entries)} current files, {len(excluded)} explicit historical exclusions; runtime untouched.')
