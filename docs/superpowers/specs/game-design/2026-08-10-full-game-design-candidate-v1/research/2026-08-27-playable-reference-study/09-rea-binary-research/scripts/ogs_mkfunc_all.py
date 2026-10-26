# -*- coding: utf-8 -*-
# Final function recovery:
#  A) per-word disassembly in target windows (0 words = nop, included)
#  B) raw jal-target scan across text; create a function at every target
#  C) decompile the functions containing anchor sites
import os
import time
import jarray
from ghidra.app.decompiler import DecompInterface

t0 = time.time()
program = currentProgram
listing = program.getListing()
mem = program.getMemory()
fm = program.getFunctionManager()

WINDOWS = [
    (0x00107000, 0x0010b000),
    (0x0018f000, 0x00194000),
    (0x00231000, 0x00232400),
    (0x0035e000, 0x003e5000),
]
SITES = ["00107d58", "00108614", "0010ad88", "001900a8", "001901f0",
         "001902d4", "00190504", "00192bac", "00192bdc",
         "00231c70", "00231e60", "00231ea0", "00231f90",
         "0035f1c4", "0035f5e4", "0036d7dc", "0036e620",
         "00371dac", "0037280c", "00372bdc", "00379984", "003e46f8"]
STUBS = ["00107ae8", "0010ad0c", "0018ff94", "00192ae0", "00231854",
         "0035f1a0", "0035f5c0", "0036d7d8", "0036e61c", "00371da8",
         "00372808", "00372bd8", "00379948", "003e46f4"]

def read_word(a):
    buf = jarray.zeros(4, 'b')
    mem.getBytes(a, buf)
    return ((buf[3] & 0xff) << 24) | ((buf[2] & 0xff) << 16) | \
           ((buf[1] & 0xff) << 8) | (buf[0] & 0xff)

# ---- pass 0: drop stub functions from previous pass ----------------------
removed = 0
for s in STUBS:
    f = fm.getFunctionAt(toAddr(s))
    if f is not None:
        fm.removeFunction(f.getEntryPoint())
        removed += 1
print("stub removed=%d (%.1fs)" % (removed, time.time() - t0))

# ---- pass A: per-word disassembly (0 words = nop, disassemble too) -------
fixed = 0
bad = 0
for (lo, hi) in WINDOWS:
    a = toAddr(lo)
    while a.getOffset() < hi:
        if getInstructionAt(a) is None:
            try:
                clearListing(a, a.add(3))
                disassemble(a)
                if getInstructionAt(a) is not None:
                    fixed += 1
                else:
                    bad += 1
            except:
                bad += 1
        a = a.add(4)
print("passA fixed=%d bad=%d (%.1fs)" % (fixed, bad, time.time() - t0))

# ---- pass B: jal-target function creation --------------------------------
# raw scan all text words for jal (opcode 0x03)
jal_targets = set()
for blk in mem.getBlocks():
    if not blk.isInitialized():
        continue
    bs = blk.getStart().getOffset()
    be = bs + blk.getSize()
    lo = max(bs, 0x00100000)
    hi = min(be, 0x00500000)
    if lo >= hi:
        continue
    n = hi - lo
    buf = jarray.zeros(n, 'b')
    blk.getBytes(toAddr(lo), buf)
    for i in range(0, n - 3, 4):
        w = (buf[i+3] & 0xff) << 24 | (buf[i+2] & 0xff) << 16 | \
            (buf[i+1] & 0xff) << 8 | (buf[i] & 0xff)
        if (w >> 26) == 0x03:                       # jal
            t = (w & 0x3FFFFFF) << 2
            if 0x00100000 <= t < 0x00500000:
                jal_targets.add(t)
print("jal targets=%d (%.1fs)" % (len(jal_targets), time.time() - t0))

created = 0
failed = 0
for t in sorted(jal_targets):
    ta = toAddr("%08x" % t)
    if fm.getFunctionAt(ta) is not None:
        continue
    if getInstructionAt(ta) is None:
        try:
            w = read_word(ta)
            if 0x20202020 <= w <= 0x7E7E7E7E:       # looks like ASCII data
                failed += 1
                continue
            clearListing(ta, ta.add(3))
            disassemble(ta)
        except:
            failed += 1
            continue
    f = createFunction(ta, None)
    if f is not None:
        created += 1
    else:
        failed += 1
print("passB created=%d failed=%d (%.1fs)" % (created, failed, time.time() - t0))

# ---- pass C: decompile anchor-containing functions -----------------------
di = DecompInterface()
di.openProgram(program)
outdir = '/tmp/ogs_decomp'
done = {}
for sa in SITES:
    site = toAddr(sa)
    f = getFunctionContaining(site)
    if f is None:
        print("SITE %s: STILL NO FUNC" % sa)
        continue
    ep = f.getEntryPoint().toString()
    if ep in done:
        print("SITE %s -> %s (already)" % (sa, ep))
        continue
    res = di.decompileFunction(f, 180, monitor)
    if res.decompileCompleted():
        code = res.getDecompiledFunction().getC()
        path = os.path.join(outdir, "%s_%s.c" % (ep, f.getName()))
        fh = open(path, 'w')
        fh.write(code)
        fh.close()
        done[ep] = code.count("\n")
        print("SITE %s -> %s DECOMP lines=%d" % (sa, ep, done[ep]))
    else:
        print("SITE %s -> %s DECOMP-FAIL %s" % (sa, ep, str(res.getErrorMessage())[:60]))
print("ALL DONE funcs=%d (%.1fs)" % (len(done), time.time() - t0))
