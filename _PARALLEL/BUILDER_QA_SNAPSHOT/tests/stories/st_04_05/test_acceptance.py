from __future__ import annotations

import unittest

from cmf_builder.domain.context_manifest import (
    GOVERNED_PRIORITY_ORDER,
    MANIFEST_CATEGORIES,
    ContextDisposition,
)
from tests.stories.st_04_05 import build_context, compile_command


class MinimumCompleteContextAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            _,
            self.repository,
            self.observations,
            self.run_id,
            _,
        ) = build_context()
        self.receipt = self.service.compile(compile_command(self.run_id))
        self.graph = self.service.get_active(self.run_id)

    def test_ac_01_compiles_exact_two_phase_manifests_and_receipt(self) -> None:
        self.assertEqual(
            tuple(item.phase_ref for item in self.graph.manifests),
            ("governed_contract_ready", "ratified_boundary_ready"),
        )
        self.assertEqual(self.receipt.manifest_count, 2)
        self.assertEqual(self.receipt.reference_count, 6)
        self.assertEqual(self.receipt.stream_version, 20)
        self.receipt.validate(self.graph)

    def test_ac_02_registers_every_reference_with_identity_authority_and_hash(self) -> None:
        self.assertEqual(len(self.graph.references), 6)
        for declaration in self.graph.references:
            declaration.__post_init__()
            self.assertTrue(declaration.reference_id)
            self.assertTrue(declaration.version)
            self.assertTrue(declaration.owner)
            self.assertTrue(declaration.authority)
        for manifest in self.graph.manifests:
            self.assertEqual(len(manifest.all_items), 6)
            for item in manifest.all_items:
                self.assertEqual(len(item.artifact_hash), 71)
                self.assertTrue(item.provenance)

    def test_ac_03_04_applies_phase_loading_and_typed_pointer_boundaries(self) -> None:
        manifests = {item.phase_ref: item for item in self.graph.manifests}
        ratified = manifests["ratified_boundary_ready"]
        governed = manifests["governed_contract_ready"]
        self.assertEqual(set(ratified.required), {"source_lock_ref_v1", "human_ratification_ref_v1"})
        self.assertEqual(
            set(governed.required),
            {
                "frozen_atomic_boundary_ref_v1",
                "boundary_validation_receipt_ref_v1",
                "constitutional_authority_pointer_v1",
            },
        )
        pointer = next(
            item for item in governed.included
            if item.reference_id == "constitutional_authority_pointer_v1"
        )
        self.assertEqual(pointer.loading_mode, "retrieval_only")
        self.assertEqual(pointer.pointer_target, "canonical_authority_ref")
        self.assertEqual(governed.retrieved, ())

    def test_ac_05_spr_is_explicitly_not_applicable_and_never_included(self) -> None:
        for manifest in self.graph.manifests:
            self.assertEqual(manifest.not_applicable, ("synthetic_spr_v1",))
            spr = next(item for item in manifest.excluded if item.reference_id == "synthetic_spr_v1")
            self.assertIs(spr.disposition, ContextDisposition.NOT_APPLICABLE)
            self.assertEqual(spr.loading_mode, "forbidden_at_runtime")

    def test_ac_06_07_priority_budgets_and_classes_are_complete(self) -> None:
        self.assertEqual(self.graph.manifest_categories, MANIFEST_CATEGORIES)
        for manifest in self.graph.manifests:
            self.assertEqual(manifest.priority_order, GOVERNED_PRIORITY_ORDER)
            self.assertLessEqual(manifest.total_governed_tokens, manifest.hard_budget.tokens)
            self.assertLessEqual(manifest.soft_budget.tokens, manifest.hard_budget.tokens)
            self.assertEqual(manifest.conditionally_required, ())
            self.assertEqual(manifest.optional, ())
            self.assertEqual(manifest.forbidden, ())

    def test_ac_09_manifests_are_complete_minimal_and_reproducible(self) -> None:
        for manifest in self.graph.manifests:
            self.assertEqual(len(manifest.included) + len(manifest.excluded), 6)
            self.assertEqual(manifest.summarized, ())
            self.assertEqual(manifest.retrieved, ())
            self.assertEqual(manifest.compressed, ())
            self.assertEqual(
                manifest.total_governed_tokens,
                sum(item.governed_tokens for item in manifest.included),
            )

    def test_ac_11_runtime_external_and_production_boundaries_remain_closed(self) -> None:
        self.assertFalse(self.graph.conversation_history_allowed)
        self.assertFalse(self.graph.runtime_loading_allowed)
        self.assertFalse(self.graph.production_eligible)
        self.assertFalse(self.graph.certified)
        canonical = self.graph.canonical_bytes().decode("utf-8").lower()
        for prohibited in (
            "format02", "vae_runtime", "delegation_runtime", "gpu_execution",
            "conversation_history_payload", "production_publication",
        ):
            self.assertNotIn(prohibited, canonical)

    def test_observations_cover_completeness_minimality_and_no_truncation(self) -> None:
        story = [item for item in self.observations.observations if item.story_id == "ST-04.05"]
        names = {item.event_name for item in story}
        self.assertIn("ST-04.05:ContextCompletenessValidated", names)
        self.assertIn("ST-04.05:ContextMinimalityValidated", names)
        self.assertIn("ST-04.05:BudgetsAndNoTruncationValidated", names)
        for item in story:
            self.assertEqual(item.minimum_context_graph_id, self.graph.graph_id)
            self.assertEqual(item.context_manifest_count, 2)


if __name__ == "__main__":
    unittest.main()
