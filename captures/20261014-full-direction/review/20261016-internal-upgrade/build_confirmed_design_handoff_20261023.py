"""Consolidate exact accepted source files and separately marked production supports."""
from pathlib import Path
import hashlib,html,json,zipfile
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
MANIFEST='confirmed-design-handoff-20261023.json'
READER='confirmed-design-handoff-20261023.html'
ZIP='confirmed-design-source-20261023.zip'
def read(n):return json.loads((OUT/n).read_text())
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
entries={}
def add(item,asset,scope,status='confirmed_source_design'):
    f=item['file'];h=sha(OUT/f);assert h==item.get('sha256',h),f
    entries[f]=dict(file=f,sha256=h,asset=asset,scope=scope,status=status,production_authorized=True,runtime_accepted=False)
freeze=read('source-design-freeze-20261018.json')
for x in freeze['files']:add(x,x.get('identity','社勇王/勇拳/组件'),x.get('role','已确定设计'))
for x in read('mecha-source-batch-acceptance-20261021.json')['files']:add(x,'M02' if x['production_record'].startswith('M02') else 'M05','已确定当前正侧背/头部源设计')
head=read('mecha-source-decisions-20261019-r17.json')['M01'];add(dict(file=head['source'],sha256=head['sha256']),'M01','仅R16头部，整机另行收敛')
cargo=read('M11-turnaround-delivery-production-r9.json')
add(cargo['approved_master'],'M11','R8整机形象母稿')
add(cargo['selected_head_reference'],'M11','用户指定原头部父源；整机与颏甲依R8/R9')
for x in cargo['items']:add(x,'M11','已确定R8形象的R9授权修正三视','authorized_derived_support')
add(cargo['vehicle_context'],'M11','车形结构参考；不冒充完整变形通过','authorized_derived_support')
add(read('M14-design-fixed-20261022.json')['selected_master'],'M14','R4身份/音乐功能/收纳父源；表面三视依R6')
for x in read('aircraft-design-fixed-20261023-r6.json')['files']:add(x,x['asset'],'当前R6已确定三视源设计')
parent=next(x for x in read('aircraft-synthesis-production-r3.json')['items'] if x['id']=='M08');add(parent,'M08','R3身份与航空形态父源；不冒充R6新航空三视','parent_context_only')
docs=['source-design-freeze-20261018.json','mecha-source-batch-acceptance-20261021.json','mecha-source-decisions-20261019-r17.json','M11-design-fixed-20261022.json','M11-turnaround-delivery-production-r9.json','M14-design-fixed-20261022.json','aircraft-design-fixed-20261023-r6.json','aircraft-airframe-production-r6.json','aircraft-airframe-prompts-r6.json']
groups=[('社勇王、勇拳与组件；六名角色','source-design-freeze-20261018.html'),('旧拳王','M02-turnaround-r2.html'),('完全版王者：素体/全装/头部双状态','M05-turnaround-r12.html'),('货柜领袖：确定形象及派生三视','M11-source-delivery-r9.html'),('无牌：仅已定R16头部','M01-family-head-review-r14.html#head-proportion-r16'),('雷翎、歌翼：当前R6三视','aircraft-airframe-r6.html')]
manifest=dict(date='2026-10-23',revision='confirmed-design-handoff',authorization_verbatim='好的，已确定的设计可以交付给主对话，然后进行下一批',reader=READER,recipient=dict(thread_id='01a0f799-a7fc-7173-b8b2-8ce9f1c8861a',title='战斗主玩法打磨'),files=list(entries.values()),metadata_records=[dict(file=f,sha256=sha(OUT/f)) for f in docs],groups=[dict(name=a,reader=b) for a,b in groups],source_precedence=['当前各对象已确定源图及逐SHA采用回执优先','雷翎/歌翼当前为R6，R4敦实/R5过瘦和失败视向退出正向依据','社勇王整机规定轮廓/比例，部件过程图仅解释归属','无牌仅R16头部固定，不将旧整机头型或双槽长冠回流','馆守Z沿现有资产，本次没有重做'],scope='确定源设计及明确标记的授权派生/父源交付；模型、动作、声音、完整变形与运行分别由当前制作结果判断。',runtime_assets_replaced_by_sender=False,next_batch=dict(ids=['M06','M07'],names=['预算二号救援机','市政吊装机'],source_only=True,shared_runtime_modified=False),dispatch_record='交接发送记录-20261016.json')
write(MANIFEST,manifest)
links=''.join(f'<li><a href="{html.escape(b,quote=True)}">{html.escape(a)}</a></li>' for a,b in groups)
rows=''.join(f'<tr><td>{html.escape(x["asset"])}</td><td><a href="{x["file"]}">{html.escape(x["file"])}</a></td><td>{html.escape(x["scope"])}</td><td>{x["status"]}</td></tr>' for x in entries.values())
(OUT/READER).write_text('''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>已确定设计交付｜2026-10-23</title><style>body{margin:0;background:#eeeae0;color:#173347;font:16px/1.8 system-ui}main{max-width:1350px;margin:auto;padding:28px}a{color:#126184}table{border-collapse:collapse;width:100%;font-size:13px}td,th{padding:10px;border-bottom:1px solid #ccd0c5;text-align:left;overflow-wrap:anywhere}.scope{background:#faf8ef;border-left:4px solid #c6533c;padding:14px}nav{display:flex;gap:22px;flex-wrap:wrap}</style></head><body><main><nav><a href="index.html">素材总览</a><a href="confirmed-design-source-20261023.zip">下载集中源文件包</a><a href="confirmed-design-handoff-20261023.json">逐文件清单与使用范围</a></nav><h1>已确定设计 · 集中交付</h1><p class="scope">本次交付给「战斗主玩法打磨」。雷翎/歌翼当前六张R6三视已确定；此前已确认来源按各自范围一并整理。授权派生和父源在清单中分别标记。馆守Z沿现有资产，无牌仅固定头部。</p><ul>'''+links+'</ul><p>下一批：预算二号救援机与市政吊装机源设计。主工程由原对话继续集中接入。</p><table><thead><tr><th>对象</th><th>原文件</th><th>范围</th><th>源状态</th></tr></thead><tbody>'+rows+'</tbody></table></main></body></html>')
files=list(entries)+docs+[MANIFEST]
with zipfile.ZipFile(OUT/ZIP,'w',zipfile.ZIP_DEFLATED) as z:
    for f in dict.fromkeys(files):z.write(OUT/f,arcname=f)
