from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCES = (
    ROOT / "src/cmf_builder/domain/category_runtime_rules.py",
    ROOT / "src/cmf_builder/application/category_policy_commands.py",
)


def test_sources_have_no_external_runtime_network_or_transport_imports() -> None:
    prohibited = (
        "import openai",
        "from openai",
        "import requests",
        "import socket",
        "import subprocess",
        "visual_asset_editor",
        "delegation.runtime",
    )
    for path in SOURCES:
        source = path.read_text(encoding="utf-8")
        assert all(token not in source for token in prohibited)


def test_sources_use_exact_authority_and_do_not_claim_production() -> None:
    command_source = SOURCES[1].read_text(encoding="utf-8")
    assert "Action.COMPILE_CATEGORY_POLICY" in command_source
    assert "production_ready=True" not in command_source
    assert "certified=True" not in command_source
    for path in SOURCES:
        source = path.read_text(encoding="utf-8")
        assert "D:/Work/" not in source
        assert "D:\\Work\\" not in source


def test_runtime_rules_are_declarative_and_do_not_execute_workflows() -> None:
    domain_source = SOURCES[0].read_text(encoding="utf-8")
    assert "runtime_plan_requirements" in domain_source
    assert "external_runtime_execution" in domain_source
    assert "def execute(" not in domain_source
    assert "def run(" not in domain_source
