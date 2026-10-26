# -*- coding: utf-8 -*-
# Dump raw dwords around a vtable address, resolving code pointers.
# Usage: -postScript ogs_vtable.py 0057cda0
import time
t0 = time.time()
program = currentProgram
fm = program.getFunctionManager()
mem = program.getMemory()

args = getScriptArgs()
vts = args if args else ["0057cda0"]

for vs in vts:
    base = toAddr(vs)
    print("=== region around %s ===" % vs)
    lines = []
    start = base.add(-0x20)
    for i in range(0, 48):
        a = start.add(i * 4)
        try:
            v = mem.getInt(a) & 0xffffffff
        except:
            continue
        tag = ""
        if 0x00100008 <= v <= 0x00490000:
            fn = fm.getFunctionAt(toAddr("%08x" % v))
            tag = "-> %s" % (fn.getName() if fn else "code?")
        lines.append("%s: %08x %s" % (a.toString(), v, tag))
    out = open('/tmp/ogs_vtable_%s.txt' % vs, 'w')
    out.write("\n".join(lines) + "\n")
    out.close()
    print("\n".join(lines))
print("DONE elapsed=%.1fs" % (time.time() - t0))
