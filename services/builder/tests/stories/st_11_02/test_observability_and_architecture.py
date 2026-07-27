from __future__ import annotations

import ast
from hashlib import sha256
import json
import unittest

from cmf_builder.domain.implementation_plan import PLAN_INPUT_PATH, PLAN_INPUT_SHA256
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_11_02 import build_context, plan_command


class ImplementationPlanObservabilityArchitectureTests(unittest.TestCase):
    def test_success_observations_are_complete_and_attributable(self) -> None:
        service, _, _, _, observations, run_id, _, capsule = build_context(seed="ST-11.02-observe")
        receipt = service.compile(plan_command(run_id))
        story = [item for item in observations.observations if item.story_id == "ST-11.02"]
        self.assertEqual(len(story), 5)
        self.assertEqual(story[0].event_name, "implementation_plan_compilation_started")
        self.assertEqual(story[-1].event_name, "implementation_plan_compilation_committed")
        for item in story:
            self.assertEqual(item.development_capsule_id, capsule.capsule_id)
            self.assertEqual(item.failure_context["plan_receipt_id"], receipt.receipt_id)
            self.assertFalse(item.failure_context["implementation_authorized"])

    def test_rejection_observation_has_typed_failure_context(self) -> None:
        service, _, _, _, observations, run_id, _, _ = build_context(seed="ST-11.02-reject")
        with self.assertRaises(Exception):
            service.compile(plan_command(run_id, actor_id="agent-1"))
        item = observations.observations[-1]
        self.assertEqual(item.event_name, "implementation_plan_compilation_rejected")
        self.assertEqual(item.outcome, "FAIL")
        self.assertIn("code", item.failure_context)

    def test_input_is_exact_hash_pinned_and_portable(self) -> None:
        path = ROOT / PLAN_INPUT_PATH
        self.assertEqual(sha256(path.read_bytes()).hexdigest(), PLAN_INPUT_SHA256)
        value = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(value["owned_obligations"], ["FR-156", "FR-157"])
        self.assertFalse(value["implementation_authorized"])
        self.assertTrue(all(":/" not in json.dumps(item) for item in value["increments"]))

    def test_new_sources_respect_layering_and_have_no_external_imports(self) -> None:
        for relative in (
            "src/cmf_builder/domain/implementation_plan.py",
            "src/cmf_builder/application/implementation_plan_commands.py",
        ):
            path = ROOT / relative
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
            imports = {
                alias.name
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            } | {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            }
            self.assertFalse({name.split(".", 1)[0] for name in imports} & {"boto3", "fastapi", "requests", "sqlalchemy"})
            if "/domain/" in relative:
                self.assertFalse(any(name.startswith(("cmf_builder.application", "cmf_builder.adapters")) for name in imports))


if __name__ == "__main__":
    unittest.main()
