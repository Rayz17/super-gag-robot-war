#!/usr/bin/env python3
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
inv_p=root/'_meta/inventory.json'
inv=json.loads(inv_p.read_text())
by={it['id']:it for it in inv['items']}
for p in sorted((root/'incoming').glob('dir-*.jpg')):
  m=re.match(r'dir-([A-Z]\d{2})-', p.name)
  if not m: continue
  i=m.group(1)
  if i in by and by[i].get('status')=='todo':
    by[i]['status']='draft-v1'; by[i]['file']=p.name
  elif i in by and by[i].get('file')!=p.name and 'locked' not in str(by[i].get('status')):
    by[i]['file']=p.name
    if by[i]['status']=='todo': by[i]['status']='draft-v1'
inv_p.write_text(json.dumps(inv,ensure_ascii=False,indent=2),encoding='utf-8')
done=sum(1 for it in inv['items'] if it['status']!='todo')
print(f'done={done} todo={len(inv["items"])-done}')
