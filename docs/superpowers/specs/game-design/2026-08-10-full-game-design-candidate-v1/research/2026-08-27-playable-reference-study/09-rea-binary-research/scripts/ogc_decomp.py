# -*- coding: utf-8 -*-
# Decompile a list of functions by entry address; save each to /tmp/ogs_decomp/.
# Usage: analyzeHeadless <dir> OGS-project114 -process SLPS_257.33 -noanalysis \
#        -scriptPath /tmp/ogs_scripts -postScript ogc_decomp.py 00373180 003d5b30 ...
import os
from ghidra.app.decompiler import DecompInterface

program = currentProgram
fm = program.getFunctionManager()
di = DecompInterface()
di.openProgram(program)

outdir = '/tmp/ogs_decomp'
if not os.path.exists(outdir):
    os.makedirs(outdir)

args = getScriptArgs()
if not args:
    args = ["00373180", "003d5b30", "003d2b80", "0013be70", "002ef100", "00176800"]

for a in args:
    addr = toAddr(a)
    f = fm.getFunctionAt(addr)
    if f is None:
        f = getFunctionContaining(addr)
    if f is None:
        print("SKIP %s: no function" % a)
        continue
    res = di.decompileFunction(f, 120, monitor)
    if not res.decompileCompleted():
        print("FAIL %s %s: %s" % (a, f.getName(), res.getErrorMessage()))
        continue
    code = res.getDecompiledFunction().getC()
    path = os.path.join(outdir, "%s_%s.c" % (a, f.getName()))
    fh = open(path, 'w')
    fh.write(code)
    fh.close()
    print("OK %s %s -> %s (%d lines)" % (a, f.getName(), path, code.count("\n")))
print("DECOMP BATCH DONE args=%s" % ",".join(args))
