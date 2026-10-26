"""Package authorized M06 source views without changing the selected master or runtime."""
from pathlib import Path
import hashlib, json, shutil, sys, zipfile
from PIL import Image

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
GEN=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470')
RECORD='M06-turnaround-production-r3.json'
READER='M06-turnaround-r3.html'
ZIP='M06-turnaround-source-20261023-r3.zip'
def read(name):return json.loads((OUT/name).read_text())
def write(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def copy(source,target):
    if target.exists():assert sha(source)==sha(target),'Versioned output changed'
    else:shutil.copyfile(source,target)

selected=read('M06-design-fixed-20261023-r2.json')['selected_master']
assert sha(OUT/selected['file'])==selected['sha256']
if (OUT/'M06-turnaround-design-fixed-20261023-r3.json').exists():
    acceptance=read('M06-turnaround-design-fixed-20261023-r3.json')
    for item in acceptance['files']:assert sha(OUT/item['file'])==item['sha256']
    side=next(x for x in acceptance['files'] if x['id']=='SIDE')
    assert sha(Path(sys.argv[1]))==side['sha256'], 'Accepted side source cannot be replaced'
    print(json.dumps({'accepted_receipt_preserved':'M06-turnaround-design-fixed-20261023-r3.json'},ensure_ascii=False))
    raise SystemExit(0)
jobs=[('FRONT','正面','exec-c079e1c5-1dbb-4967-b5fe-e35af3c1f531.png','M06-front-r3.png'),('SIDE','左侧面',str(Path(sys.argv[1]).resolve()),'M06-side-r3c.png'),('REAR','背面','exec-8e9db4a6-e8a3-4274-b56c-f45ca3189d01.png','M06-rear-r3.png')]
items=[]
for ident,label,source,name in jobs:
    source=Path(source) if Path(source).is_absolute() else GEN/source
    target=OUT/'samples'/name;copy(source,target)
    with Image.open(target) as im:size,mode=list(im.size),im.mode
    items.append(dict(id=ident,label=label,file=target.relative_to(OUT).as_posix(),sha256=sha(target),pixel_size=size,mode=mode,generated_source=str(source),derived_under_user_authorization=True,user_accepted=False,runtime_integrated=False,handoff_sent=False))
attempt=OUT/'samples/M06-side-oblique-attempt-r3.png'
copy(GEN/'exec-78ccaf65-7fb1-4955-858b-a2b166dc0c6e.png',attempt)
intermediate=OUT/'samples/M06-side-projection-attempt-r3b.png'
copy(GEN/'exec-ad03407a-4593-4690-b6cb-ac4174738a50.png',intermediate)
prompts=[f'M06-{view}-turnaround-prompt-r3.txt' for view in ['front','side','rear']]+['M06-side-projection-correction-prompt-r3b.txt','M06-side-components-projection-prompt-r3c.txt']
review=read('M06-turnaround-author-review-r3.json')
record=dict(date='2026-10-23',revision='M06-turnaround-r3',asset='预算二号正侧背三视源图',canon_entity='V353U032',generation_mode='built-in image_gen',existing_batch='design-followthrough-r1.json',parent=selected,source_acceptance_receipt='M06-design-fixed-20261023-r2.json',user_request='直接做三视图啊',reader=READER,items=items,
    side_standard={'radio':'机体右耳：前视观看者左，背视观看者右；左侧面近耳为青绿盖，白模块在远侧','replacement_leg':'机体左小腿：前视观看者右，背视观看者左','held_tool':'机体左手：前视观看者右，背视观看者左','waist':'机体右腰工具箱，左腰供能接头'},
    prompts=prompts,prompt_index='M06-turnaround-prompts-r3.json',author_review='M06-turnaround-author-review-r3.json',
    attempts=[{'file':attempt.relative_to(OUT).as_posix(),'sha256':sha(attempt),'role':'侧面首稿有斜角，不作当前侧面源'},{'file':intermediate.relative_to(OUT).as_posix(),'sha256':sha(intermediate),'role':'侧姿已收正，但卷盘与夹具侧面投影仍需局部修正'}],
    experience={'start':'已采用预算二号R2主形与A头型，需要完整正侧背表达职业机部件与前后结构。','input':'按同一母稿分别绘制正/左侧/背；首侧稿有斜角，改以新正面为比例和侧别依据重绘左侧，再按背面核卷盘轴向与夹具侧厚。','visible_consequence':'三张独立源图能对照头部体积、替换腿、左手夹具与卷盘/三制式背架。','next':'沿当前三视继续分件/模型和工作动作；新源图派生与机构/运行分别验证。'},
    limits=['本批为二维源图派生，不是同一三维模型的机械正交投影。','整机/A头型沿已确定母稿，新增三图未冒充新的逐图用户验收。','隐藏机构、驾驶舱空间、线缆收放、工具受力和连续动作仍需制作核对。'],new_images_user_accepted=False,canon_changed=False,runtime_assets_modified=False,handoff_sent=False)
write(RECORD,record)
write('M06-turnaround-prompts-r3.json',{'mode':'built-in image_gen','parent':selected,'prompts':prompts,'side_correction_primary_reference':items[0]['file']})
cards=''.join(f'<article id="{x["id"]}"><h2>{x["label"]}</h2><a href="{x["file"]}"><img src="{x["file"]}" alt="预算二号{x["label"]}，沿A头型与R2整机派生"></a><p><a href="{x["file"]}">原尺寸源图</a></p></article>' for x in items)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>预算二号｜正侧背三视</title><style>body{margin:0;background:#eeeae0;color:#183647;font:16px/1.8 system-ui}main{max-width:1750px;margin:auto;padding:24px}a{color:#12617c}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,42px);line-height:1.3}.views{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}img{display:block;width:100%;height:auto;background:#fff}h2{font-size:20px;margin-bottom:10px}.scope{padding:12px 18px;background:#faf7ed;border-left:4px solid #bd9d24}.note{font-size:14px;color:#526d75}details{margin-top:26px}@media(max-width:800px){.views{grid-template-columns:1fr}}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="M06-labor-identity-r2.html">已确定整机与A头型</a><a href="M06-turnaround-source-20261023-r3.zip">三视源图与提示词包</a></nav><h1>预算二号：正面、左侧面、背面</h1><p class="scope">沿已确定A作业盔与R2整机展开。通讯模块在机体右耳，青绿替换件在左小腿，夹具由左手持握；保留检修舱、防尘套和卷盘/三制式供能背架。</p><section class="views">'''+cards+'''</section><details><summary>已确定母稿</summary><img src="samples/M06-labor-identity-r2b.png" alt="预算二号已确定R2整机、A头型与供能背架母稿"></details><p class="note">本批按授权交付二维三视源图；同件模型、隐藏机构和连续工作动作另验。源设计母稿保持原文件。</p><p><a href="M06-turnaround-production-r3.json">制作与来源</a> · <a href="M06-turnaround-prompts-r3.json">内置生图提示词</a> · <a href="M06-turnaround-author-review-r3.json">实际查看记录</a></p></main></body></html>'''
(OUT/READER).write_text(page)
ledger=read('design-followthrough-r1.json')
ledger['latest_m06_turnaround']=RECORD
ledger['production_focus'].update(current_step='已沿确定R2整机/A头型交付独立正面、修正左侧面与背面源图；实际比例和侧别查看见本批记录。',next=record['experience']['next'])
ledger['experience_record_m06_turnaround_r3']={'classification':'experience','record':RECORD,'original_requirement':['M06','V353U032','CML143','直接做三视图啊'],'actual_artifacts':[x['file'] for x in items],**record['experience'],'author_review':record['author_review'],'independent_review':False,'new_images_user_accepted':False,'runtime_changed':False}
ident='ART-M06-SIDE-PROJECTION-R3'
defect=next((x for x in ledger['defect_ledger'] if x['id']==ident),None)
if defect is None:
    defect={'id':ident,'defect':'首侧稿带三分之四斜角，胸口/双脚露出过多；近侧腰模块误用工具箱。','attempts':[],'method_changes':[],'closed':False}
    ledger['defect_ledger'].append(defect)
if not defect['attempts']:
    defect['attempts']=[{'files':[attempt.relative_to(OUT).as_posix()],'observed':True,'outcome':'persists','result':'首侧图实际为斜侧，腰侧件也未统一。'},{'files':[intermediate.relative_to(OUT).as_posix()],'observed':True,'outcome':'partly_corrected_components_persist','result':'主姿与左腰模块改善，卷盘轴向及夹具刃面仍未成侧面。'},{'files':[items[1]['file']],'observed':True,'outcome':'author_observed_profile_correction','result':review['side_correction_result'],'evidence':record['author_review']}]
    defect['method_changes']=[{'status':'applied','old':'正侧背各自仅用同一多视研究板生成。','new':'侧面改以本轮正面为比例/侧别锚；再限定侧面两组件、以背面判断卷盘轴向与夹具侧厚。','applied_evidence':record['author_review']}]
defect['remaining']='具体观察与剩余透视近似见作者查看记录；源图不代签同模型正交或机构。'
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_m06_turnaround']=RECORD;write('sample-author-review.json',author)
files=[x['file'] for x in items]+prompts+[RECORD,'M06-turnaround-prompts-r3.json',record['author_review'],selected['file'],'M06-design-fixed-20261023-r2.json']
manifest={'revision':'M06-turnaround-r3','files':[{'file':f,'sha256':sha(OUT/f)} for f in files],'selected_parent_unchanged':True,'new_images_user_accepted':False,'runtime_assets_modified':False}
write('M06-turnaround-delivery-manifest-r3.json',manifest)
with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files+['M06-turnaround-delivery-manifest-r3.json']:z.write(OUT/f,f)
with zipfile.ZipFile(OUT/ZIP) as z:
    assert z.testzip() is None
    for x in manifest['files']:assert hashlib.sha256(z.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps({'reader':str(OUT/READER),'source_files':[x['file'] for x in items],'zip':str(OUT/ZIP)},ensure_ascii=False))
