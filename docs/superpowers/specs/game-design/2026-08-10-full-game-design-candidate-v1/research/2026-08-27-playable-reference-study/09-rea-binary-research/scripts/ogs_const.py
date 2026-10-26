# -*- coding: utf-8 -*-
# MIPS lui/ori(addiu) constant-pair scan: map string addresses -> referencing
# functions, without relying on Ghidra reference analysis.
# Usage: analyzeHeadless <dir> OGS-project114 -process SLPS_257.33 -noanalysis \
#        -postScript ogs_const.py
import re
import time
import jarray

t0 = time.time()
program = currentProgram
listing = program.getListing()
mem = program.getMemory()
fm = program.getFunctionManager()

# ---- printable ASCII run scan (string candidate addresses) ---------------
run_re = re.compile(r'[\x20-\x7e]{6,}')
str_at = {}          # "0052xxxx" -> text
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
print("strings=%d (%.1fs)" % (len(str_at), time.time() - t0))

# ---- single pass: pair lui(page) with following ori/addiu(low) -----------
# ori form:   full = HI | LO          (zero-extended)
# addiu form: full = HI + signext(LO) (sign-extended %lo)
def sign16(v):
    return v - 0x10000 if v >= 0x8000 else v

fcache = {}
def fn_cached(iaddr):
    k = iaddr.toString()
    if k not in fcache:
        f = getFunctionContaining(iaddr)
        fcache[k] = "%s@%s" % (f.getName(), f.getEntryPoint()) if f else "-"
    return fcache[k]

def scalars_of(instr):
    out = []
    for i in range(instr.getNumOperands()):
        s = instr.getScalar(i)
        if s is not None:
            out.append(s.getUnsignedValue())
    return out

hits = {}            # string addr "0052xxxx" -> set of function labels
pending = []         # recent lui: [hi, seq]
seq = 0
for instr in listing.getInstructions(True):
    seq += 1
    m = instr.getMnemonicString()
    if m not in ("lui", "aui", "_aui", "_lui", "ori", "addiu", "daddiu",
                 "_ori", "_addiu", "_daddiu"):
        continue
    scalars = scalars_of(instr)
    if not scalars:
        continue
    val = scalars[-1]
    if m in ("lui", "aui", "_aui", "_lui"):
        if 0x00520000 <= val <= 0x00570000:
            pending.append([val, seq])
            if len(pending) > 32:
                pending = pending[-32:]
    else:
        for (phi, pseq) in reversed(pending):
            if seq - pseq > 8:
                break
            full = (phi | val) if m in ("ori", "_ori") else (phi + sign16(val))
            key = "%08x" % full
            if key in str_at:
                hits.setdefault(key, set()).add(fn_cached(instr.getAddress()))

print("const-pair hits=%d (%.1fs)" % (len(hits), time.time() - t0))

out = open('/tmp/ogs_const_xref.txt', 'w')
for key in sorted(hits.keys()):
    out.write("%s | %s | %s\n" % (key, str_at[key], ",".join(sorted(hits[key]))))
out.close()
print("DONE elapsed=%.1fs" % (time.time() - t0))
