"""M0082 focused tests for deterministic editorial expression calculus."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "packages"
    / "ca_runtime"
    / "src"
    / "ca_runtime"
    / "editorial_expression_calculus.py"
)
_SPEC = importlib.util.spec_from_file_location("cae_m0082_editorial_expression_calculus", MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
import sys

_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

NarrativeEditingGrammar = _MODULE.NarrativeEditingGrammar
compile_editorial_expression = _MODULE.compile_editorial_expression
get_editorial_expression_profile = _MODULE.get_editorial_expression_profile


def _grammar(**overrides):
    payload = {
        "format_id": "VIDEO",
        "scene_kind": "EVIDENCE",
        "rhythm": "STEADY",
        "attention": "FOCUS",
        "information": "PROVE",
        "texture": "CLEAN",
        "captioning": "SUPPORTIVE",
        "source_evidence_refs": ("evidence:seg-01", "evidence:asset-01"),
        "source_quality": "HIGH",
    }
    payload.update(overrides)
    return NarrativeEditingGrammar(**payload)


def test_success_is_bounded_and_replay_deterministic():
    grammar = _grammar()

    first = compile_editorial_expression(grammar)
    second = compile_editorial_expression(grammar)

    assert first == second
    assert first.canonical_sha256 == second.canonical_sha256
    assert first.source_evidence_refs == grammar.source_evidence_refs
    assert first.shot_duration_ms == first.cut_interval_ms
    assert 0 <= first.pace_bps <= 10_000
    assert 0 <= first.occupancy_bps <= 10_000
    assert 0 <= first.visual_density_bps <= 10_000
    assert 0 <= first.caption_density_bps <= 10_000
    assert 0 <= first.contrast_bps <= 10_000
    assert 0 <= first.salience_bps <= 10_000
    assert 0 <= first.intervention_frequency_per_minute <= 12


def test_format_and_scene_profile_selection_is_deterministic_and_distinct():
    evidence = _grammar()
    video = compile_editorial_expression(evidence)
    presentation = compile_editorial_expression(
        _grammar(format_id="PRESENTATION", scene_kind="EVIDENCE")
    )
    pivot = compile_editorial_expression(_grammar(scene_kind="PIVOT"))

    assert video.profile_id == "M0082:VIDEO:EVIDENCE"
    assert presentation.profile_id == "M0082:PRESENTATION:EVIDENCE"
    assert pivot.profile_id == "M0082:VIDEO:PIVOT"
    assert presentation.profile_id != video.profile_id
    assert pivot.profile_id != video.profile_id
    assert video.salience_bps != pivot.salience_bps


def test_all_supported_format_scene_profiles_compile_within_declared_bounds():
    formats = ("VIDEO", "CAROUSEL", "SUPERVISUAL", "PRESENTATION")
    scenes = ("OPENING", "EXPOSITION", "EVIDENCE", "PIVOT", "CLIMAX", "RESOLUTION")

    for format_id in formats:
        for scene_kind in scenes:
            grammar = _grammar(format_id=format_id, scene_kind=scene_kind)
            expression = compile_editorial_expression(grammar)
            profile = get_editorial_expression_profile(format_id, scene_kind)
            assert profile.profile_id == expression.profile_id
            assert profile.shot_duration_ms.minimum <= expression.shot_duration_ms <= profile.shot_duration_ms.maximum
            assert profile.hold_duration_ms.minimum <= expression.hold_duration_ms <= profile.hold_duration_ms.maximum
            assert profile.occupancy_bps.minimum <= expression.occupancy_bps <= profile.occupancy_bps.maximum
            assert profile.scale_bps.minimum <= expression.scale_bps <= profile.scale_bps.maximum
            assert profile.motion_amplitude_bps.minimum <= expression.motion_amplitude_bps <= profile.motion_amplitude_bps.maximum
            assert profile.motion_velocity_bps_per_second.minimum <= expression.motion_velocity_bps_per_second <= profile.motion_velocity_bps_per_second.maximum
            assert profile.visual_density_bps.minimum <= expression.visual_density_bps <= profile.visual_density_bps.maximum
            assert profile.caption_density_bps.minimum <= expression.caption_density_bps <= profile.caption_density_bps.maximum
            assert profile.contrast_bps.minimum <= expression.contrast_bps <= profile.contrast_bps.maximum
            assert profile.salience_bps.minimum <= expression.salience_bps <= profile.salience_bps.maximum
            assert profile.intervention_frequency_per_minute.minimum <= expression.intervention_frequency_per_minute <= profile.intervention_frequency_per_minute.maximum


def test_good_looking_but_wrong_source_quality_fails_closed():
    with pytest.raises(ValueError, match="source_quality must be one of"):
        _grammar(source_quality="UNKNOWN")

    with pytest.raises(ValueError, match="source_quality must be one of"):
        _grammar(source_quality="LOW")


def test_missing_or_duplicate_evidence_is_rejected():
    with pytest.raises(ValueError, match="source_evidence_refs"):
        NarrativeEditingGrammar(
            format_id="VIDEO",
            scene_kind="EVIDENCE",
            source_evidence_refs=(),
            source_quality="HIGH",
        )

    with pytest.raises(ValueError, match="unique"):
        _grammar(source_evidence_refs=("evidence:seg-01", "evidence:seg-01"))


def test_unsupported_profile_fails_closed():
    with pytest.raises(_MODULE.EditorialExpressionProfileError, match="no editorial expression profile"):
        get_editorial_expression_profile("UNKNOWN", "EVIDENCE")

    # The public profile lookup is deterministic and returns the same object
    # for repeated requests, so downstream compilers cannot observe mutation.
    first = get_editorial_expression_profile("VIDEO", "EVIDENCE")
    second = get_editorial_expression_profile("VIDEO", "EVIDENCE")
    assert first == second


def test_clean_expression_changes_when_grammar_changes_but_remains_bounded():
    steady = compile_editorial_expression(_grammar(rhythm="STEADY"))
    accelerated = compile_editorial_expression(_grammar(rhythm="ACCELERATE"))

    assert accelerated.pace_bps > steady.pace_bps
    assert accelerated.shot_duration_ms < steady.shot_duration_ms
    assert accelerated.motion_amplitude_bps >= steady.motion_amplitude_bps
    assert 0 <= accelerated.pace_bps <= 10_000


def test_compile_rejects_source_quality_that_cannot_be_reached():
    # The model validates the source-quality floor before any expression is emitted.
    with pytest.raises(ValueError, match="source_quality must be one of"):
        _grammar(source_quality="UNVERIFIED")
