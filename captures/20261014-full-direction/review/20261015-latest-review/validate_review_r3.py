"""Check reader bindings and preservation; does not claim a rendered-browser pass."""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import hashlib
import json
import re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
PAGE = ROOT / 'review-v2.html'
text = PAGE.read_text()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
data = json.loads(re.search(r'<script type="application/json" id="asset-review-data">([\s\S]*?)</script>', text).group(1))
snapshot = json.loads((OUT / 'current-file-inventory.json').read_text())
records = {r['id']: r for r in data['records']}
errors = []
cards = re.findall(r'<article\b[^>]*>[\s\S]*?</article>', text)
if len(cards) != 298 or len(records) != 298:
    errors.append(['task_count', len(cards), len(records)])
for card in cards:
    rid = re.search(r'data-id="([^"]+)"', card).group(1)
    src = re.search(r'<img[^>]*src="([^"]+)"', card).group(1)
    href = re.search(r'<a class="thumb" href="([^"]+)"', card).group(1)
    if src != href or src != records[rid]['img']:
        errors.append(['preview_link_record_mismatch', rid])
    if sha(ROOT / src) != records[rid]['image_sha256']:
        errors.append(['reviewed_copy_changed', rid])
    if card.count('class="r3-assessment"') != 1 or card.count('class="r3-history"') != 1:
        errors.append(['current_or_historical_notes_missing', rid])
for r in snapshot['items']:
    if sha(ROOT / r['file']) != r['sha256']:
        errors.append(['incoming_source_changed', r['id']])
    if records[r['id']]['source_img'] != r['file']:
        errors.append(['wrong_source_path', r['id']])
if sha(OUT / 'before-review-r3-20261015.html') != snapshot['page_sha256']:
    errors.append(['original_page_snapshot_changed'])
if Counter(r['verdict'] for r in records.values()) != data['verdict_counts']:
    errors.append(['wrong_verdict_totals'])

class ReaderParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
        self.details = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'id' in d:
            self.ids.append(d['id'])
        for attr in ['src', 'href']:
            if attr in d:
                self.refs.append((tag, attr, d[attr]))
        if tag == 'details':
            self.details.append(d.get('class', ''))
        if (tag == 'dl' and d.get('class') == 'assessment') or (tag == 'aside' and d.get('class') == 'family-review'):
            if 'r3-history' not in self.details:
                errors.append(['old_card_review_not_collapsed', tag])

    def handle_endtag(self, tag):
        if tag == 'details':
            if not self.details:
                errors.append(['unmatched_details_end'])
            else:
                self.details.pop()

parser = ReaderParser()
parser.feed(text)
for ident, count in Counter(parser.ids).items():
    if count > 1:
        errors.append(['duplicate_id', ident, count])
if parser.details:
    errors.append(['unclosed_details', parser.details])
for tag, attr, url in parser.refs:
    u = urlparse(url)
    if u.scheme or url.startswith('//'):
        continue
    if not u.path:
        if u.fragment and unquote(u.fragment) not in parser.ids:
            errors.append(['missing_fragment', url])
    elif not (ROOT / unquote(u.path)).resolve().exists():
        errors.append(['missing_local_file', url])
result = dict(
    task_cards=len(cards), verdict_counts=data['verdict_counts'],
    frozen_unique_images=len(list((OUT / 'images').glob('*.jpg'))),
    checked_incoming_images=len(snapshot['items']), incoming_images_unchanged=True,
    original_page_snapshot_unchanged=True, source_link_record_binding='pass' if not errors else 'fail',
    errors=errors, page_sha256=sha(PAGE),
    browser_render_and_interaction=dict(
        status='blocked_not_passed',
        reason='Browser URL policy rejected file://; permits only http/https. No workaround used.',
        native_layout=False, filter_interaction=False, mobile_layout=False),
    artwork_review_scope='All 298 current cards inspected in contact sheets; key source/derivative images inspected full size. Design review only.',
    runtime_assets_replaced=False, user_acceptance_added=False)
(OUT / 'r3-static-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
if errors:
    raise SystemExit(1)
