#!/usr/bin/env python3
"""Publish source-bound art adoption review and samples. No runtime/Canon writes."""
from pathlib import Path
import csv, hashlib, html, json, os, re
from collections import Counter

PROJECT = Path(__file__).resolve().parents[4]
ROOT = PROJECT / 'captures/20261014-full-direction'
OUT = Path(__file__).resolve().parent
PAGE = ROOT / 'review-v2.html'
OLD = ROOT / 'review/20261015-latest-review'
TASK = PROJECT / 'docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate'
LABELS = {'D':'二维原画可加工采用','M':'结构与造型母版可采用','R':'内部修订后派生','V':'图形、版式与演出参考'}
NEXT = {
 'D':'保留主体设计；去除版头与伪字，按用途导出透明立绘、统一眼线的头肩头像或分层背景。二维资源可先进入候选接入，不代替三维单位。',
 'M':'保留本图的主体结构与识别点；沿母版做低模、UV和贴图，需要活动的对象再适配共享骨架/动作。由真实模型派生头像与状态，不把背景JPEG当作战斗模型。',
 'R':'保留本图已经成立的画法和可取局部，由项目内部沿既有身份/功能母版修订；同一对象先统一再派生，不继续向外援逐张追求完美。',
 'V':'采用已成立的符号、镜位或时序含义；按真实效果事件重制为矢量、材质、分层图或共享动画配置。生成伪字、固定数字与整张说明板不进入游戏。'
}
def esc(s): return html.escape(str(s), quote=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p, base=OUT): return os.path.relpath(p, base).replace(os.sep,'/')
def write_json(p, data): p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

inventory = json.loads((OUT/'latest-card-inventory.json').read_text())
previous = {r['id']:r for r in json.loads((OLD/'latest-review-data.json').read_text())['records']}
patches = {r['id']:r for r in csv.DictReader((OUT/'review-r4.tsv').open(), delimiter='\t')}
mapping_rows = list(csv.DictReader((TASK/'外援美术制作清单-20261012/接入替换映射.csv').open()))
mapping = {r.get('\ufeff编号',r.get('编号')):r for r in mapping_rows}
decisions = json.loads((OUT/'user-art-decisions-20261016.json').read_text())
accepted_ids={r['id'] for r in decisions['accepted_character_identities'] if r['identity_direction_accepted']}
accepted_receipts={r['id']:r for r in decisions['accepted_character_identities'] if r['identity_direction_accepted']}
dialogue_record_path=next((OUT/name for name in ['dialogue-production-r2.json','dialogue-production-r1.json'] if (OUT/name).exists()),OUT/'dialogue-production-r1.json')
dialogue_export_record=json.loads(dialogue_record_path.read_text()) if dialogue_record_path.exists() else None
dialogue_exports={r['id']:r for r in dialogue_export_record['items']} if dialogue_export_record else {}
supporting_record_path=next((OUT/name for name in ['supporting-character-production-r3.json','supporting-character-production-r2.json','supporting-character-production-r1.json'] if (OUT/name).exists()),OUT/'supporting-character-production-r1.json')
supporting_export_record=json.loads(supporting_record_path.read_text()) if supporting_record_path.exists() else None
if supporting_export_record:dialogue_exports.update({r['id']:r for r in supporting_export_record['items']})
brave_record_path=next((OUT/name for name in ['brave-production-r4.json','brave-production-r3.json','brave-production-r2.json','brave-production-r1.json'] if (OUT/name).exists()),OUT/'brave-production-r1.json')
brave_source_record=json.loads(brave_record_path.read_text()) if brave_record_path.exists() else None
followthrough_path=OUT/'design-followthrough-r1.json'
followthrough=json.loads(followthrough_path.read_text()) if followthrough_path.exists() else None
component_record_path=OUT/followthrough['component_design_record'] if followthrough and followthrough.get('component_design_record') else None
component_source_record=json.loads(component_record_path.read_text()) if component_record_path else None
expression_path=OUT/'people-expression-production-r1.json'
expression_record=json.loads(expression_path.read_text()) if expression_path.exists() else None
expression_exports={r['id']:r for r in expression_record['items']} if expression_record else {}
freeze_path=OUT/'source-design-freeze-20261018.json'
freeze=json.loads(freeze_path.read_text()) if freeze_path.exists() else None
for source in decisions['refs'].values():
    assert sha(OUT/source['frozen_copy'])==source['sha256'], 'Selected source changed'
for receipt in decisions['accepted_character_identities']:
    assert sha((OUT/receipt['current_reference_from_reader']).resolve())==receipt['reference_sha256'], 'Accepted identity source changed'
production_keys={
 'M03':['guardian_project_identity','guardian_external_option'],
 'M04':['brave_v17','brave_v18','brave_v19','brave_core_longhair_v11','bomber_v17','subtrain_v17','drill_v17'],
 'F09':['brave_core_longhair_v11'], 'F10':['brave_v17','brave_v18','brave_v19','brave_core_longhair_v11'],
 'F11':['brave_v18','drill_v17'], 'F12':['brave_v17','brave_v18','bomber_v17','subtrain_v17'],
 'S14':['brave_v17','brave_v18','brave_v19','brave_core_longhair_v11'],
 'N14':['brave_v17','brave_v18','brave_v19','brave_core_longhair_v11'],
 'N11':['brave_v17','brave_v19','brave_core_longhair_v11'],
 'H04':['doudeng_project_shape'],'H07':['tangjiao_project_shape'],'H09':['jiaojia_project_shape']
}

assert len(inventory)==298 and sum(x['changed'] for x in inventory)==43
assert all(x['id'] in patches for x in inventory if x['changed'])

