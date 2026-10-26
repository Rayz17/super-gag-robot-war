# Ghidra headless 脚本(Jython):统计 + 反编译样证
# 用法: analyzeHeadless <dir> <proj> -process SLPS_257.33 -postScript ogc_stats.py
import sys

program = currentProgram
fm = program.getFunctionManager()
listing = program.getListing()

func_count = fm.getFunctionCount()
inst_count = 0
undef_count = 0
for instr in listing.getInstructions(True):
    inst_count += 1
    if instr.getMnemonicString() in ("???", "invalid"):
        undef_count += 1
print("STATS functions=%d instructions=%d undefined=%d (%.1f%% defined)" % (
    func_count, inst_count, undef_count, 100.0 * (inst_count - undef_count) / max(1, inst_count)))

# 找游戏调试串,反编译引用它的函数作为样证
target = None
for data in listing.getDefinedData(True):
    v = data.getValue()
    if v is not None and "invalid motion_type" in str(v):
        target = data.getAddress()
        break
if target is None:
    found = findBytes(None, "69 6e 76 61 6c 69 64 20 6d 6f 74 69 6f 6e")  # "invalid motion"
    if found:
        target = found
print("STRING motion_type at %s" % target)

if target is not None:
    refs = getReferencesTo(target)
    print("XREFS: %d" % len(refs))
    if refs:
        func = getFunctionContaining(refs[0].getFromAddress())
        if func:
            print("FUNCTION: %s @ %s" % (func.getName(), func.getEntryPoint()))
            di = DecompInterface()
            di.openProgram(program)
            res = di.decompileFunction(func, 120, monitor)
            if res.decompileCompleted():
                code = res.getDecompiledFunction().getC()
                lines = code.split("\n")
                print("DECOMPILE_OK lines=%d, 前 40 行:" % len(lines))
                for l in lines[:40]:
                    print(l)
            else:
                print("DECOMPILE_FAIL: %s" % res.getErrorMessage())
