from __future__ import annotations

import unittest

from cmf_builder.domain.capability_ownership import (
    CAPABILITY_OWNERSHIP_SCHEMA_ID,
    CAPABILITY_OWNERSHIP_SCHEMA_VERSION,
    EXPECTED_CAPABILITIES,
    CapabilityOwnerKind,
)
from cmf_builder.domain.run import LifecycleState
from tests.stories.st_04_01 import build_context, compile_command


class CapabilityOwnershipAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            self.repository,
            self.observations,
            self.run_id,
            self.constitutional_receipt,
        ) = build_context()
        self.receipt = self.service.compile(compile_command(self.run_id))
        self.graph = self.repository.get_capability_ownership_graph(
            self.receipt.graph_id
        )
        assert self.graph is not None

    def test_ac_01_exact_active_parent_and_lineage_are_preserved(self) -> None:
        run = self.repository.load_run(self.run_id)
        report = self.repository.get_constitutional_validation_report(
            self.graph.constitutional_report_id
        )
        ir = self.repository.get_harness_ir(self.graph.ir_id)
        assert report is not None and ir is not None
        self.assertEqual(self.graph.run_id, run.run_id)
        self.assertEqual(self.graph.ir_hash, ir.ir_hash)
        self.assertEqual(self.graph.source_lock_ref, ir.source_lock_ref)
        self.assertEqual(self.graph.boundary_ref, ir.boundary_ref)
        self.assertEqual(self.graph.ratification_ref, ir.ratification_ref)
        self.assertEqual(self.graph.model_ref, ir.model_ref)
        self.assertEqual(self.graph.artifact_set_id, report.artifact_set_id)
        self.assertEqual(self.graph.constitutional_report_hash, report.report_hash)
        self.assertEqual(
            self.graph.constitutional_receipt_id,
            self.constitutional_receipt.receipt_id,
        )
        self.assertEqual(
            self.graph.constitutional_receipt_hash,
            self.constitutional_receipt.receipt_hash,
        )

    def test_ac_02_03_inventory_is_exact_unique_canonical_and_fully_owned(self) -> None:
        self.assertEqual(self.graph.capability_ids, EXPECTED_CAPABILITIES)
        self.assertEqual(len(self.graph.decisions), 3)
        self.assertEqual(len(set(self.graph.capability_ids)), 3)
        self.assertEqual(
            self.graph.owner_kind_counts,
            ((CapabilityOwnerKind.CODE.value, 3),),
        )
        self.assertTrue(all(item.owner_id for item in self.graph.decisions))

    def test_ac_04_05_06_explicit_ownership_has_authority_reliability_and_cost(self) -> None:
        for decision in self.graph.decisions:
            self.assertIs(decision.owner_kind, CapabilityOwnerKind.CODE)
            self.assertTrue(decision.owner_id.startswith("cmf_builder."))
            self.assertTrue(decision.authority_boundary)
            self.assertGreaterEqual(len(decision.reliability_evidence), 4)
            self.assertGreaterEqual(len(decision.cost_evidence), 3)
            self.assertIsNone(decision.handoff_responsibility)
            self.assertFalse(decision.ordered_participants)

    def test_ac_08_empty_registry_is_evidence_only_and_scope_stays_synthetic(self) -> None:
        self.assertFalse(self.graph.external_skills_required)
        self.assertFalse(self.graph.dynamic_skill_discovery_allowed)
        self.assertFalse(self.graph.production_eligible)
        self.assertFalse(self.graph.certified)
        self.assertIn("a4a9e5af", self.graph.empty_registry_fixture_hash)
        joined = self.graph.canonical_bytes().decode("utf-8").lower()
        for prohibited in ("discover_skills", "select_skills", "package_skills"):
            self.assertNotIn(prohibited, joined)

    def test_ac_09_run_attachment_and_receipt_are_atomic_content_addressed(self) -> None:
        run = self.repository.load_run(self.run_id)
        self.assertIs(run.lifecycle_state, LifecycleState.GENESIS)
        self.assertEqual(run.stream_version, 14)
        self.assertEqual(run.capability_ownership_ref, self.graph.graph_id)
        self.assertEqual(run.capability_ownership_hash, self.graph.graph_hash)
        self.assertIsNone(run.capability_ownership_invalidation_ref)
        self.graph.validate()
        self.receipt.validate(self.graph)
        self.assertEqual(self.repository.capability_ownership_graph_count, 1)
        self.assertEqual(self.repository.capability_ownership_receipt_count, 1)

    def test_ac_11_required_success_observations_are_complete_and_payload_free(self) -> None:
        observations = [
            item
            for item in self.observations.observations
            if item.story_id == "ST-04.01"
        ]
        names = {item.event_name for item in observations}
        self.assertEqual(
            names,
            {
                "ST-04.01:CapabilityOwnershipCompiled",
                "ST-04.01:CapabilityCoverageValidated",
                "ST-04.01:OwnershipEvidenceValidated",
                "ST-04.01:OutcomeVerified",
            },
        )
        for item in observations:
            self.assertEqual(item.capability_graph_id, self.graph.graph_id)
            self.assertEqual(item.capability_receipt_id, self.receipt.receipt_id)
            self.assertEqual(item.capability_count, 3)
            self.assertEqual(item.capability_owner_kind_counts, (("CODE", 3),))
            self.assertEqual(item.capability_reliability_coverage_count, 3)
            self.assertEqual(item.capability_cost_coverage_count, 3)
            self.assertEqual(item.constitutional_report_id, self.graph.constitutional_report_id)
            self.assertNotIn("decisions", repr(item.failure_context))

    def test_contract_identity_is_exact(self) -> None:
        self.assertEqual(self.graph.schema_id, CAPABILITY_OWNERSHIP_SCHEMA_ID)
        self.assertEqual(self.graph.schema_version, CAPABILITY_OWNERSHIP_SCHEMA_VERSION)
        self.assertTrue(self.graph.graph_id.removeprefix("capability-ownership-graph_") in self.graph.graph_hash)
        self.assertTrue(self.receipt.receipt_id.removeprefix("capability-ownership-receipt_") in self.receipt.receipt_hash)


if __name__ == "__main__":
    unittest.main()
