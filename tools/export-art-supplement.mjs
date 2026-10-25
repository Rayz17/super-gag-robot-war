import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const target = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = process.argv[2] && path.resolve(process.argv[2]);
if (!source || source === target || !fs.existsSync(path.join(source, 'docs/superpowers/specs/data/canon/authority_manifest.tsv'))) throw new Error('Provide the original project directory');
const date = '2026-10-26';
const base = 'captures/20261014-full-direction/review/20261016-internal-upgrade';
const styleBase = 'docs/superpowers/specs/work-packages/2026-10-02-chao-gag-linked-operation-candidate/v5完整整改计划-20261008';
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const clean = value => String(value ?? '').replace(/[\t\r\n]/g, ' ');
const readJSON = relative => JSON.parse(fs.readFileSync(path.join(source, relative), 'utf8'));
const planned = new Map();
const evidence = new Set();
const labels = { H01: '纪存', H02: '白鸢', H03: '七海', H04: '兜灯', H07: '唐胶', H09: '胶价王', M01: '无牌一号：仅R16头部', M02: '旧拳王', M03: '馆守Z', M04: '社勇王', F09: '勇拳', F11: '钻探机与腿部组件', F12: '海底列车与臂壳', M05: '完全版王者', M06: '预算二号', M08: '雷翎', M09: '灰崎警备劳务机', M10: '消防架桥机', M11: '货柜领袖', M14: '歌翼' };
const lockIDs = { H01: 'CML132', H02: 'CML132', H03: 'CML132', H04: 'CML132', H07: 'CML132', H09: 'CML132', M01: 'CML133', M02: 'CML136', M03: 'CML130;CML131', M04: 'CML132', F09: 'CML132', F11: 'CML132', F12: 'CML132', M05: 'CML134;CML135', M06: 'CML143', M08: 'CML141', M09: 'CML144', M10: 'CML145', M11: 'CML138;CML139', M14: 'CML140;CML142' };

function add(relative, item) {
  if (path.isAbsolute(relative) || relative.split('/').includes('..')) throw new Error('Unsafe relative source path');
  const bytes = fs.readFileSync(path.join(source, relative));
  const actual = hash(bytes);
  if (item.expected_sha256 && item.expected_sha256 !== actual) throw new Error('Acceptance fingerprint drift: ' + relative);
  const previous = planned.get(relative);
  if (previous) return;
  planned.set(relative, { path: relative, ...item, sha256: actual, bytes: bytes.length, payload: bytes });
}

function addBatch(name, fixedStatus, fixedAsset) {
  const receipt = path.posix.join(base, name), record = readJSON(receipt);
  evidence.add(receipt);
  for (const f of record.files || []) {
    const relative = path.posix.join(base, f.file);
    const id = fixedAsset || path.basename(f.file).match(/^(H\d\d|M\d\d|F\d\d)/)?.[1] || 'ASSEMBLY';
    add(relative, { asset_id: id, name: labels[id] || id, status: fixedStatus || f.status || 'confirmed_source_design', scope: f.scope || f.role || '指定源设计，具体采用范围见回执', receipt, lock_ids: lockIDs[id] || 'CML132', expected_sha256: f.sha256, runtime_accepted: false });
  }
}

addBatch('confirmed-design-handoff-20261023.json');
addBatch('M06-turnaround-design-fixed-20261023-r3.json', 'confirmed_source_design', 'M06');
addBatch('city-response-design-fixed-20261023-r2.json', 'confirmed_source_design');
addBatch('city-response-main-handoff-20261024.json', 'authorized_derived_support_not_individually_accepted');
for (const name of ['source-design-freeze-20261018.json', 'mecha-source-batch-acceptance-20261021.json', 'mecha-source-decisions-20261019-r17.json', 'M11-design-fixed-20261022.json', 'M11-head-selected-and-turnaround-r6.json', 'M11-turnaround-delivery-production-r9.json', 'M14-design-fixed-20261022.json', 'aircraft-design-fixed-20261023-r6.json', 'M06-design-fixed-20261023-r2.json', 'city-response-user-correction-20261024-r4.json']) evidence.add(path.posix.join(base, name));

