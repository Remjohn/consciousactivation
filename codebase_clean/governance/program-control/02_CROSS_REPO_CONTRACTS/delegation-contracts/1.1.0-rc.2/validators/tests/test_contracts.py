from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import ValidationError

from cmf_delegation_validators.canonical import canonical_hash
from cmf_delegation_validators.contracts import (
    _is_transient,
    load_registry,
    load_schema,
    validate_all_examples,
    validate_closed_schemas,
    validate_payload,
    validate_release_manifest,
    validate_release_receipt,
)
from cmf_delegation_validators.paths import LAYOUT, ROOT


class ContractSchemaTests(unittest.TestCase):
    def test_all_registered_examples_validate(self) -> None:
        self.assertEqual(validate_all_examples(), 26)

    def test_all_public_objects_are_closed(self) -> None:
        validate_closed_schemas()

    def test_registry_has_unique_pinned_schema_ids(self) -> None:
        registry = load_registry()
        self.assertEqual(registry["package_version"], "1.1.0-rc.2")
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
                "source_provenance",
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
        self.assertIn("activative_call_refs", lineage["required"])
        self.assertNotIn("reaction_receipt_refs", lineage["required"])
        self.assertNotIn("expression_moment_refs", lineage["required"])
        self.assertEqual(lineage["properties"]["reaction_receipt_refs"]["minItems"], 1)
        self.assertEqual(lineage["properties"]["expression_moment_refs"]["minItems"], 1)
        resource_ref = schema["$defs"]["ResourceIdentityRef"]
        self.assertEqual(
            set(resource_ref["required"]),
            {"resource_id", "version", "payload_hash", "canonical_ref"},
        )
        self.assertFalse(resource_ref["additionalProperties"])

    def test_release_manifest_pins_all_stage3_package_files(self) -> None:
        self.assertGreater(validate_release_manifest(), 75)

    def test_source_kind_is_mandatory_typed_and_closed(self) -> None:
        entry = next(
            item for item in load_registry()["messages"] if item["message_type"] == "visual-asset-demand"
        )
        payload = json.loads((ROOT / entry["example_path"]).read_text(encoding="utf-8"))
        self.assertEqual(payload["source_provenance"]["source_kind"], "interview_expression")
        missing = copy.deepcopy(payload)
        missing.pop("source_provenance")
        with self.assertRaises(ValidationError):
            validate_payload("visual-asset-demand", missing)
        unknown = copy.deepcopy(payload)
        unknown["source_provenance"]["source_kind"] = "free_form_guess"
        with self.assertRaises(ValidationError):
            validate_payload("visual-asset-demand", unknown)
        extra = copy.deepcopy(payload)
        extra["source_provenance"]["untyped_note"] = "not allowed"
        with self.assertRaises(ValidationError):
            validate_payload("visual-asset-demand", extra)

    def test_interview_expression_requires_non_empty_reaction_and_expression_refs(self) -> None:
        entry = next(
            item for item in load_registry()["messages"] if item["message_type"] == "visual-asset-demand"
        )
        payload = json.loads((ROOT / entry["example_path"]).read_text(encoding="utf-8"))
        for field in ("reaction_receipt_refs", "expression_moment_refs"):
            missing = copy.deepcopy(payload)
            missing["activative_semantic_lineage"].pop(field)
            with self.assertRaises(ValidationError):
                validate_payload("visual-asset-demand", missing)
            empty = copy.deepcopy(payload)
            empty["activative_semantic_lineage"][field] = []
            with self.assertRaises(ValidationError):
                validate_payload("visual-asset-demand", empty)
            empty_string = copy.deepcopy(payload)
            empty_string["activative_semantic_lineage"][field][0]["resource_id"] = ""
            with self.assertRaises(ValidationError):
                validate_payload("visual-asset-demand", empty_string)

    def test_non_interview_source_does_not_require_interview_refs_but_validates_them_if_supplied(self) -> None:
        entry = next(
            item for item in load_registry()["messages"] if item["message_type"] == "visual-asset-demand"
        )
        payload = json.loads((ROOT / entry["example_path"]).read_text(encoding="utf-8"))
        payload["source_provenance"]["source_kind"] = "authored_source"
        without_interview_refs = copy.deepcopy(payload)
        without_interview_refs["activative_semantic_lineage"].pop("reaction_receipt_refs")
        without_interview_refs["activative_semantic_lineage"].pop("expression_moment_refs")
        validate_payload("visual-asset-demand", without_interview_refs)
        for field in ("reaction_receipt_refs", "expression_moment_refs"):
            invalid = copy.deepcopy(payload)
            invalid["activative_semantic_lineage"][field] = []
            with self.assertRaises(ValidationError):
                validate_payload("visual-asset-demand", invalid)

    def test_generated_bindings_expose_governed_source_kind(self) -> None:
        python_types = (ROOT / "contracts/generated/python/cmf_delegation_contracts/types.py").read_text(
            encoding="utf-8"
        )
        typescript_types = (ROOT / "contracts/generated/typescript/index.ts").read_text(
            encoding="utf-8"
        )
        for value in ("interview_expression", "legacy_migrated"):
            self.assertIn(value, python_types)
            self.assertIn(value, typescript_types)
        self.assertIn("source_provenance: SourceProvenance", python_types)
        self.assertIn("source_provenance: SourceProvenance", typescript_types)

    def test_release_receipt_is_exact_when_running_from_release_layout(self) -> None:
        if LAYOUT == "RELEASE":
            self.assertGreater(validate_release_receipt(), 75)

    def test_transient_and_cache_paths_are_forbidden_from_manifests(self) -> None:
        for relative_path in (
            "validators/.pytest_cache/v/cache/nodeids",
            "protocol/__pycache__/engine.cpython-312.pyc",
            "contracts/examples/draft.tmp",
            "fixtures/.DS_Store",
            "Thumbs.db",
        ):
            self.assertTrue(_is_transient(relative_path))
        manifest_name = "release-manifest.json" if LAYOUT == "RELEASE" else "source-manifest.json"
        manifest = json.loads((ROOT / "contracts" / manifest_name).read_text(encoding="utf-8"))
        self.assertFalse(any(_is_transient(item["path"]) for item in manifest["files"]))


if __name__ == "__main__":
    unittest.main()
