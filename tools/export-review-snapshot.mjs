import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const target = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = process.argv[2] && path.resolve(process.argv[2]);
if (!source || source === target || !fs.existsSync(path.join(source, 'docs/superpowers/specs/data/canon/authority_manifest.tsv'))) {
  throw new Error('Usage: node tools/export-review-snapshot.mjs /absolute/source/project');
}
const allowed = new Set(['.md', '.tsv', '.csv', '.json', '.txt', '.yaml', '.yml', '.toml', '.mmd', '.html', '.svg']);
const maxBytes = 2_000_000;
const records = [];
const excluded = [];
const oldManifest = path.join(target, 'review/SOURCE-MANIFEST.tsv');
const previousPaths = fs.existsSync(oldManifest) ? fs.readFileSync(oldManifest, 'utf8').trimEnd().split('\n').slice(1).map(line => line.split('\t')[0]) : [];
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const clean = value => String(value).replace(/[\t\r\n]/g, ' ');
const story = 'docs/superpowers/specs/剧情梗概/V35全剧故事重构-2026-09-11/';
const prose = 'docs/superpowers/specs/story-runtime/effect-tests/C01-C03-prose-refinement-2026-09-09/';
const c04 = 'docs/superpowers/specs/story-runtime/effect-tests/C04-author-first-2026-09-05/reader-build/';
const coreStory = new Set(['27-全剧故事概要-v5.md', '28-全剧玩法与真实分支构思-v5.md', '30-概要定点收口与逐章写作计划-v1.md', '31-全剧分章与展开安排-v1.md', '32-C05章级展开卡-v1.md'].map(p => story + p));
const productionKeep = ['游戏制作方法与工程约定.md', '体验批次模板.md', 'experience-production-loop.svg', 'art-direction-v0.3/', 'battle-presentation-v0.1/', 'multi-play-runtime/'];
const utilityScripts = ['canon-query.sh', 'canon_query.py'];
const proseChapters = new Set(['C01-纯剧情章节Reader-修订稿.md', 'C02-纯剧情章节Reader-修订稿.md', 'C03-纯剧情章节Reader-修订稿.md'].map(p => prose + p));

function classify(relative) {
  if (coreStory.has(relative)) return ['P0', 'current_story_candidate'];
  if (relative.startsWith(prose) && !relative.includes('/_history/')) return [proseChapters.has(relative) ? 'P0' : 'P1', 'event_preserving_prose_revision'];
  if (relative.startsWith(c04) && !relative.includes('/_history/')) return [relative === c04 + 'C04-纯剧情章节Reader.md' ? 'P0' : 'P1', 'new_C04_story_and_adaptation'];
  if (/game-design\/[^/]+\/00(?:c-core-game-design-master-review|-user-reading-guide)\.md$/.test(relative)) return ['P0', 'gameplay_integrated_design'];
  if (relative.includes('/data/canon/')) return ['P1', 'authority_source_mixed_record_levels'];
  if (/\/data\/character_(?:layer|voice|runtime)\//.test(relative)) return ['P1', 'character_support_check_source'];
  if (relative.includes('/data/design_graph/')) return ['P1', 'document_graph_mixed_lifecycles'];
  if (relative.includes('/work-packages/2026-10-02-')) return ['P1', 'later_gameplay_candidate'];
  if (relative.includes('/work-packages/')) return ['P2', 'gameplay_iteration_and_feedback'];
  if (relative.includes('/workflow-skills/')) return ['P1', 'workflow_reference_snapshot'];
  if (relative.startsWith('研究报告/')) return ['P1', 'srw_crossover_reference_research'];
  if (relative.startsWith('scripts/')) return ['P1', 'readonly_query_or_check_utility'];
  if (relative.endsWith('2026-09-05-chao-gag-author-first-writing-method-v1.md')) return ['P1', 'current_writing_method'];
  if (relative.startsWith(story)) return ['P2', 'earlier_story_iteration_or_material'];
  if (relative.includes('/effect-tests/') || relative.includes('/_history/') || relative.includes('/history-quarantine/')) return ['P2', 'experiment_or_history_not_default_input'];
  if (relative.includes('/V35.9/rebuild/')) return ['P1', 'formal_chain_or_reference_check_current_status'];
  return ['P2', 'support_or_legacy_check_authority'];
}

function exclusion(relative, size) {
  if (!allowed.has(path.extname(relative).toLowerCase())) return 'not_selected_document_format';
  if (size > maxBytes) return 'large_file_over_2MB';
  if (/(?:^|\/)(?:\.git|\.obsidian|node_modules|__pycache__|\.godot)(?:\/|$)/.test(relative)) return 'local_or_vendor_state';
  if (/(?:\/_history\/.*\/workspace\/|\/before-[^/]*\/workspace\/)/.test(relative)) return 'duplicate_workspace_snapshot';
  if (/\/story-runtime\/(?:generated|context-packs|inbox)\//.test(relative)) return 'generated_index_or_transient_context';
  if (/\/09-rea-binary-research\/(?:evidence|OGS-)/.test(relative)) return 'third_party_binary_research_dump';
  if (/(?:fixture|smoke|capture|frame-manifest|screenshot|runtime-output|event-trace|replay-events)/i.test(path.basename(relative))) return 'generated_test_or_capture_evidence';
  const productionPrefix = 'docs/superpowers/specs/production/';
  if (relative.startsWith(productionPrefix)) {
    const rest = relative.slice(productionPrefix.length);
    if (!productionKeep.some(p => p.endsWith('/') ? rest.startsWith(p) : rest === p)) return 'implementation_production_evidence_out_of_scope';
  }
  if (/\/(?:\.env(?:\.[^/]*)?|credentials[^/]*|[^/]*\.pem|[^/]*\.key)$/.test(relative)) return 'private_configuration';
  return null;
}

function copyFile(from, relative, originKind = 'project') {
  const bytes = fs.readFileSync(from);
  try { new TextDecoder('utf-8', { fatal: true }).decode(bytes); }
  catch { excluded.push({ path: relative, bytes: bytes.length, reason: 'non_utf8_document' }); return; }
  const destination = path.join(target, relative);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, bytes);
  fs.chmodSync(destination, fs.statSync(from).mode & 0o777);
  const [priority, role] = classify(relative);
  records.push({ path: relative, priority, role, origin_kind: originKind, bytes: bytes.length, sha256: hash(bytes) });
}

function walk(directory, prefix) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name, 'en'))) {
    const from = path.join(directory, entry.name);
    const relative = path.posix.join(prefix, entry.name);
    if (entry.isSymbolicLink()) { excluded.push({ path: relative, bytes: 0, reason: 'symlink_not_followed' }); continue; }
    if (entry.isDirectory()) { walk(from, relative); continue; }
    if (!entry.isFile()) continue;
    const size = fs.statSync(from).size;
    const reason = exclusion(relative, size);
    if (reason) excluded.push({ path: relative, bytes: size, reason });
    else copyFile(from, relative);
  }
}