const standardPath = 'docs/superpowers/specs/production/art-direction-v0.3/visual-standard-20261010.json';
const standard = readJSON(standardPath);
for (const [relative, expected] of [[standard.source, standard.source_sha256], [standard.tactics_target, standard.target_sha256]]) {
  if (hash(fs.readFileSync(path.join(source, relative))) !== expected) throw new Error('Style source fingerprint drift: ' + relative);
}
evidence.add(standardPath);
evidence.add(standard.source);
evidence.add('docs/superpowers/specs/production/art-direction-v0.3/series-art-direction-ab-lock-v1.md');
evidence.add('docs/superpowers/specs/production/art-direction-v0.3/art-style-and-complexity-budget-v1.md');
const html = fs.readFileSync(path.join(source, standard.source), 'utf8');
for (const match of html.matchAll(/<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi)) {
  const src = match[1];
  if (/^(?:https?:|data:)/.test(src)) continue;
  const relative = path.posix.normalize(path.posix.join(path.posix.dirname(standard.source), src));
  let status = 'style_reference';
  if (/deprecated|11b-|11c-/.test(src)) status = 'negative_comparison_not_adopted';
  else if (src.startsWith('existing-style/')) status = 'style_example_not_current_identity';
  else if (relative === standard.tactics_target) status = 'user_confirmed_tactics_target';
  add(relative, { asset_id: 'STYLE', name: path.basename(relative), status, scope: '视觉总参考原页面中的实际图片；画风参考与主体身份采用分别判断', receipt: standard.source, lock_ids: 'CML128', runtime_accepted: false });
}
for (const [filename, title, status, locks] of [
  ['series_style_storyframe_v23a_kinetic_cel.png', 'KINETIC_CEL常态画法', 'approved_style_language_example', 'CML128'],
  ['series_style_storyframe_v23b_archive_offset.png', 'ARCHIVE_OFFSET峰值画法', 'approved_style_language_example', 'CML128'],
  ['guardian_z_collector_e02_lockframe_candidate_v10x.png', '馆守Z V10X既有母稿', 'confirmed_scoped_parent_not_runtime_acceptance', 'CML130;CML131'],
]) {
  const relative = 'docs/superpowers/specs/production/art-direction-v0.3/art-delivery/review/' + filename;
  add(relative, { asset_id: filename.startsWith('guardian') ? 'M03' : 'STYLE', name: title, status, scope: filename.startsWith('guardian') ? '沿用现有馆守Z；收藏/身份母稿与C01当时缺臂状态不同，不能恢复已毁右前臂' : '画法示范，旧人物/机体外形不覆盖10月已定源', receipt: 'docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv', lock_ids: locks, runtime_accepted: false });
}
for (const name of ['GF_PLAN_1280x720_v2.png', 'GF_CONTACT_1280x720_v2.png']) add('docs/superpowers/specs/production/c01-current-demo-v1/art-a9-gold-frame/delivery/' + name, { asset_id: 'C01_FRAME', name, status: 'confirmed_nonseparable_frame_anchor', scope: 'C01整帧构图/动作/身份锚，不可拆成人物新母稿或直接当运行资产', receipt: 'docs/superpowers/specs/剧情梗概/V35-GF纪存与BREAKER用户视觉锚Current-Canon迁移-2026-08-23.md', lock_ids: 'CML001;CML129', runtime_accepted: false });
evidence.add('docs/superpowers/specs/剧情梗概/V35-GF纪存与BREAKER用户视觉锚Current-Canon迁移-2026-08-23.md');
const refreshDocs = [
  'docs/superpowers/specs/data/canon/authority_manifest.tsv',
  'docs/superpowers/specs/data/canon/authority_overrides.tsv',
  'docs/superpowers/specs/data/canon/character_mecha_art_locks.tsv',
  'docs/superpowers/specs/剧情梗概/V35-PRODUCTION-STATUS.md',
  styleBase + '/实施进度-20261010.json',
  styleBase + '/覆盖核对.html',
];
refreshDocs.forEach(p => evidence.add(p));
for (const relative of evidence) add(relative, { asset_id: 'PROVENANCE', name: path.basename(relative), status: 'source_record', scope: '原始采用/方向/交接依据；其中旧方案和未确认输出不因同步升格', receipt: relative, lock_ids: '', runtime_accepted: false });

