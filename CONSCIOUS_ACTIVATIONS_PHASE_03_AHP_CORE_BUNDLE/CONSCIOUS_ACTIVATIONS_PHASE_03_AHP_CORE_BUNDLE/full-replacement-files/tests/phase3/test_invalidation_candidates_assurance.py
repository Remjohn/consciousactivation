from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import ref  # type: ignore
from cmf_pipeline import PipelineApplication
from cmf_pipeline.domain.errors import PipelineValidationError


class InvalidationCandidateAssuranceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.app = PipelineApplication(Path(self.temp.name) / "pipeline.sqlite3")
        self.app.initialize()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_descendant_only_invalidation_and_rerun(self) -> None:
        self.app.graph.add_dependency("semantic:root", "node:a", "semantic_dependency")
        self.app.graph.add_dependency("node:a", "node:b", "workflow_dependency")
        self.app.graph.add_dependency("unaffected:x", "unaffected:y", "workflow_dependency")
        plan = self.app.invalidation.plan(
            root_ids=["semantic:root"],
            reason="operator correction",
            preserved_ids=["unaffected:x", "unaffected:y"],
            replacement_refs=[ref("semantic:replacement")],
            idempotency_key="invalidation",
        )["object"]["payload"]
        self.assertEqual(plan["affected_descendant_ids"], ["node:a", "node:b"])
        self.assertFalse(plan["global_invalidation"])
        rerun = self.app.invalidation.rerun_plan(plan, reusable_checkpoint_ids=["checkpoint:1"])
        self.assertEqual(rerun["rerun_target_ids"], ["node:a", "node:b", "semantic:root"])
        self.assertTrue(rerun["unaffected_work_reused"])

    def test_preserved_descendant_is_rejected(self) -> None:
        self.app.graph.add_dependency("root", "child", "workflow_dependency")
        with self.assertRaises(PipelineValidationError):
            self.app.invalidation.plan(
                root_ids=["root"], reason="bad", preserved_ids=["child"], replacement_refs=[], idempotency_key="bad"
            )

    def test_candidate_search_uses_integer_budget_and_deterministic_tie_break(self) -> None:
        candidates = [
            {"candidate_id": "candidate:b", "artifact_ref": ref("artifact:b"), "quality_score_bps": 9000, "cost_units": 4, "sequence": 2, "eligible": True, "failure_codes": []},
            {"candidate_id": "candidate:a", "artifact_ref": ref("artifact:a"), "quality_score_bps": 9000, "cost_units": 3, "sequence": 1, "eligible": True, "failure_codes": []},
        ]
        portfolio = self.app.candidates.evaluate(candidates, max_candidates=2, budget_units=10, quality_threshold_bps=9500, plateau_window=2, plateau_delta_bps=0)
        self.assertEqual(portfolio["best_candidate_id"], "candidate:a")
        self.assertEqual(portfolio["stop_reason"], "PLATEAU")
        self.assertEqual(portfolio["spent_units"], 7)

    def test_assurance_detects_contract_release_drift(self) -> None:
        contract = ref("contract:release", "a" * 64)
        implementation = ref("implementation:one", "b" * 64)
        runtime = ref("runtime:python", "c" * 64)
        fingerprint = self.app.assurance.execution_fingerprint(
            contract_release_ref=contract,
            implementation_ref=implementation,
            runtime_ref=runtime,
            tool_refs=[ref("tool:one", "d" * 64)],
            evaluator_ref=None,
            model_ref=None,
            hardware_profile="local-cpu-development",
            precision="not_applicable",
        )
        sandbox = self.app.assurance.sandbox_declaration(
            implementation_ref=implementation,
            allowed_actions=["read", "write-local-state"],
            forbidden_actions=["external-provider-call"],
            allowed_relative_paths=[".conscious-activations/data"],
            network_policy="DENY_ALL",
            secret_reference_ids=[],
            resource_limits={"max_runtime_seconds": 60},
        )
        passed = self.app.assurance.assurance_check(target_ref=ref("run:one"), fingerprint=fingerprint, sandbox=sandbox, observed_contract_release_ref=contract)
        self.assertEqual(passed["result"], "PASS")
        failed = self.app.assurance.assurance_check(target_ref=ref("run:one"), fingerprint=fingerprint, sandbox=sandbox, observed_contract_release_ref=ref("contract:other", "e" * 64))
        self.assertEqual(failed["result"], "FAIL")
        self.assertIn("CONTRACT_RELEASE_DRIFT", failed["findings"])


if __name__ == "__main__":
    unittest.main()
