# -*- coding: utf-8 -*-
# Force-disassemble instruction gaps in the text segment [0x100000, 0x500000).
# Skips gaps that are entirely zero padding or larger than 256KB.
# Usage: analyzeHeadless <dir> OGS-project114 -process SLPS_257.33 -noanalysis \
#        -postScript ogs_force_disasm.py
import time
import jarray
from ghidra.program.model.address import AddressSet

t0 = time.time()
program = currentProgram
listing = program.getListing()
mem = program.getMemory()

LO, HI = 0x00100000, 0x00500000
covered = AddressSet()
for cu in listing.getCodeUnits(True):
    a = cu.getAddress()
    if a.getOffset() < LO or a.getOffset() >= HI:
        continue
    covered.addRange(a, a.add(cu.getLength() - 1))
n_inst = 0
ii = listing.getInstructions(True)
while ii.hasNext():
    if ii.next().getAddress().getOffset() < HI:
        n_inst += 1
print("existing code units covered=%d instructions=%d (%.1fs)"
      % (covered.getNumAddresses(), n_inst, time.time() - t0))

# gaps = [LO,HI) minus covered
full = AddressSet(toAddr(LO), toAddr(HI - 1))
gaps = full.subtract(covered)

gap_ranges = []
it = gaps.getAddressRanges()
while it.hasNext():
    r = it.next()
    gap_ranges.append((r.getMinAddress().getOffset(), r.getMaxAddress().getOffset()))
print("gap count=%d total gap bytes=%d" % (len(gap_ranges), gaps.getNumAddresses()))

def all_zero(lo, hi):
    buf = jarray.zeros(hi - lo, 'b')
    mem.getBytes(toAddr(lo), buf)
    for b in buf:
        if (b & 0xff) != 0:
            return False
    return True

forced = 0
total_forced = 0
for (lo, hi) in gap_ranges:
    length = hi - lo + 1
    if length > 256 * 1024:
        print("SKIP big gap %08x-%08x (%dKB)" % (lo, hi, length // 1024))
        continue
    lo4 = (lo + 3) & ~3
    if lo4 + 4 > hi:
        continue
    try:
        if all_zero(lo4 & ~0xf, hi):
            continue
    except:
        pass
    try:
        clearListing(toAddr(lo4), toAddr(hi))
        disassemble(toAddr(lo4))
        forced += 1
        total_forced += length
    except Exception as e:
        print("ERR gap %08x: %s" % (lo, e))
print("forced disassembly on %d gaps, %d bytes (%.1fs)"
      % (forced, total_forced, time.time() - t0))
print("FORCE DISASM DONE")
