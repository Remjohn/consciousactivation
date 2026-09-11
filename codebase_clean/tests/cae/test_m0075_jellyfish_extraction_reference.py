"""M0075 bounded tests for the Jellyfish-to-CAE reference mapping."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "docs/cae/CAE_Visual_Production_Storyboard_Extraction_M0075_v1"
MAPPING = BUNDLE / "M0075_JELLYFISH_MAPPING.json"


def _mapping() -> dict:
    return json.loads(MAPPING.read_text(encoding="utf-8"))


def test_successful_mapping_binds_to_existing_cae_authority() -> None:
    data = _mapping()
    paths = {entry["upstream_path"] for entry in data["adopted_behaviors"]}
    assert "backend/app/services/studio/shot_preparation_state.py" in paths
    assert "backend/app/services/studio/shot_extracted_candidates.py" in paths
    assert "backend/app/services/studio/shot_assets.py" in paths
    assert "EditorialStoryboardRecord" in data["concept_mapping"]["StoryboardSession"]["cae_authority"]
    assert data["concept_mapping"]["StoryboardRevision"]["cae_authority"] == ["GraphRevisionRecord"]


def test_good_looking_but_wrong_preview_cannot_promote_semantics() -> None:
    data = _mapping()
    counterexample = data["anti_centroid"]["good_looking_but_wrong"]
    assert "not tied to the approved evidence/asset lineage" in counterexample
    expected = data["anti_centroid"]["expected_result"]
    assert "promotion remains blocked" in expected
    assert "provenance" in expected


def test_negative_controls_require_explicit_exclusions_and_stale_route() -> None:
    data = _mapping()
    exclusions = set(data["excluded_behavior"])
    assert "generation runtime and task execution" in exclusions
    assert "parallel authoritative storyboard state model" in exclusions
    assert data["revision_and_operator_mapping"]["edit"]["error_route"] == "StaleBaseRevisionError"


def test_reference_validator_passes() -> None:
    from importlib.util import module_from_spec, spec_from_file_location

    module_path = BUNDLE / "validate_m0075_extraction.py"
    spec = spec_from_file_location("m0075_validator", module_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate()


def test_no_upstream_code_was_copied() -> None:
    copied_roots = [ROOT / "engines/storyboard/references/jellyfish"]
    for copied_root in copied_roots:
        if copied_root.exists():
            files = [p for p in copied_root.rglob("*") if p.is_file()]
            pytest.fail(f"M0075 reference extraction unexpectedly copied upstream code: {files}")

