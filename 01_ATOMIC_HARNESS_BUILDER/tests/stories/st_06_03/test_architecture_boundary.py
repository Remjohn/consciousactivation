from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILES = (
    ROOT / "src/cmf_builder/domain/category_syntax.py",
    ROOT / "src/cmf_builder/application/syntax_commands.py",
)


def test_story_sources_do_not_import_external_runtime_or_network_clients() -> None:
    prohibited = (
        "import openai",
        "from openai",
        "import requests",
        "from requests",
        "import socket",
        "import subprocess",
        "cmf_builder.vae",
        "cmf_builder.delegation",
    )
    for path in SOURCE_FILES:
        source = path.read_text(encoding="utf-8")
        assert all(token not in source for token in prohibited)


def test_story_sources_contain_no_absolute_workspace_paths_or_certification_claims() -> None:
    for path in SOURCE_FILES:
        source = path.read_text(encoding="utf-8")
        assert "D:/Work/" not in source
        assert "D:\\Work\\" not in source
        assert "production_ready=True" not in source
        assert "certified=True" not in source


def test_command_boundary_uses_explicit_category_syntax_authority_action() -> None:
    source = SOURCE_FILES[1].read_text(encoding="utf-8")
    assert "Action.COMPILE_CATEGORY_SYNTAX" in source
    assert "Action.COMPILE_CATEGORY_PROFILES" not in source
