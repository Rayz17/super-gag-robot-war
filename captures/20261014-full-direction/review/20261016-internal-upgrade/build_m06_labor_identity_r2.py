"""Continue M06 source exploration in the existing art batch; no runtime writes."""
from pathlib import Path
import hashlib, html, json, shutil, sys, zipfile
from PIL import Image

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parents[3]
RECORD = 'M06-labor-identity-production-r2.json'
READER = 'M06-labor-identity-r2.html'
PROMPTS = ['M06-labor-identity-prompt-r2.txt', 'M06-labor-identity-correction-prompt-r2b.txt']
def read(name): return json.loads((OUT/name).read_text())
def write(name, value): (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def copy(source, target):
    if target.exists(): assert sha(source) == sha(target), 'Versioned source already differs'
    else: shutil.copyfile(source, target)

final = Path(sys.argv[1]).resolve()
if (OUT/'M06-design-fixed-20261023-r2.json').exists():
    acceptance=read('M06-design-fixed-20261023-r2.json')
    selected=acceptance['selected_master']
    assert sha(OUT/selected['file'])==selected['sha256']
    assert sha(final)==selected['sha256'], 'Accepted source cannot be replaced by a different image'
    print(json.dumps({'accepted_receipt_preserved':'M06-design-fixed-20261023-r2.json','source_sha256':selected['sha256']},ensure_ascii=False))
    raise SystemExit(0)
first = Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470/exec-3b6d901e-ac1c-40dd-930d-1e980fd35663.png')
target = OUT/'samples/M06-labor-identity-r2b.png'
attempt = OUT/'samples/M06-labor-identity-attempt-r2.png'
copy(final, target); copy(first, attempt)
prior = read('public-works-source-production-r1.json')
m06 = next(x for x in prior['items'] if x['id'] == 'M06')
m07 = next(x for x in prior['items'] if x['id'] == 'M07')
assert sha(OUT/m07['file']) == m07['sha256']
with Image.open(target) as im: pixels, mode = list(im.size), im.mode
sources = [
    {'kind':'current_canon','file':'docs/superpowers/specs/data/canon/entities.tsv','row':'V353U032','use':'低费修复、撤离和补给，以廉价替代件完成高价值工程'},
    {'kind':'project_ip_research','file':'docs/superpowers/specs/data/research/robot_ip_deep_dossier_pool_v1.tsv','row':'IPD016','use':'工务机动队投射Patlabor；城市劳动、维修、预算与公共空间'},
    {'kind':'accepted_story','file':'docs/superpowers/specs/剧情梗概/V35.9/rebuild/reader/C03-章节连续阅读稿.md','anchor':'预算二号的背架连着三代不同的旧电路','use':'供能背架与转接能力有故事依据；具体卷盘、三种接口外形是本轮候选实现'},
    {'kind':'official_ip','url':'https://patlabor.tokyo/','use':'Labor是进入各行业的通用人形作业机械'},
    {'kind':'official_ip_mecha','url':'https://patlabor.tokyo/mechanic/689/','use':'官方说明二号机头部与维修替换件有关；借用零件历史塑造外形的方法，不投射或复制该单机身份'},
    {'kind':'official_licensed_model','url':'https://www.goodsmile.com/ja/product/7467/MODEROID%2B%E3%83%96%E3%83%AB%E3%83%89%E3%83%83%E3%82%B0%E3%82%BB%E3%83%83%E3%83%88','use':'核实Bulldog作为作业Labor的产品说明；未成功取得照片，未作为已查看图片或图生输入'}
]
item = dict(id='M06',name='预算二号救援机',canon_entity='V353U032',file=target.relative_to(OUT).as_posix(),sha256=sha(target),generated_source=str(final),pixel_size=pixels,mode=mode,user_accepted=False,runtime_integrated=False,
    role='市政维修与应急供能；廉价旧件维持关键公共服务',
    source_refs=[{'file':m06['file'],'sha256':m06['sha256'],'role':'继承配色、替换腿侧别及成人厚实体态；旧头和通用铠甲不再作为本轮目标'},
                 {'file':'samples/M14-front-airframe-r6.png','sha256':sha(OUT/'samples/M14-front-airframe-r6.png'),'role':'仅取项目墨线与块面阴影，不取航空机体身份、比例或配色'}])
record = dict(date='2026-10-23',revision='M06-labor-identity-r2',existing_batch='design-followthrough-r1.json',reader=READER,status='candidate_not_user_accepted',generation_mode='built-in image_gen',items=[item],source_basis=sources,
    user_feedback='预算二号的ip投射是什么，这个头有点丑，然后机设上没有特色，有没有结合ip自身的特点来确定设计语言',
    interpretation={'confirmed':'工务机动队主要投射Patlabor；预算二号本身未指定等同某一台原作机体。','design_proposal':'市政维修老兵：作业护盔、可检修躯体、替换件与三代供能适配背架。'},
    head_options=[{'id':'A','direction':'安全作业盔、分离双目和白色护颌；整机采用的研究方向','author_recommendation':True},{'id':'B','direction':'焊接护罩方案；是否作为A的可动附件仍须设计确认'},{'id':'C','direction':'设备式救援传感头，提供更强机械感的备选'}],
    historical_attempt={'file':attempt.relative_to(OUT).as_posix(),'sha256':sha(attempt),'issue':'头部放大图通讯模块的物理侧别与主图不一致'},
    author_review={'reviewer':'author','independent_review':False,'actual_media':[target.relative_to(OUT).as_posix()],'record':'M06-labor-identity-author-review-r2.json','user_accepted':False,'runtime_tested':False},
    experience={'start':'玩家需要从外形读出预算二号是维修、撤离与供能职业机。','input':'以当前Canon、IP研究和已接受C03供能行动重新组织头部、检修躯体与背架。','visible_consequence':'护盔、胸部检修舱、双目、替换色小腿、救援夹具及卷盘/三制式接口形成具体识别点。','next':'沿本轮候选收敛头部与整机，再补同形正侧背；实际工作动作和运行另验。'},
    limits=['本轮是源设计候选，具体接口、胸部舱盖和夹具外形尚未获采用。','背架接三代旧电路的职责来自当前故事；未据此增加新技能、数值或剧情。','二维研究图不能证明受力、线缆收放、操纵舱空间或完整机构运动。'],
    unchanged_m07={'file':m07['file'],'sha256':m07['sha256']},prompts=PROMPTS,canon_changed=False,runtime_assets_modified=False,handoff_sent=False)
write(RECORD, record)
write('M06-labor-identity-prompts-r2.json',{'mode':'built-in image_gen','prompts':PROMPTS,'input_images':item['source_refs'],'local_correction_target':record['historical_attempt']})
links=''.join('<li>'+html.escape(x['use'])+' '+(f'<a href="{x["url"]}">官方来源</a>' if 'url' in x else f'<code>{html.escape(x["file"])}#{html.escape(x.get("row",x.get("anchor","")))}</code>')+'</li>' for x in sources)
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>预算二号｜城市维修与供能 R2</title><style>body{margin:0;background:#eeeae0;color:#183647;font:16px/1.8 system-ui}main{max-width:1536px;margin:auto;padding:26px}a{color:#12617c}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,42px);line-height:1.3}img{width:100%;height:auto;display:block;background:#faf8f0}section{margin-top:28px}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #bcc9c7;text-align:left;padding:10px}code{overflow-wrap:anywhere;font-size:12px}.scope{padding:12px 18px;background:#faf7ed;border-left:4px solid #bd9d24}details{padding:14px 0}.note{font-size:14px;color:#526d75}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="public-works-source-r1.html#M07">市政吊装机当前稿</a><a href="M06-labor-identity-source-20261023-r2.zip">源图与提示词包</a></nav><h1>预算二号：城市维修老兵</h1><p class="scope">所属工务机动队主要投射《机动警察》的城市职业机。上一稿只沿旧黄绿工具机造型细化，职业结构与记忆点不足。本轮将已定故事里的“三代旧电路同时供能”转为整机语言。</p><section id="M06"><a href="samples/M06-labor-identity-r2b.png"><img src="samples/M06-labor-identity-r2b.png" alt="预算二号R2整机、安全作业盔三方向及卷盘供能背架研究"></a><p>A为整机使用的研究头型；B为焊接护罩方向，C为救援传感器方向。尚未固定新头型或整机。</p></section><section><table><thead><tr><th>部位</th><th>设计取舍</th><th>它说明什么</th></tr></thead><tbody><tr><td>头部</td><td>有纵向体积的作业护盔、白色眉护、双目、保护颌</td><td>观察清楚、可靠、有经验的职业机</td></tr><tr><td>躯体</td><td>带搭扣的检修舱盖、圆角壳板、关节防尘套</td><td>能够维护和换件的工作设备</td></tr><tr><td>背架</td><td>电缆卷盘与三种制式接口</td><td>连接不同年代的设备，坚持供能</td></tr><tr><td>四肢与工具</td><td>一条替换色小腿、通用安装点、紧凑救援夹具</td><td>廉价替换件仍能完成有价值的救援</td></tr></tbody></table></section><details><summary>上一稿对照</summary><img src="samples/M06-public-works-master-r1b.png" alt="预算二号R1旧稿，通用铠甲头身和大型工具"></details><details><summary>IP与故事依据、候选边界</summary><ul>'''+links+'''</ul><p>具体护盔、接口外形与夹具是本轮候选。未把单一原作机体等同于预算二号，也未增加新剧情或玩法。</p></details><p class="note">已实际查看二维源图；新设计待采用，同模型多视、连续作业、声音与运行另验。市政吊装机和已确定资产保持原来源。</p><p><a href="M06-labor-identity-prompts-r2.json">内置生图提示词</a> · <a href="M06-labor-identity-production-r2.json">来源与制作记录</a></p></main></body></html>'''
(OUT/READER).write_text(page)
ledger=read('design-followthrough-r1.json')
ledger['latest_m06_labor_identity_source']=RECORD
ledger['production_focus'].update(current_step='预算二号按Patlabor职业机与已定C03三代供能行动重画整机、A/B/C头部及背架；通讯模块侧别作局部修正，实际结果见本轮作者查看记录。',next=record['experience']['next'])
ledger['experience_record_m06_labor_identity_r2']={'classification':'experience','record':RECORD,'original_requirement':['M06','V353U032','IPD016','current user feedback'],'actual_artifacts':[item['file']],'start':record['experience']['start'],'input':record['experience']['input'],'visible_consequence':record['experience']['visible_consequence'],'author_review':'M06-labor-identity-author-review-r2.json','independent_review':False,'new_images_user_accepted':False,'runtime_changed':False,'next':record['experience']['next']}
defect=next(x for x in ledger['defect_ledger'] if x['id']=='ART-M06-IP-IDENTITY-20261023')
if not any(x.get('evidence')==RECORD for x in defect['attempts']):
    defect['attempts'].append({'files':[item['file']],'observed':True,'observer':'author','outcome':'author_observed_occupational_features_added','result':'作业盔、检修舱、卷盘/三制式接口和救援夹具进入机体；新稿未获用户采用。','evidence':RECORD})
defect['method_changes'][0].update(status='applied',applied_evidence=RECORD)
defect['remaining']='整机及新头型待用户采用，隐面与机构仍需后续核对；不以作者观察关闭。'
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_m06_labor_identity_source']=RECORD;write('sample-author-review.json',author)
files=[item['file'],RECORD,*PROMPTS,'M06-labor-identity-prompts-r2.json','M06-labor-identity-author-review-r2.json']+[x['file'] for x in item['source_refs']]
for f in files: assert (OUT/f).is_file(),f
manifest={'revision':'M06-labor-identity-r2','files':[{'file':f,'sha256':sha(OUT/f)} for f in files],'user_accepted':False,'runtime_assets_modified':False}
write('M06-labor-identity-delivery-manifest-r2.json',manifest)
with zipfile.ZipFile(OUT/'M06-labor-identity-source-20261023-r2.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files+['M06-labor-identity-delivery-manifest-r2.json']: z.write(OUT/f,f)
with zipfile.ZipFile(OUT/'M06-labor-identity-source-20261023-r2.zip') as z:
    assert z.testzip() is None
    for x in manifest['files']: assert hashlib.sha256(z.read(x['file'])).hexdigest()==x['sha256']
print(json.dumps({'source':str(target),'reader':str(OUT/READER),'source_package':str(OUT/'M06-labor-identity-source-20261023-r2.zip'),'user_accepted':False},ensure_ascii=False))
