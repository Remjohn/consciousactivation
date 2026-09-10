from __future__ import annotations

import pytest

from programs.visual_derivative_production_program.reference.arc_reel_review_adapter import (
    AdapterContractError,
    ArcReelObservedAction,
    ArcReelReviewEvent,
    CAETarget,
    map_arcreel_review_event,
    replay_fingerprint,
)


def _event(**overrides):
    payload = dict(
        interaction_id="interaction:001",
        action=ArcReelObservedAction.APPROVE,
        project_ref="ref:project:001",
        stage="storyboard_review",
        actor_id="operator:alice",
        actor_type="human",
        storyboard_id="storyboard:001",
        source_evidence_refs=("evidence:001",),
        source_artifact_ref="artifact:001",
        expected_state_version=7,
        observed_state_version=7,
        operator_approved=True,
    )
    payload.update(overrides)
    return ArcReelReviewEvent(**payload)


def test_happy_path_review_maps_to_existing_operator_gate():
    mapped = map_arcreel_review_event(_event())
    assert mapped.target is CAETarget.OPERATOR_GATE
    assert mapped.canonical_operation == "approve_existing_canonical_gate"
    assert mapped.required_lane == "COMMANDER"
    assert mapped.requires_operator_gate is True
    assert mapped.preserve_provenance is True
    assert len(mapped.mapping_sha256) == 64


def test_good_looking_but_wrong_generation_without_evidence_is_rejected():
    event = _event(
        action=ArcReelObservedAction.REGENERATE,
        operator_approved=True,
        generation_requested=True,
        source_evidence_refs=(),
    )
    with pytest.raises(AdapterContractError, match="evidence lineage"):
        map_arcreel_review_event(event)


def test_unauthorized_mutation_is_rejected():
    event = _event(
        action=ArcReelObservedAction.EDIT,
        operator_approved=False,
        semantic_revision_requested=True,
    )
    with pytest.raises(AdapterContractError, match="operator approval"):
        map_arcreel_review_event(event)


def test_non_human_actor_cannot_progress_operator_review():
    event = _event(actor_type="model_program")
    with pytest.raises(AdapterContractError, match="actor_type=human"):
        map_arcreel_review_event(event)


def test_stale_state_is_rejected_before_mapping():
    event = _event(expected_state_version=6, observed_state_version=7)
    with pytest.raises(AdapterContractError, match="stale state"):
        map_arcreel_review_event(event)


def test_edit_and_regenerate_remain_distinct_contracts():
    edit = map_arcreel_review_event(
        _event(
            action=ArcReelObservedAction.EDIT,
            semantic_revision_requested=False,
            generation_requested=False,
        )
    )
    regen = map_arcreel_review_event(
        _event(
            action=ArcReelObservedAction.REGENERATE,
            generation_requested=True,
        )
    )
    assert edit.canonical_operation == "compile_existing_revision_program"
    assert regen.canonical_operation == "request_operator_constrained_regeneration"
    assert edit.canonical_operation != regen.canonical_operation


def test_timeline_inspection_is_read_only_and_projection_backed():
    mapped = map_arcreel_review_event(
        _event(
            action=ArcReelObservedAction.INSPECT_TIMELINE,
            operator_approved=False,
            source_evidence_refs=(),
            source_artifact_ref=None,
            canvas_projection_ref="ref:timeline_projection:001",
        )
    )
    assert mapped.target is CAETarget.TIMELINE_PROJECTION
    assert mapped.requires_operator_gate is False
    assert "TimelineProjectionModel" in mapped.notes[0]


def test_replay_is_deterministic_and_idempotent():
    event = _event(action=ArcReelObservedAction.REVIEW, operator_approved=False)
    first = map_arcreel_review_event(event)
    second = map_arcreel_review_event(event)
    assert first == second
    assert replay_fingerprint(event) == replay_fingerprint(event)


def test_malformed_project_ref_is_rejected():
    with pytest.raises(AdapterContractError, match="canonical ref"):
        map_arcreel_review_event(_event(project_ref="project-001"))
