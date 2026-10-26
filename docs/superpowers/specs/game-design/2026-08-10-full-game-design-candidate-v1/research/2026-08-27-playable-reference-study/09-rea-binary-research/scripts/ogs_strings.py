# -*- coding: utf-8 -*-
# OGS SLPS_257.33 string intelligence harvest (Ghidra 11.4.3 headless, Jython 2.7)
# Usage:
#   analyzeHeadless <dir> OGS-project114 -process SLPS_257.33 -noanalysis \
#       -postScript ogs_strings.py
# Output: /tmp/ogs_strings.txt  (address | text | xref-functions)
import re
import time
import jarray

t0 = time.time()
program = currentProgram
listing = program.getListing()
mem = program.getMemory()
fm = program.getFunctionManager()

# ---- 1) map: referenced-to-address -> list of from-addresses -------------
addr2refs = {}
ri = program.getReferenceManager().getReferenceIterator(program.getMinAddress())
nrefs = 0
while ri.hasNext():
    ref = ri.next()
    nrefs += 1
    key = ref.getToAddress().toString()
    if key not in addr2refs:
        addr2refs[key] = []
    addr2refs[key].append(ref.getFromAddress().toString())

# ---- 2) function cache ----------------------------------------------------
fcache = {}
def fn_of(from_str):
    if from_str in fcache:
        return fcache[from_str]
    f = getFunctionContaining(toAddr(from_str))
    r = "%s@%s" % (f.getName(), f.getEntryPoint()) if f else "-"
    fcache[from_str] = r
    return r

# ---- 3) raw scan of initialized memory for printable ASCII runs ----------
KEYWORDS = ["damage", "battle", "weapon", "pilot", "attack", "armor", "defen",
            "dodge", "avoid", "hit", "morale", "spirit", "seishin", "exp",
            "level", "money", "terrain", "motion", "action", "status",
            "state", "unit", "energy", "invalid", "range", "assert", "error",
            "cost", "power", "skill", "ability", "cutin", "effect", "anim"]
FMT = ("%d", "%s", "%x", "%X", "%u", "%f", "%02d")
run_re = re.compile(r'[\x20-\x7e]{6,}')

hits = {}
total_runs = 0
for blk in mem.getBlocks():
    if not blk.isInitialized():
        continue
    size = blk.getSize()
    if size <= 0 or size > 64 * 1024 * 1024:
        continue
    buf = jarray.zeros(size, 'b')
    blk.getBytes(blk.getStart(), buf)
    s = "".join([chr(b & 0xff) for b in buf])
    start_off = blk.getStart().getOffset()
    for m in run_re.finditer(s):
        total_runs += 1
        text = m.group(0)
        low = text.lower()
        is_fmt = any(f in text for f in FMT)
        is_kw = any(k in low for k in KEYWORDS)
        if not (is_fmt or is_kw):
            continue
        addr_str = "%08x" % (start_off + m.start())
        if addr_str in hits:
            continue
        hits[addr_str] = text

# ---- 4) resolve xref functions for hits, write catalog -------------------
out = open('/tmp/ogs_strings.txt', 'w')
out.write("# printable_runs=%d keyword_or_format_hits=%d refs_total=%d elapsed=%.1fs\n"
          % (total_runs, len(hits), nrefs, time.time() - t0))
kw_summary = {}
for addr_str in sorted(hits.keys()):
    text = hits[addr_str]
    refs = addr2refs.get(addr_str, [])
    fns = sorted(set([fn_of(r) for r in refs]))
    out.write("%s | %s | %s\n" % (addr_str, text, ",".join(fns) if fns else "-"))
    low = text.lower()
    for k in KEYWORDS:
        if k in low:
            kw_summary[k] = kw_summary.get(k, 0) + 1
            break
out.write("# keyword summary: %s\n" % repr(sorted(kw_summary.items())))
out.close()
print("HARVEST DONE hits=%d runs=%d refs=%d elapsed=%.1fs"
      % (len(hits), total_runs, nrefs, time.time() - t0))
