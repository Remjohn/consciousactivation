from __future__ import annotations

import json
import unittest

from cmf_delegation_validators.lifecycle import (
    LifecycleError,
    load_lifecycle,
    transition,
    validate_sequence,
)
from cmf_delegation_validators.paths import FIXTURES_ROOT, ROOT


NORMATIVE_STATES = {
    "DRAFT",
    "SUBMITTED",
    "REJECTED",
    "ACCEPTED",
    "IN_PROGRESS",
    "RESULT_READY",
    "RESULT_REJECTED",
    "COMPLETED",
    "AMENDMENT_REQUIRED",
    "SUPERSEDED",
    "COST_APPROVAL_REQUIRED",
    "CAPABILITY_GAP",
    "HUMAN_REVIEW_REQUIRED",
    "CANCELLATION_REQUESTED",
    "CANCELLED",
    "PARTIAL_RESULT_READY",
    "INVALIDATED",
    "REVOKED",
    "REPLACED",
}


class LifecycleTests(unittest.TestCase):
    def test_every_declared_transition_is_executable(self) -> None:
        transitions = load_lifecycle()["transitions"]
        keys = set()
        for item in transitions:
            key = (item["from_state"], item["trigger"], item["principal_type"])
            self.assertNotIn(key, keys)
            keys.add(key)
            self.assertEqual(
                transition(item["from_state"], item["trigger"], item["principal_type"]),
                item["to_state"],
            )

    def test_illegal_and_wrong_authority_transitions_fail(self) -> None:
        with self.assertRaises(LifecycleError):
            transition("DRAFT", "result_declared", "VISUAL_ASSET_EDITOR")
        with self.assertRaises(LifecycleError):
            transition("RESULT_READY", "result_accepted", "VISUAL_ASSET_EDITOR")

    def test_all_format02_lifecycle_sequences_are_contiguous(self) -> None:
        manifest = json.loads(
            (FIXTURES_ROOT / "format02" / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["scenario_count"], 10)
        for item in manifest["scenarios"]:
            scenario = json.loads((ROOT / item["path"]).read_text(encoding="utf-8"))
            terminal = (
                validate_sequence(scenario["lifecycle_sequence"])
                if scenario["lifecycle_sequence"]
                else scenario["expected_initial_state"]
            )
            self.assertEqual(terminal, scenario["expected_terminal_state"])

    def test_normative_state_universe_is_exact(self) -> None:
        lifecycle = load_lifecycle()
        observed = {
            state
            for item in lifecycle["transitions"]
            for state in (item["from_state"], item["to_state"])
        }
        self.assertEqual(observed, NORMATIVE_STATES)
        self.assertEqual(
            set(lifecycle["terminal_states"]),
            {"REJECTED", "SUPERSEDED", "CANCELLED", "COMPLETED", "INVALIDATED", "REVOKED", "REPLACED"},
        )

    def test_normative_transition_expansion_has_required_branches(self) -> None:
        transitions = {
            (item["from_state"], item["trigger"], item["to_state"], item["principal_type"])
            for item in load_lifecycle()["transitions"]
        }
        self.assertEqual(len(transitions), 44)
        required = {
            ("DRAFT", "submission_validation_accepted", "SUBMITTED", "DELEGATION_PROTOCOL"),
            ("SUBMITTED", "admission_accepted", "ACCEPTED", "VISUAL_ASSET_EDITOR"),
            ("ACCEPTED", "amendment_proposed", "AMENDMENT_REQUIRED", "VISUAL_ASSET_EDITOR"),
            ("IN_PROGRESS", "budget_escalation_requested", "COST_APPROVAL_REQUIRED", "VISUAL_ASSET_EDITOR"),
            ("COST_APPROVAL_REQUIRED", "budget_escalation_denied", "CAPABILITY_GAP", "CONTENT_HARNESS"),
            ("ACCEPTED", "human_review_requested", "HUMAN_REVIEW_REQUIRED", "VISUAL_ASSET_EDITOR"),
            ("IN_PROGRESS", "partial_result_declared", "PARTIAL_RESULT_READY", "VISUAL_ASSET_EDITOR"),
            ("RESULT_READY", "result_rejected", "RESULT_REJECTED", "CONTENT_HARNESS"),
            ("RESULT_REJECTED", "revalidation_started", "IN_PROGRESS", "VISUAL_ASSET_EDITOR"),
            ("SUBMITTED", "cancellation_requested", "CANCELLATION_REQUESTED", "CONTENT_HARNESS"),
            ("CANCELLATION_REQUESTED", "cancellation_receipted", "CANCELLED", "VISUAL_ASSET_EDITOR"),
            ("AMENDMENT_REQUIRED", "demand_superseded", "SUPERSEDED", "CONTENT_HARNESS"),
            ("COMPLETED", "result_invalidated", "INVALIDATED", "CONTENT_HARNESS"),
            ("COMPLETED", "result_revoked", "REVOKED", "VISUAL_ASSET_EDITOR"),
            ("INVALIDATED", "replacement_acknowledged", "REPLACED", "CONTENT_HARNESS"),
        }
        self.assertTrue(required.issubset(transitions))

    def test_every_absent_state_trigger_principal_triple_is_rejected(self) -> None:
        transitions = load_lifecycle()["transitions"]
        declared = {
            (item["from_state"], item["trigger"], item["principal_type"])
            for item in transitions
        }
        triggers = {item["trigger"] for item in transitions}
        principals = {
            "CONTENT_HARNESS",
            "DELEGATION_PROTOCOL",
            "VISUAL_ASSET_EDITOR",
            "CONTROL_TOWER",
        }
        checked = 0
        for state in NORMATIVE_STATES:
            for trigger in triggers:
                for principal_type in principals:
                    if (state, trigger, principal_type) in declared:
                        continue
                    with self.assertRaises(LifecycleError):
                        transition(state, trigger, principal_type)
                    checked += 1
        self.assertGreater(checked, 2000)

    def test_non_contiguous_sequence_fails(self) -> None:
        sequence = [
            {
                "from_state": "DRAFT",
                "trigger": "submission_validation_accepted",
                "to_state": "SUBMITTED",
                "principal_type": "DELEGATION_PROTOCOL",
            },
            {
                "from_state": "IN_PROGRESS",
                "trigger": "result_declared",
                "to_state": "RESULT_READY",
                "principal_type": "VISUAL_ASSET_EDITOR",
            },
        ]
        with self.assertRaises(LifecycleError):
            validate_sequence(sequence)


if __name__ == "__main__":
    unittest.main()
