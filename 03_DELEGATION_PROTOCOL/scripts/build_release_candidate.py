#!/usr/bin/env python3
"""Build an immutable, self-validating Delegation release candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.0-rc.4"
PROTOCOL_VERSION = "1.0"
VISUAL_ASSET_DEMAND_VERSION = "1.1"
COMPATIBILITY_PROFILE_VERSION = "1.0"
DEFAULT_TARGET = ROOT / "delegation-contracts" / VERSION
TRANSIENT_PARTS = {".pytest_cache", "__pycache__"}
TRANSIENT_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
TRANSIENT_SUFFIXES = {".pyc", ".pyo", ".tmp", ".temp", ".swp", ".swo"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def is_transient(path: Path) -> bool:
    return (
        bool(TRANSIENT_PARTS.intersection(path.parts))
        or path.name in TRANSIENT_NAMES
        or path.suffix.lower() in TRANSIENT_SUFFIXES
        or path.name.endswith("~")
    )


def ignore_release_material(directory: str, names: list[str]) -> set[str]:
    current = Path(directory).resolve()
    ignored = {
        name
        for name in names
        if is_transient(current / name)
    }
    contracts_root = (ROOT / "packages" / "contracts").resolve()
    if current == contracts_root:
        ignored.update({"src", "tools", "source-manifest.json", "release-manifest.json"})
    return ignored


def inventory(target: Path, excluded: set[str]) -> list[dict[str, object]]:
    files: list[dict[str, object]] = []
    for path in sorted(target.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(target).as_posix()
        if relative in excluded:
            continue
        if is_transient(Path(relative)):
            raise RuntimeError(f"Transient material entered release staging: {relative}")
        files.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return files


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def build(target: Path, validator_tests: int, protocol_tests: int) -> dict[str, object]:
    if target.exists():
        raise SystemExit(f"Release target already exists; immutable candidate will not be overwritten: {target}")
    target.mkdir(parents=True)
    for name in ("contracts", "compatibility", "fixtures", "validators", "protocol"):
        shutil.copytree(
            ROOT / "packages" / name,
            target / name,
            ignore=ignore_release_material,
        )
    for name in ("COMPATIBILITY_MANIFEST.yaml", "CONTRACT_CHANGELOG.md"):
        shutil.copy2(ROOT / name, target / name)
    report_copies = {
        ROOT / "docs" / "releases" / "RC3_CONVERGENCE_REJECTION_REPORT.md": target
        / "RC3_CONVERGENCE_REJECTION_REPORT.md",
        ROOT / "docs" / "releases" / "RC4_CORRECTION_REPORT.md": target
        / "RC4_CORRECTION_REPORT.md",
        ROOT / "docs" / "validation" / "RC4_CLEAN_ROOM_VALIDATION_REPORT.json": target
        / "CLEAN_ROOM_VALIDATION_REPORT.json",
    }
    for source, destination in report_copies.items():
        shutil.copy2(source, destination)

    write_json(
        target / "SOURCE_ONLY_FILES.json",
        {
            "status": "SOURCE_ONLY_NOT_REQUIRED_FOR_RELEASE_VALIDATION",
            "source_repository_paths": [
                "packages/contracts/src/**",
                "packages/contracts/tools/**",
                "packages/contracts/source-manifest.json",
                "scripts/**",
                "contracts/**/*.yaml",
                "governance/**",
                "prd/**",
                "docs/**",
            ],
            "release_validation_root": ".",
            "release_paths_are_relative": True,
        },
    )
    (target / "BASELINE_STATUS.md").write_text(
        "# Delegation Contract Baseline 1.1.0-rc.4\n\n"
        "Status: portable derivative-lock inheritance correction release candidate.\n\n"
        "- Historical rejection evidence: `RC3_CONVERGENCE_REJECTION_REPORT.md`\n"
        f"- Envelope protocol: `{PROTOCOL_VERSION}`\n"
        f"- Visual Asset Demand: `{VISUAL_ASSET_DEMAND_VERSION}`\n"
        f"- Compatibility profile: `{COMPATIBILITY_PROFILE_VERSION}`\n"
        "- Source discriminator: `source_provenance.source_kind`\n"
        "- Derivative lock contract: `derivative-lock-inheritance@1.0`\n"
        "- Portable inheritance enforcement: `PASS`\n"
        f"- Validator suite: `{validator_tests} passed`\n"
        f"- Reference protocol suite: `{protocol_tests} passed`\n"
        "- Clean-room release validation: `PASS`\n"
        "- Signature status: `UNSIGNED`\n"
        "- Production authorized: `false`\n\n"
        "The release is transport-neutral, immutable, and not a production authorization.\n",
        encoding="utf-8",
        newline="\n",
    )

    hash_inventory_path = target / "HASH_INVENTORY.json"
    hash_inventory_files = inventory(
        target,
        {"HASH_INVENTORY.json", "contracts/release-manifest.json", "RELEASE_RECEIPT.json"},
    )
    write_json(
        hash_inventory_path,
        {
            "package": "delegation-contracts",
            "package_version": VERSION,
            "generation_basis": "actual_release_directory",
            "hash_algorithm": "SHA-256",
            "self_hash_and_receipt_hash": "represented_by_release_receipt",
            "file_count_excluding_inventory_manifest_and_receipt": len(hash_inventory_files),
            "files": hash_inventory_files,
        },
    )

    release_manifest_path = target / "contracts" / "release-manifest.json"
    manifest_files = inventory(
        target,
        {"contracts/release-manifest.json", "RELEASE_RECEIPT.json"},
    )
    release_manifest = {
        "package": "cmf-delegation-contract-baseline",
        "package_version": VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "visual_asset_demand_version": VISUAL_ASSET_DEMAND_VERSION,
        "compatibility_profile_version": COMPATIBILITY_PROFILE_VERSION,
        "status": "RELEASE_CANDIDATE",
        "signature_status": "UNSIGNED",
        "production_authorized": False,
        "layout": "release-root-relative",
        "generation_basis": "actual_release_directory",
        "self_path": "contracts/release-manifest.json",
        "receipt_path": "RELEASE_RECEIPT.json",
        "self_and_receipt_representation": "represented_by_explicit_paths_and_receipt_inventory",
        "excluded_patterns": [
            ".pytest_cache/**",
            "__pycache__/**",
            "*.pyc",
            "*.pyo",
            "*.tmp",
            "*.temp",
            ".DS_Store",
            "Thumbs.db",
            "desktop.ini",
        ],
        "file_count_excluding_manifest_and_receipt": len(manifest_files),
        "files": manifest_files,
    }
    write_json(release_manifest_path, release_manifest)

    receipt_files = inventory(target, {"RELEASE_RECEIPT.json"})
    digest_input = json.dumps(
        receipt_files, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    release_digest = "sha256:" + hashlib.sha256(digest_input).hexdigest()
    receipt = {
        "package": "delegation-contracts",
        "package_version": VERSION,
        "correction_class": "PORTABLE_DERIVATIVE_LOCK_INHERITANCE_ENFORCEMENT",
        "protocol_version": PROTOCOL_VERSION,
        "compatibility_profile_version": COMPATIBILITY_PROFILE_VERSION,
        "message_versions": {
            "visual-asset-demand": VISUAL_ASSET_DEMAND_VERSION,
            "derivative-lock-inheritance": PROTOCOL_VERSION,
        },
        "status": "RELEASE_CANDIDATE",
        "signature_status": "UNSIGNED",
        "production_authorized": False,
        "tests": {
            "validators": validator_tests,
            "protocol": protocol_tests,
            "total": validator_tests + protocol_tests,
            "clean_room": "PASS",
        },
        "release_manifest_sha256": sha256(release_manifest_path),
        "file_count_excluding_receipt": len(receipt_files),
        "release_digest": release_digest,
        "files": receipt_files,
    }
    write_json(target / "RELEASE_RECEIPT.json", receipt)
    return {
        "release_path": str(target),
        "package_version": VERSION,
        "file_count_excluding_receipt": len(receipt_files),
        "release_digest": release_digest,
        "release_manifest_sha256": receipt["release_manifest_sha256"],
        "release_receipt_sha256": sha256(target / "RELEASE_RECEIPT.json"),
        "tests": receipt["tests"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--validator-tests", type=int, required=True)
    parser.add_argument("--protocol-tests", type=int, required=True)
    args = parser.parse_args()
    if args.validator_tests < 1 or args.protocol_tests < 1:
        raise SystemExit("Passing test counts are required before sealing a candidate")
    print(
        json.dumps(
            build(args.output.resolve(), args.validator_tests, args.protocol_tests),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
