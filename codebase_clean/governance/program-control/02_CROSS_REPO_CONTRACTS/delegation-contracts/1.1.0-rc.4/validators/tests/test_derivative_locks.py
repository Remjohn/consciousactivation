from __future__ import annotations

import json
from copy import deepcopy
import unittest

from jsonschema import ValidationError

from cmf_delegation_validators.compatibility import (
    CompatibilityError,
    negotiate,
    validate_derivative_lock_adapter,
)
from cmf_delegation_validators.contracts import validate_payload
from cmf_delegation_validators.derivative_locks import (
    DERIVATION_CLASSIFICATION_REQUIRED,
    LOCK_INHERITANCE_VALID,
    PARENT_LOCK_EVIDENCE_REQUIRED,
    PARENT_LOCK_REMOVED,
    PARENT_LOCK_WEAKENED,
    UNAUTHORIZED_LOCK_RELAXATION,
    migrate_legacy_derivative_lock_claim,
    validate_derivative_lock_inheritance,
)
from cmf_delegation_validators.paths import COMPATIBILITY_ROOT, FIXTURES_ROOT, ROOT


class DerivativeLockInheritanceTests(unittest.TestCase):
    def fixture(self, name: str) -> dict[str, object]:
        return json.loads(
            (FIXTURES_ROOT / "compatibility" / "derivative-locks" / name).read_text(
                encoding="utf-8"
            )
        )

    def test_exact_lock_inheritance_passes(self) -> None:
        claim = self.fixture("exact-inheritance.valid.json")
        validate_payload("derivative-lock-inheritance", claim)
        outcome = validate_derivative_lock_inheritance(claim)
        self.assertTrue(outcome["valid"])
        self.assertEqual(outcome["status"], LOCK_INHERITANCE_VALID)
        self.assertEqual(outcome["added_lock_ids"], [])

    def test_stricter_lock_addition_passes(self) -> None:
        outcome = validate_derivative_lock_inheritance(
            self.fixture("stricter-addition.valid.json")
        )
        self.assertTrue(outcome["valid"])
        self.assertEqual(outcome["status"], LOCK_INHERITANCE_VALID)
        self.assertEqual(outcome["added_lock_ids"], ["lock-no-added-symbolism"])

    def test_lock_removal_fails_and_requires_new_upstream_demand(self) -> None:
        outcome = validate_derivative_lock_inheritance(
            self.fixture("lock-removal.invalid.json")
        )
        self.assertEqual(outcome["status"], PARENT_LOCK_REMOVED)
        self.assertTrue(outcome["requires_new_authoritative_demand"])

    def test_lock_weakening_fails_and_requires_new_upstream_demand(self) -> None:
        outcome = validate_derivative_lock_inheritance(
            self.fixture("lock-weakening.invalid.json")
        )
        self.assertEqual(outcome["status"], PARENT_LOCK_WEAKENED)
        self.assertTrue(outcome["requires_new_authoritative_demand"])

    def test_missing_parent_evidence_fails_without_assumption(self) -> None:
        outcome = validate_derivative_lock_inheritance(
            self.fixture("missing-parent-evidence.invalid.json")
        )
        self.assertEqual(outcome["status"], PARENT_LOCK_EVIDENCE_REQUIRED)

    def test_immutable_parent_reference_can_be_resolved_from_release_only_input(self) -> None:
        claim = self.fixture("exact-inheritance.valid.json")
        resolved = deepcopy(claim["parent_lock_evidence"]["parent_wrong_reading_locks"])
        claim["parent_lock_evidence"]["parent_wrong_reading_locks"] = None
        outcome = validate_derivative_lock_inheritance(claim, resolved)
        self.assertEqual(outcome["status"], LOCK_INHERITANCE_VALID)

    def test_ambiguous_derivation_type_fails_with_typed_outcome(self) -> None:
        outcome = validate_derivative_lock_inheritance(
            self.fixture("ambiguous-derivation.invalid.json")
        )
        self.assertEqual(outcome["status"], DERIVATION_CLASSIFICATION_REQUIRED)

    def test_semantic_transformation_cannot_use_deterministic_shortcut(self) -> None:
        outcome = validate_derivative_lock_inheritance(
            self.fixture("semantic-shortcut.invalid.json")
        )
        self.assertEqual(outcome["status"], UNAUTHORIZED_LOCK_RELAXATION)

    def test_authorized_relaxation_uses_new_immutable_demand_version(self) -> None:
        claim = self.fixture("authorized-new-demand-relaxation.valid.json")
        outcome = validate_derivative_lock_inheritance(claim)
        self.assertTrue(outcome["valid"])
        self.assertTrue(outcome["authorized_relaxation"])
        authorization = claim["authoritative_lock_authorization"]
        governing = claim["governing_authoritative_demand_ref"]
        self.assertGreater(
            authorization["authoritative_demand_ref"]["version"], governing["version"]
        )
        self.assertEqual(authorization["supersedes_demand_ref"], governing)

    def test_empty_derivative_lock_array_is_schema_invalid(self) -> None:
        claim = self.fixture("exact-inheritance.valid.json")
        claim["derivative_wrong_reading_locks"] = []
        with self.assertRaises(ValidationError):
            validate_payload("derivative-lock-inheritance", claim)

    def test_generated_python_and_typescript_preserve_structured_contract(self) -> None:
        python_types = (
            ROOT / "contracts/generated/python/cmf_delegation_contracts/types.py"
        ).read_text(encoding="utf-8")
        typescript = (ROOT / "contracts/generated/typescript/index.ts").read_text(
            encoding="utf-8"
        )
        for token in (
            "WrongReadingLockEvidence",
            "ParentLockEvidence",
            "AuthoritativeLockAuthorization",
            "DerivativeLockInheritance",
            "derivative_wrong_reading_locks",
        ):
            self.assertIn(token, python_types)
            self.assertIn(token, typescript)

    def test_adapter_preserves_parent_derivative_and_lock_evidence(self) -> None:
        source = self.fixture("adapter.source.json")
        expected = self.fixture("adapter.expected.json")
        self.assertEqual(validate_derivative_lock_adapter(source, expected), expected)
        changed = deepcopy(expected)
        changed["derivative_wrong_reading_locks"][0]["enforcement_level"] += 1
        with self.assertRaisesRegex(CompatibilityError, "LOSSY_ADAPTER"):
            validate_derivative_lock_adapter(source, changed)

    def test_legacy_migration_never_guesses_classification_or_parent_evidence(self) -> None:
        source = self.fixture("legacy-unclassified.input.json")
        first = migrate_legacy_derivative_lock_claim(source)
        second = migrate_legacy_derivative_lock_claim(source)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], DERIVATION_CLASSIFICATION_REQUIRED)
        self.assertNotIn("target", first)
        migration = json.loads(
            (
                COMPATIBILITY_ROOT
                / "migrations/derivative-lock-inheritance-v0-to-v1.json"
            ).read_text(encoding="utf-8")
        )
        self.assertFalse(migration["automatic"])
        self.assertEqual(migration["inference"], "PROHIBITED")

    def test_parse_without_derivative_enforcement_is_incompatible(self) -> None:
        manifest = json.loads(
            (COMPATIBILITY_ROOT / "manifest.json").read_text(encoding="utf-8")
        )
        provider = deepcopy(manifest)
        provider["derivative_asset_flows"]["lock_inheritance_modes"] = ["PARSE"]
        with self.assertRaisesRegex(
            CompatibilityError, "DERIVATIVE_LOCK_ENFORCEMENT_UNSUPPORTED"
        ):
            negotiate(manifest, provider)


if __name__ == "__main__":
    unittest.main()
