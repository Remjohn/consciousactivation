from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def safe_relative(value: str) -> Path:
    path=Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe relative path: {value}")
    return path

def verify(bundle_root: Path) -> dict[str, object]:
    manifest=json.loads((bundle_root/"PACKAGE_MANIFEST.json").read_text(encoding="utf-8")); failures=[]
    for entry in manifest["files"]:
        path=bundle_root/safe_relative(entry["path"])
        if not path.is_file(): failures.append({"path":entry["path"],"error":"missing"}); continue
        observed=sha256(path)
        if observed!=entry["sha256"]: failures.append({"path":entry["path"],"error":"sha256 mismatch"})
        if path.stat().st_size!=entry["bytes"]: failures.append({"path":entry["path"],"error":"byte count mismatch"})
    operations=json.loads((bundle_root/"FILE_OPERATIONS.json").read_text(encoding="utf-8"))
    for operation in operations["operations"]:
        source=bundle_root/"full-replacement-files"/safe_relative(operation["path"])
        if not source.is_file(): failures.append({"path":operation["path"],"error":"operation source missing"})
        elif sha256(source)!=operation["new_sha256"]: failures.append({"path":operation["path"],"error":"operation hash mismatch"})
    return {"schema_version":"ca-phase07-bundle-verification/v1","bundle_id":manifest["bundle_id"],"file_count":len(manifest["files"]),"operation_count":len(operations["operations"]),"failures":failures,"result":"PASS" if not failures else "FAIL"}

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--bundle",type=Path,default=Path(__file__).resolve().parents[1]); args=parser.parse_args(); result=verify(args.bundle.resolve()); print(json.dumps(result,indent=2,sort_keys=True)); return 0 if result["result"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
