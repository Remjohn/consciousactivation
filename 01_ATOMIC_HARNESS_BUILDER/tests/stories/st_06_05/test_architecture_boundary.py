from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCES = (
    ROOT / "src/cmf_builder/domain/conversational_feedback.py",
    ROOT / "src/cmf_builder/application/conversational_commands.py",
)


def test_sources_do_not_import_external_runtime_network_or_storage_clients() -> None:
    prohibited = (
        "import openai",
        "import requests",
        "import socket",
        "import subprocess",
        "import sqlite3",
        "visual_asset_editor",
        "delegation.runtime",
    )
    for path in SOURCES:
        source = path.read_text(encoding="utf-8")
        assert all(token not in source for token in prohibited)


def test_no_actual_human_payload_or_evidence_issuance_surface_exists() -> None:
    domain_source = SOURCES[0].read_text(encoding="utf-8")
    assert "response_payload_permitted=False" in domain_source
    assert "EXTERNAL_HUMAN_CAPTURE_AUTHORITY" in domain_source
    assert "def issue_reaction_receipt" not in domain_source
    assert "def issue_expression_moment" not in domain_source
    assert "actual_human_response:" not in domain_source


def test_exact_authority_action_and_nonproduction_boundary() -> None:
    command_source = SOURCES[1].read_text(encoding="utf-8")
    assert "Action.COMPILE_CONVERSATIONAL_FEEDBACK" in command_source
    for path in SOURCES:
        source = path.read_text(encoding="utf-8")
        assert "production_ready=True" not in source
        assert "certified=True" not in source
        assert "D:/Work/" not in source
        assert "D:\\Work\\" not in source