delivered_by_id = {x['id']:dict(x) for x in inventory}
# These are semantically swapped files. Preserve every original byte and filename.
actual = {x['id']:dict(x) for x in inventory}
actual['M03']['file'] = delivered_by_id['S11']['file']
actual['S11']['file'] = delivered_by_id['M03']['file']
records=[]
for x in inventory:
    id=x['id']; old=previous[id]; p=patches.get(id); group=id[0]
    route = p['route'] if p else ('V' if group in 'XGC UIN'.replace(' ','') else 'D' if (group=='H' and old['verdict']=='A') or (group=='S' and old['verdict']=='A') else 'M' if old['verdict']=='A' else 'R')
    src=ROOT/actual[id]['file']; assert src.is_file()
    m=mapping.get(id,{})
    record={
      'id':id,'group':group,'name':x['name'],'route':route,'route_label':LABELS[route],
      'image':actual[id]['file'],'sha256':sha(src),'size_bytes':src.stat().st_size,
      'changed_image':bool(x['changed']),'fresh_opinion':id in patches,
      'binding_corrected':id in ['M03','S11'],
      'delivered_label_image':delivered_by_id[id]['file'],
      'retained':p['use'] if p else old['use'],
      'current_issue':p['issue'] if p else ('图像未变，本轮按原主体与用途接收；前轮详细问题保留在历史意见中。关联新稿的结论以本轮对应卡片为准。' if old['verdict']=='A' else '本图未换稿，原有设定/功能或表现问题仍由内部修订；见下方前轮具体诊断。关联新稿已改善的问题不重复作为本图退稿理由。'),
      'internal_next':p['next'] if p else NEXT[route],
      'prior_specific_issue':old['content'],'prior_specific_next':old['revision'],
      'related':old.get('related',[]),'issue_tags':old.get('issue_tags',[]),
      'current_assets':m.get('当前资源','').splitlines(),
      'loaders':m.get('接入位置','').splitlines(),
      'original_requirement':old.get('required_files',[]),
      'runtime_replaced':False,'runtime_user_accepted':False,
      'identity_direction_accepted':id in accepted_ids,
      'identity_acceptance_scope':accepted_receipts[id]['scope'] if id in accepted_ids else '',
      'identity_accepted_reference':str((OUT/accepted_receipts[id]['current_reference_from_reader']).resolve().relative_to(PROJECT)) if id in accepted_ids else '',
      'identity_accepted_reference_sha256':accepted_receipts[id]['reference_sha256'] if id in accepted_ids else '',
      'production_refs':[str((OUT/decisions['refs'][key]['frozen_copy']).relative_to(PROJECT)) for key in production_keys[id]] if id in production_keys else [str((OUT/next(r['current_reference_from_reader'] for r in decisions['accepted_character_identities'] if r['id']==id)).resolve().relative_to(PROJECT))] if id in accepted_ids else [str(src.relative_to(PROJECT))],
      'user_decision_ref':str((OUT/'user-art-decisions-20261016.json').relative_to(PROJECT)),
      'identity_reference_status':'explicit_user_direction' if id in accepted_ids else 'candidate_pending_distinctive_revision' if id=='M01' else 'selected_parts_or_shape_restyle' if id in production_keys else 'source_review_only'
    }
    if id=='M01':record['production_refs']=[str((OUT/'samples/M01-independent-master-v3.png').relative_to(PROJECT))]
    if id in accepted_ids and record['identity_accepted_reference'] not in record['production_refs']:
        record['production_refs'].append(record['identity_accepted_reference'])
    if id in dialogue_exports:
        export=dialogue_exports[id]
        export_path=OUT/export['file']
        assert sha(export_path)==export['sha256'], 'Dialogue export changed'
        ref_path=str(export_path.relative_to(PROJECT))
        if ref_path not in record['production_refs']:record['production_refs'].append(ref_path)
        if export.get('style_reference'):
            assert sha(OUT/export['style_reference'])==export['style_reference_sha256'], 'Portrait style reference changed'
            record['production_refs'].append(str((OUT/export['style_reference']).relative_to(PROJECT)))
        record['derived_dialogue_export']={'file':ref_path,'sha256':export['sha256'],'frame_record':str((OUT/export.get('frame_record',dialogue_record_path.name)).relative_to(PROJECT)),'parent_identity_accepted':id in accepted_ids,'parent_shape_selected':bool(export.get('shape_policy_user_selected',id in accepted_ids)),'export_user_accepted':False,'runtime_integrated':False,'current_status':export.get('current_status','derivative_candidate')}
    if brave_source_record and id in ['M04','F10','F12','S14','N11','N14']:
        body=brave_source_record['full_body'];arm=brave_source_record['arm_structure']
        assert sha(OUT/body['file'])==body['sha256'], 'Combined body source changed'
        for candidate in [body['file'],arm['current']]:
            candidate_ref=str((OUT/candidate).relative_to(PROJECT))
            if candidate_ref not in record['production_refs']:record['production_refs'].append(candidate_ref)
        if brave_source_record.get('bomber_component'):
            component=brave_source_record['bomber_component']
            assert sha(OUT/component['file'])==component['sha256'], 'Bomber component source changed'
            record['production_refs'].append(str((OUT/component['file']).relative_to(PROJECT)))
        record['derived_combined_design']={'record':str(brave_record_path.relative_to(PROJECT)),'kind':'unaccepted integrated source candidate','user_design_accepted':False,'model_produced':False,'runtime_integrated':False,'current_status':brave_source_record.get('current_status','unaccepted_candidate')}
    if id in expression_exports:
        expression=expression_exports[id]
        assert sha(OUT/expression['file'])==expression['sha256'], 'Expression export changed'
        record['production_refs'].append(str((OUT/expression['file']).relative_to(PROJECT)))
        record['derived_expression']={'record':str(expression_path.relative_to(PROJECT)),'state':expression['state'],'file':str((OUT/expression['file']).relative_to(PROJECT)),'sha256':expression['sha256'],'user_accepted':expression.get('source_design_user_accepted',False),'acceptance_scope':expression.get('acceptance_scope',''),'runtime_integrated':False,'handoff_sent':False}
    if id=='H02' and dialogue_export_record.get('previous_record'):
        record['known_invalid_derivative']={'file':'samples/H02-baiyuan-dialogue-r1.png','reason':'three hands; user reported, old mother also examined','replacement':record['derived_dialogue_export']['file'],'replacement_user_accepted':False,'replacement_runtime_integrated':False}
    if followthrough and id in ['F09','M04','F10','F11','F12','S14','N11','N14']:
        selected=followthrough['core'] if id=='F09' else followthrough['full_body']
        assert sha(OUT/selected['file'])==selected['sha256'], 'Followthrough source changed'
        selected_ref=str((OUT/selected['file']).relative_to(PROJECT))
        if selected_ref not in record['production_refs']:record['production_refs'].append(selected_ref)
        record['design_followthrough']={'record':str(followthrough_path.relative_to(PROJECT)),'user_accepted':False,'model_hold':'paused_design_pending','runtime_integrated':False,'handoff_sent':False}
        if id!='F09' and followthrough.get('latest_front_revision_record'):
            record['front_view_revision']={'record':str((OUT/followthrough['latest_front_revision_record']).relative_to(PROJECT)),'current_file':selected_ref,'sha256':selected['sha256'],'current_status':selected['status'],'user_accepted':selected.get('user_accepted',False),'acceptance_scope':'front appearance only','runtime_integrated':False}
        if id!='F09' and followthrough.get('corrected_side_view'):
            side=followthrough['corrected_side_view']
            assert sha(OUT/side['file'])==side['sha256'], 'Corrected side source changed'
            record['production_refs'].append(str((OUT/side['file']).relative_to(PROJECT)))
            record['side_view_revision']={'record':str((OUT/followthrough['side_correction_record']).relative_to(PROJECT)),'current_file':str((OUT/side['file']).relative_to(PROJECT)),'old_file_status':'user_rejected_inconsistent_with_front_history_only','current_status':side.get('current_use','revised_candidate_not_exact_model_projection'),'user_selected_reference':side.get('current_use')=='user_selected_reference_20261018','user_accepted':False,'runtime_integrated':False}
        if id!='F09' and followthrough.get('corrected_rear_view'):
            rear=followthrough['corrected_rear_view']
            assert sha(OUT/rear['file'])==rear['sha256'], 'Rear source changed'
            record['production_refs'].append(str((OUT/rear['file']).relative_to(PROJECT)))
            record['rear_view_revision']={'record':str((OUT/followthrough['latest_body_review_record']).relative_to(PROJECT)),'current_file':str((OUT/rear['file']).relative_to(PROJECT)),'current_status':rear.get('current_use','rear_three_quarter_source_candidate_not_locked'),'user_selected_reference':rear.get('current_use')=='user_selected_reference_20261018','user_accepted':False,'runtime_integrated':False}
    if component_source_record and id in ['F09','M04','F10','F11','F12','S14','N11','N14']:
        component_ids={'F09':['F09'],'F11':['F11'],'F12':['F12-bomber','F12-train'],'N11':['F09','F12-train']}.get(id,[a['id'] for a in component_source_record['assets']])
        component_files=[]
        for asset in component_source_record['assets']:
            if asset['id'] not in component_ids:continue
            for kind in [kind for kind in ['master','views','assembly','assembly_terminal','fold_map','protective_cradle','state_framework'] if asset.get(kind)]:
                part=asset[kind]
                assert sha(OUT/part['file'])==part['sha256'], 'Four-machine design source changed: '+part['file']
                ref=str((OUT/part['file']).relative_to(PROJECT))
                if ref not in record['production_refs']:record['production_refs'].append(ref)
                component_files.append({'component':asset['id'],'kind':kind,'file':ref,'sha256':part['sha256'],**({'source_region_pixels':part['source_region_pixels'],'presentation':part['presentation']} if part.get('source_region_pixels') else {})})
        record['four_machine_design']={'record':str(component_record_path.relative_to(PROJECT)),'reader':str((OUT/component_source_record['delivery_reader']).relative_to(PROJECT)),'files':component_files,'user_accepted':component_source_record.get('user_accepted',False),'acceptance_scope':component_source_record.get('acceptance_scope',''),'open_corrections':[item['id'] for item in component_source_record.get('consistency_review',[]) if not item.get('new_user_accepted')],'view_kind':'source_design_drawings_not_same_model_projections','model_produced':False,'runtime_integrated':False,'handoff_sent':False}
        if component_source_record.get('selected_set'):
            selection_scope={'F09':[6,9,11],'F11':[1,2,5,10],'F12':[1,2,3,4,7,8,9,10],'N11':[6,7,9,11]}.get(id,list(range(1,12)))
            selected_sources=[item for item in component_source_record.get('current_set',component_source_record['selected_set']) if item['number'] in selection_scope]
            record['historical_production_refs']=record['production_refs']
            record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in selected_sources]
            for component_file in component_files:
                if component_file['file'] not in record['production_refs']:record['production_refs'].append(component_file['file'])
            record['selected_art_baseline']={'record':str(component_record_path.relative_to(PROJECT)),'user_accepted':True,'acceptance_scope':component_source_record['acceptance_scope'],'baseline_files':component_source_record['selected_set'],'current_files':selected_sources,'local_corrections_drawn':component_source_record.get('source_revision_drawn',False),'local_corrections_user_accepted':component_source_record.get('user_accepted',False),'local_corrections_completed':component_source_record.get('source_design_fixed',False),'completion_scope':'source design only; model/runtime separate'}
            if record.get('derived_combined_design'):record['derived_combined_design']['superseded_for_production_by']=str(component_record_path.relative_to(PROJECT))
    if freeze and id in ['H01','H02','H03','H04','H07','H09','F09','M04','F10','F11','F12','S14','N11','N14']:
        record['source_design_freeze']={'record':str(freeze_path.relative_to(PROJECT)),'status':freeze['status'],'acceptance_scope':freeze['acceptance_scope'],'runtime_user_accepted':False}
        if id in dialogue_exports:
            record['historical_production_refs']=record['production_refs']
            record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in freeze['files'] if item.get('identity')==id]
            record['derived_dialogue_export'].update(export_user_accepted=True,current_status='source_design_fixed_runtime_separate',acceptance_scope='current source design; crop/alpha/runtime technical QA separate')
            if record.get('known_invalid_derivative'):record['known_invalid_derivative']['replacement_user_accepted']=True
        if record.get('design_followthrough'):
            record['design_followthrough'].update(user_accepted=True,model_hold='source_design_confirmed_downstream_not_dispatched')
        for field in ['front_view_revision','side_view_revision','rear_view_revision']:
            if record.get(field):record[field].update(user_accepted=True,current_status='source_design_fixed_runtime_separate')
        if record.get('design_followthrough'):record['design_followthrough']['handoff_sent']=bool(followthrough.get('new_handoff_sent'))
        if record.get('four_machine_design'):record['four_machine_design']['handoff_sent']=bool(component_source_record.get('handoff_sent'))
        if record.get('derived_expression'):record['derived_expression']['handoff_sent']=bool(expression_record.get('handoff_sent'))
    if id=='M01' and (OUT/'M01-recognition-production-r4.json').exists():
        candidate=json.loads((OUT/'M01-recognition-production-r4.json').read_text())
        assert sha(OUT/candidate['file'])==candidate['sha256'], 'M01 candidate source changed'
        field='rejected_head_reference' if candidate.get('head_design_user_rejected') else 'next_design_candidate'
        record[field]={'file':str((OUT/candidate['file']).relative_to(PROJECT)),'sha256':candidate['sha256'],'record':str((OUT/'M01-recognition-production-r4.json').relative_to(PROJECT)),'status':candidate.get('current_status'),'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
    if id=='M01' and (OUT/'M01-head-directions-production-r5.json').exists():
        heads=json.loads((OUT/'M01-head-directions-production-r5.json').read_text())
        for head in heads['items']:assert sha(OUT/head['file'])==head['sha256'], 'Head reference changed: '+head['id']
        record['head_design_alternatives']={'record':str((OUT/'M01-head-directions-production-r5.json').relative_to(PROJECT)),'reader':str((OUT/heads['reader']).relative_to(PROJECT)),'files':heads['items'],'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_issue']='用户已否定R4长耳冠片；六种新头型分别比较，尚未选定，不回流旧相似头胸。'
        record['internal_next']='比较A中央独冠/B低位V冠/C重眉面甲/D三齿短冠/E单侧折角/F后掠翼冠；选定头型后才合回完整身体，不先批量派生。'
    if id=='M01' and (OUT/'M01-head-AE-production-r6.json').exists():
        merged=json.loads((OUT/'M01-head-AE-production-r6.json').read_text())
        assert sha(OUT/merged['file'])==merged['sha256'], 'A+E head source changed'
        record['current_head_candidate']={'record':str((OUT/'M01-head-AE-production-r6.json').relative_to(PROJECT)),'file':str((OUT/merged['file']).relative_to(PROJECT)),'sha256':merged['sha256'],'selected_direction':['A','E'],'direction_selected_by_user':True,'exact_new_drawing_user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_issue']='用户已选择A+E整合方向，要求左右对称并区别馆守Z；新绘正面/三分之四已形成，具体新图待看。'
        record['internal_next']='按A中央冠脊与E双侧短折角检查正面结构、连续视窗/封闭面甲及与现有馆守的区别；当前新图确认后再合回完整机体。'
    if id=='M01' and (OUT/'M01-head-aft-antenna-production-r7.json').exists():
        corrected=json.loads((OUT/'M01-head-aft-antenna-production-r7.json').read_text())
        assert sha(OUT/corrected['file'])==corrected['sha256'], 'Aft antenna head source changed'
        record['current_head_candidate']={'record':str((OUT/'M01-head-aft-antenna-production-r7.json').relative_to(PROJECT)),'file':str((OUT/corrected['file']).relative_to(PROJECT)),'sha256':corrected['sha256'],'selected_direction':['A','E'],'direction_selected_by_user':True,'latest_user_correction':corrected['user_directive'],'exact_new_drawing_user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_issue']='A+E头型延续，按最新意见取消双侧天线折角外张，R7已实际改成直线向后；具体修正图待确认。'
        record['internal_next']='检查两视图的直线后向天线与脸部对称；冠脊、连续视窗、封闭面甲及配色延续，确认后再合回完整机体。馆守沿用现有。'
    if id=='M01' and (OUT/'M01-head-crest-consistency-production-r8.json').exists():
        crest=json.loads((OUT/'M01-head-crest-consistency-production-r8.json').read_text())
        assert sha(OUT/crest['file'])==crest['sha256'], 'Crest consistency head source changed'
        record['current_head_candidate']={'record':str((OUT/'M01-head-crest-consistency-production-r8.json').relative_to(PROJECT)),'file':str((OUT/crest['file']).relative_to(PROJECT)),'sha256':crest['sha256'],'selected_direction':['A','E'],'direction_selected_by_user':True,'preserved_user_acceptance':crest['preserved_user_acceptance'],'latest_user_correction':crest['user_directive'],'exact_new_drawing_user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_issue']='用户表示R7总体可以，侧天线保持；指出中央冠脊跨视图不一致。当前R8以前视为依据，实际局部修正右侧长槽收尖与白色分段，待确认。'
        record['internal_next']='保持已认可总体、脸部及侧天线，检查同一冠脊的分段/嵌件/末端；后续以同一模型输出准确视图，再合回完整机体。馆守沿用现有。'
    if id=='M01' and (OUT/'M01-head-center-groove-production-r9.json').exists():
        groove=json.loads((OUT/'M01-head-center-groove-production-r9.json').read_text())
        assert sha(OUT/groove['file'])==groove['sha256'], 'Center groove head source changed'
        front=groove['front_view_reference']
        assert sha(OUT/front['file'])==front['sha256'], 'Front reference source changed'
        record['current_head_candidate']={'record':str((OUT/'M01-head-center-groove-production-r9.json').relative_to(PROJECT)),'file':str((OUT/groove['file']).relative_to(PROJECT)),'sha256':groove['sha256'],'front_view_reference':front,'selected_direction':['A','E'],'direction_selected_by_user':True,'preserved_user_acceptance':groove['preserved_user_acceptance'],'latest_user_correction':groove['user_directive'],'exact_new_drawing_user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_issue']='R8仍把中央黄色凹槽画成偏侧面，用户已反证。当前R9b用实际冠体顶槽投影作参考，独立重绘三分之四；正面沿R7左视图，新图待确认。'
        record['internal_next']='按同一冠体的顶面中央凹槽与全白外壁制作，保留正面、脸部、配色和已认可侧天线；不沿失败R8侧缝。整头精确视图由同一模型输出，馆守沿用现有。'
    if id=='M01' and (OUT/'M01-head-front-match-production-r10.json').exists():
        frontal=json.loads((OUT/'M01-head-front-match-production-r10.json').read_text())
        assert sha(OUT/frontal['file'])==frontal['sha256'], 'Front crown matched source changed'
        adopted=frontal['adopted_design']
        assert sha(OUT/adopted['file'])==adopted['sha256'], 'Adopted side master changed'
        record['current_head_candidate']={'record':str((OUT/'M01-head-front-match-production-r10.json').relative_to(PROJECT)),'file':str((OUT/frontal['file']).relative_to(PROJECT)),'sha256':frontal['sha256'],'adopted_three_quarter_reference':adopted,'adopted_three_quarter_user_accepted':True,'design_adoption_receipt':frontal['design_adoption_receipt'],'selected_direction':['A','E'],'direction_selected_by_user':True,'latest_user_correction':frontal['user_directive'],'exact_new_drawing_user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_issue']='用户已采用R9b头部设计，三分之四原稿保持；当前R10据此修正正面冠体与中央凹槽，新正面待确认。'
        record['internal_next']='以已采用头部为母稿派生，保持三分之四、脸部、配色和侧天线；新正面与完整机体/模型/运行分别验证，馆守沿用现有。'
    if id=='M01' and (OUT/'M01-head-twin-grooves-production-r11.json').exists():
        twin=json.loads((OUT/'M01-head-twin-grooves-production-r11.json').read_text())
        assert sha(OUT/twin['file'])==twin['sha256'], 'Twin side groove front changed'
        adopted=twin['adopted_design']
        assert sha(OUT/adopted['file'])==adopted['sha256'], 'Adopted side master changed'
        record['current_head_candidate']={'record':str((OUT/'M01-head-twin-grooves-production-r11.json').relative_to(PROJECT)),'file':str((OUT/twin['file']).relative_to(PROJECT)),'sha256':twin['sha256'],'adopted_three_quarter_reference':adopted,'adopted_three_quarter_user_accepted':True,'latest_user_interpretation':twin['latest_user_interpretation'],'correct_cross_section':twin['shared_crest_definition'],'selected_direction':['A','E'],'direction_selected_by_user':True,'exact_new_drawing_user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_issue']='用户明确左右各一道黄槽，中央应为白色实体；作者旧单中槽解释及模型参考作废。当前R11按两线修正前视，侧视保持，新图待确认。'
        record['internal_next']='按白外缘/左黄槽/白中脊/右黄槽/白外缘制作，保留已采用侧视及下方小黄块；不再沿用旧单中槽原画与模型，整机/运行分开。馆守沿用现有。'
    if id=='M01' and (OUT/'M01-turnaround-production-r12.json').exists():
        turnaround=json.loads((OUT/'M01-turnaround-production-r12.json').read_text())
        assert sha(OUT/turnaround['file'])==turnaround['sha256'], 'M01 turnaround changed'
        receipt=json.loads((OUT/'M01-head-design-fixed-20261019.json').read_text())
        for item in receipt['files']:assert sha(OUT/item['file'])==item['sha256'], 'Accepted M01 head changed'
        record['current_head_candidate'].update(exact_new_drawing_user_accepted=True,head_design_fixed=True,user_acceptance_receipt='M01-head-design-fixed-20261019.json')
        record['current_turnaround_candidate']={'record':str((OUT/'M01-turnaround-production-r12.json').relative_to(PROJECT)),'file':str((OUT/turnaround['file']).relative_to(PROJECT)),'sha256':turnaround['sha256'],'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in receipt['files']]+[str((OUT/turnaround['file']).relative_to(PROJECT))]
        record['identity_reference_status']='head_design_fixed_full_body_turnaround_candidate'
        record['current_issue']='R11双侧黄槽/白中脊头部已由用户确认，已补整机正侧背R12b；背视初稿误画前脸及腿足后局部修正，当前整机新稿待看。'
        record['internal_next']='沿已确认头部与R12b整机候选继续固定隐面及关节；手绘三视不代替同模型投影，技术导出和运行另验。馆守沿用现有。'
    if id in ['M02','M05']:
        next_record='M02-master-production-r1.json' if id=='M02' else 'M05-full-loadout-production-r1.json'
        if (OUT/next_record).exists():
            candidate=json.loads((OUT/next_record).read_text())
            assert sha(OUT/candidate['file'])==candidate['sha256'], 'Next batch mecha changed: '+id
            record['internal_source_candidate']={'record':str((OUT/next_record).relative_to(PROJECT)),'file':str((OUT/candidate['file']).relative_to(PROJECT)),'sha256':candidate['sha256'],'reader':str((OUT/'next-batch-mecha-20261019.html').relative_to(PROJECT)),'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
            record['production_refs']=[str((OUT/candidate['file']).relative_to(PROJECT))]+[str(((PROJECT if ref.get('base')=='project' else OUT)/ref['file']).resolve().relative_to(PROJECT)) for ref in candidate['source_refs']]
            record['identity_reference_status']='internal_source_sample_pending_user'
            if id=='M02':
                record['current_issue']='已沿M02头胸与象牙白/土棕/深红身份绘新样例，统一短颈重肩与厚拳；N10只取拳重，不取另一套头胸。具体新稿待看。'
                record['internal_next']='新母稿确认后派生无透视正侧背、头像和拳击动作；前探拳的透视放大不作为左右拳实际尺寸差。'
            else:
                record['current_issue']='已沿当前王者形象补全装备样例：自身右臂钻/左盾、背肩双主炮轴座、层翼/翼根推进器与腿侧舱；首稿裁切翼尖已补。新稿待看。'
                record['internal_next']='确认后固定头冠与盾徽、钻盾接口、炮翼分组及活动让位，再补结构和三视；不从手绘图推定模型运动已通过。'
    if id=='M01' and (OUT/'M01-head-position-production-r14.json').exists():
        family=json.loads((OUT/'M01-family-production-r13.json').read_text())
        position=json.loads((OUT/'M01-head-position-production-r14.json').read_text())
        assert sha(OUT/family['file'])==family['sha256'], 'M01 family body changed'
        for item in position['items']:assert sha(OUT/item['file'])==item['sha256'], 'Head option changed: '+item['id']
        record['historical_head_acceptance']='M01-head-design-fixed-20261019.json'
        record['current_head_candidate']={'record':str((OUT/'M01-head-position-production-r14.json').relative_to(PROJECT)),'items':position['items'],'user_selected':None,'author_recommended':position['author_recommended'],'exact_new_drawing_user_accepted':False,'head_design_fixed':False,'runtime_integrated':False,'handoff_sent':False}
        record['rejected_turnaround']=record.pop('current_turnaround_candidate',{})
        record['rejected_turnaround']['status']='user_requested_overall_design_rework'
        record['current_body_candidate']={'record':str((OUT/'M01-family-production-r13.json').relative_to(PROJECT)),'file':str((OUT/family['file']).relative_to(PROJECT)),'sha256':family['sha256'],'status':'body_family_candidate_head_under_revision','user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/family['file']).relative_to(PROJECT))]+[str((OUT/item['file']).relative_to(PROJECT)) for item in position['items']]
        record['identity_reference_status']='same_series_body_candidate_head_position_open'
        record['current_issue']='用户指出R12矮圆像机器河童，与王者不像同一系列；R13重整长腿小头与同族胸肩，但头顶天线仍差。现实际绘四种冠型，作者优先D、B需缩短为备选，尚未选定。'
        record['internal_next']='先选克制但有主角感的头冠，统一侧天线后向，再合回量产基础体并重补视图。王者保持旧系列豪华主角机与过武装层级；不继续固定失败R12比例。'
    if id=='M01' and (OUT/'M01-synthesis-head-production-r15.json').exists():
        synthesis=json.loads((OUT/'M01-synthesis-head-production-r15.json').read_text())
        assert sha(OUT/synthesis['file'])==synthesis['sha256'], 'M01 synthesis head changed'
        for ref in synthesis['source_refs']:assert sha(OUT/ref['file'])==ref['sha256'], 'Synthesis reference changed: '+ref['file']
        record['historical_head_position_options']=record['current_head_candidate']
        record['current_head_candidate']={'record':str((OUT/'M01-synthesis-head-production-r15.json').relative_to(PROJECT)),'file':str((OUT/synthesis['file']).relative_to(PROJECT)),'sha256':synthesis['sha256'],'reference_direction':'Baikanfu and classic Optimus Prime head architecture synthesis','exact_new_drawing_user_accepted':False,'head_design_fixed':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/synthesis['file']).relative_to(PROJECT)),record['current_body_candidate']['file']]
        record['identity_reference_status']='same_series_body_candidate_synthesis_head_pending_user'
        record['current_issue']='用户最新提出综合天威勇士与擎天柱头型。已核实际官方参考并画R15：中央低额块、方正盔体、高位侧后双天线，保留无牌脸/色系及同族颈下。新图尚未认可。'
        record['internal_next']='先看综合头部具体新稿，固定天线高度/倾角和根位后补同头正侧面、装回整机及更新三视；R14选型不替代本次新参考方向。'
    if id=='M01' and (OUT/'M01-head-proportion-production-r16.json').exists():
        proportion=json.loads((OUT/'M01-head-proportion-production-r16.json').read_text())
        assert sha(OUT/proportion['file'])==proportion['sha256'], 'M01 head proportion source changed'
        for ref in proportion['source_refs']:assert sha(OUT/ref['file'])==ref['sha256'], 'Proportion edit master changed'
        record['historical_synthesis_head']=record['current_head_candidate']
        record['current_head_candidate']={'record':str((OUT/'M01-head-proportion-production-r16.json').relative_to(PROJECT)),'file':str((OUT/proportion['file']).relative_to(PROJECT)),'sha256':proportion['sha256'],'synthesis_direction_may_continue':True,'exact_new_drawing_user_accepted':False,'head_design_fixed':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/proportion['file']).relative_to(PROJECT)),record['current_body_candidate']['file']]
        record['identity_reference_status']='synthesis_direction_retained_local_head_proportion_revision_pending'
        record['current_issue']='用户表示综合方向还行，但头反复被压扁。已局部重画R16，恢复头壳纵向体积、收拢颞侧，保留低额块/双侧后位天线/视窗面甲；新图尚待看稿。'
        record['internal_next']='按头壳本体高宽继续核对，不能以天线高度代替头高；小头通过相对身体整体缩小实现，确认新比例后再做同头多视图及整机。'
    if id=='M05' and (OUT/'M01-head-position-production-r14.json').exists():
        record['series_relationship_direction']='M01-M05-series-direction-20261019.json'
        record['internal_next']+=' 最新用户明确其为原系列钦定主角机，保持相对无牌更臃肿华丽及过度武装；两机共享装甲语法，不统一配色或装备。'
    if (OUT/'mecha-source-decisions-20261019-r17.json').exists():
        receipt=json.loads((OUT/'mecha-source-decisions-20261019-r17.json').read_text())
        if id=='M01':
            assert sha(OUT/receipt['M01']['source'])==receipt['M01']['sha256'], 'Accepted R16 head changed'
            record['current_head_candidate'].update(exact_new_drawing_user_accepted=True,head_design_fixed=True,user_acceptance_receipt='mecha-source-decisions-20261019-r17.json')
            record['identity_reference_status']='R16_head_source_accepted_full_machine_separate'
            record['current_issue']='用户明确当前R16可以，低额块、侧后双天线与正常纵向头壳固定。认可仅绑定指定头部源图；R13颈下与整机仍需合回检查。'
            record['internal_next']='沿R16头部母稿合回R13颈下，固定比例后补同头正侧背；小头通过相对身体整体缩小实现。旧R13头型不得回流，模型与运行另验。'
        if id=='M02':
            assert sha(OUT/receipt['M02']['source'])==receipt['M02']['sha256'], 'Current boxer source changed'
            record['internal_source_candidate'].update(source_direction_usable_to_continue=True,redesign_required=False,user_feedback_receipt='mecha-source-decisions-20261019-r17.json')
            record['identity_reference_status']='source_direction_usable_continue_no_redesign'
            record['current_issue']='用户表示旧拳王问题不大，沿当前R1源图继续，不重选造型。象牙白/土棕/深红、短颈重肩与厚拳保持。'
            record['internal_next']='按当前母稿补无透视正侧背和同源派生；前探拳的透视放大不作为左右拳实际尺寸差，模型和运行分别验证。'
    if id=='M05' and (OUT/'M05-style-unification-production-r2.json').exists():
        style=json.loads((OUT/'M05-style-unification-production-r2.json').read_text())
        assert sha(OUT/style['file'])==style['sha256'], 'King style sample changed'
        for ref in style['source_refs']:assert sha(OUT/ref['file'])==ref['sha256'], 'King style reference changed'
        record['previous_internal_source_candidate']=record['internal_source_candidate']
        record['internal_source_candidate']={'record':str((OUT/'M05-style-unification-production-r2.json').relative_to(PROJECT)),'file':str((OUT/style['file']).relative_to(PROJECT)),'sha256':style['sha256'],'reader':str((OUT/'M05-style-match-r2.html').relative_to(PROJECT)),'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/style['file']).relative_to(PROJECT))]+[str((OUT/ref['file']).relative_to(PROJECT)) for ref in style['source_refs']]
        record['identity_reference_status']='style_unification_sample_pending_user'
        record['current_issue']='王者R2只统一大块面、线条和分层明暗，收敛碎线/反光；藏蓝白红金、厚重全装、右钻左盾、双肩炮与层翼保持。新画法样例待看。'
        record['internal_next']='看R2画法与无牌的协调程度，再沿同一母稿固定冠片/盾徽、炮翼分组和结构视图；不把同系处理成相同配色或删装备。'
    if id=='M05' and (OUT/'M05-modular-production-r4.json').exists():
        modular=json.loads((OUT/'M05-modular-production-r4.json').read_text())
        for item in modular['items']:assert sha(OUT/item['file'])==item['sha256'], 'King modular source changed: '+item['id']
        selected=next(item for item in modular['items'] if item['id']=='FULL')
        record['previous_style_source_candidate']=record['internal_source_candidate']
        record['internal_source_candidate']={'record':str((OUT/'M05-modular-production-r4.json').relative_to(PROJECT)),'file':str((OUT/selected['file']).relative_to(PROJECT)),'sha256':selected['sha256'],'reader':str((OUT/'M05-modular-r4.html').relative_to(PROJECT)),'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_modular_source_bundle']=modular['items']
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in modular['items']]
        record['identity_reference_status']='L_harpoon_head_core_and_accessory_source_candidates_pending_user'
        record['current_issue']='用户要求图四脸、五组冠构件、对称侧瓣及中轴前伸L型倒钩；现已画头部正侧对照、素体、全装及配件分组。内侧两瓣加长；全装保留厚重与有用冗余，新稿待看。'
        record['internal_next']='按本轮实际图核头部前伸方向、素体/全装同一身体及六组配件挂点；继续统一精确数量、盾板、隐藏面和卸装状态，不从示意板自动推定模型或运行已完成。'
    if id=='M05' and (OUT/'M05-head-upward-L-production-r5.json').exists():
        head5=json.loads((OUT/'M05-head-upward-L-production-r5.json').read_text())
        assert sha(OUT/head5['file'])==head5['sha256'], 'King upward horn source changed'
        record['previous_modular_source_candidate']=record['internal_source_candidate']
        record['internal_source_candidate']={'record':str((OUT/'M05-head-upward-L-production-r5.json').relative_to(PROJECT)),'file':str((OUT/head5['file']).relative_to(PROJECT)),'sha256':head5['sha256'],'reader':str((OUT/'M05-modular-r4.html').relative_to(PROJECT))+'#head','user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_modular_source_bundle']=[dict(head5,id='HEAD')]+[dict(x,head_geometry_outdated=x['id'] in ['CORE','FULL']) for x in record['current_modular_source_bundle'] if x['id']!='HEAD']
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in record['current_modular_source_bundle']]
        record['identity_reference_status']='upward_L_head_candidate_body_horn_update_pending'
        record['current_issue']='用户纠正中角应向上刺出，类似独角仙。R5保留短前探根座，长角身上挑、主尖朝上和朝回倒钩；脸及两对侧冠保持。旧R4整机中角尚待同步。'
        record['internal_next']='先看当前朝上角的正侧结构，沿选定头部再同步素体/全装；R4两张整机仅保留颈下与配件参考，不再沿水平前刺中角派生。'
    if id=='M05' and (OUT/'M05-head-riese-production-r6.json').exists():
        head6=json.loads((OUT/'M05-head-riese-production-r6.json').read_text())
        assert sha(OUT/head6['file'])==head6['sha256'], 'King Riese-reference head source changed'
        for ref in head6['source_refs']: assert sha(OUT/ref['file'])==ref['sha256'], 'King R6 reference changed'
        record['previous_upward_L_source_candidate']=record['internal_source_candidate']
        record['internal_source_candidate']={'record':str((OUT/'M05-head-riese-production-r6.json').relative_to(PROJECT)),'file':str((OUT/head6['file']).relative_to(PROJECT)),'sha256':head6['sha256'],'reader':str((OUT/'M05-modular-r4.html').relative_to(PROJECT))+'#head','user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_modular_source_bundle']=[dict(head6,id='HEAD')]+[x for x in record['current_modular_source_bundle'] if x['id']!='HEAD']
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in record['current_modular_source_bundle']]
        record['identity_reference_status']='riese_reference_horn_candidate_body_horn_update_pending'
        record['current_issue']='R5直立箭头角被用户否定。R6实际参考古铁巨神图，改厚根上挑刀刃角与细侧天线，保留图四脸和原色；正面中轴收正，整机旧角待同步。'
        record['internal_next']='先判断当前独立头稿的造型与正侧关系，再同步素体/全装；新稿待用户看稿，不沿被否定的R5继续派生。'
    if id=='M05' and (OUT/'M05-head-design-fixed-20261020.json').exists():
        fixed6=json.loads((OUT/'M05-head-design-fixed-20261020.json').read_text())
        for ref in fixed6['files']: assert sha(OUT/ref['file'])==ref['sha256'], 'Selected King head changed'
        record['accepted_head_source']={'receipt':str((OUT/'M05-head-design-fixed-20261020.json').relative_to(PROJECT)),'file':str((OUT/fixed6['files'][0]['file']).relative_to(PROJECT)),'sha256':fixed6['files'][0]['sha256'],'user_accepted':True,'scope':'指定R6b头部源设计，仅限原图。'}
        record['current_modular_source_bundle']=[dict(x,user_accepted=True,acceptance_receipt='M05-head-design-fixed-20261020.json') if x['id']=='HEAD' else x for x in record['current_modular_source_bundle']]
    if id=='M05' and (OUT/'M05-modular-head-sync-production-r7.json').exists():
        sync7=json.loads((OUT/'M05-modular-head-sync-production-r7.json').read_text())
        for item in sync7['items']: assert sha(OUT/item['file'])==item['sha256'], 'King synchronized body changed'
        record['previous_head_source_candidate']=record['internal_source_candidate']
        selected=next(x for x in sync7['items'] if x['id']=='FULL')
        record['internal_source_candidate']={'record':str((OUT/'M05-modular-head-sync-production-r7.json').relative_to(PROJECT)),'file':str((OUT/selected['file']).relative_to(PROJECT)),'sha256':selected['sha256'],'reader':str((OUT/'M05-modular-r4.html').relative_to(PROJECT))+'#chassis','user_accepted':bool(selected.get('user_accepted')),'runtime_integrated':False,'handoff_sent':False}
        record['current_modular_source_bundle']=[x for x in record['current_modular_source_bundle'] if x['id'] not in ['CORE','FULL']]+sync7['items']
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in record['current_modular_source_bundle']]
        record['identity_reference_status']='R6b_head_user_accepted_R7_body_source_candidates'
        record['current_issue']='用户指定采用R6b头部原图，CML134固定该源设计；已将同一头型合回R7素体与全装，保留颈下与配件。整机合回结果仍分开判断。'
        record['internal_next']='沿已选头型继续统一多视、隐藏根位、素体/配件接口与装卸状态；不重选头型，不扩大为模型/运行认可。'
    if id=='M05' and (OUT/'M05-battle-mask-production-r8.json').exists():
        mask8=json.loads((OUT/'M05-battle-mask-production-r8.json').read_text())
        assert sha(OUT/mask8['file'])==mask8['sha256'], 'Selected King mask changed'
        record['accepted_mask_source']={'record':str((OUT/'M05-battle-mask-production-r8.json').relative_to(PROJECT)),'file':str((OUT/mask8['file']).relative_to(PROJECT)),'sha256':mask8['sha256'],'user_accepted':True,'scope':'R8战斗面罩源图；转换示意与新增红鳍另记。'}
        record['accepted_body_sources']=[x for x in record['current_modular_source_bundle'] if x['id'] in ['CORE','FULL'] and x.get('user_accepted')]
    if id=='M05' and (OUT/'M05-red-fin-production-r9.json').exists():
        fin9=json.loads((OUT/'M05-red-fin-production-r9.json').read_text())
        for item in fin9['items']+fin9['source_refs']: assert sha(OUT/item['file'])==item['sha256'], 'King red-fin source changed'
        current={x['id']:x for x in fin9['items']}
        record['previous_body_source']=record['internal_source_candidate']
        record['internal_source_candidate']={'record':str((OUT/'M05-red-fin-production-r9.json').relative_to(PROJECT)),'file':str((OUT/current['MASK']['file']).relative_to(PROJECT)),'sha256':current['MASK']['sha256'],'reader':str((OUT/'M05-battle-mask-r8.html').relative_to(PROJECT)),'user_accepted':bool(fin9.get('user_accepted')),'runtime_integrated':False,'handoff_sent':False}
        record['current_modular_source_bundle']=[dict(x,helmet_extension_pending=x['id'] in ['CORE','FULL']) for x in record['current_modular_source_bundle'] if x['id']!='HEAD']+[dict(current['NORMAL'],id='HEAD'),dict(current['MASK'],id='BATTLE_HEAD')]
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in record['current_modular_source_bundle']]
        record['identity_reference_status']='R7_and_R8_sources_accepted_R9_red_fin_dual_state_candidates'
        record['current_issue']='R7源设计与R8战斗面罩已采用；最新按用户标注加头顶中线红鳍，正面由金色中角遮住、侧面展开鳍面。普通／战斗两状态共用同一头盔；R9新增图仍供看稿。'
        record['internal_next']='沿双状态头稿固定红鳍隐面和面罩收纳/轨迹，再合回整机；转换局部板不代替模型与动画，R7源稿尚未合入红鳍与闭合面罩。'
    if id=='M05' and (OUT/'M05-turnaround-production-r12.json').exists():
        tri11=json.loads((OUT/'M05-turnaround-production-r12.json').read_text())
        for item in tri11['items']+tri11['source_refs']: assert sha(OUT/item['file'])==item['sha256'], 'King turnaround source changed'
        current_front=next(x for x in tri11['items'] if x['id']=='FULL_FRONT')
        record['accepted_red_fin_dual_head_sources']=fin9['items']
        record['current_turnaround_source_bundle']=tri11['items']
        record['internal_source_candidate']={'record':str((OUT/'M05-turnaround-production-r12.json').relative_to(PROJECT)),'file':str((OUT/current_front['file']).relative_to(PROJECT)),'sha256':current_front['sha256'],'reader':str((OUT/'M05-turnaround-r12.html').relative_to(PROJECT)),'user_accepted':bool(current_front.get('user_accepted')),'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in tri11['items']]
        record['identity_reference_status']='R7_R8_R9_source_designs_accepted_R11_turnaround_drawings_candidate'
        record['current_issue']='R9红鳍双状态源设计已采用。R11恢复完整大腿与长胫甲；R12按实际正侧稿重排背视右肘/钻轴，并加中央喷口和双燃料罐。'
        record['internal_next']='继续沿R11逐面核对结构与接口；新三视稿不自动成为同模型投影、活动让位或运行验收。'
        record['turnaround_proportion_feedback']='这又将机体做矮了'
        if tri11.get('new_turnaround_images_user_accepted'):
            record['identity_reference_status']='M05_R12_selected_source_designs_user_accepted'
            record['source_acceptance_receipt']=tri11['user_acceptance']['receipt']
            record['current_issue']='2026-10-21用户认可当前素体/全装三视与双状态头部7张源设计；长腿、前向右钻、中央主喷口与双罐以所选图和哈希为准。'
            record['internal_next']='沿已认可当前源稿制作同模型、关节/面罩运动与运行资产；各工序分别检查，不回流旧矮身形或后向钻头。'
    if id=='M02' and (OUT/'M02-turnaround-production-r2.json').exists():
        boxer2=json.loads((OUT/'M02-turnaround-production-r2.json').read_text())
        for item in boxer2['items']+[boxer2['parent']]: assert sha(OUT/item['file'])==item['sha256'], 'Old Boxer source changed'
        current_front=next(x for x in boxer2['items'] if x['id']=='FRONT')
        record['previous_M02_source']=record['internal_source_candidate']
        record['current_turnaround_source_bundle']=boxer2['items']
        record['internal_source_candidate']={'record':str((OUT/'M02-turnaround-production-r2.json').relative_to(PROJECT)),'file':str((OUT/current_front['file']).relative_to(PROJECT)),'sha256':current_front['sha256'],'reader':str((OUT/'M02-turnaround-r2.html').relative_to(PROJECT)),'user_accepted':bool(current_front.get('user_accepted')),'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in boxer2['items']]
        record['identity_reference_status']='M02_R1_direction_usable_R2_turnaround_drawings_candidate'
        record['current_issue']='旧拳王沿现有方向补正侧背：象牙白/土棕/深红、厚肩红拳套、正常头部体积与替换装甲左右保留。新图尚未自动认可。'
        record['internal_next']='据同一组源稿继续收敛隐面、关节与拳套结构，再制作动作/模型；不把三视绘制当成运行验收。'
        if boxer2.get('new_images_user_accepted'):
            record['identity_reference_status']='M02_R2_selected_source_designs_user_accepted'
            record['source_acceptance_receipt']=boxer2['user_acceptance']['receipt']
            record['current_issue']='2026-10-21用户认可当前正面、R2b修正左侧面与背面3张源设计；厚肩红拳套、正常头壳和左右修补甲以所选图为准。'
            record['internal_next']='沿已认可当前源稿继续模型和拳击动作；本次源设计认可不扩大为同模型正交或运行验收。'
    if id=='M11' and (OUT/'M11-cargo-production-r1.json').exists():
        cargo=json.loads((OUT/'M11-cargo-production-r1.json').read_text())
        for item in cargo['items']: assert sha(OUT/item['file'])==item['sha256'], 'Cargo source changed'
        for item in cargo['source_refs']: assert sha(PROJECT/item['file'])==item['sha256'], 'Cargo reference changed'
        current_front=next(x for x in cargo['items'] if x['id']=='FRONT')
        record['internal_source_candidate']={'record':str((OUT/'M11-cargo-production-r1.json').relative_to(PROJECT)),'file':str((OUT/current_front['file']).relative_to(PROJECT)),'sha256':current_front['sha256'],'reader':str((OUT/'M11-cargo-r1.html').relative_to(PROJECT)),'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['current_turnaround_source_bundle']=cargo['items']
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in cargo['items']]
        record['identity_reference_status']='CML028_head_preserved_M11_new_source_candidates'
        record['current_issue']='已沿v4头脸画出机器人正侧背及四轴货车；每侧肩后/前臂/小腿双轮共四轮位，货柜保持独立。背面轮轴视向与侧面斜角已局部修正，新图供本轮看稿。'
        record['internal_next']='先审当前双形态与部件对应，再沿所选稿制作同模型转轴/连续变形与关联事件图；不把部件表当作变形验证。'
    if id=='M11' and (OUT/'M11-future-production-r2.json').exists():
        future=json.loads((OUT/'M11-future-production-r2.json').read_text())
        for item in future['items']: assert sha(OUT/item['file'])==item['sha256'], 'Future cargo output changed'
        for item in future['source_refs']: assert sha((PROJECT if item.get('path_base')=='project_root' else OUT)/item['file'])==item['sha256'], 'Future cargo input changed'
        current_robot=next(x for x in future['items'] if x['id']=='ROBOT')
        record['historical_R1_source_bundle']=record.get('current_turnaround_source_bundle',[])
        record['current_turnaround_source_bundle']=[]
        record['current_dual_form_source_bundle']=future['items']
        record['internal_source_candidate']={'record':str((OUT/'M11-future-production-r2.json').relative_to(PROJECT)),'file':str((OUT/current_robot['file']).relative_to(PROJECT)),'sha256':current_robot['sha256'],'reader':str((OUT/'M11-future-r2.html').relative_to(PROJECT)),'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in future['items']]
        record['identity_reference_status']='CML137_future_vehicle_no_horizontal_antenna_direction_authorized_R2_candidates'
        record['turnaround_status']='R2车形/人形母稿/头部近景已画；R1侧背是历史，不作为R2当前几何。'
        record['current_issue']='用户要求参考Tesla货车更未来、人形对应变化、保留领袖投射但拉开具体头脸并取消水平天线。R2已改大弧面风挡、平滑前罩/导流肩壳和内嵌通讯块，三张新稿待看。'
        record['internal_next']='先审R2车形、人形与头部；沿选定造型补侧背、转轴/净空与连续变形，不把旧横天线或柴油方头稿回流。'
    if id=='M11' and (OUT/'M11-structure-and-head-production-r4.json').exists():
        current_name=next(name for name in ['M11-turnaround-delivery-production-r9.json','M11-turnaround-structure-production-r7.json','M11-heroic-antenna-production-r5.json','M11-structure-and-head-production-r4.json'] if (OUT/name).exists())
        current=json.loads((OUT/current_name).read_text())
        for item in current['items']: assert sha(OUT/item['file'])==item['sha256'], 'M11 current source changed'
        head=next((x for x in current['items'] if x['id']=='FRONT'),current['items'][0])
        record['historical_R2_source_bundle']=record.get('current_dual_form_source_bundle',[])
        record['current_dual_form_source_bundle']=current['items']+([current['vehicle_context']] if current.get('vehicle_context') and not any(x['id']=='VEHICLE' for x in current['items']) else [])
        record['current_body_context_source']=current['body_context']
        record['current_layout_study']=current['layout_study']
        record['internal_source_candidate']={'record':str((OUT/current_name).relative_to(PROJECT)),'file':str((OUT/head['file']).relative_to(PROJECT)),'sha256':head['sha256'],'reader':str((OUT/current['reader']).relative_to(PROJECT)),'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in record['current_dual_form_source_bundle']]+[str((OUT/current['layout_study']['record']).relative_to(PROJECT))]
        record['identity_reference_status']='CML137_integrated_helmet_camera_rearview_direction_current_drawings_candidate'
        record['turnaround_status']='整体盔型两案各有正面/斜视；非同模型正交。R2整机仅颈下参考，R1侧背历史。'
        record['current_issue']='按最新头盔参考重组额框、侧盔与护颊，撤掉独立顶鳍；车形改摄像头后视。同件刚体布局补部件去向，支撑与净空未成立，新稿待看。'
        record['internal_next']='沿所选整体盔型统一整机和隐面；对齐车壳、头部收纳、全程净空及支撑，再制作详细多视和变形。'
        if current_name=='M11-heroic-antenna-production-r5.json':
            record['identity_reference_status']='CML137_visible_antennas_positive_hero_direction_R5_head_candidate'
            record['turnaround_status']='R5同一头部正面与斜视候选；不是同模型正交。R4两案已被用户否定，R2整机只作颈下参考。'
            record['current_issue']='用户明确天线必须保留且不必尖，反对眼镜蛇宽罩与反派神态；R5补明确耳侧钝头天线、收窄侧盔、简化面甲并局部放平眼眉。新稿未采用。'
            record['internal_next']='先沿明确可见天线与可靠正面角色神态收敛头部，再统一整机/隐面和实际收纳；R4无天线宽冠不回流。'
        if current_name in ['M11-turnaround-structure-production-r7.json','M11-turnaround-delivery-production-r9.json']:
            record['current_turnaround_source_bundle']=[x for x in current['items'] if x['id'] in ['FRONT','SIDE','REAR']]
            record['head_source_acceptance']=current['selected_head_reference']
            record['identity_reference_status']='M11_exact_eac75eab_head_user_selected_R7_turnaround_structure_drawings_candidate'
            record['turnaround_status']='人形正侧背、车形三视、颏甲与结构板已画；不是同精细模型正交或运行认可。'
            record['current_issue']='用户指定原眼形头稿和比例，身体按R2长腿尺度；R7补勇者颏甲、双形态三视、头仓与轮架/腿架/货台结构。头仓同件包络已核对，整机受力仍未验证。'
            record['internal_next']='沿指定原头与当前源稿继续精细分件模型和三视对齐；校核整机收纳、驾驶空间、轮架扫掠与支撑，不以局部草模代替全机验证。'
        if current_name=='M11-turnaround-delivery-production-r9.json':
            record['approved_design_master']=current['approved_master']
            record['source_acceptance_receipt']=current['user_acceptance_receipt']
            record['source_delivery_manifest']='M11-delivery-manifest-r9.json'
            record['source_delivery_ready']=True
            record['identity_reference_status']='M11_R8_master_user_selected_R9_authorized_source_delivery'
            record['current_turnaround_alignment']='R9_source_views_corrected_to_R8_master'
            record['current_issue']='货柜领袖R8整体形象已确定，R9正侧背已按露颈沉肩和原背架体量修正并整理源设计交付。'
            record['internal_next']='沿确定母稿与三视进入模型工序；精细结构、连续变形和运行另验。源设计会话接续下一批。'
    if id=='M11' and (OUT/'M11-posture-production-r8.json').exists() and not (OUT/'M11-turnaround-delivery-production-r9.json').exists():
        posture=json.loads((OUT/'M11-posture-production-r8.json').read_text())
        item=posture['items'][0]
        assert sha(OUT/item['file'])==item['sha256'], 'M11 posture source changed'
        record['previous_R7_turnaround_source_bundle']=record.get('current_turnaround_source_bundle',[])
        record['current_turnaround_alignment']='requires_R8_posture_alignment'
        record['current_layout_study']={**record['current_layout_study'],'R8_posture_applicability':'prior_R7_head_bay_only; new_neck_stroke_and_shoulder_clearance_not_checked'}
        record['current_posture_candidate']=item
        record['preferred_whole_body_basis']=posture['preferred_visual_basis']
        record['internal_source_candidate']={'record':str((OUT/'M11-posture-production-r8.json').relative_to(PROJECT)),'file':str((OUT/item['file']).relative_to(PROJECT)),'sha256':item['sha256'],'reader':str((OUT/'M11-turnaround-structure-r7.html').relative_to(PROJECT))+'#posture-r8','user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs'].append(str((OUT/item['file']).relative_to(PROJECT)))
        record['identity_reference_status']='M11_selected_head_preferred_f27_state_R8_posture_candidate'
        record['current_issue']='用户肯定f27斜侧稿状态后指出缩脖子；R8沿此基底协调颈部、肩线和胸甲上沿，保留厚重体量、原头和长腿。'
        record['internal_next']='沿R8体态同步正侧背及颈部展开/肩架/胸甲活动结构；旧三视和头仓不自动获得新体态适用结论。'
    if id in ['M08','F07','M14','F08'] and (OUT/'aircraft-source-batch-20261022.json').exists():
        aircraft=json.loads((OUT/'aircraft-source-batch-20261022.json').read_text())
        owner='M08' if id in ['M08','F07'] else 'M14'
        item=next(x for x in aircraft['items'] if x['id']==owner)
        assert sha(OUT/item['file'])==item['sha256'], 'Aircraft candidate changed'
        record['internal_source_candidate']={'record':str((OUT/'aircraft-source-batch-20261022.json').relative_to(PROJECT)),'file':str((OUT/item['file']).relative_to(PROJECT)),'sha256':item['sha256'],'reader':str((OUT/aircraft['reader']).relative_to(PROJECT))+'#'+owner,'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT))]
        record['current_dual_form_source_bundle']=[item]
        record['identity_reference_status']='aircraft_dual_form_source_candidate_existing_working_reference_preserved'
        record['current_issue']='已接续下一批，完成同一机体人形/航空态候选，检查座舱、翼根、喷口和挂点；雷翎枪口朝向已修。具体新图未采用。'
        record['internal_next']='沿候选收敛隐面和三视，补一个可信折叠中间态，再制作同件模型；双态图不代表连续变形成立。'
    if id in ['M08','F07','M14','F08'] and (OUT/'aircraft-runtime-comparison-20261022.json').exists():
        comparison=json.loads((OUT/'aircraft-runtime-comparison-20261022.json').read_text())
        owner='M08' if id in ['M08','F07'] else 'M14'
        finding=comparison['findings'][owner]
        model=next(x for x in comparison['runtime_models'] if x['id']==finding['runtime_id'] and x['aircraft']==id.startswith('F'))
        assert sha(PROJECT/model['project_model'])==model['model_sha256'], 'Current aircraft model changed'
        record['historical_redesign_candidate']=record.pop('internal_source_candidate',None)
        record['historical_structure_study_bundle']=record.pop('current_dual_form_source_bundle',[])
        record['current_runtime_design_reference']={'file':model['project_model'],'sha256':model['model_sha256'],'capture':str((OUT/model['capture_file']).relative_to(PROJECT)),'reader':str((OUT/comparison['reader']).relative_to(PROJECT))+'#'+owner,'kind':'existing_runtime_model_unmodified_diagnostic_capture','user_accepted_as_new_design':False}
        record['production_refs']=[model['project_model'],str((OUT/model['capture_file']).relative_to(PROJECT)),str((OUT/'aircraft-runtime-comparison-20261022.json').relative_to(PROJECT))]
        record['identity_reference_status']='retain_current_runtime_design_pending_palette_material_comparison'
        record['current_issue']='现用Demo机设已实际取图比较，轮廓与识别点比新稿更明确；新稿保留作结构研究，不推荐替换整机。两机来自不同IP谱系，共享本作画法。'
        record['internal_next']='保留现用头胸、翼形、比例、模型与骨架，先比较同构图配色和有限材质清理；本轮未制作换色样本、未改运行资产。'
    if id in ['M08','F07','M14','F08'] and (OUT/'aircraft-existing-design-recolour-production-r2.json').exists():
        colour=json.loads((OUT/'aircraft-existing-design-recolour-production-r2.json').read_text())
        owner='M08' if id in ['M08','F07'] else 'M14'
        item=next(x for x in colour['items'] if x['id']==owner)
        assert sha(OUT/item['file'])==item['sha256'], 'Aircraft colour source changed'
        record['current_colour_style_candidate']={'record':str((OUT/'aircraft-existing-design-recolour-production-r2.json').relative_to(PROJECT)),'file':str((OUT/item['file']).relative_to(PROJECT)),'sha256':item['sha256'],'reader':str((OUT/colour['reader']).relative_to(PROJECT))+'#'+owner,'scope':item['scope'],'user_accepted':False,'runtime_integrated':False}
        record['production_refs'].insert(0,str((OUT/item['file']).relative_to(PROJECT)))
        record['identity_reference_status']='existing_runtime_identity_with_candidate_colour_style_source'
        record['retained']='保留现用雷翎窄长头、黄胸核、放射刃翼与宽胫尖足；航空态保留层叠翼与推进器群。' if owner=='M08' else '保留现用歌翼长双红角、黄胸核、肩翼/垂翼甲与长腿；航空态保留红白机身与原翼尾。'
        record['current_issue']='现用机设仍为造型依据；已沿其重绘双形态配色与表面修订稿，进一步清理旧亮裂纹。新图为色样，未替换原模型。'
        record['internal_next']='先核对源稿的识别点、色块和材质画法；同模型材质、正常战棋镜头和派生三视仍分别核对，不沿上一轮蓝紫/粉白候选另造机体。'
    if id in ['M08','F07','M14','F08'] and (OUT/'aircraft-synthesis-production-r3.json').exists():
        synthesis=json.loads((OUT/'aircraft-synthesis-production-r3.json').read_text())
        owner='M08' if id in ['M08','F07'] else 'M14'
        item=next(x for x in synthesis['items'] if x['id']==owner)
        assert sha(OUT/item['file'])==item['sha256'], 'Aircraft synthesis source changed'
        record['historical_colour_style_candidate']=record.pop('current_colour_style_candidate',None)
        record['current_synthesis_candidate']={'record':str((OUT/'aircraft-synthesis-production-r3.json').relative_to(PROJECT)),'file':str((OUT/item['file']).relative_to(PROJECT)),'sha256':item['sha256'],'reader':str((OUT/synthesis['reader']).relative_to(PROJECT))+'#'+owner,'scope':item['role'],'user_accepted':False,'runtime_integrated':False}
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)),str((OUT/'aircraft-synthesis-production-r3.json').relative_to(PROJECT))]+[r['file'] for r in item['source_refs']]
        record['identity_reference_status']='story_ip_led_synthesis_candidate_r3_not_whole_model_recolour'
        record['retained']='现用红白蓝与刃翼节奏、前建议稿航空关节/座舱胸；实际采用用户参考启发的V形侧天线。' if owner=='M08' else '现用白红/修长身形/翼展、前建议稿座舱与航空结构，重画头盔和翼甲；按护航/保护歌声取舍。'
        record['current_issue']='R2整体回退路线被用户否定；R3已将新头、航空结构与既有识别点综合，并提供同页头部近景。'
        record['internal_next']='沿R3候选实看并收敛头/翼/配件与三视；歌翼附加挂舱仍需背视与腿部映射，不把提示词或生成图当作完整变形证明。'
    if id in ['M14','F08'] and (OUT/'M14-music-support-production-r4.json').exists():
        music=json.loads((OUT/'M14-music-support-production-r4.json').read_text())
        item=music['item']
        assert sha(OUT/item['file'])==item['sha256'], 'Songwing music source changed'
        record['current_music_module_candidate']={'record':str((OUT/'M14-music-support-production-r4.json').relative_to(PROJECT)),'file':str((OUT/item['file']).relative_to(PROJECT)),'sha256':item['sha256'],'reader':str((OUT/music['reader']).relative_to(PROJECT)),'scope':'folding music-broadcast equipment on R3 base','user_accepted':bool(item.get('user_accepted')),'runtime_integrated':False}
        record['production_refs'].insert(0,str((OUT/item['file']).relative_to(PROJECT)))
        record['current_issue']='R3方向获用户正面反馈后，沿主体补可收拢肩后声传播翼；现有角色表仍为隼真驾驶、莉歌歌姬，未合并身份。'
        record['internal_next']='核对声翼展开/闭合/航空收纳与翼根净空，保留R3头型和主体；同件模型、广播规则和实听另行验证。'
    if id in ['M14','F08'] and (OUT/'M14-design-fixed-20261022.json').exists():
        accepted= json.loads((OUT/'M14-design-fixed-20261022.json').read_text())
        record['selected_source_master']={'record':str((OUT/'M14-design-fixed-20261022.json').relative_to(PROJECT)),'file':str((OUT/accepted['selected_master']['file']).relative_to(PROJECT)),'sha256':accepted['selected_master']['sha256'],'user_accepted':True,'scope':accepted['acceptance_scope']}
        record['identity_reference_status']='M14_R4_exact_music_source_user_accepted_new_turnaround_drawings_separate'
        record['current_issue']='用户以“这版可以。出具三视图”采用歌翼R4源设计，保持原头型、长腿和双声翼；新三视按授权派生。'
    if id=='M14' and (OUT/'M14-turnaround-production-r5.json').exists():
        turnaround=json.loads((OUT/'M14-turnaround-production-r5.json').read_text())
        for item in turnaround['items']:assert sha(OUT/item['file'])==item['sha256'], 'Songwing view changed'
        record['current_turnaround_source_bundle']=turnaround['items']
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in turnaround['items']]+[str((OUT/turnaround['selected_master']['file']).relative_to(PROJECT))]
        record['internal_next']='沿已采用R4主形使用R5正面/修正侧背三视，统一声翼朝向；源图隐面细节、模型与运行分别验证。'
    if id=='M08' and (OUT/'M08-turnaround-production-r4.json').exists():
        turnaround=json.loads((OUT/'M08-turnaround-production-r4.json').read_text())
        for item in turnaround['items']:assert sha(OUT/item['file'])==item['sha256'], 'Leiling view changed'
        record['current_turnaround_source_bundle']=turnaround['items']
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in turnaround['items']]+[str((OUT/turnaround['selected_master']['file']).relative_to(PROJECT))]
        record['current_issue']='按用户追问，沿R3综合方向补齐正面、修正左侧面与背面；长枪保持右手，背部肩壳/脊柱/骨盆按后视重画。'
        record['internal_next']='使用当前R4三视与R3母稿继续同件模型核对；隐面几何、完整变形、模型和运行分别验证。'
        record['identity_reference_status']='M08_R3_direction_R4_requested_turnaround_source_delivery'
    if id=='M08' and (OUT/'M08-turnaround-production-r5.json').exists():
        turnaround=json.loads((OUT/'M08-turnaround-production-r5.json').read_text())
        for item in turnaround['items']:assert sha(OUT/item['file'])==item['sha256'], 'Leiling R5 view changed'
        record['historical_rejected_proportion_turnaround']=record.get('current_turnaround_source_bundle',[])
        record['current_turnaround_source_bundle']=turnaround['items']
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in turnaround['items']]+[str((OUT/turnaround['selected_master']['file']).relative_to(PROJECT))]
        record['current_issue']='用户指出R4三视做矮失去秀气感；R5回到R3比例，收窄肩胸和四肢、提高髋线，重修正面并同步侧背。'
        record['internal_next']='以R5修长三视和R3原稿继续核对；R4身形退出当前依据，新源图与模型/运行分别验证。'
        record['identity_reference_status']='M08_R4_proportions_rejected_R5_slender_repair_source_delivery'
    if id in ['M08','M14'] and (OUT/'aircraft-airframe-production-r6.json').exists():
        revision=json.loads((OUT/'aircraft-airframe-production-r6.json').read_text())
        machine=next(x for x in revision['items'] if x['id']==id)
        for item in machine['views']:assert sha(OUT/item['file'])==item['sha256'], 'Airframe R6 source changed'
        record['previous_turnaround_source_bundle']=record.get('current_turnaround_source_bundle',[])
        record['current_turnaround_source_bundle']=machine['views']
        record['current_airframe_surface_candidate']={'record':str((OUT/'aircraft-airframe-production-r6.json').relative_to(PROJECT)),'file':str((OUT/machine['front']['file']).relative_to(PROJECT)),'sha256':machine['front']['sha256'],'reader':str((OUT/revision['reader']).relative_to(PROJECT))+'#'+id,'user_accepted':False,'runtime_integrated':False}
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in machine['views']]+[str((OUT/'aircraft-airframe-production-r6.json').relative_to(PROJECT))]
        record['current_issue']='用户认可歌翼体态与两机主形，指出雷翎R5过瘦过长及两机线条太高达化；R6直接以歌翼比例作锚，减少装饰切面并增强进气道/蒙皮/翼根/发动机舱。'
        record['internal_next']='当前使用R6正侧背候选；歌翼R4原主形采用范围保留，新表面、隐面几何、航空态对应与模型/运行分别核对。'
        record['identity_reference_status']='established_forms_preserved_R6_airframe_surface_candidate_Songwing_proportion_anchor'
        if (OUT/'aircraft-design-fixed-20261023-r6.json').exists():
            acceptance=json.loads((OUT/'aircraft-design-fixed-20261023-r6.json').read_text())
            record['selected_airframe_source_design']=record.pop('current_airframe_surface_candidate')
            record['selected_airframe_source_design'].update(user_accepted=True,acceptance_record=str((OUT/'aircraft-design-fixed-20261023-r6.json').relative_to(PROJECT)),scope=acceptance['scope'])
            record['identity_reference_status']='R6_current_source_views_user_accepted'
            record['current_issue']='用户已确定当前R6源设计，授权交付主对话并进行下一批；此前两轮比例反例不回流。'
            record['internal_next']='沿当前已确定三视进入分件/模型/材质制作，具体航空对应、完整变形与运行分别验证。'
    if id in ['M06','M07'] and (OUT/'public-works-source-production-r1.json').exists():
        works=json.loads((OUT/'public-works-source-production-r1.json').read_text())
        item=next(x for x in works['items'] if x['id']==id)
        assert sha(OUT/item['file'])==item['sha256'], 'Public works source changed'
        record['internal_source_candidate']={'record':str((OUT/'public-works-source-production-r1.json').relative_to(PROJECT)),'file':str((OUT/item['file']).relative_to(PROJECT)),'sha256':item['sha256'],'reader':str((OUT/works['reader']).relative_to(PROJECT))+'#'+id,'user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT))]+[str((OUT/ref['file']).relative_to(PROJECT)) for ref in item['source_refs']]
        record['current_issue']='沿原有职业机造型完成首轮源板，分别细化维修工具/替换件与吊装/稳定/收拢结构；局部修正箱内配件与收拢钩，具体新稿仍为候选。'
        record['internal_next']='实际对照当前源板收敛主形，随后补多视与工作动作/模型；当前源图不直接替换主工程。'
        record['identity_reference_status']='existing_identity_retained_public_works_R1_source_candidate'
    if id=='M06' and (OUT/'M06-labor-identity-production-r2.json').exists():
        current=json.loads((OUT/'M06-labor-identity-production-r2.json').read_text())
        item=current['items'][0]
        assert sha(OUT/item['file'])==item['sha256'], 'M06 labor identity source changed'
        record['previous_internal_source_candidate']=record.get('internal_source_candidate')
        record['internal_source_candidate']={'record':str((OUT/'M06-labor-identity-production-r2.json').relative_to(PROJECT)),'file':str((OUT/item['file']).relative_to(PROJECT)),'sha256':item['sha256'],'reader':str((OUT/current['reader']).relative_to(PROJECT))+'#M06','user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT))]+[str((OUT/ref['file']).relative_to(PROJECT)) for ref in item['source_refs']]
        record['current_issue']='用户指出R1头部丑、机设缺少特色；R2按Patlabor城市职业机与已接受C03三代旧电路供能行动，重画护盔/检修躯体/卷盘适配背架与救援夹具。'
        record['internal_next']='先收敛R2整机及A/B/C头部，之后补同形多视；新图待采用，未新增玩法或替换主模型。'
        record['identity_reference_status']='Patlabor_occupational_and_story_power_supply_led_M06_R2_candidate'
        if (OUT/'M06-design-fixed-20261023-r2.json').exists():
            receipt=json.loads((OUT/'M06-design-fixed-20261023-r2.json').read_text())
            assert item['sha256']==receipt['selected_master']['sha256'], 'Selected M06 source changed'
            record['internal_source_candidate'].update(user_accepted=True,selected_head='A',acceptance_receipt=str((OUT/'M06-design-fixed-20261023-r2.json').relative_to(PROJECT)),acceptance_scope=receipt['scope'])
            record['selected_source_master']=record['internal_source_candidate'].copy()
            record['identity_reference_status']='M06_R2_main_and_A_head_source_user_accepted'
            record['current_issue']='用户已采用R2整机与A作业盔头型；B/C保留未采用研究，头部通讯模块透视侧别在后续同头三视统一。'
            record['internal_next']='沿已采用A头型与R2整机派生正侧背，统一通讯侧别；机构、模型和运行另验。'
    if id=='M06' and (OUT/'M06-turnaround-production-r3.json').exists():
        current=json.loads((OUT/'M06-turnaround-production-r3.json').read_text())
        for item in current['items']:assert sha(OUT/item['file'])==item['sha256'], 'M06 turnaround source changed'
        record['current_turnaround_source_bundle']=current['items']
        record['current_turnaround_source_record']=str((OUT/'M06-turnaround-production-r3.json').relative_to(PROJECT))
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT)) for item in current['items']]+[str((OUT/current['parent']['file']).relative_to(PROJECT))]
        record['current_issue']='已沿确定R2整机/A头型完成独立正面、修正左侧面和背面；统一右耳通讯、左腿替换件、左手夹具与供能背架。'
        record['internal_next']='使用本轮三视和已定母稿继续分件/模型核对；新源图派生与同件模型、机构/动作/运行分别验。'
    if id=='M06' and (OUT/'M06-turnaround-design-fixed-20261023-r3.json').exists():
        accepted=json.loads((OUT/'M06-turnaround-design-fixed-20261023-r3.json').read_text())
        for item in accepted['files']:assert sha(OUT/item['file'])==item['sha256'], 'Accepted M06 source view changed'
        record['selected_turnaround_source_design']={'record':str((OUT/'M06-turnaround-design-fixed-20261023-r3.json').relative_to(PROJECT)),'files':accepted['files'],'user_accepted':True,'scope':accepted['scope']}
        record['identity_reference_status']='M06_R3_current_source_views_user_accepted'
        record['current_issue']='用户以“没问题，下一批”采用当前正R3/侧R3c/背R3三张源图，R2/A主形父源保持；早期斜侧与B/C不回流。'
        record['internal_next']='沿已确定当前三视进入分件/模型与工作动作；机构和运行另验。'
    if id in ['M09','M10'] and (OUT/'city-response-source-production-r2.json').exists():
        current=json.loads((OUT/'city-response-source-production-r2.json').read_text())
        item=next(x for x in current['items'] if x['id']==id)
        assert sha(OUT/item['file'])==item['sha256'], 'City response source changed'
        record['internal_source_candidate']={'record':str((OUT/'city-response-source-production-r2.json').relative_to(PROJECT)),'file':str((OUT/item['file']).relative_to(PROJECT)),'sha256':item['sha256'],'reader':str((OUT/current['reader']).relative_to(PROJECT))+'#'+id,'user_accepted':item.get('user_accepted',False),'runtime_integrated':False,'handoff_sent':False}
        record['production_refs']=[str((OUT/item['file']).relative_to(PROJECT))]+[str((OUT/ref['file']).relative_to(PROJECT)) for ref in current['source_refs'] if ref.get('id')==id]
        record['current_issue']='用户肯定头部/配色与总体方向，要求减少机动步兵感；R2保持上述局部，肩胸前臂/胫甲改连续曲面，六墙保留。' if id=='M09' else '用户否定四足背桥主形；R2按工程类变形金刚重画正常双足人形/消防架桥载具，四支腿用于车辆作业支撑。'
        record['internal_next']='按当前具体新稿收敛；用户采用后直接补正侧背，不只登记后停。模型、机构、动作和运行另验。'
        record['identity_reference_status']='M09_head_palette_preserved_curved_Labor_shell_candidate' if id=='M09' else 'M10_user_requested_engineering_transformer_biped_vehicle_candidate'
    if id in ['M09','M10'] and (OUT/'city-response-design-fixed-20261023-r2.json').exists():
        accepted=json.loads((OUT/'city-response-design-fixed-20261023-r2.json').read_text())
        item=next(x for x in accepted['files'] if x['id']==id)
        assert sha(OUT/item['file'])==item['sha256'], 'Accepted city response parent changed'
        record['selected_source_design']={'record':str((OUT/'city-response-design-fixed-20261023-r2.json').relative_to(PROJECT)),**item,'user_accepted':True}
        record['identity_reference_status']=id+'_R2_master_user_accepted'
        record['internal_next']='沿已确定父源直接补齐并核对正侧背；模型、机构、动作和运行另验。'
    if id in ['M09','M10'] and (OUT/'city-response-turnaround-production-r3.json').exists():
        current=json.loads((OUT/'city-response-turnaround-production-r3.json').read_text())
        machine=next(x for x in current['items'] if x['id']==id)
        for item in machine['views']:assert sha(OUT/item['file'])==item['sha256'], 'City response view changed'
        record['current_turnaround_source_bundle']=machine['views']
        record['current_turnaround_source_record']=str((OUT/'city-response-turnaround-production-r3.json').relative_to(PROJECT))
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in machine['views']]+[str((OUT/machine['parent']['file']).relative_to(PROJECT))]
        record['current_issue']='沿用户确定R2父源完成正侧背源图，保留头部、配色与成人比例；装备数量、侧别和后部结构按本轮实际查看记录核对。'
        record['internal_next']='使用当前三视与已定父源继续分件/模型核对，二维派生不代替同件机构、工作动作和运行。'
    if id in ['M09','M10'] and (OUT/'city-response-refinement-production-r4.json').exists():
        current=json.loads((OUT/'city-response-refinement-production-r4.json').read_text())
        machine=next(x for x in current['items'] if x['id']==id)
        for item in machine['views']+machine['extras']:assert sha(OUT/item['file'])==item['sha256'], 'City R4 source changed'
        record['current_turnaround_source_bundle']=machine['views']
        record['current_turnaround_source_record']=str((OUT/'city-response-refinement-production-r4.json').relative_to(PROJECT))
        record['current_supplementary_source_bundle']=machine['extras']
        record['production_refs']=[str((OUT/x['file']).relative_to(PROJECT)) for x in machine['extras']+machine['views']]+[str((OUT/machine['parent']['file']).relative_to(PROJECT))]
        record['current_issue']='用户指出R3正面矮胖且头型错；R4从指定母稿重推正面，局部等比缩头/收肩并同步侧背，新增图仍待看稿。' if id=='M09' else '用户表示消防人形问题不大，本轮保持三张人形原图；新增载具三视与六步变形/作业设计图，机构净空与承重另验。'
        record['internal_next']='按R4源图与已定R2父源继续分件核对；新派生用户认可、同件机构、连续动作与运行分别判断。'
        if id=='M09':record['subsequent_rejected_derivative']={'file':'samples/M09-front-r3b.png','feedback':'city-response-user-correction-20261024-r4.json','reason':'用户指出矮胖且头型偏离指定母稿'}
    if id in ['M09','M10'] and (OUT/'city-response-main-handoff-20261024.json').exists():
        handoff=json.loads((OUT/'city-response-main-handoff-20261024.json').read_text())
        record['current_source_handoff']={'record':str((OUT/'city-response-main-handoff-20261024.json').relative_to(PROJECT)),'sent':handoff.get('sent',False),'receiver':handoff['recipient'],'receiver_acknowledged':handoff.get('receiver_acknowledged',False),'receiver_runtime_integration_confirmed':False}
    if id in ['M07','M12'] and (OUT/'crane-mirror-source-production-r1.json').exists():
        current=json.loads((OUT/'crane-mirror-source-production-r1.json').read_text())
        machine=next(x for x in current['items'] if x['id']==id)
        for v in machine['views']:assert sha(OUT/v['file'])==v['sha256'], 'Crane/mirror source changed'
        if id=='M07':
            record['current_turnaround_source_bundle']=machine['views']
            record['current_turnaround_source_record']=str((OUT/'crane-mirror-source-production-r1.json').relative_to(PROJECT))
            record['current_issue']='沿既有R1b主形补收拢行驶态正侧背；前视吊臂轴线已局部收正，驾驶舱/卷盘侧别、配重与钩架按本轮源图对应。'
            record['internal_next']='当前多视为二维派生源图，吊索/吊臂/稳定腿机构、精确同件投影与实际作业另验。'
            record['identity_reference_status']='existing_M07_master_R2_stowed_views_candidate'
        else:
            record['internal_source_candidate']={'record':str((OUT/'crane-mirror-source-production-r1.json').relative_to(PROJECT)),'file':str((OUT/machine['file']).relative_to(PROJECT)),'sha256':machine['sha256'],'reader':str((OUT/current['reader']).relative_to(PROJECT))+'#M12','user_accepted':False,'runtime_integrated':False,'handoff_sent':False}
            record['current_issue']='保留旧菱形独眼头与紫白配色，新增有根部连接的棱镜收放和航空机身组织；与雷翎共架为本轮试案，未定母体关系不抬为Canon。'
            record['internal_next']='先收敛镜星主形与共架选择，随后补同形三视与部件；不自动改雷翎已定源、剧情身份或运行。'
            record['identity_reference_status']='M12_existing_identity_M08_shared_airframe_proposal_not_Canon'
        record['production_refs']=[str((OUT/v['file']).relative_to(PROJECT)) for v in machine['views']]+[str((OUT/r['file']).relative_to(PROJECT)) for r in current['source_refs'] if r['id']==id]
    if id=='M03' and decisions.get('guardian_policy',{}).get('reuse_existing'):
        record['historical_production_refs']=record['production_refs']
        record['production_refs']=[f for f in record['current_assets'] if f and (PROJECT/f).is_file()]
        record['current_issue']='用户最新明确馆守Z不用重做，沿用现有；旧风格转绘/新造型计划撤回，不据此批准外援备选替换。'
        record['internal_next']='沿用现有馆守Z资产和既有加载映射，取消本美术会话的重做及风格转绘；必要技术维护仍依原职责。'
        record['project_action']='reuse_existing_no_redesign'
        record['guardian_user_decision']=decisions['guardian_policy']
    records.append(record)
