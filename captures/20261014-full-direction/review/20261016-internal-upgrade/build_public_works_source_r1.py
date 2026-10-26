"""Deliver two civil-machine source boards; continue the existing art ledger."""
from pathlib import Path
import hashlib,json,shutil,zipfile
from PIL import Image
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='public-works-source-production-r1.json'
READER='public-works-source-r1.html'
PROMPTS='public-works-source-prompts-r1.json'
ZIP='public-works-source-20261023-r1.zip'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(origin,target):
    if target.exists():assert sha(target)==sha(origin)
    else:shutil.copyfile(origin,target)
adoption={x['id']:x for x in read('adoption-manifest.json')['records']}
items=[];history=[]
for ident,name,entity,original,final,attempt,role in [
 ('M06','预算二号救援机','V353U032','e0af32775ebde492fa870edb0552fe34ced1adc6479d2b44d03a741c142a3934.jpg','exec-c8c51d9b-7d70-4caf-99d5-6f0b77eed8fd.png','exec-adcbba8a-0a1b-4c54-bdd0-9ac714f8f805.png','低费维修、撤离与补给；保留黄绿工具机、替换色小腿及模块化工具。'),
 ('M07','市政吊装机','V353U031','232edd1b03a9dfc8e8f70aa0c93dc57b11a5e8b5069a9a8be45603742639f6c0.jpg','exec-e9e1915b-a6ed-4e65-bfb0-bbb8431684ff.png','exec-c0e548a9-bbd1-4285-9609-f91508779aec.png','吊装、推拉与施工；保留吊臂、履带、稳定支腿及单驾驶舱。')
]:
    origin=OUT.parent/'20261015-latest-review/images'/original
    ref=OUT/f'refs/{ident}-public-works-original-20261023.jpg';copy(origin,ref)
    target=OUT/f'samples/{ident}-public-works-master-r1b.png';copy(GEN/final,target)
    old=OUT/f'samples/{ident}-public-works-master-attempt-r1.png';copy(GEN/attempt,old)
    with Image.open(target) as im:size=list(im.size);mode=im.mode
    items.append(dict(id=ident,name=name,canon_entity=entity,role=role,file=target.relative_to(OUT).as_posix(),sha256=sha(target),generated_source=str(GEN/final),pixel_size=size,mode=mode,source_refs=[dict(file=ref.relative_to(OUT).as_posix(),sha256=sha(ref),project_original=origin.relative_to(ROOT).as_posix(),role='原有身份与造型依据'),dict(file='samples/M14-front-airframe-r6.png',sha256=sha(OUT/'samples/M14-front-airframe-r6.png'),role='仅取已确定项目画法，不取机体身份/比例/配色')],prompts=[f'{ident}-public-works-master-prompt-r1.txt',f'{ident}-public-works-local-correction-prompt-r1b.txt'],existing_consumer_refs=adoption[ident]['current_assets'],user_accepted=False,runtime_integrated=False))
    history.append(dict(id=ident,file=old.relative_to(OUT).as_posix(),sha256=sha(old),role='局部功能细节修正前的首稿'))
review=dict(reviewer='author',independent_review=False,actual_media=[x['file'] for x in items],observations=[
 '预算二号保留原黄/青绿/象牙白、圆顶头盔、短单天线、琥珀视窗和厚实工具机身体；前后视中的替换色小腿侧别对应。主图左手持工具、右手空手，后视持握侧没有交换。',
 '预算二号工具快拆连接与备件箱可见；首稿箱内有似备用头的物件，局部改为带轴端和管接头的泵/电机模块，主机轮廓基本保持。',
 '市政吊装机保留伸缩吊臂、液压举升、配重、单驾驶舱、卷扬钢索与一对履带；未强制改成人形。主视可见三只外伸支脚，第四只被机体遮挡，后续多视仍须核对四支腿归属。',
 '市政吊装机首稿收拢小图的吊钩悬空，局部修正后钩块收近驾驶舱前下方红色固定座，钢索从臂端连至钩块；主作业态与钩头放大图保持。',
 '两张沿原造型改为独立源板，减少背景干扰；一台黄绿救援工具机、一台青绿/象牙/朱红吊装机，共享墨线与块面阴影，但没有统一洗色。',
 '源板的后视/收拢小图是绘制研究，不能独自证明同件工程正交、受力或连续机构运动。'
],runtime_tested=False,new_images_user_accepted=False)
record=dict(date='2026-10-23',revision='public-works-source-r1',existing_batch='design-followthrough-r1.json',reader=READER,status='next_batch_source_candidates',generation_mode='built-in image_gen',previous_confirmed_design_delivery='confirmed-design-handoff-20261023.json',items=items,historical_attempts=history,author_review=review,
    experience=dict(start='在城市修复/撤离和吊装局面中，需要可辨认的两类职业机。',input='原机设与当前Canon对照，先出源板，再局部修正备件/吊钩收纳。',visible_consequence='预算二号工具/替换件与吊装机作业/收拢形态可比较。',next='依据具体源稿继续收敛，后续沿选定主形补多视、模型与工作动作。'),
    limits=['本批仅源设计工序；未启动或改写主工程，正常战棋镜头、连续动作、声音与原生输入不在本次实测范围。','新两张源稿未获用户采用；不改变已确定设计或当前故事/工作能力规则。'],canon_changed=False,runtime_assets_modified=False,handoff_sent=False)
