from __future__ import annotations

"""
Root-level apply_bundle.py for the Conscious Activations repository.
Auto-discovers the next unapplied phase bundle and delegates to its own
apply_bundle.py script, forwarding all CLI arguments.
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Ordered list of known bundles (path relative to repo root)
KNOWN_BUNDLES: list[Path] = [
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_01_FOUNDATION_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_02_AIR_CORE_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_03_AHP_CORE_BUNDLE"
    / "CONSCIOUS_ACTIVATIONS_PHASE_03_AHP_CORE_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_01_03_TRACEABILITY_AND_GAP_CLOSURE_BUNDLE"
    / "CONSCIOUS_ACTIVATIONS_PHASE_01_03_TRACEABILITY_AND_GAP_CLOSURE_BUNDLE",
    REPO_ROOT / "CONSCIOUS_ACTIVATIONS_PHASE_04_INTERVIEW_EXPRESSION_BUNDLE"
    / "CONSCIOUS_ACTIVATIONS_PHASE_04_INTERVIEW_EXPRESSION_BUNDLE",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bundle_is_applied(bundle_root: Path, repo: Path) -> bool:
    """Check if this bundle has already been applied (via receipt or file ops)."""
    manifest_path = bundle_root / "PACKAGE_MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        bundle_id = manifest.get("bundle_id")
        if bundle_id:
            receipt = repo / ".conscious-activations" / "bundle-state" / bundle_id / "apply_receipt.json"
            if receipt.exists():
                return True
    ops_path = bundle_root / "FILE_OPERATIONS.json"
    if not ops_path.exists():
        return False
    ops = json.loads(ops_path.read_text(encoding="utf-8"))
    for op in ops["operations"]:
        target = repo / op["path"]
        if not target.exists():
            return False
        if sha256_file(target) != op["new_sha256"]:
            return False
    return True


def find_bundle_apply_script(bundle_root: Path) -> Path | None:
    candidate = bundle_root / "scripts" / "apply_bundle.py"
    return candidate if candidate.exists() else None


def main() -> int:
    # Parse only our own args; remaining args are forwarded to the bundle script
    parser = argparse.ArgumentParser(
        description="Auto-discover and apply the next unapplied phase bundle."
    )
    parser.add_argument("--repo", type=Path, required=True, help="Path to the repo root")
    parser.add_argument(
        "--bundle",
        type=Path,
        default=None,
        help="Explicit bundle root to apply (skips auto-discovery)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--keep-failed", action="store_true")
    parser.add_argument("--create-branch", default=None)
    parser.add_argument("--commit", action="store_true")

    args = parser.parse_args()
    repo = args.repo.resolve()

    if not (repo / "CMF_PROGRAM_CONTROL").is_dir():
        print(
            json.dumps(
                {"result": "ERROR", "reason": f"not a Conscious Activations repository: {repo}"},
                indent=2,
            )
        )
        return 2

    # Determine which bundle to apply
    if args.bundle:
        bundle_candidates = [args.bundle.resolve()]
    else:
        bundle_candidates = KNOWN_BUNDLES

    chosen_bundle: Path | None = None
    for bundle_path in bundle_candidates:
        if not bundle_path.exists():
            print(f"[skip] bundle not found: {bundle_path.relative_to(REPO_ROOT)}")
            continue
        if bundle_is_applied(bundle_path, repo):
            manifest = json.loads((bundle_path / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
            print(f"[already applied] {manifest.get('bundle_id', bundle_path.name)}")
            continue
        chosen_bundle = bundle_path
        break

    if chosen_bundle is None:
        print(
            json.dumps(
                {
                    "result": "UP_TO_DATE",
                    "reason": "All known bundles are already applied.",
                },
                indent=2,
            )
        )
        return 0

    apply_script = find_bundle_apply_script(chosen_bundle)
    if apply_script is None:
        print(
            json.dumps(
                {
                    "result": "ERROR",
                    "reason": f"No apply_bundle.py found in {chosen_bundle}",
                },
                indent=2,
            )
        )
        return 2

    manifest = json.loads((chosen_bundle / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    print(f"[applying] {manifest.get('bundle_id', chosen_bundle.name)}")
    print(f"[script]   {apply_script}")
    print()

    # Build forwarded arguments
    fwd: list[str] = ["--repo", str(repo), "--bundle", str(chosen_bundle)]
    if args.dry_run:
        fwd.append("--dry-run")
    if args.allow_dirty:
        fwd.append("--allow-dirty")
    if args.skip_tests:
        fwd.append("--skip-tests")
    if args.keep_failed:
        fwd.append("--keep-failed")
    if args.create_branch:
        fwd += ["--create-branch", args.create_branch]
    if args.commit:
        fwd.append("--commit")

    result = subprocess.run(
        [sys.executable, str(apply_script)] + fwd,
        cwd=str(chosen_bundle / "scripts"),
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
