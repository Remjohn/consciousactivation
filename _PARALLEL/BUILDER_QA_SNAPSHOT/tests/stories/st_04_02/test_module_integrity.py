from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.domain.responsibility_modules import (
    ModuleBoundaryInvalid,
    ModuleCoverageInvalid,
    ModuleDependencyInvalid,
    ModulePublicContract,
    ModuleTestSeam,
    ResponsibilityModule,
    ResponsibilityModuleGraph,
)
from tests.stories.st_04_02 import build_context, compile_command


class ResponsibilityModuleIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        cls.graph = service.get_active(run_id)
        cls.parent = repository.get_capability_ownership_graph(cls.graph.capability_graph_id)
        assert cls.parent is not None

    def test_hidden_side_effect_is_rejected(self) -> None:
        with self.assertRaises(ModuleBoundaryInvalid):
            ModulePublicContract(inputs=("in",), outputs=("out",), side_effects=("database_write",))

    def test_incomplete_test_seam_is_rejected(self) -> None:
        with self.assertRaises(ModuleBoundaryInvalid):
            ModuleTestSeam(
                public_command="compile",
                expected_fixtures=(),
                contract_tests=("contract",),
                failure_injections=("failure",),
                observable_outputs=("receipt",),
            )

    def test_horizontal_technology_layer_identity_is_rejected(self) -> None:
        source = self.graph.modules[0]
        with self.assertRaises(ModuleBoundaryInvalid):
            replace(source, module_id="database_module", responsibility="database")

    def test_self_dependency_is_rejected(self) -> None:
        source = self.graph.modules[0]
        with self.assertRaises(ModuleDependencyInvalid):
            replace(source, dependencies=(source.module_id,))

    def test_missing_or_duplicate_capability_is_rejected(self) -> None:
        first, second = self.graph.modules
        cases = (
            (replace(first, owned_capabilities=(first.owned_capabilities[0],)), replace(second, owned_capabilities=(second.owned_capabilities[0],))),
            (first, replace(second, owned_capabilities=(first.owned_capabilities[0], *second.owned_capabilities))),
        )
        for modules in cases:
            with self.subTest(modules=modules), self.assertRaises(ModuleCoverageInvalid):
                ResponsibilityModuleGraph.create(
                    capability_graph=self.parent,
                    modules=modules,
                    authority_identity="code-1",
                )

    def test_unresolved_dependency_is_rejected(self) -> None:
        first, second = self.graph.modules
        with self.assertRaises(ModuleDependencyInvalid):
            ResponsibilityModuleGraph.create(
                capability_graph=self.parent,
                modules=(first, replace(second, dependencies=("missing_module",))),
                authority_identity="code-1",
            )

    def test_cycle_is_rejected(self) -> None:
        first, second = self.graph.modules
        with self.assertRaises(ModuleDependencyInvalid):
            ResponsibilityModuleGraph.create(
                capability_graph=self.parent,
                modules=(replace(first, dependencies=(second.module_id,)), second),
                authority_identity="code-1",
            )

    def test_failure_owner_must_be_an_owned_capability_owner(self) -> None:
        first, second = self.graph.modules
        with self.assertRaises(ModuleBoundaryInvalid):
            ResponsibilityModuleGraph.create(
                capability_graph=self.parent,
                modules=(replace(first, failure_owner="cmf_builder.unowned"), second),
                authority_identity="code-1",
            )

    def test_changed_governed_boundary_produces_new_immutable_identity(self) -> None:
        first, second = self.graph.modules
        changed = ResponsibilityModuleGraph.create(
            capability_graph=self.parent,
            modules=(replace(first, boundary_rationale=first.boundary_rationale + "_v2"), second),
            authority_identity="code-1",
        )
        self.assertNotEqual(changed.graph_id, self.graph.graph_id)
        self.assertNotEqual(changed.graph_hash, self.graph.graph_hash)


if __name__ == "__main__":
    unittest.main()