with zipfile.ZipFile(OUT/ZIP) as z:
    assert z.testzip() is None
    for f in dict.fromkeys(files):assert hashlib.sha256(z.read(f)).hexdigest()==sha(OUT/f)
prompt=f'''用户已在美术对话明确授权：“好的，已确定的设计可以交付给主对话，然后进行下一批”。现将已确定设计集中交付给「战斗主玩法打磨」。

交付入口：{OUT/READER}
逐文件清单及SHA：{OUT/MANIFEST}
集中源文件包：{OUT/ZIP}
最新采用回执：{OUT/'aircraft-design-fixed-20261023-r6.json'}

当前制作依据：社勇王/勇拳与组件和六名角色沿10月18日固定清单；旧拳王沿R2三视；王者沿R12素体/全装及双状态头部；货柜领袖沿R8确定形象和R9授权修正三视；雷翎与歌翼沿本次确定的R6正侧背（CML141/CML142）。无牌仅R16头部已定，整机不以旧头稿代替；馆守Z继续沿现有资产。清单区分confirmed_source_design、authorized_derived_support及parent_context_only。源设计采用不代签模型、完整变形、动作、声音或运行。

请按你当前施工排期沿这些确定源稿继续制作/接入，并在原台账记录实际使用来源；保留正在进行的局面和原生录制，按原安全接入时点处理。本美术对话没有改主工程或替你填写运行结果。

按用户要求，本美术对话接着处理原清单M06预算二号救援机与M07市政吊装机，先沿现有造型出源稿，区分维修/撤离工具与吊臂/稳定腿。这里先同步对象，避免重复改主模型；你的当前主玩法施工照常继续。'''
(OUT/'main-dialogue-handoff-20261023.txt').write_text(prompt+'\n')
print(json.dumps(dict(reader=str(OUT/READER),manifest=MANIFEST,source_package=str(OUT/ZIP),confirmed=sum(x['status']=='confirmed_source_design' for x in entries.values()),supports=sum(x['status']!='confirmed_source_design' for x in entries.values()),zip_verified=True),ensure_ascii=False))
