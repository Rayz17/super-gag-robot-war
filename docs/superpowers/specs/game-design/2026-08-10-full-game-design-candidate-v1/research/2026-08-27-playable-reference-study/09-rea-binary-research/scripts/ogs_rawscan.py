# -*- coding: utf-8 -*-
# Raw machine-code scan for MIPS lui/addiu(ori/daddiu) string-address pairs,
# bypassing Ghidra disassembly gaps. Finds menu-string refs in "bad data" zones.
# Output: /tmp/ogs_raw_xref.txt
import time
import jarray

t0 = time.time()
program = currentProgram
fm = program.getFunctionManager()
mem = program.getMemory()

def sign16(v):
    return v - 0x10000 if v >= 0x8000 else v

# string candidates (same regex approach) in rodata 0x0052-0x0056
import re
run_re = re.compile(r'[\x20-\x7e]{6,}')
str_at = {}
for blk in mem.getBlocks():
    if not blk.isInitialized():
        continue
    bs = blk.getStart().getOffset()
    be = bs + blk.getSize()
    lo = max(bs, 0x520000)
    hi = min(be, 0x560000)
    if lo >= hi:
        continue
    buf = jarray.zeros(hi - lo, 'b')
    blk.getBytes(toAddr(lo), buf)
    s = "".join([chr(b & 0xff) for b in buf])
    for m in run_re.finditer(s):
        str_at["%08x" % (lo + m.start())] = m.group(0)
print("strings=%d (%.1fs)" % (len(str_at), time.time() - t0))

# raw scan of code words
OP_LUI = 0x0F << 26          # 0x3C000000
OP_ADDIU = 0x09 << 26        # 0x24000000
OP_DADDIU = 0x19 << 26       # 0x64000000
OP_ORI = 0x0D << 26          # 0x34000000

hits = {}     # string addr -> set of code addr strings
fcache = {}
def fn_of(caddr):
    if caddr not in fcache:
        f = getFunctionContaining(toAddr(caddr))
        fcache[caddr] = "%s@%s" % (f.getName(), f.getEntryPoint()) if f else "(no-func)"
    return fcache[caddr]

for blk in mem.getBlocks():
    if not blk.isInitialized():
        continue
    bs = blk.getStart().getOffset()
    be = bs + blk.getSize()
    lo = max(bs, 0x00100000)
    hi = min(be, 0x00500000)
    if lo >= hi:
        continue
    buf = jarray.zeros(hi - lo, 'b')
    blk.getBytes(toAddr(lo), buf)
    n = len(buf)
    words = []
    append = words.append
    for i in range(0, n - 3, 4):
        append(((buf[i+3] & 0xff) << 24) | ((buf[i+2] & 0xff) << 16) |
               ((buf[i+1] & 0xff) << 8) | (buf[i] & 0xff))
    nw = len(words)
    print("code words=%d (%.1fs)" % (nw, time.time() - t0))
    pending = []   # [hi_value, word_index]
    for iw in range(nw):
        w = words[iw]
        op = w & 0xFC000000
        if op == OP_LUI:
            hi = (w & 0xFFFF) << 16   # raw imm field, shifted like Ghidra displays
            if 0x520000 <= hi <= 0x5A0000:
                pending.append([hi, iw])
                if len(pending) > 64:
                    pending = pending[-64:]
        elif op in (OP_ADDIU, OP_DADDIU, OP_ORI):
            lo16 = w & 0xFFFF
            for (phi, piw) in reversed(pending):
                if iw - piw > 8:
                    break
                if op == OP_ORI:
                    full = phi | lo16
                else:
                    full = (phi + sign16(lo16)) & 0xFFFFFFFF
                key = "%08x" % full
                if key in str_at:
                    ca = lo + iw * 4
                    hits.setdefault(key, set()).add(
                        "%s@%s" % ("%08x" % ca, fn_of(ca)))
    pending = []

print("raw hits=%d (%.1fs)" % (len(hits), time.time() - t0))
out = open('/tmp/ogs_raw_xref.txt', 'w')
for key in sorted(hits.keys()):
    out.write("%s | %s | %s\n" % (key, str_at[key], ",".join(sorted(hits[key]))))
out.close()
print("DONE elapsed=%.1fs" % (time.time() - t0))
