"""Publish a visible music-support module on the positively reviewed Songwing R3."""
from pathlib import Path
import hashlib,html,json,shutil
from PIL import Image
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[3]
RECORD='M14-music-support-production-r4.json'
READER='M14-music-support-r4.html'
def read(name):return json.loads((OUT/name).read_text())
def write(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
origin=Path('/Users/rayz/.codex/generated_images/01a13f08-23a0-74c2-b2f5-7913c7e81470/exec-d6d57289-f1a7-4974-a912-1bf7faacc750.png')
target=OUT/'samples/M14-music-support-r4.png'
if target.exists():assert sha(target)==sha(origin)
else:shutil.copyfile(origin,target)
with Image.open(target) as im:size=list(im.size);mode=im.mode
base=next(x for x in read('aircraft-synthesis-production-r3.json')['items'] if x['id']=='M14')
assert sha(OUT/base['file'])==base['sha256']
item=dict(id='M14',name='歌翼音乐传播模块',file=target.relative_to(OUT).as_posix(),sha256=sha(target),pixel_size=size,mode=mode,generated_source=str(origin),base_source=base['file'],base_sha256=base['sha256'],prompt='M14-music-support-prompt-r4.txt',user_accepted=False,runtime_integrated=False)
cast='docs/superpowers/specs/data/character_layer/pilot_cast.tsv'
roles=dict(source=cast,source_sha256=sha(PROJECT/cast),pilot=dict(id='CH022',name='隼真',role='歌翼可变机飞行员；从抢镜到保护别人的声音'),singer=dict(id='CH021',name='莉歌',role='星间歌姬；以舞台战舰、歌声支援为主要关联'),scope='现有角色表分工；不因本轮硬件外观提案更改人物身份、驾驶关系或登场阶段。')
design=dict(purpose='让歌翼能接收、转播和投射歌声，音乐功能可辨；歌姬和飞行员仍分工配合。',
 equipment=['双肩后翼状声传播板：外壳合拢为整流罩，翻开展露深色扬声器面。','每侧可见一大一小两个圆形单元，分别承担低/高频扩声的视觉表达；不声明实际声学工程参数。','翼根短定向中继表面和闭合舱：用于宇宙环境的歌声/通讯信号转播。'],
 atmosphere='大气或有声学介质的空间可通过扩声单元发声。',space='真空环境以电磁信号传输，在接收设备/舰舱播放；不表现真空中普通喇叭直接把声波传遍战场。',
 instrument_choice='本案先以扬声器、格栅分区和展开动作表达音乐；不加巨型吉他、钢琴、音符贴纸或乐器型武器。',
 ip_interpretation='Macross为明确主投射。林明美的歌声介入战争很贴合；拉克丝的公众发声/和平立场可以作为创作参考，当前档案未锁定二人融合。',
 mechanical_boundary='新增可折叠模块外观，不新增声波杀伤、洗脑、真空声传播或已完成的游戏技能。')
observations=['头盔/双红天线、琥珀光学面与座舱胸沿用R3，长腿与主体翼展可追认。','整机展开态及右上背部局部均可见每侧一大一小两个扬声器单元，铰链/支架可读。','闭合背部局部有完整红白外壳，航空态两片新整流罩贴近上机身，未让裸露扬声器迎风。','航空态仍保留R3多挂舱/发动机构型，本轮没有证明已经精简到两台发动机；具体翼根与附加模块净空需背视/同件模型继续核对。']
record=dict(revision='M14-music-support-r4',date='2026-10-22',existing_batch='design-followthrough-r1.json',status='candidate_optional_music_support_module_on_R3',reader=READER,
 user_feedback='这一版好了很多；歌翼是否应有歌唱功能、驾驶员是否宇宙歌姬，以及是否融合林明美/拉克丝，需不需要扩音器或乐器特征。',
 generation_mode='built-in image_gen; identity-preserving equipment edit',item=item,role_check=roles,design=design,
 external_references=[dict(url='https://macross.jp/pages/series?title=macross',used='林明美与歌声/战争关系'),dict(url='https://gundam-official.com/seed/seed/character/detail.php?id=26',used='拉克丝是歌姬；不据此推定为本项目已锁融合角色'),dict(url='https://www.bandaispirits.co.jp/products/search/detail.php?grp_id=5325&prd_id=4573102663153000',used='Macross7 Sound Booster肩部可展开扬声器的官方设计参照；不复制其机型')],
 author_review=dict(reviewer='author',independent_review=False,actual_media=[item['file']],observations=observations,judgement='音乐功能已有可辨硬件和收纳表达，主形维持R3；具体模块尚未获得用户采用。'),
 runtime_assets_modified=False,canon_changed=False,character_roles_changed=False,main_thread_messaged=False,
 limits=['当前仅二维源设计，闭合/展开/航空形态不等于同件模型或碰撞验证。','本轮未生成或实听歌曲/音效，未制作广播技能和战斗规则。','R3得到继续完善的正面反馈，不扩大为全源稿、人物身份或运行的定稿回执。'])
write(RECORD,record)
write('M14-music-support-prompts-r4.json',dict(mode='built-in image_gen',prompt=item['prompt'],input_file=item['base_source'],input_sha256=item['base_sha256'],output=item['file']))
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>歌翼｜音乐传播模块R4</title><style>*{box-sizing:border-box}body{margin:0;background:#eeeae0;color:#193345;font:16px/1.8 system-ui}main{max-width:1540px;margin:auto;padding:28px}a{color:#09657c}nav{display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,4vw,44px);line-height:1.3}.board{display:block;width:100%;height:auto}table{width:100%;border-collapse:collapse}td,th{padding:12px 16px;text-align:left;border-bottom:1px solid #bdc9c7}.scope{padding:14px 18px;border-left:4px solid #ca5946;background:#faf5eb}.note{font-size:14px;color:#546b75}h2{margin-top:34px}@media(max-width:700px){main{padding:18px}}</style></head><body><main><nav><a href="aircraft-synthesis-r3.html">R3两台综合设计</a><a href="index.html">素材总览</a><a href="M14-music-support-prompts-r4.json">实际内置生图提示词</a></nav><h1>让歌翼成为能传递歌声的护航机</h1><p class="scope">保留R3头型、座舱胸、翼展和长腿，补可收拢的肩后扩声板与翼根中继设备。歌姬和飞行员按现有角色表分工配合。</p><a href="samples/M14-music-support-r4.png"><img class="board" src="samples/M14-music-support-r4.png" alt="歌翼R4：整机音乐模块展开、背部闭合与展开局部、航空态收纳"></a><h2>先分清角色</h2><table><tr><th>角色</th><th>现有角色表定位</th><th>与歌翼的关系</th></tr><tr><td>隼真</td><td>可变机飞行员</td><td>驾驶歌翼，从抢镜转向保护他人的声音</td></tr><tr><td>莉歌</td><td>星间歌姬</td><td>主要关联舞台战舰与歌声支援，可由歌翼中继传播</td></tr></table><p>Macross是明确主投射。林明美式的歌声介入战争契合莉歌；拉克丝式的公众发声与和平立场可吸收为创作参考，当前档案没有写成两者已经融合。</p><h2>本案的功能取舍</h2><ul>'''+''.join('<li>'+html.escape(x)+'</li>' for x in design['equipment'])+'''</ul><p>大气内扩声；宇宙中通过电磁信号向舰艇、座舱和通讯终端转播。音乐感来自声传播翼、扬声器和展开动作，本案保留原有战机主体。</p><p>这种展开设备可参考Macross7的<a href="https://www.bandaispirits.co.jp/products/search/detail.php?grp_id=5325&amp;prd_id=4573102663153000">Sound Booster官方设计资料</a>。人物灵感核对见<a href="https://macross.jp/pages/series?title=macross">Macross官方资料</a>与<a href="https://gundam-official.com/seed/seed/character/detail.php?id=26">拉克丝官方角色页</a>。</p><details><summary>实际图面观察与尚未验证</summary><ul>'''+''.join('<li>'+html.escape(x)+'</li>' for x in observations)+'''</ul><p>二维源设计候选；未改运行、人物身份或技能，未生成或实听歌曲/音效。</p></details><p class="note"><a href="M14-music-support-production-r4.json">来源、角色核对与作者观察</a></p></main></body></html>'''
(OUT/READER).write_text(page)
for name in ['aircraft-synthesis-r3.html','aircraft-runtime-comparison-20261022.html']:
    p=OUT/name;s=p.read_text()
    note=f'<aside id="songwing-music-r4" class="scope"><h2>歌翼新增：音乐传播模块R4</h2><p>沿这版主体增加可收拢扩声板与中继设备，保留歌姬/飞行员分工。<a href="{READER}">查看展开、闭合与航空收纳 →</a></p></aside>'
    if 'id="songwing-music-r4"' not in s:p.write_text(s.replace('</nav>','</nav>'+note,1))
ledger=read('design-followthrough-r1.json')
ledger['latest_songwing_music_module']=RECORD
ledger['production_focus'].update(current_step='歌翼R4音乐模块候选已绘并实看，含人形展开、背部闭合/展开与航空收纳；现有角色表为隼真驾驶、莉歌歌姬。',current_scope='歌翼R3附加音乐传播模块源设计，不改雷翎R3、不改人物身份和运行。',next='沿当前主体收敛模块净空和派生三视；歌声效果、音效和同件模型仍分别制作验证。')
ledger['experience_record_songwing_music_r4']=dict(classification='experience',record=RECORD,original_requirement=['M14','F08','N13','CML023'],start='用户认为R3明显改善，提出音乐能力外观和歌姬/驾驶员关系疑问。',input='核对现有角色表和官方IP资料，沿歌翼R3新增折叠双声翼，保留主形。',visible_consequence='两侧扬声器在支援态展开，背部和航空态可见闭合整流罩；音频传播功能成为可辨识配件。',actual_artifacts=[item['file']],author_review=RECORD+'#author_review',independent_review=False,user_acceptance=False,runtime_changed=False,normal_tactical_scene_verified=False,sound_listened=False,next='模块归属/净空、三视、动作和实听未由源图验证。')
write('design-followthrough-r1.json',ledger)
author=read('sample-author-review.json');author['latest_songwing_music_module']=RECORD;write('sample-author-review.json',author)
user=read('user-art-decisions-20261016.json');user['latest_songwing_music_feedback']=dict(date='2026-10-22',positive_R3_feedback='这一版我觉得好了很多',request=record['user_feedback'],interpretation='R3方向正面认可并继续完善；新音乐模块待看，不改人物身份。',execution_record=RECORD,new_module_accepted=False);write('user-art-decisions-20261016.json',user)
print(json.dumps(dict(reader=str(OUT/READER),file=item['file'],runtime_changed=False,character_roles_changed=False),ensure_ascii=False))