write(RECORD,record)
write(PROMPTS,dict(mode='built-in image_gen',items=[dict(id=x['id'],files=x['prompts'],reference_roles=x['source_refs']) for x in items]))
sections=''.join(f'<section id="{x["id"]}"><h2>{x["name"]}</h2><p>{x["role"]}</p><a href="{x["file"]}"><img src="{x["file"]}" alt="{x["name"]}整机与作业结构首稿"></a><p><a href="{x["file"]}">原尺寸源图</a></p><details><summary>沿用的原设计参考</summary><img src="{x["source_refs"][0]["file"]}" alt="{x["name"]}原设计参考"></details></section>' for x in items)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>下一批｜预算二号与市政吊装机</title><style>body{margin:0;background:#eeeae0;color:#183647;font:16px/1.8 system-ui}main{max-width:1500px;margin:auto;padding:26px}a{color:#12617c}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,42px);line-height:1.3}h2{margin-top:36px}img{width:100%;height:auto;display:block;background:#faf8f0}.scope{padding:12px 18px;background:#faf7ed;border-left:4px solid #b9a322}.note{font-size:14px;color:#526d75}details{margin-top:16px}section{padding-bottom:24px;border-bottom:1px solid #ccd0c5}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="confirmed-design-handoff-20261023.html">已确定设计交付单</a><a href="public-works-source-20261023-r1.zip">源图与内置生图提示词包</a></nav><h1>下一批：城市职业机</h1><p class="scope">沿原有造型细化。预算二号突出维修工具、通用替换件和低成本维护；市政吊装机突出吊臂、履带、稳定腿及收拢姿态。</p>'''+sections+'''<p class="note">两张为本批新源稿。隐藏支腿、结构尺寸与连续作业仍需后续多视/模型核对；已确定设计的交付与主工程接入另有记录。</p><p><a href="public-works-source-prompts-r1.json">实际内置生图提示词</a> · <a href="public-works-source-production-r1.json">源文件与实际查看记录</a></p></main></body></html>'''
(OUT/READER).write_text(page)
ledger=read('design-followthrough-r1.json');ledger['latest_public_works_source']=RECORD;ledger['production_focus'].update(current_step='预算二号/市政吊装机首稿已绘制、实际查看并局部修正备件与收拢吊钩；源板和提示词包已整理。',next='沿源稿收敛主形；后续多视与工作动作/模型仍分别检查。')
ledger['experience_record_public_works_r1']=dict(classification='experience',record=RECORD,original_requirement=['M06','M07','V353U032','V353U031'],actual_artifacts=[x['file'] for x in items],start=record['experience']['start'],input=record['experience']['input'],visible_consequence=record['experience']['visible_consequence'],author_review=RECORD+'#author_review',independent_review=False,new_images_user_accepted=False,runtime_changed=False,next=record['experience']['next'])
ledger['defect_ledger'].append(dict(id='ART-PUBLIC-WORKS-DETAIL-R1',defect='预算二号箱内配件似头部，吊装机收拢态吊钩未固定。',attempts=[dict(files=[x['file'] for x in history],observed=True,outcome='persists',result='首稿有上述局部功能细节问题。'),dict(files=[x['file'] for x in items],observed=True,outcome='author_observed_source_detail_improvement',result='箱内改泵/电机模块，收拢钩改靠固定座；主形保持。',evidence=RECORD)],method_changes=[dict(status='applied',old='一张源板同时生成主机和细节。',new='以实际源板作编辑目标，只局部改配件/固定点，不重造整机。',applied_evidence=RECORD)],closed=False,remaining='隐藏支腿、机构尺寸与动作仍由多视/同件模型核对。'))
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_public_works_source']=RECORD;write('sample-author-review.json',author)
notes='预算二号与市政吊装机首轮源设计：沿原主形细化维修工具/替换件与吊装/稳定/收拢结构。内置image_gen生成，R1b局部修正。此包为二维候选源图，不代签模型、动作、受力或运行。\n';(OUT/'public-works-source-notes-r1.txt').write_text(notes)
files=[x['file'] for x in items]+[f for x in items for f in x['prompts']]+[r['file'] for x in items for r in x['source_refs']]+[RECORD,PROMPTS,'public-works-source-notes-r1.txt']
manifest=dict(revision='public-works-source-delivery-r1',files=[dict(file=f,sha256=sha(OUT/f)) for f in dict.fromkeys(files)],new_images_user_accepted=False,runtime_replaced=False);write('public-works-source-delivery-manifest-r1.json',manifest)
with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for f in list(dict.fromkeys(files))+['public-works-source-delivery-manifest-r1.json']:z.write(OUT/f,arcname=f)
with zipfile.ZipFile(OUT/ZIP) as z:
    assert z.testzip() is None
    for x in manifest['files']:assert hashlib.sha256(z.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps(dict(reader=str(OUT/READER),source_package=str(OUT/ZIP),new_source_boards=len(items),user_accepted=False),ensure_ascii=False))