by_id={r['id']:r for r in records}
counts=Counter(r['route'] for r in records)
manifest={'revision':'r4-internal-adoption-20261016','scope':'43 changed images visually re-reviewed; 255 same hashes retain prior source review; 298 adoption routes','review_kind':'source/plan review; exact selected character identities approved per user receipts; derived colors and runtime separate','parent_source_page_sha256':sha(OUT/'before-review-r4.html') if (OUT/'before-review-r4.html').is_file() else sha(PAGE),'binding_corrections':{'M03':'Content formerly filed under S11 is Guardian; filename retained','S11':'Content formerly filed under M03 is Nanami; filename retained'},'route_counts':dict(counts),'runtime_assets_replaced':False,'canon_changed':bool((OUT/'M01-head-design-fixed-20261019.json').exists()),'canon_change_scope':'CML133 head source and latest same-series/crown direction only; new drawings and runtime separate','identity_directions_accepted_by_user':sorted(accepted_ids),'user_decisions':decisions,'records':records}
if (OUT/'M05-head-design-fixed-20261020.json').exists():
    manifest['canon_changed']=True
    manifest['canon_change_scope']='CML133无牌已确认头部；CML134王者指定R6b头部源图。新整机和模型/运行另记。'
if (OUT/'M05-battle-mask-production-r8.json').exists():
    manifest['canon_change_scope']='CML133无牌头部、CML134王者基础头部、CML135王者R7源设计与R8面罩。新增红鳍具体图和转换机构/运行另记。'
if (OUT/'M05-turnaround-production-r12.json').exists():
    manifest['canon_change_scope']='CML133无牌头部、CML134王者基础头部、CML135王者R7/R8/R9源设计已采用。R12新三视仍为绘制源稿，未扩大模型或运行认可。'
if (OUT/'mecha-source-batch-acceptance-20261021.json').exists():
    manifest['canon_change_scope']='CML135王者R12当前7张与CML136旧拳王R2当前3张源设计获用户认可；M01仍仅R16头部，M11新图候选。同模型/动作/运行分别验证。'
    manifest['latest_source_acceptance']='mecha-source-batch-acceptance-20261021.json'
if (OUT/'M11-future-production-r2.json').exists():
    manifest['canon_change_scope']+=' CML137登记M11未来车形/对应人形/无水平天线的用户方向；R2具体新图未自动采用。'
    manifest['latest_source_direction']='M11-future-direction-r2.json'
if (OUT/'M11-structure-and-head-production-r4.json').exists():
    manifest['canon_change_scope']+=' CML137最新方向为整体盔型、无独立顶天线及摄像头后视；R4具体头稿和结构布局均未获采用。'
    manifest['latest_source_direction']='M11-integrated-head-direction-r4.json'
if (OUT/'M11-heroic-antenna-production-r5.json').exists():
    manifest['canon_change_scope']+=' 用户否定R4无天线宽冠/眼镜蛇神态，CML137明确可见天线与正面角色气质；R5具体新稿仍候选。'
    manifest['latest_source_direction']='M11-heroic-antenna-direction-r5.json'
if (OUT/'M11-turnaround-structure-production-r7.json').exists():
    manifest['canon_change_scope']+=' 用户指定eac75eab原头源稿和比例并授权颏甲/三视/可变优化；R7新增图稿仍候选，局部头仓不代表整机通过。'
    manifest['latest_source_direction']='M11-head-aspect-chin-direction-r7.json'
    manifest['latest_M11_head_source_acceptance']='M11-head-selected-and-turnaround-r6.json'
if (OUT/'M11-posture-production-r8.json').exists():
    manifest['latest_source_direction']='M11-posture-direction-r8.json'
    manifest['canon_change_scope']+=' CML137按用户肯定的f27状态修缩脖子；R8体态图仍为新稿，旧三视与头仓待同步。'
if (OUT/'M11-turnaround-delivery-production-r9.json').exists():
    manifest['latest_source_direction']='M11-design-fixed-20261022.json'
    manifest['latest_M11_source_delivery']='M11-delivery-manifest-r9.json'
    manifest['canon_change_scope']+=' 用户已确定R8整机形象，CML139固定源稿；R9修正三视按授权交付。'
