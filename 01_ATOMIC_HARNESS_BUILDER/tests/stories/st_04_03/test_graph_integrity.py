from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.domain.phase_graph import (
    PhaseAuthorityInvalid,
    PhaseCoverageInvalid,
    PhaseDependencyInvalid,
    PhaseExecutionPlan,
    PhaseGraph,
    PhaseNode,
)
from tests.stories.st_04_03 import build_context, compile_command


class PhaseGraphIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.compile(compile_command(run_id))
        cls.graph = service.get_active(run_id)
        cls.parent = repository.get_responsibility_module_graph(cls.graph.module_graph_id)
        assert cls.parent is not None

    def test_phase_requires_entry_exit_gate_and_module_contracts(self) -> None:
        source = self.graph.phases[0]
        for change in ({"entry_conditions": ()}, {"exit_evidence": ()}, {"required_gates": ()}, {"module_refs": ()}):
            with self.subTest(change=change), self.assertRaises(PhaseCoverageInvalid):
                replace(source, **change)

    def test_self_edge_and_dependency_parallel_conflict_are_rejected(self) -> None:
        source = self.graph.phases[0]
        with self.assertRaises(PhaseDependencyInvalid):
            replace(source, dependencies=(source.phase_id,))
        with self.assertRaises(PhaseDependencyInvalid):
            replace(source, dependencies=("other",), parallel_with=("other",))

    def test_non_code_execution_kind_is_rejected(self) -> None:
        with self.assertRaises(PhaseAuthorityInvalid):
            replace(self.graph.phases[0], execution_kind="EXTERNAL_RUNTIME")

    def test_duplicate_phase_identity_is_rejected(self) -> None:
        first, second = self.graph.phases
        with self.assertRaises(PhaseCoverageInvalid):
            PhaseExecutionPlan.create((first, replace(second, phase_id=first.phase_id)))

    def test_missing_phase_is_rejected_as_an_unresolved_dependency(self) -> None:
        first, second = self.graph.phases
        with self.assertRaises(PhaseDependencyInvalid):
            PhaseGraph.create(
                module_graph=self.parent,
                phases=(first,),
                authority_identity="code-1",
            )

    def test_duplicate_module_coverage_is_rejected(self) -> None:
        first, second = self.graph.phases
        with self.assertRaises(PhaseCoverageInvalid):
            PhaseGraph.create(
                module_graph=self.parent,
                phases=(first, replace(second, module_refs=first.module_refs)),
                authority_identity="code-1",
            )

    def test_unresolved_dependency_and_cycle_are_rejected(self) -> None:
        first, second = self.graph.phases
        with self.assertRaises(PhaseDependencyInvalid):
            PhaseGraph.create(
                module_graph=self.parent,
                phases=(replace(first, dependencies=("missing",)), second),
                authority_identity="code-1",
            )
        with self.assertRaises(PhaseDependencyInvalid):
            PhaseGraph.create(
                module_graph=self.parent,
                phases=(replace(first, dependencies=(second.phase_id,)), replace(second, dependencies=(first.phase_id,))),
                authority_identity="code-1",
            )

    def test_asymmetric_or_gate_incompatible_parallelism_is_rejected(self) -> None:
        first, second = self.graph.phases
        independent_second = replace(second, dependencies=())
        with self.assertRaises(PhaseDependencyInvalid):
            PhaseExecutionPlan.create((replace(first, parallel_with=(second.phase_id,)), independent_second))
        with self.assertRaises(PhaseDependencyInvalid):
            PhaseExecutionPlan.create((replace(first, parallel_with=(second.phase_id,)), replace(independent_second, parallel_with=(first.phase_id,))))

    def test_explicit_symmetric_gate_compatible_parallelism_is_supported(self) -> None:
        first, second = self.graph.phases
        common_gates = ("shared_governed_gate",)
        phases = (
            replace(first, dependencies=(), parallel_with=(second.phase_id,), required_gates=common_gates),
            replace(second, dependencies=(), parallel_with=(first.phase_id,), required_gates=common_gates),
        )
        plan = PhaseExecutionPlan.create(phases)
        self.assertEqual(plan.parallel_pairs, (tuple(sorted((first.phase_id, second.phase_id))),))
        self.assertEqual(set(plan.initially_runnable), {first.phase_id, second.phase_id})

    def test_failure_owner_and_exit_evidence_must_remain_module_owned(self) -> None:
        first, second = self.graph.phases
        with self.assertRaises(PhaseAuthorityInvalid):
            PhaseGraph.create(
                module_graph=self.parent,
                phases=(replace(first, failure_owner="cmf_builder.unowned"), second),
                authority_identity="code-1",
            )
        with self.assertRaises(PhaseCoverageInvalid):
            PhaseGraph.create(
                module_graph=self.parent,
                phases=(replace(first, exit_evidence=("unowned_output",)), second),
                authority_identity="code-1",
            )

    def test_changed_governed_topology_produces_new_immutable_identity(self) -> None:
        first, second = self.graph.phases
        changed = PhaseGraph.create(
            module_graph=self.parent,
            phases=(replace(first, responsibility=first.responsibility + "_v2"), second),
            authority_identity="code-1",
        )
        self.assertNotEqual(changed.graph_id, self.graph.graph_id)
        self.assertNotEqual(changed.graph_hash, self.graph.graph_hash)


if __name__ == "__main__":
    unittest.main()
