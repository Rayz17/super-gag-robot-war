# C01 rejected 3D source quarantine

Status: `HISTORY_QUARANTINE / NON_EXECUTABLE / NEVER_ART_INPUT / NEVER_RUNTIME`

This directory preserves rejected C01 Blender and Three.js source bytes outside
the active `c01-current-demo-v1` production namespace. It is excluded from C01
production preflight by location, but location alone is not the safety boundary:

- source files use `.forbidden.txt` and model/cache binaries use
  `.forbidden.bin`, so they are not default executable/openable inputs;
- old commands, URLs and embedded render paths are retained only inside those
  inert evidence files and are intentionally not repaired into working entrypoints;
- nothing here may be executed, opened in Blender, served to a browser, used as
  ImageGen/art input, copied into Godot, or promoted to Runtime/Default/Canon;
- restoration requires an explicit producer decision and must first move the
  bytes out of quarantine under a newly approved production method.

`MIGRATION_MANIFEST.tsv` records the exact original production path, current
quarantine path and SHA-256 of every byte-preserved file. Failed PNGs, their
hashes and QA receipts remain at their original production paths.
