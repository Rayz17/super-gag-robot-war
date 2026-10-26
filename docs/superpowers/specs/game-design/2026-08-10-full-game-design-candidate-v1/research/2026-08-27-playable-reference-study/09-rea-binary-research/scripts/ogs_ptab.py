# -*- coding: utf-8 -*-
# Pointer-table + const-pair joint scan:
#  A) find 4-byte LE pointers into the string set in data segments
#  B) const-pair scan (aui/addiu) matching strings OR pointer-table entries
# Output: /tmp/ogs_ptrtab.txt, /tmp/ogs_joint_xref.txt
import re
import time
import jarray

t0 = time.time()
program = currentProgram
listing = program.getListing()
fm = program.getFunctionManager()
mem = program.getMemory()

def sign16(v):
    return v - 0x10000 if v >= 0x8000 else v

fcache = {}
def fn_cached(iaddr):
    k = iaddr.toString()
    if k not in fcache:
        f = getFunctionContaining(iaddr)
        fcache[k] = "%s@%s" % (f.getName(), f.getEntryPoint()) if f else "-"
    return fcache[k]

# ---- printable strings ----------------------------------------------------
run_re = re.compile(r'[\x20-\x7e]{6,}')
str_at = {}
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
        str_at["%08x" % (start_off + m.start())] = m.group(0)

# ---- A) pointer tables ----------------------------------------------------
# byte-wise scan (Itanium name strings are length-prefixed -> unaligned
# pointers); skip the code segment, scan data >= 0x00500000.
ptab = {}   # ptr loc "addr" -> string addr string
targets = set(str_at.keys())
for blk in mem.getBlocks():
    if not blk.isInitialized():
        continue
    size = blk.getSize()
    if size <= 0 or size > 64 * 1024 * 1024:
        continue
    bstart = blk.getStart().getOffset()
    bend = bstart + size
    lo = max(bstart, 0x500000)
    if lo >= bend:
        continue
    off0 = lo - bstart
    n = bend - lo
    buf = jarray.zeros(n, 'b')
    blk.getBytes(toAddr(lo), buf)
    for i in range(0, n - 3):
        v = (buf[i] & 0xff) | ((buf[i+1] & 0xff) << 8) | \
            ((buf[i+2] & 0xff) << 16) | ((buf[i+3] & 0xff) << 24)
        if v <= 0x100000 or v > 0x600000:
            continue
        key = "%08x" % v
        if key in str_at:
            loc = "%08x" % (lo + i)
            ptab[loc] = key
            targets.add(loc)
print("strings=%d ptr_entries=%d targets=%d (%.1fs)"
      % (len(str_at), len(ptab), len(targets), time.time() - t0))

ptr2str = {}
for loc, sa in ptab.items():
    ptr2str[loc] = sa

# ---- B) const-pair scan over targets --------------------------------------
def scalars_of(instr):
    out = []
    for i in range(instr.getNumOperands()):
        sc = instr.getScalar(i)
        if sc is not None:
            out.append(sc.getUnsignedValue())
    return out

HI = ("lui", "aui", "_aui", "_lui")
LO = ("ori", "addiu", "daddiu", "_ori", "_addiu", "_daddiu")
hits = {}
pending = []
seq = 0
for instr in listing.getInstructions(True):
    seq += 1
    m = instr.getMnemonicString()
    if m not in HI and m not in LO:
        continue
    scalars = scalars_of(instr)
    if not scalars:
        continue
    val = scalars[-1]
    if m in HI:
        if 0x00520000 <= val <= 0x005A0000:
            pending.append([val, seq])
            if len(pending) > 32:
                pending = pending[-32:]
    else:
        for (phi, pseq) in reversed(pending):
            if seq - pseq > 8:
                break
            if m in ("ori", "_ori"):
                full = phi | (val & 0xFFFF)
            else:
                # Ghidra sign-extends immediates to 64-bit: 0xFFFFFFA0 = -0x60
                sv = val if val < 0x80000000 else val - 0x100000000
                full = phi + sv
            key = "%08x" % (full & 0xFFFFFFFF)
            if key in targets:
                hits.setdefault(key, set()).add(fn_cached(instr.getAddress()))

print("joint hits=%d (%.1fs)" % (len(hits), time.time() - t0))

out = open('/tmp/ogs_joint_xref.txt', 'w')
for key in sorted(hits.keys()):
    label = str_at.get(key)
    if label is None:
        sa = ptr2str.get(key)
        label = "PTR->" + str_at.get(sa, sa) if sa else "(ptr)"
    out.write("%s | %s | %s\n" % (key, label, ",".join(sorted(hits[key]))))
out.close()

# pointer table catalog: which strings are pointed to, and where
out2 = open('/tmp/ogs_ptrtab.txt', 'w')
bys = {}
for loc, sa in ptab.items():
    bys.setdefault(sa, []).append(loc)
for sa in sorted(bys.keys()):
    out2.write("%s | %s | %s\n" % (sa, str_at[sa], ",".join(sorted(bys[sa]))))
out2.close()
print("DONE elapsed=%.1fs" % (time.time() - t0))
