from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe relative path: {value}")
    return path


def verify(bundle_root: Path) -> dict[str, object]:
    manifest_path = bundle_root / "PACKAGE_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    failures: list[dict[str, str]] = []
    for entry in manifest["files"]:
        relative = safe_relative(entry["path"])
        path = bundle_root / relative
        if not path.is_file():
            failures.append({"path": entry["path"], "error": "missing"})
            continue
        observed = sha256(path)
        if observed != entry["sha256"]:
            failures.append({"path": entry["path"], "error": f"sha256 {observed} != {entry['sha256']}"})
        if path.stat().st_size != entry["bytes"]:
            failures.append({"path": entry["path"], "error": "byte count mismatch"})

    operations = json.loads((bundle_root / "FILE_OPERATIONS.json").read_text(encoding="utf-8"))
    for operation in operations["operations"]:
        source = bundle_root / "full-replacement-files" / safe_relative(operation["path"])
        if not source.is_file():
            failures.append({"path": operation["path"], "error": "operation source missing"})
        elif sha256(source) != operation["new_sha256"]:
            failures.append({"path": operation["path"], "error": "operation new hash mismatch"})

    return {
        "schema_version": "ca-phase01-bundle-verification/v1",
        "bundle_id": manifest["bundle_id"],
        "file_count": len(manifest["files"]),
        "operation_count": len(operations["operations"]),
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = verify(args.bundle.resolve())
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
