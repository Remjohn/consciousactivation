"""M0079 acceptance tests for the canonical editable storyboard domain."""

from __future__ import annotations

import hashlib
import sqlite3

import pytest

from ca_runtime.editorial_discovery_store import (
    ContentCandidateRecord,
    EditorialDiscoveryStore,
    EditorialStoryboardRecord,
    EvidenceSegmentRecord,
)
from ca_runtime.preparation_graph_store import StaleBaseRevisionError
from ca_runtime.storyboard_session import (
    FeedbackDecision,
    MotionPlan,
    StoryboardElement,
    StoryboardRevisionValidationError,
    StoryboardScene,
    StoryboardSessionStore,
    StoryboardShot,
    TransformationIntent,
    TransformationRecipe,
    VisualAssetReference,
)


def _authoritative_store() -> EditorialDiscoveryStore:
    store = EditorialDiscoveryStore(":memory:")
    ws = "ws-m0079"
    segment_text = "The line was losing time to false alarms."
    store.insert_evidence_segment(
        EvidenceSegmentRecord(
            workspace_id=ws,
            segment_id="seg-01",
            session_id="interview-01",
            speaker="Operator",
            start_time_ms=0,
            end_time_ms=2200,
            verbatim_text=segment_text,
            boundary_type="SYNTACTIC_SENTENCE",
            text_sha256=hashlib.sha256(segment_text.encode()).hexdigest(),
        )
    )
    store.insert_content_candidate(
        ContentCandidateRecord(
            workspace_id=ws,
            candidate_id="candidate-01",
            candidate_type="PROBLEM_SOLUTION_ARC",
            title="False Alarm Triage",
            hook_statement="False alarms were costing the line time.",
            narrative_completeness="COMPLETE_ARC",
            evidence_links=[{"segment_id": "seg-01"}],
            production_status="SELECTED_FOR_PRODUCTION",
        )
    )
    store.insert_editorial_storyboard(
        EditorialStoryboardRecord(
            workspace_id=ws,
            storyboard_id="STB-M0079-01",
            candidate_id="candidate-01",
            title="False Alarm Triage",
            hook_statement="False alarms were costing the line time.",
            priority_rank=1,
            evidence_links=[{"segment_id": "seg-01"}],
            narrative_structure=[{"segment_id": "seg-01"}],
            approved_by="operator-chief",
        )
    )
    return store


def _scene(*, grounded: bool = True) -> StoryboardScene:
    evidence = ["seg-01"] if grounded else []
    element = StoryboardElement(
        element_id="element-01",
        kind="SOURCE_FRAME",
        semantic_purpose="Make the operational problem legible.",
        source_evidence_refs=evidence,
        asset_references=[
            VisualAssetReference(
                reference_id="asset-ref-01",
                asset_id="asset-conveyor-01",
                evidence_refs=evidence,
                source_quality="HIGH",
                rights_status="CLEARED",
                approved=True,
            )
        ],
        transformation_intent=TransformationIntent(
            intent_id="intent-01",
            source_element_id="element-01",
            semantic_target="Show the false alarm mechanism.",
            mode="FOCUS",
            emphasis="MECHANISM",
        ),
        transformation_recipe=TransformationRecipe(
            recipe_id="recipe-01",
            intent_id="intent-01",
            primitives=[{"op": "CROP", "region": "alarm-panel"}],
        ),
        motion_plan=MotionPlan(
            motion_plan_id="motion-01",
            duration_ms=2200,
            # CAE canonical payloads use integer fixed-point values; floats are
            # intentionally rejected by ca_contracts.canonical_sha256.
            keyframes=[{"at_ms": 0, "scale_bps": 10000}, {"at_ms": 2200, "scale_bps": 10800}],
            intensity_bps=800,
            attention_cost_bps=500,
        ),
    )
    return StoryboardScene(
        scene_id="scene-01",
        scene_order=0,
        semantic_purpose="Ground the claim in the interview evidence.",
        source_evidence_refs=evidence,
        shots=[
            StoryboardShot(
                shot_id="shot-01",
                start_ms=0,
                end_ms=2200,
                semantic_purpose="Reveal the problem.",
                shot_language={"shot_size": "MEDIUM", "camera_move": "HOLD"},
                elements=[element],
            )
        ],
    )


