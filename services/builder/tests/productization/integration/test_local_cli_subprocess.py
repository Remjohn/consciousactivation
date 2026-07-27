from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[3]
GENERIC = ROOT / "tests/fixtures/productization/manifests/generic_text_summary.json"


def _run(arguments: list[str], *, database: Path):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = f"{ROOT / 'src'}{os.pathsep}{ROOT}"
    environment["CMF_BUILDER_DB"] = str(database)
    return subprocess.run(
        [sys.executable, "-m", "cmf_builder.cli", "--format", "json", *arguments],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def test_local_module_cli_persists_builds_and_exports_across_fresh_processes() -> None:
    with TemporaryDirectory() as directory_text:
        directory = Path(directory_text)
        database = directory / "state" / "builder.sqlite3"
        ingest = _run(["ingest", str(GENERIC)], database=database)
        assert ingest.returncode == 0, ingest.stderr
        manifest_id = json.loads(ingest.stdout)["artifact_id"]
        build = _run(["build", "--artifact-id", manifest_id], database=database)
        assert build.returncode == 0, build.stderr
        definition_id = json.loads(build.stdout)["artifact_id"]
        destination = directory / "export" / "generic.zip"
        export = _run(
            ["export", "--artifact-id", definition_id, "--output", str(destination)],
            database=database,
        )
        assert export.returncode == 0, export.stderr
        assert destination.is_file()