walk(path.join(source, 'docs'), 'docs');
walk(path.join(source, '研究报告'), '研究报告');
for (const name of utilityScripts) copyFile(path.join(source, 'scripts', name), 'scripts/' + name);
const skillRoot = path.join(process.env.HOME, '.codex', 'skills');
for (const name of ['chao-gag-canon', 'chao-gag-story-writer', 'chao-gag-writing-pipeline']) {
  const root = path.join(skillRoot, name);
  function skillWalk(directory) {
    for (const e of fs.readdirSync(directory, { withFileTypes: true })) {
      const p = path.join(directory, e.name);
      if (e.isDirectory()) { if (!['.git', '__pycache__'].includes(e.name)) skillWalk(p); }
      else if (e.isFile() && /\.(?:md|tsv|json|py|sh)$/.test(e.name) && fs.statSync(p).size <= maxBytes) {
        copyFile(p, path.posix.join('review/workflow-skills', name, path.relative(root, p).split(path.sep).join('/')), 'project_specific_skill');
      }
    }
  }
  skillWalk(root);
}
records.sort((a, b) => a.path.localeCompare(b.path, 'en'));
excluded.sort((a, b) => a.path.localeCompare(b.path, 'en'));
const currentPaths = new Set(records.map(r => r.path));
for (const relative of previousPaths) {
  const destination = path.resolve(target, relative);
  if (!destination.startsWith(target + path.sep)) throw new Error('Unsafe previous manifest path');
  if (!currentPaths.has(relative) && fs.existsSync(destination)) fs.unlinkSync(destination);
}
const columns = ['path', 'priority', 'role', 'origin_kind', 'bytes', 'sha256'];
fs.writeFileSync(path.join(target, 'review/SOURCE-MANIFEST.tsv'), [columns.join('\t'), ...records.map(r => columns.map(k => clean(r[k])).join('\t'))].join('\n') + '\n');
fs.writeFileSync(path.join(target, 'review/EXCLUDED-FILES.tsv'), ['path\tbytes\treason', ...excluded.map(r => [r.path, r.bytes, r.reason].map(clean).join('\t'))].join('\n') + '\n');
const metadata = {
  as_of_client_date: '2026-10-22',
  purpose: 'external_story_setting_game_design_review',
  source_branch: execFileSync('git', ['branch', '--show-current'], { cwd: source, encoding: 'utf8' }).trim(),
  source_head: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: source, encoding: 'utf8' }).trim(),
  includes_uncommitted_workspace_documents: true,
  source_head_is_not_document_snapshot: true,
  repository_visibility_observed: 'private',
  included_files: records.length,
  included_bytes: records.reduce((sum, r) => sum + r.bytes, 0),
  excluded_files: excluded.length,
  manifest_sha256: hash(fs.readFileSync(path.join(target, 'review/SOURCE-MANIFEST.tsv'))),
  source_files_modified_by_export: false,
  excluded_root_areas: ['game-godot', 'artifacts', 'captures', 'outputs', 'qa', 'external_repos', 'other_vaults', 'other_projects', 'git_history'],
};
fs.writeFileSync(path.join(target, 'review/snapshot-metadata.json'), JSON.stringify(metadata, null, 2) + '\n');
console.log(JSON.stringify(metadata, null, 2));
