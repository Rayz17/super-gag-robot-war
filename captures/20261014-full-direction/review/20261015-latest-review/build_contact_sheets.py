from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import re, html, json, hashlib, collections

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
page = ROOT / 'review-v2.html'
text = page.read_text()
rows = []
for card in re.findall(r'<article\b[^>]*>[\s\S]*?</article>', text):
    rid = re.search(r'data-id="([^"]+)"', card).group(1)
    src = re.search(r'<img[^>]*src="([^"]+)"', card).group(1)
    name = html.unescape(re.sub('<[^>]+>', '', re.search(r'<h3[^>]*>(.*?)</h3>', card).group(1)))
    path = ROOT / src
    image = Image.open(path)
    old = re.search(r'<dl class="assessment">([\s\S]*?)</dl>', card)
    rows.append(dict(id=rid, group=rid[0], name=name, file=src,
                     sha256=hashlib.sha256(path.read_bytes()).hexdigest(), size=list(image.size),
                     card_verdict_before=re.search(r'data-verdict="([^"]+)"', card).group(1),
                     old_review=html.unescape(re.sub('<[^>]+>', ' ', old.group(1))) if old else ''))
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
font = ImageFont.truetype(font_path, 20)
small = ImageFont.truetype(font_path, 13)
sheets = []
for group in collections.OrderedDict.fromkeys(row['group'] for row in rows):
    entries = [r for r in rows if r['group'] == group]
    for start in range(0, len(entries), 12):
        chunk = entries[start:start + 12]
        sheet = Image.new('RGB', (1536, 326 * ((len(chunk) + 2) // 3)), '#eeeae0')
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(chunk):
            x, y = i % 3 * 512, i // 3 * 326
            image = ImageOps.contain(Image.open(ROOT / row['file']).convert('RGB'), (500, 281))
            sheet.paste(image, (x + (512 - image.width) // 2, y))
            draw.text((x + 8, y + 284), row['id'] + ' ' + row['name'][:15], font=font, fill='#123a40')
            draw.text((x + 8, y + 307), Path(row['file']).stem[-34:], font=small, fill='#55646a')
        name = f'{group}-{start // 12 + 1:02d}.jpg'
        sheet.save(OUT / name, quality=91)
        sheets.append(dict(sheet=name, ids=[r['id'] for r in chunk]))
(OUT / 'current-file-inventory.json').write_text(json.dumps(dict(
    page_sha256=hashlib.sha256(text.encode()).hexdigest(), items=rows, sheets=sheets
), ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(count=len(rows), sheets=sheets), ensure_ascii=False))
