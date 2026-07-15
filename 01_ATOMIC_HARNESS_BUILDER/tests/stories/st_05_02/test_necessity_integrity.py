from __future__ import annotations

from hashlib import sha256
import json
import unittest

from cmf_builder.domain.skill_registry import (
    CAPABILITY_IDS,
    REGISTRY_POLICY_ID,
    REGISTRY_POLICY_SHA256,
    REGISTRY_REF,
    SKILL_NECESSITY_INPUT_PATH,
    SKILL_NECESSITY_INPUT_SHA256,
    MissingRequiredSkill,
    SkillNecessityAuthorityInvalid,
    SkillNecessityEvidenceInvalid,
    UndeclaredSkillRequirement,
)
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_05_02 import build_context, evaluate_command


class SyntheticSkillNecessityIntegrityTests(unittest.TestCase):
    def _evaluate_override(self, override: tuple[str, str, str]):
        service, _, repository, _, run_id, _, _, snapshot = build_context()
        command = evaluate_command(
            run_id,
            snapshot.snapshot_id,
            snapshot.snapshot_hash,
            capability_evidence_overrides=(override,),
        )
        return service, repository, command

    def test_exact_governed_input_hash_and_capability_set_are_pinned(self) -> None:
        path = ROOT / SKILL_NECESSITY_INPUT_PATH
        self.assertEqual(sha256(path.read_bytes()).hexdigest(), SKILL_NECESSITY_INPUT_SHA256)
        value = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            tuple(sorted(item["capability_id"] for item in value["capability_requirements"])),
            CAPABILITY_IDS,
        )

    def test_decision_preserves_exact_registry_policy_and_upstream_lineage(self) -> None:
        service, _, repository, _, run_id, _, _, snapshot = build_context()
        service.evaluate(evaluate_command(run_id, snapshot.snapshot_id, snapshot.snapshot_hash))
        decision = service.get_active(run_id)
        self.assertEqual(decision.registry_ref, REGISTRY_REF)
        self.assertEqual(decision.registry_hash, snapshot.registry_hash)
        self.assertEqual(decision.policy_id, REGISTRY_POLICY_ID)
        self.assertEqual(decision.policy_hash, f"sha256:{REGISTRY_POLICY_SHA256}")
        self.assertEqual(decision.source_lock_ref, snapshot.source_lock_ref)
        self.assertEqual(decision.ir_id, snapshot.ir_id)
        self.assertEqual(decision.minimum_context_graph_id, snapshot.minimum_context_graph_id)

    def test_genuine_target_failure_is_detected_instead_of_hidden_by_empty_registry(self) -> None:
        service, repository, command = self._evaluate_override(
            (CAPABILITY_IDS[0], "target_failure_observed", "true")
        )
        with self.assertRaises(MissingRequiredSkill):
            service.evaluate(command)
        self.assertEqual(repository.skill_necessity_decision_count, 0)

    def test_undeclared_or_unregistered_skill_requirement_fails_closed(self) -> None:
        service, repository, command = self._evaluate_override(
            (CAPABILITY_IDS[1], "registered_skill_ref", "missing-skill@1.0.0")
        )
        with self.assertRaises(UndeclaredSkillRequirement):
            service.evaluate(command)
        self.assertEqual(repository.skill_necessity_decision_count, 0)

    def test_unverifiable_code_ownership_evidence_fails_closed(self) -> None:
        service, repository, command = self._evaluate_override(
            (CAPABILITY_IDS[2], "implementation_evidence", "unverifiable")
        )
        with self.assertRaises(SkillNecessityEvidenceInvalid):
            service.evaluate(command)
        self.assertEqual(repository.skill_necessity_decision_count, 0)

    def test_skill_or_material_adaptation_cannot_bypass_gap_authority(self) -> None:
        for alternative in ("harness_local_adaptation", "new_canonical_skill"):
            with self.subTest(alternative=alternative):
                service, repository, command = self._evaluate_override(
                    (CAPABILITY_IDS[3], "selected_alternative", alternative)
                )
                with self.assertRaises(SkillNecessityAuthorityInvalid):
                    service.evaluate(command)
                self.assertEqual(repository.skill_necessity_decision_count, 0)


if __name__ == "__main__":
    unittest.main()
