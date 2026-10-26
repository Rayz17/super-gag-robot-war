import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.resolve(process.argv[2] || '');
const staging = path.resolve(process.argv[3] || '');
if (!process.argv[2] || !process.argv[3] || root === source || staging === root || staging === source || !fs.existsSync(path.join(source, 'docs/superpowers/specs/data/canon/authority_manifest.tsv'))) throw new Error('Provide source project and separate archive staging directory');
const out = path.join(root, 'review/library');
fs.mkdirSync(out, { recursive: true });
fs.mkdirSync(path.join(staging, 'snapshot'), { recursive: true });
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const clean = s => String(s ?? '').replace(/[\t\r\n]/g, ' ');
const tsv = p => { const lines = fs.readFileSync(p, 'utf8').trimEnd().split('\n'); const keys = lines.shift().split('\t'); return lines.map(l => Object.fromEntries(l.split('\t').map((v, i) => [keys[i], v]))); };
const curated = new Map(tsv(path.join(root, 'review/art/ASSET-MANIFEST.tsv')).map(r => [r.path, r]));
const oldText = tsv(path.join(root, 'review/SOURCE-MANIFEST.tsv'));
const oldTextMap = new Map(oldText.map(r => [r.path, r]));
const previousLibrary = fs.existsSync(path.join(out, 'FILE-MANIFEST.tsv')) ? tsv(path.join(out, 'FILE-MANIFEST.tsv')) : [];
const textFormats = new Set(['.md', '.tsv', '.csv', '.json', '.jsonl', '.txt', '.yaml', '.yml', '.toml', '.mmd', '.html', '.svg', '.py', '.sh', '.gd', '.tscn', '.tres', '.gdshader', '.js', '.mjs', '.css', '.xml', '.cfg']);
const imageFormats = new Set(['.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif', '.bmp', '.tga', '.exr', '.hdr']);
const nativeFormats = new Set(['.blend', '.glb', '.gltf', '.bin', '.fbx', '.obj', '.mtl', '.res', '.scn', '.wav', '.ogg', '.mp3', '.flac', '.mp4', '.webm', '.ogv', '.mov', '.avi', '.psd', '.kra', '.ora', '.xcf', '.aseprite', '.ase', '.zip', '.tgz', '.gz', '.tar', '.7z']);
const threeDFormats = new Set(['.blend', '.glb', '.gltf', '.bin', '.fbx', '.obj', '.mtl', '.res', '.scn', '.exr', '.hdr']);
const twoDBinaryFormats = new Set(['.psd', '.kra', '.ora', '.xcf', '.aseprite', '.ase', '.pdf', '.docx', '.xlsx', '.pptx']);
const skipDirs = new Set(['.git', '.godot', '.obsidian', 'node_modules', '__pycache__', '.venv', '.ruff_cache', 'vendor']);
const secretPatterns = [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, /\bgh[pousr]_[A-Za-z0-9]{30,}\b/, /\bgithub_pat_[A-Za-z0-9_]{30,}\b/, /\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b/, /\bmsy_[A-Za-z0-9_-]{20,}\b/, /\bAKIA[0-9A-Z]{16}\b/, /Authorization["']?\s*:\s*["']?Bearer\s+[A-Za-z0-9_.-]{30,}/i, /X-Amz-Signature=[A-Za-z0-9]{40,}/i];
const scopes = [
  ['docs', 'settings_and_production'], ['研究报告', 'ip_reference'],
  ['captures/20261014-full-direction', 'full_art_direction'], ['grok-delivery', 'external_art_handoff'],
  ['game-godot/assets', 'game_side_assets'], ['game-godot/content', 'game_content'], ['game-godot/data', 'game_rules'],
  ['outputs', 'early_2d_candidates_and_evidence'], ['demo/chapter1/assets', 'historical_demo_2d'],
  ['artifacts/formulas/production-lab-v1/source', 'source_2d_design_sheets'],
];
const records = [], exclusions = [], secrets = [], copiedText = [], packageMap = new Map(), nativeCopies = new Map();
const exclude = (relative, bytes, reason, scope) => exclusions.push({ path: relative, bytes, reason, scope });

function nativeBucket(relative, scope) {
  const parts = relative.split('/');
  if (relative.startsWith('artifacts/formulas/production-lab-v1/source/')) return 'source-' + parts[4];
  if (relative.startsWith('game-godot/assets/formula_lab/linked_campaign_v6/')) return 'game-v6-' + parts[4];
  if (relative.startsWith('game-godot/assets/formula_lab/')) return 'game-' + parts[3];
  if (relative.startsWith('game-godot/assets/')) return 'game-' + parts[2];
  if (scope === 'settings_and_production') return 'production-' + (parts.includes('c01-current-demo-v1') ? 'c01' : 'other');
  return scope;
}

function importFile(relative, scope) {
  const from = path.join(source, relative), size = fs.statSync(from).size, ext = path.extname(relative).toLowerCase();
  if (['early_2d_candidates_and_evidence', 'historical_demo_2d'].includes(scope) && !/\.(?:png|jpe?g|webp|svg|psd|kra|ora|xcf|aseprite|ase|md)$/i.test(relative)) return exclude(relative, size, 'not_2d_art_or_design_note', scope);
  if (scope === 'source_2d_design_sheets') {
    const sub = relative.replace('artifacts/formulas/production-lab-v1/source/', '');
    const parts = sub.split('/');
    const flatDesign = parts.length === 2 || (parts.length === 3 && parts[1] === 'rejected');
    const threeDWork = /^(?:guardian-meshy|linked-campaign-models|stage-art)/.test(parts[0]);
    const textureOrInspection = /(?:atlas|paint|projection|inspection|inspect|runtime-|rig-|meshy|crop-contact|coordinate-review)/i.test(sub);
    if (!flatDesign || threeDWork || textureOrInspection || !/\.(?:png|jpe?g|webp|svg|psd|kra|ora|xcf|aseprite|ase)$/i.test(relative)) return exclude(relative, size, '3d_source_or_qa_not_2d_design_sheet', scope);
  }
  if (/(?:^|\/)(?:\.DS_Store|\.env(?:\.[^/]*)?|credentials[^/]*|[^/]*\.pem|[^/]*\.key)$/.test(relative)) return exclude(relative, size, 'private_or_machine_state', scope);
  if (['.import', '.uid', '.pyc', '.log', '.save', '.blend1', '.blend2', '.ttf', '.otf', '.woff', '.woff2'].includes(ext)) return exclude(relative, size, 'cache_autosave_log_or_bundled_font', scope);
  if (threeDFormats.has(ext)) return exclude(relative, size, '3d_asset_excluded_by_user', scope);
  if (scope === 'game_side_assets' && /\/(?:models|materials|environment|assembly|assembly-fixed[^/]*|layouts|stage_cache|tools|actions|textures|mesh|rig|blender)(?:\/|$)/.test(relative)) return exclude(relative, size, '3d_material_rig_or_model_support_excluded_by_user', scope);
  if (['game_side_assets', 'source_2d_design_sheets'].includes(scope) && /(?:[_-](?:normal(?:map)?|roughness|metallic|occlusion|base_?color|albedo|orm|diffuse|texture)(?:[_-]\d+)?|_Image_\d+)\.(?:png|jpe?g|webp)$/i.test(relative)) return exclude(relative, size, '3d_texture_map_excluded_by_user', scope);
  if (relative.startsWith('game-godot/assets/formula_lab/linked_campaign_v2/terrain/')) return exclude(relative, size, '3d_terrain_material_excluded_by_user', scope);
  if (/\.(?:wav|ogg|mp3|flac|mp4|webm|ogv|mov|avi|zip|tgz|gz|tar|7z)$/.test(relative)) return exclude(relative, size, 'audio_video_or_redundant_mixed_archive_outside_2d_review', scope);
  if (/\/data\/story\/.*fixture.*\.tsv$/.test(relative)) return exclude(relative, size, 'generated_test_matrix_not_setting_source', scope);
  if (/\/09-rea-binary-research\/(?:evidence|OGS-)/.test(relative)) return exclude(relative, size, 'third_party_binary_research', scope);
  if (relative.startsWith('artifacts/formulas/production-lab-v1/source/') && relative.includes('/research/')) return exclude(relative, size, 'third_party_tool_research_not_project_asset', scope);
  if (/(?:\/_history\/.*\/workspace\/|\/before-[^/]*\/workspace\/)/.test(relative)) return exclude(relative, size, 'duplicate_workspace_backup', scope);
  if (!textFormats.has(ext) && !imageFormats.has(ext) && !twoDBinaryFormats.has(ext)) return exclude(relative, size, 'non_design_format_review_separately', scope);
  const bytes = fs.readFileSync(from), digest = sha(bytes), previous = curated.get(relative);
  if (previous && previous.status !== 'source_record' && previous.sha256 !== digest) throw new Error('Curated asset changed: ' + relative);
  if (textFormats.has(ext)) {
    const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
    if (secretPatterns.some(re => re.test(text))) { secrets.push(relative); exclude(relative, size, 'sensitive_endpoint_or_token_metadata_not_published', scope); return; }
  }
  let storage = 'git';
  if (size >= 95 * 1024 * 1024) storage = 'release';
  const status = previous && previous.sha256 === digest ? previous.status : /(?:\/history-quarantine\/|\/_history\/|deprecated|superseded|rejected)/i.test(relative) ? 'history_reference_not_current' : scope === 'game_side_assets' ? 'game_side_file_not_acceptance' : 'source_material_check_record_authority';
  const record = { path: relative, scope, storage, status, bytes: size, sha256: digest, package_id: '', asset_id: previous?.asset_id || path.basename(relative).match(/(?:^|[-_])([MHFBNSTU]\d\d)(?:[-_.]|$)/i)?.[1]?.toUpperCase() || '', acceptance_receipt: previous?.receipt || '', runtime_accepted_by_export: false };
  const destination = path.join(storage === 'git' ? root : path.join(staging, 'snapshot'), relative);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  if (storage === 'release' && nativeCopies.has(digest)) {
    if (fs.existsSync(destination)) fs.unlinkSync(destination);
    fs.linkSync(nativeCopies.get(digest), destination);
  } else {
    if (storage === 'release' && fs.existsSync(destination)) fs.unlinkSync(destination);
    fs.writeFileSync(destination, bytes);
    if (storage === 'release') nativeCopies.set(digest, destination);
  }
  if (storage === 'git' && textFormats.has(ext)) copiedText.push({ path: relative, priority: oldTextMap.get(relative)?.priority || (relative.includes('/data/canon/') ? 'P1' : 'P2'), role: oldTextMap.get(relative)?.role || 'complete_' + scope + '_check_authority', origin_kind: 'project', bytes: size, sha256: digest });
  if (storage === 'release') {
    const bucket = nativeBucket(relative, scope).replace(/[^A-Za-z0-9_-]/g, '_');
    packageMap.set(bucket, [...(packageMap.get(bucket) || []), record]);
  }
  records.push(record);
}

function walk(relative, scope) {
  for (const entry of fs.readdirSync(path.join(source, relative), { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name, 'en'))) {
    const child = path.posix.join(relative, entry.name);
    if (entry.isSymbolicLink()) { exclude(child, 0, 'symlink_not_followed', scope); continue; }
    if (entry.isDirectory()) {
      if (skipDirs.has(entry.name)) { exclude(child + '/', 0, entry.name === 'vendor' ? 'third_party_originals_not_republished' : 'machine_cache_or_private_directory', scope); continue; }
      walk(child, scope);
    } else if (entry.isFile()) importFile(child, scope);
  }
}
for (const [relative, scope] of scopes) if (fs.existsSync(path.join(source, relative))) { console.log('Importing ' + relative); walk(relative, scope); }
for (const relative of ['scripts/canon-query.sh', 'scripts/canon_query.py']) importFile(relative, 'query_utilities');
const packages = [];
fs.mkdirSync(path.join(staging, 'lists'), { recursive: true });
for (const [bucket, rows] of packageMap) {
  let part = 1, current = [], currentBytes = 0;
  const flush = () => {
    if (!current.length) return;
    const packageId = bucket + '-' + String(part++).padStart(2, '0');
    current.forEach(r => { r.package_id = packageId; });
    const list = path.join(staging, 'lists', packageId + '.list');
    fs.writeFileSync(list, Buffer.from(current.map(r => r.path + '\0').join('')));
    packages.push({ package_id: packageId, file: packageId + '.tar.zst', files: current.length, source_bytes: currentBytes, member_list: list });
    current = []; currentBytes = 0;
  };
  for (const row of rows) { if (currentBytes + row.bytes > 1400 * 1024 * 1024) flush(); current.push(row); currentBytes += row.bytes; }
  flush();
}
records.sort((a, b) => a.path.localeCompare(b.path, 'en'));
const currentPaths = new Set(records.map(r => r.path));
for (const old of previousLibrary) {
  if (old.storage !== 'git' || currentPaths.has(old.path)) continue;
  const destination = path.resolve(root, old.path);
  if (destination.startsWith(root + path.sep) && fs.existsSync(destination) && sha(fs.readFileSync(destination)) === old.sha256) fs.unlinkSync(destination);
}
const writeTSV = (file, fields, rows) => fs.writeFileSync(path.join(root, file), [fields.join('\t'), ...rows.map(r => fields.map(k => clean(r[k])).join('\t'))].join('\n') + '\n');
writeTSV('review/library/FILE-MANIFEST.tsv', ['path', 'scope', 'storage', 'status', 'asset_id', 'bytes', 'sha256', 'package_id', 'acceptance_receipt', 'runtime_accepted_by_export'], records);
writeTSV('review/library/EXCLUSIONS.tsv', ['path', 'scope', 'bytes', 'reason'], exclusions);
fs.writeFileSync(path.join(out, 'PACKAGES.json'), JSON.stringify(packages.map(({ member_list, ...r }) => ({ ...r, url: 'https://github.com/Rayz17/super-gag-robot-war/releases/download/review-assets-20261026/' + r.file, upload_status: 'pending' })), null, 2) + '\n');
fs.writeFileSync(path.join(staging, 'build-plan.json'), JSON.stringify(packages, null, 2) + '\n');

const sourceTexts = new Map(copiedText.map(r => [r.path, r]));
for (const r of oldText) if (!sourceTexts.has(r.path) && r.origin_kind === 'project_specific_skill') sourceTexts.set(r.path, r);
const sortedTexts = [...sourceTexts.values()].sort((a, b) => a.path.localeCompare(b.path, 'en'));
writeTSV('review/SOURCE-MANIFEST.tsv', ['path', 'priority', 'role', 'origin_kind', 'bytes', 'sha256'], sortedTexts);
const metadataFile = path.join(root, 'review/snapshot-metadata.json'), metadata = JSON.parse(fs.readFileSync(metadataFile, 'utf8'));
metadata.included_files = sortedTexts.length; metadata.included_bytes = sortedTexts.reduce((s, r) => s + Number(r.bytes), 0); metadata.manifest_sha256 = sha(fs.readFileSync(path.join(root, 'review/SOURCE-MANIFEST.tsv')));
metadata.complete_library_date = '2026-10-26'; metadata.complete_library_manifest = 'review/library/FILE-MANIFEST.tsv';
fs.writeFileSync(metadataFile, JSON.stringify(metadata, null, 2) + '\n');

const byScope = {};
for (const r of records) { byScope[r.scope] ??= { files: 0, git_files: 0, release_files: 0, bytes: 0 }; byScope[r.scope].files++; byScope[r.scope][r.storage + '_files']++; byScope[r.scope].bytes += r.bytes; }
const stats = { date: '2026-10-26', requested_scope: 'complete_2d_art_and_settings_no_3d', three_d_included: false, source_scopes: scopes.map(([p, scope]) => ({ path: p, scope })), files: records.length, git_files: records.filter(r => r.storage === 'git').length, release_files: records.filter(r => r.storage === 'release').length, bytes: records.reduce((s, r) => s + r.bytes, 0), packages: packages.length, text_files: sortedTexts.length, by_scope: byScope, exclusion_records: exclusions.length, secret_signal_files: secrets, source_modified: false, asset_acceptance_granted: false };
fs.writeFileSync(path.join(out, 'IMPORT-RESULT.json'), JSON.stringify(stats, null, 2) + '\n');
console.log(JSON.stringify(stats, null, 2));
