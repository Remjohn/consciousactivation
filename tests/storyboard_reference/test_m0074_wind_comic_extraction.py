from copy import deepcopy

import pytest

from engines.storyboard.references.wind_comic.reference_adapter import (
    AdapterValidationError,
    SketchLock,
    append_feedback,
    audit_timeline,
    compile_roundtrip_proposal,
    export_pull_sheet,
    merge_pull_sheet,
    parse_roundtrip_csv,
    validate_scene_consistency,
)


BASELINE = [
    {
        "shotNumber": 1,
        "sceneDescription": "hero enters room",
        "scene": "room",
        "characters": ["hero"],
        "duration": 3,
        "composition": "wide",
        "cameraAngle": "eye-level",
        "cameraMovement": "push-in",
        "startSec": 0,
        "endSec": 3,
        "styleAnchorRef": "style:001",
        "sceneAnchorRef": "scene:room:v1",
    },
    {
        "shotNumber": 2,
        "sceneDescription": "door closes",
        "scene": "room",
        "characters": ["hero"],
        "duration": 2,
        "composition": "medium",
        "cameraAngle": "eye-level",
        "cameraMovement": "static",
        "startSec": 3,
        "endSec": 5,
        "styleAnchorRef": "style:001",
        "sceneAnchorRef": "scene:room:v1",
    },
]


def test_round_trip_success_and_idempotence():
    csv_text = export_pull_sheet(BASELINE)
    rows = parse_roundtrip_csv(csv_text)
    proposal, changes, unknown = merge_pull_sheet(BASELINE, rows)
    assert proposal == BASELINE
    assert changes == []
    assert unknown == []
    assert export_pull_sheet(proposal) == csv_text


def test_round_trip_good_looking_but_wrong_edit_is_explicitly_detected():
    csv_text = export_pull_sheet(BASELINE)
    csv_text = csv_text.replace("push-in", "whip-pan", 1)
    rows = parse_roundtrip_csv(csv_text)
    proposal, changes, unknown = merge_pull_sheet(BASELINE, rows)
    assert unknown == []
    assert proposal[0]["cameraMovement"] == "whip-pan"
    assert changes == [{"shotNumber": 1, "field": "cameraMovement", "from": "push-in", "to": "whip-pan"}]
    # The edit can look visually plausible, but is still a governed proposal and
    # does not become a canonical state mutation inside this adapter.
    assert BASELINE[0]["cameraMovement"] == "push-in"


def test_timeline_rejects_plausible_but_wrong_overlap():
    result = audit_timeline([
        {"shotNumber": 1, "duration": 3, "startSec": 0, "endSec": 3},
        {"shotNumber": 2, "duration": 2, "startSec": 2.5, "endSec": 4.5},
    ])
    assert not result["ok"]
    assert "overlap_or_backtrack:S1->S2" in result["errors"]


def test_timeline_success_is_replay_stable():
    result = audit_timeline(BASELINE)
    replay = audit_timeline(BASELINE)
    assert result == replay
    assert result["ok"]
    assert result["totalDurationSec"] == 5


def test_negative_malformed_duration_is_blocked():
    rows = parse_roundtrip_csv(export_pull_sheet(BASELINE))
    rows[0]["fields"]["duration"] = "-2"
    with pytest.raises(AdapterValidationError, match="duration must be positive"):
        merge_pull_sheet(BASELINE, rows)


def test_unknown_shot_is_reported_not_created():
    edited = export_pull_sheet(BASELINE) + ""
    edited = edited.rstrip("\n") + "\n3," + ("," * 17) + "\n"
    rows = parse_roundtrip_csv(edited)
    proposal, changes, unknown = merge_pull_sheet(BASELINE, rows)
    assert 3 in unknown
    assert len(proposal) == 2
    assert changes == []


def test_sketch_lock_validates_lineage_and_fails_closed():
    lock = SketchLock(
        shot_number=1,
        sketch_ref="artifact://sketch/S1",
        source_sha256="a" * 64,
        style_anchor_ref="style:001",
        scene_anchor_ref="scene:room:v1",
    )
    lock.validate()
    with pytest.raises(AdapterValidationError, match="source_sha256"):
        SketchLock(shot_number=1, sketch_ref="x", source_sha256="bad").validate()


def test_scene_consistency_requires_canonical_anchors():
    assert validate_scene_consistency(
        BASELINE,
        required_style_anchor_ref="style:001",
        scene_anchor_by_name={"room": "scene:room:v1"},
    )["ok"]

    wrong = deepcopy(BASELINE)
    wrong[1]["sceneAnchorRef"] = "scene:other:v1"
    report = validate_scene_consistency(
        wrong,
        required_style_anchor_ref="style:001",
        scene_anchor_by_name={"room": "scene:room:v1"},
    )
    assert not report["ok"]
    assert "scene_anchor_mismatch:S2" in report["errors"]


def test_feedback_is_append_only_and_input_unchanged():
    history = [{"revisionId": "r1", "feedback": "keep"}]
    original = deepcopy(history)
    updated = append_feedback(
        history,
        revision_id="r2",
        actor_id="operator-1",
        target_ref="shot:2",
        feedback="tighten timing",
        created_at="2026-09-10T15:00:00Z",
    )
    assert history == original
    assert len(updated) == 2
    with pytest.raises(AdapterValidationError, match="already exists"):
        append_feedback(
            updated,
            revision_id="r2",
            actor_id="operator-1",
            target_ref="shot:2",
            feedback="duplicate",
            created_at="2026-09-10T15:01:00Z",
        )


def test_roundtrip_proposal_requires_authorization_and_fresh_baseline():
    rows = parse_roundtrip_csv(export_pull_sheet(BASELINE))
    digest = "d" * 64
    with pytest.raises(AdapterValidationError, match="authorization"):
        compile_roundtrip_proposal(
            BASELINE, rows, expected_baseline_digest=digest, current_baseline_digest=digest, operator_authorized=False
        )
    with pytest.raises(AdapterValidationError, match="stale"):
        compile_roundtrip_proposal(
            BASELINE, rows, expected_baseline_digest="a" * 64, current_baseline_digest=digest, operator_authorized=True
        )
    result = compile_roundtrip_proposal(
        BASELINE, rows, expected_baseline_digest=digest, current_baseline_digest=digest, operator_authorized=True
    )
    assert result["requires_promotion"] is True
    assert result["changes"] == []
