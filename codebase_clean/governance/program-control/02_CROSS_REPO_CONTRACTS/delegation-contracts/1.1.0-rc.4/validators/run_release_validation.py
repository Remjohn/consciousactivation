#!/usr/bin/env python3
"""Validate a clean Delegation release using release-relative paths only."""

from __future__ import annotations

import json
import sys
from pathlib import Path


RELEASE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RELEASE_ROOT / "validators"))
sys.path.insert(0, str(RELEASE_ROOT / "contracts" / "generated" / "python"))

from cmf_delegation_contracts.types import (  # noqa: E402
    DerivativeLockInheritance,
    ParentLockEvidence,
    SourceProvenance,
    WrongReadingLockEvidence,
)
from cmf_delegation_validators.compatibility import (  # noqa: E402
    migrate_pre_discriminator_visual_asset_demand,
    migrate_visual_asset_demand_v1,
    negotiate,
)
from cmf_delegation_validators.contracts import (  # noqa: E402
    validate_all_examples,
    validate_closed_schemas,
    validate_release_manifest,
    validate_release_receipt,
)
from cmf_delegation_validators.paths import (  # noqa: E402
    COMPATIBILITY_ROOT,
    FIXTURES_ROOT,
    LAYOUT,
)
from cmf_delegation_validators.release_identity import validate_release_identity  # noqa: E402
from cmf_delegation_validators.derivative_locks import (  # noqa: E402
    DERIVATION_CLASSIFICATION_REQUIRED,
    LOCK_INHERITANCE_VALID,
    PARENT_LOCK_EVIDENCE_REQUIRED,
    PARENT_LOCK_REMOVED,
    PARENT_LOCK_WEAKENED,
    UNAUTHORIZED_LOCK_RELAXATION,
    migrate_legacy_derivative_lock_claim,
    validate_derivative_lock_inheritance,
)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def is_transient(path: Path) -> bool:
    return (
        bool({".pytest_cache", "__pycache__"}.intersection(path.parts))
        or path.name in {".DS_Store", "Thumbs.db", "desktop.ini"}
        or path.suffix.lower() in {".pyc", ".pyo", ".tmp", ".temp", ".swp", ".swo"}
        or path.name.endswith("~")
    )


def main() -> None:
    if LAYOUT != "RELEASE":
        raise SystemExit("run_release_validation.py must execute from a clean release layout")
    checks: dict[str, object] = {}
    checks["examples"] = validate_all_examples()
    validate_closed_schemas()
    checks["closed_schemas"] = "PASS"

    checks["release_identity"] = validate_release_identity()

    if SourceProvenance.__annotations__.get("source_kind") is None:
        raise RuntimeError("Generated Python SourceProvenance lacks source_kind")
    typescript = (RELEASE_ROOT / "contracts/generated/typescript/index.ts").read_text(
        encoding="utf-8"
    )
    if not all(
        value.__annotations__
        for value in (DerivativeLockInheritance, ParentLockEvidence, WrongReadingLockEvidence)
    ):
        raise RuntimeError("Generated Python derivative lock structures are incomplete")
    for required in (
        "SourceKind",
        "SourceProvenance",
        "interview_expression",
        "DerivativeLockInheritance",
        "WrongReadingLockEvidence",
        "ParentLockEvidence",
    ):
        if required not in typescript:
            raise RuntimeError(f"Generated TypeScript lacks {required}")
    checks["generated_types"] = "PASS"

    fixture_paths = sorted(FIXTURES_ROOT.rglob("*.json"))
    for path in fixture_paths:
        load_json(path)
    checks["fixture_json"] = len(fixture_paths)
    migration_paths = sorted((COMPATIBILITY_ROOT / "migrations").glob("*.json"))
    for path in migration_paths:
        load_json(path)
    checks["migration_declarations"] = len(migration_paths)

    direct = load_json(FIXTURES_ROOT / "compatibility/direct/compatible.input.json")
    expected = load_json(FIXTURES_ROOT / "compatibility/direct/compatible.expected.json")
    if negotiate(direct["requester"], direct["provider"]) != expected:
        raise RuntimeError("Direct compatibility fixture mismatch")
    constitutional = FIXTURES_ROOT / "compatibility/constitutional"
    legacy = load_json(constitutional / "aip-lineage.source.json")
    migrated = migrate_visual_asset_demand_v1(legacy["source"], legacy["owner_context"])
    if migrated != load_json(constitutional / "aip-lineage.expected.json"):
        raise RuntimeError("V1 demand migration fixture mismatch")
    pre_source = load_json(constitutional / "pre-source-kind.source.json")
    required = migrate_pre_discriminator_visual_asset_demand(pre_source)
    if required != load_json(
        constitutional / "source-kind-classification-required.expected.json"
    ):
        raise RuntimeError("Source-kind classification-required result mismatch")
    classification = load_json(constitutional / "source-kind-owner-classification.json")
    classified = migrate_pre_discriminator_visual_asset_demand(pre_source, classification)
    if classified != load_json(constitutional / "source-kind-migration.expected.json"):
        raise RuntimeError("Source-kind migration fixture mismatch")
    checks["compatibility_and_migrations"] = "PASS"

    derivative_root = FIXTURES_ROOT / "compatibility/derivative-locks"
    derivative_expectations = {
        "exact-inheritance.valid.json": LOCK_INHERITANCE_VALID,
        "stricter-addition.valid.json": LOCK_INHERITANCE_VALID,
        "lock-removal.invalid.json": PARENT_LOCK_REMOVED,
        "lock-weakening.invalid.json": PARENT_LOCK_WEAKENED,
        "missing-parent-evidence.invalid.json": PARENT_LOCK_EVIDENCE_REQUIRED,
        "ambiguous-derivation.invalid.json": DERIVATION_CLASSIFICATION_REQUIRED,
        "semantic-shortcut.invalid.json": UNAUTHORIZED_LOCK_RELAXATION,
        "authorized-new-demand-relaxation.valid.json": LOCK_INHERITANCE_VALID,
    }
    for fixture_name, expected_status in derivative_expectations.items():
        outcome = validate_derivative_lock_inheritance(load_json(derivative_root / fixture_name))
        if outcome["status"] != expected_status:
            raise RuntimeError(
                f"Derivative fixture {fixture_name} returned {outcome['status']}, expected {expected_status}"
            )
    legacy_derivative = load_json(derivative_root / "legacy-unclassified.input.json")
    if migrate_legacy_derivative_lock_claim(legacy_derivative)["status"] != DERIVATION_CLASSIFICATION_REQUIRED:
        raise RuntimeError("Legacy derivative migration inferred a classification")
    checks["portable_derivative_lock_validation"] = "PASS"

    checks["release_manifest_files"] = validate_release_manifest()
    checks["release_receipt_files"] = validate_release_receipt()
    transients = [
        path.relative_to(RELEASE_ROOT).as_posix()
        for path in RELEASE_ROOT.rglob("*")
        if path.is_file() and is_transient(path.relative_to(RELEASE_ROOT))
    ]
    if transients:
        raise RuntimeError(f"Transient release files found: {transients}")
    checks["transient_files"] = 0
    print(json.dumps({"status": "PASS", "layout": LAYOUT, "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
