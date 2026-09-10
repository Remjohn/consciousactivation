from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml


REPO = Path(__file__).resolve().parents[2]
REF = REPO / "docs/cae/CAE_Production_Reference/M0078_shot_grammar_reference.yaml"
LOCAL_SEEDANCE_SOURCE = (
    REPO
    / "engines/video/openchatcut/upstream/src/agent/skills/video-gen/references/seedance2.md"
)


def load_reference() -> dict:
    data = yaml.safe_load(REF.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_happy_path_reference_shot_is_deterministically_valid():
    data = load_reference()
    shot = data["test_vectors"]["success"]

    assert shot["end_seconds"] > shot["start_seconds"]
    assert shot["duration_seconds"] == pytest.approx(
        shot["end_seconds"] - shot["start_seconds"]
    )
    assert shot["asset_refs"]
    assert shot["assistant_target_ids"]


def test_good_looking_but_wrong_shot_is_rejected_by_timing_invariant():
    data = load_reference()
    shot = data["test_vectors"]["good_looking_but_wrong"]

    declared_duration = shot["duration_seconds"]
    window_duration = shot["end_seconds"] - shot["start_seconds"]

    # The shot could look perfectly plausible to a reviewer, but the timing
    # contract is still invalid. The mismatch must be caught deterministically.
    assert declared_duration != window_duration


def test_external_sources_cannot_be_declared_semantic_authority():
    data = load_reference()
    forbidden_authorities = {
        source["source_id"]
        for source in data["source_attribution"]
        if source.get("authority") in {"SEMANTIC_AUTHORITY", "PROGRAM_AUTHORITY"}
    }
    assert forbidden_authorities == set()
    assert data["authority_boundary"]["external_sources"] == "behavioral_reference_only"
    assert data["authority_boundary"]["prompt_as_authority"] is False


def test_seedance_local_source_is_present_and_source_commit_gap_is_explicit():
    data = load_reference()
    assert LOCAL_SEEDANCE_SOURCE.is_file()

    source = next(
        item for item in data["source_attribution"]
        if item["source_id"] == "seedance2_openchatcut_adapter"
    )

    # The archive contains the exact source file, but not the upstream Git
    # metadata. We must not invent a commit SHA.
    assert source["source_commit"] == "UNVERIFIED_FROM_ARCHIVE"
    assert source["local_source_verified"] is True


def test_malformed_source_metadata_is_rejected():
    data = load_reference()
    source = data["source_attribution"][0]

    malformed = dict(source)
    malformed["exact_path"] = ""

    assert malformed["exact_path"] == ""
    with pytest.raises(AssertionError):
        assert malformed["exact_path"], "source path is required"


def test_reference_registry_round_trip_is_stable():
    first = load_reference()
    canonical_first = json.dumps(
        first, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    second = yaml.safe_load(yaml.safe_dump(first, sort_keys=False, allow_unicode=True))
    canonical_second = json.dumps(
        second, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )

    assert hashlib.sha256(canonical_first.encode()).hexdigest() == hashlib.sha256(
        canonical_second.encode()
    ).hexdigest()


def test_assistant_targeting_is_explicit_not_selection_implicit():
    data = load_reference()
    adopted = data["source_behavior_adopted"]["waoowaoo"]

    assert any("assistant discussion/refinement is an explicit interaction" in item.lower() for item in adopted)
    assert any("canvas selection" in item.lower() for item in adopted)
    assert data["state_transition_contract"]["error_route"].startswith("reject")
