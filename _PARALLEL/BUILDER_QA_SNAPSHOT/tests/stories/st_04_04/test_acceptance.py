from __future__ import annotations

import unittest

from cmf_builder.domain.handoff import InternalHandoffDecisionAction
from tests.stories.st_04_04 import (
    RECEIVER_AUTHORITY,
    RECEIVER_PHASE,
    SENDER_PHASE,
    build_context,
    compile_command,
    decision_command,
    governed_artifacts,
    issue_command,
)


class InternalHandoffAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, self.repository, self.observations, self.run_id, _ = build_context()
        self.compile_receipt = self.service.compile(compile_command(self.run_id))
        self.graph = self.service.get_active(self.run_id)
        self.phase_graph = self.repository.get_phase_graph(self.graph.phase_graph_id)
        assert self.phase_graph is not None

    def test_ac_01_02_compiles_exact_context_and_handoff_coverage(self) -> None:
        self.assertEqual(tuple(item.phase_ref for item in self.graph.context_graph.contexts), (
            "governed_contract_ready", "ratified_boundary_ready",
        ))
        self.assertEqual(tuple(item.contract_id for item in self.graph.contracts), (
            "ratified_boundary_to_governed_contract_v1",
        ))
        self.assertEqual(self.compile_receipt.context_count, 2)
        self.assertEqual(self.compile_receipt.contract_count, 1)
        self.assertEqual(self.compile_receipt.field_count, 2)
        self.assertEqual(self.compile_receipt.stream_version, 17)
        self.graph.validate(self.phase_graph)
        self.compile_receipt.validate(self.graph, self.phase_graph)

    def test_ac_02_preserves_complete_phase_graph_lineage(self) -> None:
        for field in (
            "run_id", "target_profile_ref", "phase_graph_id", "phase_graph_hash",
            "module_graph_id", "module_graph_hash", "capability_graph_id",
            "capability_graph_hash", "ir_id", "ir_hash", "source_lock_ref",
            "boundary_ref", "ratification_ref", "model_ref", "artifact_set_id",
            "constitutional_report_id", "constitutional_report_hash",
            "constitutional_receipt_id", "constitutional_receipt_hash",
        ):
            expected = getattr(self.phase_graph, "graph_id" if field == "phase_graph_id" else "graph_hash" if field == "phase_graph_hash" else field)
            self.assertEqual(getattr(self.graph, field), expected)

    def test_ac_03_06_owner_authority_and_context_rules_are_explicit(self) -> None:
        contexts = {item.phase_ref: item for item in self.graph.context_graph.contexts}
        self.assertEqual(contexts[SENDER_PHASE].field("source_lock_ref").owner, "cmf_builder.source_lock")
        self.assertEqual(contexts[RECEIVER_PHASE].field("constitutional_authority_ref").authority, "governing_source")
        for context in contexts.values():
            self.assertEqual(context.conditional_loads, ())
            self.assertEqual(context.unload_behavior, "DROP_NON_OUTPUT_CONTEXT_AFTER_PHASE")
            self.assertTrue(context.excluded_fields)

    def test_ac_05_issues_exact_sender_receiver_modules_and_artifacts(self) -> None:
        artifacts = governed_artifacts(self.service, self.repository, self.run_id)
        receipt = self.service.issue(issue_command(self.run_id, artifacts))
        handoff = self.repository.get_internal_handoff(receipt.handoff_id)
        assert handoff is not None
        handoff.validate(self.graph, self.phase_graph)
        receipt.validate(handoff, None)
        self.assertEqual((handoff.sender_phase, handoff.receiver_phase), (SENDER_PHASE, RECEIVER_PHASE))
        self.assertEqual((handoff.sender_module, handoff.receiver_module), ("atomic_boundary_module", "governed_contract_module"))
        self.assertEqual(tuple(item.field for item in handoff.artifacts), (
            "boundary_validation_receipt_ref", "frozen_atomic_boundary_ref",
        ))
        self.assertEqual(receipt.stream_version, 18)

    def test_ac_04_acceptance_is_attributable_and_does_not_mutate_source(self) -> None:
        artifacts = governed_artifacts(self.service, self.repository, self.run_id)
        issued = self.service.issue(issue_command(self.run_id, artifacts))
        handoff_before = self.repository.get_internal_handoff(issued.handoff_id)
        accepted = self.service.decide(decision_command(self.run_id, issued.handoff_id))
        handoff_after = self.repository.get_internal_handoff(issued.handoff_id)
        decision = self.repository.get_internal_handoff_decision(issued.handoff_id)
        assert handoff_before is not None and decision is not None
        self.assertEqual(handoff_after, handoff_before)
        self.assertEqual(decision.action, InternalHandoffDecisionAction.ACCEPTED)
        self.assertEqual(decision.receiver_authority, RECEIVER_AUTHORITY)
        accepted.validate(handoff_before, decision)
        self.assertEqual(accepted.stream_version, 19)

    def test_governed_rejection_has_typed_reason_and_no_downstream_artifact(self) -> None:
        artifacts = governed_artifacts(self.service, self.repository, self.run_id)
        issued = self.service.issue(issue_command(self.run_id, artifacts))
        rejected = self.service.decide(decision_command(
            self.run_id,
            issued.handoff_id,
            action=InternalHandoffDecisionAction.REJECTED,
            reason_code="RECEIVER_CONTRACT_REJECTED",
            reason="Receiver rejected the handoff without creating downstream state.",
        ))
        decision = self.repository.get_internal_handoff_decision(issued.handoff_id)
        handoff = self.repository.get_internal_handoff(issued.handoff_id)
        assert decision is not None and handoff is not None
        self.assertEqual(rejected.action, "REJECTED")
        self.assertEqual(decision.reason_code, "RECEIVER_CONTRACT_REJECTED")
        self.assertEqual(self.repository.internal_handoff_count, 1)
        self.assertEqual(self.repository.internal_handoff_decision_count, 1)

    def test_ac_09_11_observations_are_attributable_and_external_scope_is_absent(self) -> None:
        artifacts = governed_artifacts(self.service, self.repository, self.run_id)
        issued = self.service.issue(issue_command(self.run_id, artifacts))
        self.service.decide(decision_command(self.run_id, issued.handoff_id))
        story_observations = [item for item in self.observations.observations if item.story_id == "ST-04.04"]
        self.assertIn("ST-04.04:ContextGraphCompiled", {item.event_name for item in story_observations})
        self.assertIn("ST-04.04:InternalHandoffIssued", {item.event_name for item in story_observations})
        self.assertIn("ST-04.04:InternalHandoffAccepted", {item.event_name for item in story_observations})
        for item in story_observations:
            self.assertEqual(item.handoff_graph_id, self.graph.graph_id)
        canonical = self.graph.canonical_bytes().decode("utf-8").lower()
        for prohibited in ("vae", "delegation_runtime", "format02", "gpu", "transport", "production_publication"):
            self.assertNotIn(prohibited, canonical)


if __name__ == "__main__":
    unittest.main()
