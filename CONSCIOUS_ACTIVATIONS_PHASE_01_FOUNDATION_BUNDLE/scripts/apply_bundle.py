from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from verify_bundle import safe_relative, sha256, verify


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=check,
    )


def is_git_repo(repo: Path) -> bool:
    return (repo / ".git").exists() and shutil.which("git") is not None


def rollback_from_receipt(repo: Path, receipt: dict[str, object], *, force: bool = False) -> None:
    for record in reversed(receipt["files"]):
        target = repo / safe_relative(record["path"])
        new_sha = record["new_sha256"]
        if target.exists() and not force and sha256(target) != new_sha:
            raise RuntimeError(f"refusing rollback; applied file drifted: {record['path']}")
        if record["operation"] == "create":
            if target.exists():
                target.unlink()
        else:
            backup = Path(record["backup_path"])
            if not backup.is_file():
                raise RuntimeError(f"missing backup: {backup}")
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(backup, target)

    created_directories = [repo / safe_relative(value) for value in receipt.get("created_directories", [])]
    transient_names = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    for directory in sorted(created_directories, key=lambda item: len(item.parts), reverse=True):
        if not directory.exists():
            continue
        for child in sorted(directory.rglob("*"), key=lambda item: len(item.parts), reverse=True):
            if child.is_file() and child.suffix in {".pyc", ".pyo"}:
                child.unlink()
            elif child.is_dir() and child.name in transient_names:
                shutil.rmtree(child, ignore_errors=True)
        try:
            directory.rmdir()
        except OSError:
            if force:
                shutil.rmtree(directory)
            else:
                raise RuntimeError(f"refusing to remove non-empty created directory: {directory}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--keep-failed", action="store_true")
    parser.add_argument("--create-branch")
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    repo = args.repo.resolve()
    bundle = args.bundle.resolve()
    if not (repo / "CMF_PROGRAM_CONTROL").is_dir():
        raise SystemExit(f"not a Conscious Activations repository: {repo}")

    bundle_report = verify(bundle)
    if bundle_report["result"] != "PASS":
        print(json.dumps(bundle_report, indent=2, sort_keys=True))
        raise SystemExit("bundle verification failed")

    baseline = json.loads((bundle / "BASELINE_LOCK.json").read_text(encoding="utf-8"))
    operations = json.loads((bundle / "FILE_OPERATIONS.json").read_text(encoding="utf-8"))
    manifest = json.loads((bundle / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    bundle_id = manifest["bundle_id"]

    git_repo = is_git_repo(repo)
    if git_repo:
        status = git(repo, "status", "--porcelain").stdout.strip()
        if status and not args.allow_dirty:
            raise SystemExit("git worktree is dirty; commit/stash changes or pass --allow-dirty")
        if args.create_branch:
            existing = git(repo, "branch", "--list", args.create_branch).stdout.strip()
            if existing:
                raise SystemExit(f"branch already exists: {args.create_branch}")

    failures: list[str] = []
    actions: list[dict[str, object]] = []
    for required in baseline["required_existing_files"]:
        target = repo / safe_relative(required["path"])
        if not target.is_file():
            failures.append(f"required baseline file missing: {required['path']}")
        elif sha256(target) != required["sha256"]:
            failures.append(f"required baseline hash mismatch: {required['path']}")

    for op in operations["operations"]:
        target = repo / safe_relative(op["path"])
        if target.exists():
            observed = sha256(target)
            if observed == op["new_sha256"]:
                actions.append({**op, "action": "already_applied"})
                continue
            if op["operation"] == "create":
                failures.append(f"create target already exists with different bytes: {op['path']}")
                continue
            if observed != op["old_sha256"]:
                failures.append(f"replace target hash mismatch: {op['path']}")
                continue
            actions.append({**op, "action": "replace"})
        else:
            if op["operation"] == "replace":
                failures.append(f"replace target missing: {op['path']}")
                continue
            actions.append({**op, "action": "create"})

    plan = {
        "schema_version": "ca-phase01-apply-plan/v1",
        "bundle_id": bundle_id,
        "repo": str(repo),
        "actions": actions,
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
    }
    print(json.dumps(plan, indent=2, sort_keys=True))
    if failures:
        return 2
    if args.dry_run:
        return 0

    if git_repo and args.create_branch:
        git(repo, "checkout", "-b", args.create_branch)

    state_root = repo / ".conscious-activations" / "bundle-state" / bundle_id
    backup_root = state_root / "backups"
    staging_root = repo / ".conscious-activations" / "apply-staging" / bundle_id
    if state_root.exists():
        raise SystemExit(f"bundle state already exists: {state_root}")
    backup_root.mkdir(parents=True, exist_ok=True)
    staging_root.mkdir(parents=True, exist_ok=True)

    applied: list[dict[str, object]] = []
    created_directories: set[Path] = set()
    for action in actions:
        if action["action"] == "already_applied":
            continue
        cursor = (repo / safe_relative(action["path"])).parent
        while cursor != repo and not cursor.exists():
            created_directories.add(cursor)
            cursor = cursor.parent

    try:
        for action in actions:
            if action["action"] == "already_applied":
                continue
            rel = safe_relative(action["path"])
            source = bundle / "full-replacement-files" / rel
            staged = staging_root / rel
            staged.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, staged)
            if sha256(staged) != action["new_sha256"]:
                raise RuntimeError(f"staged hash mismatch: {action['path']}")

        for action in actions:
            if action["action"] == "already_applied":
                continue
            rel = safe_relative(action["path"])
            target = repo / rel
            backup_path = None
            if action["action"] == "replace":
                backup_path = backup_root / rel
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staging_root / rel, target)
            applied.append(
                {
                    "path": action["path"],
                    "operation": action["action"],
                    "old_sha256": action.get("old_sha256"),
                    "new_sha256": action["new_sha256"],
                    "backup_path": str(backup_path) if backup_path else None,
                }
            )

        receipt = {
            "schema_version": "ca-phase01-apply-receipt/v1",
            "bundle_id": bundle_id,
            "applied_at_utc": utc_now(),
            "repo": str(repo),
            "files": applied,
            "created_directories": [
                str(path.relative_to(repo)).replace("\\\\", "/")
                for path in sorted(created_directories, key=lambda item: (len(item.parts), str(item)))
            ],
            "tests": "not_run" if args.skip_tests else "pending",
            "result": "APPLIED_PENDING_TESTS" if not args.skip_tests else "APPLIED_TESTS_SKIPPED",
        }
        state_root.mkdir(parents=True, exist_ok=True)
        receipt_path = state_root / "apply_receipt.json"
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        if not args.skip_tests:
            report_path = state_root / "validation_report.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(repo / "scripts" / "phase1" / "validate_phase1.py"),
                    "--report",
                    str(report_path),
                ],
                cwd=repo,
                text=True,
            )
            if completed.returncode != 0:
                receipt["tests"] = "FAIL"
                receipt["result"] = "APPLY_FAILED_VALIDATION"
                receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                if not args.keep_failed:
                    rollback_from_receipt(repo, receipt, force=True)
                    receipt["result"] = "ROLLED_BACK_AFTER_VALIDATION_FAILURE"
                    receipt_path.parent.mkdir(parents=True, exist_ok=True)
                    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                return 3
            receipt["tests"] = "PASS"
            receipt["result"] = "APPLIED_VALIDATED"
            receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        shutil.rmtree(staging_root, ignore_errors=True)

        if args.commit:
            if not is_git_repo(repo):
                raise RuntimeError("--commit requires a git repository")
            git(repo, "add", "--all")
            git(repo, "commit", "-m", "implement Phase 1 application foundation and shared contracts")

        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 0
    except Exception:
        if applied and not args.keep_failed:
            receipt = {
                "schema_version": "ca-phase01-apply-receipt/v1",
                "bundle_id": bundle_id,
                "applied_at_utc": utc_now(),
                "repo": str(repo),
                "files": applied,
                "created_directories": [
                    str(path.relative_to(repo)).replace("\\\\", "/")
                    for path in sorted(created_directories, key=lambda item: (len(item.parts), str(item)))
                ],
                "tests": "not_completed",
                "result": "EXCEPTION_ROLLBACK",
            }
            rollback_from_receipt(repo, receipt, force=True)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
