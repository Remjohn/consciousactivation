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
WORKSPACE_ROOT = REPO_ROOT.parent
PIN_PATH = REPO_ROOT / "contracts/integration/DELEGATION_CONTRACT_PIN.yaml"
COMPATIBILITY_PATH = REPO_ROOT / "contracts/integration/DELEGATION_RC4_COMPATIBILITY.yaml"
FIXTURE_PATH = REPO_ROOT / "validation/fixtures/delegation-rc4/VAE_RC4_BOUNDARY_CASES.json"
ALIAS_PATH = WORKSPACE_ROOT / "CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/FORMAT02_PROFILE_ALIAS_REGISTRY.yaml"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class DelegationRC4IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pin = load_yaml(PIN_PATH)
        cls.compatibility = load_yaml(COMPATIBILITY_PATH)
        cls.fixture = load_json(FIXTURE_PATH)
        cls.release = Path(cls.pin["package"]["release_path"])
        sys.path.insert(0, str(cls.release / "validators"))
        from cmf_delegation_validators.compatibility import (
            CompatibilityError,
            migrate_pre_discriminator_visual_asset_demand,
            negotiate,
            validate_derivative_lock_adapter,
            validate_visual_asset_demand_adapter,
        )
        from cmf_delegation_validators.contracts import validate_payload
        from cmf_delegation_validators.derivative_locks import validate_derivative_lock_inheritance

        cls.CompatibilityError = CompatibilityError
        cls.migrate_pre_discriminator_visual_asset_demand = staticmethod(migrate_pre_discriminator_visual_asset_demand)
        cls.negotiate = staticmethod(negotiate)
        cls.validate_derivative_lock_adapter = staticmethod(validate_derivative_lock_adapter)
        cls.validate_visual_asset_demand_adapter = staticmethod(validate_visual_asset_demand_adapter)
        cls.validate_payload = staticmethod(validate_payload)
        cls.validate_derivative_lock_inheritance = staticmethod(validate_derivative_lock_inheritance)
        cls.demand = load_json(cls.release / "contracts/examples/visual-asset-demand.example.json")

    def test_exact_rc4_release_and_hashes(self) -> None:
        integrity = self.pin["integrity"]
        receipt_path = self.release / integrity["release_receipt"]["path"]
        manifest_path = self.release / integrity["release_manifest"]["path"]
        receipt = load_json(receipt_path)
        self.assertEqual(self.pin["package"]["package_version"], "1.1.0-rc.4")
        self.assertEqual(receipt["release_digest"], integrity["release_digest"])
        self.assertEqual(sha256(receipt_path), integrity["release_receipt"]["sha256"])
        self.assertEqual(sha256(manifest_path), integrity["release_manifest"]["sha256"])

    def test_receipt_declares_exact_163_file_set(self) -> None:
        receipt = load_json(self.release / "RELEASE_RECEIPT.json")
        self.assertEqual(len(receipt["files"]), 163)
        actual = {path.relative_to(self.release).as_posix() for path in self.release.rglob("*") if path.is_file() and path.name != "RELEASE_RECEIPT.json" and "__pycache__" not in path.parts and ".pytest_cache" not in path.parts}
        self.assertEqual(actual, {item["path"] for item in receipt["files"]})
        for item in receipt["files"]:
            path = self.release / item["path"]
            self.assertEqual(path.stat().st_size, item["bytes"])
            self.assertEqual(sha256(path), item["sha256"])

    def test_rc3_to_rc4_difference_is_portable_derivative_contract(self) -> None:
        rc3 = WORKSPACE_ROOT / "CMF_PROGRAM_CONTROL/02_CROSS_REPO_CONTRACTS/delegation-contracts/1.1.0-rc.3"
        self.assertEqual(sha256(rc3 / "contracts/schemas/visual-asset-demand.schema.json"), sha256(self.release / "contracts/schemas/visual-asset-demand.schema.json"))
        self.assertTrue((self.release / "contracts/schemas/derivative-lock-inheritance.schema.json").is_file())
        self.assertEqual(self.fixture["expected_semantic_change"], "portable_derivative_lock_inheritance_contract_and_enforcement")

    def test_source_kind_and_interview_provenance_remain_enforced(self) -> None:
        self.validate_payload("visual-asset-demand", self.demand)
        invalid = copy.deepcopy(self.demand)
        invalid["source_provenance"]["source_kind"] = "guessed_source"
        with self.assertRaises(ValidationError):
            self.validate_payload("visual-asset-demand", invalid)
        for field in ("reaction_receipt_refs", "expression_moment_refs"):
            invalid = copy.deepcopy(self.demand)
            invalid["activative_semantic_lineage"][field] = []
            with self.assertRaises(ValidationError):
                self.validate_payload("visual-asset-demand", invalid)

    def test_existing_request_mapping_remains_lossless(self) -> None:
        mapping = load_yaml(REPO_ROOT / "contracts/integration/VISUAL_ASSET_DEMAND_REQUEST_MAPPING.yaml")
        self.assertEqual(mapping["source_release"], "delegation-contracts@1.1.0-rc.4")
        self.assertEqual(set(mapping["preserved_top_level_fields"]), set(self.demand))
        self.assertEqual(self.validate_visual_asset_demand_adapter(self.demand, copy.deepcopy(self.demand)), self.demand)

    def test_vae_declares_evaluate_for_every_rc4_required_domain(self) -> None:
        manifest = load_json(self.release / "compatibility/manifest.json")
        required = {item["domain"]: set(item["required_modes"]) for item in manifest["required_semantic_domains"]}
        claims = self.compatibility["semantic_capabilities"]
        for domain, modes in required.items():
            self.assertTrue(modes.issubset(set(claims[domain]["support_modes"])), domain)
            if "EVALUATE" in modes:
                self.assertTrue(claims[domain]["evaluator_profile_refs"], domain)

    def test_rc4_compatibility_negotiation_passes_with_vae_capabilities(self) -> None:
        requester = load_json(self.release / "compatibility/manifest.json")
        provider = copy.deepcopy(requester)
        provider["semantic_capabilities"] = [dict({"domain": domain, "feature_contract_families": []}, **claim) for domain, claim in self.compatibility["semantic_capabilities"].items()]
        provider["derivative_asset_flows"] = self.compatibility["derivative_asset_flows"]
        negotiated = self.negotiate(requester, provider)
        self.assertEqual(negotiated["behavioral_enforcement"], "PASS")

    def test_unsupported_evaluation_profile_requirement_is_rejected(self) -> None:
        supported = {self.compatibility["capability_claim"]["supported_profile"]}
        requested = self.fixture["evaluation"]["unsupported_profile"]
        with self.assertRaises(self.CompatibilityError):
            if requested not in supported:
                raise self.CompatibilityError("UNSUPPORTED_EVALUATION_PROFILE")

    def test_rc4_derivative_inheritance_accepts_only_valid_relationships(self) -> None:
        root = self.release / "fixtures/compatibility/derivative-locks"
        for name in self.fixture["derivative_cases"]["accept"]:
            self.assertEqual(self.validate_derivative_lock_inheritance(load_json(root / name))["status"], "LOCK_INHERITANCE_VALID", name)
        for name, expected in self.fixture["derivative_cases"]["reject"].items():
            self.assertEqual(self.validate_derivative_lock_inheritance(load_json(root / name))["status"], expected, name)

    def test_derivative_adapter_preserves_parent_evidence_exactly(self) -> None:
        source = load_json(self.release / "contracts/examples/derivative-lock-inheritance.example.json")
        self.assertEqual(self.validate_derivative_lock_adapter(source, copy.deepcopy(source)), source)
        changed = copy.deepcopy(source)
        changed["parent_lock_evidence"]["parent_lock_set_hash"] = "sha256:" + "0" * 64
        with self.assertRaises(self.CompatibilityError):
            self.validate_derivative_lock_adapter(source, changed)

    def test_capability_does_not_claim_evaluator_or_production_certification(self) -> None:
        claim = self.compatibility["capability_claim"]
        self.assertTrue(claim["EVALUATE_declared_where_RC4_requires"])
        self.assertTrue(claim["capability_contract_compatible"])
        self.assertEqual(claim["evaluator_status"], "specified_not_certified")
        self.assertFalse(claim["production_certification"])
        self.assertFalse(claim["capability_presence_implies_certification"])

    def test_format02_uses_shared_canonical_alias_registry(self) -> None:
        alias = load_yaml(ALIAS_PATH)
        declared = self.compatibility["format_profile_alias_registry"]
        self.assertEqual(sha256(ALIAS_PATH), declared["sha256"])
        self.assertEqual(alias["canonical_profile_id"], self.fixture["format_profile"]["canonical_id"])
        self.assertEqual(alias["certification_state"]["strongest_current_state"], "contract_compatible")
        self.assertFalse(alias["certification_state"]["production_certified"])

    def test_result_mapping_targets_rc4_and_cannot_authorize_consumption(self) -> None:
        mapping = load_yaml(REPO_ROOT / "contracts/integration/ASSET_RESULT_MAPPING.yaml")
        self.assertEqual(mapping["target_release"], "delegation-contracts@1.1.0-rc.4")
        self.assertFalse(mapping["authority_constraints"]["result_may_grant_downstream_consumption"])

    def test_unsigned_trust_and_stage5_gate_remain_closed(self) -> None:
        trust = self.pin["trust"]
        self.assertEqual(trust["status"], "local_unsigned_release_candidate")
        self.assertFalse(trust["production_eligible"])
        self.assertFalse(trust["implementation_authorized"])
        self.assertFalse(trust["stage5_allowed"])


if __name__ == "__main__":
    unittest.main()
