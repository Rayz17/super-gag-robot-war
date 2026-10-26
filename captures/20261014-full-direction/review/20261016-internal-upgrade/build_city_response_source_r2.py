"""Continue M09/M10 source designs after the user's two distinct corrections."""
from pathlib import Path
import hashlib,json,shutil,sys,zipfile
from PIL import Image

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='city-response-source-production-r2.json'
READER='city-response-source-r2.html'
ZIP='city-response-source-20261023-r2.zip'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(source,target):
    if target.exists():assert sha(source)==sha(target),'Versioned source already differs'
    else:shutil.copyfile(source,target)

if (OUT/'city-response-design-fixed-20261023-r2.json').exists():
    accepted=read('city-response-design-fixed-20261023-r2.json')
    for item in accepted['files']:
        assert sha(OUT/item['file'])==item['sha256'], 'Accepted city source changed'
    print(json.dumps({'accepted_source_preserved':accepted['files']},ensure_ascii=False))
    raise SystemExit(0)

adoption={x['id']:x for x in read('adoption-manifest.json')['records']}
items=[]
for ident,name,entity,origin,file,role,prompt in [
    ('M09','灰崎警备劳务机','V353U033',Path(sys.argv[1]).resolve(),'M09-curved-labor-r2.png','城市非致命警备、交通封控与六面隔离墙','M09-curved-labor-surface-prompt-r2.txt'),
    ('M10','消防架桥机','V353U034',Path(sys.argv[2]).resolve(),'M10-engineering-transformer-r2.png','双足工程变形机／消防架桥载具的视觉提案','M10-engineering-transformer-prompt-r2.txt')]:
    target=OUT/'samples'/file;copy(origin,target)
    with Image.open(target) as im:size,mode=list(im.size),im.mode
    items.append(dict(id=ident,name=name,canon_entity=entity,role=role,file=target.relative_to(OUT).as_posix(),sha256=sha(target),pixel_size=size,mode=mode,generated_source=str(origin),prompt=prompt,user_accepted=False,runtime_integrated=False,handoff_sent=False,existing_consumer_refs=adoption[ident]['current_assets']))
histories=[]
for ident,origin,name,reason in [
    ('M09','exec-67f427db-4e20-4063-b595-b79567e83f3d.png','M09-wall-count-attempt-r1.png','首稿背上六面加手持一面，数量误为七'),
    ('M09','exec-9635f65b-78b5-4045-9e82-a7e45b961e9f.png','M09-patrol-master-r1b.png','用户肯定头部/配色，但要求躯体壳面改成Patlabor曲面语言'),
    ('M10','exec-f2cd65dd-4d46-417d-9a4a-a2ab9651ea97.png','M10-rejected-quad-apparatus-r1.png','用户明确否定四足主形并要求工程类变形金刚设计')]:
    target=OUT/'samples'/name;copy(GEN/origin,target)
    histories.append(dict(id=ident,file=target.relative_to(OUT).as_posix(),sha256=sha(target),reason=reason,current_source=False))
source_refs=[]
edit_target=OUT/'samples/M09-patrol-master-r1b.png'
source_refs.append(dict(id='M09',file=edit_target.relative_to(OUT).as_posix(),sha256=sha(edit_target),role='本轮M09曲面修改的直接目标；用户肯定头部与配色的指定图'))
for ident in ['M09','M10']:
    source=ROOT/'captures/20261014-full-direction'/adoption[ident]['image']
    target=OUT/'refs'/f'{ident}-city-response-original-20261023.jpg';copy(source,target)
    source_refs.append(dict(id=ident,file=target.relative_to(OUT).as_posix(),sha256=sha(target),role='原有身份/部件参考；不以旧图覆盖用户新要求或当前故事'))
for file,url,role in [
    ('refs/M09-patlabor-official-20261023.png','https://patlabor.tokyo/mechanic/689/','官方Patlabor外壳曲面与关节参考；不取原头、纹章或黑白涂装'),
    ('refs/M10-grapple-official-01-20261023.jpg','https://tf.takaratomy.co.jp/products-lineup/tf_mp/mp-35','官方Grapple载具部件组织参考；不复制头脸、具体造型或商标'),
    ('samples/M06-front-r3.png','M06-turnaround-design-fixed-20261023-r3.json','已确定项目墨线/块面与成人比例参考，不复制机体身份')]:
    source_refs.append(dict(file=file,sha256=sha(OUT/file),source=url,role=role))
