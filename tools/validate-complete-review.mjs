import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const staging = process.argv[2] && path.resolve(process.argv[2]);
const text = fs.readFileSync(path.join(root, 'review/library/FILE-MANIFEST.tsv'), 'utf8').trimEnd().split('\n');
const keys = text.shift().split('\t');
const records = text.map(l => Object.fromEntries(l.split('\t').map((v, i) => [keys[i], v])));
const packages = JSON.parse(fs.readFileSync(path.join(root, 'review/library/PACKAGES.json'), 'utf8'));
const stats = JSON.parse(fs.readFileSync(path.join(root, 'review/library/IMPORT-RESULT.json'), 'utf8'));
const packageMap = new Map(packages.map(p => [p.package_id, p]));
const errors = [], seen = new Set(), membership = new Map();
const forbidden3d = new Set(['.glb', '.gltf', '.blend', '.blend1', '.fbx', '.obj', '.mtl', '.scn', '.res', '.exr', '.hdr']);
const digest = async file => { const h = crypto.createHash('sha256'); for await (const b of fs.createReadStream(file)) h.update(b); return h.digest('hex'); };
for (const r of records) {
  if (!r.path || path.isAbsolute(r.path) || r.path.split('/').includes('..') || seen.has(r.path)) { errors.push('unsafe_or_duplicate:' + r.path); continue; }
  seen.add(r.path);
  if (forbidden3d.has(path.extname(r.path).toLowerCase())) errors.push('3d_asset_forbidden_by_user:' + r.path);
  if (!r.scope || !r.status || !/^[a-f0-9]{64}$/.test(r.sha256) || r.runtime_accepted_by_export !== 'false') errors.push('missing_scope_or_ungranted_acceptance:' + r.path);
  if (!['git', 'release'].includes(r.storage)) { errors.push('unknown_storage:' + r.path); continue; }
  if (r.storage === 'release') {
    if (!packageMap.has(r.package_id)) errors.push('missing_package:' + r.path);
    const group = membership.get(r.package_id) || { files: 0, bytes: 0 };
    group.files++; group.bytes += Number(r.bytes); membership.set(r.package_id, group);
  }
  const full = r.storage === 'git' ? path.join(root, r.path) : staging ? path.join(staging, 'snapshot', r.path) : null;
  if (full && (!fs.existsSync(full) || fs.statSync(full).size !== Number(r.bytes) || await digest(full) !== r.sha256)) errors.push('file_hash_or_size:' + r.path);
}
for (const p of packages) {
  const group = membership.get(p.package_id);
  if (!group || group.files !== p.files || group.bytes !== p.source_bytes) errors.push('package_members:' + p.package_id);
  if (!p.archive_bytes || !p.sha256 || p.archive_bytes >= 2 * 1024 ** 3) errors.push('unbuilt_or_oversize_package:' + p.package_id);
  if (staging) {
    const archive = path.join(staging, 'archives', p.file);
    if (!fs.existsSync(archive) || fs.statSync(archive).size !== p.archive_bytes || await digest(archive) !== p.sha256) errors.push('package_hash_or_size:' + p.package_id);
  }
}
if (stats.files !== records.length || stats.git_files !== records.filter(r => r.storage === 'git').length || stats.release_files !== records.filter(r => r.storage === 'release').length || stats.packages !== packages.length) errors.push('coverage_stats');
if (stats.three_d_included !== false || stats.release_files || packages.length) errors.push('unexpected_3d_or_binary_attachment_scope');
const result = { pass: !errors.length, files: records.length, git_files: stats.git_files, release_files: stats.release_files, packages: packages.length, three_d_assets_included: false, snapshot_hash_validation: 'all_2d_and_setting_git_files', remote_upload: 'verify_git_tree_after_push', errors, source_modified: false, visual_or_runtime_acceptance: 'not_granted' };
fs.writeFileSync(path.join(root, 'review/library/VALIDATION.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
if (!result.pass) process.exitCode = 1;
