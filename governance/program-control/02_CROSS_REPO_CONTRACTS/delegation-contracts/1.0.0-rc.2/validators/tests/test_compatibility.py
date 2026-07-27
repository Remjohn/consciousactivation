from __future__ import annotations

import json
import unittest

import yaml

from cmf_delegation_validators.compatibility import (
    CompatibilityError,
    adapt_legacy_demand_ref,
    migrate_legacy_submission_receipt,
    negotiate,
)
from cmf_delegation_validators.contracts import load_registry, validate_payload
from cmf_delegation_validators.paths import COMPATIBILITY_ROOT, FIXTURES_ROOT, ROOT


class CompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(
            (COMPATIBILITY_ROOT / "manifest.json").read_text(encoding="utf-8")
        )

    def test_release_candidate_negotiates_with_itself(self) -> None:
        result = negotiate(self.manifest, self.manifest)
        self.assertEqual(result["protocol_version"], "1.0")
        self.assertEqual(result["signature_algorithm"], "Ed25519")

    def test_missing_required_feature_fails_negotiation(self) -> None:
        provider = dict(self.manifest)
        provider["required_features"] = ["closed.schemas"]
        with self.assertRaises(CompatibilityError):
            negotiate(self.manifest, provider)

    def test_direct_compatibility_golden_vector(self) -> None:
        fixture_root = FIXTURES_ROOT / "compatibility" / "direct"
        inputs = json.loads((fixture_root / "compatible.input.json").read_text(encoding="utf-8"))
        expected = json.loads((fixture_root / "compatible.expected.json").read_text(encoding="utf-8"))
        self.assertEqual(negotiate(inputs["requester"], inputs["provider"]), expected)

    def test_legacy_demand_ref_adapter_is_lossless_and_deterministic(self) -> None:
        legacy = json.loads(
            (FIXTURES_ROOT / "conformance" / "legacy-demand-ref.input.json").read_text(encoding="utf-8")
        )
        context = json.loads(
            (FIXTURES_ROOT / "conformance" / "legacy-demand-ref.context.json").read_text(encoding="utf-8")
        )
        self.assertEqual(adapt_legacy_demand_ref(legacy, context), context)
        self.assertEqual(adapt_legacy_demand_ref(legacy, context), adapt_legacy_demand_ref(legacy, context))

    def test_adapter_rejects_unpinned_or_mismatched_context(self) -> None:
        with self.assertRaises(CompatibilityError):
            adapt_legacy_demand_ref({"demand_ref": "old"}, {"request_id": "old"})
        context = {
            "request_id": "new",
            "version": 1,
            "payload_hash": "sha256:" + "a" * 64,
            "canonical_ref": "cmf-contract://demands/new/1",
        }
        with self.assertRaises(CompatibilityError):
            adapt_legacy_demand_ref({"demand_ref": "old"}, context)

    def test_legacy_submission_receipt_requires_explicit_migration(self) -> None:
        migration = json.loads(
            (COMPATIBILITY_ROOT / "migrations" / "submission-receipt-v0-to-v1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(migration["automatic"])
        self.assertEqual(migration["classification"], "EXPLICIT_MIGRATION_REQUIRED")
        self.assertNotIn(
            "submission-receipt",
            {item["message_type"] for item in load_registry()["messages"]},
        )

    def test_owner_evidenced_submission_receipt_migration_is_golden_and_repeatable(self) -> None:
        fixture_root = FIXTURES_ROOT / "compatibility" / "migration"
        source = json.loads((fixture_root / "submission-receipt.source.json").read_text(encoding="utf-8"))
        evidence = json.loads(
            (fixture_root / "submission-receipt.owner-evidence.json").read_text(encoding="utf-8")
        )
        expected = json.loads(
            (fixture_root / "submission-receipt.expected.json").read_text(encoding="utf-8")
        )
        first = migrate_legacy_submission_receipt(source, evidence)
        second = migrate_legacy_submission_receipt(source, evidence)
        self.assertEqual(first, expected)
        self.assertEqual(first, second)
        validate_payload(
            "submission-validation-receipt",
            first["targets"]["submission_validation_receipt"],
        )
        validate_payload("admission-receipt", first["targets"]["admission_receipt"])
        validate_payload("contract-migration", first["receipt"])

    def test_submission_receipt_migration_rejects_missing_owner_and_lossy_target(self) -> None:
        fixture_root = FIXTURES_ROOT / "compatibility" / "migration"
        source = json.loads((fixture_root / "submission-receipt.source.json").read_text(encoding="utf-8"))
        evidence = json.loads(
            (fixture_root / "submission-receipt.owner-evidence.json").read_text(encoding="utf-8")
        )
        with self.assertRaisesRegex(CompatibilityError, "MIGRATION_REQUIRED"):
            migrate_legacy_submission_receipt(
                source,
                {"protocol_validation_producer": "DELEGATION_PROTOCOL"},
            )
        lossy = json.loads(
            (fixture_root / "submission-receipt.lossy.invalid.json").read_text(encoding="utf-8")
        )
        with self.assertRaisesRegex(CompatibilityError, "TARGET_INVALID"):
            migrate_legacy_submission_receipt(lossy["source"], evidence)

    def test_root_manifest_matches_the_release_candidate_and_is_not_publishable(self) -> None:
        root_manifest = yaml.safe_load(
            (ROOT / "COMPATIBILITY_MANIFEST.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(root_manifest["package_version"], self.manifest["package_version"])
        self.assertEqual(root_manifest["protocol_versions"], self.manifest["protocol_versions"])
        self.assertEqual(root_manifest["release_status"], "RELEASE_CANDIDATE")
        self.assertEqual(root_manifest["readiness"]["local_stage4_gates"], "PASS")
        self.assertEqual(root_manifest["readiness"]["overall_stage4_verdict"], "FAIL")
        self.assertFalse(root_manifest["readiness"]["stage5_authorized"])
        self.assertFalse(root_manifest["publication"]["publishable"])
        self.assertGreater(len(root_manifest["publication"]["blockers"]), 0)
        self.assertEqual(root_manifest["integrity"]["signature_status"], "UNSIGNED")


if __name__ == "__main__":
    unittest.main()
