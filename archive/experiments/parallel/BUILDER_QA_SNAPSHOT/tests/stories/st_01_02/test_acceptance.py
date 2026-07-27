from __future__ import annotations

from hashlib import sha256
import unittest

from cmf_builder.application.evidence_commands import (
    EvidenceWorkspaceCommandRejected,
    SOURCE_PROFILE_ID,
    SOURCE_PROFILE_VERSION,
    TARGET_CANDIDATE_URI,
)
from cmf_builder.domain.run import LifecycleState
from tests.stories.st_01_02 import ROOT, build_context, lock_command


class EvidenceWorkspaceAcceptanceTests(unittest.TestCase):
    def test_ac_01_02_06_09_locks_the_exact_synthetic_definition(self) -> None:
        service, repository, _, _, run_id = build_context()
        receipt = service.lock(lock_command(run_id))

        run = repository.load_run(run_id)
        source_lock = repository.get_source_lock(receipt.source_lock_ref)
        self.assertIsNotNone(source_lock)
        assert source_lock is not None
        self.assertEqual(run.lifecycle_state, LifecycleState.SOURCE_LOCKED)
        self.assertEqual(run.source_lock_ref, source_lock.lock_id)
        self.assertEqual(run.stream_version, 5)
        self.assertEqual(receipt.outcome, "PASS")
        self.assertEqual(receipt.source_profile_ref, f"{SOURCE_PROFILE_ID}@{SOURCE_PROFILE_VERSION}")
        self.assertEqual(receipt.event_ids, tuple(event.event_id for event in run.events[-3:]))
        self.assertTrue(receipt.receipt_hash.startswith("sha256:"))
        self.assertEqual(receipt.diagnostics[0].code, "SourceDiagnosticAccepted")
        self.assertEqual(source_lock.target_candidate_ref, TARGET_CANDIDATE_URI)
        self.assertEqual(source_lock.file_count, 1)
        descriptor = source_lock.ordered_descriptors[0]
        self.assertEqual(descriptor.role, "governed_task_definition")
        self.assertEqual(descriptor.privacy_class, "non_personal_synthetic")
        self.assertTrue(descriptor.canonical_uri.startswith("repo://"))
        self.assertNotIn(str(ROOT), descriptor.canonical_uri)

    def test_ac_03_04_10_source_is_read_only_and_scope_is_non_production(self) -> None:
        source = ROOT / (
            "development-capsules/ST-01.01-SYNTHETIC-PROOF/"
            "SYNTHETIC_TARGET_PROFILE_FIXTURE.yaml"
        )
        before = (sha256(source.read_bytes()).hexdigest(), source.stat().st_mtime_ns)
        service, repository, _, _, run_id = build_context()
        receipt = service.lock(lock_command(run_id))
        after = (sha256(source.read_bytes()).hexdigest(), source.stat().st_mtime_ns)

        source_lock = repository.get_source_lock(receipt.source_lock_ref)
        assert source_lock is not None
        self.assertEqual(before, after)
        self.assertEqual(source_lock.source_profile_ref, "synthetic_task_definition_source_v1@1.0.0")
        self.assertNotIn("Format02", source_lock.target_candidate_ref)
        self.assertEqual(repository.source_lock_count, 1)

    def test_ac_01_03_10_rejects_profile_or_candidate_substitution_without_mutation(self) -> None:
        cases = (
            {"source_profile_path": "format02/source-profile.json"},
            {"source_profile_sha256": "0" * 64},
            {"target_candidate_uri": "repo://format02/corpus.zip"},
        )
        for index, changes in enumerate(cases):
            with self.subTest(changes=changes):
                service, repository, observations, _, run_id = build_context()
                with self.assertRaises(EvidenceWorkspaceCommandRejected):
                    service.lock(
                        lock_command(
                            run_id,
                            command_id=f"substitution-{index}",
                            **changes,
                        )
                    )
                self.assertEqual(repository.event_count(run_id), 2)
                self.assertEqual(repository.source_lock_count, 0)
                rejected = [
                    item
                    for item in observations.observations
                    if item.story_id == "ST-01.02" and item.outcome == "FAIL"
                ]
                self.assertEqual(len(rejected), 2)


if __name__ == "__main__":
    unittest.main()
