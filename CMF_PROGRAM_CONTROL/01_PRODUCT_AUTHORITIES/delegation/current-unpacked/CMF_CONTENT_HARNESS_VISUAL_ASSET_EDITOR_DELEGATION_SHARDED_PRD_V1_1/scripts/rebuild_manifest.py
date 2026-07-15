#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={"MANIFEST.json","LOCAL_VERIFICATION.json"}
def h(p):
    x=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):x.update(b)
    return x.hexdigest()
files=[]
for p in sorted(ROOT.rglob("*")):
    if not p.is_file():continue
    rel=p.relative_to(ROOT).as_posix()
    if rel in EXCLUDE or rel.startswith("validation/"):continue
    files.append({"path":rel,"bytes":p.stat().st_size,"sha256":h(p)})
manifest={"package":ROOT.name,"manifest_version":"1.0","files":files,"file_count":len(files)}
(ROOT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
print(len(files))
