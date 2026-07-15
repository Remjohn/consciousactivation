from __future__ import annotations

import unittest

from cmf_builder.domain.capability_ownership import EXPECTED_CAPABILITIES
from cmf_builder.domain.responsibility_modules import (
    RESPONSIBILITY_MODULE_SCHEMA_ID,
    RESPONSIBILITY_MODULE_SCHEMA_VERSION,
)
from tests.stories.st_04_02 import build_context, compile_command


class ResponsibilityModuleAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            self.repository,
            self.observations,
            self.run_id,
            self.capability_receipt,
        ) = build_context()
        self.receipt = self.service.compile(compile_command(self.run_id))
        self.graph = self.service.get_active(self.run_id)
        self.parent = self.repository.get_capability_ownership_graph(
            self.graph.capability_graph_id
        )
        assert self.parent is not None

    def test_ac_01_exact_active_parent_and_full_lineage_are_preserved(self) -> None:
        self.assertEqual(self.graph.capability_graph_id, self.parent.graph_id)
        self.assertEqual(self.graph.capability_graph_hash, self.parent.graph_hash)
        for field in (
            "run_id", "ir_id", "ir_hash", "source_lock_ref", "boundary_ref",
            "ratification_ref", "model_ref", "artifact_set_id",
            "constitutional_report_id", "constitutional_report_hash",
            "constitutional_receipt_id", "constitutional_receipt_hash",
        ):
            self.assertEqual(getattr(self.graph, field), getattr(self.parent, field))

    def test_ac_02_capability_partition_is_exact_unique_and_canonical(self) -> None:
        self.assertEqual(tuple(sorted(self.graph.capability_ids)), EXPECTED_CAPABILITIES)
        self.assertEqual(len(self.graph.capability_ids), 3)
        self.assertEqual(len(set(self.graph.capability_ids)), 3)
        self.assertEqual(self.graph.module_ids, tuple(sorted(self.graph.module_ids)))
        self.assertEqual(self.graph.module_ids, ("atomic_boundary_module", "governed_contract_module"))

    def test_ac_03_04_modules_are_responsibility_centered_and_complete(self) -> None:
        forbidden = {"database", "api", "ui", "router", "agent", "adapter", "queue", "worker", "infrastructure"}
        for module in self.graph.modules:
            self.assertTrue(module.responsibility)
            self.assertTrue(module.boundary_rationale)
            self.assertTrue(module.owned_capabilities)
            self.assertTrue(module.public_contract.inputs)
            self.assertTrue(module.public_contract.outputs)
            self.assertFalse(module.public_contract.side_effects)
            self.assertTrue(module.invariants)
            self.assertTrue(module.exclusions)
            self.assertTrue(module.failure_owner)
            self.assertTrue(module.failure_modes)
            self.assertFalse(set(module.module_id.removesuffix("_module").split("_")) <= forbidden)

    def test_ac_05_every_module_has_a_complete_public_test_seam(self) -> None:
        for module in self.graph.modules:
            seam = module.test_seam
            self.assertTrue(seam.public_command)
            self.assertTrue(seam.expected_fixtures)
            self.assertTrue(seam.contract_tests)
            self.assertTrue(seam.failure_injections)
            self.assertTrue(seam.observable_outputs)

    def test_ac_06_authority_reliability_and_cost_evidence_are_preserved(self) -> None:
        self.assertEqual(self.graph.capability_ownerships, self.parent.decisions)
        self.assertTrue(all(item.reliability_evidence for item in self.graph.capability_ownerships))
        self.assertTrue(all(item.cost_evidence for item in self.graph.capability_ownerships))

    def test_ac_07_dependency_topology_is_explicit_and_resolved(self) -> None:
        modules = {item.module_id: item for item in self.graph.modules}
        self.assertEqual(modules["atomic_boundary_module"].dependencies, ())
        self.assertEqual(modules["governed_contract_module"].dependencies, ("atomic_boundary_module",))
        self.assertEqual(self.graph.dependency_count, 1)

    def test_ac_08_scope_is_synthetic_nonproduction_and_noncertified(self) -> None:
        self.assertFalse(self.graph.implicit_modules_allowed)
        self.assertFalse(self.graph.production_eligible)
        self.assertFalse(self.graph.certified)
        joined = self.graph.canonical_bytes().decode("utf-8").lower()
        for prohibited in ("format02", "vae_runtime", "delegation_runtime", "gpu", "control_tower", "workflow_ir"):
            self.assertNotIn(prohibited, joined)

    def test_ac_09_11_atomic_receipt_run_and_observations_are_complete(self) -> None:
        run = self.repository.load_run(self.run_id)
        self.assertEqual(run.stream_version, 15)
        self.assertEqual(run.responsibility_module_ref, self.graph.graph_id)
        self.assertEqual(run.responsibility_module_hash, self.graph.graph_hash)
        self.graph.validate(self.parent)
        self.receipt.validate(self.graph, self.parent)
        self.assertEqual(self.graph.schema_id, RESPONSIBILITY_MODULE_SCHEMA_ID)
        self.assertEqual(self.graph.schema_version, RESPONSIBILITY_MODULE_SCHEMA_VERSION)
        observations = [item for item in self.observations.observations if item.story_id == "ST-04.02"]
        self.assertEqual(
            {item.event_name for item in observations},
            {
                "ST-04.02:ResponsibilityModulesCompiled",
                "ST-04.02:CapabilityPartitionValidated",
                "ST-04.02:ModuleContractsValidated",
                "ST-04.02:TestSeamsValidated",
                "ST-04.02:OutcomeVerified",
            },
        )
        for item in observations:
            self.assertEqual(item.module_graph_id, self.graph.graph_id)
            self.assertEqual(item.module_receipt_id, self.receipt.receipt_id)
            self.assertEqual(item.module_count, 2)
            self.assertEqual(item.module_capability_coverage_count, 3)
            self.assertEqual(item.module_contract_coverage_count, 2)
            self.assertEqual(item.module_test_seam_coverage_count, 2)


if __name__ == "__main__":
    unittest.main()
