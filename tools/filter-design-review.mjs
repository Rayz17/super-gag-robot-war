import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = name => {
  const lines = fs.readFileSync(path.join(root, name), 'utf8').trimEnd().split('\n');
  const keys = lines.shift().split('\t');
  return { keys, rows: lines.map(line => Object.fromEntries(line.split('\t').map((value, i) => [keys[i], value]))) };
};
const write = (name, data) => fs.writeFileSync(path.join(root, name), [data.keys.join('\t'), ...data.rows.map(row => data.keys.map(key => String(row[key] ?? '').replace(/[\t\r\n]/g, ' ')).join('\t'))].join('\n') + '\n');
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const manifest = read('review/library/FILE-MANIFEST.tsv');
const sources = read('review/SOURCE-MANIFEST.tsv');
const exclusions = read('review/library/EXCLUSIONS.tsv');
const curated = read('review/art/ASSET-MANIFEST.tsv');
const outsideCurated = new Set(curated.rows.filter(row => row.asset_id === 'C01_FRAME' || row.status === 'user_confirmed_tactics_target').map(row => row.path));
const curatedPaths = new Set(curated.rows.filter(row => !outsideCurated.has(row.path)).map(row => row.path));
const original = 'captures/20261014-full-direction/review-v2.html';
const html = fs.readFileSync(path.join(root, original), 'utf8');
const allowedId = id => /^[MHEFBST]\d{2}$/.test(id) || /^N(?:09|1[0-4])$/.test(id);
const strip = value => (value || '').replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
const cards = [...html.matchAll(/<article class="card"([^>]*)>([\s\S]*?)<\/article>/g)].map(match => ({
  id: match[1].match(/data-id="([^"]+)"/)?.[1],
  group: match[1].match(/data-group="([^"]+)"/)?.[1],
  name: strip(match[2].match(/<h3 class="name">([\s\S]*?)<\/h3>/)?.[1]),
  image: path.posix.normalize(path.posix.join(path.posix.dirname(original), match[2].match(/<img[^>]+src="([^"]+)"/)?.[1] || '')),
  verdict: strip(match[2].match(/<div class="review-verdict[^>]*>([\s\S]*?)<\/div>/)?.[1]),
})).filter(card => allowedId(card.id));
if (cards.length !== 134) throw new Error('Unexpected design card count');
const cardPaths = new Set(cards.map(card => card.image));
const isImage = name => /\.(?:png|jpe?g|webp|svg|psd|kra|ora|xcf|aseprite|ase)$/i.test(name);
const uiOrExecution = /(?:^|[\/_.-])(?:ui|ue|hud|icon|icons|popup|overlay|viewport|qa|captures|runtime|debug|mask|shadow|hitbox|atlas|sprite|sprites)(?:[\/_.-]|$)|界面|交互原型|验收截图/i;
function keepDesign(row) {
  const name = row.path;
  if (!isImage(name)) return true;
  if (outsideCurated.has(name) || name.includes('/art-a9-gold-frame/')) return false;
  if (curatedPaths.has(name) || cardPaths.has(name)) return true;
  if (row.scope === 'full_art_direction') {
    const file = path.basename(name);
    const ids = [...file.matchAll(/(?:^|[-_])([MHEFBSXGCUITN]\d{2})(?=[-_.]|$)/gi)].map(match => match[1].toUpperCase());
    if (ids.length) return ids.every(allowedId);
    if (/^[MHEFBST]-\d{2}\./.test(file)) return true;
    if (name.includes('/20261016-internal-upgrade/') && !/(?:samples|small-scale|tactics|contact-?sheet|screen)/i.test(name)) return true;
    return /\/style-lock\/(?:01-|02-)/.test(name);
  }
  if (uiOrExecution.test(name)) return false;
  if (row.scope === 'source_2d_design_sheets' || row.scope === 'external_art_handoff') return true;
  if (row.scope === 'early_2d_candidates_and_evidence') return /\/art-candidates-|\/battle-presentation-v0.1\/(?:01-cutin|02-mecha-pose)/.test(name);
  if (row.scope === 'historical_demo_2d') return /(?:portrait|character|background|mecha|concept)/i.test(name);
  if (row.scope === 'game_side_assets') return /\/backgrounds\/|\/portraits\/|\/candidate\/c02_short_plan\/|(?:design|reference|turnaround|concept|silhouette|full_body)/i.test(name) && !/(?:emission|roughness|normal|texture)/i.test(name);
  if (row.scope === 'settings_and_production') {
    if (/\/art-direction-v0.3\/art-delivery\//.test(name)) return true;
    if (/外援美术制作清单-20261012\/(?:current|reference)\//.test(name)) return !/(?:dir-[GCUINX]\d|[GCUINX]-\d)/.test(path.basename(name));
    if (/v5完整整改计划-20261008\/(?:existing-style|target-look)\//.test(name)) return true;
    return /(?:user-confirmation|source-lock|generation-raw|\/sources\/|\/source\/|\/delivery\/|\/reference\/|\/refs\/|concept|design|turnaround|threeview|structure|identity|proportion|construction|用户确认|设定图|三视图)/i.test(name) && !/(?:camera-v2|rig-|animation|frame-|four-facing|composite|preflight|topology|tactical-read|dialogue-ui|comms-ui)/i.test(name);
  }
  return false;
}
const initiallyKept = manifest.rows.filter(keepDesign);
const hashes = new Set(initiallyKept.filter(row => isImage(row.path)).map(row => row.sha256));
const kept = manifest.rows.filter(row => keepDesign(row) || (row.scope === 'full_art_direction' && /\/images\/[a-f0-9]{64}\./.test(row.path) && hashes.has(row.sha256)));
const keepPaths = new Set(kept.map(row => row.path));
const removed = manifest.rows.filter(row => !keepPaths.has(row.path));
for (const row of removed) {
  fs.unlinkSync(path.join(root, row.path));
  exclusions.rows.push({ path: row.path, scope: row.scope, bytes: row.bytes, reason: 'outside_external_design_art_scope_uiue_or_execution_evidence' });
}
manifest.rows = kept;
sources.rows = sources.rows.filter(row => !isImage(row.path) || keepPaths.has(row.path));
curated.rows = curated.rows.filter(row => keepPaths.has(row.path));
write('review/library/FILE-MANIFEST.tsv', manifest);
write('review/library/EXCLUSIONS.tsv', exclusions);
write('review/SOURCE-MANIFEST.tsv', sources);
write('review/art/ASSET-MANIFEST.tsv', curated);
fs.writeFileSync(path.join(root, 'review/library/DESIGN-CARDS.json'), JSON.stringify({ source: original, source_sha256: sha(Buffer.from(html)), selected_design_cards: cards, excluded_categories: ['G', 'C', 'U', 'I', 'X', 'N01-N08'], source_card_count: 298, policy: 'design_art_for_external_story_and_setting_review_no_uiue_no_3d' }, null, 2) + '\n');
const statsPath = path.join(root, 'review/library/IMPORT-RESULT.json');
const stats = JSON.parse(fs.readFileSync(statsPath));
stats.requested_scope = 'external_review_design_art_and_settings_no_uiue_no_3d';
stats.uiue_included = false;
stats.design_cards = cards.length;
stats.files = stats.git_files = kept.length;
stats.bytes = kept.reduce((sum, row) => sum + Number(row.bytes), 0);
stats.text_files = sources.rows.length;
stats.exclusion_records = exclusions.rows.length;
delete stats.recovered_2d_evidence_files;
stats.by_scope = {};
for (const row of kept) {
  const group = stats.by_scope[row.scope] ??= { files: 0, git_files: 0, release_files: 0, bytes: 0 };
  group.files++; group.git_files++; group.bytes += Number(row.bytes);
}
fs.writeFileSync(statsPath, JSON.stringify(stats, null, 2) + '\n');
const curatedStatsPath = path.join(root, 'review/art/IMPORT-RESULT.json');
const curatedStats = JSON.parse(fs.readFileSync(curatedStatsPath));
curatedStats.files = curated.rows.length;
curatedStats.images = curated.rows.filter(row => /\.(?:png|jpe?g|webp)$/i.test(row.path)).length;
curatedStats.vectors = curated.rows.filter(row => row.path.endsWith('.svg')).length;
curatedStats.bytes = curated.rows.reduce((sum, row) => sum + Number(row.bytes), 0);
curatedStats.by_status = {};
for (const row of curated.rows) curatedStats.by_status[row.status] = (curatedStats.by_status[row.status] || 0) + 1;
curatedStats.art_scope = stats.requested_scope;
fs.writeFileSync(curatedStatsPath, JSON.stringify(curatedStats, null, 2) + '\n');
const metaPath = path.join(root, 'review/snapshot-metadata.json');
const meta = JSON.parse(fs.readFileSync(metaPath));
meta.included_files = sources.rows.length;
meta.included_bytes = sources.rows.reduce((sum, row) => sum + Number(row.bytes), 0);
meta.excluded_files = exclusions.rows.length;
meta.manifest_sha256 = sha(fs.readFileSync(path.join(root, 'review/SOURCE-MANIFEST.tsv')));
meta.art_scope = stats.requested_scope;
fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2) + '\n');
console.log(JSON.stringify({ files: kept.length, removed: removed.length, bytes: stats.bytes, images: kept.filter(row => isImage(row.path)).length, cards: cards.length }));
