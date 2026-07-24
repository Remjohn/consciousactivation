from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Known bundle locations (path relative to repo root, supports nested bundles)
KNOWN_BUNDLES = [
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_01_FOUNDATION_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_02_AIR_CORE_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_03_AHP_CORE_BUNDLE" / "CONSCIOUS_ACTIVATIONS_PHASE_03_AHP_CORE_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_01_03_TRACEABILITY_AND_GAP_CLOSURE_BUNDLE" / "CONSCIOUS_ACTIVATIONS_PHASE_01_03_TRACEABILITY_AND_GAP_CLOSURE_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_04_INTERVIEW_EXPRESSION_BUNDLE" / "CONSCIOUS_ACTIVATIONS_PHASE_04_INTERVIEW_EXPRESSION_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_05_SEMANTIC_PRODUCTION_COMPILER_BUNDLE" / "CONSCIOUS_ACTIVATIONS_PHASE_05_SEMANTIC_PRODUCTION_COMPILER_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_06_COMPOSITION_MEDIA_RUNTIMES_BUNDLE" / "CONSCIOUS_ACTIVATIONS_PHASE_06_COMPOSITION_MEDIA_RUNTIMES_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_07_STUDIO_SUPERVISION_BUNDLE" / "CONSCIOUS_ACTIVATIONS_PHASE_07_STUDIO_SUPERVISION_BUNDLE",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe relative path: {value}")
    return path


def verify_bundle(bundle_root: Path) -> dict:
    manifest_path = bundle_root / "PACKAGE_MANIFEST.json"
    if not manifest_path.exists():
        return {
            "bundle_root": str(bundle_root),
            "result": "SKIP",
            "reason": "PACKAGE_MANIFEST.json not found",
        }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    bundle_id = manifest.get("bundle_id", str(bundle_root.name))
    failures = []

    for entry in manifest["files"]:
        path = bundle_root / safe_relative(entry["path"])
        if not path.is_file():
            failures.append({"path": entry["path"], "error": "missing"})
            continue
        observed = sha256(path)
        if observed != entry["sha256"]:
            failures.append({"path": entry["path"], "error": "sha256 mismatch"})
        if path.stat().st_size != entry["bytes"]:
            failures.append({"path": entry["path"], "error": "byte count mismatch"})

    ops_path = bundle_root / "FILE_OPERATIONS.json"
    ops_count = 0
    if ops_path.exists():
        ops = json.loads(ops_path.read_text(encoding="utf-8"))
        ops_count = len(ops["operations"])
        for op in ops["operations"]:
            src = bundle_root / "full-replacement-files" / safe_relative(op["path"])
            if not src.is_file():
                failures.append({"path": op["path"], "error": "operation source missing"})
            elif sha256(src) != op["new_sha256"]:
                failures.append({"path": op["path"], "error": "operation hash mismatch"})

    return {
        "bundle_id": bundle_id,
        "bundle_root": str(bundle_root.relative_to(REPO_ROOT)),
        "file_count": len(manifest["files"]),
        "operation_count": ops_count,
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }


def main() -> int:
    results = []
    overall = "PASS"

    for bundle_path in KNOWN_BUNDLES:
        if not bundle_path.exists():
            results.append({
                "bundle_root": str(bundle_path.relative_to(REPO_ROOT)),
                "result": "SKIP",
                "reason": "bundle directory not found",
            })
            continue
        report = verify_bundle(bundle_path)
        results.append(report)
        if report["result"] == "FAIL":
            overall = "FAIL"

    summary = {
        "repo": str(REPO_ROOT),
        "overall_result": overall,
        "bundles": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