// Validate each selected image before copying any payload into the review repository.
for (const item of planned.values()) {
  if (!/\.(?:png|jpe?g|webp)$/i.test(item.path)) continue;
  const out = execFileSync('/usr/bin/sips', ['-g', 'pixelWidth', '-g', 'pixelHeight', path.join(source, item.path)], { encoding: 'utf8' });
  const width = Number(out.match(/pixelWidth:\s*(\d+)/)?.[1]), height = Number(out.match(/pixelHeight:\s*(\d+)/)?.[1]);
  if (!width || !height) throw new Error('Unreadable image: ' + item.path);
  item.pixel_width = width;
  item.pixel_height = height;
}
for (const item of planned.values()) {
  const destination = path.join(target, item.path);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, item.payload);
  delete item.payload;
}
const all = [...planned.values()].sort((a, b) => a.path.localeCompare(b.path, 'en'));
fs.mkdirSync(path.join(target, 'review/art'), { recursive: true });
const columns = ['path', 'asset_id', 'name', 'status', 'scope', 'receipt', 'lock_ids', 'bytes', 'sha256', 'pixel_width', 'pixel_height', 'runtime_accepted'];
fs.writeFileSync(path.join(target, 'review/art/ASSET-MANIFEST.tsv'), [columns.join('\t'), ...all.map(r => columns.map(k => clean(r[k])).join('\t'))].join('\n') + '\n');
const groups = [...new Set(all.filter(x => x.asset_id !== 'PROVENANCE').map(x => x.asset_id))];
const order = ['STYLE', 'H01', 'H02', 'H03', 'H04', 'H07', 'H09', 'M04', 'F09', 'F11', 'F12', 'M03', 'M01', 'M02', 'M05', 'M06', 'M08', 'M14', 'M11', 'M09', 'M10', 'C01_FRAME'];
groups.sort((a, b) => order.indexOf(a) - order.indexOf(b));
const relativeURL = p => '../../' + p;
const gallery = ['# 已定美术与资产图册', '', '2026-10-26增补。状态来自逐图采用或交接记录；图片保留原字节。先读[美术评审入口](../04-美术风格与已定资产.md)。', '', '“已确定”只覆盖所列源设计；授权派生、父源背景、旧画法样例和反例分别标明。模型、完整变形、动作、声音与运行没有在此获得新验收。', '', '| 状态 | 用法 |', '| --- | --- |', '| confirmed_source_design | 明确采用的具体源图或确认交接中的固定源 |', '| authorized_derived_support / authorized_derived_support_not_individually_accepted | 沿已定母稿制作的授权派生，未逐图确认 |', '| parent_context_only | 辅助识别来源，不替换最新三视 |', '| style_reference / approved_style_language_example / user_confirmed_tactics_target | 画法、用途或特定盘面靶图，不授予所有图中机体身份资格 |', '| style_example_not_current_identity | 视觉参考页中的旧样例，当前角色外形按本图册对应新母稿 |', '| negative_comparison_not_adopted | 明确反例，不作为正向目标 |', '| confirmed_scoped_parent_not_runtime_acceptance / confirmed_nonseparable_frame_anchor | 原有有限范围母稿/整帧锚，不扩大为运行资产 |', ''];
for (const id of groups) {
  const items = all.filter(x => x.asset_id === id);
  gallery.push('## ' + (labels[id] || (id === 'STYLE' ? '风格与靶图' : id === 'C01_FRAME' ? 'C01有限范围整帧锚' : id)), '');
  let hero = items.find(x => /dialogue|palette|front-backpack-fins|core-master|posture-r8|front-airframe|front-r3\.png|curved-labor-r2|engineering-transformer-r2/.test(x.path) && x.status === 'confirmed_source_design');
  if (id === 'STYLE') hero = items.find(x => x.status === 'user_confirmed_tactics_target');
  if (!hero && items.length <= 3) hero = items.find(x => /\.png$/.test(x.path) && !/negative|parent_context/.test(x.status));
  if (hero && /\.(?:png|jpe?g)$/.test(hero.path)) gallery.push('![' + (labels[id] || hero.name) + '](' + relativeURL(hero.path) + ')', '', '**上图范围：**' + hero.scope + '；状态：`' + hero.status + '`。', '');
  gallery.push('| 图稿 | 状态 | 确认范围与来源 |', '| --- | --- | --- |');
  for (const item of items) gallery.push('| [' + path.basename(item.path) + '](' + relativeURL(item.path) + ') | `' + item.status + '` | ' + item.scope.replace(/\|/g, '/') + '；[原记录](' + relativeURL(item.receipt) + ')；' + item.lock_ids + ' |');
  gallery.push('');
}
gallery.push('原图尺寸、字节与SHA见[资产清单](ASSET-MANIFEST.tsv)。未收入M07/M12未确认新稿；旧画法例图和否决图仅供对应范围比较，不作为当前主体采用。', '');
fs.writeFileSync(path.join(target, 'review/art/README.md'), gallery.join('\n'));