if (OUT/'M14-design-fixed-20261022.json').exists():
    selected=json.loads((OUT/'M14-design-fixed-20261022.json').read_text())
    manifest['canon_changed']=True
    manifest['latest_source_acceptance']='M14-design-fixed-20261022.json'
    manifest['canon_change_scope']+=' '+selected['authority_registration']['source_lock']+'固定用户采用的歌翼R4音乐传播源稿，CML023更新当前参考；R5三视按授权派生，人物身份与模型/运行不迁移。'
if (OUT/'aircraft-design-fixed-20261023-r6.json').exists():
    accepted=json.loads((OUT/'aircraft-design-fixed-20261023-r6.json').read_text())
    manifest['latest_source_acceptance']='aircraft-design-fixed-20261023-r6.json'
    manifest['canon_change_scope']+=' '+str(accepted['authority_registration'])+'固定当前R6六张源稿；CML023参考更新，模型/运行另验。'
if (OUT/'M06-design-fixed-20261023-r2.json').exists():
    accepted=json.loads((OUT/'M06-design-fixed-20261023-r2.json').read_text())
    manifest['latest_source_acceptance']='M06-design-fixed-20261023-r2.json'
    manifest['canon_change_scope']+=' '+accepted['authority_registration']+'固定预算二号R2整机与A头型；B/C备选、三视/机构/模型/运行另判。'
if (OUT/'M06-turnaround-design-fixed-20261023-r3.json').exists():
    manifest['latest_source_acceptance']='M06-turnaround-design-fixed-20261023-r3.json'
    manifest['canon_change_scope']+=' CML143当前参考扩展至用户采用的M06正R3/侧R3c/背R3三视；R2/A父源保留，模型/运行另验。'
if (OUT/'city-response-source-production-r2.json').exists():
    manifest['latest_source_candidate_batch']='city-response-source-production-r2.json'
if (OUT/'city-response-design-fixed-20261023-r2.json').exists():
    manifest['latest_source_acceptance']='city-response-design-fixed-20261023-r2.json'
    manifest['canon_change_scope']+=' CML144/CML145固定用户采用的灰崎/消防R2父源；新增三视与机构/模型/运行分别判断。'
if (OUT/'city-response-turnaround-production-r3.json').exists():
    manifest['latest_authorized_turnaround_delivery']='city-response-turnaround-production-r3.json'
if (OUT/'city-response-refinement-production-r4.json').exists():
    manifest['latest_authorized_turnaround_delivery']='city-response-refinement-production-r4.json'
    manifest['latest_source_candidate_batch']='city-response-refinement-production-r4.json'
if (OUT/'city-response-main-handoff-20261024.json').exists():
    manifest['latest_source_handoff']='city-response-main-handoff-20261024.json'
if (OUT/'crane-mirror-source-production-r1.json').exists():
    manifest['latest_source_candidate_batch']='crane-mirror-source-production-r1.json'
write_json(OUT/'adoption-manifest.json',manifest)
with (OUT/'adoption-manifest.csv').open('w',newline='',encoding='utf-8-sig') as f:
    columns=['id','name','route_label','retained','current_issue','internal_next','image','sha256','production_refs','identity_direction_accepted','identity_acceptance_scope','current_assets','loaders']
    w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
    for r in records:w.writerow({k:'\n'.join(r[k]) if isinstance(r[k],list) else r[k] for k in columns})

plan = '''# 外援新版接收与内部美术升级 · 2026-10-16

这批来稿足够作为项目内部升级的风格与造型来源。下一步以同一对象的稳定身份为中心，修订源图、模型、贴图和派生图。配色逐对象决定；KINETIC_CEL统一绘制水平，Memphis用于标题及关键事件的海报层。

## 最新用户修订：无牌独立造型

用户指出旧无牌太像高达，旧头胸/肩腰不再作为升级母版。保留改装竞技与体术身份，v3候选改为运动型头盔、连续护目窗、闭合护面、整体胸壳和开放转腰结构；没有据此宣称法律审查或用户美术认可。旧海报、构图与动作页的主体来源被暂停，确认新候选后再派生。

## 已完成的本轮工作

- 对43项换图重新看图，另外更新无牌、旧拳王、七海三项关联意见；255项同哈希稿沿用前次图面审查，重新给出用途去向。
- M03/S11文件内容挂反，阅读页和采用清单按图义校正。原来稿字节和文件名保留。
- 制作七海、无牌、啮线体、六层避难楼四张内部源图样例，另做天冲拳事件图和正常镜头构图目标稿。
- 四张源图做浅底透明合成检查。画面里的光晕RGB位于透明区；正常合成无光圈。没有据此宣称运行材质/边缘已验收。
- 正常镜头样例发现我方过小，已再作比例修正。该图仍是生图目标稿，不能证明模型、占格、深度遮挡或玩法结果。

## 怎样采用298项来稿

每张的采用部分、内部下一步、原接入映射与目标位置，见同目录adoption-manifest.csv/json及原阅读页。四种去向是加工方式，不是完成度或用户认可。

1. 二维原画可加工采用：主要是已有形象成立的人物和少量背景。清除版头、伪字、背景并导出，不无故换脸或重做服装。
2. 结构与造型母版可采用：主体成立的机甲、敌体、建筑、部件、地形，作为低模/贴图制作来源；不能将JPEG贴到站立平面冒充3D模型。
3. 内部修订后派生：保留来稿的设计收益，回到项目身份和用途修正。如王者补回武器冗余、合体使用唯一完整核心、车辆/飞机维持同一套零件。
4. 图形、版式与演出参考：UI、图标、轨迹、状态、动作示意。采用语义与构图，在现有事件和界面系统里重建，不整张照搬说明板。

## 同一风格，保留不同对象

- 人物：各自脸、发型、年龄、服装大分区不变；对话画同一头身规范，头像同一眼线/头顶留白。不能用全身缩图做头像。
- 我方机甲：保留各自IP家族、能力与涂装；同一对象锁头胸、拳/武器接口、膝足与轮廓。两级硬阴影、压力墨线和大色块统一，不能把所有机器涂成青白金。
- 敌体：单格标准敌人以相当的视觉分量对抗机甲。按功能区分咬切、射击、架设、重楔、飞行等剪影，不靠统一红色描边才认得敌人。
- 建筑：生活楼必须像多层现代住宅；供电、泵站、吊装、车站各有功能轮廓。先图再低模、UV与贴图；封闭屋顶、窗洞和楼板厚度必须合理。
- 尺寸：视觉档位与逻辑占格分离。小型/标准单格、重型2×2、特定超大型3×3；人物/机器犬约四分之一格视觉量。不得再以原作米数机械缩成大小悬殊的一堆物件。
- 地形：体块、凹槽、断面、渠岸深度用必要几何表达；表面材质用贴图补充，不把完整凹坑或半毁屋顶烘焙在平面上。
- 色彩：机体保留身份色。A供能区、B渠岸、C装卸区依据材质与环境分别定主色，不能复制同一套青白红。战术色只表示当前规则，光墙/轨迹按需显示。
- Memphis：仅标题/切入/关键事件局部使用错位色块、圆点、斜带及真实排版；不铺到正常棋盘、人物面部或机械结构上。动效短、有终点、可减弱，不常驻高频闪烁。

## 样例的判断与仍须验证之处

H03：保持原脸、短发与白/藏蓝/酒红外套，已去掉说明板，适合继续派生对话与头像。表情族和对话中的眼线比例还需实际接入。

M01：用户已否定旧稿的高达式外形，前轮保持旧头胸的建议撤回。新的v3候选保留改装体术机定位与白青绿/金色，但重做头盔、护面、胸壳、肩腰轮廓。旧拳击事件和构图中的身体只作为历史，等待新方向确认后重派生。

E01：保留机械甲虫与咬切器构造，试用靛紫壳/珊瑚切刃，作为与地面分离的颜色候选。不是把全体敌人染紫；小尺寸下的眼部、口器和腿间空隙仍须在3D镜头检验。

B01：六层住宅的封闭屋顶、厚楼板、转角玻璃和入口明确，科幻程度采用克制的近未来住宅方式。当前线条比机体细，制作低模时需收敛窗栏/设备密度；不能直接贴一张正面图代替全楼。

TACTICS：同一现有B场地构图里检查主角、敌体、楼房与地面分色，修过机体偏小的问题。仍是目标插画，地格密度、可走边界、遮挡与相机需要实机量测。

IMPACT：天冲拳海报背景图形可用CSS/游戏节点平移、裁切、淡入实现；这不是已经完成的战斗动画。

## 升级顺序与每段交付

### 0. 先确认本轮样例

用户判断四类主体的绘制方向、机体/建筑的体量和事件海报是否合适。需要调整时只修被指出的维度，保留已稳定身份。确认不是对298张单独设计或所有配色的自动认可。

### 1. 统一母版和派生规则

覆盖M01—M15、H01—H12、E01—E11。先确认无牌独立造型候选，不沿用被否定的高达式头胸；再完成无牌/旧拳王/王者、七海、啮线体、避难楼这条制作链，扩到其余对象。所有对象记录来源哈希、身份锚、配色与派生文件。王者合并早期武器冗余和本轮正确挂点；馆守按当前身份母版与自身右臂毁损事实制作；合体核心不能换脸。人物不重新发明服装。

交付是可追溯的生产母版、结构视图和头像/立绘候选；通过正常距离检查后进入下一段。源图数量不能代替质量。

### 2. 模型、材质与部件

覆盖F01—F18、B01—B34、T01—T16以及所有活动单位。沿已有game-godot主工程资源映射制作低模、UV、贴图和少量必要体积；地图地面保留深度与结构。部件按所属机体共用节点，飞机/车辆/合体用相同零件变换，不独立生成每个状态后拼接。

首个实机体验为B面桥座的观察→推开威胁/托桥→列车通过。先以正确机甲、标准敌体、避难楼/供电设施/列车和渠岸做同位正常镜头，再推广A/C。此顺序不缩减52包和331条原要求。

交付是实际加载的模型/材质/状态，加正常镜头、旋转视角、遮挡和尺寸证据。建筑损坏需有真实断面，不准半毁屋顶贴面。

### 3. 共享动作与事件演出

N01—N14作为动作来源；常规待机、走跑、飞行、射击、持物、操作、受击/击破使用动作族和机体参数适配。仅天冲拳及确有身份价值的体术招式定制发力。攻击/操作事件→各对象处理自身状态；不做每对机体/建筑的接触坐标表。机柜只需合理手部动作加状态反馈，不制作开门接线细节。

X01—X30、C01—C16由真实结果事件驱动爆炸、贯穿、位移、碰撞、失锁和环境响应；同一次结果供预演、执行、回放和HUD使用。连续动作、命中可读性与声音实听都要检查。

### 4. 图形、UI和剧情事件

覆盖G01—G25、U01—U20、I01—I65、S01—S21。保留来稿已成立的语义，沿现有输入/HUD改成按需信息：光标探索看对象，选中看范围，指向目标看弹道/位移/预计耐久，离开收起细节。头像来自母版头肩。标准高度世界空间威胁光墙由规则占格生成，深度遮挡正确，不将线框贴过楼顶。

纪存调度、白鸢预演、七海核验撤令各自保留职责；界面文字和数字来自真实状态。海报层只用于名场面、标题或明确事件切入。救援、工房、清障、变形/合体事件沿唯一对象母版分层，不能又换人换机。

### 5. 扩展与验收

在第二种机体、第二类设施和第二战场验证复用，再推广全量。回到原52包/331条台账逐项绑定实现位置和实际体验；不另建一套“美术已完成”进度覆盖原状态。

源稿确认、正常镜头目标、主工程加载、连续演出/声音、原生输入、用户最终接受分别记录。当前只完成第一批源稿样例和接收分析；没有替换游戏资源、没有完成全量美术、没有替用户签署认可。

## 原接入映射与目标位置

全部298项沿用20261012派单中的接入映射，见adoption-manifest.csv/json；它不是逐个加载点都在本轮运行验证。四张样例的资源和脚本路径已核对存在，七海、避难楼的引用也已对照代码。四张样例对应：

- H03：chapter_c02_v1/qihai.png；dialogue_presenter、campaign_stage、people_rules与chapter_c02/ui。
- M01：stage_battle_v11/hero.glb及linked_campaign_v6/portraits/hero.png；catalog、round_armaments、campaign_world与rescue_data。
- E01：linked_campaign_v4/models/claw.glb；campaign_data、rescue_data、rescue_cases与full_data。
- B01：linked_campaign_v6/environment/refuge-habitat-{0,1,2}.glb；full_art、fixture_art、environment_art与presentation_layout。

这些是接入目标，不是本轮已经覆盖的文件。完整绝对/工程相对路径保存在采用清单。

## 来源、制作与检查

来源：本轮43项更新来稿、原298项派单/接入映射、前轮逐图诊断、项目最新视觉总参考、CML128风格与各对象身份来源。M03/S11对应按实际内容校正，原图未改。

样例通过内置Imagegen生成，提示词、输入图、原输出位置见prompts*.json与generation*.json；选中输出已复制samples目录。alpha-check.jpg是透明素材合成检查；small-scale-check.jpg检查80/100/140px量级的轮廓。两者都不是游戏运行证据。

HTML检查采用本地结构/链接/脚本语法检查。先前浏览工具对该file页面有明确安全拒绝，本轮没有绕过，也不宣称浏览器交互或原生游戏已验证。
'''
plan=plan.replace('## 最新用户修订：无牌独立造型','## 上一轮：无牌独立试稿，继续按最新识别性原则修订')
plan=plan.replace('## 上一轮：无牌独立试稿', (OUT/'direction-revision-content.md').read_text()+'\n\n## 上一轮：无牌独立试稿',1)
plan=plan.replace('H03：保持原脸','H03：新形象已获用户确认，保持原脸')
plan=plan.replace('用户判断四类主体的绘制方向、机体/建筑的体量和事件海报是否合适。','三主角的新形象已确认；其余形象与机体按最新来源及组合要求检查样例，继续比较体量与海报用量。')
plan=plan.replace('先确认无牌独立造型候选，不沿用被否定的高达式头胸；','三主角沿确认形象，唐胶/兜灯/胶价王及馆守优先转绘原形象，社勇王按V17/V18/V19和长发核心整合；无牌补足独立且鲜明的特征，不沿用被否定的旧头胸；')
plan=plan.replace('当前只完成第一批源稿样例和接收分析；没有替换游戏资源、没有完成全量美术、没有替用户签署认可。','当前完成样例、接收分析和本次用户方向吸收；三主角形象已获确认。未替换运行资源，不将此扩大为全量美术或运行验收。')
plan += '\n\n## 与战斗主线的交接\n\n本会话先制作美术源图与独立候选件；正式运行资源、加载映射与原生验证拟由主玩法会话集中接入。详见[美术交接说明](美术交接说明-20261016.md)。主玩法已在交接说明第8节确认分工、人物裁切/眼线和3D骨架接口；美术制作并行推进，正式替换只避开单次原生录制。H01/H02已做独立透明导出，H03复用，见dialogue-production-r1.json。发送与接收记录见交接发送记录-20261016.json，接收确认不等于运行接入或品质通过。\n'
plan += '\n最新状态：dialogue-production-r2.json修复白鸢旧导出的三手错误，旧R1不作新派生来源。\n'
if freeze:
    manifest['canon_changed']=True
    manifest['canon_change_scope']+=' 另保留Working美术源范围CML132；非故事、身份或运行迁移。'
    manifest['current_source_design_freeze']={'record':str(freeze_path.relative_to(PROJECT)),'scope':freeze['acceptance_scope'],'runtime_accepted':False}
    write_json(OUT/'adoption-manifest.json',manifest)
    plan += '\n2026-10-18用户确认：社勇王整机、四机组件及六名角色本批设计固定。具体图稿见[本批设计固定清单](source-design-freeze-20261018.html)；后续沿固定源制作，不重新发散造型。技术派生、模型、动作与运行分别验证。\n'
    if followthrough.get('new_handoff_sent'):
        plan += '\n已按用户要求集中交给“战斗主玩法打磨”，内容见[source-design-freeze-handoff-20261018.md](source-design-freeze-handoff-20261018.md)，实际发送见原交接发送记录。当前无牌R4长耳头冠已被否定，改为[六种头部参考](M01-head-directions-r5.html)；馆守Z按最新决定沿用现有，取消重做。新头部尚未确认、未发送或替换运行。\n'
if decisions.get('guardian_policy',{}).get('reuse_existing'):
    plan=plan.replace('唐胶/兜灯/胶价王及馆守优先转绘原形象','唐胶/兜灯/胶价王沿确认形象，馆守沿用现有资产')
    plan += '\n最新馆守范围：沿用现有馆守Z，不再安排新造型或画风转绘；上文日期较早的馆守转绘建议已被本次用户决定覆盖。既有玩法、动作和必要技术维护按原职责继续。\n'
if (OUT/'M01-head-AE-production-r6.json').exists():
    plan += '\n最新无牌方向：用户选择A中央冠脊+E折角侧翼，要求对称并区别馆守Z。已实际绘制[同一头部的正面/三分之四整合稿](M01-head-AE-r6.html)，对照连续视窗、封闭面甲、侧后短翼与馆守的前额横角/双眼/口栅。方向已选，具体新绘待看；未替换运行或发送新候选。\n'
if (OUT/'M01-head-aft-antenna-production-r7.json').exists():
    plan += '\n最新R7局部修正：按用户指定R6原图，把双侧天线改为单段直线朝后，与中央冠脊同向，取消折角外张；头型、面甲、连续视窗与配色延续。[当前图与R6对照](M01-head-AE-r6.html)。此前E折角形态被本次明确意见覆盖；具体新图待确认，未交接或替换运行。\n'
if (OUT/'M01-head-crest-consistency-production-r8.json').exists():
    plan += '\n最新R8：用户认可R7总体及侧天线方向，同时要求修正头顶冠脊跨视图不一致。以正面为结构依据，局部修正三分之四的金槽收尖及白色分段，[当前R8与R7对照](M01-head-AE-r6.html)；保留已有认可，新修正未自动签认，精确投影仍由后续同一模型输出。\n'
if (OUT/'M01-head-center-groove-production-r9.json').exists():
    plan += '\n最新R9b：R8只改槽尾/分段，未修到凹槽所在面的错误，用户已明确反证。现用实际冠体中央顶槽投影作参考，独立重绘三分之四；正面沿R7左视图。[当前组合与原错误对照](M01-head-AE-r6.html)。新图待确认，脸部、配色和已认可侧天线保持，不能把R8当作此项通过证据。\n'
if (OUT/'M01-head-front-match-production-r10.json').exists():
    plan += '\n最新R10：用户已明确采用R9b所示头部设计，以它为母稿保持三分之四，修正正面冠体及凹槽。[当前正面与采用设计对照](M01-head-AE-r6.html)。采用范围见M01-head-design-adoption-20261018.json及Working CML133；新正面仍待确认，不扩大为完整机体或运行认可。\n'
if (OUT/'M01-head-twin-grooves-production-r11.json').exists():
    plan=plan.replace('最新R9b：','历史R9b（作者单中槽解释已作废）：').replace('最新R10：','历史R10（前视单中槽错误）：')
    plan='# 当前无牌冠脊解释 · R11\n\n用户明确两条黄色凹槽在左右标线，中间为连续白色实体；下方小黄块保留，已采用侧视不改。旧单中槽描述和Blender参考作废。当前图见[M01读页](M01-head-AE-r6.html)，具体解释见M01-head-groove-interpretation-20261018.json；新前视未自动认可。以下旧轮文字保留历史，以本段明确解释为准。\n\n'+plan
if (OUT/'M01-turnaround-production-r12.json').exists():
    plan=plan.replace('# 当前无牌冠脊解释 · R11','# 历史：R11施工时的冠脊解释').replace('新前视未自动认可。','R11前视随后已由用户确认，详见本页最新段落。')
    plan='# 当前机体批次 · 2026-10-19\n\n无牌R11头部已由用户确认，双侧黄槽与白中脊固定。已补[整机正侧背R12b](M01-turnaround-r12.html)，新整机三视图待看，不扩大头部确认范围。\n\n下一批已绘制[旧拳王与完全版王者新样例](next-batch-mecha-20261019.html)：旧拳王沿自身头胸/配色统一重肩厚拳；王者沿当前形象恢复右钻左盾、背肩双炮、层翼及腿侧舱。两张新样例均待用户看稿，确认后再补结构和同源派生。\n\n馆守Z沿用现有；社勇王与六名人物的固定29文件批次不变。新图暂未发送主玩法对话，模型/加载/动作/运行另行验证。本批接续design-followthrough-r1.json，不另建进度台账。实际提示词见[本批索引](mecha-batch-prompts-20261019.json)。\n\n以下保留原计划与带日期的修订历史，以本段及各对象最新记录为准。\n\n'+plan
if (OUT/'M01-head-position-production-r14.json').exists():
    plan='# 当前：无牌头冠位置R14与同系列整机R13\n\n用户指出旧无牌矮圆、像机器河童，且与完全版王者不同系列。R12整机已退回；R13拉开头身与腿长，统一胸肩及关节家族，但最新反馈头顶天线位置仍差，现已画[四种克制头冠方向](M01-family-head-review-r14.html)。作者优先D，B为需要压短的备选，用户尚未选定。\n\n王者保持原虚构系列钦定主角机的臃肿、华丽与过武装；无牌是同系列量产基础体、本作重要角色，依靠头冠、简洁胸甲和金色前臂护轨形成记忆点，并由体术姿态显出主角感。旧R11局部认可保留历史，不能阻止最新头冠形态重新探索；新R13/R14均未自动认可。头型选定后再合回整机及补正侧背，不在未选头型上继续批量派生。\n\n[实际提示词](M01-family-and-head-prompts-r13-r14.json)。馆守Z、社勇王/人物固定29文件和主玩法台账保持。以下为此前计划与当时状态，当前以本段为准。\n\n'+plan
if (OUT/'M01-synthesis-head-production-r15.json').exists():
    plan='# 当前：无牌综合头型R15\n\n用户提出“考虑一下天威勇士和擎天柱的头型综合”。已核对官方图，先按倍功夫/Baikanfu与经典G1取样，完成[综合头肩样例](M01-family-head-review-r14.html#synthesis-r15)：中央低额块、方正盔体、高位侧后双天线，保持无牌青白金、琥珀视窗、白面甲及与王者同族的颈下。新图待用户看稿，尚未选定。\n\n参考拆解、原图与[内置生图实际提示词](M01-synthesis-head-prompt-r15.json)均已绑定；头型确认后固定天线体量/根位并补正侧面与整机三视。R14四方向保留历史，馆守与固定源图批次不变。以下为此前计划与当时状态。\n\n'+plan
if (OUT/'M01-head-proportion-production-r16.json').exists():
    plan='# 当前：综合方向保留，头部比例修正R16\n\n用户表示综合头型看着还行，同时明确指出头部反复被压扁。作者此前把克制/小头处理为低盔顶和横向展宽，现已只修[头壳本体比例](M01-family-head-review-r14.html#head-proportion-r16)，恢复纵向体积、收拢颞侧，保留综合结构/视窗/面甲和配色。\n\n新修正图尚待用户看稿；原始图像按自身比例显示，不拉伸原图。以后小头通过相对身体整体缩小实现，不以压低头壳实现。提示词见[M01-head-proportion-prompt-r16.json](M01-head-proportion-prompt-r16.json)。以下保留此前计划与当时状态。\n\n'+plan
if (OUT/'mecha-source-decisions-20261019-r17.json').exists():
    plan='# 当前：无牌头部固定，旧拳王沿用，王者统一画法\n\n用户确认[无牌R16头部](M01-family-head-review-r14.html#head-proportion-r16)，低额块、侧后双天线与正常纵向头壳固定。接下来先合回R13颈下，检查整机比例后再补视图；R13图上的旧头型不再派生。旧拳王当前样例问题不大，沿该方向继续，无需重选造型。\n\n王者需要小幅统一绘制语言：大块面、墨线层级、两级阴影与关节细节向无牌靠拢，减少闪亮反光和细碎刻线；保留原藏蓝白红金、华丽全装、右钻左盾、双肩炮、层翼和腿侧舱。[R2样例与新旧对照](M05-style-match-r2.html)已完成，具体画法待看，不扩大为王者造型或模型认可。\n\n[用户决定与具体来源](mecha-source-decisions-20261019-r17.json) · [内置生图实际提示词](M05-style-unification-prompt-r2.json)。接续原design-followthrough-r1.json；馆守和29张固定源保持，当前新图未交接。以下为带日期的修订历史，以本段为准。\n\n'+plan
if (OUT/'M05-modular-production-r4.json').exists():
    plan='# 当前：王者L角、素体与配件包R4\n\n头部以用户图四的脸为依据，四瓣侧冠成对、内侧两瓣加长；中间改为朝前的L型犄角，前端加朝回的鱼叉倒钩。正面中轴作透视缩短，左侧显示L形和倒钩。\n\n[本轮头部、素体、全装与配件包](M05-modular-r4.html)已分别绘制。素体保留同一头胸和完整双手，外挂按冠军外甲、翼与推进、双重炮、右臂钻、左盾和腿侧弹仓六组整理；成对低位推进舱为新增候选。保留原藏蓝白红金、厚重华丽与有用冗余，不把拆包理解为削弱王者身份。\n\n新图待看；精确结构、各视图及活动让位仍沿同一母稿继续固定。[用户要求](M05-modular-direction-r4.json) · [配件分组](M05-module-catalog-r4.json) · [全部实际提示词](M05-modular-prompts-r4.json)。接续原台账；无牌已确认头部、旧拳王方向、馆守及固定源图保持，新图未交接。以下为此前计划与当时状态。\n\n'+plan
if (OUT/'M05-head-upward-L-production-r5.json').exists():
    plan='# 当前：王者改为朝上独角仙L角R5 · 2026-10-20\n\n用户纠正中央角不是向前刺出，而是类似独角仙的向上L角。当前[头部正侧修正](M05-modular-r4.html#head)采用短前探底座、向上长角身和朝回倒钩；图四脸、两对侧冠与色系保持。旧R4水平前刺解释作废。\n\n本次只修头部源稿。R4素体/全装尚含旧角，明确只作颈下与配件参考；当前头部选定后再同步，不在错误中角上继续派生。[用户纠正](M05-head-upward-L-direction-r5.json) · [实际提示词](M05-head-upward-L-prompt-r5.json)。仍沿原台账，新稿未交接或替换运行。以下为此前计划与当时状态。\n\n'+plan
if (OUT/'M05-head-riese-production-r6.json').exists():
    plan='# 当前：王者角与天线重整R6 · 2026-10-20\n\n用户否定R5直立箭头角，指定参考古铁巨神。本轮实际观察参考图，改厚根、连贯上挑的刀刃额角与两对较细的侧天线，保留图四脸和王者原色；正面中轴另行收正。[当前头部](M05-modular-r4.html#head) · [本次来源和要求](M05-head-riese-direction-r6.json) · [实际提示词](M05-head-riese-prompt-r6.json)。\n\n当前只做头稿。R4素体/全装继续仅作颈下与配件参考；头部选定后再同步整机。接续原台账，新稿待看，未交接或改运行。以下为此前各轮计划及当时状态，R5执行已被最新反馈否定。\n\n'+plan
if (OUT/'M05-head-design-fixed-20261020.json').exists():
    plan='# 当前：王者R6b头部选定与R7整机同步 · 2026-10-20\n\n用户附R6b原图明确“用这张的设计”，[指定头部](M05-modular-r4.html#head)及哈希由CML134固定；头型不再发散。[本次认可范围](M05-head-design-fixed-20261020.json)。\n\n已把同一头型合回[素体与全装R7](M05-modular-r4.html#chassis)，保留原身体、双手／钻盾、双炮、层翼及四个腿侧弹仓；新整机图是源稿候选，不扩大头部原图认可。[实际提示词](M05-modular-head-sync-prompts-r7.json)。多视、隐藏根位、配件接口和运行继续各自验证，馆守及固定29源保持，新图未交接。以下为此前计划及当时状态。\n\n'+plan
if (OUT/'M05-red-fin-production-r9.json').exists():
    plan='# 当前：王者战斗面罩与红色中线鳍 · 2026-10-20\n\n用户认可R7素体/全装源稿并要求追加普通脸／战斗面罩转换；R8面罩随后已采用。最新按侧图红线增加头顶中线红鳍，保留同一皇冠、眼眉和耳罩，普通脸／面罩两状态共用头盔。[当前双状态与转换示意](M05-battle-mask-r8.html) · [面罩采用及红鳍要求](M05-mask-and-fin-direction-r9.json)。\n\nR9首稿的前视红色背衬已局部收掉：薄鳍在正面被金色中角遮住，侧面展开。新增红鳍图供看稿，R7整机尚未合入红鳍与闭合面罩；收纳体积与机关轨迹仍需结构稿/模型校核。[实际提示词](M05-red-fin-final-prompts-r9.json)。接续原台账，未改运行或自动交接。以下为此前计划与当时状态。\n\n'+plan
if (OUT/'M05-turnaround-production-r12.json').exists():
    plan='# 当前：王者恢复身形的三视 R12 · 2026-10-20\n\n用户已采用红鳍双状态头部并要求补三视，随后指出R10把机体画矮。现改为每个视角独立出图，先恢复R7整机的长腿与正常头部体积，再推侧背。[全装三视](M05-turnaround-r12.html#full) · [素体三视](M05-turnaround-r12.html#core) · [两状态头部](M05-turnaround-r12.html#head)。\n\nR10比例稿退出当前来源；R11新稿与已采用R7/R8/R9源设计分开。接续原design-followthrough-r1.json及其中唯一比例缺陷记录，未改运行或自动交接。[实际提示词](M05-turnaround-prompts-r12.json)。以下为此前计划及当时状态。\n\n'+plan
