import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = process.argv[2] ? path.resolve(process.argv[2]) : null;
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const manifestPath = path.join(root, 'review/SOURCE-MANIFEST.tsv');
const lines = fs.readFileSync(manifestPath, 'utf8').trimEnd().split('\n');
const keys = lines.shift().split('\t');
const records = lines.map(l => Object.fromEntries(l.split('\t').map((v, i) => [keys[i], v])));
const errors = [];
const secretSignals = [];
const sourceDrift = [];
const seen = new Set();
const strongSecrets = [
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,
  /\bgh[pousr]_[A-Za-z0-9]{30,}\b/,
  /\bgithub_pat_[A-Za-z0-9_]{30,}\b/,
  /\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b/,
  /\bAKIA[0-9A-Z]{16}\b/,
  /Authorization\s*:\s*Bearer\s+[A-Za-z0-9_.-]{30,}/i,
];
for (const r of records) {
  if (seen.has(r.path)) errors.push('duplicate:' + r.path);
  seen.add(r.path);
  const full = path.resolve(root, r.path);
  if (!full.startsWith(root + path.sep) || !fs.existsSync(full)) { errors.push('missing_or_unsafe:' + r.path); continue; }
  const bytes = fs.readFileSync(full);
  if (sha(bytes) !== r.sha256 || bytes.length !== Number(r.bytes)) errors.push('hash_or_size:' + r.path);
  const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  if (strongSecrets.some(re => re.test(text))) secretSignals.push(r.path);
  if (source) {
    const original = r.origin_kind === 'project_specific_skill'
      ? path.join(process.env.HOME, '.codex/skills', r.path.slice('review/workflow-skills/'.length))
      : path.join(source, r.path);
    if (!fs.existsSync(original) || sha(fs.readFileSync(original)) !== r.sha256) sourceDrift.push(r.path);
  }
}
const meta = JSON.parse(fs.readFileSync(path.join(root, 'review/snapshot-metadata.json'), 'utf8'));
if (meta.included_files !== records.length || meta.manifest_sha256 !== sha(fs.readFileSync(manifestPath))) errors.push('metadata_manifest_mismatch');
const navigation = ['README.md', 'AGENTS.md', 'review/01-阅读指南与当前资料.md', 'review/02-外部评审提示词.md', 'review/03-版本分歧与待核问题.md', 'review/SNAPSHOT.md'];
let navigationLinks = 0;
for (const relative of navigation) {
  const full = path.join(root, relative), text = fs.readFileSync(full, 'utf8');
  if (text.includes('\r') || !text.endsWith('\n') || /[ \t]+$/m.test(text)) errors.push('navigation_whitespace:' + relative);
  for (const match of text.matchAll(/\[[^\]\n]*\]\((?:<([^>]+)>|([^\s)]+))\)/g)) {
    const url = match[1] || match[2];
    if (/^[a-z][a-z0-9+.-]*:/i.test(url) || url.startsWith('#')) continue;
    navigationLinks++;
    if (!fs.existsSync(path.resolve(path.dirname(full), decodeURIComponent(url.split('#')[0])))) errors.push('navigation_link:' + relative + ':' + url);
  }
}
const gaps = [];
for (const r of records.filter(r => r.path.endsWith('.md'))) {
  const full = path.join(root, r.path), text = fs.readFileSync(full, 'utf8');
  for (const match of text.matchAll(/\[[^\]\n]*\]\((?:<([^>]+)>|([^\s)]+))\)/g)) {
    const url = match[1] || match[2];
    if (/^[a-z][a-z0-9+.-]*:/i.test(url) || url.startsWith('#')) continue;
    let destination;
    try { destination = path.resolve(path.dirname(full), decodeURIComponent(url.split('#')[0])); }
    catch { gaps.push([r.path, url, 'unparseable_original_link']); continue; }
    if (!fs.existsSync(destination)) gaps.push([r.path, url, path.isAbsolute(url) ? 'original_machine_path_unavailable' : 'omitted_media_source_or_original_gap']);
  }
}
fs.writeFileSync(path.join(root, 'review/LINK-GAPS.tsv'), ['source_path\ttarget\treason', ...gaps.map(row => row.map(v => String(v).replace(/[\t\r\n]/g, ' ')).join('\t'))].join('\n') + '\n');
const result = { pass: !errors.length && !secretSignals.length && !sourceDrift.length, source_files: records.length, source_bytes: records.reduce((sum, r) => sum + Number(r.bytes), 0), navigation_links: navigationLinks, original_link_gaps: gaps.length, errors, secret_signal_files: secretSignals, live_source_comparison: source ? 'performed' : 'not_requested', source_drift: sourceDrift };
fs.writeFileSync(path.join(root, 'review/VALIDATION.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
if (!result.pass) process.exitCode = 1;
