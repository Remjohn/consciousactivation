from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import ValidationError

from cmf_delegation_validators.canonical import canonical_hash
from cmf_delegation_validators.contracts import (
    load_registry,
    load_schema,
    validate_all_examples,
    validate_closed_schemas,
    validate_payload,
    validate_release_manifest,
)
from cmf_delegation_validators.paths import ROOT


class ContractSchemaTests(unittest.TestCase):
    def test_all_registered_examples_validate(self) -> None:
        self.assertEqual(validate_all_examples(), 26)

    def test_all_public_objects_are_closed(self) -> None:
        validate_closed_schemas()

    def test_registry_has_unique_pinned_schema_ids(self) -> None:
        registry = load_registry()
        self.assertEqual(registry["package_version"], "1.1.0-rc.1")
        message_types = [item["message_type"] for item in registry["messages"]]
        schema_ids = [item["schema_id"] for item in registry["messages"]]
        self.assertEqual(len(message_types), len(set(message_types)))
        self.assertEqual(len(schema_ids), len(set(schema_ids)))
        for item in registry["messages"]:
            expected_version = "1.1" if item["message_type"] == "visual-asset-demand" else "1.0"
            self.assertTrue(
                item["schema_id"].endswith(
                    f"/{item['message_type']}/{expected_version}/schema.json"
                )
            )

    def test_legacy_submission_receipt_is_not_an_active_contract(self) -> None:
        message_types = {item["message_type"] for item in load_registry()["messages"]}
        self.assertNotIn("submission-receipt", message_types)
        self.assertIn("submission-validation-receipt", message_types)
        self.assertIn("admission-receipt", message_types)

    def test_result_cannot_grant_downstream_consumption(self) -> None:
        result_schema = load_schema("asset-result-contract")
        acknowledgement_schema = load_schema("result-acknowledgement")
        self.assertNotIn("authorization", result_schema["properties"])
        self.assertIn("consumption_authorized", acknowledgement_schema["properties"])

    def test_unknown_payload_field_is_rejected(self) -> None:
        entry = next(
            item for item in load_registry()["messages"] if item["message_type"] == "visual-asset-submission"
        )
        payload = json.loads((ROOT / entry["example_path"]).read_text(encoding="utf-8"))
        invalid = copy.deepcopy(payload)
        invalid["unexpected"] = True
        with self.assertRaises(ValidationError):
            validate_payload("visual-asset-submission", invalid)

    def test_every_example_is_canonical_hashable(self) -> None:
        for item in load_registry()["messages"]:
            payload = json.loads((ROOT / item["example_path"]).read_text(encoding="utf-8"))
            self.assertRegex(canonical_hash(payload), r"^sha256:[0-9a-f]{64}$")

    def test_demand_identity_is_exact_and_versioned(self) -> None:
        demand_ref = load_schema("visual-asset-submission")["$defs"]["DemandIdentityRef"]
        self.assertEqual(
            set(demand_ref["required"]),
            {"request_id", "version", "payload_hash", "canonical_ref"},
        )
        self.assertFalse(demand_ref["additionalProperties"])

    def test_visual_asset_demand_is_constitution_complete_and_closed(self) -> None:
        schema = load_schema("visual-asset-demand")
        required = set(schema["required"])
        self.assertTrue(
            {
                "activative_semantic_lineage",
                "activation_contract",
                "visual_semantic_pack",
                "visual_narrative_program",
                "feature_contracts",
                "somatic_route_request",
                "wrong_reading_locks",
            }.issubset(required)
        )
        self.assertEqual(schema["x-cmf-message-version"], "1.1")
        self.assertEqual(schema["properties"]["wrong_reading_locks"]["minItems"], 1)
        self.assertFalse(schema["additionalProperties"])
        for legacy_alias in ("activative_intent", "wrongness_locks", "composition"):
            self.assertNotIn(legacy_alias, schema["properties"])

    def test_constitutional_lineage_uses_exact_resource_identity_refs(self) -> None:
        schema = load_schema("visual-asset-demand")
        lineage = schema["properties"]["activative_semantic_lineage"]
        self.assertTrue(
            {
                "activative_call_refs",
                "reaction_receipt_refs",
                "expression_moment_refs",
            }.issubset(lineage["required"])
        )
        resource_ref = schema["$defs"]["ResourceIdentityRef"]
        self.assertEqual(
            set(resource_ref["required"]),
            {"resource_id", "version", "payload_hash", "canonical_ref"},
        )
        self.assertFalse(resource_ref["additionalProperties"])

    def test_release_manifest_pins_all_stage3_package_files(self) -> None:
        self.assertGreater(validate_release_manifest(), 75)


if __name__ == "__main__":
    unittest.main()
