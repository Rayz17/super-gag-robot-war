"""Publish native generated colour studies; never modifies gameplay models."""
from pathlib import Path
import hashlib, html, json, shutil, sys
from PIL import Image

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='aircraft-existing-design-recolour-production-r2.json'
READER='aircraft-existing-design-recolour-r2.html'
def read(name):return json.loads((OUT/name).read_text())
def write(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def ref(file,role,base=OUT):
    path=base/file
    return dict(file=path.relative_to(PROJECT).as_posix(),sha256=sha(path),role=role)

comparison=read('aircraft-runtime-comparison-20261022.json')
for row in comparison['runtime_models']:
    assert sha(PROJECT/row['project_model'])==row['model_sha256'], row['project_model']
    assert sha(OUT/row['capture_file'])==row['capture_sha256'], row['capture_file']
items=[]
for ident,name,runtime,initial,final in [
    ('M08','雷翎','leiling','exec-67bdf0a1-cd4e-4157-bdab-bc3ea47d9680.png',sys.argv[1]),
    ('M14','歌翼','song','exec-507a03f1-4ced-4cc0-b64c-8280836fc440.png',sys.argv[2])]:
    copies=[]
    for rev,source in [('r2',GEN/initial),('r2b',Path(final))]:
        target=OUT/f'samples/{ident}-existing-design-recolour-{rev}.png'
        if target.exists():assert sha(target)==sha(source), 'Refuse to overwrite different source'
        else:shutil.copyfile(source,target)
        assert sha(target)==sha(source)
        with Image.open(target) as im:size=list(im.size);mode=im.mode
        copies.append(dict(file=target.relative_to(OUT).as_posix(),sha256=sha(target),generated_source=str(source),pixel_size=size,mode=mode))
    refs=[ref(f'aircraft-runtime-comparison-20261022/{runtime}_robot.png','exact existing robot identity/pose'),ref(f'aircraft-runtime-comparison-20261022/{runtime}_aircraft.png','exact existing aircraft identity/view'),ref('samples/M04-front-backpack-fins-r7.png','drawing style only; no parts or colours transferred')]
    items.append(dict(id=ident,name=name,runtime_id=runtime,**copies[-1],previous_surface_attempt=copies[0],source_refs=refs,
        prompts=[f'{ident}-existing-design-recolour-prompt-r2.txt',f'{ident}-existing-design-cleanup-prompt-r2b.txt'],
        scope='colour and drawing-language study preserving existing design identifiers; not new geometry master',
        user_accepted=False,runtime_integrated=False))

observations={
 'M08':['保留窄长头盔、红中脊与双尖、叶形黄胸核、放射刃翼、宽胫尖足和原下垂短枪。','主块从旧紫灰蓝整理为更清楚的钴蓝/墨蓝，朱红和象牙仍沿原部件分布；手和枪改深石墨。','首轮肩臂残留旧贴图裂纹样亮线；R2b已局部清理，肩/胫以完整蓝面和少量硬阴影为主。'],
 'M14':['保留长双红角、尖收头脸、黄胸核、横肩翼、垂翼臂甲和修长腿足。','沿现用红白涂装改为暖象牙与朱红大面，关节/手/足收为石墨，座舱和少量功能边保留暖黄。','首轮红色臂翼和腿甲残留碎亮线；R2b已局部清理，红色长面与象牙甲片的分区更完整。']}
record=dict(revision='aircraft-existing-design-recolour-r2',date='2026-10-22',existing_batch='design-followthrough-r1.json',
 user_request='那你还是调整一下雷灵和歌翼的这个设计吧。',
 execution='built-in image_gen; each character initial two-form edit followed by local surface cleanup',
 status='candidate_source_colour_and_drawing_studies',reader=READER,items=items,
 source_models=comparison['runtime_models'],art_direction=ref('docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md','current Working drawing language',PROJECT),
 author_review=dict(reviewer='author',independent_review=False,actual_media=[x['file'] for x in items],observations=observations,
   final_surface_observation=dict(M08='已实看R2b，肩/胫的大蓝面更完整，原头胸、放射翼和航空推进器群可追认。',M14='已实看R2b，红色臂翼和胫甲碎亮线减少，长双角、肩翼与修长身形可追认。'),
   invariant_limits='主要识别点经作者实看保留；二维生成线稿不等于逐顶点保持原模型，隐面和发动机内部未验证。'),
 limitations=['二维重绘保留主要识别点，不等于原模型逐面换色；白底编排与原诊断图不是同像素相机对照。','两形态的轮廓和涂装关系供设计审阅，未验证完整折变、三视几何或连续动作。','未改原模型/贴图/骨架/动作或运行入口；新色样未获用户采用。'],
 runtime_assets_modified=False,canon_changed=False,main_thread_messaged=False)
write(RECORD,record)
write('aircraft-existing-design-recolour-prompts-r2.json',dict(mode='built-in image_gen',items=[dict(id=x['id'],source_refs=x['source_refs'],initial_prompt=x['prompts'][0],cleanup_prompt=x['prompts'][1],cleanup_input=x['previous_surface_attempt']) for x in items]))

sections=[]
for x in items:
    previous=f"aircraft-runtime-comparison-20261022/{x['runtime_id']}"
    rows=''.join('<li>'+html.escape(s)+'</li>' for s in observations[x['id']])
    sections.append(f'''<section id="{x['id']}"><h2>{x['name']} · 现用机设配色修订</h2><a href="{x['file']}"><img class="board" src="{x['file']}" alt="{x['name']}保留现用机设的人形与航空态配色修订"></a><ul>{rows}</ul><details><summary>与现用Demo原造型对照</summary><div class="pair"><figure><img src="{previous}_robot.png" alt="{x['name']}现用人形原造型"><figcaption>现用人形 · 原模型未改</figcaption></figure><figure><img src="{previous}_aircraft.png" alt="{x['name']}现用航空态原造型"><figcaption>现用航空态 · 原模型未改</figcaption></figure></div></details></section>''')
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>雷翎与歌翼｜沿现用机设的配色修订</title><style>*{box-sizing:border-box}body{margin:0;background:#eeeae0;color:#193345;font:16px/1.8 system-ui}main{max-width:1540px;margin:auto;padding:28px}a{color:#08677e}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,43px);line-height:1.35}h2{margin-top:38px}.board{width:100%;height:auto;display:block;background:#faf8f0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:15px 0}figure img{width:100%;display:block}figcaption,.note{font-size:14px;color:#526870}details{margin:22px 0}section{border-top:1px solid #bdc9c6;padding-top:10px;margin-top:30px}.scope{border-left:4px solid #cc5946;background:#faf6eb;padding:14px 20px}@media(max-width:700px){main{padding:18px}.pair{grid-template-columns:1fr}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="#M08">雷翎</a><a href="#M14">歌翼</a><a href="aircraft-runtime-comparison-20261022.html">此前机设比较</a><a href="aircraft-existing-design-recolour-prompts-r2.json">本轮实际提示词</a></nav><h1>保留原有轮廓，统一色块与画法</h1><p>雷翎保留墨蓝红刃翼，歌翼保留红白肩翼与修长身形。两台继续拥有各自的头型与飞行轮廓，共享深墨线、硬阴影和哑光装甲画法。</p><p class="scope">这轮是沿现用机设的配色与表面修订稿。保留既有识别点，未将上一轮蓝紫／粉白新机设恢复为替换母版。</p>'''+''.join(sections)+'''<p class="note">本页为二维源稿，原模型、骨架与动作未改；完整三视、变形机构与正常战棋镜头下的材质效果尚未据此验收。</p><p><a href="aircraft-existing-design-recolour-production-r2.json">源文件、原模型与作者查看记录</a></p></main></body></html>'''
(OUT/READER).write_text(page)

prior=OUT/'aircraft-runtime-comparison-20261022.html'
s=prior.read_text()
notice=f'<aside id="latest-recolour-r2" class="verdict"><h2>本轮已出：沿现用机设的配色修订</h2><p>保留两台原有识别点，已做人形与航空态源稿。<a href="{READER}">查看雷翎与歌翼修改稿 →</a></p><p>以下保留此前新旧机设比较及其当时结论。</p></aside>'
if 'id="latest-recolour-r2"' not in s:prior.write_text(s.replace('<h1>',notice+'<h1>',1))

ledger=read('design-followthrough-r1.json')
ledger['latest_aircraft_recolour']=RECORD
ledger['production_focus'].update(current_step='沿现用雷翎/歌翼分别绘制双形态配色修订，完成一次表面亮裂纹清理。',current_scope='现用机设识别点保留的二维源稿；不改原模型、骨架、动作或其他会话状态。',next='完成源稿人工观察与文件核对；沿当前机设做同模型材质试验时，再按正常镜头复核。')
ledger['experience_record_aircraft_recolour_r2']=dict(classification='experience',original_requirement=['M08','F07','M14','F08','N13'],user_request=record['user_request'],start='前轮新机设未胜过现用设计，用户要求继续调整两台设计。',input='实际读取现用四模型取图作为身份源，按本作画法重绘同一机体双形态；观察残留亮裂纹后局部清理。',visible_consequence='保留原头胸、翼形和身形，改色块/线条和表面；实际最终观察见本轮记录。',actual_artifacts=[x['file'] for x in items],author_review=RECORD+'#author_review',independent_review=False,user_acceptance=False,runtime_changed=False,next='同模型材质、正常镜头和派生三视仍分别核对。')
defect=next(x for x in ledger['defect_ledger'] if x.get('id')=='ART-AIRCRAFT-IDENTITY-ADVANTAGE-02')
change=defect['method_changes'][0]
change.update(status='applied',application_scope='source_study_only',actual_method='直接以现用两形态取图为图像输入，保留识别点做配色/表面重绘；未实施原计划的同几何运行材质试验。',applied_evidence=RECORD,retest='本轮二维源稿实看；同模型同机位/光照材质复测仍未做。')
defect['remaining']='新源稿具体采用待用户判断；同模型材质和正常战棋镜头复测仍未做，不能据二维图关闭运行品质项。'
defect['closed']=False
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_aircraft_recolour']=RECORD;write('sample-author-review.json',author)
decisions=read('user-art-decisions-20261016.json')
decisions['latest_aircraft_adjustment_request']=dict(date='2026-10-22',request=record['user_request'],execution_record=RECORD,new_drawings_user_accepted=False)
write('user-art-decisions-20261016.json',decisions)
print(json.dumps(dict(reader=str(OUT/READER),items=[x['file'] for x in items],runtime_assets_modified=False),ensure_ascii=False))