record=dict(date='2026-10-23',revision='city-response-source-r2',existing_batch='design-followthrough-r1.json',reader=READER,status='source_candidates_after_user_feedback',generation_mode='built-in image_gen',items=items,historical_attempts=histories,source_refs=source_refs,
    authority_basis=[{'source':'docs/superpowers/specs/data/canon/entities.tsv','ids':['V353U033','V353U034'],'use':'警务/封控与消防/架桥/降温职业职责'},{'source':'docs/superpowers/specs/data/research/robot_ip_deep_dossier_pool_v1.tsv','id':'IPD016','use':'Patlabor城市职业机体系，不能用通用军事杂兵替代'},{'source':'docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C01-闭馆以后万机出击.md','anchor':'橙白色消防架桥机、倒车、四条稳定腿和背部桥板','use':'保留橙白消防、架桥与支撑；不得把稳定腿硬解释为四足主形'},{'source':'docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C03-章节连续阅读稿.md','anchor':'灰崎六面交通墙、消防水幕与热障','use':'配件服务具体职业动作'}],
    latest_user_feedback={'M09':read('design-followthrough-r1.json')['latest_m09_user_feedback'],'M10':read('design-followthrough-r1.json')['latest_m10_user_feedback']},
    interpretation={'M09':'保留用户肯定的头部/灰白配色/身形/六墙，专改肩胸臂腿的连续曲面和结构线。','M10':'按用户最新要求重做工程变形语言：正常双足人形和消防架桥载具；四支腿只作车辆施工支撑。车型、轮组和部件对应为候选设计，不自动增加剧情或玩法。'},
    author_review='city-response-author-review-r2.json',
    experience={'start':'下一批城市职业机需要从形态上读出交通封控与消防架桥两种职责。','input':'沿M09已肯定局部改曲面；撤回M10四足主形，参考工程变形机重组人形/车型/工作形态。','visible_consequence':'两张源板分别展示头部/交通墙/携行关系与双足人形/载具/稳定支腿作业关系。','next':'用户采用整机方向后直接补正侧背，不只登记后停；隐藏结构和模型/动作仍另验。'},
    pending_previous_batch=[{'id':'M07','file':'samples/M07-public-works-master-r1b.png','state':'原源板保留，未扩大为多视/模型完成'}],
    limits=['本批新图为源设计候选，M09头部/配色的正面反馈不自动等于全图采用。','M10变形、桥面受力/收纳、支腿和水路是视觉提案，未由同件机构或连续动作验证。','主工程模型、战棋镜头、规则、声音与运行未改。'],canon_changed=False,runtime_assets_modified=False,handoff_sent=False)
