import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = process.argv[2] ? path.resolve(process.argv[2]) : null;
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const lines = fs.readFileSync(path.join(root, 'review/art/ASSET-MANIFEST.tsv'), 'utf8').trimEnd().split('\n');
const keys = lines.shift().split('\t');
const records = lines.map(line => Object.fromEntries(line.split('\t').map((value, i) => [keys[i], value])));
const errors = [], sourceDrift = [], secretSignals = [], seen = new Set();
const statuses = new Set(['source_record', 'confirmed_source_design', 'parent_context_only', 'authorized_derived_support_not_individually_accepted', 'authorized_derived_support', 'confirmed_scoped_parent_not_runtime_acceptance', 'approved_style_language_example', 'confirmed_nonseparable_frame_anchor', 'style_example_not_current_identity', 'negative_comparison_not_adopted', 'style_reference', 'user_confirmed_tactics_target']);
const strongSecrets = [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, /\bgh[pousr]_[A-Za-z0-9]{30,}\b/, /\bgithub_pat_[A-Za-z0-9_]{30,}\b/, /\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b/, /\bAKIA[0-9A-Z]{16}\b/, /Authorization\s*:\s*Bearer\s+[A-Za-z0-9_.-]{30,}/i];

function imageDimensions(bytes, relative) {
  if (/\.png$/i.test(relative)) {
    if (bytes.length < 24 || !bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10])) || bytes.toString('ascii', 12, 16) !== 'IHDR') throw new Error('bad_png_header');
    return [bytes.readUInt32BE(16), bytes.readUInt32BE(20)];
  }
  if (/\.jpe?g$/i.test(relative)) {
    if (bytes.readUInt16BE(0) !== 0xffd8) throw new Error('bad_jpeg_header');
    let offset = 2;
    while (offset < bytes.length) {
      if (bytes[offset++] !== 0xff) throw new Error('bad_jpeg_marker');
      while (bytes[offset] === 0xff) offset++;
      const marker = bytes[offset++];
      if (marker === 0xd9 || marker === 0xda) break;
      if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd8)) continue;
      const length = bytes.readUInt16BE(offset);
      if (length < 2 || offset + length > bytes.length) throw new Error('bad_jpeg_segment');
      if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(marker)) return [bytes.readUInt16BE(offset + 5), bytes.readUInt16BE(offset + 3)];
      offset += length;
    }
    throw new Error('jpeg_dimensions_missing');
  }
  throw new Error('unsupported_raster_format');
}

for (const record of records) {
  if (seen.has(record.path)) errors.push('duplicate:' + record.path);
  seen.add(record.path);
  const full = path.resolve(root, record.path);
  if (!full.startsWith(root + path.sep) || !fs.existsSync(full)) { errors.push('missing_or_unsafe:' + record.path); continue; }
  const bytes = fs.readFileSync(full);
  if (sha(bytes) !== record.sha256 || bytes.length !== Number(record.bytes)) errors.push('hash_or_size:' + record.path);
  if (bytes.length >= 100 * 1024 * 1024) errors.push('github_file_size_limit:' + record.path);
  if (!statuses.has(record.status) || !record.scope || !record.asset_id) errors.push('missing_or_unknown_scope:' + record.path);
  if (record.runtime_accepted !== 'false') errors.push('ungranted_runtime_acceptance:' + record.path);
  if (!record.receipt || !fs.existsSync(path.join(root, record.receipt))) errors.push('missing_receipt:' + record.path);
  if (/\.(?:png|jpe?g|webp)$/i.test(record.path)) {
    try {
      const [width, height] = imageDimensions(bytes, record.path);
      if (!width || !height || width !== Number(record.pixel_width) || height !== Number(record.pixel_height)) errors.push('image_dimensions:' + record.path);
    } catch (error) { errors.push(error.message + ':' + record.path); }
  } else {
    const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
    if (strongSecrets.some(pattern => pattern.test(text))) secretSignals.push(record.path);
    if (record.path.endsWith('.json')) {
      try { JSON.parse(text); } catch { errors.push('invalid_json:' + record.path); }
    }
    if (record.path.endsWith('.svg') && !/<svg\b/.test(text)) errors.push('invalid_svg:' + record.path);
  }
  if (source) {
    const original = path.join(source, record.path);
    if (!fs.existsSync(original) || sha(fs.readFileSync(original)) !== record.sha256) sourceDrift.push(record.path);
  }
}

const excludedPaths = new Set(fs.readFileSync(path.join(root, 'review/library/EXCLUSIONS.tsv'), 'utf8').split('\n').slice(1).filter(line => line.endsWith('\toutside_external_design_art_scope_uiue_or_execution_evidence')).map(line => line.split('\t')[0]));
let htmlImageLinks = 0, intentionallyExcludedLinks = 0;
for (const record of records.filter(item => item.path.endsWith('.html'))) {
  const full = path.join(root, record.path), html = fs.readFileSync(full, 'utf8');
  // Only the visual-reference page promises a complete local image set.
  if (!record.path.endsWith('/给Astra的视觉总参考.html')) continue;
  for (const match of html.matchAll(/<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi)) {
    if (/^(?:https?:|data:)/.test(match[1])) continue;
    htmlImageLinks++;
    const linked = path.resolve(path.dirname(full), match[1]);
    if (!fs.existsSync(linked)) {
      if (excludedPaths.has(path.relative(root, linked))) intentionallyExcludedLinks++;
      else errors.push('visual_reference_missing_image:' + match[1]);
    }
  }
}
const stats = JSON.parse(fs.readFileSync(path.join(root, 'review/art/IMPORT-RESULT.json'), 'utf8'));
const byStatus = {};
for (const record of records) byStatus[record.status] = (byStatus[record.status] || 0) + 1;
const images = records.filter(item => /\.(?:png|jpe?g|webp)$/i.test(item.path)).length;
const vectors = records.filter(item => item.path.endsWith('.svg')).length;
const bytes = records.reduce((sum, item) => sum + Number(item.bytes), 0);
if (stats.files !== records.length || stats.images !== images || stats.vectors !== vectors || stats.bytes !== bytes || JSON.stringify(stats.by_status) !== JSON.stringify(byStatus)) errors.push('import_stats_mismatch');
const result = { pass: !errors.length && !sourceDrift.length && !secretSignals.length, files: records.length, images, vectors, bytes, by_status: byStatus, original_visual_reference_image_links: htmlImageLinks, links_explicitly_excluded_by_user_scope: intentionallyExcludedLinks, errors, secret_signal_files: secretSignals, live_source_comparison: source ? 'performed' : 'not_requested', source_drift: sourceDrift, visual_quality_acceptance: 'not_granted_by_integrity_check', runtime_acceptance: 'not_performed' };
fs.writeFileSync(path.join(root, 'review/art/VALIDATION.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result, null, 2));
if (!result.pass) process.exitCode = 1;
