"""CAE-M0096 bounded certification audit.

This test deliberately stays stdlib-only so it can run in a dependency-poor archive.
It verifies the governed brownfield path and the live proof gates without fabricating
runtime/media evidence. It is an audit/control test, not a replacement for live
campaign execution or operator visual approval.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_m067():
    path = ROOT / "tests" / "e2e" / "m067_real_campaign_harness.py"
    spec = importlib.util.spec_from_file_location("m067_real_campaign_harness", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_m0096_current_authority_equivalents_match_precedence_hashes() -> None:
    precedence_path = ROOT / "governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml"
    constitution_path = ROOT / "governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md"
    precedence = precedence_path.read_text(encoding="utf-8")

    assert not (ROOT / "docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md").exists()
    assert not (ROOT / "governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml").exists()
    assert constitution_path.exists()
    assert "  document: docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md" in precedence
    assert "  sha256: 21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b" in precedence
    expected_hash = precedence.split("  sha256:", 1)[1].splitlines()[0].strip()
    assert sha256_file(constitution_path) == expected_hash

    authority_pack = ROOT / "docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10"
    expected = {
        "00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md",
        "01_CAE_Product_Update_Visual_Asset_Editor.md",
        "02_CAE_PRD_Update_Visual_Asset_Studio.md",
        "03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md",
    }
    assert {p.name for p in authority_pack.iterdir() if p.is_file()} >= expected


def test_m0096_reuses_canonical_visual_path_and_false_proof_countercase() -> None:
    required = [
        "packages/ca_runtime/src/ca_runtime/storyboard_session.py",
        "packages/ca_runtime/src/ca_runtime/storyboard_programs.py",
        "packages/ca_runtime/src/ca_runtime/transformation_recipe.py",
        "api/routers/visual_studio.py",
        "api/services/visual_studio_contracts.py",
        "tests/cae/test_m0079_storyboard_session_revision.py",
        "tests/e2e/m067_real_campaign_harness.py",
        "tests/phase6/test_m065_openchatcut_runtime.py",
    ]
    for rel in required:
        assert (ROOT / rel).is_file(), rel

    session = read(required[0])
    visual_studio = read("api/routers/visual_studio.py")
    m0079 = read("tests/cae/test_m0079_storyboard_session_revision.py")
    m0083 = read("docs/cae/specs/M0083/M0083_EVIDENCE_RECEIPT.json")

    assert "FeedbackDecision.GOOD" in session
    assert "immutable" in session
    assert '"studio_path": ["RETRIEVE", "TRANSFORM", "COMPOSE", "GENERATE"]' in visual_studio
    assert "test_good_looking_but_ungrounded_asset_is_blocked" in m0079
    assert all(token in m0083 for token in ("RETRIEVE", "TRANSFORM", "COMPOSE", "GENERATE"))
    assert "No model output, arbitrary effect dictionary, free-form operation name" in read(
        "docs/cae/specs/M0083/TRANSFORMATION_INTENT_RECIPE_SPEC.md"
    )


def test_m0096_live_precondition_gate_fails_closed_in_current_environment() -> None:
    m067 = load_m067()
    fidelity = m067.environment_fidelity()

    assert fidelity["git"]["git_metadata_present"] is False
    assert fidelity["git"]["git_commit_sha"] is None
    assert fidelity["source_media"]["present"] is False
    assert fidelity["openchatcut"]["reachable"] is False

    with pytest.raises(m067.M067Blocked):
        m067.require_live_environment()


def test_m0096_source_media_policy_does_not_promote_synthetic_fixtures() -> None:
    media = sorted((ROOT / "tests").rglob("*.mp4"))
    assert media, "Expected the snapshot's known media fixture inventory to be inspectable."
    assert all("synthetic" in p.name.lower() or "corrupt" in p.name.lower() or p.stat().st_size == 0 for p in media)


def test_m0096_external_runtime_mapping_is_downstream_only() -> None:
    local_visual = read("engines/video/openchatcut/upstream/package.json")
    assert '"license": "AGPL-3.0-or-later"' in local_visual
    edit_source = read("engines/video/openchatcut/upstream/src/agent/tools/edit-item-visual.ts")
    geometry_source = read("engines/video/openchatcut/upstream/src/editor/visualFrameGeometry.ts")
    assert "clamp" in edit_source.lower()
    assert "border" in geometry_source.lower() or "radius" in geometry_source.lower()
    mapping = read("docs/cae/evidence/M0096/M0096_UPSTREAM_TO_CAE_MAPPING.md")
    assert "https://github.com/0xsline/OpenChatCut" in mapping
