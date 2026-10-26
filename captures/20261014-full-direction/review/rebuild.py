#!/usr/bin/env python3
"""Regenerate review/index.html from ../_meta/inventory.json + ../incoming/dir-*.jpg."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INV_PATH = ROOT / "_meta" / "inventory.json"
INCOMING = ROOT / "incoming"
OUT = HERE / "index.html"

GROUP_ORDER = list("MHEFBSXGCUITN")
GROUP_LABELS = {
    "M": "机体 Mecha",
    "H": "人物 Human",
    "E": "敌体 Enemy",
    "F": "部件 Feature",
    "B": "建筑 Building",
    "S": "场景 Scene",
    "X": "特效 FX",
    "G": "图形 Graphic",
    "C": "合体 Combo",
    "U": "UI",
    "I": "信息 Info",
    "T": "地形 Terrain",
    "N": "叙事 Narrative",
}

ASSET_RE = re.compile(r"^dir-([A-Z]\d+[A-Za-z0-9]*)-", re.I)


def is_done(status: str) -> bool:
    s = (status or "").lower()
    if not s or s == "todo":
        return False
    return True


def scan_incoming() -> dict[str, str]:
    """Map item id -> relative path ../incoming/filename (newest/longest name wins)."""
    found: dict[str, str] = {}
    if not INCOMING.is_dir():
        return found
    for p in sorted(INCOMING.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        m = ASSET_RE.match(p.name)
        if not m:
            continue
        item_id = m.group(1).upper()
        # Prefer locked / higher version names lexicographically last among same id
        rel = f"../incoming/{p.name}"
        if item_id not in found or p.name > Path(found[item_id]).name:
            found[item_id] = rel
    return found


def esc(s: str) -> str:
    return (
        (s or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def badge_class(status: str) -> str:
    s = (status or "todo").lower()
    if s == "todo":
        return "todo"
    if "locked" in s:
        return "locked"
    if "pass" in s or "done" in s or "draft" in s:
        return "done"
    return "done"


def build_html(inv: dict, assets: dict[str, str]) -> str:
    items = inv.get("items") or []
    by_group: dict[str, list] = defaultdict(list)
    for it in items:
        g = it.get("group") or "?"
        by_group[g].append(it)

    # Counts: done = has asset OR non-todo status
    total = len(items)
    done_n = 0
    todo_n = 0
    group_stats = {}
    for g in GROUP_ORDER:
        glist = by_group.get(g, [])
        g_done = 0
        g_todo = 0
        for it in glist:
            has = it["id"] in assets
            if is_done(it.get("status", "")) or has:
                g_done += 1
            else:
                g_todo += 1
        group_stats[g] = (len(glist), g_done, g_todo)
        done_n += g_done
        todo_n += g_todo

    rev = esc(inv.get("revision", ""))
    style = esc(inv.get("style", "KINETIC_CEL"))
    now = datetime.now().strftime("%Y-%m-%d %H:%M CST")

    # Filter tabs
    tabs = ['<button type="button" class="tab active" data-group="ALL">ALL '
            f'<span class="n">{done_n}/{total}</span></button>']
    for g in GROUP_ORDER:
        n, gd, gt = group_stats[g]
        if n == 0:
            continue
        tabs.append(
            f'<button type="button" class="tab" data-group="{g}" '
            f'title="{esc(GROUP_LABELS.get(g, g))}">{g} '
            f'<span class="n">{gd}/{n}</span></button>'
        )

    sections = []
    for g in GROUP_ORDER:
        glist = by_group.get(g, [])
        if not glist:
            continue
        n, gd, gt = group_stats[g]
        label = GROUP_LABELS.get(g, g)
        cards = []
        for it in glist:
            iid = it["id"]
            status = it.get("status") or "todo"
            has = iid in assets
            bc = badge_class(status)
            if has and bc == "todo":
                bc = "done"
            purpose = esc(it.get("purpose") or "")
            design = esc(it.get("design") or "")
            name = esc(it.get("name") or "")
            tmpl = esc(it.get("template") or "")
            states = it.get("states") or []
            states_html = ""
            if states:
                states_html = (
                    '<div class="states">'
                    + "".join(f'<span class="st">{esc(str(s))}</span>' for s in states)
                    + "</div>"
                )
            thumb = ""
            if has:
                src = esc(assets[iid])
                thumb = (
                    f'<a class="thumb" href="{src}" target="_blank" rel="noopener">'
                    f'<img src="{src}" alt="{iid}" loading="lazy"></a>'
                )
            else:
                thumb = '<div class="thumb empty">no asset</div>'
            cards.append(
                f'<article class="card" data-group="{g}" data-id="{esc(iid)}" '
                f'data-status="{esc(status)}" id="{esc(iid)}">'
                f"{thumb}"
                f'<div class="meta">'
                f'<div class="row1"><span class="id">{esc(iid)}</span>'
                f'<span class="badge {bc}">{esc(status)}</span></div>'
                f'<h3 class="name">{name}</h3>'
                f'<div class="tmpl">{tmpl}</div>'
                f'<p class="purpose"><strong>目的</strong> {purpose}</p>'
                f'<p class="design"><strong>设计</strong> {design}</p>'
                f"{states_html}"
                f"</div></article>"
            )
        sections.append(
            f'<section class="group" data-group="{g}" id="group-{g}">'
            f'<header class="ghead"><h2>{g} · {esc(label)}</h2>'
            f'<span class="gcount">done {gd} / todo {gt} / total {n}</span></header>'
            f'<div class="grid">{"".join(cards)}</div></section>'
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>超Gag 方向总审 · {rev}</title>
<style>
:root {{
  --ink:#1a2a32; --muted:#5a6e76; --paper:#f3f1ea; --panel:#fffef9;
  --line:#cfd9d4; --teal:#176b73; --amber:#a96120; --red:#c44b3a;
  --ok:#2a7a4b; --todo:#8a6a20; --locked:#176b73;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC",
    "Segoe UI",sans-serif; line-height:1.55; font-size:14px;
}}
a {{ color:var(--teal); }}
.banner {{
  background:linear-gradient(90deg,#123a40,#176b73 55%,#2a5560);
  color:#f4f8f6; padding:14px 20px; border-bottom:4px solid #c44b3a;
}}
.banner .lock {{
  font-size:12px; letter-spacing:.08em; text-transform:uppercase; opacity:.85;
}}
.banner h1 {{ margin:4px 0 2px; font-size:20px; font-weight:750; }}
.banner .cite {{
  font-size:13px; opacity:.95; max-width:1100px;
}}
.banner code {{
  background:rgba(0,0,0,.25); padding:1px 6px; border-radius:4px; font-size:12px;
}}
.toolbar {{
  position:sticky; top:0; z-index:5; background:rgba(243,241,234,.96);
  backdrop-filter:blur(6px); border-bottom:1px solid var(--line);
  padding:10px 16px; display:flex; flex-wrap:wrap; gap:8px; align-items:center;
}}
.summary {{
  font-size:13px; color:var(--muted); margin-right:8px; white-space:nowrap;
}}
.summary strong {{ color:var(--ok); }}
.summary .todo {{ color:var(--todo); font-weight:700; }}
.tabs {{ display:flex; flex-wrap:wrap; gap:6px; }}
.tab {{
  font:inherit; cursor:pointer; border:1px solid var(--line); background:var(--panel);
  border-radius:999px; padding:5px 11px; color:var(--ink);
}}
.tab .n {{ font-size:11px; color:var(--muted); margin-left:4px; }}
.tab.active, .tab:hover {{ border-color:var(--teal); background:#e4efeb; }}
.tab.active {{ background:var(--teal); color:#fff; }}
.tab.active .n {{ color:#d7ece8; }}
main {{ max-width:1400px; margin:0 auto; padding:18px 16px 60px; }}
.group {{ margin-bottom:28px; }}
.group[hidden], .card[hidden] {{ display:none !important; }}
.ghead {{
  display:flex; flex-wrap:wrap; align-items:baseline; gap:12px;
  border-bottom:2px solid var(--line); padding-bottom:6px; margin-bottom:12px;
}}
.ghead h2 {{ margin:0; font-size:18px; color:var(--teal); }}
.gcount {{ font-size:12px; color:var(--muted); }}
.grid {{
  display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:12px;
}}
.card {{
  background:var(--panel); border:1px solid var(--line); border-radius:10px;
  overflow:hidden; display:flex; flex-direction:column; min-height:100%;
}}
.thumb {{
  display:block; background:#e8ece6; aspect-ratio:16/9; overflow:hidden;
  border-bottom:1px solid var(--line);
}}
.thumb img {{
  width:100%; height:100%; object-fit:cover; display:block;
}}
.thumb.empty {{
  display:flex; align-items:center; justify-content:center;
  color:var(--muted); font-size:12px; letter-spacing:.04em;
}}
.meta {{ padding:10px 12px 12px; display:flex; flex-direction:column; gap:4px; flex:1; }}
.row1 {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; }}
.id {{
  font-family:ui-monospace,Menlo,monospace; font-weight:700; font-size:13px;
  background:#e4efeb; padding:2px 7px; border-radius:4px; color:var(--teal);
}}
.badge {{
  font-size:11px; padding:2px 7px; border-radius:4px; font-weight:650;
  max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}}
.badge.todo {{ background:#f3e6c4; color:#6a4e10; }}
.badge.done {{ background:#d5ebd9; color:#1e5a32; }}
.badge.locked {{ background:#d0e7ea; color:#0f4c54; }}
.name {{ margin:2px 0 0; font-size:15px; line-height:1.35; }}
.tmpl {{ font-size:11px; color:var(--muted); letter-spacing:.03em; }}
.purpose, .design {{ margin:4px 0 0; font-size:12.5px; color:#2c3c42; }}
.purpose strong, .design strong {{ color:var(--muted); font-weight:650; }}
.design {{
  display:-webkit-box; -webkit-line-clamp:4; -webkit-box-orient:vertical;
  overflow:hidden;
}}
.states {{ display:flex; flex-wrap:wrap; gap:4px; margin-top:6px; }}
.st {{
  font-size:10px; padding:1px 6px; border-radius:3px; background:#eef1ea;
  color:var(--muted); border:1px solid var(--line);
}}
.foot {{
  max-width:1400px; margin:0 auto; padding:0 16px 40px;
  font-size:12px; color:var(--muted);
}}
@media (max-width:600px) {{
  .grid {{ grid-template-columns:1fr; }}
  .banner h1 {{ font-size:17px; }}
}}
</style>
</head>
<body>
<header class="banner">
  <div class="lock">STYLE LOCK · Astra KINETIC_CEL</div>
  <h1>超Gag 全方向总审 · {rev}</h1>
  <p class="cite">风格锁引用：<strong>Astra KINETIC_CEL</strong> ／
    唯一入口 <code>给Astra的视觉总参考</code> ／
    Working Canon = <strong>KINETIC_CEL</strong> ／
    本页 inventory 标注：{style}</p>
  <p class="cite">硬边色块、压力墨线、最多两级硬阴影；禁止 photoreal／PBR／ITB 灰板。
    重建脚本 <code>review/rebuild.py</code> · 生成于 {now}</p>
</header>

<div class="toolbar">
  <div class="summary">合计 <strong>{done_n}</strong> done ·
    <span class="todo">{todo_n} todo</span> · {total} items ·
    assets {len(assets)}</div>
  <div class="tabs" role="tablist" aria-label="分组筛选">
    {"".join(tabs)}
  </div>
</div>

<main>
{"".join(sections)}
</main>

<p class="foot">Offline file:// OK · thumbnails use relative <code>../incoming/…</code> ·
  loading=lazy · regenerate: <code>python3 review/rebuild.py</code></p>

<script>
(function () {{
  var tabs = document.querySelectorAll(".tab");
  var groups = document.querySelectorAll(".group");
  function apply(g) {{
    tabs.forEach(function (t) {{
      t.classList.toggle("active", t.getAttribute("data-group") === g);
    }});
    groups.forEach(function (sec) {{
      var sg = sec.getAttribute("data-group");
      var show = (g === "ALL" || sg === g);
      sec.hidden = !show;
    }});
    if (g !== "ALL") {{
      var el = document.getElementById("group-" + g);
      if (el) el.scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}
  }}
  tabs.forEach(function (t) {{
    t.addEventListener("click", function () {{
      apply(t.getAttribute("data-group"));
    }});
  }});
  // deep link #M05 or #group-X
  if (location.hash) {{
    var h = location.hash.slice(1);
    if (h.indexOf("group-") === 0) apply(h.slice(6));
    else {{
      var card = document.getElementById(h);
      if (card) {{
        apply(card.getAttribute("data-group"));
        setTimeout(function () {{ card.scrollIntoView({{ behavior: "smooth", block: "center" }}); }}, 50);
      }}
    }}
  }}
}})();
</script>
</body>
</html>
"""


def main() -> None:
    inv = json.loads(INV_PATH.read_text(encoding="utf-8"))
    assets = scan_incoming()
    html = build_html(inv, assets)
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Items: {len(inv.get('items') or [])}")
    print(f"Assets: {len(assets)}")
    for iid, rel in sorted(assets.items()):
        print(f"  {iid} -> {rel}")


if __name__ == "__main__":
    main()
