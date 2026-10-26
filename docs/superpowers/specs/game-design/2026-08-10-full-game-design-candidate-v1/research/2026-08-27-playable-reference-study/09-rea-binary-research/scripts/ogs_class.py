# -*- coding: utf-8 -*-
# 1) Enumerate game classes: all callers of the debug-name registrar
#    FUN_00150080(param, s_ClassName) -> class name + ctor address.
# 2) Dump the CMapBattleUnit vtable at 0x0057cda0.
# Usage: analyzeHeadless <dir> OGS-project114 -process SLPS_257.33 -noanalysis \
#        -postScript ogs_class.py
import re
import time
from ghidra.app.decompiler import DecompInterface

t0 = time.time()
program = currentProgram
listing = program.getListing()
fm = program.getFunctionManager()
mem = program.getMemory()

REGISTRAR = "00150080"

# ---- 1) find all callers of the registrar via jal flows ------------------
callers = []
target = toAddr(REGISTRAR)
ri = program.getReferenceManager().getReferencesTo(target)
for ref in ri:
    callers.append(ref.getFromAddress())
print("registrar refs=%d (%.1fs)" % (len(callers), time.time() - t0))

if len(callers) == 0:
    # fallback: scan jal flows
    for instr in listing.getInstructions(True):
        m = instr.getMnemonicString()
        if m in ("jal", "_jal", "bal"):
            for fl in instr.getFlows():
                if fl == target:
                    callers.append(instr.getAddress())

di = DecompInterface()
di.openProgram(program)

name_re = re.compile(r's_([A-Za-z_][A-Za-z0-9_:]*)_[0-9a-f]{8}')
catalog = {}
for ca in callers:
    f = getFunctionContaining(ca)
    if f is None:
        continue
    res = di.decompileFunction(f, 30, monitor)
    if not res.decompileCompleted():
        continue
    code = res.getDecompiledFunction().getC()
    ms = name_re.findall(code)
    if ms:
        catalog[f.getEntryPoint().toString()] = (f.getName(), sorted(set(ms)))
print("catalog=%d (%.1fs)" % (len(catalog), time.time() - t0))

out = open('/tmp/ogs_classes.txt', 'w')
for ep in sorted(catalog.keys()):
    name, cnames = catalog[ep]
    out.write("%s | %s | %s\n" % (ep, name, ",".join(cnames)))
out.close()

# ---- 2) dump vtable at 0x0057cda0 ----------------------------------------
def dump_vtable(vt, label, maxn=64):
    a = toAddr(vt)
    lines = []
    for i in range(maxn):
        try:
            val = mem.getLong(a.add(i * 8))
        except:
            break
        if val < 0x100000 or val > 0x600000:
            break
        fa = toAddr("%08x" % val)
        fn = fm.getFunctionAt(fa)
        lines.append("  [%02d] %08x %s" % (i, val, fn.getName() if fn else "?"))
    open('/tmp/ogs_vtable_%s.txt' % label, 'w').write(
        "vtable %s = %08x, %d entries\n%s\n" % (label, vt, len(lines),
                                                "\n".join(lines)))
    print("vtable %s entries=%d" % (label, len(lines)))

dump_vtable(0x0057cda0, "CMapBattleUnit")
dump_vtable(0x0057cda0 - 0x40, "CMapBattleUnit_m40")
print("DONE elapsed=%.1fs" % (time.time() - t0))
