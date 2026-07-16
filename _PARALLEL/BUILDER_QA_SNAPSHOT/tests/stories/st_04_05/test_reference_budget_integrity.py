from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.domain.context_manifest import (
    ContextBudgetOverflow,
    ContextContractInvalid,
    ContextDisposition,
    PhaseContextManifest,
)
from tests.stories.st_04_05 import build_context, compile_command


class ReferenceAndBudgetIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, _, _, _, self.run_id, _ = build_context()
        self.service.compile(compile_command(self.run_id))
        self.graph = self.service.get_active(self.run_id)

    def test_required_overflow_names_causes_and_does_not_truncate(self) -> None:
        policy = self.graph.policies[0]
        manifest = self.graph.manifests[0]
        overflow_policy = replace(
            policy,
            hard_budget=replace(policy.hard_budget, tokens=1),
            soft_budget=replace(policy.soft_budget, tokens=1),
        )
        with self.assertRaises(ContextBudgetOverflow) as raised:
            PhaseContextManifest.create(
                phase_ref=manifest.phase_ref,
                module_ref=manifest.module_ref,
                responsibility=manifest.responsibility,
                policy=overflow_policy,
                included=manifest.included,
                excluded=manifest.excluded,
            )
        self.assertTrue(raised.exception.context["overflowing_reference_ids"])
        self.assertEqual(len(raised.exception.context["remediation_choices"]), 3)
        self.assertFalse(raised.exception.context["silent_truncation"])

    def test_duplicate_conflicting_or_unjustified_context_fails_closed(self) -> None:
        policy = self.graph.policies[0]
        manifest = self.graph.manifests[0]
        with self.assertRaises(ContextContractInvalid):
            replace(policy, optional_references=policy.required_references).__post_init__()
        with self.assertRaises(ContextContractInvalid):
            replace(
                manifest,
                included=(*manifest.included, manifest.included[0]),
            ).validate(policy)

    def test_forbidden_or_not_applicable_context_cannot_consume_budget(self) -> None:
        item = self.graph.manifests[0].excluded[-1]
        with self.assertRaises(ContextContractInvalid):
            replace(
                item,
                disposition=ContextDisposition.FORBIDDEN,
                governed_tokens=1,
            ).__post_init__()

    def test_pointer_and_influence_boundaries_cannot_be_weakened(self) -> None:
        declaration = next(
            item for item in self.graph.references
            if item.reference_id == "constitutional_authority_pointer_v1"
        )
        with self.assertRaises(ContextContractInvalid):
            replace(declaration, progressive_disclosure_pointer=None).__post_init__()
        with self.assertRaises(ContextContractInvalid):
            replace(
                declaration,
                may_influence=(*declaration.may_influence, "source_evidence_identity"),
            ).__post_init__()


if __name__ == "__main__":
    unittest.main()
