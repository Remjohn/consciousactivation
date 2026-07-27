from __future__ import annotations

import json
from copy import deepcopy
import unittest

import yaml

from cmf_delegation_validators.compatibility import (
    CompatibilityError,
    adapt_legacy_demand_ref,
    migrate_legacy_submission_receipt,
    migrate_visual_asset_demand_v1,
    migrate_pre_discriminator_visual_asset_demand,
    negotiate,
    validate_adapter_claim,
    validate_visual_asset_demand_adapter,
)
from cmf_delegation_validators.contracts import load_registry, validate_payload
from cmf_delegation_validators.paths import (
    COMPATIBILITY_ROOT,
    FIXTURES_ROOT,
    ROOT,
    WORKSPACE_ROOT,
)


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

    def test_visual_asset_demand_migration_is_lossless_traceable_and_repeatable(self) -> None:
        fixture_root = FIXTURES_ROOT / "compatibility" / "constitutional"
        inputs = json.loads((fixture_root / "aip-lineage.source.json").read_text(encoding="utf-8"))
        expected = json.loads(
            (fixture_root / "aip-lineage.expected.json").read_text(encoding="utf-8")
        )
        first = migrate_visual_asset_demand_v1(inputs["source"], inputs["owner_context"])
        second = migrate_visual_asset_demand_v1(inputs["source"], inputs["owner_context"])
        self.assertEqual(first, expected)
        self.assertEqual(first, second)
        validate_payload("visual-asset-demand", first["target"])
        validate_payload("contract-migration", first["receipt"])
        source_lineage = inputs["owner_context"]["semantic_context"][
            "activative_semantic_lineage"
        ]
        target_lineage = first["target"]["activative_semantic_lineage"]
        self.assertEqual(target_lineage, source_lineage)
        self.assertEqual(
            target_lineage["activative_intelligence_pack_ref"]["version"],
            source_lineage["activative_intelligence_pack_ref"]["version"],
        )
        self.assertEqual(
            target_lineage["activative_intelligence_pack_ref"]["payload_hash"],
            source_lineage["activative_intelligence_pack_ref"]["payload_hash"],
        )
        self.assertEqual(target_lineage["reaction_receipt_refs"], source_lineage["reaction_receipt_refs"])
        self.assertEqual(target_lineage["expression_moment_refs"], source_lineage["expression_moment_refs"])
        self.assertTrue(first["target"]["wrong_reading_locks"])
        self.assertEqual(
            first["target"]["source_provenance"],
            inputs["owner_context"]["semantic_context"]["source_provenance"],
        )

    def test_visual_asset_demand_migration_requires_complete_owner_context(self) -> None:
        fixture_root = FIXTURES_ROOT / "compatibility" / "constitutional"
        inputs = json.loads((fixture_root / "aip-lineage.source.json").read_text(encoding="utf-8"))
        incomplete = dict(inputs["owner_context"])
        incomplete["semantic_context"] = dict(incomplete["semantic_context"])
        incomplete["semantic_context"].pop("visual_narrative_program")
        with self.assertRaisesRegex(CompatibilityError, "MIGRATION_REQUIRED"):
            migrate_visual_asset_demand_v1(inputs["source"], incomplete)

    def test_expression_moment_drop_is_a_lossy_adapter(self) -> None:
        fixture = json.loads(
            (
                FIXTURES_ROOT
                / "compatibility"
                / "constitutional"
                / "expression-moment-drop.invalid.json"
            ).read_text(encoding="utf-8")
        )
        with self.assertRaisesRegex(CompatibilityError, "LOSSY_ADAPTER"):
            validate_adapter_claim(fixture["adapter_claim"], fixture["protected_paths"])

    def test_parse_only_and_missing_evaluator_evidence_are_incompatible(self) -> None:
        root = FIXTURES_ROOT / "compatibility" / "constitutional"
        parse_only = json.loads(
            (root / "wrong-reading-unsupported.invalid.json").read_text(encoding="utf-8")
        )
        with self.assertRaisesRegex(CompatibilityError, "SEMANTIC_ENFORCEMENT_UNSUPPORTED"):
            negotiate(parse_only["requester"], parse_only["provider"])
        evaluator_gap = json.loads(
            (root / "evaluator-gap.invalid.json").read_text(encoding="utf-8")
        )
        with self.assertRaisesRegex(CompatibilityError, "EVALUATOR_EVIDENCE_MISSING"):
            negotiate(evaluator_gap["requester"], evaluator_gap["provider"])
        source_parse_only = json.loads(
            (root / "source-provenance-parse-only.invalid.json").read_text(encoding="utf-8")
        )
        with self.assertRaisesRegex(CompatibilityError, "SEMANTIC_ENFORCEMENT_UNSUPPORTED"):
            negotiate(source_parse_only["requester"], source_parse_only["provider"])

    def test_pre_discriminator_migration_never_guesses_source_kind(self) -> None:
        root = FIXTURES_ROOT / "compatibility" / "constitutional"
        source = json.loads((root / "pre-source-kind.source.json").read_text(encoding="utf-8"))
        expected = json.loads(
            (root / "source-kind-classification-required.expected.json").read_text(encoding="utf-8")
        )
        result = migrate_pre_discriminator_visual_asset_demand(source)
        self.assertEqual(result, expected)
        self.assertEqual(result["status"], "SOURCE_KIND_CLASSIFICATION_REQUIRED")
        self.assertNotIn("target", result)

    def test_owner_classified_source_kind_migration_is_traceable_and_repeatable(self) -> None:
        root = FIXTURES_ROOT / "compatibility" / "constitutional"
        source = json.loads((root / "pre-source-kind.source.json").read_text(encoding="utf-8"))
        owner = json.loads(
            (root / "source-kind-owner-classification.json").read_text(encoding="utf-8")
        )
        expected = json.loads((root / "source-kind-migration.expected.json").read_text(encoding="utf-8"))
        first = migrate_pre_discriminator_visual_asset_demand(source, owner)
        second = migrate_pre_discriminator_visual_asset_demand(source, owner)
        self.assertEqual(first, expected)
        self.assertEqual(first, second)
        self.assertEqual(first["target"]["source_provenance"]["source_kind"], "interview_expression")
        validate_payload("visual-asset-demand", first["target"])
        validate_payload("contract-migration", first["receipt"])

    def test_interview_classification_does_not_manufacture_missing_provenance(self) -> None:
        root = FIXTURES_ROOT / "compatibility" / "constitutional"
        source = json.loads((root / "pre-source-kind.source.json").read_text(encoding="utf-8"))
        owner = json.loads(
            (root / "source-kind-owner-classification.json").read_text(encoding="utf-8")
        )
        source["activative_semantic_lineage"].pop("reaction_receipt_refs")
        result = migrate_pre_discriminator_visual_asset_demand(source, owner)
        self.assertEqual(result["status"], "INTERVIEW_PROVENANCE_REQUIRED")
        self.assertNotIn("target", result)

    def test_adapter_preserves_source_discriminator_and_interview_provenance(self) -> None:
        entry = next(
            item for item in load_registry()["messages"] if item["message_type"] == "visual-asset-demand"
        )
        source = json.loads((ROOT / entry["example_path"]).read_text(encoding="utf-8"))
        self.assertEqual(validate_visual_asset_demand_adapter(source, deepcopy(source)), source)
        changed = deepcopy(source)
        changed["source_provenance"]["source_kind"] = "public_comment"
        with self.assertRaisesRegex(CompatibilityError, "LOSSY_ADAPTER"):
            validate_visual_asset_demand_adapter(source, changed)

    def test_root_manifest_matches_the_release_candidate_and_is_not_publishable(self) -> None:
        root_manifest = yaml.safe_load(
            (WORKSPACE_ROOT / "COMPATIBILITY_MANIFEST.yaml").read_text(encoding="utf-8")
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
