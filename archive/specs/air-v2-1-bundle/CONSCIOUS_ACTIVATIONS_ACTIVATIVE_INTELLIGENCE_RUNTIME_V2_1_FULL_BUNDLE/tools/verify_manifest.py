from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
errors=[]
for row in manifest["files"]:
    p=ROOT/row["path"]
    if not p.is_file(): errors.append(f"missing {row['path']}"); continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h!=row["sha256"]: errors.append(f"hash mismatch {row['path']}")
    if p.stat().st_size!=row["bytes"]: errors.append(f"size mismatch {row['path']}")
if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)
print(f"PASS {len(manifest['files'])} files")