def test_session_revision_round_trip_and_compile_receipt():
    editorial = _authoritative_store()
    store = StoryboardSessionStore(editorial_store=editorial)
    session = store.create_session(
        workspace_id="ws-m0079",
        editorial_storyboard_id="STB-M0079-01",
        created_by="operator-chief",
        semantic_program_id="PRG-M0079-01",
        harness_id="HARNESS-VIDEO-01",
    )
    assert store.create_session(
        workspace_id=session.workspace_id,
        editorial_storyboard_id=session.editorial_storyboard_id,
        created_by="operator-chief",
        session_id=session.session_id,
    ).session_id == session.session_id

    revision = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        author_id="operator-chief",
        scenes=[_scene()],
        source_evidence_refs=["seg-01"],
        base_revision_id=None,
    )
    assert revision.revision_seq == 1
    assert store.get_revision(session.workspace_id, session.session_id, revision.revision_id).canonical_sha256 == revision.canonical_sha256

    report = store.validate_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        revision_id=revision.revision_id,
    )
    assert report.passed is True
    feedback = store.record_feedback(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        revision_id=revision.revision_id,
        operator_id="operator-chief",
        decision=FeedbackDecision.GOOD,
        note="Evidence and transformation remain legible.",
    )
    assert feedback.decision == FeedbackDecision.GOOD
    receipt = store.compile_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        revision_id=revision.revision_id,
    )
    assert receipt.editorial_storyboard_id == "STB-M0079-01"
    assert store.compile_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        revision_id=revision.revision_id,
    ).lineage_sha256 == receipt.lineage_sha256


def test_good_looking_but_ungrounded_asset_is_blocked():
    editorial = _authoritative_store()
    store = StoryboardSessionStore(editorial_store=editorial)
    session = store.create_session(
        workspace_id="ws-m0079",
        editorial_storyboard_id="STB-M0079-01",
        created_by="operator-chief",
    )
    wrong_scene = _scene()
    wrong_scene.shots[0].elements[0].asset_references[0].evidence_refs = []
    with pytest.raises(StoryboardRevisionValidationError, match="not evidence-grounded"):
        store.save_revision(
            workspace_id=session.workspace_id,
            session_id=session.session_id,
            author_id="operator-chief",
            scenes=[wrong_scene],
            source_evidence_refs=["seg-01"],
            base_revision_id=None,
        )


def test_stale_revision_and_cross_workspace_authority_fail_closed():
    editorial = _authoritative_store()
    store = StoryboardSessionStore(editorial_store=editorial)
    session = store.create_session(
        workspace_id="ws-m0079",
        editorial_storyboard_id="STB-M0079-01",
        created_by="operator-chief",
    )
    first = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        author_id="operator-chief",
        scenes=[_scene()],
        source_evidence_refs=["seg-01"],
        base_revision_id=None,
    )
    second = store.save_revision(
        workspace_id=session.workspace_id,
        session_id=session.session_id,
        author_id="operator-chief",
        scenes=[_scene()],
        source_evidence_refs=["seg-01"],
        base_revision_id=first.revision_id,
    )
    assert second.base_revision_id == first.revision_id
    with pytest.raises(StaleBaseRevisionError):
        store.save_revision(
            workspace_id=session.workspace_id,
            session_id=session.session_id,
            author_id="operator-chief",
            scenes=[_scene()],
            source_evidence_refs=["seg-01"],
            base_revision_id=first.revision_id,
        )
    with pytest.raises(Exception, match="not found in workspace"):
        store.create_session(
            workspace_id="ws-other-tenant",
            editorial_storyboard_id="STB-M0079-01",
            created_by="other-operator",
        )
