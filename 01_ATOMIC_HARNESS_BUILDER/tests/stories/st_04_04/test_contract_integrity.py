from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.domain.handoff import (
    ContextFieldDeclaration,
    GovernedHandoffArtifact,
    HandoffContractInvalid,
    HandoffLineageInvalid,
    PhaseContextGraph,
    PhaseHandoffGraph,
)
from tests.stories.st_04_04 import build_context, compile_command, governed_artifacts


class InternalHandoffContractIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, self.repository, _, self.run_id, _ = build_context()
        self.service.compile(compile_command(self.run_id))
        self.graph = self.service.get_active(self.run_id)
        self.phase_graph = self.repository.get_phase_graph(self.graph.phase_graph_id)
        assert self.phase_graph is not None

    def test_missing_phase_context_fails_closed(self) -> None:
        with self.assertRaises(HandoffContractInvalid):
            PhaseContextGraph.create(
                phase_graph=self.phase_graph,
                contexts=self.graph.context_graph.contexts[:-1],
            )

    def test_context_output_exposure_cannot_omit_governed_field(self) -> None:
        context = self.graph.context_graph.contexts[0]
        changed = replace(context, downstream_exposure=context.downstream_exposure[:-1])
        with self.assertRaises(HandoffContractInvalid):
            PhaseContextGraph.create(
                phase_graph=self.phase_graph,
                contexts=(changed, self.graph.context_graph.contexts[1]),
            )

    def test_context_cannot_include_and_exclude_same_field(self) -> None:
        context = self.graph.context_graph.contexts[0]
        with self.assertRaises(HandoffContractInvalid):
            replace(context, excluded_fields=(*context.excluded_fields, context.field_names[0]))

    def test_context_loading_cannot_be_silently_implemented(self) -> None:
        context = self.graph.context_graph.contexts[0]
        with self.assertRaises(HandoffContractInvalid):
            replace(context, conditional_loads=("load_external_context",))

    def test_duplicate_context_field_owner_fails_closed(self) -> None:
        context = self.graph.context_graph.contexts[0]
        duplicate = ContextFieldDeclaration(
            field=context.included_fields[0].field,
            owner="conflicting.owner",
            authority="code",
            mutability="IMMUTABLE",
        )
        with self.assertRaises(HandoffContractInvalid):
            replace(context, included_fields=(*context.included_fields, duplicate))

    def test_contract_cannot_weaken_mutation_or_compatibility_policy(self) -> None:
        contract = self.graph.contracts[0]
        for field, value in (
            ("downstream_rewrite", "ALLOWED"),
            ("mutability", "MUTABLE"),
            ("compatibility", "ANY"),
            ("invalidation", "NONE"),
        ):
            with self.subTest(field=field), self.assertRaises(HandoffContractInvalid):
                replace(contract, **{field: value})

    def test_reversed_or_dangling_consumer_fails_closed(self) -> None:
        contract = self.graph.contracts[0]
        for consumer in (contract.producer_phase, "undeclared_phase"):
            with self.subTest(consumer=consumer), self.assertRaises(HandoffContractInvalid):
                PhaseHandoffGraph.create(
                    phase_graph=self.phase_graph,
                    contexts=self.graph.context_graph.contexts,
                    contracts=(replace(contract, consumer_phases=(consumer,)),),
                    authority_identity="code-1",
                )

    def test_changed_governed_context_produces_new_identity(self) -> None:
        first, second = self.graph.context_graph.contexts
        changed_first = replace(first, excluded_fields=(*first.excluded_fields, "new_explicit_exclusion"))
        changed = PhaseHandoffGraph.create(
            phase_graph=self.phase_graph,
            contexts=(changed_first, second),
            contracts=self.graph.contracts,
            authority_identity="code-1",
        )
        self.assertNotEqual(changed.graph_id, self.graph.graph_id)
        self.assertNotEqual(changed.context_graph.context_graph_id, self.graph.context_graph.context_graph_id)

    def test_external_product_handoff_and_production_flags_fail_validation(self) -> None:
        for changed in (
            replace(self.graph, external_product_handoffs=("delegation",)),
            replace(self.graph, production_eligible=True),
            replace(self.graph, certified=True),
        ):
            with self.assertRaises(HandoffContractInvalid):
                changed.validate(self.phase_graph)

    def test_handoff_artifacts_require_hash_version_and_lineage(self) -> None:
        valid = governed_artifacts(self.service, self.repository, self.run_id)[0]
        with self.assertRaises(HandoffLineageInvalid):
            GovernedHandoffArtifact(
                field=valid.field,
                artifact_id=valid.artifact_id,
                artifact_hash="not-a-hash",
                version=valid.version,
                lineage_refs=valid.lineage_refs,
            )
        with self.assertRaises((HandoffLineageInvalid, HandoffContractInvalid)):
            replace(valid, lineage_refs=())


if __name__ == "__main__":
    unittest.main()
