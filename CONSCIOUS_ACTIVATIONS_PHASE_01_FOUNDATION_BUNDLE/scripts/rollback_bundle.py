from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from apply_bundle import is_git_repo, git, rollback_from_receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--bundle-id", default="CA-PHASE01-FOUNDATION-2026-07-23")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()

    repo = args.repo.resolve()
    state_root = repo / ".conscious-activations" / "bundle-state" / args.bundle_id
    receipt_path = state_root / "apply_receipt.json"
    if not receipt_path.is_file():
        raise SystemExit(f"apply receipt not found: {receipt_path}")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    rollback_from_receipt(repo, receipt, force=args.force)
    receipt["result"] = "ROLLED_BACK"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.commit:
        if not is_git_repo(repo):
            raise SystemExit("--commit requires a git repository")
        git(repo, "add", "--all")
        git(repo, "commit", "-m", "rollback Phase 1 application foundation bundle")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
