from __future__ import annotations

import copy
import json
import unittest

from cmf_delegation_validators.authority import (
    AuthorityError,
    load_authority_registry,
    resolve_value_owner,
    validate_authority,
)
from cmf_delegation_validators.contracts import load_registry
from cmf_delegation_validators.paths import ROOT


PRINCIPALS = {
    "CONTENT_HARNESS",
    "DELEGATION_PROTOCOL",
    "VISUAL_ASSET_EDITOR",
    "CONTROL_TOWER",
}


class AuthorityTests(unittest.TestCase):
    def test_each_registered_producer_is_authorized(self) -> None:
        registry = load_registry()
        for item in load_authority_registry()["messages"]:
            contract = next(
                entry for entry in registry["messages"] if entry["message_type"] == item["message_type"]
            )
            payload = json.loads((ROOT / contract["example_path"]).read_text(encoding="utf-8"))
            for principal_type in item["allowed_producers"]:
                candidate = copy.deepcopy(payload)
                if item["message_type"] == "delegation-envelope":
                    principal_ref = {
                        "principal_id": principal_type.lower().replace("_", "-"),
                        "principal_type": principal_type,
                        "product_version": "1.0",
                    }
                    candidate["sender"] = principal_ref
                    candidate["authority"]["principal"] = principal_ref
                    candidate["integrity"]["signer"] = principal_ref
                if item["message_type"] == "delegation-failure":
                    candidate["detecting_principal"] = {
                        "principal_id": principal_type.lower().replace("_", "-"),
                        "principal_type": principal_type,
                        "product_version": "1.0",
                    }
                validate_authority(item["message_type"], principal_type, candidate)

    def test_every_authority_entry_has_exact_non_wildcard_paths(self) -> None:
        for item in load_authority_registry()["messages"]:
            paths = item["value_owner_by_path"]
            self.assertGreater(len(paths), 0)
            self.assertNotIn("/*", paths)
            self.assertTrue(all("*" not in path for path in paths))
            self.assertTrue(all(owner in PRINCIPALS | {"SIGNING_PRINCIPAL"} for owner in paths.values()))

    def test_unknown_value_path_fails_closed(self) -> None:
        with self.assertRaises(AuthorityError):
            resolve_value_owner("visual-asset-demand", "/not_registered")

    def test_single_owner_messages_reject_other_principals(self) -> None:
        for item in load_authority_registry()["messages"]:
            allowed = set(item["allowed_producers"])
            denied = PRINCIPALS - allowed
            for principal_type in denied:
                with self.assertRaises(AuthorityError):
                    validate_authority(item["message_type"], principal_type)

    def test_protocol_owns_validation_and_editor_owns_admission(self) -> None:
        validate_authority("submission-validation-receipt", "DELEGATION_PROTOCOL")
        validate_authority("admission-receipt", "VISUAL_ASSET_EDITOR")
        with self.assertRaises(AuthorityError):
            validate_authority("submission-validation-receipt", "VISUAL_ASSET_EDITOR")
        with self.assertRaises(AuthorityError):
            validate_authority("admission-receipt", "DELEGATION_PROTOCOL")

    def test_only_content_harness_acknowledges_results(self) -> None:
        validate_authority("result-acknowledgement", "CONTENT_HARNESS")
        with self.assertRaises(AuthorityError):
            validate_authority("result-acknowledgement", "VISUAL_ASSET_EDITOR")

    def test_governance_fact_owners_match_stage2(self) -> None:
        expected = {
            "amendment-proposal": "VISUAL_ASSET_EDITOR",
            "amendment-response": "CONTENT_HARNESS",
            "selective-invalidation-receipt": "VISUAL_ASSET_EDITOR",
            "revocation-notice": "VISUAL_ASSET_EDITOR",
            "replacement-notice": "VISUAL_ASSET_EDITOR",
        }
        for message_type, principal_type in expected.items():
            validate_authority(message_type, principal_type)
            for denied in PRINCIPALS - {principal_type}:
                with self.assertRaises(AuthorityError):
                    validate_authority(message_type, denied)

    def test_result_forbidden_authorization_path_is_detected(self) -> None:
        entry = next(
            item for item in load_registry()["messages"] if item["message_type"] == "asset-result-contract"
        )
        payload = json.loads((ROOT / entry["example_path"]).read_text(encoding="utf-8"))
        invalid = copy.deepcopy(payload)
        invalid["authorization"] = {"downstream_consumption_authorized": True}
        with self.assertRaises(AuthorityError):
            validate_authority("asset-result-contract", "VISUAL_ASSET_EDITOR", invalid)

    def test_envelope_signing_identity_must_be_consistent(self) -> None:
        entry = next(
            item for item in load_registry()["messages"] if item["message_type"] == "delegation-envelope"
        )
        payload = json.loads((ROOT / entry["example_path"]).read_text(encoding="utf-8"))
        validate_authority("delegation-envelope", "CONTENT_HARNESS", payload)
        invalid = copy.deepcopy(payload)
        invalid["integrity"]["signer"]["principal_type"] = "VISUAL_ASSET_EDITOR"
        with self.assertRaises(AuthorityError):
            validate_authority("delegation-envelope", "CONTENT_HARNESS", invalid)


if __name__ == "__main__":
    unittest.main()
