from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path
import unittest

from cmf_builder.domain.handoff import PHASE_HANDOFF_INPUT_PATH, PHASE_HANDOFF_INPUT_SHA256


ROOT = Path(__file__).resolve().parents[3]
NEW_SOURCE = {
    "src/cmf_builder/domain/handoff.py",
    "src/cmf_builder/application/handoff_commands.py",
}
ALLOWED_IMPORT_ROOTS = {
    "__future__", "dataclasses", "datetime", "enum", "hashlib", "json",
    "pathlib", "typing", "cmf_builder",
}


class InternalHandoffArchitectureTests(unittest.TestCase):
    def test_exact_two_story_source_modules_exist(self) -> None:
        self.assertEqual({path for path in NEW_SOURCE if (ROOT / path).is_file()}, NEW_SOURCE)

    def test_story_modules_use_only_standard_library_and_builder(self) -> None:
        for relative in NEW_SOURCE:
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
            roots: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    roots.add((node.module or "").split(".", 1)[0])
            self.assertTrue(roots <= ALLOWED_IMPORT_ROOTS, (relative, roots))

    def test_domain_remains_independent_of_application_and_adapters(self) -> None:
        tree = ast.parse((ROOT / "src/cmf_builder/domain/handoff.py").read_text(encoding="utf-8"))
        imports = {
            node.module for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        self.assertFalse(any(item.startswith(("cmf_builder.application", "cmf_builder.adapters")) for item in imports))

    def test_handoff_input_is_exactly_hash_pinned(self) -> None:
        self.assertEqual(sha256((ROOT / PHASE_HANDOFF_INPUT_PATH).read_bytes()).hexdigest(), PHASE_HANDOFF_INPUT_SHA256)

    def test_no_external_transport_database_runtime_or_schema_is_added(self) -> None:
        joined = "\n".join((ROOT / path).read_text(encoding="utf-8").lower() for path in sorted(NEW_SOURCE))
        for prohibited in (
            "import requests", "import httpx", "import sqlalchemy", "import fastapi",
            "import subprocess", "message_broker", "network_api", "cloud_transport",
            "vae_runtime", "delegation_runtime", "comfyui", "gpu_execution",
            "execute_phase", "workflow_runtime", "control_tower",
        ):
            self.assertNotIn(prohibited, joined)
        self.assertFalse(any((ROOT / name).exists() for name in ("requirements.txt", "poetry.lock", "package-lock.json")))


if __name__ == "__main__":
    unittest.main()