if (OUT/'M02-turnaround-production-r2.json').exists():
    plan='# 当前：补齐旧拳王三视 R2 · 2026-10-20\n\n按用户追问，沿现有R1方向补[旧拳王正侧背](M02-turnaround-r2.html)，保留象牙白/土棕/深红、厚肩红拳套、正常头部体积和修补装甲左右。先展开站直正面，再由它约束侧背，未重新发散造型。\n\n王者当前三视继续保留。旧拳王本次新源稿与模型、拳击动作及运行分开；接续design-followthrough-r1.json，不另建进度台账。[实际提示词](M02-turnaround-prompts-r2.json)。以下为此前计划与当时状态。\n\n'+plan
if (OUT/'M11-cargo-production-r1.json').exists() and not plan.startswith('# 当前：货柜领袖双形态 R1'):
    plan='# 当前：货柜领袖双形态 R1 · 2026-10-21\n\n用户明确“好的 这批素材过了，继续下一批”。[本次采用回执](mecha-source-batch-acceptance-20261021.json)固定旧拳王R2当前3张与王者R12当前7张源设计；历史弃稿不回流，无牌仍仅R16头部认可。\n\n下一批已出[货柜领袖机器人正侧背与四轴货车](M11-cargo-r1.html)：沿CML028 v4头脸，统一四轴八轮位、驾驶室分件和独立可卸货柜；背面轮轴视向与侧面斜角完成局部修正。四张新图待用户看稿。\n\n接续原design-followthrough-r1.json；同模型转轴、连续变形、关联事件图、模型/动作和运行各工序另记。馆守Z、固定29源、其他会话台账保持。实际[提示词组](M11-cargo-prompts-r1.json)。以下为此前计划与当时状态。\n\n'+plan
if (OUT/'M11-future-production-r2.json').exists() and not plan.startswith('# 当前：货柜领袖未来双形态 R2'):
    plan='# 当前：货柜领袖未来双形态 R2 · 2026-10-21\n\n用户要求车形参考Tesla货车更未来，人形随之对应；保留擎天柱/货运领袖文化投射但拉开具体头脸，并明确不要水平天线。CML137登记该方向，旧v4横向颞鳍不再约束后续派生。\n\n本轮已画[未来车形、人形母稿和头部近景](M11-future-r2.html)：大弧面无中分风挡、平滑前罩、导流覆壳；人形单片弧面胸窗和圆弧肩壳同步，头部内嵌通讯块取消横向杆。三张具体新图供本轮看稿，未自动采用。\n\n四轴/八轮位与独立货柜沿用为本轮结构提案。R1侧背仅历史，不作为R2当前几何；新头型和整机选定后再补多视/同模型变形。接续design-followthrough-r1.json，馆守、固定29源和上一批已认可10张保持。实际[提示词组](M11-future-prompts-r2.json)。以下为此前计划与当时状态。\n\n'+plan
if (OUT/'M11-structure-and-head-production-r4.json').exists():
    plan='# 当前：货柜领袖整体盔型与变形布局 · 2026-10-21\n\n按最新头盔参考改整体额框—侧盔—护颊，两种新头稿不含独立顶天线；车形补摄像头后视。[当前头部、车形与展开草模](M11-structure-and-head-r4.html)。具体新稿未获采用，R2整机仅作颈下参考。\n\n同一组刚体及八轮位已出四状态与运动导出；驾驶空间、部件碰撞、承重/支撑仍未解决，不能称完整变形已验证。R3生成分镜多出支撑腿和压短比例已弃用，方法变更已实际落实，沿用design-followthrough-r1.json的唯一缺陷记录。\n\n[实际提示词组](M11-structure-and-head-prompts-r4.json)；此前固定29源、旧拳王/王者已认可10张保持。以下为各轮历史计划及当时状态。\n\n'+plan
if (OUT/'M11-heroic-antenna-production-r5.json').exists():
    plan='# 当前：货柜领袖保留天线与正面角色头型 · 2026-10-21\n\n用户再次明确不是不要天线，且不一定要尖；否定R4宽冠的眼镜蛇和邪恶观感。当前[同一头部正面与斜视](M11-heroic-antenna-r5.html)画出明确耳侧钝头天线，收窄侧盔、简化面甲，再局部放平眼眉。R4 A/B均退出当前推荐，新稿待看。\n\n使用[内置生图提示词组](M11-heroic-head-prompts-r5.json)。原defect_ledger保留用户反证及已执行换法；此轮只修头部，既有车形/布局沿用，未重做或宣称变形问题已解决。以下为此前各轮及其当时状态。\n\n'+plan
if (OUT/'M11-turnaround-structure-production-r7.json').exists():
    plan='# 当前：货柜领袖指定头部、双形态三视与可变结构 · 2026-10-21\n\n用户明确指定eac75eab原眼形头稿，要求保持原头比例、身体按R2长腿头身比，并新增勇者式前凸颏甲。现补[人形三视、车形三视与结构设计](M11-turnaround-structure-r7.html)，包括头仓/天线后折和轮架、腿架、三片货台去向。[当前7张源稿](M11-turnaround-structure-production-r7.json)。\n\n头仓同件草模已做，检查范围限矩形包络和收纳终态；详细装配、驾驶空间、整机受力与全程碰撞未验证。用户原头认可不扩大到新增图稿或运行。比例反复失败、侧角/背架修正与错误带柜分镜的移除均记在原defect_ledger。[实际提示词](M11-turnaround-structure-prompts-r7.json)。以下为此前各轮及当时状态。\n\n'+plan
if (OUT/'M11-posture-production-r8.json').exists():
    plan='# 当前：货柜领袖肩颈体态修正 · 2026-10-21\n\n用户肯定f27斜侧稿整体状态，随后指出缩脖子，要求参考擎天柱体态。已沿同一稿保留厚重肩胸、背架和长腿，调整颈部露出、肩线与胸甲上沿。[当前R8看稿与原稿对照](M11-turnaround-structure-r7.html#posture-r8) · [实际提示词](M11-posture-prompt-r8.txt)。\n\n新斜侧稿已出；此前三视和头仓活动结构尚未同步R8，沿原design-followthrough-r1.json继续，不自动签署新图或运行。以下为此前各轮及当时状态。\n\n'+plan
if (OUT/'M11-turnaround-delivery-production-r9.json').exists():
    plan='# 当前：货柜领袖形象确定与修正三视交付 · 2026-10-22\n\n用户确定R8整体形象。R9正侧背已按露颈沉肩、原头型、长腿及纵向货台背架修正；[三视与交付包](M11-source-delivery-r9.html) · [实际提示词组](M11-turnaround-prompts-r9.json)。已确定形象的派生继续沿此稿，源设计交付与模型/运行分别判断。下一批接原清单雷翎与歌翼的航空双形态。\n\n'+plan
if (OUT/'aircraft-source-batch-20261022.json').exists():
    plan='# 当前：雷翎与歌翼双形态首稿 · 2026-10-22\n\n货柜领袖形象已确定，[修正三视及源交付包](M11-source-delivery-r9.html)已完成。本批接原M08/F07、M14/F08及N13要求，已绘[两台双形态候选](aircraft-source-batch-20261022.html)，补座舱/机鼻、主翼根、喷口和挂架对应。雷翎航空枪向首稿错误已局部修正R1b；实际挂点为近侧机身背部导轨。\n\n[实际内置生图提示词组](aircraft-source-prompts-20261022.json)。新图尚未采用；三视、一个可信中间态和同件模型仍按原范围继续，原Working参考不自动替换。接续design-followthrough-r1.json。以下保留此前各轮及当时状态。\n\n'+plan
if (OUT/'aircraft-runtime-comparison-20261022.json').exists():
    plan='# 当前：保留雷翎、歌翼现用机设，先比较配色与材质 · 2026-10-22\n\n[现用模型与新稿对照](aircraft-runtime-comparison-20261022.html)：现用雷翎的放射刃翼、窄头和歌翼的长双角、肩翼裙甲更有记忆点，新稿不推荐替换。雷翎投射Transformers喷气重涂谱系，歌翼投射Macross可变战机谱系；不同机设共享本作画法，不强制同机架。\n\n保留现用模型、头胸、翼形、比例、骨架与动作；下一步先做同构图保形配色和有限材质清理的比较。本轮完成现用四模型取图与作者比较，没有制作换色样本或修改运行资产。新稿转作结构研究，撤回沿其直接补整机三视/模型的当前安排。原design-followthrough-r1.json已接续，以下是此前各轮及当时状态。\n\n'+plan
if (OUT/'aircraft-existing-design-recolour-production-r2.json').exists():
    plan='# 当前：雷翎与歌翼沿现用机设的配色修订 · 2026-10-22\n\n按用户继续调整的要求，已沿Demo现有头胸、翼形与身形分别绘制[两台双形态配色修订稿](aircraft-existing-design-recolour-r2.html)。雷翎为墨蓝/钴蓝、朱红与象牙切面，歌翼为暖象牙、朱红与石墨关节；共同清理旧亮裂纹与碎反射。\n\n[实际内置生图提示词](aircraft-existing-design-recolour-prompts-r2.json)。本轮为二维源稿，原模型/贴图/骨架/动作未改；同模型材质及正常镜头效果尚未验证，具体色样未自动获用户采用。上一轮蓝紫/粉白新机设仍只作结构研究。接续design-followthrough-r1.json，以下为此前各轮及当时状态。\n\n'+plan
if (OUT/'aircraft-synthesis-production-r3.json').exists():
    plan='# 当前：雷翎与歌翼故事/IP综合设计R3 · 2026-10-22\n\n用户反证R2整机回退，要求综合指定头型、较好的前建议稿与现用机设长处。已完成[两台综合整机、头部近景与航空态](aircraft-synthesis-r3.html)。雷翎实际改成V形侧天线/座舱胸/长枪与刃翼组合；歌翼按可变战机护航职责重画航空头盔、座舱胸和翼腿结构，恢复前建议稿的插画体积与关节完成度。\n\n[实际内置生图提示词](aircraft-synthesis-prompts-r3.json)。R2不再作为整机约束。源稿仍为候选，歌翼附加挂舱未完全按两主发动机精简，需要背视继续收敛；原模型、骨架与运行未改。原defect_ledger保留两轮反证与本次实际换法，以下为此前各轮及当时状态。\n\n'+plan
if (OUT/'M14-music-support-production-r4.json').exists():
    plan='# 当前：歌翼R3增加音乐传播模块R4 · 2026-10-22\n\n用户认为R3好了很多，并询问歌姬/驾驶员分工与扩音器、乐器特征。核对现有角色表：隼真驾驶歌翼，莉歌为星间歌姬；本轮沿该分工绘制[音乐模块展开、闭合与航空收纳](M14-music-support-r4.html)，保留R3主体和雷翎R3。\n\n[实际内置生图提示词](M14-music-support-prompts-r4.json)。大气内扩声，宇宙中转播歌声信号；不将普通声波写成真空传播。当前为附加模块源设计候选，未改人物身份、剧情、运行或技能，未生成或实听歌曲/音效。源图不能证明净空与完整变形。接续原design-followthrough-r1.json，以下为此前各轮及当时状态。\n\n'+plan
if (OUT/'M14-turnaround-production-r5.json').exists():
    plan='# 当前：歌翼R4已采用，正侧背三视R5交付 · 2026-10-22\n\n用户以“这版可以。出具三视图”采用歌翼R4源设计，CML140绑定该原稿及哈希、CML023更新参考。已沿同一母稿绘制[正面、修正侧面和修正背面](M14-turnaround-r5.html)，保持长身比例，三图统一声翼前向展开；背面展示外壳/支架与后跟。\n\n[源图与实际内置生图提示词包](M14-source-turnaround-20261022-r5.zip)。侧背初稿的转角/脚尖错误已局部修正并记入原defect_ledger；最终源图仍带少量插画透视，不作为精密机构投影。新三视按授权交付，不代签逐图新用户认可或模型/音频/运行。以下为此前各轮与当时状态。\n\n'+plan
if (OUT/'M08-turnaround-production-r4.json').exists():
    plan='# 当前：雷翎三视R4补齐 · 2026-10-22\n\n按用户追问，沿R3综合稿绘制[雷翎正面、修正左侧面和背面](M08-turnaround-r4.html)，保留V形侧天线、座舱胸、红白蓝刃翼及长腿。修正侧向投影、肩后壳与后骨盆，长枪始终在机体右手。\n\n[原尺寸源图与实际内置生图提示词包](M08-source-turnaround-20261022-r4.zip) · [歌翼已交付三视](M14-turnaround-r5.html)。本批为二维源设计派生，细部隐面与精确投影待同件模型核对；没有扩大新图或运行认可。接续原design-followthrough-r1.json。以下为此前各轮与当时状态。\n\n'+plan
if (OUT/'M08-turnaround-production-r5.json').exists():
    plan='# 当前：雷翎恢复修长身形三视R5 · 2026-10-22\n\n用户用R3原设定指出R4三视变矮、变敦实。已回到原稿修正肩胸宽度、腰髋位置和长腿，头盔保留纵向体积；重绘正面后同步侧背。[修长身形三视与前后对照](M08-turnaround-r5.html) · [原尺寸源图及实际内置生图提示词](M08-source-turnaround-20261022-r5.zip)。\n\nR4不再作为当前身形锚。新图为按要求修正的二维设定，隐面、精确投影、模型和运行另行核对。接续原design-followthrough-r1.json及ART-M08-TURNAROUND-PROPORTION-R5缺陷。以下为此前各轮与当时状态。\n\n'+plan
if (OUT/'aircraft-airframe-production-r6.json').exists():
    plan='# 当前：歌翼比例作锚，航空结构线修订R6 · 2026-10-23\n\n用户指出雷翎R5过瘦过长，明确歌翼三视比例正确、两机整体形态不错。已按此保留主形，雷翎体态直接参照歌翼；两机简化肩/腿装饰切面，增强进气道、机壳蒙皮、翼根和发动机舱。[两机正侧背与同页体态对照](aircraft-airframe-r6.html) · [原图和实际内置生图提示词包](aircraft-airframe-source-20261023-r6.zip)。\n\nR4偏敦实和R5过细长的比例不再反向套用。接续原缺陷台账，改变比例来源与表面构造方法；原歌翼R4采用范围保持，新R6表面/三视仍为派生源稿，未改人物或运行。以下保留此前各轮与当时状态。\n\n'+plan
if (OUT/'public-works-source-production-r1.json').exists():
    plan='# 当前：已确定设计集中交付，下一批城市职业机首稿 · 2026-10-23\n\n已按用户授权向「战斗主玩法打磨」发送[已确定设计与逐文件清单](confirmed-design-handoff-20261023.html)。R6雷翎/歌翼当前六张源设计已采用，CML141/CML142与CML023参考已登记；集中包包含此前已确定来源，授权派生与父源另有标记。发送记录不代签接入或运行。\n\n下一批按原M06/M07接续，已绘制[预算二号与市政吊装机首轮源稿](public-works-source-r1.html)：预算二号沿黄绿工具机细化快拆工具/替换件，吊装机沿吊臂/履带/稳定腿细化作业和收拢态。[源图与实际内置生图提示词](public-works-source-20261023-r1.zip)。两张新稿为Candidate，未再次交付作已定资产或修改主模型。原台账继续，以下保留此前各轮与当时状态。\n\n'+plan
if (OUT/'M06-labor-identity-production-r2.json').exists():
    plan='# 当前：预算二号职业机语言 R2 · 2026-10-23\n\n用户否定R1的头部美观与机设特色。本轮核实工务机动队的Patlabor投射与预算二号低费维修/供能职责，以已定C03“三代旧电路”行动重画[整机、头部三方向与供能背架](M06-labor-identity-r2.html)。A为整机采用的研究头型；B/C为备选，具体新设计尚未获用户采用。保留原黄绿、替换腿侧别与正常体态；市政吊装机和此前已确定资产沿原来源。\n\n[源图与内置生图提示词包](M06-labor-identity-source-20261023-r2.zip)。本轮不增加剧情/数值规则，不作为已定设计发给主对话；后续沿采用方向补多视与实际工作动作。\n\n'+plan
if (OUT/'M06-design-fixed-20261023-r2.json').exists():
    plan=plan.replace('A为整机采用的研究头型；B/C为备选，具体新设计尚未获用户采用。','用户以“行就这样”采用R2整机与A作业盔头型；[采用范围](M06-design-fixed-20261023-r2.json)已绑定原图及哈希，B/C保留未采用研究。通讯侧别在同头三视中统一。',1)
    plan=plan.replace('本轮不增加剧情/数值规则，不作为已定设计发给主对话；后续沿采用方向补多视与实际工作动作。','本轮只登记源设计采用；后续沿已定A头型与整机补多视，机构、实际工作动作和运行另验。',1)
if (OUT/'M06-turnaround-production-r3.json').exists():
    plan='# 当前：预算二号正侧背三视源图 · 2026-10-23\n\n按用户“直接做三视图啊”，沿已定R2整机/A头型完成[正面、修正左侧面、背面](M06-turnaround-r3.html)。三张为独立原尺寸源图，保留母稿身形与头部体积，右耳通讯模块、左小腿替换件、左手救援夹具及卷盘/三制式背架按侧别对应。首侧稿斜角已重绘，并局部核卷盘轴向和工具侧厚。\n\n[三视源图与内置生图提示词](M06-turnaround-source-20261023-r3.zip)。R2整机/A头型的采用记录保持；新三视按授权派生，模型/机构/动作/运行另验。\n\n'+plan
if (OUT/'city-response-source-production-r2.json').exists():
    plan='# 当前：灰崎曲面职业机 / 消防工程变形机 · 2026-10-23\n\n预算二号当前三视已由用户“没问题，下一批”采用，[指定文件与范围](M06-turnaround-design-fixed-20261023-r3.json)已登记至CML143。下一批[灰崎与消防修订源板](city-response-source-r2.html)：灰崎保留用户肯定的头部/配色/身形，改曲面肩胸与四肢；消防撤回被否定的四足主形，按工程变形机重画双足人形、消防架桥车与稳定支腿工作态。\n\n[当前两机原图与内置生图提示词](city-response-source-20261023-r2.zip)。两张新源图未自动采用；用户采用方向后直接补三视。M07市政吊装机原源板保持，多视缺口继续保留在原台账；本批未改主工程模型、规则或运行。\n\n'+plan
if (OUT/'city-response-design-fixed-20261023-r2.json').exists():
    plan=plan.replace('两张新源图未自动采用；用户采用方向后直接补三视。','两张R2父源已由用户“可以，出三视图”采用，登记在CML144/CML145。')
if (OUT/'city-response-turnaround-production-r3.json').exists():
    plan='# 当前：灰崎与消防架桥机 · 六张三视源图 · 2026-10-24\n\n沿已确定R2整机完成[两机正、侧、背](city-response-turnaround-r3.html)，头部、配色与成人身形保持。灰崎核对五面背负加一面手持，后膝/脚跟改为后部结构；消防核对两窗驾驶室、六轮、成对桥板、右腰双罐与左腰卷盘。侧面按初稿实际问题局部收正。\n\n[六张原图与内置生图提示词](city-response-turnaround-source-20261024-r3.zip)。本轮新增为二维派生源图，未代签用户采用或模型/机构/运行；当前台账仍是design-followthrough-r1.json，M07缺口保持。\n\n'+plan
if (OUT/'city-response-refinement-production-r4.json').exists():
    plan='# 当前：灰崎头身修正 / 消防载具与变形图 · 2026-10-24\n\n用户指出灰崎R3正面矮胖且头型偏离指定R2母稿；[R4修正三视](city-response-refinement-r4.html#M09)从母稿重新推正面，再局部等比缩小头部、收肩并同步侧背。保持原腿长与曲面职业机语言，五背负加一手持重新清点。新增图未代签用户通过。\n\n消防当前人形按“问题不大”保留原三张；补[载具三视与六步变形图](city-response-refinement-r4.html#M10-vehicle)，说明头仓/手臂工具柜/三轴轮组/双桥包/消防水路/稳定支腿的对应。[原图与内置生图提示词](city-response-refinement-source-20261024-r4.zip)。中间动作仍为设计提案，净空、连续运动与承重未由同件机构验证。既有R2父源、其他已定机体与主工程运行保持。\n\n'+plan
if (OUT/'crane-mirror-source-production-r1.json').exists():
    plan='# 当前：市政吊装机三视 / 镜星源设计试案 · 2026-10-24\n\n灰崎/消防最新8张源图已按用户要求[发送主对话](city-response-main-handoff-20261024.json)，不推定接收方已接入或运行验收。下一批[市政吊装机与镜星](crane-mirror-source-r1.html)：吊装沿R1b主形补收拢行驶态正侧背；镜星保留菱形独眼/紫白，棱镜改为有机械连接与收纳位的干扰设备。\n\n镜星暂以雷翎R6的航空机架组织做共架试案；当前C02 Reader没有直接锁定其母体，不据此改Canon或雷翎源图。[四张原图与内置生图提示词](crane-mirror-source-20261024-r1.zip)。新稿留本会话看方向；机构、模型、动作和运行另验，当前台账仍为design-followthrough-r1.json。\n\n'+plan
(OUT/'美术接收与升级计划.md').write_text(plan)
direction_html=(OUT/'direction-revision-section.html').read_text()
if (OUT/'design-followthrough-section.html').exists():
    direction_html=direction_html.replace('<details class="direction-detail">',(OUT/'design-followthrough-section.html').read_text()+'\n<details class="direction-detail">',1)


sample_defs=[
 ('H03','七海 · 对话立绘','H03-qihai-dialogue-v1.png','保留成年脸、短发与白/藏蓝/酒红。将说明稿清成独立人物；头像与表情由这张脸继续派生。','形象方向已确认 · 导出与运行分别验收'),
 ('M01','无牌一号 · 独立造型v3','M01-independent-master-v3.png','旧稿整体近似仍需修正；v3待补足有特色的头冠/胸甲。V形、分叉与耳侧天线可按机体采用，不能一概去特色。','v3仍待修订 · 补足独立且鲜明的头冠/胸部特征'),
 ('E01','啮线体 · 敌体颜色试样','E01-cable-biter-master-v1.png','保留咬切器和机械甲虫；试用靛紫壳与珊瑚刃，靠轮廓和材质分区形成威胁。','配色候选 · 不代表全体敌人改紫色'),
 ('B01','避难楼 · 六层近未来住宅','B01-refuge-habitat-master-v1.png','封闭屋顶、厚楼板、转角窗与公共入口。用近未来住宅结构取代小屋比例，减少发光管装饰。','建筑源稿 · 下一步是低模与UV贴图')
]
sample_html=''
for id,title,file,why,scope in sample_defs:
    r=by_id[id]
    sample_html+=f'''<article class="sample" id="sample-{id}"><div class="sample-head"><span>{id}</span><h3>{title}</h3></div><p>{why}</p><div class="pair"><figure><a href="{esc(rel(ROOT/r['image']))}"><img src="{esc(rel(ROOT/r['image']))}" alt="{title}外援来源图" loading="lazy"></a><figcaption>{"旧造型来源 · 用户已否定作为升级母版" if id=="M01" else "外援来源 · 保留已成立设计"}</figcaption></figure><figure class="cutout"><a href="samples/{file}"><img src="samples/{file}" alt="{title}内部样例" loading="lazy"></a><figcaption>内部样例 · {scope}</figcaption></figure></div><p class="note">{scope}。<a href="../../review-v2.html#{id}">查看该项具体采用与修订意见</a></p></article>'''

gallery=[]
for r in records:
    route=r['route'];issues=' '.join(r['issue_tags']);targets=''.join(f'<li><code>{esc(x)}</code></li>' for x in r['current_assets']) or '<li>按原派单的图形/场景/动作位置接入</li>'
    loaders=''.join(f'<li><code>{esc(x)}</code></li>' for x in r['loaders'])
    history = f'<p><b>前轮具体诊断（同图时仍可作为修订依据，关联新稿以r4为准）：</b>{esc(r["prior_specific_issue"])}</p><p>{esc(r["prior_specific_next"])}</p>' if not r['fresh_opinion'] and previous[r['id']]['verdict']!='A' else ''
    if r['identity_direction_accepted']:
        history += f'<p class="identity-accepted">本对象已认可的身份母稿：<a href="{esc(rel(PROJECT/r["identity_accepted_reference"]))}">打开实际获认可图</a>。{esc(r["identity_acceptance_scope"])} 上方外援图不因编号相同而自动获形象认可。</p>'

    gallery.append(f'''<details class="asset" id="asset-{r['id']}" data-route="{route}" data-group="{r['group']}" data-changed="{str(r['changed_image']).lower()}" data-search="{esc(' '.join([r['id'],r['name'],r['retained'],r['internal_next'],issues]))}"><summary><span class="asset-id">{r['id']}</span><b>{esc(r['name'])}</b><span class="pill route-{route}">{LABELS[route]}</span>{'<small>换图复核</small>' if r['changed_image'] else ''}</summary><div class="asset-body"><a href="{esc(rel(ROOT/r['image']))}"><img src="{esc(rel(ROOT/r['image']))}" loading="lazy" alt="{r['id']} 当前图"></a><div><h4>采用什么</h4><p>{esc(r['retained'])}</p><h4>内部怎样做</h4><p>{esc(r['internal_next'])}</p><p class="note">{esc(r['current_issue'])}</p>{history}<details><summary>原接入映射与目标位置</summary><ul class="paths">{targets}{loaders}</ul><p class="hash">源图 SHA-256 {r['sha256']}</p></details><p><a href="../../review-v2.html#{r['id']}">原页意见及历史</a></p></div></div></details>''')

