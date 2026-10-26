# -*- coding: utf-8 -*-
# Clear + disassemble non-instruction zones between instructions in text.
# Zones >256KB or all-zero are skipped.
import time
import jarray

t0 = time.time()
program = currentProgram
listing = program.getListing()
mem = program.getMemory()

LO, HI = 0x00100000, 0x00500000
zones = []
prev_end = None
ii = listing.getInstructions(True)
while ii.hasNext():
    instr = ii.next()
    a = instr.getAddress().getOffset()
    if a >= HI:
        break
    e = instr.getAddress().add(instr.getLength()).getOffset()
    if prev_end is not None and a - prev_end > 8 and prev_end >= LO:
        zones.append((prev_end, a - 1))
    prev_end = e
print("zones=%d (%.1fs)" % (len(zones), time.time() - t0))

def all_zero(lo, hi):
    n = hi - lo + 1
    buf = jarray.zeros(n, 'b')
    mem.getBytes(toAddr(lo), buf)
    for b in buf:
        if (b & 0xff) != 0:
            return False
    return True

forced = 0
bytes_done = 0
sizes = []
for (lo, hi) in zones:
    length = hi - lo + 1
    if length > 256 * 1024:
        continue
    lo4 = (lo + 3) & ~3
    if lo4 + 4 > hi:
        continue
    try:
        if all_zero(lo4, hi):
            continue
    except:
        pass
    try:
        clearListing(toAddr(lo4), toAddr(hi))
        disassemble(toAddr(lo4))
        forced += 1
        bytes_done += length
        sizes.append(length)
    except Exception as e:
        print("ERR zone %08x: %s" % (lo, str(e)[:80]))
sizes.sort(reverse=True)
print("forced=%d bytes=%d biggest=%s (%.1fs)"
      % (forced, bytes_done, [hex(s) for s in sizes[:10]], time.time() - t0))
print("ZONE DISASM DONE")