write(RECORD,record)
prompts=['M09-curved-labor-surface-prompt-r2.txt','M10-engineering-transformer-prompt-r2.txt']
write('city-response-prompts-r2.json',dict(mode='built-in image_gen',current_prompts=prompts,history_prompts=['M09-city-response-master-prompt-r1.txt','M09-wall-count-correction-prompt-r1b.txt','M10-city-response-master-prompt-r1.txt'],reference_roles=source_refs))
sections=''.join(f'<section id="{x["id"]}"><h2>{x["name"]}</h2><p>{record["interpretation"][x["id"]]}</p><a href="{x["file"]}"><img src="{x["file"]}" alt="{x["name"]}修订源板与职业结构研究"></a><p><a href="{x["file"]}">原尺寸源图</a></p></section>' for x in items)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>灰崎与消防架桥机｜下一批修订源板</title><style>body{margin:0;background:#eeeae0;color:#183647;font:16px/1.8 system-ui}main{max-width:1600px;margin:auto;padding:24px}a{color:#12617c}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,42px);line-height:1.3}img{display:block;width:100%;height:auto;background:#fff}section{margin-top:32px;border-top:1px solid #c5cec8;padding-top:16px}.scope{padding:12px 18px;background:#faf7ed;border-left:4px solid #bd9d24}.note{font-size:14px;color:#526d75}details{margin:24px 0}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="M06-turnaround-r3.html">已确定预算二号三视</a><a href="city-response-source-20261023-r2.zip">两机源图与提示词</a></nav><h1>灰崎：曲面职业机；消防：工程变形机</h1><p class="scope">按用户两条具体反馈分别修订。灰崎保留头部/配色，只调整躯体曲面；消防撤回四足主形，改正常双足人形与消防架桥载具。</p>'''+sections+'''<details><summary>实际参考与取舍</summary><p>灰崎参考<a href="https://patlabor.tokyo/mechanic/689/">Patlabor官方图</a>的曲面外壳与关节处理；消防参考<a href="https://tf.takaratomy.co.jp/products-lineup/tf_mp/mp-35">Grapple官方图</a>的载具部件组织。头部、色彩与职业职责按本项目和用户本轮要求取舍。</p><p>消防“四条稳定腿”服务车辆工作姿态。旧四足主形已撤回，不作为后续建模来源。旧三段桥/SEG3等历史规格未抬回当前约束。</p></details><p class="note">当前是新源板；具体新图与变形/承重机构、模型、动作和运行分别判断。采用方向后直接补三视。市政吊装机原稿的多视缺口仍在原台账保留。</p><p><a href="city-response-source-production-r2.json">来源与制作记录</a> · <a href="city-response-author-review-r2.json">实际查看记录</a> · <a href="city-response-prompts-r2.json">内置生图提示词</a></p></main></body></html>'''
(OUT/READER).write_text(page)
review=read('city-response-author-review-r2.json')
ledger=read('design-followthrough-r1.json');ledger['latest_city_response_source']=RECORD
ledger['production_focus'].update(current_step='已按用户最新反馈绘制灰崎曲面修订与消防双足工程变形修订源板，实际查看记录与保留项见本批。',next=record['experience']['next'])
ledger['experience_record_city_response_r2']={'classification':'experience','record':RECORD,'original_requirement':['M09','M10','V353U033','V353U034','latest user feedback'],'actual_artifacts':[x['file'] for x in items],**record['experience'],'author_review':record['author_review'],'independent_review':False,'new_images_user_accepted':False,'runtime_changed':False}
m10=next(x for x in ledger['defect_ledger'] if x['id']=='ART-M10-QUAD-MAIN-SILHOUETTE-20261023')
m10['method_changes'][0].update(status='applied',applied_evidence=RECORD)
if not any(x.get('evidence')==RECORD for x in m10['attempts']):m10['attempts'].append({'files':[items[1]['file']],'observed':True,'observer':'author','outcome':'author_observed_new_biped_and_vehicle_design','result':review['M10_result'],'evidence':RECORD})
m10['remaining']='新稿尚未获采用；变形/支腿/桥面机构与连续作业仍需后续核对。'
ident='ART-M09-CURVED-SURFACES-20261023'
if not any(x['id']==ident for x in ledger['defect_ledger']):ledger['defect_ledger'].append({'id':ident,'defect':'头部和配色获得肯定，但躯体碎折角与军用装甲感过强，Patlabor曲面壳体语言不足。','attempts':[{'files':['samples/M09-patrol-master-r1b.png'],'observed':True,'observer':'human user','outcome':'persists','result':'用户明确要求更多曲面和Patlabor机体线条。'},{'files':[items[0]['file']],'observed':True,'observer':'author','outcome':'author_observed_surface_revision','result':review['M09_result'],'evidence':RECORD}],'method_changes':[{'status':'applied','old':'沿原铠甲切面补细节。','new':'保持头/色/比例，肩胸前臂胫甲改连续模压曲面，交通墙保持平板结构。','applied_evidence':RECORD}],'closed':False,'remaining':'新曲面源图待采用；六墙数量/部件与隐藏面仍逐图核对。'})
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_city_response_source']=RECORD;write('sample-author-review.json',author)
files=[x['file'] for x in items]+prompts+['M09-city-response-master-prompt-r1.txt','M09-wall-count-correction-prompt-r1b.txt','M10-city-response-master-prompt-r1.txt']+[RECORD,'city-response-prompts-r2.json',record['author_review']]+[x['file'] for x in source_refs]
files=list(dict.fromkeys(files))
manifest={'revision':'city-response-source-r2','files':[{'file':f,'sha256':sha(OUT/f)} for f in files],'new_images_user_accepted':False,'runtime_assets_modified':False}
write('city-response-delivery-manifest-r2.json',manifest)
with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files+['city-response-delivery-manifest-r2.json']:z.write(OUT/f,f)
with zipfile.ZipFile(OUT/ZIP) as z:
    assert z.testzip() is None
    for x in manifest['files']:assert hashlib.sha256(z.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps({'reader':str(OUT/READER),'source_files':[x['file'] for x in items],'zip':str(OUT/ZIP)},ensure_ascii=False))
