import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.resolve(process.argv[2] || '');
if (!process.argv[2] || root === source) throw new Error('Separate source project required');
const loadTSV = relative => {
  const lines = fs.readFileSync(path.join(root, relative), 'utf8').trimEnd().split('\n');
  const fields = lines.shift().split('\t');
  return { fields, rows: lines.map(line => Object.fromEntries(line.split('\t').map((v, i) => [fields[i], v]))) };
};
const writeTSV = (relative, data) => fs.writeFileSync(path.join(root, relative), [data.fields.join('\t'), ...data.rows.map(row => data.fields.map(key => String(row[key] ?? '').replace(/[\t\r\n]/g, ' ')).join('\t'))].join('\n') + '\n');
const manifest = loadTSV('review/library/FILE-MANIFEST.tsv');
const exclusions = loadTSV('review/library/EXCLUSIONS.tsv');
const sources = loadTSV('review/SOURCE-MANIFEST.tsv');
const existing = new Set(manifest.rows.map(row => row.path));
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const scopes = [
  ['outputs', 'early_2d_candidates_and_evidence'],
  ['demo/chapter1/assets', 'historical_demo_2d'],
  ['artifacts/formulas/production-lab-v1/source', 'source_2d_design_sheets'],
];
let added = 0;
function walk(relative, scope, base) {
  const directory = path.join(source, relative);
  if (!fs.existsSync(directory)) return;
  for (const item of fs.readdirSync(directory, { withFileTypes: true })) {
    const next = path.posix.join(relative, item.name);
    if (item.isSymbolicLink()) continue;
    if (item.isDirectory()) {
      if (['vendor', 'research', '.git', '.godot', 'node_modules', 'textures', 'materials', 'models', 'blender'].includes(item.name)) continue;
      walk(next, scope, base);
      continue;
    }
    if (!item.isFile() || existing.has(next)) continue;
    const bytes = fs.readFileSync(path.join(source, next));
    const ext = path.extname(next).toLowerCase();
    const image = /\.(?:png|jpe?g|webp|svg|psd|kra|ora|xcf|aseprite|ase)$/i.test(next);
    const note = ext === '.md';
    let allowed = image || note;
    let reason = 'not_2d_art_or_design_note';
    if (scope === 'source_2d_design_sheets') {
      const sub = next.slice(base.length + 1);
      const parts = sub.split('/');
      const flat = parts.length === 2 || (parts.length === 3 && parts[1] === 'rejected');
      const threeD = /^(?:guardian-meshy|linked-campaign-models|stage-art)/.test(parts[0]);
      const excluded = /(?:atlas|paint|projection|inspection|inspect|runtime-|rig-|meshy|crop-contact|coordinate-review)/i.test(sub);
      allowed = image && flat && !threeD && !excluded;
      reason = '3d_source_or_qa_not_2d_design_sheet';
    }
    if (allowed && scope === 'source_2d_design_sheets' && /(?:[_-](?:normal(?:map)?|roughness|metallic|occlusion|base_?color|albedo|orm|diffuse|texture)(?:[_-]\d+)?|_Image_\d+)\.(?:png|jpe?g|webp)$/i.test(next)) { allowed = false; reason = '3d_texture_map_excluded_by_user'; }
    if (!allowed) {
      exclusions.rows.push({ path: next, scope, bytes: bytes.length, reason });
      continue;
    }
    if (note && /(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}|-----BEGIN .*PRIVATE KEY-----)/.test(bytes.toString('utf8'))) throw new Error('Sensitive source note: ' + next);
    const destination = path.join(root, next);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.writeFileSync(destination, bytes);
    const digest = sha(bytes);
    const status = scope === 'historical_demo_2d' || /(?:rejected|not-adopted|pre-user|unbound)/i.test(next) ? 'history_reference_not_current' : 'candidate_or_production_reference_check_original_receipt';
    manifest.rows.push({ path: next, scope, storage: 'git', status, asset_id: '', bytes: bytes.length, sha256: digest, package_id: '', acceptance_receipt: '', runtime_accepted_by_export: false });
    if (note || ext === '.svg') sources.rows.push({ path: next, priority: 'P2', role: scope, origin_kind: 'project', bytes: bytes.length, sha256: digest });
    existing.add(next);
    added++;
  }
}
for (const [relative, scope] of scopes) walk(relative, scope, relative);
manifest.rows.sort((a, b) => a.path.localeCompare(b.path, 'en'));
sources.rows.sort((a, b) => a.path.localeCompare(b.path, 'en'));
writeTSV('review/library/FILE-MANIFEST.tsv', manifest);
writeTSV('review/library/EXCLUSIONS.tsv', exclusions);
writeTSV('review/SOURCE-MANIFEST.tsv', sources);
const statsPath = path.join(root, 'review/library/IMPORT-RESULT.json');
const stats = JSON.parse(fs.readFileSync(statsPath, 'utf8'));
stats.files = manifest.rows.length;
stats.git_files = manifest.rows.length;
stats.bytes = manifest.rows.reduce((sum, row) => sum + Number(row.bytes), 0);
stats.text_files = sources.rows.length;
stats.exclusion_records = exclusions.rows.length;
stats.source_scopes = [...stats.source_scopes.filter(row => !scopes.some(([p]) => row.path === p)), ...scopes.map(([p, scope]) => ({ path: p, scope }))];
stats.by_scope = {};
for (const row of manifest.rows) {
  const group = stats.by_scope[row.scope] ??= { files: 0, git_files: 0, release_files: 0, bytes: 0 };
  group.files++;
  group.git_files++;
  group.bytes += Number(row.bytes);
}
fs.writeFileSync(statsPath, JSON.stringify(stats, null, 2) + '\n');
const metaPath = path.join(root, 'review/snapshot-metadata.json');
const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
meta.included_files = sources.rows.length;
meta.included_bytes = sources.rows.reduce((sum, row) => sum + Number(row.bytes), 0);
meta.excluded_files = exclusions.rows.length;
meta.manifest_sha256 = sha(fs.readFileSync(path.join(root, 'review/SOURCE-MANIFEST.tsv')));
fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2) + '\n');
console.log(JSON.stringify({ added, files: stats.files, text_files: stats.text_files, bytes: stats.bytes }, null, 2));
