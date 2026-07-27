from __future__ import annotations

import unittest

from cmf_builder.domain.skill_registry import (
    CAPABILITY_IDS,
    GOVERNED_ALTERNATIVE_ORDER,
    SkillDesignBriefDisposition,
    SkillNecessityVerdict,
)
from tests.stories.st_05_02 import build_context, evaluate_command


class SyntheticSkillNecessityAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            self.repository,
            self.observations,
            self.run_id,
            _,
            _,
            self.snapshot,
        ) = build_context()
        self.receipt = self.service.evaluate(evaluate_command(
            self.run_id,
            self.snapshot.snapshot_id,
            self.snapshot.snapshot_hash,
        ))
        self.decision = self.service.get_active(self.run_id)

    def test_ac_01_commits_one_decision_and_receipt_against_exact_snapshot(self) -> None:
        self.assertEqual(self.repository.skill_necessity_decision_count, 1)
        self.assertEqual(self.repository.skill_necessity_receipt_count, 1)
        self.assertEqual(self.receipt.stream_version, 22)
        self.assertEqual(self.decision.snapshot_id, self.snapshot.snapshot_id)
        self.receipt.validate(self.decision)

    def test_ac_02_assesses_exactly_five_capabilities_with_governed_evidence(self) -> None:
        self.assertEqual(self.decision.capability_ids, CAPABILITY_IDS)
        for evidence in self.decision.capability_evidence:
            self.assertIs(evidence.verdict, SkillNecessityVerdict.BUILDER_OWNED_CODE)
            self.assertFalse(evidence.target_failure_observed)
            self.assertEqual(evidence.current_owner_kind, "builder_code")
            self.assertTrue(evidence.implementation_evidence_refs)
            self.assertTrue(evidence.reliability_evidence_refs)
            self.assertTrue(evidence.context_requirement_refs)

    def test_ac_03_records_governed_alternatives_in_exact_order(self) -> None:
        for evidence in self.decision.capability_evidence:
            self.assertEqual(
                tuple(item.alternative_id for item in evidence.alternative_assessments),
                GOVERNED_ALTERNATIVE_ORDER,
            )
            selected = [item for item in evidence.alternative_assessments if item.selected]
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0].alternative_id, "deterministic_code")
            self.assertEqual(selected[0].adequacy, "COMPLETE")

    def test_ac_04_emits_proven_no_skill_outcome_without_fabricated_brief(self) -> None:
        self.assertEqual(self.decision.outcome, "NO_NEW_SKILL_REQUIRED")
        self.assertEqual(self.decision.external_skills_required_count, 0)
        self.assertEqual(self.decision.missing_required_skills_count, 0)
        self.assertEqual(self.decision.adaptations_required_count, 0)
        self.assertEqual(self.decision.experiments_required_count, 0)
        self.assertEqual(self.decision.jit_capsules_required_count, 0)
        self.assertFalse(self.decision.skill_execution_required)
        self.assertFalse(self.decision.production_skill_certification)
        self.assertEqual(self.decision.skill_design_brief_count, 0)
        self.assertIs(
            self.decision.brief_disposition,
            SkillDesignBriefDisposition.NOT_APPLICABLE_NO_GAP,
        )

    def test_ac_12_success_observations_expose_decision_and_zero_gap_evidence(self) -> None:
        story = [item for item in self.observations.observations if item.story_id == "ST-05.02"]
        self.assertEqual(
            {item.event_name for item in story},
            {
                "synthetic_skill_necessity_started",
                "synthetic_skill_alternatives_assessed",
                "synthetic_no_skill_decision_committed",
            },
        )
        for item in story:
            self.assertEqual(item.skill_necessity_decision_id, self.decision.decision_id)
            self.assertEqual(item.skill_necessity_receipt_id, self.receipt.receipt_id)
            self.assertEqual(item.skill_necessity_capability_count, 5)
            self.assertEqual(item.skill_alternative_assessment_count, 50)
            self.assertEqual(item.skill_target_failure_count, 0)
            self.assertEqual(item.skill_missing_required_count, 0)


if __name__ == "__main__":
    unittest.main()
