from __future__ import annotations

import ast
from hashlib import sha256
import json
import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.domain.implementation_feedback import FEEDBACK_INPUT_PATH, FEEDBACK_INPUT_SHA256, ImplementationFeedbackInvalidatedError
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_11_03 import build_context, feedback_command


class ImplementationFeedbackLifecycleArchitectureTests(unittest.TestCase):
    def test_upstream_invalidation_disables_active_and_preserves_history(self) -> None:
        service, _, atomicity, repository, _, run_id, _, _ = build_context(seed="ST-11.03-invalidation")
        service.govern(feedback_command(run_id))
        proposal = service.get_active(run_id)
        atomicity.reopen(ReopenAtomicBoundaryCommand(
            command_id="reopen-after-proposal", run_id=run_id, actor_id="architect-1",
            expected_version=25, correlation_id="st-11-03-reopen",
            causation_id=proposal.proposal_id, reason="Authorized upstream correction.",
        ))
        self.assertTrue(repository.is_amendment_proposal_invalidated(proposal.proposal_id))
        with self.assertRaises(ImplementationFeedbackInvalidatedError):
            service.get_active(run_id)
        self.assertEqual(service.get_historical(proposal.proposal_id).canonical_bytes(), proposal.canonical_bytes())

    def test_observability_covers_start_items_commit_replay_and_rejection(self) -> None:
        service, _, _, _, observations, run_id, _, _ = build_context(seed="ST-11.03-observe")
        service.govern(feedback_command(run_id))
        story = [item for item in observations.observations if item.story_id == "ST-11.03"]
        self.assertEqual(len(story), 5)
        self.assertEqual(story[0].event_name, "implementation_feedback_ingestion_started")
        self.assertEqual(story[-1].event_name, "implementation_feedback_proposal_committed")
        self.assertTrue(all(item.failure_context["authority_mutated"] is False for item in story))
        service.govern(feedback_command(run_id))
        self.assertEqual(observations.observations[-1].event_name, "implementation_feedback_ingestion_replayed")

    def test_input_pin_and_evidence_are_portable_and_hash_valid(self) -> None:
        path = ROOT / FEEDBACK_INPUT_PATH
        self.assertEqual(sha256(path.read_bytes()).hexdigest(), FEEDBACK_INPUT_SHA256)
        value = json.loads(path.read_text(encoding="utf-8"))
        for item in value["feedback_items"]:
            self.assertFalse(item["requested_authority_mutation"])
            self.assertTrue(all(":/" not in ref for ref in item["evidence_refs"]))
            for ref, expected in zip(item["evidence_refs"], item["evidence_hashes"], strict=True):
                self.assertEqual(f"sha256:{sha256((ROOT / ref).read_bytes()).hexdigest()}", expected)

    def test_new_sources_respect_layering_and_external_boundaries(self) -> None:
        for relative in (
            "src/cmf_builder/domain/implementation_feedback.py",
            "src/cmf_builder/application/implementation_feedback_commands.py",
        ):
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"), filename=relative)
            imports = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names} | {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
            self.assertFalse({item.split(".", 1)[0] for item in imports} & {"boto3", "fastapi", "requests", "sqlalchemy"})
            if "/domain/" in relative:
                self.assertFalse(any(item.startswith(("cmf_builder.application", "cmf_builder.adapters")) for item in imports))


if __name__ == "__main__":
    unittest.main()