styles='''
:root{--bg:#f1eee4;--paper:#fbf8ef;--ink:#172f3e;--muted:#516775;--line:#d1d7d2;--teal:#187a82;--coral:#d85f4c;--gold:#b68b2d;--blue:#4b5d8e}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.8 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}a{color:#176c7c;text-underline-offset:3px}img{display:block;max-width:100%}button,input,select{font:inherit}button{cursor:pointer}header.hero{max-width:1320px;margin:auto;padding:52px 32px 30px}.kicker{text-transform:uppercase;letter-spacing:.12em;font-size:12px;color:var(--teal);font-weight:750}h1{font-size:clamp(32px,4.8vw,62px);line-height:1.18;letter-spacing:-.04em;max-width:970px;margin:18px 0 24px}h2{font-size:clamp(25px,3vw,36px);line-height:1.35;margin:0 0 16px}h3{font-size:22px;line-height:1.4}h4{font-size:14px;margin:12px 0 2px;color:var(--teal)}p{margin:10px 0}.lead{font-size:20px;line-height:1.8;max-width:1000px}.note{font-size:13px;line-height:1.8;color:var(--muted)}.hero-links{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}.hero-links a,.action{padding:9px 16px;border:1px solid #9db6b7;border-radius:4px;background:var(--paper);text-decoration:none;font-weight:650}.hero-links a:first-child{background:var(--teal);color:#fff;border-color:var(--teal)}nav.toc{position:sticky;top:0;z-index:10;background:rgba(241,238,228,.97);border-block:1px solid var(--line);display:flex;gap:20px;flex-wrap:wrap;padding:12px max(24px,calc((100vw - 1256px)/2));font-size:14px}nav a{text-decoration:none}main{max-width:1320px;margin:auto;padding:0 32px 64px}section{padding:40px 0;border-bottom:1px solid var(--line)}.steps,.decision-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.decision{border-left:4px solid var(--teal);padding:12px 20px;background:var(--paper)}.decision h3{margin:0 0 6px;font-size:19px}.decision small{font-weight:700;color:var(--teal)}.sample{margin:28px 0 38px;padding:24px;background:var(--paper);border-radius:8px}.sample-head{display:flex;gap:14px;align-items:center}.sample-head span{font:700 15px/1 ui-monospace,monospace;color:var(--teal)}.sample-head h3{margin:0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}.pair figure{margin:0;background:#e6e4db;border-radius:5px;overflow:hidden}.pair figure>a{height:430px;display:flex;align-items:center;justify-content:center}.pair img{width:100%;height:100%;object-fit:contain}.pair .cutout{background:#dfe3dd}.pair figcaption{padding:10px 14px;background:#eef0e8;font-size:13px}.scene img{width:100%;border-radius:5px}.scene figcaption{font-size:13px;color:var(--muted);padding:12px 0}.scene{margin:20px 0}.scene-toggle{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}.scene-toggle button{padding:8px 15px;border:1px solid #a3b8b7;background:var(--paper);color:var(--ink);border-radius:4px}.scene-toggle button[aria-pressed=true]{background:var(--teal);color:white}.scene-view[hidden]{display:none}.scope{padding:14px 18px;background:#e4ebe7;border-left:4px solid var(--teal);font-size:14px}.caution{background:#f4e7cc;border-left-color:#b68b2d}.bullets{padding-left:22px}.poster{position:relative;isolation:isolate;aspect-ratio:16/9;overflow:hidden;background:#132f41;border-radius:7px;color:#f8edd4}.poster .stripe{position:absolute;left:-10%;top:20%;width:120%;height:25%;background:#f0b545;transform:rotate(-21deg);z-index:-1}.poster .coral{position:absolute;right:-8%;bottom:-30%;width:56%;height:80%;background:#da654f;transform:rotate(-16deg);z-index:-1}.poster .dots{position:absolute;left:4%;bottom:7%;width:27%;height:25%;background-image:radial-gradient(#ebdabc 2px,transparent 2px);background-size:16px 16px;opacity:.6;z-index:-1}.poster .ring{position:absolute;width:32%;aspect-ratio:1;border:18px solid #208a93;left:38%;top:12%;border-radius:50%;z-index:-1}.poster img{position:absolute;right:1%;bottom:-6%;height:108%;width:60%;object-fit:contain;filter:drop-shadow(8px 9px 0 #142b3f)}.poster-copy{position:absolute;left:6%;top:13%;width:45%;z-index:2}.poster-copy small{display:block;letter-spacing:.2em;font-size:clamp(9px,1.3vw,15px);color:#172f3e;font-weight:800}.poster h3{font-size:clamp(32px,6.5vw,90px);font-weight:900;margin:70px 0 2px;line-height:1;letter-spacing:-.08em;transform:skew(-6deg);text-shadow:4px 4px 0 #163644}.poster p{font-size:clamp(11px,1.5vw,20px);margin:16px 0}.poster .tag{display:inline-block;background:#f0e4c8;color:#173341;padding:3px 12px;font-size:12px;font-weight:700;letter-spacing:.1em}.poster.play img{animation:poster-unit 1.2s both}.poster.play .stripe{animation:poster-band .8s both}.poster.play .ring{animation:poster-ring 1.2s both}.poster.play h3{animation:poster-title .8s both}@keyframes poster-unit{from{transform:translate(35px,30px) scale(.94);opacity:0}40%{opacity:1}to{transform:translate(0,0) scale(1);opacity:1}}@keyframes poster-band{from{transform:translateX(-140px) rotate(-21deg)}to{transform:translateX(0) rotate(-21deg)}}@keyframes poster-ring{from{transform:scale(.65);opacity:0}to{transform:scale(1);opacity:1}}@keyframes poster-title{from{transform:translateX(-40px) skew(-6deg);opacity:0}to{transform:translateX(0) skew(-6deg);opacity:1}}.pipeline{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin:24px 0}.pipeline div{padding:17px 15px;border-top:4px solid var(--teal);background:var(--paper)}.pipeline b{display:block;font-size:17px}.pipeline small{font-size:12px;line-height:1.6;display:block;color:var(--muted)}.phase{background:var(--paper);padding:20px 24px;margin:15px 0;border-radius:6px}.phase h3{margin:0 0 8px;font-size:20px}.phase .deliver{padding-top:10px;margin-top:10px;border-top:1px solid var(--line);font-size:14px}.sample-checks{width:100%;border-collapse:collapse;margin:20px 0;font-size:14px}.sample-checks td,.sample-checks th{text-align:left;vertical-align:top;padding:13px;border-bottom:1px solid var(--line)}.sample-checks th{background:#e5ebe5}.controls{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0}.controls input{flex:1;min-width:180px}.controls input,.controls select{padding:9px 11px;background:var(--paper);border:1px solid #a2b5b5;border-radius:4px;color:var(--ink)}.asset{border-bottom:1px solid #cbd5d0;padding:3px 0}.asset>summary{display:flex;gap:12px;align-items:center;padding:14px 4px;cursor:pointer;list-style:none;flex-wrap:wrap}.asset>summary::before{content:'+';font-weight:800;color:var(--teal);width:14px}.asset[open]>summary::before{content:'−'}.asset-id{font:700 14px ui-monospace,monospace;width:40px}.asset>summary>b{min-width:190px;flex:1}.asset>summary>small{font-size:11px;color:var(--coral)}.pill{font-size:12px;border-radius:3px;padding:3px 8px;background:#e5e8df}.route-D{background:#dceadd;color:#285c41}.route-M{background:#dce8eb;color:#235569}.route-R{background:#f1e5cc;color:#77531e}.route-V{background:#e3e1f0;color:#594a7b}.asset-body{display:grid;grid-template-columns:minmax(180px,.75fr) 1.25fr;gap:24px;padding:8px 16px 25px}.asset-body>a>img{width:100%;height:auto}.asset-body p{font-size:14px}.asset-body details{font-size:12px;color:var(--muted)}.paths{padding-left:18px;overflow-wrap:anywhere}.paths code{font-size:11px}.hash{font-size:10px;overflow-wrap:anywhere}.asset[hidden]{display:none}footer{font-size:12px;color:var(--muted);max-width:1260px;margin:auto;padding:24px 0 50px}.swatches{display:flex;gap:6px;margin:12px 0}.swatches i{width:40px;height:16px;border-radius:2px;display:block}.table-wrap{overflow:auto}
@media(max-width:760px){header.hero{padding:32px 20px 24px}main{padding:0 20px 40px}.lead{font-size:17px}nav.toc{gap:12px;padding:10px 20px}.decision-grid,.steps,.pair,.asset-body{grid-template-columns:1fr}.sample{padding:16px}.pair figure>a{height:350px}.pipeline{grid-template-columns:1fr 1fr}.poster h3{margin-top:30px}.poster .ring{border-width:8px}.poster .tag{font-size:9px}.asset>summary>b{min-width:120px}.asset>summary .pill{font-size:11px}.sample-checks{font-size:12px}.sample-checks td,.sample-checks th{padding:8px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.poster.play *{animation:none!important}}
@media print{nav.toc,.controls,.scene-toggle,.action{display:none}body{background:white}.asset:not([open]){display:none}.pair figure>a{height:350px}section{break-inside:auto}.sample,.phase{break-inside:avoid}.poster *{animation:none!important}}
'''
styles += '\n.identity-accepted{padding:9px 12px;background:#dce9dc;border-left:4px solid #4a7853;font-size:13px;font-weight:650;color:#2a5038}.direction-refs{display:grid;gap:16px;margin:20px 0;align-items:start}.direction-refs.three{grid-template-columns:repeat(3,minmax(0,1fr))}.direction-refs.two{grid-template-columns:repeat(2,minmax(0,1fr))}.direction-ref{margin:0;background:#e2e5dd;border:1px solid #cbd5cd;border-radius:6px;overflow:hidden}.direction-ref>a{display:block;position:relative}.direction-ref img{width:100%;height:auto;object-fit:contain}.direction-ref.identity img{height:370px;padding:12px}.direction-ref figcaption{padding:13px;background:#f8f5eb;font-size:13px;line-height:1.75}.direction-ref figcaption p{margin:6px 0}.direction-copy{padding:5px 20px;font-size:15px}.direction-copy ol{padding-left:23px}.direction-copy li{margin:10px 0}.direction-detail>summary{cursor:pointer;color:#176c7c;font-size:14px;font-weight:650}@media(max-width:800px){.direction-refs.three,.direction-refs.two{grid-template-columns:1fr}.direction-ref.identity img{height:330px}}\n'
route_cards=''.join(f'<div class="decision"><small>{counts[k]}项 · 加工去向</small><h3>{v}</h3><p>{NEXT[k]}</p></div>' for k,v in LABELS.items())
current_capture = PROJECT/'artifacts/formulas/production-lab-v1/qa/B16-20261012/continuation-r2/water-terrain-04/00-normal-B.png'
plan_link='美术接收与升级计划.md'
doc=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>外援新版接收与内部美术样例 · 2026.10.16</title><style>{styles}</style></head><body>
<header class="hero"><p class="kicker">超GAG / art direction / 2026.10.16 / r4</p><h1>把这套画风变成<br>我们自己的资产</h1><p class="lead">新版来稿已经足够确定 <b>KINETIC_CEL</b> 的主体画法。接下来保留它画得好的部分，由项目内部统一人物身份、机甲组件与设施功能；配色逐对象决定，关键事件另用少量 Memphis 海报语言。</p><p>三主角及三个配角的R2形象已确认；具体来源与范围见最新R4段。<b>已沿选定11张做本轮修订与补图：原头加载、双格栅背包、列车护套/展开状态及钻机腿足对应；新稿待确认。</b></p><div class="hero-links"><a href="brave-components-r8.html#redraw-r12">看本轮修订与部件对应图</a><a href="#brave-front-fins-r7">已确认整机</a><a href="../../review-v2.html#latest-review-r4">看原页最新评审</a><a href="{plan_link}">完整升级计划</a><a href="adoption-manifest.csv">下载298项接收清单</a></div><p class="note">复核43项换图；255项与上一轮逐字节相同。原工程及既有工作保留；三主角确认形象方向，其余模型、派生和运行验收分别记录。</p></header>
<nav class="toc" aria-label="页内目录"><a href="#brave-components-r8">四机图组</a><a href="#brave-front-fins-r7">正面补翼</a><a href="#design-followthrough-20261017">本轮设计</a><a href="#direction-20261016">最新人物/合体决定</a><a href="#adopt">怎样采用</a><a href="#samples">四类样例</a><a href="#tactics">正常镜头</a><a href="#impact">事件海报</a><a href="#plan">升级顺序</a><a href="#inventory">298项去向</a></nav><main>
{direction_html}
<section id="adopt"><h2>按用途接收，具体设计由内部收敛</h2><p>最新改稿已经解决了一批实质问题：合体里保留完整核心、王者右钻左盾和肩炮方向、贯穿/失锁图形等。需要继续处理的是跨图换头换甲、武器缺少冗余、颜色混成一组，以及建筑/界面画法跳档。</p><div class="decision-grid">{route_cards}</div><p class="scope"><b>先校正两个挂反的文件：</b>M03文件实际画七海，S11文件实际画馆守。原页预览与本清单已按图义换回，原来稿不改名、不覆盖。各图文字自称“锁定/通过”均不作为项目事实。</p><p class="note">“可采用”指设计或原画的用途成立。外援交付为方向图，二维导出、三维生产、界面实现和实机检查分别完成，不能把298张方向图算成298件运行资产。</p></section>
<section id="samples"><p class="scope caution"><b>用户最新修订：</b>旧无牌太像高达，旧头胸母版停用。下方已换成独立造型v3候选；旧拳击事件图、场景稿及旧缩小检查中的无牌均仅留历史，尚未按新造型更新。</p><h2>先看四个对象，确认同一绘制水平</h2><p>保留不同机体与人物自己的识别点。统一墨线、色块和阴影的控制；环境依据自己的材质配色。</p>{sample_html}<p class="scope">前轮四张源图做过浅底透明合成检查（其中旧无牌已停作母版；新稿检查另见下方）：<a href="alpha-check.jpg">查看透明检查</a> · <a href="small-scale-check.jpg">查看80/100/140px缩小辨识</a> · <a href="M01-independent-check-v3.jpg">新无牌透明与缩小检查</a>。原输出和全部提示词已保存。它们是本轮内部候选，不会自动覆盖已有正式资源。</p></section>
<section id="tactics"><p class="scope caution"><b>主体造型待更新：</b>这里两张构图包含已被否定的旧无牌，仅保留环境分色与体量诊断。不得继续用其中的机体作为制作母版。</p><h2>正常镜头里，机甲、敌体与楼房要站得住</h2><p>沿现有B面渠岸与桥座构图试画同一套画法。第一稿的无牌太小，第二稿将其放大，敌体保留有威胁的体量；楼房保持六层现代住宅，地面、渠岸、轨槽和楼体有可读的结构层次。</p><div class="scene-toggle" role="group" aria-label="构图对照"><button type="button" data-scene="target" aria-pressed="true">内部构图目标稿</button><button type="button" data-scene="current" aria-pressed="false">现有工程留存截图</button><button type="button" data-scene="first" aria-pressed="false">第一稿：机体偏小</button></div>
<figure class="scene scene-view" data-view="target"><a href="samples/tactics-lookdev-v2.png"><img src="samples/tactics-lookdev-v2.png" alt="比例修订后的正常镜头美术目标稿"></a><figcaption>生图目标稿：暖灰地坪、蓝绿水体、靛紫敌体、白青金主角、砂灰住宅。尺寸按战棋视觉档位组织。</figcaption></figure><figure class="scene scene-view" data-view="current" hidden><img src="{esc(rel(current_capture))}" alt="20261016 B16-R2现有工程留存截图"><figcaption>当日B16-R2留存截图，未因本轮样例而改变。用于比较现有材质、颜色与单位分量。</figcaption></figure><figure class="scene scene-view" data-view="first" hidden><img src="samples/tactics-lookdev-v1.png" alt="第一稿机体比例偏小"><figcaption>第一稿：主角相对六层楼偏小，已在上面的目标稿修正；保留作判断依据。</figcaption></figure>
<p class="scope caution"><b>这张是美术目标插画，尚未进入Godot。</b>它不能证明格子占用、可走路径、深度遮挡或机体动作已经正确。实际制作仍采用低模、UV贴图和共享动作，不能退回二维站牌。</p><ul class="bullets"><li>人物、机体、敌体、建筑各保留自己的色系；四类对象的制作精度与线条控制要协调。</li><li>建筑窗栏仍偏细，转低模时需要收敛；不能将细节密度当科幻感。</li><li>普通敌体不再按“宠物体积”缩放；放大后必须同时检查实际占格、地图密度和可选中区域。</li></ul></section>
<section id="impact"><p class="scope"><a href="#direction-20261016">最新：三主角形象已确认；社勇王改为V19比例、V17巨拳重量；炮筒图源疑似V20待核对，查看计划与参考。</a></p><p class="scope caution"><b>历史版式：</b>下方身体仍是被否定的旧无牌。图形/排版节奏可参考，主体须在独立造型确认后重做。</p><h2>Memphis放在事件峰值里</h2><p>用同一套无牌身体做上冲拳事件图，背景斜带、圆环、点阵和真实中文排版单独制作。主体保持自己的装甲与颜色；图形短暂进入、停住、退出，不把正常棋盘变成海报。</p><div class="poster" id="event-poster"><div class="stripe"></div><div class="coral"></div><div class="dots"></div><div class="ring"></div><img src="samples/M01-rising-punch-event-v1.png" alt="无牌一号同源天冲拳事件插画"><div class="poster-copy"><small>UNLICENSED ONE / SIGNATURE MOVE</small><h3>天冲拳</h3><p>把力量，送到上面。</p><span class="tag">事件海报 · 动效样例</span></div></div><p><button class="action" id="play-poster" type="button">播放1.2秒版式动效</button></p><p class="note">这是插画+图形层的平移、缩放与淡入演示；支持减少动态效果偏好，没有声轨。它没有替代骨架动作、命中、目标受击和声音制作。文案仅为版式样例，不写入剧情。</p></section>
<section id="plan"><h2>从样例确认，接到真实模型和体验</h2><div class="pipeline" role="img" aria-label="母版，结构，低模贴图，共享动作事件，正常镜头验收五步"><div><b>01 母版</b><small>身份、色块、形态与来源</small></div><div><b>02 结构</b><small>正侧背、组件、状态</small></div><div><b>03 低模与贴图</b><small>必要体积、UV、材质</small></div><div><b>04 动作与事件</b><small>共用动作族、特技、响应</small></div><div><b>05 实际体验</b><small>正常镜头、输入、连续演出、声音</small></div></div>
<div class="phase"><h3>继续确认机体与转绘样例</h3><p>三主角及三个配角的形象已确认；配角R3完成小幅调色候选。接下来重点检查重要机体识别性、社勇王R4分件、馆守画风转换，以及敌体、建筑与事件海报用量。颜色与具体设计可以单独修，不自动扩成对全包素材的认可。</p><p class="deliver">当前交付：四张主体源图、天冲拳事件图、正常镜头目标稿、298项采用清单和逐项修订意见。正式资源尚未覆盖。</p></div>
<div class="phase"><h3>一、人物与机体母版先锁定</h3><p>M01—M15、H01—H12、E01—E11。六名人物沿确认形象派生，三个配角R2已过、R3只调配色；馆守优先转绘原形象。无牌补足独立特征；社勇王按V19比例、V17上覆与巨拳重量、V18胸腿和V11长发核心整合；列车炮按明确展开要求制作，疑似V20版本待核对；旧拳王保留厚拳架；王者把早期武器冗余补回新版正确挂点。馆守按已有身份母版和右臂毁损事实制作，合体固定完整核心。头像从母版头肩派生，人物统一眼线与对话比例。</p><p class="deliver">交付：可追溯母版、身份锚、结构视图、头像/立绘与状态候选。用户确认与制作检查分别记录。</p></div>
<div class="phase"><h3>二、部件、建筑与地面按图做低模</h3><p>F01—F18、B01—B34、T01—T16。车辆/飞机/合体用同一套组件；住宅、供电柜、桥座、列车、泵站保留功能轮廓。地面的沟槽、渠岸、断面与屋顶有合理几何，材质贴图负责补足表面表现。</p><p class="deliver">先接入B面“看见桥座威胁→推开/托桥→列车通过”的完整体验，再推广A/C与全量对象。必须用实际正常镜头、转动视角与加载位置证明变化。</p></div>
<div class="phase"><h3>三、动作复用，状态与后果由事件驱动</h3><p>N01—N14提供动作思路，X01—X30/C01—C16提供反馈语言。走跑、飞行、射击、操作、受击使用动作族适配，天冲拳等有身份价值的体术再定制。攻击事件让每个目标处理自己的受击，不做逐对接触参数；机柜只需合理手部动作与状态响应。</p><p class="deliver">连续动画、弹道/爆炸/位移、环境与目标响应、声音一起检查。预演、执行、回放与HUD读同一结果。</p></div>
<div class="phase"><h3>四、把图形与剧情图接回操作语言</h3><p>G01—G25、U01—U20、I01—I65、S01—S21。光标探索、选中范围、目标轨迹、预计耐久、位移落点与碰撞按需显示；标准高度光墙使用世界空间深度遮挡。纪存/白鸢/七海职能分别表达，真实文字和数字单独排版，名场面少量使用海报层。</p><p class="deliver">在第二种机体、第二类设施和第二战场验证复用后推广；回到原52包/331条台账逐项绑定实现和证据，不另造一份美术完成度。</p></div>
<div class="table-wrap"><table class="sample-checks"><thead><tr><th>检查层</th><th>怎样判断</th><th>当前状态</th></tr></thead><tbody><tr><td>风格与主体</td><td>同一脸、头胸、组件和建筑功能；四类制作水平协调</td><td>六名人物形象来源已确认；衍生/运行与机体结构继续分别检查</td></tr><tr><td>战棋画面</td><td>正常距离的分色、分量、可选中与遮挡</td><td>目标插画已做；运行验收尚未进行</td></tr><tr><td>模型/动作/声音</td><td>真实加载、连续演出、事件后果与实听</td><td>保留原工程；本轮没有冒记为完成</td></tr><tr><td>全量范围</td><td>全部已采纳要求与原台账匹配</td><td>仍沿用52包/331条，未缩减、未关单</td></tr></tbody></table></div><p><a href="{plan_link}">完整制作约定、范围和接入说明</a> · <a href="prompts.json">首批提示词</a> · <a href="prompts-second-pass.json">派生/修订提示词</a> · <a href="prompt-scene-scale.json">比例修订提示词</a> · <a href="M01-independent-prompt-v3.json">无牌独立造型提示词</a></p></section>
<section id="inventory"><h2>298项的具体采用去向</h2><p>搜索编号、对象或用途，展开即可看到可取部分、内部下一步和原工程资源位置。前轮诊断折叠保留；本轮换图项以新意见为准。</p><div class="controls"><input id="asset-search" type="search" placeholder="搜索：M05、七海、桥座、贯穿…" aria-label="搜索素材"><select id="route-filter" aria-label="按采用方式筛选"><option value="ALL">所有采用方式</option>{''.join(f'<option value="{k}">{v}（{counts[k]}）</option>' for k,v in LABELS.items())}</select><select id="changed-filter" aria-label="按是否更新筛选"><option value="ALL">所有版本</option><option value="true">43项换图复核</option></select><span id="asset-count" class="note" aria-live="polite">298 / 298项</span></div>{''.join(gallery)}</section>
<section><h2>本轮边界与来源</h2><p>采用的是外援风格与设计收益，内部样例由内置Imagegen制作。原图、提示词、输出、采用清单和对应代码位置都留在此目录。原资源没有覆盖；无牌头部源设计及最新冠型重选要求已记录在CML133，未改剧情、能力或登场。新整机与新样例仍分别看稿。</p><p class="note">本地文件已做结构、资源存在性和脚本语法检查。先前浏览器工具对该file页面有明确安全拒绝，因此本轮没有绕过；页面实际浏览器布局/交互与游戏原生体验均不冒记为通过。</p></section>
</main><footer>2026.10.16 · 超GAG内部美术候选 / r4 · 原页的r2/r3意见保留历史 · 用户认可单独记录</footer>
<script>
const assets=[...document.querySelectorAll('.asset')],search=document.getElementById('asset-search'),route=document.getElementById('route-filter'),changed=document.getElementById('changed-filter');
function applyAssets(){{const q=search.value.trim().toLowerCase();let n=0;for(const a of assets){{const show=(!q||a.dataset.search.toLowerCase().includes(q))&&(route.value==='ALL'||a.dataset.route===route.value)&&(changed.value==='ALL'||a.dataset.changed===changed.value);a.hidden=!show;if(show)n++;}}document.getElementById('asset-count').textContent=n+' / 298项';}}
[search,route,changed].forEach(e=>e.addEventListener(e===search?'input':'change',applyAssets));
document.querySelectorAll('[data-scene]').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('[data-scene]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('[data-view]').forEach(x=>x.hidden=x.dataset.view!==b.dataset.scene);}}));
let posterTimer;document.getElementById('play-poster').addEventListener('click',()=>{{const p=document.getElementById('event-poster');clearTimeout(posterTimer);p.classList.remove('play');requestAnimationFrame(()=>requestAnimationFrame(()=>{{p.classList.add('play');posterTimer=setTimeout(()=>p.classList.remove('play'),1350);}}));}});
if(location.hash.startsWith('#asset-')){{const el=document.getElementById(location.hash.slice(1));if(el)el.open=true;}}
</script></body></html>'''
if (OUT/'mecha-source-decisions-20261019-r17.json').exists():
    doc=doc.replace('三主角及三个配角的R2形象已确认；具体来源与范围见最新R4段。<b>已沿选定11张做本轮修订与补图：原头加载、双格栅背包、列车护套/展开状态及钻机腿足对应；新稿待确认。</b>','<b>无牌R16头部已确认，旧拳王沿当前样例继续。</b>王者R2只统一线条、块面与明暗，保留原配色和华丽厚重全装；新样例供看稿。社勇王与六名人物的固定设计保持。')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M05-style-match-r2.html">王者画法统一与新旧对照</a><a href="M01-family-head-review-r14.html#head-proportion-r16">已确认无牌头部</a>',1)
    doc=doc.replace('无牌头部源设计及最新冠型重选要求已记录在CML133','无牌R16指定头部源设计已记录在CML133')
if (OUT/'M05-modular-production-r4.json').exists():
    doc=doc.replace('王者R2只统一线条、块面与明暗，保留原配色和华丽厚重全装；新样例供看稿。','王者R4按图四脸及中轴前伸L角重画头部，并分别整理素体、全装和六组配件包；新图供看稿。')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M05-modular-r4.html">王者L角、素体与配件包</a>',1)
if (OUT/'M05-head-upward-L-production-r5.json').exists():
    doc=doc.replace('王者R4按图四脸及中轴前伸L角重画头部，并分别整理素体、全装和六组配件包；新图供看稿。','王者R5按最新纠正改为朝上独角仙式L角；当前头部已重画，R4素体/全装的旧中角待同步。')
if (OUT/'M05-head-riese-production-r6.json').exists():
    doc=doc.replace('王者R5按最新纠正改为朝上独角仙式L角；当前头部已重画，R4素体/全装的旧中角待同步。','王者R6按古铁巨神参考重整角与天线，保留图四脸与原色；R5执行已否定，整机旧角待同步。').replace('王者L角、素体与配件包</a>','王者当前头部、素体与配件包</a>')
if (OUT/'M05-head-design-fixed-20261020.json').exists():
    doc=doc.replace('王者R6按古铁巨神参考重整角与天线，保留图四脸与原色；R5执行已否定，整机旧角待同步。','王者R6b指定头部已选定，CML134固定该原图；R7素体与全装已同步头型，整机新图与运行另记。')
if (OUT/'M05-red-fin-production-r9.json').exists():
    doc=doc.replace('王者R6b指定头部已选定，CML134固定该原图；R7素体与全装已同步头型，整机新图与运行另记。','王者R7源稿与R8战斗面罩已采用；最新追加红色中线鳍，普通脸与面罩共用头盔。')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M05-battle-mask-r8.html">王者双状态与红色头鳍</a>',1)
if (OUT/'M05-turnaround-production-r12.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M05-turnaround-r12.html">王者素体、全装与头部三视</a>',1)
    doc=doc.replace('王者R7源稿与R8战斗面罩已采用；最新追加红色中线鳍，普通脸与面罩共用头盔。','王者R7/R8/R9源设计已采用；按最新反馈恢复整机腿身比例，素体与全装逐面补三视。')
if (OUT/'M02-turnaround-production-r2.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M02-turnaround-r2.html">旧拳王正侧背三视</a>',1)
if (OUT/'M11-cargo-production-r1.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M11-cargo-r1.html">当前下一批：货柜领袖双形态</a><a href="mecha-source-batch-acceptance-20261021.json">旧拳王／王者本批已采用</a>',1)
if (OUT/'M11-future-production-r2.json').exists():
    doc=doc.replace('当前下一批：货柜领袖双形态','货柜领袖R1历史')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M11-future-r2.html">当前：货柜领袖未来双形态R2</a>',1)
if (OUT/'M11-structure-and-head-production-r4.json').exists():
    doc=doc.replace('当前：货柜领袖未来双形态R2','货柜领袖R2历史')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M11-structure-and-head-r4.html">当前：货柜领袖整体盔型与布局</a>',1)
if (OUT/'M11-heroic-antenna-production-r5.json').exists():
    doc=doc.replace('当前：货柜领袖整体盔型与布局','货柜领袖R4历史与布局')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M11-heroic-antenna-r5.html">当前：货柜领袖保留天线与正面头型</a>',1)
if (OUT/'M11-turnaround-structure-production-r7.json').exists():
    doc=doc.replace('当前：货柜领袖保留天线与正面头型','货柜领袖R5头稿历史')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M11-turnaround-structure-r7.html">当前：货柜领袖三视与可变结构</a>',1)
if (OUT/'M11-posture-production-r8.json').exists():
    doc=doc.replace('当前：货柜领袖三视与可变结构','上一轮：货柜领袖三视与可变结构')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M11-turnaround-structure-r7.html#posture-r8">当前：货柜领袖肩颈体态修正</a>',1)
if decisions.get('guardian_policy',{}).get('reuse_existing'):
    for old,new in [('馆守优先转绘原形象','馆守沿用现有资产，不重做'),('馆守画风转换','馆守沿用现有'),('馆守仍沿原身份转绘','馆守沿用现有，不重做')]:
        doc=doc.replace(old,new)
if (OUT/'M11-turnaround-delivery-production-r9.json').exists():
    doc=doc.replace('当前：货柜领袖肩颈体态修正','货柜领袖R8母稿')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M11-source-delivery-r9.html">货柜领袖形象确定与三视交付</a>',1)
if (OUT/'aircraft-source-batch-20261022.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="aircraft-source-batch-20261022.html">下一批：雷翎与歌翼双态候选</a>',1)
if (OUT/'aircraft-runtime-comparison-20261022.json').exists():
    doc=doc.replace('下一批：雷翎与歌翼双态候选','雷翎与歌翼：此前结构研究稿')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="aircraft-runtime-comparison-20261022.html">当前：现用机设与新稿对照</a>',1)
if (OUT/'aircraft-existing-design-recolour-production-r2.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="aircraft-existing-design-recolour-r2.html">当前：雷翎与歌翼配色修订</a>',1)
if (OUT/'aircraft-synthesis-production-r3.json').exists():
    doc=doc.replace('当前：雷翎与歌翼配色修订','R2回退换色稿（历史）')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="aircraft-synthesis-r3.html">当前：雷翎与歌翼综合设计R3</a>',1)
if (OUT/'M14-music-support-production-r4.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M14-music-support-r4.html">当前：歌翼音乐传播模块R4</a>',1)
if (OUT/'M14-turnaround-production-r5.json').exists():
    doc=doc.replace('当前：歌翼音乐传播模块R4','歌翼R4已采用母稿')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M14-turnaround-r5.html">当前：歌翼音乐传播版三视R5</a>',1)
if (OUT/'M08-turnaround-production-r4.json').exists():
    doc=doc.replace('当前：歌翼音乐传播版三视R5','歌翼音乐传播版三视R5')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M08-turnaround-r4.html">当前：雷翎正侧背三视R4</a>',1)
if (OUT/'M08-turnaround-production-r5.json').exists():
    doc=doc.replace('当前：雷翎正侧背三视R4','雷翎R4历史三视（比例已退出）')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M08-turnaround-r5.html">当前：雷翎修长身形三视R5</a>',1)
if (OUT/'aircraft-airframe-production-r6.json').exists():
    doc=doc.replace('当前：雷翎修长身形三视R5','雷翎R5历史（比例过瘦）')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="aircraft-airframe-r6.html">当前：两机航空结构线与三视R6</a>',1)
if (OUT/'public-works-source-production-r1.json').exists():
    doc=doc.replace('当前：两机航空结构线与三视R6','已确定：雷翎/歌翼三视R6')
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="public-works-source-r1.html">当前：预算二号与市政吊装机首稿</a><a href="confirmed-design-handoff-20261023.html">已确定设计集中交付</a>',1)
if (OUT/'M06-labor-identity-production-r2.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M06-labor-identity-r2.html">最新：预算二号职业机语言与头部 R2</a>',1)
if (OUT/'M06-turnaround-production-r3.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="M06-turnaround-r3.html">最新：预算二号正侧背三视</a>',1)
if (OUT/'city-response-source-production-r2.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="city-response-source-r2.html">最新：灰崎曲面 / 消防工程变形修订</a>',1)
if (OUT/'city-response-turnaround-production-r3.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="city-response-turnaround-r3.html">最新：灰崎与消防架桥机三视图</a>',1)
if (OUT/'city-response-refinement-production-r4.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="city-response-refinement-r4.html">最新：灰崎修正 / 消防载具与变形图</a>',1)
if (OUT/'crane-mirror-source-production-r1.json').exists():
    doc=doc.replace('<div class="hero-links">','<div class="hero-links"><a href="crane-mirror-source-r1.html">最新：吊装机三视 / 镜星共架试案</a>',1)
(OUT/'index.html').write_text(doc)

# Amend the existing reader without discarding artist updates or prior reviews.
source=PAGE.read_text()
backup=OUT/'before-review-r4.html'
state=OUT/'published-state.json'
if 'id="latest-review-r4"' in source:
    if not state.is_file() or sha(PAGE)!=json.loads(state.read_text())['page_sha256']:
        raise SystemExit('Page changed after our publication; inspect current external updates before editing.')
    source=backup.read_text()
else:
    if backup.exists() and source!=backup.read_text():raise SystemExit('Initial backup exists but current page changed; inspect rather than overwrite.')
    if not backup.exists():backup.write_text(source)
source_hash=hashlib.sha256(source.encode()).hexdigest()
assert source_hash=='5b90a84e45109b2fc8fcb6686845ccfe2e33c56b92cd3f805e4f4a2c0d1eccbb', 'New source version detected; re-review before publishing'
cards=re.findall(r'<article\b[^>]*class="card".*?</article>',source,re.S)
assert len(cards)==298
new_cards={}
for c in cards:
    id=re.search(r'data-id="([A-Z]\d+)"',c).group(1);r=by_id[id]
    meta=c.split('<div class="meta">',1)[1].rsplit('</div></article>',1)[0]
    purpose=re.search(r'<p class="purpose">.*?</p>',c,re.S)
    purpose=purpose.group(0) if purpose else ''
    if r['identity_direction_accepted']:
        purpose += f'<p class="r4-note"><b>人物形象认可绑定：</b><a href="{esc(rel(PROJECT/r["identity_accepted_reference"],ROOT))}">实际身份母稿</a>。{esc(r["identity_acceptance_scope"])} 不将当前外援卡片整图当作已认可的新身份。</p>'

    pimg=r['image']; search_text=' '.join([id,r['name'],r['route_label'],r['retained'],r['current_issue'],r['internal_next']])
    prior_issue=f'<p class="r4-note">前轮详细诊断仍收在下方历史记录；关联43项新图的判断以本轮对应项为准。</p>' if not r['fresh_opinion'] else ''
    routeclass={'D':'A','M':'A','R':'B','V':'B'}[r['route']]
    new_cards[id]=f'''<article class="card" data-group="{r['group']}" data-id="{id}" data-status="r4-source-review" data-verdict="{r['route']}" data-user-pref="false" data-changed="{str(r['changed_image']).lower()}" data-issues="{','.join(r['issue_tags'])}" data-current-search="{esc(search_text)}" id="{id}"><a class="thumb" href="{esc(pimg)}" target="_blank" rel="noopener"><img src="{esc(pimg)}" alt="{id} {esc(r['name'])} r4实际对应图" loading="lazy" width="1280" height="720"></a><div class="meta"><div class="row1"><span class="id">{id}</span><span class="source-status">r4 · {'换图复核' if r['changed_image'] else '未换图，沿用来源审查'}</span></div><h3 class="name">{esc(r['name'])}</h3>{purpose}<div class="review-verdict rv-{routeclass}">{r['route_label']}</div><dl class="r3-assessment"><dt>本轮保留什么</dt><dd>{esc(r['retained'])}</dd><dt>当前判断</dt><dd>{esc(r['current_issue'])}</dd><dt>由项目内部怎样完成</dt><dd>{esc(r['internal_next'])}</dd></dl>{prior_issue}<p class="review-links"><a href="review/20261016-internal-upgrade/index.html#asset-{id}">采用清单与加载位置</a> · <a href="../../docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate/外援美术制作清单-20261012/index.html#{id}">原派单要求</a></p><details class="r3-production"><summary>r4实际文件绑定</summary><p>当前对应：<a href="{esc(pimg)}">同一张固定图</a></p><p class="r4-note">{'已按图义校正M03/S11挂反关系。原文件名和内容保留。' if r['binding_corrected'] else '原图字节未改；采用意见不是运行接入或用户认可。'}</p><p class="required-files">SHA-256：{r['sha256']}</p></details><details class="r4-history"><summary>前轮r3/r2图面意见与原规格（历史）</summary><p class="r4-note">历史记录不替代r4当前图义、采用路线和文件绑定。已经被新版解决的问题，不再照旧要求重做。</p>{meta}</details></div></article>'''

def replace_card(m):
    id=re.search(r'data-id="([A-Z]\d+)"',m.group()).group(1)
    return new_cards[id]
source=re.sub(r'<article\b[^>]*class="card".*?</article>',replace_card,source,flags=re.S)
start=source.index('<section class="review-intro r3-intro"')
end=source.index('<main>',start)
history_intro=source[start:end]
fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-alert"><b>最新用户决定：</b>三主角新形象及兜灯/唐胶/胶价王R2形象已确认，后三人只微调配色；馆守仍沿原身份转绘。社勇王整体方向与画法成立，当前R4补V17头、肩翼可动分件、V18感钝机头与膝钻前向。重要机体允许鲜明头冠。社勇王采用V19身高/头身比，V11双拳强化至V17重量，结合V17上覆与V18胸腿；列车拆两节、车头朝后、中段左右打开为臂外炮筒，疑似V20图源未找到，不再错绑V19。<a href="review/20261016-internal-upgrade/index.html#direction-20261016">查看参考与更新方案</a></p><p class="r3-kicker">2026.10.16 · 新版接收r4 · 43项换图复核 / 298项用途清单</p><h2>这批已足够确定方向。接下来由项目内部统一母版，制作升级资产。</h2><p class="r3-lead">保留你接受的KINETIC_CEL绘制水平与机甲、敌体、人物、建筑风格，具体配色和设定逐对象修正。标题与关键事件适量使用Memphis海报层。本轮已经实际制作四张主体样例、正常战棋构图目标和天冲拳事件海报。</p><p class="r3-alert"><b>最新用户决定：</b>旧无牌太像高达，撤回“保留旧头胸”建议，M01改为内部重设；已新增独立造型v3候选。旧天冲拳/场景稿中的无牌只保留历史，待新方向确认后更新。</p><div class="review-jump"><a href="review/20261016-internal-upgrade/index.html#samples">看四类新样例</a><a href="review/20261016-internal-upgrade/index.html#tactics">正常镜头目标</a><a href="review/20261016-internal-upgrade/index.html#impact">事件海报动效</a><a href="review/20261016-internal-upgrade/index.html#plan">升级顺序</a><a href="review/20261016-internal-upgrade/index.html#inventory">298项采用去向</a></div><p><b>新版已改善：</b>完整核心持续保留、王者右钻左盾与肩炮方向、部分航空结构、贯穿/失锁图标、现代城市事件构图。<b>内部继续处理：</b>同一机体跨图换头换甲、王者武器冗余减少、部件颜色不一致、建筑/人物/UI画法跳档。</p><p class="r3-alert"><b>M03/S11内容挂反已校正：</b>原M03文件是七海，原S11文件才是馆守；本页预览和采用清单按实际图义对应，原文件保留。不能根据错误文件名继续审错对象。</p><div class="r3-counts">{''.join(f'<a href="review/20261016-internal-upgrade/index.html#inventory"><b>{counts[k]}</b> {v}</a>' for k,v in LABELS.items())}</div><div class="r4-sample-strip">{''.join(f'<a href="review/20261016-internal-upgrade/index.html#sample-{id}"><img src="review/20261016-internal-upgrade/samples/{file}" alt="{title}内部样例"><span>{title}</span></a>' for id,title,file,why,scope in sample_defs)}</div><p class="readiness-note">这是源图接收与内部升级样例，<b>没有覆盖运行资产或完成52包整改；六名人物的指定形象已由用户确认；派生配色及运行仍分开记录</b>。下一步按最新来源补齐机体/配角样例，六名人物沿确认形象派生；继续原台账的低模/贴图/共享动作/界面和实际体验。</p></section><details class="r4-old-overview"><summary>前轮r3总评与历史对照（已折叠，最新判断看上方）</summary>{history_intro}</details>'''
fresh_intro=fresh_intro.replace('<div class="review-jump">','<p class="r3-alert"><b>10月18日R12修订：</b>已按授权做装配双口背包、面罩状态、列车护套与展开对应、钻机腿足归属等源图修订。原选基准保留，新修订待确认，运行与交接未变。</p><div class="review-jump"><a href="review/20261016-internal-upgrade/brave-components-r8.html#redraw-r12">本轮实际修订与8项对照</a><a href="review/20261016-internal-upgrade/index.html#brave-front-fins-r7">已确认整机</a><a href="review/20261016-internal-upgrade/index.html#baiyuan-hands-repair">白鸢手部修正</a><a href="review/20261016-internal-upgrade/index.html#design-followthrough-20261017">最新设计</a>',1)
if (OUT/'M01-head-directions-production-r5.json').exists():
    fresh_intro=fresh_intro.replace('<b>最新用户决定：</b>','<b>此前来源与决定：</b>')
    fresh_intro=fresh_intro.replace('原选基准保留，新修订待确认，运行与交接未变。','本批设计已固定并集中交接，模型及运行分别验收。')
    fresh_intro=fresh_intro.replace('馆守仍沿原身份转绘','馆守沿用现有，不重做')
    fresh_intro=fresh_intro.replace('<p class="r3-alert">','<p class="r3-alert"><b>10月18日最新：</b>馆守Z沿用现有资产，取消重做。无牌R4长耳冠片已被否定，<a href="review/20261016-internal-upgrade/M01-head-directions-r5.html">六种头部新参考在此比较</a>；尚未选定、不作运行替换。社勇王与六名角色的固定设计保持。</p><p class="r3-alert">',1)
if (OUT/'M01-head-AE-production-r6.json').exists():
    fresh_intro=fresh_intro.replace('<b>10月18日最新：</b>','<b>此前六种探索：</b>')
    fresh_intro=fresh_intro.replace('<p class="r3-alert">','<p class="r3-alert"><b>当前用户选择：</b>无牌按A中央冠脊与E折角侧翼整合，左右对称并拉开与馆守Z的差异。<a href="review/20261016-internal-upgrade/M01-head-AE-r6.html">正面/三分之四新稿与现有馆守对照</a>；具体新绘待看。馆守继续沿用现有，社勇王/人物固定图集保持。</p><p class="r3-alert">',1)
if (OUT/'M01-head-aft-antenna-production-r7.json').exists():
    fresh_intro=fresh_intro.replace('<b>当前用户选择：</b>','<b>此前A+E整合：</b>')
    fresh_intro=fresh_intro.replace('<p class="r3-alert">','<p class="r3-alert"><b>当前R7局部修正：</b>无牌两侧天线取消折角外张，直线朝后、与中央冠脊同向。<a href="review/20261016-internal-upgrade/M01-head-AE-r6.html">查看双视图修正与R6对照</a>；脸型、连续视窗、面甲及配色延续，具体新图待确认。馆守沿用现有。</p><p class="r3-alert">',1)
if (OUT/'M01-head-crest-consistency-production-r8.json').exists():
    fresh_intro=fresh_intro.replace('<b>当前R7局部修正：</b>','<b>此前R7侧天线修正：</b>')
    fresh_intro=fresh_intro.replace('<p class="r3-alert">','<p class="r3-alert"><b>当前R8冠脊修正：</b>R7总体与两侧后向天线的认可保留；按用户指出的问题，以正面为依据局部修正三分之四冠脊的金槽收尖及白色分段。<a href="review/20261016-internal-upgrade/M01-head-AE-r6.html">查看当前R8与R7对照</a>；新局部修正待确认，馆守沿用现有。</p><p class="r3-alert">',1)
if (OUT/'M01-head-center-groove-production-r9.json').exists():
    fresh_intro=fresh_intro.replace('<b>当前R8冠脊修正：</b>','<b>此前R8尝试（凹槽位置仍错）：</b>')
    fresh_intro=fresh_intro.replace('<p class="r3-alert">','<p class="r3-alert"><b>当前R9b中央凹槽修正：</b>R8未解决凹缝从中央跑到侧面的错误，已保留失败记录。现用同一冠体实际投影作参考，独立重绘三分之四的顶槽与白色外壁，正面沿用。<a href="review/20261016-internal-upgrade/M01-head-AE-r6.html">查看当前组合、用户标错图与空间参考</a>；新图待确认，馆守沿用现有。</p><p class="r3-alert">',1)
if (OUT/'M01-head-front-match-production-r10.json').exists():
    fresh_intro=fresh_intro.replace('<b>当前R9b中央凹槽修正：</b>','<b>此前R9b修正（设计已采用）：</b>')
    fresh_intro=fresh_intro.replace('<p class="r3-alert">','<p class="r3-alert"><b>当前R10正面修正：</b>用户已采用R9b所示无牌头部设计，三分之四原稿保持；现按它的冠体修正正面天线/中央凹槽。<a href="review/20261016-internal-upgrade/M01-head-AE-r6.html">查看当前正面与已采用设计</a>；新正面待确认，完整机体和运行另验，馆守沿用现有。</p><p class="r3-alert">',1)
if (OUT/'M01-head-twin-grooves-production-r11.json').exists():
    fresh_intro=fresh_intro.replace('<b>当前R10正面修正：</b>','<b>旧R10尝试（单中槽误读，已作废）：</b>')
    fresh_intro=fresh_intro.replace('<p class="r3-alert">','<p class="r3-alert"><b>当前R11：白中脊、双侧黄槽。</b>用户标线已明确左右各一道槽，中间是白色实体。作者旧单中槽解释及模型参考作废；当前前视按两线修正，已采用侧视不改。<a href="review/20261016-internal-upgrade/M01-head-AE-r6.html">看当前修稿与用户标线</a>。新图待确认，馆守沿用现有。</p><p class="r3-alert">',1)
if (OUT/'M01-turnaround-production-r12.json').exists():
    old_open=fresh_intro.index('>')+1
    old_close=fresh_intro.index('</section>')
    historical_inner=fresh_intro[old_open:old_close]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.19 · 无牌三视图 / 下一批机体样例</p><h2>无牌头部已确认，整机正侧背已补齐。下一批旧拳王与王者已有新图。</h2><p class="r3-lead">无牌保留双侧黄槽、白色中脊和直线后向天线，整机沿原竞技体术轮廓补正侧背。旧拳王统一重肩厚拳，完全版王者恢复右钻左盾、背肩双炮与分层翼的全装备分量。</p><div class="review-jump"><a href="review/20261016-internal-upgrade/M01-turnaround-r12.html">无牌三视图</a><a href="review/20261016-internal-upgrade/next-batch-mecha-20261019.html#old-boxer">旧拳王新样例</a><a href="review/20261016-internal-upgrade/next-batch-mecha-20261019.html#complete-king">王者全装备新样例</a><a href="review/20261016-internal-upgrade/index.html#plan">原升级计划</a></div><div class="r4-sample-strip"><a href="review/20261016-internal-upgrade/M01-turnaround-r12.html"><img src="review/20261016-internal-upgrade/samples/M01-turnaround-r12b.png" alt="无牌整机正侧背"><span>无牌 · 新三视图</span></a><a href="review/20261016-internal-upgrade/next-batch-mecha-20261019.html#old-boxer"><img src="review/20261016-internal-upgrade/samples/M02-old-boxer-master-r1.png" alt="旧拳王新样例"><span>旧拳王 · 新样例</span></a><a href="review/20261016-internal-upgrade/next-batch-mecha-20261019.html#complete-king"><img src="review/20261016-internal-upgrade/samples/M05-full-loadout-r1b.png" alt="完全版王者全装备新样例"><span>完全版王者 · 全装备样例</span></a></div><p class="readiness-note">无牌头部源设计已确认；新整机三视和两张新样例待看。馆守Z沿用现有；社勇王与六名角色固定设计保持。新图尚未替换运行或发送主玩法对话。</p><details class="r4-history"><summary>此前逐轮讨论与源图接收历史（含当时待确认状态）</summary>{historical_inner}</details></section>'''+fresh_intro[old_close+len('</section>'):]
if (OUT/'M01-head-position-production-r14.json').exists():
    current_heads=json.loads((OUT/'M01-head-position-production-r14.json').read_text())
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    choices=''.join(f'<a href="review/20261016-internal-upgrade/M01-family-head-review-r14.html#head-{item["id"]}"><img src="review/20261016-internal-upgrade/{item["file"]}" alt="无牌头冠{item["id"]}：{item["title"]}"><span>{item["id"]} · {item["title"]}</span></a>' for item in current_heads['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.19 · 无牌头冠位置R14 / 同系列整机R13</p><h2>克制的量产无牌，也要有闪光时的主角感。</h2><p class="r3-lead">旧R12整机矮圆且与王者不同系列，已按用户意见重做。R13调整身材和胸肩家族后，头顶天线仍需修改，现已绘制四种主冠位置；作者优先D，B为压短后的备选，尚未替用户选定。</p><div class="review-jump"><a href="review/20261016-internal-upgrade/M01-family-head-review-r14.html#head-options">四个头冠方向与意见</a><a href="review/20261016-internal-upgrade/M01-family-head-review-r14.html#body">同系列整机对照</a><a href="review/20261016-internal-upgrade/index.html#plan">更新升级计划</a></div><div class="r4-sample-strip">{choices}</div><p class="readiness-note">王者保留原系列豪华主角机的臃肿与过武装，无牌保持量产基础体与自身记忆点。旧头冠局部认可按历史保留，新头型重选；馆守Z与社勇王/人物固定批次保持，运行未替换。</p><details class="r4-history"><summary>此前交付与当时认可状态（当前头冠已重新开放）</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M01-synthesis-head-production-r15.json').exists():
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.19 · 无牌综合头型R15</p><h2>中央低额块，方正盔体，高位侧后双天线。</h2><p class="r3-lead">按用户最新提出的天威勇士与擎天柱头型综合，实际查看官方参考后绘制新头肩样例；无牌的青白金、连续琥珀视窗、白面甲和同族颈下保持。新图尚未确认。</p><div class="review-jump"><a href="review/20261016-internal-upgrade/M01-family-head-review-r14.html#synthesis-r15">综合新稿与参考拆解</a><a href="review/20261016-internal-upgrade/index.html#next-design-m01-r15">当前升级计划</a></div><a href="review/20261016-internal-upgrade/M01-family-head-review-r14.html#synthesis-r15"><img src="review/20261016-internal-upgrade/samples/M01-synthesis-head-r15.png" alt="无牌R15综合头型，中央低额块与高位侧后双天线" style="width:100%;max-height:820px;object-fit:contain;background:#dfe5de"></a><p class="readiness-note">具体新头型待看稿；选定后再固定天线体量/倾角、根位和同头多视图。馆守Z及社勇王/人物固定源保持，运行未替换。</p><details class="r4-history"><summary>此前头冠探索与当时状态</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M01-head-proportion-production-r16.json').exists():
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.19 · 无牌头部比例修正R16</p><h2>综合结构保留，补回头壳本体的纵向体积。</h2><p class="r3-lead">用户表示综合方向还行，但头部反复被压扁。此次只修头壳高宽、收紧颞侧与眉沿，保留低额块、侧后双天线、琥珀视窗和白面甲；新修正图尚待看稿。</p><div class="review-jump"><a href="review/20261016-internal-upgrade/M01-family-head-review-r14.html#head-proportion-r16">新稿与前后对照</a><a href="review/20261016-internal-upgrade/index.html#next-design-m01-r16">更新升级计划</a></div><a href="review/20261016-internal-upgrade/M01-family-head-review-r14.html#head-proportion-r16"><img src="review/20261016-internal-upgrade/samples/M01-head-proportion-r16.png" alt="无牌R16修正头壳纵向体积和侧部展宽" style="width:100%;max-height:920px;object-fit:contain;background:#dfe5de"></a><p class="readiness-note">小头通过相对身体整体缩小实现，保留头壳正常高宽；不把天线计作头高。馆守及固定源图批次保持，运行未替换。</p><details class="r4-history"><summary>此前综合头型及探索历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M05-style-unification-production-r2.json').exists():
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.19 · 无牌头部确认 / 王者画法统一R2</p><h2>无牌头部固定，旧拳王沿用，王者小幅统一画法。</h2><p class="r3-lead">王者的新样例收敛碎线和反光，用清晰块面、墨线与分层明暗适配当前无牌。原藏蓝白红金、右钻左盾、双肩炮、层翼和厚重全装保持。</p><div class="review-jump"><a href="review/20261016-internal-upgrade/M05-style-match-r2.html">王者新旧对照与具体修改</a><a href="review/20261016-internal-upgrade/M01-family-head-review-r14.html#head-proportion-r16">已确认无牌头部</a><a href="review/20261016-internal-upgrade/next-batch-mecha-20261019.html#old-boxer">旧拳王当前样例</a><a href="review/20261016-internal-upgrade/index.html#plan">升级计划</a></div><a href="review/20261016-internal-upgrade/M05-style-match-r2.html"><img src="review/20261016-internal-upgrade/samples/M05-full-loadout-style-r2.png" alt="完全版王者R2，保留全装配色与武器，统一块面和明暗" style="width:100%;max-height:920px;object-fit:contain;background:#dfe5de"></a><p class="readiness-note">无牌认可仅限R16指定头部；旧拳王沿当前方向继续。王者R2具体新图待看，整机视图/模型/运行分别验证。馆守及固定29文件保持，新图未交接。</p><details class="r4-history"><summary>此前综合头型与当时状态</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M05-modular-production-r4.json').exists():
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.19 · 王者L角 / 素体与配件包R4</p><h2>同一台王者，叠上多套豪华配件包。</h2><p class="r3-lead">图四的脸配对称四瓣侧冠，中间改前伸L型犄角，尖端有朝回的鱼叉倒钩。已分别制作头部正侧、素体、全装及配件分组，保持原配色、厚重华丽和有用冗余。</p><div class="review-jump"><a href="review/20261016-internal-upgrade/M05-modular-r4.html#head">当前L角头部</a><a href="review/20261016-internal-upgrade/M05-modular-r4.html#chassis">素体与全装</a><a href="review/20261016-internal-upgrade/M05-modular-r4.html#packages">配件包整理与加强意见</a><a href="review/20261016-internal-upgrade/index.html#plan">升级计划</a></div><a href="review/20261016-internal-upgrade/M05-modular-r4.html"><img src="review/20261016-internal-upgrade/samples/M05-head-L-harpoon-r4b.png" alt="王者新头部，前伸L角与朝回倒钩的正侧对照" style="width:100%;max-height:750px;object-fit:contain;background:#dfe5de"></a><p class="readiness-note">王者本轮新稿待看；手绘结构示意未代替同模型投影或运行验证。无牌R16头部、旧拳王当前方向、馆守及固定29源保持，新图未交接。</p><details class="r4-history"><summary>此前王者画法比较与当时状态</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M05-head-upward-L-production-r5.json').exists():
    head5=json.loads((OUT/'M05-head-upward-L-production-r5.json').read_text())
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.20 · 王者朝上独角仙L角R5</p><h2>短底座前探后上挑，主尖朝上。</h2><p class="r3-lead">用户纠正中央角应像独角仙般向上刺出；此前长段水平向前的解释错误。新稿保留图四脸与两对侧冠，角身朝上，顶端保留朝回倒钩。</p><a href="review/20261016-internal-upgrade/M05-modular-r4.html#head"><img src="review/20261016-internal-upgrade/{head5['file']}" alt="王者朝上独角仙L角R5，正面与左侧对照" style="width:100%;max-height:820px;object-fit:contain;background:#dfe5de"></a><p><a href="review/20261016-internal-upgrade/M05-modular-r4.html#head">查看当前头部正侧及来源 →</a></p><p class="readiness-note">本次为头部源稿修正。R4整机旧中角尚待同步，仅作颈下/配件参考；新稿未认可、未交接或替换运行。</p><details class="r4-history"><summary>此前错误的水平前刺角与配件整理历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M05-head-riese-production-r6.json').exists():
    head6=json.loads((OUT/'M05-head-riese-production-r6.json').read_text())
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.20 · 王者角与天线R6</p><h2>厚根上挑额角，细侧天线分层。</h2><p class="r3-lead">用户否定R5直立箭头角，指定参考古铁巨神。新稿保留图四脸与王者原色，重新组织刀刃额角和两对侧天线；正面收正中轴，侧面表达前后弧度。</p><a href="review/20261016-internal-upgrade/M05-modular-r4.html#head"><img src="review/20261016-internal-upgrade/{head6['file']}" alt="王者R6角与天线参考修正，正侧候选" style="width:100%;max-height:820px;object-fit:contain;background:#dfe5de"></a><p><a href="review/20261016-internal-upgrade/M05-modular-r4.html#head">查看当前头部及参考来源 →</a></p><p class="readiness-note">头稿待看，整机旧角尚待同步。无牌已确认头部、旧拳王方向、馆守及固定29源保持。</p><details class="r4-history"><summary>此前已否定的角与各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M05-head-design-fixed-20261020.json').exists():
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.20 · 王者头部选定与整机同步</p><h2>沿这颗头，统一素体和全装。</h2><p class="r3-lead">用户指定采用R6b头部，CML134固定原图及哈希。已将同一头型合回R7素体与全装，保持身体比例和装备；头部认可与新整机图分开。</p><a href="review/20261016-internal-upgrade/M05-modular-r4.html#chassis"><img src="review/20261016-internal-upgrade/samples/M05-full-head-sync-r7.png" alt="王者R7全装同步选定头型，整机新稿" style="width:100%;max-height:950px;object-fit:contain;background:#dfe5de"></a><p><a href="review/20261016-internal-upgrade/M05-modular-r4.html#head">已选定头部原图 →</a> · <a href="review/20261016-internal-upgrade/M05-modular-r4.html#chassis">素体与全装同步稿 →</a></p><p class="readiness-note">认可范围为指定R6b头部源设计；新整机、模型与运行另记。馆守及固定29源保持，新图未交接。</p><details class="r4-history"><summary>此前候选及各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M05-red-fin-production-r9.json').exists():
    fin9=json.loads((OUT/'M05-red-fin-production-r9.json').read_text())
    current_mask=next(x for x in fin9['items'] if x['id']=='MASK')
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.20 · 王者战斗面罩与红色头鳍</p><h2>一顶头盔，普通脸与战斗面罩。</h2><p class="r3-lead">R7源稿与R8面罩已采用；按最新侧图标注在头顶中线加红鳍。侧面展开鳍面，正面由金色中角遮住，两个面部状态共用皇冠和头盔。</p><a href="review/20261016-internal-upgrade/M05-battle-mask-r8.html"><img src="review/20261016-internal-upgrade/{current_mask['file']}" alt="王者新增红鳍与战斗面罩正侧源稿" style="width:100%;max-height:820px;object-fit:contain;background:#dfe5de"></a><p><a href="review/20261016-internal-upgrade/M05-battle-mask-r8.html">普通脸／战斗面罩及转换示意 →</a></p><p class="readiness-note">新增红鳍图供看稿；转换板为局部构造示意。整机R7尚未合入红鳍与闭合面罩，模型与运行另记。</p><details class="r4-history"><summary>此前源设计与各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M05-turnaround-production-r12.json').exists():
    tri11=json.loads((OUT/'M05-turnaround-production-r12.json').read_text())
    current_front=next(x for x in tri11['items'] if x['id']=='FULL_FRONT')
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.20 · 王者三视 R12</p><h2>恢复原稿身形，再展开正、侧、背。</h2><p class="r3-lead">按反馈恢复完整大腿、长胫甲与正常头部体积；新稿同步右肘前屈和钻头朝前，背包加中央主喷口及双燃料罐。素体与全装共用基础身体和红鳍头盔。</p><a href="review/20261016-internal-upgrade/M05-turnaround-r12.html"><img src="review/20261016-internal-upgrade/{current_front['file']}" alt="王者R11全装正面，恢复长腿身形" style="width:100%;max-height:1050px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M05-turnaround-r12.html#full">全装三视 →</a> · <a href="review/20261016-internal-upgrade/M05-turnaround-r12.html#core">素体三视 →</a> · <a href="review/20261016-internal-upgrade/M05-turnaround-r12.html#head">两状态头部 →</a></p><p class="readiness-note">R7/R8/R9源设计已采用，R12新三视仍为绘制源稿；模型与运行另记。</p><details class="r4-history"><summary>此前源设计与各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M02-turnaround-production-r2.json').exists():
    boxer2=json.loads((OUT/'M02-turnaround-production-r2.json').read_text())
    current_front=next(x for x in boxer2['items'] if x['id']=='FRONT')
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.20 · 旧拳王三视 R2</p><h2>沿现有造型，补齐旧拳王正、侧、背。</h2><p class="r3-lead">象牙白、土棕与深红，厚肩红拳套和替换装甲保留。先将前探透视展开为站直正面，再按同一身形绘制侧背；拳套体积与腿长逐面对应。</p><a href="review/20261016-internal-upgrade/M02-turnaround-r2.html"><img src="review/20261016-internal-upgrade/{current_front['file']}" alt="旧拳王当前正面三视源稿" style="width:100%;max-height:1050px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M02-turnaround-r2.html">旧拳王三视对照 →</a> · <a href="review/20261016-internal-upgrade/M05-turnaround-r12.html">王者当前三视 →</a></p><p class="readiness-note">沿已认可可继续的旧拳王方向补绘，新图和模型/动作/运行分别验证。</p><details class="r4-history"><summary>王者三视与此前各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M11-cargo-production-r1.json').exists():
    cargo=json.loads((OUT/'M11-cargo-production-r1.json').read_text())
    vehicle=next(x for x in cargo['items'] if x['id']=='VEHICLE')
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.21 · 下一批：货柜领袖 R1</p><h2>四轴双形态，机器人正、侧、背。</h2><p class="r3-lead">沿已确定v4头脸统一白蓝橙货运躯体，每侧四轮位可追认，货柜保持独立载荷。已收正背面轮轴视向与侧面斜角；本轮四张新源稿供看稿。</p><a href="review/20261016-internal-upgrade/M11-cargo-r1.html"><img src="review/20261016-internal-upgrade/{vehicle['file']}" alt="货柜领袖当前四轴载柜货车源稿" style="width:100%;max-height:900px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M11-cargo-r1.html">查看双形态、三面与部件对应 →</a></p><p class="readiness-note">旧拳王R2当前3张、王者R12当前7张源稿已获用户认可，<a href="review/20261016-internal-upgrade/mecha-source-batch-acceptance-20261021.json">本次采用范围</a>已登记。货柜领袖新稿、同模型与运行分别判断。</p><details class="r4-history"><summary>上一批图稿与此前各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M11-future-production-r2.json').exists():
    future=json.loads((OUT/'M11-future-production-r2.json').read_text())
    vehicle=next(x for x in future['items'] if x['id']=='VEHICLE')
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.21 · 货柜领袖未来双形态 R2</p><h2>流线电驱车形，同步人形与无水平天线头部。</h2><p class="r3-lead">按用户新方向参考Tesla货车，改大弧面风挡、平滑前罩和导流覆壳；人形胸肩与同一车形对应，头部保留中央摄像头与分节面甲，通讯模块贴合盔体。</p><a href="review/20261016-internal-upgrade/M11-future-r2.html"><img src="review/20261016-internal-upgrade/{vehicle['file']}" alt="货柜领袖R2未来流线四轴货车" style="width:100%;max-height:900px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M11-future-r2.html">查看新版车形、人形与头部近景 →</a></p><p class="readiness-note">本轮三张新稿供看稿；R1旧侧背仅历史。旧拳王／王者上一批10张及此前固定29源保持。</p><details class="r4-history"><summary>R1旧车形及此前各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M11-structure-and-head-production-r4.json').exists():
    current=json.loads((OUT/'M11-structure-and-head-production-r4.json').read_text())
    head=next(x for x in current['items'] if x['id']=='HEAD_OPTIONS')
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.21 · 货柜领袖整体盔型与布局</p><h2>额框、侧盔与护颊连成整体。</h2><p class="r3-lead">按用户参考重画两种整体头盔，取消独立顶天线，保持正常头高。车形已补摄像头后视，同件刚体草模说明部件去向，驾驶空间与展开支撑仍未解决。</p><a href="review/20261016-internal-upgrade/M11-structure-and-head-r4.html"><img src="review/20261016-internal-upgrade/{head['file']}" alt="货柜领袖整体头盔A/B正面与斜视候选" style="width:100%;max-height:1000px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M11-structure-and-head-r4.html">查看头部、车形和变形布局 →</a></p><p class="readiness-note">具体新稿待看，R2整机仅颈下参考；同件运动导出不是完整变形验证。</p><details class="r4-history"><summary>R2双形态及此前各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M11-heroic-antenna-production-r5.json').exists():
    current=json.loads((OUT/'M11-heroic-antenna-production-r5.json').read_text())
    head=current['items'][0]
    prior_start=fresh_intro.index('>')+1
    prior_end=fresh_intro.index('</section>')
    prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.21 · 货柜领袖保留天线与正面角色头型</p><h2>明确耳侧天线，收窄头盔，放平眼眉。</h2><p class="r3-lead">按用户再次纠正保留天线，采用钝头耳侧上伸结构；撤去R4宽冠，面甲减少密集叠片，眼形改得更平稳。R4 A/B已被否定，当前新稿供看稿。</p><a href="review/20261016-internal-upgrade/M11-heroic-antenna-r5.html"><img src="review/20261016-internal-upgrade/{head['file']}" alt="货柜领袖明确钝头天线与平稳眼眉的头部修正版" style="width:100%;max-height:1000px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M11-heroic-antenna-r5.html">查看头部修正版 →</a></p><p class="readiness-note">具体新稿未采用；车形与布局沿用，此轮没有宣称完成变形或整机同步。</p><details class="r4-history"><summary>已被否定的R4头型及此前各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M11-turnaround-structure-production-r7.json').exists():
    current=json.loads((OUT/'M11-turnaround-structure-production-r7.json').read_text())
    front=next(x for x in current['items'] if x['id']=='FRONT')
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.21 · 货柜领袖双形态三视与可变结构</p><h2>指定头部、勇者颏甲与原长腿身形。</h2><p class="r3-lead">按用户附图保留原眼形和头部纵向体积，新增前凸颏甲；补人形正侧背、车形三视、头仓/天线与轮架/腿架/三片货台设计。具体新稿供看稿，局部草模不代表全机结构通过。</p><a href="review/20261016-internal-upgrade/M11-turnaround-structure-r7.html"><img src="review/20261016-internal-upgrade/{front['file']}" alt="货柜领袖当前长腿正面与原比例头部颏甲" style="width:100%;max-height:1150px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M11-turnaround-structure-r7.html">查看人形/车形三视与结构优化 →</a></p><p class="readiness-note">指定原头稿已采用；新增颏甲、三视与结构稿未自动采用。此前固定源与运行资产保持。</p><details class="r4-history"><summary>此前头稿及各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M11-posture-production-r8.json').exists():
    current=json.loads((OUT/'M11-posture-production-r8.json').read_text())
    item=current['items'][0]
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.21 · 货柜领袖肩颈体态修正</p><h2>抬出头颈，打开肩胸。</h2><p class="r3-lead">沿用户肯定的f27斜侧稿保留体量，露出短实装甲颈部，降低肩线并协调胸甲上沿；保持原头型、双侧天线、勇者颏甲和长腿。</p><a href="review/20261016-internal-upgrade/M11-turnaround-structure-r7.html#posture-r8"><img src="review/20261016-internal-upgrade/{item['file']}" alt="货柜领袖R8肩颈体态修正" style="width:100%;max-height:1150px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M11-turnaround-structure-r7.html#posture-r8">查看修正版与原稿对照 →</a></p><p class="readiness-note">当前为斜侧源稿；旧三视和头仓活动结构尚未同步R8。</p><details class="r4-history"><summary>此前三视与结构及各轮历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M11-turnaround-delivery-production-r9.json').exists():
    current=json.loads((OUT/'M11-turnaround-delivery-production-r9.json').read_text())
    item=current['items'][0]
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 货柜领袖形象确定与三视交付</p><h2>沿确定形象，统一肩颈与背架。</h2><p class="r3-lead">R8整体形象已由用户确定，R9正侧背保持原头型、双侧天线、勇者颏甲和长腿，修正肩颈与纵向货台背架。</p><a href="review/20261016-internal-upgrade/M11-source-delivery-r9.html"><img src="review/20261016-internal-upgrade/{item['file']}" alt="货柜领袖修正正面源稿" style="width:100%;max-height:1150px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/M11-source-delivery-r9.html">查看修正三视及下载交付包 →</a></p><details class="r4-history"><summary>此前源稿与结构研究</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'aircraft-source-batch-20261022.json').exists():
    current=json.loads((OUT/'aircraft-source-batch-20261022.json').read_text())
    item=current['items'][0]
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 下一批：雷翎与歌翼</p><h2>先看清同一套座舱、翼根与发动机。</h2><p class="r3-lead">蓝紫远射机与粉白巡演支援机分别完成双形态首轮候选；雷翎航空枪口朝向已局部修正。货柜领袖已确定形象，修正三视和源设计包可下载。</p><a href="review/20261016-internal-upgrade/aircraft-source-batch-20261022.html"><img src="review/20261016-internal-upgrade/{item['file']}" alt="雷翎双形态新候选" style="width:100%;max-height:850px;object-fit:contain;background:#fff"></a><p><a href="review/20261016-internal-upgrade/aircraft-source-batch-20261022.html">查看雷翎与歌翼首轮新稿 →</a> · <a href="review/20261016-internal-upgrade/M11-source-delivery-r9.html">货柜领袖三视与交付包 →</a></p><p class="readiness-note">下一批新图供看稿，未替换原Working参考或运行资产。</p><details class="r4-history"><summary>货柜领袖本批交付及此前源稿</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'aircraft-runtime-comparison-20261022.json').exists():
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 雷翎与歌翼现用机设比较</p><h2>保留现用轮廓，先对齐配色与材质。</h2><p class="r3-lead">已从当前Demo加载器取出人形与航空态比较。现用雷翎的放射刃翼、窄头，歌翼的长双角、肩翼裙甲，比新稿更有记忆点。新稿保留作结构研究，不推荐替换整机。</p><p>雷翎投射《变形金刚》喷气重涂谱系，歌翼投射《超时空要塞》可变战机谱系。两机不是同一IP系列，但应共享本作画法。</p><p><a href="review/20261016-internal-upgrade/aircraft-runtime-comparison-20261022.html">查看现用全身、航空态与新稿逐项对照 →</a> · <a href="review/20261016-internal-upgrade/M11-source-delivery-r9.html">货柜领袖三视与交付包 →</a></p><p class="readiness-note">下一步保留现用机设做配色与有限材质试样；本轮未换色、未改模型或运行资产。当前取图是原加载器的独立观察视角，不代替正常战棋镜头实测。</p><details class="r4-history"><summary>此前双形态研究稿及货柜领袖交付</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'aircraft-existing-design-recolour-production-r2.json').exists():
    current=json.loads((OUT/'aircraft-existing-design-recolour-production-r2.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    preview=''.join(f'<a href="review/20261016-internal-upgrade/aircraft-existing-design-recolour-r2.html#{x["id"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="{x["name"]}沿现用机设配色修订" style="width:100%;height:auto;background:#faf8f0"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 雷翎与歌翼配色修订</p><h2>保留既有识别点，统一色块与画法。</h2><p class="r3-lead">沿Demo现用机设绘制两台双形态修订。雷翎保留深色红刃翼，歌翼保留红白肩翼与修长身形；共同清理碎亮线与划痕，原头型、翼形和主要比例继续保留。</p>{preview}<p><a href="review/20261016-internal-upgrade/aircraft-existing-design-recolour-r2.html">查看修改稿与现用造型对照 →</a></p><p class="readiness-note">本轮为配色与画法源稿，未更换模型、骨架或运行贴图；具体新色样未自动采用。</p><details class="r4-history"><summary>此前现用机设比较及各轮源稿</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'aircraft-synthesis-production-r3.json').exists():
    current=json.loads((OUT/'aircraft-synthesis-production-r3.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    preview=''.join(f'<a href="review/20261016-internal-upgrade/aircraft-synthesis-r3.html#{x["id"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="{x["name"]}R3整机、匹配头部与航空态综合设计" style="width:100%;height:auto;background:#faf8f0"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 雷翎与歌翼故事/IP综合设计R3</p><h2>新头、旧识别点与前建议稿真正综合。</h2><p class="r3-lead">R2整机回退只换色被用户否定。本轮雷翎实际采用参考启发的V形侧天线，结合座舱胸、长枪和刃翼；歌翼按可变战机/护航重画头盔、座舱与翼腿，沿前建议稿提升画法。</p>{preview}<p><a href="review/20261016-internal-upgrade/aircraft-synthesis-r3.html">查看综合设计、故事取舍与头部核对 →</a></p><p class="readiness-note">当前为源设计候选，未更换运行资产；歌翼附加挂舱和背部映射仍需继续收敛。</p><details class="r4-history"><summary>被反证的R2回退稿及此前比较</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M14-music-support-production-r4.json').exists():
    music=json.loads((OUT/'M14-music-support-production-r4.json').read_text())
    item=music['item']
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 歌翼音乐传播模块R4</p><h2>沿R3主体，让歌声功能可见。</h2><p class="r3-lead">肩后声传播板翻开露出扬声器，闭合后收为背部/航空整流罩。现有角色表为隼真驾驶、莉歌歌姬；本轮保留头型、主体与雷翎R3。</p><a href="review/20261016-internal-upgrade/M14-music-support-r4.html"><img src="review/20261016-internal-upgrade/{item['file']}" alt="歌翼音乐模块展开、闭合与航空收纳候选" style="width:100%;height:auto;background:#faf8f0"></a><p><a href="review/20261016-internal-upgrade/M14-music-support-r4.html">查看角色分工、音乐模块与IP取舍 →</a> · <a href="review/20261016-internal-upgrade/aircraft-synthesis-r3.html">雷翎与歌翼R3主体 →</a></p><p class="readiness-note">当前为音乐模块源设计，未更改人物身份、运行或广播规则，也未生成或实听歌曲。</p><details class="r4-history"><summary>R3综合主体及此前各轮</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M14-turnaround-production-r5.json').exists():
    current=json.loads((OUT/'M14-turnaround-production-r5.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    previews=''.join(f'<a href="review/20261016-internal-upgrade/{x["file"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="歌翼{x["label"]}R5三视源稿" style="width:100%;height:auto"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 歌翼音乐传播版三视R5</p><h2>沿已采用R4，统一正侧背。</h2><p class="r3-lead">保留头型、长腿、座舱胸与暖象牙/朱红涂装。声翼统一向前展开，背面看外壳和支架；侧背修正初稿的转角与脚尖方向。</p><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">{previews}</div><p><a href="review/20261016-internal-upgrade/M14-turnaround-r5.html">查看三视与下载源图/提示词包 →</a></p><p class="readiness-note">R4原源设计已采用，三视按授权派生。新绘制、精确机构与模型/运行分别判断。</p><details class="r4-history"><summary>已采用R4音乐版及此前综合设计</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M08-turnaround-production-r4.json').exists():
    current=json.loads((OUT/'M08-turnaround-production-r4.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    previews=''.join(f'<a href="review/20261016-internal-upgrade/{x["file"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="雷翎{x["label"]}R4三视源稿" style="width:100%;height:auto"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 雷翎三视R4补齐</p><h2>沿R3综合稿，补齐正侧背。</h2><p class="r3-lead">保留V形侧天线、座舱胸、修长比例与红白蓝刃翼。三视为相同展开状态，长枪始终在机体右手；侧面及背部肩壳/脊柱/骨盆已按视向修正。</p><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">{previews}</div><p><a href="review/20261016-internal-upgrade/M08-turnaround-r4.html">查看雷翎三视与下载源图/提示词包 →</a> · <a href="review/20261016-internal-upgrade/M14-turnaround-r5.html">歌翼三视 →</a></p><p class="readiness-note">本次为二维设定源图，隐面细部、精确机构与同件模型仍分别核对。</p><details class="r4-history"><summary>歌翼三视、音乐版及此前综合稿</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M08-turnaround-production-r5.json').exists():
    current=json.loads((OUT/'M08-turnaround-production-r5.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    previews=''.join(f'<a href="review/20261016-internal-upgrade/{x["file"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="雷翎{x["label"]}R5修长身形三视" style="width:100%;height:auto"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.22 · 雷翎修长身形三视R5</p><h2>回到原设定的轻巧长身形。</h2><p class="r3-lead">R4被指出变矮、变敦实。本次沿R3原稿收窄肩胸和四肢、拉开腰段、提高髋线并延续长腿，头盔保持纵向体积；重绘正面后同步侧背。</p><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">{previews}</div><p><a href="review/20261016-internal-upgrade/M08-turnaround-r5.html">查看修正三视、原设定与前后对照 →</a> · <a href="review/20261016-internal-upgrade/M14-turnaround-r5.html">歌翼三视 →</a></p><p class="readiness-note">R4比例已退出当前依据；本轮是二维源图修正，隐面与同件模型仍分别核对。</p><details class="r4-history"><summary>R4比例反例、歌翼三视及此前原稿</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'aircraft-airframe-production-r6.json').exists():
    current=json.loads((OUT/'aircraft-airframe-production-r6.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    previews=''.join(f'<a href="review/20261016-internal-upgrade/{current["reader"]}#{x["id"]}"><img src="review/20261016-internal-upgrade/{x["front"]["file"]}" alt="{x["name"]}R6体态与航空结构线正面" style="width:100%;height:auto"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.23 · 雷翎与歌翼航空结构线R6</p><h2>比例按歌翼，主形保留。</h2><p class="r3-lead">放弃雷翎R5过瘦过长的比例。直接以歌翼实际三视作体态锚，减少两机肩腿的装饰折角，让座舱、进气道、翼根和发动机舱更明确；头冠、配色、长枪与音乐模块继续保留。</p><div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px">{previews}</div><p><a href="review/20261016-internal-upgrade/{current['reader']}">查看两机修订三视及源图/提示词包 →</a></p><p class="readiness-note">已按新正面同步侧背；本轮为二维源设定修订，原歌翼R4采用记录保留，新表面与完整变形/模型另验。</p><details class="r4-history"><summary>前两轮比例反例与原主形来源</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'public-works-source-production-r1.json').exists():
    current=json.loads((OUT/'public-works-source-production-r1.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    previews=''.join(f'<a href="review/20261016-internal-upgrade/{current["reader"]}#{x["id"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="{x["name"]}整机与作业结构首稿" style="width:100%;height:auto"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.23 · 集中交付与下一批城市职业机</p><h2>沿已有造型，细化维修与吊装。</h2><p class="r3-lead">已确定设计已发送给「战斗主玩法打磨」，雷翎/歌翼R6六张来源已固定。下一批预算二号保留黄绿工具机与替换件特征，市政吊装机保留吊臂、履带和稳定支腿；两张新源板完成局部功能细节修正。</p>{previews}<p><a href="review/20261016-internal-upgrade/{current['reader']}">查看下一批首稿与提示词包 →</a> · <a href="review/20261016-internal-upgrade/confirmed-design-handoff-20261023.html">已确定设计集中交付单 →</a></p><p class="readiness-note">新首稿供比较，未直接替换模型或运行。交付发送、源设计采用和运行验收分别记录。</p><details class="r4-history"><summary>已确定雷翎/歌翼三视与此前来源</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M06-labor-identity-production-r2.json').exists():
    current=json.loads((OUT/'M06-labor-identity-production-r2.json').read_text());item=current['items'][0]
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.23 · 预算二号职业机语言 R2</p><h2>市政维修老兵，接通三代旧电路。</h2><p class="r3-lead">工务机动队主要投射《机动警察》的城市职业机。R1头部和通用铠甲被指出缺少特色；本次将作业护盔、检修舱、关节防尘套、替换件及卷盘供能背架连成整机设计。</p><a href="review/20261016-internal-upgrade/{current['reader']}"><img src="review/20261016-internal-upgrade/{item['file']}" alt="预算二号R2整机、作业盔三方向与三制式供能背架" style="width:100%;height:auto"></a><p><a href="review/20261016-internal-upgrade/{current['reader']}">查看整机与头部研究、IP及故事依据 →</a> · <a href="review/20261016-internal-upgrade/public-works-source-r1.html#M07">市政吊装机当前稿 →</a></p><p class="readiness-note">具体新稿为候选；A为整机采用方向，B/C为备选。既定故事职责、源设计采用与运行验证分别保留。</p><details class="r4-history"><summary>上一批源稿及此前已确定设计交付</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'M06-design-fixed-20261023-r2.json').exists():
    fresh_intro=fresh_intro.replace('具体新稿为候选；A为整机采用方向，B/C为备选。既定故事职责、源设计采用与运行验证分别保留。','用户已采用R2整机与A头型，B/C保留为未采用研究。<a href="review/20261016-internal-upgrade/M06-design-fixed-20261023-r2.json">采用范围与后续三视修正项</a>已登记；机构、模型和运行另验。',1)
if (OUT/'M06-turnaround-production-r3.json').exists():
    current=json.loads((OUT/'M06-turnaround-production-r3.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    previews=''.join(f'<a href="review/20261016-internal-upgrade/{x["file"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="预算二号{x["label"]}源图" style="width:100%;height:auto"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.23 · 预算二号三视源图</p><h2>沿确定A头型与整机，完成正、侧、背。</h2><p class="r3-lead">保持成人厚实体态与头壳体积，通讯模块在机体右耳、青绿替换件在左小腿、救援夹具在左手；背部保留卷盘和三制式供能接口。</p><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">{previews}</div><p><a href="review/20261016-internal-upgrade/{current['reader']}">查看三视原图与源包 →</a></p><p class="readiness-note">新三视按用户授权派生；已确定母稿保持，模型、机构与工作动作另验。</p><details class="r4-history"><summary>已确定整机/A头型及此前源稿</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'city-response-source-production-r2.json').exists():
    current=json.loads((OUT/'city-response-source-production-r2.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    previews=''.join(f'<a href="review/20261016-internal-upgrade/{current["reader"]}#{x["id"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="{x["name"]}按用户反馈修订源板" style="width:100%;height:auto"></a>' for x in current['items'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.23 · 灰崎 / 消防两条方向修订</p><h2>灰崎保留头与色，消防重做工程变形主形。</h2><p class="r3-lead">灰崎减少肩胸与四肢碎切面，改连续曲面和清楚关节；消防改为正常双足人形与消防架桥车，驾驶室/轮组/桥板可追认，四支腿只用于车辆作业支撑。</p>{previews}<p><a href="review/20261016-internal-upgrade/{current['reader']}">查看两机修订源图与参考取舍 →</a></p><p class="readiness-note">预算二号当前三视已确定；本轮两张新图仍为源设计候选，采用方向后直接补三视。车型/架桥机构与运行另验。</p><details class="r4-history"><summary>已确定预算二号三视及此前源稿</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'city-response-design-fixed-20261023-r2.json').exists():
    fresh_intro=fresh_intro.replace('本轮两张新图仍为源设计候选，采用方向后直接补三视。','两张R2整机父源已由用户采用。')
if (OUT/'city-response-turnaround-production-r3.json').exists():
    current=json.loads((OUT/'city-response-turnaround-production-r3.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    previews=''
    for machine in current['items']:
        pictures=''.join(f'<a href="review/20261016-internal-upgrade/{x["file"]}"><img src="review/20261016-internal-upgrade/{x["file"]}" alt="{machine["name"]}{x["label"]}" style="width:100%;height:auto"></a>' for x in machine['views'])
        previews+=f'<h3>{machine["name"]}</h3><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">{pictures}</div>'
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.24 · 灰崎 / 消防三视图</p><h2>沿已定整机，完成两机正、侧、背。</h2><p class="r3-lead">保留头部、配色和成人身形。灰崎保留连续曲面与六墙；消防保留双足工程体态、轮组与成对折叠桥板。</p>{previews}<p><a href="review/20261016-internal-upgrade/{current['reader']}">查看三视原图与源包 →</a></p><p class="readiness-note">R2父源已经确定；本轮为二维派生源图，分件模型与机构/工作动作另验。</p><details class="r4-history"><summary>已确定整机父源与此前源图</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'city-response-refinement-production-r4.json').exists():
    current=json.loads((OUT/'city-response-refinement-production-r4.json').read_text())
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    m09=next(x for x in current['items'] if x['id']=='M09');m10=next(x for x in current['items'] if x['id']=='M10')
    views=''.join(f'<a href="review/20261016-internal-upgrade/{v["file"]}"><img src="review/20261016-internal-upgrade/{v["file"]}" alt="灰崎{v["label"]}" style="width:100%;height:auto"></a>' for v in m09['views'])
    sheets=''.join(f'<h3>{v["label"]}</h3><a href="review/20261016-internal-upgrade/{v["file"]}"><img src="review/20261016-internal-upgrade/{v["file"]}" alt="消防{v["label"]}" style="width:100%;height:auto"></a>' for v in m10['extras'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.24 · 灰崎修正 / 消防补全</p><h2>灰崎校正头身；消防补载具和变形图。</h2><p class="r3-lead">按指定母稿重新推灰崎正面，等比缩头/收肩并同步侧背。消防保留当前人形，补两窗消防架桥车三视与六步部件对应图。</p><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px">{views}</div>{sheets}<p><a href="review/20261016-internal-upgrade/{current['reader']}">查看修正原图与图纸 →</a></p><p class="readiness-note">新修订供看稿；变形路径、净空与承重仍需机构核对。R3灰崎正面已由用户指出偏差，保留为历史。</p><details class="r4-history"><summary>此前两机源图与反馈历史</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
if (OUT/'crane-mirror-source-production-r1.json').exists():
    current=json.loads((OUT/'crane-mirror-source-production-r1.json').read_text())
    crane=next(x for x in current['items'] if x['id']=='M07');mirror=next(x for x in current['items'] if x['id']=='M12')
    prior_start=fresh_intro.index('>')+1;prior_end=fresh_intro.index('</section>');prior_inner=fresh_intro[prior_start:prior_end]
    views=''.join(f'<a href="review/20261016-internal-upgrade/{v["file"]}"><img src="review/20261016-internal-upgrade/{v["file"]}" alt="市政吊装机{v["label"]}" style="width:100%;height:auto"></a>' for v in crane['views'])
    fresh_intro=f'''<section class="review-intro r3-intro" id="latest-review-r4"><p class="r3-kicker">2026.10.24 · 下一批职业机 / 镜像机</p><h2>吊装机补三视，镜星试航空共架与棱镜收放。</h2><p class="r3-lead">灰崎/消防的最新8张源图清单已发送主对话。当前新稿接续原台账：吊装机保持青绿/象牙白/红结构色，镜星保留紫白与菱形独眼。</p><h3>市政吊装机 · 收拢行驶态</h3><div style="display:grid;grid-template-columns:1fr 1.35fr 1fr;gap:12px;align-items:center">{views}</div><h3>镜星 · 共架试案</h3><a href="review/20261016-internal-upgrade/{mirror['file']}"><img src="review/20261016-internal-upgrade/{mirror['file']}" alt="镜星新源板，含棱镜收放与航空形态试案" style="width:100%;height:auto"></a><p><a href="review/20261016-internal-upgrade/{current['reader']}">查看下一批原图与设计依据 →</a></p><p class="readiness-note">镜星与雷翎的共架关系仍是试案。新稿未发送、未代签采用或机构/运行通过。</p><details class="r4-history"><summary>已发送灰崎 / 消防及此前源图</summary>{prior_inner}</details></section>'''+fresh_intro[prior_end+len('</section>'):]
source=source[:start]+fresh_intro+source[end:]
source=source.replace('超GAG 外援最新交付复核 r3 · 298项逐图意见','超GAG 外援新版接收 r4 · 采用清单与内部升级样例').replace('超GAG 外援美术 · 最新交付复核 r3','超GAG 外援美术 · 新版接收与内部升级 r4')
source=source.replace('原来稿页生成于 2026-10-14 · 最新复核：2026-10-16 · r3：当前文件 / 同源 / 功能 / 配色 / 画法（Asia/Shanghai）','原来稿页生成于 2026-10-14 · 最新接收：2026-10-16 · r4：按用途接收 / 内部统一母版 / 样例确认后推广（Asia/Shanghai）')
source=re.sub(r'<div class="summary">.*?</div>',f'<div class="summary">298项采用路线 · 本轮43项换图复核<br>风格保留，具体对象由内部统一；下方为r4当前意见。</div>',source,count=1,flags=re.S)
source=re.sub(r'<select[^>]*id="review-verdict-filter".*?</select>','<select id="review-verdict-filter"><option value="ALL">所有采用方式</option>'+''.join(f'<option value="{k}">{v}（{counts[k]}）</option>' for k,v in LABELS.items())+'<option value="CHANGED">43项换图复核</option></select>',source,count=1,flags=re.S)
source=re.sub(r'<span class="gcount">本组(\d+)项 · A \d+ / B \d+ / C \d+</span>',r'<span class="gcount">本组\1项 · r4按采用方式标记</span>',source)
css='''\n/* r4 source adoption; previous opinions remain explicitly historical. */\n.r4-sample-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:24px 0}.r4-sample-strip a{display:block;background:#e2e5dd;border-radius:5px;text-align:center;text-decoration:none;white-space:normal;overflow:hidden}.r4-sample-strip img{width:100%;height:230px;object-fit:contain}.r4-sample-strip span{display:block;padding:8px;font-size:12px}.r4-note{font-size:12px;color:#5a6e76;overflow-wrap:anywhere}.r4-history{border-top:1px solid #d1d9d2;margin-top:10px;padding-top:10px}.r4-history>summary,.r4-old-overview>summary{font-size:13px;color:#58716d;cursor:pointer}.r4-old-overview{max-width:1368px;margin:14px auto;padding:12px 24px;background:#e9ede5;border-radius:6px}.r4-history .r3-card-current{padding:10px;background:#f2f3ed}@media(max-width:700px){.r4-sample-strip{grid-template-columns:1fr 1fr}.r4-sample-strip img{height:190px}}\n'''
source=source.replace('</style>',css+'</style>',1)
source=re.sub(r'<p class="foot">.*?</p>', '<p class="foot">2026-10-16 r4：43项换图复核，298项加工去向。M03/S11按实际内容校正，原图保留。源图与内部样例不等于运行替换或新增认可。</p>', source, flags=re.S)
# Keep the existing small UI script; update any embedded review payload to current facts.
source=re.sub(r'(<script[^>]*type="application/json"[^>]*>).*?(</script>)',lambda m:m[1]+json.dumps(manifest,ensure_ascii=False).replace('</','<\\/')+m[2],source,flags=re.S)
PAGE.write_text(source)
write_json(OUT/'published-state.json',{'original_page_sha256':source_hash,'page_sha256':sha(PAGE),'reader_sha256':sha(OUT/'index.html'),'counts':dict(counts),'runtime_replaced':False,'browser_verified':False})
print(json.dumps({'cards':len(records),'changed':43,'routes':dict(counts),'reader':str(OUT/'index.html'),'page_sha256':sha(PAGE)},ensure_ascii=False))
