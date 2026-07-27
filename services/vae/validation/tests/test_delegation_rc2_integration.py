from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

from jsonschema import ValidationError
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
PIN_PATH = REPO_ROOT / "contracts/integration/DELEGATION_CONTRACT_PIN.yaml"
FIXTURE_PATH = REPO_ROOT / "validation/fixtures/delegation-rc2/VAE_BOUNDARY_CASES.json"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(relative_path: str) -> dict:
    return yaml.safe_load((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def inherited_locks_are_valid(case: dict) -> bool:
    parent = set(case["parent_locks"])
    derivative = set(case["derivative_locks"])
    if case["derivative_kind"] in {
        "deterministic_delivery_variant",
        "non_semantic_derivative",
    }:
        return parent.issubset(derivative)
    upstream = case.get("derivative_demand", {})
    return (
        upstream.get("upstream_authorized") is True
        and upstream.get("request_id") == case["parent_demand"]["request_id"]
        and upstream.get("version", 0) > case["parent_demand"]["version"]
    )


@unittest.skip("Historical RC2/RC3 integration evidence; active suite is test_delegation_rc4_integration.py")
class DelegationRC2IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pin = yaml.safe_load(PIN_PATH.read_text(encoding="utf-8"))
        cls.release = Path(cls.pin["package"]["release_path"])
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        sys.path.insert(0, str(cls.release / "validators"))
        from cmf_delegation_validators.compatibility import (  # noqa: PLC0415
            CompatibilityError,
            migrate_pre_discriminator_visual_asset_demand,
            negotiate,
            validate_visual_asset_demand_adapter,
        )
        from cmf_delegation_validators.contracts import validate_payload  # noqa: PLC0415

        cls.CompatibilityError = CompatibilityError
        cls.migrate_pre_discriminator_visual_asset_demand = staticmethod(
            migrate_pre_discriminator_visual_asset_demand
        )
        cls.negotiate = staticmethod(negotiate)
        cls.validate_visual_asset_demand_adapter = staticmethod(
            validate_visual_asset_demand_adapter
        )
        cls.validate_payload = staticmethod(validate_payload)
        cls.demand = json.loads(
            (cls.release / "contracts/examples/visual-asset-demand.example.json").read_text(
                encoding="utf-8"
            )
        )

    def test_exact_release_and_manifest_pin(self) -> None:
        integrity = self.pin["integrity"]
        receipt_path = self.release / integrity["release_receipt"]["path"]
        manifest_path = self.release / integrity["release_manifest"]["path"]
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(self.pin["package"]["package_version"], "1.1.0-rc.3")
        self.assertEqual(receipt["release_digest"], integrity["release_digest"])
        self.assertEqual(sha256(receipt_path), integrity["release_receipt"]["sha256"])
        self.assertEqual(sha256(manifest_path), integrity["release_manifest"]["sha256"])
        self.assertEqual(
            receipt["release_manifest_sha256"], integrity["release_manifest"]["sha256"]
        )

    def test_receipt_declares_the_exact_release_file_set(self) -> None:
        receipt = json.loads((self.release / "RELEASE_RECEIPT.json").read_text(encoding="utf-8"))
        declared = {item["path"] for item in receipt["files"]}
        actual = {
            path.relative_to(self.release).as_posix()
            for path in self.release.rglob("*")
            if path.is_file()
            and path.name != "RELEASE_RECEIPT.json"
            and "__pycache__" not in path.parts
            and ".pytest_cache" not in path.parts
        }
        self.assertEqual(actual, declared)
        for item in receipt["files"]:
            path = self.release / item["path"]
            self.assertEqual(path.stat().st_size, item["bytes"])
            self.assertEqual(sha256(path), item["sha256"])

    def test_source_only_manifest_hash_is_pinned_without_extending_release_trust(self) -> None:
        source = self.pin["integrity"]["source_manifest"]
        self.assertEqual(sha256(Path(source["path"])), source["sha256"])
        self.assertEqual(
            source["status"], "source_only_provenance_not_distributed_or_receipt_covered"
        )
        self.assertFalse((self.release / "contracts/source-manifest.json").exists())

    def test_typed_source_discriminator_and_conditional_provenance(self) -> None:
        self.validate_payload("visual-asset-demand", self.demand)
        for mutation in ("missing_discriminator", "unknown_discriminator"):
            invalid = copy.deepcopy(self.demand)
            if mutation == "missing_discriminator":
                invalid["source_provenance"].pop("source_kind")
            else:
                invalid["source_provenance"]["source_kind"] = "guessed_source"
            with self.assertRaises(ValidationError):
                self.validate_payload("visual-asset-demand", invalid)

        for field in ("reaction_receipt_refs", "expression_moment_refs"):
            for value in (None, []):
                invalid = copy.deepcopy(self.demand)
                if value is None:
                    invalid["activative_semantic_lineage"].pop(field)
                else:
                    invalid["activative_semantic_lineage"][field] = value
                with self.assertRaises(ValidationError):
                    self.validate_payload("visual-asset-demand", invalid)

        non_interview = copy.deepcopy(self.demand)
        non_interview["source_provenance"]["source_kind"] = "authored_source"
        non_interview["activative_semantic_lineage"].pop("reaction_receipt_refs")
        non_interview["activative_semantic_lineage"].pop("expression_moment_refs")
        self.validate_payload("visual-asset-demand", non_interview)

    def test_request_mapping_is_complete_and_lossless(self) -> None:
        mapping = load_yaml("contracts/integration/VISUAL_ASSET_DEMAND_REQUEST_MAPPING.yaml")
        self.assertEqual(set(mapping["preserved_top_level_fields"]), set(self.demand))
        self.assertEqual(
            self.validate_visual_asset_demand_adapter(self.demand, copy.deepcopy(self.demand)),
            self.demand,
        )
        lossy = copy.deepcopy(self.demand)
        lossy["activative_semantic_lineage"].pop("expression_moment_refs")
        with self.assertRaises(self.CompatibilityError):
            self.validate_visual_asset_demand_adapter(self.demand, lossy)

    def test_parse_without_enforcement_is_rejected(self) -> None:
        fixture = json.loads(
            (
                self.release
                / "fixtures/compatibility/constitutional/source-provenance-parse-only.invalid.json"
            ).read_text(encoding="utf-8")
        )
        with self.assertRaises(self.CompatibilityError):
            self.negotiate(fixture["requester"], fixture["provider"])

    def test_migration_never_guesses_or_invents_source_provenance(self) -> None:
        root = self.release / "fixtures/compatibility/constitutional"
        source = json.loads((root / "pre-source-kind.source.json").read_text(encoding="utf-8"))
        result = self.migrate_pre_discriminator_visual_asset_demand(source)
        self.assertEqual(result["status"], "SOURCE_KIND_CLASSIFICATION_REQUIRED")
        self.assertNotIn("target", result)

        owner = json.loads(
            (root / "source-kind-owner-classification.json").read_text(encoding="utf-8")
        )
        source["activative_semantic_lineage"].pop("reaction_receipt_refs")
        result = self.migrate_pre_discriminator_visual_asset_demand(source, owner)
        self.assertEqual(result["status"], "INTERVIEW_PROVENANCE_REQUIRED")
        self.assertNotIn("target", result)

    def test_generated_python_and_typescript_expose_source_kind(self) -> None:
        python_types = (
            self.release / "contracts/generated/python/cmf_delegation_contracts/types.py"
        ).read_text(encoding="utf-8")
        typescript_types = (
            self.release / "contracts/generated/typescript/index.ts"
        ).read_text(encoding="utf-8")
        self.assertIn("SourceKind = Literal[", python_types)
        self.assertIn("source_provenance: SourceProvenance", python_types)
        self.assertIn("export type SourceKind =", typescript_types)
        self.assertIn("source_provenance: SourceProvenance", typescript_types)

    def test_h003_derivative_lock_inheritance_and_authorized_relaxation(self) -> None:
        for case in self.fixture["wrong_reading_lock_inheritance"]:
            valid = inherited_locks_are_valid(case)
            if case["expected"] == "REJECT":
                self.assertFalse(valid, case["id"])
            else:
                self.assertTrue(valid, case["id"])

    def test_h004_feature_contract_reference_is_typed_versioned_and_immutable(self) -> None:
        boundary = self.fixture["feature_contract_boundary"]
        authoritative = boundary["authoritative_contract_ref"]
        realization_ref = boundary["VAE_realization"]["authoritative_contract_ref"]
        self.assertEqual(authoritative, realization_ref)
        self.assertEqual(
            set(authoritative), {"resource_id", "version", "payload_hash", "canonical_ref"}
        )
        self.assertEqual(boundary["authoritative_owner"], "CONTENT_HARNESS")
        self.assertEqual(boundary["realization_owner"], "VISUAL_ASSET_EDITOR")
        result_mapping = load_yaml("contracts/integration/ASSET_RESULT_MAPPING.yaml")
        self.assertEqual(
            result_mapping["feature_contract_realization"]["mutation_of_authoritative_contract"],
            "rejected",
        )

    def test_result_mapping_is_complete_and_cannot_authorize_consumption(self) -> None:
        mapping = load_yaml("contracts/integration/ASSET_RESULT_MAPPING.yaml")
        mapped = {
            field
            for fields in mapping["required_result_mappings"].values()
            for field in fields
        }
        schema = json.loads(
            (self.release / "contracts/schemas/asset-result-contract.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(mapped, set(schema["required"]))
        self.assertNotIn("authorization", schema["properties"])
        self.assertFalse(mapping["authority_constraints"]["result_may_grant_downstream_consumption"])

    def test_trust_boundary_remains_unsigned_and_stage5_closed(self) -> None:
        trust = self.pin["trust"]
        self.assertEqual(trust["status"], "local_unsigned_release_candidate")
        self.assertFalse(trust["production_trusted"])
        self.assertFalse(trust["implementation_authorized"])
        self.assertFalse(trust["stage5_allowed"])
        compatibility = load_yaml("contracts/integration/DELEGATION_RC2_COMPATIBILITY.yaml")
        self.assertEqual(compatibility["evaluation_claim"]["status"], "specified_not_certified")
        self.assertFalse(
            compatibility["evaluation_claim"]["production_EVALUATE_capability_claimed"]
        )


if __name__ == "__main__":
    unittest.main()