// Refresh only existing document-manifest rows whose original files were copied in this supplement.
const sourceManifest = path.join(target, 'review/SOURCE-MANIFEST.tsv');
const lines = fs.readFileSync(sourceManifest, 'utf8').trimEnd().split('\n');
const header = lines.shift().split('\t');
const refreshed = [];
const updated = lines.map(line => {
  const cells = line.split('\t'), record = Object.fromEntries(header.map((key, i) => [key, cells[i]]));
  const item = planned.get(record.path);
  if (item && record.sha256 !== item.sha256) { record.bytes = String(item.bytes); record.sha256 = item.sha256; refreshed.push(record.path); }
  return header.map(key => clean(record[key])).join('\t');
});
fs.writeFileSync(sourceManifest, [header.join('\t'), ...updated].join('\n') + '\n');
const metadataPath = path.join(target, 'review/snapshot-metadata.json');
const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
metadata.included_bytes = updated.reduce((sum, line) => sum + Number(line.split('\t')[header.indexOf('bytes')]), 0);
metadata.manifest_sha256 = hash(fs.readFileSync(sourceManifest));
metadata.art_supplement_date = date;
metadata.art_supplement_manifest = 'review/art/ASSET-MANIFEST.tsv';
metadata.document_refreshes_20261026 = [...new Set([...(metadata.document_refreshes_20261026 || []), ...refreshed])];
metadata.excluded_root_areas_note = 'captures and media remain excluded from the base text export; explicit art-supplement files are included separately.';
fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2) + '\n');
const stats = { date, files: all.length, images: all.filter(x => /\.(?:png|jpe?g|webp)$/i.test(x.path)).length, vectors: all.filter(x => x.path.endsWith('.svg')).length, bytes: all.reduce((s, x) => s + x.bytes, 0), by_status: {}, refreshed_documents: metadata.document_refreshes_20261026 };
for (const item of all) stats.by_status[item.status] = (stats.by_status[item.status] || 0) + 1;
fs.writeFileSync(path.join(target, 'review/art/IMPORT-RESULT.json'), JSON.stringify(stats, null, 2) + '\n');
console.log(JSON.stringify(stats, null, 2));
