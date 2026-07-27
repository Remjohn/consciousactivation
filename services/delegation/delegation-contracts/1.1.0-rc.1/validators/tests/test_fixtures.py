from __future__ import annotations

import hashlib
import json
import unittest

from cmf_delegation_validators.authority import AuthorityError, validate_authority
from cmf_delegation_validators.contracts import load_registry, validate_payload
from cmf_delegation_validators.paths import FIXTURES_ROOT, ROOT


class FixtureTests(unittest.TestCase):
    EXPECTED_SCENARIOS = {
        "SCN-01": "Successful single character asset",
        "SCN-02": "Atomic multi-asset Delegation Set",
        "SCN-03": "In-flight demand supersession",
        "SCN-04": "Budget escalation and approval",
        "SCN-05": "Constraint conflict and amendment",
        "SCN-06": "Safe cancellation",
        "SCN-07": "Result invalidation and replacement",
        "SCN-08": "Authority violation rejection",
        "SCN-09": "Compatibility migration",
        "SCN-10": "Replay and out-of-order resilience",
    }

    def test_format02_manifest_hashes_and_message_references(self) -> None:
        manifest = json.loads(
            (FIXTURES_ROOT / "format02" / "manifest.json").read_text(encoding="utf-8")
        )
        known_messages = {item["message_type"] for item in load_registry()["messages"]}
        self.assertEqual(len(manifest["scenarios"]), 10)
        for item in manifest["scenarios"]:
            path = ROOT / item["path"]
            actual_hash = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(actual_hash, item["hash"])
            scenario = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(scenario["title"], self.EXPECTED_SCENARIOS[scenario["scenario_id"]])
            for message in scenario["message_sequence"]:
                self.assertIn(message["message_type"], known_messages)
                fixture_path = ROOT / message["fixture_ref"]
                self.assertTrue(fixture_path.is_file())
                fixture_hash = "sha256:" + hashlib.sha256(fixture_path.read_bytes()).hexdigest()
                self.assertEqual(fixture_hash, message["fixture_hash"])
                payload = json.loads(fixture_path.read_text(encoding="utf-8"))
                validate_payload(message["message_type"], payload)
                if message["expected_disposition"] == "REJECTED":
                    with self.assertRaises(AuthorityError):
                        validate_authority(
                            message["message_type"],
                            message["principal_type"],
                            payload,
                        )
                else:
                    validate_authority(
                        message["message_type"],
                        message["principal_type"],
                        payload,
                    )
            audit = scenario["assertions"]["audit"]["expected_sequence"]
            outbox = scenario["assertions"]["outbox"]["expected_deliveries"]
            self.assertEqual(len(audit), len(scenario["message_sequence"]))
            self.assertEqual(
                len(outbox),
                len(
                    [
                        message
                        for message in scenario["message_sequence"]
                        if message["expected_disposition"] != "IDEMPOTENT_REPLAY"
                    ]
                ),
            )
            self.assertTrue(
                all(not delivery["duplicate_domain_effect_allowed"] for delivery in outbox)
            )
            if scenario["scenario_id"] == "SCN-02":
                self.assertEqual(len(scenario["member_correlations"]), 3)
            else:
                self.assertEqual(len(scenario["member_correlations"]), 1)

    def test_format02_portfolio_has_all_mandatory_assertion_families(self) -> None:
        required = {
            "authority",
            "identity",
            "audit",
            "outbox",
            "effect_counts",
            "projection",
            "prohibited_effects",
            "negative_variants",
            "race_variants",
        }
        for scenario_id in self.EXPECTED_SCENARIOS:
            scenario = json.loads(
                (FIXTURES_ROOT / "format02" / "scenarios" / f"{scenario_id}.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertTrue(required.issubset(scenario["assertions"]))
            for assertion_name in required:
                self.assertTrue(scenario["assertions"][assertion_name])
            self.assertTrue(scenario["assertions"]["audit"]["receipt_chain_required"])
            self.assertTrue(
                scenario["assertions"]["outbox"]["accepted_effects_publish_after_atomic_commit"]
            )

    def test_constitutional_scenarios_carry_executable_assertions(self) -> None:
        expected = {"SCN-01", "SCN-02", "SCN-05", "SCN-08", "SCN-09", "SCN-10"}
        for scenario_id in self.EXPECTED_SCENARIOS:
            scenario = json.loads(
                (FIXTURES_ROOT / "format02" / "scenarios" / f"{scenario_id}.json").read_text(
                    encoding="utf-8"
                )
            )
            if scenario_id in expected:
                self.assertTrue(scenario["assertions"]["constitutional"])
            else:
                self.assertNotIn("constitutional", scenario["assertions"])

    def test_constitutional_compatibility_fixtures_are_manifested_inputs(self) -> None:
        root = FIXTURES_ROOT / "compatibility" / "constitutional"
        expected_files = {
            "expression-moment-drop.invalid.json",
            "wrong-reading-unsupported.invalid.json",
            "aip-lineage.source.json",
            "aip-lineage.expected.json",
            "evaluator-gap.invalid.json",
        }
        self.assertEqual({path.name for path in root.glob("*.json")}, expected_files)

    def test_delegation_set_fixture_has_three_independent_members(self) -> None:
        registry = load_registry()
        entry = next(item for item in registry["messages"] if item["message_type"] == "delegation-set")
        payload = json.loads((ROOT / entry["example_path"]).read_text(encoding="utf-8"))
        members = payload["member_demands"]
        self.assertEqual(len(members), 3)
        self.assertEqual(len({member["request_id"] for member in members}), 3)
        self.assertEqual(payload["minimum_completed"], 3)


if __name__ == "__main__":
    unittest.main()
