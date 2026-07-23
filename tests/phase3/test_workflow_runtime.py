from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import ref  # type: ignore
from cmf_pipeline import PipelineApplication
from cmf_pipeline.demo import write_demo_harness
from cmf_pipeline.domain.errors import PipelineConflict, PipelineLifecycleError


class WorkflowRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.app = PipelineApplication(self.root / "pipeline.sqlite3")
        self.app.initialize()
        self.app.load_default_development_candidates()
        package = self.root / "harness.zip"
        write_demo_harness(package)
        self.imported = self.app.import_harness_package(package, idempotency_key="import")
        binding_result = self.app.compile_binding(self.imported["projection"], self.imported["graph_receipt"], idempotency_key="binding")
        self.binding = binding_result["object"]["payload"]
        workflow_result = self.app.compile_workflow(self.imported["projection"], self.binding, self.imported["graph_receipt"], idempotency_key="workflow")
        self.workflow = workflow_result["object"]["payload"]
        self.binding_ref = ref(self.binding["manifest_id"], binding_result["object"]["canonical_sha256"])

    def tearDown(self) -> None:
        self.temp.cleanup()

    def create_run(self, key: str = "run") -> dict[str, object]:
        return self.app.runs.create_run(
            self.workflow["workflow_id"],
            binding_manifest_ref=self.binding_ref,
            context_refs=self.imported["projection"]["semantic_dependencies"],
            batch_ref=None,
            idempotency_key=key,
        )

    def _finish(self, run_id: str, node_id: str, ordinal: int) -> None:
        self.app.runs.dispatch_node(
            run_id,
            node_id,
            context_refs=self.imported["projection"]["semantic_dependencies"],
            allowed_actions=["execute"],
            forbidden_actions=["change_air_meaning"],
            tool_ids=["synthetic-development-adapter"],
            idempotency_key=f"dispatch:{ordinal}",
        )
        self.app.runs.start_node(run_id, node_id, idempotency_key=f"start:{ordinal}")
        self.app.runs.complete_node(
            run_id,
            node_id,
            output_ref=ref(f"output:{node_id}", chr(96 + ordinal) * 64),
            validation_receipt_refs=[f"receipt:{ordinal}"],
            idempotency_key=f"complete:{ordinal}",
        )

    def test_deterministic_scheduler_checkpoint_and_replay(self) -> None:
        run = self.create_run()
        run_id = run["run_id"]
        self.assertEqual(self.app.runs.ready_nodes(run_id), ["node:inspect"])
        self._finish(run_id, "node:inspect", 1)
        checkpoint = self.app.runs.checkpoint(run_id, idempotency_key="checkpoint")
        self.assertTrue(checkpoint["checkpoint_id"].startswith("pipeline-checkpoint:"))
        self.assertEqual(self.app.runs.ready_nodes(run_id), ["node:compose"])
        self._finish(run_id, "node:compose", 2)
        self.assertEqual(self.app.runs.ready_nodes(run_id), ["node:review"])
        self._finish(run_id, "node:review", 3)
        status = self.app.runs.status(run_id)
        self.assertEqual(status["state"], "COMPLETED")
        replay = self.app.runs.replay(run_id)
        self.assertEqual(replay["event_count"], 13)
        self.assertEqual(replay["current_state"]["state"], "COMPLETED")

    def test_idempotency_conflict_and_replay(self) -> None:
        first = self.create_run("same-key")
        second = self.create_run("same-key")
        self.assertEqual(first["run_id"], second["run_id"])
        self.assertTrue(second["idempotent_replay"])
        with self.assertRaises(PipelineConflict):
            self.app.runs.create_run(
                self.workflow["workflow_id"],
                binding_manifest_ref=self.binding_ref,
                context_refs=[],
                batch_ref=None,
                idempotency_key="same-key",
            )

    def test_cancel_quarantines_late_running_result(self) -> None:
        run_id = self.create_run("cancel")["run_id"]
        self.app.runs.dispatch_node(
            run_id,
            "node:inspect",
            context_refs=self.imported["projection"]["semantic_dependencies"],
            allowed_actions=["inspect"],
            forbidden_actions=["external_call"],
            tool_ids=["synthetic-development-adapter"],
            idempotency_key="cancel-dispatch",
        )
        self.app.runs.start_node(run_id, "node:inspect", idempotency_key="cancel-start")
        cancelled = self.app.runs.cancel_run(run_id, reason="operator cancelled", idempotency_key="cancel-command")
        self.assertEqual(cancelled["state"], "CANCEL_REQUESTED")
        late = self.app.runs.complete_node(
            run_id,
            "node:inspect",
            output_ref=ref("output:late"),
            validation_receipt_refs=["receipt:late"],
            idempotency_key="cancel-late",
        )
        self.assertEqual(late["state"], "QUARANTINED")
        self.assertFalse(late["consumable"])
        self.assertEqual(self.app.runs.status(run_id)["state"], "CANCELLED")

    def test_pause_resume_guards_dispatch(self) -> None:
        run_id = self.create_run("pause")["run_id"]
        self.app.runs.pause_run(run_id, idempotency_key="pause-command")
        with self.assertRaises(PipelineLifecycleError):
            self.app.runs.dispatch_node(
                run_id,
                "node:inspect",
                context_refs=self.imported["projection"]["semantic_dependencies"],
                allowed_actions=["inspect"],
                forbidden_actions=["external_call"],
                tool_ids=["synthetic-development-adapter"],
                idempotency_key="paused-dispatch",
            )
        self.app.runs.resume_run(run_id, idempotency_key="resume-command")
        self.assertEqual(self.app.runs.ready_nodes(run_id), ["node:inspect"])


if __name__ == "__main__":
    unittest.main()
