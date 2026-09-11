"""M0090 acceptance tests for governed SAM3 TrackingSession state."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import types
from pathlib import Path

import pytest

# The uploaded runtime image does not include the repository's PostgreSQL client
# dependency. Load this CAE tracking module directly in that narrow test-only
# condition; production imports still resolve through the normal ca_runtime package.
if importlib.util.find_spec("psycopg") is None:
    runtime_src = Path(__file__).resolve().parents[2] / "packages" / "ca_runtime" / "src"
    pkg = types.ModuleType("ca_runtime")
    pkg.__path__ = [str(runtime_src / "ca_runtime")]
    sys.modules["ca_runtime"] = pkg
    spec = importlib.util.spec_from_file_location(
        "ca_runtime.tracking_session", runtime_src / "ca_runtime" / "tracking_session.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["ca_runtime.tracking_session"] = module
    spec.loader.exec_module(module)

from ca_runtime.tracking_session import (
    BBoxGeometry,
    TrackFrame,
    TrackSegment,
    TrackingAuthorizationError,
    TrackingAuthorityError,
    TrackingFeedbackDecision,
    TrackingIdempotencyConflictError,
    TrackingPrompt,
    TrackingPromptKind,
    TrackingRevisionStatus,
    TrackingSessionStore,
    TrackingStaleRevisionError,
    TrackingTarget,
    TrackingPromotionError,
    PointGeometry,
    project_openchatcut_tracking,
    project_storyboard_bbox,
)
from engines.intelligence.vision.sam3.adapter import (
    Sam3RuntimeContractError,
    Sam3TrackingAdapter,
)


def _sha(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _store() -> TrackingSessionStore:
    return TrackingSessionStore(operator_authorizer=lambda workspace_id, actor_id: actor_id.startswith("operator-"))


def _target() -> TrackingTarget:
    return TrackingTarget(
        target_id="target-speaker-01",
        target_ref="speaker-01",
        operator_id="operator-chief",
        label="selected speaker",
    )


def _prompt(frame_index: int = 10) -> TrackingPrompt:
    return TrackingPrompt(
        prompt_id="prompt-01",
        target_id="target-speaker-01",
        kind=TrackingPromptKind.BOX,
        frame_index=frame_index,
        source_frame_sha256=_sha(f"frame-{frame_index}"),
        box=BBoxGeometry(x_bps=2500, y_bps=2000, width_bps=2500, height_bps=4000),
    )


def _segment() -> TrackSegment:
    return TrackSegment(
        segment_id="segment-01",
        target_id="target-speaker-01",
        start_frame=10,
        end_frame=11,
        frames=[
            TrackFrame(
                frame_index=10,
                source_frame_sha256=_sha("frame-10"),
                confidence_bps=9400,
                bbox=BBoxGeometry(x_bps=2500, y_bps=2000, width_bps=2500, height_bps=4000),
            ),
            TrackFrame(
                frame_index=11,
                source_frame_sha256=_sha("frame-11"),
                confidence_bps=9300,
                bbox=BBoxGeometry(x_bps=2600, y_bps=2000, width_bps=2500, height_bps=4000),
            ),
        ],
    )


def _session(store: TrackingSessionStore):
    return store.create_session(
        workspace_id="ws-m0090",
        canonical_context_ref="storyboard-session-01",
        source_uri="evidence://interview-01/video.mp4",
        source_media_sha256=_sha("media"),
        width_px=1920,
        height_px=1080,
        frame_count=60,
        frame_rate_milli_fps=30000,
        target=_target(),
        actor_id="operator-chief",
        session_id="tracking-session-01",
    )


def test_happy_path_requires_operator_promotion_and_exposes_governed_geometry():
    store = _store()
    session = _session(store)
    create_receipts = store.list_receipts(session.workspace_id, session.session_id)
    assert create_receipts[0].operation == "CREATE_SESSION"
    assert create_receipts[0].postcondition_status == "DRAFT"
    assert create_receipts[0].validator_result == "PASS"
    revision = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        target=session.target,
        prompts=[_prompt()],
        segments=[_segment()],
        author_id="operator-chief",
        base_revision_id=None,
        idempotency_key="seed-01",
    )
    with pytest.raises(TrackingPromotionError):
        project_storyboard_bbox(revision, source_media_sha256=session.source_media_sha256)

    store.record_feedback(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        revision_id=revision.revision_id,
        operator_id="operator-chief",
        decision=TrackingFeedbackDecision.GOOD,
        note="Target confirmed in preview.",
    )
    accepted_id = store.get_session(session.workspace_id, session.session_id).latest_revision_id
    assert accepted_id != revision.revision_id
    accepted = store.get_revision(session.workspace_id, session.session_id, accepted_id)
    assert accepted.status == TrackingRevisionStatus.ACCEPTED
    receipt_ops = [receipt.operation for receipt in store.list_receipts(session.workspace_id, session.session_id)]
    assert receipt_ops == ["CREATE_SESSION", "SAVE_REVISION", "FEEDBACK_GOOD"]
    assert accepted.source_media_sha256 == session.source_media_sha256
    assert accepted.canonical_sha256
    assert store.get_revision(session.workspace_id, session.session_id, revision.revision_id).status == TrackingRevisionStatus.PROPOSED
    storyboard = project_storyboard_bbox(accepted, source_media_sha256=session.source_media_sha256)
    openchatcut = project_openchatcut_tracking(
        accepted,
        source_media_sha256=session.source_media_sha256,
        video_width_px=session.width_px,
        video_height_px=session.height_px,
    )
    assert storyboard.frames[0].x_bps == 2500
    assert openchatcut.regions[0].x_px == 480
    assert openchatcut.regions[0].source_frame_sha256 == _sha("frame-10")
    with pytest.raises(TrackingPromotionError, match="source media hash"):
        project_storyboard_bbox(accepted, source_media_sha256=_sha("different-media"))


def test_good_looking_but_wrong_target_is_rejected_without_mutating_session():
    store = _store()
    session = _session(store)
    wrong_target = _target().model_copy(update={"target_ref": "speaker-02"})
    with pytest.raises(Exception, match="does not match"):
        store.save_revision(
            workspace_id=session.workspace_id,
            session_id=session.session_id,
            target=wrong_target,
            prompts=[_prompt()],
            segments=[_segment()],
            author_id="operator-chief",
            base_revision_id=None,
            idempotency_key="wrong-target",
        )
    assert store.list_revisions(session.workspace_id, session.session_id) == []
    assert store.get_session(session.workspace_id, session.session_id).status == "DRAFT"


def test_unauthorized_operator_and_cross_workspace_write_fail_closed():
    store = _store()
    with pytest.raises(TrackingAuthorizationError):
        store.create_session(
            workspace_id="ws-m0090",
            canonical_context_ref="storyboard-session-01",
            source_uri="evidence://interview-01/video.mp4",
            source_media_sha256=_sha("media"),
            width_px=1920,
            height_px=1080,
            frame_count=60,
            frame_rate_milli_fps=30000,
            target=_target().model_copy(update={"operator_id": "model"}),
            actor_id="model",
        )

    session = _session(store)
    with pytest.raises(TrackingAuthorityError):
        store.save_revision(
            workspace_id="ws-other",
            session_id=session.session_id,
            target=session.target,
            prompts=[_prompt()],
            segments=[_segment()],
            author_id="operator-chief",
            base_revision_id=None,
        )


def test_stale_revision_is_rejected_without_second_revision():
    store = _store()
    session = _session(store)
    first = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        target=session.target,
        prompts=[_prompt(10)],
        segments=[_segment()],
        author_id="operator-chief",
        base_revision_id=None,
        idempotency_key="r1",
    )
    second = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        target=session.target,
        prompts=[_prompt(12)],
        segments=[_segment()],
        author_id="operator-chief",
        base_revision_id=first.revision_id,
        idempotency_key="r2",
    )
    with pytest.raises(TrackingStaleRevisionError):
        store.save_revision(
            workspace_id=session.workspace_id,
            session_id=session.session_id,
            target=session.target,
            prompts=[_prompt(14)],
            segments=[_segment()],
            author_id="operator-chief",
            base_revision_id=first.revision_id,
            idempotency_key="stale",
        )
    assert [r.revision_id for r in store.list_revisions(session.workspace_id, session.session_id)] == [
        first.revision_id,
        second.revision_id,
    ]


def test_malformed_source_hash_and_geometry_are_rejected():
    with pytest.raises(ValueError):
        TrackFrame(
            frame_index=1,
            source_frame_sha256="not-a-hash",
            confidence_bps=9000,
            bbox=BBoxGeometry(x_bps=1, y_bps=1, width_bps=1, height_bps=1),
        )
    with pytest.raises(ValueError):
        BBoxGeometry(x_bps=9000, y_bps=0, width_bps=2000, height_bps=100)
    with pytest.raises(ValueError):
        TrackingPrompt(
            prompt_id="mask-01",
            target_id="target-speaker-01",
            kind=TrackingPromptKind.MASK,
            frame_index=0,
            source_frame_sha256=_sha("frame-0"),
        )


def test_idempotent_replay_returns_same_revision_and_conflict_is_detected():
    store = _store()
    session = _session(store)
    first = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        target=session.target,
        prompts=[_prompt()],
        segments=[_segment()],
        author_id="operator-chief",
        base_revision_id=None,
        idempotency_key="same-request",
        created_at="2026-09-11T00:00:00Z",
    )
    replay = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        target=session.target,
        prompts=[_prompt()],
        segments=[_segment()],
        author_id="operator-chief",
        base_revision_id=None,
        idempotency_key="same-request",
        created_at="2099-01-01T00:00:00Z",
    )
    assert replay.revision_id == first.revision_id
    assert replay.canonical_sha256 == first.canonical_sha256
    with pytest.raises(TrackingIdempotencyConflictError):
        store.save_revision(
            workspace_id=session.workspace_id,
            session_id=session.session_id,
            target=session.target,
            prompts=[_prompt(12)],
            segments=[_segment()],
            author_id="operator-chief",
            base_revision_id=None,
            idempotency_key="same-request",
        )


def test_feedback_is_append_only_and_rejected_revision_is_preserved():
    store = _store()
    session = _session(store)
    revision = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        target=session.target,
        prompts=[_prompt()],
        segments=[_segment()],
        author_id="operator-chief",
        base_revision_id=None,
    )
    store.record_feedback(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        revision_id=revision.revision_id,
        operator_id="operator-chief",
        decision=TrackingFeedbackDecision.REJECT,
        reason_category="WRONG_SUBJECT",
    )
    assert len(store.feedback(session.workspace_id, session.session_id, revision.revision_id)) == 1
    preserved = store.get_revision(session.workspace_id, session.session_id, revision.revision_id)
    assert preserved.status == TrackingRevisionStatus.PROPOSED
    assert store.get_session(session.workspace_id, session.session_id).status == "REJECTED"
    assert store.list_revisions(session.workspace_id, session.session_id)[0].revision_id == revision.revision_id



def test_operator_prompt_family_maps_to_native_tracker_without_semantic_identity_calls():
    class FakePredictor:
        def __init__(self):
            self.calls = []

        def init_state(self, *, video_path):
            self.calls.append(("init_state", video_path))
            return {}

        def add_new_points_or_box(self, inference_state, **kwargs):
            self.calls.append(("points_or_box", kwargs))

        def add_new_mask(self, inference_state, **kwargs):
            self.calls.append(("mask", kwargs))

        def propagate_in_video(self, inference_state, *, start_frame_idx):
            return []

    predictor = FakePredictor()
    adapter = Sam3TrackingAdapter(predictor, mask_loader=lambda ref: [[1]])
    adapter.start_session(runtime_session_id="runtime-02", video_path="video.mp4")
    adapter.seed(runtime_session_id="runtime-02", prompt=TrackingPrompt(
        prompt_id="p-box", target_id="target-speaker-01", kind=TrackingPromptKind.BOX, frame_index=1,
        source_frame_sha256=_sha("frame-1"),
        box=BBoxGeometry(x_bps=1000, y_bps=2000, width_bps=3000, height_bps=4000),
    ))
    adapter.seed(runtime_session_id="runtime-02", prompt=TrackingPrompt(
        prompt_id="p-point", target_id="target-speaker-01", kind=TrackingPromptKind.POINT, frame_index=2,
        source_frame_sha256=_sha("frame-2"), point=PointGeometry(x_bps=3000, y_bps=4000),
    ))
    adapter.seed(runtime_session_id="runtime-02", prompt=TrackingPrompt(
        prompt_id="p-face", target_id="target-speaker-01", kind=TrackingPromptKind.FACE, frame_index=3,
        source_frame_sha256=_sha("frame-3"), face_ref="face-selection-01",
        box=BBoxGeometry(x_bps=4000, y_bps=2000, width_bps=2000, height_bps=3000),
    ))
    adapter.seed(runtime_session_id="runtime-02", prompt=TrackingPrompt(
        prompt_id="p-mask", target_id="target-speaker-01", kind=TrackingPromptKind.MASK, frame_index=4,
        source_frame_sha256=_sha("frame-4"), mask_ref="artifact://mask-01",
    ))
    assert [call[0] for call in predictor.calls] == [
        "init_state", "points_or_box", "points_or_box", "points_or_box", "mask"
    ]
    face_call = predictor.calls[3][1]
    assert face_call["box"] == [0.4, 0.2, 0.6, 0.5]
    assert face_call["obj_id"] == 1


def test_native_adapter_records_explicit_gap_and_source_hashes():
    class FakePredictor:
        def init_state(self, *, video_path):
            return {}

        def add_new_points_or_box(self, inference_state, **kwargs):
            return None

        def add_new_mask(self, inference_state, **kwargs):
            return None

        def propagate_in_video(self, inference_state, *, start_frame_idx):
            return [
                (10, [1], None, [[[0, 1], [0, 1]]], [[0.0]]),
                (12, [1], None, [[[1, 1], [0, 1]]], [[2.0]]),
            ]

    adapter = Sam3TrackingAdapter(FakePredictor())
    adapter.start_session(runtime_session_id="runtime-03", video_path="video.mp4")
    segment = adapter.propagate(
        runtime_session_id="runtime-03", target_id="target-speaker-01", segment_id="segment-03",
        start_frame=10, end_frame=12,
        source_frame_hashes={10: _sha("frame-10"), 12: _sha("frame-12")}, width_px=2, height_px=2,
    )
    assert [frame.frame_index for frame in segment.frames] == [10, 12]
    assert segment.gaps[0].start_frame == 11 and segment.gaps[0].end_frame == 11
    assert segment.frames[0].source_frame_sha256 == _sha("frame-10")
    assert segment.frames[1].confidence_bps > segment.frames[0].confidence_bps

def test_runtime_adapter_requires_source_hash_for_real_geometry_output():
    class FakePredictor:
        def init_state(self, *, video_path):
            return {"video_path": video_path}

        def add_new_points_or_box(self, **kwargs):
            return None

        def add_new_mask(self, **kwargs):
            return None

        def propagate_in_video(self, state, *, start_frame_idx):
            return [
                (start_frame_idx, [1], None, [[[0, 1], [0, 1]]], [[0.0]]),
            ]

    adapter = Sam3TrackingAdapter(FakePredictor())
    adapter.start_session(runtime_session_id="runtime-01", video_path="video.mp4")
    with pytest.raises(Sam3RuntimeContractError, match="missing source frame hash"):
        adapter.propagate(
            runtime_session_id="runtime-01",
            target_id="target-speaker-01",
            segment_id="segment-01",
            start_frame=0,
            end_frame=0,
            source_frame_hashes={},
            width_px=2,
            height_px=2,
        )
