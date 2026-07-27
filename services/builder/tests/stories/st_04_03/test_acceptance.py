from __future__ import annotations

import unittest

from cmf_builder.domain.phase_graph import PHASE_GRAPH_SCHEMA_ID, PHASE_GRAPH_SCHEMA_VERSION
from tests.stories.st_04_03 import build_context, compile_command


class PhaseGraphAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, self.repository, self.observations, self.run_id, _ = build_context()
        self.receipt = self.service.compile(compile_command(self.run_id))
        self.graph = self.service.get_active(self.run_id)
        self.parent = self.repository.get_responsibility_module_graph(self.graph.module_graph_id)
        assert self.parent is not None

    def test_ac_01_08_exact_parent_and_full_lineage_are_preserved(self) -> None:
        self.assertEqual(self.graph.module_graph_hash, self.parent.graph_hash)
        for field in (
            "run_id", "target_profile_ref", "capability_graph_id", "capability_graph_hash",
            "ir_id", "ir_hash", "source_lock_ref", "boundary_ref", "ratification_ref",
            "model_ref", "artifact_set_id", "constitutional_report_id",
            "constitutional_report_hash", "constitutional_receipt_id", "constitutional_receipt_hash",
        ):
            self.assertEqual(getattr(self.graph, field), getattr(self.parent, field))
        self.assertEqual(self.graph.modules, self.parent.modules)

    def test_ac_02_every_module_and_responsibility_is_represented_exactly_once(self) -> None:
        self.assertEqual(self.graph.phase_ids, ("governed_contract_ready", "ratified_boundary_ready"))
        self.assertEqual(tuple(sorted(self.graph.module_refs)), self.parent.module_ids)
        self.assertEqual(len(set(self.graph.module_refs)), 2)
        for phase in self.graph.phases:
            self.assertTrue(phase.responsibility)
            self.assertTrue(phase.module_refs)
            self.assertTrue(phase.entry_conditions)
            self.assertTrue(phase.exit_evidence)
            self.assertTrue(phase.failure_owner)
            self.assertTrue(phase.required_gates)

    def test_ac_03_topological_order_and_runnable_state_are_deterministic(self) -> None:
        plan = self.graph.execution_plan
        self.assertEqual(plan.topological_order, ("ratified_boundary_ready", "governed_contract_ready"))
        self.assertEqual(plan.initially_runnable, ("ratified_boundary_ready",))
        self.assertEqual(plan.blocked_by, (("governed_contract_ready", ("ratified_boundary_ready",)),))

    def test_ac_04_parallelism_is_explicit_and_never_defaulted(self) -> None:
        self.assertFalse(self.graph.default_parallelism_allowed)
        self.assertEqual(self.graph.execution_plan.parallel_pairs, ())
        self.assertTrue(all(not phase.parallel_with for phase in self.graph.phases))

    def test_ac_06_authority_failure_ownership_and_gates_are_preserved(self) -> None:
        modules = {module.module_id: module for module in self.parent.modules}
        for phase in self.graph.phases:
            owners = {modules[reference].failure_owner for reference in phase.module_refs}
            self.assertEqual(owners, {phase.failure_owner})
            self.assertGreaterEqual(len(phase.required_gates), 2)
            self.assertEqual(phase.execution_kind, "DETERMINISTIC_CODE")

    def test_ac_07_scope_is_declarative_synthetic_and_nonproduction(self) -> None:
        self.assertFalse(self.graph.implicit_phases_allowed)
        self.assertFalse(self.graph.production_eligible)
        self.assertFalse(self.graph.certified)
        joined = self.graph.canonical_bytes().decode("utf-8").lower()
        for prohibited in ("format02", "delegation_runtime", "vae_runtime", "control_tower", "workflow_ir", "execute_phase"):
            self.assertNotIn(prohibited, joined)

    def test_ac_09_11_run_receipt_and_observations_are_complete(self) -> None:
        run = self.repository.load_run(self.run_id)
        self.assertEqual(run.stream_version, 16)
        self.assertEqual(run.phase_graph_ref, self.graph.graph_id)
        self.assertEqual(run.phase_graph_hash, self.graph.graph_hash)
        self.graph.validate(self.parent)
        self.receipt.validate(self.graph, self.parent)
        self.assertEqual(self.graph.schema_id, PHASE_GRAPH_SCHEMA_ID)
        self.assertEqual(self.graph.schema_version, PHASE_GRAPH_SCHEMA_VERSION)
        observations = [item for item in self.observations.observations if item.story_id == "ST-04.03"]
        self.assertEqual(
            {item.event_name for item in observations},
            {"ST-04.03:PhaseGraphCompiled", "ST-04.03:TopologyValidated", "ST-04.03:RunnableStateDerived", "ST-04.03:ParallelismValidated", "ST-04.03:OutcomeVerified"},
        )
        for item in observations:
            self.assertEqual(item.phase_graph_id, self.graph.graph_id)
            self.assertEqual(item.phase_receipt_id, self.receipt.receipt_id)
            self.assertEqual(item.phase_count, 2)
            self.assertEqual(item.phase_module_coverage_count, 2)
            self.assertEqual(item.phase_dependency_count, 1)
            self.assertEqual(item.phase_gate_count, 4)
            self.assertEqual(item.phase_initially_runnable_count, 1)
            self.assertEqual(item.phase_blocked_count, 1)


if __name__ == "__main__":
    unittest.main()
